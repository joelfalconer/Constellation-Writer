from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import yaml

from packages.catalog.core import (
    build_catalog,
    catalog_digest,
    catalog_projection,
    delete_catalog,
)
from packages.manuscript.core import (
    load_manifest,
    ordered_sheet_ids,
    reorder_root_placement,
)
from packages.mutation.core import (
    ControlledFailure,
    PlannedWrite,
    apply_operation_plan,
    apply_text_mutation,
    move_canonical_file,
    typed_uuid7,
)
from packages.recovery.core import (
    create_snapshot,
    load_recovery_buffer,
    persist_recovery_buffer,
    preserve_conflict,
    restore_snapshot_file,
)
from packages.vault.core import (
    find_sheet_by_id,
    load_sheet_with_sidecar,
    sha256_file,
)


S1 = "sh_018f0000-0000-7000-8000-000000000001"
S2 = "sh_018f0000-0000-7000-8000-000000000002"
M1 = "ms_018f0000-0000-7000-8000-000000000001"
P1 = "prj_018f0000-0000-7000-8000-000000000001"
N1 = "nd_018f0000-0000-7000-8000-000000000001"
N2 = "nd_018f0000-0000-7000-8000-000000000002"


def sheet_text(sheet_id: str, title: str, body: str) -> str:
    return (
        f"---\nid: {sheet_id}\nschema: constellation_sheet_v1\n"
        f"kind: manuscript\ntitle: {title}\n---\n\n# {title}\n\n{body}\n"
    )


