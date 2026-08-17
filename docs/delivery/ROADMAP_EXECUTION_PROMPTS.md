# Constellation Writer Roadmap Execution Prompts

These prompts are execution work orders for ChatGPT/Codex-class agents with repository access. Use the **Shared Execution Header** plus one work order at a time. Do not collapse later gates merely because the repository contains detailed specifications.

## Shared Execution Header

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
```

---

## Prompt 00 — Post-merge canonical reconciliation and F1 entry

```text
TASK: Reconcile repository state after foundation PR #1 was merged and prepare a clean F1 entry state.

The merge of PR #1 is the explicit human F0 acceptance event. Do not reinterpret it as F1 acceptance.

Required work:
- Verify `main` contains merge commit `1f01da3c76611d9ad9b1b297c2b8f265a91a6daa` or its valid descendant.
- Reconcile `CURRENT_STATE.yaml`, `docs/validation/FOUNDATION_GATE_REPORT.md`, `docs/validation/F1_READINESS_REPORT.md`, `docs/programme/DELIVERABLES_REGISTER.yaml`, backlog, milestone language, and issue #2 so they no longer say F0 human acceptance is pending.
- Preserve F1 blockers: #3 shell spike, #4 editor spike, #5 compile spike, #7 evidence locator backfill, and any unresolved critical contradiction.
- Add/verify the F0 acceptance receipt and connect it to the merge commit and prior successful CI run.
- Run the foundation validator and contract tests from a clean checkout of main.
- Confirm no canonical/derived authority drift was introduced by promotion.

Acceptance:
- F0 is recorded `accepted` with explicit evidence.
- F1 remains `conditional_not_ready` unless all F1 closure criteria are actually met.
- Main validates cleanly.
- Every open F1 blocker has an owner/issue, acceptance test, and revisit trigger.

Deliverables:
- reconciled state files;
- F0 gate receipt;
- fresh validation receipt;
- focused PR and short transition note for issue #2.
```

## Prompt 01 — Evidence lineage and benchmark refresh (#7)

```text
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

## Prompt 02 — Desktop shell decision spike (#3)

```text
TASK: Execute issue #3 and decide ADR-0004 through measured Tauri 2 vs Electron evidence.

Build equivalent minimal shell controls. Do not build the product UI yet.

Both controls must include:
- editor placeholder using the same web editor component;
- native open/save dialogs;
- project-directory permission boundary;
- filesystem watcher;
- native menu and keyboard shortcut;
- clipboard and drag/drop;
- crash/restart fixture;
- safe bridge call for an atomic-file-write placeholder.

Test at minimum on Windows and macOS where the available environment permits, recording any environment limitation explicitly:
- startup time and idle memory;
- packaged size;
- 50k-word document rendering baseline;
- IME composition and mixed-script/bidi;
- accessibility tree, keyboard navigation, 200% zoom, high contrast;
- native dialog and menu behavior;
- symlink/path escape and permission boundary;
- crash/restart event handling;
- dev/build complexity and signing/package implications.

Decision method:
- Apply hard vetoes first: accessibility failure, unsafe file boundary, unacceptable editor behavior, or materially unfixable platform inconsistency.
- Compare surviving options on writer experience, reliability, security boundary, implementation complexity, packaging, and reversal cost.
- Do not reward Tauri merely for smaller binaries or Electron merely for ecosystem familiarity.

Deliverables:
- two bounded spike implementations;
- repeatable benchmark scripts/results;
- platform limitation log;
- ADR-0004 updated to accepted/rejected/deferred with evidence;
- desktop scaffold recommendation;
- PR linked to #3.
```

## Prompt 03 — Professional prose editor decision spike (#4)

```text
TASK: Execute issue #4 and determine whether CodeMirror 6 can satisfy the Editor Doctrine under serious prose load.

Candidate: CodeMirror 6.
Rival control: bounded ProseMirror and/or a native/contenteditable control for the hardest behaviors. The rival must be real enough to falsify a convenient CodeMirror choice.

Prototype requirements:
- Markdown Sheet editor preserving source-text sovereignty;
- standard/narrow/wide/review measures;
- Draft and Revise modes;
- typewriter scrolling;
- comments plus overlapping patch/annotation decorations;
- return-token restoration after navigation/pane changes;
- 10k, 25k, and 50k word Sheet fixtures;
- native-feeling undo, selection, clipboard, find, spellcheck where feasible;
- no block-document model leaking into canonical prose.

Measure:
- p50/p95/p99 keystroke-to-paint where measurable;
- cursor and selection latency;
- long-document degradation;
- IME composition;
- bidi/mixed-script;
- screen-reader semantics and keyboard navigation;
- 200% zoom/high contrast/reduced motion;
- pane toggles without scroll/cursor displacement;
- decoration removal returning to clean prose;
- browser/WebView differences relevant to the shell spike.

Run a bounded sustained-writing simulation now; reserve the full six-hour professional assay for F4.

Decision:
- Update ADR-0005 with measured evidence.
- Accept CodeMirror only if it can plausibly become a prose instrument rather than an IDE wearing linen.
- If a critical defect is fixable only through invasive forks, include that as reversal/maintenance cost.

Deliverables:
- spike implementation and fixtures;
- performance/accessibility report;
- rival comparison;
- ADR-0005 decision;
- editor package bootstrap recommendation;
- PR linked to #4.
```

