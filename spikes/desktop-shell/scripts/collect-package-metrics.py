#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--shell', required=True)
parser.add_argument('--platform', required=True)
parser.add_argument('--root', required=True)
parser.add_argument('--output', required=True)
args = parser.parse_args()

root = Path(args.root)
files = [p for p in root.rglob('*') if p.is_file()] if root.is_dir() else [root]
size = sum(p.stat().st_size for p in files if p.exists())
report = {
    'shell': args.shell,
    'platform': args.platform,
    'package_root': str(root),
    'package_exists': root.exists(),
    'package_file_count': len(files),
    'package_bytes': size,
    'package_mib': round(size / 1024 / 1024, 3),
    'measurement_note': 'Tauri bundles do not include the OS WebView runtime; Electron packages include Chromium/Node. Size is recorded but is not a standalone decision criterion.'
}
Path(args.output).parent.mkdir(parents=True, exist_ok=True)
Path(args.output).write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
