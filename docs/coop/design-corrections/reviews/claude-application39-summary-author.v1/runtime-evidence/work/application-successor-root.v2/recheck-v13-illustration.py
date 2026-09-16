from pathlib import Path
import hashlib,json,importlib.util
r=Path.cwd();p=r/'docs/coop/design-corrections/foundation/canonical.py';s=importlib.util.spec_from_file_location('count_c',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
rows=[]
for label,names in [('short',[f'c{i}' for i in range(21)]),('medium',[f'cb-crate-{i:02d}' for i in range(21)]),('long',[f'opensip-workspace-component-number-{i:02d}' for i in range(21)])]:
 value={n:2021 for n in names};raw=m.canonical(value);rows.append({'label':label,'map':value,'canonicalText':raw.decode(),'bytes':len(raw),'exceeds255':len(raw)>255})
assert [x['bytes'] for x in rows]==[222,400,946]
o=r/'docs/coop/design-corrections/reviews/codex-post-reset.v1/v13-crate-illustration-recheck.v1.json';assert not o.exists();o.write_text(json.dumps({'standing':'Codex reproduction of actual independent reviewer illustrative map-size examples. Synthetic canonical integer edition maps, not real workspace execution or a universal crate threshold.','canonicalSource':{'path':str(p.relative_to(r)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()},'rows':rows,'priorFailedAttempt':'An initial system-python invocation failed at importing jsonschema before any measurement or output record. This execution uses the declared isolated review environment; the environment error is not a design finding.'},indent=2)+'\n');print([(r['label'],r['bytes']) for r in rows])
