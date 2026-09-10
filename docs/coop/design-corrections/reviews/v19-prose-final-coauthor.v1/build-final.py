"""Emit the two bounded corrections, byte-verified against the captured read-only inputs.

Correction 1: precedence-final.md — root's exact precedence-proposed.md bytes (assessed sound).
Correction 2: scope-remedy-{before,after}.py — the ONE SCOPE_LIMIT_REMEDY value.
Nothing else is written; no captured input is modified.
"""
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------- correction 1
proposed = (HERE / 'precedence-proposed.md').read_bytes()
prior = Path('/tmp/opensip-design-corrections/v19-precedence-coauthor.v1/after-paragraph.md').read_bytes()
(HERE / 'precedence-final.md').write_bytes(proposed)
assert (HERE / 'precedence-final.md').read_bytes() == proposed, 'exact-byte emission'

# ---------------------------------------------------------------- correction 2
model = (HERE / 'native-model.observed.py').read_bytes()
assert hashlib.sha256(model).hexdigest() == \
    '9663ef2bccece114c740f2f09c86cddbbb558f9cc82086effee432ef0c2f2add'

BEFORE = (
    b'    "nativeContextDigests": ("narrow the analysis explicitly - fewer workspace roots for this invocation; "\n'
    b'                             "no context was truncated, and units that genuinely share one compiler closure, "\n'
    b'                             "standard library and effective options already collapse to one member"),\n'
)
AFTER = (
    b'    "nativeContextDigests": ("narrow the analysis explicitly - fewer workspace roots for this invocation; "\n'
    b'                             "no context was truncated"),\n'
)
assert model.count(BEFORE) == 1, model.count(BEFORE)

spliced = model.replace(BEFORE, AFTER)
assert spliced.count(AFTER) == 1 and spliced.replace(AFTER, BEFORE) == model

(HERE / 'scope-remedy-before.py').write_bytes(BEFORE)
(HERE / 'scope-remedy-after.py').write_bytes(AFTER)

# the emitted value is EXACTLY root's proposed sentence, and only this key changes
ns_b, ns_a = {}, {}
exec(b'D = {\n' + BEFORE + b'}\n', ns_b)
exec(b'D = {\n' + AFTER + b'}\n', ns_a)
val_before = ns_b['D']['nativeContextDigests']
val_after = ns_a['D']['nativeContextDigests']
ROOT_VALUE = ('narrow the analysis explicitly - fewer workspace roots for this '
              'invocation; no context was truncated')
assert val_after == ROOT_VALUE, repr(val_after)
assert set(ns_b['D']) == set(ns_a['D']) == {'nativeContextDigests'}

def rep(tag, b):
    b.decode('utf-8')
    print('%-24s bytes=%-5d chars=%-5d lines=%-3d maxwidth=%-4d sha256=%s'
          % (tag, len(b), len(b.decode()), b.decode().count('\n'),
             max(len(l) for l in b.decode().splitlines()), hashlib.sha256(b).hexdigest()))

rep('precedence-proposed', proposed)
rep('precedence-final', (HERE / 'precedence-final.md').read_bytes())
rep('prior after-paragraph', prior)
rep('scope-remedy-before', BEFORE)
rep('scope-remedy-after', AFTER)
print()
print('precedence-final == root proposal byte-for-byte:', proposed == (HERE / 'precedence-final.md').read_bytes())
print('remedy value before:', repr(val_before))
print('remedy value after :', repr(val_after))
print('value == root proposal exactly:', val_after == ROOT_VALUE)
print('model sha256 (unmodified):', hashlib.sha256(model).hexdigest())
print('spliced-model sha256 (NOT written, rebase arithmetic only):',
      hashlib.sha256(spliced).hexdigest())
print('other SCOPE_LIMIT_REMEDY entries touched: 0')
