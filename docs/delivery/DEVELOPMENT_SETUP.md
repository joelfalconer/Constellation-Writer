# Development Setup v0.1

## Foundation validation only

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r tools/validator/requirements.txt
python tools/validator/validate.py --repo .
pytest -q tests/contracts
```

## Planned application toolchain

Candidate stack pending ADR spikes:

- Node.js active LTS and pnpm;
- TypeScript frontend;
- Tauri 2 and stable Rust;
- CodeMirror 6;
- SQLite through Rust-owned package;
- Pandoc as a pinned optional output adapter.

Do not install or commit a full application scaffold until the shell/editor spike records its decision.

## Repository checks

Before PR:

1. run foundation validator;
2. run contract tests;
3. inspect generated validation report;
4. update affected ADR/spec/status records;
5. include rollback notes for contract changes;
6. avoid committing `.workbench/`, build artifacts, private corpora, credentials, or font binaries.

## Environment principles

- Repeatable commands over workstation folklore.
- Pinned adapter versions where output may change.
- Cross-platform path and line-ending tests.
- No network requirement for validator or core writing tests after dependencies are installed.
