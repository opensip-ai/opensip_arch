"""V02: F6 verification - selected support pins, portable HERE-relative path,
and the root's claim that the finalizer bytes equal the original.
"""
import ast
import hashlib
import os

V2 = '/private/tmp/opensip-design-corrections/claude-application-tools-review.v2/inputs'
V1 = '/tmp/opensip-design-corrections/claude-application-tools-review.v1/inputs'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()

# Extract the pin dict literally from the assembler source (no execution).
src = open(os.path.join(V2, 'assemble-records.successor.v1.py')).read()
pins = None
for n in ast.walk(ast.parse(src)):
    if (isinstance(n, ast.Assign) and len(n.targets) == 1
            and getattr(n.targets[0], 'id', '') == 'selected_support'):
        pins = ast.literal_eval(n.value)
print('declared selected_support pins:')
for k, v in sorted(pins.items()):
    print('  ', k, '=', v)

print()
for rel, expected in sorted(pins.items()):
    p = os.path.join(V2, 'files', rel)
    exists = os.path.isfile(p)
    got = sha(p) if exists else None
    print('pin check |', rel)
    print('   staged source exists:', exists, '| path: inputs/files/' + rel)
    print('   sha256 matches pin  :', got == expected, '|', got)

# Root's claim: finalizer bytes unchanged, equal to the original top-level input.
fin_files = os.path.join(V2, 'files/docs/coop/design-corrections/finalize-application.v1.py')
fin_top_v2 = os.path.join(V2, 'finalize-application.v1.py')
fin_top_v1 = os.path.join(V1, 'finalize-application.v1.py')
print()
print('finalizer files/ copy   :', sha(fin_files))
print('finalizer v2 top-level  :', sha(fin_top_v2))
print('finalizer v1 top-level  :', sha(fin_top_v1))
print('ALL THREE IDENTICAL     :', sha(fin_files) == sha(fin_top_v2) == sha(fin_top_v1))
print('equals pinned constant  :', sha(fin_files) == pins['docs/coop/design-corrections/finalize-application.v1.py'])

# Portability: is the copy source now HERE-relative rather than an absolute /tmp path?
abs_literals = [n.value for n in ast.walk(ast.parse(src))
                if isinstance(n, ast.Constant) and isinstance(n.value, str)
                and n.value.startswith('/tmp/')]
print()
print('absolute /tmp literals remaining in assembler:', abs_literals)
print('support_source expression present:', 'HERE / ' + "'files'" in src or "HERE / 'files'" in src)

# The generator is new in v2; confirm it was absent from v1 inputs.
gen = 'docs/operations/generate-current-design-catalog.py'
print()
print('generator present in v2 inputs/files:', os.path.isfile(os.path.join(V2, 'files', gen)))
print('generator present anywhere in v1 inputs:', os.path.isfile(os.path.join(V1, 'files', gen)))
print('generator bytes:', os.path.getsize(os.path.join(V2, 'files', gen)))
