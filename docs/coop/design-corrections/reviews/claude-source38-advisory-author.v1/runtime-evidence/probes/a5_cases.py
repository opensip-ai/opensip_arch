"""A5 focused regression control: the retained native F11 typescript_mode cases (native-cases.v2.json, unchanged by the
A5 patch) evaluated against source38's model and root's A5 model, plus the mode-table row question for a jsconfig with
explicit allowJs=false. Imports each model read-only (interpreter -B: no bytecode written). Output: receipts/a5-cases.json.
"""
import hashlib, importlib.util, json, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v1')
TREES = {'source38': Path('/tmp/opensip-design-corrections/candidate-subject.v38'),
         'rootA5': Path('/tmp/opensip-design-corrections/root-consumer24-js-options.v1/source')}
REL = 'docs/coop/design-corrections/native/'
out = {'standing': 'focused reference-model control; not a native checker run, not qualification'}


def load(tag, root):
    spec = importlib.util.spec_from_file_location('a5_native_' + tag, root / REL / 'native_evidence_model.v2.py')
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


cases_raw = (TREES['source38'] / REL / 'native-cases.v2.json').read_bytes()
out['casesSha256'] = {t: hashlib.sha256((r / REL / 'native-cases.v2.json').read_bytes()).hexdigest() for t, r in TREES.items()}
cases = [c for c in json.loads(cases_raw)['cases'] if c.get('steps') and all(s['fn'] == 'typescript_mode' for s in c['steps'])]
extra = {'jsconfig-explicit-allowJs-false': dict(listing=['src/a.js', 'src/b.ts'], unit_root='', package_json=None, tsconfig=None,
                                                jsconfig={'compilerOptions': {'allowJs': False}}, lockfiles=[], node_modules_in_read_set=False),
         'tsconfig-checkJs-only-no-js': dict(listing=['src/b.ts'], unit_root='', package_json=None, tsconfig={'compilerOptions': {'checkJs': True}},
                                             jsconfig=None, lockfiles=[], node_modules_in_read_set=False)}
for tag, root in TREES.items():
    m = load(tag, root)
    rows = []
    for c in cases:
        got = m.typescript_mode(**c['steps'][0]['args'])
        exp = {k[len('$m.'):]: v for k, v in c['expect'].items()}
        diff = {k: {'expected': v, 'actual': got.get(k)} for k, v in exp.items() if got.get(k) != v}
        rows.append({'case': c['id'], 'kind': c['kind'], 'agrees': not diff, 'diff': diff})
    ext = {}
    for name, args in extra.items():
        g = m.typescript_mode(**args)
        ext[name] = {k: g[k] for k in ('languageMode', 'configOrigin', 'allowJs', 'checkJs', 'jsAdmittedToProgram', 'jsDiagnosticsEnabled',
                                       'programRootFiles', 'jsRootFiles')}
    out[tag] = {'modelSha256': hashlib.sha256((root / REL / 'native_evidence_model.v2.py').read_bytes()).hexdigest(),
                'typescriptModeCases': rows, 'extra': ext}
print(json.dumps(out, indent=1))
(BASE / 'receipts' / 'a5-cases.json').write_text(json.dumps(out, indent=1) + '\n')
