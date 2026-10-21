from pathlib import Path
import json,hashlib,importlib.util,sys,os
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'source-census-r2';B.mkdir(exist_ok=False)
W=Path('/Users/sb/code/opensip-ai/opensip-rust3-send-takeover')
pins=json.loads((F/'mutation-owning-r2/report.json').read_text())['sourcePins']
assert all(hashlib.sha256((W/p['path']).read_bytes()).hexdigest()==p['sha256']for p in pins)
source=W/'tools/operability/exceptions.json';raw=source.read_bytes();old=json.loads(raw)
spec=importlib.util.spec_from_file_location('d2b4b_public_source_census',W/'tools/check_operability.py');tool=importlib.util.module_from_spec(spec);sys.modules[spec.name]=tool;spec.loader.exec_module(tool)
proposal=tool.proposed_rows(W)
assert {(r['path'],r['class']):r['count']for r in proposal['rows']}=={(r['path'],r['class']):r['count']for r in old['rows']} and len(old['rows'])==115
# Keep the accepted owner annotations verbatim; proposed_rows is a heuristic
# for fresh rows and must not overwrite the invocation-mode owner assignment.
key=lambda row:(row['path'],row['member'],row['kind'])
before={key(r):r for r in old['mintAudit']['rows']};after={key(r):r for r in proposal['mintAudit']['rows']}
assert len(before)==453 and len(before)==len(old['mintAudit']['rows'])and len(after)==len(proposal['mintAudit']['rows'])
assert set(before)<=set(after)
changed=[dict(before=before[k],after=after[k])for k in before if before[k]!=after[k]]
added=[r for k,r in after.items()if k not in before]
assert all(r['path']in {p['path']for p in pins} and r['kind']=='call' and r['member']in ['from','into']for r in added)
assert all(r['after']['path']in {p['path']for p in pins}and r['after']['kind']=='call'and r['after']['member']in ['from','into']and r['after']['count']>r['before']['count']for r in changed)
new=json.loads(raw);new['mintAudit']['rows']=proposal['mintAudit']['rows']
for k in old:
 if k!='mintAudit':assert new[k]==old[k]
for k in old['mintAudit']:
 if k!='rows':assert new['mintAudit'][k]==old['mintAudit'][k]
(B/'original-exceptions.json').write_bytes(raw)
source.write_text(json.dumps(new,indent=2)+'\n')
result=tool.source_check(W);assert result['passed'],result
report=dict(standing='Proposed lexical constructor census refresh for independent full4b review; not provenance or mint authority',beforeRows=len(before),afterRows=len(after),operabilityRows=115,all453ParentRowsPreserved=True,added=added,changed=changed,removed=[],allOwnerDefinitionsUnchanged=True,memberListUnchanged=True,standingUnchanged=True,testSupportAndTerminationDeclarationsUnchanged=True,assessment='New from/into call identifiers in codec projection/container/integer/string construction and synthetic tests. No native scope/identity/owner admission is created; these ambiguous lexical calls remain inventoried, not exempted.',beforeSha256=hashlib.sha256(raw).hexdigest(),afterSha256=hashlib.sha256(source.read_bytes()).hexdigest(),sourceCheck=result,productQualification=False)
(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('PUBLIC SOURCE115/CONSTRUCTOR'+str(len(after))+' PASS;453PARENTROWS PRESERVED;NO MINT AUTHORITY')
