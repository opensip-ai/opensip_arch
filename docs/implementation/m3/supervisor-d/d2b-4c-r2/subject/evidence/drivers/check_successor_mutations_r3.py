from pathlib import Path
import os,json,hashlib,subprocess,tempfile,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'successor-mutations-r3';B.mkdir();W=Path('/Users/sb/code/opensip-ai/opensip-rust3-successor-takeover');R='/opt/homebrew/Cellar/rust/1.95.0/bin/'
T=Path(tempfile.mkdtemp(prefix='n-',dir=subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip()));T.chmod(0o700);os.setpriority(os.PRIO_PROCESS,0,10)
E=dict(os.environ,CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(F/'target'),TMPDIR=str(T),CC='/usr/bin/cc',CXX='/usr/bin/c++',AR='/usr/bin/ar',CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER='/usr/bin/cc',SDKROOT=subprocess.check_output(['/usr/bin/xcrun','--show-sdk-path'],text=True).strip())
sha=lambda b:hashlib.sha256(b).hexdigest();prefix='crates/components/src/provider_protocol/rust3/'
mutations=[dict(name='census-token-defers-nonsymbol-echoes',path=prefix+'receive.rs',old='self.context.symbol_census.is_some() && self.law.census.is_symbol(&k.relation);',new='self.census_token;',test='successor_participant_census_token_never_defers_nonsymbol_counts_or_scope')]

paths=sorted(subprocess.check_output(['git','ls-files','-m','-o','--exclude-standard'],cwd=W,text=True).splitlines());pins=[dict(path=p,bytes=(W/p).stat().st_size,sha256=sha((W/p).read_bytes()))for p in paths]
originals={m['path']:(W/m['path']).read_bytes()for m in mutations};report=dict(standing='UNACCEPTED candidate freshcompiled runtime guard mutations; no unit review or qualification',sourcePins=pins,runs=[],allKilled=False,sourceRestored=False)
def save():(B/'report.json').write_text(json.dumps(report,indent=2)+'\n')
try:
 for m in mutations:
  assert all((W/p).read_bytes()==b for p,b in originals.items());source=W/m['path'];original=originals[m['path']];assert original.count(m['old'].encode())==1;changed=original.replace(m['old'].encode(),m['new'].encode());source.write_bytes(changed);D=B/m['name'];D.mkdir();(D/'mutated-source.rs').write_bytes(changed)
  c=subprocess.run([R+'cargo','test','--locked','--offline','-p','opensip-components','--lib','--no-run','--message-format=json'],cwd=W,env=E,capture_output=True);(D/'artifacts.jsonl').write_bytes(c.stdout);(D/'build.log').write_bytes(c.stderr);assert c.returncode==0
  rows=[j for l in c.stdout.splitlines()if l.startswith(b'{')and(j:=json.loads(l)).get('reason')=='compiler-artifact'and j.get('executable')and j['target']['name']=='opensip_components'];assert len(rows)==1 and not rows[0]['fresh'];binary=Path(rows[0]['executable'])
  c=subprocess.run([str(binary),m['test'],'--nocapture'],cwd=W,env=E,capture_output=True);log=c.stdout+c.stderr;(D/'tests.log').write_bytes(log);text=log.decode(errors='replace');failures=re.findall(r'^test (.+) \.\.\. FAILED$',text,re.M)
  run=dict(name=m['name'],sourcePath=m['path'],originalSourceSha256=sha(original),mutantSourceSha256=sha(changed),binary=str(binary),binarySha256=sha(binary.read_bytes()),freshlyCompiled=True,exitCode=c.returncode,failureSet=failures,summaries=re.findall(r'^test result:.*$',text,re.M),killed=c.returncode!=0 and len(failures)==1 and m['test'] in failures[0]);report['runs'].append(run);save();assert run['killed'];source.write_bytes(original)
finally:
 for p,b in originals.items():(W/p).write_bytes(b)
 report['sourceRestored']=all((W/p).read_bytes()==b for p,b in originals.items());save()
assert report['sourceRestored'] and all(sha((W/p['path']).read_bytes())==p['sha256']for p in pins);report['allKilled']=len(report['runs'])==1 and all(r['killed']for r in report['runs']);save();assert report['allKilled'];print('Nonsymbol-scope freshcompiled runtime mutant KILLED; exact sources restored. Restored full candidate suites still required.')
