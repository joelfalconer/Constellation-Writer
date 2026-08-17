# Editor Doctrine v0.2

**Status:** candidate  
**Supersedes:** unintegrated v0.1 draft after acceptance  
**Imports:** `INV-AUTH-001`, `INV-RETURN-001`, canonical user-state separation

## Doctrine

The editor is the sovereign authorship surface. It holds prose, selection, cursor, revision overlays, and minimal safety state. Navigator, inspector, command palette, compile, Compendium, and AI remain summonable and jurisdictionally bounded.

## Locked direction

- Semantic plain-text editing, not a block-editor manuscript body.
- Draft and Revise are the only primary cognitive modes in the first release.
- Typing never waits on indexing, graph, sync, compile, or AI.
- Cursor, scroll, pane layout, and recent context are local user state, not canonical Sheet sidecar fields.
- Every summoned tool preserves or provides a return path to the prior Sheet, selection, cursor, and scroll context.
- AI appears through reviewable patches, comments, or reports, never ambient ghost text by default.

## Performance budgets

- Keystroke to visible character: ideal under 16 ms, failing when sustained above 50 ms.
- Recent Sheet switch: ideal under 80 ms.
- Command palette open: under 80 ms.
- Initial project search results: under 200 ms for reference scale.
- Autosave must not block typing.

## Pane jurisdictions

- Editor: prose and revision overlays.
- Navigator: location, order, and manuscript structure.
- Inspector: current-object metadata and instruments.
- Command palette: action, navigation, and transformation invocation.
- Status layer: save, conflict, target, and relevant trust state.

## Minimum gate

A writer can create, resume, draft, split, move, search, compile, recover, and return to the exact sentence without a dashboard or permanent AI surface.

## Open decisions

- CodeMirror 6 versus ProseMirror versus native component.
- Exact Markdown syntax-softening behavior.
- Split-editor support in first release.
- Typography defaults after fatigue testing.
