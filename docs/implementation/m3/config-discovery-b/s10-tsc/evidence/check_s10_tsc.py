"""S10-TSC content checks (read-only; design evidence, no product qualification).

Independently of prepare_s10_tsc.py it recomputes what each architecture copy may differ from its parents by, executes
both native-model copies (as the B2-c0 loader does, with __file__ at the native corrections directory) to check the new
D9 row and remedy through the model's own functions, validates the composed DomainDetail against the S10 common v4 copy,
replays the bound B2-c0 checker with the S10 model copy in place of B-S9's, and compares the product copies with the
candidate worktree. Usage: check_s10_tsc.py --architecture A --product W --packages P --work DIR --out FILE"""
from pathlib import Path
import argparse, copy, difflib, hashlib, importlib.util, json, subprocess, sys

U = 'docs/implementation/m3/config-discovery-b/s10-tsc'
CODE = 'native.typescript-config-unresolved'
KEYS = ['native.typescript-config-bound', 'native.typescript-config-extends-cycle',
        'native.typescript-config-extends-unresolved', 'native.typescript-config-malformed']
X4TC = 'docs/implementation/m2/continuation-diagnostics-x4tc-r1/reference/public-detail-registry.json'
NMM = 'docs/implementation/m3/snapshot-plan-c/native-metadata-missing-r1/completion/public-detail-registry.v1.json'
NMM_DESIGN = 'docs/implementation/m3/snapshot-plan-c/native-metadata-missing-r1/completion/design/common.schema.json'
MODELS = {'native_evidence_model.py': 'docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.py',
          'native_evidence_model.v2.py': 'docs/implementation/m3/native-g/rustflags-long-lint-r1/reference/native_evidence_model.v2.py'}
SD7 = 'docs/implementation/m3/supervisor-d/sd-7/successor.json'
ADMISSION = 'docs/implementation/m3/config-discovery-b/b-s10/admission-registry.json'
SOURCES = 'docs/implementation/m3/native-publication/native-common-materialization-r1/sources/'
COMMON = [f'schemas/sources/common-v{v}.schema.json' for v in (1, 3, 4)]
NATIVE = 'docs/coop/design-corrections/native/'
B2C0 = 'docs/implementation/m3/config-discovery-b/b2-c-reference/'
D9_ROW = {'class': 'request-rejected', 'exitCode': 2, 'code': 'CONFIG.INVALID', 'successorCode': None, 'interim': False,
          'typedDetailCarrier': 'request rejection detail'}
results = []


def check(name, ok, **detail):
    results.append(dict(name=name, passed=bool(ok), **detail))
    print(('PASS ' if ok else 'FAIL ') + name, flush=True)


