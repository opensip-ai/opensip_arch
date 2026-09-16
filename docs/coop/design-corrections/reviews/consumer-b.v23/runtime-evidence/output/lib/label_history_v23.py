"""Generation-label provenance audit for generation 23, driven by the retained before-images.

The generation-22 audit's evidence rule, unchanged (the earliest before-image that contains the SAME
sentence, labels masked, carries that sentence's true generation), now also able to use
lib.before-image.v22. Its V22-D1 corrections are kept: a two-label sentence is narrative and is
drift-checked, split literals are counted, current declarations are KEYS, and every helper row
whose id is `VNN-...` must carry generation vNN.

Occurrence kinds:
  current-declaration   consumerId / inputKit / ROOT-RUNTIME-CONSUMER constant, or this origin's
                        own self-attribution. Must name the generation doing the work (23).
  ancestry-row          a row or list enumerating the ancestry; each entry names its own generation.
  historical-narrative  a statement about ONE earlier generation's defect or work. Its label is
                        evidence and must not move.

Nothing is rewritten here. Run with `--expect-current` after the rebind to also require every
current declaration to name generation 23.
"""
import json
import os
import re
import sys

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'
LIB = OUT + '/lib'
THIS = 'v23'
BEFORE = ['lib.before-image.v14', 'lib.before-image.v15', 'lib.before-image.v16',
          'lib.before-image.v17', 'lib.before-image.v18', 'lib.before-image.v19',
          'lib.before-image.v20', 'lib.before-image.v22']
GEN = re.compile(r'consumer-b\.v(\d+)')
SPLIT = re.compile(r"""consumer-b\.?['"]\s*\+\s*['"]\.?v(\d+)""")
CURRENT_DECL = ('consumerId', 'inputKit', 'generationUnderReview', 'thisGeneration')
ROOT_ASSIGN = re.compile(r'^\s*(OUT|ROOT|RUNTIME|LIB|KIT|SUB|SUBJ|BEFORE|CONSUMER|V\d+|DEST|'
                         r'TARGET)\s*=')
ANCESTRY_ROW = re.compile(r"^\s*\{?'generation':\s*'consumer-b")
ROW_ID = re.compile(r"'id':\s*'V(\d+)-[A-Z]")
# 'CURRENT_ORIGIN': the first post-rebind run classified the audit check
# `c['generation'] == 'consumer-b.v23', 'CUSTODY_NAMES_THE_CURRENT_ORIGIN'` as a historical
# narrative (it carries no key and no self-attribution phrase) and reported the rebind's correct
# update of it as drift. A check that names THE CURRENT ORIGIN is a current declaration.
SELF_ATTRIBUTION = ('authored by', 'Independently authored', 'Independently derived',
                    'reconstruction core', 'schema-admission layer for',
                    'requirement-status maintenance for', 'names consumer-b',
                    'design review -- consumer-b', 'CURRENT_ORIGIN')
LIST_ONLY = re.compile(r"""^\s*\[?\s*(?:['"](?:/tmp/opensip-design-corrections/)?consumer-b\.?['"]"""
                       r"""\s*\+\s*['"]\.?v\d+['"]\s*(?:\+\s*['"][^'"]*['"])?\s*,?\s*)+\]?\)?,?\s*$""")
# the generation-23 tools quote other generations on purpose; they are not report content
SELF_EXCLUDED = ('label_history_v23.py', 'rebind_v23.py', 'census_v23.py', 'verify_kit_v23.py',
                 'preserve_predecessors_v23.py', 'history_standing_v23.py')
CURRENT_DECL_KEY = re.compile(r"""['"](?:%s)['"]\s*:""" % '|'.join(CURRENT_DECL))


def norm(line):
    return SPLIT.sub("consumer-b.'+'vNN", GEN.sub('consumer-b.vNN', line)).strip()


def labels_of(line):
    return ['v' + m.group(1) for m in GEN.finditer(line)] + \
        ['v' + m.group(1) for m in SPLIT.finditer(line)]


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
    with open(OUT + '/notes/v23-label-history.json', 'w') as f:
        json.dump(doc, f, indent=1)
    print('non-path generation labels in active code:', len(rows))
    print('  current declarations                          :', len(decls),
          '(not naming %s: %d)' % (THIS, len(stale_decls)))
    for r in stale_decls[:40]:
        print('     %-26s:%-5d %s %s' % (r['file'].split('/')[-1], r['line'],
                                         r['currentLabels'], r['text'][:70]))
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
