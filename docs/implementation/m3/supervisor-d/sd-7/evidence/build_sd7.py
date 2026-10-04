"""Build contract successor SD-7 r2 (law M3-D r5, successor SD-7), in law VD2's clean form.

The record (law VD2, "SD-7 r2"):
- passageSupersessions: one contract passage supersession of SD-5's NE:3540 override. It names SD-5's record by exact
  pin, has the same parent (NE) and selector, its `before` is SD-5's `after`, and its `after` is the raw NE:3540
  release-declaration row followed by SD-5's row conformed to M3-D r5 item 24 (LD-R4-1);
- passageOverrides: NE:3539, a key no bound successor overrides, inserting item 25's request-class row after the
  NOT-SELECTED row (LD-R4-2); and line 1159 of B-S9's two native-model copies, widening
  PUBLIC_ROUTE_REMEDIES["PROVIDER.NOT_SELECTED"].
The two row texts and the remedy are SD-7 r1's, byte for byte (r1's members are kept, for the record only, in
reviews/grok-sd-7-r2/r1-members/). There is no NE copy: NE stays the selected native-evidence contract.

Writes, deterministically: sd-7/PASSAGES.md, sd-7/evidence/fold-report.json (law VD2 item 4's effective NE, which must
equal r1's NE7 byte for byte, and the exact supersededPassages list the review must carry), sd-7/successor.json,
../sd-7-subject.json, and ../sd-7-unit.json (the lead's DRAFT-PENDING-REVIEW record, not part of the subject; it names
reviews/grok-sd-7-r2/review.json, the review it awaits).

Usage: build_sd7.py [--check]   (--check rebuilds in memory, compares with disk and writes nothing)
Run with python3 -I -B. It reads the architecture repository and, read-only through `git show`, the product lock at
LOCK_REV. A rerun reproduces the same bytes. The lock is used for assertions and for the fold; if an NE override or a
B-S9-copy override binds after LOCK_REV, these assertions fail and the unit must be rebuilt and re-reviewed."""
import hashlib, json, subprocess, sys
from pathlib import Path

A = Path(__file__).resolve().parents[6]
PRODUCT = Path('/Users/sb/code/opensip-ai/opensip')
LOCK_REV = '4c761e8'
LOCK_SUCCESSORS = 94
B = 'docs/implementation/m3/supervisor-d/'
D = B + 'sd-7/'
NE = 'docs/v2/contracts/product-v1/native-evidence.md'
SD5 = B + 'sd-5/successor.json'
NEMS = ['docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.py',
        'docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.v2.py']
R1 = 'docs/implementation/m3/reviews/grok-sd-7-r2/r1-members/'
R1_NE7 = {'bytes': 380848, 'sha256': '0dd155c2e2439b2223cdcfaec2ecad61c89bcf6a348f3be3c8f3350e9555ebd3'}
HAND = [D + 'README.md', D + 'evidence/build_sd7.py', D + 'evidence/check_sd7.py', D + 'evidence/verify_scratch.py']
CHECK = '--check' in sys.argv[1:]
NOT_SELECTED_LINE = 3539
SD5_LINE = 3540
REMEDY_LINE = 1159


def raw(p):
    return (A / p).read_bytes()


def pin_bytes(p, b):
    return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def pin(p):
    return pin_bytes(p, raw(p))


