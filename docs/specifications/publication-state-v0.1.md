# Publication State Spec v0.1

## Purpose

Preserve what canonical inputs produced a released or externally relied-on artifact, so later drafts can be compared without confusing current working canon with published fact.

## Publication state object

```yaml
id: pub_...
project_id: prj_...
manuscript_id: ms_...
compile_id: cmp_...
name: Issue 01 release
status: candidate|released|withdrawn|superseded
created_at: timestamp
released_at: optional
input_revisions:
  - object_id: sh_...
    revision_id: rev_...
    content_hash: sha256:...
compile_profile_id: cp_...
compile_profile_version: 0.1.0
artifact_records: []
source_map_path: publications/<id>/source-map.json
qa_report_path: publications/<id>/qa.json
checksums_path: publications/<id>/checksums.sha256
canon_scope: main
```

## Canonicality

Publication state is a durable event/record. Artifacts may be canonical release records, while previews remain derived.

## Release flow

```text
freeze revisions → resolve compile plan → validate → compile → verify → create publication archive → review → mark released
```

A released state is immutable. Corrections create a new publication state linked by `supersedes` or `corrects`.

## Continuity integration

Claims can be scoped or locked to publication states. A draft contradiction with published material is a high-severity continuity issue, not an automatic manuscript error.

## Source-map requirement

Every output segment should map back to manuscript placement, Sheet, revision, and source span where technically possible.

## Artifact records

Record format, path, hash, MIME type, renderer/adapter version, and verification result.

## Withdrawal

Withdrawing a release records reason, actor, timestamp, and successor. It does not erase the previous publication state.

## MVP

Publication archive for an explicit final compile, frozen input receipt, checksums, QA, source map, and supersession links.