def load_json(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def exec_model(arch, source, name):
    located = arch / NATIVE / name
    spec = importlib.util.spec_from_loader('s10_' + name.replace('.', '_'), loader=None, origin=str(located))
    module = importlib.util.module_from_spec(spec)
    module.__file__ = str(located)
    exec(compile(Path(source).read_bytes(), str(located), 'exec'), module.__dict__)
    return module


def main():
    ap = argparse.ArgumentParser()
    for opt in ('--architecture', '--product', '--packages', '--work', '--out'):
        ap.add_argument(opt, type=Path, required=True)
    a = ap.parse_args()
    arch, product = a.architecture, a.product
    sys.path.insert(0, str(a.packages))
    import jsonschema

    # 1. Registry: the union of both lines plus exactly one record and four aliases.
    reg = load_json(arch / U / 'registry/public-detail-registry.v1.json')
    m2, m3 = load_json(arch / X4TC), load_json(arch / NMM)
    union = {r['code']: r for r in m2['records']}
    union.update({r['code']: r for r in m3['records']})
    got = {r['code']: r for r in reg['records']}
    check('registry records are the union of both lines plus the one new record',
          set(got) == set(union) | {CODE} and all(got[c] == union[c] for c in union) and len(got) == len(reg['records']),
          records=len(got), fromM2=len(m2['records']), fromM3=len(m3['records']))
    check('the new record is owned by native and names item 14a', got[CODE]['owner'] == 'native' and 'item 14a' in got[CODE]['selector'])
    check('records keep the m2 line order (sorted by code)', [r['code'] for r in reg['records']] == sorted(got))
    aliases = {x['internalCode']: x['publicCode'] for x in reg['internalAliases']}
    base_aliases = {x['internalCode']: x['publicCode'] for x in m2['internalAliases']}
    check('aliases are the parents plus exactly the four keys, each to the new detail',
          aliases == {**base_aliases, **{k: CODE for k in KEYS}} and len(reg['internalAliases']) == len(base_aliases) + 4)
    check('every alias target is a registered record', all(v in got for v in aliases.values()))
    check('no internal key is itself a public record', not set(KEYS) & set(got))
    kept = [k for k in m2 if k not in ('standing', 'records', 'internalAliases')]
    check('other m2 fields unchanged; two provenance fields added',
          all(reg[k] == m2[k] for k in kept) and set(reg) == set(m2) | {'snapshotPlanCCorrections', 'typescriptConfigRefusalCorrection'}
          and reg['snapshotPlanCCorrections'] == m3['standing'])

    # 2. The design mirror and the three product sources: the enum gains only the code, at the end.
    def enum_only(candidate, parent):
        c, p = copy.deepcopy(candidate), copy.deepcopy(parent)
        ce, pe = c['$defs']['DomainDetailCode'].pop('enum'), p['$defs']['DomainDetailCode'].pop('enum')
        return c == p and ce == pe + [CODE]
    check('design mirror: nmm copy plus the code', enum_only(load_json(arch / U / 'design/common.schema.json'), load_json(arch / NMM_DESIGN)))
    design_enum = load_json(arch / U / 'design/common.schema.json')['$defs']['DomainDetailCode']['enum']
    check('design mirror enum covers every registry record except the m2-only evaluator3 members',
          set(design_enum) <= set(got), missingFromMirror=sorted(set(got) - set(design_enum)))
    for path in COMMON:
        name = Path(path).name
        cand = arch / U / 'product' / path
        check(f'{name}: the accepted product source plus the code', enum_only(load_json(cand), load_json(arch / SOURCES / name)))
        check(f'{name}: product worktree bytes equal the S10 copy', (product / path).read_bytes() == cand.read_bytes())

    # 3. Model copies: SD-7's bound line 1159 and six inserted lines; nothing else.
    sd7 = [o for o in load_json(arch / SD7)['passageOverrides'] if o['parent']['path'].endswith('native_evidence_model.py')][0]
    for name, parent in MODELS.items():
        old = (arch / parent).read_text(encoding='utf-8').splitlines()
        new = (arch / U / 'reference' / name).read_text(encoding='utf-8').splitlines()
        ops = [op for op in difflib.SequenceMatcher(a=old, b=new, autojunk=False).get_opcodes() if op[0] != 'equal']
        replaced = [op for op in ops if op[0] == 'replace']
        inserted = [op for op in ops if op[0] == 'insert']
        sd7_ok = (len(replaced) == 1 and replaced[0][1:3] == (1158, 1159) and old[1158] == sd7['before'] and new[replaced[0][3]] == sd7['after'])
        check(f'{name}: only SD-7 line 1159 replaced, and two 3-line insertions', sd7_ok and len(inserted) == 2 and
              all(op[4] - op[3] == 3 for op in inserted) and len(ops) == 3, ops=[list(op) for op in ops])
        added = [new[i] for op in inserted for i in range(op[3], op[4])]
        check(f'{name}: inserted lines carry only comments and the two keyed rows', all(
            line.lstrip().startswith('#') or line.lstrip().startswith(f'"{CODE}": ') for line in added))
        m = exec_model(arch, arch / U / 'reference' / name, name)
        base = exec_model(arch, arch / parent, name)
        check(f'{name}: d9_map is the request-rejected CONFIG.INVALID row', m.d9_map(CODE) == {'detail': CODE, **D9_ROW})
        check(f'{name}: D9_MAP otherwise equals the parent', {k: v for k, v in m.D9_MAP.items() if k != CODE} == base.D9_MAP)
        remedies = dict(base.PUBLIC_ROUTE_REMEDIES)
        remedies['PROVIDER.NOT_SELECTED'] = sd7['after'].split('": "', 1)[1].rsplit('",', 1)[0]
        check(f'{name}: PUBLIC_ROUTE_REMEDIES is the effective parent plus the one key',
              {k: v for k, v in m.PUBLIC_ROUTE_REMEDIES.items() if k != CODE} == remedies and CODE in m.PUBLIC_ROUTE_REMEDIES)
        check(f'{name}: CONFIG.INVALID remedy unchanged (the D9 code is not the public detail)',
              m.PUBLIC_ROUTE_REMEDIES['CONFIG.INVALID'] == base.PUBLIC_ROUTE_REMEDIES['CONFIG.INVALID'])
        remedy = m.PUBLIC_ROUTE_REMEDIES[CODE]
        common4 = load_json(arch / U / 'product/schemas/sources/common-v4.schema.json')
        validator = jsonschema.Draft202012Validator({**common4, '$ref': '#/$defs/DomainDetail'})
        details = [m._detail(CODE, key, 'packages/web/tsconfig.json') for key in KEYS]
        check(f'{name}: each key composes a DomainDetail admitted by the S10 common v4',
              all(not list(validator.iter_errors(d)) and d['remedy'] == remedy for d in details),
              subjects=[d['subject'] for d in details])
        if name == 'native_evidence_model.py':
            first_remedy = remedy
    check('both copies carry one remedy string', first_remedy == remedy)
    product_text = (product / 'crates/host/src/outcomes.rs').read_text()
    check('the product carrier is the model string byte for byte',
          f'pub(crate) const REMEDY_TYPESCRIPT_CONFIG_UNRESOLVED: &str = "{remedy}";' in product_text,
          characters=len(remedy), sha256=hashlib.sha256(remedy.encode()).hexdigest())

    # 4. The admission registry copy: B-S10's with the three common rows (and the v1 alias row) re-pinned.
    adm, parent = load_json(arch / U / 'admission-registry.json'), load_json(arch / ADMISSION)
    ok = True
    for group in ('sources', 'aliases'):
        for x, y in zip(adm[group], parent[group], strict=True):
            if x['sourcePath'] in COMMON:
                raw = (arch / U / 'product' / x['sourcePath']).read_bytes()
                ok &= {k: v for k, v in x.items() if k not in ('bytes', 'sha256')} == {k: v for k, v in y.items() if k not in ('bytes', 'sha256')}
                ok &= x['bytes'] == len(raw) and x['sha256'] == hashlib.sha256(raw).hexdigest()
            else:
                ok &= x == y
    check('admission registry: B-S10 copy with only the common rows re-pinned', ok and set(adm) == set(parent))
    check('admission registry: product bytes equal the S10 copy',
          (product / 'schemas/admission-registry.json').read_bytes() == (arch / U / 'admission-registry.json').read_bytes())

    # 5. The bound B2-c0 checker, replayed with the S10 model copy in place of B-S9's.
    ref = (arch / B2C0 / 'reference/native_unit_reference.py').read_text()
    raw = (arch / U / 'reference/native_evidence_model.py').read_bytes()
    line = [l for l in ref.splitlines() if l.startswith('MODEL = (')][0]
    patched = ref.replace(line, f"MODEL = ('{U}/reference/native_evidence_model.py', {len(raw)}, '{hashlib.sha256(raw).hexdigest()}')")
    a.work.mkdir(parents=True, exist_ok=True)
    (a.work / 'native_unit_reference.py').write_text(patched)
    out = a.work / 'b2c0-replay.json'
    r = subprocess.run([sys.executable, '-I', '-B', str(arch / B2C0 / 'evidence/check.py'), '--architecture', str(arch),
                        '--packages', str(a.packages), '--reference', str(a.work / 'native_unit_reference.py'),
                        '--out', str(out), '--no-mutations'], capture_output=True, text=True)
    (a.work / 'b2c0-replay.log').write_text(r.stdout + r.stderr)
    bound = load_json(arch / B2C0 / 'evidence/checks.json')
    replay = load_json(out) if out.exists() else {}
    fields = ['cases', 'unitCases', 'historicalPassed', 'currentPassed', 'casesWithExplainedDifference', 'memberCases', 'joinSweep', 'passed']
    check('B2-c0 replay over the S10 model copy: exit 0 and every result equal to the bound record',
          r.returncode == 0 and all(replay.get(f) == bound.get(f) for f in fields),
          exitCode=r.returncode, differing=[f for f in fields if replay.get(f) != bound.get(f)])

    passed = all(x['passed'] for x in results)
    a.out.write_text(json.dumps(dict(standing='S10-TSC CONTENT CHECK: design evidence only; no product qualification',
                                     passed=passed, checks=results), indent=2) + '\n')
    print('passed', passed)
    sys.exit(0 if passed else 1)


if __name__ == '__main__':
    main()
