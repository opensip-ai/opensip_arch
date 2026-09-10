"""ADAPTATION of the ACTUAL INDEPENDENT REVIEWER's p02, run against PRE and POST source.

NOT my construction. Provenance: the four vectors and two controls below are from
`/tmp/opensip-design-corrections/post-reset-review.v10/probes/p02_order_independence.py`, authored by
the actual independent reviewer, session 4628c693-7a5e-4567-a1c8-e2f7ae322651, captured verbatim at
`digest-corrections-author.v9/reviewer-p02-input/p02_order_independence.py`
(sha256 d1c85d61504a009bb5aa227b80d70da2f83aaa57c0037eb7eb537d8f0abdc92b) with its harness
(d390200e412f54748a4e6ec06fc0ef0f8a8c63e0ac8a5f34b8c9ed06375c78f9) and result
(f11079f282b8fec6142d0ba2965a161a58cc38dd7c7c22224295d9323fc4a993). Their conclusions are theirs.

Why this is an adaptation and not their script: theirs hardcodes the reviewer's own copy paths and
`harness.emit(...)` writes to `/tmp/opensip-design-corrections/post-reset-review.v10/work/p02.json`.
Running it would overwrite live review output. So the vector builders are reproduced unchanged and
the loading/emitting is replaced with my own disposable paths.

It measures PRE and POST so the cases are shown to be DISCRIMINATING, not merely counted. PRE is the
frozen v10 identity-model.py (kept verbatim at digest-corrections-author.v9/PRE-identity-model.py)
placed into a copy of the work tree at runs/pre-image/ so the files it imports and root owns
(canonical.py and the schema documents) resolve; only the two owned files differ between the images.
"""
import copy,hashlib,importlib.util,json
from pathlib import Path

V9=Path('/tmp/opensip-design-corrections/digest-corrections-author.v9')
WORK=V9/'work'
IMAGES={'pre':V9/'runs/pre-image/docs/coop/design-corrections/foundation/identity-model.py',
        'post':WORK/'docs/coop/design-corrections/foundation/identity-model.py'}
REL='file'
ANN={'representation':'raw-artifact','retention':'not-joined',
     'reason':'reviewer probe field, deliberately not joined'}

def load(label,path):
    spec=importlib.util.spec_from_file_location('p02_'+label,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def selector_of(doc,name):
    row=doc['x-opensip-relation-registry']['relations'][name]
    return doc['$defs'][row['selector'].split('/')[-1]]

# ---- reviewer's vector builders, reproduced unchanged --------------------------------------------
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

def c_only_unannotated(doc):
    selector_of(doc,REL)['properties']['probe']={'$ref':'#/$defs/DigestHex'}

def c_only_annotated(doc):
    selector_of(doc,REL)['properties']['probe']={'$ref':'#/$defs/DigestHex','x-opensip-digest':ANN}

VECTORS=[('caseA_unannotated_first',a_unannotated_first),('caseA_annotated_first',a_annotated_first),
         ('caseB_items_first',b_items_first),('caseB_addprops_first',b_addprops_first),
         ('control_only_unannotated',c_only_unannotated),('control_only_annotated',c_only_annotated)]

def measure(label,path):
    M=load(label,path);rows={}
    for name,build in VECTORS:
        doc=copy.deepcopy(M.RELATION_DOCUMENT);build(doc)
        try:
            M.relation_annotation_closure(REL,doc);rows[name]={'verdict':'ADMIT','cause':None}
        except Exception as exc:
            rows[name]={'verdict':'REFUSE','cause':type(exc).__name__+':'+str(exc)}
    return rows,hashlib.sha256(path.read_bytes()).hexdigest()

# Case B is a PURE JSON key-order swap: the two documents are canonically EQUAL, so any verdict
# difference is an implementation artifact and nothing else. Case A moves the annotation between the
# container and the local refinement, so those two documents genuinely differ - what must match there
# is the multiset of sightings at the path, not the bytes.
M=load('canon',IMAGES['post'])
def canonical_of(build):
    doc=copy.deepcopy(M.RELATION_DOCUMENT);build(doc)
    return M.C.canonical(selector_of(doc,REL)['properties']['probe'])
b_equal=canonical_of(b_items_first)==canonical_of(b_addprops_first)
a_equal=canonical_of(a_unannotated_first)==canonical_of(a_annotated_first)

rows={};hashes={}
for label,path in IMAGES.items():rows[label],hashes[label]=measure(label,path)

def assess(r):
    return {'caseA_orderDependent':r['caseA_unannotated_first']['verdict']!=r['caseA_annotated_first']['verdict'],
            'caseA_verdicts':[r['caseA_unannotated_first']['verdict'],r['caseA_annotated_first']['verdict']],
            'caseB_orderDependent':r['caseB_items_first']['verdict']!=r['caseB_addprops_first']['verdict'],
            'caseB_verdicts':[r['caseB_items_first']['verdict'],r['caseB_addprops_first']['verdict']],
            'controlsBehaveAsDeclared':(r['control_only_unannotated']['verdict']=='REFUSE'
                                        and r['control_only_annotated']['verdict']=='ADMIT')}

pre,post=assess(rows['pre']),assess(rows['post'])
print(json.dumps({
 'standing':'actual Claude coauthor ADAPTATION of an INDEPENDENT REVIEWER construction, measured '
            'across PRE (frozen v10) and POST (disposable work copy); schema/reference evidence '
            'only, not a payload or Run attack, no acceptance and no product qualification',
 'reviewerSession':'4628c693-7a5e-4567-a1c8-e2f7ae322651',
 'reviewerVerdictNotInferred':True,
 'capturedInputs':'digest-corrections-author.v9/reviewer-p02-input (verbatim, unmodified)',
 'imageSha256':hashes,
 'caseBIsCanonicallyIdentical':b_equal,
 'caseAIsAContainerPlacementChangeNotAKeyOrderSwap':not a_equal,
 'pre':rows['pre'],'post':rows['post'],
 'preAssessment':pre,'postAssessment':post,
 'flippedFromAdmitToRefuse':sorted(k for k in rows['pre']
                                   if rows['pre'][k]['verdict']=='ADMIT' and rows['post'][k]['verdict']=='REFUSE'),
 'unchanged':sorted(k for k in rows['pre'] if rows['pre'][k]['verdict']==rows['post'][k]['verdict']),
 'verdict':('CLOSED: both order-dependences are gone, the controls still behave, and the two '
            'annotated-first vectors flipped to REFUSE'
            if (pre['caseA_orderDependent'] and pre['caseB_orderDependent']
                and not post['caseA_orderDependent'] and not post['caseB_orderDependent']
                and post['controlsBehaveAsDeclared'])
            else 'NOT AS EXPECTED: see the two tables')},indent=1))
