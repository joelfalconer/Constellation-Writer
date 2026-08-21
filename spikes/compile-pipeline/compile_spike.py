#!/usr/bin/env python3
"""Bounded compile architecture spike for Constellation Writer issue #5.

This is intentionally not a production Markdown parser. Its purpose is to prove
or falsify architecture boundaries:

- Manuscript Manifest owns assembly order, membership and semantic role.
- Compile Profile may select an export scope and map semantics to rendering.
- Workbench owns frozen inputs, semantic segments, QA and source maps.
- Pandoc is an optional pinned output adapter, never the canonical compiler.

The spike is dependency-light except for PyYAML, already used by repository
validation. It is safe to run without Pandoc; direct Markdown/HTML fallbacks and
all Constellation-owned evidence still materialize.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Any, Iterable

import yaml

SPIKE_VERSION = "0.1.0"
SCHEMA_PLAN = "cw_compile_plan_spike_v1"
SCHEMA_AST = "cw_workbench_ast_spike_v1"
SCHEMA_QA = "cw_compile_qa_spike_v1"
SCHEMA_SOURCE_MAP = "cw_compile_source_map_spike_v1"
SCHEMA_RECEIPT = "cw_compile_receipt_spike_v1"

HEADER_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
IMAGE_RE = re.compile(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$")
FOOTNOTE_DEF_RE = re.compile(r"^\[\^([^\]]+)\]:\s*(.*)$")
CITATION_RE = re.compile(r"\[@([A-Za-z0-9_.:+-]+)\]")
FOOTNOTE_REF_RE = re.compile(r"\[\^([^\]]+)\]")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
STRONG_RE = re.compile(r"\*\*([^*]+)\*\*")
EM_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")

FORBIDDEN_PROFILE_KEYS = {
    "assembly_overrides",
    "order_overrides",
    "role_overrides",
    "membership_overrides",
}

ALWAYS_BLOCKING_CODES = {
    "invalid_manifest",
    "invalid_profile",
    "missing_included_sheet",
    "duplicate_sheet_id",
    "sheet_id_mismatch",
    "sheet_path_escape",
    "asset_path_escape",
    "forbidden_profile_structure_override",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def semantic_digest(value: Any) -> str:
    return sha256_text(canonical_json(value))


def normalize_plain_text(value: str) -> str:
    return " ".join(value.replace("\r\n", "\n").replace("\r", "\n").split())


def ensure_within(root: Path, candidate: Path) -> Path:
    root_resolved = root.resolve()
    candidate_resolved = candidate.resolve()
    if candidate_resolved == root_resolved or root_resolved in candidate_resolved.parents:
        return candidate_resolved
    raise ValueError(f"path escapes root: {candidate}")


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def qa_issue(
    code: str,
    severity: str,
    message: str,
    *,
    placement_id: str | None = None,
    sheet_id: str | None = None,
    source_path: str | None = None,
    line_start: int | None = None,
    line_end: int | None = None,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    issue = {
        "code": code,
        "severity": severity,
        "message": message,
    }
    locator = {
        key: value
        for key, value in {
            "placement_id": placement_id,
            "sheet_id": sheet_id,
            "source_path": source_path,
            "line_start": line_start,
            "line_end": line_end,
        }.items()
        if value is not None
    }
    if locator:
        issue["locator"] = locator
    if details:
        issue["details"] = details
    return issue


def parse_frontmatter(text: str) -> tuple[dict[str, Any], list[str], int]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, lines, 1
    closing = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing = index
            break
    if closing is None:
        raise ValueError("unterminated YAML frontmatter")
    metadata = yaml.safe_load("\n".join(lines[1:closing])) or {}
    if not isinstance(metadata, dict):
        raise ValueError("frontmatter must be a mapping")
    body = lines[closing + 1 :]
    body_first_line = closing + 2
    return metadata, body, body_first_line


def scan_sheet_registry(project_root: Path, qa: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    registry: dict[str, dict[str, Any]] = {}
    sheets_root = ensure_within(project_root, project_root / "sheets")
    if not sheets_root.exists():
        return registry

    for path in sorted(sheets_root.rglob("*.md")):
        try:
            safe_path = ensure_within(sheets_root, path)
            raw = safe_path.read_bytes()
            text = raw.decode("utf-8")
            metadata, _, _ = parse_frontmatter(text)
            sheet_id = metadata.get("id")
            if not sheet_id:
                continue
            if sheet_id in registry:
                qa.append(
                    qa_issue(
                        "duplicate_sheet_id",
                        "error",
                        f"duplicate Sheet ID {sheet_id}",
                        sheet_id=sheet_id,
                        source_path=str(path.relative_to(project_root)),
                        details={"other_path": registry[sheet_id]["relative_path"]},
                    )
                )
                continue
            registry[sheet_id] = {
                "path": safe_path,
                "relative_path": str(safe_path.relative_to(project_root)).replace("\\", "/"),
                "bytes": raw,
                "text": text,
                "metadata": metadata,
                "sha256": sha256_bytes(raw),
            }
        except Exception as exc:
            qa.append(
                qa_issue(
                    "sheet_scan_failed",
                    "error",
                    f"failed to scan {path}: {exc}",
                    source_path=str(path.relative_to(project_root)),
                )
            )
    return registry


def profile_scope_select(node: dict[str, Any], profile: dict[str, Any]) -> tuple[bool, str | None]:
    scope = profile.get("scope") or {}
    if not isinstance(scope, dict):
        return False, "invalid_profile_scope"
    role = node.get("role") or "section"
    placement_id = node.get("id")

    include_roles = set(scope.get("include_roles") or [])
    exclude_roles = set(scope.get("exclude_roles") or [])
    include_placements = set(scope.get("include_placement_ids") or [])
    exclude_placements = set(scope.get("exclude_placement_ids") or [])

    if include_roles and role not in include_roles:
        return False, "profile_scope_role_not_selected"
    if role in exclude_roles:
        return False, "profile_scope_role_excluded"
    if include_placements and placement_id not in include_placements:
        return False, "profile_scope_placement_not_selected"
    if placement_id in exclude_placements:
        return False, "profile_scope_placement_excluded"
    return True, None


def resolve_manifest(
    manifest: dict[str, Any],
    profile: dict[str, Any],
    qa: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    for key in sorted(FORBIDDEN_PROFILE_KEYS):
        if key in profile:
            qa.append(
                qa_issue(
                    "forbidden_profile_structure_override",
                    "error",
                    f"Compile Profile may not define {key}; manuscript assembly authority remains in the manifest",
                    details={"key": key},
                )
            )

    root_nodes = manifest.get("root_nodes")
    if not isinstance(root_nodes, list):
        qa.append(qa_issue("invalid_manifest", "error", "root_nodes must be an array"))
        return [], []

    selected: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []

    def visit(node: dict[str, Any], parent_included: bool = True) -> None:
        if not isinstance(node, dict):
            qa.append(qa_issue("invalid_manifest", "error", "manifest node must be an object"))
            return

        placement_id = node.get("id")
        node_type = node.get("type")
        explicit_include = node.get("include")
        if explicit_include is None:
            assembly_include = parent_included
        elif isinstance(explicit_include, bool):
            assembly_include = parent_included and explicit_include
        else:
            qa.append(
                qa_issue(
                    "invalid_manifest",
                    "error",
                    f"placement {placement_id} include must be boolean or absent",
                    placement_id=placement_id,
                )
            )
            assembly_include = False

        export_selected = False
        scope_reason = None
        if assembly_include:
            export_selected, scope_reason = profile_scope_select(node, profile)
            if scope_reason == "invalid_profile_scope":
                qa.append(qa_issue("invalid_profile", "error", "profile scope must be a mapping"))

        record = {
            "placement_id": placement_id,
            "type": node_type,
            "sheet_id": node.get("sheet_id"),
            "title": node.get("title"),
            "role": node.get("role") or "section",
            "assembly_include": assembly_include,
            "export_selected": export_selected,
        }

        if node_type == "sheet_ref":
            if assembly_include and export_selected:
                selected.append(record)
            else:
                reason = "manifest_excluded" if not assembly_include else scope_reason or "profile_scope_excluded"
                excluded.append({**record, "reason": reason})
        elif node_type in {"container", "generated", "asset_ref", "placeholder"}:
            if not assembly_include or not export_selected:
                excluded.append({**record, "reason": "manifest_excluded" if not assembly_include else scope_reason or "structural_node"})
        else:
            qa.append(
                qa_issue(
                    "unsupported_manifest_node_type",
                    "warning",
                    f"unsupported manifest node type {node_type!r}",
                    placement_id=placement_id,
                )
            )

        for child in node.get("children") or []:
            visit(child, assembly_include)

    for node in root_nodes:
        visit(node)

    for ordinal, item in enumerate(selected):
        item["ordinal"] = ordinal
    return selected, excluded


def make_segment_id(placement_id: str, ordinal: int, kind: str) -> str:
    raw = f"{placement_id}:{ordinal}:{kind}"
    return "seg_" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


def parse_sheet_blocks(
    placement: dict[str, Any],
    sheet: dict[str, Any],
    project_root: Path,
    profile: dict[str, Any],
    qa: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    try:
        metadata, lines, first_line = parse_frontmatter(sheet["text"])
    except Exception as exc:
        qa.append(
            qa_issue(
                "invalid_sheet_frontmatter",
                "error",
                f"failed to parse Sheet frontmatter: {exc}",
                placement_id=placement["placement_id"],
                sheet_id=placement["sheet_id"],
                source_path=sheet["relative_path"],
            )
        )
        return []

    if metadata.get("id") != placement.get("sheet_id"):
        qa.append(
            qa_issue(
                "sheet_id_mismatch",
                "error",
                "Sheet frontmatter ID does not match manifest reference",
                placement_id=placement["placement_id"],
                sheet_id=placement["sheet_id"],
                source_path=sheet["relative_path"],
                details={"frontmatter_id": metadata.get("id")},
            )
        )

    blocks: list[dict[str, Any]] = []
    paragraph: list[str] = []
    paragraph_start: int | None = None
    comment_buffer: list[str] = []
    comment_start: int | None = None
    in_comment = False
    in_code_fence = False
    code_fence_marker = None
    code_buffer: list[str] = []
    code_start: int | None = None

    def append_block(kind: str, data: dict[str, Any], line_start: int | None, line_end: int | None) -> None:
        ordinal = len(blocks)
        blocks.append(
            {
                "segment_id": make_segment_id(placement["placement_id"], ordinal, kind),
                "kind": kind,
                "placement_id": placement["placement_id"],
                "sheet_id": placement["sheet_id"],
                "revision_sha256": sheet["sha256"],
                "source_path": sheet["relative_path"],
                "source_line_start": line_start,
                "source_line_end": line_end,
                "role": placement["role"],
                **data,
            }
        )

    def flush_paragraph(line_end: int | None) -> None:
        nonlocal paragraph, paragraph_start
        if paragraph:
            text = "\n".join(paragraph).strip()
            if text:
                append_block(
                    "paragraph",
                    {
                        "text": text,
                        "citation_keys": sorted(set(CITATION_RE.findall(text))),
                        "footnote_refs": sorted(set(FOOTNOTE_REF_RE.findall(text))),
                    },
                    paragraph_start,
                    line_end,
                )
        paragraph = []
        paragraph_start = None

    for offset, raw_line in enumerate(lines):
        line_no = first_line + offset
        line = raw_line.rstrip("\n")
        stripped = line.strip()

        if in_comment:
            comment_buffer.append(line)
            if "-->" in line:
                in_comment = False
                if profile.get("include_comments", False):
                    append_block("comment", {"text": "\n".join(comment_buffer)}, comment_start, line_no)
                else:
                    qa.append(
                        qa_issue(
                            "comment_excluded",
                            "info",
                            "comment excluded by compile profile",
                            placement_id=placement["placement_id"],
                            sheet_id=placement["sheet_id"],
                            source_path=sheet["relative_path"],
                            line_start=comment_start,
                            line_end=line_no,
                        )
                    )
                comment_buffer = []
                comment_start = None
            continue

        if in_code_fence:
            code_buffer.append(line)
            if stripped.startswith(code_fence_marker or "```"):
                in_code_fence = False
                append_block(
                    "code_block",
                    {"text": "\n".join(code_buffer[1:-1]), "fence": code_fence_marker},
                    code_start,
                    line_no,
                )
                code_buffer = []
                code_start = None
                code_fence_marker = None
            continue

        if "<!--" in line:
            flush_paragraph(line_no - 1)
            in_comment = True
            comment_start = line_no
            comment_buffer = [line]
            if "-->" in line[line.index("<!--") + 4 :]:
                in_comment = False
                if profile.get("include_comments", False):
                    append_block("comment", {"text": line}, line_no, line_no)
                else:
                    qa.append(
                        qa_issue(
                            "comment_excluded",
                            "info",
                            "comment excluded by compile profile",
                            placement_id=placement["placement_id"],
                            sheet_id=placement["sheet_id"],
                            source_path=sheet["relative_path"],
                            line_start=line_no,
                            line_end=line_no,
                        )
                    )
                comment_buffer = []
                comment_start = None
            continue

        if stripped.startswith("```") or stripped.startswith("~~~"):
            flush_paragraph(line_no - 1)
            in_code_fence = True
            code_fence_marker = stripped[:3]
            code_start = line_no
            code_buffer = [line]
            continue

        if not stripped:
            flush_paragraph(line_no - 1)
            continue

        header = HEADER_RE.match(line)
        if header:
            flush_paragraph(line_no - 1)
            append_block(
                "heading",
                {"level": len(header.group(1)), "text": header.group(2).strip()},
                line_no,
                line_no,
            )
            continue

        footnote = FOOTNOTE_DEF_RE.match(line)
        if footnote:
            flush_paragraph(line_no - 1)
            append_block(
                "footnote_definition",
                {"label": footnote.group(1), "text": footnote.group(2)},
                line_no,
                line_no,
            )
            continue

        image = IMAGE_RE.match(line)
        if image:
            flush_paragraph(line_no - 1)
            alt, target = image.groups()
            append_block("image", {"alt": alt, "target": target}, line_no, line_no)
            continue

        if stripped.startswith(":::"):
            flush_paragraph(line_no - 1)
            append_block("unsupported", {"text": line, "syntax": "fenced_div"}, line_no, line_no)
            qa.append(
                qa_issue(
                    "unsupported_markdown_extension",
                    "warning",
                    "fenced div syntax is outside the spike Workbench AST",
                    placement_id=placement["placement_id"],
                    sheet_id=placement["sheet_id"],
                    source_path=sheet["relative_path"],
                    line_start=line_no,
                    line_end=line_no,
                    details={"syntax": "fenced_div"},
                )
            )
            continue

        if stripped.startswith("<") and stripped.endswith(">"):
            flush_paragraph(line_no - 1)
            append_block("unsupported", {"text": line, "syntax": "raw_html"}, line_no, line_no)
            qa.append(
                qa_issue(
                    "unsupported_markdown_extension",
                    "warning",
                    "raw HTML is outside the spike Workbench AST",
                    placement_id=placement["placement_id"],
                    sheet_id=placement["sheet_id"],
                    source_path=sheet["relative_path"],
                    line_start=line_no,
                    line_end=line_no,
                    details={"syntax": "raw_html"},
                )
            )
            continue

        if paragraph_start is None:
            paragraph_start = line_no
        paragraph.append(line)

    flush_paragraph(first_line + len(lines) - 1)

    if in_comment:
        qa.append(
            qa_issue(
                "unterminated_comment",
                "warning",
                "unterminated HTML comment",
                placement_id=placement["placement_id"],
                sheet_id=placement["sheet_id"],
                source_path=sheet["relative_path"],
                line_start=comment_start,
            )
        )
    if in_code_fence:
        qa.append(
            qa_issue(
                "unterminated_code_fence",
                "warning",
                "unterminated code fence",
                placement_id=placement["placement_id"],
                sheet_id=placement["sheet_id"],
                source_path=sheet["relative_path"],
                line_start=code_start,
            )
        )

    # Title de-duplication law: a manifest placement title is contextual assembly
    # metadata. If the first authored heading already expresses that title, do not
    # synthesize a second heading. If a chapter/front/back-matter placement has no
    # matching heading, synthesize one from the manifest and mark provenance.
    title = placement.get("title")
    first_authored_heading = next((block for block in blocks if block["kind"] == "heading"), None)
    roles_requiring_visible_title = {
        "chapter",
        "part",
        "frontmatter",
        "backmatter",
        "title_page",
        "appendix",
        "preface",
        "acknowledgements",
    }
    if title and placement.get("role") in roles_requiring_visible_title:
        if not first_authored_heading or first_authored_heading.get("text") != title:
            generated = {
                "segment_id": make_segment_id(placement["placement_id"], 999999, "generated_title"),
                "kind": "generated_title",
                "placement_id": placement["placement_id"],
                "sheet_id": placement["sheet_id"],
                "revision_sha256": sheet["sha256"],
                "source_path": sheet["relative_path"],
                "source_line_start": None,
                "source_line_end": None,
                "role": placement["role"],
                "level": 1,
                "text": title,
                "provenance": "manifest_placement_title",
            }
            blocks.insert(0, generated)

    # Validate asset references after all blocks exist.
    for block in blocks:
        if block["kind"] != "image":
            continue
        target = block["target"]
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
            continue
        target_path = project_root / target
        try:
            safe_asset = ensure_within(project_root, target_path)
        except ValueError:
            qa.append(
                qa_issue(
                    "asset_path_escape",
                    "error",
                    f"asset path escapes project root: {target}",
                    placement_id=block["placement_id"],
                    sheet_id=block["sheet_id"],
                    source_path=block["source_path"],
                    line_start=block["source_line_start"],
                    line_end=block["source_line_end"],
                )
            )
            continue
        if not safe_asset.exists():
            qa.append(
                qa_issue(
                    "missing_asset",
                    "warning",
                    f"referenced asset does not exist: {target}",
                    placement_id=block["placement_id"],
                    sheet_id=block["sheet_id"],
                    source_path=block["source_path"],
                    line_start=block["source_line_start"],
                    line_end=block["source_line_end"],
                    details={"asset": target},
                )
            )

    return blocks


def build_workbench_ast(
    selected: list[dict[str, Any]],
    sheet_registry: dict[str, dict[str, Any]],
    project_root: Path,
    profile: dict[str, Any],
    qa: list[dict[str, Any]],
) -> dict[str, Any]:
    blocks: list[dict[str, Any]] = []
    previous_role: str | None = None
    previous_placement: str | None = None

    for placement in selected:
        sheet_id = placement.get("sheet_id")
        sheet = sheet_registry.get(sheet_id)
        if not sheet:
            qa.append(
                qa_issue(
                    "missing_included_sheet",
                    "error",
                    f"included Sheet {sheet_id} is missing",
                    placement_id=placement.get("placement_id"),
                    sheet_id=sheet_id,
                )
            )
            continue

        if previous_role == "scene" and placement.get("role") == "scene":
            break_id = make_segment_id(placement["placement_id"], -1, "scene_break")
            blocks.append(
                {
                    "segment_id": break_id,
                    "kind": "scene_break",
                    "placement_id": placement["placement_id"],
                    "sheet_id": sheet_id,
                    "revision_sha256": sheet["sha256"],
                    "source_path": sheet["relative_path"],
                    "source_line_start": None,
                    "source_line_end": None,
                    "role": "scene_break",
                    "provenance": {
                        "kind": "manifest_semantic_boundary",
                        "between": [previous_placement, placement["placement_id"]],
                    },
                }
            )

        blocks.extend(parse_sheet_blocks(placement, sheet, project_root, profile, qa))
        previous_role = placement.get("role")
        previous_placement = placement.get("placement_id")

    return {
        "schema": SCHEMA_AST,
        "spike_version": SPIKE_VERSION,
        "blocks": blocks,
    }


def render_inline(value: str) -> str:
    escaped = html.escape(value, quote=False)
    escaped = LINK_RE.sub(lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>', escaped)
    escaped = STRONG_RE.sub(r"<strong>\1</strong>", escaped)
    escaped = EM_RE.sub(r"<em>\1</em>", escaped)
    escaped = CITATION_RE.sub(lambda m: f'<span class="citation" data-key="{html.escape(m.group(1))}">[@{html.escape(m.group(1))}]</span>', escaped)
    escaped = FOOTNOTE_REF_RE.sub(lambda m: f'<sup class="footnote-ref" data-label="{html.escape(m.group(1))}">[{html.escape(m.group(1))}]</sup>', escaped)
    return escaped.replace("\n", "<br>\n")


def render_markdown(ast: dict[str, Any]) -> tuple[str, dict[str, dict[str, Any]]]:
    chunks: list[str] = []
    locators: dict[str, dict[str, Any]] = {}
    cursor = 0

    for block in ast["blocks"]:
        kind = block["kind"]
        if kind in {"heading", "generated_title"}:
            rendered = "#" * int(block.get("level", 1)) + " " + block.get("text", "")
        elif kind == "paragraph":
            rendered = block.get("text", "")
        elif kind == "footnote_definition":
            rendered = f"[^{block['label']}]: {block.get('text', '')}"
        elif kind == "image":
            rendered = f"![{block.get('alt', '')}]({block.get('target', '')})"
        elif kind == "scene_break":
            rendered = "* * *"
        elif kind == "code_block":
            rendered = "```\n" + block.get("text", "") + "\n```"
        elif kind == "comment":
            rendered = block.get("text", "")
        else:
            rendered = block.get("text", "")

        if chunks:
            separator = "\n\n"
            chunks.append(separator)
            cursor += len(separator)
        start = cursor
        chunks.append(rendered)
        cursor += len(rendered)
        locators[block["segment_id"]] = {
            "kind": "character_span",
            "start": start,
            "end": cursor,
        }

    text = "".join(chunks).rstrip() + "\n"
    return text, locators


def render_html(ast: dict[str, Any], title: str, standalone: bool = True) -> tuple[str, dict[str, dict[str, Any]]]:
    body_chunks: list[str] = []
    locators: dict[str, dict[str, Any]] = {}
    cursor = 0

    for block in ast["blocks"]:
        segment_id = block["segment_id"]
        kind = block["kind"]
        sid = html.escape(segment_id, quote=True)
        if kind in {"heading", "generated_title"}:
            level = int(block.get("level", 1))
            rendered = f'<h{level} id="{sid}">{render_inline(block.get("text", ""))}</h{level}>'
        elif kind == "paragraph":
            rendered = f'<p id="{sid}">{render_inline(block.get("text", ""))}</p>'
        elif kind == "footnote_definition":
            rendered = f'<aside id="{sid}" class="footnote" data-label="{html.escape(block["label"], quote=True)}">{render_inline(block.get("text", ""))}</aside>'
        elif kind == "image":
            rendered = f'<figure id="{sid}"><img src="{html.escape(block.get("target", ""), quote=True)}" alt="{html.escape(block.get("alt", ""), quote=True)}"></figure>'
        elif kind == "scene_break":
            rendered = f'<hr id="{sid}" class="scene-break">'
        elif kind == "code_block":
            rendered = f'<pre id="{sid}"><code>{html.escape(block.get("text", ""))}</code></pre>'
        elif kind == "comment":
            rendered = f'<!-- {html.escape(block.get("text", ""))} -->'
        else:
            rendered = f'<pre id="{sid}" class="unsupported">{html.escape(block.get("text", ""))}</pre>'

        if body_chunks:
            body_chunks.append("\n")
            cursor += 1
        start = cursor
        body_chunks.append(rendered)
        cursor += len(rendered)
        locators[segment_id] = {
            "kind": "character_span_in_html_body",
            "start": start,
            "end": cursor,
        }

    body = "".join(body_chunks)
    if standalone:
        document = (
            "<!doctype html>\n<html><head><meta charset=\"utf-8\">"
            f"<title>{html.escape(title)}</title></head><body>\n{body}\n</body></html>\n"
        )
    else:
        document = body + "\n"
    return document, locators


def source_map_for(ast: dict[str, Any], markdown_locators: dict[str, Any], html_locators: dict[str, Any]) -> dict[str, Any]:
    segments = []
    for ordinal, block in enumerate(ast["blocks"]):
        segments.append(
            {
                "ordinal": ordinal,
                "segment_id": block["segment_id"],
                "semantic_kind": block["kind"],
                "placement_id": block.get("placement_id"),
                "sheet_id": block.get("sheet_id"),
                "revision": {
                    "kind": "frozen_content_digest",
                    "sha256": block.get("revision_sha256"),
                },
                "source": {
                    "path": block.get("source_path"),
                    "line_start": block.get("source_line_start"),
                    "line_end": block.get("source_line_end"),
                },
                "outputs": {
                    "markdown": markdown_locators.get(block["segment_id"]),
                    "html": html_locators.get(block["segment_id"]),
                    "adapter": {
                        "kind": "semantic_segment_ordinal",
                        "ordinal": ordinal,
                        "segment_id": block["segment_id"],
                    },
                },
            }
        )
    return {"schema": SCHEMA_SOURCE_MAP, "spike_version": SPIKE_VERSION, "segments": segments}


def pandoc_version(pandoc_path: str) -> str:
    completed = subprocess.run(
        [pandoc_path, "--version"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return completed.stdout.splitlines()[0].strip()


def run_pandoc_adapter(
    pandoc_path: str,
    markdown_path: Path,
    project_root: Path,
    output_path: Path,
    target: str,
    qa: list[dict[str, Any]],
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "target": target,
        "requested_binary": pandoc_path,
        "status": "not_run",
    }
    env = os.environ.copy()
    env.setdefault("SOURCE_DATE_EPOCH", "946684800")  # 2000-01-01 UTC

    try:
        version = pandoc_version(pandoc_path)
        record["version"] = version
        output_path.parent.mkdir(parents=True, exist_ok=True)
        to_format = "epub3" if target == "epub" else target
        command = [
            pandoc_path,
            str(markdown_path),
            "--from=markdown+footnotes+citations",
            f"--to={to_format}",
            "--standalone",
            f"--resource-path={project_root}",
            "--output",
            str(output_path),
        ]
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
        )
        record["command"] = ["pandoc", *command[1:]]
        record["stderr"] = completed.stderr.strip()
        record["returncode"] = completed.returncode
        if completed.returncode != 0:
            record["status"] = "failed"
            qa.append(
                qa_issue(
                    "pandoc_adapter_failed",
                    "warning",
                    f"Pandoc adapter failed for {target}; Constellation-owned fallbacks remain valid",
                    details={"returncode": completed.returncode, "stderr": completed.stderr.strip(), "target": target},
                )
            )
            return record

        record["status"] = "passed"
        record["artifact_sha256"] = sha256_bytes(output_path.read_bytes())

        roundtrip = subprocess.run(
            [pandoc_path, str(output_path), "--to=plain"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
        )
        record["roundtrip_returncode"] = roundtrip.returncode
        if roundtrip.returncode == 0:
            normalized = normalize_plain_text(roundtrip.stdout)
            record["roundtrip_plain_sha256"] = sha256_text(normalized)
            record["roundtrip_plain"] = normalized
        else:
            qa.append(
                qa_issue(
                    "pandoc_roundtrip_failed",
                    "warning",
                    f"Pandoc could not round-trip {target} output for semantic comparison",
                    details={"stderr": roundtrip.stderr.strip(), "target": target},
                )
            )
        return record
    except (FileNotFoundError, PermissionError, subprocess.SubprocessError, OSError) as exc:
        record["status"] = "unavailable"
        record["error"] = str(exc)
        qa.append(
            qa_issue(
                "pandoc_adapter_failed",
                "warning",
                f"Pandoc adapter unavailable for {target}; Constellation-owned fallbacks remain valid",
                details={"error": str(exc), "target": target},
            )
        )
        return record


def blocking_issues(qa: list[dict[str, Any]], profile: dict[str, Any]) -> list[dict[str, Any]]:
    fail_on = set(profile.get("fail_on") or [])
    blocked = []
    for issue in qa:
        if issue["code"] in ALWAYS_BLOCKING_CODES or issue["code"] in fail_on:
            blocked.append(issue)
    return blocked


def compile_project(
    project_root: Path,
    manifest_path: Path,
    profile_path: Path,
    output_dir: Path,
    pandoc_path: str | None = None,
) -> dict[str, Any]:
    project_root = project_root.resolve()
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    qa: list[dict[str, Any]] = []

    try:
        manifest_path = ensure_within(project_root, manifest_path)
        profile_path = ensure_within(project_root, profile_path)
    except ValueError as exc:
        qa.append(qa_issue("invalid_manifest", "error", str(exc)))
        manifest_path = Path(manifest_path)
        profile_path = Path(profile_path)

    try:
        manifest = load_yaml(manifest_path)
        if not isinstance(manifest, dict):
            raise ValueError("manifest must be a mapping")
    except Exception as exc:
        manifest = {}
        qa.append(qa_issue("invalid_manifest", "error", f"failed to load manifest: {exc}"))

    try:
        profile = load_yaml(profile_path)
        if not isinstance(profile, dict):
            raise ValueError("profile must be a mapping")
    except Exception as exc:
        profile = {}
        qa.append(qa_issue("invalid_profile", "error", f"failed to load profile: {exc}"))

    selected, excluded = resolve_manifest(manifest, profile, qa)
    sheet_registry = scan_sheet_registry(project_root, qa)

    frozen_inputs: list[dict[str, Any]] = []
    for kind, path in (("manuscript_manifest", manifest_path), ("compile_profile", profile_path)):
        if path.exists():
            frozen_inputs.append(
                {
                    "kind": kind,
                    "path": str(path.relative_to(project_root)).replace("\\", "/"),
                    "sha256": sha256_bytes(path.read_bytes()),
                }
            )

    for placement in selected:
        sheet_id = placement.get("sheet_id")
        sheet = sheet_registry.get(sheet_id)
        if sheet:
            placement["revision"] = {"kind": "frozen_content_digest", "sha256": sheet["sha256"]}
            placement["source_path"] = sheet["relative_path"]
            frozen_inputs.append(
                {
                    "kind": "sheet",
                    "sheet_id": sheet_id,
                    "placement_id": placement["placement_id"],
                    "path": sheet["relative_path"],
                    "sha256": sheet["sha256"],
                }
            )

    plan_core = {
        "schema": SCHEMA_PLAN,
        "spike_version": SPIKE_VERSION,
        "manuscript_id": manifest.get("id"),
        "manuscript_title": manifest.get("title"),
        "profile_id": profile.get("id"),
        "profile_target": profile.get("target"),
        "authority": {
            "assembly": "manuscript_manifest",
            "export_scope": "compile_profile_scope_only",
            "semantic_roles": "manuscript_manifest",
            "workbench_ast": "constellation_writer",
            "qa_and_source_map": "constellation_writer",
            "pandoc": "output_adapter_only",
        },
        "frozen_inputs": frozen_inputs,
        "selected_placements": selected,
        "excluded_placements": excluded,
    }
    plan = {**plan_core, "semantic_digest": semantic_digest(plan_core)}

    ast = build_workbench_ast(selected, sheet_registry, project_root, profile, qa)
    ast["semantic_digest"] = semantic_digest(ast["blocks"])

    markdown, markdown_locators = render_markdown(ast)
    html_output, html_locators = render_html(
        ast,
        manifest.get("title") or "Untitled",
        standalone=bool((profile.get("output") or {}).get("standalone", True)),
    )
    source_map = source_map_for(ast, markdown_locators, html_locators)

    write_json(output_dir / "compile-plan.json", plan)
    write_json(output_dir / "workbench-ast.json", ast)
    write_text(output_dir / "output.md", markdown)
    write_text(output_dir / "output.html", html_output)
    write_json(output_dir / "source-map.json", source_map)

    adapter_records: list[dict[str, Any]] = []
    if pandoc_path:
        adapter_records.append(
            run_pandoc_adapter(
                pandoc_path,
                output_dir / "output.md",
                project_root,
                output_dir / "output.docx",
                "docx",
                qa,
            )
        )
        adapter_records.append(
            run_pandoc_adapter(
                pandoc_path,
                output_dir / "output.md",
                project_root,
                output_dir / "output.epub",
                "epub",
                qa,
            )
        )

    blocked = blocking_issues(qa, profile)
    qa_report = {
        "schema": SCHEMA_QA,
        "spike_version": SPIKE_VERSION,
        "issues": qa,
        "counts": {
            "error": sum(1 for item in qa if item["severity"] == "error"),
            "warning": sum(1 for item in qa if item["severity"] == "warning"),
            "info": sum(1 for item in qa if item["severity"] == "info"),
            "blocking": len(blocked),
        },
        "blocking_codes": sorted({item["code"] for item in blocked}),
    }
    write_json(output_dir / "qa.json", qa_report)

    receipt = {
        "schema": SCHEMA_RECEIPT,
        "spike_version": SPIKE_VERSION,
        "status": "blocked" if blocked else "passed",
        "plan_semantic_digest": plan["semantic_digest"],
        "ast_semantic_digest": ast["semantic_digest"],
        "markdown_sha256": sha256_text(markdown),
        "html_sha256": sha256_text(html_output),
        "source_map_sha256": sha256_text(canonical_json(source_map)),
        "adapter_records": adapter_records,
        "fallbacks_valid_without_adapter": True,
        "unresolved": [
            "spike_parser_is_not_production_markdown_parser",
            "binary_source_map_is_semantic_segment_level_not_byte_addressed",
            "citation_bibliography_resolution_is_not_implemented_in_this_spike",
        ],
    }
    write_json(output_dir / "receipt.json", receipt)
    return receipt


def compare_bundles(left: Path, right: Path) -> dict[str, Any]:
    left_receipt = json.loads((left / "receipt.json").read_text(encoding="utf-8"))
    right_receipt = json.loads((right / "receipt.json").read_text(encoding="utf-8"))

    direct_fields = [
        "plan_semantic_digest",
        "ast_semantic_digest",
        "markdown_sha256",
        "html_sha256",
        "source_map_sha256",
    ]
    direct = {field: left_receipt.get(field) == right_receipt.get(field) for field in direct_fields}

    def adapter_index(receipt: dict[str, Any]) -> dict[str, dict[str, Any]]:
        return {record["target"]: record for record in receipt.get("adapter_records") or []}

    left_adapters = adapter_index(left_receipt)
    right_adapters = adapter_index(right_receipt)
    adapter_comparison: dict[str, Any] = {}
    for target in sorted(set(left_adapters) | set(right_adapters)):
        lrec = left_adapters.get(target, {})
        rrec = right_adapters.get(target, {})
        adapter_comparison[target] = {
            "left_version": lrec.get("version"),
            "right_version": rrec.get("version"),
            "left_status": lrec.get("status"),
            "right_status": rrec.get("status"),
            "roundtrip_semantic_equal": (
                lrec.get("roundtrip_plain_sha256") is not None
                and lrec.get("roundtrip_plain_sha256") == rrec.get("roundtrip_plain_sha256")
            ),
            "byte_equal": (
                lrec.get("artifact_sha256") is not None
                and lrec.get("artifact_sha256") == rrec.get("artifact_sha256")
            ),
        }

    result = {
        "schema": "cw_compile_bundle_comparison_spike_v1",
        "direct_equivalence": direct,
        "direct_all_equal": all(direct.values()),
        "adapter_comparison": adapter_comparison,
        "adapter_semantic_all_equal": all(
            item.get("roundtrip_semantic_equal") for item in adapter_comparison.values()
        )
        if adapter_comparison
        else None,
    }
    return result


def cli_compile(args: argparse.Namespace) -> int:
    project_root = Path(args.project)
    manifest = Path(args.manifest)
    profile = Path(args.profile)
    if not manifest.is_absolute():
        manifest = project_root / manifest
    if not profile.is_absolute():
        profile = project_root / profile
    receipt = compile_project(
        project_root,
        manifest,
        profile,
        Path(args.out),
        pandoc_path=args.pandoc,
    )
    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    if receipt["status"] == "blocked" and not args.allow_blocked:
        return 2
    return 0


def cli_compare(args: argparse.Namespace) -> int:
    result = compare_bundles(Path(args.left), Path(args.right))
    if args.out:
        write_json(Path(args.out), result)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not result["direct_all_equal"]:
        return 3
    if args.require_adapter_semantics and result["adapter_semantic_all_equal"] is not True:
        return 4
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    compile_cmd = sub.add_parser("compile", help="freeze and compile one project/manuscript/profile")
    compile_cmd.add_argument("--project", required=True)
    compile_cmd.add_argument("--manifest", required=True)
    compile_cmd.add_argument("--profile", required=True)
    compile_cmd.add_argument("--out", required=True)
    compile_cmd.add_argument("--pandoc")
    compile_cmd.add_argument("--allow-blocked", action="store_true")
    compile_cmd.set_defaults(func=cli_compile)

    compare_cmd = sub.add_parser("compare", help="compare two compile bundles")
    compare_cmd.add_argument("--left", required=True)
    compare_cmd.add_argument("--right", required=True)
    compare_cmd.add_argument("--out")
    compare_cmd.add_argument("--require-adapter-semantics", action="store_true")
    compare_cmd.set_defaults(func=cli_compare)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
