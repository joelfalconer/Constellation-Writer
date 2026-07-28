# Draft, Revise, and Focus Modes v0.1

## Draft mode

Optimizes forward prose production.

Visible by default:

- prose;
- minimal location marker;
- quiet save state;
- optional word target.

Hidden by default:

- comments and annotations;
- style diagnostics;
- entity and claim overlays;
- AI suggestions;
- compile warnings not threatening work safety.

## Revise mode

Supports inspection and controlled change.

Available overlays:

- annotations;
- changed-since-snapshot;
- provenance;
- style and repetition findings;
- compile warnings;
- entity and claim evidence;
- proposed patches.

Overlays are individually toggled and fully dismissible.

## Focus mode

Focus is a presentation state, not a separate canonical mode.

Reveal sequence:

1. hide Inspector;
2. hide Navigator;
3. reduce status detail;
4. retain save, conflict, and recovery-critical information;
5. keep command palette and emergency navigation available.

## State ownership

- mode and pane state: local user state;
- overlay configuration: local user preference;
- prose and annotations: canonical files;
- analysis results: derived unless explicitly saved as records.

## Laws

- Switching modes never rewrites prose.
- Draft mode does not nag with background analysis.
- A mode switch preserves selection, cursor, and scroll.
- Critical save or conflict state remains visible in every mode.
