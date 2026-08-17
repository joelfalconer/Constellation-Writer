# Accessibility Test Matrix v0.1

## Platforms

- Windows with Narrator and NVDA where available.
- macOS with VoiceOver.
- Keyboard-only operation on every supported desktop platform.

## Matrix

| Area | Tests | Hard gate |
|---|---|---|
| Editor | character/word/line/paragraph navigation, selection, IME, bidi | no blocked authorship path |
| Navigator | tree traversal, reorder, indent/outdent, inclusion | pointer not required |
| Palette | open, search, result reason, consequence, escape return | focus returns correctly |
| Inspector | landmark naming, contextual updates, controls | updates do not steal focus |
| Diff review | before/after semantics, hunk decisions | color not sole signal |
| Recovery | save failure, conflict, restore preview | safety and actions announced |
| Compile | warning list, source jump, progress | no inaccessible final-export blocker |
| Visual | 200% zoom, high contrast, forced colors, dark/light | no clipped essential controls |
| Motion | reduced motion | no required animated meaning |

## Keyboard gate

Create a project, write, navigate, split, reorder, search, compile, snapshot, review a patch, and restore without pointer input.

## Reporting

Record defect severity, task blocked, workaround, platform, assistive technology, reproduction, affected invariant, and acceptance owner.
