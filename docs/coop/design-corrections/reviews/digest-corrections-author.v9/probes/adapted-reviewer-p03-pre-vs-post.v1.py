"""ADAPTATION of the ACTUAL INDEPENDENT REVIEWER's p03, run against PRE and POST source.

NOT my construction. Provenance: `/tmp/opensip-design-corrections/post-reset-review.v10/probes/
p03_order_hardened.py`, authored by the actual independent reviewer, session
4628c693-7a5e-4567-a1c8-e2f7ae322651, captured verbatim at
`digest-corrections-author.v9/reviewer-p02-input/p03_order_hardened.py`
(sha256 c58b7ccc35cf7bd2013d81555726597e7b9e6458ef6eb09602279afb2b19bd50) with its result
(db281a0d91b6f78495a7fe9a1bec894e1a298e626ac6563514e344aa2e01a039), per
`input-custody-addendum.v1.json`. Their conclusions are theirs; no final verdict is inferred.

p03 hardens p02 against fair objections: every hypothetical document is checked against the
JSON Schema 2020-12 metaschema, case B is shown to be a pure key-order swap of identical content, and
the shipped document is shown to have no same-path collision at all.

This adaptation keeps the vector builders and the metaschema check unchanged, and replaces only the
reviewer's hardcoded load/emit paths - their `harness.emit` writes into their live review directory -
with my disposable ones, measuring PRE (frozen v10) against POST (my work copy).
"""
import copy,collections,hashlib,importlib.util,json
from pathlib import Path
from jsonschema import Draft202012Validator

V9=Path('/tmp/opensip-design-corrections/digest-corrections-author.v9')
IMAGES={'pre':V9/'runs/pre-image/docs/coop/design-corrections/foundation/identity-model.py',
        'post':V9/'work/docs/coop/design-corrections/foundation/identity-model.py'}
REL='file'
ANN={'representation':'raw-artifact','retention':'not-joined',
     'authority':'hypothetical-schema-probe',
     'reason':'reviewer schema-only control; no runtime field or authority introduced'}

