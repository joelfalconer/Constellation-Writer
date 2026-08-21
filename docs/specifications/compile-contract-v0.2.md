# Compile Contract v0.2

**Status:** F1 candidate pending issue #5 evidence and gate promotion  
**Imports:** `INV-CMP-001`, `INV-ASM-001`, Manuscript Manifest v0.2, Sheet Schema v0.2, Compile Profile schema, provenance and validation contracts  
**Supersedes for F1 review:** Compile Contract v0.1

## 1. Purpose and scope

Compile is a deterministic, inspectable build pipeline that transforms a frozen projection of canonical manuscript structure and authored content into output artifacts without moving canonical authority into the renderer or output adapter.

The governing sentence is:

> **The Manifest answers “what is the work?” The Compile Profile answers “how should this declared projection of the work become this output?”**

A compile may select an explicit export scope, but it may not silently redefine manuscript order, membership, semantic role, or authored source.

The compiler must remain useful when every optional adapter is unavailable. Constellation-owned compile plan, Workbench AST, QA, source map, Markdown output, and HTML output are therefore upstream of DOCX/EPUB adapters.

## 2. Non-goals

Compile does not:

- own authored Sheet text;
- own manuscript order or placement identity;
- silently “fix” source during export;
- turn a Compile Profile into a second manuscript manifest;
- permit Pandoc, a template engine, or any future adapter to become canonical state;
- promise lossless round-trip from every output format back to canonical Sheets;
- treat byte identity as the sole definition of deterministic output for archive formats containing permitted metadata;
- require network access or a hosted runner for ordinary local compilation;
- make SQLite, search indexes, previews, or caches necessary to reconstruct the build.

## 3. Core principles and authority model

### One owner per semantic dimension

| Dimension | Canonical owner | Compile behavior |
|---|---|---|
| Sheet text and intrinsic identity | Sheet | freeze exact revision/content digest; never rewrite source |
| Manuscript placement and order | Manuscript Manifest | expand in declared order |
| Manuscript membership | Manuscript Manifest | resolve placement/parent inclusion from manifest |
| Placement semantic role | Manuscript Manifest | carry role unchanged into compile plan |
| Contextual placement title | Manuscript Manifest | resolve title behavior before target rendering |
| Semantic structural breaks | Manuscript Manifest | represent as semantic compile-plan/AST nodes |
| Export scope | Compile Profile | select an explicit projection of already-declared manifest nodes |
| Target-format treatment | Compile Profile + renderer | map resolved semantics to representation/style |
| Frozen compile plan | Constellation compiler | derived, reproducible build input |
| Workbench AST | Constellation compiler | derived semantic representation |
| QA and source map | Constellation compiler | derived evidence/diagnostic products |
| DOCX/EPUB conversion | pinned adapter | output-only transformation, never state authority |

### Structural non-interference law

A Compile Profile **must not** contain or imply:

- arbitrary placement reordering;
- assembly membership overrides;
- semantic role overrides;
- hidden Sheet substitution;
- target-specific mutation of canonical files.

A profile may narrow output through an explicit `scope` selector. A scope is a deterministic projection, not a mutation of the Manuscript Manifest. Preview and final export must use the same resolved scope and compile plan.

### Adapter isolation law

A target adapter receives a Constellation-controlled representation only after manifest resolution, source freezing, AST construction, validation, and direct fallback generation. An adapter may not parse canonical project directories as its own project model.

## 4. Proposed model and executable contract

### Inputs

Canonical or declared inputs:

- Project manifest;
- Manuscript Manifest;
- exact Sheet files/revisions selected by that Manifest;
- canonical Sheet metadata required for compile semantics;
- canonical assets and source records when referenced;
- Compile Profile;
- optional Style Map and citation data when the selected target requires them.

Derived inputs such as SQLite rows, search indexes, graph edges, embeddings, previews, and cached word counts may accelerate a compile but can never be required for correctness.

### Freeze record

Before semantic transformation, the compiler records at minimum:

```yaml
frozen_input:
  kind: manuscript_manifest | compile_profile | sheet | asset | source | style_map
  canonical_id: optional_stable_id
  placement_id: optional_placement_id
  path: writer_visible_relative_path
  content_digest: sha256_or_accepted_revision_digest
```

The frozen set is immutable for the duration of one compile. An external edit after freezing belongs to the next compile, not a half-mutated current build.

### Linear compile plan

The compiler expands the Manifest into an ordered sequence containing at minimum:

```yaml
compile_plan_entry:
  ordinal: 0
  placement_id: nd_...
  sheet_id: sh_...
  frozen_revision_digest: sha256:...
  semantic_role: scene
  contextual_title: Opening Scene
  assembly_include: true
  export_selected: true
  selection_reason: manifest_included_and_scope_selected
  semantic_break_before: optional
  source_path: sheets/...
```

