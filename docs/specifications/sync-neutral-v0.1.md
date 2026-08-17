# Sync-Neutral File Contract v0.1

## Purpose

Allow projects to survive ordinary file-sync tools without making synchronization a core v1 service or pretending that file sync provides transactional collaboration.

## Assumptions

- One active writer at a time is the supported v1 posture.
- Dropbox, OneDrive, iCloud Drive, Syncthing, Git, external editors, and manual copies may change files.
- Sync conflicts are normal and must preserve both versions.

## File behavior

- Canonical files are written atomically in their containing directory.
- Writes avoid touching unrelated files.
- Derived churn remains under `.workbench/` and is excluded from sync by recommendation.
- Relative paths are used inside the vault.
- IDs survive rename and move.
- File watchers treat events as hints and verify hashes before action.

## Ignore guidance

```text
.workbench/cache/
.workbench/indexes/
.workbench/previews/
.workbench/thumbnails/
.workbench/tmp/
.workbench/locks/
```

User state may be excluded by default. Recovery buffers should be backed up intentionally but not synchronously merged.

## Conflict protocol

1. Detect base-hash mismatch.
2. Suspend write acknowledgement.
3. Preserve base, in-memory/current, and external versions.
4. Create conflict manifest.
5. Offer three-way comparison when a common base exists.
6. Apply resolution through a Mutation Envelope.
7. Retain conflict receipt and rollback path.

## Unsupported v1 behaviors

- simultaneous editing of the same Sheet;
- automatic manifest merge after concurrent reordering;
- distributed locks;
- presence, comments, or permissions;
- conflict-free replicated data types.

## Git posture

Project files should produce intelligible diffs. Git integration may later create named snapshots or release commits, but Git is not required for writing or recovery.

## Acceptance

Copy a project between machines, rename Sheets, create competing Sheet edits, rebuild all derived state, and restore both versions without silent overwrite.
