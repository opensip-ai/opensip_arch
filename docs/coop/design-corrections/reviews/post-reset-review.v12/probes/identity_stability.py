"""Independent (Claude v12) probe: no unintended model/contract/schema change; identities stable."""
import importlib.util,os,sys,json,hashlib
def load(root):
    d=os.path.join(root,'docs/coop/design-corrections/foundation')
    spec=importlib.util.spec_from_file_location('M_'+os.path.basename(root),os.path.join(d,'identity-model.py'))
    M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
    return M,d
out={}
for tag,root in [('v11','/tmp/opensip-design-corrections/candidate-subject.v11'),
                 ('v12','/tmp/opensip-design-corrections/candidate-subject.v12')]:
    M,d=load(root)
    C=M.C
    o={}
    # registered documents / schemas: canonical digest of every schema JSON in foundation
    schemas={}
    for fn in sorted(os.listdir(d)):
        if fn.endswith('.json') and 'source-pins' not in fn and 'report' not in fn:
            schemas[fn]=hashlib.sha256(open(os.path.join(d,fn),'rb').read()).hexdigest()
    o['schemaFiles']=schemas
    # canonical digest of the registered relation document and the law
    o['relationDocumentCanonical']=hashlib.sha256(C.canonical(M.RELATION_DOCUMENT)).hexdigest()
    o['digestLawCanonical']=hashlib.sha256(C.canonical(M.RELATION_DOCUMENT['x-opensip-digest-law'])).hexdigest()
    o['registryCanonical']=hashlib.sha256(C.canonical(M.RELATION_DOCUMENT['x-opensip-relation-registry'])).hexdigest()
    o['relations']=sorted(M.RELATIONS)
    # closure rows for every relation
    o['closureRows']={n:hashlib.sha256(C.canonical(M.relation_annotation_closure(n))).hexdigest()
                      for n in sorted(M.RELATIONS)}
    # coverage sweep
    o['coverageCanonical']=hashlib.sha256(C.canonical(M.relation_digest_annotation_coverage())).hexdigest()
    out[tag]=o
diffs=[]
for k in out['v12']:
    if out['v11'].get(k)!=out['v12'][k]:
        diffs.append(k)
print('COMPARED KEYS',sorted(out['v12']))
print('DIFFERING KEYS',diffs)
for k in diffs:
    print('  v11',json.dumps(out['v11'].get(k))[:400])
    print('  v12',json.dumps(out['v12'][k])[:400])
print('schema files identical:',out['v11']['schemaFiles']==out['v12']['schemaFiles'],
      '(count %d)'%len(out['v12']['schemaFiles']))
print('relation document canonical identical:',out['v11']['relationDocumentCanonical']==out['v12']['relationDocumentCanonical'])
print('all closure rows identical:',out['v11']['closureRows']==out['v12']['closureRows'])
print('coverage identical:',out['v11']['coverageCanonical']==out['v12']['coverageCanonical'])
json.dump(out,open('/tmp/opensip-design-corrections/post-reset-review.v12/probes/identity-stability.json','w'),indent=1)