## Prompt 04 — Compile architecture decision spike (#5)

```text
TASK: Execute issue #5 and prove or falsify ADR-0006: Constellation Writer owns compile semantics; Pandoc is only a pinned output adapter.

Build:
1. Freeze reference project inputs with object/revision hashes.
2. Resolve the manuscript manifest into a deterministic linear compile plan.
3. Parse Sheet Markdown into a minimal Workbench AST with semantic roles.
4. Apply title/heading/inclusion/scene-break/front/back matter transforms.
5. Render canonical Markdown and HTML directly from the Workbench pipeline.
6. Render DOCX and EPUB through a pinned Pandoc adapter.
7. Emit QA findings and output source maps resolving output segments to placement ID, Sheet ID, revision, and source span.

Use the repository golden cases, including front/back matter, chapter/scene roles, footnotes/citations, images/missing assets, comments excluded by default, unsupported extensions, repeated compile, and adapter-version comparison.

Hard gates:
- identical frozen canonical inputs + profile produce semantically equivalent output;
- every exclusion/lossy transform is explained in QA;
- source maps survive transforms sufficiently for traceability;
- Pandoc failure does not destroy the compile plan and leaves Markdown fallback;
- adapter-specific behavior never becomes hidden canonical semantics.

Deliverables:
- compile-plan and Workbench-AST implementation;
- direct Markdown/HTML renderer;
- pinned adapter proof for DOCX/EPUB;
- golden-test results;
- ADR-0006 decision;
- PR linked to #5.
```

## Prompt 05 — F1 Architecture Coherent closure

```text
TASK: Integrate the F1 evidence after #3, #4, #5, and the relevant portion of #7 complete. Decide F1 rather than merely summarizing it.

Inputs:
- accepted F0 foundation on main;
- current contract validation results;
- shell, editor, and compile spike receipts;
- refreshed evidence ledger/coverage report;
- unresolved contradictions and risks;
- ADR-0004/5/6 outcomes.

Perform an adversarial architecture review:
- identify any durable field with multiple canonical owners;
- detect enum/lifecycle drift;
- test object vs placement vs revision vs anchor identity boundaries;
- test Mutation Envelope vs PatchSession vs Recovery ownership;
- test whether technology choices force hidden canonical state or undermine portability;
- test whether editor/runtime choices weaken accessibility or source-text sovereignty;
- test compile semantics for adapter leakage.

For every serious rival, record accept/reject/defer and falsifier. Do not scalar-score away veto failures.

If closure criteria pass:
- update relevant ADRs to accepted;
- mark machine-checked contracts appropriately;
- issue `F1_ARCHITECTURE_COHERENT_RECEIPT.md` with evidence links;
- update CURRENT_STATE, roadmap, backlog, risks, and issue #2;
- route directly into #6.

If they do not pass:
- do not issue a pass receipt;
- create targeted remediation issues with acceptance tests and keep F1 open.

Deliverables:
- F1 gate report and receipt or failure report;
- cross-spec/authority validation output;
- updated decisions/risks;
- integration PR.
```

## Prompt 06 — F2 durable substrate vertical slice (#6)

