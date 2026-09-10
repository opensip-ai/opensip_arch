"""Every prior counterexample class, measured on frozen v11 AND the corrected model.

Root's instruction was to preserve all of them. Measuring both images rather than only the corrected
one is what shows the typed-equality change altered NOTHING except the typed-distinct pair.
"""
import copy,hashlib,importlib.util,json
from pathlib import Path

V10=Path('/tmp/opensip-design-corrections/digest-corrections-author.v10')
IMAGES={'preFrozenV11':V10/'runs/pre-image/docs/coop/design-corrections/foundation/identity-model.py',
        'corrected':V10/'work/docs/coop/design-corrections/foundation/identity-model.py'}
ANN={'representation':'raw-artifact','retention':'not-joined','authority':'test','reason':'control'}
BARE={'$ref':'#/$defs/DigestHex'}

def load(label,path):
    spec=importlib.util.spec_from_file_location('prior_'+label,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def measure(label,path):
    M=load(label,path);out={}
    def verdict(document,relation='file'):
        try:
            M.relation_annotation_closure(relation,document);return 'ADMIT'
        except Exception as exc:return str(exc).split(':')[0]

    admitted=[]
    for relation in sorted(M.RELATIONS):
        selector=M.RELATIONS[relation]['selector'].split('/')[-1]
        for form in ('DigestHex','CanonicalPath','Sha256Text'):
            d=copy.deepcopy(M.RELATION_DOCUMENT)
            d['$defs'][selector]['properties']['stray']={'$ref':'#/$defs/'+form}
            if verdict(d,relation)=='ADMIT':admitted.append(relation+'/'+form)
    out['prior39InjectionsAdmitted']=admitted

    nine={}
    for loc in ('field','alias','branch'):
        for ret in ('preimage','invented-retention','not-joined'):
            d=copy.deepcopy(M.RELATION_DOCUMENT);d['$defs']['ProbeAlias']={'$ref':'#/$defs/DigestHex'}
            a=dict(ANN,retention=ret);f={'$ref':'#/$defs/ProbeAlias'}
            if loc=='field':f['x-opensip-digest']=a
            elif loc=='alias':d['$defs']['ProbeAlias']['x-opensip-digest']=a
            else:f={'oneOf':[{'type':'null'},dict(BARE,**{'x-opensip-digest':a})]}
            d['$defs']['FilePayloadV1']['properties']['stray']=f
            nine[loc+'-'+ret]=verdict(d)
    out['inheritedLimbNineVectors']=nine

    def location(where):
        d=copy.deepcopy(M.RELATION_DOCUMENT);d['$defs']['StrayAliasV1']={'$ref':'#/$defs/DigestHex'}
        d['$defs']['FilePayloadV1']['properties']['stray']={'$ref':'#/$defs/StrayAliasV1'}
        if where=='field':d['$defs']['FilePayloadV1']['properties']['stray']['x-opensip-digest']=ANN
        if where=='alias':d['$defs']['StrayAliasV1']['x-opensip-digest']=ANN
        if where=='terminal':d['$defs']['DigestHex']=dict(d['$defs']['DigestHex'],**{'x-opensip-digest':ANN})
        return verdict(d)
    out['annotationLocations']={w:location(w) for w in ('nowhere','field','alias','terminal')}

    def same_path(order,shape):
        d=copy.deepcopy(M.RELATION_DOCUMENT);marked=dict(BARE,**{'x-opensip-digest':ANN})
        selector=d['$defs']['FilePayloadV1']['properties']
        if shape=='container':
            d['$defs']['ProbeContainerV1']={'type':'object','properties':{
                'leaf':BARE if order=='unannotated-first' else marked}}
            selector['probe']={'$ref':'#/$defs/ProbeContainerV1',
                               'properties':{'leaf':marked if order=='unannotated-first' else BARE}}
        else:
            selector['probe']=({'items':BARE,'additionalProperties':marked} if order=='unannotated-first'
                               else {'additionalProperties':marked,'items':BARE})
        return verdict(d)
    out['samePathOrderIndependence']={s+'/'+o:same_path(o,s) for s in ('container','keyorder')
                                      for o in ('unannotated-first','annotated-first')}

    def three(position):
        d=copy.deepcopy(M.RELATION_DOCUMENT);marked=dict(BARE,**{'x-opensip-digest':ANN})
        nodes=[marked,marked,dict(BARE)];nodes.insert(position,nodes.pop(2))
        d['$defs']['ProbeInnerV1']={'type':'object','properties':{'leaf':nodes[0]}}
        d['$defs']['ProbeOuterV1']={'$ref':'#/$defs/ProbeInnerV1','properties':{'leaf':nodes[1]}}
        d['$defs']['FilePayloadV1']['properties']['probe']={
            '$ref':'#/$defs/ProbeOuterV1','properties':{'leaf':nodes[2]}}
        return verdict(d)
    out['monotonicMissingness']={'missing-at-'+str(p):three(p) for p in (0,1,2)}

    def unjoinable(shape,retention):
        d=copy.deepcopy(M.RELATION_DOCUMENT)
        inner=dict(BARE,**{'x-opensip-digest':dict(ANN,retention=retention)})
        d['$defs']['FilePayloadV1']['properties']['stray']=(
            {'type':'object','additionalProperties':False,'required':['inner'],'properties':{'inner':inner}}
            if shape=='nested' else {'type':'array','items':inner})
        return verdict(d)
    out['topLevelJoinAddressing']={s+'/'+r:unjoinable(s,r) for s in ('nested','array')
                                   for r in ('preimage','not-joined')}

    out['previousPathRetention']=M.RELATION_DOCUMENT['$defs']['VcsChangePayloadV1'][
        'properties']['previousPath']['x-opensip-digest']['retention']
    coverage=M.relation_digest_annotation_coverage()
    out['shippedCoverage']={k:coverage[k] for k in ('total','annotated','unannotated')}
    out['shippedCoherentEveryRelation']=sorted({verdict(copy.deepcopy(M.RELATION_DOCUMENT),r)
                                                for r in M.RELATIONS})
    return out,hashlib.sha256(path.read_bytes()).hexdigest()

rows={};hashes={}
for label,path in IMAGES.items():rows[label],hashes[label]=measure(label,path)
differing=[k for k in rows['preFrozenV11'] if rows['preFrozenV11'][k]!=rows['corrected'][k]]
print(json.dumps({
 'standing':'actual Claude coauthor measurement of every prior counterexample class across frozen '
            'v11 and the corrected model; schema/reference evidence only, no acceptance',
 'imageSha256':hashes,
 'preFrozenV11':rows['preFrozenV11'],'corrected':rows['corrected'],
 'classesDifferingBetweenTheImages':differing,
 'verdict':('PRESERVED: every prior class is identical on both images; the typed-equality change '
            'altered nothing except the typed-distinct pair measured separately'
            if not differing else 'A PRIOR CLASS MOVED: see classesDifferingBetweenTheImages')},indent=1))
