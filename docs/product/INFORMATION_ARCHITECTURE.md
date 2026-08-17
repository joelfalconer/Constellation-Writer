# Information Architecture v0.1

## Product frame

Constellation Writer is organized around the writer's active manuscript context, not around dashboards or a taxonomy browser.

## Primary surfaces

```text
Project
├── Writer Chair
│   ├── Navigator
│   ├── Editor
│   ├── Inspector
│   └── Command Palette
├── Manuscript Machine
│   ├── Binder / assembly
│   ├── Compile preview
│   ├── QA report
│   └── Artifacts
├── Recall
│   ├── Quick open
│   ├── Project search
│   ├── Recent context
│   └── Saved scopes
├── Continuity Sidecar
│   ├── Entities
│   ├── Claims
│   ├── Evidence
│   └── Conflicts
└── Trust
    ├── Save and recovery
    ├── Snapshots
    ├── Archives
    ├── Validation
    └── Project folder
```

## Default route

Opening a project routes to the most recent valid writing context:

1. active manuscript;
2. active Sheet;
3. cursor and scroll state for the local user;
4. active editor mode;
5. collapsed or revealed panes.

A damaged or missing recent-context record never blocks project opening. The app falls back to the manuscript's first included writable Sheet, then to a project overview only when no writable Sheet exists.

## Navigation hierarchy

### Level 1: project

Switch project, validate, snapshot, archive, inspect project folder.

### Level 2: manuscript

Switch assembly, create alternate arrangement, compile, inspect progress.

### Level 3: placement

Navigate Part, Chapter, Scene, Section, or other manifest node.

### Level 4: Sheet

Draft, revise, annotate, inspect metadata, follow evidence.

### Level 5: span

Selection, comment, patch review, citation, entity mention, evidence anchor.

## Cross-cutting instruments

Search, commands, recovery, and validation are cross-cutting. They are summoned from the current context and must preserve a return token.

## Anti-patterns

- Project home as a metric dashboard.
- Separate navigation systems for files, manuscripts, search, and Compendium that cannot explain their relationship.
- Context-free global commands that mutate unknown targets.
- Persistent secondary surfaces that reduce the editor below the dominant visual area.

## Acceptance

- A new user can explain Project → Manuscript → Placement → Sheet after one guided example.
- A returning user reaches the prior sentence without traversing a dashboard.
- Every result or warning exposes its scope and return path.
