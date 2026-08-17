# Trust Laws

1. **Legibility:** the app can explain where durable work lives.
2. **Acknowledgement:** saved, unsaved, buffered, conflicted, and backed-up states are distinguishable.
3. **Reversibility:** high-consequence transformations have a tested return path.
4. **Attribution:** non-human and imported changes retain provenance.
5. **Conservatism:** uncertain conflict resolution preserves both versions.
6. **Determinism:** compile semantics derive from frozen inputs and a versioned profile.
7. **Degraded operation:** cache, network, graph, semantic, and AI failure do not prevent local drafting.
8. **No counterfeit certainty:** inferred claims, fuzzy anchors, and lossy imports expose uncertainty.
9. **Privacy by boundary:** context packs, recovery buffers, and private logs are not included in handoff archives by default.
10. **Repair transparency:** automatic repair reports exactly what it changed and how to undo it.

## Trust acceptance questions

- Can the writer tell whether the last paragraph is on disk?
- Can the project open after deleting `.workbench/`?
- Can an external edit be reconciled without overwrite?
- Can a compile warning be traced to its source?
- Can an AI-assisted change be inspected and reversed?
- Can a full archive restore on a clean machine?
