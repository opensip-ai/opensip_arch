"""Independent (Claude v12) probe: each normative sentence treated as a falsifiable claim."""
import copy,importlib.util,os,sys,json,itertools
d='/tmp/opensip-design-corrections/candidate-subject.v12/docs/coop/design-corrections/foundation'
spec=importlib.util.spec_from_file_location('M',os.path.join(d,'identity-model.py'))
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M);C=M.C
R=[]
def case(claim,name,fn,expect):
    try: fn();got='ADMIT'
    except C.AdmissionError as e: got=str(e).split(':')[0]
    except Exception as e: got='ERR:'+type(e).__name__
    R.append({'proseClaim':claim,'case':name,'expected':expect,'got':got,'ok':got==expect})
def doc(): return copy.deepcopy(M.RELATION_DOCUMENT)
def props(dd,rel='file'):
    return dd['$defs'][M.RELATIONS[rel]['selector'].split('/')[-1]]['properties']
def ann(**kw):
    b={'representation':'raw-artifact','retention':'not-joined','authority':'claude',
       'reason':'reviewer control'};b.update(kw);return b

# CLAIM: "Directly annotated top-level selector properties remain subject to retention and join
# checks even when their scalar form is not one of these three." (byteLength refs UInt64)
def bl_bad_retention():
    dd=doc();props(dd)['byteLength']=dict(props(dd)['byteLength'],
        **{'x-opensip-digest':ann(retention='not-a-real-retention')})
    M.relation_annotation_closure('file',dd)
case('direct-non-governed-annotation-subject-to-retention','byteLength/invalid-retention',
     bl_bad_retention,'RELATION_DIGEST_RETENTION')
def bl_no_join():
    dd=doc();props(dd)['byteLength']=dict(props(dd)['byteLength'],
        **{'x-opensip-digest':ann(retention='preimage')})
    dd['x-opensip-relation-registry']['relations']['file']['snapshotJoins'][0].pop('lengthField')
    M.relation_annotation_closure('file',dd)
case('direct-non-governed-annotation-subject-to-join','byteLength/joined-retention-without-join',
     bl_no_join,'RELATION_DIGEST_LAW_RESIDUE')
# and a NON-top-level non-governed annotated member must NOT be dragged in
def nested_nongoverned():
    dd=doc();props(dd)['cxNested']={'type':'object',
        'properties':{'inner':dict({'$ref':'#/$defs/UInt64'},**{'x-opensip-digest':ann()})}}
    M.relation_annotation_closure('file',dd)
case('non-governed-nested-member-is-not-a-governed-occurrence','nested-nongoverned-annotated',
     nested_nongoverned,'ADMIT')

# CLAIM: "An annotated alternative does not cover an unannotated alternative"
def branch_isolation(order):
    dd=doc()
    alts=[dict({'$ref':'#/$defs/DigestHex'},**{'x-opensip-digest':ann()}),
          {'$ref':'#/$defs/Sha256Text'}]           # second alternative UNANNOTATED
    props(dd)['cxProbe']={'oneOf':alts if order==0 else list(reversed(alts))}
    M.relation_annotation_closure('file',dd)
for o in (0,1):
    case('annotated-alternative-does-not-cover-unannotated','branch-isolation-order-%d'%o,
         lambda oo=o:branch_isolation(oo),'RELATION_DIGEST_UNANNOTATED')
# CLAIM: "a parent annotation may cover each alternative it encloses"
def parent_covers():
    dd=doc()
    props(dd)['cxProbe']={'x-opensip-digest':ann(),
        'oneOf':[{'$ref':'#/$defs/DigestHex'},{'$ref':'#/$defs/Sha256Text'}]}
    M.relation_annotation_closure('file',dd)
case('parent-annotation-covers-each-alternative','parent-covers-both',parent_covers,'ADMIT')

# CLAIM: "Object-key order and the order in which these paths are visited must not change admission."
def key_order(perm):
    dd=doc()
    node={'x-opensip-digest':ann(),'type':'object',
          'properties':{'a':{'$ref':'#/$defs/DigestHex'},'b':{'$ref':'#/$defs/Sha256Text'}}}
    node={k:node[k] for k in perm}
    props(dd)['cxProbe']=node
    M.relation_annotation_closure('file',dd)
