from pathlib import Path
import json,hashlib,shutil,subprocess
B=Path('/tmp/opensip-design-corrections');L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews');O=Path(__file__).parent;A=B/'claude-view-attribution-assessment.v1';S=B/'source40-corrections-successor.v1/source';F=B/'candidate-subject.v40';H=lambda b:hashlib.sha256(b).hexdigest()
assert json.loads((A/'process-completion.json').read_bytes())['exitCode']==0
assert (A/'review.md').is_file() and (A/'review.json').is_file()
pub=L/A.name/'final-public-artifact-manifest.json';m=json.loads(pub.read_bytes())
for r in m['files']:
 p=pub.parent/r['retainedPath'] if 'retainedPath' in r else F/r['sameAsSubjectPath'];raw=p.read_bytes();assert H(raw)==r['sha256'] and len(raw)==r['bytes'];assert raw==(A/r['runtimePath']).read_bytes()
d=json.loads((A/'delta-manifest.json').read_bytes());assert H((A/'correction.patch').read_bytes())==d['patchSha256']=='f795b00609b4479dc09e5608d9d16cd5d06cf8531f0f324d57f06039d79d91b8'
assert len(d['changedFiles'])==4
for r in d['changedFiles']:
 rel=r['path'];old=(S/rel).read_bytes();new=(A/'work/patched-tree'/rel).read_bytes();assert old==(F/rel).read_bytes() and H(old)==r['baseSha256'];assert H(new)==r['afterSha256'] and len(new)==r['afterBytes']
for r in d['changedFiles']:
 rel=r['path'];p=O/'before'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((S/rel).read_bytes());shutil.copy2(A/'work/patched-tree'/rel,S/rel)
report={'standing':'Root reviewed entire four-file patch and substantive author report. Integrated exact verified author correction into NEW isolated successor of40. No source/consumer/application acceptance and no LIVE activation. Focused owner controls plus broad pinned suites and independent review remain required.','publicManifestSha256':H(pub.read_bytes()),'publicFilesVerified':len(m['files']),'reviewMdSha256':H((A/'review.md').read_bytes()),'reviewJsonSha256':H((A/'review.json').read_bytes()),'delta':d,'rootDecision':'Adopt literal named-scope law for all applicability, same-scope attribution, preserve captured unattributed views and cross-universe targets. No new refusal code/schema. Shared fixture helper change is necessary for maintained law-conforming controls.'}
(O/'integration.json').write_text(json.dumps(report,indent=2)+'\n');shutil.copytree(O,L/O.name);print(json.dumps(report))
