# External Editor Compatibility Tests v0.1

## Purpose

Prove that durable Sheet text remains useful outside Constellation Writer and that external edits do not erase identity, structure, or recoverability.

## Editor classes

Test at least:

- generic plain-text editor;
- Markdown editor;
- command-line editor;
- file manager rename/move;
- formatter or line-ending normalizer.

Record versions and operating systems.

## Test cases

| ID | Action | Expected result |
|---|---|---|
| EXT-01 | open Sheet in generic text editor | prose and minimum frontmatter readable |
| EXT-02 | edit body and save | app detects revision and preserves ID |
| EXT-03 | rename Sheet file | app relocates by ID; manuscript refs survive |
| EXT-04 | move Sheet within vault | path mirror updates; order unchanged |
| EXT-05 | delete frontmatter | app detects identity loss and offers repair, never silently assigns ID |
| EXT-06 | change title heading only | identity remains; title-resolution rules visible |
| EXT-07 | change LF to CRLF | content opens and normalizes according to policy without prose loss |
| EXT-08 | add unsupported Markdown extension | editing continues; compile emits explicit warning |
| EXT-09 | edit while app has dirty buffer | both versions preserved in conflict bundle |
| EXT-10 | duplicate Sheet file | duplicate ID error blocks ambiguous writes |

## Pass criteria

- No hidden application block is required to read prose.
- External body edits are accepted when identity metadata remains valid.
- Rename and move never alter identity.
- Conflict creates a reviewable three-version bundle when a common base exists.
- Repair actions are logged and reversible.
