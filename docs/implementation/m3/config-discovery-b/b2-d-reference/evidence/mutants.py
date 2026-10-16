"""B2-d0 negative controls: each mutant weakens one of the reference's changes; the checker must fail on every one.
Mutated copies and their outputs live in a private temporary directory; nothing here is kept.

  python3 -I -B mutants.py <architecture checkout> <python-packages snapshot>
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REF = HERE.parent / 'reference' / 'framework_recognition_reference.py'
MUTANTS = [
    # Change 1 undone at both sites: the model's regex results kept, and no parsed results added.
    ('cargo-regex-kept', [("        recognized = [r for r in result['recognized'] if r['recognizerId'] not in ('cargo-workspace', 'cargo-package')]\n",
                           "        recognized = list(result['recognized'])\n"),
                          ("        if 'Cargo.toml' in files:\n            doc = self.parse_cargo(files['Cargo.toml'])\n",
                           "        if False:\n            doc = self.parse_cargo(files['Cargo.toml'])\n")]),
    ('jsonc-unchecked', "            if r['recognizerId'] == 'typescript-config' and not self.jsonc_ok(files[r['evidence'][0]['path']]):\n",
     "            if r['recognizerId'] == 'typescript-config' and False:\n"),
    ('yaml-unchecked', "            if r['recognizerId'] == 'pnpm-workspace':\n", "            if False:\n"),
    ('entry-bound-per-result', "    union = {p for r in recognized for p in r['effects']['entryPoints']}\n    if len(union) > MAX_ENTRY_POINTS:\n",
     "    union = max((r['effects']['entryPoints'] for r in recognized), key=len, default=[])\n    if len(union) > MAX_ENTRY_POINTS:\n"),
    ('entry-bound-skipped-under-explicit', "        entry_bound(recognized)\n", "        if explicit_entry_points is None:\n            entry_bound(recognized)\n"),
    ('state-rule-reverted', "        elif any(r['unresolvedChoices'] for r in recognized):\n", "        elif any(r['unresolvedChoices'] for r in recognized) and any(r['effects']['entryPoints'] for r in recognized):\n"),
    ('explicit-empty-as-absent', "        if explicit_entry_points is not None:\n", "        if explicit_entry_points:\n"),
    ('yaml-plain-colon', "    if not value or value[0] in _INDICATORS or ':' in value or value.lower() in _RESERVED:\n",
     "    if not value or value[0] in _INDICATORS or ': ' in value or value.lower() in _RESERVED:\n"),
    ('yaml-dash-separation', "        m = re.fullmatch(r'( +)- +(.*)', line)\n", "        m = re.fullmatch(r'( +)- *(.*)', line)\n"),
    ('toml-node-limit-off-by-one', "            if remaining < 0:\n", "            if remaining < -1:\n"),
    ('toml-byte-cap-dropped', "        if len(raw) > TOML_MAX_BYTES:\n            return None\n", ""),
    ('yaml-null-packages-accepted', "    if state == 'block' and not out:\n", "    if False:\n"),
    ('yaml-characters-unchecked', "    if not all(_yaml_character_ok(ch) for ch in '\\n'.join(lines)):\n", "    if False:\n"),
    ('toml-python-digit-limit-kept', "        sys.set_int_max_str_digits(0)\n", ""),
    ('yaml-empty-flow-unseparated', "            if re.fullmatch(r'packages: +\\[\\] *( +#.*)?', line):\n", "            if re.fullmatch(r'packages: *\\[\\] *( +#.*)?', line):\n"),
    ('yaml-eof-cr-stripped', "    text = text.replace('\\r\\n', '\\n')\n", "    text = text.replace('\\r\\n', '\\n').rstrip('\\r')\n"),
    ('evidence-bound-dropped', "        if not 1 <= len(r['evidence']) <= MAX_EVIDENCE:\n", "        if False:\n"),
]


def main():
    arch, packages = sys.argv[1], sys.argv[2]
    source = REF.read_text()
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        for row in MUTANTS:
            name, edits = row[0], (row[1] if len(row) == 2 else [(row[1], row[2])])
            text = source
            for before, after in edits:
                assert text.count(before) == 1, name
                text = text.replace(before, after)
            mutant = Path(tmp) / ('m-' + name + '.py')
            mutant.write_text(text)
            out = Path(tmp) / ('m-' + name + '.json')
            r = subprocess.run([sys.executable, '-I', '-B', str(HERE / 'check.py'), arch, packages, str(mutant), str(out)], capture_output=True, text=True)
            failed = json.loads(out.read_text())['failed'] if out.is_file() else ['<checker raised>']
            rows.append(dict(name=name, caught=r.returncode != 0, failedChecks=failed[:6], exitCode=r.returncode))
            print(name, 'caught' if r.returncode != 0 else 'SURVIVED', failed[:3])
    (HERE / 'mutants.json').write_text(json.dumps(dict(schemaVersion=1, rows=rows, allCaught=all(r['caught'] for r in rows)), indent=1) + '\n')
    return 0 if all(r['caught'] for r in rows) else 1


if __name__ == '__main__':
    sys.exit(main())
