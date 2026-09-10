"""Independent (Claude v12) probe of the typed-annotation-equality delta.

Constructed from scratch by this reviewer: my own document shapes, my own pair table, my own
oracle. Runs the SAME probe against the frozen v11 model and the frozen v12 model so that
discrimination is measured by pre/post source, not by counting checks or grepping the source.
"""
import copy,importlib.util,json,sys,os

def load(root):
    d=os.path.join(root,'docs/coop/design-corrections/foundation')
    sys.path.insert(0,d)
    for name,fn in (('canonical','canonical.py'),):
        spec=importlib.util.spec_from_file_location(name,os.path.join(d,fn))
        m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m)
    spec=importlib.util.spec_from_file_location('identity_model_'+os.path.basename(root),
                                                os.path.join(d,'identity-model.py'))
    M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
    sys.path.pop(0)
    return M

# My own typed-distinct pairs: canonically different JSON, but Python-equal.
PAIRS=[('int1-vs-true',1,True),
       ('int0-vs-false',0,False),
       ('obj-int-vs-bool',{'n':1},{'n':True}),
       ('arr-int-vs-bool',[1],[True]),
       ('deep-arr-in-obj',{'x':{'y':[0,1]}},{'x':{'y':[False,True]}}),
       ('mixed-depth3',{'a':[{'b':1}]},{'a':[{'b':True}]})]

def ann(v):
    return {'representation':'raw-artifact','retention':'not-joined',
            'authority':'claude-v12-probe','reason':'reviewer probe control','ordinal':v}

LOCATIONS=('direct-property-plus-alias','two-step-alias-chain','nullable-oneOf-branch',
           'enclosing-object-container','container-ref-overlay','same-path-double-arrival',
           'array-items-container')

def build(M,location,a_val,b_val):
    """Same governed leaf reached twice, one annotation per arrival."""
    doc=copy.deepcopy(M.RELATION_DOCUMENT)
    leaf={'$ref':'#/$defs/DigestHex'}
    A,B=ann(a_val),ann(b_val)
    props=doc['$defs']['FilePayloadV1']['properties']
    if location=='direct-property-plus-alias':
        doc['$defs']['ClaudeAliasA']=dict(leaf,**{'x-opensip-digest':B})
        props['claudeProbe']=dict({'$ref':'#/$defs/ClaudeAliasA'},**{'x-opensip-digest':A})
    elif location=='two-step-alias-chain':
        doc['$defs']['ClaudeAliasZ']=dict(leaf,**{'x-opensip-digest':B})
        doc['$defs']['ClaudeAliasY']=dict({'$ref':'#/$defs/ClaudeAliasZ'},**{'x-opensip-digest':A})
        props['claudeProbe']={'$ref':'#/$defs/ClaudeAliasY'}
    elif location=='nullable-oneOf-branch':
        props['claudeProbe']={'x-opensip-digest':A,
                              'oneOf':[dict(leaf,**{'x-opensip-digest':B}),{'type':'null'}]}
    elif location=='enclosing-object-container':
        props['claudeProbe']={'type':'object','x-opensip-digest':A,
                              'properties':{'inner':dict(leaf,**{'x-opensip-digest':B})}}
    elif location=='container-ref-overlay':
        doc['$defs']['ClaudeContainer']={'type':'object',
            'properties':{'inner':dict(leaf,**{'x-opensip-digest':B})}}
        props['claudeProbe']={'$ref':'#/$defs/ClaudeContainer',
                              'properties':{'inner':dict(leaf,**{'x-opensip-digest':A})}}
    elif location=='same-path-double-arrival':
        doc['$defs']['ClaudeInner']={'type':'object',
            'properties':{'inner':dict(leaf,**{'x-opensip-digest':B})}}
        doc['$defs']['ClaudeOuter']={'$ref':'#/$defs/ClaudeInner',
            'properties':{'inner':dict(leaf,**{'x-opensip-digest':A})}}
        props['claudeProbe']={'$ref':'#/$defs/ClaudeOuter'}
    elif location=='array-items-container':
        props['claudeProbe']={'type':'array','x-opensip-digest':A,
                              'items':dict(leaf,**{'x-opensip-digest':B})}
    return doc

def outcome(M,doc):
    """ADMIT, or the refusal cause."""
    try:
        r=M.relation_annotation_closure('file',doc)
        return 'ADMIT'
    except Exception as e:
        return str(e).split(':')[0] or type(e).__name__

def surviving(M,doc):
    try:
        s=M.relation_digest_annotation_coverage(doc)['byRelation']['file']['sightings']
        hits=[x for x in s if 'claudeProbe' in x['path']]
        return len(hits[0]['annotations']) if hits else None
    except Exception as e:
        return 'ERR:'+type(e).__name__

def run(root):
    M=load(root)
    out={'conflict':{},'positiveControl':{},'survivors':{}}
    for loc in LOCATIONS:
        for label,x,y in PAIRS:
            for orient in (0,1):
                a,b=(x,y) if orient==0 else (y,x)
                doc=build(M,loc,a,b)
                out['conflict']['%s|%s|%d'%(loc,label,orient)]=outcome(M,doc)
                out['survivors']['%s|%s|%d'%(loc,label,orient)]=surviving(M,doc)
            # positive control: identical typed annotations must remain usable (ADMIT)
            out['positiveControl']['%s|%s'%(loc,label)]=outcome(M,build(M,loc,x,x))
    return out

if __name__=='__main__':
    res={}
    for tag,root in [('v11','/tmp/opensip-design-corrections/candidate-subject.v11'),
                     ('v12','/tmp/opensip-design-corrections/candidate-subject.v12')]:
        res[tag]=run(root)
    disc=[]
    for k in res['v12']['conflict']:
        a,b=res['v11']['conflict'][k],res['v12']['conflict'][k]
        if a!=b: disc.append((k,a,b))
    print('total conflict cases',len(res['v12']['conflict']))
    print('v12 all conflict? ',all(v=='RELATION_DIGEST_ANNOTATION_CONFLICT' for v in res['v12']['conflict'].values()))
    from collections import Counter
    print('v12 outcomes',Counter(res['v12']['conflict'].values()))
    print('v11 outcomes',Counter(res['v11']['conflict'].values()))
    print('DISCRIMINATING (v11 != v12):',len(disc))
    locs=Counter(k.split('|')[0] for k,_,_ in disc)
    for k,v in sorted(locs.items()): print('   %-32s %d'%(k,v))
    print('positive controls v12 all ADMIT?',all(v=='ADMIT' for v in res['v12']['positiveControl'].values()))
    print('positive controls v12 outcomes',Counter(res['v12']['positiveControl'].values()))
    print('survivors v12 (should be 2 everywhere)',Counter(map(str,res['v12']['survivors'].values())))
    print('survivors v11',Counter(map(str,res['v11']['survivors'].values())))
    json.dump(res,open('/tmp/opensip-design-corrections/post-reset-review.v12/probes/typed-equality-result.json','w'),indent=1,default=str)
