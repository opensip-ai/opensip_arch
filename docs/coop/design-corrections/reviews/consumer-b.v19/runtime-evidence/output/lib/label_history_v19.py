"""Generation-label provenance audit, driven by the retained before-images.

V18-D6 found that a mechanical path rebind had rewritten generation-labelled CONTENT in the
helper-correction record. This audit asks the same question of every active module, and answers it
with EVIDENCE rather than with a guess: output/lib.before-image.v14 / .v15 / .v16 / .v17 are
byte copies of this origin's own earlier library, so the EARLIEST before-image that contains the
same sentence carries that sentence's TRUE generation label.

For every `consumer-b.vNN` label in active code that is not used as a filesystem path, this module
records:

  kind = current-declaration   the record field that names the generation DOING the work
                               (consumerId / inputKit / receipt headers). These must become the
                               current generation.
  kind = historical-narrative  a helper-correction id, an ancestry row or a narrative sentence
                               about an earlier generation. These must keep their TRUE label, and
                               the earliest before-image occurrence is the evidence for it.

Nothing is rewritten here; this module only measures and reports.
"""
import json
import os
import re

OUT = '/tmp/opensip-design-corrections/consumer-b.v19/output'
LIB = OUT + '/lib'
BEFORE = ['lib.before-image.v14', 'lib.before-image.v15', 'lib.before-image.v16',
          'lib.before-image.v17']
GEN = re.compile(r'consumer-b\.v(\d+)')
CURRENT_DECL = ('consumerId', 'inputKit', 'generationUnderReview', 'thisGeneration')
# A line that ASSIGNS this runtime's own root or consumer constant, or that enumerates the whole
# ancestry, is a CURRENT DECLARATION or an ancestry list -- not a historical narrative about one
# earlier generation. Only the latter can "drift": its label names a specific past generation.
ROOT_ASSIGN = re.compile(r'^\s*(OUT|ROOT|RUNTIME|LIB|KIT|SUB|BEFORE|CONSUMER|V\d+|DEST|TARGET)'
                         r'\s*=')
ANCESTRY_LINE = re.compile(r'consumer-b[^\n]{0,40}consumer-b')
ANCESTRY_ROW = re.compile(r"^\s*\{?'generation':\s*'consumer-b")
# SELF-ATTRIBUTION of the generation doing the work: a module's own docstring, or the standing
# sentence of a synthetic observation this generation re-mints. These are true of the CURRENT copy
# and are re-stated every generation, so they are current declarations, not claims about an
# earlier generation's work.
SELF_ATTRIBUTION = ('authored by', 'Independently authored', 'Independently derived',
                    'reconstruction core', 'schema-admission layer for',
                    'requirement-status maintenance for', 'names consumer-b')


def norm(line):
    return GEN.sub('consumer-b.vNN', line).strip()


def main():
    # index every before-image line, normalised, to the generations it appeared with
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
                tail = line[m.end():m.end() + 1]
                if tail == '/':
                    continue            # a path, handled by the rebind itself
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
    with open(OUT + '/notes/v19-label-history.json', 'w') as f:
        json.dump(doc, f, indent=1)
    print('non-path generation labels in active code:', len(rows))
    print('  current declarations (must become this generation):', len(decls))
    print('  historical narratives with DRIFTED labels        :', len(drift))
    for r in drift:
        print('     %-26s:%-5d now=%-4s true=%-12s %s'
              % (r['file'].split('/')[-1], r['line'], r['currentLabel'],
                 ','.join(r['earliestLabels']), r['text'][:62]))
    print('  historical narratives with no before-image evidence:', len(unknown))
    for r in unknown[:20]:
        print('     %-26s:%-5d %-4s %s'
              % (r['file'].split('/')[-1], r['line'], r['currentLabel'], r['text'][:70]))
    print('verdict:', doc['verdict'])


main()
