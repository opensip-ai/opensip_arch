"""DECISIVE PROBE for RRS-A1's hypothesised asymmetric case.

Question: does the enumeration owner ADMIT a Plan in which universe U2 is a SELECTED,
AVAILABLE binding on a symbol-only cell whose symbol extent contains a path, while U2 has NO
binding on the inventory cell and therefore no file inventory and no lawful file@enumerated
subject scope?

If it ADMITS, the structural omission root describes is reachable in retained evidence.
If it REFUSES, admission already prevents it and I say so rather than invent it.

Scope: this drives the enumeration owner's OWN admission
(enumeration_model.v1.admit_enumeration) through the frozen checker's own helpers and shapes.
It is NOT a full Run and is not claimed to be. It qualifies no native producer.
"""
import importlib.util, json, sys
from pathlib import Path

SRC = Path('/tmp/opensip-design-corrections/repair-selection-successor.v2/source')
FOUND = SRC / 'docs/coop/design-corrections/foundation'
sys.path.insert(0, str(FOUND))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CH = load('enum_check', FOUND / 'check-enumeration.v1.py')
M = CH.M

memb = CH.membership()
sc = CH.scope()
faults = []
file_ext = M.host_file_extent(memb, CH.SNAPSHOT, sc, '.', faults)
source = CH.blobs()
pkg_proj = M.project_named_packages(CH.SNAPSHOT, sc, '.', memb, source, [])
pkg_ext = pkg_proj['namedPaths']
inv_ext = [{'kind': 'file', 'paths': file_ext}, {'kind': 'package', 'paths': pkg_ext}]
files = CH.sort_files([CH.file_row(p) for p in file_ext])
pkgs = CH.sort_pkgs([CH.pkg_row(n['path'], n['packageName']) for n in pkg_proj['named']])

u1 = CH.uni('ts-tsconfig', ['src/a.ts', 'src/b.ts', 'src/extra.js'])
u2 = CH.uni('ts-tsconfig', ['src/b.ts'])
retained = {CH.U1: {'configGraph': CH.graph('tsconfig.json')},
            CH.U2: {'configGraph': CH.graph('tsconfig.build.json')}}
sym_ext_u2 = M.host_symbol_extent(memb, CH.SNAPSHOT, sc, '.', 'ts-tsconfig', u2, retained[CH.U2], [])
fallback_sym = M.host_symbol_extent(memb, CH.SNAPSHOT, sc, '.', 'ts-tsconfig', None, None, [])
print('file extent        ', file_ext)
print('package extent     ', pkg_ext)
print('U2 symbol extent   ', sym_ext_u2)
print('fallback symbol ext', fallback_sym)

spec_asym = CH.spec([
    {'capabilityId': 'inventory', 'languageMode': 'ts-tsconfig', 'workspaceRoot': '.', 'required': True},
    {'capabilityId': 'syntax', 'languageMode': 'ts-tsconfig', 'workspaceRoot': '.', 'required': True},
])


def plan_cells(sym_bindings):
    return {'schemaVersion': 1, 'snapshotId': CH.SNAP, 'scopeDigest': M.raw_digest(sc),
            'membershipDigest': M.raw_digest(memb),
            'cells': [
                {'capabilityId': 'inventory', 'languageMode': 'ts-tsconfig', 'workspaceRoot': '.',
                 'required': True, 'kinds': M._cap_kinds('inventory'),
                 'programBindings': [CH.binding(0, CH.U1, None, inv_ext)]},
                {'capabilityId': 'syntax', 'languageMode': 'ts-tsconfig', 'workspaceRoot': '.',
                 'required': True, 'kinds': M._cap_kinds('syntax'),
                 'programBindings': sym_bindings},
            ]}


# --- CASE B: the hypothesised asymmetry, constructed exactly as the frozen checker's own
# `alternate-program-symbol-extents` case constructs an alternate program.
ep_asym = plan_cells([CH.binding(0, CH.U2, 'tsconfig.build.json',
                                 [{'kind': 'symbol', 'paths': sym_ext_u2}], 'explicit-plan-selection')])
res_b = CH.admit(ep_asym, [CH.inv('file', 'complete', files, file_ext, cell=0, prog=0),
                           CH.inv('package', 'complete', pkgs, pkg_ext, cell=0, prog=0),
                           CH.inv('symbol', 'complete',
                                  [CH.sym_row('ts-symbol:src/b.ts#h', 'src/b.ts')],
                                  sym_ext_u2, cell=1, prog=0)],
                 memb, sc, {CH.U1: u1, CH.U2: u2}, retained, source, spec_obj=spec_asym)
