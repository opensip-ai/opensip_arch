"""Isolated proposal only; actual-Claude assessment and successor review still required."""
from pathlib import Path
import ast,hashlib,json,difflib
root=Path.cwd();out=Path('/tmp/opensip-design-corrections/v18-checker-proposal.v1');out.mkdir(exist_ok=False)
rel='docs/coop/design-corrections/workflows/check_workflows.v1.py';p=root/rel;s=p.read_text();tree=ast.parse(s);lines=s.splitlines(keepends=True);edits=[]
for n in ast.walk(tree):
 if not isinstance(n,ast.Compare) or not any(isinstance(x,ast.Attribute) and x.attr=='detail' for x in [n.left,*n.comparators]):continue
 gets=[c for c in ast.walk(n) if isinstance(c,ast.Call) and isinstance(c.func,ast.Attribute) and c.func.attr=='get' and c.args and isinstance(c.args[0],ast.Constant) and c.args[0].value in ('refusal','recoverRefusal')]
 if not gets:continue
 assert len(gets)==1 and n.lineno==n.end_lineno
 c=gets[0];key=c.args[0].value;owner=ast.get_source_segment(s,c.func.value);original=ast.get_source_segment(s,n);replacement=f"({key!r} in {owner} and {original})";edits.append({'line':n.lineno,'start':n.col_offset,'end':n.end_col_offset,'before':original,'after':replacement})
assert len(edits)==10
for e in sorted(edits,key=lambda e:(e['line'],e['start']),reverse=True):
 i=e['line']-1;assert lines[i][e['start']:e['end']]==e['before'];lines[i]=lines[i][:e['start']]+e['after']+lines[i][e['end']:]
t=''.join(lines);ast.parse(t);q=out/'proposal'/rel;q.parent.mkdir(parents=True);q.write_text(t);(out/'checker.before.py').write_text(s);(out/'checker.diff').write_text(''.join(difflib.unified_diff(s.splitlines(True),t.splitlines(True),fromfile='frozen17/'+rel,tofile='proposal18/'+rel)))
(out/'proposal.json').write_text(json.dumps({'standing':'Root isolated reference-checker correction proposal; live and frozen sources unchanged. Actual Claude substantive assessment pending.','path':rel,'beforeSha256':hashlib.sha256(s.encode()).hexdigest(),'afterSha256':hashlib.sha256(t.encode()).hexdigest(),'scope':'Every one of the ten nullable-detail exception comparisons now requires the expected-refusal key to exist. A deliberate explicit null remains supported. Existing detail/error-code/remedy checks are preserved. No product semantic/model/schema change.','edits':edits,'implementationAuthorized':False,'sourceIntegrated':False},indent=2)+'\n');print((out/'checker.diff').read_text())
