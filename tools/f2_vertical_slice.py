#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any

REPO_IMPORT_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_IMPORT_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_IMPORT_ROOT))

from packages.catalog.core import build_catalog, catalog_digest, catalog_path, catalog_projection, delete_catalog
from packages.manuscript.core import load_manifest, ordered_sheet_ids, reorder_root_placement
from packages.mutation.core import (
    ControlledFailure,
    PlannedWrite,
    StaleBaseError,
    apply_operation_plan,
    apply_text_mutation,
    move_canonical_file,
)
from packages.recovery.core import (
    clear_recovery_buffer,
    create_snapshot,
    load_recovery_buffer,
    persist_recovery_buffer,
    preserve_conflict,
    restore_snapshot_file,
)
from packages.vault.core import find_sheet_by_id, load_sheet_with_sidecar, project_manifest, sha256_file


@dataclass
class Check:
    id: str
    passed: bool
    detail: Any


def run_command(repo_root: Path, command: list[str]) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=repo_root, text=True, capture_output=True, check=False)
    return {
        "command": command,
        "returncode": completed.returncode,
        "passed": completed.returncode == 0,
        "stdout_sha256": sha256(completed.stdout.encode()).hexdigest(),
        "stderr_sha256": sha256(completed.stderr.encode()).hexdigest(),
        "stdout_tail": completed.stdout[-6000:],
        "stderr_tail": completed.stderr[-6000:],
    }


def run_validator(repo_root: Path, fixture: Path, report: Path) -> dict[str, Any]:
    command = [
        sys.executable,
        "tools/validator/validate.py",
        "--repo",
        ".",
        "--fixture",
        str(fixture.relative_to(repo_root)),
        "--report",
        str(report.relative_to(repo_root)),
    ]
    result = run_command(repo_root, command)
    result["report"] = report.relative_to(repo_root).as_posix()
    return result