print('\nCASE B  symbol-only SELECTED AVAILABLE universe, no file inventory ->', res_b['result'])
print('  refusals :', res_b['refusals'])
print('  subjects :', sorted(res_b.get('subjects') or {}))

# --- CASE C: an UNAVAILABLE selected binding whose retained host extent contains the path.
ep_unavail = plan_cells([CH.unavail_binding(0, [{'kind': 'symbol', 'paths': fallback_sym}])])
res_c = CH.admit(ep_unavail, [CH.inv('file', 'complete', files, file_ext, cell=0, prog=0),
                              CH.inv('package', 'complete', pkgs, pkg_ext, cell=0, prog=0),
                              CH.inv('symbol', 'unavailable', [], [], cell=1, prog=0,
                                     extra={'deficiency': 'provider-unavailable', 'nativeCause': None})],
                 memb, sc, {CH.U1: u1}, retained, source, spec_obj=spec_asym,
                 universe_domains={CH.U1: CH.TS_DOMAIN})
print('\nCASE C  UNAVAILABLE selected binding retaining a host symbol extent ->', res_c['result'])
print('  refusals :', res_c['refusals'])
print('  retained extent contains src/b.ts:', 'src/b.ts' in fallback_sym)

# --- CASE D: candidate-only cell census.
spec_cand = CH.spec([
    {'capabilityId': 'clones-near', 'languageMode': 'ts-tsconfig', 'workspaceRoot': '.', 'required': True},
    {'capabilityId': 'inventory', 'languageMode': 'ts-tsconfig', 'workspaceRoot': '.', 'required': True},
])
# cells are sorted by (capabilityId, languageMode, workspaceRoot): `clones-near` precedes
# `inventory`, so the candidate cell is cellOrdinal 0 and the inventory cell is 1.
ep_cand = {'schemaVersion': 1, 'snapshotId': CH.SNAP, 'scopeDigest': M.raw_digest(sc),
           'membershipDigest': M.raw_digest(memb),
           'cells': [
               {'capabilityId': 'clones-near', 'languageMode': 'ts-tsconfig', 'workspaceRoot': '.',
                'required': True, 'kinds': M._cap_kinds('clones-near'),
                'programBindings': [CH.binding(0, CH.U2, 'tsconfig.build.json', [],
                                               'explicit-plan-selection',
                                               candidate_source_paths=['src/b.ts'])]},
               {'capabilityId': 'inventory', 'languageMode': 'ts-tsconfig', 'workspaceRoot': '.',
                'required': True, 'kinds': M._cap_kinds('inventory'),
                'programBindings': [CH.binding(0, CH.U1, None, inv_ext)]},
           ]}
res_d = CH.admit(ep_cand, [CH.inv('file', 'complete', files, file_ext, cell=1, prog=0),
                           CH.inv('package', 'complete', pkgs, pkg_ext, cell=1, prog=0)],
                 memb, sc, {CH.U1: u1, CH.U2: u2}, retained, source, spec_obj=spec_cand)
print('\nCASE D  candidate-only cell with candidateSourcePaths ->', res_d['result'])
print('  refusals :', res_d['refusals'])
print('  cap kinds for clones-near:', M._cap_kinds('clones-near'))

out = {
    'standing': 'enumeration-owner admission only; NOT a full Run; qualifies no native producer',
    'snapshot': list(CH.SNAPSHOT),
    'fileExtent': file_ext, 'packageExtent': pkg_ext,
    'u2SymbolExtent': sym_ext_u2, 'unavailableFallbackSymbolExtent': fallback_sym,
    'caseB_symbolOnlySelectedAvailableUniverse': {'result': res_b['result'], 'refusals': res_b['refusals']},
    'caseC_unavailableSelectedBinding': {'result': res_c['result'], 'refusals': res_c['refusals']},
    'caseD_candidateOnlyCell': {'result': res_d['result'], 'refusals': res_d['refusals']},
}
Path(__file__).resolve().parent.joinpath('symbol-only-admission.json').write_text(
    json.dumps(out, indent=2) + '\n')
print('\nWROTE symbol-only-admission.json')
