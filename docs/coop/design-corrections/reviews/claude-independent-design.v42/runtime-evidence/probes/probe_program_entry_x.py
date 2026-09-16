"""Independent programEntry x provenance discrimination: source41 versus source42 enumeration owner admission, each tree's own
enumeration_model through its own check-enumeration baseline helpers (membership, scope, rows, bindings), in separate processes.
Only the named binding fields, and the unit/universe/context/graph a language mode requires, differ from the maintained
default-unit baseline. Admission-level (the owner join that complete Run closure calls via evaluator_input_model
reconstruct -> ENUM.admit_enumeration); not claimed as full Runs.
usage: probe_program_entry_x.py  |  probe_program_entry_x.py --child ROOT LABEL OUT"""
import contextlib, copy, importlib.util, io, json, subprocess, sys, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v42')
TREES = [('source41', RT / 'work/base41'), ('source42', RT / 'work/source42-pkg')]
PY = '/tmp/opensip-architecture-review-env/bin/python'
OUT = RT / 'receipts/probes/program-entry-x.json'
PE = 'ENUMERATION_BINDING_PROGRAM_ENTRY'
# case -> (expected source41, expected source42); REFUSE means exactly [ENUMERATION_BINDING_PROGRAM_ENTRY]
EXPECT = {
    'ts-default-null': ('ADMIT', 'ADMIT'),
    'ts-default-marker-nonnull': ('REFUSE', 'REFUSE'),
    'ts-explicit-marker-nonnull': ('ADMIT', 'ADMIT'),
    'ts-explicit-null-provenance-only-change': ('ADMIT', 'REFUSE'),
    'ts-explicit-null-graph-entry-build-config': ('REFUSE', 'REFUSE'),
    'ts-explicit-build-config-nonnull': ('ADMIT', 'ADMIT'),
    'ts-default-null-plus-explicit-build-config': ('ADMIT', 'ADMIT'),
    'js-allowjs-default-null': ('ADMIT', 'ADMIT'),
    'js-allowjs-explicit-null': ('ADMIT', 'REFUSE'),
    'js-synthesized-default-null': ('ADMIT', 'ADMIT'),
    'js-synthesized-explicit-null': ('ADMIT', 'REFUSE'),
    'js-synthesized-explicit-package-json-nonnull': ('REFUSE', 'REFUSE'),
    'rust-default-null': ('ADMIT', 'ADMIT'),
    'rust-default-cargo-nonnull': ('REFUSE', 'REFUSE'),
    'rust-explicit-null': ('ADMIT', 'ADMIT'),
    'rust-explicit-cargo-nonnull': ('ADMIT', 'ADMIT'),
    'syntax-default-null': ('ADMIT', 'ADMIT'),
    'syntax-default-readme-nonnull': ('REFUSE', 'REFUSE'),
    'syntax-explicit-null': ('ADMIT', 'ADMIT'),
    'syntax-explicit-readme-nonnull': ('ADMIT', 'ADMIT'),
    'unavailable-default-null': ('ADMIT', 'ADMIT'),
    'unavailable-explicit-null': ('ADMIT', 'ADMIT'),
    'unavailable-default-marker-nonnull': ('ADMIT', 'ADMIT'),
    'unavailable-explicit-build-config-nonnull': ('ADMIT', 'ADMIT'),
}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


