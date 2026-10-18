from pathlib import Path
import os,subprocess,json,tempfile,re
B=Path('/tmp/opensip-implementation/d3b1-enforcement-baseline-r1');B.mkdir(exist_ok=False);assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1';os.setpriority(os.PRIO_PROCESS,0,10)
T=Path(tempfile.mkdtemp(prefix='opensip-d3b1-env-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);E=dict(os.environ,TMPDIR=str(T));rows=[]
for label,root in [('base','opensip-d3b1-base-takeover'),('candidate','opensip-d3b1-takeover')]:
 w=Path('/Users/sb/code/opensip-ai')/root
 args=['/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B','tools/tests/test_check_operability.py','-v']
 with (B/(label+'.log')).open('wb') as log:r=subprocess.run(args,cwd=w,env=E,stdout=log,stderr=subprocess.STDOUT)
 out=(B/(label+'.log')).read_text();failed=re.findall(r'^FAIL: (\S+)',out,re.M);rows.append(dict(side=label,exitCode=r.returncode,failed=failed));print(rows[-1],flush=True)
assert rows[0]['failed']==rows[1]['failed']==['test_this_worktree_matches_its_exception_list_and_lock']
(B/'checks.json').write_text(json.dumps(dict(rows=rows,equalFailureSets=True,standing='One pre-existing generated owner-label expectation mismatch, not introduced by D3b-1; not a whole-check pass.',privateTMPDIR=str(T),TMPDIRMode='0700',laneOwnedByThisProcess=True),indent=2)+'\n')
