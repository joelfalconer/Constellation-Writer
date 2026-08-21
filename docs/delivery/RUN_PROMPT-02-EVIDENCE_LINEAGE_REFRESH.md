# Compiled Execution Prompt 02 — Evidence Lineage and Benchmark Refresh

Compiled from the Shared Execution Header and Prompt 01 in `docs/delivery/ROADMAP_EXECUTION_PROMPTS.md`.

```text
You are operating on `joelfalconer/Constellation-Writer`, whose `main` branch is the canonical project source of truth.

Before changing anything:
1. Read `README.md`, `CURRENT_STATE.yaml`, `ROADMAP.md`, `PROJECT_MANIFEST.yaml`.
2. Read `docs/constitution/PRODUCT_CONSTITUTION.md`, `CANONICALITY_MATRIX.yaml`, `STATE_AUTHORITY_MATRIX.yaml`, `INVARIANT_REGISTRY.yaml`, `DEPENDENCY_RULES.md`, and relevant ADRs.
3. Read the relevant specification(s), schemas, fixtures, validation contracts, issue body, and prior receipts.
4. Inspect current GitHub issues, PRs, CI state, and branch state instead of trusting stale prose.

Operating laws:
- The editor remains the sovereign authorship surface.
- Writer-owned files/manifests hold durable truth; derived stores must remain rebuildable.
- Never introduce SQLite-only durable state.
- Identity is independent of title/path/placement.
- Mutation Envelope owns transaction/application semantics; PatchSession owns review/provenance decisions.
- No AI or automation silently mutates canonical state.
- Preserve exact failures, minority findings, rejected alternatives, and unresolved risks.
- Use deterministic code/tests for parsing, hashing, validation, performance measurement, and reproducible transforms.
- Do not promote a technology or gate because the implementation is convenient or the documentation is persuasive.

Working method:
- Treat this as a Research OS `system_design_strategy` or `computational_analysis` run as appropriate.
- Establish a compact run contract in the run receipt.
- Prefer primary/official technical documentation when current external facts matter.
- Create a dedicated branch.
- Build the smallest executable artifact that can falsify the candidate decision.
- Add fixtures and negative controls before claiming success.
- Run tests and CI.
- Update ADRs/contracts only to the extent supported by evidence.
- Open a focused PR with measured results, unresolved risks, rollback path, and gate destination.
- Do not merge your own PR unless explicitly instructed.

TASK: Execute issue #7: backfill exact evidence locators and refresh benchmark evidence without contaminating architecture with model memory.

Use the existing Deep Research report and source registry as the starting corpus. For current product claims, research primary/official sources on the web and record access/version dates.

Required work:
- Backfill exact page/section/span locators for EU-001 through EU-010 where the source supports them.
- Keep conversation-derived EU-011+ explicitly classified as inference/design unless independently evidenced.
- Build or refresh benchmark dossiers for Ulysses, Scrivener, iA Writer, Drafts, Obsidian, Final Draft, Vellum, and Atticus.
- Separate historical report findings from current product-state observations.
- Update `SOURCE_REGISTRY.yaml`, `SOURCE_DECISIONS.yaml`, `EVIDENCE_UNITS.jsonl`, benchmark dossiers, `FEATURE_ATOMICITY.yaml`, `SWITCHING_MAP.md`, `WORKFLOW_FRICTION_MAP.md`, and `COVERAGE_REPORT.md` only where evidence warrants.
- Record unsupported claims as gaps, not guesses.

Hard gates:
- Every consequential benchmark claim has a locator or explicit unresolved reason.
- No inference is promoted to evidence by repetition.
- Current-version claims cite current primary sources.
- Architecture recommendations remain distinguishable from source assertions.

Output:
- evidence-delta report;
- updated machine-readable ledgers;
- source coverage matrix;
- contradictions/new uncertainties;
- PR linked to #7.
```
