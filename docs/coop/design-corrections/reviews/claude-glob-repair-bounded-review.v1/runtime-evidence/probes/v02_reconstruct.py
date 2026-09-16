"""V02 — the decisive independent check for task 1.

The stated goal is a published law "reconstructable without source code, preserving existing
behavior". So I implement the predicate FROM THE CONTRACT PROSE ONLY and differential-test it against
the unchanged reference workflows_model.v1.glob_match over a large generated space plus every
required example and every named edge case.

My reconstruction below is written from these prose clauses only:
  - split both at every literal '/', preserving empty segments; anchored; case sensitive
  - an ordinary segment matches exactly one candidate segment, in full
  - '*' = zero or more Unicode scalar values within the segment; '?' = exactly one scalar;
    neither consumes '/'; every other character matches itself; braces/brackets literal;
    no escape syntax; consecutive stars have the same power as one star
  - a segment exactly '**' matches zero or more WHOLE candidate segments, at start/middle/end,
    may consume the final filename, does not require a directory
  - 'a**b' is ordinary and cannot consume a separator
  - the (i,j) recurrence in the contract's "Equivalently" paragraph
"""
import importlib.util, itertools, json, os, sys

SNAP = '/tmp/opensip-design-corrections/candidate-subject.v31'
OUT = '/tmp/opensip-design-corrections/claude-glob-repair-bounded-review.v1/receipts'
os.makedirs(OUT, exist_ok=True)

spec = importlib.util.spec_from_file_location(
    'wfm31', os.path.join(SNAP, 'docs/coop/design-corrections/workflows/workflows_model.v1.py'))
WFM = importlib.util.module_from_spec(spec)
sys.modules['wfm31'] = WFM
spec.loader.exec_module(WFM)
REF = WFM.glob_match


# ---------------- my reconstruction, from the prose ----------------
def seg_match_prose(p, s):
    """Ordinary segment: '*' = zero or more scalars, '?' = exactly one scalar, others literal.
    Written as a straightforward scalar-indexed recurrence, not copied from any implementation."""
    from functools import lru_cache
    P, S = list(p), list(s)          # list() iterates Unicode scalar values

    @lru_cache(maxsize=None)
    def m(i, j):
        if i == len(P):
            return j == len(S)
        c = P[i]
        if c == '*':
            # zero or more scalars in this segment
            return any(m(i + 1, k) for k in range(j, len(S) + 1))
        if j == len(S):
            return False
        if c == '?':
            return m(i + 1, j + 1)
        return c == S[j] and m(i + 1, j + 1)
    return m(0, 0)


def glob_match_prose(pattern, candidate):
    P = pattern.split('/')           # preserves empty segments
    S = candidate.split('/')

    from functools import lru_cache

    @lru_cache(maxsize=None)
    def rec(i, j):
        if i == len(P):
            return j == len(S)
        if P[i] == '**':
            return any(rec(i + 1, k) for k in range(j, len(S) + 1))
        return j < len(S) and seg_match_prose(P[i], S[j]) and rec(i + 1, j + 1)
    return rec(0, 0)


R = {'standing': 'reconstruction written from contract prose; reference taken from frozen31'}

# ---------------- the 20 required examples ----------------
REQUIRED = [
    ('**/*.ts', 'a.ts', True), ('**/*.ts', 'src/nested/a.ts', True),
    ('*.ts', 'src/a.ts', False),
    ('src/**', 'src', True), ('src/**', 'src/legacy.js', True),
    ('src/**', 'src/nested/legacy.js', True),
    ('src/**/*', 'src', False), ('src/**/*', 'src/legacy.js', True),
    ('a/**/b', 'a/b', True), ('a/**/b', 'a/x/y/b', True),
    ('a/*/b', 'a/b', False),
    ('a**b', 'a/x/b', False), ('a**b', 'axxb', True),
    ('*', '.hidden', True),
    ('a.ts', 'A.ts', False), ('a.ts', 'a.ts.extra', False),
    ('?.ts', 'é.ts', True),              # single scalar e-acute
    ('?.ts', 'é.ts', False),            # e + combining acute
    ('[ab].ts', 'a.ts', False), ('[ab].ts', '[ab].ts', True),
    ('{a,b}.ts', 'a.ts', False), ('{a,b}.ts', '{a,b}.ts', True),
]
rows = []
for pat, cand, want in REQUIRED:
    got_ref = REF(pat, cand)
    got_pro = glob_match_prose(pat, cand)
    rows.append({'pattern': pat, 'candidate': cand, 'documented': want,
                 'reference': got_ref, 'myReconstruction': got_pro,
                 'referenceAgreesWithDoc': got_ref == want,
                 'reconstructionAgreesWithDoc': got_pro == want})
R['requiredExamples'] = rows
bad_ref = [r for r in rows if not r['referenceAgreesWithDoc']]
bad_pro = [r for r in rows if not r['reconstructionAgreesWithDoc']]
print('required examples: %d | reference disagreements: %d | reconstruction disagreements: %d'
      % (len(rows), len(bad_ref), len(bad_pro)))
for r in bad_ref:
    print('   REF DISAGREES %-12r %-24r documented=%s reference=%s'
          % (r['pattern'], r['candidate'], r['documented'], r['reference']))
