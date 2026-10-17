"""C1c-0 r2's receipt-specific record in the open C1b batch interval (C1c plan r4, LD-C1C-9 and its R1-RF-3 and
R2-RF-2 rows), from public receipt fields only.

The batch's accepted baseline is C1a4's blind refresh (product 0772eb7): both receipts, the discovery receipt
(discovery_census_held_out.json) and the companion snapshot receipt (snapshot_ledger_census_held_out.json), current
there. C1b-0 opened the batch (product c9c18f7) and recorded that baseline's receipt pins and its own binding deltas
(c1b-0-r2/evidence/census-regeneration.json). This record checks, per receipt:
  - the baseline: the receipt's bytes on main equal the refresh's (0772eb7) and C1b-0's recorded baseline pins;
  - the batch's delta so far (main's current bindings against the receipt): exactly C1b-0's, the generator-closure
    digest in `reference`, and in the companion that same digest nested in its `discovery` binding;
  - C1c-0's own delta (the candidate's current bindings against main's): exactly what C1c-0 edits or adds;
  - the cumulative delta (the candidate's against the receipt): exactly the union of the two, every binding named
    by its top-level key and, for a pin list, by path (a new source is an added pin);
  - the candidate leaves both receipts' bytes unchanged, and its regenerated records render each receipt's held-out
    rows `outstanding: held-out (blind receipt stale)` with `heldOutMargin: outstanding`.
Only a receipt's `bindings` and `state` are read; no row, store or overlay. The bindings are computed by each
checkout's own tools, one subprocess per checkout, with the main checkout as the packages root. No network or
environment input.
Usage: receipt_specific_record.py <candidate> <main> <architecture> <out.json>
       receipt_specific_record.py --bindings <product> <architecture> <packages-root>   (internal: both bindings)"""
from pathlib import Path
import hashlib, importlib.util, json, subprocess, sys

DISCOVERY_RECEIPT = 'crates/security/src/custody/discovery_census_held_out.json'
COMPANION_RECEIPT = 'crates/security/src/snapshot_ledger_census_held_out.json'
DISCOVERY_RECORD = 'crates/security/src/custody/discovery_census.json'
SNAPSHOT_RECORD = 'crates/security/src/snapshot_ledger_census.json'
REFRESH = '0772eb7f383cdbff1c3d0869486094a95ef7693a'
C1B0_RECORD = 'docs/implementation/m3/snapshot-plan-c/c1b-0-r2/evidence/census-regeneration.json'
STALE = 'outstanding: held-out (blind receipt stale)'
RULE = 'crates/security/src/custody/discovery_rule.rs'
PIN_LISTS = ('closure', 'reference', 'tools', 'snapshotSources')
# C1b-0's binding changes (its census-regeneration.json): the generator-closure digest among the reference pins.
C1B0 = dict(discovery={'reference': ['tools/contracts/generator-closure.json']},
            companion={'discovery': {'reference': ['tools/contracts/generator-closure.json']}})
# C1c-0's own, derived from what it edits: the discovery receipt's CLOSURE row for the rule and the census tool's pin
# (its re-pinned CLOSURE); the companion's discovery bindings, the two tools it edits, and the snapshot sources it edits
# or adds that the model pins or anchors (the host session's tests among them: the session anchors read them).
C1C0 = dict(discovery={'closure': [RULE], 'tool': None},
            companion={'discovery': {'closure': [RULE], 'tool': None},
                       'tools': ['tools/security/discovery_census.py', 'tools/security/snapshot_ledger_model.py'],
                       'snapshotSources': ['crates/host/src/snapshot.rs', 'crates/host/src/snapshot_tests.rs',
                                           'crates/security/src/snapshot_read_set.rs', 'crates/security/src/snapshot_source.rs',
                                           'crates/security/src/snapshot_walk.rs']})


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


if sys.argv[1] == '--bindings':
    product, arch, packages_root = Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    census = load('snapshot_ledger_census', product / 'tools/security/snapshot_ledger_census.py')
    c = census.Census(product, arch, packages_root)
    print(json.dumps(dict(discovery=c.dc.receipt_bindings(product, arch, c.c), companion=c.bindings())))
    raise SystemExit(0)

