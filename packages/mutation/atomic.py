from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable
import ctypes
import errno
import json
import os
import secrets
import sys
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


class PostCommitError(MutationError):
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


def _atomic_exchange(left: Path, right: Path) -> None:
    """Atomically exchange two existing filesystem names on supported targets."""
    if sys.platform.startswith("linux"):
        libc = ctypes.CDLL(None, use_errno=True)
        renameat2 = getattr(libc, "renameat2", None)
        if renameat2 is None:
            raise MutationError("renameat2(RENAME_EXCHANGE) unavailable")
        AT_FDCWD = -100
        RENAME_EXCHANGE = 0x2
        result = renameat2(
            AT_FDCWD, os.fsencode(left), AT_FDCWD, os.fsencode(right), RENAME_EXCHANGE
        )
        if result != 0:
            err = ctypes.get_errno()
            raise OSError(err, os.strerror(err))
        return
    if sys.platform == "darwin":
        libc = ctypes.CDLL(None, use_errno=True)
        renamex_np = getattr(libc, "renamex_np", None)
        if renamex_np is None:
            raise MutationError("renamex_np(RENAME_SWAP) unavailable")
        RENAME_SWAP = 0x00000002
        result = renamex_np(os.fsencode(left), os.fsencode(right), RENAME_SWAP)
        if result != 0:
            err = ctypes.get_errno()
            raise OSError(err, os.strerror(err))
        return
    raise MutationError(f"atomic exchange unsupported on {sys.platform}")


def _replace_existing_with_backup(target: Path, replacement: Path, backup: Path) -> None:
    backup.parent.mkdir(parents=True, exist_ok=True)
    if backup.exists():
        raise MutationError(f"backup path already exists: {backup}")
    if os.name != "nt" and target.parent.stat().st_dev != backup.parent.stat().st_dev:
        raise MutationError("displaced backup must be on the same filesystem as the canonical target")
    if os.name == "nt":
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        replace_file = kernel32.ReplaceFileW
        replace_file.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_void_p, ctypes.c_void_p]
        replace_file.restype = ctypes.c_int
        ok = replace_file(str(target), str(replacement), str(backup), 0, None, None)
        if not ok:
            err = ctypes.get_last_error()
            raise OSError(err, ctypes.FormatError(err))
        return
    _atomic_exchange(replacement, target)
    os.replace(replacement, backup)


def _rollback_existing_from_backup(target: Path, backup: Path, app_copy: Path) -> None:
    app_copy.parent.mkdir(parents=True, exist_ok=True)
    if app_copy.exists():
        raise MutationError(f"rollback app path already exists: {app_copy}")
    if os.name == "nt":
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        replace_file = kernel32.ReplaceFileW
        replace_file.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_void_p, ctypes.c_void_p]
        replace_file.restype = ctypes.c_int
        ok = replace_file(str(target), str(backup), str(app_copy), 0, None, None)
        if not ok:
            err = ctypes.get_last_error()
            raise OSError(err, ctypes.FormatError(err))
        return
    _atomic_exchange(target, backup)
    os.replace(backup, app_copy)


def atomic_replace_bytes(
    path: Path,
    data: bytes,
    *,
    expected_sha256: str | None = None,
    displaced_backup: Path | None = None,
    failpoint: str | None = None,
    _precommit_hook: Callable[[Path], None] | None = None,
) -> dict[str, Any]:
    """Replace one file, preserving the displaced version when CAS semantics matter.

    When ``expected_sha256`` is supplied, the commit uses an OS atomic exchange /
    ReplaceFile primitive and keeps the exact file displaced at commit time. If
    its hash does not match the expected base, the swap is atomically rolled back
    and the intended application bytes remain separately recoverable.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    before_exists = path.exists()
    before = path.read_bytes() if before_exists else b""
    before_hash = sha256_bytes(before) if before_exists else None
    if expected_sha256 is not None and before_hash != expected_sha256:
        raise StaleBaseError(f"stale base for {path}: expected {expected_sha256}, found {before_hash}")

    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".cwtmp", dir=path.parent)
    temp_path = Path(temp_name)
    committed = False
    backup_path: Path | None = None
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        if failpoint == "after_temp_fsync":
            raise ControlledFailure("controlled failure after temp fsync")
        if failpoint == "permission_error_before_commit":
            raise PermissionError(errno.EACCES, "controlled permission failure")
        if failpoint == "disk_full_before_commit":
            raise OSError(errno.ENOSPC, "controlled disk-full failure")
        if before_exists:
            try:
                os.chmod(temp_path, path.stat().st_mode)
            except OSError:
                pass
        if _precommit_hook:
            _precommit_hook(path)

        if expected_sha256 is not None:
            if not path.exists():
                raise StaleBaseError(f"target disappeared before guarded commit: {path}")
            backup_path = displaced_backup or path.with_name(f".{path.name}.{secrets.token_hex(8)}.cwold")
            _replace_existing_with_backup(path, temp_path, backup_path)
            committed = True
            displaced_hash = sha256_file(backup_path)
            current_hash = sha256_file(path)
            intended_hash = sha256_bytes(data)
            if displaced_hash != expected_sha256:
                app_copy = backup_path.with_name(backup_path.name + ".cwapp")
                _rollback_existing_from_backup(path, backup_path, app_copy)
                _fsync_directory(path.parent)
                raise StaleBaseError(
                    f"base changed during guarded commit for {path}: expected {expected_sha256}, displaced {displaced_hash}"
                )
            if current_hash != intended_hash:
                raise PostCommitError(
                    f"target changed immediately after commit for {path}: intended {intended_hash}, found {current_hash}"
                )
        else:
            os.replace(temp_path, path)
            committed = True
        _fsync_directory(path.parent)
        if failpoint == "after_replace":
            raise PostCommitError("controlled failure after committed replacement")
    finally:
        if temp_path.exists():
            temp_path.unlink(missing_ok=True)

    return {
        "path": str(path),
        "before_sha256": before_hash,
        "after_sha256": sha256_bytes(data),
        "bytes": len(data),
        "atomic_boundary": "guarded_single_file_exchange" if expected_sha256 is not None else "single_file_replace",
        "displaced_backup": str(backup_path) if backup_path and backup_path.exists() else None,
        "committed": committed,
    }


def write_json_atomic(path: Path, value: Any) -> None:
    atomic_replace_bytes(path, (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
