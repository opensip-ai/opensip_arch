"""Run the native checker with the pin gate bypassed (pins are Codex's; expected to mismatch until the final re-pin).
The report is written to the path given as argv[1], not into the repository."""
import importlib.util, sys
from pathlib import Path
HERE = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/native')
spec = importlib.util.spec_from_file_location('chk', HERE / 'check_native_evidence.v2.py'); chk = importlib.util.module_from_spec(spec); spec.loader.exec_module(chk)
chk.verify_pins = lambda: []
chk.REPORT_PATH = Path(sys.argv[1])
sys.exit(chk.main([]))
