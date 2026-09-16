"""Launcher: run a probe under the reference interpreter, capturing full receipts."""
import json, os, subprocess, sys

REF = '/tmp/opensip-architecture-review-env/bin/python'
HERE = os.path.dirname(os.path.abspath(__file__))
target = sys.argv[1]
if not os.path.isabs(target):
    target = os.path.join(HERE, target)
p = subprocess.run([REF, '-I', '-B', target] + sys.argv[2:], capture_output=True, text=True)
sys.stdout.write(p.stdout)
sys.stderr.write(p.stderr)
receipt = {'command': [REF, '-I', '-B', target] + sys.argv[2:], 'exitCode': p.returncode,
           'stdout': p.stdout, 'stderr': p.stderr}
name = os.path.basename(target).replace('.py', '') + '.receipt.json'
os.makedirs(os.path.join(HERE, 'receipts'), exist_ok=True)
json.dump(receipt, open(os.path.join(HERE, 'receipts', name), 'w'), indent=2)
print('EXIT', p.returncode)
sys.exit(p.returncode)
