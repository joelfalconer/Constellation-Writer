# PatchSession Spec v0.2

**Status:** candidate  
**Imports:** Mutation Envelope, provenance, revision, anchor, consequence contracts

## Role

PatchSession is the writer-facing review, provenance, and decision container for one or more Mutation Envelopes. It no longer owns the complete transaction model by itself.

## Required behavior

- AI-originated canonical changes always begin as proposed patches.
- Patch targets include stable object IDs, base revisions, hashes, and anchors where relevant.
- Review supports accept, reject, edit, defer, and partial acceptance.
- Stale bases block blind application.
- Applied changes produce resulting revisions and logged outcomes.
- Reversal is a new governed mutation.

## Patch formats

- Unified diff for text
- JSON Patch or object merge for parsed metadata
- File operations for create, move, split, merge, and delete
- Generated records for candidate entities, claims, and evidence

## Authorship

The system distinguishes source, authorship, acceptance, and provenance. Human acceptance does not erase AI origin; AI origin does not remove human authority over the final manuscript.

## MVP

Whole-patch accept/reject, base-revision validation, readable logs, provenance, stale detection, and snapshot-backed reversal. Hunk-level partial acceptance follows immediately after the vertical slice.
