import json,hashlib,os,re
R='/tmp/opensip-design-corrections/candidate-subject.v21/docs/coop/design-corrections'
def T(p): return open(os.path.join(R,p)).read()
def raw(p): return hashlib.sha256(open(os.path.join(R,p),'rb').read()).hexdigest()
out={}

# ---- CX-V20-SENTINEL-SUCCESS: the positive must distinguish ANY Refusal (incl detail=None) ----
ci=T('foundation/check-identity.py')
m=re.findall(r"[^\n]*_SENTINEL[^\n]*",ci)
out['sentinel']={'occurrences':len(m),'lines':m[:14]}

# ---- CX-V20-FINAL-FIXTURE: native fixture declared digest == FINAL native document digest ----
actual=raw('native/native-evidence.schemas.v2.json')
nc=T('native/native-cases.v2.json')
out['nativeFixtureDigest']={'actualNativeSchemaDoc':actual,
  'actualDigestAppearsInNativeCases':actual in nc,
  'actualDigestAppearsInCheckIdentity':actual in ci,
  'actualDigestAppearsInIdentitySchemas':actual in T('foundation/identity-schemas.v2.json')}
# any OTHER 64-hex that is claimed as the native schema doc digest?
claims=set(re.findall(r'"payloadSchemaDigest"\s*:\s*"([0-9a-f]{64})"',nc))
out['nativeFixtureDigest']['payloadSchemaDigestValuesInCases']=sorted(claims)
docs={}
for p in ['native/native-evidence.schemas.v2.json','workflows/schemas/imported-evidence.schema.json',
          'workflows/schemas/test-execution.schema.json','workflows/schemas/policy-document.schema.json',
          'foundation/import-source-context.schema.json','foundation/relation-payload-schemas.v2.json']:
    docs[raw(p)]=p
out['nativeFixtureDigest']['resolvedClaims']={c:docs.get(c,'UNRESOLVED-not-a-registered-document') for c in sorted(claims)}

# ---- RC-6 at BOTH boundaries ----
nm=T('native/native_evidence_model.v2.py')
out['rc6']={'coverage_bijection_callsites':len(re.findall(r'coverage_bijection\(',nm)),
  'admit_coverage_result_v3_calls_bijection':bool(re.search(r'def admit_coverage_result_v3.*?coverage_bijection\(',nm,re.S)),
  'examinedExhaustive_guard':[l.strip() for l in nm.splitlines() if 'examinedExhaustive' in l and ('complete' in l or 'raise' in l or 'if ' in l)][:8]}
im=T('foundation/identity-model.py')
out['rc6']['identity_model_reruns_coverage_admission']=bool(re.search(r'admit_coverage_result_v3',im))
out['rc6']['identity_model_bijection_ref']=[l.strip() for l in im.splitlines() if 'coverage_bijection' in l or 'admit_coverage_result_v3' in l][:6]

# ---- registered-schema-document guard reachable at closure ----
out['schemaDocGuard']={'SCHEMA_DOCUMENT_UNREGISTERED_lines':[l.strip() for l in im.splitlines() if 'SCHEMA_DOCUMENT_UNREGISTERED' in l][:6],
  'registered_schema_documents_body':'\n'.join(im.splitlines()[622:640])}

# ---- Law 1 three enforcement points ----
out['law1_sites']={'foundation_helper':'identity-model.admit_parameter_selection',
  'native_pre_plan':bool(re.search(r'IM\.admit_parameter_selection\(spec\["parameters"\]\)',T('native/native_evidence_model.v2.py'))),
  'foundation_run_closure':bool(re.search(r"admit_parameter_selection\(analysis_spec\['parameters'\]\)",im)),
  'workflow_verifier':bool(re.search(r'def verify_scope_parameter_binding',T('workflows/workflows_model.v1.py')))}

# ---- ledgers count ----
import glob
led=[p for p in glob.glob(os.path.join(R,'*/source-pins.v*.json'))]
out['ledgerCount']={'n':len(led),'paths':sorted(os.path.relpath(p,R) for p in led)}
print(json.dumps(out,indent=1))
json.dump(out,open('/tmp/opensip-design-corrections/post-reset-review.v21/results/law-targeted.json','w'),indent=1)
