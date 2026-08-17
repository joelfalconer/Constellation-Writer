# Accessibility and Inclusive Design Spec v0.1

## Baseline

- All core workflows are keyboard-operable.
- Main landmarks and controls expose stable accessible names.
- Focus order follows visible and task order.
- Focus is never trapped in palettes, dialogs, diff views, or sidebars.
- Text zoom to 200% preserves writing, navigation, and recovery flows.
- Status and warnings do not rely on color alone.
- Reduced-motion settings remove nonessential animation.
- High-contrast and forced-color modes remain usable.

## Editor-specific requirements

- Screen readers can navigate characters, words, lines, paragraphs, headings, and selections.
- IME composition is not interrupted by autosave, decorations, or background analysis.
- Bidi and mixed-direction text preserve caret and selection behavior.
- Patch decorations expose semantic before/after information outside color.
- Typewriter scrolling and focus dimming can be disabled independently.

## Cognitive accessibility

- Draft mode suppresses noncritical analysis.
- Commands disclose scope and consequence.
- Errors say what happened, whether work is safe, and what to do next.
- The same action uses consistent labels across palette, menu, shortcut help, and Inspector.

## Validation

Test with keyboard-only navigation, screen readers on supported platforms, reduced motion, high contrast, 200% zoom, long documents, IME input, and recovery dialogs under simulated stress.