_keys=['x-opensip-digest','type','properties']
_outs=set()
for perm in itertools.permutations(_keys):
    try: key_order(perm);_outs.add('ADMIT')
    except C.AdmissionError as e:_outs.add(str(e).split(':')[0])
R.append({'proseClaim':'object-key-order-must-not-change-admission','case':'6-key-permutations',
          'expected':'single-outcome','got':sorted(_outs),'ok':len(_outs)==1})

# CLAIM: "Later annotated occurrences cannot undo that absence" - both visit orders
def missing_then_annotated(order):
    dd=doc()
    miss={'type':'object','properties':{'inner':{'$ref':'#/$defs/DigestHex'}}}
    anno={'type':'object','properties':{'inner':dict({'$ref':'#/$defs/DigestHex'},
        **{'x-opensip-digest':ann()})}}
    dd['$defs']['CX_1']=miss if order==0 else anno
    dd['$defs']['CX_2']=dict((anno if order==0 else miss),**{'$ref':'#/$defs/CX_1'})
    props(dd)['cxProbe']={'$ref':'#/$defs/CX_2'}
    M.relation_annotation_closure('file',dd)
for o in (0,1):
    case('later-annotated-occurrence-cannot-undo-absence','missing-annotated-order-%d'%o,
         lambda oo=o:missing_then_annotated(oo),'RELATION_DIGEST_UNANNOTATED')

# CLAIM: "It cannot claim a joinable retention that the current join vocabulary cannot address."
def nested_claims_joinable():
    dd=doc()
    props(dd)['cxProbe']={'type':'object','properties':{'inner':dict({'$ref':'#/$defs/DigestHex'},
        **{'x-opensip-digest':ann(retention='snapshot-inventoried')})}}
    M.relation_annotation_closure('file',dd)
case('nested-cannot-claim-joinable-retention','nested-claims-snapshot-inventoried',
     nested_claims_joinable,'RELATION_DIGEST_UNJOINABLE_LOCATION')
# scalar alternative of a top-level property PRESERVES the address
def scalar_alt_joinable():
    dd=doc()
    p=props(dd)
    p['path']={'x-opensip-digest':p['path']['x-opensip-digest'],
               'oneOf':[{'$ref':'#/$defs/CanonicalPath'},{'type':'null'}]}
    M.relation_annotation_closure('file',dd)
case('scalar-alternative-preserves-join-address','path-as-nullable-alternative',
     scalar_alt_joinable,'ADMIT')

# CLAIM: exemption reason is a READER obligation; admission checks declared retention only
def exempt_no_reason():
    dd=doc()
    a=ann();a.pop('reason')
    props(dd)['cxProbe']=dict({'$ref':'#/$defs/DigestHex'},**{'x-opensip-digest':a})
    M.relation_annotation_closure('file',dd)
case('admission-checks-declared-retention-not-prose','not-joined-without-reason-text',
     exempt_no_reason,'ADMIT')
def exempt_empty_reason():
    dd=doc()
    props(dd)['cxProbe']=dict({'$ref':'#/$defs/DigestHex'},**{'x-opensip-digest':ann(reason='')})
    M.relation_annotation_closure('file',dd)
case('admission-checks-declared-retention-not-prose','not-joined-with-empty-reason',
     exempt_empty_reason,'ADMIT')
# no new reason KEY is invented by the law
law=M.RELATION_DOCUMENT['x-opensip-digest-law']
R.append({'proseClaim':'no-new-reason-key-invented','case':'law-retention-vocabulary',
          'expected':['not-joined','preimage','provider-output-retained','snapshot-inventoried'],
          'got':sorted(law['retention']),
          'ok':sorted(law['retention'])==['not-joined','preimage','provider-output-retained','snapshot-inventoried']})

ok=sum(1 for r in R if r['ok'])
print(json.dumps(R,indent=1))
print('CASES',len(R),'OK',ok,'FAILED',[r['case'] for r in R if not r['ok']])
json.dump(R,open('/tmp/opensip-design-corrections/post-reset-review.v12/probes/prose-claims-result.json','w'),indent=1)