candidate, main, arch, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])


def current(product):
    return json.loads(subprocess.check_output([sys.executable, '-I', '-B', __file__, '--bindings', str(product), str(arch), str(main)], cwd=product))


def delta(now, bound):
    """Each changed top-level binding: a pin list by its changed, added or removed paths; the nested discovery
    bindings by their own delta; any other binding as None (changed)."""
    result = {}
    for k in sorted(set(now) | set(bound)):
        a, b = now.get(k), bound.get(k)
        if a == b:
            continue
        if k in PIN_LISTS and isinstance(a, list) and isinstance(b, list):
            x, y = {r['path']: r for r in a}, {r['path']: r for r in b}
            result[k] = sorted(p for p in set(x) | set(y) if x.get(p) != y.get(p))
        elif k == 'discovery' and isinstance(a, dict) and isinstance(b, dict):
            result[k] = delta(a, b)
        else:
            result[k] = None
    return result


def union(x, y):
    result = {}
    for k in sorted(set(x) | set(y)):
        a, b = x.get(k), y.get(k)
        if isinstance(a, dict) or isinstance(b, dict):
            result[k] = union(a or {}, b or {})
        elif isinstance(a, list) or isinstance(b, list):
            result[k] = sorted(set(a or []) | set(b or []))
        else:
            result[k] = None
    return result


def sha(raw):
    return dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


main_now, cand_now = current(main), current(candidate)
c1b0 = json.loads((arch / C1B0_RECORD).read_bytes())['baseline']
doc, ok = {}, True
for name, path, record_path, entries, recorded in (('discovery', DISCOVERY_RECEIPT, DISCOVERY_RECORD, 'entries', 'discoveryReceipt'),
                                                   ('companion', COMPANION_RECEIPT, SNAPSHOT_RECORD, 'heldOutEntries', 'companionReceipt')):
    raw = (main / path).read_bytes()
    receipt = json.loads(raw)
    refresh = subprocess.check_output(['/usr/bin/git', 'show', REFRESH + ':' + path], cwd=main)
    baseline = dict(receipt=path, state=receipt['state'], pin=sha(raw), equalsRefresh=raw == refresh,
                    equalsC1b0RecordedBaseline=sha(raw) == {k: c1b0[recorded][k] for k in ('bytes', 'sha256')})
    batch, own, cumulative = delta(main_now[name], receipt['bindings']), delta(cand_now[name], main_now[name]), delta(cand_now[name], receipt['bindings'])
    record = json.loads((candidate / record_path).read_bytes())
    held = [e for e in record[entries] if isinstance(e.get('status'), str) and (e['status'].startswith('outstanding') or e['status'] == 'blind-census')]
    row = dict(baseline=baseline, receiptBytesUnchanged=(candidate / path).read_bytes() == raw,
               batchDeltaSoFar=batch, c1c0OwnDelta=own, cumulativeDelta=cumulative, cumulativeIsUnion=cumulative == union(batch, own),
               renderedHeldOutRows=len(held), allRenderedStale=bool(held) and all(e['status'] == STALE for e in held),
               heldOutMargin=record.get('heldOutMargin'))
    row['passed'] = (baseline['equalsRefresh'] and baseline['equalsC1b0RecordedBaseline'] and baseline['state'] == 'holds (blind census)'
                     and row['receiptBytesUnchanged'] and batch == C1B0[name] and own == C1C0[name] and row['cumulativeIsUnion']
                     and row['allRenderedStale'] and row['heldOutMargin'] == 'outstanding')
    ok = ok and row['passed']
    doc[name] = row
doc.update(expected=dict(c1b0=C1B0, c1c0=C1C0), refresh=REFRESH, allPassed=ok,
           standing='C1c-0 r2 receipt-specific record in the open C1b batch: each receipt against the refresh baseline, the batch so far and C1c-0\'s own bindings')
out.write_text(json.dumps(doc, indent=2) + '\n')
print(json.dumps(doc))
raise SystemExit(0 if ok else 1)
