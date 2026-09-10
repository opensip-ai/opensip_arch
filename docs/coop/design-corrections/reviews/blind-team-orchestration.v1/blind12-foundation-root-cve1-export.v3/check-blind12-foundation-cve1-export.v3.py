from pathlib import Path
import importlib.util,json,hashlib,shutil
B=Path('/tmp/opensip-design-corrections');S=B/'candidate-subject.v24';F=S/'docs/coop/design-corrections/foundation/identity-model.v3.py'
s=importlib.util.spec_from_file_location('root_cve1_selected_owner',F);M=importlib.util.module_from_spec(s);s.loader.exec_module(M);N=M.native_admission()
p=B/'consumer-b.v12-team-foundation-corrections.v1/output/foundation/cve1-eight-types.json';j=json.loads(p.read_text());rows=[]
for i,r in enumerate(j['vectors']):
    hx=r.get('committedBytesHex',r.get('hex'))
    if hx is None:continue
    raw=bytes.fromhex(hx);decoded=N.cve1_decode(raw);encoded=N.cve1_encode(r['decoded']) if 'decoded' in r else N.cve1_encode(dict(reversed(list(decoded.items()))));reencoded=N.cve1_encode(decoded)
    ok=(M.C.equal_typed(decoded,r['decoded']) if 'decoded' in r else True) and encoded==raw and reencoded==raw and len(raw)==r.get('byteLength',len(raw))
    rows.append({'index':i,'kind':r['inputKind'],'passed':ok,'explicitDecodedValueCompared':'decoded' in r,'byteLength':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
assert len(rows)==16
report={'standing':'Actual frozen owner decode/encode of all retained positive CVE1 vectors, not whole-consumer admission; no root results supplied to blind team.','inputSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'ownerSha256':hashlib.sha256(F.read_bytes()).hexdigest(),'nativeOwnerPath':str(N.__file__),'nativeOwnerSha256':hashlib.sha256(Path(N.__file__).read_bytes()).hexdigest(),'checks':rows,'passed':all(r['passed']for r in rows),'limitations':'Root adapter v2 expected a decoded field on the key-order-only vector and stopped with KeyError before producing a report; this v3 checks 15 explicit decoded values and 16 canonical round trips, reversing decoded map insertion order for the key-order vector. Negative source inputs are not present as raw encoded bytes in this CVE1 artifact; their helper execution not rerun here. Does not validate capability manifest field admission or complete graph.'}
o=B/'blind12-foundation-root-cve1-export.v3';o.mkdir();shutil.copy2(p,o/p.name);shutil.copy2(Path(__file__),o/Path(__file__).name);(o/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'count':len(rows),'passed':report['passed']}));assert report['passed']