```text
TASK: Execute issue #6 as the first real substrate implementation. The objective is executable evidence, not another design document.

Implement the required loop against the canonical reference vault:
1. create/open project;
2. scan and validate canonical files;
3. read Sheet frontmatter + sidecar;
4. edit and atomically write a Sheet;
5. persist and recover a recovery buffer;
6. render manuscript order from placement/Sheet IDs;
7. reorder a placement without changing prose;
8. create the SQLite working catalog;
9. delete `.workbench`/catalog and rebuild entirely from canonical files;
10. detect external modification and preserve base/current/external versions;
11. create a named snapshot;
12. restore an individual Sheet;
13. emit operation/recovery receipts.

Implement in clear package boundaries: vault, catalog, mutation, recovery, manuscript resolver, and a minimal CLI or desktop harness depending on the accepted shell decision.

Failure injection is mandatory:
- terminate before temp-file flush;
- terminate after temp write but before rename;
- fail rename/replace;
- disk-full/permission-denied simulation where feasible;
- corrupt SQLite;
- duplicate Sheet IDs;
- external edit during dirty in-memory state.

Hard gates:
- zero silent acknowledged-text loss;
- target canonical file is old-valid or new-valid after interrupted single-file write;
- no SQLite-only durable state;
- rename/move preserves object identity;
- validator passes before and after cache deletion/rebuild;
- conflicts preserve both versions;
- recovery events are explainable and reversible.

Deliverables:
- executable packages and harness;
- integration/failure tests;
- F2 vertical-slice receipt with raw evidence;
- updated specs only where implementation falsified them;
- PR linked to #6.
```

## Prompt 07 — P2 Manuscript Machine implementation

```text
TASK: Build the manuscript machine on top of the accepted F2 substrate and the compile architecture decision.

Scope:
- deterministic manifest resolver;
- resolved compile plan;
- Workbench AST;
- direct Markdown and HTML renderers;
- DOCX/EPUB adapter path only as approved by ADR-0006;
- semantic style mapping;
- compile QA;
- output source maps;
- publication archive package;
- compile preview model that never becomes a second editing truth.

Required behaviors:
- nested groups, chapters, scenes, front/back matter, appendices;
- explicit include/exclude and profile override precedence;
- title/heading suppression and numbering;
- scene/section breaks;
- alternate manuscript arrangements reusing the same Sheets;
- missing asset and unsupported-markup warnings;
- comments/annotations excluded unless profile says otherwise;
- same frozen inputs produce semantically equivalent build outputs.

Tests:
- execute every compile golden case in `tests/compile`;
- add regressions for every defect found;
- compare source maps against exact Sheet revisions/spans;
- prove failed adapter export leaves canonical state untouched and direct Markdown output available.

Deliverables:
- production-candidate compiler packages;
- compile QA/source-map artifacts;
- publication archive fixture;
- benchmark and determinism receipt;
- focused PR and roadmap state update.
```

## Prompt 08 — F3 Trust Proven: recovery, corruption, conflicts, rollback

```text
TASK: Close or fail F3 Trust Proven using destructive, repeatable tests against the executable substrate. Do not infer trust from unit-test coverage.

Run the repository failure-injection and recovery drill suite, expanding it where implementation exposes new boundaries.

Required disaster drills:
- editor/process crash with dirty recovery buffer;
- power-loss-style interruption at each atomic-write stage;
- disk full and permission denied;
- leftover temp/backup artifacts on reopen;
- corrupted SQLite/WAL/SHM and full rebuild;
- deleted `.workbench` directory;
- corrupted Sheet sidecar;
- corrupted manuscript manifest;
- external edits while clean and while dirty;
- cloud-sync-style competing versions and duplicate IDs;
- multi-file mutation failure midway;
- accepted AI/script patch reversal via inverse patch or snapshot;
- failed migration rollback;
- archive export, checksum validation, restore to a clean directory, and rebuild.

UX evidence is part of the gate:
- every failure message states what happened, what is safe, what is at risk, and available actions;
- no conflict message blames the writer;
- no repair silently overwrites a competing canonical version.

Hard pass conditions:
- zero silent data-loss events across the defined matrix;
- every recoverable disaster has a tested route;
- derived corruption never requires canonical reconstruction from cache;
- archive restore reproduces canonical content and manuscript semantics;
- patch/migration rollback leaves receipts.

Deliverables:
- raw drill logs and fixtures;
- recovery/failure test implementation;
- UX recovery-copy findings;
- F3 gate receipt or explicit failure report;
- defect issues with rollback/retest criteria.
```

## Prompt 09 — P3 Writer Chair implementation

