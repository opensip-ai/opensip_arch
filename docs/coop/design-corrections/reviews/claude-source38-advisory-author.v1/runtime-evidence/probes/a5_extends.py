"""A5 focused `extends` cases: official TypeScript 5.6.3 (root's retained bytes, custody re-verified) versus the root A5
prose law transcribed literally. Only new cases; the 32 direct-option observations are not repeated.

Root prose (A5 native-evidence.md): "an explicit allowJs value wins, including false. A jsconfig entry defaults it to
true; otherwise omitted allowJs derives from effective checkJs, whose omitted default is false. Apply configuration
inheritance before these defaults."  Transcription: merge base then own compilerOptions (own wins); then
allowJs = merged.allowJs if present, else (True if entry is jsconfig else merged.checkJs or False).
Output: receipts/a5-extends.json.
"""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v1')
A5 = Path('/tmp/opensip-design-corrections/root-consumer24-js-options.v1')
cust = json.loads((A5 / 'compiler-custody.json').read_text())
custody = {f['path']: hashlib.sha256((A5 / f['path']).read_bytes()).hexdigest() == f['sha256'] for f in cust['files']}
node = shutil.which('node')
out = {'standing': 'focused compiler observation of new extends cases; supporting evidence only', 'compilerCustody': custody, 'node': node}
if not all(custody.values()) or node is None:
    (BASE / 'receipts' / 'a5-extends.json').write_text(json.dumps(out, indent=1) + '\n')
    print(json.dumps(out, indent=1))
    sys.exit(2)
out['nodeVersion'] = subprocess.run([node, '--version'], capture_output=True, text=True).stdout.strip()
p = subprocess.run([node, str(BASE / 'probes' / 'a5_extends.cjs')], capture_output=True, text=True, timeout=600)
out['nodeExit'] = p.returncode
if p.returncode:
    out['stderr'] = p.stderr[-3000:]
    (BASE / 'receipts' / 'a5-extends.json').write_text(json.dumps(out, indent=1) + '\n')
    print(json.dumps(out, indent=1))
    sys.exit(1)
obs = json.loads(p.stdout)
out['compilerVersion'] = obs['compilerVersion']


def prose(entry, own, base):
    merged = dict(base, **own)
    check = bool(merged.get('checkJs', False))
    if 'allowJs' in merged:
        return bool(merged['allowJs']), check
    return (True if entry == 'jsconfig.json' else check), check


rows = []
for r in obs['rows']:
    pa, pc = prose(r['entry'], r['own'], r['base']['options'])
    rows.append(dict(r, proseAllowJs=pa, proseCheckJs=pc,
                     proseJsAdmitted=pa and bool(r['jsRootFiles']) if pa == r['effectiveAllowJs'] else pa and r['jsFilePresent'],
                     compilerJsAdmitted=r['effectiveAllowJs'] and bool(r['jsRootFiles']),
                     agrees=(pa, pc) == (r['effectiveAllowJs'], r['checkJs'])))
out['rows'] = rows
out['disagreements'] = sorted({r['id'] for r in rows if not r['agrees']})
(BASE / 'receipts' / 'a5-extends.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps({'compilerVersion': out['compilerVersion'], 'node': out['nodeVersion'], 'cases': len(rows),
                  'table': [(r['id'], r['jsFilePresent'], 'tsc', r['effectiveAllowJs'], r['checkJs'], r['jsRootFiles'], r['optionDiagnostics'],
                             'prose', r['proseAllowJs'], r['proseCheckJs']) for r in rows],
                  'disagreements': out['disagreements']}, indent=1))
