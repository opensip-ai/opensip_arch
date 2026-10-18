"""Conservative D3b-1 structural guard: scan every tracked and unignored
candidate Rust source in components/src and platform/src, including tests.
No source is excluded based on its name or a guessed cfg expression. This
is a lexical absence check, not a Rust reachability or Linux qualification.
"""
from pathlib import Path
import json,os,re,subprocess,sys
root=Path(sys.argv[1]).resolve();env=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for key in ('GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE'):env.pop(key,None)
paths=set()
for extra in ([],['--others','--exclude-standard']):
 paths.update(subprocess.check_output(['/usr/bin/git','ls-files',*extra,'--','crates/components/src','crates/platform/src'],cwd=root,env=env,text=True).splitlines())
pattern=re.compile('|'.join(re.escape(x) for x in ['c'+'group','CLONE_INTO_'+'CGROUP','clone'+'3']),re.I)
findings=[];scanned=[]
for path in sorted(paths):
 if not path.endswith('.rs'):continue
 scanned.append(path)
 for line,text in enumerate((root/path).read_text().splitlines(),1):
  if pattern.search(text):findings.append(dict(path=path,line=line))
print(json.dumps(dict(passed=not findings,scanned=scanned,excludedFiles=[],testFilesIncluded=True,findings=findings,qualification=False),indent=2))
sys.exit(bool(findings))
