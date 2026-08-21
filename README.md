# Constellation Writer

Constellation Writer is a local-first professional writing workbench for serious longform authorship.

> Calm editor. Brutal recall. Governed transformation.

The product is manuscript-first rather than dashboard-first, graph-first, or AI-first. Writer-owned files and manifests hold durable truth; search, graph, semantic indexes, previews, QA, and AI outputs are derived or governed projections.

## Foundation doctrine

- the editor is the sovereign authorship surface;
- manuscript prose remains writer-owned plain text;
- identity is stable and independent of title, path, or placement;
- the Manuscript Manifest owns assembly;
- SQLite and other indexes remain rebuildable;
- transformations are inspectable, provenance-bearing, and recoverable;
- Compendium and AI capabilities remain subordinate to the manuscript.

## Validation without hosted CI

Project validity does not depend on paid GitHub Actions capacity. The default deterministic validation route is local:

```bash
python -m pip install -r tools/validator/requirements.txt
python tools/local_validate.py --suite all
```

GitHub Actions workflows are retained as optional manual replication recipes, not automatic merge gates. See `docs/validation/LOCAL_VALIDATION_POLICY.md`.

## Current phase

The repository is in governed foundation and F1 architecture-coherence work. Read `CURRENT_STATE.yaml`, `ROADMAP.md`, and `docs/constitution/` before making architectural changes.