def child(root, label, outfile):
    CE = load('pe_check_enum_' + label, Path(root) / 'docs/coop/design-corrections/foundation/check-enumeration.v1.py')
    M = CE.M
    sc = CE.scope()
    source = CE.blobs()
    roots = ['src/a.ts', 'src/b.ts', 'src/extra.js']
    res = {}

    def world(unit_patch=None):
        m = copy.deepcopy(CE.membership())
        if unit_patch:
            m['units'][0].update(unit_patch)
        fext = M.host_file_extent(m, CE.SNAPSHOT, sc, '.', [])
        proj = M.project_named_packages(CE.SNAPSHOT, sc, '.', m, source, [])
        return {'memb': m, 'fext': fext, 'pext': proj['namedPaths'],
                'ext': [{'kind': 'file', 'paths': fext}, {'kind': 'package', 'paths': proj['namedPaths']}],
                'files': CE.sort_files([CE.file_row(p) for p in fext]),
                'pkgs': CE.sort_pkgs([CE.pkg_row(n['path'], n['packageName']) for n in proj['named']])}

    def admit(name, w, mode, bindings, universes, retained, domains, contexts, state='complete'):
        try:
            enum = {'schemaVersion': 1, 'snapshotId': CE.SNAP, 'scopeDigest': M.raw_digest(sc), 'membershipDigest': M.raw_digest(w['memb']),
                    'cells': [{'capabilityId': 'inventory', 'languageMode': mode, 'workspaceRoot': '.', 'required': True,
                               'kinds': M._cap_kinds('inventory'), 'programBindings': bindings}]}
            invs = []
            for p in range(len(bindings)):
                if state == 'complete':
                    invs += [CE.inv('file', 'complete', copy.deepcopy(w['files']), w['fext'], prog=p),
                             CE.inv('package', 'complete', copy.deepcopy(w['pkgs']), w['pext'], prog=p)]
                else:
                    carrier = {'deficiency': 'provider-unavailable', 'nativeCause': None}
                    invs += [CE.inv('file', 'unavailable', [], [], prog=p, extra=dict(carrier)),
                             CE.inv('package', 'unavailable', [], [], prog=p, extra=dict(carrier))]
            pd = M.raw_digest(enum)
            for i in invs:
                i['parameterDigest'] = pd
            r = M.admit_enumeration(
                plan=CE.plan_obj(sc), plan_id=CE.PLAN_ID,
                analysis_spec=CE.spec([{'capabilityId': 'inventory', 'languageMode': mode, 'workspaceRoot': '.', 'required': True}]),
                scope_descriptor=sc, membership=w['memb'], enumeration_plan=enum, inventories=invs, native_contexts=contexts,
                universes=universes, closures={CE.PROV: {'kind': 'provider'}, CE.DET: {'kind': 'detector'}},
                snapshot_paths=list(CE.SNAPSHOT), source_blobs=source, retained_inputs=retained, policy_document=None,
                universe_domains=domains)
            res[name] = {'result': r['result'], 'refusals': r['refusals']}
        except Exception:  # noqa: BLE001
            res[name] = {'error': traceback.format_exc()[-1200:]}

    U1, U2, CTX = CE.U1, CE.U2, CE.CTX
    ts = world()
    tsU, tsD, tsC = {U1: CE.uni('ts-tsconfig', roots)}, {U1: CE.TS_DOMAIN}, {CTX: {'languageMode': 'ts-tsconfig'}}
    marker = {U1: {'configGraph': CE.graph('tsconfig.json')}}
    build = {U1: {'configGraph': CE.graph('tsconfig.build.json')}}

    def b(w, entry, prov='default-unit', uni=U1, ordinal=0):
        return CE.binding(ordinal, uni, entry, w['ext'], prov)

    admit('ts-default-null', ts, 'ts-tsconfig', [b(ts, None)], tsU, marker, tsD, tsC)
    admit('ts-default-marker-nonnull', ts, 'ts-tsconfig', [b(ts, 'tsconfig.json')], tsU, marker, tsD, tsC)
    admit('ts-explicit-marker-nonnull', ts, 'ts-tsconfig', [b(ts, 'tsconfig.json', 'explicit-plan-selection')], tsU, marker, tsD, tsC)
    admit('ts-explicit-null-provenance-only-change', ts, 'ts-tsconfig', [b(ts, None, 'explicit-plan-selection')], tsU, marker, tsD, tsC)
    admit('ts-explicit-null-graph-entry-build-config', ts, 'ts-tsconfig', [b(ts, None, 'explicit-plan-selection')], tsU, build, tsD, tsC)
    admit('ts-explicit-build-config-nonnull', ts, 'ts-tsconfig', [b(ts, 'tsconfig.build.json', 'explicit-plan-selection')], tsU, build, tsD, tsC)
    admit('ts-default-null-plus-explicit-build-config', ts, 'ts-tsconfig',
          [b(ts, None), b(ts, 'tsconfig.build.json', 'explicit-plan-selection', U2, 1)],
          {U1: CE.uni('ts-tsconfig', roots), U2: CE.uni('ts-tsconfig', ['src/b.ts'])},
          {U1: {'configGraph': CE.graph('tsconfig.json')}, U2: {'configGraph': CE.graph('tsconfig.build.json')}},
          {U1: CE.TS_DOMAIN, U2: CE.TS_DOMAIN}, tsC)
    ja = world({'languageMode': 'js-allowjs', 'unitKind': 'js-program'})
    jaArgs = ({U1: CE.uni('js-allowjs', roots)}, marker, tsD, {CTX: {'languageMode': 'js-allowjs'}})
    admit('js-allowjs-default-null', ja, 'js-allowjs', [b(ja, None)], *jaArgs)
    admit('js-allowjs-explicit-null', ja, 'js-allowjs', [b(ja, None, 'explicit-plan-selection')], *jaArgs)
    js = world({'languageMode': 'js-synthesized', 'unitKind': 'js-program', 'markerPath': 'package.json', 'recognizerId': 'node-package'})
    jsArgs = ({U1: CE.uni('js-synthesized', roots)}, {U1: {'configGraph': CE.graph(None)}}, tsD, {CTX: {'languageMode': 'js-synthesized'}})
    admit('js-synthesized-default-null', js, 'js-synthesized', [b(js, None)], *jsArgs)
    admit('js-synthesized-explicit-null', js, 'js-synthesized', [b(js, None, 'explicit-plan-selection')], *jsArgs)
    admit('js-synthesized-explicit-package-json-nonnull', js, 'js-synthesized', [b(js, 'package.json', 'explicit-plan-selection')], *jsArgs)
    rsArgs = ({U1: {'nativeContextId': CTX}}, {}, {U1: CE.RUST_DOMAIN}, tsC)
    admit('rust-default-null', ts, 'rust-cargo', [b(ts, None)], *rsArgs)
    admit('rust-default-cargo-nonnull', ts, 'rust-cargo', [b(ts, 'Cargo.toml')], *rsArgs)
    admit('rust-explicit-null', ts, 'rust-cargo', [b(ts, None, 'explicit-plan-selection')], *rsArgs)
    admit('rust-explicit-cargo-nonnull', ts, 'rust-cargo', [b(ts, 'Cargo.toml', 'explicit-plan-selection')], *rsArgs)
    syArgs = ({U1: {'nativeContextId': CTX}}, {}, {U1: 'native.semantic-universe.syntax.v2'}, tsC)
    admit('syntax-default-null', ts, 'syntax-only', [b(ts, None)], *syArgs)
    admit('syntax-default-readme-nonnull', ts, 'syntax-only', [b(ts, 'README.md')], *syArgs)
    admit('syntax-explicit-null', ts, 'syntax-only', [b(ts, None, 'explicit-plan-selection')], *syArgs)
    admit('syntax-explicit-readme-nonnull', ts, 'syntax-only', [b(ts, 'README.md', 'explicit-plan-selection')], *syArgs)

    def ub(entry, prov):
        x = CE.unavail_binding(0, ts['ext'])
        x['programEntry'], x['provenance'] = entry, prov
        return x

    admit('unavailable-default-null', ts, 'ts-tsconfig', [ub(None, 'default-unit')], tsU, marker, tsD, tsC, state='unavailable')
    admit('unavailable-explicit-null', ts, 'ts-tsconfig', [ub(None, 'explicit-plan-selection')], tsU, marker, tsD, tsC, state='unavailable')
    admit('unavailable-default-marker-nonnull', ts, 'ts-tsconfig', [ub('tsconfig.json', 'default-unit')], tsU, marker, tsD, tsC, state='unavailable')
    admit('unavailable-explicit-build-config-nonnull', ts, 'ts-tsconfig', [ub('tsconfig.build.json', 'explicit-plan-selection')], tsU, marker, tsD, tsC,
          state='unavailable')
    Path(outfile).write_text(json.dumps(res, indent=1))


