"""V08 — RRS-A2: check each requested wording point against the captured in-progress bytes.

These are captured in-progress author bytes, not a final handoff. I check whether each of root's
five wording requests is (a) already satisfied, (b) contradicted, or (c) simply absent.
"""
import json, os, re

RR = '/tmp/opensip-design-corrections/root-repair-selection-author-review.v1/captured'
OUT = '/tmp/opensip-design-corrections/claude-glob-repair-bounded-review.v1/receipts'
MODP = os.path.join(RR, 'docs/coop/design-corrections/workflows/repair_closed_world_selection.v1.py')
WFS = os.path.join(RR, 'docs/v2/contracts/product-v1/workflows-and-surfaces.md')
mod = open(MODP, encoding='utf-8').read()
wfs = open(WFS, encoding='utf-8').read()
R = {}


def show(label, text, pattern, ctx=1):
    hits = []
    lines = text.splitlines()
    for i, l in enumerate(lines, 1):
        if re.search(pattern, l, re.I):
            hits.append({'line': i, 'text': l.strip()[:300]})
    print('\n--- %s (%d hits) ---' % (label, len(hits)))
    for h in hits[:ctx * 12]:
        print('%5d  %s' % (h['line'], h['text'][:230]))
    return hits


# A2-1 / A2-2: the EMPTY sentinel and the authoritative-boolean comment
R['moduleEMPTY'] = show('module EMPTY sentinel', mod, r'\bEMPTY\b')
R['authoritativeInModule'] = show('module: "authoritative"', mod, r'authoritativ')
R['entryPoints'] = show('entryPointsRecognized / nonliteralLoading', mod + '\n' + wfs,
                        r'entryPointsRecognized|nonliteralLoading')

# A2-3: summary vs eligibility when a relevant universe has no Coverage
R['noCoverage'] = show('relevant universe with no Coverage', mod + '\n' + wfs,
                       r'no Coverage|without Coverage|missing[- ]coverage|absent Coverage')

# A2-4: partition key ordering
R['ordering'] = show('partition key / ordering', mod, r'partition|sort|order|key')
KEY_MEMBERS = ['relation', 'resolution', 'sourceUniverse', 'targetUniverse',
               'subjectScopeCommitment', 'coverage']
R['keyMembersNamedInModule'] = {k: mod.count(k) for k in KEY_MEMBERS}
R['utf8OrderingNamedInProse'] = bool(re.search(r'UTF-8 byte|utf-8 byte|byte order', wfs, re.I))
R['utf8OrderingNamedInModule'] = bool(re.search(r'UTF-8|utf8|\.encode\(\)', mod))
print('\nkey members named in module :', R['keyMembersNamedInModule'])
print('UTF-8 byte ordering named in the contract prose :', R['utf8OrderingNamedInProse'])
print('UTF-8 / encode() present in the module          :', R['utf8OrderingNamedInModule'])

# does the module actually build a partition key, and in what order?
mk = re.findall(r'def (\w*partition\w*|\w*key\w*)\s*\(', mod)
R['keyBuildingFunctions'] = mk
for m in re.finditer(r'\n(\s*)(?:key|partition)\w*\s*=\s*\(([^)]{0,300})\)', mod):
    print('   key tuple:', m.group(2).replace('\n', ' ')[:220])
    R.setdefault('keyTuples', []).append(m.group(2).replace('\n', ' ')[:300])

# A2-5: dissent remedy wording
R['remedy'] = show('remedy text', mod, r'"remedy"|remedy')
rem = re.findall(r'"remedy":\s*\(?\s*"([^"]{0,400})"', mod)
R['remedyStrings'] = rem
print('\n--- remedy strings (%d) ---' % len(rem))
for s in rem:
    print('   ', s[:240])
R['remedyNamesCoverageIdentity'] = any('coverage' in s.lower() and
                                       ('identity' in s.lower() or 'coverage2:' in s.lower())
                                       for s in rem)
R['remedyNamesRelationRungUniverse'] = any(
    ('relation' in s.lower() or 'rung' in s.lower() or 'universe' in s.lower()) for s in rem)
print('\nremedy names coverage identity / full key :', R['remedyNamesCoverageIdentity'])
print('remedy names relation/rung/sourceUniverse :', R['remedyNamesRelationRungUniverse'])

R['ASSESSMENT'] = {
    'A2_sentinelDescribedAsFiveFieldLeastClosed': None,
    'A2_moduleCallsDisplayBooleanAuthoritative': None,
    'A2_summaryVsEligibilityExplained': None,
    'A2_utf8AndKeySequencePublished': R['utf8OrderingNamedInProse'],
    'A2_remedyNamesActualRetainedRecord': R['remedyNamesCoverageIdentity']}
json.dump(R, open(os.path.join(OUT, 'v08-rrsa2.json'), 'w'), indent=1, default=str)
print('\nwrote v08-rrsa2.json')