def load(label,path):
    spec=importlib.util.spec_from_file_location('p03_'+label,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def selector_of(doc,name):
    row=doc['x-opensip-relation-registry']['relations'][name]
    return doc['$defs'][row['selector'].split('/')[-1]]

# ---- reviewer's builders, reproduced unchanged ---------------------------------------------------
def a_unannotated_first(doc):
    doc['$defs']['ProbeContainer']={'type':'object','properties':{'leaf':{'$ref':'#/$defs/DigestHex'}}}
    selector_of(doc,REL)['properties']['probe']={
        '$ref':'#/$defs/ProbeContainer',
        'properties':{'leaf':{'$ref':'#/$defs/DigestHex','x-opensip-digest':ANN}}}

def a_annotated_first(doc):
    doc['$defs']['ProbeContainer']={'type':'object',
        'properties':{'leaf':{'$ref':'#/$defs/DigestHex','x-opensip-digest':ANN}}}
    selector_of(doc,REL)['properties']['probe']={
        '$ref':'#/$defs/ProbeContainer','properties':{'leaf':{'$ref':'#/$defs/DigestHex'}}}

def b_items_first(doc):
    selector_of(doc,REL)['properties']['probe']={
        'items':{'$ref':'#/$defs/DigestHex'},
        'additionalProperties':{'$ref':'#/$defs/DigestHex','x-opensip-digest':ANN}}

def b_addprops_first(doc):
    selector_of(doc,REL)['properties']['probe']={
        'additionalProperties':{'$ref':'#/$defs/DigestHex','x-opensip-digest':ANN},
        'items':{'$ref':'#/$defs/DigestHex'}}

def c_unannotated_only(doc):
    doc['$defs']['ProbeContainer']={'type':'object','properties':{'leaf':{'$ref':'#/$defs/DigestHex'}}}
    selector_of(doc,REL)['properties']['probe']={'$ref':'#/$defs/ProbeContainer'}

def c_annotated_only(doc):
    doc['$defs']['ProbeContainer']={'type':'object',
        'properties':{'leaf':{'$ref':'#/$defs/DigestHex','x-opensip-digest':ANN}}}
    selector_of(doc,REL)['properties']['probe']={'$ref':'#/$defs/ProbeContainer'}

VECTORS=[('caseA_unannotated_seen_first',a_unannotated_first),
         ('caseA_annotated_seen_first',a_annotated_first),
         ('caseB_items_written_first',b_items_first),
         ('caseB_addprops_written_first',b_addprops_first),
         ('control_unannotated_only',c_unannotated_only),
         ('control_annotated_only',c_annotated_only)]

def measure(label,path):
    M=load(label,path);rows={}
    for name,build in VECTORS:
        doc=copy.deepcopy(M.RELATION_DOCUMENT);build(doc)
        metaschema_ok,metaschema_err=True,None
        try:Draft202012Validator.check_schema(doc)
        except Exception as exc:metaschema_ok,metaschema_err=False,str(exc)[:200]
        try:
            M.relation_annotation_closure(REL,doc);verdict,cause='ADMIT',None
        except Exception as exc:verdict,cause='REFUSE',type(exc).__name__+':'+str(exc)
        rows[name]={'verdict':verdict,'cause':cause,'metaschemaValid':metaschema_ok,
                    'metaschemaError':metaschema_err}
    shipped=M.relation_digest_annotation_coverage(copy.deepcopy(M.RELATION_DOCUMENT))
    paths=[s['path'] for s in shipped['sightings']]
    rows['_shippedScope']={'sightingPaths':len(paths),
        'duplicatePaths':[p for p,n in collections.Counter(paths).items() if n>1],
        'shippedHasNoSamePathCollision':len(paths)==len(set(paths)),
        'shippedUnannotated':shipped['unannotated']}
    return rows,hashlib.sha256(path.read_bytes()).hexdigest()

rows={};hashes={}
for label,path in IMAGES.items():rows[label],hashes[label]=measure(label,path)

def assess(r):
    return {'caseA_orderDecidesAdmission':r['caseA_unannotated_seen_first']['verdict']!=r['caseA_annotated_seen_first']['verdict'],
            'caseB_orderDecidesAdmission':r['caseB_items_written_first']['verdict']!=r['caseB_addprops_written_first']['verdict'],
            'controlsDiscriminate':(r['control_unannotated_only']['verdict']=='REFUSE'
                                    and r['control_annotated_only']['verdict']=='ADMIT'),
            'allHypotheticalDocumentsMetaschemaValid':all(
                v['metaschemaValid'] for k,v in r.items() if not k.startswith('_'))}

pre,post=assess(rows['pre']),assess(rows['post'])
print(json.dumps({
 'standing':'actual Claude coauthor ADAPTATION of an INDEPENDENT REVIEWER construction, measured '
            'across PRE (frozen v10) and POST (disposable work copy); schema/reference evidence '
            'only, not a payload or Run attack, no acceptance and no product qualification',
 'reviewerSession':'4628c693-7a5e-4567-a1c8-e2f7ae322651',
 'reviewerVerdictNotInferred':True,
 'imageSha256':hashes,
 'pre':rows['pre'],'post':rows['post'],
 'preAssessment':pre,'postAssessment':post,
 'flippedFromAdmitToRefuse':sorted(k for k,v in rows['pre'].items()
                                   if not k.startswith('_') and v['verdict']=='ADMIT'
                                   and rows['post'][k]['verdict']=='REFUSE'),
 'verdict':('CLOSED: order no longer decides admission in either case, every hypothetical document '
            'is metaschema valid in both images, the controls still discriminate, and the shipped '
            'document has no same-path collision either way'
            if (pre['caseA_orderDecidesAdmission'] and pre['caseB_orderDecidesAdmission']
                and not post['caseA_orderDecidesAdmission'] and not post['caseB_orderDecidesAdmission']
                and post['controlsDiscriminate'] and post['allHypotheticalDocumentsMetaschemaValid'])
            else 'NOT AS EXPECTED: see the two tables')},indent=1))
