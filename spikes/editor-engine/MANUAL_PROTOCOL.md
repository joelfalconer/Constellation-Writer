# Physical Editor Assay Protocol

## Purpose

Close the evidence classes that hosted Chromium automation cannot validly represent before ADR-0005 is treated as a durable editor-engine commitment.

## Environment capture

Record OS/version, hardware, display scale, keyboard/input method, browser/Electron version, assistive technology, language/IME, project fixture hash, editor package versions, and build commit.

## Six-hour writer protocol

Use representative longform work rather than synthetic typing. Keep the editor dominant and use normal Draft/Revise transitions. At hours 1, 3, and 6 record hesitation before common actions, accidental mode changes, cursor or scroll loss, unprocessed warning residue, save checking, visual discomfort, selection mistakes, undo distrust, and time to resume after interruptions.

## IME and mixed-script veto tests

On Windows and macOS, test at least one real East Asian IME with candidate windows, composition updates, conversion, cancellation, undo, selections crossing composition boundaries, and revision decorations active. Test mixed Arabic/Hebrew/English text with keyboard navigation and selection.

A composition event emitted by JavaScript is not a pass.

## Accessibility veto tests

Run keyboard-only operation plus VoiceOver on macOS and Narrator or NVDA on Windows. Verify character, word, line, paragraph, heading and selection navigation; stable accessible naming; no focus traps; usable 200% zoom; forced/high-contrast modes; and semantic before/after information for revision states.

## Native interaction tests

Exercise clipboard cut/copy/paste, drag selection, Finder/Explorer text/file drag where applicable, context menu, undo/redo, dead keys, platform shortcuts, and long-press/key-repeat behavior in the selected Electron shell.

## Hard vetoes

Reject or reopen ADR-0005 for source-text loss, composition corruption, inaccessible core text navigation, materially broken bidi caret/selection, persistent cursor/scroll loss, or sustained input latency above the accepted budget on representative writer hardware.
