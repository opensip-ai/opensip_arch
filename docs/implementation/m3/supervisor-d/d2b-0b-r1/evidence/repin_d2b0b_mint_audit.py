"""D2b-0b's post-generation step: the operability mint-audit census re-pinned for the regenerated carriers, as B-S10
did for its regenerated invocation.rs (c019e9e: crates/contracts/src/generated/invocation.rs `into` 135 to 150). The
count is measured by tools/check_operability.py's own mint_inventory(), never written by hand; the only difference
allowed is the generated protocol.rs's `into` calls, and every other row must already agree."""
from pathlib import Path
import importlib.util, json
W = Path('/Users/sb/code/opensip-ai/opensip-d2b0b'); EX = 'tools/operability/exceptions.json'; GEN = 'crates/contracts/src/generated/protocol.rs'
spec = importlib.util.spec_from_file_location('d2b0b_operability', W / 'tools/check_operability.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
record = json.loads((W / EX).read_bytes()); expected = record['mintAudit']['rows']; actual = m.mint_inventory(W)
key = lambda r: (r['path'], r['member'], r['kind'])
assert [key(r) for r in expected] == [key(r) for r in actual], 'the mint census rows differ in more than counts'
diff = [(e, a) for e, a in zip(expected, actual) if e != a]
assert len(diff) == 1 and key(diff[0][0]) == (GEN, 'into', 'call'), diff
before = diff[0][0]['count']; diff[0][0]['count'] = diff[0][1]['count']
assert record['mintAudit']['rows'] == actual
text = (W / EX).read_text(); new = json.dumps(record, indent=2) + '\n'
assert json.loads(text) != record and json.dumps(json.loads(text), indent=2) + '\n' == text, 'exceptions.json is not in the canonical two-space form'
(W / EX).write_text(new); print(json.dumps(dict(path=GEN, member='into', kind='call', before=before, after=diff[0][1]['count'])))
