from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from packages.mutation.core import apply_text_mutation
from packages.vault.core import dump_yaml, load_yaml, safe_project_path, sha256_file


class ManuscriptError(RuntimeError):
    pass


def load_manifest(
    project_root: Path, relative_path: str | Path
) -> dict[str, Any]:
    value = load_yaml(safe_project_path(project_root, relative_path))
    if not isinstance(value, dict) or not isinstance(value.get("id"), str):
        raise ManuscriptError("invalid manuscript manifest")
    return value


def iter_nodes(
    nodes: Iterable[dict[str, Any]], parent_id: str | None = None
):
    for ordinal, node in enumerate(nodes):
        yield parent_id, ordinal, node
        yield from iter_nodes(node.get("children") or [], node.get("id"))


def ordered_sheet_ids(manifest: dict[str, Any]) -> list[str]:
    result: list[str] = []
    for _parent, _ordinal, node in iter_nodes(manifest.get("root_nodes") or []):
        if node.get("type") == "sheet_ref" and node.get("include", True) is not False:
            result.append(node["sheet_id"])
    return result


def reorder_root_placement(
    project_root: Path,
    manifest_relative_path: str | Path,
    placement_id: str,
    new_index: int,
) -> dict[str, Any]:
    path = safe_project_path(project_root, manifest_relative_path)
    before_hash = sha256_file(path)
    manifest = load_manifest(project_root, manifest_relative_path)
    nodes = manifest.get("root_nodes") or []
    matches = [
        index for index, node in enumerate(nodes) if node.get("id") == placement_id
    ]
    if len(matches) != 1:
        raise ManuscriptError(
            f"placement {placement_id} resolves {len(matches)} times at root"
        )
    old_index = matches[0]
    node = nodes.pop(old_index)
    if new_index < 0:
        new_index = max(0, len(nodes) + 1 + new_index)
    new_index = min(max(new_index, 0), len(nodes))
    nodes.insert(new_index, node)
    manifest["root_nodes"] = nodes
    receipt = apply_text_mutation(
        project_root,
        manifest_relative_path,
        dump_yaml(manifest),
        object_id=manifest["id"],
        object_type="manuscript",
        intent=f"reorder placement {placement_id} from {old_index} to {new_index}",
        expected_sha256=before_hash,
        consequence="canonical_high",
    )
    return {"old_index": old_index, "new_index": new_index, "operation": receipt}
