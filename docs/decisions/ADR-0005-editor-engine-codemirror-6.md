# ADR-0005: Use CodeMirror 6 as the candidate editor engine

- Status: proposed
- Decision class: high reversal cost
- Review gate: Editor Spike E1

## Context

The editor must preserve plain text, native-feeling selection and undo, keyboard fluency, low latency, large-document viewport performance, and layered revision decorations without becoming a block editor.

CodeMirror 6 models editor state separately from the view and routes changes through transactions. Its modular extension system permits a narrow prose-oriented configuration rather than adopting a complete IDE shell.

## Decision

Prototype CodeMirror 6 as the primary text engine. Keep domain operations above its transaction model:

- CodeMirror transactions represent immediate editor changes;
- autosave groups acknowledged changes into Mutation Envelopes;
- PatchSessions remain reviewable domain transformations;
- canonical source remains the Sheet file, not editor state serialization.

## Risks

- CodeMirror is code-editor-rooted and may require substantial prose, IME, bidi, screen-reader, and typography work.
- Decorations and custom widgets can degrade selection fidelity if abused.
- Native platform text behavior may differ from WebView expectations.

## Acceptance spike

Test six-hour prose editing, 50,000-word Sheets, composition/IME, bidi text, screen reader navigation, native clipboard, typewriter scrolling, comments, overlapping revision overlays, and cursor preservation during pane changes.

## References

- https://codemirror.net/docs/guide/
- https://codemirror.net/docs/ref/
