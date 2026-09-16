"""P20: final integrity — assessment parses, inputs untouched, deliverables listed."""
import json, os

RT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json.load(open(os.path.join(RT, 'assessment.json')))
print('assessment.json parses OK')

for root in ('/tmp/opensip-design-corrections/candidate-subject.v32',
             '/tmp/opensip-design-corrections/consumer-b.v19',
             '/tmp/opensip-design-corrections/root-blind19-final-source32.v1',
             '/tmp/opensip-design-corrections/root-blind19-execution-disagreement.v1'):
    n = sum(len(f) for _d, _s, f in os.walk(root))
    print('%-68s %6d files (read-only this session)' % (root, n))

print('\ndeliverables in this runtime:')
total = 0
for dp, _d, fs in os.walk(RT):
    for f in sorted(fs):
        total += 1
        if dp == RT:
            print('  %9d  %s' % (os.path.getsize(os.path.join(dp, f)), f))
print('  probes/ + probes/receipts/ : %d further files' % (total - len(os.listdir(RT))))
print('total runtime artifacts:', total)