An excluded placement remains explainable in the compile receipt with the authority and reason that excluded it.

### Workbench AST

The v1 Workbench AST is intentionally smaller than a universal publishing AST. Its purpose is to preserve Constellation-owned semantics and provenance across direct renderers and output adapters.

Minimum node families:

- heading;
- paragraph;
- list and list item;
- block quote;
- code block;
- footnote definition/reference;
- citation marker;
- image/asset reference;
- semantic scene/section break;
- generated structural title/front/back matter node;
- explicit unsupported/lossy node for syntax not safely represented.

Every semantically emitted node receives a stable compile-segment identifier for the frozen build.

### Direct renderers

Markdown and HTML are mandatory Constellation-owned executable targets for F2. They establish that the manuscript can still compile when external adapters fail.

Direct renderers must consume the Workbench AST, not re-read canonical Sheets independently.

### Pandoc adapter

For the F1 candidate architecture:

1. Constellation renders a controlled adapter representation from the Workbench AST.
2. A pinned Pandoc binary may convert that representation to DOCX or EPUB.
3. The compiler captures adapter version, invocation, exit status, warnings, artifact digest, and semantic verification results.
4. Adapter failure cannot invalidate already-generated compile plan, Workbench AST, QA, source map, Markdown, or HTML fallback.
5. Pandoc version changes are treated as adapter changes subject to golden tests, not as silent compiler upgrades.

DOCX/EPUB archive byte differences are not automatically semantic failures. When target metadata is nondeterministic, the build sets a controlled reproducibility environment such as `SOURCE_DATE_EPOCH` and separately checks semantic equivalence.

## 5. Source maps, QA, and explainability

### Source map

Every authored output segment must resolve to:

```yaml
source_map_segment:
  segment_id: seg_...
  semantic_kind: paragraph
  placement_id: nd_...
  sheet_id: sh_...
  frozen_revision_digest: sha256:...
  source:
    path: sheets/...
    span:
      line_start: 12
      line_end: 14
  outputs:
    markdown: character_or_structural_locator
    html: element_or_character_locator
    adapter: semantic_segment_or_target_locator
```

Generated structural nodes must identify their generation authority instead of pretending to have authored source spans.

The first executable binary adapter may retain segment-level/ordinal provenance rather than byte-addressed locations inside DOCX/EPUB, but the limitation must be explicit. Richer reverse maps can be added only when they are measurable and stable.

### QA finding contract

Every finding records:

- code and severity;
- whether it blocks the selected profile;
- placement/Sheet/revision/source locator where relevant;
- what was excluded, transformed, unsupported, or missing;
- which authority/policy produced the outcome;
- remediation or accepted-loss explanation when consequential.

Hard errors include at minimum:

- invalid Manifest/Profile;
- missing included Sheet;
- ambiguous duplicate identity;
- canonical path escape;
- unresolved destructive conflict;
- profile attempt to override Manifest structure/role;
- required asset missing under a profile that declares it blocking.

Warnings/profile-governed findings include:

- excluded comments/annotations;
- unsupported Markdown extensions;
- optional missing assets;
- unresolved citations;
- unreviewed AI provenance in a final profile;
- target-specific lossy transforms;
- adapter warnings/version drift.

Silent loss is never an acceptable compile behavior.

## 6. Determinism, cache, and failure semantics

### Semantic determinism

Identical frozen canonical inputs, profile semantics, compiler version, and adapter version must produce semantically equivalent:

- compile plan;
- Workbench AST;
- inclusion/exclusion decisions;
- direct Markdown/HTML;
- QA findings apart from explicitly nonsemantic timestamps;
- source-map relationships.

Byte identity is required for deterministic text/JSON products where practical. It is preferred, but not sufficient by itself, for archive/binary formats.

### Cache law

Compile caches are derived and disposable. Deleting all compile caches must not change the resolved plan, semantic artifact, QA outcome, or source map.

### Failure isolation

- Source files are never mutated by compile.
- A failed target build does not overwrite the last successful output unless the user explicitly chooses that behavior.
- Output should be written to a temporary location and promoted atomically where the filesystem permits.
- Adapter failure records the failure and leaves Constellation-owned fallbacks available.
- A partial adapter artifact is quarantined or removed, never presented as successful output.

## 7. Edge cases and adversarial cases

The compile service must explicitly test:

