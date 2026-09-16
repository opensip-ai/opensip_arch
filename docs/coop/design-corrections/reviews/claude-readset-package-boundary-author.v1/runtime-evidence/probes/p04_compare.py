"""p04: expectations over p02 (helper matrices, edited vs baseline model) and p03 (checkers, discrimination).
Output: receipts/p04-compare.json.
"""
import json, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-readset-package-boundary-author.v1')
R = BASE / 'receipts'
edited = {r['path']: r for r in json.loads((R / 'p02-edited.json').read_text())['rows']}
baseline = {r['path']: r for r in json.loads((R / 'p02-baseline.json').read_text())['rows']}
ed_meta = json.loads((R / 'p02-edited.json').read_text())
bl_meta = json.loads((R / 'p02-baseline.json').read_text())
checks = {}


def ck(name, ok, detail=None):
    checks[name] = {'ok': bool(ok), **({'detail': detail} if detail is not None else {})}


def kinds(rows, key, value):
    return sorted(p for p, r in rows.items() if r[key] == value)


LAWFUL = {'ordinary', 'ordinary-store', 'first-party', 'lookalike'}
ck('models loaded from the intended trees',
   ed_meta['loadedModelFile'].startswith(str((BASE / 'work/source').resolve())) and
   bl_meta['loadedModelFile'].startswith(str((BASE / 'work/hybrid-baseline-model').resolve())) and ed_meta['modelSha256'] != bl_meta['modelSha256'],
   [ed_meta['loadedModelFile'], bl_meta['loadedModelFile']])
ck('edited, base layout: ordinary, store, first-party and lookalike rows lawful; every other kind refuses',
   all((not r['fault:base']) == (r['kind'] in LAWFUL) for r in edited.values()),
   {p: (r['kind'], r['fault:base']) for p, r in edited.items() if (not r['fault:base']) != (r['kind'] in LAWFUL)})
ck('edited, nested rows listed: separately listed nested packages lawful; deeper, sibling, unlisted store sibling, boundary file, VCS still refuse',
   all((not r['fault:base+nested']) == (r['kind'] in LAWFUL | {'nested'}) for r in edited.values()),
   {p: (r['kind'], r['fault:base+nested']) for p, r in edited.items() if (not r['fault:base+nested']) != (r['kind'] in LAWFUL | {'nested'})})
ck('edited, no read set: only first-party and first-party-realpath rows lawful',
   all((not r['fault:none']) == (r['kind'] == 'first-party' or (r['kind'] == 'lookalike' and False)) for r in edited.values()),
   {p: (r['kind'], r['fault:none']) for p, r in edited.items() if (not r['fault:none']) != (r['kind'] == 'first-party')})
for layout, expected_kinds in (('base', {'nested', 'nested-deeper', 'nested-unlisted-sibling', 'nested-boundary-as-file'}),
                               ('base+nested', {'nested-deeper', 'nested-unlisted-sibling', 'nested-boundary-as-file'}),
                               ('none', set())):
    key = 'fault:' + layout
    newly = sorted(p for p in edited if edited[p][key] and not baseline[p][key])
    relaxed = sorted(p for p in edited if baseline[p][key] and not edited[p][key])
    expected = sorted(p for p in edited if edited[p]['kind'] in expected_kinds)
    ck('baseline -> edited with layout %s: newly refused are exactly the nested-boundary crossings, nothing relaxed' % layout,
       newly == expected and relaxed == [], {'newly': newly, 'expected': expected, 'relaxed': relaxed})
ck('discovery instrument identical under both models and still the outermost anchor',
   all(edited[p]['discovery'] == baseline[p]['discovery'] for p in edited)
   and edited['node_modules/left-pad/node_modules/evil/index.js']['discovery'] == ['node_modules', 'dependency-tree'])
for name in ('edited-a4', 'edited-all', 'semantic-edited', 'baseline-model-a4', 'substring-mutant-a4'):
    p = R / ('p03-%s.json' % name)
    d = json.loads(p.read_text()) if p.exists() else None
    ck('p03 %s expectation' % name, d is not None and d['expectationMet'],
       None if d is None else {k: d.get(k) for k in ('exit', 'total', 'passed', 'failedCases', 'count', 'blocked', 'faults')})
out = {'checks': checks, 'allOk': all(c['ok'] for c in checks.values())}
(R / 'p04-compare.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps(out, indent=1)[:15000])
sys.exit(0 if out['allOk'] else 1)
