from pathlib import Path
import json,hashlib,shutil
base=Path(__file__).resolve().parent;capture=base/'required-findings-before.v1';assert not capture.exists();capture.mkdir()
rels=['files/docs/coop/design-corrections/finalize-application.v1.py','check-finalizer.py','launch-application-review.py','verify-applied.py','prepare-validation.py','freeze-application.py','assemble-records.py']
for rel in rels:
 p=capture/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(base/rel,p)
p=base/rels[0];s=p.read_text();needle="    assert review['verdict'] == 'ACCEPT', 'Independent application ACCEPT required'\n";assert needle in s
s=s.replace(needle,needle+"    for key in ('newMustIssues', 'newShouldIssues'):\n        assert isinstance(review.get(key), list) and not review[key], 'Unresolved or unaccounted required application findings: ' + key\n");p.write_text(s)
p=base/'check-finalizer.py';s=p.read_text();s=s.replace("'verdict':verdict,'subjectManifestSha256':mh","'verdict':verdict,'subjectManifestSha256':mh,'newMustIssues':[],'newShouldIssues':[]")
needle="negative('changes-required-is-never-application-authority',altered_verdict)\n";assert needle in s
s=s.replace(needle,needle+'''def required_findings(a,key,value,remove=False):
 d=json.loads(a[4].read_text())
 if remove:d.pop(key)
 else:d[key]=value
 a[4].write_text(json.dumps(d));a[5]=sha(a[4]);(a[0]/'docs/review.json').write_bytes(a[4].read_bytes())
for key in ('newMustIssues','newShouldIssues'):
 negative('ACCEPT-with-unresolved-'+key+'-refuses-without-writes',lambda a,key=key:required_findings(a,key,[{'id':'synthetic-required-finding'}]))
 negative('ACCEPT-with-unaccounted-'+key+'-refuses-without-writes',lambda a,key=key:required_findings(a,key,None,True))
 negative('ACCEPT-with-mistyped-'+key+'-refuses-without-writes',lambda a,key=key:required_findings(a,key,{}))
''');p.write_text(s)
p=base/'launch-application-review.py';s=p.read_text();s=s.replace('ACCEPT requires no unresolved MUST/SHOULD application/design issue.','ACCEPT requires no unresolved MUST/SHOULD application/design issue. Include top-level newMustIssues and newShouldIssues arrays, both empty for ACCEPT; an absent or malformed account is not application authority.');p.write_text(s)
p=base/'verify-applied.py';s=p.read_text();needle="assert review['verdict']=='ACCEPT' and review['subjectManifestSha256']==activation['applicationManifest']['sha256']\n";assert needle in s;s=s.replace(needle,needle+"assert all(isinstance(review.get(k),list) and not review[k] for k in ('newMustIssues','newShouldIssues'))\n");p.write_text(s)
p=base/'freeze-application.py';s=p.read_text();needle="    assert sha(actual) == record['sha256'] and result.get('verdict', result.get('overallVerdict')) == verdict\n";assert needle in s;s=s.replace(needle,needle+"    assert all(isinstance(result.get(k), list) and not result[k] for k in ('newMustIssues', 'newShouldIssues')), 'Required prerequisite findings unresolved or unaccounted'\n");p.write_text(s)
p=base/'assemble-records.py';s=p.read_text();s=s.replace("assert not design.get('newMustIssues') and not design.get('newShouldIssues'), 'Unresolved required design findings remain'","assert all(isinstance(design.get(k),list) and not design[k] for k in ('newMustIssues','newShouldIssues')), 'Unresolved or unaccounted required design findings remain'");p.write_text(s)
p=base/'prepare-validation.py';s=p.read_text();s=s.replace("'legacy-current-before.json','legacy-preapplication-provenance.v1.json'","'legacy-current-before.json','legacy-preapplication-provenance.v1.json','harden-required-findings.v1.py','required-findings-hardening.v1.json','required-findings-selftest.v1.json'")
needle="finalizer=files/(dc+'finalize-application.v1.py')";assert needle in s;s=s.replace(needle,"shutil.copytree(Path(__file__).with_name('required-findings-before.v1'),support/'required-findings-before.v1')\n"+needle);p.write_text(s)
rows=[]
for rel in rels:
 p=base/rel;compile(p.read_text(),str(p),'exec');rows.append({'path':rel,'beforeSha256':hashlib.sha256((capture/rel).read_bytes()).hexdigest(),'afterSha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(base/'required-findings-hardening.v1.json').write_text(json.dumps({'standing':'Codex prospective documentation application tooling change; independent final application review still required. No current/frozen design source edited or application performed.','reason':'An ACCEPT headline is insufficient if required findings remain or were not explicitly accounted. Align finalizer, prerequisites and postapply verification with the existing strict review gate.','files':rows,'selftestExpected':'20 synthetic checks, including both required-finding arrays unresolved, absent and mistyped. Actual results recorded separately.','implementationAuthorized':False},indent=2)+'\n')
print('Prospective application tooling hardened; exact before-images retained; run synthetic selftest next.')
