# Foundation Validator

The validator owns deterministic checks for the candidate contract and fixture package.

## Run

```bash
python -m pip install -r tools/validator/requirements.txt
python tools/validator/validate.py --repo .
```

The command validates JSON Schemas, reference fixture instances, Sheet frontmatter, identifier declarations, and manuscript Sheet references. It writes `build/validation-report.json`.

## Boundaries

- Passing means the checked artifacts are mechanically consistent with current candidate schemas.
- Passing does not promote the architecture to accepted status.
- Product behavior, atomicity, recovery, compile determinism, and usability require executable tests beyond this validator.