def make_project(root: Path) -> None:
    (root / "sheets").mkdir(parents=True)
    (root / "meta/sheets").mkdir(parents=True)
    (root / "manuscripts").mkdir(parents=True)
    (root / "materials").mkdir(parents=True)
    (root / "project.yml").write_text(
        yaml.safe_dump(
            {
                "id": P1,
                "schema_version": "0.1.0",
                "name": "Fixture",
                "created_at": "2026-01-01T00:00:00+00:00",
                "modified_at": "2026-01-01T00:00:00+00:00",
                "default_manuscript_id": M1,
                "canonical_policy": "manifest_first",
                "text_dialect": "constellation_markdown_v1",
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    for sid, title, body in ((S1, "One", "Alpha"), (S2, "Two", "Beta")):
        (root / "sheets" / f"{sid}-{title.lower()}.md").write_text(
            sheet_text(sid, title, body), encoding="utf-8"
        )
        (root / "meta/sheets" / f"{sid}.sheet.yml").write_text(
            yaml.safe_dump(
                {
                    "id": sid,
                    "schema_version": "0.1.0",
                    "title": title,
                    "kind": "manuscript",
                    "status": "draft",
                    "created_at": "2026-01-01T00:00:00+00:00",
                    "modified_at": "2026-01-01T00:00:00+00:00",
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
    manifest = {
        "id": M1,
        "schema_version": "0.1.0",
        "project_id": P1,
        "title": "Fixture",
        "kind": "novel",
        "root_nodes": [
            {
                "id": N1,
                "type": "sheet_ref",
                "sheet_id": S1,
                "title": "One",
                "include": True,
                "role": "scene",
                "children": [],
            },
            {
                "id": N2,
                "type": "sheet_ref",
                "sheet_id": S2,
                "title": "Two",
                "include": True,
                "role": "scene",
                "children": [],
            },
        ],
    }
    (root / "manuscripts/main.manuscript.yml").write_text(
        yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8"
    )


class SubstrateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        make_project(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def test_uuid7_typed(self):
        value = typed_uuid7("op")
        self.assertRegex(
            value,
            r"^op_[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
        )

    def test_sheet_sidecar_recovery_and_atomic_save(self):
        sheet, _path, sidecar = load_sheet_with_sidecar(self.root, S1)
        self.assertEqual(sidecar["id"], S1)
        edited = sheet.raw_text + "\nRecovered.\n"
        persist_recovery_buffer(self.root, S1, sheet.sha256, edited)
        recovered = load_recovery_buffer(self.root, S1)
        receipt = apply_text_mutation(
            self.root,
            sheet.path.relative_to(self.root),
            recovered["content"],
            object_id=S1,
            object_type="sheet",
            intent="test save",
            expected_sha256=sheet.sha256,
        )
        self.assertEqual(receipt["application"]["state"], "applied")
        self.assertEqual(find_sheet_by_id(self.root, S1).raw_text, edited)

    def test_single_file_failure_preserves_old_bytes(self):
        sheet = find_sheet_by_id(self.root, S1)
        before = sheet.sha256
        with self.assertRaises(ControlledFailure):
            apply_text_mutation(
                self.root,
                sheet.path.relative_to(self.root),
                sheet.raw_text + "changed",
                object_id=S1,
                object_type="sheet",
                intent="fail",
                expected_sha256=before,
                failpoint="after_temp_fsync",
            )
        self.assertEqual(find_sheet_by_id(self.root, S1).sha256, before)

    def test_manifest_reorder_does_not_touch_prose(self):
        before_hashes = {
            sid: find_sheet_by_id(self.root, sid).sha256 for sid in (S1, S2)
        }
        before = ordered_sheet_ids(
            load_manifest(self.root, "manuscripts/main.manuscript.yml")
        )
        reorder_root_placement(
            self.root, "manuscripts/main.manuscript.yml", N2, 0
        )
        after = ordered_sheet_ids(
            load_manifest(self.root, "manuscripts/main.manuscript.yml")
        )
        self.assertEqual(after, list(reversed(before)))
        self.assertEqual(
            before_hashes,
            {sid: find_sheet_by_id(self.root, sid).sha256 for sid in (S1, S2)},
        )

    def test_catalog_delete_rebuild_equivalence(self):
        build_catalog(self.root)
        projection = catalog_projection(self.root)
        digest = catalog_digest(self.root)
        delete_catalog(self.root)
        build_catalog(self.root)
        self.assertEqual(projection, catalog_projection(self.root))
        self.assertEqual(digest, catalog_digest(self.root))

    def test_conflict_preserves_three_versions(self):
        sheet = find_sheet_by_id(self.root, S1)
        base = sheet.path.read_bytes()
        app = base + b"app\n"
        external = base + b"external\n"
        result = preserve_conflict(
            self.root,
            object_type="sheet",
            object_id=S1,
            relative_path=sheet.path.relative_to(self.root),
            base_bytes=base,
            app_bytes=app,
            external_bytes=external,
        )
        self.assertTrue(result and result["zero_loss"])
        manifest = yaml.safe_load((self.root / result["manifest_path"]).read_text())
        self.assertEqual(manifest["status"], "unresolved")
        for key in ("base", "current_app_version", "external_version"):
            self.assertTrue((self.root / manifest[key]["file"]).exists())

    def test_snapshot_restore(self):
        sheet = find_sheet_by_id(self.root, S2)
        rel = sheet.path.relative_to(self.root)
        snap = create_snapshot(
            self.root, "named", [rel], object_ids={rel.as_posix(): S2}
        )
        before = sheet.sha256
        apply_text_mutation(
            self.root,
            rel,
            sheet.raw_text + "changed\n",
            object_id=S2,
            object_type="sheet",
            intent="change",
            expected_sha256=before,
        )
        result = restore_snapshot_file(
            self.root, snap["snapshot_root"], rel, object_id=S2
        )
        self.assertEqual(find_sheet_by_id(self.root, S2).sha256, before)
        self.assertTrue((self.root / result["receipt_path"]).exists())

    def test_move_preserves_identity(self):
        sheet = find_sheet_by_id(self.root, S1)
        old = sheet.path.relative_to(self.root)
        new = Path("sheets/moved/renamed.md")
        move_canonical_file(
            self.root, old, new, object_id=S1, object_type="sheet"
        )
        moved = find_sheet_by_id(self.root, S1)
        self.assertEqual(moved.id, S1)
        self.assertEqual(moved.path.relative_to(self.root), new)

    def test_multi_file_failure_rolls_back(self):
        a = Path("materials/a.txt")
        b = Path("materials/b.txt")
        (self.root / a).write_text("a0", encoding="utf-8")
        (self.root / b).write_text("b0", encoding="utf-8")
        ah = sha256_file(self.root / a)
        bh = sha256_file(self.root / b)
        with self.assertRaises(ControlledFailure):
            apply_operation_plan(
                self.root,
                [
                    PlannedWrite(a.as_posix(), P1, "material", b"a1", ah),
                    PlannedWrite(b.as_posix(), P1, "material", b"b1", bh),
                ],
                intent="rollback",
                fail_after_applies=1,
            )
        self.assertEqual(sha256_file(self.root / a), ah)
        self.assertEqual(sha256_file(self.root / b), bh)
        receipts = list((self.root / "mutations/receipts").glob("*.json"))
        self.assertTrue(receipts)
        values = [json.loads(path.read_text()) for path in receipts]
        failed = [value for value in values if "application_state" in value]
        self.assertTrue(
            any(value["application_state"] == "failed_recovered" for value in failed)
        )


if __name__ == "__main__":
    unittest.main()
