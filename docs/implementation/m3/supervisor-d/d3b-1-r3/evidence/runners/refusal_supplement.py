from pathlib import Path
import os,json,subprocess,tempfile,re
F=Path('/tmp/opensip-implementation/d3b1-full-takeover-r1');B=Path('/tmp/opensip-implementation/d3b1-refusal-supplement-r1');B.mkdir(exist_ok=False);assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1';os.setpriority(os.PRIO_PROCESS,0,10)
R='/opt/homebrew/Cellar/rust/1.95.0/bin/';T=Path(tempfile.mkdtemp(prefix='opensip-d3b1-refusal-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700)
E=dict(os.environ,PATH='/opt/homebrew/bin:'+R+':/usr/bin:/bin',CARGO_HOME='/Users/sb/.cargo',CARGO=R+'cargo',RUSTC=R+'rustc',TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip(),CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc')
rows=[]
for label,w in [('base',Path('/Users/sb/code/opensip-ai/opensip-d3b1-base-takeover')),('candidate',Path('/Users/sb/code/opensip-ai/opensip-d3b1-takeover'))]:
 artifacts=[json.loads(line) for line in (F/(label+'-build-artifacts.jsonl')).read_text().splitlines() if line.startswith('{')]
 found=[m for m in artifacts if m.get('reason')=='compiler-artifact' and m['target']['name']=='refusal_tests' and m.get('executable')];assert len(found)==1
 binary=found[0]['executable'];args=[binary,'--test-threads=1']
 with (B/(label+'.log')).open('wb') as log:r=subprocess.run(args,cwd=w,env=E,stdout=log,stderr=subprocess.STDOUT)
 out=(B/(label+'.log')).read_text(errors='replace');failed=sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$',out,re.M)));summary=re.findall(r'test result: (?:ok|FAILED)\. (\d+) passed; (\d+) failed; (\d+) ignored;',out);assert summary
 rows.append(dict(side=label,args=args,exitCode=r.returncode,passed=int(summary[-1][0]),failed=failed,ignored=int(summary[-1][2])));print(label,rows[-1],flush=True)
 (B/'checks.json').write_text(json.dumps(dict(reason='Correct direct harness environment: CARGO was missing from the first full-lane invocation. Those two setup failures are not classified as inherited product failures.',supersedesOnly=['base-refusal_tests','candidate-refusal_tests'],CARGO=E['CARGO'],RUSTC=E['RUSTC'],rows=rows,allPassed=all(x['exitCode']==0 for x in rows),privateTMPDIR=str(T),TMPDIRMode='0700',laneOwnedByThisProcess=True),indent=2)+'\n')
assert all(x['exitCode']==0 for x in rows)
