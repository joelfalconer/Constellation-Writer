# Typography and Reading System v0.1

## Default prose surface

```yaml
base_size_px: 18
line_height: 1.55
line_width_ch: 66
line_width_modes: {narrow: 56, standard: 66, wide: 76, review: 82}
paragraph_spacing_em: 0.85
minimum_side_padding_px: 24
typewriter_line_position_percent: 42
```

The implementation may tune values after testing, but must preserve readable measure, strong cursor visibility, and stable layout under pane changes.

## Font posture

- Default to a serious editorial serif or highly readable system text face.
- Keep a monospace option for raw Markdown and code-heavy material.
- Font selection is a view preference, never a manuscript transform.
- Project archives need not contain font binaries.

## Paragraph profiles

- `book_draft`: optional first-line indent, compact paragraph gap.
- `essay`: no first-line indent, open paragraph gap.
- `screenplay`: Fountain-aware display profile.
- `poetry`: preserve line breaks and white space.

Display profiles must not rewrite source text.

## Markdown visibility

- `semantic`: syntax visible but visually quiet.
- `assisted`: inactive syntax softened without becoming inaccessible.
- `raw`: complete source presentation.

## Accessibility laws

- Body text meets WCAG AA, AAA preferred for default themes.
- Selection, caret, focused controls, diagnostics, and patch states cannot rely on color alone.
- Zoom and font-size changes preserve line identity, cursor, and scroll anchor.
- Reduced motion removes nonessential transitions.

## Validation

Typography testing includes six-hour use, 200% zoom, narrow windows, dark and light modes, high contrast, IME composition, bidi text, and screen reader traversal.
