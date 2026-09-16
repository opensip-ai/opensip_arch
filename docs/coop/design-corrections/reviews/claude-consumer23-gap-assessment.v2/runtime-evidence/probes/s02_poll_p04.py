"""S02 — bounded poll of the interrupted v1 p04 rehearsal: every 15 s for up to 660 s, record the newest write among p04
outputs and the kit, and whether the summary receipt or the runner's command.json appears. File metadata only; no process
listing, no writes to v1. If nothing changes for far longer than any launcher child's observed runtime (<= 130 s in root's and
my own runs), the run is concluded dead."""
import json, os, time

V1 = '/tmp/opensip-design-corrections/claude-consumer23-gap-assessment.v1'
RC1 = os.path.join(V1, 'receipts')
KIT = os.path.join(V1, 'disposable/kit36-successor')
OUT = '/tmp/opensip-design-corrections/claude-consumer23-gap-assessment.v2/receipts'
iso = lambda t: time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(t))


def newest():
    best = (0.0, None)
    for root in (RC1, KIT):
        for d, _, fs in os.walk(root):
            for f in fs:
                p = os.path.join(d, f)
                if root == RC1 and 'p04' not in os.path.relpath(p, RC1):
                    continue
                try:
                    m = os.path.getmtime(p)
                except OSError:
                    continue
                if m > best[0]:
                    best = (m, os.path.relpath(p, V1))
    return best


start = time.time()
first = newest()
samples = []
changed = False
done = False
while time.time() - start < 660:
    cur = newest()
    summary = os.path.isfile(os.path.join(RC1, 'p04-successor-rehearsal.json'))
    runner = os.path.isfile(os.path.join(RC1, 'p04_successor_rehearsal', 'command.json'))
    samples.append({'t': iso(time.time()), 'newest': cur[1], 'newestUtc': iso(cur[0]), 'summary': summary, 'runnerCommand': runner})
    if cur[0] > first[0]:
        changed = True
    if summary or runner:
        done = True
        break
    time.sleep(15)
R = {'startUtc': iso(start), 'endUtc': iso(time.time()), 'initialNewest': {'path': first[1], 'utc': iso(first[0])}, 'anyNewWriteDuringPoll': changed,
     'completedDuringPoll': done, 'samples': samples[::4] + samples[-1:],
     'conclusion': ('p04 COMPLETED' if done else 'p04 STILL WRITING (alive)' if changed else
                    'p04 NOT ACTIVE: no p04 or kit write for the whole poll window plus the preceding interval; its summary receipt and runner command.json never appeared; it was stopped when the previous CLI process ended')}
print(json.dumps({k: v for k, v in R.items() if k != 'samples'}, indent=1))
json.dump(R, open(os.path.join(OUT, 's02-poll-p04.json'), 'w'), indent=1)
print('wrote s02-poll-p04.json')
