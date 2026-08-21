# Compile Pipeline Decision Spike

This directory is the bounded executable probe for issue #5 and ADR-0006. It is **not** the production compiler.

## Question under test

Can Constellation Writer own all durable and semantic compile authority while using Pandoc only as a pinned output adapter for formats such as DOCX and EPUB?

The spike therefore separates five layers:

1. **Canonical source:** writer-owned Sheet files and the Manuscript Manifest.
2. **Assembly authority:** the Manifest owns order, membership, placement role, contextual title behavior, and semantic breaks.
3. **Export projection:** the Compile Profile may select an explicit scope and map resolved roles to target treatment, but cannot rewrite assembly or semantic roles.
4. **Constellation compiler:** frozen input digests, linear compile plan, minimal Workbench AST, direct Markdown/HTML renderers, QA, and source maps.
5. **Adapter boundary:** Pandoc receives only Constellation-rendered controlled Markdown and owns no canonical state or manuscript semantics.

## Executable artifacts

`compile_spike.py` emits:

- `compile-plan.json`
- `workbench-ast.json`
- `output.md`
- `output.html`
- `source-map.json`
- `qa.json`
- `receipt.json`
- optional `output.docx` and `output.epub` when a Pandoc binary is supplied

Every frozen input is SHA-256 hashed. Every semantic AST segment receives a stable spike segment ID. Source maps trace authored output segments to placement ID, Sheet ID, frozen content digest, source path, and line span. Binary formats retain segment-order provenance at this spike stage rather than pretending to provide byte-accurate reverse maps.

## Run

```bash
python spikes/compile-pipeline/compile_spike.py compile \
  --project fixtures/reference-novel \
  --manifest manuscripts/main.manuscript.yml \
  --profile compile/profiles/draft-html.compile.yml \
  --out build/compile-spike/reference
```

With a pinned Pandoc binary:

```bash
python spikes/compile-pipeline/compile_spike.py compile \
  --project fixtures/reference-novel \
  --manifest manuscripts/main.manuscript.yml \
  --profile compile/profiles/draft-html.compile.yml \
  --out build/compile-spike/reference-pandoc \
  --pandoc /absolute/path/to/pandoc
```

Compare two frozen builds:

```bash
python spikes/compile-pipeline/compile_spike.py compare \
  --left build/compile-spike/repeat-a \
  --right build/compile-spike/repeat-b
```

## Golden cases

The automated suite executes the repository's CG-001 through CG-009 intent and adds authority/security negative controls:

- manifest order beats filesystem order;
- excluded material stays absent and explainable;
- contextual titles do not duplicate matching authored headings;
- scene breaks exist as semantic AST nodes;
- comments are excluded by default with QA provenance;
- missing assets carry source locators;
- source maps cover authored segments;
- repeated frozen compiles are semantically equivalent;
- unavailable Pandoc leaves Constellation-owned fallbacks intact;
- Compile Profiles cannot override manifest structure or role;
- profile scope is a projection rather than an assembly mutation;
- unsupported syntax is visible instead of silently lost;
- asset path escape is a hard gate.

## Evidence limits

This spike deliberately does **not** claim:

- that its small Markdown parser is a production parser;
- bibliography/citation-engine completeness;
- byte-addressed source maps inside DOCX/EPUB archives;
- exhaustive professional publishing fidelity;
- that byte-identical archives are required when semantic equivalence is the correct criterion.

Those boundaries remain explicit in the compile receipt and ADR interpretation.

## CI posture

The GitHub workflow is a reproducible evidence runner, not a product dependency. Normal compile execution must remain local and offline-capable. The workflow downloads two official Pandoc release binaries, verifies their published SHA-256 digests, and compares semantic round trips across versions.
