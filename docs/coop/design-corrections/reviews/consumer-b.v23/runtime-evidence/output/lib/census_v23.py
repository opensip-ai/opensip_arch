"""LITERAL PATH CENSUS for generation 23 -- run BEFORE any copied code is executed.

Written fresh for this generation (the copied library is generation 22's; generation 21 was prepared
and never ran, so no generation-21 tree exists). Same method as the generation-22 census this origin
authored, with 23 as the expected generation:

  * pure read of this runtime's own files; no filesystem access outside it. A referenced root is
    judged by STRING comparison, never by stat'ing a sibling generation.
  * a line is a WRITE candidate when it carries a write-producing construct on a line that also
    carries a path literal, or when it ASSIGNS a constant other lines use as an output root.
  * four groups, and only `active` may be executed:
      active                 this generation's import path (output/lib)
      archived-before-image  output/lib.before-image.* -- historical byte copies, never executed
      quarantined-legacy     output/lib.quarantine-legacy -- tools pinned to an earlier generation
      report-content         an OCCURRENCE class: a historical generation label inside report or
                             correction CONTENT (V18-D6, V19-D1, V22-D1 were caused by rewriting
                             these), counted and NOT rebound.

Split literals ('consumer-b.' + 'v22') are counted as ROOT assignments too (V20-D6). The copied
generation-22 rebind / census / custody tools are NOT executed: each hardcodes generation 22 as its
own runtime, so running one would write into, or judge, the wrong generation.
"""
import json
import os
import re

RUNTIME = '/tmp/opensip-design-corrections/consumer-b.v23'
OUT = RUNTIME + '/output'
THIS_GEN = 'v23'

GEN = re.compile(r'consumer-b\.v(\d+)')
SPLIT_GEN = re.compile(r"""consumer-b\.?['"]\s*\+\s*['"]\.?v(\d+)""")
WRITE_HINTS = (
    "open(", "json.dump", ".write(", "os.makedirs", "shutil.copytree", "shutil.copy",
    "shutil.move", "shutil.rmtree", "os.remove", "os.unlink", "os.rename", "os.rmdir",
    ".export(", "writelines",
)
ROOT_ASSIGN = re.compile(r'^\s*(OUT|ROOT|BEFORE|LIB|DEST|TARGET|SUB|SUBJ|KIT|RUNTIME|V\d+|BASE|'
                         r'REC)\s*=')
CONTENT_MARKERS = ('generation', 'consumerId', 'ancestry', 'ANCESTRY', 'HELPER CORRECTION',
                   'CORRECTED (', 'V17-D', 'V18-D', 'V19-D', 'V20-D', 'V22-D', 'V16-D', 'V15-D',
                   'previous-review', 'wasReportedAs', 'originalFailure',
                   'declaredInputIdenticalTo', 'historical', 'prior generation',
                   'sameDefectClassAs', 'sameOriginAncestry')


def group_of(rel):
    s = '/' + rel
    if '/lib.before-image.' in s:
        return 'archived-before-image'
    if '/lib.quarantine-legacy/' in s:
        return 'quarantined-legacy'
    return 'active'


def is_path_occurrence(line, m):
    tail = line[m.end():m.end() + 2]
    return tail.startswith('/') or tail.startswith("'/") or tail.startswith('"/')


