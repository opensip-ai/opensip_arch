"""Recheck root-selected admission cases on released, retained coauthor v2 bytes.
This is root coauthor assessment, not independent acceptance or qualification.
Run only after the final handoff and complete retention have been inspected.
"""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys
root=Path.cwd();scripts=Path(__file__).parent
src=Path('/tmp/opensip-design-corrections/bv4-corrections-author.v2')
ev=root/'docs/coop/design-corrections/reviews/bv4-corrections-author.v2'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert (ev/'custody.json').is_file(), 'Final retained coauthor evidence required'
assert sha(src/'handoff.json')==sha(ev/'handoff.json')
r=json.loads((src/'response.json').read_text());assert r['is_error'] is False
h=json.loads((ev/'handoff.json').read_text())
for row in h['delta']['aggregateVsFrozenV13']['changedFiles']:
 assert sha(src/'work'/row['path'])==row['afterSha256'],row['path']
out=Path('/tmp/opensip-design-corrections/bv4-final-source-recheck.v2');out.mkdir(exist_ok=False)
shutil.copytree(src/'work',out/'work')
before={str(p.relative_to(out/'work')):{'sha256':sha(p),'bytes':p.stat().st_size} for p in (out/'work').rglob('*') if p.is_file()}
(out/'copy-before.json').write_text(json.dumps(before,indent=2)+'\n')
commands=[]
for name,old_dir,new_dir in [
 ('probe-bv4-totality-v3.py','bv4-totality-recheck.v3','totality'),
 ('probe-bv4-derivation-v1.py','bv4-derivation-recheck.v1','derivation'),
 ('probe-bv4-request-v1.py','bv4-request-recheck.v1','request')]:
 s=(scripts/name).read_text()
 s=s.replace('/tmp/opensip-design-corrections/bv4-corrections-author.v1/work',str(src/'work'))
 s=s.replace('/tmp/opensip-design-corrections/bv4-totality-recheck.v1/work',str(out/'work'))
 s=s.replace('/tmp/opensip-design-corrections/'+old_dir,str(out/new_dir))
 s=s.replace('captured interim','released final').replace('Interim root diagnostic','Final-source root diagnostic').replace('interim coauthor','final coauthor').replace('interim author','final author')
 # This diagnostic itself cannot grant the final source assent that follows its assessment.
 p=out/name;p.write_text(s)
 with (out/(new_dir+'.stdout')).open('w') as stdout, (out/(new_dir+'.stderr')).open('w') as stderr:
  cmd=[sys.executable,'-I','-B',str(p)];res=subprocess.run(cmd,cwd=root,stdout=stdout,stderr=stderr)
 commands.append({'argv':cmd,'cwd':str(root),'exitCode':res.returncode,'scriptSha256':sha(p)})
 assert res.returncode==0, (name,res.returncode)
a=json.loads((out/'totality/report.json').read_text())['cases']
b=json.loads((out/'derivation/report.json').read_text())['cases']
c=json.loads((out/'request/report.json').read_text())['cases']
assert a[0]['outcome']=='ADMIT' and a[2]['outcome']=='ADMIT'
assert 'COVERAGE_INVENTORY_TOTALITY_OMITS_PATH' in a[1].get('error',''),a[1]
assert 'native.coverage-cause-relation-not-in-scope' in b[0].get('error','') and b[1]['outcome']=='ADMIT',b
assert c[0]['outcome']=='ADMIT',c[0]
assert any(e['coverage']=='unknown' and e['deficiency']=='language-tier-unsupported' and e['nativeCause']=='capability-missing' for e in c[0]['coverageEntries'])
after={str(p.relative_to(out/'work')):{'sha256':sha(p),'bytes':p.stat().st_size} for p in (out/'work').rglob('*') if p.is_file()}
assert before.keys()==after.keys()
delta=[{'path':rel,'before':before[rel],'after':v} for rel,v in after.items() if v!=before[rel]]
assert [r['path'] for r in delta]==['docs/coop/design-corrections/integration-fixtures.py'],delta
report={'standing':'Root final-source admission rechecks only. Synthetic author fixtures plus root mutations; no native execution, independent review, qualification or final source assent inferred. The three additional request relations reuse the references request and are not request/output bijection tests.',
 'coauthorHandoffSha256':sha(src/'handoff.json'),'commands':commands,'copyChanges':delta,
 'cases':{'totality':a,'derivation':b,'request':c}}
(out/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
shutil.copyfile(__file__,out/Path(__file__).name)
print(json.dumps({'out':str(out),'requiredControls':'PASS','copyChanges':len(delta)},indent=2))
