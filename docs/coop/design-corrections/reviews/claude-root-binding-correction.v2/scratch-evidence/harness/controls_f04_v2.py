"""F-04 v2 controls: selector/guard agreement, newline-separated dot segments, legitimate
newline-containing segments, length boundaries, and explicit null/list shape.

Runs the SAME matrix against any tree, so completed v1 and v2 give a directly comparable
before/after. Writes only the JSON path given on argv.

Agreement is measured FOR THE REPRESENTATION BEING CLAIMED: the guard outcome is compared to
declarative validation of the scalar against the selector itself (#/$defs/InternalUnitRootV1 or
#/$defs/CanonicalRelativeDirV1), NOT to full WorkspaceUnitV2 validity. Those are different
questions -- the guard deliberately does not decide `required`, `unitKind` or any other field,
so a minimal caller may be guard-admissible and not a complete unit. Full-unit validity is
reported alongside as information only.
"""
import copy
import importlib.util
import json
import sys

TREE = sys.argv[1]
OUT = sys.argv[2]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


NV = load('nv', TREE + '/docs/coop/design-corrections/native/native_evidence_model.v2.py')
SCHEMAS = NV.SCHEMAS
MAXR = SCHEMAS['$defs']['InternalUnitRootV1']['maxLength']
MAXM = SCHEMAS['$defs']['CanonicalRelativeDirV1']['maxLength']


def law_dir(v):
    """Stated law: split on '/', exact segment equality; only '/', backslash, NUL excluded."""
    if not isinstance(v, str) or v == '':
        return False
    if v.startswith('/') or '\\' in v or '\x00' in v:
        return False
    return not any(s in ('', '.', '..') for s in v.split('/'))


def law_root(v):
    return isinstance(v, str) and (v == '' or law_dir(v))


def selector_ok(selector, value):
    """Declarative validation of ONE scalar against ONE selector."""
    try:
        NV.validate_native(selector, value)
        return True
    except Exception:
        return False


def full_unit_ok(u):
    try:
        NV.validate_native('WorkspaceUnitV2', u)
        return True
    except Exception:
        return False


def guard(units):
    try:
        NV.admit_unit_roots(units)
        return 'ADMIT', None
    except Exception as exc:
        return 'REFUSE', str(exc)[:170]


BASE = {'unitOrdinal': 0, 'languageFamily': 'tsjs', 'languageMode': 'ts-tsconfig',
        'unitKind': 'ts-program', 'markerPath': 'tsconfig.json', 'markerSha256': '0' * 64,
        'recognizerId': 'typescript-config', 'recognizerVersion': 1, 'provenance': 'DISCOVERED'}


def unit(root=..., members=...):
    u = copy.deepcopy(BASE)
    if root is not ...:
        u['rootPath'] = root
    if members is not ...:
        u['memberPackageRoots'] = members
    return u


rows = []


def case(group, name, u, probe=None, law=None, note=None):
    """probe = (selectorName, scalarValue) when the case claims one representation."""
    outcome, detail = guard([u])
    row = {'group': group, 'case': name, 'guard': outcome, 'guardDetail': detail,
           'fullUnitSchemaValid': full_unit_ok(u)}
    if probe is not None:
        sel, val = probe
        sv = selector_ok(sel, val)
        row['selector'] = sel
        row['selectorValid'] = sv
        row['guardAgreesWithSelector'] = (outcome == 'ADMIT') == sv
    if law is not None:
        row['statedLaw'] = law
        row['guardMatchesLaw'] = (outcome == 'ADMIT') == law
    if note:
        row['note'] = note
    rows.append(row)


R = 'InternalUnitRootV1'
M = 'CanonicalRelativeDirV1'

# 1. newline-separated dot segments (root's counterexamples)
for v in ['a\n/../b', 'a\n/./b', '\n/.', '\n/..', 'a\r/../b']:
    case('newline-separated-dot-segment', 'rootPath=%r' % v, unit(v, []), (R, v), law_root(v),
         'exact dot segment after a newline segment; the stated law forbids it')

# 2. legitimate newline-containing segments (the owning grammar permits them)
for v in ['a/.\n', 'a/..\n', 'a\n/b', '.\n', '..\n', 'a\n', 'a/b\n', 'a /b']:
    case('legitimate-newline-segment', 'rootPath=%r' % v, unit(v, []), (R, v), law_root(v),
         'segment holds a newline but is not exactly . or ..; normalize_explicit_root and '
         'ordered() both permit it')

# 3. settled cases
for v in ['', 'crates/alpha', 'crates/foo#bar', '.hidden', 'a/.hidden', '..a', 'a..', 'a b',
          'deep/a/b/c/d', '...', '.', '..', 'crates/alpha/', 'crates//alpha', '/abs',
          'a/./b', 'a/../b', 'a\\b', 'a\x00b']:
    case('settled', 'rootPath=%r' % v, unit(v, []), (R, v), law_root(v))

