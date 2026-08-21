# Hosted Spike Limitation Log

The following evidence states are deliberately unresolved by CI:

| Requirement | Hosted evidence | Status |
|---|---|---|
| real IME candidate-window behavior | synthetic DOM composition events only | unmeasured physical veto |
| screen-reader navigation | role/ARIA/contenteditable inspection only | unmeasured physical veto |
| 200% zoom | browser layout can be exercised but not human usability | manual assay required |
| OS high contrast | Playwright forced-colors emulation | partial, not physical validation |
| native clipboard/drag | browser control only | selected-shell physical assay required |
| six-hour editing | protocol specified, not automated | human assay required |
| long-session fatigue | cannot be simulated honestly | human assay required |
| representative hardware latency | hosted runner measurements only | replicate on writer hardware |

CI results may select an F2 scaffold only if these limits remain explicit revisit conditions.
