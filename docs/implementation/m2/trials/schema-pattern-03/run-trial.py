from pathlib import Path
import json,subprocess,re,itertools,random
B=Path('/tmp/opensip-implementation/m2-schema-pattern-trial-03');O=B.with_name('m2-schema-pattern-trial-02');mapping=json.loads((O/'adaptations.json').read_bytes());inverse={v:k for k,v in mapping.items()};assert len(inverse)==len(mapping)
cases=[{'pattern':inverse[c['pattern']],'text':c['text']} for c in (json.loads(line) for line in (O/'cases-adapted.jsonl').read_bytes().splitlines())]
patterns=sorted(mapping);texts=set()
for core in ['0.0.0','1.2.3','01.2.3','1.02.3','1.2.03','1.2','1.2.3.4','9'*130+'.0.0']:
 for pre in ['', '-0','-01','-a','-a.1','-a..b','-.','-a-1','--','-α']:
  for build in ['', '+0','+01','+a.b','+a..b','+.','+','+a+b']:texts.add(core+pre+build)
for pfx in ['DIRECTORY_CUSTODY:','MARKER_CUSTODY:Cargo.toml:','MARKER_CUSTODY:package.json:','ENFORCED-PLATFORM:','RP-DO-','#/$defs/','/','--']:
 for tail in ['','A','A_','A1','1','01','abc','a.b','a..b','a-b','A/B','a/..','DEPTH','😀','a'*64,'a'*65]:texts.add(pfx+tail)
for body in ['😀','é','e\u0301','a','.', '\n']:
 for n in [0,1,254,255,256,257]:texts.add(body*n);texts.add('x/'+body*n+'/z')
rng=random.Random(20260915)
for _ in range(1000):texts.add(''.join(rng.choices('aA01._-:/\\\n\r\0é😀',k=rng.randrange(0,25))))
cases += [{'pattern':p,'text':v} for p in patterns for v in sorted(texts)]
cargo='/opt/homebrew/Cellar/rust/1.95.0/bin/cargo';commands=[]
for name,cmd in [('build',[cargo,'build','--offline','--manifest-path',str(B/'probe/Cargo.toml')]),('clippy',[cargo,'clippy','--locked','--offline','--manifest-path',str(B/'probe/Cargo.toml'),'--','-D','warnings'])]:
 r=subprocess.run(cmd,capture_output=True,timeout=300);(B/(name+'.stdout')).write_bytes(r.stdout);(B/(name+'.stderr')).write_bytes(r.stderr);commands.append({'name':name,'command':cmd,'exitCode':r.returncode});assert r.returncode==0,(name,r.stderr.decode())
raw=''.join(json.dumps(c,ensure_ascii=True,separators=(',',':'))+'\n' for c in cases).encode();(B/'cases.jsonl').write_bytes(raw);expected=[bool(re.search(c['pattern'],c['text'])) for c in cases]
r=subprocess.run([str(B/'probe/target/debug/opensip-closed-pattern-trial')],input=raw,capture_output=True,timeout=180);(B/'probe.stdout').write_bytes(r.stdout);(B/'probe.stderr').write_bytes(r.stderr);assert r.returncode==0;actual=r.stdout.splitlines();assert len(actual)==len(cases)
mis=[{**c,'pythonReference':e,'closedRust':a.decode()} for c,e,a in zip(cases,expected,actual) if a==b'E' or (a==b'1')!=e];(B/'mismatches.json').write_text(json.dumps(mis,indent=2)+'\n')
unknown=[{'pattern':p,'text':'anything'} for p in ['', '.*','^.*$',patterns[0]+'x']];r=subprocess.run([str(B/'probe/target/debug/opensip-closed-pattern-trial')],input=''.join(json.dumps(c)+'\n' for c in unknown).encode(),capture_output=True,timeout=30);assert r.returncode==0 and r.stdout.splitlines()==[b'E']*4
result={'standing':'Exploratory closed pattern predicates; no product or schema runtime selection. Finite comparison is not complete schema or resource-budget proof.','patterns':len(patterns),'cases':len(cases),'mismatches':len(mis),'unknownPatternsRefused':4,'newExternalDependencies':0,'noHeapAllocationInMatcher':True,'commands':commands,'productChanged':False};(B/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert not mis,mis[:10]
