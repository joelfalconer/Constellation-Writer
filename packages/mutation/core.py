from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
import json
import os
import secrets
import tempfile
import time
import uuid

from packages.vault.core import safe_project_path, sha256_bytes, sha256_file


class MutationError(RuntimeError):
    pass


class StaleBaseError(MutationError):
    pass


class ControlledFailure(MutationError):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def typed_uuid7(prefix: str) -> str:
    ms = int(time.time() * 1000) & ((1 << 48) - 1)
    rand_a = secrets.randbits(12)
    rand_b = secrets.randbits(62)
    value = (ms << 80) | (0x7 << 76) | (rand_a << 64) | (0b10 << 62) | rand_b
    return f"{prefix}_{uuid.UUID(int=value)}"


def _fsync_directory(path: Path) -> None:
    if not hasattr(os, "O_DIRECTORY"):
        return
    try:
        fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    except OSError:
        return
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic_replace_bytes(
    path: Path,
    data: bytes,
    *,
    expected_sha256: str | None = None,
    failpoint: str | None = None,
) -> dict[str, Any]:
    """Replace one file through a same-directory temporary file.

    The replacement is atomic only to the extent guaranteed by the underlying
    filesystem for os.replace on the same filesystem. The directory is fsynced
    where the platform exposes a usable directory descriptor.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    before_exists = path.exists()
    before = path.read_bytes() if before_exists else b""
    before_hash = sha256_bytes(before) if before_exists else None
    if expected_sha256 is not None and before_hash != expected_sha256:
        raise StaleBaseError(
            f"stale base for {path}: expected {expected_sha256}, found {before_hash}"
        )

    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".cwtmp", dir=path.parent
    )
    temp_path = Path(temp_name)
    replaced = False
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        if failpoint == "after_temp_fsync":
            raise ControlledFailure("controlled failure after temp fsync")
        if before_exists:
            try:
                os.chmod(temp_path, path.stat().st_mode)
            except OSError:
                pass
        os.replace(temp_path, path)
        replaced = True
        _fsync_directory(path.parent)
        if failpoint == "after_replace":
            raise ControlledFailure("controlled failure after replace")
    finally:
        if not replaced and temp_path.exists():
            temp_path.unlink(missing_ok=True)

    return {
        "path": str(path),
        "before_sha256": before_hash,
        "after_sha256": sha256_bytes(data),
        "bytes": len(data),
        "atomic_boundary": "single_file_replace",
    }


def write_json_atomic(path: Path, value: Any) -> None:
    atomic_replace_bytes(
        path,
        (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8"),
    )


def _bundle_root(project_root: Path, op_id: str) -> Path:
    return safe_project_path(project_root, Path("recovery/bundles") / op_id)


def _write_bundle_manifest(bundle_root: Path, value: dict[str, Any]) -> None:
    write_json_atomic(bundle_root / "bundle.json", value)


def _load_bundle_manifest(bundle_root: Path) -> dict[str, Any]:
    return json.loads((bundle_root / "bundle.json").read_text(encoding="utf-8"))


def write_mutation_receipt(project_root: Path, receipt: dict[str, Any]) -> Path:
    op_id = receipt["operation_id"]
    path = safe_project_path(
        project_root, Path("mutations/receipts") / f"{op_id}.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    write_json_atomic(path, receipt)
    return path


def _prepare_single_file_bundle(
    project_root: Path,
    *,
    op_id: str,
    relative_path: str,
    object_id: str,
    object_type: str,
    before_exists: bool,
    before: bytes,
    after: bytes,
    intent: str,
) -> tuple[Path, dict[str, Any]]:
    root = _bundle_root(project_root, op_id)
    (root / "before").mkdir(parents=True, exist_ok=True)
    (root / "after").mkdir(parents=True, exist_ok=True)
    atomic_replace_bytes(root / "before/0000.bin", before)
    atomic_replace_bytes(root / "after/0000.bin", after)
    manifest = {
        "schema": "cw_recovery_bundle_v1",
        "kind": "single_file",
        "state": "prepared",
        "operation_id": op_id,
        "intent": intent,
        "created_at": now_iso(),
        "targets": [
            {
                "relative_path": relative_path,
                "object_id": object_id,
                "object_type": object_type,
                "before_exists": before_exists,
                "before_sha256": sha256_bytes(before) if before_exists else None,
                "after_sha256": sha256_bytes(after),
                "before_file": "before/0000.bin",
                "after_file": "after/0000.bin",
            }
        ],
    }
    _write_bundle_manifest(root, manifest)
    return root, manifest


def apply_text_mutation(
    project_root: Path,
    relative_path: str | Path,
    text: str,
    *,
    object_id: str,
    object_type: str,
    intent: str,
    expected_sha256: str | None,
    consequence: str = "canonical_low",
    source_kind: str = "human",
    actor_id: str = "local-user",
    failpoint: str | None = None,
    hard_exit_after_replace: bool = False,
) -> dict[str, Any]:
    """Apply one canonical text mutation with a durable recovery journal.

    A before/after recovery bundle is fully persisted before canonical
    replacement. If the process terminates after replacement but before receipt
    finalization, ``reconcile_incomplete_operations`` can classify the target by
    hash and finalize the intended write without guessing.
    """
    op_id = typed_uuid7("op")
    rel = Path(relative_path).as_posix()
    target = safe_project_path(project_root, rel)
    before_exists = target.exists()
    before = target.read_bytes() if before_exists else b""
    before_hash = sha256_bytes(before) if before_exists else None
    if expected_sha256 is not None and before_hash != expected_sha256:
        raise StaleBaseError(
            f"stale base for {rel}: expected {expected_sha256}, found {before_hash}"
        )
    after = text.encode("utf-8")
    bundle_root, bundle = _prepare_single_file_bundle(
        project_root,
        op_id=op_id,
        relative_path=rel,
        object_id=object_id,
        object_type=object_type,
        before_exists=before_exists,
        before=before,
        after=after,
        intent=intent,
    )
    receipt: dict[str, Any] = {
        "operation_id": op_id,
        "schema": "cw_mutation_receipt_v1",
        "source": {"kind": source_kind, "actor_id": actor_id},
        "intent": intent,
        "consequence": consequence,
        "target": {
            "object_id": object_id,
            "object_type": object_type,
            "path": rel,
        },
        "expected_base_sha256": expected_sha256,
        "recovery_bundle": bundle_root.relative_to(project_root).as_posix(),
        "started_at": now_iso(),
        "application": {"state": "applying"},
    }
    try:
        result = atomic_replace_bytes(
            target,
            after,
            expected_sha256=expected_sha256,
            failpoint=failpoint,
        )
        if hard_exit_after_replace:
            # Used only by subprocess failure-injection assays. The persisted
            # bundle is the restart witness for the now-unfinalized mutation.
            os._exit(86)
        receipt["application"] = {"state": "applied", **result}
        bundle["state"] = "applied"
        bundle["completed_at"] = now_iso()
        _write_bundle_manifest(bundle_root, bundle)
    except Exception as exc:
        current_hash = sha256_file(target) if target.exists() else None
        intended_hash = sha256_bytes(after)
        if current_hash == intended_hash:
            # A post-replacement exception means the canonical write happened;
            # report it as applied-with-finalization-error rather than lying
            # that the write failed.
            receipt["application"] = {
                "state": "applied_unconfirmed",
                "after_sha256": current_hash,
                "finalization_error": f"{type(exc).__name__}: {exc}",
            }
        else:
            receipt["application"] = {
                "state": "failed",
                "error": f"{type(exc).__name__}: {exc}",
            }
            bundle["state"] = "failed_before_apply"
            bundle["completed_at"] = now_iso()
            _write_bundle_manifest(bundle_root, bundle)
        receipt["completed_at"] = now_iso()
        write_mutation_receipt(project_root, receipt)
        raise
    receipt["completed_at"] = now_iso()
    receipt["receipt_path"] = str(
        write_mutation_receipt(project_root, receipt).relative_to(project_root)
    )
    return receipt


@dataclass(frozen=True)
class PlannedWrite:
    relative_path: str
    object_id: str
    object_type: str
    content: bytes
    expected_sha256: str | None


def apply_operation_plan(
    project_root: Path,
    writes: Iterable[PlannedWrite],
    *,
    intent: str,
    actor_id: str = "local-user",
    fail_after_applies: int | None = None,
    hard_exit_after_applies: int | None = None,
) -> dict[str, Any]:
    """Apply a recovery-backed multi-file plan without claiming atomicity.

    Before and intended-after images are persisted before any canonical write.
    A restart can therefore classify each target as before, after, or divergent.
    Mixed before/after state is rolled back by
    ``reconcile_incomplete_operations``.
    """
    op_id = typed_uuid7("op")
    plan = list(writes)
    bundle_root = _bundle_root(project_root, op_id)
    bundle_root.mkdir(parents=True, exist_ok=True)
    before_records: list[dict[str, Any]] = []

    for index, item in enumerate(plan):
        target = safe_project_path(project_root, item.relative_path)
        before_exists = target.exists()
        before = target.read_bytes() if before_exists else b""
        before_hash = sha256_bytes(before) if before_exists else None
        if item.expected_sha256 is not None and before_hash != item.expected_sha256:
            raise StaleBaseError(f"stale base for {item.relative_path}")
        before_file = bundle_root / "before" / f"{index:04d}.bin"
        after_file = bundle_root / "after" / f"{index:04d}.bin"
        before_file.parent.mkdir(parents=True, exist_ok=True)
        after_file.parent.mkdir(parents=True, exist_ok=True)
        atomic_replace_bytes(before_file, before)
        atomic_replace_bytes(after_file, item.content)
        before_records.append(
            {
                "relative_path": item.relative_path,
                "object_id": item.object_id,
                "object_type": item.object_type,
                "before_exists": before_exists,
                "before_sha256": before_hash,
                "after_sha256": sha256_bytes(item.content),
                "before_file": before_file.relative_to(bundle_root).as_posix(),
                "after_file": after_file.relative_to(bundle_root).as_posix(),
            }
        )

    bundle = {
        "schema": "cw_recovery_bundle_v1",
        "kind": "multi_file",
        "state": "prepared",
        "operation_id": op_id,
        "intent": intent,
        "created_at": now_iso(),
        "targets": before_records,
    }
    _write_bundle_manifest(bundle_root, bundle)

    receipt: dict[str, Any] = {
        "schema": "cw_mutation_receipt_v1",
        "operation_id": op_id,
        "intent": intent,
        "source": {"kind": "human", "actor_id": actor_id},
        "consequence": "canonical_high",
        "atomicity": "recovery_backed_multi_file",
        "recovery_bundle": bundle_root.relative_to(project_root).as_posix(),
        "started_at": now_iso(),
        "targets": [],
    }
    applied_indexes: list[int] = []
    try:
        for index, item in enumerate(plan):
            target = safe_project_path(project_root, item.relative_path)
            result = atomic_replace_bytes(
                target, item.content, expected_sha256=item.expected_sha256
            )
            receipt["targets"].append(
                {"index": index, "state": "applied", **result}
            )
            applied_indexes.append(index)
            if (
                hard_exit_after_applies is not None
                and len(applied_indexes) >= hard_exit_after_applies
            ):
                os._exit(87)
            if (
                fail_after_applies is not None
                and len(applied_indexes) >= fail_after_applies
            ):
                raise ControlledFailure(
                    f"controlled multi-file failure after {len(applied_indexes)} applies"
                )
        receipt["application_state"] = "applied"
        bundle["state"] = "applied"
        bundle["completed_at"] = now_iso()
        _write_bundle_manifest(bundle_root, bundle)
    except Exception as exc:
        receipt["failure"] = f"{type(exc).__name__}: {exc}"
        rollback_errors: list[str] = []
        for index in reversed(applied_indexes):
            item = plan[index]
            record = before_records[index]
            target = safe_project_path(project_root, item.relative_path)
            before = (bundle_root / record["before_file"]).read_bytes()
            try:
                if record["before_exists"]:
                    atomic_replace_bytes(target, before)
                else:
                    target.unlink(missing_ok=True)
                receipt["targets"].append({"index": index, "state": "restored"})
            except Exception as rollback_exc:
                rollback_errors.append(f"{item.relative_path}: {rollback_exc}")
        if rollback_errors:
            receipt["application_state"] = "failed_recovery_required"
            receipt["rollback_errors"] = rollback_errors
            bundle["state"] = "recovery_required"
        else:
            receipt["application_state"] = "failed_recovered"
            bundle["state"] = "failed_recovered"
        bundle["completed_at"] = now_iso()
        _write_bundle_manifest(bundle_root, bundle)
        receipt["completed_at"] = now_iso()
        write_mutation_receipt(project_root, receipt)
        raise

    receipt["completed_at"] = now_iso()
    receipt["receipt_path"] = str(
        write_mutation_receipt(project_root, receipt).relative_to(project_root)
    )
    return receipt


def _target_state(project_root: Path, record: dict[str, Any]) -> str:
    target = safe_project_path(project_root, record["relative_path"])
    if not target.exists():
        return "before" if not record["before_exists"] else "divergent"
    current = sha256_file(target)
    if current == record.get("after_sha256"):
        return "after"
    if current == record.get("before_sha256"):
        return "before"
    return "divergent"


def reconcile_incomplete_operations(project_root: Path) -> list[dict[str, Any]]:
    """Reconcile prepared recovery bundles left by abrupt termination.

    Single-file operations finalize if the target equals the persisted intended
    after-image. Mixed multi-file state is rolled back to every persisted
    before-image. Divergent state is never overwritten automatically.
    """
    bundles = safe_project_path(project_root, "recovery/bundles")
    results: list[dict[str, Any]] = []
    if not bundles.exists():
        return results
    for bundle_root in sorted(path for path in bundles.iterdir() if path.is_dir()):
        manifest_path = bundle_root / "bundle.json"
        if not manifest_path.is_file():
            continue
        manifest = _load_bundle_manifest(bundle_root)
        if manifest.get("state") != "prepared":
            continue
        states = [
            _target_state(project_root, record)
            for record in manifest.get("targets") or []
        ]
        result: dict[str, Any] = {
            "operation_id": manifest["operation_id"],
            "kind": manifest.get("kind"),
            "observed_states": states,
            "reconciled_at": now_iso(),
        }
        if any(state == "divergent" for state in states):
            manifest["state"] = "recovery_required"
            result["application_state"] = "recovery_required"
        elif manifest.get("kind") == "single_file":
            if states == ["after"]:
                manifest["state"] = "applied_recovered_after_crash"
                result["application_state"] = "applied_recovered_after_crash"
            else:
                manifest["state"] = "aborted_before_apply"
                result["application_state"] = "aborted_before_apply"
        elif states and all(state == "after" for state in states):
            manifest["state"] = "applied_recovered_after_crash"
            result["application_state"] = "applied_recovered_after_crash"
        elif states and all(state == "before" for state in states):
            manifest["state"] = "aborted_before_apply"
            result["application_state"] = "aborted_before_apply"
        else:
            rollback_errors: list[str] = []
            for record in reversed(manifest.get("targets") or []):
                target = safe_project_path(project_root, record["relative_path"])
                before = (bundle_root / record["before_file"]).read_bytes()
                try:
                    if record["before_exists"]:
                        atomic_replace_bytes(target, before)
                    else:
                        target.unlink(missing_ok=True)
                except Exception as exc:
                    rollback_errors.append(f"{record['relative_path']}: {exc}")
            if rollback_errors:
                manifest["state"] = "recovery_required"
                result["application_state"] = "recovery_required"
                result["rollback_errors"] = rollback_errors
            else:
                manifest["state"] = "failed_recovered_after_crash"
                result["application_state"] = "failed_recovered_after_crash"
        manifest["reconciled_at"] = result["reconciled_at"]
        _write_bundle_manifest(bundle_root, manifest)
        receipt = {
            "schema": "cw_mutation_receipt_v1",
            "operation_id": manifest["operation_id"],
            "intent": manifest.get("intent"),
            "source": {"kind": "recovery", "actor_id": "startup-reconciler"},
            "consequence": (
                "canonical_high"
                if manifest.get("kind") == "multi_file"
                else "canonical_low"
            ),
            "recovery_bundle": bundle_root.relative_to(project_root).as_posix(),
            **result,
            "completed_at": now_iso(),
        }
        receipt_path = write_mutation_receipt(project_root, receipt)
        result["receipt_path"] = receipt_path.relative_to(project_root).as_posix()
        results.append(result)
    return results


def move_canonical_file(
    project_root: Path,
    source_relative: str | Path,
    destination_relative: str | Path,
    *,
    object_id: str,
    object_type: str,
) -> dict[str, Any]:
    op_id = typed_uuid7("op")
    source = safe_project_path(project_root, source_relative)
    destination = safe_project_path(project_root, destination_relative)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not source.exists():
        raise MutationError(f"source does not exist: {source_relative}")
    if destination.exists():
        raise MutationError(f"destination already exists: {destination_relative}")
    before_hash = sha256_file(source)
    os.replace(source, destination)
    _fsync_directory(destination.parent)
    if source.parent != destination.parent:
        _fsync_directory(source.parent)
    receipt = {
        "schema": "cw_mutation_receipt_v1",
        "operation_id": op_id,
        "intent": "move canonical file without changing object identity",
        "consequence": "canonical_low",
        "target": {"object_id": object_id, "object_type": object_type},
        "application": {
            "state": "applied",
            "operation": "move",
            "source": Path(source_relative).as_posix(),
            "destination": Path(destination_relative).as_posix(),
            "sha256": before_hash,
        },
        "completed_at": now_iso(),
    }
    receipt["receipt_path"] = str(
        write_mutation_receipt(project_root, receipt).relative_to(project_root)
    )
    return receipt
