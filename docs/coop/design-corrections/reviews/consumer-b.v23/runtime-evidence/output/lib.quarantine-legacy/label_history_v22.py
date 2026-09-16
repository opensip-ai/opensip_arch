"""Generation-label provenance audit for generation 22, driven by the retained before-images.

Same evidence rule as the generation-19/20 audits this origin wrote (the earliest before-image that
contains the SAME sentence, labels masked, carries that sentence's true generation), now also able
to use lib.before-image.v20 -- plus two corrections to the instrument itself:

  V22-D1 (blind spot).  The generation-20 audit classified any line with two `consumer-b` labels
        within 40 characters as an ANCESTRY row and never drift-checked it. The V19-D2 helper
        sentence quotes a rebind as "`consumer-b.v18`+`/` -> `consumer-b.v19`+`/`", which is two
        labels in 40 characters, so when the generation-20 rebind's bare-label pass turned the
        second label into v20 the audit still said NO HISTORICAL LABEL DRIFT. A line is now an
        ancestry row only when it is a `'generation':` row, names three or more generations, or
        says `ancestry`; a two-label sentence is narrative and is drift-checked.
  SPLIT literals.  Labels written as 'consumer-b.' + 'vNN' are counted too (V20-D6 showed that
        current declarations hide in that form), and every helper-correction row whose id is
        `VNN-...` must carry generation vNN -- a direct provenance check that does not depend on
        before-image coverage.

Occurrence kinds:
  current-declaration   consumerId / inputKit / ROOT-RUNTIME-CONSUMER constant, or this origin's
                        own self-attribution. Must name the generation doing the work.
  ancestry-row          a row or list enumerating the ancestry; each entry names its own generation.
  historical-narrative  a statement about ONE earlier generation's defect or work. Its label is
                        evidence and must not move.

Nothing is rewritten here; this module measures and reports. Run with `--expect-current` after the
rebind to also require every current declaration to name generation 22.
"""
import json
import os
import re
import sys

OUT = '/tmp/opensip-design-corrections/consumer-b.v22/output'
LIB = OUT + '/lib'
THIS = 'v22'
BEFORE = ['lib.before-image.v14', 'lib.before-image.v15', 'lib.before-image.v16',
          'lib.before-image.v17', 'lib.before-image.v18', 'lib.before-image.v19',
          'lib.before-image.v20']
GEN = re.compile(r'consumer-b\.v(\d+)')
SPLIT = re.compile(r"""consumer-b\.?['"]\s*\+\s*['"]\.?v(\d+)""")
CURRENT_DECL = ('consumerId', 'inputKit', 'generationUnderReview', 'thisGeneration')
ROOT_ASSIGN = re.compile(r'^\s*(OUT|ROOT|RUNTIME|LIB|KIT|SUB|SUBJ|BEFORE|CONSUMER|V\d+|DEST|'
                         r'TARGET)\s*=')
ANCESTRY_ROW = re.compile(r"^\s*\{?'generation':\s*'consumer-b")
ROW_ID = re.compile(r"'id':\s*'V(\d+)-[A-Z]")
SELF_ATTRIBUTION = ('authored by', 'Independently authored', 'Independently derived',
                    'reconstruction core', 'schema-admission layer for',
                    'requirement-status maintenance for', 'names consumer-b',
                    'design review -- consumer-b')
# a continuation line of a split-literal generation LIST: only list items, nothing else
LIST_ONLY = re.compile(r"""^\s*\[?\s*(?:['"](?:/tmp/opensip-design-corrections/)?consumer-b\.?['"]"""
                       r"""\s*\+\s*['"]\.?v\d+['"]\s*(?:\+\s*['"][^'"]*['"])?\s*,?\s*)+\]?\)?,?\s*$""")
# the tools of THIS generation quote other generations on purpose (their own docstrings explain
# the defects they detect); they are not report content
SELF_EXCLUDED = ('label_history_v22.py', 'rebind_v22.py', 'census_v22.py', 'verify_kit_v22.py')


def norm(line):
    return SPLIT.sub("consumer-b.'+'vNN", GEN.sub('consumer-b.vNN', line)).strip()


def labels_of(line):
    return ['v' + m.group(1) for m in GEN.finditer(line)] + \
        ['v' + m.group(1) for m in SPLIT.finditer(line)]


# A current declaration is a KEY (`'consumerId': ...`), not the word in prose: the first
# post-rebind run classified three historical helper sentences that merely mention "consumerId"
# (V16-D row, V20-D6 originalFailure / correction) as current declarations and asked for them to
# name generation 22 -- which would have been exactly the V18-D6 rewrite this audit exists to stop.
CURRENT_DECL_KEY = re.compile(r"""['"](?:%s)['"]\s*:""" % '|'.join(CURRENT_DECL))


def classify(line):
    labs = labels_of(line)
    if (CURRENT_DECL_KEY.search(line) or ROOT_ASSIGN.match(line)
            or any(k in line for k in SELF_ATTRIBUTION)):
        return 'current-declaration'
    if (ANCESTRY_ROW.match(line) or len(labs) >= 3 or 'ncestry' in line
            or LIST_ONLY.match(line)):
        return 'ancestry-row'
    return 'historical-narrative'


