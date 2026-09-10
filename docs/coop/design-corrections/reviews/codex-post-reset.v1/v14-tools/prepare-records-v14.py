"""Prepare current review routing BEFORE pins/checks. Requires actual final source assessment.
This does not grant independent acceptance, blind acceptance, readiness or implementation.
"""
from pathlib import Path
import hashlib,json,copy
root=Path.cwd();dc=root/'docs/coop/design-corrections';ev=dc/'reviews/codex-post-reset.v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,d):
    assert not p.exists(),str(p)
    p.write_text(json.dumps(d,indent=2)+'\n')
assessment=ev/'coauthor-assessment-bv4-v3.json'
a=read(assessment)
assert a['finalSourceAssent'] is True and a['independentAcceptance'] is False
author=dc/'reviews/bv4-corrections-author.v3'
assert (author/'custody.json').is_file()
handoff=read(author/'handoff.json')
for row in handoff['delta']['aggregateVsFrozenV13']['changedFiles']:
    assert sha(root/row['path'])==row['afterSha256'],row['path']
blind_path=dc/'reviews/consumer-b.v4/output/blind-review.json';blind=read(blind_path)
assert sha(blind_path)=='a49eaa503ff0ceaf2bdcdc017b51937bd1322e0ca7f2bda505bda0537342cec1'
prior_path=dc/'reviews/post-reset-review.v13/review.json';prior=read(prior_path)
assert prior['overallVerdict']=='ACCEPT' and prior['newMustIssues']==[] and prior['newShouldIssues']==[]
manifest='8e6670f74d6e0bbed50b6c4914b3c7b29f627221f1591f4add5567f652f4c023'
def evidence(p,selector=None):
    out={'path':str(p.relative_to(root)),'sha256':sha(p)}
    if selector is not None:out['selector']=selector
    return out
intents={
'CB4-MUST-1':'Close relation-specific anchor cardinality: inventory facts have zero anchors, source-text facts at least one within the shared bounds, and body facts exactly one. Retain raw inventory path/digest/length and per-universe totality; preserve finding/repair/proof locations.',
'CB4-MUST-2':'Name the existing typed cause carriers and enforce declared deficiency support, with derivation-policy-unmet restricted to types and requirement-relative/existential sufficiency preserved. State selected-scalar limitations without inventing a new cause format.',
'CB4-SHOULD-1':'Derive clone payload body language from the same selected body-language rule as body identity, rather than the enclosing engine universe.',
'CB4-SHOULD-2':'Publish and enforce matrix capability identifiers, authenticated release declaration membership and a fixed full-product default distinct from installed availability; retain explicit overrides and correct unsupported/public disclosure routes.'}
items=[]
for key,severity in [('newMustIssues','MUST'),('newShouldIssues','SHOULD')]:
    for ix,row in enumerate(blind[key]):
        items.append({'id':row['id'],'severity':severity,'finding':row['title'],
        'reviewEvidence':evidence(blind_path,f'/{key}/{ix}'),
        'intendedCorrection':intents[row['id']],
        'status':'AUTHOR-CORRECTED-PENDING-INDEPENDENT-REVIEW',
        'finalSourceAssessment':evidence(assessment)})
assert len(items)==4
advs=read(ev/'advisory-application-account.v13.proposed.json')
assert len(advs['items'])==37
prior_dispositions={
'CLAUDE-V13-ADV-1':'Correct the successor validation-summary native.matrixCells to the actual66 before final pins and freezing. Preserve frozen v13 and its stale60 record verbatim; the applied summary must also measure equality with the accepted matrix/report.',
'CLAUDE-V13-ADV-2':'Preserve the concrete222/400/946 measurements and their actual source: the historical723-byte illustration is name-dependent and21crates is not a threshold. The applying D372 clarification must state this while preserving the raw32-byte digest law.'}
for ix,row in enumerate(prior['newAdvisories']):
    advs['items'].append({'id':row['id'],'reviewEvidence':evidence(prior_path,f'/newAdvisories/{ix}'),'disposition':prior_dispositions[row['id']]})
blind_advs={
'CB4-ADV-1':'Correct the current normative matrix count to66 (11capabilities by6modes); retain original review and frozen60 prose as history, and measure the successor summary before its freeze.',
'CB4-ADV-2':'Include the registered syntax semantic-universe/context domains in both normative prose enumerations; preserve the machine domain registry authority and selected language bindings.',
'CB4-ADV-3':'Publish the actual four effect-name to permission-token mapping against the existing seven-token truth table; no permission, enforcement claim or qualification is granted by the mapping.',
'CB4-ADV-4':'Preserve document-digest-keyed parameter identity and its explicit duplicate-selector refusal. The current distinct representation classes are unambiguous; a future second parameter selector in the same document requires a separately designed change.'}
for ix,row in enumerate(blind['nonBlockingAdvisories']):
    advs['items'].append({'id':row['id'],'reviewEvidence':evidence(blind_path,f'/nonBlockingAdvisories/{ix}'),'disposition':blind_advs[row['id']]})
