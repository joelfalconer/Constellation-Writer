# Import and Interoperability Spec v0.1

## Purpose

Bring external writing into Constellation Writer without hiding loss, inventing structure, or trapping the imported project in a proprietary representation.

## Supported initial inputs

- plain text and Markdown;
- folders of text files;
- DOCX;
- HTML;
- Fountain;
- Scrivener and Ulysses exports through documented interchange formats rather than private database reverse engineering.

PDF is a source/material import, not a reliable manuscript round-trip format.

## Import stages

```text
inspect → fingerprint → parse → map → preview → approve → mutate → validate → receipt
```

### Inspect

Record source path, format, hash, encoding, package structure, file count, and available metadata.

### Parse

Convert into a neutral import model. Do not write canonical files yet.

### Map

Propose Project, Manuscript, Placement, Sheet, annotation, source, and asset records. Every new durable object receives a new typed ID unless a trusted Constellation ID is present.

### Preview

Show:

- objects and files to create;
- proposed order and nesting;
- headings and formatting transforms;
- unsupported or lossy elements;
- assets copied or externally linked;
- comments, footnotes, and citations treatment.

### Apply

Use a high-consequence Mutation Envelope, operation plan, and recovery bundle.

## Interoperability laws

1. Import never silently discards unsupported content.
2. Source files are not modified.
3. Original source may be copied into `materials/imports/` with hash and provenance.
4. Export or handoff formats do not become canonical project state.
5. Plain Markdown remains usable outside the app.
6. Round-trip claims must be earned per format through golden tests.

## Loss classes

```yaml
loss_classes:
  none: semantic_content_and_structure_preserved
  presentation_only: visual_formatting_changed_but_semantics_preserved
  recoverable: content_preserved_in_source_or_attachment_but_not_native
  semantic: meaning_or_structure_cannot_be_preserved
  unknown: requires_user_review
```

Semantic loss blocks import acceptance unless explicitly overridden.

## Format notes

### Markdown and folders

Prefer one Sheet per file; use headings and directory structure only as proposed assembly, never identity.

### DOCX

Map paragraphs, headings, lists, footnotes, comments, citations, and images into the neutral import model. Track unsupported fields and revision markup.

### Fountain

Preserve Fountain text semantics and create script-aware Sheets or a single imported script according to the chosen import profile.

## Receipt

Each import emits source hashes, mappings, warnings, created IDs, file paths, operation ID, validation result, and rollback locator.

## MVP

Markdown, text, directory, DOCX, and Fountain import with preview, loss report, and rollback.

## Deferred

Native Scrivener package parsing, Ulysses library parsing, FDX, advanced tracked-change round trip, cloud document import, and collaborative history.
