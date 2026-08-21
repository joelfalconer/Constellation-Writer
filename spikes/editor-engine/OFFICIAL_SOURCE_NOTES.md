# Editor Engine Official Source Notes

## CodeMirror 6

Primary references inherited from ADR-0005:

- https://codemirror.net/docs/guide/
- https://codemirror.net/docs/ref/

The spike uses the documented state/transaction/view/decorations architecture and keeps canonical source outside editor-state serialization.

## ProseMirror

Primary references:

- https://prosemirror.net/docs/guide/
- https://prosemirror.net/docs/ref/

The rival is intentionally tested as a structured-document editor with Markdown parse/serialize boundaries rather than pretending it is a plain-text buffer. This makes source normalization observable rather than hidden.

## Version discipline

Package ranges are declared in `package.json`. Each CI artifact also records the resolved dependency graph. The decision report must cite those resolved versions rather than assuming the ranges resolved identically on every run.
