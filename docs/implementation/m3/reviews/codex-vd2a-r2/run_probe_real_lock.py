"""Lead evidence for VD2-a r2 (not a subject member): run law VD2's evidence/probe_real_lock.py unchanged except for
two reads of unbound SD-7 r1 draft files, which SD-7 r2's drafting replaced in place.

The probe reads SD-7 r1's NE7 copy (sd-7/contracts/native-evidence.md) and draft record (sd-7/successor.json) only as
reference texts: NE7 supplies the R1 rows and the fold target, and the r1 record is case R5's unbound target. Both
are retained, tracked, in reviews/grok-sd-7-r2/r1-members/. This runner checks those copies against the pins the law
records (NE7 380,848 B, 0dd155c2...; r1 record 5,440 B, c1b9baa7..., Codex's VD2-a r1 probe-context.json), then
executes the probe with exactly those two reads redirected. The tool, the lock, every bound architecture read and
the 17 cases are unchanged. Codex's VD2-a r1 review made the same substitution from its own retained copies.
Usage: python3.14 -I -B run_probe_real_lock.py [probe_real_lock.py arguments]"""
import hashlib, sys
from pathlib import Path
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
PROBE = A / 'docs/implementation/m3/verify-design-vd2/evidence/probe_real_lock.py'
R1 = A / 'docs/implementation/m3/reviews/grok-sd-7-r2/r1-members'
PINS = {'sd-7/contracts/native-evidence.md': (380848, '0dd155c2e2439b2223cdcfaec2ecad61c89bcf6a348f3be3c8f3350e9555ebd3'),
        'sd-7/successor.json': (5440, 'c1b9baa76f0b888300cd72696d5b3e73ca5c94bdd3fdbd6e7a6249ab71914a4d')}
for rel, (size, digest) in PINS.items():
    raw = (R1 / rel).read_bytes()
    assert (len(raw), hashlib.sha256(raw).hexdigest()) == (size, digest), rel
source = PROBE.read_text()
assert hashlib.sha256(source.encode()).hexdigest() == 'c9692666c79886e141dbcdf597b2b36ebbde4f6823239eda297f367dfe51da5b'
for old, new in (('(A / NE7).read_bytes()', "(R1 / 'sd-7/contracts/native-evidence.md').read_bytes()"),
                 ('(A / SD7R1).read_bytes()', "(R1 / 'sd-7/successor.json').read_bytes()")):
    assert source.count(old) == 1, old
    source = source.replace(old, new)
sys.argv = [str(PROBE), *sys.argv[1:]]
namespace = {'__name__': '__main__', '__file__': str(PROBE), 'R1': R1}
exec(compile(source, str(PROBE) + ' (two SD-7 r1 reads redirected)', 'exec'), namespace)
