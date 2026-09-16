"""FROM-SCRATCH replay entry point.

  python3 output/lib/run.py output/lib/replay_run.py <export.store.json> [<out.replay.json>]

Loads ONLY the exported bytes in a fresh process, re-runs retained-closure admission,
recomputes the complete proof bundle and every output identity from the retained inputs,
and compares them to the retained claim. Exits non-zero on any refusal or mismatch.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_replay as R

path = sys.argv[1]
label = os.path.basename(path).split('.')[0]
res = R.replay(path, label)
outp = sys.argv[2] if len(sys.argv) > 2 else path.replace('.store.json', '.replay.json')
full = res.pop('closureFullReport')
with open(outp, 'w') as f:
    json.dump(res, f, indent=1)
with open(outp.replace('.replay.json', '.closure.json'), 'w') as f:
    json.dump(full, f, indent=1)

print('run          :', res['runId'])
print('closure      :', res['closure']['admitted'], 'passed', res['closure']['checksPassed'],
      'n/a', res['closure']['checksNotApplicable'],
      'refused', res['closure']['checksRefused'])
for r in res['closure']['refusals'][:10]:
    print('   CLOSURE REFUSE', r['check'], '|', json.dumps(r['detail'])[:200])
print('replay       :', res['verdict'])
if res.get('replayAttempted'):
    for c in res['bundleComparisons']:
        print('  %-20s equal=%s recomputed=%s retained=%s'
              % (c['object'], c['equal'], c['recomputedSha256'][:16],
                 c['retainedSha256'][:16]))
        for d in c.get('fieldDifferences', []):
            print('     DIFF field', d['field'])
            print('       recomputed', json.dumps(d['recomputed'])[:400])
            print('       retained  ', json.dumps(d['retained'])[:400])
    for c in res['identityComparisons']:
        print('  %-12s equal=%s %s' % (c['identity'], c['equal'], c['recomputed'][:28]))
    print('  findings recomputed', len(res['findingComparisons']),
          'all equal', all(r.get('equal') for r in res['findingComparisons']),
          'claimed-not-recomputed', res['claimedFindingsNotRecomputed'])
    print('  witnesses', len(res['witnessComparisons']),
          'all bytes equal', all(w['witnessBytesEqual'] for w in res['witnessComparisons']))
    print('  verdict recomputed/retained:', res['recomputedVerdict'],
          '/', res['retainedVerdict'])
sys.exit(0 if res.get('replayAdmitted') else 1)