for r in bad_pro:
    print('   RECON DISAGREES %-12r %-24r documented=%s mine=%s'
          % (r['pattern'], r['candidate'], r['documented'], r['myReconstruction']))
R['allRequiredExamplesHoldInReference'] = not bad_ref
R['allRequiredExamplesHoldInMyReconstruction'] = not bad_pro

# ---------------- exhaustive differential test ----------------
PAT_TOKENS = ['a', 'b', '*', '?', '**', 'a*', '*a', 'a?', '?a', '**a', 'a**', 'a**b', '', '***',
              '*?', '?*', '[ab]', '{a,b}', 'a*b']
CAND_TOKENS = ['a', 'b', 'ab', '', 'axb', '.hidden', '[ab]', '{a,b}', 'A']
mismatches = []
tested = 0
for np_ in (1, 2, 3):
    for nc in (1, 2, 3):
        for pt in itertools.product(PAT_TOKENS, repeat=np_):
            pat = '/'.join(pt)
            if not pat:
                continue
            for ct in itertools.product(CAND_TOKENS, repeat=nc):
                cand = '/'.join(ct)
                tested += 1
                a, b = REF(pat, cand), glob_match_prose(pat, cand)
                if a != b:
                    mismatches.append({'pattern': pat, 'candidate': cand,
                                       'reference': a, 'myReconstruction': b})
R['differentialCasesTested'] = tested
R['differentialMismatches'] = mismatches[:40]
R['differentialMismatchCount'] = len(mismatches)
print('\ndifferential test: %d (pattern, candidate) pairs | mismatches: %d'
      % (tested, len(mismatches)))
for m in mismatches[:15]:
    print('   %-22r %-18r reference=%-5s mine=%s'
          % (m['pattern'], m['candidate'], m['reference'], m['myReconstruction']))

# ---------------- named edge cases from the prose ----------------
EDGE = [
    ('leading ** with terminal filename', '**', 'a.ts', True),
    ('** alone matches empty path', '**', '', True),
    ('** alone matches nested', '**', 'a/b/c', True),
    ('** consumes zero segments (middle)', 'a/**/b', 'a/b', True),
    ('** consumes zero segments (leading)', '**/a', 'a', True),
    ('** consumes zero segments (trailing)', 'a/**', 'a', True),
    ('trailing slash is an empty final segment', 'src/', 'src', False),
    ('trailing slash matches empty final segment', 'src/', 'src/', True),
    ('empty middle segment preserved', 'a//b', 'a//b', True),
    ('empty middle segment not elided', 'a//b', 'a/b', False),
    ('* does not cross separator', '*', 'a/b', False),
    ('? does not cross separator', '?', '/', False),
    ('consecutive stars == one star', '**a', 'xxa', True),
    ('*** is ordinary', '***', 'abc', True),
    ('*** cannot cross separator', '***', 'a/b', False),
    ('dot segments not resolved', 'a/./b', 'a/./b', True),
    ('dot segments not resolved to a/b', 'a/./b', 'a/b', False),
    ('parent segments not resolved', 'a/../b', 'a/../b', True),
    ('case sensitivity', 'A', 'a', False),
    ('anchored, no implicit prefix', 'a', 'ab', False),
    ('anchored, no implicit suffix', 'b', 'ab', False),
    ('empty candidate vs * ', '*', '', True),
    ('empty candidate vs ?', '?', '', False),
    ('literal bracket class inert', '[a-z]', 'q', False),
    ('literal bracket matches itself', '[a-z]', '[a-z]', True),
    ('brace inert', '{a}', 'a', False),
    ('astral scalar with ?', '?', '\U0001F600', True),
    ('astral scalar counted once', '??', '\U0001F600', False),
]
erows = []
for name, pat, cand, want in EDGE:
    a, b = REF(pat, cand), glob_match_prose(pat, cand)
    erows.append({'case': name, 'pattern': pat, 'candidate': cand, 'expectedFromProse': want,
                  'reference': a, 'myReconstruction': b,
                  'referenceMatchesProse': a == want, 'agree': a == b})
R['edgeCases'] = erows
print('\n--- named edge cases ---')
for r in erows:
    flag = '' if r['referenceMatchesProse'] else '   <-- REFERENCE DIVERGES FROM PROSE'
    print('%-42s %-10r %-12r prose=%-5s ref=%-5s mine=%-5s%s'
          % (r['case'][:42], r['pattern'], r['candidate'], r['expectedFromProse'],
             r['reference'], r['myReconstruction'], flag))
R['edgeDivergences'] = [r for r in erows if not r['referenceMatchesProse']]
R['edgeDisagreements'] = [r for r in erows if not r['agree']]
print('\nreference/prose divergences : %d' % len(R['edgeDivergences']))
print('reference/mine disagreements: %d' % len(R['edgeDisagreements']))

R['CONCLUSION'] = {
    'lawIsReconstructableFromProseAlone': (not mismatches and not bad_pro),
    'referenceMatchesEveryDocumentedExample': not bad_ref,
    'referenceMatchesEveryProseEdgeCase': not R['edgeDivergences']}
print('\nCONCLUSION:', json.dumps(R['CONCLUSION']))
json.dump(R, open(os.path.join(OUT, 'v02-reconstruct.json'), 'w'), indent=1, default=str)
print('wrote v02-reconstruct.json')
