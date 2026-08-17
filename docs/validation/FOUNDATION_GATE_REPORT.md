# Foundation Gate Report v0.3

## Decision summary

**F0 Project Defined:** **accepted** and promoted to `main` through merge commit `1f01da3c76611d9ad9b1b297c2b8f265a91a6daa`.  
**F1 Architecture Coherent:** entered but `conditional_not_ready`.

F0 acceptance is a human project-definition decision. It does not convert technology candidates, executable-behavior hypotheses, or incomplete evidence lineage into F1 acceptance.

## Evidence available

- Programme definition, user/non-user profiles, scope, success definition, deliverables, and routing.
- Product Constitution, sovereignty, canonicality, authority, dependency, trust, anti-feature, and reversal-cost laws.
- Integrated component specifications and shared contract kernel.
- Research evidence ledger, source decisions, feature atomicity, switching/friction maps, benchmark dossier candidates, and coverage report.
- Expanded reference novel, deterministic validator, and negative controls.
- Product experience contracts and writer journey maps.
- Prototype stress, performance, recovery, privacy, accessibility, external-editor, compile-golden, and failure-injection test definitions.
- Candidate technology ADRs with routed spikes.
- F0 acceptance receipt linked to the merge and CI evidence.
- Clean `main` validation receipt for GitHub Actions run `32010291279`.

## F0 gate

| Criterion | State |
|---|---|
| project identity clear | pass |
| intended users and deliberate non-fit defined | pass |
| v1 scope and non-goals explicit | pass |
| authority hierarchy defined | pass |
| deliverables mapped and materialized | pass |
| success criteria testable | pass |
| backlog, milestones, owners/routes exist | pass |
| human acceptance | **pass: PR #1 merge instruction and merge commit** |
| post-merge clean CI baseline | **pass: run 32010291279** |

**F0 decision: accepted.**

## F1 entry gates

| Criterion | State |
|---|---|
| modeled durable fields have explicit candidate authorities | pass candidate |
| shared enums and lifecycles reconcile under validator | machine checked |
| reference fixture validates | pass at main run `32010291279` |
| negative fixtures fail for expected reasons | pass in CI contract suite |
| mutation/recovery ownership has one candidate direction | pass candidate through Mutation Envelope, critical tension retained as `CON-003` pending F1 confirmation |
| technology spike plans have hard gates | pass, issues #3–#5 |
| evidence-lineage gap has explicit route | pass, issue #7 |
| human F1 architecture approval | open |

## Active F1 blockers

1. **#3 shell spike:** Tauri 2 versus Electron must be measured before ADR-0004 can be accepted.
2. **#4 editor spike:** CodeMirror 6 must survive prose, IME, bidi, accessibility, selection, and sustained-load controls before ADR-0005 can be accepted.
3. **#5 compile spike:** the Workbench AST/Pandoc boundary must prove deterministic semantics, source maps, and graceful adapter failure before ADR-0006 can be accepted.
4. **#7 evidence lineage:** exact locators and current benchmark-source distinctions must be repaired before F1 human review claims strong evidence traceability.
5. **`CON-003` mutation ownership:** the shared Mutation Envelope direction remains a candidate resolution until F1 adversarial review confirms that PatchSession and Recovery do not retain competing transaction ownership.

## Sequencing clarification

Earlier foundation drafts listed durable substrate vertical slice #6 as an F1 blocker. The accepted roadmap execution sequence now closes **F1 Architecture Coherent before beginning F2 durable substrate vertical slice #6**. Accordingly:

- #6 is the first F2 executable gate after F1;
- #6 remains a powerful later falsifier of F1 assumptions;
- #6 is not treated as evidence already obtained;
- F1 may request a bounded implementation probe only if a specific architecture question cannot otherwise be resolved.

## Exceptions and unresolved material

- Deep Research evidence entries still require exact source-locator backfill.
- Benchmark dossiers are not yet fresh current-product audits.
- No desktop shell or editor candidate has passed its technology spike.
- No compile pipeline candidate has passed its golden implementation spike.
- No recovery implementation has passed failure injection.
- ADR-0004, ADR-0005, and ADR-0006 remain proposed.
- F1 human architecture approval remains open.

## Route

1. Execute #7 evidence lineage and benchmark refresh.
2. Execute technology spikes #3, #4, and #5, in parallel where practical.
3. Run the F1 adversarial architecture review against the resulting evidence.
4. Resolve or explicitly defer every serious rival and `CON-003` with falsifiers.
5. Issue an F1 pass receipt only if closure criteria are actually met.
6. If F1 passes, route directly into durable substrate vertical slice #6 for F2.

## Promotion rule

Documentation completeness is not architecture validation. F1 may not close until the current machine-checked contracts remain clean, the active F1 blockers are adjudicated with evidence, critical contradictions have accepted treatment, and the human F1 gate decision is recorded.
