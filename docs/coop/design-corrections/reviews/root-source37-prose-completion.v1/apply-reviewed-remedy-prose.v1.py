from pathlib import Path
import json,hashlib,difflib,ast,shutil
B=Path('/tmp/opensip-design-corrections');S=B/'consumer23-source-clarifications.v1/source';A=B/'claude-consumer23-source-author.v1';C=B/'claude-consumer23-remedy-reconciliation.v2';O=B/'root-source37-prose-completion.v1';L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews');h=lambda b:hashlib.sha256(b).hexdigest()
assert not O.exists()
for p in [A,C]:assert json.loads((p/'process-completion.json').read_bytes())['exitCode']==0 and not json.loads((p/'result.json').read_bytes())['is_error']
rows=json.loads((A/'after-manifest.json').read_bytes())['files'];original={}
for row in rows:
 b=(S/row['path']).read_bytes();assert h(b)==row['sha256'] and b==Path(row['image']).read_bytes();original[row['path']]=b
r=json.loads((C/'reconciliation.json').read_bytes());assert h((C/'recommended-edits.diff').read_bytes())=='8dd70655d6a5af584d629564e7cd0bd9f1623a788923671d512507bdbda9243e'
edits=[e for issue in r['issues'].values() for e in issue['recommendedEdits']];assert len(edits)==5;new={}
for e in edits:
 rel=e['file'];s=new.get(rel,original[rel].decode());assert s.count(e['anchor'])==1
 assert e['kind'] in ['replace','insert-after'];replacement=e['text'] if e['kind']=='replace' else e['anchor']+e['text'];new[rel]=s.replace(e['anchor'],replacement)
assert set(new)==set(r['recommendedEditsRehearsal']['files'])
for rel,s in new.items():
 if rel.endswith('.py'):ast.parse(s)
O.mkdir();measured=[]
for rel,s in new.items():
 for sub,raw in [('before',original[rel]),('after',s.encode())]:p=O/sub/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
 p=O/'diffs'/(rel+'.diff');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(''.join(difflib.unified_diff(original[rel].decode().splitlines(True),s.splitlines(True),fromfile='author/'+rel,tofile='root-completed/'+rel)))
 (S/rel).write_text(s);measured.append({'path':rel,'beforeSha256':h(original[rel]),'afterSha256':h(s.encode())})
assert h((S/'docs/coop/design-corrections/native/native-evidence.schemas.v2.json').read_bytes())=='3e37c7b7a6a620dcadc0aaed862eed242065ebd0ce9910da16faa25464f8b0b0'
record={'standing':'Root applied five exact reviewed Claude remedy recommendations to three assembly files after both authors completed. Prose/docstring only beyond completed six-file author changes; no schema mutation or acceptance.','sourceAssessmentSha256':h((C/'reconciliation.json').read_bytes()),'recommendedDiffSha256':h((C/'recommended-edits.diff').read_bytes()),'appliedEdits':5,'files':measured,'rootReadScope':'Whole reconciliation markdown, final-response and full recommended diff read; selected JSON and D9 reducer/composer/native/query owning clauses assessed.','limitations':['Final whole-source fresh acceptance and blind reconstruction pending','Host D9 reduction and stage-implied coverageId pairing remain explicitly outside this native helper; final source review must assess those owning boundaries','No product qualification or implementation authorization']};(O/'completion.json').write_text(json.dumps(record,indent=2)+'\n');shutil.copy2(Path(__file__),O/Path(__file__).name);shutil.copytree(O,L/O.name);print(json.dumps(record,indent=2))
