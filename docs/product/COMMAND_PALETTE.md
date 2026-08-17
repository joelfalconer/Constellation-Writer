# Command Palette Contract v0.1

## Purpose

The command palette is the summonable action and navigation layer. It is not a chat interface.

## Modes

- **Commands:** invoke registered actions.
- **Quick open:** locate Sheets, manuscripts, sources, and entities.
- **Scoped search:** enter literal or structured queries.
- **Recent context:** return to recently active spans or Sheets.

The palette may blend modes when ranking remains explainable.

## Result contract

Each result contains:

```yaml
id: stable_result_or_command_id
label: human_readable_label
kind: command|sheet|manuscript|entity|search_scope|recent_context
scope: current_selection|sheet|manuscript|project|global
consequence: safe|reversible_local|canonical_low|canonical_high|destructive|ai_mutating
reason: exact_match|recent|alias|command_keyword|structural_match
shortcut: optional
```

## Laws

1. Opening target p95 ≤ 80 ms, hard target ≤ 150 ms.
2. Search updates do not block typing in the editor.
3. Destructive or high-consequence commands expose scope before confirmation.
4. The palette closes after a completed action unless the action is explicitly iterative.
5. Escape restores the prior editor state.
6. AI operations are labelled as transformations and route to PatchSession review.
7. Commands are registry-owned and testable, not scattered UI callbacks.

## Ranking order

1. exact command or title match;
2. current manuscript context;
3. recent use;
4. alias and keyword match;
5. project-wide fuzzy match;
6. optional semantic suggestions, visibly labelled.

## Empty and failure states

- No results: preserve query and offer scope changes.
- Index rebuilding: run direct canonical scan for supported scopes.
- Ambiguous destructive target: block execution and require explicit selection.