assert len(advs['items'])==43 and len({r['id'] for r in advs['items']})==43
advs['standing']='43 individually accounted historical advisories; proposed successor corrections and explicit limits. No new independent acceptance or product qualification.'
write(ev/'advisory-application-account.v14.proposed.json',advs)
write(dc/'post-reset-dispositions.v14.proposed.json',{
'standing':'PROPOSED v14 correction of fresh blind Bv4 and same-scope Codex counterexamples; independent acceptance pending',
'predecessorManifestSha256':manifest,'actualPredecessorReview':evidence(prior_path),
'actualBlockingBlindReview':evidence(blind_path),'items':items,
'additionalCounterexamples':{'standing':'Additional same-class source findings and custody clarification do not rewrite original Bv4 severities or counts.','assessment':evidence(assessment),'priorAssessment':evidence(ev/'coauthor-assessment-bv4-v1.json'),'secondPassAssessment':evidence(ev/'coauthor-assessment-bv4-v2.json')},
'actualCoauthorHandoff':{**evidence(author/'handoff.json'),'sessionId':'77758b10-d7ba-4868-9d42-ae0b13e84cb6','role':'COAUTHOR follow-up, not independent acceptance'},
'advisoryAccount':{'path':'reviews/codex-post-reset.v1/advisory-application-account.v14.proposed.json','standing':'43 explicit accounts; original severity and limits preserved.'},
'implementationAuthorized':False,'readinessChanged':False,'productQualification':False,
'remaining':['fresh independent review of exact frozen successor at zero unresolved MUST/SHOULD','new fresh blind on same accepted normative inputs','complete independently reviewed application and readiness reconciliation']})
# Crosswalk is a pinned source: update it NOW, never after pin refresh/reference execution.
p=dc/'correction-crosswalk.proposed.json';before=p.read_bytes();cw=read(p)
before_path=ev/'crosswalk-before-v14.json';assert not before_path.exists();before_path.write_bytes(before)
for row in cw['items']:
    old=copy.deepcopy(row.get('latestCompletedReview'))
    if old and old not in row['historicalReviews']:row['historicalReviews'].append(old)
    row['latestCompletedReview']={**evidence(prior_path),
        'subjectManifestSha256':manifest,'overallVerdict':'ACCEPT','unresolvedMustIds':[],'unresolvedShouldIds':[],
        'selector':'/arDispositions/'+row['id'],
        'standing':'Historical independent v13 acceptance. Fresh Bv4 subsequently required corrections; this accepts neither successor bytes nor blind reconstructability.'}
    old_blind=copy.deepcopy(row.get('latestCompletedBlindReview'))
    history=row.setdefault('historicalBlindReviews',[])
    if old_blind and old_blind not in history:history.append(old_blind)
    row['latestCompletedBlindReview']={**evidence(blind_path),
        'overallVerdict':'CHANGES_REQUIRED','subjectManifestSha256':manifest,
        'unresolvedMustIds':[r['id'] for r in blind['newMustIssues']],
        'unresolvedShouldIds':[r['id'] for r in blind['newShouldIssues']]}
    row['status']='AUTHOR-CORRECTED-PENDING-INDEPENDENT-REVIEW'
assert len(cw['items'])==16
p.write_text(json.dumps(cw,indent=2)+'\n')
write(ev/'crosswalk-update-v14.json',{'beforeSha256':hashlib.sha256(before).hexdigest(),'afterSha256':sha(p),'standing':'Pre-pin current routing update; historical evidence retained. No readiness change.'})
p=dc/'README.md';before=p.read_bytes();bp=ev/'corrections-readme-before-v14.md';assert not bp.exists();bp.write_bytes(before)
p.write_text('''# Architecture corrections — v14 awaiting independent review

**Not ready for implementation.** Actual Claude and Codex addressed the fresh blind review's anchor cardinality, typed cause carriers, clone body-language and capability/default findings. The [technical assessment](reviews/codex-post-reset.v1/technical-review.v14.md) records exact final source, counterexample rechecks and limits. Reference results remain subject to the final pin seal and independent reproduction.

The intended product remains one complete design implemented in stages. The corrected frozen candidate must receive fresh independent acceptance with zero unresolved MUST/SHOULD, a new blind consumer on those accepted normative bytes, and complete independently reviewed application/readiness reconciliation. Historical v13 acceptance does not accept these successor bytes. No product implementation, commit or push is authorized. [The resume guide](reviews/NEXT-REVIEW.md) owns current status.

## Earlier progress — historical

'''+before.decode())
print('Prepared 4 required dispositions, 43 advisory accounts and current 16-row crosswalk. No acceptance.')
