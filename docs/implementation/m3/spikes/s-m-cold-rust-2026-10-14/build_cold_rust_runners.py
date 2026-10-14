from pathlib import Path
import shutil, re, hashlib
# Build the U-5b cold runner variants (PLAN-r3 D-7, U-5 for the Rust rows: F = SM-3 + SM-5 + SM-7 + SM-9, T = F + SM-4).
# Each is the accepted runner copied byte-for-byte into its own directory (outputs land there), with exactly U-5a's
# insertions: the cold_reset import (cold_reset.py is U-5a's accepted file, byte-equal), `_cr.reset(env,T)` as the FIRST
# statement of the single measured loop (before any timestamp), and `_cr.write(<dir>)` before the lane is released.
# Runner-specific edits, each asserted: the SM-4 runner (U-1 static-profile, bsabsent) has no env/T in its loop, so the
# reset takes a placeholder dict and the series root (its compiler children run with their constructed environment;
# each run already writes a fresh output root), and its result is redirected here; the replay runner is restricted to
# the eight Rust row sizes and redirected here (as U-5a did for the TS sizes).
W = Path(__file__).resolve().parent; SP = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/spikes'); B = Path('/tmp/opensip-implementation'); U2C = SP / 's-m-u2c-rust-sealing-transfer-2026-10-14/runners'
ACC = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/spikes/s-m-cold-ts-2026-10-13/cold_reset.py'); assert (W / 'cold_reset.py').read_bytes() == ACC.read_bytes()
U2CW = Path('/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/u2c')
JOBS = {'sm3': (SP / 's-m-sm3-ready-2026-10-09', 'run_ready.py', [], 'n', 'B'),
        'sm4': (SP / 's-m-u1-build-script-outputs-absent-2026-10-13', 'run_bsabsent_static_profile_series_r1.py', [], 'ordinal', 'H'),
        'replay': (B / 'sm-replay-sized-2026-10-13', 'run_sized_replay_r2.py', ['sized-packets-r1.json'], 'n', 'H'),
        'sm5': (U2C, 'run_u2c_sm5_two_part_r2.py', ['probe_two_part.py', '../u2c-inputs.json'], 'n', 'W'),
        'sm7': (U2C, 'run_u2c_sm7_r3.py', ['receiver_ne_fields.py', '../u2c-inputs.json'], 'n', 'W')}  # published U-2c (codex-sm-u2c-r2), SM-7 r3
RUST_SIZES = {71, 98, 192, 208, 239, 279, 301, 808}
import sys
only = sys.argv[1:]
for name, (src, runner, aux, var, outdir) in JOBS.items():
    if only and name not in only: continue
    d = W / name
    if d.exists(): continue  # never rebuilt over
    d.mkdir()
    for f in aux: shutil.copyfile(src / f, d / Path(f).name)
    s = (src / runner).read_text(); orig = s
    lines = s.split('\n'); k = max(i for i, l in enumerate(lines[:12]) if l.startswith('import') or l.startswith('from'))
    lines.insert(k + 1, "import sys as _s;_s.path.insert(0,str(Path(__file__).resolve().parent.parent));import cold_reset as _cr")
    loops = [i for i, l in enumerate(lines) if l.strip() == f'for {var} in range(10):']; assert len(loops) == 1, name
    i = loops[0]; body = lines[i + 1]; indent = body[:len(body) - len(body.lstrip())]; assert len(indent) > len(lines[i]) - len(lines[i].lstrip())
    lines.insert(i + 1, indent + ('_cr.reset(_cold_env,root)' if name == 'sm4' else '_cr.reset(env,T)')); s = '\n'.join(lines)
    m = re.search(r'\nfinally:\n', s); assert m and s.count('\nfinally:\n') == 1
    # the write goes at the end of the try body, with the try body's indentation
    tryind = ' ' if name != 'sm4' else '    '
    s = s[:m.start()] + f'\n{tryind}_cr.write({outdir})' + s[m.start():]
    if name == 'sm4':
        a = "dest = V / 'bsabsent-static-profile-series-r1.json'; assert not dest.exists()"; assert s.count(a) == 1
        s = s.replace(a, "H = Path(__file__).resolve().parent; dest = H / 'bsabsent-static-profile-series-cold-rust.json'; assert not dest.exists(); _cold_env = {}  # U-5b: redirected; placeholder env for the reset")
    if name == 'replay':
        a = "for count in sorted(int(c) for c in packets['packets']):"; assert s.count(a) == 1
        s = s.replace(a, "for count in sorted({71,98,192,208,239,279,301,808}):  # U-5b: the eight Rust row sizes only")
        for a, b in [("dest=H/'sized-replay-results-r2.json'", "dest=H/'sized-replay-results-cold-rust.json'"),
                     ("out=H/f'replay-r2-{count}-{n}.stdout';err=H/f'replay-r2-{count}-{n}.stderr'", "out=H/'evidence'/f'replay-{count}-{n}.stdout';err=H/'evidence'/f'replay-{count}-{n}.stderr'")]:
            assert s.count(a) == 1, a; s = s.replace(a, b)
        (d / 'evidence').mkdir()
    (d / runner).write_text(s); (d / 'ACCEPTED-RUNNER-SOURCE').write_text(f'{src / runner}\nsha256 {hashlib.sha256(orig.encode()).hexdigest()}\n')
    print(name, 'built')
