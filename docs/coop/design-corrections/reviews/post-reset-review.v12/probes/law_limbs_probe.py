"""Independent (Claude v12) probe of the three law limbs, missingness, exemptions and controls."""
import copy,importlib.util,json,sys,os
ROOT='/tmp/opensip-design-corrections/candidate-subject.v12'
d=os.path.join(ROOT,'docs/coop/design-corrections/foundation')
sys.path.insert(0,d)
spec=importlib.util.spec_from_file_location('canonical',os.path.join(d,'canonical.py'))
C=importlib.util.module_from_spec(spec);sys.modules['canonical']=C;spec.loader.exec_module(C)
spec=importlib.util.spec_from_file_location('M',os.path.join(d,'identity-model.py'))
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
C=M.C  # HARNESS CORRECTION: the model binds its own canonical module; exception identity must match

R=[]
def case(name,fn,expect):
    try:
        fn(); got='ADMIT'
    except C.AdmissionError as e: got=str(e).split(':')[0]
    except Exception as e: got='ERR:'+type(e).__name__+':'+str(e)[:80]
    ok = (got==expect)
    R.append({'case':name,'expected':expect,'got':got,'ok':ok})
    return ok

def doc(): return copy.deepcopy(M.RELATION_DOCUMENT)
def sel(dd,rel='file'):
    row=dd['x-opensip-relation-registry']['relations'][rel]
    return dd['$defs'][row['selector'].split('/')[-1]]['properties'],row
def ann(**kw):
    b={'representation':'raw-artifact','retention':'not-joined','authority':'claude-probe',
       'reason':'reviewer probe control'}
    b.update(kw);return b

# ---- CONTROL: shipped document admits for every registered relation
case('control/all-13-registered-relations-admit',
     lambda: [M.relation_annotation_closure(n) for n in M.RELATIONS], 'ADMIT')

# ---- LIMB 1: unannotated governed field
def limb1():
    dd=doc();p,_=sel(dd)
    p['claudeUnannotated']={'$ref':'#/$defs/DigestHex'}   # governed form, no annotation
    M.relation_annotation_closure('file',dd)
case('limb1/unannotated-governed-field',limb1,'RELATION_DIGEST_UNANNOTATED')

# ---- LIMB 2: annotated governed field with no join and a JOINED retention
def limb2():
    dd=doc();p,_=sel(dd)
    p['claudeResidue']=dict({'$ref':'#/$defs/DigestHex'},
        **{'x-opensip-digest':ann(retention='preimage')})
    M.relation_annotation_closure('file',dd)
case('limb2/annotated-field-without-join',limb2,'RELATION_DIGEST_LAW_RESIDUE')

# ---- LIMB 3: join naming a field absent from the selector
def limb3():
    dd=doc();p,row=sel(dd)
    row['snapshotJoins'].append({'pathField':'claudeNoSuchField'})
    M.relation_annotation_closure('file',dd)
case('limb3/join-names-missing-field',limb3,'RELATION_JOIN_FIELD_UNKNOWN')

# ---- All three limbs share the SAME effective annotations: same injection via an ALIAS def
def limb1_alias():
    dd=doc();p,_=sel(dd)
    dd['$defs']['ClaudeBare']={'$ref':'#/$defs/DigestHex'}
    p['claudeUnannotated']={'$ref':'#/$defs/ClaudeBare'}
    M.relation_annotation_closure('file',dd)
case('limb1/via-alias-definition',limb1_alias,'RELATION_DIGEST_UNANNOTATED')
def limb2_alias():
    dd=doc();p,_=sel(dd)
    dd['$defs']['ClaudeAnn']=dict({'$ref':'#/$defs/DigestHex'},
        **{'x-opensip-digest':ann(retention='preimage')})
    p['claudeResidue']={'$ref':'#/$defs/ClaudeAnn'}
    M.relation_annotation_closure('file',dd)
case('limb2/via-alias-definition',limb2_alias,'RELATION_DIGEST_LAW_RESIDUE')
def limb1_branch():
    dd=doc();p,_=sel(dd)
    p['claudeUnannotated']={'oneOf':[{'$ref':'#/$defs/DigestHex'},{'type':'null'}]}
    M.relation_annotation_closure('file',dd)
case('limb1/via-nullable-branch',limb1_branch,'RELATION_DIGEST_UNANNOTATED')
def limb2_branch():
    dd=doc();p,_=sel(dd)
    p['claudeResidue']={'x-opensip-digest':ann(retention='preimage'),
                        'oneOf':[{'$ref':'#/$defs/DigestHex'},{'type':'null'}]}
    M.relation_annotation_closure('file',dd)
case('limb2/via-nullable-branch',limb2_branch,'RELATION_DIGEST_LAW_RESIDUE')

# ---- Invalid retention refuses
def badret():
    dd=doc();p,_=sel(dd)
    p['claudeProbe']=dict({'$ref':'#/$defs/DigestHex'},
        **{'x-opensip-digest':ann(retention='invented-retention')})
    M.relation_annotation_closure('file',dd)
case('retention/invented-value-refuses',badret,'RELATION_DIGEST_RETENTION')

# ---- not-joined exemption preserved (lawful, must ADMIT)
def notjoined():
    dd=doc();p,_=sel(dd)
    p['claudeProbe']=dict({'$ref':'#/$defs/DigestHex'},
        **{'x-opensip-digest':ann(retention='not-joined')})
    M.relation_annotation_closure('file',dd)
case('exemption/not-joined-still-admits',notjoined,'ADMIT')

