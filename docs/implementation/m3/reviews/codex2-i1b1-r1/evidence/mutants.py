"""I1-b1 mutation check: each mutant of policy.rs must make at least one of the
three cycle_representative tests fail. Run under the lane lock by mutants.sh.
The original file is restored after every mutant and checked at the end."""
import hashlib, json, os, pathlib, subprocess, sys

ROOT = pathlib.Path('/Users/sb/code/opensip-ai/opensip-i1b1')
P = ROOT / 'crates/evaluator/src/policy.rs'
OUT = pathlib.Path(sys.argv[1])
ORIGINAL = P.read_bytes()
SHA = hashlib.sha256(ORIGINAL).hexdigest()
BASE = subprocess.run(['git', '-C', str(ROOT), 'show', 'HEAD:crates/evaluator/src/policy.rs'],
                      check=True, capture_output=True).stdout

def sub(old, new, count=1):
    def apply(text):
        assert text.count(old) == count, (old, text.count(old))
        return text.replace(old, new)
    return apply

MUTANTS = [
    ('control: unmutated', lambda t: t),
    ('M0 base policy.rs (HEAD)', None),
    ('M1 op law: drop root', sub('root && member_is(atom, "relation", "imports")', 'member_is(atom, "relation", "imports")')),
    ('M2 op law: drop relation', sub('root && member_is(atom, "relation", "imports")', 'root')),
    ('M3 op law: drop rung', sub('&& member_is(atom, "minResolution", "resolved-target")', '')),
    ('M4 op law: drop filters', sub('&& optional(atom, "filters") == Some(&V::Array(Vec::new()))', '')),
    ('M5 op law: drop endpoint', sub('&& optional(atom, "endpoint").is_none()', '')),
    ('M6 op law: drop evidence', sub('&& optional(atom, "evidence").is_none()', '')),
    ('M7 op law: drop subject kind', sub('&& subject_kind.is_none_or(|k| k == "file")', '')),
    ('M8 op law: program pass demands Some(file)', sub('subject_kind.is_none_or(|k| k == "file")', 'subject_kind == Some("file")')),
    ('M9 keep the source-kind check for the op', sub('if !cycle\n        && !kinds', 'if !kinds')),
    ('M10 op law never applied', sub('let cycle = member_is(atom, "op", "cycle-representative");', 'let cycle = false;')),
    ('M11 policy pass: every node is root', sub('depth == 1, registry', 'true, registry')),
    ('M12 program pass: every node is root', lambda t: sub('.map(|n| (n, false))', '.map(|n| (n, true))')(
        sub('"not" => stack.push((field(node, "operand")?, false))', '"not" => stack.push((field(node, "operand")?, true))')(t))),
]

env = dict(os.environ)
results = []
try:
    for name, mutate in MUTANTS:
        if mutate is None:
            P.write_bytes(BASE)
        else:
            P.write_text(mutate(ORIGINAL.decode()))
        r = subprocess.run(['nice', '-n', '10', 'cargo', 'test', '-p', 'opensip-evaluator', '--lib', '--locked',
                            '--offline', '--', 'pack_tests::cycle_representative'],
                           cwd=ROOT, env=env, capture_output=True, text=True)
        log = r.stdout + r.stderr
        failed = sorted({line.split()[1] for line in log.splitlines()
                         if line.startswith('test ') and line.rstrip().endswith('FAILED')})
        compiled = 'running ' in log
        results.append({'mutant': name, 'rc': r.returncode, 'compiled': compiled,
                        'killed': r.returncode != 0, 'failedTests': failed})
        (OUT / ('mutant-%02d.log' % len(results))).write_text(log)
        print(json.dumps(results[-1]), flush=True)
finally:
    P.write_bytes(ORIGINAL)
assert hashlib.sha256(P.read_bytes()).hexdigest() == SHA
(OUT / 'mutants.json').write_text(json.dumps({'policySha256': SHA, 'results': results}, indent=1) + '\n')
print('restored', SHA)
