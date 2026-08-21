# ADR-0005: Select CodeMirror 6 as the F2 professional prose editor scaffold

- Status: accepted
- Accepted scope: F2 editor scaffold, subject to explicit physical veto and revisit conditions
- Decision class: high reversal cost
- Review gate: F1 technology review
- Evidence issue: #4
- Evidence run: `32460827533`
- Evidence report: `spikes/editor-engine/results/EDITOR_ENGINE_SPIKE_REPORT-2026-08-21.md`

## Context

The editor is Constellation Writer's sovereign authorship surface. It must preserve exact plain text, native-feeling selection and undo, keyboard fluency, low latency, large-document viewport performance, and layered revision decorations without becoming a block editor or transferring durable domain authority into its internal document model.

The original candidate was CodeMirror 6 because it separates state and view, routes local edits through transactions, and can be configured as a prose instrument while canonical source remains the Sheet file. F1 required that candidate to survive a serious ProseMirror control rather than becoming architecture by preference.

## Decision

Use **CodeMirror 6 as the F2 professional prose editor scaffold**.

Keep domain operations above the editor transaction model:

- CodeMirror transactions represent immediate editor-local changes;
- canonical manuscript source remains the exact writer-owned Sheet text;
- autosave and durable writes flow through the governed native/domain boundary and Mutation Envelope semantics;
- PatchSessions remain reviewable transformation/provenance objects;
- editor decorations, viewport state, syntax assistance, and analysis overlays do not become canonical manuscript state;
- the editor adapter must remain replaceable without migrating project formats.

Retain ProseMirror as the principal structured-editor rival and fallback.

## Evidence

A bounded spike ran CodeMirror 6 and ProseMirror in the same Vite/Chromium harness against one deterministic 50,446-word longform fixture on GitHub-hosted Windows and macOS runners.

Successful decision head: `fbe91cf91ae5122887768d8469a99d744277fb6d`.

- editor workflow `32460827533`: success on Windows and macOS;
- foundation validation `32460827551`: success.

Resolved CodeMirror versions were `@codemirror/state` 6.7.1, `@codemirror/view` 6.43.9, `@codemirror/commands` 6.11.0, and `@codemirror/lang-markdown` 6.5.2. The rival used ProseMirror view 1.42.2, state 1.4.4, model 1.25.11, markdown 1.13.6, history 1.5.0, commands 1.7.2, and keymap 1.2.3. Both artifacts ran Chromium 151.0.7922.34 through Playwright 1.62.1.

Both candidates:

- ran the same 50,446-word fixture;
- supported bounded Draft/Revise and overlapping decoration controls;
- preserved source while decorations were toggled;
- completed exact undo round trips in the tested operations;
- restored the recorded return token with 0 px scroll drift in the bounded pane-toggle control;
- exposed textbox/contenteditable semantics;
- survived synthetic composition event dispatch, which is explicitly not real IME evidence.

### Hosted p95 observations

| Platform | Engine | Keystroke | Cursor | Selection | Pane toggle |
|---|---|---:|---:|---:|---:|
| Windows | CodeMirror 6 | 17.6 ms | 18.2 ms | 18.2 ms | 17.5 ms |
| Windows | ProseMirror | 17.5 ms | 18.0 ms | 18.0 ms | 17.6 ms |
| macOS | CodeMirror 6 | 19.9 ms | 33.5 ms | 33.1 ms | 20.5 ms |
| macOS | ProseMirror | 20.6 ms | 34.8 ms | 33.3 ms | 18.4 ms |

These are hosted-runner synthetic transaction-to-next-frame observations, not product SLO proof. The macOS cursor/selection p95 values slightly exceed the current 32 ms maximum target for both engines. This is retained as a representative-hardware replication trigger rather than used as a false candidate discriminator.

## Why CodeMirror won this gate

### 1. Exact source sovereignty is architectural, not cosmetic

