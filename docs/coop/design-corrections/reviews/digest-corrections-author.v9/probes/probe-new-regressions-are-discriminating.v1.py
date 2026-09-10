"""PROBE: are the new in-suite regressions DISCRIMINATING, or just more passing checks?

Root asked for pre/post comparison of the actual source rather than a corpus count. So each new
regression's construction is run against the FROZEN v10 model and against the corrected one, and the
outcomes are compared. A regression that behaves identically on both would not be evidence of
anything; the ones that flip are what shows the correction bites.

Constructions are the ones the suite ships, which for the two same-path pairs are the independent
reviewer's (session 4628c693-7a5e-4567-a1c8-e2f7ae322651), and for the three-at-one-path family are
mine.
"""
import copy,hashlib,importlib.util,json
from pathlib import Path

V9=Path('/tmp/opensip-design-corrections/digest-corrections-author.v9')
IMAGES={'frozenV10':V9/'runs/pre-image/docs/coop/design-corrections/foundation/identity-model.py',
        'corrected':V9/'work/docs/coop/design-corrections/foundation/identity-model.py'}
ANN={'representation':'raw-artifact','retention':'not-joined','authority':'test',
     'reason':'a control, not a shipped field'}
BARE={'$ref':'#/$defs/DigestHex'}

def load(label,path):
    spec=importlib.util.spec_from_file_location('disc_'+label,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def same_path_pair(M,order,shape):
    document=copy.deepcopy(M.RELATION_DOCUMENT)
    marked=dict(BARE,**{'x-opensip-digest':ANN})
    selector=document['$defs']['FilePayloadV1']['properties']
    if shape=='container':
        document['$defs']['ProbeContainerV1']={'type':'object','properties':{
            'leaf':BARE if order=='unannotated-first' else marked}}
        selector['probe']={'$ref':'#/$defs/ProbeContainerV1',
                           'properties':{'leaf':marked if order=='unannotated-first' else BARE}}
    else:
        selector['probe']=({'items':BARE,'additionalProperties':marked} if order=='unannotated-first'
                           else {'additionalProperties':marked,'items':BARE})
    return document

def three_with_missing(M,position):
    document=copy.deepcopy(M.RELATION_DOCUMENT)
    marked=dict(BARE,**{'x-opensip-digest':ANN})
    nodes=[marked,marked,dict(BARE)]
    nodes.insert(position,nodes.pop(2))
    document['$defs']['ProbeInnerV1']={'type':'object','properties':{'leaf':nodes[0]}}
    document['$defs']['ProbeOuterV1']={'$ref':'#/$defs/ProbeInnerV1','properties':{'leaf':nodes[1]}}
    document['$defs']['FilePayloadV1']['properties']['probe']={
        '$ref':'#/$defs/ProbeOuterV1','properties':{'leaf':nodes[2]}}
    return document

def three_all_annotated(M):
    document=copy.deepcopy(M.RELATION_DOCUMENT)
    marked=dict(BARE,**{'x-opensip-digest':ANN})
    document['$defs']['ProbeInnerV1']={'type':'object','properties':{'leaf':marked}}
    document['$defs']['ProbeOuterV1']={'$ref':'#/$defs/ProbeInnerV1','properties':{'leaf':marked}}
    document['$defs']['FilePayloadV1']['properties']['probe']={
        '$ref':'#/$defs/ProbeOuterV1','properties':{'leaf':marked}}
    return document

CASES=[('container-unannotated-first',lambda M:same_path_pair(M,'unannotated-first','container')),
       ('container-annotated-first',lambda M:same_path_pair(M,'annotated-first','container')),
       ('keyorder-unannotated-first',lambda M:same_path_pair(M,'unannotated-first','keyorder')),
       ('keyorder-annotated-first',lambda M:same_path_pair(M,'annotated-first','keyorder')),
       ('three-missing-at-0',lambda M:three_with_missing(M,0)),
       ('three-missing-at-1',lambda M:three_with_missing(M,1)),
       ('three-missing-at-2',lambda M:three_with_missing(M,2)),
       ('three-all-annotated-POSITIVE-CONTROL',three_all_annotated)]

def measure(label,path):
    M=load(label,path);rows={}
    for name,build in CASES:
        try:
            M.relation_annotation_closure('file',build(M));rows[name]='ADMIT'
        except Exception as exc:rows[name]=str(exc)
    rows['shippedDocumentCoherentForEveryRelation']=all(
        (lambda r:(lambda:True)())(r) for r in M.RELATIONS)
    ok={}
    for relation in sorted(M.RELATIONS):
        try:
            M.relation_annotation_closure(relation);ok[relation]='PASS'
        except Exception as exc:ok[relation]='REFUSED:'+str(exc)[:60]
    rows['shippedDocumentCoherentForEveryRelation']=sorted(set(ok.values()))
    return rows,hashlib.sha256(path.read_bytes()).hexdigest()

rows={};hashes={}
for label,path in IMAGES.items():rows[label],hashes[label]=measure(label,path)

discriminating=sorted(name for name,_ in CASES
                      if rows['frozenV10'][name]!=rows['corrected'][name])
identical=sorted(name for name,_ in CASES if rows['frozenV10'][name]==rows['corrected'][name])

print(json.dumps({
 'standing':'actual Claude coauthor pre/post measurement of the NEW regressions against the frozen '
            'v10 model and the corrected one; schema/reference evidence only, not a payload or Run '
            'attack, no acceptance and no product qualification',
 'imageSha256':hashes,
 'frozenV10':rows['frozenV10'],'corrected':rows['corrected'],
 'discriminating':discriminating,
 'identicalOnBoth':identical,
 'positiveControlAdmitsOnBoth':(rows['frozenV10']['three-all-annotated-POSITIVE-CONTROL']=='ADMIT'
                                and rows['corrected']['three-all-annotated-POSITIVE-CONTROL']=='ADMIT'),
 'note':'the two unannotated-FIRST vectors already refused on frozen v10, which is exactly why the '
        'defect was invisible to an order-blind test; they are retained as controls that the '
        'correction did not break the direction that already worked'},indent=1))
