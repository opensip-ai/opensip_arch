from pathlib import Path
import shutil, re
# Build the U-5a cold runner variants: each is the accepted runner copied byte-for-byte into its own directory (so its
# outputs land there, never over accepted evidence), with exactly these insertions: an import of cold_reset after the
# imports, and `_cr.reset(env,T)` as the first statement of the single `for n in range(10):` measured loop (before any
# timestamp); plus `_cr.write(B)` before the
# lane is released. The replay variant also restricts its sizes to the six TS row sizes.
W = Path(__file__).resolve().parent; SP = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/spikes'); B = Path('/tmp/opensip-implementation')
JOBS = {'sm1': (SP / 's-m-sm1-ready-closure-2026-10-09', 'run_ready.py', ['ready.cjs']),
        'sealing': (SP / 's-m-sealing-typed-2026-10-09', 'run_set.py', ['probe.py', 'control-template.json']),  # attempt 0 omitted control-template.json (retained)
        'transfer': (SP / 's-m-transfer-2026-10-09', 'run_transfer.py', ['receiver.py']),
        'cohort': (SP / 's-m-ts-cohort-2026-10-09', 'run_cohort.py', ['cohort.cjs']),
        'synthesized': (SP / 's-m-ts-synthesized-2026-10-10', 'run_synthesized_ts.py', ['synthesized.cjs']),
        'replay': (B / 'sm-replay-sized-2026-10-13', 'run_sized_replay_r2.py', ['sized-packets-r1.json'])}
for name, (src, runner, aux) in JOBS.items():
    d = W / name
    if d.exists(): continue  # already built (and possibly run); never rebuilt over
    d.mkdir(); (d / 'evidence').mkdir()
    for f in aux: shutil.copyfile(src / f, d / f)
    s = (src / runner).read_text(); orig = s
    lines = s.split('\n'); k = max(i for i, l in enumerate(lines[:6]) if l.startswith('import') or l.startswith('from'))
    lines.insert(k + 1, "import sys as _s;_s.path.insert(0,str(Path(__file__).resolve().parent.parent));import cold_reset as _cr")
    # The reset is the FIRST statement of each measured iteration, before any timestamp, so no reset work is timed.
    loops = [i for i, l in enumerate(lines) if l.strip() == 'for n in range(10):']; assert len(loops) == 1, name
    i = loops[0]; body = lines[i + 1]; indent = body[:len(body) - len(body.lstrip())]; assert len(indent) > len(lines[i]) - len(lines[i].lstrip())
    lines.insert(i + 1, indent + '_cr.reset(env,T)'); s = '\n'.join(lines); n = 1
    m = re.search(r'\nfinally:\n', s); assert m and s.count('\nfinally:\n') == 1
    s = s[:m.start()] + '\n _cr.write(B)' + s[m.start():] if name != 'replay' else s[:m.start()] + '\n _cr.write(H)' + s[m.start():]
    if name == 'replay':
        a = "for count in sorted(int(c) for c in packets['packets']):"; assert s.count(a) == 1
        s = s.replace(a, "for count in sorted({141,193,678,936,1159,1381}):  # U-5a: the six TS row sizes only")
        s = s.replace("dest=H/'sized-replay-results-r2.json'", "dest=H/'sized-replay-results-cold-ts.json'")
        s = s.replace("out=H/f'replay-r2-{count}-{n}.stdout';err=H/f'replay-r2-{count}-{n}.stderr'", "out=H/'evidence'/f'replay-{count}-{n}.stdout';err=H/'evidence'/f'replay-{count}-{n}.stderr'")
    (d / runner).write_text(s); (d / 'ACCEPTED-RUNNER-SOURCE').write_text(f'{src / runner}\n')
    print(name, 'popen sites', n)
