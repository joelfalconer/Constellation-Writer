from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable
import json
import shutil

from packages.mutation.core import apply_text_mutation, atomic_replace_bytes, now_iso, typed_uuid7, write_json_atomic
from packages.vault.core import canonical_file, dump_yaml, load_yaml, project_manifest, safe_project_path, sha256_bytes, sha256_file


class RecoveryError(RuntimeError):
    pass


def _slug(value: str) -> str:
    cleaned = "-".join(part for part in value.lower().replace("_", "-").split() if part)
    return "".join(ch for ch in cleaned if ch.isalnum() or ch in "-.")[:64] or "snapshot"


def recovery_buffer_path(project_root: Path, sheet_id: str) -> Path:
    return safe_project_path(project_root, Path("recovery/buffers") / f"{sheet_id}.buffer.json")


def persist_recovery_buffer(project_root: Path, sheet_id: str, base_sha256: str, content: str) -> dict[str, Any]:
    value = {"schema": "cw_recovery_buffer_v1", "sheet_id": sheet_id, "base_sha256": base_sha256,
             "content_sha256": sha256_bytes(content.encode("utf-8")), "created_at": now_iso(), "content": content}
    path = recovery_buffer_path(project_root, sheet_id); path.parent.mkdir(parents=True, exist_ok=True); write_json_atomic(path, value)
    return {"path": path.relative_to(project_root).as_posix(), **value}


def load_recovery_buffer(project_root: Path, sheet_id: str) -> dict[str, Any]:
    path = recovery_buffer_path(project_root, sheet_id)
    if not path.exists(): raise RecoveryError(f"no recovery buffer for {sheet_id}")
    value = json.loads(path.read_text(encoding="utf-8")); actual = sha256_bytes(value["content"].encode("utf-8"))
    if actual != value.get("content_sha256"): raise RecoveryError(f"recovery buffer checksum mismatch for {sheet_id}")
    return value


def clear_recovery_buffer(project_root: Path, sheet_id: str) -> None:
    recovery_buffer_path(project_root, sheet_id).unlink(missing_ok=True)


def create_snapshot(project_root: Path, name: str, relative_paths: Iterable[str | Path], *, snapshot_type: str = "manual_named", scope: str = "object", object_ids: dict[str, str] | None = None) -> dict[str, Any]:
    project = project_manifest(project_root); snapshot_id = typed_uuid7("snap")
    snapshot_root = safe_project_path(project_root, Path("snapshots") / f"{snapshot_id}-{_slug(name)}")
    files_root = snapshot_root / "files"; files_root.mkdir(parents=True, exist_ok=True)
    included: list[dict[str, Any]] = []; object_ids = object_ids or {}
    for relative in relative_paths:
        rel = Path(relative); source = canonical_file(project_root, rel)
        destination = safe_project_path(project_root, files_root / rel)
        destination.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(source, destination)
        included.append({"path": rel.as_posix(), "object_id": object_ids.get(rel.as_posix()), "sha256": sha256_file(source)})
    manifest = {"id": snapshot_id, "schema_version": "0.1.0", "project_id": project["id"], "type": snapshot_type,
                "scope": scope, "created_at": now_iso(), "name": name, "included_files": included}
    atomic_replace_bytes(snapshot_root / "snapshot.yml", dump_yaml(manifest).encode("utf-8"))
    return {"snapshot_id": snapshot_id, "snapshot_root": snapshot_root, "manifest": manifest}


