"""Remaining targeted checks: other added inventory rows, owner literal subsets, rerun stdout deltas, D9 selectors, TCB dependents, blind/advisory accounts, v12-A1/A2."""
import json, hashlib, os, re, difflib
PK = '/private/tmp/opensip-design-corrections/application-stage.v46/'
S = PK + 'files/'
S45 = '/private/tmp/opensip-design-corrections/application-stage.v45.2/'
SNAP = '/tmp/opensip-design-corrections/candidate-subject.v45/'
R = '/Users/sb/code/opensip-ai/opensip_arch/'
DC = 'docs/coop/design-corrections/'
def h(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def ptr(doc, p):
    for part in [x.replace('~1', '/').replace('~0', '~') for x in p.strip('/').split('/')] if p.strip('/') else []:
        doc = doc[int(part)] if isinstance(doc, list) else doc[part]
    return doc
out = {}
# 1 other added inventory rows
inv46 = {r['path']: r for r in json.load(open(S + 'docs/operations/document-inventory.v1.json'))['files']}
inv45 = {r['path'] for r in json.load(open(S45 + 'files/docs/operations/document-inventory.v1.json'))['files']}
added = sorted(set(inv46) - inv45)
other = [p for p in added if not p.startswith(DC + 'reviews/application-review.v45/')]
out['otherAdded'] = {'n': len(other), 'paths': other, 'hashOk': all(os.path.exists(R + p) and h(R + p) == inv46[p]['sha256'] for p in other)}
# 2 owner literal subset
dr = json.load(open(R + DC + 'reviews/claude-independent-design.v45/review.json'))
own = json.load(open(S + DC + 'review-owner-dispositions.v1.json'))
res = []
for rec in own['records']:
    d = next(x for x in dr['scopedReviewOwnerDispositions'] if x['id'] == rec['id'])
    res.append((rec['id'], all(rec.get(k) == v for k, v in d.items()), rec.get('applicationDisposition'), rec.get('designGrade'), rec.get('gradeAuthority')))
out['ownerSubset'] = res
# 3 rerun stdout deltas
for n in ['evaluator3/enumeration.stdout', 'evaluator3/execution-inputs.stdout']:
    a = open(PK + 'support/reference-rerun/' + n).read().splitlines(); b = open(PK + 'support/reference-rerun.v46/' + n).read().splitlines()
    d = [l for l in difflib.unified_diff(a, b, lineterm='', n=0) if l[:1] in '+-' and not l.startswith(('+++', '---'))]
    norm = [re.sub(r'application-stage\.v4[56](\.2)?(-validation)?', 'STAGE', l[1:]).replace('reference-rerun.v46', 'reference-rerun') for l in d]
    out.setdefault('stdoutDelta', {})[n] = {'changedLines': len(d), 'pathOnly': len(set(x for x in norm)) * 2 == len(norm) or sorted(norm[0::2]) == sorted(norm[1::2]), 'sample': d[:4]}
# 4 D9
ir = json.load(open(S + DC + 'inherited-residuals.applied.v1.json'))
c1 = ir['parents'][6]['carriedCrossUnitObligation']; c2 = ir['residuals'][7]['carriedCrossUnitObligation']
out['d9Equal'] = c1 == c2
out['d9OtherCarriers'] = [(k, i, r['id']) for k in ('parents', 'residuals') for i, r in enumerate(ir[k]) if 'carriedCrossUnitObligation' in r]
src = c1['obligationSource']; ns = json.load(open(SNAP + src['path']))
out['d9SourceHash'] = h(SNAP + src['path']) == src['sha256'] and h(S + src['path']) == src['sha256'] if os.path.exists(S + src['path']) else h(SNAP + src['path']) == src['sha256']
out['d9Obligation'] = ptr(ns, src['selector'])
cs = c1['selectedCompositionIsComplete']; cj = json.load(open(SNAP + cs['path']))
d9c = ptr(cj, cs['selector'])
out['d9FaultCause'] = {'hash': h(SNAP + cs['path']) == cs['sha256'], 'members': d9c.get('enum')}
ia = c1['inheritedArtifactUnchanged']; ij = json.load(open(SNAP + ia['path']))
out['d9Inherited'] = {'hash': h(SNAP + ia['path']) == ia['sha256'], 'enum': ptr(ij, ia['selector'])}
out['d9IntegrationHash'] = h(SNAP + c1['enforcedInAcceptedSource']['path']) == c1['enforcedInAcceptedSource']['sha256']
t = open(SNAP + c1['enforcedInAcceptedSource']['path']).read().splitlines()
out['d9IntegrationLines'] = [(i + 1, l.strip()[:160]) for i, l in enumerate(t) if 'host-invariant' in l or 'ILLEGAL_STATE' in l][:12]
wf = open(SNAP + 'docs/v2/contracts/product-v1/workflows-and-surfaces.md').read().splitlines()
out['d9WorkflowsLines'] = [(i + 1, l.strip()[:200]) for i, l in enumerate(wf) if 'host-invariant' in l][:8]
# 5 TCB dependents in evaluation dispositions
ev = json.load(open(S + DC + 'evaluation-residual-dispositions.applied.v1.json'))
deps = []
for it in ev['items']:
    tj = json.dumps(it)
    if 'TCB-SCOPE-01' in tj: deps.append(it['id'])
out['evalTCBMentions'] = sorted(deps)
out['evalIds'] = [it['id'] for it in ev['items']]
out['evalGrades'] = sorted(set(str(it.get('designGrade')) for it in ev['items']))
r12 = json.dumps(ir['residuals'][11])
out['R12mentionsTCB'] = 'TCB-SCOPE-01' in r12
app = json.load(open(S + DC + 'application.v1.json'))
tcb = app['sharedTrustedCodeAssumption']
out['tcbKeys'] = list(tcb)
out['tcbAccountsEqualDesign'] = tcb['acceptedDesignAccount'] == dr['sharedAssumptionTCBSCOPE01']
out['tcbRootEqDesign'] = tcb['rootDesignAccount'] == dr['sharedAssumptionTCBSCOPE01']
out['tcbOther'] = {k: v for k, v in tcb.items() if k not in ('acceptedDesignAccount', 'rootDesignAccount')}
# 6 blind review + advisories
bl = json.load(open(R + DC + 'reviews/consumer-b.v24-source45.v1/blind-review.json'))
out['blind'] = {k: (bl[k] if not isinstance(bl[k], (list, dict)) else len(bl[k])) for k in bl}
out['blindOrigin'] = bl.get('origin')
adv = json.load(open(S + DC + 'accepted-review-advisories.v1.json'))
out['advTop'] = {k: (len(v) if isinstance(v, (list, dict)) else v) for k, v in adv.items()}
# 7 v12-A1
ic = json.load(open(R + DC + 'reviews/codex-post-reset.v1/identity-check-counts.v45.json'))
out['identityCounts'] = {k: v for k, v in ic.items() if not isinstance(v, (list, dict))}
out['identityCountsHash'] = h(R + DC + 'reviews/codex-post-reset.v1/identity-check-counts.v45.json')
# recount from rerun identity report
idr = json.load(open(PK + 'support/reference-rerun.v46/foundation/identity-report.json'))
def collect(o, acc):
    if isinstance(o, dict):
        if 'id' in o and ('passed' in o or 'ok' in o or 'status' in o): acc.append((o['id'], o.get('passed', o.get('ok', o.get('status')))))
        for v in o.values(): collect(v, acc)
    elif isinstance(o, list):
        for v in o: collect(v, acc)
    return acc
calls = collect(idr, [])
from collections import Counter
cc = Counter(i for i, _ in calls)
out['identityRecount'] = {'calls': len(calls), 'distinct': len(cc), 'dupExtra': sum(v - 1 for v in cc.values()), 'dupIds': {k: v for k, v in cc.items() if v > 1}, 'nonPass': sum(1 for _, p in calls if p not in (True, 'PASS', 'passed', 'ok'))}
# 8 v12-A2
rep = app.get('acceptedDesignReproduction', {})
out['reproKeys'] = list(rep)
cmds = rep.get('commands', [])
chk = []
for c in cmds:
    s = c.get('source'); sh = c.get('sourceSha256')
    chk.append((c.get('name'), s, sh == h(SNAP + s) if s and os.path.exists(SNAP + s) else None, c.get('reproductionCommand', c.get('argv'))))
out['reproCommands'] = chk
json.dump(out, open('/private/tmp/opensip-design-corrections/application-review.v46/probes/out/p09.json', 'w'), indent=1, ensure_ascii=False, default=str)
print(json.dumps(out, indent=1, ensure_ascii=False, default=str)[:16000])
