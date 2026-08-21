from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Any
import json
import sqlite3

from packages.manuscript.core import iter_nodes
from packages.mutation.core import atomic_replace_bytes
from packages.vault.core import (
    load_yaml,
    manifest_paths,
    project_manifest,
    safe_project_path,
    scan_sheets,
    scan_sidecars,
    sha256_file,
)


CATALOG_SCHEMA_VERSION = 1


def catalog_path(project_root: Path) -> Path:
    return safe_project_path(project_root, ".workbench/cache/catalog.sqlite")


def delete_catalog(project_root: Path) -> None:
    path = catalog_path(project_root)
    path.unlink(missing_ok=True)
    for suffix in ("-wal", "-shm"):
        Path(str(path) + suffix).unlink(missing_ok=True)


def _schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA journal_mode=DELETE;
        PRAGMA foreign_keys=ON;
        CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE sheets(
          id TEXT PRIMARY KEY,
          path TEXT NOT NULL,
          title TEXT,
          kind TEXT,
          status TEXT,
          body_sha256 TEXT NOT NULL,
          sidecar_path TEXT,
          sidecar_sha256 TEXT
        );
        CREATE TABLE manuscripts(
          id TEXT PRIMARY KEY,
          path TEXT NOT NULL,
          title TEXT,
          kind TEXT,
          sha256 TEXT NOT NULL
        );
        CREATE TABLE placements(
          manuscript_id TEXT NOT NULL,
          placement_id TEXT NOT NULL,
          parent_id TEXT,
          ordinal INTEGER NOT NULL,
          node_type TEXT NOT NULL,
          sheet_id TEXT,
          role TEXT,
          include_value TEXT NOT NULL,
          PRIMARY KEY(manuscript_id, placement_id)
        );
        CREATE INDEX placements_sheet_id ON placements(sheet_id);
        """
    )


def build_catalog(project_root: Path) -> dict[str, Any]:
    root = project_root.resolve()
    path = catalog_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".sqlite.building")
    temp.unlink(missing_ok=True)
    conn = sqlite3.connect(temp)
    try:
        _schema(conn)
        project = project_manifest(root)
        conn.execute(
            "INSERT INTO meta(key,value) VALUES(?,?)",
            ("schema_version", str(CATALOG_SCHEMA_VERSION)),
        )
        conn.execute(
            "INSERT INTO meta(key,value) VALUES(?,?)",
            ("rebuild_source", "canonical_project_files"),
        )
        conn.execute(
            "INSERT INTO meta(key,value) VALUES(?,?)",
            ("project_id", project["id"]),
        )

        sheets = scan_sheets(root)
        sidecars = scan_sidecars(root)
        for sheet_id, sheet in sorted(sheets.items()):
            sidecar_path = None
            sidecar = None
            sidecar_hash = None
            if sheet_id in sidecars:
                spath, sidecar = sidecars[sheet_id]
                sidecar_path = spath.relative_to(root).as_posix()
                sidecar_hash = sha256_file(spath)
            conn.execute(
                "INSERT INTO sheets VALUES(?,?,?,?,?,?,?,?)",
                (
                    sheet_id,
                    sheet.path.relative_to(root).as_posix(),
                    (sidecar or {}).get("title") or sheet.frontmatter.get("title"),
                    sheet.frontmatter.get("kind"),
                    (sidecar or {}).get("status"),
                    sheet.sha256,
                    sidecar_path,
                    sidecar_hash,
                ),
            )

        manuscript_count = 0
        placement_count = 0
        for manifest_path in manifest_paths(root):
            manifest = load_yaml(manifest_path)
            if not isinstance(manifest, dict) or not manifest.get("id"):
                continue
            manuscript_count += 1
            manifest_id = manifest["id"]
            conn.execute(
                "INSERT INTO manuscripts VALUES(?,?,?,?,?)",
                (
                    manifest_id,
                    manifest_path.relative_to(root).as_posix(),
                    manifest.get("title"),
                    manifest.get("kind"),
                    sha256_file(manifest_path),
                ),
            )
            for parent_id, ordinal, node in iter_nodes(
                manifest.get("root_nodes") or []
            ):
                placement_count += 1
                include = node.get("include", True)
                conn.execute(
                    "INSERT INTO placements VALUES(?,?,?,?,?,?,?,?)",
                    (
                        manifest_id,
                        node.get("id"),
                        parent_id,
                        ordinal,
                        node.get("type"),
                        node.get("sheet_id"),
                        node.get("role"),
                        json.dumps(include),
                    ),
                )
        conn.commit()
    finally:
        conn.close()

    # The catalog is derived. Build separately, then replace the cache file.
    atomic_replace_bytes(path, temp.read_bytes())
    temp.unlink(missing_ok=True)
    return {
        "path": path.relative_to(root).as_posix(),
        "sheets": len(sheets),
        "manuscripts": manuscript_count,
        "placements": placement_count,
        "digest": catalog_digest(root),
    }


def _rows(conn: sqlite3.Connection, table: str) -> list[list[Any]]:
    return [list(row) for row in conn.execute(f"SELECT * FROM {table} ORDER BY rowid")]


def catalog_projection(project_root: Path) -> dict[str, Any]:
    path = catalog_path(project_root)
    conn = sqlite3.connect(path)
    try:
        return {
            "meta": _rows(conn, "meta"),
            "sheets": _rows(conn, "sheets"),
            "manuscripts": _rows(conn, "manuscripts"),
            "placements": _rows(conn, "placements"),
        }
    finally:
        conn.close()


def catalog_digest(project_root: Path) -> str:
    payload = json.dumps(
        catalog_projection(project_root),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return sha256(payload.encode("utf-8")).hexdigest()
