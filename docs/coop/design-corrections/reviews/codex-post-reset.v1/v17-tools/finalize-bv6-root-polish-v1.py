"""Finalize the prepared proposal; initial AST check counted a changed docstring as behavior."""
from pathlib import Path
import ast,difflib,hashlib,json
base=Path('/tmp/opensip-design-corrections');old=base/'bv6-corrections-author.v3';out=base/'bv6-root-final-polish.v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=json.loads((old/'handoff.json').read_text());rows=[]
class StripDoc(ast.NodeTransformer):
 def generic_visit(self,node):
  super().generic_visit(node)
  if isinstance(node,(ast.Module,ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and node.body and isinstance(node.body[0],ast.Expr) and isinstance(node.body[0].value,ast.Constant) and isinstance(node.body[0].value.value,str):node.body=node.body[1:]
  return node
def behavior(p):return ast.dump(StripDoc().visit(ast.parse(p.read_text())))
for r in h['changedSource']['files']:
 rel=r['path'];a=old/'work'/rel;p=out/'work'/rel;assert sha(a)==r['v3Sha256']
 if sha(p)!=sha(a):
  if p.name=='workflows_model.v1.py':assert behavior(a)==behavior(p)
  q=out/'delta'/(str(len(rows)).zfill(2)+'-'+p.name+'.diff');diff=''.join(difflib.unified_diff(a.read_text().splitlines(True),p.read_text().splitlines(True),fromfile='finalv3/'+rel,tofile='root-polish/'+rel))
  if q.exists():assert q.read_text()==diff
  else:q.write_text(diff)
  rows.append({'path':rel,'beforeSha256':sha(a),'afterSha256':sha(p),'diff':str(q.relative_to(out)),'diffSha256':sha(q)})
assert len(rows)==5
p=out/'proposal.json';assert not p.exists();p.write_text(json.dumps({'standing':'Root-authored remaining copies of already agreed receipt/projection/precision laws. Exact Claude substantive review pending. No integration.','finalV3HandoffSha256':sha(old/'handoff.json'),'files':rows,'behavioralScope':'Model AST unchanged after removing docstrings (docstring/comment clarification only); one prose-substring check removed. Other changes reconcile documents and state existing lossy projection limitations. No new payload field, operation, permission, retry or capability.','initialAttempt':'prepare-bv6-root-polish-v1.py completed all5edits then failed its overbroad AST assertion because that assertion counted a docstring. Source/failedscript preserved; this finalizer strips only docstrings for the executable-AST comparison.','requiredReview':'Claude must substantively assess exact source/deltas and may disagree; no assent presumed.'},indent=2)+'\n');print(json.dumps({'out':str(out),'files':rows},indent=1))
