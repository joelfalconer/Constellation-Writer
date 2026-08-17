#!/usr/bin/env python3
"""Deterministic foundation validator for Constellation Writer."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource


class NoDatesSafeLoader(yaml.SafeLoader):
    pass


for ch, resolvers in list(NoDatesSafeLoader.yaml_implicit_resolvers.items()):
    NoDatesSafeLoader.yaml_implicit_resolvers[ch] = [
        item for item in resolvers if item[0] != "tag:yaml.org,2002:timestamp"
    ]


def load_yaml(path: Path) -> Any:
    return yaml.load(path.read_text(encoding="utf-8"), Loader=NoDatesSafeLoader)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_frontmatter(path: Path) -> dict[str, Any] | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    value = yaml.load(text[4:end], Loader=NoDatesSafeLoader)
    return value if isinstance(value, dict) else None


def issue(issues: list[dict[str, Any]], severity: str, code: str, path: Path | str, message: str) -> None:
    issues.append({"severity": severity, "code": code, "path": str(path), "message": message})


def build_registry(schema_root: Path) -> tuple[Registry, dict[str, dict[str, Any]]]:
    registry = Registry()
    schemas: dict[str, dict[str, Any]] = {}
    for path in schema_root.rglob("*.schema.json"):
        schema = load_json(path)
        Draft202012Validator.check_schema(schema)
        uri = schema.get("$id")
        if not uri:
            raise ValueError(f"{path}: schema has no $id")
        schemas[uri] = schema
        registry = registry.with_resource(uri, Resource.from_contents(schema))
    return registry, schemas


def validate_instance(instance: Any, schema_uri: str, schemas: dict[str, dict[str, Any]], registry: Registry, path: Path, issues: list[dict[str, Any]]) -> None:
    schema = schemas.get(schema_uri)
    if not schema:
        issue(issues, "critical", "SCHEMA_MISSING", path, f"schema not loaded: {schema_uri}")
        return
    validator = Draft202012Validator(schema, registry=registry)
    for err in sorted(validator.iter_errors(instance), key=lambda e: [str(part) for part in e.path]):
        location = "/".join(str(part) for part in err.path)
        issue(issues, "error", "SCHEMA_INSTANCE", f"{path}#{location}", err.message)


def iter_nodes(nodes: Iterable[dict[str, Any]]) -> Iterable[dict[str, Any]]:
    for node in nodes:
        yield node
        yield from iter_nodes(node.get("children") or [])


def check_enum(registry_values: list[str], schema_values: list[str], name: str, issues: list[dict[str, Any]]) -> None:
    if set(registry_values) != set(schema_values):
        issue(
            issues,
            "error",
            "ENUM_DRIFT",
            "registries/enums.yaml",
            f"{name} registry={sorted(registry_values)} schema={sorted(schema_values)}",
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--fixture", default="fixtures/reference-novel")
    parser.add_argument("--report", default="build/validation-report.json")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    fixture_arg = Path(args.fixture)
    fixture = fixture_arg if fixture_arg.is_absolute() else repo / fixture_arg
    issues: list[dict[str, Any]] = []

    try:
        registry, schemas = build_registry(repo / "contracts")
    except Exception as exc:
        issue(issues, "critical", "SCHEMA_META", "contracts", str(exc))
        registry, schemas = Registry(), {}

    mappings: dict[Path, str] = {
        fixture / "project.yml": "https://constellation-writer.local/contracts/project/project.schema.json",
        fixture / "manuscripts/main.manuscript.yml": "https://constellation-writer.local/contracts/manuscript/manuscript.schema.json",
        fixture / "manuscripts/alternate-opening.manuscript.yml": "https://constellation-writer.local/contracts/manuscript/manuscript.schema.json",
        fixture / "compile/profiles/draft-html.compile.yml": "https://constellation-writer.local/contracts/compile/compile-profile.schema.json",
        fixture / "compendium/entities/ent_018f0000-0000-7000-8000-000000000001.entity.yml": "https://constellation-writer.local/contracts/compendium/entity.schema.json",
        fixture / "compendium/claims/clm_018f0000-0000-7000-8000-000000000001.claim.yml": "https://constellation-writer.local/contracts/compendium/claim.schema.json",
        fixture / "compendium/evidence/ev_018f0000-0000-7000-8000-000000000001.evidence.yml": "https://constellation-writer.local/contracts/compendium/evidence.schema.json",
        fixture / "patches/ps_018f0000-0000-7000-8000-000000000001/session.yml": "https://constellation-writer.local/contracts/mutation/patch-session.schema.json",
        fixture / "backups/snapshots/snap_018f0000-0000-7000-8000-000000000001/snapshot.yml": "https://constellation-writer.local/contracts/recovery/snapshot.schema.json",
        fixture / "recovery/conflicts/cf_018f0000-0000-7000-8000-000000000001/conflict.yml": "https://constellation-writer.local/contracts/recovery/conflict.schema.json",
        fixture / "backups/archives/example.archive.yml": "https://constellation-writer.local/contracts/recovery/archive.schema.json",
    }
    for path in (fixture / "meta/sheets").glob("*.yml"):
        mappings[path] = "https://constellation-writer.local/contracts/sheet/sheet-sidecar.schema.json"

    parsed: dict[Path, Any] = {}
    for path, uri in mappings.items():
        if not path.exists():
            issue(issues, "error", "MISSING_FIXTURE", path, "required fixture missing")
            continue
        try:
            parsed[path] = load_yaml(path)
            validate_instance(parsed[path], uri, schemas, registry, path, issues)
        except Exception as exc:
            issue(issues, "error", "VALIDATE_EXCEPTION", path, str(exc))

    sheet_paths: dict[str, list[Path]] = {}
    for path in (fixture / "sheets").glob("*.md"):
        frontmatter = parse_frontmatter(path)
        if not frontmatter or not isinstance(frontmatter.get("id"), str):
            issue(issues, "error", "SHEET_FRONTMATTER", path, "missing valid frontmatter id")
            continue
        sheet_paths.setdefault(frontmatter["id"], []).append(path)
    for sheet_id, paths in sheet_paths.items():
        if len(paths) > 1:
            issue(issues, "error", "DUPLICATE_SHEET_ID", ", ".join(str(p) for p in paths), f"{sheet_id} appears in multiple Sheet bodies")
    sheet_ids = set(sheet_paths)

    sidecar_paths: dict[str, list[Path]] = {}
    for path in (fixture / "meta/sheets").glob("*.yml"):
        try:
            value = parsed.get(path) or load_yaml(path)
            sidecar_paths.setdefault(value["id"], []).append(path)
        except Exception as exc:
            issue(issues, "error", "SIDECAR_PARSE", path, str(exc))
    for sheet_id, paths in sidecar_paths.items():
        if len(paths) > 1:
            issue(issues, "error", "DUPLICATE_SIDECAR_ID", ", ".join(str(p) for p in paths), f"{sheet_id} has multiple sidecars")
        if sheet_id not in sheet_ids:
            issue(issues, "error", "ORPHAN_SIDECAR", paths[0], f"{sheet_id} has no Sheet body")
    for sheet_id, paths in sheet_paths.items():
        if sheet_id not in sidecar_paths:
            issue(issues, "warning", "MISSING_SIDECAR", paths[0], f"{sheet_id} has no sidecar")

    manuscript_ids: set[str] = set()
    for manifest_path in (fixture / "manuscripts").glob("*.yml"):
        try:
            manifest = parsed.get(manifest_path) or load_yaml(manifest_path)
            manuscript_ids.add(manifest["id"])
            node_ids: set[str] = set()
            for node in iter_nodes(manifest.get("root_nodes") or []):
                if node.get("id") in node_ids:
                    issue(issues, "error", "DUPLICATE_NODE_ID", manifest_path, f"duplicate placement {node.get('id')}")
                node_ids.add(node.get("id"))
                if node.get("sheet_id") and node["sheet_id"] not in sheet_ids:
                    issue(issues, "error", "MISSING_SHEET_REF", manifest_path, f"{node['sheet_id']} does not resolve")
        except Exception as exc:
            issue(issues, "error", "MANIFEST_PARSE", manifest_path, str(exc))

    compile_path = fixture / "compile/profiles/draft-html.compile.yml"
    if compile_path.exists():
        profile = parsed.get(compile_path) or load_yaml(compile_path)
        if profile.get("manuscript_id") not in manuscript_ids:
            issue(issues, "error", "MISSING_MANUSCRIPT_REF", compile_path, f"{profile.get('manuscript_id')} does not resolve")

    entity_ids = {load_yaml(path)["id"] for path in (fixture / "compendium/entities").glob("*.yml")}
    claims = [load_yaml(path) for path in (fixture / "compendium/claims").glob("*.yml")]
    evidence = [load_yaml(path) for path in (fixture / "compendium/evidence").glob("*.yml")]
    claim_ids = {value["id"] for value in claims}
    evidence_ids = {value["id"] for value in evidence}
    for value in claims:
        if value.get("subject_entity_id") not in entity_ids:
            issue(issues, "error", "MISSING_ENTITY_REF", "compendium/claims", f"{value.get('subject_entity_id')} does not resolve")
        for evidence_id in value.get("evidence_ids") or []:
            if evidence_id not in evidence_ids:
                issue(issues, "error", "MISSING_EVIDENCE_REF", "compendium/claims", f"{evidence_id} does not resolve")
    for value in evidence:
        if value.get("claim_id") not in claim_ids:
            issue(issues, "error", "MISSING_CLAIM_REF", "compendium/evidence", f"{value.get('claim_id')} does not resolve")
        anchor = value.get("anchor") or {}
        if anchor.get("object_id") not in sheet_ids:
            issue(issues, "error", "MISSING_ANCHOR_SHEET", "compendium/evidence", f"{anchor.get('object_id')} does not resolve")

    annotation_uri = "https://constellation-writer.local/contracts/annotations/annotation.schema.json"
    for path in (fixture / "annotations").glob("*.jsonl"):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
                validate_instance(value, annotation_uri, schemas, registry, path, issues)
                if value.get("sheet_id") not in sheet_ids:
                    issue(issues, "error", "MISSING_ANNOTATION_SHEET", f"{path}:{number}", f"{value.get('sheet_id')} does not resolve")
                if (value.get("anchor") or {}).get("object_id") != value.get("sheet_id"):
                    issue(issues, "error", "ANNOTATION_ANCHOR_MISMATCH", f"{path}:{number}", "anchor object and Sheet differ")
            except Exception as exc:
                issue(issues, "error", "ANNOTATION_PARSE", f"{path}:{number}", str(exc))

    matrix_path = repo / "docs/constitution/CANONICALITY_MATRIX.yaml"
    if matrix_path.exists():
        matrix = load_yaml(matrix_path)
        states: dict[str, str] = {}
        for entry in matrix.get("entries") or []:
            state, owner = entry.get("state"), entry.get("owner")
            if state in states and states[state] != owner:
                issue(issues, "critical", "AUTHORITY_DRIFT", matrix_path, f"{state} has owners {states[state]} and {owner}")
            states[state] = owner

    enum_path = repo / "registries/enums.yaml"
    if enum_path.exists() and schemas:
        enums = load_yaml(enum_path)
        check_enum(enums["sheet_kinds"], schemas["https://constellation-writer.local/contracts/sheet/sheet-sidecar.schema.json"]["properties"]["kind"]["enum"], "sheet_kinds", issues)
        check_enum(enums["manuscript_kinds"], schemas["https://constellation-writer.local/contracts/manuscript/manuscript.schema.json"]["properties"]["kind"]["enum"], "manuscript_kinds", issues)
        check_enum(enums["consequence_levels"], schemas["https://constellation-writer.local/contracts/common/consequence.schema.json"]["$defs"]["ConsequenceLevel"]["enum"], "consequence_levels", issues)
        check_enum(enums["canon_states"], schemas["https://constellation-writer.local/contracts/common/lifecycle.schema.json"]["$defs"]["CanonState"]["enum"], "canon_states", issues)
        check_enum(enums["mutation_states"], schemas["https://constellation-writer.local/contracts/common/lifecycle.schema.json"]["$defs"]["PatchState"]["enum"], "mutation_states", issues)
        check_enum(enums["canonicality_classes"], schemas["https://constellation-writer.local/contracts/common/canonicality.schema.json"]["$defs"]["CanonicalityClass"]["enum"], "canonicality_classes", issues)

    failed = any(item["severity"] in {"error", "critical"} for item in issues)
    report = {
        "validator_version": "0.2.0",
        "status": "failed" if failed else ("passed_with_warnings" if issues else "passed"),
        "issues": issues,
        "counts": {"schemas": len(schemas), "sheets": len(sheet_ids), "manuscripts": len(manuscript_ids), "issues": len(issues)},
    }
    output = repo / args.report
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
