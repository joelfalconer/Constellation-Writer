# Compile Contract v0.1

**Status:** initial candidate  
**Imports:** `INV-CMP-001`, Manuscript Manifest, Sheet Schema, provenance and validation contracts

## Purpose

Compile is a deterministic build pipeline that transforms canonical manuscript structure and content into explainable output artifacts.

## Inputs

- Project manifest
- Manuscript manifest
- Resolved Sheet revisions
- Sheet metadata and annotations
- Compile profile
- Style map
- Assets and sources

## Stages

1. Resolve inclusion and roles.
2. Freeze input revisions.
3. Build a linear compile plan.
4. Validate required content and references.
5. Parse source into an internal semantic document model.
6. Apply profile transformations.
7. Render target format.
8. Validate artifact.
9. Emit QA report and output source map.
10. Optionally create a publication archive.

## Required outputs

- Artifact
- Compile receipt
- QA report
- Source map from output segments to manuscript placement, Sheet, revision, and source span

## Determinism

Identical canonical inputs, frozen revisions, profile semantics, and compiler version must produce semantically equivalent output. Byte identity is preferred where practical but not required for formats containing nondeterministic metadata.

## Initial targets

Markdown and HTML are the first executable targets. DOCX follows once semantic and source-map behavior is proven. EPUB and screenplay formats remain planned.

## Hard warnings

Missing included Sheet, broken required asset, invalid profile, and unresolved destructive conflict block final compile. Comments, stale evidence, unreviewed AI provenance, duplicate titles, and unsupported syntax are profile-governed warnings.
