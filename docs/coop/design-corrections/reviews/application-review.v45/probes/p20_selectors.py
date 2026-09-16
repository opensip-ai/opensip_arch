import json, sys, re
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2/'
R = '/Users/sb/code/opensip-ai/opensip_arch/'
C = '/tmp/opensip-design-corrections/candidate-subject.v45/'
print('python', sys.version)
docs = {}
def load(p):
    if p not in docs: docs[p] = json.load(open(R + p))
    return docs[p]
def ptr(doc, pointer):
    for part in pointer.lstrip('/').split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        doc = doc[int(part)] if isinstance(doc, list) else doc[part]
    return doc
recs = ['readiness-row-map.v1.json', 'review-owner-dispositions.v1.json', 'correction-crosswalk.applied.v1.json', 'inherited-residuals.applied.v1.json', 'evaluation-residual-dispositions.applied.v1.json', 'qualification-gates.applied.v1.json', 'accepted-review-advisories.v1.json', 'application.v1.json']
n = 0; bad = []
def walk(o, rec, path, parent_id=None):
    global n
    if isinstance(o, dict):
        pid = o.get('id', parent_id)
        if 'selector' in o and 'path' in o and o['path'].endswith('.json') and isinstance(o['selector'], str) and o['selector'].startswith('/') and '/reviews/' in o['path']:
            n += 1
            try:
                v = ptr(load(o['path']), o['selector'])
                if isinstance(v, dict) and 'id' in v and pid and v['id'] != pid and not path.endswith('sharedTrustedCodeAssumption/acceptedDesignAccountSource'):
                    bad.append((rec, path, o['selector'], 'id mismatch', v['id'], pid))
            except Exception as ex:
                bad.append((rec, path, o['selector'], 'unresolved', str(ex)))
        for k, v in o.items(): walk(v, rec, path + '/' + k, pid)
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, rec, path + '/' + str(i), parent_id)
for r in recs:
    walk(json.load(open(S + 'files/docs/coop/design-corrections/' + r)), r, '')
print('review selectors resolved', n, 'problems', bad)
dr = load('docs/coop/design-corrections/reviews/claude-independent-design.v45/review.json')
app = json.load(open(S + 'files/docs/coop/design-corrections/application.v1.json'))
print('TCB accepted account == design review sharedAssumptionTCBSCOPE01', app['sharedTrustedCodeAssumption']['acceptedDesignAccount'] == dr['sharedAssumptionTCBSCOPE01'])
ca = load('docs/coop/design-corrections/reviews/codex-post-reset.v1/design-assent.v45.json')
print('TCB root account == codex sharedAssumption', app['sharedTrustedCodeAssumption']['rootDesignAccount'] == ca['sharedAssumption'])
print('design review contracts == app acceptedContracts', ca['contracts'] == app['acceptedContracts'])
m = json.load(open(S + 'application-subject.v45.json'))
fp = {e['path'] for e in m['files']}
for p in ['docs/coop/design-corrections/application-activation.v1.json', m['retainedManifestPath'], m['retainedReviewPath']]:
    print('in manifest files?', p, p in fp)
print('all file paths safe', all((p.startswith('docs/') or p == 'README.md') and '..' not in p.split('/') for p in fp))
# D-372 identity bullet in proposed act vs staged body
act = open(C + 'docs/coop/design-corrections/D-372-corrections.proposed.md', encoding='utf-8').read()
i = act.find('semantic identities'); j = act.find('identity versions')
print('proposed act identity bullet:', act[max(0, i - 200): i + 200] if i >= 0 else None, '|', j)
body = open(S + 'files/docs/coop/COORDINATOR-DECISIONS.md', encoding='utf-8').read()
body = body[body.index('## D-372 — complete intended-product design'):]
# compare the body with the proposed act text after its header
import difflib
al = act.splitlines(); bl = body.splitlines()
ud = list(difflib.unified_diff(al, bl, 'proposed-act', 'staged-D372-body', n=0, lineterm=''))
open('/private/tmp/opensip-design-corrections/application-review.v45/probes/p20_act_vs_body.diff', 'w').write('\n'.join(ud))
print('act vs body diff lines', len(ud))
ide = open(C + 'docs/v2/contracts/product-v1/identity-and-evidence.md', encoding='utf-8').read()
for pat in [r'profile[- ]?3', r'profile[- ]?2', r'run3', r'evaluator3', r'major[- ]?two', r'major 2', r'major2']:
    print('identity contract', pat, len(re.findall(pat, ide)))
nat = open(C + 'docs/v2/contracts/product-v1/native-evidence.md', encoding='utf-8').read()
print('native permission-truth-tables refs', sorted(set(re.findall(r'permission-truth-tables\.v\d+\.json', nat))))
for mm in re.finditer(r'permission-truth-tables\.v\d+\.json[^\n]{0,200}', nat):
    print('   ', mm.group(0)[:260])
