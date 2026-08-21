# Editor Engine Spike: CodeMirror 6 vs ProseMirror

This bounded F1 spike tests whether CodeMirror 6 can serve as the sovereign prose editor without inheriting code-editor behavior that violates Constellation Writer's source-text, accessibility, selection, revision-overlay, return-to-sentence, or latency contracts.

The ProseMirror control is a serious structured-editor rival. Both controls run in the same Vite/Chromium harness, use the same deterministic 50,000-word fixture, expose the same Draft/Revise and return-token operations, and execute the same synthetic benchmark protocol.

## What this spike can establish

- exact source preservation at CodeMirror mount;
- source normalization pressure in the ProseMirror Markdown parse/serialize path;
- decoration toggling without source mutation;
- undo round trips;
- synthetic transaction-to-frame p95 observations;
- cursor/selection transaction behavior;
- pane-toggle return-token restoration;
- baseline DOM accessibility semantics;
- reproducible Windows/macOS Chromium renderer measurements.

## What it cannot establish in hosted CI

Hosted automation is not accepted as proof of real IME candidate-window behavior, VoiceOver/Narrator/NVDA traversal, physical high-contrast behavior, native platform clipboard/drag edge cases, or six-hour human fatigue. Those remain explicit manual veto tests.

## Commands

```bash
npm install
npm test
npm run build
npx playwright install chromium
npm run benchmark -- --platform=local
node scripts/evaluate-results.mjs results/raw/local-editor-engine.json
```
