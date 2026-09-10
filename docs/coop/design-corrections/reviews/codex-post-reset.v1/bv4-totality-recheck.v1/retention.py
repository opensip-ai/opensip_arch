from pathlib import Path
import json,hashlib,shutil
root=Path.cwd();dest=root/'docs/coop/design-corrections/reviews/codex-post-reset.v1/bv4-totality-recheck.v1'
assert not dest.exists()
src=Path('/tmp/opensip-design-corrections/bv4-totality-recheck.v1')
manifest=root/'docs/coop/design-corrections/reviews/candidate-subject.v13.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(manifest)=='8e6670f74d6e0bbed50b6c4914b3c7b29f627221f1591f4add5567f652f4c023'
m=json.loads(manifest.read_text());base={r['path']:r for r in m['files']}
same=[];changed=[];added=[];capture=[];actual=set()
for p in sorted((src/'work').rglob('*')):
 assert not p.is_symlink()
 if not p.is_file():continue
 rel=str(p.relative_to(src/'work'));actual.add(rel)
 row={'path':rel,'sha256':sha(p),'bytes':p.stat().st_size}
 old=base.get(rel)
 if old and all(row[k]==old[k] for k in ('sha256','bytes')):same.append(rel)
 else:
  row['beforeSha256']=old['sha256'] if old else None
  (changed if old else added).append(row);capture.append((p,Path('work')/rel))
deleted=sorted(set(base)-actual);assert not added and not deleted
for n in (1,2,3):
 d=Path('/tmp/opensip-design-corrections/bv4-totality-recheck.v'+str(n))
 for p in sorted(d.iterdir()):
  if p.is_file():capture.append((p,Path('attempt'+str(n))/p.name))
dest.mkdir();files=[]
for p,rel in capture:
 q=dest/rel;q.parent.mkdir(exist_ok=True,parents=True);h=sha(p);shutil.copyfile(p,q);assert sha(q)==h==sha(p)
 files.append({'path':str(rel),'sha256':h,'bytes':q.stat().st_size})
(dest/'source-copy-account.json').write_text(json.dumps({'baseManifestSha256':sha(manifest),'actualFiles':len(actual),'unchangedFiles':same,'changedFiles':changed,'addedFiles':added,'deletedFiles':deleted,'note':'Captured interim author source; integration-fixtures.py adapted by root from 54 named author fixture definitions. Before-image retained. No accepted repository source edited.'},indent=2)+'\n')
(dest/'assessment.json').write_text(json.dumps({'standing':'Actual root source review and selected complete-Run diagnostic; not independent acceptance, final-source assent or product qualification.','finding':'The interim coverage_inventory_totality guard filters relation/rung but ignores sourceUniverse/targetUniverse, allowing another universe in the same view to pay the complete file scope obligation.','caseResults':{'attempt1':'Valid base ADMIT; extra-scope cases StopIteration harness error because native H-frames live in blobs, not typed objects.','attempt2':'Valid base ADMIT; extra-scope cases properly REFUSE UNIVERSE_LANGUAGE_NOT_REQUESTED:syntax because the diagnostic omitted its request.','attempt3':'Added actual syntax-only inventory request and rekeyed Plan/stage. Valid base ADMIT; second complete scope with no own-universe file fact ADMIT counterexample; second scope with its own file fact ADMIT positive control.'},'requiredCorrection':'Match owning snapshot, relation/rung and both universe coordinates when deriving the totality obligation; preserve producer/view checks and two-universe valid control.','deliveredToClaude':'Exact three probe/report attempts copied to active coauthor codex-totality-recheck.v1; CODEX-PUBLIC-NOTE.md appended. Receipt/application not yet asserted.','files':files,'sourceCopyAccountSha256':sha(dest/'source-copy-account.json')},indent=2)+'\n')
shutil.copyfile(__file__,dest/'retention.py')
print(json.dumps({'files':len(files),'changedSourceFiles':len(changed),'unchanged':len(same),'retainedAt':str(dest)},indent=2))