def restore_snapshot_file(project_root: Path, snapshot_root: Path, relative_path: str | Path, *, object_id: str, object_type: str = "sheet") -> dict[str, Any]:
    project = project_manifest(project_root)
    root = safe_project_path(project_root, snapshot_root)
    manifest_path = canonical_file(project_root, root / "snapshot.yml")
    manifest = load_yaml(manifest_path)
    if not isinstance(manifest, dict) or manifest.get("project_id") != project.get("id"):
        raise RecoveryError("snapshot project identity does not match current project")
    rel = Path(relative_path)
    matches = [record for record in manifest.get("included_files", []) if record.get("path") == rel.as_posix()]
    if len(matches) != 1: raise RecoveryError(f"snapshot manifest does not uniquely contain {rel}")
    record = matches[0]
    if record.get("object_id") not in (None, object_id): raise RecoveryError("snapshot object identity mismatch")
    source = canonical_file(project_root, root / "files" / rel)
    actual_snapshot_hash = sha256_file(source)
    if actual_snapshot_hash != record.get("sha256"):
        raise RecoveryError(f"snapshot checksum mismatch for {rel}")
    snapshot_text = source.read_text(encoding="utf-8")
    target = safe_project_path(project_root, rel); current_hash = sha256_file(target) if target.exists() else None
    pre = create_snapshot(project_root, f"pre-restore-{object_id}", [rel], snapshot_type="pre_destructive_operation", scope="object", object_ids={rel.as_posix(): object_id}) if target.exists() else None
    receipt = apply_text_mutation(project_root, rel, snapshot_text, object_id=object_id, object_type=object_type,
                                  intent="restore one file from named snapshot", expected_sha256=current_hash,
                                  consequence="destructive", source_kind="recovery")
    if sha256_file(target) != record["sha256"]: raise RecoveryError("restored file does not match snapshot manifest checksum")
    result = {"schema": "cw_restore_receipt_v1", "restored_path": rel.as_posix(), "object_id": object_id,
              "source_snapshot": root.relative_to(project_root).as_posix(),
              "pre_restore_snapshot": pre["snapshot_root"].relative_to(project_root).as_posix() if pre else None,
              "mutation_operation_id": receipt["operation_id"], "restored_sha256": record["sha256"], "completed_at": now_iso()}
    receipt_path = safe_project_path(project_root, Path("recovery/receipts") / f"restore-{receipt['operation_id']}.json")
    receipt_path.parent.mkdir(parents=True, exist_ok=True); write_json_atomic(receipt_path, result); result["receipt_path"] = receipt_path.relative_to(project_root).as_posix(); return result


def preserve_conflict(project_root: Path, *, object_type: str, object_id: str, relative_path: str | Path, base_bytes: bytes, app_bytes: bytes, external_bytes: bytes) -> dict[str, Any] | None:
    base_hash = sha256_bytes(base_bytes); app_hash = sha256_bytes(app_bytes); external_hash = sha256_bytes(external_bytes)
    if external_hash == base_hash or external_hash == app_hash: return None
    conflict_id = typed_uuid7("cf"); root = safe_project_path(project_root, Path("recovery/conflicts") / conflict_id); versions = root / "versions"; versions.mkdir(parents=True, exist_ok=True)
    paths: dict[str, str] = {}
    for name, data in (("base", base_bytes), ("current_app", app_bytes), ("external", external_bytes)):
        path = versions / f"{name}.bin"; atomic_replace_bytes(path, data); paths[name] = path.relative_to(project_root).as_posix()
    manifest = {"id": conflict_id, "schema_version": "0.1.0", "object_type": object_type, "object_id": object_id,
                "path": Path(relative_path).as_posix(), "created_at": now_iso(),
                "base": {"sha256": base_hash, "file": paths["base"]},
                "current_app_version": {"sha256": app_hash, "file": paths["current_app"]},
                "external_version": {"sha256": external_hash, "file": paths["external"]},
                "status": "unresolved", "resolution": None}
    atomic_replace_bytes(root / "conflict.yml", dump_yaml(manifest).encode("utf-8"))
    receipt = {"schema": "cw_conflict_receipt_v1", "conflict_id": conflict_id, "path": Path(relative_path).as_posix(),
               "preserved": paths, "zero_loss": all((project_root / path).exists() for path in paths.values()), "created_at": now_iso()}
    receipt_path = safe_project_path(project_root, Path("recovery/receipts") / f"{conflict_id}.json"); receipt_path.parent.mkdir(parents=True, exist_ok=True); write_json_atomic(receipt_path, receipt)
    receipt["receipt_path"] = receipt_path.relative_to(project_root).as_posix(); receipt["manifest_path"] = (root / "conflict.yml").relative_to(project_root).as_posix(); return receipt
