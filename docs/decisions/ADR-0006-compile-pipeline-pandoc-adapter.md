# ADR-0006: Own the compile plan and use Pandoc as a pinned output adapter

- **Status:** accepted for F2 scaffold
- **Accepted scope:** Constellation-owned compile plan/Workbench AST with Pandoc 3.10.1 as the pinned DOCX/EPUB adapter baseline
- **Decision class:** high for semantic authority, medium for adapter replacement
- **Review gate:** F1 Compile Spike C1
- **Evidence issue:** #5
- **Evidence run:** `32468472581`
- **Evidence artifact:** `9441576333`
- **Artifact digest:** `sha256:75c5018dcb748f0e2a843445955068cf359f9c6f9872a0a047e69b22eee68b34`
- **Contract:** `docs/specifications/compile-contract-v0.2.md`

## Context

Constellation Writer must own deterministic manuscript resolution, semantic roles, QA, source mapping, and writer-visible failure behavior. It also needs professional Markdown, HTML, DOCX, and EPUB output without turning an external document converter into the product's canonical compiler.

Pandoc's documented architecture is a reader → AST → writer pipeline, with filters operating on Pandoc's intermediate AST. That makes it a strong conversion engine, but not automatically a safe owner for Constellation's manuscript semantics. The architecture decision therefore depended on an executable boundary: can Constellation freeze and resolve the work first, preserve its own semantic/provenance model, and treat Pandoc as a replaceable output adapter?

## Decision

Use the following F2 compile architecture:

1. **Sheets own authored source and intrinsic identity.**
2. **The Manuscript Manifest owns assembly order, membership, contextual placement title, semantic role, and structural break intent.**
3. **The Compile Profile may select an explicit export scope and map resolved semantics to target-format treatment.** It may not reorder the manuscript, override membership, or redefine semantic roles.
4. **Constellation freezes exact compile inputs** and records content digests before transformation.
5. **Constellation builds the linear compile plan and Workbench AST.**
6. **Constellation owns QA, source maps, artifact verification, and direct Markdown/HTML renderers.**
7. **Pandoc is invoked only after those steps** using a controlled Constellation-rendered representation.
8. **Pandoc 3.10.1 is the pinned F2 DOCX/EPUB adapter baseline.** Version changes require golden comparison before promotion.
9. **Adapter failure must preserve the compile plan, Workbench AST, QA, source map, Markdown, and HTML fallback.**
10. **Preview and final export use the same resolved compile plan.**

Pandoc is therefore not the canonical compiler, project parser, assembly authority, Workbench AST owner, or source-map authority.

## Measured evidence

Run `32468472581` executed the issue #5 boundary on Ubuntu 24.04 with Python 3.12.14.

### Golden and negative controls

Thirteen deterministic tests passed, including the repository's CG-001 through CG-009 intent plus authority/security controls:

- Manifest order beat filesystem order;
- excluded placements remained absent and explainable;
- matching placement title and first authored H1 did not duplicate;
- scene break survived as a semantic AST node;
- comments were excluded by default with QA evidence;
- missing assets carried placement/Sheet/source-line locators;
- source maps covered every authored test segment with placement, Sheet, frozen revision digest and source span;
- repeated frozen compile was semantically equivalent;
- unavailable Pandoc preserved Constellation-owned fallbacks;
- profile role/structure override was rejected as a hard gate;
- profile scope acted as output projection without changing `assembly_include`;
- unsupported syntax remained visible through QA instead of disappearing;
- asset path escape blocked the compile.

### Frozen reference compile

Two adapter-free reference-manuscript builds produced identical semantic/direct digests:

```yaml
plan_semantic_digest: 4e248c591d0060bed1b8ff81b2f687c9939f39851aae317f0121da6e364819ce
ast_semantic_digest: 482047b0677ca22c6ffba2df32a0d55d9d1cc610703636016dec91488db39b4b
markdown_sha256: 750942ba12534d7d62bbf423b818f0d4d793d07e4a4ffb15fe46d7f6b475d79c
html_sha256: 340f902bdcb7f48559073ab65e420d39e1d3780a7d8d5e31b4066505682e5813
source_map_sha256: c595054e2800180e083189792cb2bd4facb8a21f803fe64cc84af09712f7c410
```

`direct_all_equal` was `true`.

### Adapter-version control

The workflow downloaded official Linux amd64 release archives and verified their published SHA-256 digests before execution:

- Pandoc `3.10.1`: `72948bf5784f560d5ad1876709daca27e0667f262da727bb33f77b58e52df2f5`
- Pandoc `3.9.0.2`: `a69abfababda8a56969a254b09f9553a7be89ddec00d4e0fe9fd585d71a67508`

Both versions successfully produced DOCX and EPUB from the same Constellation-owned adapter input.

