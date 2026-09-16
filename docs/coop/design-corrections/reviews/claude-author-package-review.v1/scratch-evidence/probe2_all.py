
import importlib.util,json
from pathlib import Path
SRC=Path('/tmp/opensip-design-corrections/candidate-subject.v25')
PKG=Path('/tmp/opensip-design-corrections/claude-return-review.v1/inputs/docs/coop/design-corrections/reviews/codex-author-followup.v2')
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
CK=load('chk',PKG/'check-export.v4.py')
M=load('owner',SRC/'docs/coop/design-corrections/foundation/identity-model.v3.py')
groups=[('checkpoint3',['ts.store.json']),
 ('normalized-examples6',['rust.store.json','rust-partial.store.json','syntax-code.store.json','syntax-data.store.json']),
 ('rust-selection-examples1',['rust-bin.store.json','rust-lib-only.store.json'])]
for g,files in groups:
    claims=dict((c['path'],c['runId']) for c in json.loads((PKG/g/'claims.json').read_text()))
    for f in files:
        raw=(PKG/g/f).read_bytes()
        objects,blobs=CK.decode_store(raw,M,[])
        rid=claims[f];run=objects[rid][1]
        seal=objects[run['evaluationSealId']][1];proof=objects[seal['proofBundleId']][1]
        pps=proof['predicateProofs']
        scopes_in_store=[k for k in objects if k.startswith('scope2:')]
        ops=sorted(set(pp['operation'] for pp in pps))
        distinct=len(set(tuple(pp['scopeIds']) for pp in pps))
        sizes=sorted(set(len(pp['scopeIds']) for pp in pps))
        print(g+'/'+f)
        print('   predicates=',len(pps),'ops=',ops,'distinctScopeTuples=',distinct,'tupleSizes=',sizes,'scopeRecords=',len(scopes_in_store))
        print('   verdict=',proof['verdict'],'findings=',len(proof['findingIds']),'execDefs=',len(proof['executionDeficiencies']),'state=',proof['evaluationState'])
        for d in proof['executionDeficiencies']:
            print('     execdef',d['cause'],'cov',[r['digest'][:10] for r in d['inputRefs'] if r['domain']=='coverage'],'nc',d['nativeCause'])
        print('   rules:',[(r['ruleId'],r['outcome'],len(r['deficiencies'])) for r in proof['ruleResults']])
