"""A5 proposed amendment (separate from the source38 working tree; root's A5 directory is read-only).

1. Copies root's A5 after-bytes of native-evidence.md and native-cases.v2.json into a5-review/amended/ and applies
   exact counted replacements: the inheritance/default law, the ts-tsconfig mode row, and the F11 typescript_mode
   cases (the stale checkJs-only negative case becomes the explicit-false case; checkJs-only with and without JS
   roots and an explicit-false jsconfig are added).
2. Writes a5-review/proposed-amendment.diff (unified, root A5 after -> amended).
3. Checks the amended law, transcribed, against every compiler observation retained so far (root's 32 direct rows
   and this runtime's 20 extends rows), and the literal root law against the same rows.
4. Evaluates every typescript_mode case of the amended native-cases against root's A5 model (unchanged) and the
   source38 model. Output: receipts/a5-amendment.json.
"""
import difflib, hashlib, importlib.util, json, shutil, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v1')
A5 = Path('/tmp/opensip-design-corrections/root-consumer24-js-options.v1')
S38 = Path('/tmp/opensip-design-corrections/candidate-subject.v38')
NE = 'docs/v2/contracts/product-v1/native-evidence.md'
NC = 'docs/coop/design-corrections/native/native-cases.v2.json'
MODEL = 'docs/coop/design-corrections/native/native_evidence_model.v2.py'
OUTDIR = BASE / 'a5-review'
AM = OUTDIR / 'amended'
sha = lambda b: hashlib.sha256(b).hexdigest()
out = {'standing': 'proposed A5 amendment and focused checks; not integrated, not root-accepted, not qualification'}

PROSE_OLD = ("For the selected option projection, an explicit `allowJs` value wins, including\n"
             "`false`. A jsconfig entry defaults it to `true`; otherwise omitted `allowJs`\n"
             "derives from effective `checkJs`, whose omitted default is `false`. Apply\n"
             "configuration inheritance before these defaults. The pre-Plan marker observation")
PROSE_NEW = ("For the selected option projection, every node of that graph whose `kind` is\n"
             "`jsconfig` (the exact basename law of `TypeScriptConfigGraphV1`) supplies\n"
             "`allowJs=true` as if written in that node, unless the node itself writes\n"
             "`allowJs`. Inheritance then applies over the graph: a node's own options,\n"
             "including that supplied value, take precedence over the bases it extends, and\n"
             "later `extends` entries over earlier ones. After inheritance an `allowJs` value\n"
             "wins, including `false`; otherwise `allowJs` derives from the effective\n"
             "`checkJs`, whose omitted default is `false`. So a `jsconfig.json` entry extending\n"
             "a base that writes `allowJs: false` is effective `allowJs=true` unless the entry\n"
             "writes `allowJs` itself, and a `tsconfig.json` entry extending a base named\n"
             "`jsconfig.json` inherits `true`. The pre-Plan marker observation")
ROW_OLD = ("| `ts-tsconfig` | `tsconfig.json` at the unit root (or named by discovery), effective `allowJs=false` | "
           "`typescript-v2`, `configOrigin=tsconfig` |")
ROW_NEW = ("| `ts-tsconfig` | `tsconfig.json`/`jsconfig.json` at the unit root (or named by discovery) with effective "
           "`allowJs=false` (a jsconfig entry only when it writes `allowJs: false`) | `typescript-v2`, `configOrigin` "
           "derived from the entry (`tsconfig` or `jsconfig`) |")


def mode_case(cid, kind, listing, tsconfig, jsconfig, expect):
    return {"id": cid, "feedback": ["F11"], "kind": kind,
            "steps": [{"fn": "typescript_mode", "args": {"listing": listing, "unit_root": "", "package_json": None,
                                                        "tsconfig": tsconfig, "jsconfig": jsconfig, "lockfiles": [],
                                                        "node_modules_in_read_set": True}, "bind": "m"}],
            "expect": {"$m." + k: v for k, v in expect.items()}}


NEW_CASES = [
    mode_case("ts-tsconfig-explicit-allowjs-false-excludes-js", "negative", ["src/a.js", "src/b.ts"],
              {"compilerOptions": {"allowJs": False, "checkJs": True}}, None,
              {"languageMode": "ts-tsconfig", "allowJs": False, "checkJs": True, "jsAdmittedToProgram": False,
               "jsDiagnosticsEnabled": True, "jsRootFiles": [], "programRootFiles": ["src/b.ts"]}),
    mode_case("tsconfig-checkjs-only-admits-js", "positive", ["src/a.js", "src/b.ts"],
              {"compilerOptions": {"checkJs": True}}, None,
              {"languageMode": "js-allowjs", "allowJs": True, "checkJs": True, "jsAdmittedToProgram": True,
               "jsDiagnosticsEnabled": True, "jsRootFiles": ["src/a.js"], "programRootFiles": ["src/a.js", "src/b.ts"]}),
    mode_case("tsconfig-checkjs-only-without-js-roots", "positive", ["src/b.ts"],
              {"compilerOptions": {"checkJs": True}}, None,
              {"languageMode": "js-allowjs", "allowJs": True, "jsAdmittedToProgram": False, "jsDiagnosticsEnabled": True,
               "jsRootFiles": [], "programRootFiles": ["src/b.ts"]}),
    mode_case("jsconfig-explicit-allowjs-false-excludes-js", "negative", ["src/a.js", "src/b.ts"],
              None, {"compilerOptions": {"allowJs": False}},
              {"languageMode": "ts-tsconfig", "configOrigin": "jsconfig", "allowJs": False, "jsAdmittedToProgram": False,
               "jsDiagnosticsEnabled": False, "jsRootFiles": [], "programRootFiles": ["src/b.ts"]}),
]

