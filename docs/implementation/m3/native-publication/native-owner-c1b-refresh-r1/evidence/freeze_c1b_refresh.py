"""The C1b batch refresh's freeze (C1b plan r6 LD-C1B-7; the pre-run gate's frozen final input bindings and current
receipt bindings), from public fields only. Run on product main once C1b-2, the batch's last unit, is integrated. It
records:
  - the freeze base (main's HEAD) and the architecture head;
  - the five tools' bytes and the architecture-side bound inputs' bytes (the corpus manifest and discovery's
    reference-loading sources, as the discovery receipt binds them);
  - **the frozen final input bindings:** both receipts' bindings as each tool's own binding function computes them on
    main (discovery's `receipt_bindings`; the companion's `Census.bindings`), in full;
  - **the current receipt bindings:** the committed receipts' pins, state and `bindings`, which are still the 0772eb7
    refresh's bytes;
  - the cumulative delta per receipt (the frozen bindings against the committed receipt's), which must be exactly the
    union of the joined units' accepted own deltas, the units read as data from joined-units.json beside this script
    (the lead's LD-CBR-3: C2b-0 and C1c-1 may join before the freeze). Each joined unit's product commit must be on main
    and recorded in CURRENT-STATE under its publication.
Only a receipt's `bindings` and `state` are read: no row, store, overlay or cache. No network or environment input.
Usage: freeze_c1b_refresh.py <out json>
       freeze_c1b_refresh.py --bindings <product> <architecture> <packages-root>   (internal: both bindings)"""
from pathlib import Path
import hashlib, importlib.util, json, subprocess, sys

A = Path('/Users/sb/code/opensip-ai/opensip_arch'); P = A.parent / 'opensip'
PRE = 'docs/implementation/m3/snapshot-plan-c/'
S = Path('/tmp/opensip-implementation/native-owner-patterns-2026-10-20/combined-refresh-r1/architecture').resolve()
REFRESH = '0772eb7f383cdbff1c3d0869486094a95ef7693a'
DISCOVERY_RECEIPT = 'crates/security/src/custody/discovery_census_held_out.json'
COMPANION_RECEIPT = 'crates/security/src/snapshot_ledger_census_held_out.json'
TOOLS = ('tools/security/discovery_census.py', 'tools/security/discovery_member_model.py', 'tools/security/snapshot_ledger_census.py',
         'tools/security/snapshot_ledger_model.py', 'tools/security/discovery_workspace_ledger.py')
ARCH_INPUTS = ('docs/implementation/m3/corpus/t2-corpus-manifest.draft.json',
               'docs/implementation/m3/config-discovery-b/b2-b-reference/reference/discovery_scan_reference.py',
               'docs/coop/design-corrections/security/security_lifecycle_model_v1.py',
               'docs/implementation/m3/config-discovery-b/b2-a-reference/reference/discovery-defaults.sx1-r1.py',
               'docs/coop/design-corrections/foundation/canonical.py')
# The joined units, as data (LD-CBR-3), in integration order.
JOINED = Path(__file__).resolve().parent / 'joined-units.json'
STATE = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06/CURRENT-STATE.json')
PIN_LISTS = ('closure', 'reference', 'tools', 'snapshotSources')


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


def delta(now, bound):
    """Each changed top-level binding: a pin list by its changed, added or removed paths; the nested discovery
    bindings by their own delta; any other binding as None (changed). (receipt_specific_record.py's.)"""
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


def pin(root, rel):
    raw = (root / rel).read_bytes(); return dict(path=rel, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


git = lambda *a: subprocess.check_output(['/usr/bin/git', *a], cwd=P).decode().strip()
assert git('status', '--porcelain') == '', 'main must be clean'
frozen = json.loads(subprocess.check_output([sys.executable, '-I', '-B', __file__, '--bindings', str(P), str(A), str(P)], cwd=P))
joined = json.loads(JOINED.read_bytes())['joined']
state = json.loads(STATE.read_bytes())
expected = {'discovery': {}, 'companion': {}}
units = []
for entry in joined:
    assert state.get(entry['publication'], {}).get('productCode') == entry['productCode'], ('not the recorded integration', entry['unit'])
    assert subprocess.run(['/usr/bin/git', 'merge-base', '--is-ancestor', entry['productCode'], 'HEAD'], cwd=P).returncode == 0, ('not on main', entry['unit'])
    if entry['ownDeltaKey'] is None:
        own = entry['ownDelta']  # the batch's opening unit: its accepted record states its own delta in prose and pins
    else:
        record = json.loads((A / entry['record']).read_bytes()); assert record['allPassed'], entry['record']
        own = {n: record[n][entry['ownDeltaKey']] for n in ('discovery', 'companion')}
    units.append(dict(unit=entry['unit'], productCode=entry['productCode'], record=pin(A, entry['record']), ownDelta=own))
    expected = {n: union(expected[n], own[n]) for n in expected}
receipts = {}
ok = True
for name, rel in (('discovery', DISCOVERY_RECEIPT), ('companion', COMPANION_RECEIPT)):
    raw = (P / rel).read_bytes(); receipt = json.loads(raw)
    refresh = subprocess.check_output(['/usr/bin/git', 'show', REFRESH + ':' + rel], cwd=P)
    cumulative = delta(frozen[name], receipt['bindings'])
    receipts[name] = dict(receipt=pin(P, rel), state=receipt['state'], bytesEqualRefresh=raw == refresh, bindings=receipt['bindings'],
                          cumulativeDelta=cumulative, expectedCumulativeDelta=expected[name], cumulativeIsTheBatchsUnion=cumulative == expected[name])
    ok = ok and raw == refresh and receipt['state'] == 'holds (blind census)' and cumulative == expected[name]
out = dict(standing='C1b batch refresh freeze: frozen final input bindings and current receipt bindings, public fields only',
           freezeBase=git('rev-parse', 'HEAD'), architectureHead=subprocess.check_output(['/usr/bin/git', 'rev-parse', 'HEAD'], cwd=A).decode().strip(),
           refreshBaseline=REFRESH, tools=[pin(P, t) for t in TOOLS], architectureInputs=[pin(A, x) for x in ARCH_INPUTS],
           joinedUnits=pin(S, JOINED.relative_to(S).as_posix()),
           frozenBindings=frozen, receipts=receipts, units=units, passed=ok)
Path(sys.argv[1]).write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(dict(freezeBase=out['freezeBase'], passed=ok, cumulative={n: receipts[n]['cumulativeDelta'] for n in receipts})))
raise SystemExit(0 if ok else 1)
