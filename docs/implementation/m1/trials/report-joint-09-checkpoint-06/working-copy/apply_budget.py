"""Second generation phase: apply hash-bound derived sizes, not depth qualification."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
result=json.loads((HERE/'joint-budget-derivation.json').read_bytes())
path=HERE/'composed-sources/report-projection.proposed.schema.json'
raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==result['inputReportSha256']
depth=json.loads((HERE/'joint-depth-derivation.json').read_bytes())
assert depth['inputReportSha256']==result['inputReportSha256']
assert type(depth['documentMaxContainerDepth']) is int
schema=json.loads(raw);props=schema['$defs']['BudgetProfileV1']['properties']
for key,value in [('documentMaxBytes',result['documentMaxBytes']),('ledgerMaxBytes',result['ledgerMaxBytes']),('rootMemberMaxBytes',sum(result['rootMemberMaxBytes'].values()))]:props[key]={'const':value}
assert len(str(props['maxJsonDepth']['const']))==len(str(depth['documentMaxContainerDepth']))
props['maxJsonDepth']={'const':depth['documentMaxContainerDepth']}
path.write_text(json.dumps(schema,indent=2)+'\n')
new=path.read_bytes();source_result=json.loads((HERE/'composition-result.json').read_bytes())
row=next(r for r in source_result['outputs'] if r['path']==str(path.relative_to(HERE)))
row.update(sha256=hashlib.sha256(new).hexdigest(),bytes=len(new))
source_result['budgetPhase']={'inputReportSha256':result['inputReportSha256'],'derivationSha256':hashlib.sha256((HERE/'joint-budget-derivation.json').read_bytes()).hexdigest(),'depthDerivationSha256':hashlib.sha256((HERE/'joint-depth-derivation.json').read_bytes()).hexdigest(),'depthStanding':'Conservative schema/owner boundary bound39 proposed; original owner codec32 retained, including feature query documents. Not a claim that39 is reachable under every semantic join.'}
(HERE/'composition-result.json').write_text(json.dumps(source_result,indent=2)+'\n')
print(json.dumps({'documentMaxBytes':result['documentMaxBytes'],'rootMemberMaxBytes':sum(result['rootMemberMaxBytes'].values()),'ledgerMaxBytes':result['ledgerMaxBytes']}))
