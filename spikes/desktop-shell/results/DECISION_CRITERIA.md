# Shell Decision Criteria

## Hard vetoes

A candidate is vetoed if evidence shows any of the following without a credible bounded repair:

1. unsafe project-root or bridge boundary;
2. source-text editor behavior that is materially inconsistent across target platforms;
3. critical accessibility failure attributable to the shell/runtime;
4. critical IME/composition failure attributable to the shell/runtime;
5. crash/restart behavior that prevents the recovery architecture from operating predictably.

## Surviving-option comparison

After vetoes, compare:

- writer-surface consistency across Windows/macOS;
- reliability and crash isolation;
- security boundary clarity;
- native filesystem/dialog/menu integration;
- packaged/runtime cost without treating size as a proxy for quality;
- implementation and debugging complexity;
- signing/update burden;
- maintenance and reversal cost if the shell must later change.

## Decision statuses

- `accepted`: suitable scaffold with no known unresolved F1 veto; later empirical veto triggers may remain.
- `rejected`: a hard veto or dominated architecture is established.
- `deferred`: current environment cannot resolve a decision-critical uncertainty.

The evidence report must list unmeasured criteria rather than converting them into neutral scores.
