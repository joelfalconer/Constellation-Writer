# Official source notes for compile spike

**Accessed:** 2026-08-21  
**Purpose:** establish documented Pandoc mechanics and pin reproducible adapter controls. These sources do not establish that Pandoc is architecturally fit for Constellation Writer; that decision belongs to the executable spike.

## Pandoc architecture

Official filters documentation describes Pandoc as a reader → Pandoc AST → writer pipeline, with filters operating on the AST between reader and writer.

- https://pandoc.org/filters.html
- https://pandoc.org/MANUAL.html

**Architectural use in this spike:** this supports treating Pandoc as a capable conversion engine, but does not grant it canonical authority. Constellation still freezes inputs, resolves Manifest semantics, builds its own compile plan/Workbench AST, and sends only a controlled adapter representation downstream.

## Reproducible builds

The official Pandoc user guide documents that targets including EPUB and DOCX contain build timestamps and that setting `SOURCE_DATE_EPOCH` makes those timestamps deterministic. It also notes that formats may contain other unique identifiers, so archive byte identity is not the only semantic-equivalence test.

- https://pandoc.org/MANUAL.html#reproducible-builds
- https://pandoc.org/demo/example33/18-reproducible-builds.html

The spike sets `SOURCE_DATE_EPOCH=946684800` for adapter invocations and separately compares semantic round-trip text.

## Pinned current control

Pandoc `3.10.1` is the current release used by this run.

- Release: https://github.com/jgm/pandoc/releases/tag/3.10.1
- Release date: 2026-07-22
- Linux amd64 asset: `pandoc-3.10.1-linux-amd64.tar.gz`
- Published SHA-256: `72948bf5784f560d5ad1876709daca27e0667f262da727bb33f77b58e52df2f5`

## Prior-version drift control

Pandoc `3.9.0.2` is used as the immediately relevant prior stable control available in the official release series.

- Release: https://github.com/jgm/pandoc/releases/tag/3.9.0.2
- Linux amd64 asset: `pandoc-3.9.0.2-linux-amd64.tar.gz`
- Published SHA-256: `a69abfababda8a56969a254b09f9553a7be89ddec00d4e0fe9fd585d71a67508`

The workflow verifies both asset digests before execution.

## Evidence boundary

Official documentation establishes product mechanics, not Constellation-specific fitness. The following require deterministic evidence from this repository:

- whether Manifest authority survives the adapter boundary;
- whether adapter failure preserves direct fallbacks;
- whether source-map provenance remains usable;
- whether DOCX/EPUB semantic output remains equivalent across pinned versions;
- whether unsupported syntax/loss is surfaced through QA rather than hidden;
- whether the implementation cost is preferable to owning every binary writer ourselves.
