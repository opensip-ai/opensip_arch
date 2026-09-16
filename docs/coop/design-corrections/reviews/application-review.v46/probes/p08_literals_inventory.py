"""Literal design-review disposition equality in application records; inventory/classification scope checks; removed v45 root support files."""
import json, hashlib, os, re
PK = '/private/tmp/opensip-design-corrections/application-stage.v46/'
S = PK + 'files/'
R = '/Users/sb/code/opensip-ai/opensip_arch/'
S45 = '/private/tmp/opensip-design-corrections/application-stage.v45.2/'
def h(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
out = {}
dr = json.load(open(R + 'docs/coop/design-corrections/reviews/claude-independent-design.v45/review.json'))
def rows_of(coll):
    v = dr[coll]
    return v if isinstance(v, list) else [dict(id=k, **x) if isinstance(x, dict) else {'id': k, 'value': x} for k, x in v.items()]
drmap = {}
for coll in ['inheritedResidualDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions', 'scopedReviewOwnerDispositions']:
    for r in rows_of(coll):
        drmap[(coll, r.get('id'))] = r
out['designReviewRows'] = {c: sum(1 for k in drmap if k[0] == c) for c in set(k[0] for k in drmap)}
# find independentDisposition-like embeddings in application records
recs = ['inherited-residuals.applied.v1.json', 'evaluation-residual-dispositions.applied.v1.json', 'review-owner-dispositions.v1.json', 'correction-crosswalk.applied.v1.json', 'readiness-row-map.v1.json', 'application.v1.json']
eq = {}; neq = []
def walk(o, path, fname):
    if isinstance(o, dict):
        if 'id' in o and ('appliedByThisReview' in o or 'finalApplicationOutcomeGranted' in o) and ('disposition' in o):
            cands = [v for k, v in drmap.items() if k[1] == o['id']]
            match = any(c == o for c in cands)
            if match: eq[fname] = eq.get(fname, 0) + 1
            else:
                diffs = []
                for c in cands:
                    diffs.append(sorted(k for k in set(c) | set(o) if c.get(k) != o.get(k)))
                neq.append((fname, path, o['id'], diffs))
        for k, v in o.items(): walk(v, path + '/' + k, fname)
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, path + '/' + str(i), fname)
for f in recs:
    p = S + 'docs/coop/design-corrections/' + f
    if os.path.exists(p): walk(json.load(open(p)), '', f)
out['literalEqual'] = eq; out['literalNotEqual'] = neq[:40]; out['literalNotEqualCount'] = len(neq)
# TCB dependents in design review
out['designReviewTCB'] = dr.get('sharedAssumptionTCBSCOPE01')
# inventory
inv = json.load(open(S + 'docs/operations/document-inventory.v1.json'))
cls = json.load(open(S + 'docs/operations/document-classification.v1.json'))
m = json.load(open(PK + 'application-subject.v46.json'))
fh = {e['path']: e['sha256'] for e in m['files']}
invrows = {r['path']: r for r in inv['files']}
out['invDupPaths'] = len(inv['files']) - len(invrows)
out['invFileCount'] = [inv['fileCount'], len(inv['files'])]
bad = []
for p, s in fh.items():
    if p in ('docs/operations/document-inventory.v1.json', 'docs/operations/document-classification.v1.json'): continue
    r = invrows.get(p)
    if r is None: bad.append((p, 'no row'))
    elif r.get('sha256') != s: bad.append((p, 'sha', r.get('sha256')))
out['stagedRowsBad'] = bad
w = inv['workingTreeDelta']
cp = w['contentPaths']
out['contentPaths'] = {'n': len(cp), 'unique': len(set(cp)), 'missingRows': [p for p in cp if p not in invrows][:10], 'stagedNotInContent': [p for p in fh if p not in cp and p not in w['excludedPaths']][:10]}
# late evidence: rows under application-review.v45/ hash vs live
lp45 = 'docs/coop/design-corrections/reviews/application-review.v45/'
rows45 = [p for p in invrows if p.startswith(lp45)]
live45 = []
for dp, dn, fn in os.walk(R + lp45):
    for x in fn: live45.append(os.path.relpath(os.path.join(dp, x), R))
out['review45Rows'] = {'rows': len(rows45), 'liveFiles': len(live45), 'liveNotInRows': sorted(set(live45) - set(rows45))[:10], 'rowsNotLive': sorted(set(rows45) - set(live45))[:10],
                       'hashMismatch': [p for p in rows45 if os.path.exists(R + p) and h(R + p) != invrows[p].get('sha256')][:10], 'inContentPaths': sum(1 for p in rows45 if p in set(cp))}
# any rows under application-review.v46/ or root-application46-delta or application-subject.v46
out['postFreezeRows'] = [p for p in invrows if 'application-review.v46/' in p or 'root-application46-delta' in p or p.endswith('application-subject.v46.json') or p.endswith('application-activation.v1.json')]
out['subject45RetainedRow'] = invrows.get('docs/coop/design-corrections/reviews/application-subject.v45.json', {}).get('sha256')
# classification
crows = {r['path']: r for r in cls['files']}
out['classCounts'] = {'declared': cls['counts'], 'sum': sum(cls['counts'].values()), 'rows': len(cls['files']), 'actual': {}}
for r in cls['files']: out['classCounts']['actual'][r['classification']] = out['classCounts']['actual'].get(r['classification'], 0) + 1
out['classVsInvPathsEqual'] = set(crows) == set(invrows)
out['classShaMismatch'] = [p for p in crows if crows[p].get('sha256') != invrows[p].get('sha256')][:10]
nav = [p for p, r in crows.items() if r['classification'].startswith('current/navigation')]
out['navigationDocs'] = nav
selfref = [p for p, r in crows.items() if r['classification'] == 'current/architecture' and r.get('currentNavigationReferences') == ['docs/catalog/current-design.md'] and not r.get('referencedByCount')]
out['catalogOnlyReferenced'] = selfref
out['added188Classes'] = {}
old = json.load(open(S45 + 'files/docs/operations/document-classification.v1.json'))
oldp = {r['path'] for r in old['files']}
for p, r in crows.items():
    if p not in oldp: out['added188Classes'][r['classification']] = out['added188Classes'].get(r['classification'], 0) + 1
# removed root support files in v45 package
for n in ['accepted-source-application-delta.json', 'assembly-metadata.json', 'bound-review-receipt.json']:
    p = S45 + n
    out.setdefault('removed45Root', {})[n] = open(p).read()[:900] if os.path.exists(p) else None
json.dump(out, open('/private/tmp/opensip-design-corrections/application-review.v46/probes/out/p08.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False)[:14000])
