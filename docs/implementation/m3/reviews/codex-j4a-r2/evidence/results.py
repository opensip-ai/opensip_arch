#!/usr/bin/env python3
"""Summarize J4a's lane logs (lanes.sh) into results.json: each step's exit and
seconds, and the cargo test totals per test lane. Reads only the logs."""
import json, re, sys
from pathlib import Path

lanes = Path(sys.argv[1])
steps = {}
for line in (lanes / 'summary.txt').read_text().splitlines():
    m = re.match(r'(\S+) exit=(\d+) seconds=(\d+)$', line)
    if m:
        steps[m.group(1)] = {'exit': int(m.group(2)), 'seconds': int(m.group(3))}
totals = {}
for name in ('ws1', 'ws2', 'ws-doc', 'feature'):
    log = lanes / f'{name}.log'
    if not log.exists():
        continue
    passed = failed = ignored = binaries = 0
    for m in re.finditer(r'test result: (\w+)\. (\d+) passed; (\d+) failed; (\d+) ignored', log.read_text()):
        binaries += 1
        passed += int(m.group(2)); failed += int(m.group(3)); ignored += int(m.group(4))
    totals[name] = {'passed': passed, 'failed': failed, 'ignored': ignored, 'testBinaries': binaries}
out = {'steps': steps, 'tests': totals}
(lanes / 'results.json').write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
print(json.dumps(out, sort_keys=True))
