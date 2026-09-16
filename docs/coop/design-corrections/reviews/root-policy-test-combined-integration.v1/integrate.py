from pathlib import Path
import json,hashlib,shutil,difflib,subprocess
B=Path('/tmp/opensip-design-corrections');R=Path(__file__).parent;L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews');T=B/'source39-corrections-successor.v1/source';A=B/'claude-policy-test-imported-universe-author.v1';F=B/'candidate-subject.v39';H=lambda b:hashlib.sha256(b).hexdigest()
mf=L/'candidate-subject.v39.json';assert H(mf.read_bytes())=='f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009';m=json.loads(mf.read_bytes())
public=L/A.name/'final-public-artifact-manifest.json';pub=json.loads(public.read_bytes())
for row in pub['files']:
 p=public.parent/row['retainedPath'] if 'retainedPath' in row else F/row['sameAsSubjectPath'];b=p.read_bytes();assert len(b)==row['bytes'] and H(b)==row['sha256'],str(p)
assert json.loads((A/'process-completion.json').read_bytes())['exitCode']==0
assert not json.loads((A/'result.json').read_bytes()).get('is_error')
d=json.loads((A/'custody/combined-delta-manifest.json').read_bytes());assert len(d['changes'])==6
for row in m['files']:
 b=(T/row['path']).read_bytes();assert len(b)==row['bytes'] and H(b)==row['sha256'],row['path']
changes=[]
for row in d['changes']:
 p=T/row['path'];before=p.read_bytes();after=(A/'work/source'/row['path']).read_bytes();assert H(before)==row['beforeSha256'] and H(after)==row['afterSha256'];assert len(after)==row['afterBytes']
 q=R/'before'/row['path'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(before);p.write_bytes(after);changes.append(row)
# Preserve registered source39 schema bytes; clarify the exact historic annotation scope.
p=T/'docs/v2/contracts/product-v1/native-evidence.md';before=p.read_bytes();text=before.decode();anchor='successor with its own re-registration, not a text correction.\n';assert text.count(anchor)==1
paragraph='\n**Prerelease document revision and historical standing.** The unchanged bytes above are the named\n`publicD9Termination` annotation. A separate prerelease revision changed\n`#/$defs/ResolvedNodeModulesLayoutV1/description` in the same schema document. Its registered raw digest\nchanged from `3e37c7b7a6a620dcadc0aaed862eed242065ebd0ce9910da16faa25464f8b0b0`\n(source38) to `2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043`\n(source39); the source39 registry and rebuilt reference exports use the latter. This is an explicit\ndocument revision and re-registration despite the unchanged filename and record majors. The older digest\nis not an alias for the newer bytes and is not registered by the source39 reference profile. Historical\nsource38 artifacts remain evidence for their own frozen source and registry; this revision grants no\ncross-profile replay or migration acceptance. The retained historical bytes and identities are not rewritten.\n'
text=text.replace(anchor,anchor+paragraph);after=text.encode();q=R/'before/docs/v2/contracts/product-v1/native-evidence.md';q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(before);p.write_bytes(after)
(R/'native-revision-clarification.diff').write_text(''.join(difflib.unified_diff(before.decode().splitlines(True),text.splitlines(True),fromfile='source39/native-evidence.md',tofile='successor/native-evidence.md')))
assert H((T/'docs/coop/design-corrections/native/native-evidence.schemas.v2.json').read_bytes())=='2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043'
# Root's exact independently authored probe, with source/output path adaptations only.
old=B/'root-policy-test-imported-universe-probe.v1/probe.py';probe=old.read_text().replace("B/'claude-policy-test-known-hit-author.v1/work/source39'", "B/'source39-corrections-successor.v1/source'");(R/'probe.py').write_text(probe)
assert old.read_text()!=probe
cmd=['/tmp/opensip-architecture-review-env/bin/python','-I','-B',str(R/'probe.py')];result=subprocess.run(cmd,capture_output=True,text=True);(R/'probe.stdout.json').write_text(result.stdout);(R/'probe.stderr.txt').write_text(result.stderr);assert result.returncode==0
report=json.loads((R/'report.json').read_bytes());by={(x['source'],x['factUniverse']):x['result'] for x in report['rows']};assert by['author-correction','typescript']['observedVerdict']=='fail' and len(by['author-correction','typescript']['findings'])==1;assert by['author-correction','rust']['observedVerdict']=='indeterminate' and by['author-correction','rust']['findings']==[];assert by['frozen39','rust']['observedVerdict']=='fail'
record={'standing':'Combined bounded AUTHOR correction integrated into mutable successor only. Root counterexample discriminates unchanged defective frozen39 from corrected copy. Native advisory clarification authored by root; independent successor review pending. No acceptance/freeze/product/application.', 'publicManifestSha256':H(public.read_bytes()),'publicFilesVerified':len(pub['files']),'baseFilesVerified':len(m['files']),'combinedPatchSha256':d['patchSha256'],'changes':changes,'nativeClarification':{'beforeSha256':H(before),'afterSha256':H(after)},'rootProbe':{'command':cmd,'exitCode':result.returncode,'sameUniverseKnownHitPreserved':True,'foreignUniverseNoKnownHit':True}}
(R/'integration.json').write_text(json.dumps(record,indent=2)+'\n');dest=L/R.name;shutil.copytree(R,dest);print(json.dumps(record))
