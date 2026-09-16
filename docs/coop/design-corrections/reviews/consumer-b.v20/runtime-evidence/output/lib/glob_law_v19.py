"""S2 CLOSED: the portable glob contract arrived in this kit, so the matching predicate is now
reconstructed from published law instead of being reported as an unstated case.

What this measures:

  1. every one of the TWENTY required examples of
     foundation/glob-pattern-contract.v1.md, against this origin's own independent predicate
     (opensip_eval.glob_match). The table is the kit's, the implementation is this origin's.
  2. the properties the prose states and the table does not exhaust: anchoring, case sensitivity,
     no dotfile exclusion, `?` counting SCALARS rather than graphemes, no escape syntax, trailing
     slash as an empty final segment, no `.`/`..` resolution, and `**` at beginning / middle / end.
  3. the ScopeDocument composition law (include-any AND not-exclude-any, exclusion wins).
  4. WHAT THIS CHANGED IN THIS ORIGIN'S OWN RECONSTRUCTION, measured rather than assumed: the
     previous generation implemented the other reading of a terminal `**`, so every glob actually
     used by this origin's Runs, rules and repair descriptor is re-evaluated under both readings
     and the difference is reported per pattern.

Standing: this closes the generation-16 SHOULD V16-S2 on PUBLISHED LAW. It is not a claim about
any implementation outside this runtime, and the contract itself says scope selection "is not
evidence of exhaustive extraction or native coverage".
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_eval as E

OUT = '/tmp/opensip-design-corrections/consumer-b.v20/output'

# The kit's own required-example table, transcribed with its exact expectations.
REQUIRED = [
    ('**/*.ts', 'a.ts', True),
    ('**/*.ts', 'src/nested/a.ts', True),
    ('*.ts', 'src/a.ts', False),
    ('src/**', 'src', True),
    ('src/**', 'src/legacy.js', True),
    ('src/**', 'src/nested/legacy.js', True),
    ('src/**/*', 'src', False),
    ('src/**/*', 'src/legacy.js', True),
    ('a/**/b', 'a/b', True),
    ('a/**/b', 'a/x/y/b', True),
    ('a/*/b', 'a/b', False),
    ('a**b', 'a/x/b', False),
    ('a**b', 'axxb', True),
    ('*', '.hidden', True),
    ('a.ts', 'A.ts', False),
    ('a.ts', 'a.ts.extra', False),
    ('?.ts', 'é.ts', True),                 # one scalar before the dot
    ('?.ts', 'é.ts', False),               # `e` plus combining acute accent
    ('[ab].ts', 'a.ts', False),
    ('[ab].ts', '[ab].ts', True),
    ('{a,b}.ts', 'a.ts', False),
    ('{a,b}.ts', '{a,b}.ts', True),
    ('src/', 'src', False),                      # trailing slash is an empty final segment
]

# Properties the prose states, derived by this origin from the law rather than from the table.
DERIVED = [
    ('**', 'a', True, 'a single `**` matches one segment (zero or more, applied at the end)'),
    ('**', '', True, 'and the empty candidate, which splits to one empty segment'),
    ('**/**', 'a/b', True, 'two `**` segments may split the same candidate'),
    ('a/**', 'a', True, 'terminal `**` consumes zero segments, so the parent itself matches'),
    ('**/a', 'a', True, 'leading `**/` consumes zero segments'),
    ('**/a', 'x/y/a', True, 'leading `**/` consumes several'),
    ('a/**/b/**', 'a/b', True, 'both `**` consume zero'),
    ('*', 'a/b', False, '`*` never consumes a separator'),
    ('?', 'ab', False, '`?` is exactly one scalar'),
    ('a?c', 'abc', True, '`?` inside an ordinary segment'),
    ('**.ts', 'a.ts', True, '`**.ts` is an ORDINARY segment: two stars have one star\'s power'),
    ('**.ts', 'x/a.ts', False, 'and it cannot consume a separator'),
    ('a/./b', 'a/b', False, '`.` is not resolved'),
    ('a/../b', 'b', False, '`..` is not resolved'),
    ('A*', 'a.ts', False, 'case sensitive'),
    ('.*', '.hidden', True, 'dotfiles are not excluded'),
    ('*.ts', '.hidden.ts', True, 'and a leading dot is an ordinary character'),
    ('a\\b', 'a\\b', True, 'no escape syntax: a backslash is literal where a field admits one'),
    ('', '', True, 'the empty pattern matches only the empty candidate'),
    ('', 'a', False, 'and nothing else'),
    ('a//b', 'a//b', True, 'empty segments are preserved on both sides'),
    ('a//b', 'a/b', False, 'so they must line up'),
]

COMPOSITION = [
    (['src/**'], [], 'src/a.js', True, 'one include matches'),
    (['src/**'], ['src/**/*.test.js'], 'src/a.test.js', False, 'exclusion wins'),
    (['src/**'], ['src/**/*.test.js'], 'src/a.js', True, 'a non-matching exclude does not block'),
    ([], [], 'src/a.js', False,
     'with NO include pattern nothing is selected by this composition law; absent/empty-list '
     'behaviour belongs to the owning field, which is why the predicate takes it as a parameter'),
    (['**'], ['**'], 'a', False, 'exclusion wins even over a universal include'),
]

# Every glob this origin's own reconstruction actually uses, and the OLD reading it used before.
USED_BY_THIS_ORIGIN = [
    ('src/**/*.js', 'lib/run_syntax_code_full.py policy rule.no-duplicate-body '
                    'subjectEnumeration.include'),
    ('src/**/*', 'lib/phase6_repair.py RepairPlanDescriptor.permittedEditScope'),
    ('src/**/*.ts', 'lib/run_ts_full.py policy include (TypeScript subject)'),
    ('crates/**/*.rs', 'lib/run_rust_full.py policy include (Rust subject)'),
]
OLD_READING_NOTE = (
    'the generation-18 predicate translated a pattern to a regex in which a terminal `**` became '
    '`(?:[^/]+/)*`, so `src/**` matched NEITHER `src` NOR `src/legacy.js`. That was the reading '
    'this origin reported as UNDECIDED (V16-S2). The published contract decides the other way, '
    'and the difference is measured below per pattern actually used.')


def old_reading(pattern, candidate):
    """The generation-18 implementation, kept verbatim so the delta is measured and not asserted."""
    import re as _re

    def seg_re(seg):
        out = ''
        for ch in seg:
            out += '[^/]*' if ch == '*' else ('[^/]' if ch == '?' else _re.escape(ch))
        return out
    parts = pattern.split('/')
    rx = []
    for i, seg in enumerate(parts):
        if seg == '**':
            rx.append('(?:[^/]+/)*')
        else:
            rx.append(seg_re(seg) + ('/' if i < len(parts) - 1 else ''))
    full = ('^' + ''.join(rx) + '$').replace('(?:[^/]+/)*/', '(?:[^/]+/)*')
    return bool(_re.match(full, candidate))


def main():
    rows, fails = [], []
    for pat, cand, want in REQUIRED:
        got = E.glob_match(pat, cand)
        ok = got == want
        rows.append({'family': 'required-example', 'pattern': pat, 'candidate': cand,
                     'expected': want, 'measured': got, 'result': 'PASS' if ok else 'FAIL'})
        if not ok:
            fails.append((pat, cand, want, got))
    for pat, cand, want, why in DERIVED:
        got = E.glob_match(pat, cand)
        ok = got == want
        rows.append({'family': 'derived-property', 'pattern': pat, 'candidate': cand,
                     'expected': want, 'measured': got, 'why': why,
                     'result': 'PASS' if ok else 'FAIL'})
        if not ok:
            fails.append((pat, cand, want, got))
    for inc, exc, cand, want, why in COMPOSITION:
        got = E.in_scope(inc, exc, cand)
        ok = got == want
        rows.append({'family': 'composition', 'include': inc, 'exclude': exc, 'candidate': cand,
                     'expected': want, 'measured': got, 'why': why,
                     'result': 'PASS' if ok else 'FAIL'})
        if not ok:
            fails.append((str((inc, exc)), cand, want, got))

    # measured delta on the patterns this origin actually uses
    delta = []
    probes = ['src', 'src/a.js', 'src/nested/a.js', 'src/a.ts', 'src/legacy.js', 'a.ts',
              'crates/app/src/main.rs', 'crates', 'README.md', 'package.json']
    for pat, site in USED_BY_THIS_ORIGIN:
        diffs = [c for c in probes if E.glob_match(pat, c) != old_reading(pat, c)]
        delta.append({'pattern': pat, 'site': site,
                      'candidatesProbed': probes,
                      'candidatesWhereTheTwoReadingsDISAGREE': diffs,
                      'selectionChangedForThisOrigin': bool(diffs),
                      'nowSelects': [c for c in probes if E.glob_match(pat, c)]})

    doc = {'standing': __doc__, 'requiredExampleCount': len(REQUIRED),
           'derivedPropertyCount': len(DERIVED), 'compositionCaseCount': len(COMPOSITION),
           'checks': rows, 'failures': fails,
           'oldReadingNote': OLD_READING_NOTE,
           'measuredDeltaOnPatternsThisOriginUses': delta,
           'v16S2Disposition': (
               'RESOLVED BY THIS KIT. foundation/glob-pattern-contract.v1.md is new in this '
               'input and states the terminal-`**` case directly ("This rule applies at the '
               'beginning, middle, and end, and may consume the final filename segment. It does '
               'not require a directory"), with `src/**` -> `src`, `src/legacy.js` and '
               '`src/nested/legacy.js` all true in its required table, and '
               'workflow-projection-contract section 14 repeats it ("terminal `src/**` includes '
               '`src/legacy.js`"). The ambiguity this origin reported is gone; no glob law was '
               'invented here and the predicate is reconstructed from the published law.'),
           'whatThisDoesNotClaim': (
               'no implementation outside this runtime is certified, and the contract itself '
               'states that scope selection is not evidence of exhaustive extraction or native '
               'coverage. This module also grants no repair authorization.')}
    with open(OUT + '/vectors/glob-law.json', 'w') as f:
        json.dump(doc, f, indent=1)
    print('required examples : %d' % len(REQUIRED))
    print('derived properties: %d' % len(DERIVED))
    print('composition cases : %d' % len(COMPOSITION))
    print('FAILURES          : %d' % len(fails))
    for f_ in fails:
        print('   FAIL pattern=%r candidate=%r expected=%s measured=%s' % f_)
    print()
    for d in delta:
        print('%-16s %-58s readingsDisagreeOn=%s'
              % (d['pattern'], d['site'][:58], d['candidatesWhereTheTwoReadingsDISAGREE']))
    assert not fails, fails


main()
