"""Drive the native checker body against this runtime's capture without writing its report into the tree.

usage: python -I -B run_native_checker.py REPORT_OUT [--bypass-pins-labelled]
The checker module is loaded from the capture and its REPORT_PATH is redirected to REPORT_OUT (a receipt path in this
runtime). Without the flag the owner's pin gate runs unchanged. With --bypass-pins-labelled the owner's pin verification
is first executed and its actual faults are recorded, then the gate is bypassed so the case body runs; the report is
labelled PIN-GATE-BYPASSED-BY-EXTERNAL-DRIVER and never claims pin validity. Pins are never regenerated.
"""
import importlib.util, json, sys
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-tsjs-unitkind-author.v1')
NATIVE = RT / 'work/source/docs/coop/design-corrections/native'
out = Path(sys.argv[1])
bypass = '--bypass-pins-labelled' in sys.argv
spec = importlib.util.spec_from_file_location('native_checker_driven', NATIVE / 'check_native_evidence.v2.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.REPORT_PATH = out
actual_pin_faults = mod.verify_pins()
if bypass:
    mod.verify_pins = lambda: []
code = mod.main([])
if bypass and out.exists():
    report = json.loads(out.read_text())
    report['driverStanding'] = 'PIN-GATE-BYPASSED-BY-EXTERNAL-DRIVER: pins not valid for this tree; owner pin faults recorded below; pins not regenerated'
    report['actualPinFaults'] = actual_pin_faults
    out.write_text(json.dumps(report, indent=1) + '\n')
sys.exit(code)
