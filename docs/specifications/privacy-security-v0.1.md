# Privacy and Security Spec v0.1

## Security posture

Constellation Writer is local-first, not security-by-obscurity. The product minimizes network use, narrows filesystem capabilities, separates private history from handoff packages, and treats AI context as an explicit disclosure event.

## Data classes

```yaml
public: safe_for_public_artifacts
project_private: ordinary manuscript_and_metadata
sensitive: personal_legal_medical_client_or_embargoed_material
secret: credentials_tokens_keys
```

Secrets must never be stored in project files, patch logs, fixtures, or archives.

## Local storage

- Canonical project files inherit OS permissions.
- `.workbench/` may contain sensitive excerpts, caches, recovery buffers, and context packs.
- Logs minimize prose content unless needed for recovery or patch review.
- Temporary files are cleaned after verified writes and recoverable failures.

## AI context boundary

Before remote transmission:

1. resolve the exact ContextPack;
2. enforce Sheet and project exclusions;
3. show scope and provider;
4. require explicit operation initiation;
5. record model/provider and context hash;
6. retain or discard raw context according to policy.

No AI service is required for local writing.

## Archive presets

- `private_full`: may include patch history and private sources.
- `editor_handoff`: excludes recovery buffers, AI contexts, private annotations, and unrelated materials.
- `publication`: includes frozen inputs, profile, artifact, QA, and source map.

## Desktop shell controls

- allowlist filesystem paths to opened projects;
- narrow command bridge;
- no arbitrary shell execution from manuscript content;
- validate and sandbox compile adapters;
- treat HTML, links, images, and imported documents as untrusted input;
- store service credentials in OS secret storage, never project files.

## Threat cases

- malicious imported HTML or archive paths;
- prompt injection inside research sources;
- archive path traversal;
- symlink escape outside project root;
- plugins or scripts requesting broad write/network access;
- deleted prose retained unexpectedly in logs;
- public fixture accidentally containing private corpus.

## MVP gates

Path confinement, archive traversal protection, no secret persistence, AI context preview, privacy-aware archives, and log-retention controls.
