# F0 Project Defined Acceptance Receipt

Date: 2026-08-17
Repository: `joelfalconer/Constellation-Writer`
Gate: F0 Project Defined
Decision: **accepted and promoted to `main`**

## Decision evidence

The project owner explicitly instructed that foundation PR #1 be merged. The accepted foundation head was `35d6bfbd305c6f386781f249cc6588b65b4fb60b`, which passed GitHub Actions run `32008685742` before promotion. PR #1 was then merged through commit `1f01da3c76611d9ad9b1b297c2b8f265a91a6daa`.

A clean GitHub Actions checkout of `main` at the merge commit passed run `32010291279`. The preserved `foundation-validation-report` artifact (`9281496266`, digest `sha256:5f45cd432d3f147d55cb73c71c3044e68b0dfc6ba4c0c8be46e9a0744e1936a5`) reports validator v0.2.0 `passed`, with 22 schemas, 3 Sheets, 2 manuscripts, and zero issues. The same workflow also completed the negative contract test suite successfully.

## Accepted F0 scope

F0 acceptance promotes the following as the canonical foundation for continued work:

- project charter, thesis, vision, users, anti-personas, scope and success definition;
- Product Constitution and F0 governance package;
- canonicality, authority, invariant, dependency, trust and anti-feature contracts as the accepted F0 baseline subject to later governed supersession;
- common contract kernel and integrated component specifications in their recorded candidate/machine-checked states;
- reference fixture, validator, validation definitions and delivery plan;
- recorded unresolved risks, contradictions and evidence gaps.

Acceptance of the package does not convert every candidate schema, ADR or implementation hypothesis into an F1-accepted decision.

## Explicit non-claims

F0 acceptance does **not** close F1, F2, F3, or F4. It does not prove:

- Tauri 2 is the correct desktop shell;
- CodeMirror 6 is adequate for professional prose;
- the compile/Pandoc boundary is correct in practice;
- the evidence ledger has complete exact source locators;
- atomic writes or recovery work in executable product code;
- compile output is deterministic in implementation;
- professional writers find the editor superior or sustainable under long sessions.

## Next route

1. Complete evidence-locator backfill and benchmark refresh in #7.
2. Execute shell, editor, and compile spikes #3, #4, and #5.
3. Resolve or explicitly retain any critical contradiction, including mutation-ownership tension `CON-003` until F1 adjudication confirms the shared Mutation Envelope boundary.
4. Run the F1 adversarial architecture review and issue an F1 gate decision.
5. If F1 passes, route directly to durable substrate vertical slice #6 for F2.

Rollback condition: if F1 or later executable evidence falsifies a foundation decision, supersede the affected ADR/contract through the governed change process rather than treating F0 promotion as irreversible.
