from pathlib import Path
import json,hashlib,os,re,subprocess,tempfile
W=Path('/Users/sb/code/opensip-ai/opensip-d3b1-takeover');A=W.parent/'opensip_arch';B=Path('/tmp/opensip-implementation/d3b1-final-proofs-r2');B.mkdir(exist_ok=False);assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1';os.setpriority(os.PRIO_PROCESS,0,10)
R='/opt/homebrew/Cellar/rust/1.95.0/bin/';PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14';T=Path(tempfile.mkdtemp(prefix='opensip-d3b1-proofs-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);E=dict(os.environ,TMPDIR=str(T));paths=subprocess.check_output(['git','diff','--name-only'],cwd=W,text=True).splitlines();fmt=[]
for path in paths:
 if not path.endswith('.rs'):continue
 base=subprocess.check_output(['git','show','HEAD:'+path],cwd=W);raw=(W/path).read_bytes()
 args=[R+'rustfmt','--edition','2024','--emit','stdout'];fmt.append(dict(path=path,baseClean=subprocess.check_output(args,input=base,env=E)==base,candidateClean=subprocess.check_output(args,input=raw,env=E)==raw))
assert all(r['baseClean'] and r['candidateClean'] for r in fmt)
source=(W/'tools/security/discovery_census.py').read_text();closure=set(re.findall(r"\('(crates/[^']+)', \d+, '[0-9a-f]{64}'\)",source));assert len(closure)>10 and not set(paths)&closure
rows=[]
for name,args in [('verify-design',[PY,'-I','-B','tools/verify_design.py','--architecture',str(A),'--implementation',str(W)]),('operability-source',[PY,'-I','-B','tools/check_operability.py','source','--repository',str(W)])]:
 with (B/(name+'.log')).open('wb') as out:r=subprocess.run(args,cwd=W,env=E,stdout=out,stderr=subprocess.STDOUT)
 rows.append(dict(name=name,exitCode=r.returncode));assert r.returncode==0
pins=json.loads(Path('/tmp/opensip-implementation/d3b1-final-candidate-r4/product-pins.json').read_text());assert pins==[dict(path=p,bytes=len((W/p).read_bytes()),sha256=hashlib.sha256((W/p).read_bytes()).hexdigest()) for p in paths]
(B/'checks.json').write_text(json.dumps(dict(allPassed=True,rows=rows,formatting=fmt,closureCount=len(closure),changedClosurePaths=[],dependencyManifestsChanged=[p for p in paths if p.endswith('Cargo.toml') or p=='Cargo.lock'],finalProductPins=pins,privateTMPDIR=str(T),TMPDIRMode='0700',laneOwnedByThisProcess=True,qualification=False),indent=2)+'\n');print('final source pins, formatting, closure and design/source checks pass')
