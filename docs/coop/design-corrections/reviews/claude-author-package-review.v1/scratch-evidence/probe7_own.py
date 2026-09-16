
import importlib.util,json,base64
from pathlib import Path
PKG=Path('/tmp/opensip-design-corrections/claude-return-review.v1/inputs/docs/coop/design-corrections/reviews/codex-author-followup.v2')
F=Path('/tmp/opensip-design-corrections/candidate-subject.v25/docs/coop/design-corrections/foundation')
s=importlib.util.spec_from_file_location('mi',F/'identity-model.v3.py');M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
def read(sub,name):
    d=json.loads((PKG/sub/(name+'.store.json')).read_text())
    claim=next(x for x in json.loads((PKG/sub/'claims.json').read_text()) if x['name']==name)
    o=d['objectTable'];b={k:base64.b64decode(v) for k,v in d['blobs'].items()}
    run=o[claim['runId']];e=o[run['evidenceId']]
    facts=[o[f] for v in e['viewIds'] for f in o[v]['facts']]
    return o,b,run,e,facts
res={}
for label,sub,name in [('lib','normalized-examples6','rust'),('bin','rust-selection-examples1','rust-bin'),('lib-only','rust-selection-examples1','rust-lib-only')]:
    o,b,run,e,facts=read(sub,name)
    f=[x for x in facts if x['relation']=='clones'][0]
    domains=next(k for k,v in M.DIGESTS['domainSets'].items() if 'native.semantic-universe.rust.v2' in v)
    _,u,_=M.parse_h_frame(b[f['sourceUniverse']],domains)
    own_id=u['sourceUnitOwnershipId'];hexd=own_id.split(':',1)[1]
    raw=b.get(hexd)
    print('===',label,'ownership',own_id[:26])
    if raw is None:
        print('   ownership preimage NOT retained in export blobs')
        res[label]=None;continue
    try:
        dom,payload,_=M.parse_h_frame(raw,None)
        print('   parsed domain:',dom)
    except Exception as ex:
        try:
            payload=json.loads(raw);print('   plain json')
        except Exception:
            print('   unparsable',str(ex)[:90]);res[label]=None;continue
    res[label]=payload
    print('   ',json.dumps(payload,sort_keys=True)[:700])
print()
print('=== ownership payload field diff ===')
avail={k:v for k,v in res.items() if v}
if len(avail)>1:
    keys=sorted(set(k for v in avail.values() for k in v))
    for k in keys:
        vals={lab:json.dumps(v.get(k),sort_keys=True) for lab,v in avail.items()}
        tag='DIFFERS' if len(set(vals.values()))>1 else 'same   '
        print(tag,k)
        if tag.startswith('DIFFERS'):
            for lab in avail: print('     ',lab,'=',vals[lab][:400])