def main():
    expect_current = '--expect-current' in sys.argv
    # Keyed by (file, masked sentence) -> per before-image the SORTED MULTISET of label tuples of
    # every line with that masked text. The first draft kept one label list per key, so two
    # distinct lines whose masked text is identical (a sibling-path list) were compared with each
    # other and reported as drift; comparing the multiset removes that false positive without
    # hiding a real change of any one occurrence.
    hist = {}
    for d in BEFORE:
        gen_of_dir = d.split('.')[-1]
        root = os.path.join(OUT, d)
        if not os.path.isdir(root):
            continue
        for n in sorted(os.listdir(root)):
            if not n.endswith('.py'):
                continue
            per_key = {}
            for line in open(os.path.join(root, n), encoding='utf-8'):
                if 'consumer-b' not in line:
                    continue
                labs = labels_of(line)
                if not labs:
                    continue
                per_key.setdefault(norm(line), []).append(tuple(labs))
            for key, multiset in per_key.items():
                hist.setdefault((n, key), []).append(
                    {'beforeImage': gen_of_dir, 'labels': sorted(multiset)})
    current_multisets = {}
    for n in sorted(os.listdir(LIB)):
        if not n.endswith('.py') or n in SELF_EXCLUDED:
            continue
        for line in open(os.path.join(LIB, n), encoding='utf-8'):
            labs = labels_of(line)
            if labs:
                current_multisets.setdefault((n, norm(line)), []).append(tuple(labs))

    rows, row_id_mismatch = [], []
    for n in sorted(os.listdir(LIB)):
        if not n.endswith('.py') or n in SELF_EXCLUDED:
            continue
        for i, line in enumerate(open(os.path.join(LIB, n), encoding='utf-8'), 1):
            m_id = ROW_ID.search(line)
            if m_id:
                labs = labels_of(line)
                if labs and labs[0] != 'v' + m_id.group(1):
                    row_id_mismatch.append({'file': 'output/lib/' + n, 'line': i,
                                            'rowGeneration': 'v' + m_id.group(1),
                                            'label': labs[0], 'text': line.strip()[:170]})
            labs = labels_of(line)
            if not labs:
                continue
            # a path occurrence is the rebind's business, not report content
            if all(line[m.end():m.end() + 1] == '/' for m in GEN.finditer(line)) \
                    and not SPLIT.search(line):
                continue
            kind = classify(line)
            prior = hist.get((n, norm(line)), [])
            earliest = prior[0] if prior else None
            now_multiset = sorted(current_multisets.get((n, norm(line)), []))
            rows.append({
                'file': 'output/lib/' + n, 'line': i, 'currentLabels': labs, 'kind': kind,
                'earliestBeforeImage': earliest['beforeImage'] if earliest else None,
                'earliestLabels': ([list(t) for t in earliest['labels']]
                                   if earliest else None),
                'labelDriftedSinceEarliestBeforeImage': bool(
                    earliest and [list(t) for t in earliest['labels']]
                    != [list(t) for t in now_multiset]),
                'text': line.strip()[:170]})
    drift = [r for r in rows if r['labelDriftedSinceEarliestBeforeImage']
             and r['kind'] == 'historical-narrative']
    decls = [r for r in rows if r['kind'] == 'current-declaration']
    stale_decls = [r for r in decls if any(lab != THIS for lab in r['currentLabels'])]
    unknown = [r for r in rows if r['kind'] == 'historical-narrative'
               and r['earliestLabels'] is None]
    failed = bool(drift or row_id_mismatch or (expect_current and stale_decls))
    doc = {'standing': __doc__, 'rows': rows,
           'historicalNarrativesWhoseLabelDrifted': drift,
           'helperRowsWhoseGenerationDisagreesWithTheirId': row_id_mismatch,
           'currentDeclarations': decls,
           'currentDeclarationsNotNamingThisGeneration': stale_decls,
           'expectCurrentDeclarationsToNameThisGeneration': expect_current,
           'historicalNarrativesWithNoBeforeImageEvidence': unknown,
           'method': ('the earliest before-image containing the SAME sentence (with the label '
                      'masked) carries that sentence\'s true generation; a later copy that '
                      'disagrees was rewritten by a mechanical rebind. Helper rows are also '
                      'checked directly against their own id.'),
           'verdict': ('LABEL DRIFT PRESENT -- historical narratives must be restored'
                       if (drift or row_id_mismatch) else
                       ('CURRENT DECLARATIONS NOT YET REBOUND' if expect_current and stale_decls
                        else 'NO HISTORICAL LABEL DRIFT'))}
    with open(OUT + '/notes/v22-label-history.json', 'w') as f:
        json.dump(doc, f, indent=1)
    print('non-path generation labels in active code:', len(rows))
    print('  current declarations                          :', len(decls),
          '(not naming %s: %d)' % (THIS, len(stale_decls)))
    if expect_current:
        for r in stale_decls[:20]:
            print('     %-26s:%-5d %s %s' % (r['file'].split('/')[-1], r['line'],
                                             r['currentLabels'], r['text'][:60]))
    print('  historical narratives with DRIFTED labels     :', len(drift))
    for r in drift:
        print('     %-26s:%-5d now=%s true=%s (%s) %s'
              % (r['file'].split('/')[-1], r['line'], r['currentLabels'],
                 r['earliestLabels'], r['earliestBeforeImage'], r['text'][:50]))
    print('  helper rows whose generation disagrees with id:', len(row_id_mismatch))
    for r in row_id_mismatch:
        print('     %-26s:%-5d id=%s label=%s' % (r['file'].split('/')[-1], r['line'],
                                                  r['rowGeneration'], r['label']))
    print('  historical narratives with no before-image evidence:', len(unknown))
    print('verdict:', doc['verdict'])
    raise SystemExit(1 if failed else 0)


main()
