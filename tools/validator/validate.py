#!/usr/bin/env python3
"""Deterministic foundation validator for Constellation Writer."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

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
    return yaml.load(text[4:end], Loader=NoDatesSafeLoader)


def build_registry(schema_root: Path) -> tuple[Registry, dict[str, dict]]:
    registry = Registry()
    schemas: dict[str, dict] = {}
    for path in schema_root.rglob("*.schema.json"):
        schema = load_json(path)
        Draft202012Validator.check_schema(schema)
        uri = schema.get("$id")
        if not uri:
            raise ValueError(f"{path}: schema has no $id")
        schemas[uri] = schema
        registry = registry.with_resource(uri, Resource.from_contents(schema))
    return registry, schemas


def validate_instance(
    instance: Any,
    schema_uri: str,
    schemas: dict[str, dict],
    registry: Registry,
    path: Path,
    issues: list[dict[str, Any]],
) -> None:
    schema = schemas[schema_uri]
    validator = Draft202012Validator(schema, registry=registry)
    for err in sorted(validator.iter_errors(instance), key=lambda e: list(e.path)):
        issues.append(
            {
                "severity": "error",
                "code": "SCHEMA_INSTANCE",
                "path": str(path),
                "message": err.message,
            }
        )


def gather_ids(value: Any, found: list[tuple[str, str]], path: str = "") -> None:
    if isinstance(value, dict):
        if isinstance(value.get("id"), str):
            found.append((value["id"], path))
        for key, child in value.items():
            gather_ids(child, found, f"{path}/{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            gather_ids(child, found, f"{path}/{index}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--fixture", default="fixtures/reference-novel")
    parser.add_argument("--report", default="build/validation-report.json")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    fixture = repo / args.fixture
    issues: list[dict[str, Any]] = []

    try:
        registry, schemas = build_registry(repo / "contracts")
    except Exception as exc:
        issues.append(
            {
                "severity": "critical",
                "code": "SCHEMA_META",
                "path": "contracts",
                "message": str(exc),
            }
        )
        registry, schemas = Registry(), {}

    mappings = {
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

    for path, uri in mappings.items():
        if not path.exists():
            issues.append(
                {
                    "severity": "error",
                    "code": "MISSING_FIXTURE",
                    "path": str(path),
                    "message": "required fixture missing",
                }
            )
            continue
        try:
            validate_instance(load_yaml(path), uri, schemas, registry, path, issues)
        except Exception as exc:
            issues.append(
                {
                    "severity": "error",
                    "code": "VALIDATE_EXCEPTION",
                    "path": str(path),
                    "message": str(exc),
                }
            )

    annotation_schema = "https://constellation-writer.local/contracts/annotations/annotation.schema.json"
    for path in (fixture / "annotations").glob("*.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                validate_instance(json.loads(line), annotation_schema, schemas, registry, path, issues)

    sheet_ids: set[str] = set()
    for path in (fixture / "sheets").glob("*.md"):
        frontmatter = parse_frontmatter(path)
        if not frontmatter or not frontmatter.get("id"):
            issues.append(
                {
                    "severity": "error",
                    "code": "SHEET_FRONTMATTER",
                    "path": str(path),
                    "message": "missing valid frontmatter id",
                }
            )
        else:
            sheet_ids.add(frontmatter["id"])

    found: list[tuple[str, str]] = []
    for path in fixture.rglob("*"):
        if path.suffix in {".yml", ".yaml"}:
            try:
                gather_ids(load_yaml(path), found, str(path.relative_to(repo)))
            except Exception as exc:
                issues.append(
                    {
                        "severity": "error",
                        "code": "YAML_PARSE",
                        "path": str(path),
                        "message": str(exc),
                    }
                )
    for path in (fixture / "sheets").glob("*.md"):
        frontmatter = parse_frontmatter(path)
        if frontmatter and frontmatter.get("id"):
            found.append((frontmatter["id"], str(path.relative_to(repo))))

    by_id: dict[str, list[str]] = {}
    for object_id, locator in found:
        by_id.setdefault(object_id, []).append(locator)

    canonical_suffixes = (
        "project.yml",
        ".manuscript.yml",
        ".sheet.yml",
        ".entity.yml",
        ".claim.yml",
        ".evidence.yml",
        "session.yml",
        "snapshot.yml",
        "conflict.yml",
        ".archive.yml",
    )
    for object_id, locators in by_id.items():
        declarations = [
            locator for locator in locators if any(locator.endswith(suffix) for suffix in canonical_suffixes)
        ]
        if not object_id.startswith("sh_") and len(declarations) > 1:
            issues.append(
                {
                    "severity": "error",
                    "code": "DUPLICATE_DECLARATION",
                    "path": ", ".join(declarations),
                    "message": f"{object_id} declared more than once",
                }
            )

    for manifest_path in (fixture / "manuscripts").glob("*.yml"):
        manifest = load_yaml(manifest_path)

        def walk(nodes: list[dict[str, Any]] | None) -> None:
            for node in nodes or []:
                sheet_id = node.get("sheet_id")
                if sheet_id and sheet_id not in sheet_ids:
                    issues.append(
                        {
                            "severity": "error",
                            "code": "MISSING_SHEET_REF",
                            "path": str(manifest_path),
                            "message": f"{sheet_id} does not resolve",
                        }
                    )
                walk(node.get("children"))

        walk(manifest.get("root_nodes"))

    failed = any(issue["severity"] in {"error", "critical"} for issue in issues)
    report = {
        "validator_version": "0.1.0",
        "status": "failed" if failed else ("passed_with_warnings" if issues else "passed"),
        "issues": issues,
        "counts": {"schemas": len(schemas), "issues": len(issues)},
    }
    output = repo / args.report
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
