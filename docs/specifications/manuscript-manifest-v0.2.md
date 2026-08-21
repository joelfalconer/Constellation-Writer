# Manuscript Manifest v0.2

**Status:** F1 candidate  
**Imports:** `INV-ASM-001`, object and placement identity contracts, Compile Contract v0.2 authority model

## Definition

A manuscript is a directed assembly of placement nodes that reference Sheets or structural objects. The Manifest owns **order, nesting, assembly inclusion, placement titles, semantic compile roles, and structural break intent**.

The Manifest is the canonical answer to “what is this work and in what order?” A Compile Profile may select an explicit export projection from that work, but it may not silently redefine the assembly.

## Identity model

- Manuscript ID identifies the assembly.
- Placement ID identifies a location in the assembly.
- Sheet ID identifies the durable authored object.
- Revision/content digest identifies the Sheet state frozen by a compile or historical record.

Placement ID and Sheet ID are distinct because one Sheet may appear in multiple manuscripts or placements without changing authored identity.

## Ordering

Array order is the v0.2 canonical ordering representation for solo-first human readability. Filesystem order, filename prefixes, Sheet creation time, and title sort are never authoritative.

Fractional/order keys remain a migration option triggered only by app-managed sync or concurrent Manifest editing. Until such a migration occurs, no second order field may disagree with array order.

## Node kinds

Current candidate kinds:

- `sheet_ref`
- `container`
- `generated`
- `asset_ref`
- `placeholder`

All placement nodes receive stable Placement IDs. UI-only state such as binder collapse, selection, scroll, transient color, and per-user view preferences is not canonical Manifest state.

## Assembly inclusion

### Authority law

Assembly membership resolves from the Manifest only:

1. parent placement assembly inclusion;
2. placement `include` when explicitly declared;
3. a Manifest/schema default when omitted.

A Sheet kind or sidecar default may help the application choose an initial value **when creating a placement**, but it is not a hidden compile-time authority after the placement exists.

A Compile Profile does not override assembly membership. It may define an explicit `scope` that selects a deterministic export projection of already-included placements. The compiler must report both dimensions separately:

```yaml
placement_resolution:
  assembly_include: true
  assembly_authority: manuscript_manifest
  export_selected: false
  export_reason: profile_scope_role_not_selected
```

This separation prevents “excluded from this output” from becoming indistinguishable from “not part of the manuscript.”

Excluded assembly material remains visible, searchable, and reusable by alternate Manifests. Material outside one profile scope remains part of the assembly even when absent from that target artifact.

## Semantic roles

Roles are contextual manuscript semantics, not styling instructions. A placement role such as `chapter`, `scene`, `appendix`, or `frontmatter` is owned by the Manifest.

A Compile Profile maps a resolved role to target-format treatment. It may not change `scene` into `chapter`, or otherwise mutate role truth to obtain convenient styling.

Sheet `kind` may suggest an initial placement role at insertion time, but the resulting placement role is canonical in the Manifest for that assembly context.

## Titles and headings

The Manifest owns contextual placement titles and title behavior. Authored headings remain Sheet text.

The compile plan must resolve the relationship explicitly so that, for example, a placement title identical to the first authored H1 does not accidentally render twice. A target profile may style or suppress the resolved semantic title according to declared rendering rules, but it cannot silently rename the placement in canonical state.

## Semantic breaks

Scene, section, page, and other structural break intent is Manifest context. The compiler carries break semantics into the Workbench AST. A renderer maps that semantic node to a target representation such as a scene divider, page break, or section boundary.

Target-specific formatting defaults may fill representation details only after semantic intent has been resolved.

## Multiple manuscripts and alternate cuts

One project may contain multiple Manifests. They may reuse the same Sheet pool while differing in order, placement titles, roles, and assembly membership.

Alternate cuts are separate explicit Manifests or declared variants, not hidden order states inside a Compile Profile. A snapshot records historical state; a variant defines a distinct current assembly; an export profile defines representation. Those are different objects.

## Binder implications

The structural navigator renders the Manifest, not the filesystem. Minimum operations include:

- add Sheet/container/placeholder;
- reorder and nest;
- toggle assembly inclusion;
- assign semantic role;
- edit contextual title behavior;
- reveal source file;
- show all usages of a shared Sheet;
- preview resolved export selection without confusing it with assembly inclusion.

Every pointer operation must have a keyboard equivalent. Binder collapse and other view state remain local user state.

## Compile significance

The compiler performs:

`Manifest assembly resolution → frozen Sheet revisions → explicit profile scope projection → linear compile plan → Workbench AST → target renderers/adapters`

The Manifest therefore provides structural truth to every target. A DOCX profile and an HTML profile may select different explicit scopes or representations, but neither becomes a second hidden Binder.

## Edge cases

- Missing included Sheet: compile hard error with preserved placement.
- Excluded parent with included child: child remains assembly-excluded until the parent context is included; no profile may tunnel through the parent silently.
- Same Sheet in two Manifests: valid and visible in usage metadata.
- Same Sheet twice in one Manifest: disallowed by default unless duplicate placement is explicitly supported and surfaced.
- External file rename/move: stable Sheet ID preserves identity; path registry/repair resolves location.
- Empty container: valid planning structure but profile/QA may warn if included in a final artifact.
- Generated node: generator contract and provenance must be deterministic and visible.
- Corrupt or conflicting Manifest: preserve both/conflict evidence; never infer a new order silently.

## Acceptance tests

- Filesystem sorting cannot change output order.
- Reordering modifies the Manifest but not Sheet prose or identity.
- One Sheet may appear across multiple manuscripts with shared-use visibility.
- Manifest assembly inclusion can be reconstructed without reading a Compile Profile.
- Profile scope can remove a placement from one output while `assembly_include` remains true.
- A Compile Profile attempting to reorder, change membership, or override semantic role fails validation or a compile hard gate.
- Preview and final export report the same resolved Manifest order and explicit scope projection.

## Locked F1 decisions

1. Manifest owns assembly order.
2. Manifest owns placement membership.
3. Manifest owns contextual semantic roles.
4. Manifest owns contextual title and semantic break intent.
5. Profile scope is a projection, not an assembly override.
6. Sheet kind/defaults may seed placement creation but are not hidden runtime authorities.
7. Placement IDs remain distinct from Sheet IDs.
8. Array order remains canonical until a deliberate ordering migration is approved.
