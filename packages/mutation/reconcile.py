from __future__ import annotations

from pathlib import Path
from typing import Any
import os

from .atomic import MutationError, _fsync_directory, atomic_replace_bytes, now_iso, typed_uuid7
from .operations import (
    _load_bundle_manifest, _preserve_divergent, _restore_record_if_unchanged,
    _write_bundle_manifest, write_mutation_receipt,
)
from packages.vault.core import safe_project_path, sha256_file

def _target_state(project_root: Path, record: dict[str, Any]) -> str:
    target = safe_project_path(project_root, record["relative_path"])
    if not target.exists():
        return "before" if not record["before_exists"] else "divergent"
    current = sha256_file(target)
    if current == record.get("after_sha256"): return "after"
    if current == record.get("before_sha256"): return "before"
    return "divergent"


def reconcile_incomplete_operations(project_root: Path) -> list[dict[str, Any]]:
    bundles = safe_project_path(project_root, "recovery/bundles")
    results: list[dict[str, Any]] = []
    if not bundles.exists(): return results
    for bundle_root in sorted(path for path in bundles.iterdir() if path.is_dir()):
        manifest_path = bundle_root / "bundle.json"
        if not manifest_path.is_file(): continue
        manifest = _load_bundle_manifest(bundle_root)
        late = []
        for index, record in enumerate(manifest.get("targets") or []):
            displaced_rel = record.get("displaced_file")
            if displaced_rel:
                displaced = bundle_root / displaced_rel
                if displaced.exists() and record.get("before_sha256") and sha256_file(displaced) != record.get("before_sha256"):
                    late.append({"index": index, "file": displaced_rel, "sha256": sha256_file(displaced)})
        if late and manifest.get("state") in {"applied", "applied_unconfirmed"}:
            manifest["state"] = "applied_with_late_external_conflict"
            result = {"operation_id": manifest["operation_id"], "kind": manifest.get("kind"),
                      "application_state": "applied_with_late_external_conflict", "late_external_versions": late,
                      "reconciled_at": now_iso()}
            _write_bundle_manifest(bundle_root, manifest)
            result["receipt_path"] = write_mutation_receipt(project_root, {"schema": "cw_mutation_receipt_v1", **result, "completed_at": now_iso()}).relative_to(project_root).as_posix()
            results.append(result)
            continue
        if manifest.get("state") not in {"prepared", "applied_unconfirmed"}: continue
        states = [_target_state(project_root, record) for record in manifest.get("targets") or []]
        result: dict[str, Any] = {"operation_id": manifest["operation_id"], "kind": manifest.get("kind"), "observed_states": states, "reconciled_at": now_iso()}
        if any(state == "divergent" for state in states):
            for index, (state, record) in enumerate(zip(states, manifest.get("targets") or [])):
                if state == "divergent":
                    target = safe_project_path(project_root, record["relative_path"])
                    if target.exists(): record["divergent_file"] = _preserve_divergent(bundle_root, index, target.read_bytes())
            manifest["state"] = "recovery_required"; result["application_state"] = "recovery_required"
        elif manifest.get("kind") == "single_file":
            if states == ["after"]: manifest["state"] = "applied_recovered_after_crash"; result["application_state"] = "applied_recovered_after_crash"
            else: manifest["state"] = "aborted_before_apply"; result["application_state"] = "aborted_before_apply"
        elif states and all(state == "after" for state in states):
            manifest["state"] = "applied_recovered_after_crash"; result["application_state"] = "applied_recovered_after_crash"
        elif states and all(state == "before" for state in states):
            manifest["state"] = "aborted_before_apply"; result["application_state"] = "aborted_before_apply"
        else:
            rollback_errors: list[str] = []
            for index, record in reversed(list(enumerate(manifest.get("targets") or []))):
                ok, detail = _restore_record_if_unchanged(project_root, bundle_root, record, index)
                if not ok: rollback_errors.append(f"{record['relative_path']}: {detail}")
            if rollback_errors:
                manifest["state"] = "recovery_required"; result["application_state"] = "recovery_required"; result["rollback_errors"] = rollback_errors
            else:
                manifest["state"] = "failed_recovered_after_crash"; result["application_state"] = "failed_recovered_after_crash"
        manifest["reconciled_at"] = result["reconciled_at"]; _write_bundle_manifest(bundle_root, manifest)
        receipt = {"schema": "cw_mutation_receipt_v1", "operation_id": manifest["operation_id"], "intent": manifest.get("intent"),
                   "source": {"kind": "recovery", "actor_id": "startup-reconciler"},
                   "consequence": "canonical_high" if manifest.get("kind") == "multi_file" else "canonical_low",
                   "recovery_bundle": bundle_root.relative_to(project_root).as_posix(), **result, "completed_at": now_iso()}
        result["receipt_path"] = write_mutation_receipt(project_root, receipt).relative_to(project_root).as_posix(); results.append(result)
    return results


def move_canonical_file(project_root: Path, source_relative: str | Path, destination_relative: str | Path, *, object_id: str, object_type: str) -> dict[str, Any]:
    op_id = typed_uuid7("op")
    source = safe_project_path(project_root, source_relative); destination = safe_project_path(project_root, destination_relative)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not source.exists(): raise MutationError(f"source does not exist: {source_relative}")
    if source.is_symlink(): raise MutationError(f"source may not be symlink: {source_relative}")
    before_hash = sha256_file(source)
    try:
        os.link(source, destination, follow_symlinks=False)
    except FileExistsError as exc:
        raise MutationError(f"destination already exists: {destination_relative}") from exc
    except OSError as exc:
        raise MutationError(f"no-clobber canonical move unsupported or failed: {exc}") from exc
    _fsync_directory(destination.parent)
    source.unlink()
    _fsync_directory(source.parent)
    receipt = {"schema": "cw_mutation_receipt_v1", "operation_id": op_id, "intent": "move canonical file without changing object identity",
               "consequence": "canonical_low", "target": {"object_id": object_id, "object_type": object_type},
               "application": {"state": "applied", "operation": "move_no_clobber", "source": Path(source_relative).as_posix(),
                               "destination": Path(destination_relative).as_posix(), "sha256": before_hash}, "completed_at": now_iso()}
    receipt["receipt_path"] = str(write_mutation_receipt(project_root, receipt).relative_to(project_root)); return receipt
