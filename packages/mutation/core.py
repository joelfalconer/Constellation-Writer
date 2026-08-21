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
    """Replace one file through a same-directory temp file and os.replace.

    This is the F2 single-file atomicity boundary. It is conditional on the
    underlying filesystem providing the expected os.replace semantics. A stale
    expected hash blocks application before the replacement begins.
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


def write_mutation_receipt(project_root: Path, receipt: dict[str, Any]) -> Path:
    op_id = receipt["operation_id"]
    path = safe_project_path(
        project_root, Path("mutations/receipts") / f"{op_id}.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    write_json_atomic(path, receipt)
    return path


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
) -> dict[str, Any]:
    op_id = typed_uuid7("op")
    target = safe_project_path(project_root, relative_path)
    receipt: dict[str, Any] = {
        "operation_id": op_id,
        "schema": "cw_mutation_receipt_v1",
        "source": {"kind": source_kind, "actor_id": actor_id},
        "intent": intent,
        "consequence": consequence,
        "target": {
            "object_id": object_id,
            "object_type": object_type,
            "path": Path(relative_path).as_posix(),
        },
        "expected_base_sha256": expected_sha256,
        "started_at": now_iso(),
        "application": {"state": "applying"},
    }
    try:
        result = atomic_replace_bytes(
            target,
            text.encode("utf-8"),
            expected_sha256=expected_sha256,
            failpoint=failpoint,
        )
        receipt["application"] = {"state": "applied", **result}
    except Exception as exc:
        receipt["application"] = {
            "state": "failed",
            "error": f"{type(exc).__name__}: {exc}",
        }
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
) -> dict[str, Any]:
    """Apply a recovery-backed multi-file plan.

    Every target's before-image is persisted to a recovery bundle before any
    canonical write. On failure, already-applied targets are restored from the
    bundle. The operation never claims cross-file atomicity.
    """
    op_id = typed_uuid7("op")
    plan = list(writes)
    bundle_root = safe_project_path(
        project_root, Path("recovery/bundles") / op_id
    )
    bundle_root.mkdir(parents=True, exist_ok=True)
    before_records: list[dict[str, Any]] = []

    for index, item in enumerate(plan):
        target = safe_project_path(project_root, item.relative_path)
        before_exists = target.exists()
        before = target.read_bytes() if before_exists else b""
        before_hash = sha256_bytes(before) if before_exists else None
        if item.expected_sha256 is not None and before_hash != item.expected_sha256:
            raise StaleBaseError(f"stale base for {item.relative_path}")
        bundle_file = bundle_root / "before" / f"{index:04d}.bin"
        bundle_file.parent.mkdir(parents=True, exist_ok=True)
        atomic_replace_bytes(bundle_file, before)
        before_records.append(
            {
                "relative_path": item.relative_path,
                "object_id": item.object_id,
                "object_type": item.object_type,
                "existed": before_exists,
                "sha256": before_hash,
                "bundle_file": bundle_file.relative_to(project_root).as_posix(),
            }
        )

    plan_manifest = {
        "schema": "cw_recovery_bundle_v1",
        "operation_id": op_id,
        "intent": intent,
        "created_at": now_iso(),
        "targets": before_records,
    }
    write_json_atomic(bundle_root / "bundle.json", plan_manifest)

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
                fail_after_applies is not None
                and len(applied_indexes) >= fail_after_applies
            ):
                raise ControlledFailure(
                    f"controlled multi-file failure after {len(applied_indexes)} applies"
                )
        receipt["application_state"] = "applied"
    except Exception as exc:
        receipt["failure"] = f"{type(exc).__name__}: {exc}"
        rollback_errors: list[str] = []
        for index in reversed(applied_indexes):
            item = plan[index]
            record = before_records[index]
            target = safe_project_path(project_root, item.relative_path)
            before = (project_root / record["bundle_file"]).read_bytes()
            try:
                if record["existed"]:
                    atomic_replace_bytes(target, before)
                else:
                    target.unlink(missing_ok=True)
                receipt["targets"].append({"index": index, "state": "restored"})
            except Exception as rollback_exc:
                rollback_errors.append(f"{item.relative_path}: {rollback_exc}")
        if rollback_errors:
            receipt["application_state"] = "failed_recovery_required"
            receipt["rollback_errors"] = rollback_errors
        else:
            receipt["application_state"] = "failed_recovered"
        receipt["completed_at"] = now_iso()
        write_mutation_receipt(project_root, receipt)
        raise

    receipt["completed_at"] = now_iso()
    receipt["receipt_path"] = str(
        write_mutation_receipt(project_root, receipt).relative_to(project_root)
    )
    return receipt


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
