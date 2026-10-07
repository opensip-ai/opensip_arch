import pathlib,json,hashlib
p=pathlib.Path('/Users/sb/code/opensip-ai/opensip');a=pathlib.Path('/Users/sb/code/opensip-ai/opensip_arch');b=pathlib.Path('/tmp/opensip-implementation/x4tc-authoring/design');prefix='docs/implementation/m2/continuation-diagnostics-x4tc-r1';codes=['CONTINUE-INDEX-NOT-TRUSTED','CONTINUE-COMPONENT-NOT-TRUSTED']
def write(rel,x):
 f=b/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(x,indent=2)+'\n');return f.read_bytes()
def pin(rel,raw):return dict(path=rel,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
old=(p/'schemas/sources/common-v4.schema.json').read_bytes();schema=json.loads(old);values=schema['$defs']['DomainDetailCode']['enum'];assert len(values)==322 and not set(codes)&set(values);values.extend(codes)
raw=write('schemas/common.v4.schema.json',schema);new=json.loads(raw);new['$defs']['DomainDetailCode']['enum']=new['$defs']['DomainDetailCode']['enum'][:-2];assert new==json.loads(old)
source_pin=pin(prefix+'/schemas/common.v4.schema.json',raw)
reg=json.loads((a/'docs/implementation/m2/existing-root-diagnostics-468a/reference/public-detail-registry.json').read_text());before=dict(reg);records=reg['records']
for code in codes:records.append(dict(code=code,owner='security',selector='docs/implementation/m2/trust-admission-x4t/PROPOSAL-r12.md; Lead decision: two continuation codes; request-rejected exit 2 EXTENSION.ADMISSION_REJECTED'))
records.sort(key=lambda r:r['code']);assert len(records)==324 and len({r['code'] for r in records})==324
reg['trustContinuationCorrection']=dict(codes=codes,owner='docs/implementation/m2/trust-admission-x4t/PROPOSAL-r12.md',activation='Current common4, public registry/D9 routes, generation/admission maps and generated bindings require independent selection and strict drift before role-accurate emission; no runtime enablement by preparation.')
write('reference/public-detail-registry.json',reg)
adm=json.loads((p/'schemas/admission-registry.json').read_text());rows=[r for r in adm['sources'] if r['sourcePath']=='schemas/sources/common-v4.schema.json'];assert len(rows)==1;rows[0].update(bytes=source_pin['bytes'],sha256=source_pin['sha256']);write('schemas/admission-registry.json',adm)
write('diagnostic-routes.json',dict(schemaVersion=1,standing='PROPOSED X4T-c exact two-code D9 composition only; no new route, class or exit',routes=[dict(role=role,detail=code,outcomeClass='request-rejected',exit=2,errorCode='EXTENSION.ADMISSION_REJECTED') for role,code in [('TR-INDEX',codes[0]),('TR-COMPONENT',codes[1])]],inheritedCoreDetail='CONTINUE-CORE-NOT-TRUSTED',inheritedSubject='role-naming continuation subject unchanged'))
write('preparation.json',dict(standing='UNFROZEN ARCHITECTURE COPY PREPARATION ONLY; NO ACCEPTANCE/BIND/GENERATION',common4=source_pin,oldCodePositionsPreserved=322,newCodeCount=2,currentCommonCodeCount=324,publicRegistryCount=324,common1Or3Changed=False,sourceDependenciesChanged=False,productEdited=False))
print('prepared complete common4/public registry/admission copies and exact D9 routes')
