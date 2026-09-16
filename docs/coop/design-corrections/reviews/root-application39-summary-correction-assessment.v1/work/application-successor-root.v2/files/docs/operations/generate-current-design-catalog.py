"""Generate the current-design navigation page from the current classification inventory.
This is documentation accounting, not architecture acceptance or historical source authentication.
"""
import argparse
import json
import posixpath
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def render(classification):
    rows = sorted((row for row in classification['files'] if row['classification'] == 'current/architecture'), key=lambda row: row['path'])
    lines = ['# Current design', '',
             'Generated from [`document-classification.v1.json`](../operations/document-classification.v1.json) by `docs/operations/generate-current-design-catalog.py`. Custody paths are unchanged. The [D-372 application](../coop/design-corrections/application.v1.json) identifies the current owning contracts and the retained scope of older chapters.', '']
    for row in rows:
        tag = 'LINK RECORDED' if row.get('referencedByCount', 0) or row.get('currentNavigationReferences') else 'NO LINK RECORDED'
        link = posixpath.relpath(row['path'], 'docs/catalog')
        lines.append(f"- `{tag}` [{row['path']}]({link})")
    return '\n'.join(lines) + '\n'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--classification', type=Path, default=ROOT / 'docs/operations/document-classification.v1.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'docs/catalog/current-design.md')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = render(json.loads(args.classification.read_text()))
    if args.check:
        matches = args.output.exists() and args.output.read_text() == result
        print('PASS current-design catalog' if matches else 'FAIL current-design catalog differs from classification')
        raise SystemExit(not matches)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result)
    print(args.output)
