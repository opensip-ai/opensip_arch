"""LITERAL PATH CENSUS -- run BEFORE any copied code is executed.

Purpose, stated exactly: find every `consumer-b.vN` path literal in every copied Python/shell
file of this runtime, classify each occurrence as a READ or a WRITE destination, and prove that
no write destination can land outside this generation.

Method:
  * pure read of this runtime's own files; NO filesystem access outside it (a referenced root
    is judged by STRING comparison, not by stat'ing a sibling directory);
  * a line is a WRITE candidate when it contains any write-producing construct
    (open(..,'w'|'a'|'x'|'wb'), json.dump(, .write(, os.makedirs, shutil.copy*/move/rmtree,
    os.remove/unlink/rename, .export(, put_record/put_blob into a path, subprocess with a
    redirect) on a line that also carries a path literal, or the line ASSIGNS a constant that
    other lines use as an output root (OUT/BEFORE/ROOT/DEST/TARGET);
  * the census is printed AND retained, because the rebind that follows is judged against it.

This file is written fresh for this generation. The copied rebind scripts are NOT executed:
each hardcodes a previous generation as its own LIB/BEFORE root, so running one would write a
before-image into a read-only earlier generation. That is precisely the V17-D8 defect class.
"""
import json
import os
import re
import sys

RUNTIME = '/tmp/opensip-design-corrections/consumer-b.v18'
OUT = RUNTIME + '/output'
LIB = OUT + '/lib'

GEN = re.compile(r'consumer-b\.v(\d+)')
WRITE_HINTS = (
    "open(", "json.dump", ".write(", "os.makedirs", "shutil.copytree", "shutil.copy",
    "shutil.move", "shutil.rmtree", "os.remove", "os.unlink", "os.rename", "os.rmdir",
    ".export(", "writelines",
)
ROOT_ASSIGN = re.compile(r'^\s*(OUT|ROOT|BEFORE|LIB|DEST|TARGET|SUB|KIT|RUNTIME|V\d+|BASE|REC)'
                         r'\s*=')


def classify(line):
    hints = [h for h in WRITE_HINTS if h in line]
    return hints


def group_of(rel):
    """ACTIVE code is what this generation may execute; an ARCHIVED before-image is a
    historical copy that must stay byte-identical and must never be executed."""
    return 'archived-before-image' if '/lib.before-image.' in '/' + rel else 'active'


def main():
    files = []
    for d, _dirs, names in os.walk(OUT):
        for n in sorted(names):
            if n.endswith(('.py', '.sh', '.bash')):
                files.append(os.path.join(d, n))
    files.sort()
    rows, writes, roots = [], [], {}
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
                hints = classify(line)
                is_assign = bool(ROOT_ASSIGN.match(line))
                row = {'file': rel, 'group': group_of(rel), 'line': i,
                       'generation': gen,
                       'isRootAssignment': is_assign,
                       'writeConstructsOnThisLine': hints,
                       'text': line.strip()[:160]}
                rows.append(row)
                roots.setdefault(gen, set()).add(rel)
                if hints or is_assign:
                    writes.append(row)
    # a WRITE destination is dangerous when its generation is not this one AND the file is
    # ACTIVE code. An archived before-image legitimately still names its own generation: that
    # is what makes it a before-image, and it is never executed.
    foreign_writes = [r for r in writes
                      if r['generation'] != 'v18' and r['group'] == 'active']
    foreign_any = [r for r in rows
                   if r['generation'] != 'v18' and r['group'] == 'active']
    archived = [r for r in rows if r['group'] == 'archived-before-image']
    doc = {
        'standing': __doc__,
        'runtime': RUNTIME,
        'filesScanned': len(files),
        'occurrencesTotal': len(rows),
        'occurrencesByGeneration': {g: sorted(v) for g, v in sorted(roots.items())},
        'activeFiles': sorted({r['file'] for r in rows if r['group'] == 'active'}),
        'archivedBeforeImageOccurrences': len(archived),
        'archivedBeforeImageStanding': (
            'output/lib.before-image.v14 / .v15 / .v16 are HISTORICAL COPIES retained as '
            'evidence of earlier corrections. They legitimately still name their own '
            'generation, they are NOT rebound, and they are NEVER executed: no stage of this '
            "generation's command imports from them."),
        'writeOrRootAssignmentOccurrences': writes,
        'foreignGenerationWriteOrRootAssignments': foreign_writes,
        'foreignGenerationOccurrencesAny': foreign_any,
        'allOccurrences': rows,
        'copiedRebindScriptsNotExecuted': sorted(
            os.path.basename(p) for p in files
            if os.path.basename(p).startswith('rebind_')),
        'verdict': ('CLEAN' if not foreign_writes else
                    'FOREIGN WRITE DESTINATIONS PRESENT -- rebind required before execution'),
    }
    os.makedirs(OUT + '/notes', exist_ok=True)
    with open(OUT + '/notes/v18-path-census.json', 'w') as f:
        json.dump(doc, f, indent=1)
    print('files scanned          :', len(files),
          '(active %d, archived before-image %d)'
          % (len(doc['activeFiles']),
             len({r['file'] for r in archived})))
    print('path-literal occurrences:', len(rows))
    print('by generation          :',
          {g: len(v) for g, v in sorted(roots.items())})
    print('write/root-assign rows :', len(writes))
    print('FOREIGN write/root rows (ACTIVE code only):', len(foreign_writes))
    for r in foreign_writes[:40]:
        print('   %-34s:%-4d %-4s %-28s %s'
              % (os.path.basename(r['file']), r['line'], r['generation'],
                 ','.join(r['writeConstructsOnThisLine']) or 'ROOT=',
                 r['text'][:70]))
    print('copied rebind scripts (NOT executed):', doc['copiedRebindScriptsNotExecuted'])
    print('verdict:', doc['verdict'])


main()
