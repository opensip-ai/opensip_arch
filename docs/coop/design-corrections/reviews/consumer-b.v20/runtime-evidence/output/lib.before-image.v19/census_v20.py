"""LITERAL PATH CENSUS for generation 20 -- run BEFORE any copied code is executed.

Written fresh for this generation. Same method as the generation-19 census (which this origin
authored), with this generation as the expected one:

  * pure read of this runtime's own files; no filesystem access outside it. A referenced root is
    judged by STRING comparison, never by stat'ing a sibling generation.
  * a line is a WRITE candidate when it carries a write-producing construct on a line that also
    carries a path literal, or when it ASSIGNS a constant other lines use as an output root.
  * four groups, and only `active` may be executed:
      active                 this generation's import path (output/lib)
      archived-before-image  output/lib.before-image.* -- historical byte copies, never executed,
                             deliberately still naming their own generation
      quarantined-legacy     output/lib.quarantine-legacy -- tools pinned to an earlier
                             generation's content or write roots
      report-content         an OCCURRENCE class, not a file class: a historical generation label
                             inside report/correction CONTENT. V18-D6 and V19-D1 were both caused
                             by rewriting exactly these, so they are counted and NOT rebound.

The copied rebind scripts are NOT executed: each hardcodes a previous generation as its own
LIB/BEFORE root, so running one would write a before-image into a read-only earlier generation
(the V17-D8 defect class).
"""
import json
import os
import re

RUNTIME = '/tmp/opensip-design-corrections/consumer-b.v20'
OUT = RUNTIME + '/output'
THIS_GEN = 'v20'

GEN = re.compile(r'consumer-b\.v(\d+)')
WRITE_HINTS = (
    "open(", "json.dump", ".write(", "os.makedirs", "shutil.copytree", "shutil.copy",
    "shutil.move", "shutil.rmtree", "os.remove", "os.unlink", "os.rename", "os.rmdir",
    ".export(", "writelines",
)
ROOT_ASSIGN = re.compile(r'^\s*(OUT|ROOT|BEFORE|LIB|DEST|TARGET|SUB|KIT|RUNTIME|V\d+|BASE|REC)'
                         r'\s*=')
CONTENT_MARKERS = ('generation', 'consumerId', 'ancestry', 'ANCESTRY', 'HELPER CORRECTION',
                   'CORRECTED (', 'V17-D', 'V18-D', 'V19-D', 'V16-D', 'V15-D',
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
    rows, writes, by_gen = [], [], {}
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
    foreign_writes = [r for r in writes
                      if r['generation'] != THIS_GEN and r['group'] == 'active']
    foreign_paths = [r for r in rows
                     if r['generation'] != THIS_GEN and r['group'] == 'active'
                     and r['usedAsPath']]
    content_labels = [r for r in rows
                      if r['group'] == 'active' and r['reportContentLabel']]
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
        'historicalReportContentLabelsInActiveCode': content_labels,
        'historicalReportContentLabelStanding': (
            'these occurrences are CONTENT, not paths: helper-correction ids with their true '
            'generations, ancestry rows, and historical narrative sentences. They are counted so '
            'the rebind can be judged, and deliberately NOT rewritten -- rewriting them is '
            'defect class V18-D6 / V19-D1.'),
        'verdict': ('CLEAN' if not foreign_writes else
                    'FOREIGN WRITE DESTINATIONS PRESENT -- rebind required before execution'),
    }
    os.makedirs(OUT + '/notes', exist_ok=True)
    with open(OUT + '/notes/v20-path-census.json', 'w') as f:
        json.dump(doc, f, indent=1)
    print('files scanned           :', len(files),
          '(active %d, archived %d, quarantined %d)'
          % (len(doc['activeFiles']), len({r['file'] for r in archived}),
             len(doc['quarantinedLegacyFiles'])))
    print('path-literal occurrences:', len(rows))
    print('by generation           :', {g: len(v) for g, v in sorted(by_gen.items())})
    print('write/root-assign PATH rows:', len(writes))
    print('FOREIGN write/root rows (ACTIVE code only):', len(foreign_writes))
    for r in foreign_writes[:12]:
        print('   %-30s:%-4d %-4s %s' % (os.path.basename(r['file']), r['line'],
                                         r['generation'], r['text'][:70]))
    print('FOREIGN path reads (ACTIVE code only):', len(foreign_paths))
    for r in foreign_paths[:12]:
        print('   %-30s:%-4d %-4s %s' % (os.path.basename(r['file']), r['line'],
                                         r['generation'], r['text'][:70]))
    print('historical CONTENT labels in active code (NOT to be rebound):', len(content_labels))
    print('verdict:', doc['verdict'])


main()
