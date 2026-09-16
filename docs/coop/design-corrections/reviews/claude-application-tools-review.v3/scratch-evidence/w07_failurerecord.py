"""W07: independently check the preserved preparation-failure record's custody claim -
that the flattened review-only finalizer copy and the staged files/ copy are identical.
"""
import hashlib
import json
import os

V3 = '/private/tmp/opensip-design-corrections/claude-application-tools-review.v3'
V2 = '/tmp/opensip-design-corrections/claude-application-tools-review.v2'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()

flat = os.path.join(V3, 'inputs/finalize-application.v1.py')
staged = os.path.join(V3, 'inputs/files/docs/coop/design-corrections/finalize-application.v1.py')
v2flat = os.path.join(V2, 'inputs/finalize-application.v1.py')
v2staged = os.path.join(V2, 'inputs/files/docs/coop/design-corrections/finalize-application.v1.py')
print('v3 flattened  :', sha(flat))
print('v3 staged     :', sha(staged))
print('v2 flattened  :', sha(v2flat))
print('v2 staged     :', sha(v2staged))
print('all four identical:', len({sha(flat), sha(staged), sha(v2flat), sha(v2staged)}) == 1)

# The assembler pin must still name these exact bytes.
import ast
src = open(os.path.join(V3, 'inputs/assemble-records.successor.v1.py')).read()
pins = None
for n in ast.walk(ast.parse(src)):
    if (isinstance(n, ast.Assign) and len(n.targets) == 1
            and getattr(n.targets[0], 'id', '') == 'selected_support'):
        pins = ast.literal_eval(n.value)
print('assembler pins unchanged and matching:', json.dumps(
    {k: (v == sha(os.path.join(V3, 'inputs/files', k))) for k, v in pins.items()}))
print('no Claude process was launched by the failed preparation: attested by the record; '
      'not independently verifiable from these inputs')
