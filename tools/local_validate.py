#!/usr/bin/env python3
"""Local-first validation runner for Constellation Writer.

GitHub Actions is an optional replication surface, not the owner of project
validity. This runner executes deterministic repository checks without any
hosted CI dependency and emits a machine-readable receipt.

Default usage:
    python tools/local_validate.py --suite all

Optional Pandoc adapter exercise:
    python tools/local_validate.py --suite compile --pandoc /path/to/pandoc

The runner never installs dependencies and never requires network access.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
from typing import Sequence


RECEIPT_SCHEMA = "cw_local_validation_receipt_v1"


@dataclass
class CommandReceipt:
    id: str
    command: list[str]
    cwd: str
    returncode: int
    passed: bool
    stdout_sha256: str
    stderr_sha256: str
    stdout_tail: str
    stderr_tail: str


def digest_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()


def tail(value: str, limit: int = 8000) -> str:
    if len(value) <= limit:
        return value
    return "[...truncated...]\n" + value[-limit:]


def run_command(repo: Path, command_id: str, command: Sequence[str]) -> CommandReceipt:
    print(f"\n== {command_id} ==")
    print("$", " ".join(command))
    completed = subprocess.run(
        list(command),
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.stdout:
        print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
    if completed.stderr:
        print(completed.stderr, file=sys.stderr, end="" if completed.stderr.endswith("\n") else "\n")
    return CommandReceipt(
        id=command_id,
        command=list(command),
        cwd=str(repo),
        returncode=completed.returncode,
        passed=completed.returncode == 0,
        stdout_sha256=digest_text(completed.stdout),
        stderr_sha256=digest_text(completed.stderr),
        stdout_tail=tail(completed.stdout),
        stderr_tail=tail(completed.stderr),
    )


def ensure_python_dependencies() -> tuple[bool, list[str]]:
    missing: list[str] = []
    for module in ("yaml", "jsonschema", "referencing", "pytest"):
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    return not missing, missing


def compile_commands(repo: Path, pandoc: str | None) -> list[tuple[str, list[str]]]:
    python = sys.executable
    build_root = repo / "build" / "local-validation" / "compile"
    repeat_a = build_root / "repeat-a"
    repeat_b = build_root / "repeat-b"
    comparison = build_root / "direct-repeat-comparison.json"

    commands: list[tuple[str, list[str]]] = [
        (
            "compile_unit_tests",
            [python, "-m", "unittest", "discover", "-s", "spikes/compile-pipeline", "-p", "test_*.py", "-v"],
        ),
        (
            "compile_reference_repeat_a",
            [
                python,
                "spikes/compile-pipeline/compile_spike.py",
                "compile",
                "--project",
                "fixtures/reference-novel",
                "--manifest",
                "manuscripts/main.manuscript.yml",
                "--profile",
                "compile/profiles/draft-html.compile.yml",
                "--out",
                str(repeat_a.relative_to(repo)),
            ],
        ),
        (
            "compile_reference_repeat_b",
            [
                python,
                "spikes/compile-pipeline/compile_spike.py",
                "compile",
                "--project",
                "fixtures/reference-novel",
                "--manifest",
                "manuscripts/main.manuscript.yml",
                "--profile",
                "compile/profiles/draft-html.compile.yml",
                "--out",
                str(repeat_b.relative_to(repo)),
            ],
        ),
        (
            "compile_repeat_compare",
            [
                python,
                "spikes/compile-pipeline/compile_spike.py",
                "compare",
                "--left",
                str(repeat_a.relative_to(repo)),
                "--right",
                str(repeat_b.relative_to(repo)),
                "--out",
                str(comparison.relative_to(repo)),
                "--require-direct-equivalence",
            ],
        ),
    ]

    if pandoc:
        adapter_dir = build_root / "pandoc"
        commands.append(
            (
                "compile_optional_pandoc_adapter",
                [
                    python,
                    "spikes/compile-pipeline/compile_spike.py",
                    "compile",
                    "--project",
                    "fixtures/reference-novel",
                    "--manifest",
                    "manuscripts/main.manuscript.yml",
                    "--profile",
                    "compile/profiles/draft-html.compile.yml",
                    "--out",
                    str(adapter_dir.relative_to(repo)),
                    "--pandoc",
                    pandoc,
                ],
            )
        )

    return commands


def foundation_commands() -> list[tuple[str, list[str]]]:
    python = sys.executable
    return [
        ("foundation_schema_validation", [python, "tools/validator/validate.py", "--repo", "."]),
        ("foundation_contract_tests", [python, "-m", "pytest", "-q", "tests/contracts"]),
    ]


def write_receipt(path: Path, receipt: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic Constellation Writer validation locally")
    parser.add_argument("--repo", default=".", help="repository root")
    parser.add_argument(
        "--suite",
        choices=("all", "foundation", "compile"),
        default="all",
        help="validation suite to execute",
    )
    parser.add_argument("--pandoc", help="optional local Pandoc binary; no download is attempted")
    parser.add_argument(
        "--receipt",
        default="build/local-validation-receipt.json",
        help="receipt path relative to repository root",
    )
    parser.add_argument(
        "--continue-after-failure",
        action="store_true",
        help="run later commands after a failure instead of stopping early",
    )
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    receipt_path = repo / args.receipt
    dependency_ok, missing = ensure_python_dependencies()
    started = datetime.now(timezone.utc)

    commands: list[tuple[str, list[str]]] = []
    if args.suite in ("all", "foundation"):
        commands.extend(foundation_commands())
    if args.suite in ("all", "compile"):
        commands.extend(compile_commands(repo, args.pandoc))

    command_receipts: list[CommandReceipt] = []
    if dependency_ok:
        for command_id, command in commands:
            result = run_command(repo, command_id, command)
            command_receipts.append(result)
            if not result.passed and not args.continue_after_failure:
                break

    completed = datetime.now(timezone.utc)
    passed = dependency_ok and len(command_receipts) == len(commands) and all(item.passed for item in command_receipts)

    receipt = {
        "schema": RECEIPT_SCHEMA,
        "validation_runtime": "local_process",
        "hosted_ci_required": False,
        "suite": args.suite,
        "started_at": started.isoformat(),
        "completed_at": completed.isoformat(),
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "executable": sys.executable,
            "repo": str(repo),
            "pandoc_requested": args.pandoc,
        },
        "dependencies": {
            "available": dependency_ok,
            "missing_imports": missing,
            "install_hint": "python -m pip install -r tools/validator/requirements.txt" if missing else None,
        },
        "commands": [asdict(item) for item in command_receipts],
        "acceptance_state": "passed" if passed else "failed",
        "notes": [
            "GitHub Actions availability is not part of this acceptance result.",
            "Physical IME, accessibility, native interaction, and professional-writer assays remain separate evidence classes.",
            "Pandoc adapter execution is optional unless explicitly supplied with --pandoc.",
        ],
    }
    write_receipt(receipt_path, receipt)
    print(f"\nValidation receipt: {receipt_path}")
    print(f"Acceptance: {receipt['acceptance_state']}")

    if not dependency_ok:
        print(
            "Missing Python dependencies: " + ", ".join(missing) +
            "\nInstall from tools/validator/requirements.txt, then rerun.",
            file=sys.stderr,
        )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
