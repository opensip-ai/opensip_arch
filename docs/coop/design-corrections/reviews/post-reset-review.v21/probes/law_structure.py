import json,hashlib,os,re
R='/tmp/opensip-design-corrections/candidate-subject.v21/docs/coop/design-corrections'
def J(p): return json.load(open(os.path.join(R,p)))
def T(p): return open(os.path.join(R,p)).read()
def raw(p): return hashlib.sha256(open(os.path.join(R,p),'rb').read()).hexdigest()
out={}

# ---- LAW 8: public detail registry, two BASELINE.SCOPE_* codes, count, ledgers ----
reg=J('public-detail-registry.v1.json')
codes=None
for k,v in reg.items():
    if isinstance(v,list) and v and isinstance(v[0],dict) and ('code' in v[0]): codes=[e['code'] for e in v];key=k;break
    if isinstance(v,dict) and len(v)>50: codes=sorted(v);key=k;break
common=J('workflows/schemas/common.schema.json')
enum=common['$defs']['DomainDetailCode']['enum']
L8={'registryKeys':list(reg.keys()),'registryCodeListKey':key,'registryCount':len(codes),
    'enumCount':len(enum),'registryEqualsEnum':sorted(codes)==sorted(enum),
    'BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER':{'inRegistry':'BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER' in codes,
        'inEnum':'BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER' in enum},
    'BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH':{'inRegistry':'BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH' in codes,
        'inEnum':'BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH' in enum},
    'noThirdBaselineScopeSpelling':[c for c in codes if c.startswith('BASELINE.SCOPE')]}
out['law8_public_details']=L8

# ---- LAW 3: RC-6, registered (relation,rung) pairs ----
rp=J('foundation/relation-payload-schemas.v2.json')
rr=rp['x-opensip-relation-registry']
rows=rr if isinstance(rr,dict) else {}
pairs=[]; ladders={}
for rel,row in rows.items():
    if not isinstance(row,dict) or 'ladder' not in row: continue
    ladders[rel]=row['ladder']
    for rung in row['ladder']: pairs.append(rel+'@'+rung)
RESOLVED={'resolved-target','resolved-binding','resolved-callee','checked','from-resolved-calls'}
out['law3_rc6']={'relationCount':len(ladders),'registeredPairCount':len(pairs),'pairs':sorted(pairs),
  'resolvedPairs':sorted(p for p in pairs if p.split('@')[1] in RESOLVED),
  'nonResolvedPairCount':len([p for p in pairs if p.split('@')[1] not in RESOLVED]),
  'emptyLadders':[r for r,l in ladders.items() if not l]}
nm=T('native/native_evidence_model.v2.py')
out['law3_rc6']['examinedExhaustive_in_coverage_bijection']= 'examinedExhaustive' in nm
out['law3_rc6']['rc6_refusal_key_present']='native.coverage-bijection-mismatch' in nm
out['law3_rc6']['coverage_bijection_defined']=bool(re.search(r'def coverage_bijection',nm))

# ---- LAW 4: outputDomains / flat Domain ----
ids=J('foundation/identity-schemas.v2.json')
d=ids['$defs']
out['law4_domains']={'hasFlatDomainDef':'Domain' in d,
  'DomainIsFlatEnum': isinstance(d.get('Domain',{}).get('enum'),list),
  'DomainEnumCount': len(d.get('Domain',{}).get('enum',[]) or []),
  'RefDomainEnumCount': len(d.get('Ref',{}).get('properties',{}).get('domain',{}).get('enum',[]) or []),
  'RefDomainEqualsDomain': sorted(d.get('Domain',{}).get('enum',[]) or [])==sorted(d.get('Ref',{}).get('properties',{}).get('domain',{}).get('enum',[]) or []),
  'stageSpecOutputDomains': d.get('stage-spec',{}).get('properties',{}).get('outputDomains'),
  'execPlanStageOutputDomains': (d.get('execution-plan',{}).get('properties',{}).get('stages',{}).get('items',{}).get('properties',{}) or {}).get('outputDomains')}
byd=ids.get('x-opensip-digest-domains',{}).get('byDomain',{})
out['law4_domains']['byDomainCount']=len(byd)
out['law4_domains']['DomainEnumSubsetOfByDomain']=set(d.get('Domain',{}).get('enum',[]) or [])<=set(byd)

# ---- LAW 5: closureMembership ----
cm=ids.get('x-opensip-digest-domains',{}).get('closureMembership')
out['law5_closureMembership']={'present':cm is not None,'keys':list(cm.keys()) if isinstance(cm,dict) else None,
  'json':json.dumps(cm)[:2500] if cm else None}

# ---- LAW 6: registered-schema-document artifact class ----
def find_artifact(o,p='',acc=None):
    if acc is None: acc=[]
    if isinstance(o,dict):
        xa=o.get('x-opensip-digest')
        if isinstance(xa,dict) and xa.get('artifactClass')=='registered-schema-document': acc.append((p,xa))
        for k,v in o.items(): find_artifact(v,p+'/'+k,acc)
    elif isinstance(o,list):
        for i,v in enumerate(o): find_artifact(v,p+'/'+str(i),acc)
    return acc
fa=find_artifact(ids)
out['law6_registered_schema_document']={'occurrences':[p for p,_ in fa],'count':len(fa)}
im=T('foundation/identity-model.py')
out['law6_registered_schema_document']['SCHEMA_DOCUMENT_UNREGISTERED_in_model']='SCHEMA_DOCUMENT_UNREGISTERED' in im
out['law6_registered_schema_document']['registered_schema_documents_fn']=bool(re.search(r'def registered_schema_documents',im))

# ---- LAW 7: importIds equality ----
out['law7_importids']={'IMPORT_JOIN_in_model':'IMPORT_JOIN' in im,
  'UNSELECTED_EVALUATION_IMPORT_in_model':'UNSELECTED_EVALUATION_IMPORT' in im,
  'HIDDEN_FINDING_EVIDENCE_in_model':'HIDDEN_FINDING_EVIDENCE' in im}
m=re.search(r"[^\n]*IMPORT_JOIN[^\n]*",im); out['law7_importids']['IMPORT_JOIN_line']=m.group(0).strip() if m else None

# ---- LAW 2: ownership tuple ----
out['law2_ownership']={'uniquenessAnnotation':ids['$defs']['analysis-spec']['properties']['requestedCapabilities'].get('x-opensip-uniqueness',{}).get('ownershipTuple'),
  'internalKey_in_native':'native.requested-capability-duplicate-ownership-tuple' in nm,
  'route_registry_has_key':'native.requested-capability-duplicate-ownership-tuple' in T('native/native-evidence.schemas.v2.json')}

# ---- LAW 9: native fixture / registered-schema guard ----
nes=J('native/native-evidence.schemas.v2.json')
out['law9']={'nativeSchemaDocSha256':raw('native/native-evidence.schemas.v2.json'),
  'coverage_row_in_payload_registry':json.dumps(ids.get('x-opensip-payload-registry',{}).get('classes',{}).get('coverage'))[:600]}
print(json.dumps(out,indent=1,default=str))
