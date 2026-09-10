"""PROBE: is the new third limb actually load-bearing, or just another passing test?

v9-S1's whole point is that a check can carry a name it does not test. So this probe does not
merely re-run the suite; it NEUTRALISES the new enforcement and shows the property becomes false
again, reproducing the independent reviewer's exact finding on demand.

Three measurements:

  A. With enforcement: the reviewer's 39 injections (13 relations x 3 governed forms) each refuse,
     with the shipped document as the positive control.
  B. With relation_digest_annotation_coverage neutralised to report nothing unannotated - the
     precise shape of the pre-v7 defect, since the old closure could not see such a field at all -
     the same 39 injections are ADMITTED again.
  C. The suite check that carries the name is evaluated in both states against a document holding
     an unannotated CanonicalPath. Under enforcement it must be False; neutralised it must be True,
     which is exactly what the reviewer reproduced against the frozen v9 bytes.

If B and C did not flip, the new check would be decoration and this correction would not have
closed anything.
"""
import copy,hashlib,importlib.util,json
from pathlib import Path

ROOT=Path('/Users/sb/code/opensip-ai/opensip_arch')
MODEL=ROOT/'docs/coop/design-corrections/foundation/identity-model.py'
DOCUMENT=ROOT/'docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json'
spec=importlib.util.spec_from_file_location('identity_model_v7_probe',MODEL)
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)

def inject(relation,form,document=None):
    document=copy.deepcopy(M.RELATION_DOCUMENT if document is None else document)
    selector=document['$defs'][M.RELATIONS[relation]['selector'].split('/')[-1]]
    selector['properties']['strayUnannotated']={'$ref':'#/$defs/'+form}
    return document

def sweep():
    admitted=[];refused={}
    for relation in sorted(M.RELATIONS):
        for form in ('DigestHex','Sha256Text','CanonicalPath'):
            try:
                M.relation_annotation_closure(relation,inject(relation,form))
                admitted.append(relation+'/'+form)
            except Exception as exc:refused[relation+'/'+form]=str(exc)
    return admitted,refused

def suite_assertion(document):
    """The shipped check's assertion, evaluated against a hypothetical document."""
    relations=document['x-opensip-relation-registry']['relations']
    coverage=M.relation_digest_annotation_coverage(document)
    return bool(coverage['unannotated']==[] and coverage['total']==coverage['annotated'] and
                all(M.relation_annotation_closure(name,document) is not None for name in relations) and
                {name for name,row in relations.items() if row['snapshotJoins'] or 'bodyIdentityJoin' in row}
                =={'file','package','vcs-change','clones'})

def old_suite_assertion(document):
    """The PRE-v7 assertion the reviewer reproduced verbatim: closure non-None plus the join-bearing
    relation set. Retained here so the difference is visible rather than asserted."""
    relations=document['x-opensip-relation-registry']['relations']
    try:
        return bool(all(M.relation_annotation_closure(name,document) is not None for name in relations) and
                    {name for name,row in relations.items() if row['snapshotJoins'] or 'bodyIdentityJoin' in row}
                    =={'file','package','vcs-change','clones'})
    except Exception as exc:return 'raised:'+str(exc)[:80]

stray=inject('file','CanonicalPath')
shipped_ok={r:(M.relation_annotation_closure(r) is not None) for r in sorted(M.RELATIONS)}
admitted_with,refused_with=sweep()
with_enforcement={'injectionsAdmitted':admitted_with,'refusedCount':len(refused_with),
                  'sampleCause':sorted(refused_with.values())[0] if refused_with else None,
                  'suiteAssertionOnStrayDocument':suite_assertion(stray),
                  'oldAssertionOnStrayDocument':old_suite_assertion(stray)}

original=M.relation_digest_annotation_coverage
M.relation_digest_annotation_coverage=lambda document=None:{
    'total':0,'annotated':0,'unannotated':[],'governedForms':list(M.GOVERNED_RELATION_FORMS),
    'byRelation':{}}
try:
    admitted_without,refused_without=sweep()
    without_enforcement={'injectionsAdmitted':len(admitted_without),
                         'refusedCount':len(refused_without),
                         'suiteAssertionOnStrayDocument':suite_assertion(stray),
                         'oldAssertionOnStrayDocument':old_suite_assertion(stray)}
finally:
    M.relation_digest_annotation_coverage=original

print(json.dumps({
 'standing':'actual Claude coauthor probe; design/reference evidence only, no product qualification '
            'and no runtime security claim',
 'reviewerFinding':'post-reset-review.v9 v9-S1; construction follows the reviewer probes '
                   'probes/p03_residue_enforcement.py and probes/p04_third_limb.py, which are theirs',
 'modelSha256':hashlib.sha256(MODEL.read_bytes()).hexdigest(),
 'relationDocumentSha256':hashlib.sha256(DOCUMENT.read_bytes()).hexdigest(),
 'relationDocumentEdited':False,
 'shippedDocumentCoherentForEveryRelation':shipped_ok,
 'shippedCoverage':original(),
 'withEnforcement':with_enforcement,
 'withoutEnforcement':without_enforcement,
 'loadBearing':(with_enforcement['injectionsAdmitted']==[] and
                without_enforcement['injectionsAdmitted']==39 and
                with_enforcement['suiteAssertionOnStrayDocument'] is False and
                without_enforcement['suiteAssertionOnStrayDocument'] is True),
 # The pre-v7 blindness is the NEUTRALISED value: with enforcement removed, the old assertion
 # shape returns True on a document carrying an unannotated field, which is precisely what the
 # independent reviewer reproduced against the frozen v9 bytes. Under enforcement that same shape
 # now RAISES, because the closure it calls checks the limb.
 'preV7AssertionShapeWasBlindToIt':without_enforcement['oldAssertionOnStrayDocument'] is True,
 'andThatShapeNowRaisesUnderEnforcement':str(with_enforcement['oldAssertionOnStrayDocument'])[:60]},indent=1))