```text
TASK: Build the first writer-facing product slice only after the shell/editor decisions and durable substrate are stable enough to support it.

Goal: make the editor worthy of being the throne before broad Compendium/AI work begins.

Implement:
- desktop project open/recent project flow;
- navigator + dominant editor + collapsible inspector jurisdiction;
- Draft, Revise, and Focus modes;
- typography profiles and adjustable measure;
- typewriter scrolling and paragraph focus;
- quick open and command palette;
- literal/project search and structural navigation;
- keyboard registry commands;
- Sheet create/rename/move/split/merge where substrate supports them;
- save/recovery/conflict status that is quiet when healthy and explicit when unsafe;
- return-token preservation of Sheet, cursor, selection, scroll, and mode across summonable tools;
- compile preview entry/return;
- revision overlays that disappear cleanly in Draft mode.

Do not add:
- persistent AI chat pane;
- graph-first navigation;
- dashboard home that demotes the editor;
- block-editor manuscript semantics;
- mandatory account/sync.

Instrument from day one:
- keystroke/cursor/selection p95/p99;
- Sheet switching;
- quick-open/search latency;
- scroll/cursor displacement incidents;
- recovery-buffer status;
- background-index contention.

Deliverables:
- usable writer-chair build;
- telemetry/benchmark harness using synthetic fixtures and privacy-safe local metrics;
- accessibility smoke tests;
- product screenshots/interaction recordings where useful;
- PR plus pre-F4 readiness receipt.
```

## Prompt 10 — F4 professional-writer workflow assay (#8)

```text
TASK: Execute issue #8 against the real Writer Chair. This is an evaluation run, not a feature-development run.

Use fresh test projects and preserve raw observations. Where possible compare the same tasks against at least one established professional writing-tool control.

Assays:
- time to first word from cold launch;
- reopen project and return to exact prior sentence/context;
- 45–60 minute uninterrupted drafting block;
- repeated interruption/search/compile/return cycles;
- six-hour editing protocol;
- 20,000-word-day synthetic/high-volume workload;
- restructure chapters/scenes without prose corruption;
- revision overlays on/off and clean Draft return;
- crash/recover mid-session;
- keyboard-only core workflow;
- screen reader, IME, bidi/mixed-script, 200% zoom, high contrast, reduced motion;
- background indexing and compile during active work;
- confidence interview for save, recovery, conflict, and export states.

Measures:
- time to first word;
- time to resume sentence;
- keystroke/switch/search latency distributions;
- context-loss events;
- mode errors;
- cursor/scroll failures;
- pointer/keystroke burden on repeated tasks;
- save/recovery anxiety incidents;
- severe accessibility failures;
- perceived fatigue at intervals.

Evaluation rules:
- severe failures are vetoes, not numbers to average away;
- distinguish performance measurement from subjective preference;
- preserve dissenting participant observations;
- route architecture-caused failures back to earlier gates when necessary.

Deliverables:
- raw assay dataset and observation ledger;
- critical-incident log;
- control comparison;
- F4 gate decision with uncertainty;
- prioritized remediation backlog or Writer Value Demonstrated receipt.
```

## Prompt 11 — P4 Governed Transformation and Continuity Boundary

```text
TASK: After F2/F3 are stable and the Writer Chair is usable, implement the narrow governed-transformation and continuity boundary without turning the app into an AI cockpit or lore wiki.

Implement PatchSession UI:
- whole-patch and hunk/field-level accept/reject;
- before/after diff;
- intent, source, base revision, consequence, and provenance;
- stale patch detection;
- rebase review where confidence permits;
- inverse patch/snapshot rollback;
- review queue filtered by source/status/target.

Implement minimal Compendium Inspector:
- entity stubs;
- manual claims;
- evidence anchors to Sheet/revision/span;
- contradiction/conflict records;
- current-Sheet entity/claim lookup;
- candidate records clearly separated from active/locked canon.

Privacy/governance prerequisites for any AI extraction:
- explicit context-pack construction;
- per-Sheet AI exclusion;
- remote/local provider indication;
- provenance logging;
- candidate-only extraction;
- no silent Compendium or manuscript mutation.

Hard gates:
- writer can reject every proposed change without source mutation;
- stale base cannot blind-apply;
- partial acceptance does not force whole rewrite adoption;
- AI-origin content remains provenance-inspectable;
- no graph projection becomes canonical;
- Draft mode remains visually clean.

Deliverables:
- PatchSession review implementation;
- continuity Inspector implementation;
- privacy/context controls;
- stale/rebase/rollback tests;
- updated mutation/Compendium receipts and PR.
```

---

# Conditional post-F4 expansion prompts

Do not execute these merely because earlier schema placeholders exist. Their precondition is a stable Writer Chair, F3 trust evidence, and a positive or remediation-complete F4 outcome.

## Prompt 12 — Semantic recall without graph-first drift