# ---- Terminal governed def does NOT blanket-exempt: annotate the shared DigestHex def itself
def terminal():
    dd=doc();p,_=sel(dd)
    p['claudeUnannotated']={'$ref':'#/$defs/DigestHex'}
    # annotating the terminal def must not license every governed leaf everywhere
    dd['$defs']['DigestHex']=dict(dd['$defs']['DigestHex'],
        **{'x-opensip-digest':ann(retention='not-joined')})
    M.relation_annotation_closure('file',dd)
case('terminal-def-annotation/does-not-blanket-exempt',terminal,'RELATION_DIGEST_UNANNOTATED')

# ---- MONOTONIC MISSINGNESS: a third ANNOTATED sighting after a missing one must NOT cure it
def third_after_missing():
    dd=doc();p,_=sel(dd)
    dd['$defs']['ClaudeInnerM']={'type':'object',
        'properties':{'inner':{'$ref':'#/$defs/DigestHex'}}}                       # MISSING
    dd['$defs']['ClaudeMidM']={'$ref':'#/$defs/ClaudeInnerM',
        'properties':{'inner':dict({'$ref':'#/$defs/DigestHex'},
            **{'x-opensip-digest':ann()})}}                                        # annotated
    dd['$defs']['ClaudeOuterM']={'$ref':'#/$defs/ClaudeMidM',
        'properties':{'inner':dict({'$ref':'#/$defs/DigestHex'},
            **{'x-opensip-digest':ann()})}}                                        # annotated again
    p['claudeProbe']={'$ref':'#/$defs/ClaudeOuterM'}
    M.relation_annotation_closure('file',dd)
case('missingness/third-annotated-sighting-after-missing-still-refuses',
     third_after_missing,'RELATION_DIGEST_UNANNOTATED')

# ---- Top-level join addressing: nested/array locations must declare not-joined
def unjoinable():
    dd=doc();p,_=sel(dd)
    p['claudeProbe']={'type':'object',
        'properties':{'inner':dict({'$ref':'#/$defs/DigestHex'},
            **{'x-opensip-digest':ann(retention='preimage')})}}
    M.relation_annotation_closure('file',dd)
case('join-addressing/nested-member-cannot-be-joined',unjoinable,
     'RELATION_DIGEST_UNJOINABLE_LOCATION')

# ---- All-lawful annotations still admitted (identical annotations on both arrivals)
def lawful():
    dd=doc();p,_=sel(dd)
    a=ann()
    dd['$defs']['ClaudeAliasOK']=dict({'$ref':'#/$defs/DigestHex'},**{'x-opensip-digest':a})
    p['claudeProbe']=dict({'$ref':'#/$defs/ClaudeAliasOK'},**{'x-opensip-digest':copy.deepcopy(a)})
    M.relation_annotation_closure('file',dd)
case('control/identical-annotations-both-arrivals-admit',lawful,'ADMIT')

# ---- CYCLE: local-reference traversal must terminate
def cyclic_unannotated():
    dd=doc();p,_=sel(dd)
    dd['$defs']['ClaudeCycle']={'type':'object',
        'properties':{'self':{'$ref':'#/$defs/ClaudeCycle'},
                      'leaf':{'$ref':'#/$defs/DigestHex'}}}
    p['claudeProbe']={'$ref':'#/$defs/ClaudeCycle'}
    M.relation_annotation_closure('file',dd)
case('cycle/self-referential-container-terminates-and-refuses-when-unannotated',
     cyclic_unannotated,'RELATION_DIGEST_UNANNOTATED')
def cyclic_annotated():
    dd=doc();p,_=sel(dd)
    dd['$defs']['ClaudeCycle2']={'type':'object',
        'properties':{'self':{'$ref':'#/$defs/ClaudeCycle2'},
                      'leaf':dict({'$ref':'#/$defs/DigestHex'},
                          **{'x-opensip-digest':ann()})}}
    p['claudeProbe']={'$ref':'#/$defs/ClaudeCycle2'}
    M.relation_annotation_closure('file',dd)
case('cycle/self-referential-container-admits-when-annotated',cyclic_annotated,'ADMIT')
def mutual_cycle():
    dd=doc();p,_=sel(dd)
    dd['$defs']['ClaudeA']={'type':'object','properties':{'b':{'$ref':'#/$defs/ClaudeB'}}}
    dd['$defs']['ClaudeB']={'type':'object','properties':{'a':{'$ref':'#/$defs/ClaudeA'},
        'leaf':dict({'$ref':'#/$defs/DigestHex'},**{'x-opensip-digest':ann()})}}
    p['claudeProbe']={'$ref':'#/$defs/ClaudeA'}
    M.relation_annotation_closure('file',dd)
case('cycle/mutually-recursive-defs-terminate',mutual_cycle,'ADMIT')
def alias_only_cycle():
    dd=doc();p,_=sel(dd)
    dd['$defs']['ClaudeL1']={'$ref':'#/$defs/ClaudeL2'}
    dd['$defs']['ClaudeL2']={'$ref':'#/$defs/ClaudeL1'}
    p['claudeProbe']={'$ref':'#/$defs/ClaudeL1'}
    M.relation_annotation_closure('file',dd)
case('cycle/alias-only-cycle-terminates',alias_only_cycle,'ADMIT')

ok=sum(1 for r in R if r['ok'] is True)
print(json.dumps(R,indent=1))
print('CASES',len(R),'OK',ok,'NOT-OK',[r for r in R if r['ok'] is not True])
json.dump(R,open('/tmp/opensip-design-corrections/post-reset-review.v12/probes/law-limbs-result.json','w'),indent=1)