def dumps(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


# ---- the texts (SD-7 r1's, unchanged) ---------------------------------------------------------
OLD_REMEDY_PHRASE = 'declare a project hook, root command or probe'
NEW_REMEDY_PHRASE = 'claim a project hook, a reserved or additional root command, or a probe'   # M3-D r5 SD-7 row, verbatim
OLD_PROVENANCE = '(contract successor SD-5 of law M3-D r3, item 24)'
NEW_PROVENANCE = ('(contract successor SD-5 of law M3-D r3, item 24; conformed by contract successor SD-7 to law '
                  'M3-D r5, item 24, lead decision LD-R4-1)')
OLD_EE3B_EE5A = (
    '`EE-3b`, a claim of policy, persistence, rendering, termination or host-lifecycle authority (a `commands` entry '
    'for role `analyzer`, or a capability outside the native capability matrix\'s provider capabilities); `EE-4`, '
    'untrusted native or WASM code; `EE-5a`, a project hook, root command or contribution-granted probe.')
NEW_EE3B_EE5A = (
    '`EE-3b`, a claim of policy, persistence, rendering, termination or host-lifecycle authority (a capability outside '
    'the native capability matrix\'s provider capabilities); `EE-4`, untrusted native or WASM code; `EE-5a`, a project '
    'hook, a contribution-granted probe, or a root-command claim on the host-owned root namespace, which is exactly: (a) '
    'a closure-only manifest (role `toolchain`, `stdlib`, `rust-dev-llvm` or `grammar`) that declares `commands` at '
    'all; (b) an `analyzer` manifest whose command tree does not have exactly one entry without `parent`, or whose '
    'parentless entry\'s `name` differs from the manifest\'s `name`; or (c) a reserved root-command name among its '
    'root-namespace keys (its `name`, each of its `aliases` and, for `analyzer`, each alias of its parentless entry). '
    'An `analyzer` manifest\'s own name-bound mounted root, with any declared depth below it, is not a root-command '
    'claim, and neither is a collision with another component\'s live name; a command tree is never an `EE-3b` form. '
    'A manifest that the security owner\'s manifest admission refuses first never reaches component admission and '
    'keeps that route.')
REMEDY_NOT_SELECTED = ('this capability is not selected for that language mode, or the request asks for an external '
                       'discovery or public-lifecycle endpoint, untrusted native or WASM admission, or network-granted '
                       'analysis; no promise is made for it; restate the request without it')
OLD_REMEDY_NOT_SELECTED = 'this capability is not selected for that language mode; no promise is made for it'
REQUEST_ROW = (
    '| **request that is a request-class excluded form** (contract successor SD-7 of law M3-D r5, item 25, lead '
    'decision LD-R4-2): a well-formed request refused at typed request admission, before the durable entry, the '
    'creation prelude and any `ExecutionId` draw, as `ExcludedForm {class, subject}`, because it represents one of '
    'DR-117\'s request-class excluded forms: `EE-2`, a PlanIntent or admission request that requires an external '
    'discovery or public-lifecycle endpoint; `EE-4` (request part), a PlanIntent requesting untrusted native or WASM '
    'admission; `EE-6a`, a PlanIntent whose analysis branch requests network-granted analysis. Each is outside '
    'D-371\'s selected product, as the `NOT-SELECTED` cell of the row above is: nothing is malformed and the host made '
    'no error, so the route is the same whatever the request\'s origin, and it is never a malformed request or a host '
    'fault | | `request-rejected` (2) | `REQUEST.UNSATISFIABLE` | `PROVIDER.NOT_SELECTED`, carried as `domainDetail` '
    'with subject `excluded-form:<class>`, naming the first class in the order `EE-2`, `EE-4`, `EE-6a` when one '
    'request carries several; remedy "' + REMEDY_NOT_SELECTED + '", the code-keyed remedy it shares with the row above; '
    'the failure envelope\'s `errors` is exactly that detail; every `ExcludedForm` goes to the operational record; no '
    'runId and no executionId |')
assert REMEDY_NOT_SELECTED.isascii() and len(REMEDY_NOT_SELECTED) <= 1024 and '"' not in REMEDY_NOT_SELECTED
assert REQUEST_ROW.count('|') == 6

# ---- the lock at LOCK_REV --------------------------------------------------------------------
lock = json.loads(subprocess.run(['git', '-C', str(PRODUCT), 'show', LOCK_REV + ':design-lock.json'],
                                 check=True, capture_output=True).stdout)
assert len(lock['contractSuccessors']) == LOCK_SUCCESSORS, len(lock['contractSuccessors'])
ne_raw = raw(NE)
ne_pin = pin_bytes(NE, ne_raw)
assert ne_pin['sha256'].startswith('83b99783') and ne_pin in lock['inputs']
ne_lines = ne_raw.decode('utf-8').splitlines()
assert ne_raw.decode('utf-8') == '\n'.join(ne_lines) + '\n' and b'\r' not in ne_raw
bound_ne = []          # every bound entry on NE, in lock order: (record pin, kind, line, after)
nem_bound = {p: [] for p in NEMS}
for b in lock['contractSuccessors']:
    assert pin(b['record']['path']) == b['record'], b['record']['path']
    rec = json.loads(raw(b['record']['path']))
    for kind in ('passageOverrides', 'passageSupersessions'):
        for e in rec.get(kind, []):
            if e['parent']['path'] in nem_bound:
                nem_bound[e['parent']['path']].append(e['selector'])
            if e['parent']['path'] == NE:
                assert kind == 'passageOverrides' and e['parent'] == ne_pin and set(e['selector']) == {'line'}
                assert ne_lines[e['selector']['line'] - 1] == e['before']
                bound_ne.append((b['record'], kind, e['selector']['line'], e['after']))
assert all(v == [] for v in nem_bound.values()), nem_bound
lines_bound = [x[2] for x in bound_ne]
assert NOT_SELECTED_LINE not in lines_bound and lines_bound.count(SD5_LINE) == 1
sd5_pin = next(b['record'] for b in lock['contractSuccessors'] if b['record']['path'] == SD5)
assert sd5_pin == pin(SD5)
sd5_entry = json.loads(raw(SD5))['passageOverrides'][0]
assert sd5_entry['parent'] == ne_pin and sd5_entry['selector'] == {'line': SD5_LINE}
release_row, sd5_row = sd5_entry['after'].split('\n')
assert release_row == ne_lines[SD5_LINE - 1]
for old in (OLD_PROVENANCE, OLD_EE3B_EE5A, OLD_REMEDY_PHRASE):
    assert sd5_row.count(old) == 1, old
conformed = (sd5_row.replace(OLD_PROVENANCE, NEW_PROVENANCE).replace(OLD_EE3B_EE5A, NEW_EE3B_EE5A)
             .replace(OLD_REMEDY_PHRASE, NEW_REMEDY_PHRASE))
assert conformed.count('|') == 6

# ---- the entries ------------------------------------------------------------------------------
supersession = {'parent': ne_pin, 'selector': {'line': SD5_LINE}, 'before': sd5_entry['after'],
                'after': release_row + '\n' + conformed,
                'supersedes': {'record': sd5_pin, 'parent': ne_pin, 'selector': {'line': SD5_LINE}}}
overrides = [{'parent': ne_pin, 'selector': {'line': NOT_SELECTED_LINE}, 'before': ne_lines[NOT_SELECTED_LINE - 1],
              'after': ne_lines[NOT_SELECTED_LINE - 1] + '\n' + REQUEST_ROW}]
nem_parents = []
for p in NEMS:
    before = raw(p).decode('utf-8').splitlines()[REMEDY_LINE - 1]
    assert before == '    "PROVIDER.NOT_SELECTED": ' + json.dumps(OLD_REMEDY_NOT_SELECTED) + ',', (p, before)
    parent = pin(p)
    assert any(r == parent for b in lock['contractSuccessors']
               for r in json.loads(raw(b['record']['path'])).get('candidates', [])), 'not an accepted B-S9 copy'
    nem_parents.append(parent)
    overrides.append({'parent': parent, 'selector': {'line': REMEDY_LINE}, 'before': before,
                      'after': '    "PROVIDER.NOT_SELECTED": ' + json.dumps(REMEDY_NOT_SELECTED) + ','})

# ---- law VD2 item 4: the effective NE, folded in lock order, then SD-7 ------------------------
def fold(entries):
    text = dict()
    for line, after in entries:
        text[line] = after
    return ('\n'.join(text.get(i + 1, l) for i, l in enumerate(ne_lines)) + '\n').encode('utf-8')


before_fold = fold([(x[2], x[3]) for x in bound_ne])
after_fold = fold([(x[2], x[3]) for x in bound_ne] + [(SD5_LINE, supersession['after']),
                                                       (NOT_SELECTED_LINE, overrides[0]['after'])])
assert hashlib.sha256(before_fold).hexdigest().startswith('03b498b7')
assert {'bytes': len(after_fold), 'sha256': hashlib.sha256(after_fold).hexdigest()} == R1_NE7, 'not r1\'s NE7'
r1_ne7 = A / (R1 + 'sd-7/contracts/native-evidence.md')
if r1_ne7.exists():
    assert r1_ne7.read_bytes() == after_fold
superseded_passages = [supersession['supersedes']]
report = {
    'schemaVersion': 1,
    'productRev': LOCK_REV,
    'lockContractSuccessors': LOCK_SUCCESSORS,
    'law': 'VD2 r1 item 4: each override and supersession on a parent, in lock order, sets its passage\'s text',
    'parent': ne_pin,
    'boundEntriesFolded': [{'record': r, 'kind': k, 'selector': {'line': n}} for r, k, n, _ in bound_ne],
    'effectiveBeforeSD7': {'bytes': len(before_fold), 'sha256': hashlib.sha256(before_fold).hexdigest()},
    'sd7EntriesFolded': [{'kind': 'passageSupersessions', 'selector': {'line': SD5_LINE}},
                         {'kind': 'passageOverrides', 'selector': {'line': NOT_SELECTED_LINE}}],
    'effectiveAfterSD7': {'bytes': len(after_fold), 'sha256': hashlib.sha256(after_fold).hexdigest()},
    'equalsSD7r1NE7': True,
    'sd7r1NE7': dict(path=R1 + 'sd-7/contracts/native-evidence.md', **R1_NE7),
    'reviewSupersededPassages': superseded_passages,
}

# ---- generated files ---------------------------------------------------------------------------
files = {D + 'evidence/fold-report.json': dumps(report)}
eff_lines = after_fold.decode('utf-8').splitlines()
i_request = eff_lines.index(REQUEST_ROW)


def render():
    out = ['# SD-7 r2 passages (generated)', '',
           'Generated by `evidence/build_sd7.py`; do not edit by hand. One contract passage supersession (law VD2) and '
           'three line overrides. The texts are SD-7 r1\'s, byte for byte.', '',
           '## Supersession of SD-5\'s NE:3540 override', '',
           '`supersedes`: `%s`' % json.dumps(supersession['supersedes'], sort_keys=True), '',
           'Before (SD-5\'s `after`, two lines):', '', '```text', supersession['before'], '```', '',
           'After (the raw release-declaration row, then the conformed row):', '', '```text', supersession['after'],
           '```', '', '## Override of NE:%d (fresh key)' % NOT_SELECTED_LINE, '', 'Before:', '', '```text',
           overrides[0]['before'], '```', '', 'After:', '', '```text', overrides[0]['after'], '```', '',
           '## Effective NE §10 rows after SD-7 (law VD2 item 4)', '', '```text']
    out += eff_lines[i_request - 1:i_request + 5]
    out += ['```', '', '## Remedy overrides', '']
    for o in overrides[1:]:
        out += ['### `%s` line %d' % (o['parent']['path'], REMEDY_LINE), '', 'Before:', '', '```text', o['before'],
                '```', '', 'After:', '', '```text', o['after'], '```', '']
    return '\n'.join(out).encode('utf-8')


files[D + 'PASSAGES.md'] = render()
candidates = sorted([pin(p) for p in HAND] + [pin_bytes(p, files[p]) for p in
                    (D + 'evidence/fold-report.json', D + 'PASSAGES.md')], key=lambda r: r['path'])
record = {
    'schemaVersion': 1,
    'standing': ('PROPOSED SD-7 r2 contract successor (law M3-D r5 successor SD-7, lead decisions LD-R4-1 and LD-R4-2), '
                 'in law VD2\'s form: native-evidence section 10. (a) A contract passage supersession of SD-5\'s NE:3540 '
                 'override, naming SD-5\'s record by exact pin: SD-5\'s row conformed to M3-D r5 item 24 (EE-3b keeps only '
                 'its capability form; EE-5a\'s root command is exactly the root-command predicate (a), (b), (c), an '
                 'analyzer\'s own mounted root being admitted; the remedy says "claim a project hook, a reserved or '
                 'additional root command, or a probe"). (b) An override of NE:3539 adding item 25\'s request-class row: '
                 'request-rejected 2, REQUEST.UNSATISFIABLE, PROVIDER.NOT_SELECTED, subject excluded-form:<class>, no '
                 'runId or executionId; and line-1159 overrides of B-S9\'s two native-model copies widening '
                 'PUBLIC_ROUTE_REMEDIES["PROVIDER.NOT_SELECTED"] under NE\'s remedy-keying constraint. The texts are SD-7 '
                 'r1\'s, and the effective NE equals r1\'s complete copy byte for byte; no copy is made and NE stays '
                 'selected. Binds only after VD2-a and F8c are integrated; an earlier verify_design refuses it. Existing '
                 'codes only: no new public code, class, exit, D9 member, schema, WS, SL or product change. The exact '
                 'frozen candidate requires actual independent review, whose review lists supersededPassages, and root '
                 'assent.'),
    'parents': sorted([ne_pin] + nem_parents, key=lambda r: r['path']),
    'passageOverrides': overrides,
    'passageSupersessions': [supersession],
    'candidates': candidates,
}
files[D + 'successor.json'] = dumps(record)
rpin = pin_bytes(D + 'successor.json', files[D + 'successor.json'])
subject = {'schemaVersion': 1, 'files': sorted(candidates + [rpin], key=lambda r: r['path'])}
files[B + 'sd-7-subject.json'] = dumps(subject)
spin = pin_bytes(B + 'sd-7-subject.json', files[B + 'sd-7-subject.json'])
unit = {
    'schemaVersion': 1,
    'unit': 'supervisor-d-sd-7',
    'status': 'DRAFT-PENDING-REVIEW',
    'subjectManifest': spin,
    'independentReview': {'path': 'docs/implementation/m3/reviews/grok-sd-7-r2/review.json', 'bytes': None,
                          'sha256': None},
    'rootSubstantiveAssent': False,
    'requiredUnitFindings': [],
    'acceptedSuccessor': rpin,
    'rootAssessment': ('DRAFT. Completed by the lead after Grok\'s review: status ACCEPTED-DESIGN-UNIT, the review pin '
                       '(its review.json carries supersededPassages equal to the record\'s supersedes list), '
                       'rootSubstantiveAssent true. SD-7 r2 is M3-D r5\'s successor SD-7 in VD2\'s clean form: a contract '
                       'passage supersession of SD-5\'s NE:3540 override conforming the row to item 24 (LD-R4-1), an '
                       'NE:3539 override adding item 25\'s request-class row (LD-R4-2), and the PROVIDER.NOT_SELECTED '
                       'remedy widened in B-S9\'s two model copies. No NE copy; the effective NE equals r1\'s NE7. Bound in '
                       'design-lock.json after the VD2-a and F8c commit, in a binding-only product commit.'),
    'fullM2Complete': False,
    'productQualification': False,
}
files[B + 'sd-7-unit.json'] = (json.dumps(unit, indent=2) + '\n').encode('utf-8')

differ = []
for p, b in files.items():
    if CHECK:
        if not (A / p).exists() or raw(p) != b:
            differ.append(p)
    else:
        (A / p).parent.mkdir(parents=True, exist_ok=True)
        (A / p).write_bytes(b)
assert not differ, ('differs from disk', differ)
print(json.dumps({'mode': 'check' if CHECK else 'write', 'lockRev': LOCK_REV, 'neEntriesFolded': len(bound_ne),
                  'effectiveBeforeSD7': report['effectiveBeforeSD7'], 'effectiveAfterSD7': report['effectiveAfterSD7'],
                  'equalsSD7r1NE7': True, 'successor': rpin, 'subject': spin}, indent=1))
