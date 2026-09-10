"""Independent (Claude v12) probe: 39 injections x 13 selectors, shapes, byteLength distinction,
previousPath not-joined exemption, and the 13 closed selectors' coherence."""
import copy,importlib.util,os,sys,json
d='/tmp/opensip-design-corrections/candidate-subject.v12/docs/coop/design-corrections/foundation'
spec=importlib.util.spec_from_file_location('M',os.path.join(d,'identity-model.py'))
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M);C=M.C
FORMS=('DigestHex','Sha256Text','CanonicalPath')
SHAPES=('ref','inline','nullable','aliased','nested','array','container-ref','cyclic-container-ref')
def ann(): return {'representation':'raw-artifact','retention':'not-joined',
                   'authority':'claude-probe','reason':'reviewer control'}
def inject(rel,form,annotate=False,shape='ref'):
    dd=copy.deepcopy(M.RELATION_DOCUMENT)
    selector=dd['$defs'][M.RELATIONS[rel]['selector'].split('/')[-1]]
    node={'ref':{'$ref':'#/$defs/'+form},
          'inline':dict(dd['$defs'][form]),
          'nullable':{'oneOf':[{'$ref':'#/$defs/'+form},{'type':'null'}]},
          'aliased':{'$ref':'#/$defs/CX_Alias'},
          'nested':{'type':'object','properties':{'inner':{'$ref':'#/$defs/'+form}}},
          'array':{'type':'array','items':{'$ref':'#/$defs/'+form}},
          'container-ref':{'$ref':'#/$defs/CX_Container'},
          'cyclic-container-ref':{'$ref':'#/$defs/CX_Cycle'}}[shape]
    if shape=='aliased':dd['$defs']['CX_Alias']={'$ref':'#/$defs/'+form}
    if shape=='container-ref':dd['$defs']['CX_Container']={'type':'object',
        'properties':{'hidden':{'$ref':'#/$defs/'+form}}}
    if shape=='cyclic-container-ref':dd['$defs']['CX_Cycle']={'type':'object',
        'properties':{'hidden':{'$ref':'#/$defs/'+form},'again':{'$ref':'#/$defs/CX_Cycle'}}}
    if annotate:node=dict(node,**{'x-opensip-digest':ann()})
    selector['properties']['cxStray']=node
    return M.relation_annotation_closure(rel,dd)
def outcome(fn):
    try: fn();return 'ADMIT'
    except C.AdmissionError as e: return str(e).split(':')[0]
res={}
# ---- 39 unannotated injections, all must refuse with UNANNOTATED cause
admitted=[];causes={}
for rel in sorted(M.RELATIONS):
    for f in FORMS:
        o=outcome(lambda r=rel,ff=f:inject(r,ff))
        causes[rel+'/'+f]=o
        if o=='ADMIT':admitted.append(rel+'/'+f)
res['injections_total']=len(causes)
res['injections_admitted']=admitted
res['injections_all_unannotated_cause']=all(v=='RELATION_DIGEST_UNANNOTATED' for v in causes.values())
res['selectors']=len(set(M.RELATIONS[r]['selector'] for r in M.RELATIONS))
res['relations']=len(M.RELATIONS)
# ---- positive control: same 39 injections annotated must ADMIT
res['injections_annotated_all_admit']=all(
    outcome(lambda r=rel,ff=f:inject(r,ff,annotate=True))=='ADMIT'
    for rel in sorted(M.RELATIONS) for f in FORMS)
# ---- shapes
res['shapes_refuse']={s:outcome(lambda ss=s:inject('file','CanonicalPath',shape=ss)) for s in SHAPES}
res['shapes_admit_when_annotated']={s:outcome(lambda ss=s:inject('file','CanonicalPath',annotate=True,shape=ss)) for s in SHAPES}
# ---- byteLength: ANNOTATED but NON-GOVERNED (refs UInt64). Removing its annotation must NOT
#      trigger third-limb refusal, unlike removing a governed field's annotation.
def strip(rel,field):
    dd=copy.deepcopy(M.RELATION_DOCUMENT)
    dd['$defs'][M.RELATIONS[rel]['selector'].split('/')[-1]]['properties'][field].pop('x-opensip-digest')
    return M.relation_annotation_closure(rel,dd)
res['byteLength_is_annotated']='x-opensip-digest' in M.RELATION_DOCUMENT['$defs']['FilePayloadV1']['properties']['byteLength']
res['byteLength_ref']=M.RELATION_DOCUMENT['$defs']['FilePayloadV1']['properties']['byteLength'].get('$ref')
res['strip_nongoverned_byteLength']=outcome(lambda:strip('file','byteLength'))
res['strip_governed_fields']={f:outcome(lambda ff=f:strip('file',ff)) for f in ('path','contentSha256')}
res['strip_governed_other']={ '%s.%s'%(r,f):outcome(lambda rr=r,ff=f:strip(rr,ff))
    for r,f in [('clones','bodyIdentity'),('clones','normalisationVersion'),
                ('package','manifestPath'),('vcs-change','path'),('vcs-change','previousPath')]}
# ---- previousPath not-joined exemption preserved
pp=M.RELATION_DOCUMENT['$defs'][M.RELATIONS['vcs-change']['selector'].split('/')[-1]]['properties']['previousPath']
res['previousPath_annotation']=pp.get('x-opensip-digest')
# ---- coverage sweep totals
cov=M.relation_digest_annotation_coverage()
res['coverage_total']=cov['total'];res['coverage_annotated']=cov['annotated']
res['coverage_unannotated']=cov['unannotated']
res['coverage_byRelation_annotated']={r:v['annotated'] for r,v in cov['byRelation'].items() if v['annotated']}
res['byteLength_seen_as_ungoverned_sighting']=any(
    s['path']=='file.byteLength' and s['form'] is None and s['annotations']
    for s in cov['byRelation']['file']['sightings'])
res['all_13_relations_admit']=all(M.relation_annotation_closure(n) is not None for n in M.RELATIONS)
print(json.dumps(res,indent=1))
json.dump(res,open('/tmp/opensip-design-corrections/post-reset-review.v12/probes/injection-result.json','w'),indent=1)
