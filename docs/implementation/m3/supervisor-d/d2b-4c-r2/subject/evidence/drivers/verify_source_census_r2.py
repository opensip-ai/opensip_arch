from pathlib import Path
import json,hashlib,importlib.util,sys,os
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'source-census-r2';B.mkdir();W=Path('/Users/sb/code/opensip-ai/opensip-rust3-successor-takeover');pins=json.loads((F/'candidate-suites-r3/report.json').read_text())['sourcePins']
assert all(hashlib.sha256((W/p['path']).read_bytes()).hexdigest()==p['sha256']for p in pins)
p=W/'tools/operability/exceptions.json';raw=p.read_bytes();prior=json.loads((F/'source-census-r1/report.json').read_text());assert hashlib.sha256(raw).hexdigest()==prior['afterSha256']
spec=importlib.util.spec_from_file_location('d2b4c_final_source_census',W/'tools/check_operability.py');tool=importlib.util.module_from_spec(spec);sys.modules[spec.name]=tool;spec.loader.exec_module(tool)
r=tool.source_check(W);assert r['passed'];record=json.loads(raw);assert len(record['rows'])==115 and len(record['mintAudit']['rows'])==463 and tool.mint_inventory(W)==record['mintAudit']['rows']
report=dict(standing='Fresh current-cutoff verification of unchanged lexical census; no mint/owner authority',sourcePins=pins,operabilityRows=115,constructorRows=463,sourceCheck=r,priorRefresh='source-census-r1/report.json',exceptionsSha256=hashlib.sha256(raw).hexdigest(),exceptionsUnchanged=True,allOwnerAnnotationsUnchanged=True,productQualification=False)
(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('CURRENT SOURCE115/CONSTRUCTOR463 PASS; NO CENSUS MUTATION')
