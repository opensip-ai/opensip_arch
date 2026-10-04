"""Build contract successor S21 of law M3-J1 r5: the commit-outcome exception to WS's before-settle rule.

J1 r5's lead decision LD-r5-2 keeps 8.3's rules 1 and 2. A signal observed before settlement that meets an
undetermined commit takes the durability row (IE:1680-1681), and one that meets a commit latched after FinalGate
admission takes the DELIVERY.REQUIRED_FAILED row (SL:551-554). WS:226 still makes every before-settle aggregate
`interrupted` (130). S21 is the passage successor that states the exception on WS:226 and on WSE:226, the matching
line of WS's selected effective copy. r2 (Grok r1 RF-1) also qualifies the paragraph's per-kind sentence on WS:229
and WSE:233, which the exception made false: "an analysis attempt that the signal aborts leaves no Run". It
changes nothing else in WS, and in particular no line that contract successor S18 binds (WS:225, 227, 228, 231 and
1393; WSE:225, 229, 230, 235 and 1466).

Form: all four lines are free in the lock, so each takes one line-selector passage override. The WS and WSE
overrides carry the same before and after, pair by pair.

Writes, deterministically: s21/PASSAGES.md, s21/evidence/reading-report.json, s21/successor.json,
../s21-subject.json and ../s21-unit.json (the lead's DRAFT-PENDING-REVIEW record). With --check it builds
everything in memory and compares it with the files on disk, writing nothing. It reads the architecture
repository, and the product lock at PRODUCT_REV through read-only `git show`. Run with python3.14 -I -B at
nice -n 19."""
import hashlib, json, subprocess, sys
from pathlib import Path

A = Path(__file__).resolve().parents[6]
PRODUCT = Path('/Users/sb/code/opensip-ai/opensip')
PRODUCT_REV = '6190e66'   # r2 base: SYN-NS bound, 92 contract successors (r1 was built on 218465f, 91)
REVIEW_PATH = 'docs/implementation/m3/reviews/codex2-s21-r2/review.json'
J = 'docs/implementation/m3/host-pipeline-j/'
S = J + 's21/'
WS = 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'
WSE = 'docs/implementation/m1/source-selection-v2/reference/effective-workflows-and-surfaces.md'
S18_RECORD = J + 's18/successor.json'
J1_R5_SHA256 = '4ccb23204b9d072464c3daa63eba8238c0f0425d38ea0da6c93df21711877599'   # Codex's r5 acceptance
HAND = [S + 'README.md', S + 'evidence/build_s21.py', S + 'evidence/check_s21.py', S + 'evidence/verify_scratch.py']
GENERATED = [S + 'PASSAGES.md', S + 'evidence/reading-report.json']
CHECK = '--check' in sys.argv[1:]

LINE = 226   # the same line on both parents
PER_KIND = {'docs/v2/contracts/product-v1/workflows-and-surfaces.md': 229,
            'docs/implementation/m1/source-selection-v2/reference/effective-workflows-and-surfaces.md': 233}
# r2 (Grok r1 RF-1): the per-kind sentence, Grok's replacement verbatim. The line still ends "an import discards its",
# so the next line's "staged bytes;" still joins.
PER_KIND_BEFORE = 'Per kind: an analysis attempt aborts and leaves no Run; an import discards its'
PER_KIND_AFTER = 'Per kind: an analysis attempt that the signal aborts leaves no Run; an import discards its'
# The paragraph, with S18 bound (WS:225-228): "*before-settle* (…): remaining steps are" / LINE /
# "step is named in the termination's `runId`. *after-settle* (…". S21's after must carry the sentence into 227.
BEFORE = '`cancelled`, the aggregate is `interrupted` (130), and a Run committed by an earlier'
AFTER = (
    '`cancelled`, and the aggregate is `interrupted` (130) unless a required analysis or verify step\'s commit '
    'returned one of two outcomes, which govern instead (contract successor S21 of law M3-J1 r5): an undetermined '
    'commit is `operational-failed` (4) with `DURABILITY.COMMIT_FAILED`, fault cause `durability-commit`, no '
    '`runId` and the attempt\'s ExecutionId disclosed for read-only recovery (identity-and-evidence §5\'s '
    '`durability-undetermined`); a commit whose FinalGate was latched after admission stays committed and is '
    '`operational-failed` (4) through `DELIVERY.REQUIRED_FAILED` (`delivery-required`), with its `runId` '
    '(security-and-lifecycle S6\'s selected law). The outcome the commit returned decides, never the gate\'s latch '
    'state alone. In the `interrupted` case, a Run committed by an earlier')
# Lines S18 binds on each parent; S21 must leave every one of them alone.
S18_LINES = {WS: [225, 227, 228, 231, 1393], WSE: [225, 229, 230, 235, 1466]}
PARAGRAPH = {WS: (224, 231), WSE: (224, 235)}   # the cancellation paragraph on each parent

