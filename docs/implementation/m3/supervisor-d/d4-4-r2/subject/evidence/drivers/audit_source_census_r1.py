from pathlib import Path
import os,json,hashlib,importlib.util,sys,subprocess
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'source-census-audit-r1';B.mkdir(exist_ok=False);W=Path('/Users/sb/code/opensip-ai/opensip-d4factory-takeover')
spec=importlib.util.spec_from_file_location('d4_public_source_census',W/'tools/check_operability.py');tool=importlib.util.module_from_spec(spec);sys.modules[spec.name]=tool;spec.loader.exec_module(tool)
p=W/'tools/operability/exceptions.json';raw=p.read_bytes();old=json.loads(raw);proposal=tool.proposed_rows(W)
key=lambda r:(r['path'],r['member'],r['kind']);before={key(r):r for r in old['mintAudit']['rows']};after={key(r):r for r in proposal['mintAudit']['rows']}
changes=[dict(before=before[k],after=after[k])for k in before.keys()&after.keys()if before[k]!=after[k]];added=[after[k]for k in after.keys()-before.keys()];removed=[before[k]for k in before.keys()-after.keys()]
paths=sorted(subprocess.check_output(['git','ls-files','-m','-o','--exclude-standard'],cwd=W,text=True).splitlines());pins=[dict(path=q,bytes=(W/q).stat().st_size,sha256=hashlib.sha256((W/q).read_bytes()).hexdigest())for q in paths]
report=dict(standing='Read-only public lexical source census delta inspection before any update; not provenance/owner authority.',beforeRows=len(before),afterRows=len(after),ownerRowsBefore=old['rows'],ownerRowsProposal=proposal['rows'],ownerCountsUnchanged={(r['path'],r['class']):r['count']for r in old['rows']}=={(r['path'],r['class']):r['count']for r in proposal['rows']},added=sorted(added,key=key),changed=sorted(changes,key=lambda r:key(r['after'])),removed=sorted(removed,key=key),sourcePins=pins,beforeSha256=hashlib.sha256(raw).hexdigest(),productQualification=False)
(B/'report.json').write_text(json.dumps(report,indent=2)+'\n');(B/'proposed.json').write_text(json.dumps(proposal,indent=2)+'\n');print(json.dumps({k:report[k]for k in ['beforeRows','afterRows','ownerCountsUnchanged','added','changed','removed']},indent=2))
