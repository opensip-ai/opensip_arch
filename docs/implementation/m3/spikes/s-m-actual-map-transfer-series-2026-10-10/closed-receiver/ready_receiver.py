"""Ready handshake for the outside-product transfer probe; source is never executed."""
import sys,json
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('owned_receiver',Path(__file__).with_name('receiver.py'))
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
receive=module.receive
print('ready',flush=True)
try:print(json.dumps(receive(sys.stdin.buffer),sort_keys=True))
except Exception as error:print(type(error).__name__+': '+str(error),file=sys.stderr);sys.exit(2)
