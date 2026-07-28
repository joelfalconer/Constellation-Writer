# ADR-0006: Own the compile plan and use Pandoc as a candidate output adapter

- Status: proposed
- Decision class: medium reversal cost
- Review gate: Compile Spike C1

## Context

The product must own deterministic manuscript resolution, semantic roles, QA, and source mapping. It also needs professional Markdown, HTML, DOCX, and later EPUB output without recreating every document writer immediately.

Pandoc parses inputs into an abstract syntax tree, permits AST filters, and writes many target formats including HTML, DOCX, and EPUB. Its own documentation warns that conversions from richer formats may be lossy.

## Decision

Constellation Writer owns:

- frozen input revisions;
- manifest expansion;
- semantic compile plan;
- Workbench AST;
- QA and output source map;
- artifact verification.

Pandoc may be invoked as a pinned, sandboxed adapter for selected outputs after the Workbench AST has been transformed into a controlled Pandoc representation. Pandoc is not the canonical compiler or state owner.

## Risks

- Version changes may alter output.
- DOCX and EPUB transforms may lose unsupported semantics.
- External binary distribution and licensing/packaging require review.
- Untrusted HTML or media inputs require sandboxing and strict resource policy.

## Acceptance spike

Golden-test Markdown, HTML, DOCX, and EPUB outputs; verify headings, footnotes, citations, images, scene breaks, front/back matter, comments exclusion, deterministic semantics, and source-map continuity.

## References

- https://pandoc.org/demo/example2.html
- https://pandoc.org/filters.html
- https://pandoc.org/demos.html
