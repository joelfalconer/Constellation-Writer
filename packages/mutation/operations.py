from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable
import json
import os

from .atomic import (
    ControlledFailure, MutationError, PostCommitError, StaleBaseError,
    _fsync_directory, atomic_replace_bytes, now_iso, typed_uuid7, write_json_atomic,
)
from packages.vault.core import safe_project_path, sha256_bytes, sha256_file

def _bundle_root(project_root: Path, op_id: str) -> Path:
    return safe_project_path(project_root, Path("recovery/bundles") / op_id)


def _write_bundle_manifest(bundle_root: Path, value: dict[str, Any]) -> None:
    write_json_atomic(bundle_root / "bundle.json", value)


def _load_bundle_manifest(bundle_root: Path) -> dict[str, Any]:
    return json.loads((bundle_root / "bundle.json").read_text(encoding="utf-8"))


def write_mutation_receipt(project_root: Path, receipt: dict[str, Any]) -> Path:
    op_id = receipt["operation_id"]
    path = safe_project_path(project_root, Path("mutations/receipts") / f"{op_id}.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    write_json_atomic(path, receipt)
    return path


def _prepare_single_file_bundle(project_root: Path, *, op_id: str, relative_path: str, object_id: str, object_type: str, before_exists: bool, before: bytes, after: bytes, intent: str) -> tuple[Path, dict[str, Any]]:
    root = _bundle_root(project_root, op_id)
    (root / "before").mkdir(parents=True, exist_ok=True)
    (root / "after").mkdir(parents=True, exist_ok=True)
    atomic_replace_bytes(root / "before/0000.bin", before)
    atomic_replace_bytes(root / "after/0000.bin", after)
    manifest = {
        "schema": "cw_recovery_bundle_v1", "kind": "single_file", "state": "prepared",
        "operation_id": op_id, "intent": intent, "created_at": now_iso(),
        "targets": [{"relative_path": relative_path, "object_id": object_id, "object_type": object_type,
                     "before_exists": before_exists, "before_sha256": sha256_bytes(before) if before_exists else None,
                     "after_sha256": sha256_bytes(after), "before_file": "before/0000.bin", "after_file": "after/0000.bin"}],
    }
    _write_bundle_manifest(root, manifest)
    return root, manifest


def _preserve_divergent(bundle_root: Path, index: int, data: bytes) -> str:
    path = bundle_root / "divergent" / f"{index:04d}.bin"
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_replace_bytes(path, data)
    return path.relative_to(bundle_root).as_posix()


def apply_text_mutation(project_root: Path, relative_path: str | Path, text: str, *, object_id: str, object_type: str,
                        intent: str, expected_sha256: str | None, consequence: str = "canonical_low",
                        source_kind: str = "human", actor_id: str = "local-user", failpoint: str | None = None,
                        hard_exit_after_replace: bool = False, _precommit_hook: Callable[[Path], None] | None = None) -> dict[str, Any]:
    op_id = typed_uuid7("op")
    rel = Path(relative_path).as_posix()
    target = safe_project_path(project_root, rel)
    before_exists = target.exists()
    before = target.read_bytes() if before_exists else b""
    before_hash = sha256_bytes(before) if before_exists else None
    if expected_sha256 is not None and before_hash != expected_sha256:
        raise StaleBaseError(f"stale base for {rel}: expected {expected_sha256}, found {before_hash}")
    after = text.encode("utf-8")
    bundle_root, bundle = _prepare_single_file_bundle(project_root, op_id=op_id, relative_path=rel, object_id=object_id,
                                                       object_type=object_type, before_exists=before_exists, before=before,
                                                       after=after, intent=intent)
    displaced = bundle_root / "displaced/0000.bin"
    displaced.parent.mkdir(parents=True, exist_ok=True)
    receipt: dict[str, Any] = {
        "operation_id": op_id, "schema": "cw_mutation_receipt_v1", "source": {"kind": source_kind, "actor_id": actor_id},
        "intent": intent, "consequence": consequence,
        "target": {"object_id": object_id, "object_type": object_type, "path": rel},
        "expected_base_sha256": expected_sha256, "recovery_bundle": bundle_root.relative_to(project_root).as_posix(),
        "started_at": now_iso(), "application": {"state": "applying"},
    }
    try:
        result = atomic_replace_bytes(target, after, expected_sha256=expected_sha256,
                                      displaced_backup=displaced if expected_sha256 is not None else None,
                                      failpoint=failpoint, _precommit_hook=_precommit_hook)
        if expected_sha256 is not None and displaced.exists():
            bundle["targets"][0]["displaced_file"] = displaced.relative_to(bundle_root).as_posix()
        if hard_exit_after_replace:
            os._exit(86)
        receipt["application"] = {"state": "applied", **result}
        bundle["state"] = "applied"
        bundle["completed_at"] = now_iso()
        _write_bundle_manifest(bundle_root, bundle)
    except PostCommitError as exc:
        current_hash = sha256_file(target) if target.exists() else None
        intended_hash = sha256_bytes(after)
        if expected_sha256 is not None and displaced.exists():
            bundle["targets"][0]["displaced_file"] = displaced.relative_to(bundle_root).as_posix()
        receipt["application"] = {"state": "applied_unconfirmed", "after_sha256": current_hash,
                                  "intended_sha256": intended_hash, "finalization_error": f"{type(exc).__name__}: {exc}"}
        bundle["state"] = "applied_unconfirmed" if current_hash == intended_hash else "recovery_required"
        bundle["completed_at"] = now_iso()
        _write_bundle_manifest(bundle_root, bundle)
        receipt["completed_at"] = now_iso()
        receipt["receipt_path"] = str(write_mutation_receipt(project_root, receipt).relative_to(project_root))
        return receipt
    except Exception as exc:
        receipt["application"] = {"state": "failed", "error": f"{type(exc).__name__}: {exc}"}
        bundle["state"] = "failed_before_apply"
        bundle["completed_at"] = now_iso()
        _write_bundle_manifest(bundle_root, bundle)
        receipt["completed_at"] = now_iso()
        write_mutation_receipt(project_root, receipt)
        raise
    receipt["completed_at"] = now_iso()
    receipt["receipt_path"] = str(write_mutation_receipt(project_root, receipt).relative_to(project_root))
    return receipt


@dataclass(frozen=True)
class PlannedWrite:
    relative_path: str
    object_id: str
    object_type: str
    content: bytes
    expected_sha256: str | None


def _restore_record_if_unchanged(project_root: Path, bundle_root: Path, record: dict[str, Any], index: int) -> tuple[bool, str | None]:
    target = safe_project_path(project_root, record["relative_path"])
    current = target.read_bytes() if target.exists() else b""
    current_hash = sha256_bytes(current) if target.exists() else None
    if current_hash == record.get("before_sha256") or (not record["before_exists"] and not target.exists()):
        return True, None
    if current_hash != record.get("after_sha256"):
        divergent = _preserve_divergent(bundle_root, index, current)
        return False, f"divergent target preserved at {divergent}"
    before = (bundle_root / record["before_file"]).read_bytes()
    if record["before_exists"]:
        atomic_replace_bytes(target, before, expected_sha256=record["after_sha256"],
                             displaced_backup=bundle_root / "rollback-displaced" / f"{index:04d}.bin")
    else:
        target.unlink(missing_ok=True)
    return True, None


def apply_operation_plan(project_root: Path, writes: Iterable[PlannedWrite], *, intent: str, actor_id: str = "local-user",
                         fail_after_applies: int | None = None, hard_exit_after_applies: int | None = None,
                         _before_rollback_hook: Callable[[Path, list[int]], None] | None = None) -> dict[str, Any]:
    op_id = typed_uuid7("op")
    plan = list(writes)
    bundle_root = _bundle_root(project_root, op_id)
    bundle_root.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    for index, item in enumerate(plan):
        target = safe_project_path(project_root, item.relative_path)
        before_exists = target.exists()
        before = target.read_bytes() if before_exists else b""
        before_hash = sha256_bytes(before) if before_exists else None
        if item.expected_sha256 is not None and before_hash != item.expected_sha256:
            raise StaleBaseError(f"stale base for {item.relative_path}")
        before_file = bundle_root / "before" / f"{index:04d}.bin"
        after_file = bundle_root / "after" / f"{index:04d}.bin"
        before_file.parent.mkdir(parents=True, exist_ok=True); after_file.parent.mkdir(parents=True, exist_ok=True)
        atomic_replace_bytes(before_file, before); atomic_replace_bytes(after_file, item.content)
        records.append({"relative_path": item.relative_path, "object_id": item.object_id, "object_type": item.object_type,
                        "before_exists": before_exists, "before_sha256": before_hash, "after_sha256": sha256_bytes(item.content),
                        "before_file": before_file.relative_to(bundle_root).as_posix(), "after_file": after_file.relative_to(bundle_root).as_posix(),
                        "state": "prepared"})
    bundle = {"schema": "cw_recovery_bundle_v1", "kind": "multi_file", "state": "prepared", "operation_id": op_id,
              "intent": intent, "created_at": now_iso(), "targets": records}
    _write_bundle_manifest(bundle_root, bundle)
    receipt: dict[str, Any] = {"schema": "cw_mutation_receipt_v1", "operation_id": op_id, "intent": intent,
                               "source": {"kind": "human", "actor_id": actor_id}, "consequence": "canonical_high",
                               "atomicity": "recovery_backed_multi_file", "recovery_bundle": bundle_root.relative_to(project_root).as_posix(),
                               "started_at": now_iso(), "targets": []}
    applied: list[int] = []
    try:
        for index, item in enumerate(plan):
            target = safe_project_path(project_root, item.relative_path)
            displaced = bundle_root / "displaced" / f"{index:04d}.bin"
            displaced.parent.mkdir(parents=True, exist_ok=True)
            result = atomic_replace_bytes(target, item.content, expected_sha256=item.expected_sha256, displaced_backup=displaced)
            records[index]["state"] = "applied"
            records[index]["displaced_file"] = displaced.relative_to(bundle_root).as_posix()
            bundle["last_applied_index"] = index
            _write_bundle_manifest(bundle_root, bundle)
            receipt["targets"].append({"index": index, "state": "applied", **result})
            applied.append(index)
            if hard_exit_after_applies is not None and len(applied) >= hard_exit_after_applies:
                os._exit(87)
            if fail_after_applies is not None and len(applied) >= fail_after_applies:
                raise ControlledFailure(f"controlled multi-file failure after {len(applied)} applies")
        receipt["application_state"] = "applied"; bundle["state"] = "applied"; bundle["completed_at"] = now_iso(); _write_bundle_manifest(bundle_root, bundle)
    except Exception as exc:
        receipt["failure"] = f"{type(exc).__name__}: {exc}"
        if _before_rollback_hook:
            _before_rollback_hook(project_root, list(applied))
        rollback_errors: list[str] = []
        for index in reversed(applied):
            ok, detail = _restore_record_if_unchanged(project_root, bundle_root, records[index], index)
            if ok:
                records[index]["state"] = "restored"
                receipt["targets"].append({"index": index, "state": "restored"})
            else:
                records[index]["state"] = "divergent_preserved"
                rollback_errors.append(f"{records[index]['relative_path']}: {detail}")
        if rollback_errors:
            receipt["application_state"] = "failed_recovery_required"; receipt["rollback_errors"] = rollback_errors; bundle["state"] = "recovery_required"
        else:
            receipt["application_state"] = "failed_recovered"; bundle["state"] = "failed_recovered"
        bundle["completed_at"] = now_iso(); _write_bundle_manifest(bundle_root, bundle)
        receipt["completed_at"] = now_iso(); write_mutation_receipt(project_root, receipt); raise
    receipt["completed_at"] = now_iso(); receipt["receipt_path"] = str(write_mutation_receipt(project_root, receipt).relative_to(project_root)); return receipt
