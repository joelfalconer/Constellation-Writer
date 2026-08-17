# Privacy Leakage Tests v0.1

## Test corpus

Use synthetic private markers:

```text
PRIVATE_SHEET_MARKER
AI_CONTEXT_SECRET
RECOVERY_ONLY_TEXT
EDITOR_HANDOFF_EXCLUDED
SERVICE_TOKEN_SHOULD_NEVER_EXIST
```

No real private manuscript content belongs in the public test repository.

## Test cases

1. **Editor handoff archive:** excludes recovery buffers, AI contexts, private annotations, unrelated sources, and session logs.
2. **Publication archive:** includes only frozen release inputs and declared publication records.
3. **Remote AI preflight:** blocks Sheets with `exclude_from_ai_context: true`.
4. **ContextPack preview:** exactly matches payload selected for transmission.
5. **Logs:** do not store service credentials or full prose unless required by a declared recovery/patch policy.
6. **Crash reports:** redact project paths and text by default.
7. **Temporary files:** removed after verified write; recoverable failures retain them only in declared recovery paths.
8. **Archive traversal:** malicious `../` and absolute paths are rejected.
9. **Symlink escape:** vault operations cannot write beyond authorized project root.
10. **Public fixtures:** scanner fails CI if likely secrets or private corpus markers are introduced.

## Hard gates

- no secret storage in project files;
- no excluded Sheet text in remote context payload;
- no private marker in handoff archive;
- no archive path traversal;
- privacy override is explicit and logged.
