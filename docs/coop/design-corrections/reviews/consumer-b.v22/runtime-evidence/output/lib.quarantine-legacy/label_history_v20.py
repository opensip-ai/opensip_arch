"""Generation-label provenance audit for generation 20, driven by the retained before-images.

Same evidence-based method this origin wrote at generation 19 (the earliest before-image that
contains the SAME sentence carries that sentence's true generation label), now also able to use
lib.before-image.v19. Three kinds of occurrence are separated, because only the third can drift:

  current-declaration   a consumerId / inputKit / ROOT-RUNTIME constant, or this origin's own
                        self-attribution in a docstring or an exported synthetic-observation
                        standing. These must name the generation doing the work.
  ancestry-row          a row or list enumerating the ancestry; each entry names its own
                        generation and the list GAINS the current one.
  historical-narrative  a statement about ONE earlier generation's defect or work. Its label is
                        evidence and must not move.

Nothing is rewritten here; this module measures and reports.
"""
import json
import os
import re

OUT = '/tmp/opensip-design-corrections/consumer-b.v20/output'
LIB = OUT + '/lib'
BEFORE = ['lib.before-image.v14', 'lib.before-image.v15', 'lib.before-image.v16',
          'lib.before-image.v17', 'lib.before-image.v18', 'lib.before-image.v19']
GEN = re.compile(r'consumer-b\.v(\d+)')
CURRENT_DECL = ('consumerId', 'inputKit', 'generationUnderReview', 'thisGeneration')
ROOT_ASSIGN = re.compile(r'^\s*(OUT|ROOT|RUNTIME|LIB|KIT|SUB|BEFORE|CONSUMER|V\d+|DEST|TARGET)'
                         r'\s*=')
ANCESTRY_LINE = re.compile(r'consumer-b[^\n]{0,40}consumer-b')
ANCESTRY_ROW = re.compile(r"^\s*\{?'generation':\s*'consumer-b")
SELF_ATTRIBUTION = ('authored by', 'Independently authored', 'Independently derived',
                    'reconstruction core', 'schema-admission layer for',
                    'requirement-status maintenance for', 'names consumer-b')


def norm(line):
    return GEN.sub('consumer-b.vNN', line).strip()


def main():
    hist = {}
    for d in BEFORE:
        gen_of_dir = d.split('.')[-1]
        root = os.path.join(OUT, d)
        if not os.path.isdir(root):
            continue
        for n in sorted(os.listdir(root)):
            if not n.endswith('.py'):
                continue
            for line in open(os.path.join(root, n), encoding='utf-8'):
                if 'consumer-b.v' not in line:
                    continue
                labels = {'v' + m.group(1) for m in GEN.finditer(line)}
                hist.setdefault((n, norm(line)), []).append(
                    {'beforeImage': gen_of_dir, 'labels': sorted(labels)})

    rows = []
    for n in sorted(os.listdir(LIB)):
        if not n.endswith('.py'):
            continue
        for i, line in enumerate(open(os.path.join(LIB, n), encoding='utf-8'), 1):
            for m in GEN.finditer(line):
                label = 'v' + m.group(1)
                if line[m.end():m.end() + 1] == '/':
                    continue                     # a path: the rebind's business
                if (any(k in line for k in CURRENT_DECL) or ROOT_ASSIGN.match(line)
                        or any(k in line for k in SELF_ATTRIBUTION)):
                    kind = 'current-declaration'
                elif ANCESTRY_LINE.search(line) or ANCESTRY_ROW.match(line):
                    kind = 'ancestry-row'
                else:
                    kind = 'historical-narrative'
                prior = hist.get((n, norm(line)), [])
                earliest = prior[0] if prior else None
                rows.append({
                    'file': 'output/lib/' + n, 'line': i, 'currentLabel': label, 'kind': kind,
                    'earliestBeforeImage': earliest['beforeImage'] if earliest else None,
                    'earliestLabels': earliest['labels'] if earliest else None,
                    'labelDriftedWithTheRebind': bool(
                        earliest and earliest['labels'] != [label]),
                    'text': line.strip()[:170]})
    drift = [r for r in rows if r['labelDriftedWithTheRebind']
             and r['kind'] == 'historical-narrative']
    decls = [r for r in rows if r['kind'] == 'current-declaration']
    unknown = [r for r in rows if r['kind'] == 'historical-narrative'
               and r['earliestLabels'] is None]
    doc = {'standing': __doc__, 'rows': rows,
           'historicalNarrativesWhoseLabelDrifted': drift,
           'currentDeclarations': decls,
           'historicalNarrativesWithNoBeforeImageEvidence': unknown,
           'method': ('the earliest before-image containing the SAME sentence (with the label '
                      'masked) carries that sentence\'s true generation; a later copy that '
                      'disagrees was rewritten by a mechanical rebind'),
           'verdict': ('LABEL DRIFT PRESENT -- historical narratives must be restored'
                       if drift else 'NO HISTORICAL LABEL DRIFT')}
    with open(OUT + '/notes/v20-label-history.json', 'w') as f:
        json.dump(doc, f, indent=1)
    print('non-path generation labels in active code:', len(rows))
    print('  current declarations (must name this generation):', len(decls))
    print('  historical narratives with DRIFTED labels       :', len(drift))
    for r in drift:
        print('     %-26s:%-5d now=%-4s true=%-12s %s'
              % (r['file'].split('/')[-1], r['line'], r['currentLabel'],
                 ','.join(r['earliestLabels']), r['text'][:58]))
    print('  historical narratives with no before-image evidence:', len(unknown))
    for r in unknown[:12]:
        print('     %-26s:%-5d %-4s %s'
              % (r['file'].split('/')[-1], r['line'], r['currentLabel'], r['text'][:66]))
    print('verdict:', doc['verdict'])


main()