STANDING = (
    'PROPOSED S21 contract successor (law M3-J1 r5 successor S21, the commit-outcome exception to the before-settle '
    'rule, lead decision LD-r5-2; J1 r5 accepted by Codex, sha256 ' + J1_R5_SHA256 + '): a passage successor to '
    'workflows-and-surfaces section 1\'s before-settle consequence at WS:226 and to the matching line of its selected '
    'effective copy, WSE:226, and to the paragraph\'s per-kind sentence at WS:229 and WSE:233. Four line overrides, '
    'the WS and WSE lines of each pair with the same before and after. A signal observed before settlement '
    'leaves the aggregate interrupted (130), except where a required analysis or verify step\'s commit returned one '
    'of two outcomes, matched on the returned outcome and never on the gate\'s latch state alone: an undetermined '
    'commit (operational-failed 4, DURABILITY.COMMIT_FAILED, durability-commit, the ExecutionId disclosed, no '
    'runId; identity-and-evidence\'s durability-undetermined) or a commit latched after FinalGate admission '
    '(operational-failed 4 through DELIVERY.REQUIRED_FAILED, delivery-required, with its runId; '
    'security-and-lifecycle S6\'s selected law). The per-kind sentence then reads "an analysis attempt that the '
    'signal aborts leaves no Run", so that neither exception is contradicted. The lines contract successor S18 binds '
    '(WS:225, 227, 228, 231 and '
    '1393; WSE:225, 229, 230, 235 and 1466) are untouched, and the sentence reads on into S18\'s WS:227 and '
    'WSE:227. No code, class, exit, field, step outcome, route, public code, schema, inventory or product change. '
    'The exact frozen candidate requires actual independent review and root assent.')


def git_show(rev, path):
    return subprocess.run(['git', '-C', str(PRODUCT), 'show', '%s:%s' % (rev, path)], check=True,
                          capture_output=True).stdout


