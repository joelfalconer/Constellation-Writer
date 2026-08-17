from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
VALIDATOR = REPO / "tools/validator/validate.py"


def run_validator(fixture: Path, report: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--repo", str(REPO), "--fixture", str(fixture), "--report", str(report)],
        text=True,
        capture_output=True,
        check=False,
    )


def test_reference_fixture_passes(tmp_path: Path) -> None:
    report = tmp_path / "valid.json"
    result = run_validator(REPO / "fixtures/reference-novel", report)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(report.read_text())["status"] in {"passed", "passed_with_warnings"}


def test_duplicate_sheet_id_fails(tmp_path: Path) -> None:
    fixture = tmp_path / "reference-novel"
    shutil.copytree(REPO / "fixtures/reference-novel", fixture)
    original = fixture / "sheets/sh_018f0000-0000-7000-8000-000000000001-opening-scene.md"
    duplicate = fixture / "sheets/duplicate-opening.md"
    duplicate.write_text(original.read_text(encoding="utf-8"), encoding="utf-8")
    report = tmp_path / "duplicate.json"
    result = run_validator(fixture, report)
    payload = json.loads(report.read_text())
    assert result.returncode != 0
    assert any(item["code"] == "DUPLICATE_SHEET_ID" for item in payload["issues"])


def test_missing_manifest_reference_fails(tmp_path: Path) -> None:
    fixture = tmp_path / "reference-novel"
    shutil.copytree(REPO / "fixtures/reference-novel", fixture)
    manifest = fixture / "manuscripts/main.manuscript.yml"
    text = manifest.read_text(encoding="utf-8").replace(
        "sh_018f0000-0000-7000-8000-000000000002",
        "sh_018f9999-9999-7000-8000-000000000999",
    )
    manifest.write_text(text, encoding="utf-8")
    report = tmp_path / "missing.json"
    result = run_validator(fixture, report)
    payload = json.loads(report.read_text())
    assert result.returncode != 0
    assert any(item["code"] == "MISSING_SHEET_REF" for item in payload["issues"])
