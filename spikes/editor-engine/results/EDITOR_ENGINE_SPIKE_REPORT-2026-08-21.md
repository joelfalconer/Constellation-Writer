# Professional Prose Editor Engine Spike Report

Date: 2026-08-21  
Run: `CW-F1-EDITOR-SPIKE-004`  
Issue: #4  
Decision candidate: ADR-0005

## 1. Decision-relevant answer

Select **CodeMirror 6 as the F2 professional prose editor scaffold**, with ProseMirror retained as the serious fallback/rival.

This is a bounded architecture decision, not a declaration that the editor is production-proven. CodeMirror passed the automated hard gates that matter most to Constellation Writer's source-text architecture: exact source preservation, revision-overlay non-mutation, undo round trip, return-token scroll stability, and a 50,446-word longform control. ProseMirror performed comparably in the hosted synthetic latency measurements, but its Markdown parse/serialize boundary failed the dedicated source-fidelity round-trip fixture, demonstrating the normalization pressure expected from making a structured document model primary while canonical manuscript truth remains plain text.

Physical IME, screen-reader, bidi caret/selection, six-hour writer use, native interaction, and representative-hardware latency remain explicit veto or revisit conditions.

## 2. Run boundary and provenance

The original `docs/delivery/ROADMAP_EXECUTION_PROMPTS.md` was not present in the repository tree available to this run. The exact Shared Execution Header was therefore recovered from the already-preserved `RUN_PROMPT-03-DESKTOP_SHELL_SPIKE.md`. The Sequence Item 4 work order was grounded in issue #4, ADR-0005, and the current Typography, Modes, Navigation Return, Accessibility, Ergonomics, and Performance Budget contracts.

This is a degraded provenance mode, recorded rather than silently reconstructed.

Research OS v0.4.1 was used with the `computational_analysis` profile. Deterministic scripts own the fixture generation, measurements, hard-gate checks, and artifact capture. Model reasoning owns interpretation and the decision proposal.

## 3. Controls

Both candidates run in the same Vite/Chromium harness against the same deterministic 50,446-word fixture.

The shared control includes:

- Draft and Revise modes;
- 66ch prose measure and professional-editor typography baseline;
- typewriter positioning;
- overlapping comment/patch decorations;
- return-token capture and restoration;
- cursor, selection, undo/redo, and source extraction;
- mixed Japanese, Arabic, Hebrew, and English text;
- forced-colors and reduced-motion emulation;
- synthetic composition events with an explicit `synthetic_dom_event_only` evidence label.

CodeMirror keeps the canonical source string directly in editor state. ProseMirror parses Markdown into a structured document and serializes back through `prosemirror-markdown`, making normalization observable rather than hidden.

## 4. Resolved versions

| Component | Version |
|---|---:|
| `@codemirror/commands` | 6.11.0 |
| `@codemirror/lang-markdown` | 6.5.2 |
| `@codemirror/state` | 6.7.1 |
| `@codemirror/view` | 6.43.9 |
| `prosemirror-commands` | 1.7.2 |
| `prosemirror-history` | 1.5.0 |
| `prosemirror-keymap` | 1.2.3 |
| `prosemirror-markdown` | 1.13.6 |
| `prosemirror-model` | 1.25.11 |
| `prosemirror-state` | 1.4.4 |
| `prosemirror-view` | 1.42.2 |
| Playwright | 1.62.1 |
| Vite | 7.3.6 |
| Chromium | 151.0.7922.34 |

The Windows and macOS artifacts resolved the same dependency versions.

## 5. Measurements

Successful decision run: `32460827533` at head `fbe91cf91ae5122887768d8469a99d744277fb6d`.

| Platform | Engine | Keystroke p95 | Cursor p95 | Selection p95 | Pane toggle p95 |
|---|---|---:|---:|---:|---:|
| Windows | CodeMirror 6 | 17.6 ms | 18.2 ms | 18.2 ms | 17.5 ms |
| Windows | ProseMirror | 17.5 ms | 18.0 ms | 18.0 ms | 17.6 ms |
| macOS | CodeMirror 6 | 19.9 ms | 33.5 ms | 33.1 ms | 20.5 ms |
| macOS | ProseMirror | 20.6 ms | 34.8 ms | 33.3 ms | 18.4 ms |

Both engines are effectively tied for this hosted synthetic harness. The macOS cursor and selection p95 observations slightly exceed the current 32 ms maximum target for both controls. That is a warning and replication trigger, not a candidate-specific veto: it is one hosted-runner observation, affects both engines, and remains below the contract's sustained-failure threshold. Representative writer hardware must own the product budget decision.

