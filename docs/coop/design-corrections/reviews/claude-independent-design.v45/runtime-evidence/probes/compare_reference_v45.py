"""Compare this review's own six pinned groups and 17 evaluator3 children with the header-named current source45 reference
(codex-post-reset final-reference.v45; actual root execution root-source45-final-reference.v1), with the key-level difference of
every non-byte-equal child, and with this reviewer's own historical source44 receipts (read-only; never relabelled). Evidence
comparison only; this review's own execution on the verified source45 archive copy is the acceptance input.
Writes only receipts/reference-comparison.json."""
import glob, hashlib, json, os
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v45')
MINE = RT / 'receipts/reference'
CODEX = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v45')
ROOT = Path('/tmp/opensip-design-corrections/root-source45-final-reference.v1')
MINE44 = Path('/tmp/opensip-design-corrections/claude-independent-design.v44/receipts/reference')
PATHY = {'ownedHashes', 'receiptPath', 'hashes', 'report', 'receipt', 'v8ReceiptMisplaced', 'v10ReceiptPreserved'}


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest() if os.path.exists(p) else None


def strip(x):
    if isinstance(x, dict):
        return {k: strip(v) for k, v in x.items() if k not in PATHY}
    if isinstance(x, list):
        return [strip(v) for v in x]
    return x


