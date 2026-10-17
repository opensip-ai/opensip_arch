"""D2b-0b's expected stale receipt (LD-D2B-1, as amendment A1 assigns the refresh): the blind held-out receipt's
bindings, recomputed by the census tool's own receipt_bindings(), differ between the base and the candidate in exactly
one place: the reference-loading pin of tools/contracts/generator-closure.json (the base's, then the candidate's). The
receipt is already stale on the base (C1a4 changed the census tool and closure); those differences are recorded, and
D2b-0b adds only the closure digest. No census output embeds that digest, so the census --check passes with no
regeneration; this check records the stale receipt separately, from public fields only: the changed bindings, the
receipt's bytes (equal to the base's), and the census record's rendered held-out rows (their count, status and
heldOutMargin), never a held-out store or content. Read-only; opens no T2 data. Usage: <out json> [census --check log]."""
from pathlib import Path
import hashlib, importlib.util, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-d2b0b'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
spec = importlib.util.spec_from_file_location('d2b0b_census', W / 'tools/security/discovery_census.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
assert (W / m.TOOL).read_bytes() == (P / m.TOOL).read_bytes()
def pin(root, p): raw = (root / p).read_bytes(); return dict(path=p, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
stored = json.loads((W / m.OUTPUT_RECEIPT).read_bytes())['bindings']
assert (W / m.OUTPUT_RECEIPT).read_bytes() == (P / m.OUTPUT_RECEIPT).read_bytes()
current = m.receipt_bindings(W, A, m.costs(W)); base = m.receipt_bindings(P, A, m.costs(P))
closure = 'tools/contracts/generator-closure.json'
differing = sorted(k for k in set(base) | set(current) if base.get(k) != current.get(k))
ref_diff = [(s, c) for s, c in zip(base['reference'], current['reference']) if s != c]
stale_on_base = sorted(k for k in set(stored) | set(base) if stored.get(k) != base.get(k))
log = Path(sys.argv[2]).read_text(errors='replace') if len(sys.argv) > 2 else ''
REC = 'crates/security/src/custody/discovery_census.json'; record = json.loads((W / REC).read_bytes())
held = [e for e in record['entries'] if isinstance(e.get('status'), str) and e['status'].startswith('outstanding')]
rendered = dict(heldOutRows=len(held), statuses=sorted({e['status'] for e in held}), heldOutMargin=record['heldOutMargin'],
                recordByteEqualBase=(W / REC).read_bytes() == (P / REC).read_bytes())
out = dict(baseBindingsEqualStored=base == stored, receiptStaleOnBaseKeys=stale_on_base, differingBindingKeys=differing, referenceRowsDiffering=[dict(stored=s, current=c) for s, c in ref_diff],
           closurePinBase=pin(P, closure), closurePinCandidate=pin(W, closure), receiptByteEqualBase=True, renderedHeldOutRows=rendered, censusCheckLogTail=log[-2000:])
ok = (differing == ['reference'] and len(base['reference']) == len(current['reference']) and len(ref_diff) == 1
      and ref_diff[0][0] == pin(P, closure) and ref_diff[0][1] == pin(W, closure)
      and bool(held) and rendered['statuses'] == ['outstanding: held-out (blind receipt stale)'] and record['heldOutMargin'] == 'outstanding')
out['exactlyTheClosureDigest'] = ok
Path(sys.argv[1]).write_text(json.dumps(out, indent=2) + '\n'); print(json.dumps({k: out[k] for k in ('baseBindingsEqualStored', 'receiptStaleOnBaseKeys', 'differingBindingKeys', 'exactlyTheClosureDigest')}))
sys.exit(0 if ok else 1)
