"""CI-PT-4 for CI-1 (plan r3 LD-CIP-8): the changed-file set misses every bound input of both census receipts, as the
receipts' own binding code names them, and the four committed receipt files are byte-equal to base. The discovery
receipt binds (receipt_bindings) its tool, CLOSURE, the member model and the reference-loading product sources; the
companion receipt binds (bindings) those, its four tools and snapshotSources (sources(): the model's snapshot files and
anchors, the session files and anchors, the work ledger and ANCHORED). Sizes, caps and limits are read by that code
from those same files. No census mode is run: the --check modes need the T2 cache, which this unit may not read.
Usage: receipt_inputs.py PRODUCT_WORKTREE OUT_JSON"""
import importlib.util, json, subprocess, sys
from pathlib import Path
W = Path(sys.argv[1]); OUT = Path(sys.argv[2])
def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, W / rel); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
dc = load('discovery_census', 'tools/security/discovery_census.py')
slm = load('snapshot_ledger_model', 'tools/security/snapshot_ledger_model.py')
sl = load('snapshot_ledger_census', 'tools/security/snapshot_ledger_census.py')
discovery = {dc.TOOL, dc.MEMBER_MODEL} | {p for p, _, _ in dc.CLOSURE} | set(dc.REFERENCE_PRODUCT)
sources = set(slm.SNAPSHOT_FILES) | {p for _, p, _ in slm.SNAPSHOT_ANCHORS} | {p for _, p, _, _ in slm.SESSION_ANCHORS}
sources |= set(slm.SESSION_FILES) | {slm.WORK_LEDGER} | set(sl.ANCHORED)
companion = discovery | {sl.TOOL, sl.MODEL, sl.DISCOVERY, sl.MEMBER_MODEL} | sources
receipts = ['crates/security/src/custody/discovery_census.json', 'crates/security/src/custody/discovery_census_held_out.json',
            sl.OUTPUT, sl.OUTPUT_RECEIPT]
git = lambda *a: subprocess.check_output(['/usr/bin/git', *a], cwd=W).decode()
changed = sorted(set(git('diff', '--name-only', 'HEAD').split()) | set(git('ls-files', '--others', '--exclude-standard').split()))
missing = sorted(p for p in companion if not (W / p).is_file())
hit = dict(discovery=sorted(discovery & set(changed)), companion=sorted(companion & set(changed)), receipts=sorted(set(receipts) & set(changed)))
equal = {r: (W / r).read_bytes() == subprocess.check_output(['/usr/bin/git', 'show', 'HEAD:' + r], cwd=W) for r in receipts}
ok = not any(hit.values()) and all(equal.values()) and not missing and len(dc.CLOSURE) >= 10 and len(sources) >= 10
OUT.write_text(json.dumps(dict(changed=changed, discoveryBound=sorted(discovery), companionBound=sorted(companion), receipts=receipts,
                               receiptsByteEqualBase=equal, hit=hit, missingBoundFiles=missing, passed=ok), indent=2) + '\n')
print(len(discovery), 'discovery-bound;', len(companion), 'companion-bound;', 'changed', changed, '; hit', hit, '; passed', ok)
sys.exit(0 if ok else 1)
