# Recovery Drills

| Drill | Injection | Expected result |
|---|---|---|
| RD-01 | terminate process before autosave completes | recovery buffer offered; saved file remains valid |
| RD-02 | terminate during atomic replace | target is old-valid or new-valid; temp artifacts assessed |
| RD-03 | fill destination disk | save not acknowledged; buffer retained; Save Copy offered |
| RD-04 | deny write permissions | buffer retained; exact permission error and actions shown |
| RD-05 | corrupt SQLite bytes | database quarantined and rebuilt from canonical files |
| RD-06 | corrupt Sheet sidecar | prose opens; sidecar recovered or quarantined with review |
| RD-07 | corrupt manuscript YAML | last valid snapshot offered; filesystem order never substituted silently |
| RD-08 | create external edit while Sheet dirty | base/current/external versions preserved for merge |
| RD-09 | fail midway through multi-file operation | recovery bundle supports rollback or completion |
| RD-10 | accept harmful AI patch | inverse patch or pre-apply snapshot restores prior state |
| RD-11 | fail schema migration | pre-migration snapshot restores readable prior schema |
| RD-12 | restore archive to clean path | checksums validate; caches rebuild; manuscript recompiles |

Each drill records environment, injected fault, files present before and after, hashes, recovery UI path, outcome, and unresolved residue.
