# Local User State Spec v0.1

## Purpose

Preserve the writer's working context without turning cursor positions, pane choices, and recent activity into canonical project metadata.

## Authority

User state is local, ephemeral or recoverable application state under:

```text
.workbench/user-state/<local-user-id>/
```

It may be stored in SQLite or versioned JSON snapshots. It is safe to delete from the perspective of manuscript truth.

## State classes

### Session context

- current project and manuscript;
- active placement and Sheet;
- cursor, selection, and scroll anchors;
- Draft/Revise and focus state;
- pane widths and visibility;
- open search or review context.

### Recent context

- recently edited Sheets and spans;
- recent searches;
- recent compile profiles;
- interruption return tokens.

### Preferences

- theme and typography profile;
- shortcuts;
- focus settings;
- accessibility settings;
- default archive and AI privacy choices.

## Laws

1. User state cannot change compile output.
2. Deleting user state cannot damage canonical files.
3. User state never overwrites canonical state after divergence.
4. Recovery-critical text belongs in recovery buffers, not ordinary user state.
5. Sensitive recent-text excerpts are minimized and retention-controlled.
6. A project copied to another machine opens without user state.

## Restore order

1. Validate project and manuscript IDs.
2. Resolve active Sheet.
3. Resolve selection/cursor anchors against current revision.
4. Restore panes and mode.
5. Fall back visibly when context no longer resolves.

## Retention

Recent locations may be capped by count and age. Search history and excerpt storage can be disabled. Preferences persist until reset.

## MVP

Resume context, pane state, typography preferences, recent Sheets, return tokens, and safe fallback.