```text
TASK: Add semantic/narrative recall as a derived, optional layer on top of proven literal/structural search.

First benchmark the failure cases of literal search using real or synthetic professional-writing recall tasks. Only add embeddings/semantic machinery where it demonstrably reduces recall latency or recovers otherwise lost context.

Requirements:
- canonical files unchanged;
- embeddings/indexes disposable and fully rebuildable;
- explicit index version/model metadata;
- per-project/private-data controls;
- semantic result always resolves to canonical Sheet/revision/span;
- literal and structural search remain first-class and available offline;
- stale embedding detection after edits;
- no semantic result silently becomes a claim or canon record.

Compare at least two indexing/retrieval approaches and measure precision/recall on a labelled fixture set. Record false-confidence cases, not just successful examples.

Deliverables: retrieval benchmark, derived-index contract, rebuild tests, UX integration that preserves editor jurisdiction, and ADR/PR.
```

## Prompt 13 — Compendium expansion and graph projection

```text
TASK: Expand Compendium only after the minimal continuity boundary proves useful.

Use observed user tasks to choose additions: relations, timelines, motifs, factions, settings, objects, source dossiers, continuity families. Do not implement fields merely because a graph schema can hold them.

Requirements:
- claims/evidence remain operational centre;
- manual canon, observed manuscript claims, and inferred candidates remain distinct;
- graph is a projection from canonical records;
- deletion of graph/index must not lose canon;
- contradictions and minority/alternate continuity remain visible;
- every graph edge is traceable to relation/claim/evidence records;
- current-Sheet and current-manuscript views take precedence over global graph spectacle.

Deliverables: usage evidence, schema delta, migration plan, expanded fixtures, projection builder/rebuild tests, continuity workflows, and PR.
```

## Prompt 14 — Governed AI operations

```text
TASK: Introduce AI only as governed operations that pay rent in writer time saved or recall/revision quality.

Candidate operations: rewrite suggestion, synopsis extraction, research condensation, entity/claim candidate extraction, continuity scan, style-drift report, compile QA recommendation.

For each operation:
- define writer intent and scope;
- construct inspectable ContextPack;
- disclose local/remote provider and sensitive exclusions;
- produce report or proposed PatchSession, never direct mutation;
- require review appropriate to consequence;
- preserve model/prompt/context/output hashes where privacy policy allows;
- support reject, partial accept, stale detection, rollback;
- evaluate against a no-AI/manual control on task time and error quality.

Do not build a persistent chatbot as the primary interface unless later evidence specifically justifies it.

Deliverables: operation contracts, privacy threat model, evaluation fixtures, UI flows, provenance/retention policy, tests, and staged PRs.
```

## Prompt 15 — Optional sync architecture

```text
TASK: Design and prototype optional app-managed sync only after solo local-first reliability is proven.

Start by testing the existing sync-neutral file contract under Dropbox/OneDrive/iCloud/Syncthing-style conflict patterns. Define exactly which failures an app-managed sync layer would solve.

Requirements:
- local project remains fully usable without account/network;
- canonical file format remains inspectable outside sync;
- no silent last-writer-wins on competing canonical edits;
- stable object/placement/revision identities survive device changes;
- conflicts preserve both versions and surface understandable merge choices;
- encryption/key-management and metadata leakage are explicitly threat-modelled;
- migration into/out of app sync is reversible;
- collaboration is not smuggled into v1 sync architecture.

Compare at least two synchronization models, including a simple file/snapshot model and an operation/CRDT-capable future path. Do not adopt CRDT complexity without a proven concurrent-editing requirement.

Deliverables: sync problem evidence, architecture alternatives, threat model, conflict simulation, prototype, ADR, rollback path, and PR.
```

## Prompt 16 — Public alpha readiness

```text
TASK: Determine whether Constellation Writer is ready for a bounded public alpha. This is a release gate, not a marketing exercise.

Audit:
- editor daily-use quality;
- F2/F3/F4 evidence;
- data-loss and migration risk;
- Windows/macOS packaging/signing/update path;
- import/export fidelity;
- archive/restore drill;
- privacy and AI defaults;
- accessibility blockers;
- crash diagnostics without sensitive manuscript leakage;
- documentation for project format, backups, recovery, troubleshooting, and leaving the product;
- schema/app/version compatibility policy;
- support and rollback plan.

Run fresh-machine installation and archive-restore tests. Create an alpha fixture project and a destructive upgrade/rollback rehearsal.

Hard blockers include any reproducible silent data loss, unrecoverable migration, inaccessible primary editing flow, hidden cloud dependency, or inability to export/restore owned files.

Deliverables: alpha-readiness report, blocker ledger, release checklist, migration/rollback receipt, support docs, and explicit go/no-go decision.
```

## Sequencing summary

Execute 00 → {01, 02, 03, 04 in parallel where resources allow} → 05 → 06 → 07 and 08 → 09 → 10 → 11. Prompts 12–16 are conditional expansions after the writer, manuscript machine, and trust substrate have earned them.
