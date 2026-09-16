"""Parsed-structure comparison of native/native-cases.v2.json between the verified source44 and source45 copies, to separate a
whitespace reindent from semantic change: top-level keys, fixture keys added/removed/changed, cases added/removed/changed by id
(order preserved), and whether the source45 text equals a canonical re-serialisation of its own parse at some indent.
Writes only receipts/probes/cases-structure45.json."""
import hashlib, json
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v45')
P = 'docs/coop/design-corrections/native/native-cases.v2.json'
raw44, raw45 = (RT / 'work/base44' / P).read_bytes(), (RT / 'work/source45-pkg' / P).read_bytes()
a, b = json.loads(raw44), json.loads(raw45)
out = {'sha44': hashlib.sha256(raw44).hexdigest(), 'sha45': hashlib.sha256(raw45).hexdigest(), 'bytes44': len(raw44), 'bytes45': len(raw45),
       'topKeys44': list(a), 'topKeys45': list(b), 'topLevelNonCaseFixtureKeysEqual': {k: a.get(k) == b.get(k) for k in set(a) | set(b) if k not in ('cases', 'fixtures')}}
fa, fb = a.get('fixtures', {}), b.get('fixtures', {})
out['fixtures'] = {'count44': len(fa), 'count45': len(fb), 'added': sorted(set(fb) - set(fa)), 'removed': sorted(set(fa) - set(fb)),
                   'changed': sorted(k for k in set(fa) & set(fb) if fa[k] != fb[k]), 'orderEqual': [k for k in fa] == [k for k in fb if k in fa]}
ca, cb = {c['id']: c for c in a['cases']}, {c['id']: c for c in b['cases']}
ids_a, ids_b = [c['id'] for c in a['cases']], [c['id'] for c in b['cases']]
out['cases'] = {'count44': len(ids_a), 'count45': len(ids_b), 'uniqueIds45': len(set(ids_b)) == len(ids_b), 'added': [i for i in ids_b if i not in ca],
                'removed': [i for i in ids_a if i not in cb], 'changed': [i for i in ids_b if i in ca and ca[i] != cb[i]],
                'retainedOrderEqual': [i for i in ids_a if i in cb] == [i for i in ids_b if i in ca],
                'addedCases': {i: cb[i] for i in ids_b if i not in ca}}
for ind in (None, 1, 2, 4):
    txt = json.dumps(b, indent=ind, ensure_ascii=False) + ('\n' if ind is not None else '')
    out.setdefault('reserialisationEqualsSource45', {})[str(ind)] = txt.encode('utf-8') == raw45
    txt44 = json.dumps(a, indent=ind, ensure_ascii=False) + ('\n' if ind is not None else '')
    out.setdefault('reserialisationEqualsSource44', {})[str(ind)] = txt44.encode('utf-8') == raw44
out['semanticDeltaIsOnlyAddedCases'] = (not out['fixtures']['added'] and not out['fixtures']['removed'] and not out['fixtures']['changed'] and not out['cases']['removed']
                                        and not out['cases']['changed'] and out['cases']['retainedOrderEqual'] and all(out['topLevelNonCaseFixtureKeysEqual'].values()))
(RT / 'receipts/probes').mkdir(parents=True, exist_ok=True)
(RT / 'receipts/probes/cases-structure45.json').write_text(json.dumps(out, indent=1))
print(json.dumps({k: v for k, v in out.items() if k != 'cases'} | {'cases': {k: v for k, v in out['cases'].items() if k != 'addedCases'}}, indent=1))
print(json.dumps(out['cases']['addedCases'], indent=1)[:12000])