| Target | 3.10.1 | 3.9.0.2 | semantic round-trip | byte equality |
|---|---|---|---|---|
| DOCX | pass | pass | equal | equal |
| EPUB | pass | pass | equal | **different** |

Both targets round-tripped to the same normalized semantic digest:

`850f85e1f507a8a8e5d92ac73115a4a2df535a5dbeb1da3610680b29af949717`

The EPUB archive bytes differed between versions while the semantic round trip remained equal. This is useful evidence for the contract rule that archive byte identity is informative but cannot be the sole semantic-equivalence criterion. Adapter invocations set `SOURCE_DATE_EPOCH` to control documented build timestamp nondeterminism.

### Adapter-failure control

A deliberately nonexistent Pandoc binary produced `unavailable` adapter records for DOCX and EPUB while the compile receipt still passed and retained valid:

- `compile-plan.json`;
- `workbench-ast.json`;
- `output.md`;
- `output.html`;
- `source-map.json`;
- QA and receipt evidence.

This directly supports the adapter-isolation boundary.

## Alternatives evaluated

### A. Constellation-owned plan/AST + pinned Pandoc adapter

**Selected.** It survived the hard authority, determinism, provenance, version-drift, and adapter-failure controls while avoiding the cost of immediately implementing every binary writer.

### B. Pandoc as canonical compiler/AST owner

**Rejected by architectural hard gate.** This would allow output-adapter semantics to become manuscript semantics, weaken the Manifest's authority, and make Constellation's source map/QA dependent on a third-party intermediate model. The spike intentionally proves the useful Pandoc path without granting that authority.

### C. Constellation-owned DOCX/EPUB writers with no Pandoc

**Retained as a future alternative, not selected for F2.** It has the cleanest dependency boundary but substantially larger implementation and test surface. Nothing in the current evidence requires paying that cost now. Revisit if the pinned adapter fails output-quality, accessibility, security, packaging, licensing, or provenance requirements that cannot be repaired without semantic leakage.

## Consequences

### Positive

- Canonical project formats remain independent of Pandoc.
- Direct Markdown/HTML provide an adapter-independent survival path.
- Output adapters can be replaced without migrating writer-owned manuscripts.
- Version drift becomes measurable through golden fixtures and semantic comparisons.
- QA/source-map behavior stays under Constellation control.
- Compile Profile authority is narrowed before F2 implementation can accidentally fossilize a second Manifest.

### Costs

- Constellation must maintain a real Workbench AST and controlled adapter representation.
- Binary reverse mapping is harder than text/HTML source mapping.
- The project owns adapter pinning, packaging, verification, and upgrade testing.
- Professional DOCX/EPUB fidelity still requires larger fixtures and style/accessibility assays.

## Residual risks and unproven claims

This decision does **not** claim that the spike parser is production-ready. The run explicitly retains:

- production Markdown parser selection/schema work;
- full Workbench AST versioning;
- bibliography/CSL resolution;
- tables, lists, math, raw-HTML and richer extension policy beyond the bounded probe;
- byte-addressed DOCX/EPUB reverse source maps;
- professional reference DOCX styling;
- EPUB accessibility validation;
- PDF strategy;
- external-binary distribution, licensing, signing and update-policy review;
- untrusted media/HTML sandboxing and resource-policy hardening;
- large-manuscript performance and professional publishing assays.

None of these gaps grants Pandoc additional canonical authority.

## Revisit triggers

Reopen this ADR if any of the following occurs:

1. a pinned Pandoc version cannot produce an accepted professional output without rewriting canonical semantics;
2. a security or sandboxing requirement cannot be met at the adapter boundary;
3. packaging/licensing constraints make the adapter impractical to distribute;
4. source-map or accessibility requirements require target-writer hooks the adapter cannot provide;
5. DOCX/EPUB golden fixtures show consequential semantic drift across a required upgrade;
6. another adapter materially reduces risk while preserving the same Constellation-owned boundary;
7. owning a specific binary writer becomes cheaper than maintaining the adapter contract.

## Rollback

The adapter is intentionally replaceable. A future reversal changes the DOCX/EPUB adapter implementation and associated packaging, not canonical Sheets, Manifest identity, compile-plan semantics, or writer-owned project data.

Changing the Manifest/Compile Profile authority split after F2 has **high reversal cost** and therefore requires a separate migration/architecture decision.

## References

- `spikes/compile-pipeline/OFFICIAL_SOURCE_NOTES.md`
- `spikes/compile-pipeline/README.md`
- `docs/specifications/compile-contract-v0.2.md`
- https://pandoc.org/filters.html
- https://pandoc.org/MANUAL.html
- https://github.com/jgm/pandoc/releases/tag/3.10.1
- https://github.com/jgm/pandoc/releases/tag/3.9.0.2