def pin_bytes(path, b):
    return {'path': path, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


OUT = {}


def emit(path, b):
    OUT[path] = b


def current(path):
    return OUT[path] if path in OUT else (A / path).read_bytes()


def pin(path):
    return pin_bytes(path, current(path))


def jbytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


def lines_of(raw):
    text = raw.decode('utf-8')
    assert text.endswith('\n') and '\r' not in text and text.split('\n')[:-1] == text.splitlines()
    return text.split('\n')[:-1]


# --- the product lock: the accepted set, and the entries bound to each parent ---------------------------
lock = json.loads(git_show(PRODUCT_REV, 'design-lock.json'))
accepted = {}
for name in ('sourceManifest', 'applicationManifest'):
    for row in json.loads((A / lock['approvals'][name]['path']).read_bytes())['files']:
        accepted[row['path']] = {k: row[k] for k in ('path', 'bytes', 'sha256')}
for binding in lock['inventorySuccessors']:
    accepted[binding['candidate']['path']] = binding['candidate']
bound = {}
records = [b['record']['path'] for b in lock['contractSuccessors']]
assert S18_RECORD in records, 'S18 is not bound at ' + PRODUCT_REV
for binding in lock['contractSuccessors']:
    for row in json.loads((A / binding['subjectManifest']['path']).read_bytes())['files']:
        accepted[row['path']] = row
    record = json.loads((A / binding['record']['path']).read_bytes())
    for kind in ('passageOverrides', 'passageSupersessions'):
        for entry in record.get(kind, []):
            bound.setdefault(entry['parent']['path'], []).append(
                {'record': binding['record']['path'], 'kind': kind, 'selector': entry['selector'],
                 'after': entry['after']})

# --- the four overrides, and the effective paragraph they leave ----------------------------------------
parents, overrides, report = [], [], {'schemaVersion': 1, 'productRev': PRODUCT_REV,
                                      'contractSuccessors': len(lock['contractSuccessors']), 'parents': []}
for path in (WS, WSE):
    raw = (A / path).read_bytes()
    parent = pin_bytes(path, raw)
    assert accepted.get(path) == parent, ('parent is not the accepted pin', path)
    lines = lines_of(raw)
    entries = bound.get(path, [])
    taken = {e['selector'].get('line'): e for e in entries if 'line' in e['selector']}
    s18 = sorted(n for n, e in taken.items() if e['record'] == S18_RECORD)
    assert s18 == S18_LINES[path], (path, s18)
    mine = {LINE: (BEFORE, AFTER), PER_KIND[path]: (PER_KIND_BEFORE, PER_KIND_AFTER)}
    for n, (before, after) in sorted(mine.items()):
        assert n not in taken and n not in s18, ('line already bound', path, n)
        assert lines[n - 1] == before and after != before, (path, n, lines[n - 1])
        overrides.append({'parent': parent, 'selector': {'line': n}, 'before': before, 'after': after})
    assert lines[PER_KIND[path]].startswith('staged bytes;')   # the next line still joins
    parents.append(parent)
    first, last = PARAGRAPH[path]
    effective = []
    for n in range(first, last + 1):
        if n in mine:
            effective.append({'line': n, 'by': 'S21', 'text': mine[n][1]})
        elif n in taken:
            effective.append({'line': n, 'by': taken[n]['record'], 'text': taken[n]['after']})
        else:
            effective.append({'line': n, 'by': None, 'text': lines[n - 1]})
    reading = ' '.join(e['text'].split('\n\n')[0] for e in effective)
    assert ('remaining steps are `cancelled`, and the aggregate is `interrupted` (130) unless a required analysis or '
            'verify step\'s commit returned one of two outcomes') in reading
    assert 'In the `interrupted` case, a Run committed by an earlier step is named in the termination\'s `runId`.' \
        in reading
    assert ('Per kind: an analysis attempt that the signal aborts leaves no Run; an import discards its staged bytes;'
            in reading and 'an analysis attempt aborts and leaves no Run' not in reading)
    report['parents'].append({'parent': parent, 'boundEntries': [{k: e[k] for k in ('record', 'kind', 'selector')}
                                                                 for e in entries],
                              's18Lines': s18, 's21Lines': sorted(mine), 'effectiveParagraph': effective,
                              'readingToFirstBlankLine': reading})
emit(S + 'evidence/reading-report.json', jbytes(report))

# --- PASSAGES.md ----------------------------------------------------------------------------------------
def block(text):
    return '```text\n' + text + '\n```\n'


md = ['# S21 passages (generated by `evidence/build_s21.py`; do not edit)\n',
      'Base: the product lock at `%s` (%d contract successors, S18 among them). Each `before` is the parent\'s exact '
      'line; each `after` replaces that one line. WS:226 and WSE:226 are identical, and so are WS:229 and WSE:233 '
      '(r2, Grok r1 RF-1).\n'
      % (PRODUCT_REV, len(lock['contractSuccessors']))]
for i, o in enumerate(overrides, 1):
    md.append('## %d. `%s`, line %d\n' % (i, o['parent']['path'], o['selector']['line']))
    md.append('Before:\n\n' + block(o['before']) + '\nAfter:\n\n' + block(o['after']))
for p in report['parents']:
    md.append('## The paragraph as it reads with S18 and S21: `%s`\n' % p['parent']['path'])
    md.append('Lines %d to %d. The text after S18\'s final-output-section paragraph begins is cut at its first blank '
              'line.\n' % (p['effectiveParagraph'][0]['line'], p['effectiveParagraph'][-1]['line']))
    md.append(block(p['readingToFirstBlankLine']))
emit(S + 'PASSAGES.md', '\n'.join(md).encode('utf-8'))

# --- the record, the subject and the unit draft --------------------------------------------------------
candidates = sorted([pin(p) for p in HAND + GENERATED], key=lambda r: r['path'])
record = {'schemaVersion': 1, 'standing': STANDING, 'parents': sorted(parents, key=lambda r: r['path']),
          'passageOverrides': overrides, 'candidates': candidates}
emit(S + 'successor.json', jbytes(record))
subject = {'schemaVersion': 1, 'files': sorted(candidates + [pin(S + 'successor.json')], key=lambda r: r['path'])}
emit(J + 's21-subject.json', jbytes(subject))
unit = {
    'schemaVersion': 1, 'unit': 'host-pipeline-j-s21', 'status': 'DRAFT-PENDING-REVIEW',
    'subjectManifest': pin(J + 's21-subject.json'),
    'independentReview': {'path': REVIEW_PATH, 'bytes': None, 'sha256': None},
    'rootSubstantiveAssent': False, 'requiredUnitFindings': [],
    'acceptedSuccessor': pin(S + 'successor.json'),
    'rootAssessment': ('DRAFT r2. Completed by the lead after Grok\'s r2 review: status ACCEPTED-DESIGN-UNIT, the '
                       'review pin, rootSubstantiveAssent true. S21 is law M3-J1 r5\'s commit-outcome successor '
                       '(LD-r5-2): line overrides of WS:226 and WSE:226, stating that a before-settle signal leaves the '
                       'aggregate interrupted except where a required analysis or verify step\'s commit returned '
                       'undetermined (the durability row, with its ExecutionId) or committed latched after FinalGate '
                       'admission (DELIVERY.REQUIRED_FAILED, with its runId); and, in r2 for Grok\'s r1 RF-1, of '
                       'WS:229 and WSE:233, where the per-kind sentence becomes "an analysis attempt that the signal '
                       'aborts leaves no Run". S18\'s lines are untouched. It binds on '
                       'the verify_design at product ' + PRODUCT_REV + ' on top of ' +
                       str(len(lock['contractSuccessors'])) + ' contract successors.'),
    'fullM2Complete': False, 'productQualification': False,
}
emit(J + 's21-unit.json', jbytes(unit))

if CHECK:
    diffs = [p for p, b in OUT.items() if not (A / p).exists() or (A / p).read_bytes() != b]
    print(json.dumps({'check': 'identical' if not diffs else 'DIFFERENT', 'differing': diffs}, indent=1))
    sys.exit(1 if diffs else 0)
for p, b in OUT.items():
    (A / p).parent.mkdir(parents=True, exist_ok=True)
    (A / p).write_bytes(b)
print(json.dumps({'overrides': len(overrides), 'successor': pin(S + 'successor.json'),
                  'subject': pin(J + 's21-subject.json')}, indent=1))
