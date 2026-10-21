"""Conditional data-join analysis only. Never manufacture review/assent records.
The real selected-authority map must refuse this unaccepted design first.
"""
from pathlib import Path
import json,hashlib,shutil,importlib.util
F=Path(__file__).parent;B=F/'source-design-r1';S=B/'architecture';O=B/'join-preflight';assert not O.exists();O.mkdir()
P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch'
prepared=json.loads((B/'prepared.json').read_text());PRE='docs/implementation/m3/native-publication/native-owner-patterns-source-r1'
audit=json.loads((S/PRE/'audit.json').read_text())
def pin(root,path):
 raw=(root/path).read_bytes();return dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
L=json.loads((P/'design-lock.json').read_text())
spec=importlib.util.spec_from_file_location('trusted_design_preflight',P/'tools/verify_design.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
baseline=v.verify(A,L,P);assert baseline['passed']
# Follow the trusted verifier's actual selected base/application member union,
# not merely the smaller lock.inputs list, then its verified contract members.
actual={}
for name in ['sourceManifest','applicationManifest']:
 for row in json.loads(v.pinned_bytes(A,L['approvals'][name]))['files']:actual[row['path']]=row
for unit in baseline['contractSuccessors']:
 for row in unit['inputs']:actual[row['path']]=row
members=json.loads((S/prepared['subjectManifest']['path']).read_text())['files']
for r in members+[prepared['subjectManifest']]:assert pin(S,r['path'])==r
hypothesis=dict(actual)
for r in members:hypothesis[r['path']]=r
AP=O/'architecture';PP=O/'product';AP.mkdir();PP.mkdir()
for row in audit['metadataProductMap']:
 dst=PP/row['productPath'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/row['candidate']['path'],dst)
mapping=json.loads((PP/'schemas/admission-source-map.json').read_text())
for row in mapping['sources']:
 r=row['architectureSource'];root=S if (S/r['path']).exists() else A
 assert pin(root,r['path'])==r and hypothesis[r['path']]==r
 dst=AP/r['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/r['path'],dst)
 dst=PP/row['implementationPath'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/r['path'],dst)
r=mapping['registryArchitectureSource'];dst=AP/r['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/r['path'],dst)
refusals={}
for name,fn in [('generation',v.generation_sources),('admission',v.admission_sources)]:
 try:fn(AP,PP,actual)
 except v.DesignError as e:refusals[name]=str(e)
 else:raise AssertionError('Real authority accepted unreviewed source design')
conditional={name:fn(AP,PP,hypothesis) for name,fn in [('generation',v.generation_sources),('admission',v.admission_sources)]}
registry=json.loads((PP/'schemas/registry.json').read_text());closure=json.loads((S/PRE/'product/tools/contracts/generator-closure.json').read_text())
recipe=registry['recipes'][0];assert recipe['generatorClosureSha256']==pin(S,PRE+'/product/tools/contracts/generator-closure.json')['sha256']
assert sorted(recipe['sourceSha256s'])==sorted(r['sourceSha256'] for r in registry['sources'])
for row in closure['files']:
 root=PP if (PP/row['path']).exists() else P
 assert pin(root,row['path'])==row,row['path']
report=dict(standing='HYPOTHETICAL DATA-JOIN CHECK ONLY; NOT verify_design SUCCESS OR ACCEPTED SOURCE AUTHORITY',baselineCurrentDesignVerificationPassed=True,realSelectedAuthorityRefusals=refusals,hypotheticalSourceDesignJoins=conditional,recipeSourceHashesExact=True,generatorClosureAllRowsExact=True,checker=pin(P,'tools/verify_design.py'),subjectManifest=prepared['subjectManifest'],reviewFabricated=False,assentFabricated=False,lockChanged=False,productCodeChanged=False,generatorExecuted=False,blindRun=False,productQualification=False)
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
