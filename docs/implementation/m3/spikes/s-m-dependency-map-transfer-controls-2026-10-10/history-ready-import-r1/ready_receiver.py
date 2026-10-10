"""Ready handshake for the outside-product transfer probe; source is never executed."""
import sys,json
from receiver import receive
print('ready',flush=True)
try:print(json.dumps(receive(sys.stdin.buffer),sort_keys=True))
except Exception as error:print(type(error).__name__+': '+str(error),file=sys.stderr);sys.exit(2)
