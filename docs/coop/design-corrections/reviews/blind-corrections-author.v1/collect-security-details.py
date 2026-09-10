"""Disposable probe: run every security case and sweep and collect every refusal/detail string the
model actually emits, so the closed public-detail set is derived from real emission paths."""
import importlib.util, json, sys
from pathlib import Path
R = Path(sys.argv[1]); S = R / 'docs/coop/design-corrections/security'
sys.argv = ['check', '--report', '/tmp/opensip-design-corrections/blind-corrections-author.v1/evidence/_probe.json']
spec = importlib.util.spec_from_file_location('chk', S / 'check-security-lifecycle.v1.py')
chk = importlib.util.module_from_spec(spec)
seen = {'refusal': set(), 'detail': set(), 'refusals': set()}

def harvest(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('refusal', 'detail') and isinstance(v, str):
                seen[k].add(v)
            elif k in ('refusals', 'reasons', 'warnings') and isinstance(v, list):
                for x in v:
                    if isinstance(x, str): seen['refusals'].add(x)
            harvest(v)
    elif isinstance(o, list):
        for v in o: harvest(v)

spec.loader.exec_module(chk)
orig = chk.model.run_case
def patched(name, inp):
    out = orig(name, inp); harvest(out); return out
chk.model.run_case = patched
try:
    chk.main()
except SystemExit:
    pass
report = json.loads(Path('/tmp/opensip-design-corrections/blind-corrections-author.v1/evidence/_probe.json').read_text())
harvest(report)
print(json.dumps({k: sorted(v) for k, v in seen.items()}, indent=1))
