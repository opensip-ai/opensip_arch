#!/usr/bin/env python3
"""Probe 09 (independent): CB5-MUST-2 / CX-BV5-01.

Two halves, both against the exact frozen bytes:

A. THE FOLD ITSELF. Measure lib_name_fold against the three operations the
   published discriminator table distinguishes, confirm it is the FULL
   context-sensitive default lowercase (not Simple_Lowercase_Mapping, not
   Case_Folding), confirm locale independence, confirm the declared UCD binding
   is EFFECTIVE (it refuses when the declared case data is unavailable) and that
   the refusal is a ReferenceEnvironmentError and NOT an AdmissionError.

   The unavailable-case-data condition is SIMULATED by substituting the module's
   `unicodedata` binding. No alternate Unicode case data was executed and no
   public host fault route was exercised; that limit is recorded, not hidden.

B. THE JOIN, at real context admission. Valid library selections admit; and
   malformed / missing / ambiguous context inputs each refuse with the exact
   published typed refusal. Both directions are exercised.
"""
import copy, hashlib, importlib.util, json, os, sys, types

ROOT = '/tmp/opensip-design-corrections/post-reset-review.v16/copy-B-probes'
OUT = '/tmp/opensip-design-corrections/post-reset-review.v16'
DC = os.path.join(ROOT, 'docs/coop/design-corrections')

