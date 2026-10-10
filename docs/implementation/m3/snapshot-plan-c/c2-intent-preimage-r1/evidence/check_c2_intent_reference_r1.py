from pathlib import Path
import subprocess,os,json,hashlib
W=Path('/Users/sb/code/opensip-ai/opensip-c2-intent');B=Path('/tmp/opensip-implementation/c2-intent-checks-r1');A=W.parent/'opensip_arch';T=Path('/tmp/opensip-implementation/sm-stage-volume-2026-10-09');E=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null');os.setpriority(os.PRIO_PROCESS,0,10)
for k in ('GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE'):E.pop(k,None)
libs=list((W/'target/debug/deps').glob('libopensip_identity-*.rlib'));assert len(libs)==1,libs
subprocess.run(['/opt/homebrew/Cellar/rust/1.95.0/bin/rustc','--edition','2024',str(B/'bridge.rs'),'--extern','opensip_identity='+str(libs[0]),'-L','dependency='+str(W/'target/debug/deps'),'-o',str(B/'bridge')],env=E,check=True)
s=(A/'docs/coop/artifacts/check-c2.py').read_text();C={'__file__':str(A/'docs/coop/artifacts/check-c2.py'),'__name__':'reference'};exec(compile(s.split('\nif __name__')[0],C['__file__'],'exec'),C);contract=json.loads((A/'docs/coop/artifacts/c2-plan-stage-schema.v3.json').read_bytes())
p=T/'actual-plan-intent-v2/plan-intent.json';before=p.read_bytes();intent=json.loads(before);answer=subprocess.check_output([str(B/'bridge'),str(p)]).decode();expected=C['plan_intent_commitment'](intent,contract).removeprefix('sha256:');assert answer==expected;assert p.read_bytes()==before
vectors=[]
for n,value in enumerate([{'e\u0301':{'text':'e\u0301','items':[3,1,3]}},{'scalar':'𐀀','\ue000':'/\n\x01'},[True,None,-9223372036854775808]]):
 p=B/f'reference-vector-{n}.json';p.write_text(json.dumps(value,ensure_ascii=False));actual=subprocess.check_output([str(B/'bridge'),str(p)]).decode();want=hashlib.sha256(C['canonical_plan_intent'](value,contract)).hexdigest();assert actual==want;vectors.append(dict(case=n,sha256=actual))
(B/'reference-product.json').write_text(json.dumps(dict(actualFrozenIntentCommitment='sha256:'+answer,actualFrozenIntentUnchanged=True,referenceProductAgreement=True,nfcEscapeOrderingMultiplicityVectors=vectors,library=str(libs[0]),bareRustc=True,qualification=False),indent=2)+'\n');print('Actual frozen intent plus three independent NFC/escape/ordering vectors PASS')
