from pathlib import Path
import os,json,hashlib,importlib.util,sys
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'source-census-r1';B.mkdir(exist_ok=False);W=Path('/Users/sb/code/opensip-ai/opensip-d4factory-takeover');audit=json.loads((F/'source-census-audit-r1/report.json').read_text());proposal=json.loads((F/'source-census-audit-r1/proposed.json').read_text())
for p in audit['sourcePins']:assert hashlib.sha256((W/p['path']).read_bytes()).hexdigest()==p['sha256']
p=W/'tools/operability/exceptions.json';raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==audit['beforeSha256'];old=json.loads(raw)
assert audit['ownerCountsUnchanged'] and len(old['rows'])==115 and audit['beforeRows']==463 and audit['afterRows']==470 and not audit['changed'] and not audit['removed']
assert len(audit['added'])==7 and all(r['kind']=='call' and r['member']in ['from','into'] and r['path']in {p['path']for p in audit['sourcePins']} for r in audit['added'])
new=json.loads(raw);new['mintAudit']['rows']=proposal['mintAudit']['rows'];key=lambda r:(r['path'],r['member'],r['kind']);after={key(r):r for r in new['mintAudit']['rows']};assert all(after[key(r)]==r for r in old['mintAudit']['rows'])
for k in old:
 if k!='mintAudit':assert new[k]==old[k]
for k in old['mintAudit']:
 if k!='rows':assert new['mintAudit'][k]==old['mintAudit'][k]
(B/'original-exceptions.json').write_bytes(raw);p.write_text(json.dumps(new,indent=2)+'\n')
spec=importlib.util.spec_from_file_location('d4_refreshed_public_source_census',W/'tools/check_operability.py');tool=importlib.util.module_from_spec(spec);sys.modules[spec.name]=tool;spec.loader.exec_module(tool);check=tool.source_check(W);assert check['passed']
report=dict(standing='Proposed D4 lexical census refresh only; independent unit review pending; no mint or owner authority created.',beforeRows=463,afterRows=470,operabilityRows=115,all463ParentRowsPreservedByValue=True,all115OwnerAnnotationsUnchanged=True,ownerDefinitionsUnchanged=True,memberListAndStandingUnchanged=True,terminationAndTestSupportDeclarationsUnchanged=True,added=audit['added'],removed=[],changed=[],beforeSha256=hashlib.sha256(raw).hexdigest(),afterSha256=hashlib.sha256(p.read_bytes()).hexdigest(),sourceCheck=check,assessment='Seven ordinary from/into call rows: two codec participant error strings, synthetic factory/Plan fixture/container conversions, and the test-only full-carrier preservation control. Conservative lexical inventory includes inline test modules; no scopes, identities, source or provenance are minted.',runtimeCodeUnchangedFrom31PathSuites=True,productQualification=False)
(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('SOURCE115/LEXICAL470 PASS; ALL463 PARENT ROWS AND ALL115 OWNER ANNOTATIONS UNCHANGED; ONLY7ORDINARY FROM/INTO ROWS ADDED')
