from pathlib import Path
import json,shutil,hashlib
r=Path.cwd();dc=r/'docs/coop/design-corrections';out=dc/'reviews/codex-post-reset.v1';tmp=Path('/tmp/opensip-design-corrections/codex-post-reset.v1');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert (dc/'historical-preservation-report.v12.json').is_file()
pinned_before={}
for unit,name,key in [('foundation','source-pins.v1.json','files'),('security','source-pins.v1.json','pins'),('native','source-pins.v2.json','pins'),('workflows','source-pins.v1.json','files')]:
 for row in json.loads((dc/unit/name).read_text())[key]:
  assert sha(r/row['path'])==row['sha256'],('Stale pin before final recording',row['path'])
  pinned_before[row['path']]=row['sha256']

checks=Path('/tmp/opensip-design-corrections/final-reference-v12');report=json.loads((checks/'reference-checks.json').read_text());assert report['passed']
dest=out/'final-reference.v12';assert not dest.exists();shutil.copytree(checks,dest)
for name in ['run-final-v12.py','adapt-integration-builder-v12.py','refresh-pins-v6.py','record-v12.py','finish-v12-records.py','prepare-v12-dispositions.py','update-crosswalk-v12.py','check-final-pins.py','freeze-next.py']:
 shutil.copyfile(tmp/name,dest/name)
for stem in ['annotation-traversal-final-v12','annotation-alias-final-v12','annotation-inherited-limbs-final-v12']:
 shutil.copyfile(Path('/tmp/opensip-design-corrections')/(stem+'.log'),dest/(stem+'.log'))
rows=[{'path':str(p.relative_to(dest)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(dest.rglob('*')) if p.is_file()];(dest/'custody.json').write_text(json.dumps({'standing':'Codex executed final-source commands and integration/recording scripts, not independent acceptance.','files':rows},indent=2)+'\n')
tech=(tmp/'technical-review.v12.prepared.md').read_text()
p=out/'technical-review.v12.md';assert not p.exists();p.write_text(tech)
p=dc/'README.md';old=p.read_text();p.write_text("""# Architecture corrections — v12 awaiting independent review

**Not ready for implementation.** Actual Claude and Codex corrected annotation comparisons to use typed canonical equality throughout collection and inheritance. Codex also corrected the record-update ordering that left two source pins stale in frozen v11. The [technical assessment](reviews/codex-post-reset.v1/technical-review.v12.md) records the actual findings, released source, six final rechecks and reproduced reference commands.

Frozen v11 remains a rejected historical candidate: its earlier working-state PASS reports did not reproduce after a later crosswalk update. That error and its original evidence are preserved. The successor must pass a final pin seal and receive fresh independent acceptance with zero unresolved MUST/SHOULD, a new blind consumer on the accepted normative bytes, and complete independently reviewed application/readiness reconciliation. No product implementation, commit or push is authorized. [The resume guide](reviews/NEXT-REVIEW.md) owns current status.

## Earlier progress — historical

"""+old)
assert all(sha(r/rel)==digest for rel,digest in pinned_before.items()), 'Final recording altered a pinned source; do not freeze'
print('V12 final evidence and truthful current status recorded; independent review remains required.')
