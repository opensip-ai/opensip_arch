"""C1b-0's stale-receipt record (the base's own stale set, from C1a4 and D2b-0b, is recorded row by row and apart from C1b-0's change) (C1b plan r3, LD-C1B-7 and its R2-RF-1 rule), separate from the census output checks:
the blind held-out receipt's bindings, recomputed by the census tool's own receipt_bindings(), differ between the base
and the candidate in exactly one place: the reference-loading pin of tools/contracts/generator-closure.json (the
base's, then the candidate's). Bindings already stale on the base are recorded as such. No census output embeds that
digest, so both output --check commands pass with no regeneration; this check records the stale receipt from public
fields only: the changed bindings, the receipt's bytes (equal to the base's), and the census record's rendered held-out
rows (their count, status and heldOutMargin), never a held-out store or content. The snapshot census's own cost-source
pins (snapshot_ledger_census.py:261-262) are asserted unchanged. Read-only; opens no T2 data. (Adapted from D2b-0b's
check_d2b0b_census_stale.py.) Usage: <out json> [census --check log]."""
from pathlib import Path
import hashlib, importlib.util, json, re, sys
W = Path('/Users/sb/code/opensip-ai/opensip-c1b0'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
spec = importlib.util.spec_from_file_location('c1b0_census', W / 'tools/security/discovery_census.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
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
def rows_differing(x, y):
    if isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        return [dict(stored=u, base=v) for u, v in zip(x, y) if u != v]
    return [dict(stored=x, base=y)]
# The stale set already on the base (C1a4's and D2b-0b's changes), kept apart from C1b-0's own change, row by row and
# from public bindings only.
stale_on_base_rows = {k: rows_differing(stored.get(k), base.get(k)) for k in stale_on_base}
out = dict(baseBindingsEqualStored=base == stored, receiptStaleOnBaseKeys=stale_on_base, receiptStaleOnBaseRows=stale_on_base_rows, differingBindingKeys=differing, referenceRowsDiffering=[dict(stored=s, current=c) for s, c in ref_diff],
           closurePinBase=pin(P, closure), closurePinCandidate=pin(W, closure), receiptByteEqualBase=True, renderedHeldOutRows=rendered, censusCheckLogTail=log[-2000:])
ok = (differing == ['reference'] and len(base['reference']) == len(current['reference']) and len(ref_diff) == 1
      and ref_diff[0][0] == pin(P, closure) and ref_diff[0][1] == pin(W, closure)
      and bool(held) and rendered['statuses'] == ['outstanding: held-out (blind receipt stale)'] and record['heldOutMargin'] == 'outstanding')
for p in (m.TOOL, 'tools/security/snapshot_ledger_model.py', 'tools/security/snapshot_ledger_census.py', 'tools/security/discovery_member_model.py',
          'crates/host/src/snapshot_seal.rs', 'crates/platform/src/work_ledger.rs', 'crates/security/src/custody/discovery_census.json',
          'crates/security/src/snapshot_ledger_census.json'):
    if (P / p).exists() or (W / p).exists():
        assert (W / p).read_bytes() == (P / p).read_bytes(), p
out['snapshotCensusInputsUnchanged'] = True
out['exactlyTheClosureDigest'] = ok
Path(sys.argv[1]).write_text(json.dumps(out, indent=2) + '\n'); print(json.dumps({k: out[k] for k in ('baseBindingsEqualStored', 'receiptStaleOnBaseKeys', 'differingBindingKeys', 'exactlyTheClosureDigest')}))
sys.exit(0 if ok else 1)