def run_substrate_matrix(repo_root: Path) -> dict[str, Any]:
    return run_command(
        repo_root,
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests/substrate",
            "-p",
            "test_*.py",
            "-v",
        ],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute F2 durable-substrate vertical slice")
    parser.add_argument("--source", default="fixtures/reference-novel")
    parser.add_argument("--workdir", default="build/f2-vertical-slice")
    parser.add_argument("--repo", default=".")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    source = (repo / args.source).resolve()
    workdir = (repo / args.workdir).resolve()
    project = workdir / "project"
    if workdir.exists():
        shutil.rmtree(workdir)
    workdir.mkdir(parents=True)
    shutil.copytree(source, project)

    checks: list[Check] = []

    substrate_matrix = run_substrate_matrix(repo)
    checks.append(Check("substrate_fault_matrix", substrate_matrix["passed"], substrate_matrix))

    validation_before = run_validator(repo, project, workdir / "validation-before.json")
    checks.append(Check("validator_before", validation_before["passed"], validation_before))

    project_data = project_manifest(project)
    sheet_id = "sh_018f0000-0000-7000-8000-000000000001"
    second_sheet_id = "sh_018f0000-0000-7000-8000-000000000002"
    sheet, sidecar_path, sidecar = load_sheet_with_sidecar(project, sheet_id)
    checks.append(
        Check(
            "sheet_and_sidecar_identity",
            sidecar["id"] == sheet.id,
            {"sheet": sheet.path.relative_to(project).as_posix(), "sidecar": sidecar_path.relative_to(project).as_posix()},
        )
    )

    edited = sheet.raw_text + "\nRecovered sentence from the F2 buffer.\n"
    buffer = persist_recovery_buffer(project, sheet_id, sheet.sha256, edited)
    recovered = load_recovery_buffer(project, sheet_id)
    checks.append(Check("recovery_buffer_roundtrip", recovered["content"] == edited, {"buffer": buffer["path"]}))
    save_receipt = apply_text_mutation(
        project,
        sheet.path.relative_to(project),
        recovered["content"],
        object_id=sheet_id,
        object_type="sheet",
        intent="persist recovered editor buffer",
        expected_sha256=sheet.sha256,
    )
    clear_recovery_buffer(project, sheet_id)
    checks.append(Check("guarded_sheet_save", find_sheet_by_id(project, sheet_id).raw_text == edited, {"operation_id": save_receipt["operation_id"]}))

    manifest_rel = Path("manuscripts/main.manuscript.yml")
    manifest_before = load_manifest(project, manifest_rel)
    order_before = ordered_sheet_ids(manifest_before)
    sheet_hashes_before = {sid: find_sheet_by_id(project, sid).sha256 for sid in order_before}
    second_placement = manifest_before["root_nodes"][1]["id"]
    reorder = reorder_root_placement(project, manifest_rel, second_placement, 0)
    order_after = ordered_sheet_ids(load_manifest(project, manifest_rel))
    sheet_hashes_after = {sid: find_sheet_by_id(project, sid).sha256 for sid in order_before}
    checks.append(Check("manifest_order_from_ids", order_after == list(reversed(order_before)), {"before": order_before, "after": order_after}))
    checks.append(Check("reorder_does_not_touch_prose", sheet_hashes_before == sheet_hashes_after, {"operation_id": reorder["operation"]["operation_id"]}))

    first_catalog = build_catalog(project)
    first_projection = catalog_projection(project)
    first_digest = catalog_digest(project)
    delete_catalog(project)
    checks.append(Check("catalog_delete", not catalog_path(project).exists(), {}))
    validation_after_delete = run_validator(repo, project, workdir / "validation-after-cache-delete.json")
    checks.append(Check("validator_after_cache_delete", validation_after_delete["passed"], validation_after_delete))
    second_catalog = build_catalog(project)
    second_projection = catalog_projection(project)
    second_digest = catalog_digest(project)
    checks.append(Check("catalog_rebuild_equivalence", first_projection == second_projection and first_digest == second_digest, {"first": first_catalog, "second": second_catalog}))
    catalog_path(project).write_bytes(b"corrupt sqlite bytes")
    repaired_catalog = build_catalog(project)
    checks.append(Check("corrupt_catalog_rebuild", catalog_projection(project) == first_projection, repaired_catalog))

    current_sheet = find_sheet_by_id(project, sheet_id)
    base_bytes = current_sheet.path.read_bytes()
    app_bytes = base_bytes + b"\nApplication-side unsaved line.\n"
    external_bytes = base_bytes + b"\nExternal editor line.\n"
    current_sheet.path.write_bytes(external_bytes)
    conflict = preserve_conflict(
        project,
        object_type="sheet",
        object_id=sheet_id,
        relative_path=current_sheet.path.relative_to(project),
        base_bytes=base_bytes,
        app_bytes=app_bytes,
        external_bytes=external_bytes,
    )
    checks.append(Check("external_conflict_preserves_all_versions", bool(conflict and conflict["zero_loss"]), conflict or {}))

    second_sheet = find_sheet_by_id(project, second_sheet_id)
    second_rel = second_sheet.path.relative_to(project)
    snapshot = create_snapshot(project, "F2 named Sheet snapshot", [second_rel], object_ids={second_rel.as_posix(): second_sheet_id})
    before_snapshot_hash = second_sheet.sha256
    apply_text_mutation(
        project,
        second_rel,
        second_sheet.raw_text + "\nTemporary mutation to be restored.\n",
        object_id=second_sheet_id,
        object_type="sheet",
        intent="temporary snapshot restore assay mutation",
        expected_sha256=before_snapshot_hash,
    )
    restore = restore_snapshot_file(project, snapshot["snapshot_root"], second_rel, object_id=second_sheet_id)
    checks.append(Check("named_snapshot_restore", find_sheet_by_id(project, second_sheet_id).sha256 == before_snapshot_hash, restore))

    first_after_conflict = find_sheet_by_id(project, sheet_id)
    old_rel = first_after_conflict.path.relative_to(project)
    new_rel = Path("sheets/moved") / first_after_conflict.path.name.replace("opening-scene", "opening-scene-moved")
    move_receipt = move_canonical_file(project, old_rel, new_rel, object_id=sheet_id, object_type="sheet")
    moved = find_sheet_by_id(project, sheet_id)
    checks.append(Check("rename_move_preserves_sheet_identity", moved.id == sheet_id and moved.path.relative_to(project) == new_rel, move_receipt))

    failure_rel = Path("materials/f2-failure.txt")
    failure_path = project / failure_rel
    failure_path.parent.mkdir(parents=True, exist_ok=True)
    failure_path.write_text("before\n", encoding="utf-8")
    failure_hash = sha256_file(failure_path)
    failure_states: dict[str, bool] = {}
    for failpoint in ("after_temp_fsync", "permission_error_before_commit", "disk_full_before_commit"):
        try:
            apply_text_mutation(
                project,
                failure_rel,
                "after\n",
                object_id=project_data["id"],
                object_type="project_material",
                intent=f"controlled {failpoint}",
                expected_sha256=failure_hash,
                failpoint=failpoint,
            )
        except (ControlledFailure, OSError):
            pass
        failure_states[failpoint] = sha256_file(failure_path) == failure_hash
    checks.append(Check("precommit_failure_matrix_preserves_old_bytes", all(failure_states.values()), failure_states))

    post_receipt = apply_text_mutation(
        project,
        failure_rel,
        "committed-after-failure\n",
        object_id=project_data["id"],
        object_type="project_material",
        intent="post-commit outcome assay",
        expected_sha256=failure_hash,
        failpoint="after_replace",
    )
    checks.append(
        Check(
            "postcommit_failure_not_misreported_failed",
            post_receipt["application"]["state"] == "applied_unconfirmed" and failure_path.read_text() == "committed-after-failure\n",
            post_receipt["application"],
        )
    )

    race_base = sha256_file(failure_path)
    external_race = b"external-race-wins\n"
    def race_hook(path: Path) -> None:
        path.write_bytes(external_race)
    race_blocked = False
    try:
        apply_text_mutation(
            project,
            failure_rel,
            "application-race\n",
            object_id=project_data["id"],
            object_type="project_material",
            intent="stale-base commit race assay",
            expected_sha256=race_base,
            _precommit_hook=race_hook,
        )
    except StaleBaseError:
        race_blocked = failure_path.read_bytes() == external_race
    checks.append(Check("stale_base_race_preserves_external_version", race_blocked, {}))

    a_rel = Path("materials/f2-multi-a.txt")
    b_rel = Path("materials/f2-multi-b.txt")
    for rel, text in ((a_rel, "a-before\n"), (b_rel, "b-before\n")):
        path = project / rel
        path.write_text(text, encoding="utf-8")
    a_before = sha256_file(project / a_rel)
    b_before = sha256_file(project / b_rel)
    try:
        apply_operation_plan(
            project,
            [
                PlannedWrite(a_rel.as_posix(), project_data["id"], "project_material", b"a-after\n", a_before),
                PlannedWrite(b_rel.as_posix(), project_data["id"], "project_material", b"b-after\n", b_before),
            ],
            intent="controlled recovery-backed multi-file failure assay",
            fail_after_applies=1,
        )
    except ControlledFailure:
        pass
    checks.append(Check("multi_file_failure_rolls_back_applied_target", sha256_file(project / a_rel) == a_before and sha256_file(project / b_rel) == b_before, {}))

    validation_after = run_validator(repo, project, workdir / "validation-after.json")
    checks.append(Check("validator_after_vertical_slice", validation_after["passed"], validation_after))

    passed = all(item.passed for item in checks)
    hard_gates = {
        "zero_silent_loss": bool(conflict and conflict["zero_loss"]) and race_blocked,
        "no_sqlite_only_durable_field": first_projection == second_projection and catalog_projection(project) == first_projection,
        "rename_move_preserves_sheet_identity": moved.id == sheet_id,
        "recovery_and_conflict_receipts": bool(conflict and conflict.get("receipt_path") and restore.get("receipt_path")),
        "validator_before_and_after_cache_delete": validation_before["passed"] and validation_after_delete["passed"],
        "controlled_failure_matrix": substrate_matrix["passed"] and all(failure_states.values()),
        "postcommit_outcome_semantics": post_receipt["application"]["state"] == "applied_unconfirmed",
        "corrupt_sqlite_rebuild": catalog_projection(project) == first_projection,
    }
    receipt = {
        "schema": "cw_f2_vertical_slice_receipt_v2",
        "issue": 6,
        "project_id": project_data["id"],
        "source_fixture": args.source,
        "working_copy": project.relative_to(repo).as_posix(),
        "checks": [asdict(item) for item in checks],
        "vertical_slice_state": "passed" if passed else "failed",
        "f2_gate_state": "awaiting_full_local_validation_and_explicit_gate_decision",
        "hard_gates": hard_gates,
        "notes": [
            "This receipt proves the vertical-slice command only when executed from a complete repository checkout.",
            "It does not by itself approve F2; tools/local_validate.py --suite all remains the full local proof contract.",
            "Hosted GitHub Actions availability is not part of this result.",
        ],
    }
    receipt_path = workdir / "F2_VERTICAL_SLICE_RECEIPT.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    print(f"\nReceipt: {receipt_path}")
    return 0 if passed and all(hard_gates.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
