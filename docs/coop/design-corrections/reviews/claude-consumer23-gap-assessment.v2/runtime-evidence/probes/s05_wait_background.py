"""S05 — bounded wait (<= 540 s) for this runtime's own background probes to finish: s02 liveness poll and p05 corrected
rehearsal. Completion is the runner's command.json. Records exit codes and elapsed time; reads nothing else."""
import json, os, sys, time

RC = '/tmp/opensip-design-corrections/claude-consumer23-gap-assessment.v2/receipts'
WANT = {'s02_poll_p04': os.path.join(RC, 's02_poll_p04', 'command.json'), 'p05_successor_rehearsal2': os.path.join(RC, 'p05_successor_rehearsal2', 'command.json')}
t0 = time.time()
while time.time() - t0 < 540:
    if all(os.path.isfile(p) for p in WANT.values()):
        break
    time.sleep(10)
state = {k: (json.load(open(p))['exit'] if os.path.isfile(p) else 'still running') for k, p in WANT.items()}
newest = None
for d, _, fs in os.walk(RC):
    for f in fs:
        if f.startswith('p05-kit-'):
            m = os.path.getmtime(os.path.join(d, f))
            if newest is None or m > newest[0]:
                newest = (m, f)
print(json.dumps({'waitedSeconds': round(time.time() - t0), 'state': state,
                  'p05NewestOutput': {'file': newest[1], 'secondsAgo': round(time.time() - newest[0])} if newest else None}, indent=1))
sys.exit(0)
