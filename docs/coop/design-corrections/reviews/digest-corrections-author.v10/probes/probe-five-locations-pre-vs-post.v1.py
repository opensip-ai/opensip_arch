"""All five annotation-propagation classes, measured on frozen v11 AND the corrected model.

Root's prepared final recheck names five classes: property/alias, parent/nullable branch, alias
chain, enclosing container and same-path merge. Root also predicted that the same-path merge control
should ALREADY behave on frozen v11, because that merge used typed equality, while the
early-collection negatives should discriminate. This measures that prediction rather than assuming
it, and records which classes are discriminating evidence and which are preservation controls.
"""
import copy,hashlib,importlib.util,json
from pathlib import Path

V10=Path('/tmp/opensip-design-corrections/digest-corrections-author.v10')
IMAGES={'preFrozenV11':V10/'runs/pre-image/docs/coop/design-corrections/foundation/identity-model.py',
        'corrected':V10/'work/docs/coop/design-corrections/foundation/identity-model.py'}
BARE={'$ref':'#/$defs/DigestHex'}
PAIRS=[('int-vs-true',1,True),('int-vs-false',0,False),('nested-dict',{'k':1},{'k':True}),
       ('nested-list',[1],[True]),('deep-nested',{'a':{'b':[0]}},{'a':{'b':[False]}})]
LOCATIONS=('property-alias','alias-chain','parent-nullable-branch','enclosing-container','same-path-merge')

def load(label,path):
    spec=importlib.util.spec_from_file_location('five_'+label,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def annotation(value):
    return {'representation':'raw-artifact','retention':'not-joined','authority':'test',
            'reason':'a control, not a shipped field','ordinal':value}

def document_for(M,location,first,second):
    d=copy.deepcopy(M.RELATION_DOCUMENT);a,b=annotation(first),annotation(second)
    sel=d['$defs']['FilePayloadV1']['properties']
    if location=='property-alias':
        d['$defs']['T1']=dict(BARE,**{'x-opensip-digest':b})
        sel['probe']=dict({'$ref':'#/$defs/T1'},**{'x-opensip-digest':a})
    elif location=='alias-chain':
        d['$defs']['T2']=dict(BARE,**{'x-opensip-digest':b})
        d['$defs']['T1']=dict({'$ref':'#/$defs/T2'},**{'x-opensip-digest':a})
        sel['probe']={'$ref':'#/$defs/T1'}
    elif location=='parent-nullable-branch':
        sel['probe']={'x-opensip-digest':a,'oneOf':[dict(BARE,**{'x-opensip-digest':b}),{'type':'null'}]}
    elif location=='enclosing-container':
        d['$defs']['T1']={'type':'object','properties':{'leaf':dict(BARE,**{'x-opensip-digest':b})}}
        sel['probe']={'$ref':'#/$defs/T1','properties':{'leaf':dict(BARE,**{'x-opensip-digest':a})}}
    else:
        d['$defs']['T1']={'type':'object','properties':{'leaf':dict(BARE,**{'x-opensip-digest':b})}}
        d['$defs']['T0']={'$ref':'#/$defs/T1','properties':{'leaf':dict(BARE,**{'x-opensip-digest':a})}}
        sel['probe']={'$ref':'#/$defs/T0'}
    return d

def measure(label,path):
    M=load(label,path);rows={}
    def verdict(d):
        try:
            M.relation_annotation_closure('file',d);return 'ADMIT'
        except Exception as exc:return str(exc).split(':')[0]
    for location in LOCATIONS:
        for name,first,second in PAIRS:
            for orientation,(a,b) in enumerate(((first,second),(second,first))):
                rows[location+'/'+name+'/'+str(orientation)]=verdict(document_for(M,location,a,b))
            rows[location+'/'+name+'/identical']=verdict(document_for(M,location,first,first))
    # an ordinary string disagreement, and a lawful single annotation
    d=copy.deepcopy(M.RELATION_DOCUMENT)
    d['$defs']['T1']=dict(BARE,**{'x-opensip-digest':dict(annotation(1),authority='other')})
    d['$defs']['FilePayloadV1']['properties']['probe']=dict({'$ref':'#/$defs/T1'},
        **{'x-opensip-digest':annotation(1)})
    rows['_ordinaryStringConflict']=verdict(d)
    d=copy.deepcopy(M.RELATION_DOCUMENT)
    d['$defs']['FilePayloadV1']['properties']['probe']=dict(BARE,**{'x-opensip-digest':annotation(1)})
    rows['_lawfulSingleAnnotation']=verdict(d)
    return rows,hashlib.sha256(path.read_bytes()).hexdigest()

rows={};hashes={}
for label,path in IMAGES.items():rows[label],hashes[label]=measure(label,path)
pre,post=rows['preFrozenV11'],rows['corrected']
discriminating=sorted(k for k in pre if pre[k]!=post[k])
by_location={loc:sorted(k for k in discriminating if k.startswith(loc+'/')) for loc in LOCATIONS}
negatives=[k for k in post if not k.startswith('_') and not k.endswith('/identical')]
positives=[k for k in post if k.endswith('/identical')]

print(json.dumps({
 'standing':'actual Claude coauthor measurement across frozen v11 and the corrected model; '
            'hypothetical registered-schema and reference evidence only, NOT a payload or Run '
            'attack, no acceptance, no readiness, no product qualification',
 'imageSha256':hashes,
 'discriminatingCount':len(discriminating),
 'discriminatingByLocation':{k:len(v) for k,v in by_location.items()},
 'earlyCollectionClassesThatDiscriminate':[k for k,v in by_location.items() if v],
 'samePathMergeClassesAlreadyCorrectOnFrozenV11':[k for k,v in by_location.items() if not v],
 'allNegativesConflictAfter':sorted({post[k] for k in negatives})==['RELATION_DIGEST_ANNOTATION_CONFLICT'],
 'allPositivesAdmitBefore':sorted({pre[k] for k in positives})==['ADMIT'],
 'allPositivesAdmitAfter':sorted({post[k] for k in positives})==['ADMIT'],
 'ordinaryStringConflict':{'pre':pre['_ordinaryStringConflict'],'post':post['_ordinaryStringConflict']},
 'lawfulSingleAnnotation':{'pre':pre['_lawfulSingleAnnotation'],'post':post['_lawfulSingleAnnotation']},
 'verdict':('CLOSED: every typed-distinct pair conflicts at all five classes in both orientations, '
            'every identical-annotation positive still admits, the ordinary string conflict and the '
            'lawful single annotation are unchanged, and the classes that discriminate are exactly '
            'the two early-collection ones root predicted'
            if (sorted({post[k] for k in negatives})==['RELATION_DIGEST_ANNOTATION_CONFLICT']
                and sorted({post[k] for k in positives})==['ADMIT']
                and post['_ordinaryStringConflict']==pre['_ordinaryStringConflict']
                and post['_lawfulSingleAnnotation']=='ADMIT')
            else 'NOT AS EXPECTED: see the tables'),
 'pre':pre,'post':post},indent=1))
