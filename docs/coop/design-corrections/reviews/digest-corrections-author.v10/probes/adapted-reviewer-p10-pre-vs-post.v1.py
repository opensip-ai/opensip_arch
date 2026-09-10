"""ADAPTATION of the ACTUAL INDEPENDENT REVIEWER's p10, run against PRE and POST source.

NOT my construction. Provenance: `/tmp/opensip-design-corrections/post-reset-review.v11/probes/
p10_typed_equality.py`, authored by the actual independent reviewer, session
cd236691-03ef-4863-b612-e7d8cdf0d3ad, captured verbatim at
`digest-corrections-author.v10/reviewer-p10-input/p10_typed_equality.py`
(sha256 9d4dc7350c470bac7ecebe0679ba06b7b6f7ea8137f9502541d997cdd00c4862) with its result
(24885358ace709d05d5152153524c2c1eaaf5ca020c5189cea61adca35e50437). Their conclusions are theirs and
their final review verdict does not exist yet; none is inferred.

Their script loads from `candidate-subject.v11` and prints to stdout. It is NOT executed here: the
vector builders and annotation constants are reproduced unchanged, and loading is redirected to my
own disposable images so nothing of theirs is read from or written to.

PRE is the frozen v11 identity-model.py (retained verbatim at PRE-identity-model.py) placed into a
copy of the work tree so the files it imports and root owns resolve; only the two owned files differ.
"""
import copy,hashlib,importlib.util,json
from pathlib import Path

V10=Path('/tmp/opensip-design-corrections/digest-corrections-author.v10')
IMAGES={'preFrozenV11':V10/'runs/pre-image/docs/coop/design-corrections/foundation/identity-model.py',
        'corrected':V10/'work/docs/coop/design-corrections/foundation/identity-model.py'}

# ---- reviewer's constants and builder, reproduced unchanged -------------------------------------
BARE={"$ref":"#/$defs/DigestHex"}
A_INT={"representation":"raw-artifact","retention":"not-joined",
       "authority":"probe","reason":"typed equality","ordinal":1}
A_BOOL=dict(A_INT,ordinal=True)
A_DIFF=dict(A_INT,authority="other-authority")

def load(label,path):
    spec=importlib.util.spec_from_file_location('p10_'+label,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def ref_chain(M,on_property,on_alias):
    d=copy.deepcopy(M.RELATION_DOCUMENT)
    d["$defs"]["RevAliasV1"]=dict(BARE,**{"x-opensip-digest":on_alias})
    d["$defs"]["FilePayloadV1"]["properties"]["rev"]={
        "$ref":"#/$defs/RevAliasV1","x-opensip-digest":on_property}
    return d

def measure(label,path):
    M=load(label,path);C=M.C;rows={}
    def verdict(document):
        try:
            M.relation_annotation_closure('file',document);return 'ADMIT'
        except Exception as exc:return str(exc).split(':')[0]
    vectors={'intOnProperty_boolOnAlias':(A_INT,A_BOOL),
             'boolOnProperty_intOnAlias':(A_BOOL,A_INT),
             'controlDisagreeingPair':(A_INT,A_DIFF),
             'controlIdenticalPair':(A_INT,dict(A_INT))}
    surviving={}
    for name,(a,b) in vectors.items():
        document=ref_chain(M,a,b)
        rows[name]=verdict(document)
        sight=[x for x in M.relation_digest_annotation_coverage(document)['sightings']
               if x['path']=='file.rev']
        surviving[name]={'count':len(sight[0]['annotations']) if sight else None,
                         'ordinals':[str(x.get('ordinal'))+'/'+type(x.get('ordinal')).__name__
                                     for x in sight[0]['annotations']] if sight else None}
    rows['_surviving']=surviving
    rows['_verdictsDifferByOrder']=(rows['intOnProperty_boolOnAlias']!=rows['boolOnProperty_intOnAlias'])
    rows['_pythonEqual']=A_INT==A_BOOL
    rows['_equalTyped']=C.equal_typed(A_INT,A_BOOL)
    rows['_annotationCanonicalDistinct']=C.canonical(A_INT)!=C.canonical(A_BOOL)
    return rows,hashlib.sha256(path.read_bytes()).hexdigest()

rows={};hashes={}
for label,path in IMAGES.items():rows[label],hashes[label]=measure(label,path)
pre,post=rows['preFrozenV11'],rows['corrected']
names=[k for k in pre if not k.startswith('_')]

print(json.dumps({
 'standing':'actual Claude coauthor ADAPTATION of an INDEPENDENT REVIEWER construction, measured '
            'across PRE (frozen v11) and POST (disposable work copy); hypothetical registered-schema '
            'and reference evidence only, NOT a payload or Run attack, no acceptance, no readiness '
            'and no product qualification',
 'reviewerSession':'cd236691-03ef-4863-b612-e7d8cdf0d3ad',
 'reviewerFinalVerdictNotInferred':True,
 'capturedInputsPreservedUnmodified':True,
 'imageSha256':hashes,
 'typedFacts':{'pythonEqual':post['_pythonEqual'],'equalTyped':post['_equalTyped'],
               'annotationCanonicalDistinct':post['_annotationCanonicalDistinct']},
 'pre':{k:pre[k] for k in names},'post':{k:post[k] for k in names},
 'preSurviving':pre['_surviving'],'postSurviving':post['_surviving'],
 'flippedFromAdmitToConflict':sorted(k for k in names
                                     if pre[k]=='ADMIT' and post[k]!='ADMIT'),
 'unchanged':sorted(k for k in names if pre[k]==post[k]),
 'verdict':('CLOSED: both typed-distinct orientations now conflict, BOTH annotations survive '
            'collection so the conflict limb can see them, the ordinary disagreeing control still '
            'conflicts and the identical control still admits'
            if (pre['intOnProperty_boolOnAlias']=='ADMIT' and pre['boolOnProperty_intOnAlias']=='ADMIT'
                and post['intOnProperty_boolOnAlias']=='RELATION_DIGEST_ANNOTATION_CONFLICT'
                and post['boolOnProperty_intOnAlias']=='RELATION_DIGEST_ANNOTATION_CONFLICT'
                and post['controlDisagreeingPair']=='RELATION_DIGEST_ANNOTATION_CONFLICT'
                and post['controlIdenticalPair']=='ADMIT'
                and all(v['count']==2 for k,v in post['_surviving'].items()
                        if k.endswith('OnAlias')))
            else 'NOT AS EXPECTED: see the two tables')},indent=1))
