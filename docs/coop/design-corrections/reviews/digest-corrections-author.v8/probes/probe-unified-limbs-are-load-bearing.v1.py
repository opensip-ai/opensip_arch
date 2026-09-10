"""PROBE: do the earlier limbs actually reach the inherited annotation locations now?

Root's finding was that limbs 1 and 2 read direct property annotations while limb 3 read effective
ones, so alias and branch locations escaped retention and residue. This probe does not merely re-run
root's nine vectors green; it NEUTRALISES the unified account and shows the six alias/branch vectors
become admitted again, reproducing the exact defect on demand.

Neutralisation: `relation_digest_annotation_coverage` is wrapped so that every sighting keeps its
GOVERNED status and its unannotated verdict - so limb 3 still works and unrelated negatives are
undisturbed - but any sighting whose annotation was reached through an alias chain or a branch is
reported with NO annotations to the earlier limbs, which is precisely the pre-v8 blindness. If the
six vectors do not flip, the correction would be decoration.

The three FIELD vectors must behave identically in both states, because they never depended on the
inherited account. That is the control that shows the neutralisation is targeted rather than global.
"""
import copy,hashlib,importlib.util,json
from pathlib import Path

ROOT=Path('/Users/sb/code/opensip-ai/opensip_arch')
MODEL=ROOT/'docs/coop/design-corrections/foundation/identity-model.py'
DOCUMENT=ROOT/'docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json'
spec=importlib.util.spec_from_file_location('identity_model_v8_probe',MODEL)
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)

def vector(location,retention):
    """Root's construction, reproduced: same governed `stray`, three locations, three retentions."""
    document=copy.deepcopy(M.RELATION_DOCUMENT)
    document['$defs']['ProbeAlias']={'$ref':'#/$defs/DigestHex'}
    annotation={'representation':'raw-artifact','retention':retention,
                'authority':'hypothetical-schema-probe',
                'join':'Synthetic schema-only annotation-location control; no product field or authority.'}
    field={'$ref':'#/$defs/ProbeAlias'}
    if location=='field':field['x-opensip-digest']=annotation
    elif location=='alias':document['$defs']['ProbeAlias']['x-opensip-digest']=annotation
    else:field={'oneOf':[{'type':'null'},{'$ref':'#/$defs/DigestHex','x-opensip-digest':annotation}]}
    document['$defs']['FilePayloadV1']['properties']['stray']=field
    return document

def measure():
    rows={}
    for location in ('field','alias','branch'):
        for retention in ('preimage','invented-retention','not-joined'):
            try:
                M.relation_annotation_closure('file',vector(location,retention))
                rows[location+'-'+retention]='ADMITTED'
            except Exception as exc:rows[location+'-'+retention]=str(exc)
    return rows

with_unified=measure()

original=M.relation_digest_annotation_coverage
def blinded(document=None):
    """The pre-v8 shape: the earlier limbs see only DIRECT property annotations, while coverage
    keeps its inherited account."""
    result=copy.deepcopy(original(document))
    doc=M.RELATION_DOCUMENT if document is None else document
    for relation,entry in result['byRelation'].items():
        selector=doc['$defs'][doc['x-opensip-relation-registry']['relations'][relation]['selector'].split('/')[-1]]
        for sighting in entry['sightings']:
            direct=selector.get('properties',{}).get(sighting['field'],{})
            if not (type(direct) is dict and 'x-opensip-digest' in direct):
                sighting['annotations']=[] if sighting['annotations'] else []
                sighting['blindedFromEarlierLimbs']=True
    return result
M.relation_digest_annotation_coverage=blinded
try:
    without_unified=measure()
finally:
    M.relation_digest_annotation_coverage=original

flipped=sorted(k for k in with_unified
               if with_unified[k]!='ADMITTED' and without_unified[k]=='ADMITTED')
field_stable=all(with_unified[k]==without_unified[k] for k in with_unified if k.startswith('field-'))

print(json.dumps({
 'standing':'actual Claude coauthor probe; schema/reference evidence only, not a payload or Run '
            'attack, no runtime security claim and no product qualification',
 'rootFinding':'CODEX-PUBLIC-NOTE v7 @6015 bytes, section "All three limbs must use the same '
               'inherited annotation"; construction follows root probe '
               'annotation-inherited-limbs-draft-counterexample.v10/probe.py',
 'modelSha256':hashlib.sha256(MODEL.read_bytes()).hexdigest(),
 'relationDocumentSha256':hashlib.sha256(DOCUMENT.read_bytes()).hexdigest(),
 'relationDocumentEdited':False,
 'withUnifiedAccount':with_unified,
 'withEarlierLimbsBlinded':without_unified,
 'flippedToAdmittedWhenBlinded':flipped,
 'fieldVectorsUnaffectedByTheNeutralisation':field_stable,
 'loadBearing':(len(flipped)==4 and field_stable and
                all(with_unified[l+'-not-joined']=='ADMITTED' for l in ('field','alias','branch')))},
 indent=1))
