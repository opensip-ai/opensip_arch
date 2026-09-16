from pathlib import Path
import importlib.util,json
P=Path('/tmp/opensip-design-corrections/claude-return-successor.v1/docs/coop/design-corrections/foundation/check-enumeration.v1.py');O=Path(__file__).parent
s=importlib.util.spec_from_file_location('root_unit_guard_regression',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
# Deliberately omit exactly the enumeration root guard in this disposable process.
m.M._admit_membership_unit_roots=lambda membership,faults:True
code=m.main(['--receipt',str(O/'disabled-guard.receipt.json'),'--hashes',str(O/'disabled-guard.hashes.json')]);j=json.loads((O/'disabled-guard.receipt.json').read_text());bad=[r for r in j['mismatches'] if r['case'].startswith('internal-root-')];assert code==1 and len(bad)==4
(O/'disabled-guard.assessment.json').write_text(json.dumps({'standing':'Distinguishing guard-omission mutation in a disposable process; no source input altered, not product qualification.','expectedRootControlsFail':len(bad),'checkerExitCode':code,'passed':True},indent=2)+'\n')
