# Vertical Slice Receipt

```yaml
receipt_id: CW-VERTICAL-SLICE-001
status: pending_execution
issue: 6
validation_state: unreviewed
```

This file is intentionally **not** a completion receipt yet. It reserves the destination and required evidence so the project cannot later substitute a narrative summary for executable proof.

## Required evidence before status may become `tested`

- commit SHA and environment;
- project create/open receipt;
- atomic Sheet write result;
- crash/recovery result;
- manifest reorder hash comparison;
- SQLite delete/rebuild result;
- external conflict preservation result;
- named snapshot and Sheet restore result;
- validator report before and after cache deletion;
- failure-injection results;
- unresolved defects and severity.

## Promotion rule

Do not mark F2 or this receipt complete until the executable loop in issue #6 has run and artifacts are preserved.