def parent():
    sides, runs = {}, {}
    for label, root in TREES:
        out = RT / ('receipts/probes/program-entry-x.side-' + label + '.json')
        p = subprocess.run([PY, '-I', '-B', __file__, '--child', str(root), label, str(out)], capture_output=True, text=True, timeout=1800)
        runs[label] = {'exitCode': p.returncode, 'stderrTail': p.stderr[-2000:]}
        sides[label] = json.loads(out.read_text()) if out.exists() else {}
    rows = []
    for case, (w41, w42) in EXPECT.items():
        got = {lab: sides[lab].get(case) for lab, _ in TREES}

        def ok(g, want):
            if not g or 'error' in g:
                return False
            if want == 'ADMIT':
                return g['result'] == 'ADMIT'
            return g['result'] == 'REFUSE' and g['refusals'] == [PE]
        rows.append({'case': case, 'ok': ok(got['source41'], w41) and ok(got['source42'], w42),
                     'expected': {'source41': w41, 'source42': w42}, 'observed': got,
                     'discriminating': w41 != w42})
    rows.append({'case': 'children-completed', 'ok': all(r['exitCode'] == 0 for r in runs.values()), 'observed': runs})
    OUT.write_text(json.dumps({'standing': 'independent reviewer enumeration-owner admission probe on source41 and source42 in separate processes; not full Runs',
                               'rows': rows, 'failed': [r for r in rows if not r['ok']]}, indent=1))
    print(json.dumps({'total': len(rows), 'failed': [(r['case'], r['observed']) for r in rows if not r['ok']]}, indent=1)[:8000])


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--child':
        child(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        parent()
