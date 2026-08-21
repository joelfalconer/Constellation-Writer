from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

import yaml

MODULE_PATH = Path(__file__).with_name("compile_spike.py")
SPEC = importlib.util.spec_from_file_location("compile_spike", MODULE_PATH)
compile_spike = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(compile_spike)


def write_yaml(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def write_sheet(path: Path, sheet_id: str, title: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        f"id: {sheet_id}\n"
        "schema: constellation_sheet_v1\n"
        "kind: manuscript\n"
        f"title: {title}\n"
        "---\n\n"
        f"{body.rstrip()}\n",
        encoding="utf-8",
    )


class SyntheticProject:
    def __init__(self, root: Path):
        self.root = root
        self.manifest_path = root / "manuscripts/main.manuscript.yml"
        self.profile_path = root / "compile/profile.yml"
        self.nodes: list[dict] = []

    def add_sheet(
        self,
        *,
        sheet_id: str,
        placement_id: str,
        title: str,
        body: str,
        role: str = "scene",
        include: bool = True,
        filename: str | None = None,
    ) -> Path:
        path = self.root / "sheets" / (filename or f"{sheet_id}.md")
        write_sheet(path, sheet_id, title, body)
        self.nodes.append(
            {
                "id": placement_id,
                "type": "sheet_ref",
                "sheet_id": sheet_id,
                "title": title,
                "include": include,
                "role": role,
                "children": [],
            }
        )
        return path

    def finish(self, profile_overrides: dict | None = None) -> None:
        write_yaml(
            self.manifest_path,
            {
                "id": "ms_test",
                "schema_version": "0.1.0",
                "project_id": "prj_test",
                "title": "Synthetic Manuscript",
                "kind": "novel",
                "root_nodes": self.nodes,
            },
        )
        profile = {
            "id": "cp_test",
            "schema_version": "0.1.0",
            "name": "Synthetic Markdown",
            "manuscript_id": "ms_test",
            "target": "markdown",
            "output": {"path": "build/output.md", "standalone": True},
            "include_comments": False,
            "fail_on": ["missing_included_sheet", "invalid_manifest"],
            "role_transforms": {"chapter": "heading_1", "scene": "concatenate_with_scene_break"},
        }
        if profile_overrides:
            profile.update(profile_overrides)
        write_yaml(self.profile_path, profile)

    def compile(self, out: Path, pandoc_path: str | None = None, profile_overrides: dict | None = None):
        self.finish(profile_overrides)
        return compile_spike.compile_project(
            self.root,
            self.manifest_path,
            self.profile_path,
            out,
            pandoc_path=pandoc_path,
        )


class CompileSpikeTests(unittest.TestCase):
    def make_project(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name) / "project"
        root.mkdir(parents=True)
        return SyntheticProject(root)

    def read_json(self, out: Path, name: str):
        return json.loads((out / name).read_text(encoding="utf-8"))

    def test_cg001_manifest_order_beats_filesystem_order(self):
        project = self.make_project()
        project.add_sheet(
            sheet_id="sh_first",
            placement_id="nd_first",
            title="First",
            body="# First\n\nMANIFEST-FIRST",
            filename="z-last-by-filename.md",
        )
        project.add_sheet(
            sheet_id="sh_second",
            placement_id="nd_second",
            title="Second",
            body="# Second\n\nMANIFEST-SECOND",
            filename="a-first-by-filename.md",
        )
        out = project.root / "build/test"
        receipt = project.compile(out)
        rendered = (out / "output.md").read_text(encoding="utf-8")
        self.assertEqual(receipt["status"], "passed")
        self.assertLess(rendered.index("MANIFEST-FIRST"), rendered.index("MANIFEST-SECOND"))

    def test_cg002_excluded_sheet_absent_and_reason_in_plan(self):
        project = self.make_project()
        project.add_sheet(
            sheet_id="sh_keep",
            placement_id="nd_keep",
            title="Keep",
            body="# Keep\n\nVISIBLE",
        )
        project.add_sheet(
            sheet_id="sh_cut",
            placement_id="nd_cut",
            title="Cut",
            body="# Cut\n\nSHOULD-NOT-APPEAR",
            include=False,
        )
        out = project.root / "build/test"
        project.compile(out)
        plan = self.read_json(out, "compile-plan.json")
        rendered = (out / "output.md").read_text(encoding="utf-8")
        self.assertNotIn("SHOULD-NOT-APPEAR", rendered)
        cut = next(item for item in plan["excluded_placements"] if item["placement_id"] == "nd_cut")
        self.assertEqual(cut["reason"], "manifest_excluded")

    def test_cg003_node_title_does_not_duplicate_identical_first_heading(self):
        project = self.make_project()
        project.add_sheet(
            sheet_id="sh_chapter",
            placement_id="nd_chapter",
            title="Chapter One",
            role="chapter",
            body="# Chapter One\n\nOpening paragraph.",
        )
        out = project.root / "build/test"
        project.compile(out)
        rendered = (out / "output.md").read_text(encoding="utf-8")
        self.assertEqual(rendered.count("# Chapter One"), 1)

    def test_cg004_scene_break_is_semantic_ast_node(self):
        project = self.make_project()
        project.add_sheet(
            sheet_id="sh_a",
            placement_id="nd_a",
            title="A",
            body="# A\n\nAlpha.",
            role="scene",
        )
        project.add_sheet(
            sheet_id="sh_b",
            placement_id="nd_b",
            title="B",
            body="# B\n\nBeta.",
            role="scene",
        )
        out = project.root / "build/test"
        project.compile(out)
        ast = self.read_json(out, "workbench-ast.json")
        breaks = [block for block in ast["blocks"] if block["kind"] == "scene_break"]
        self.assertEqual(len(breaks), 1)
        self.assertEqual(breaks[0]["provenance"]["kind"], "manifest_semantic_boundary")
        self.assertIn("* * *", (out / "output.md").read_text(encoding="utf-8"))

    def test_cg005_comment_excluded_by_default_and_explained(self):
        project = self.make_project()
        project.add_sheet(
            sheet_id="sh_comment",
            placement_id="nd_comment",
            title="Comments",
            body="# Comments\n\nBefore.\n\n<!-- private editorial note -->\n\nAfter.",
        )
        out = project.root / "build/test"
        project.compile(out)
        qa = self.read_json(out, "qa.json")
        rendered = (out / "output.md").read_text(encoding="utf-8")
        self.assertNotIn("private editorial note", rendered)
        self.assertTrue(any(item["code"] == "comment_excluded" for item in qa["issues"]))

    def test_cg006_missing_asset_has_source_locator(self):
        project = self.make_project()
        project.add_sheet(
            sheet_id="sh_asset",
            placement_id="nd_asset",
            title="Asset",
            body="# Asset\n\n![Missing](assets/nope.png)",
        )
        out = project.root / "build/test"
        project.compile(out)
        qa = self.read_json(out, "qa.json")
        finding = next(item for item in qa["issues"] if item["code"] == "missing_asset")
        self.assertEqual(finding["locator"]["placement_id"], "nd_asset")
        self.assertEqual(finding["locator"]["sheet_id"], "sh_asset")
        self.assertIsInstance(finding["locator"]["line_start"], int)

    def test_cg007_source_map_covers_every_authored_output_segment(self):
        project = self.make_project()
        project.add_sheet(
            sheet_id="sh_source",
            placement_id="nd_source",
            title="Source",
            body="# Source\n\nParagraph with [link](https://example.invalid).\n\n[^n]: Footnote text.",
        )
        out = project.root / "build/test"
        project.compile(out)
        ast = self.read_json(out, "workbench-ast.json")
        source_map = self.read_json(out, "source-map.json")
        by_id = {segment["segment_id"]: segment for segment in source_map["segments"]}
        authored = [block for block in ast["blocks"] if block["source_line_start"] is not None]
        self.assertGreater(len(authored), 0)
        for block in authored:
            mapped = by_id[block["segment_id"]]
            self.assertEqual(mapped["placement_id"], "nd_source")
            self.assertEqual(mapped["sheet_id"], "sh_source")
            self.assertTrue(mapped["revision"]["sha256"])
            self.assertIsInstance(mapped["source"]["line_start"], int)
            self.assertIsNotNone(mapped["outputs"]["markdown"])
            self.assertIsNotNone(mapped["outputs"]["html"])

    def test_cg008_repeated_frozen_compile_is_semantically_equivalent(self):
        project = self.make_project()
        project.add_sheet(
            sheet_id="sh_repeat",
            placement_id="nd_repeat",
            title="Repeat",
            body="# Repeat\n\nSame input, same meaning.",
        )
        left = project.root / "build/left"
        right = project.root / "build/right"
        project.compile(left)
        project.compile(right)
        comparison = compile_spike.compare_bundles(left, right)
        self.assertTrue(comparison["direct_all_equal"], comparison)

    def test_cg009_unavailable_pandoc_preserves_constellation_fallbacks(self):
        project = self.make_project()
        project.add_sheet(
            sheet_id="sh_adapter",
            placement_id="nd_adapter",
            title="Adapter",
            body="# Adapter\n\nFallback survives.",
        )
        out = project.root / "build/test"
        receipt = project.compile(out, pandoc_path=str(project.root / "definitely-not-pandoc"))
        self.assertEqual(receipt["status"], "passed")
        self.assertTrue(receipt["fallbacks_valid_without_adapter"])
        self.assertTrue((out / "compile-plan.json").exists())
        self.assertTrue((out / "workbench-ast.json").exists())
        self.assertTrue((out / "output.md").exists())
        self.assertTrue((out / "output.html").exists())
        self.assertTrue((out / "source-map.json").exists())
        self.assertEqual({r["status"] for r in receipt["adapter_records"]}, {"unavailable"})

    def test_profile_cannot_override_manifest_structure_or_role(self):
        project = self.make_project()
        project.add_sheet(
            sheet_id="sh_authority",
            placement_id="nd_authority",
            title="Authority",
            body="# Authority\n\nManifest owns assembly.",
            role="scene",
        )
        out = project.root / "build/test"
        receipt = project.compile(
            out,
            profile_overrides={"role_overrides": {"nd_authority": "chapter"}},
        )
        qa = self.read_json(out, "qa.json")
        plan = self.read_json(out, "compile-plan.json")
        self.assertEqual(receipt["status"], "blocked")
        self.assertTrue(any(item["code"] == "forbidden_profile_structure_override" for item in qa["issues"]))
        selected = next(item for item in plan["selected_placements"] if item["placement_id"] == "nd_authority")
        self.assertEqual(selected["role"], "scene")

    def test_profile_scope_selects_projection_without_mutating_assembly(self):
        project = self.make_project()
        project.add_sheet(
            sheet_id="sh_scene",
            placement_id="nd_scene",
            title="Scene",
            body="# Scene\n\nScene body.",
            role="scene",
        )
        project.add_sheet(
            sheet_id="sh_appendix",
            placement_id="nd_appendix",
            title="Appendix",
            body="# Appendix\n\nAppendix body.",
            role="appendix",
        )
        out = project.root / "build/test"
        project.compile(out, profile_overrides={"scope": {"include_roles": ["scene"]}})
        plan = self.read_json(out, "compile-plan.json")
        appendix = next(item for item in plan["excluded_placements"] if item["placement_id"] == "nd_appendix")
        self.assertTrue(appendix["assembly_include"])
        self.assertFalse(appendix["export_selected"])
        self.assertEqual(appendix["reason"], "profile_scope_role_not_selected")

    def test_unsupported_extension_is_visible_qa_not_silent_loss(self):
        project = self.make_project()
        project.add_sheet(
            sheet_id="sh_extension",
            placement_id="nd_extension",
            title="Extension",
            body="# Extension\n\n::: note\nUnsupported fenced div.",
        )
        out = project.root / "build/test"
        project.compile(out)
        qa = self.read_json(out, "qa.json")
        self.assertTrue(any(item["code"] == "unsupported_markdown_extension" for item in qa["issues"]))
        self.assertIn("::: note", (out / "output.md").read_text(encoding="utf-8"))

    def test_asset_path_escape_is_a_hard_gate(self):
        project = self.make_project()
        project.add_sheet(
            sheet_id="sh_escape",
            placement_id="nd_escape",
            title="Escape",
            body="# Escape\n\n![Nope](../outside.png)",
        )
        out = project.root / "build/test"
        receipt = project.compile(out)
        qa = self.read_json(out, "qa.json")
        self.assertEqual(receipt["status"], "blocked")
        self.assertTrue(any(item["code"] == "asset_path_escape" for item in qa["issues"]))

    def test_review_regression_inline_comment_preserves_surrounding_prose(self):
        project = self.make_project()
        project.add_sheet(
            sheet_id="sh_inline_comment",
            placement_id="nd_inline_comment",
            title="Inline Comment",
            body="# Inline Comment\n\nBefore <!-- private note --> after.",
        )
        out = project.root / "build/test"
        receipt = project.compile(out)
        rendered = (out / "output.md").read_text(encoding="utf-8")
        qa = self.read_json(out, "qa.json")
        self.assertEqual(receipt["status"], "passed")
        self.assertIn("Before", rendered)
        self.assertIn("after.", rendered)
        self.assertNotIn("private note", rendered)
        self.assertTrue(any(item["code"] == "comment_excluded" for item in qa["issues"]))

    def test_review_regression_structural_nodes_survive_into_ast(self):
        project = self.make_project()
        project.nodes.append(
            {
                "id": "nd_part",
                "type": "container",
                "title": "Part One",
                "include": True,
                "role": "part",
                "children": [],
            }
        )
        project.nodes.append(
            {
                "id": "nd_generated",
                "type": "generated",
                "title": "Contents",
                "include": True,
                "role": "frontmatter",
                "generator": "toc",
                "children": [],
            }
        )
        out = project.root / "build/test"
        receipt = project.compile(out)
        ast = self.read_json(out, "workbench-ast.json")
        kinds = {block["kind"] for block in ast["blocks"]}
        rendered = (out / "output.md").read_text(encoding="utf-8")
        self.assertEqual(receipt["status"], "passed")
        self.assertIn("structure_title", kinds)
        self.assertIn("generated_structure", kinds)
        self.assertIn("Part One", rendered)
        self.assertIn("Contents", rendered)

    def test_review_regression_duplicate_placement_id_is_hard_gate(self):
        project = self.make_project()
        project.add_sheet(
            sheet_id="sh_one",
            placement_id="nd_duplicate",
            title="One",
            body="# One\n\nOne.",
        )
        project.add_sheet(
            sheet_id="sh_two",
            placement_id="nd_duplicate",
            title="Two",
            body="# Two\n\nTwo.",
        )
        out = project.root / "build/test"
        receipt = project.compile(out)
        qa = self.read_json(out, "qa.json")
        self.assertEqual(receipt["status"], "blocked")
        self.assertTrue(any(item["code"] == "duplicate_placement_id" for item in qa["issues"]))

    def test_review_regression_profile_must_bind_selected_manuscript(self):
        project = self.make_project()
        project.add_sheet(
            sheet_id="sh_bound",
            placement_id="nd_bound",
            title="Bound",
            body="# Bound\n\nBound manuscript.",
        )
        out = project.root / "build/test"
        receipt = project.compile(out, profile_overrides={"manuscript_id": "ms_other"})
        qa = self.read_json(out, "qa.json")
        self.assertEqual(receipt["status"], "blocked")
        self.assertTrue(any(item["code"] == "profile_manuscript_mismatch" for item in qa["issues"]))

    def test_review_regression_assets_are_content_frozen_for_adapter_input(self):
        project = self.make_project()
        asset = project.root / "assets/cover.png"
        asset.parent.mkdir(parents=True, exist_ok=True)
        asset_bytes = b"not-a-real-png-but-deterministic-fixture"
        asset.write_bytes(asset_bytes)
        project.add_sheet(
            sheet_id="sh_asset_freeze",
            placement_id="nd_asset_freeze",
            title="Asset Freeze",
            body="# Asset Freeze\n\n![Cover](assets/cover.png)",
        )
        out = project.root / "build/test"
        receipt = project.compile(out)
        plan = self.read_json(out, "compile-plan.json")
        direct = (out / "output.md").read_text(encoding="utf-8")
        adapter = (out / "adapter-input.md").read_text(encoding="utf-8")
        expected_digest = hashlib.sha256(asset_bytes).hexdigest()
        frozen = [item for item in plan["frozen_inputs"] if item.get("kind") == "asset"]
        self.assertEqual(receipt["status"], "passed")
        self.assertEqual(len(frozen), 1)
        self.assertEqual(frozen[0]["sha256"], expected_digest)
        self.assertIn("assets/cover.png", direct)
        self.assertIn("frozen-assets/", adapter)
        self.assertNotIn("assets/cover.png", adapter)
        staged = list((out / "frozen-assets").iterdir())
        self.assertEqual(len(staged), 1)
        self.assertEqual(staged[0].read_bytes(), asset_bytes)

    def test_review_regression_role_treatments_are_rendered(self):
        project = self.make_project()
        project.add_sheet(
            sheet_id="sh_role",
            placement_id="nd_role",
            title="Role Treatment",
            role="chapter",
            body="# Role Treatment\n\nBody.",
        )
        out = project.root / "build/test"
        receipt = project.compile(
            out,
            profile_overrides={"role_transforms": {"chapter": "heading_2", "scene": "concatenate_with_scene_break"}},
        )
        rendered_md = (out / "output.md").read_text(encoding="utf-8")
        rendered_html = (out / "output.html").read_text(encoding="utf-8")
        self.assertEqual(receipt["status"], "passed")
        self.assertIn("## Role Treatment", rendered_md)
        self.assertNotIn("# Role Treatment\n", rendered_md.replace("## Role Treatment\n", ""))
        self.assertIn(">Role Treatment</h2>", rendered_html)


if __name__ == "__main__":
    unittest.main()
