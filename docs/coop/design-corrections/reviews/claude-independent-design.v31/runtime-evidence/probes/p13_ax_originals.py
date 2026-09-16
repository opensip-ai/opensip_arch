"""PROBE 13 (v31) — A-5: the two cited historical artifacts are now frozen31 members.

My v27 advisory A-5 was that AX6/AX9/MD5/RX2c kept neither an inline original nor a title and their
cited source artifacts had ZERO occurrences in the subject. I re-measure that, then extract the
actual original statements for the four variants so each residual account can be assessed against
its own original rather than only against admission-and-qualification.md.
"""
import hashlib, json, os, re

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
ART = os.path.join(SRC, 'docs/coop/artifacts')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v31/receipts'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v31.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
R = {}

for rel in ('docs/coop/artifacts/evaluation-proof.v13.json',
            'docs/coop/artifacts/ep13.review-independent.json'):
    p = os.path.join(SRC, rel)
    present = rel in man and os.path.isfile(p)
    sha = hashlib.sha256(open(p, 'rb').read()).hexdigest() if present else None
    R[rel] = {'inFrozen31': present, 'sha256': sha,
              'shaMatchesManifest': present and sha == man[rel]['sha256'],
              'bytes': os.path.getsize(p) if present else None}
    print('%-52s inFrozen31=%s bytes=%s' % (os.path.basename(rel), present, R[rel]['bytes']))

# the proposal's `source` fields now resolve?
prop = json.load(open(os.path.join(SRC, 'docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json')))
srcs = sorted(set(i.get('source') for i in prop['items'] if i.get('source')))
R['proposedSourceFieldsResolve'] = {s: (s in man) for s in srcs}
print('\nproposal `source` fields resolve in frozen31:')
for s, ok in R['proposedSourceFieldsResolve'].items():
    print('   %-58s %s' % (s, ok))
R['allProposedSourcesResolve'] = all(R['proposedSourceFieldsResolve'].values())

# ---- extract the original statements for the four variants ----
ep = json.load(open(os.path.join(ART, 'evaluation-proof.v13.json')))
flat = json.dumps(ep)
R['evaluationProofTopKeys'] = sorted(ep) if isinstance(ep, dict) else '<list>'
print('\nevaluation-proof.v13.json top keys:', R['evaluationProofTopKeys'][:20])

VAR = ['AX6', 'AX9', 'MD5', 'RX2c']
found = {}


def walk(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, path + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + '/%d' % i)
    elif isinstance(o, str):
        for v in VAR:
            if re.search(r'\b' + v + r'\b', o) or o.startswith(v + '-'):
                found.setdefault(v, []).append({'path': path, 'text': o})


walk(ep)
for v in VAR:
    rows = found.get(v, [])
    R.setdefault('variantStatements', {})[v] = {
        'occurrences': len(rows),
        'samples': [{'path': r['path'], 'text': r['text'][:900]} for r in rows[:3]]}
    print('\n===== %s : %d string occurrences in evaluation-proof.v13.json =====' % (v, len(rows)))
    for r in rows[:2]:
        print('  [%s]' % r['path'][:110])
        print('   %s' % r['text'][:800].replace('\n', ' '))

json.dump(R, open(os.path.join(OUT, 'p13-ax-originals.json'), 'w'), indent=1, default=str)
print('\nwrote p13-ax-originals.json')
