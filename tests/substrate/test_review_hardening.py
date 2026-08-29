from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

import yaml

from packages.catalog.core import build_catalog, catalog_projection
from packages.mutation.core import (
    ControlledFailure,
    PlannedWrite,
    StaleBaseError,
    apply_operation_plan,
    apply_text_mutation,
    move_canonical_file,
)
from packages.recovery.core import RecoveryError, create_snapshot, restore_snapshot_file
from packages.vault.core import VaultError, find_sheet_by_id, scan_sheets, sha256_file

S1 = "sh_018f0000-0000-7000-8000-000000000001"
S2 = "sh_018f0000-0000-7000-8000-000000000002"
M1 = "ms_018f0000-0000-7000-8000-000000000001"
P1 = "prj_018f0000-0000-7000-8000-000000000001"
N1 = "nd_018f0000-0000-7000-8000-000000000001"
N2 = "nd_018f0000-0000-7000-8000-000000000002"


def _sheet(sid: str, title: str) -> str:
    return f"---\nid: {sid}\nschema: constellation_sheet_v1\nkind: manuscript\ntitle: {title}\n---\n\n# {title}\n\nBody\n"


def make_project(root: Path) -> None:
    (root / "sheets").mkdir(parents=True)
    (root / "meta/sheets").mkdir(parents=True)
    (root / "manuscripts").mkdir(parents=True)
    (root / "materials").mkdir(parents=True)
    (root / "project.yml").write_text(yaml.safe_dump({
        "id": P1, "schema_version": "0.1.0", "name": "Fixture",
        "created_at": "2026-01-01T00:00:00+00:00", "modified_at": "2026-01-01T00:00:00+00:00",
        "default_manuscript_id": M1, "canonical_policy": "manifest_first", "text_dialect": "constellation_markdown_v1",
    }, sort_keys=False), encoding="utf-8")
    for sid, title in ((S1, "One"), (S2, "Two")):
        (root / "sheets" / f"{sid}-{title.lower()}.md").write_text(_sheet(sid, title), encoding="utf-8")
        (root / "meta/sheets" / f"{sid}.sheet.yml").write_text(yaml.safe_dump({
            "id": sid, "schema_version": "0.1.0", "title": title, "kind": "manuscript", "status": "draft",
            "created_at": "2026-01-01T00:00:00+00:00", "modified_at": "2026-01-01T00:00:00+00:00",
        }, sort_keys=False), encoding="utf-8")
    (root / "manuscripts/main.manuscript.yml").write_text(yaml.safe_dump({
        "id": M1, "schema_version": "0.1.0", "project_id": P1, "title": "Fixture", "kind": "novel",
        "root_nodes": [
            {"id": N1, "type": "sheet_ref", "sheet_id": S1, "title": "One", "include": True, "role": "scene", "children": []},
            {"id": N2, "type": "sheet_ref", "sheet_id": S2, "title": "Two", "include": True, "role": "scene", "children": []},
        ],
    }, sort_keys=False), encoding="utf-8")


class ReviewHardeningTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        make_project(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def test_precommit_stale_race_preserves_external(self):
        sheet = find_sheet_by_id(self.root, S1)
        external = b"external-wins\n"
        def hook(path: Path) -> None:
            path.write_bytes(external)
        with self.assertRaises(StaleBaseError):
            apply_text_mutation(self.root, sheet.path.relative_to(self.root), "application\n", object_id=S1,
                                object_type="sheet", intent="race", expected_sha256=sheet.sha256, _precommit_hook=hook)
        self.assertEqual(sheet.path.read_bytes(), external)

    def test_postcommit_failure_is_applied_unconfirmed(self):
        sheet = find_sheet_by_id(self.root, S1)
        receipt = apply_text_mutation(self.root, sheet.path.relative_to(self.root), "after\n", object_id=S1,
                                      object_type="sheet", intent="post", expected_sha256=sheet.sha256, failpoint="after_replace")
        self.assertEqual(receipt["application"]["state"], "applied_unconfirmed")
        self.assertEqual(sheet.path.read_text(), "after\n")

    def test_permission_and_disk_failures_preserve_base(self):
        for failpoint, error in (("permission_error_before_commit", PermissionError), ("disk_full_before_commit", OSError)):
            sheet = find_sheet_by_id(self.root, S1)
            before = sheet.sha256
            with self.assertRaises(error):
                apply_text_mutation(self.root, sheet.path.relative_to(self.root), "after\n", object_id=S1,
                                    object_type="sheet", intent=failpoint, expected_sha256=before, failpoint=failpoint)
            self.assertEqual(find_sheet_by_id(self.root, S1).sha256, before)

    def test_corrupt_catalog_is_rebuilt_from_canonical_files(self):
        build_catalog(self.root)
        expected = catalog_projection(self.root)
        path = self.root / ".workbench/cache/catalog.sqlite"
        path.write_bytes(b"not sqlite")
        build_catalog(self.root)
        self.assertEqual(catalog_projection(self.root), expected)

    def test_snapshot_corruption_blocks_restore(self):
        sheet = find_sheet_by_id(self.root, S2)
        rel = sheet.path.relative_to(self.root)
        snapshot = create_snapshot(self.root, "named", [rel], object_ids={rel.as_posix(): S2})
        (snapshot["snapshot_root"] / "files" / rel).write_text("corrupt", encoding="utf-8")
        with self.assertRaises(RecoveryError):
            restore_snapshot_file(self.root, snapshot["snapshot_root"], rel, object_id=S2)

    def test_symlinked_sheet_is_rejected(self):
        target = Path(self.temp.name).parent / f"outside-{self.root.name}.md"
        target.write_text(_sheet("sh_018f0000-0000-7000-8000-000000000099", "Outside"), encoding="utf-8")
        link = self.root / "sheets/outside.md"
        try:
            link.symlink_to(target)
            with self.assertRaises(VaultError):
                scan_sheets(self.root)
        finally:
            target.unlink(missing_ok=True)

    def test_move_does_not_clobber_existing_destination(self):
        sheet = find_sheet_by_id(self.root, S1)
        destination = Path("sheets/existing.md")
        (self.root / destination).write_text("keep me", encoding="utf-8")
        with self.assertRaises(Exception):
            move_canonical_file(self.root, sheet.path.relative_to(self.root), destination, object_id=S1, object_type="sheet")
        self.assertEqual((self.root / destination).read_text(), "keep me")
        self.assertTrue(sheet.path.exists())

    def test_rollback_preserves_concurrent_divergent_version(self):
        a, b = Path("materials/a.txt"), Path("materials/b.txt")
        (self.root / a).write_text("a0", encoding="utf-8")
        (self.root / b).write_text("b0", encoding="utf-8")
        ah, bh = sha256_file(self.root / a), sha256_file(self.root / b)
        def concurrent(root: Path, applied: list[int]) -> None:
            if applied:
                (root / a).write_text("external-a", encoding="utf-8")
        with self.assertRaises(ControlledFailure):
            apply_operation_plan(self.root, [
                PlannedWrite(a.as_posix(), P1, "material", b"a1", ah),
                PlannedWrite(b.as_posix(), P1, "material", b"b1", bh),
            ], intent="rollback-race", fail_after_applies=1, _before_rollback_hook=concurrent)
        self.assertEqual((self.root / a).read_text(), "external-a")
        divergent = list((self.root / "recovery/bundles").glob("*/divergent/*.bin"))
        self.assertTrue(divergent)


if __name__ == "__main__":
    unittest.main()
