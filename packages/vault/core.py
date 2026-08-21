from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Iterable
import os

import yaml


class VaultError(RuntimeError):
    pass


class NoDatesSafeLoader(yaml.SafeLoader):
    pass


for ch, resolvers in list(NoDatesSafeLoader.yaml_implicit_resolvers.items()):
    NoDatesSafeLoader.yaml_implicit_resolvers[ch] = [
        item for item in resolvers if item[0] != "tag:yaml.org,2002:timestamp"
    ]


def sha256_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_yaml(path: Path) -> Any:
    return yaml.load(path.read_text(encoding="utf-8"), Loader=NoDatesSafeLoader)


def dump_yaml(value: Any) -> str:
    return yaml.safe_dump(value, sort_keys=False, allow_unicode=True)


def safe_project_path(project_root: Path, relative: str | Path) -> Path:
    root = project_root.resolve()
    candidate = (root / relative).resolve(strict=False)
    try:
        common = Path(os.path.commonpath([str(root), str(candidate)]))
    except ValueError as exc:
        raise VaultError(f"path is outside project root: {relative}") from exc
    if common != root:
        raise VaultError(f"path escapes project root: {relative}")
    return candidate


@dataclass(frozen=True)
class SheetDocument:
    id: str
    path: Path
    frontmatter: dict[str, Any]
    body: str
    raw_text: str
    sha256: str


def parse_sheet_text(text: str, path: Path | None = None) -> tuple[dict[str, Any], str]:
    label = str(path or "<sheet>")
    if not text.startswith("---\n"):
        raise VaultError(f"{label}: missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise VaultError(f"{label}: unterminated YAML frontmatter")
    value = yaml.load(text[4:end], Loader=NoDatesSafeLoader)
    if not isinstance(value, dict):
        raise VaultError(f"{label}: frontmatter must be a mapping")
    for key in ("id", "schema", "kind"):
        if not isinstance(value.get(key), str) or not value[key]:
            raise VaultError(f"{label}: frontmatter missing {key}")
    body = text[end + len("\n---\n"):]
    return value, body


def load_sheet(path: Path) -> SheetDocument:
    raw = path.read_text(encoding="utf-8")
    frontmatter, body = parse_sheet_text(raw, path)
    return SheetDocument(
        id=frontmatter["id"],
        path=path,
        frontmatter=frontmatter,
        body=body,
        raw_text=raw,
        sha256=sha256_bytes(raw.encode("utf-8")),
    )


def scan_sheets(project_root: Path) -> dict[str, SheetDocument]:
    sheets_root = safe_project_path(project_root, "sheets")
    found: dict[str, SheetDocument] = {}
    if not sheets_root.exists():
        return found
    for path in sorted(sheets_root.rglob("*.md")):
        doc = load_sheet(path)
        if doc.id in found:
            raise VaultError(f"duplicate Sheet id {doc.id}: {found[doc.id].path} and {path}")
        found[doc.id] = doc
    return found


def find_sheet_by_id(project_root: Path, sheet_id: str) -> SheetDocument:
    try:
        return scan_sheets(project_root)[sheet_id]
    except KeyError as exc:
        raise VaultError(f"Sheet {sheet_id} does not resolve") from exc


def scan_sidecars(project_root: Path) -> dict[str, tuple[Path, dict[str, Any]]]:
    root = safe_project_path(project_root, "meta/sheets")
    found: dict[str, tuple[Path, dict[str, Any]]] = {}
    if not root.exists():
        return found
    for path in sorted(root.rglob("*.yml")):
        value = load_yaml(path)
        if not isinstance(value, dict) or not isinstance(value.get("id"), str):
            raise VaultError(f"invalid Sheet sidecar: {path}")
        sheet_id = value["id"]
        if sheet_id in found:
            raise VaultError(f"duplicate Sheet sidecar id {sheet_id}")
        found[sheet_id] = (path, value)
    return found


def load_sheet_with_sidecar(project_root: Path, sheet_id: str) -> tuple[SheetDocument, Path, dict[str, Any]]:
    sheet = find_sheet_by_id(project_root, sheet_id)
    sidecars = scan_sidecars(project_root)
    if sheet_id not in sidecars:
        raise VaultError(f"Sheet {sheet_id} has no sidecar")
    sidecar_path, sidecar = sidecars[sheet_id]
    if sidecar.get("kind") != sheet.frontmatter.get("kind"):
        raise VaultError(f"Sheet {sheet_id} kind mismatch between body and sidecar")
    return sheet, sidecar_path, sidecar


def project_manifest(project_root: Path) -> dict[str, Any]:
    value = load_yaml(safe_project_path(project_root, "project.yml"))
    if not isinstance(value, dict) or not isinstance(value.get("id"), str):
        raise VaultError("invalid project.yml")
    return value


def manifest_paths(project_root: Path) -> Iterable[Path]:
    root = safe_project_path(project_root, "manuscripts")
    if root.exists():
        yield from sorted(root.rglob("*.yml"))


def canonical_inventory(project_root: Path) -> list[dict[str, str]]:
    root = project_root.resolve()
    inventory: list[dict[str, str]] = []
    categories = [
        Path("project.yml"),
        Path("sheets"),
        Path("meta/sheets"),
        Path("manuscripts"),
        Path("compile"),
        Path("compendium"),
        Path("sources"),
        Path("assets"),
        Path("patches"),
        Path("snapshots"),
        Path("migrations"),
        Path("mutations"),
        Path("recovery/conflicts"),
    ]
    seen: set[Path] = set()
    for category in categories:
        path = safe_project_path(root, category)
        candidates = [path] if path.is_file() else sorted(path.rglob("*")) if path.exists() else []
        for candidate in candidates:
            if not candidate.is_file() or candidate in seen:
                continue
            seen.add(candidate)
            inventory.append({
                "path": candidate.relative_to(root).as_posix(),
                "sha256": sha256_file(candidate),
            })
    return inventory
