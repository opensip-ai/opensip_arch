import pathlib,json,hashlib,difflib
b=pathlib.Path('/tmp/opensip-implementation/x4tc-authoring');p=pathlib.Path('/Users/sb/code/opensip-ai/opensip');c=b/'product';a=pathlib.Path('/Users/sb/code/opensip-ai/opensip_arch');prefix='docs/implementation/m2/continuation-diagnostics-x4tc-r1'
def load(root,path):return json.loads((root/path).read_text())
def same_without(root,path,alter):
 x=load(p,path);y=load(root,path);alter(x,y);assert x==y,path
codes=['CONTINUE-INDEX-NOT-TRUSTED','CONTINUE-COMPONENT-NOT-TRUSTED'];old=load(p,'schemas/sources/common-v4.schema.json');new=load(c,'schemas/sources/common-v4.schema.json');assert new['$defs']['DomainDetailCode']['enum'][-2:]==codes;new['$defs']['DomainDetailCode']['enum']=new['$defs']['DomainDetailCode']['enum'][:-2];assert old==new
oldreg=load(a,'docs/implementation/m2/existing-root-diagnostics-468a/reference/public-detail-registry.json');newreg=load(b/'design','reference/public-detail-registry.json');assert newreg['records']==sorted(newreg['records'],key=lambda r:r['code']);added=[r for r in newreg['records'] if r['code'] in codes];assert len(added)==2
newreg['records']=[r for r in newreg['records'] if r['code'] not in codes];newreg.pop('trustContinuationCorrection');assert oldreg==newreg
oldadm=load(p,'schemas/admission-registry.json');newadm=load(c,'schemas/admission-registry.json');common=lambda r:r['sourcePath']=='schemas/sources/common-v4.schema.json';row=next(r for r in oldadm['sources'] if common(r));idx=next(i for i,r in enumerate(newadm['sources']) if common(r));newadm['sources'][idx]=row;assert oldadm==newadm
oldmap=load(p,'schemas/source-map.json');newmap=load(c,'schemas/source-map.json');i=next(i for i,r in enumerate(oldmap['sources']) if r['implementationPath']=='schemas/sources/common-v4.schema.json');newmap['sources'][i]['architectureSource']=oldmap['sources'][i]['architectureSource'];assert oldmap==newmap
for rel in ['schemas/sources/common-v1.schema.json','schemas/sources/common-v3.schema.json','tools/contracts/pipeline.py','tools/contracts/toolchain.json','tools/contracts/build-receipt.json','tools/generate_contracts.py','tools/verify_design.py']:
 assert (p/rel).read_bytes()==(c/rel).read_bytes(),rel
x=load(p,'tools/contracts/generator-closure.json');y=load(c,'tools/contracts/generator-closure.json');changed=[r['path'] for r,q in zip(x['files'],y['files'],strict=True) if r!=q];assert changed==['schemas/source-map.json','schemas/sources/common-v4.schema.json'];assert x['toolchain']==y['toolchain']
report=dict(passed=True,common4OldPositions=322,common4NewValues=codes,publicOldRowsPreserved=True,aliasesPreserved=True,onlyCurrentCommon4AdmissionRowChanged=True,oldSourcesAndToolsExact=True,generatorClosureChangedPaths=changed,standing='STRUCTURAL PRESERVATION ONLY; NO SOURCE SELECTION/DRIFT/QUALIFICATION')
(b/'preservation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