## 6. Hard gates

| Gate | CodeMirror 6 | ProseMirror | Interpretation |
|---|---|---|---|
| 50,446-word fixture runs | pass | pass | both viable for bounded longform control |
| exact canonical source at mount | pass | longform fixture round trip pass | CM owns raw source directly; PM result depends on serializer equivalence |
| dedicated source-fidelity round trip | structurally exact by raw-text ownership | **fail** | PM normalized deliberately irregular Markdown source |
| revision overlay removal leaves source unchanged | pass | pass | both can keep decorations non-destructive |
| undo round trip exact | pass | pass | no veto |
| return-token scroll drift | 0 px | 0 px | no bounded pane-return veto |
| synthetic composition dispatch | survived | survived | not real IME proof |
| DOM textbox semantics | present | present | not screen-reader proof |

The dedicated source-fidelity fixture contains deliberate double spacing and Markdown surface choices. ProseMirror's parser/serializer did not reproduce it byte-for-byte. This does not make ProseMirror a poor editor. It makes it a weaker primary owner for a system whose canonical manuscript is the writer's exact plain-text file.

## 7. Preserved failures

Two Windows CI failures occurred before the successful run:

1. `32460543378`: `spawn EINVAL` while launching the Vite preview process under Node 24 on Windows.
2. `32460687987`: the same `spawn EINVAL` remained after converting the working-directory URL to a platform path.

The successful repair launches Vite through `process.execPath` and the absolute `vite.js` path. These are harness portability failures, not editor-engine failures. They remain recorded because the spike is evidence, not a highlight reel.

## 8. Evidence artifacts

- Windows: artifact `9438891488`, `sha256:68daf976fe6e08d264f071173a3e064d1fe0e1a52afdca666c36345eec5363e8`
- macOS: artifact `9438883335`, `sha256:a7fe1cddc5357ea9c0286d270b5ce917cb75ec441d1883e8dcb2fcc95a8fef0c`
- Foundation contracts at the measured head: run `32460827551`, success.

Each editor artifact contains the raw measurement report and resolved dependency graph.

## 9. Tournament / decision frame

Hard vetoes were applied before comparative preference.

Neither candidate showed an automated veto in undo, bounded selection, decorations, or return behavior. CodeMirror then wins the architecture decision primarily on **source sovereignty**, not on synthetic speed. The hosted timing frontier is effectively flat. ProseMirror offers a richer structured editing model, but that advantage is poorly aligned with the current invariant that manuscript truth is exact plain text and that editor transactions do not become domain mutation authority.

The selection is therefore:

1. **CodeMirror 6** - F2 scaffold winner.
2. **ProseMirror** - retained rival and fallback, especially if later product requirements make structured editing worth accepting a conversion boundary.

## 10. Unresolved physical vetoes

The following are explicitly **unmeasured**, not passes:

- real Japanese/Chinese/Korean and other IME candidate-window composition on Windows and macOS;
- VoiceOver and Narrator/NVDA traversal of character, word, line, paragraph, heading, selection, and revision states;
- mixed-script/bidi caret and selection behavior under real keyboard input;
- 200% zoom and physical OS high-contrast usability;
- native clipboard, drag, dead-key, key-repeat, and platform shortcut behavior inside the selected Electron shell;
- six-hour professional writing fatigue and native-feel assay;
- representative-hardware latency and long-session resource behavior.

The manual protocol in `spikes/editor-engine/MANUAL_PROTOCOL.md` is the required route for those controls.

## 11. Decision and rollback

ADR-0005 should accept CodeMirror 6 for the F2 editor scaffold with mandatory revisit triggers for any physical IME/accessibility/bidi veto, representative-hardware latency failure, or six-hour writer-assay failure.

A later editor-engine reversal must not migrate canonical writer-owned files, transfer durable authority into the editor document model, or alter Mutation Envelope/PatchSession ownership. Replace the editing adapter and projections, not the manuscript's truth model.

## 12. Route

- PR #13 review/merge closes issue #4 if the decision evidence is accepted.
- F1 remains `conditional_not_ready` until issue #5, `CON-003`, adversarial architecture closure, clean promotion validation, and human F1 approval are complete.
- Physical editor veto controls continue as explicit F2/F4 acceptance work, not retroactive claims about this hosted spike.
