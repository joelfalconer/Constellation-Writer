# F0 Project Defined Acceptance Receipt

Date: 2026-08-17
Repository: `joelfalconer/Constellation-Writer`
Gate: F0 Project Defined
Decision: **accepted and promoted to `main`**

## Decision evidence

The project owner explicitly instructed that foundation PR #1 be merged. Before promotion, the PR head `35d6bfbd305c6f386781f249cc6588b65b4fb60b` had a successful foundation validation workflow (`32008685742`). PR #1 was then promoted through merge commit `1f01da3c76611d9ad9b1b297c2b8f265a91a6daa`.

## Accepted scope

F0 acceptance promotes the project charter, product constitution, scope/non-goals, authority model, canonicality matrix, invariant registry, common contract kernel, integrated specification candidates, reference fixture, validation machinery, delivery plan, and recorded unresolved risks as the canonical foundation for continued work.

## Explicit non-claims

F0 acceptance does **not** close F1, F2, F3, or F4. It does not prove:

- Tauri 2 is the correct desktop shell;
- CodeMirror 6 is adequate for professional prose;
- the compile/Pandoc boundary is correct in practice;
- atomic writes or recovery work in executable code;
- compile output is deterministic in implementation;
- professional writers find the editor superior or sustainable under long sessions.

Those claims remain routed to the technology spikes, evidence backfill, vertical slice, trust drills, and professional workflow assay.

## Next route

1. Complete evidence-locator backfill and benchmark refresh (#7).
2. Execute shell, editor, and compile spikes (#3, #4, #5).
3. Integrate results and issue the F1 gate decision.
4. Build durable substrate vertical slice #6 toward F2.
5. Execute F3 trust drills.
6. Build and assay the Writer Chair toward F4.

Rollback condition: if F1 or later executable evidence falsifies a foundation decision, supersede the affected ADR/contract through the normal governed change process rather than treating F0 promotion as irreversible.