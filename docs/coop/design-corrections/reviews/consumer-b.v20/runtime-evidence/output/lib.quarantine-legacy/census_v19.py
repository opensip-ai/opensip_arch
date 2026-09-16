"""LITERAL PATH CENSUS for generation 19 -- run BEFORE any copied code is executed.

Written fresh for this generation (it is not a copy of census_v18.py: the classifier groups and
the expected generation differ, and the v18 file is itself copied code under audit).

Purpose, stated exactly: find every `consumer-b.vN` path literal in every Python/shell file of
this runtime, classify each occurrence as a READ, a WRITE destination or a ROOT assignment, and
prove that no write destination can land outside generation 19.

Method:
  * pure read of this runtime's own files; no filesystem access outside it (a referenced root is
    judged by STRING comparison, never by stat'ing a sibling generation);
  * a line is a WRITE candidate when it carries a write-producing construct on a line that also
    carries a path literal, or when it ASSIGNS a constant other lines use as an output root;
  * four groups, and only `active` may be executed:
      active                 this generation's import path (output/lib)
      archived-before-image  output/lib.before-image.* -- historical byte copies, never executed,
                             deliberately still naming their own generation
      quarantined-legacy     output/lib.quarantine-legacy -- tools whose target generation is not
                             supplied here; two would write into a read-only earlier generation
      report-content         not a group of files but a group of OCCURRENCES: a historical
                             generation label inside report/correction CONTENT (a narrative, an
                             ancestry row, a helper-correction id). V18-D6 was caused by rewriting
                             exactly these, so they are counted and NOT rebound.
  * the census is printed AND retained, because the rebind that follows is judged against it.

The copied rebind scripts are NOT executed: each hardcodes a previous generation as its own
LIB/BEFORE root, so running one would write a before-image into a read-only earlier generation.
That is the V17-D8 defect class.
"""
import json
import os
import re

RUNTIME = '/tmp/opensip-design-corrections/consumer-b.v19'
OUT = RUNTIME + '/output'
THIS_GEN = 'v19'

GEN = re.compile(r'consumer-b\.v(\d+)')
WRITE_HINTS = (
    "open(", "json.dump", ".write(", "os.makedirs", "shutil.copytree", "shutil.copy",
    "shutil.move", "shutil.rmtree", "os.remove", "os.unlink", "os.rename", "os.rmdir",
    ".export(", "writelines",
)
ROOT_ASSIGN = re.compile(r'^\s*(OUT|ROOT|BEFORE|LIB|DEST|TARGET|SUB|KIT|RUNTIME|V\d+|BASE|REC)'
                         r'\s*=')
# A generation label that is CONTENT: it sits inside a quoted narrative field or a correction id
# rather than in a filesystem path. Recognised by the absence of a path separator right after the
# label and by the line naming a record field or a historical marker.
CONTENT_MARKERS = ('generation', 'consumerId', 'ancestry', 'ANCESTRY', 'HELPER CORRECTION',
                   'CORRECTED (', 'V17-D', 'V18-D', 'V16-D', 'V15-D', 'previous-review',
                   'wasReportedAs', 'originalFailure', 'declaredInputIdenticalTo',
                   'historical', 'prior generation', "sameDefectClassAs")


def group_of(rel):
    s = '/' + rel
    if '/lib.before-image.' in s:
        return 'archived-before-image'
    if '/lib.quarantine-legacy/' in s:
        return 'quarantined-legacy'
    return 'active'


def is_path_occurrence(line, m):
    """True when the label is used as a PATH (followed by a separator or a quote that closes a
    directory root), false when it is narrative content."""
    tail = line[m.end():m.end() + 2]
    return tail.startswith('/') or tail.startswith("'/") or tail.startswith('"/')


def looks_like_content(line):
    return any(k in line for k in CONTENT_MARKERS)


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
                       'reportContentLabel': (not path_use) and looks_like_content(line),
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
        'runtime': RUNTIME,
        'thisGeneration': THIS_GEN,
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
            'these occurrences are CONTENT, not paths: helper-correction ids and their true '
            'generations, ancestry rows, and historical narrative sentences. They are counted '
            'here so the rebind can be judged, and they are deliberately NOT rewritten -- '
            'rewriting them is exactly defect V18-D6.'),
        'verdict': ('CLEAN' if not foreign_writes else
                    'FOREIGN WRITE DESTINATIONS PRESENT -- rebind required before execution'),
    }
    os.makedirs(OUT + '/notes', exist_ok=True)
    with open(OUT + '/notes/v19-path-census.json', 'w') as f:
        json.dump(doc, f, indent=1)
    print('files scanned           :', len(files),
          '(active %d, archived %d, quarantined %d)'
          % (len(doc['activeFiles']), len({r['file'] for r in archived}),
             len(doc['quarantinedLegacyFiles'])))
    print('path-literal occurrences:', len(rows))
    print('by generation           :', {g: len(v) for g, v in sorted(by_gen.items())})
    print('write/root-assign PATH rows:', len(writes))
    print('FOREIGN write/root rows (ACTIVE code only):', len(foreign_writes))
    for r in foreign_writes[:60]:
        print('   %-34s:%-4d %-4s %-26s %s'
              % (os.path.basename(r['file']), r['line'], r['generation'],
                 ','.join(r['writeConstructsOnThisLine']) or 'ROOT=', r['text'][:64]))
    print('FOREIGN path reads (ACTIVE code only):', len(foreign_paths))
    for r in foreign_paths[:25]:
        print('   %-34s:%-4d %-4s %s'
              % (os.path.basename(r['file']), r['line'], r['generation'], r['text'][:72]))
    print('historical CONTENT labels in active code (NOT to be rebound):', len(content_labels))
    print('verdict:', doc['verdict'])


main()
