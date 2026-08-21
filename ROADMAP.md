# Roadmap

## F0: Project Defined

**State: accepted 2026-08-17.**

The charter, Run Contract, scope, glossary, deliverables register, authority model, risk posture, Product Constitution, contract kernel, reference fixture, and foundation validation package were promoted through foundation PR #1.

Evidence: `docs/programme/F0_ACCEPTANCE_RECEIPT-2026-08-17.md`.

## F1: Architecture Coherent

**State: accepted 2026-08-22.**

The accepted architecture package includes:

- Electron as the F2 desktop shell scaffold;
- CodeMirror 6 as the F2 professional prose editor scaffold;
- typed UUIDv7 durable identity;
- Manuscript Manifest ownership of order, membership, placement role/title, and semantic break intent;
- Constellation-owned compile plan and Workbench AST with a pinned replaceable Pandoc edge;
- Mutation Envelope as the sole canonical application authority;
- PatchSession as the review/provenance container when review-bearing;
- Recovery as preservation/restore machinery, with restore applied through the Mutation Envelope;
- noncanonical local cursor/scroll/pane/recent-context state;
- Claim-owned Compendium `canon_state`;
- annotation storage deliberately deferred pending F2 executable evidence.

Evidence: `docs/validation/F1_ARCHITECTURE_COHERENT_RECEIPT-2026-08-22.md` and `docs/validation/F1_ADVERSARIAL_ARCHITECTURE_CLOSURE-2026-08-22.md`.

## F2: Substrate Executable

**State: active 2026-08-22.**

First executable gate:

```bash
python tools/local_validate.py --suite all
```

A passing local receipt from a real repository checkout is required before the repaired compile implementation is treated as executable substrate. Hosted GitHub Actions is optional/manual replication only and is not a project gate.

Execute durable substrate vertical slice #6:

- scan and validate canonical files;
- atomically replace individual Sheet files where the filesystem supports the required primitive;
- use recovery-backed, crash-detectable operation plans for multi-file mutations;
- persist/recover recovery buffers;
- render/reorder manifest placements without changing prose;
- build/delete/rebuild SQLite working catalog;
- preserve competing external versions;
- snapshot and restore;
- run mandatory failure injection;
- emit receipts for recovery/conflict operations;
- prove no SQLite-only durable field exists.

Current execution note: the initiating ChatGPT runtime could not obtain a repository checkout because outbound DNS could not resolve `github.com`. That observation is infrastructure-unavailable, not a validation pass or failure. The local receipt remains mandatory.

## Manuscript Machine

Build the resolved compile plan, Workbench AST, direct Markdown/HTML paths, approved DOCX/EPUB adapter path, QA, source maps, and publication archive. Execute all golden cases against frozen canonical inputs.

## F3: Trust Proven

Run destructive recovery drills against the executable substrate:

- crash and interrupted atomic-write stages;
- disk/permission failure;
- corrupt SQLite and deleted derived state;
- competing file edits and duplicate IDs;
- failed multi-file mutation;
- patch/migration rollback;
- archive checksum validation and clean-directory restore.

## Writer Chair

Build the writer-facing desktop slice using accepted shell/editor decisions. Preserve navigator/editor/inspector jurisdiction, Draft/Revise/Focus modes, keyboard-first operation, return-to-sentence behavior, literal recall, accessibility, IME, and performance instrumentation.

## F4: Writer Value Demonstrated

Run issue #8 against the integrated Writer Chair:

- professional workflows;
- sustained-use/fatigue assay;
- 20,000-word-day stress where appropriate;
- interruption recovery;
- accessibility, IME and bidi;
- comparison against serious control tools.

## Later layers

After F4, expand governed transformation, the minimal continuity boundary, semantic recall, graph projection, governed AI operations, optional sync, and public-alpha readiness only when preceding gates support them.

## Sequencing rule

**F0 → F1 → F2 → Manuscript Machine → F3 → Writer Chair → F4 → continuity/intelligence expansion.**

The Compendium, semantic recall, graph projections, and broad AI functionality remain schema-aware but implementation-deferred until the writing, manuscript, and recovery substrate has earned expansion.
