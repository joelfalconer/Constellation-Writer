# Asset and Source Spec v0.1

## Purpose

Define durable handling for images, audio, video, documents, research sources, citations, and external references without mixing them into manuscript prose or derived caches.

## Distinction

- **Asset:** a file used by the project or an output.
- **Source:** a provenance-bearing record used for research, citation, evidence, or derivation.
- One file may have both an Asset and a Source record.

## Canonical layout

```text
assets/
  originals/
  images/
  audio/
  video/
  documents/
  generated/
  assets.yml
sources/
  <source-id>.source.yml
materials/
  imports/
  research/
```

Generated previews, thumbnails, waveforms, OCR text, and embeddings live under `.workbench/` unless intentionally promoted with provenance.

## Asset record

```yaml
id: ast_...
kind: image|audio|video|document|cover|font_reference|other
path: assets/images/map.png
mime_type: image/png
sha256: ...
title: Orchard map
source_id: src_...
canonicality: canonical_state
usage: []
```

## Source record

```yaml
id: src_...
type: file|url|book|article|interview|transcript|recording|research_note|previous_draft|compile_output|manual_statement
citation_key: optional
title: string
creators: []
locator: relative_path_or_url
accessed_at: optional
content_hash: optional
provenance: {}
rights: {}
```

## Laws

1. Required compile assets are copied into or explicitly vendored by the vault.
2. Absolute external paths are allowed only as visible risk-bearing references.
3. Missing optional assets warn; missing required assets block the relevant compile profile.
4. Generated files record generator version and parent IDs.
5. OCR output is derived until reviewed and promoted.
6. Source assertions remain attributed; they do not become direct observations.
7. Fonts may be referenced by name or licensing record, but font binaries are not committed or shared without rights.

## Checks

- path resolves;
- hash matches when required;
- duplicate binary detection;
- MIME and extension agreement;
- rights and privacy flags;
- compile usage references valid IDs;
- source citations resolve.

## MVP

Images, PDFs/documents as materials, source records, citation keys, internal copying, missing-asset QA, and archive inclusion policy.