def sha256(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

sp = importlib.util.spec_from_file_location('rev16_fix9', os.path.join(DC, 'integration-fixtures.py'))
F = importlib.util.module_from_spec(sp); sys.modules['rev16_fix9'] = sp and F
sp.loader.exec_module(F)
N = F.N
import unicodedata

# ---------------------------------------------------------------- A. the fold
fold_rows = []
def fold_case(cid, s, exp_full, why):
    try:
        got = N.lib_name_fold(s); err = None
    except Exception as e:
        got, err = None, type(e).__name__
    fold_rows.append({
        'id': cid, 'input': [f'U+{ord(c):04X}' for c in s], 'inputStr': s,
        'expectedFold': [f'U+{ord(c):04X}' for c in exp_full],
        'observedFold': [f'U+{ord(c):04X}' for c in got] if got is not None else None,
        'agrees': got == exp_full,
        'casefoldWouldGive': [f'U+{ord(c):04X}' for c in s.casefold()],
        'foldDiffersFromCasefold': (got != s.casefold()) if got is not None else None,
        'error': err, 'why': why})

fold_case('F1-U0130-full-expansion', 'İ', 'i̇',
          'FULL mapping expands to TWO code points; Simple_Lowercase_Mapping would give U+0069 only')
fold_case('F2-final-sigma', 'ΟΣ', 'ος',
          'CONTEXT-SENSITIVE: Final_Sigma condition yields U+03C2, which no per-code-point map can do')
fold_case('F3-nonfinal-sigma', 'ΣΟ', 'σο',
          'the same sigma NOT in final position yields U+03C3 - position dependence is real')
fold_case('F4-sharp-s-unchanged', 'ß', 'ß',
          'NOT Case_Folding: casefold would give "ss" and change the admitted component name')
fold_case('F5-ascii-lib-name', 'ES2022', 'es2022',
          'the pinned compiler vocabulary is ASCII, where all three operations coincide')
fold_case('F6-ascii-dom', 'DOM', 'dom', 'the second live lib name')
fold_case('F7-idempotent', 'es2022', 'es2022', 'already-folded input is a fixed point')

# discriminating control: fold is NOT casefold on the whole vocabulary tested
fold_vs_casefold_differs = [r['id'] for r in fold_rows if r['foldDiffersFromCasefold']]

# locale independence: the fold must not consult an ambient locale
import locale as _locale
locale_probe = {'attemptedLocales': [], 'foldStable': True, 'observed': {}}
for loc in ('tr_TR.UTF-8', 'lt_LT.UTF-8', 'C', ''):
    try:
        _locale.setlocale(_locale.LC_ALL, loc)
        applied = True
    except Exception as e:
        applied = False
    v = N.lib_name_fold('I') + '|' + N.lib_name_fold('İ')
    locale_probe['attemptedLocales'].append({'locale': loc, 'applied': applied})
    locale_probe['observed'][loc or '(empty)'] = [f'U+{ord(c):04X}' for c in v]
try:
    _locale.setlocale(_locale.LC_ALL, 'C')
except Exception:
    pass
vals = set(map(tuple, locale_probe['observed'].values()))
locale_probe['foldStable'] = len(vals) == 1
locale_probe['note'] = ('Turkish/Lithuanian tailoring would change U+0049/U+0130 if the fold were '
                        'locale-sensitive. Whether the OS actually applied each locale is recorded; '
                        'stability across the attempts that DID apply is the measurement.')

# the version binding must be EFFECTIVE, not advertised
gate = {'declared': N.UNICODE_CASE_DATA_VERSION,
        'running': unicodedata.unidata_version,
        'agreementReport': N.unicode_case_data_agreement(),
        'referenceEnvironmentErrorIsNotAdmissionError':
            not issubclass(N.ReferenceEnvironmentError, N.AdmissionError),
        'referenceEnvironmentErrorMro': [c.__name__ for c in N.ReferenceEnvironmentError.__mro__],
        'simulationMethod': 'substituted the module-level `unicodedata` binding with a stub whose '
                            'unidata_version differs; NO alternate Unicode case data was executed '
                            'and NO public host fault route was exercised',
        }
_real = N.unicodedata
try:
    N.unicodedata = types.SimpleNamespace(unidata_version='14.0.0')
    try:
        N.lib_name_fold('ES2022')
        gate['simulatedUnavailableDeclaredVersion'] = 'ADMITTED (gate is NOT effective)'
        gate['gateEffective'] = False
        gate['raisedType'] = None
    except N.ReferenceEnvironmentError as e:
        gate['simulatedUnavailableDeclaredVersion'] = 'REFUSED'
        gate['gateEffective'] = True
        gate['raisedType'] = 'ReferenceEnvironmentError'
        gate['message'] = str(e)[:300]
    except N.AdmissionError as e:
        gate['simulatedUnavailableDeclaredVersion'] = 'REFUSED as AdmissionError (WRONG TYPE)'
        gate['gateEffective'] = True
        gate['raisedType'] = 'AdmissionError'
    # and the join site must propagate it as an environment fault, not a typed lib refusal
    try:
        N.lib_name_fold('DOM')
        gate['joinSiteUnderUnavailableData'] = 'no raise'
    except Exception as e:
        gate['joinSiteUnderUnavailableData'] = type(e).__name__
finally:
    N.unicodedata = _real
gate['restoredRunningVersion'] = N.unicode_case_data_agreement()

# ------------------------------------------------- B. the join at admission
def build_ts_context(stdlib_files=None, mutate=None, declared_components=None):
    """Reconstruct the admitted TypeScript context the same way the reference
    fixture does, then apply a mutation before admission."""
    objects, blobs = {}, {}
    def blob(b):
        d = hashlib.sha256(b).hexdigest(); blobs[d] = b; return d
    def add(domain, **v):
        # schemaVersion 2 is a const in the foundation `closure` schema; the reference
        # fixture's own helper supplies it, and omitting it was a harness error in my
        # first attempt (failed-attempt-03).
        v = {'schemaVersion': 2, **v}
        key = F.M.identifier(domain, v); objects[key] = (domain, v); return key
    if stdlib_files is None:
        stdlib_files = {'lib/lib.dom.d.ts': b'declare const dom: unknown;\n',
                        'lib/lib.es2022.d.ts': b'declare const es2022: unknown;\n'}
    tool_files = {'bin/node': b'#!fixture-runtime\n', 'lib/tsc.js': b'// fixture compiler\n'}
    def tree(files):
        return sorted(({'path': p, 'sha256': blob(b), 'bytes': len(b)} for p, b in files.items()),
                      key=lambda r: r['path'].encode())
    stdlib = add('closure', kind='stdlib', manifestDigest=blob(b'fixture-stdlib-manifest'),
                 tree=tree(stdlib_files), semanticVersion='5.6.3', protocolMajor=2, platform='any')
    toolchain = add('closure', kind='toolchain', manifestDigest=blob(b'fixture-toolchain-manifest'),
                    tree=tree(tool_files), semanticVersion='5.6.3', protocolMajor=2,
                    platform='macos-aarch64')
    tool_tree = {r['path']: r['sha256'] for r in objects[toolchain][1]['tree']}
    ctx = copy.deepcopy(F.NATIVE_FIXTURES['tsNativeContext'])
    ctx['toolchain'].update(
        compilerVersion='5.6.3', compilerPackageDigest=tool_tree['lib/tsc.js'],
        typescriptStdlibMerkleRoot=stdlib.removeprefix('closure2:'),
        libSelection=['dom', 'es2022'],
        standardLibraryComponentDigests=(declared_components(blobs) if declared_components else sorted(
            ({'component': p.rpartition('/')[2], 'sha256': blob(b)} for p, b in stdlib_files.items()),
            key=lambda r: r['component'].encode())))
    ctx['toolClosure'] = {'closureId': toolchain, 'compiler': tool_tree['lib/tsc.js'],
                          'runtime': tool_tree['bin/node']}
    ctx['configProjection']['honoredOptions']['lib'] = ['DOM', 'ES2022']
    ctx['configProjection']['configGraphPaths'] = sorted(
        ['tsconfig.base.json', 'tsconfig.json', 'tsconfig.strict.json'])
    ctx['lockfileIdentity'] = {'kind': 'package-lock', 'path': 'package-lock.json',
                               'contentSha256': hashlib.sha256(F.TS_SOURCES['package-lock.json']).hexdigest()}
    layout = {'schemaVersion': 1, 'entries': sorted(
        ({'packageName': json.loads(body)['name'], 'packageVersion': json.loads(body)['version'],
          'installPath': path.rpartition('/package.json')[0],
          'realPath': path.rpartition('/package.json')[0], 'contentSha256': blob(body)}
         for path, body in F.TS_NODE_MODULES.items()), key=lambda r: r['installPath'].encode())}
    ctx['nodeModulesLayoutDigest'] = N.resolved_node_modules_layout_digest(layout)
    if mutate:
        mutate(ctx)
    trees = {k: objects[k][1] for k in (stdlib, toolchain)}
    return N.admit_native_context('typescript', ctx, trees)

join_rows = []
def join_case(cid, group, exp_refusals, why, stdlib_files=None, mutate=None,
              declared_components=None):
    try:
        out = build_ts_context(stdlib_files, mutate, declared_components)
        obs = sorted(out['refusals']); err = None
    except Exception as e:
        obs, err = None, type(e).__name__ + ':' + str(e)[:250]
    ok = (obs is not None and sorted(exp_refusals) == obs)
    join_rows.append({'id': cid, 'group': group, 'expectedRefusals': sorted(exp_refusals),
                      'observedRefusals': obs, 'agrees': ok, 'error': err, 'why': why})

# positive control: the ordinary valid selection admits with zero refusals
join_case('J0-valid-selection', 'POSITIVE CONTROL', [],
          'libSelection ["dom","es2022"] vs honoredOptions ["DOM","ES2022"]: the fold makes these '
          'agree, and both components are in the retained complete inventory')

def m_libnotretained(c):
    c['toolchain']['libSelection'] = ['dom', 'es2022', 'esnext']
    c['configProjection']['honoredOptions']['lib'] = ['DOM', 'ES2022', 'ESNext']
join_case('J1-lib-not-retained', 'MISSING: selected lib absent from the retained tree',
          ['native.native-context-lib-not-retained:esnext'],
          'component("esnext") = lib.esnext.d.ts is not a declared component',
          mutate=m_libnotretained)

def m_disagree(c):
    c['configProjection']['honoredOptions']['lib'] = ['DOM']
join_case('J2-honoredOptions-set-disagreement', 'CONFIGURATION AGREEMENT',
          ['native.native-context-field-mismatch:libSelection'],
          'the folded name sets must be equal; the mapping does not weaken this',
          mutate=m_disagree)

def m_case_disagree(c):
    # SPELLING/CASE: honoredOptions carries a name that folds to something else entirely
    c['configProjection']['honoredOptions']['lib'] = ['DOM', 'ES2021']
join_case('J3-case-insensitive-but-not-name-insensitive', 'SPELLING: fold is not a fuzzy match',
          ['native.native-context-field-mismatch:libSelection'],
          'the fold normalises CASE only - a different NAME still disagrees',
          mutate=m_case_disagree)

def m_dupfold(c):
    c['toolchain']['libSelection'] = ['ES2022', 'dom', 'es2022']
    c['configProjection']['honoredOptions']['lib'] = ['DOM', 'ES2022']
join_case('J4-duplicate-under-fold', 'DUPLICATE under the fold',
          ['native.native-context-field-mismatch:duplicate-lib-selection'],
          'two entries with the same fold are refused. The array IS in raw-UTF-8-byte order '
          '(ES2022 < dom < es2022), so the ORDER rule is correctly silent: the order is over '
          'the retained UNFOLDED bytes, not a case-insensitive comparison.',
          mutate=m_dupfold)

def m_order(c):
    c['toolchain']['libSelection'] = ['es2022', 'dom']
join_case('J5-libSelection-order', 'ORDER: sorted by raw UTF-8 bytes of the UNFOLDED names',
          ['native.native-context-field-mismatch:lib-selection-order'],
          'each record keeps its own specified order for hashing',
          mutate=m_order)

def m_incomplete(c):
    c['toolchain']['standardLibraryComponentDigests'] = [
        r for r in c['toolchain']['standardLibraryComponentDigests'] if r['component'] != 'lib.dom.d.ts']
    c['toolchain']['libSelection'] = ['es2022']
    c['configProjection']['honoredOptions']['lib'] = ['ES2022']
join_case('J6-inventory-incomplete', 'COMPLETE INVENTORY: an unselected row may not be dropped',
          ['native.native-context-stdlib-inventory-incomplete:lib.dom.d.ts'],
          'the row set is the COMPLETE declaration inventory, selected or not',
          mutate=m_incomplete)

AMBIG = {'lib/lib.dom.d.ts': b'declare const dom: unknown;\n',
         'lib/lib.es2022.d.ts': b'declare const es2022: unknown;\n',
         'other/lib.es2022.d.ts': b'declare const other: unknown;\n'}
def ambig_declared(blobs):
    # unique declared basenames; the digest is the one the tree join actually lands on
    # (tree order puts other/lib.es2022.d.ts last, so by_component keeps its digest)
    d = {p.rpartition('/')[2]: hashlib.sha256(b).hexdigest() for p, b in AMBIG.items()}
    return sorted(({'component': c, 'sha256': h} for c, h in d.items()),
                  key=lambda r: r['component'].encode())
join_case('J7-ambiguous-basename', 'AMBIGUOUS: two tree paths, one basename',
          ['native.native-context-stdlib-tree-ambiguous-basename:lib.es2022.d.ts'],
          'the mapping target would not be unique; refused rather than resolved arbitrarily',
          stdlib_files=AMBIG, declared_components=ambig_declared)
join_case('J7b-declared-duplicate-basename', 'AMBIGUOUS: duplicated DECLARED component',
          ['native.native-context-field-mismatch:stdlib-component-order'],
          'a declared inventory that itself repeats a basename is refused by the '
          'uniqueness/order rule - a separate, correctly firing refusal',
          stdlib_files=AMBIG)

def m_tree_mismatch(c):
    rows = c['toolchain']['standardLibraryComponentDigests']
    for r in rows:
        if r['component'] == 'lib.dom.d.ts':
            r['sha256'] = 'f' * 64
join_case('J8-tree-digest-mismatch', 'RETAINED TREE DIGEST must match',
          ['native.native-context-stdlib-tree-mismatch:lib.dom.d.ts'],
          'the declared row digest must equal the retained tree blob digest',
          mutate=m_tree_mismatch)

def m_component_order(c):
    c['toolchain']['standardLibraryComponentDigests'] = list(
        reversed(c['toolchain']['standardLibraryComponentDigests']))
join_case('J9-component-order', 'ORDER: components sorted by raw UTF-8 bytes of component',
          ['native.native-context-field-mismatch:stdlib-component-order'],
          'declared array order is load-bearing for hashing',
          mutate=m_component_order)

def m_alternate_repr(c):
    # NO IMPLICIT ALTERNATE REPRESENTATION: libSelection must not be re-spelled as file names
    c['toolchain']['libSelection'] = ['lib.dom.d.ts', 'lib.es2022.d.ts']
    c['configProjection']['honoredOptions']['lib'] = ['lib.dom.d.ts', 'lib.es2022.d.ts']
join_case('J10-no-alternate-representation', 'NO implicit alternate representation',
          ['native.native-context-lib-not-retained:lib.dom.d.ts',
           'native.native-context-lib-not-retained:lib.es2022.d.ts'],
          'declaration-file names in libSelection map to lib.lib.dom.d.ts.d.ts and are refused; '
          'the mapping is one-directional and a component is never mapped back',
          mutate=m_alternate_repr)

res = {
    'probe': 'probe-09-lib-fold-and-context',
    'copyName': 'copy-B-probes',
    'boundSourceSha256': {p: sha256(os.path.join(DC, p)) for p in [
        'native/native_evidence_model.v2.py', 'native/native-evidence.schemas.v2.json',
        'integration-fixtures.py']},
    'foldCases': len(fold_rows), 'foldAgree': sum(1 for r in fold_rows if r['agrees']),
    'foldDisagree': [r for r in fold_rows if not r['agrees']],
    'foldDiffersFromCasefoldOn': fold_vs_casefold_differs,
    'localeIndependence': locale_probe,
    'versionBindingGate': gate,
    'joinCases': len(join_rows), 'joinAgree': sum(1 for r in join_rows if r['agrees']),
    'joinDisagree': [r for r in join_rows if not r['agrees']],
    'foldRows': fold_rows, 'joinRows': join_rows,
    'limits': [
        'The unavailable-declared-case-data condition is SIMULATED by substituting the module '
        'binding. No alternate Unicode case data was installed or executed.',
        'No public host fault route (section 10 operational-failed / exit 4) was exercised; only '
        'the exception type and its non-AdmissionError ancestry were measured.',
        'Pure reference admission over synthetic in-memory inputs. No real TypeScript compiler, '
        'filesystem stdlib or product host was exercised.',
        'The published simple-lowercase column is a UCD property this probe does not independently '
        'recompute; what is measured is that the fold IS the full context-sensitive mapping and is '
        'NOT case folding.',
    ],
    'notProductQualification': True,
}
with open(os.path.join(OUT, 'probe-09-lib-fold-and-context.result.json'), 'w') as f:
    json.dump(res, f, indent=2, sort_keys=True, default=str)
print(json.dumps({k: v for k, v in res.items() if k not in ('foldRows', 'joinRows')},
                 indent=2, sort_keys=True, default=str))
