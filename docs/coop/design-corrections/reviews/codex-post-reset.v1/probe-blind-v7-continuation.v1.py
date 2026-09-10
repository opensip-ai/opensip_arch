"""Root-only diagnostic continuation of failing intermediate blind graphs.
NOT original blind evidence, NOT design changes, NOT final blind acceptance. No feedback supplied.
"""
from pathlib import Path
import json,hashlib,shutil,ast
base=Path('/tmp/opensip-design-corrections/codex-post-reset.v1');previous=base/'blind-v7-preliminary-admission.v1/work';out=base/'blind-v7-diagnostic-continuation.v1';assert not out.exists();out.mkdir();work=out/'work';shutil.copytree(previous,work);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=[]
for p in work.glob('*.py'):before.append({'path':p.name,'sha256':sha(p)})
p=work/'build.py';s=p.read_text();needle='    find_id, _ = kit.w.mint("finding", finding)';assert s.count(needle)==1;s=s.replace(needle,'    finding["evidenceRefs"] = sorted(finding["evidenceRefs"], key=C)\n'+needle);ast.parse(s);p.write_text(s)
p=work/'vec_syntax.py';s=p.read_text();needle='GRAMMAR_TREE = {';assert s.count(needle)==1;s=s.replace(needle,'GRAMMAR_TREE = {"bundle/manifest": b"grammar-bundle-manifest\\n", ');needle='("grammar:" + l).encode()';assert s.count(needle)==1;s=s.replace(needle,'GRAMMAR_TREE["grammars/" + l + ".bin"]');ast.parse(s);p.write_text(s)
(out/'root-diagnostic-changes.json').write_text(json.dumps({'standing':__doc__,'source':str(previous),'before':before,'after':[{'path':p.name,'sha256':sha(p)} for p in sorted(work.glob('*.py'))],'changes':['Sort finding evidenceRefs as canonical-set using chosen canonical encoding.','Use grammar bytes in declared closure and include bundle-manifest bytes in that closure.'],'noOriginalBlindSourcesChanged':True,'noFeedbackToBlindReviewer':True},indent=2)+'\n')
src=(base/'probe-blind-v7-current-graphs.v1.py').read_text();tail=src[src.index("mp=root/"):];head='''from pathlib import Path
import json,hashlib,sys,importlib.util,contextlib,io,traceback,datetime
root=Path('/Users/sb/code/opensip-ai/opensip_arch')
out=Path('/tmp/opensip-design-corrections/codex-post-reset.v1/blind-v7-diagnostic-continuation.v1')
work=out/'work'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=[{'path':p.name,'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(work.glob('*.py'))]
''';script='"""Root diagnostic variants only; not original blind graphs or final assessment."""\n'+head+tail;ast.parse(script);(out/'run.py').write_text(script)
print(out/'run.py')
