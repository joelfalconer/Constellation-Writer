# Recovery and Backup Spec v0.2

**Status:** candidate  
**Imports:** `INV-REC-001`, `INV-CONFLICT-001`, Mutation Envelope

## Doctrine

Trust beats magic. The writer should know what is saved, what is recoverable, what is backed up, and what requires action.

## Integrated model

- Canonical single-file writes use atomic replacement.
- Active unsaved text has a recovery buffer.
- High-consequence and destructive operations create recovery artifacts through the Mutation Envelope.
- Multi-file operations use an operation plan and recovery bundle.
- Automatic and manual snapshots preserve point-in-time state.
- Archives contain canonical and selected logged files, excluding derived caches by default.
- Restore previews consequences and creates a pre-restore snapshot.
- Sync conflicts preserve base, application, and external versions.
- Corrupted SQLite is quarantined and rebuilt.

## Trust indicators

Normal saved state remains quiet. Save failure, conflict, recovery availability, or backup absence remains visible until resolved. A safety panel may explain: last canonical save, active recovery buffer, latest snapshot, latest archive, and whether only derived indexes are rebuilding.

## Minimum gate

Force crash during typing, corrupt SQLite, delete `.workbench/`, interrupt a multi-file operation, create an external edit conflict, revert an applied AI patch, and restore an archive on a clean fixture. Zero silent loss is permitted.