def main():
    files = []
    for d, _dirs, names in os.walk(OUT):
        for n in sorted(names):
            if n.endswith(('.py', '.sh', '.bash')):
                files.append(os.path.join(d, n))
    files.sort()
    rows, writes, by_gen, split_roots, split_all = [], [], {}, [], []
    for p in files:
        rel = os.path.relpath(p, RUNTIME)
        try:
            text = open(p, encoding='utf-8').read()
        except Exception as e:
            rows.append({'file': rel, 'error': str(e)})
            continue
        for i, line in enumerate(text.splitlines(), 1):
            for m in GEN.finditer(line):
                gen = 'v' + m.group(1)
                hints = [h for h in WRITE_HINTS if h in line]
                is_assign = bool(ROOT_ASSIGN.match(line))
                path_use = is_path_occurrence(line, m)
                row = {'file': rel, 'group': group_of(rel), 'line': i, 'generation': gen,
                       'usedAsPath': path_use,
                       'reportContentLabel': (not path_use)
                       and any(k in line for k in CONTENT_MARKERS),
                       'isRootAssignment': is_assign,
                       'writeConstructsOnThisLine': hints,
                       'text': line.strip()[:170]}
                rows.append(row)
                by_gen.setdefault(gen, set()).add(rel)
                if (hints or is_assign) and path_use:
                    writes.append(row)
            for m in SPLIT_GEN.finditer(line):
                if group_of(rel) == 'active':
                    rec = {'file': rel, 'line': i, 'generation': 'v' + m.group(1),
                           'isRootAssignment': bool(ROOT_ASSIGN.match(line)),
                           'text': line.strip()[:170]}
                    split_all.append(rec)
                    if rec['isRootAssignment']:
                        split_roots.append(rec)
    foreign_writes = [r for r in writes
                      if r['generation'] != THIS_GEN and r['group'] == 'active']
    foreign_paths = [r for r in rows
                     if r['generation'] != THIS_GEN and r['group'] == 'active'
                     and r['usedAsPath']]
    foreign_split_roots = [r for r in split_roots if r['generation'] != THIS_GEN]
    content_labels = [r for r in rows
                      if r['group'] == 'active' and r['reportContentLabel']]
    joined_non_path_active = [r for r in rows if r['group'] == 'active' and not r['usedAsPath']]
    archived = [r for r in rows if r['group'] == 'archived-before-image']
    quarantined = [r for r in rows if r['group'] == 'quarantined-legacy']
    doc = {
        'standing': __doc__,
        'runtime': RUNTIME, 'thisGeneration': THIS_GEN,
        'filesScanned': len(files),
        'occurrencesTotal': len(rows),
        'occurrencesByGeneration': {g: sorted(v) for g, v in sorted(by_gen.items())},
        'activeFiles': sorted({r['file'] for r in rows if r['group'] == 'active'}),
        'archivedBeforeImageOccurrences': len(archived),
        'quarantinedLegacyOccurrences': len(quarantined),
        'quarantinedLegacyFiles': sorted({r['file'] for r in quarantined}),
        'writeOrRootAssignmentPathOccurrences': writes,
        'foreignGenerationWriteOrRootAssignments': foreign_writes,
        'foreignGenerationPathOccurrences': foreign_paths,
        'joinedNonPathLabelsInActiveCode': joined_non_path_active,
        'splitLiteralLabelsInActiveCode': split_all,
        'splitLiteralRootAssignmentsInActiveCode': split_roots,
        'foreignSplitLiteralRootAssignments': foreign_split_roots,
        'historicalReportContentLabelsInActiveCode': content_labels,
        'historicalReportContentLabelStanding': (
            'these occurrences are CONTENT, not paths: helper-correction ids with their true '
            'generations, ancestry rows, and historical narrative sentences. They are counted so '
            'the rebind can be judged, and deliberately NOT rewritten -- rewriting them is defect '
            'class V18-D6 / V19-D1 / V22-D1.'),
        'verdict': ('CLEAN' if not foreign_writes and not foreign_split_roots else
                    'FOREIGN WRITE DESTINATIONS PRESENT -- rebind required before execution'),
    }
    os.makedirs(OUT + '/notes', exist_ok=True)
    with open(OUT + '/notes/v23-path-census.json', 'w') as f:
        json.dump(doc, f, indent=1)
    print('files scanned           :', len(files),
          '(active %d, archived %d, quarantined %d)'
          % (len(doc['activeFiles']), len({r['file'] for r in archived}),
             len(doc['quarantinedLegacyFiles'])))
    print('path-literal occurrences:', len(rows))
    print('by generation           :', {g: len(v) for g, v in sorted(by_gen.items())})
    print('write/root-assign PATH rows:', len(writes))
    print('FOREIGN write/root rows (ACTIVE code only):', len(foreign_writes))
    for r in foreign_writes:
        print('   W %-30s:%-4d %-4s %s' % (os.path.basename(r['file']), r['line'],
                                           r['generation'], r['text'][:90]))
    print('FOREIGN path reads (ACTIVE code only, not already listed):',
          len([r for r in foreign_paths if r not in foreign_writes]))
    for r in foreign_paths:
        if r not in foreign_writes:
            print('   R %-30s:%-4d %-4s %s' % (os.path.basename(r['file']), r['line'],
                                               r['generation'], r['text'][:90]))
    print('JOINED NON-PATH labels (ACTIVE):', len(joined_non_path_active))
    for r in joined_non_path_active:
        print('   J %-30s:%-4d %-4s content=%-5s %s' % (os.path.basename(r['file']), r['line'],
                                                        r['generation'], r['reportContentLabel'],
                                                        r['text'][:80]))
    print('SPLIT-LITERAL labels (ACTIVE):', len(split_all))
    for r in split_all:
        print('   S %-30s:%-4d %-4s root=%-5s %s' % (os.path.basename(r['file']), r['line'],
                                                     r['generation'], r['isRootAssignment'],
                                                     r['text'][:80]))
    print('verdict:', doc['verdict'])


main()
