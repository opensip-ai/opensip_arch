"""Root diagnostics for the two remaining publication gaps on released v2.
Schema-only synthetic public records; no claimed host output, Run closure or D9 execution.
"""
from pathlib import Path
import copy,hashlib,importlib.util,json,shutil
root=Path('/tmp/opensip-design-corrections/bv4-final-source-recheck.v2/work');dc=root/'docs/coop/design-corrections'
p=dc/'integration-fixtures.py';s=importlib.util.spec_from_file_location('root_final_public',p);f=importlib.util.module_from_spec(s);s.loader.exec_module(f)
rows=[]
routes=f.N.SCHEMAS['x-opensip-public-route-registry'];public=json.loads((dc/'public-detail-registry.v1.json').read_text());aliases={r['internalCode']:r['publicCode'] for r in public['internalAliases']}
for key,row in routes['keys'].items():
 for origin,target in row.get('byOriginatingBoundary',{'row':row}).items():
  literal={'code':target['publicDetail'],'subject':'capability and mode diagnostic','remedy':'inspect the admitted request or release'}
  r={'internalKey':key,'origin':origin,'publishedTarget':target['publicDetail'],'aliasPresent':key in aliases}
  try:f.W.validate_import_record('workflows/schemas/common.schema.json','#/$defs/DomainDetail',literal);r['literalTargetSchemaAdmission']='ADMIT'
  except Exception as e:r.update(literalTargetSchemaAdmission='REFUSE',error=type(e).__name__+':'+str(e),causeType=type(e.__cause__).__name__)
  rows.append(r)
units=[{'languageMode':'ts-tsconfig','rootPath':'.','languageFamily':'tsjs'}]
staged=copy.deepcopy(f.NATIVE_FIXTURES['registryStagedBuild']);full=copy.deepcopy(f.NATIVE_FIXTURES['registry'])
a=f.N.default_capability_selection(units,staged);b=f.N.default_capability_selection(units,full)
assert a['analysisSpec']==b['analysisSpec'] and len(a['analysisSpec']['requestedCapabilities'])==11
candidate=[r for r in a['undeclaredCapabilities'] if r['projection']=='selection-account-only'];assert len(candidate)==2
base={'kind':'analysis','authority':'authoritative','runId':'run2:'+'a'*64,'planId':'plan2:'+'b'*64,'verdict':'pass','requiredCoverage':'satisfied','durability':'committed','deficiency':'none','secondaryDeficiencies':[]}
carrier=[]
for label,value in [('valid closed AnalysisResult schema-only control',base),('literal addition of the helper absence account',dict(base,undeclaredCapabilities=candidate))]:
 r={'case':label}
 try:f.W.validate_import_record('workflows/schemas/invocation-record.schema.json','#/$defs/AnalysisResult',value);r['outcome']='ADMIT'
 except Exception as e:r.update(outcome='REFUSE',error=type(e).__name__+':'+str(e),causeType=type(e.__cause__).__name__)
 carrier.append(r)
assert carrier[0]['outcome']=='ADMIT' and carrier[1]['outcome']=='REFUSE'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report={'standing':'Root diagnostic on exact released coauthor v2. Literal materialization checks the handoff claim that every publicDetail target is an existing member and its aliases edit is mechanical; prose placeholders are not inferred as real codes. Synthetic AnalysisResult uses placeholder identifiers solely for schema admission, never a claimed committed Run. No host runtime, D9 interpreter, renderer execution, qualification or acceptance.','sourceRoot':str(root),'sources':[{'path':str(p.relative_to(root)),'sha256':sha(p)} for p in [dc/'native/native-evidence.schemas.v2.json',dc/'native/native_evidence_model.v2.py',dc/'public-detail-registry.v1.json',dc/'workflows/schemas/common.schema.json',dc/'workflows/schemas/command-envelope.schema.json',dc/'workflows/schemas/invocation-record.schema.json']], 'publicTargets':rows,'missingAliasKeys':sorted(set(routes['keys'])-set(aliases)), 'defaultSelection':{'requestedCount':11,'sameRequestWithFullAndStagedRelease':True,'candidateOnlyAbsences':candidate},'analysisResultCarrierControls':carrier}
out=Path('/tmp/opensip-design-corrections/bv4-public-recheck.v2');out.mkdir(exist_ok=False);(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');shutil.copyfile(__file__,out/'probe.py')
print(json.dumps({'routeBranches':len(rows),'literalTargetsAdmitted':sum(r['literalTargetSchemaAdmission']=='ADMIT' for r in rows),'literalTargetsRefused':sum(r['literalTargetSchemaAdmission']=='REFUSE' for r in rows),'missingAliasKeys':len(report['missingAliasKeys']),'carrierControls':carrier},indent=2))