# ---- 1. amended copies
problems = []
AM.mkdir(parents=True, exist_ok=False)
ne_root = (A5 / 'source' / NE).read_bytes()
nc_root = (A5 / 'source' / NC).read_bytes()
ne = ne_root.decode('utf-8')
for old, new in ((PROSE_OLD, PROSE_NEW), (ROW_OLD, ROW_NEW)):
    if ne.count(old) != 1:
        problems.append('native-evidence anchor count %d: %r' % (ne.count(old), old[:70]))
    ne = ne.replace(old, new)
doc = json.loads(nc_root)
fmt = None
for ensure in (False, True):
    if (json.dumps(doc, indent=1, ensure_ascii=ensure) + '\n').encode('utf-8') == nc_root:
        fmt = ensure
out['nativeCasesRoundTrip'] = fmt is not None
ids = [c['id'] for c in doc['cases']]
if 'ts-tsconfig-without-allowjs-excludes-js' not in ids:
    problems.append('stale case not found')
else:
    at = ids.index('ts-tsconfig-without-allowjs-excludes-js')
    doc['cases'][at:at + 1] = NEW_CASES
nc = json.dumps(doc, indent=1, ensure_ascii=bool(fmt)) + '\n'
(AM / 'native-evidence.md').write_text(ne, encoding='utf-8')
(AM / 'native-cases.v2.json').write_text(nc, encoding='utf-8')
diff = ''.join(difflib.unified_diff(ne_root.decode('utf-8').splitlines(True), ne.splitlines(True),
                                    'root-a5/' + NE, 'amended/' + NE))
diff += ''.join(difflib.unified_diff(nc_root.decode('utf-8').splitlines(True), nc.splitlines(True),
                                     'root-a5/' + NC, 'amended/' + NC))
(OUTDIR / 'proposed-amendment.diff').write_text(diff, encoding='utf-8')
out['files'] = [{'path': NE, 'rootA5After': sha(ne_root), 'amended': sha(ne.encode())},
                {'path': NC, 'rootA5After': sha(nc_root), 'amended': sha(nc.encode()),
                 'source38': sha((S38 / NC).read_bytes())}]
out['proposedAmendmentDiff'] = {'sha256': sha(diff.encode()), 'lines': diff.count('\n')}


# ---- 3. law transcriptions against every retained compiler observation
def amended_law(entry, own, base_name, base_opts):
    nodes = []
    if base_name is not None:
        nodes.append((base_name.rsplit('/', 1)[-1], base_opts))
    nodes.append((entry, own))
    merged = {}
    for name, opts in nodes:
        eff = ({'allowJs': True} if name == 'jsconfig.json' else {})
        eff.update(opts)
        merged.update(eff)
    check = bool(merged.get('checkJs', False))
    return (bool(merged['allowJs']) if 'allowJs' in merged else check), check


def root_law(entry, own, base_opts):
    merged = dict(base_opts or {}, **own)
    check = bool(merged.get('checkJs', False))
    if 'allowJs' in merged:
        return bool(merged['allowJs']), check
    return (True if entry == 'jsconfig.json' else check), check


rows = []
for r in json.loads((A5 / 'compiler-observations.json').read_text())['rows']:
    entry = r['origin'] + '.json'
    rows.append({'source': 'root-32', 'case': '%s %s js=%s' % (entry, json.dumps(r['options'], sort_keys=True), r['jsFilePresent']),
                 'compiler': (r['effectiveAllowJs'], r['checkJs']), 'amended': amended_law(entry, r['options'], None, {}),
                 'root': root_law(entry, r['options'], {})})
ext = json.loads((BASE / 'receipts' / 'a5-extends.json').read_text())
for r in ext['rows']:
    rows.append({'source': 'extends-20', 'case': '%s js=%s' % (r['id'], r['jsFilePresent']),
                 'compiler': (r['effectiveAllowJs'], r['checkJs']),
                 'amended': amended_law(r['entry'], r['own'], r['base']['name'], r['base']['options']),
                 'root': root_law(r['entry'], r['own'], r['base']['options'])})
out['lawRows'] = len(rows)
out['amendedLawDisagreements'] = [r['case'] for r in rows if tuple(r['amended']) != tuple(r['compiler'])]
out['rootLawDisagreements'] = [r['case'] for r in rows if tuple(r['root']) != tuple(r['compiler'])]


# ---- 4. amended typescript_mode cases against root's model and source38's model
def load(tag, path):
    spec = importlib.util.spec_from_file_location('a5_amend_' + tag, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


models = {'rootA5': load('root', A5 / 'source' / MODEL), 'source38': load('s38', S38 / MODEL)}
case_rows = {}
for tag, m in models.items():
    res = []
    for c in json.loads(nc)['cases']:
        if not (c.get('steps') and all(s['fn'] == 'typescript_mode' for s in c['steps'])):
            continue
        got = m.typescript_mode(**c['steps'][0]['args'])
        diff_ = {k[3:]: {'expected': v, 'actual': got.get(k[3:])} for k, v in c['expect'].items() if got.get(k[3:]) != v}
        res.append({'case': c['id'], 'agrees': not diff_, 'diff': diff_})
    case_rows[tag] = res
out['amendedCases'] = case_rows
out['problems'] = problems
ok = (not problems and out['nativeCasesRoundTrip'] and not out['amendedLawDisagreements']
      and all(r['agrees'] for r in case_rows['rootA5']))
out['allOk'] = ok
(BASE / 'receipts' / 'a5-amendment.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps({k: v for k, v in out.items() if k != 'amendedCases'}, indent=1))
print(json.dumps({t: [(r['case'], r['agrees'], r['diff']) for r in v] for t, v in case_rows.items()}, indent=1))
sys.exit(0 if ok else 1)
