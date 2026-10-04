"""Lead evidence for VD2-a (not a subject member): mutate verify_design.py's refusals one at a time and rerun
tools/tests/test_design_binding.py on each mutant, in a private temporary tree. Mutants: every raise carrying one of
VD2's seven messages (VD1's copies of three of them included) replaced by pass, VD2's before-text check, and seven
weakened VD2 conditions. Nothing is written to the worktree. Expected: 18 mutants, 17 killed; the one survivor is
the root-kind half of check 2.5 ("drop root-kind check"), which no lock can reach (REQUEST.md judgment call 3).
Usage: python3.14 -I -B mutate_vd2a.py WORKTREE (exit 1 while any mutant survives)."""
import subprocess, sys, tempfile, os, re
from pathlib import Path
W = Path(sys.argv[1]); PY = sys.executable
src = (W / 'tools/verify_design.py').read_text(); tests = (W / 'tools/tests/test_design_binding.py').read_text()
mutants = []
for msg in ['superseded record is not an earlier contract successor', 'superseded passage is not in the named record',
            'contract passage supersession selects a different passage', 'double supersession: the named passage is not the current meaning',
            'passage override restates a superseded contract meaning', 'contract review superseded passages differ from the record',
            'contract passage supersession is not listed by its review']:
    needle = f"raise DesignError('{msg}')"
    idx = [m.start() for m in re.finditer(re.escape(needle), src)]
    for i in idx:
        mutants.append((msg + f' @{i}', src[:i] + 'pass' + src[i + len(needle):]))
# before check: only the VD2 copy (first occurrence after 'VD2: a contract passage')
start = src.index('VD2: a contract passage')
needle = "raise DesignError('passage supersession before text differs from the superseded meaning')"
i = src.index(needle, start)
mutants.append(('VD2 before check', src[:i] + 'pass' + src[i + len(needle):]))
# partial conditions
for old, new, label in [
        ("target is None or target['parent'] != named['parent']", "target is None", 'drop named parent pin check'),
        ("entry['parent'] != target['parent'] or key[1] != target_key[2]", "key[1] != target_key[2]", 'drop same-parent check'),
        ("entry['parent'] != target['parent'] or key[1] != target_key[2]", "entry['parent'] != target['parent']", 'drop same-selector check'),
        ("(tail is None and kind != 'override') or (tail is not None and tail != target_key)", "(tail is not None and tail != target_key)", 'drop root-kind check'),
        ("(tail is None and kind != 'override') or (tail is not None and tail != target_key)", "(tail is None and kind != 'override')", 'drop tail check'),
        ("if entry['parent']['path'] not in chain_index:", "if False:", 'never classify as contract'),
        ("        links += record_links\n", "", 'count not accumulated')]:
    a = src.index('record_links = 0'); b = src.index("here = inventory_row(entry['parent']") if 'count' not in label else src.index('links += record_links') + 30
    seg = src[a:b]; assert seg.count(old) == 1, old
    mutants.append((label, src[:a] + seg.replace(old, new) + src[b:]))
survivors = []
for label, body in mutants:
    with tempfile.TemporaryDirectory() as t:
        os.chmod(t, 0o700); (Path(t) / 'tools/tests').mkdir(parents=True)
        (Path(t) / 'tools/verify_design.py').write_text(body); (Path(t) / 'tools/tests/test_design_binding.py').write_text(tests)
        p = subprocess.run([PY, '-I', '-B', '-m', 'unittest', 'discover', '-s', 'tools/tests', '-p', 'test_design_binding.py'], cwd=t, capture_output=True, text=True)
        killed = p.returncode != 0
        fails = sorted(set(re.findall(r'^(?:FAIL|ERROR): (\w+)', p.stderr, re.M)))
        print(('KILLED  ' if killed else 'SURVIVED'), label, fails[:6])
        if not killed: survivors.append(label)
print('survivors:', survivors); sys.exit(1 if survivors else 0)