- filesystem order differing from Manifest order;
- the same Sheet used in multiple manuscripts;
- a Sheet excluded in one assembly and included in another;
- profile scope excluding an otherwise included placement;
- parent/child inclusion boundaries;
- duplicate contextual title versus authored first heading;
- empty structural containers;
- front/back matter and generated nodes;
- comments and annotations in draft vs final profiles;
- citations without resolvable bibliography data;
- footnotes/endnotes across Sheet boundaries;
- missing, external, symlinked, or path-escaping assets;
- unsupported Markdown extensions;
- externally modified Sheet after input freeze;
- adapter binary missing, crashing, timing out, or changing version;
- repeated compile with frozen identical inputs;
- target format containing build timestamps or unique identifiers;
- stale preview generated from a different compile-plan digest.

## 8. Minimum viable and high-quality versions

### Minimum passing F2 implementation

- Manifest-only assembly authority;
- frozen input digests;
- linear compile plan;
- minimal Workbench AST;
- deterministic Markdown and HTML;
- explicit scope projection;
- QA with actionable locators;
- source maps through Sheet/revision/span;
- adapter-independent fallbacks;
- compile receipt with compiler/profile/input digests;
- golden tests for order, exclusion, title de-duplication, scene breaks, comments, missing assets, source-map coverage, repeatability, and adapter failure.

### High-quality/stretch version

- complete versioned Workbench AST schema;
- role-aware DOCX/EPUB/PDF/Fountain adapters;
- richer target reverse maps;
- CSL bibliography/citation engine with provenance;
- professional reference DOCX templates/style maps;
- EPUB structural/accessibility validation;
- print/PDF preflight;
- profile inheritance with explainable resolution;
- compile-plan visual preview showing why every node is present or absent;
- artifact diffing across compiler/adapter versions;
- deterministic publication archives with receipts and checksums.

## 9. Risks, failure modes, and decisions to lock now

### Risks

- A “helpful” profile layer could slowly become a hidden second Manifest.
- A universal AST could grow until the writing product becomes a document-conversion framework.
- Adapter convenience could leak Pandoc-specific assumptions into canonical schemas.
- Binary source-map ambition could create false precision before target writers expose stable hooks.
- Golden fixtures could overfit tiny synthetic projects and miss real manuscript complexity.
- Reproducible archives can still differ because of target-specific identifiers even after timestamps are controlled.

### Decisions to lock now

1. Manifest owns assembly order, membership, contextual role, and semantic structural intent.
2. Compile Profile owns explicit export scope and target treatment only.
3. Frozen input set is established before transforms.
4. Workbench compile plan, AST, QA, and source map are Constellation-owned derived products.
5. Markdown and HTML remain direct fallback renderers.
6. Pandoc is an output adapter, never the canonical compiler or project parser.
7. Adapter versions are pinned and tested before promotion.
8. Semantic equivalence outranks archive byte identity when permitted metadata differs.
9. Compile never mutates source.
10. Preview and final export share the same resolved compile plan.

Reversal cost is **high** for changing assembly/semantic authority after F2 because every renderer, source map, preview, and migration would inherit the mistake. Reversal cost is **medium** for replacing Pandoc with another output adapter if the boundary above remains intact.

## 10. Open questions and acceptance tests

### Open questions

- Exact production Workbench AST schema and versioning strategy.
- Whether the first AST implementation should adopt a mature Markdown parser internally while preserving the Workbench semantic layer.
- Exact representation for list/table/math/raw-HTML features outside the F1 spike.
- Citation engine and CSL ownership boundary.
- Binary target source-map granularity that is both useful and truthful.
- Reference DOCX/style-map packaging and user customization.
- EPUB identifier policy for fully reproducible archives.
- PDF adapter and accessibility strategy.
- Compile Profile inheritance and named scope ownership.

### F1 spike acceptance tests

Issue #5 may resolve ADR-0006 only if the executable spike demonstrates or explicitly falsifies:

1. `CG-001` Manifest order beats filesystem order.
2. `CG-002` excluded Sheet is absent and exclusion is explained.
3. `CG-003` contextual title does not create a duplicate first heading.
4. `CG-004` scene break survives as semantic intent across renderers.
5. `CG-005` comments are profile-governed and visible in QA.
6. `CG-006` missing asset is deterministic and source-located.
7. `CG-007` every authored output segment traces to placement, Sheet, frozen revision, and span.
8. `CG-008` repeated frozen compile is semantically equivalent.
9. `CG-009` Pandoc failure leaves a valid compile plan and direct fallback.
10. A current pinned Pandoc and prior release are compared without confusing metadata-byte drift with semantic drift.
11. A Compile Profile attempting to override structure/role fails a hard gate.
12. No successful test requires Pandoc to parse canonical Sheets directly.

If any hard authority or source-fidelity gate fails, ADR-0006 remains deferred or is rejected regardless of output-format convenience.