# 4. length boundary and overlong
case('length-boundary', 'rootPath at maxLength=%d' % MAXR, unit('a' * MAXR, []),
     (R, 'a' * MAXR), True, 'exactly the declared bound must admit')
case('length-boundary', 'rootPath overlong=%d' % (MAXR + 1), unit('a' * (MAXR + 1), []),
     (R, 'a' * (MAXR + 1)), False, 'one over the bound; the pattern alone cannot see this')
seg = ('ab/' * ((MAXR // 3) + 2))[:MAXR]
seg = seg if not seg.endswith('/') else seg[:-1] + 'z'
case('length-boundary', 'rootPath multi-segment at maxLength', unit(seg, []), (R, seg),
     law_root(seg), 'segment-structured value at the bound')
case('length-boundary', 'member at maxLength=%d' % MAXM, unit('', ['a' * MAXM]),
     (M, 'a' * MAXM), None, 'member entry exactly at the bound')
case('length-boundary', 'member overlong=%d' % (MAXM + 1), unit('', ['a' * (MAXM + 1)]),
     (M, 'a' * (MAXM + 1)), None, 'member entry one over the bound')
case('length-boundary', 'member empty (minLength=1)', unit('', ['']), (M, ''), None,
     'CanonicalRelativeDirV1 has minLength 1; the project root is not a member root')

# 5. explicit null and list shape
case('shape', 'memberPackageRoots ABSENT (minimal caller)', unit('', ...), (R, ''), None,
     'permitted: the guard owns the root representation; _cargo_roots_of_units already reads '
     'this key with .get(..., []). Full-unit validity is a separate question.')
case('shape', 'memberPackageRoots = null', unit('', None), None, None,
     'present and explicitly null is not a list of roots')
case('shape', 'memberPackageRoots = "crates/alpha"', unit('', 'crates/alpha'), None, None, 'not a list')
case('shape', 'memberPackageRoots = {}', unit('', {}), None, None, 'not a list')
case('shape', 'memberPackageRoots = [null]', unit('', [None]), (M, None), None, 'null element')
case('shape', 'memberPackageRoots = [123]', unit('', [123]), (M, 123), None, 'non-string element')
case('shape', 'memberPackageRoots = ["."]', unit('', ['.']), (M, '.'), None, 'external sentinel')
case('shape', 'memberPackageRoots = ["crates/alpha"]', unit('', ['crates/alpha']),
     (M, 'crates/alpha'), None, 'lawful')
case('shape', 'rootPath ABSENT', unit(..., []), None, None,
     'rootPath is required by the schema and is the field this guard owns')
case('shape', 'rootPath = null', unit(None, []), (R, None), None, 'explicitly null')
case('shape', 'rootPath = 0', unit(0, []), (R, 0), None, 'non-string scalar')
case('shape', 'rootPath = True', unit(True, []), (R, True), None, 'non-string scalar')
case('shape', 'rootPath = ["a"]', unit(['a'], []), (R, ['a']), None, 'non-string')

# 6. container shape
for name, arg in [('units = null', None), ('units = {}', {}), ('units = "x"', 'x'),
                  ('units = [null]', [None]), ('units = [123]', [123])]:
    outcome, detail = guard(arg)
    rows.append({'group': 'container-shape', 'case': name, 'guard': outcome,
                 'guardDetail': detail})

lawrows = [r for r in rows if 'guardMatchesLaw' in r]
selrows = [r for r in rows if 'guardAgreesWithSelector' in r]
summary = {
    'tree': TREE, 'total': len(rows),
    'lawCheckedRows': len(lawrows),
    'lawMismatches': [r['case'] for r in lawrows if not r['guardMatchesLaw']],
    'selectorCheckedRows': len(selrows),
    'selectorGuardDisagreements': [r['case'] for r in selrows if not r['guardAgreesWithSelector']],
}
print(json.dumps(summary, indent=1))
print()
for r in rows:
    flag = ''
    if r.get('guardMatchesLaw') is False:
        flag = '  <-- LAW MISMATCH'
    elif r.get('guardAgreesWithSelector') is False:
        flag = '  <-- SELECTOR/GUARD DISAGREE'
    print('%-30s %-42s guard=%-7s selector=%-5s unit=%-5s%s'
          % (r['group'], r['case'][:42], r['guard'],
             r.get('selectorValid'), r.get('fullUnitSchemaValid'), flag))

json.dump({'standing': 'F-04 v2 controls; author-assisted reference evidence, not acceptance.',
           'summary': summary, 'rows': rows}, open(OUT, 'w'), indent=1)
