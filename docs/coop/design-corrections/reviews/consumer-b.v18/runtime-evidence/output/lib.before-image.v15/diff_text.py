"""Line diff of one kit markdown/text document between the prior disclosed kit and v15.
Locates changes only; every change is then read in full context from the v15 bytes.
"""
import difflib
import sys

V15 = '/tmp/opensip-design-corrections/consumer-b.v15/subject/'
V14 = '/tmp/opensip-design-corrections/consumer-b' + '.v14' + '/subject/'

rel = sys.argv[1]
a = open(V14 + rel, encoding='utf-8').read().splitlines()
b = open(V15 + rel, encoding='utf-8').read().splitlines()
n = 0
for line in difflib.unified_diff(a, b, 'prior', 'v15', lineterm='', n=2):
    print(line[:400])
    n += 1
    if n > int(sys.argv[2] if len(sys.argv) > 2 else 400):
        print('... (truncated)')
        break
print('--- old lines %d, new lines %d' % (len(a), len(b)))
