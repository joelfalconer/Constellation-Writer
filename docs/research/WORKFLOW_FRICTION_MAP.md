# Workflow and Friction Map v0.2

**Updated:** 2026-08-17  
**Status:** design-friction hypotheses with current mechanic references.

| Workflow | Desired Constellation state | Candidate friction class | Current benchmark evidence | Design response | Validation still needed |
|---|---|---|---|---|---|
| start/resume | return immediately to meaningful context | launch detour, lost location | Drafts EU-019 shows text/list/action separation but not resume performance | recent-context return token with fallback | measured resume tests |
| draft | stable prose flow | chrome, lag, analysis noise | iA Writer EU-018 documents editor-level Focus/Syntax/Style toggles | Editor Doctrine, Draft mode, latency budget | editor spike + sustained-writing assay |
| structure | move chunks without text surgery | folder/order conflation | Ulysses EU-016 and Scrivener EU-017 document Sheet/Binder chunk operations | placement IDs and manifest order | binder/manifest prototype |
| recall | find known and half-known material | weak retrieval, detour into other surfaces | Drafts EU-019 workspaces; Obsidian EU-020 backlinks/cache/graph | layered search with explained results | precision/recall task suite |
| revise | inspect changes without visual overload | overlapping diagnostics | iA Writer EU-018 demonstrates reversible text analysis overlays | individually governed overlays | CodeMirror/rival revision tests |
| annotate | comments survive edits and remain private | inline clutter, stale anchors | no sufficient current benchmark evidence collected in this pass | dedicated annotation logs and hybrid anchors | split/merge/re-anchor tests |
| research | sources remain adjacent and attributable | disconnected notes or tool switching | Scrivener EU-017 documents project material outside compiled manuscript; Obsidian EU-020 supports linked local notes | source records and material Sheets | research-led writer studies |
| compile | output matches intent | hidden inclusion and lossy transforms | Ulysses EU-016; Scrivener EU-017; Vellum EU-022; Atticus EU-023 document different assembly/export boundaries | frozen plan, QA, source map | issue #5 golden outputs |
| script planning | screenplay structure remains specialist without contaminating prose | page-aware semantics leaking into generic manuscript model | Final Draft EU-021 documents Beat Board → Outline Editor → pages | script Sheet/dialect + adapter boundary | screenplay-specific assay |
| AI assist | useful transformation without authorship loss | silent rewrite, context leakage | no vendor evidence in this refresh validates PatchSession governance | ContextPack and PatchSession | patch-review and privacy tests |
| recover | understand what is safe under stress | vague errors, overwrite, restore fear | Obsidian EU-020 documents rebuildable metadata cache; Atticus EU-023 documents cloud autosave/JSON backup, but neither validates Constellation recovery | buffers, snapshots, conflict bundles, calm copy | failure injection |
| handoff/publish | share clean manuscript without private debris | format mismatch, hidden loss | Scrivener EU-017, Vellum EU-022, Atticus EU-023 establish multiple export/formatting models | handoff/archive presets and deterministic compile | privacy + round-trip tests |

## Evidence discipline

The `candidate friction class` column is **not** transformed into evidence merely because a benchmark product has a related feature. Current official documentation supports the mechanics in the evidence column. The claims that those mechanics reduce or create friction remain hypotheses until observed or measured.

## Cross-workflow tensions

- Rich metadata versus clean external files. Ulysses External Folders provide a current example of capability tradeoffs when using interoperable Markdown rather than native library storage (EU-016).
- Immediate authoring appearance versus publication appearance. Scrivener Compile and Vellum formatting demonstrate product-level separation of working text and output styling (EU-017, EU-022).
- File truth versus derived recall. Obsidian explicitly documents local Markdown plus a rebuildable metadata cache powering Graph/Outline (EU-020).
- Integrated writing/publishing convenience versus local-first authority. Atticus documents cloud autosave and integrated formatting/export, creating a useful design contrast rather than a negative product judgment (EU-023).
- Specialist screenplay semantics versus general prose architecture. Final Draft documents page-aware outlining and Beat Board workflow (EU-021).
- Provenance retention versus privacy and archive size remains untested in the benchmark evidence collected here.