CodeMirror directly preserved the canonical source string at mount and through the tested revision-overlay operations. This aligns with the invariant that manuscript truth is the writer's exact plain-text file rather than a serialization of an editor-internal document model.

### 2. The serious rival exposed conversion pressure

The ProseMirror control deliberately used its Markdown parser/serializer boundary. It could round-trip the generated longform fixture, but it failed the dedicated source-fidelity fixture containing deliberately irregular Markdown surface choices such as double spaces. That observed normalization pressure is acceptable in many structured editors, but is poorly aligned with Constellation Writer's current file-sovereignty contract.

### 3. Synthetic performance did not justify taking the structured-model cost

Neither engine established a meaningful hosted-runner performance advantage. The timing results are close enough that source ownership, writer-surface behavior, accessibility risk, and reversal cost dominate the decision.

### 4. CodeMirror can keep revision machinery non-destructive

The control demonstrated overlapping revision decorations that disappear without mutating canonical source. This supports the Draft/Revise doctrine and PatchSession model without requiring revision metadata to live inside manuscript text.

## Hard-veto state

No automated hard veto was observed for CodeMirror in exact source preservation, bounded undo/selection operations, revision overlay removal, return-token restoration, or 50k rendering.

The following remain **unmeasured physical vetoes**, not passes:

- real IME candidate-window composition and conversion;
- VoiceOver and Narrator/NVDA text and revision-state navigation;
- mixed-script/bidi caret and selection under real keyboard input;
- physical OS high contrast and 200% zoom usability;
- native clipboard/drag, dead keys, key repeat, and platform text-service behavior;
- six-hour professional writer fatigue and native-feel testing.

Representative-hardware latency is also a mandatory replication condition because the macOS hosted run observed cursor/selection p95 around 33 ms for both engines.

## Consequences

Positive:

- canonical plain text does not require parser/serializer round trips to remain exact;
- Markdown semantics and syntax assistance can be layered without making a hidden rich-document store canonical;
- revision/comment/AI overlays can remain decorations and sidecar/domain records;
- the selected Electron shell and editor can share a stable Chromium baseline;
- editor-local transactions remain separable from domain mutation authority.

Costs:

- CodeMirror is code-editor-rooted and requires deliberate prose ergonomics rather than accepting its defaults;
- bidi, IME, accessibility, native text conventions, and long-session feel require continuing product-specific work;
- decorations and widgets can still damage selection fidelity if abused;
- prose semantics that a structured editor gets natively must be implemented through parsing, syntax trees, sidecars, or derived projections.

## Rejected alternative

ProseMirror is rejected as the primary F2 manuscript editor for now, not as a technology. Its structured document model is powerful, but the tested Markdown conversion boundary demonstrated source-normalization pressure that conflicts with the stronger plain-text canonicality requirement.

Keep the rival spike until after the editor physical veto suite and professional writer assay have run.

## Mandatory revisit triggers

Reopen this ADR if:

1. physical IME testing finds composition corruption, candidate-window failure, or destructive undo behavior;
2. VoiceOver or Narrator/NVDA finds a critical CodeMirror-specific navigation or selection failure;
3. real bidi caret/selection behavior is materially incorrect;
4. representative writer hardware shows sustained input/cursor/selection latency outside the accepted budget;
5. six-hour writer assays show persistent editor fatigue, native-feel failure, or return-to-sentence distrust;
6. revision overlays require state that cannot remain non-destructive and source-external;
7. future product requirements make a structured document model worth explicitly changing the canonical-source contract.

## Rollback

The editor choice may change without migrating canonical Sheet files. Keep domain operations, annotations, PatchSessions, and Mutation Envelope authority outside the editor engine. A later reversal should replace the editor adapter and its derived state, not writer-owned data or durable authority.

## References

- `spikes/editor-engine/results/OFFICIAL_SOURCE_NOTES.md`
- `spikes/editor-engine/results/EDITOR_ENGINE_SPIKE_REPORT-2026-08-21.md`
- `spikes/editor-engine/MANUAL_PROTOCOL.md`