def diff_paths(a, b, at=''):
    if type(a) is not type(b):
        return [at or '/']
    if isinstance(a, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            out += [at + '/' + k] if (k not in a or k not in b) else diff_paths(a[k], b[k], at + '/' + k)
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return [at + '[len %d!=%d]' % (len(a), len(b))]
        return [p for i, (x, y) in enumerate(zip(a, b)) for p in diff_paths(x, y, at + '[%d]' % i)]
    return [] if a == b else [at]


out = {'codexReferenceChecks': {'path': str(CODEX / 'reference-checks.json'), 'sha256': sha(CODEX / 'reference-checks.json'),
                                'expected': '5dc0de6011ea8ff58d614f8e0f8c35420e197aabbbee64c9c6b9fb1df0a34bc4'},
       'codexFiles': sorted(os.listdir(CODEX)), 'rootReferenceChecks': {'path': str(ROOT / 'reference-checks.json'), 'sha256': sha(ROOT / 'reference-checks.json')}}
codex = json.load(open(CODEX / 'reference-checks.json'))
root = json.load(open(ROOT / 'reference-checks.json'))
out['codexPassed'], out['codexSubjectManifestSha256'] = codex.get('passed'), codex.get('subjectManifestSha256')
out['rootPassed'], out['rootSubjectManifestSha256'] = root.get('passed'), root.get('subjectManifestSha256')
out['codexRunnerOriginalEqualsRoot'] = sha(CODEX / 'runner-original-reference-checks.json') == sha(ROOT / 'reference-checks.json') if (CODEX / 'runner-original-reference-checks.json').exists() else None
out['codexMinusRootTopLevelKeys'] = sorted(k for k in set(codex) | set(root) if codex.get(k) != root.get(k))
out['rootExecutionSourceRoots'] = sorted({c['command'][3].split('/docs/')[0] for c in root.get('commands', []) if len(c.get('command', [])) > 3})
out['rootCommandSourceShas'] = {c.get('name'): c.get('sourceSha256') for c in root.get('commands', [])}
cmds = root.get('commands', [])
mine = json.load(open(MINE / 'groups-report.all.json'))
mine44 = json.load(open(MINE44 / 'groups-report.all.json'))
out['mineCopyBefore'], out['mineCopyAfter'], out['minePassed'] = mine.get('before'), mine.get('after'), mine.get('passed')
groups = {}
for r in mine['rows']:
    name = r['name']
    c = next((x for x in cmds if x.get('name') == name), None)
    m44 = next((x for x in mine44['rows'] if x['name'] == name), None)
    groups[name] = {'mineExit': r['exitCode'], 'rootExit': (c or {}).get('exitCode'), 'rootSourceShaEqualsMineScript': (c or {}).get('sourceSha256') == r['scriptSha256'],
                    'stdoutShaEqualRootRecord': (c or {}).get('stdoutSha256') == r['stdoutSha256'],
                    'stdoutFileEqualRoot': sha(ROOT / (name + '.stdout')) == sha(MINE / (name + '.stdout')),
                    'stdoutFileEqualCodex': (sha(CODEX / (name + '.stdout')) == sha(MINE / (name + '.stdout'))) if (CODEX / (name + '.stdout')).exists() else None,
                    'historicalMine44Exit': (m44 or {}).get('exitCode'), 'stdoutEqualHistoricalMine44': (m44 or {}).get('stdoutSha256') == r['stdoutSha256'],
                    'scriptChangedVs44': (m44 or {}).get('scriptSha256') != r['scriptSha256'],
                    'stdoutMine': (MINE / (name + '.stdout')).read_text()[-300:], 'stdoutHistoricalMine44': (MINE44 / (name + '.stdout')).read_text()[-300:] if (MINE44 / (name + '.stdout')).exists() else None}
out['groups'] = groups
children = {}
for f in sorted(glob.glob(str(MINE / 'evaluator3' / '*.stdout'))):
    n = os.path.basename(f)
    rec = {'mine': sha(f), 'root': sha(ROOT / 'evaluator3' / n), 'codex': sha(CODEX / 'evaluator3' / n), 'historicalMine44': sha(MINE44 / 'evaluator3' / n)}
    rec['equalRoot'] = rec['mine'] == rec['root']
    rec['equalCodex'] = rec['mine'] == rec['codex']
    rec['equalHistoricalMine44'] = rec['mine'] == rec['historicalMine44']
    try:
        m = json.load(open(f))
        for label, base in (('root', ROOT / 'evaluator3' / n), ('historicalMine44', MINE44 / 'evaluator3' / n)):
            if not rec['equal' + label[0].upper() + label[1:]] and base.exists():
                o = json.load(open(base))
                rec[label + 'Diff'] = {'rawPaths': diff_paths(m, o)[:40], 'equalAfterStrippingPathFieldsOnly': strip(m) == strip(o),
                                       'strippedPaths': diff_paths(strip(m), strip(o))[:40]}
        for k in ('cases', 'checks'):
            if isinstance(m.get(k), list):
                rec[k + 'Count'] = len(m[k])
        if isinstance(m.get('checks'), list):
            rec['failedChecks'] = [c.get('id') or c.get('name') or json.dumps(c, sort_keys=True)[:120] for c in m['checks']
                                   if isinstance(c, dict) and c.get('ok', c.get('passed', True)) is not True]
        if isinstance(m.get('mismatches'), list):
            rec['mismatches'] = len(m['mismatches'])
    except ValueError:
        rec['nonJson'] = True
    children[n] = rec
out['children'] = children
out['childCount'] = len(children)
out['childrenEqualRoot'] = sum(1 for v in children.values() if v['equalRoot'])
out['childrenNotEqualRoot'] = sorted(k for k, v in children.items() if not v['equalRoot'])
out['childrenDifferingFromHistoricalMine44'] = sorted(k for k, v in children.items() if not v['equalHistoricalMine44'])
for label, path in (('mine', MINE / 'evaluator3/report.json'), ('root', ROOT / 'evaluator3/report.json')):
    rep = json.load(open(path))
    out['evaluator3Report_' + label] = {k: (v if not isinstance(v, (list, dict)) else type(v).__name__ + str(len(v))) for k, v in rep.items()}
out['nativeStdoutTail'] = {'mine': (MINE / 'native.stdout').read_text()[-400:], 'root': (ROOT / 'native.stdout').read_text()[-400:]}
(RT / 'receipts/reference-comparison.json').write_text(json.dumps(out, indent=1))
print(json.dumps({k: v for k, v in out.items() if k not in ('children',)}, indent=1)[:12000])
print(json.dumps({k: (v['equalRoot'], v['equalHistoricalMine44'], v.get('rootDiff', {}).get('equalAfterStrippingPathFieldsOnly'), v.get('historicalMine44Diff', {}).get('strippedPaths')) for k, v in children.items()}))
