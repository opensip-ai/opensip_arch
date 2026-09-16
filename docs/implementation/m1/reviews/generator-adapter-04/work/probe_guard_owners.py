"""Parent root custody under simulated sandbox failure, owners join end-to-end, positive publish.

Run with python3 -I -B. The custody cases wrap the real subprocess.run: every child really runs
under sandbox-exec, then the wrapper (unconfined, simulating a sandbox bypass) mutates a root.
"""
import importlib.util, json, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rebind as R

assert sys.flags.isolated
report = {}
victim = R.WORK / 'victim-guard'; victim.mkdir(exist_ok=True)
(victim / 'canary.txt').write_text('guard canary\n')

def mutate_symlink(path):
    shutil.rmtree(path); path.symlink_to(victim, target_is_directory=True)

def mutate_replace(path):
    path.rename(path.parent / (path.name + '-aside')); path.mkdir()

scenarios = {
    'output-symlinked-after-generator': ('/generator', 'output', mutate_symlink),
    'output-inode-replaced-after-generator': ('/generator', 'output', mutate_replace),
    'scratch-symlinked-after-validate': ('validate-schemas.cjs', 'runtime-scratch', mutate_symlink),
    'home-replaced-after-validate': ('validate-schemas.cjs', 'home', mutate_replace),
}
for name, (trigger, root_name, mutate) in scenarios.items():
    c = R.case('guard-' + name)
    spec = importlib.util.spec_from_file_location('g_' + name.replace('-', '_'), c / 'tools/generate_contracts.py')
    G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)
    real = G.subprocess.run; calls = []
    def wrapped(argv, _real=real, _calls=calls, **kw):
        result = _real(argv, **kw)
        if argv[0] == '/usr/bin/sandbox-exec':
            step = next((a for a in argv[3:] if a.endswith(('/generator', '.cjs', '.py'))), argv[3])
            _calls.append(Path(step).name)
            if step.endswith(trigger):
                mutate(Path(argv[3]).parent / root_name if trigger == '/generator' else Path(kw['cwd']).parent / root_name)
        return result
    # subprocess is one shared module: patch for this scenario only, then restore.
    G.subprocess.run = wrapped
    before = R.snapshot(c)
    try:
        G.generate(c, generator=R.GEN, node=R.NODE, write=True); outcome = 'ACCEPTED'
    except G.GenerationError as e:
        outcome = 'GenerationError: ' + str(e)
    except Exception as e:
        outcome = 'OTHER ' + type(e).__name__ + ': ' + str(e)
    finally:
        G.subprocess.run = real
    report[name] = {'outcome': outcome, 'sandboxedStepsRun': calls, 'checkedInOutputsUnchanged': R.snapshot(c) == before,
                    'victimFiles': sorted(p.name for p in victim.iterdir()), 'victimCanary': (victim / 'canary.txt').read_text()}

# ADV3 end to end: confined Python step emits a different owners mapping (rebound prepare.py).
base_prepare = (R.WORK / 'base/tools/contracts/prepare.py').read_text()
old = "json.dumps(options['owners'], indent=2)"
assert base_prepare.count(old) == 1
for name, new in [('owners-reordered', "json.dumps(list(reversed(options['owners'])), indent=2)"),
                  ('owners-module-changed', "json.dumps([dict(r, module='evidence') for r in options['owners']], indent=2)"),
                  ('owners-reformatted-same-data', "json.dumps(options['owners'], indent=1)")]:
    c = R.case('owners-' + name, files={'tools/contracts/prepare.py': base_prepare.replace(old, new).encode()})
    before = R.snapshot(c)
    report['ADV3:' + name] = {**R.generate(c, write=True), 'checkedInOutputsUnchanged': R.snapshot(c) == before}

# Positive: corrupt two checked-in outputs, publish, exact bytes restored, then clean drift.
c = R.case('publish-restore')
for rel in ('crates/contracts/src/generated/evidence.rs', 'apps/report/src/generated/report.ts'):
    (c / rel).write_bytes(b'corrupted\n')
w = R.generate(c, write=True); d = R.generate(c)
report['publish-restore'] = {'write': w, 'drift': d, 'stdoutSingleJsonLine': len(w['stdout'].splitlines()) == 1,
                             'allEightExactlyEqualSubject04': all((c / p).read_bytes() == (R.SUBJECT / p).read_bytes() for p in R.outputs(c))}
print(json.dumps(report, indent=1))
