"""Build contract successor SD-7 (law M3-D r5, successor SD-7): NE section 10's follow-ups from M3-D r4.

Form (lead decision LD-7.1):
- NE: a complete successor copy, B-S9's form. The copy is NE's EFFECTIVE text under the product lock at LOCK_REV
  (the raw parent with every passage override the lock binds to it applied, in lock order) with exactly two
  hunks: SD-5's row conformed to M3-D r5 item 24 (LD-R4-1), and item 25's request-class row inserted after the
  NOT-SELECTED row (LD-R4-2). SD-5's row is NE:3540's bound meaning, and verify_design refuses a second override of
  that selector, so no line override can conform it.
- The remedy: PUBLIC_ROUTE_REMEDIES["PROVIDER.NOT_SELECTED"] is widened by fresh line overrides of line 1159 of
  B-S9's two model copies, which no bound successor overrides.

Writes, deterministically: sd-7/contracts/native-evidence.md, sd-7/evidence/copies-report.json, sd-7/PASSAGES.md,
sd-7/successor.json, ../sd-7-subject.json and ../sd-7-unit.json (the lead's DRAFT-PENDING-REVIEW record, not part of
the subject; it names reviews/grok-sd-7-r1/review.json as the review it awaits).

Usage: build_sd7.py [--check]   (--check rebuilds in memory, compares with disk and writes nothing)
Run with python3 -I -B. It reads the architecture repository and, read-only through `git show`, the product lock at
LOCK_REV. A rerun reproduces the same bytes. If any NE override binds after LOCK_REV, the copy must be rebuilt on the
new lock and re-reviewed: the lock assertions below fail first."""
import hashlib, json, subprocess, sys
from pathlib import Path

A = Path(__file__).resolve().parents[6]
PRODUCT = Path('/Users/sb/code/opensip-ai/opensip')
LOCK_REV = '6190e66'
LOCK_SUCCESSORS = 92
B = 'docs/implementation/m3/supervisor-d/'
D = B + 'sd-7/'
NE = 'docs/v2/contracts/product-v1/native-evidence.md'
COPY = D + 'contracts/native-evidence.md'
SD5 = B + 'sd-5/successor.json'
NEMS = ['docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.py',
        'docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.v2.py']
HAND = [D + 'README.md', D + 'evidence/build_sd7.py', D + 'evidence/check_sd7.py', D + 'evidence/verify_scratch.py']
CHECK = '--check' in sys.argv[1:]
NOT_SELECTED_LINE = 3539   # raw NE: the "unsatisfiable capability REQUEST" (NOT-SELECTED cell) row
SD5_LINE = 3540            # raw NE: SD-5's bound override (the release declaration row, then SD-5's row)
REMEDY_LINE = 1159         # B-S9 copies: PUBLIC_ROUTE_REMEDIES["PROVIDER.NOT_SELECTED"]


def raw(p):
    return (A / p).read_bytes()


def pin_bytes(p, b):
    return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def pin(p):
    return pin_bytes(p, raw(p))


def dumps(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


# ---- the texts --------------------------------------------------------------------------------
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
applied, seen = [], {}
nem_bound = {p: [] for p in NEMS}
for b in lock['contractSuccessors']:
    assert pin(b['record']['path']) == b['record'], b['record']['path']
    rec = json.loads(raw(b['record']['path']))
    for kind in ('passageOverrides', 'passageSupersessions'):
        for e in rec.get(kind, []):
            if e['parent']['path'] in nem_bound:
                nem_bound[e['parent']['path']].append(e['selector'])
            if e['parent']['path'] != NE:
                continue
            assert kind == 'passageOverrides' and e['parent'] == ne_pin and set(e['selector']) == {'line'}
            n = e['selector']['line']
            assert ne_lines[n - 1] == e['before'], (b['record']['path'], n)
            assert '\r' not in e['after']
            if n in seen:
                assert seen[n] == e['after'], ('conflicting bound overrides', n)
                continue
            seen[n] = e['after']
            applied.append({'record': b['record'], 'kind': kind, 'selector': {'line': n}})
assert all(v == [] for v in nem_bound.values()), nem_bound
assert NOT_SELECTED_LINE not in seen and SD5_LINE in seen
sd5_record_pin = next(b['record'] for b in lock['contractSuccessors'] if b['record']['path'] == SD5)

# ---- effective NE and the copy -----------------------------------------------------------------
effective = [seen.get(i + 1, line) for i, line in enumerate(ne_lines)]   # one element per raw line
effective_text = '\n'.join(effective) + '\n'
release_row, sd5_row = effective[SD5_LINE - 1].split('\n')
assert release_row == ne_lines[SD5_LINE - 1]
sd5_after = next(o for o in json.loads(raw(SD5))['passageOverrides'] if o['selector'] == {'line': SD5_LINE})['after']
assert effective[SD5_LINE - 1] == sd5_after
for old in (OLD_PROVENANCE, OLD_EE3B_EE5A, OLD_REMEDY_PHRASE):
    assert sd5_row.count(old) == 1, old
conformed = (sd5_row.replace(OLD_PROVENANCE, NEW_PROVENANCE).replace(OLD_EE3B_EE5A, NEW_EE3B_EE5A)
             .replace(OLD_REMEDY_PHRASE, NEW_REMEDY_PHRASE))
assert conformed.count('|') == 6 and '`commands` entry for role `analyzer`' not in conformed
copy_elems = list(effective)
copy_elems[SD5_LINE - 1] = release_row + '\n' + conformed
copy_elems[NOT_SELECTED_LINE - 1] = ne_lines[NOT_SELECTED_LINE - 1] + '\n' + REQUEST_ROW
copy_text = '\n'.join(copy_elems) + '\n'
assert not any(c in copy_text for c in '\x0b\x0c\x1c\x1d\x1e\x85  \r')

# Line map: for each raw NE line, its first line in the copy and how many copy lines it spans.
segments, expanded, at, run = [], [], 1, None
for i, elem in enumerate(copy_elems):
    n_lines = elem.count('\n') + 1
    if n_lines == 1 and elem == ne_lines[i]:
        if run is not None and run[1] == i:
            run[1] = i + 1
        else:
            run = [i + 1, i + 1, at]
            segments.append(run)
    else:
        run = None
        expanded.append({'rawLine': i + 1, 'copyLine': at, 'copyLines': n_lines,
                         'source': 'SD-7' if (i + 1) in (NOT_SELECTED_LINE, SD5_LINE) else 'bound override'})
    at += n_lines
copy_line_of = {e['rawLine']: e['copyLine'] for e in expanded}
request_row_line = copy_line_of[NOT_SELECTED_LINE] + 1
conformed_row_line = copy_line_of[SD5_LINE] + 1
copy_lines = copy_text.splitlines()
assert copy_lines[request_row_line - 1] == REQUEST_ROW and copy_lines[conformed_row_line - 1] == conformed

# ---- the remedy overrides ----------------------------------------------------------------------
nem_parents, overrides = [], []
for p in NEMS:
    lines = raw(p).decode('utf-8').splitlines()
    before = lines[REMEDY_LINE - 1]
    assert before == '    "PROVIDER.NOT_SELECTED": ' + json.dumps(OLD_REMEDY_NOT_SELECTED) + ',', (p, before)
    parent = pin(p)
    assert any(r['path'] == p and r == parent for b in lock['contractSuccessors']
               for r in json.loads(raw(b['record']['path'])).get('candidates', [])), 'not an accepted B-S9 copy'
    nem_parents.append(parent)
    overrides.append({'parent': parent, 'selector': {'line': REMEDY_LINE}, 'before': before,
                      'after': '    "PROVIDER.NOT_SELECTED": ' + json.dumps(REMEDY_NOT_SELECTED) + ','})

# ---- generated files ---------------------------------------------------------------------------
files = {COPY: copy_text.encode('utf-8')}
report = {
    'schemaVersion': 1,
    'productRev': LOCK_REV,
    'lockContractSuccessors': LOCK_SUCCESSORS,
    'parent': ne_pin,
    'boundEntriesApplied': applied,
    'effectiveParent': {'bytes': len(effective_text.encode('utf-8')),
                        'sha256': hashlib.sha256(effective_text.encode('utf-8')).hexdigest()},
    'copy': pin_bytes(COPY, files[COPY]),
    'hunks': [
        {'what': 'item 25 request-class row inserted after the NOT-SELECTED row (raw NE:%d)' % NOT_SELECTED_LINE,
         'copyLine': request_row_line, 'before': None, 'after': REQUEST_ROW},
        {'what': 'SD-5 row (second line of raw NE:%d\'s bound override) conformed to M3-D r5 item 24' % SD5_LINE,
         'copyLine': conformed_row_line, 'before': sd5_row, 'after': conformed},
    ],
    'lineMap': {'note': 'unchanged raw NE lines map in runs [rawStart, rawEnd, copyStart]; every other raw line is '
                        'listed in expanded with its first copy line and span',
                'runs': segments, 'expanded': expanded},
    'remedyOverrides': [{'parent': o['parent'], 'line': REMEDY_LINE, 'before': o['before'], 'after': o['after']}
                        for o in overrides],
}
files[D + 'evidence/copies-report.json'] = dumps(report)


def render():
    out = ['# SD-7 passages (generated)', '',
           'Generated by `evidence/build_sd7.py`; do not edit by hand. The NE copy `contracts/native-evidence.md` is '
           'NE\'s effective text under the lock at `%s` with exactly the two hunks below. The remedy overrides are '
           'line overrides of B-S9\'s two model copies.' % LOCK_REV, '',
           '## NE copy, hunk 1: the request-class row (copy line %d)' % request_row_line, '',
           'Inserted after the NOT-SELECTED row (raw NE:%d, unchanged).' % NOT_SELECTED_LINE, '', '```text',
           REQUEST_ROW, '```', '',
           '## NE copy, hunk 2: SD-5\'s row conformed (copy line %d)' % conformed_row_line, '', 'Before (SD-5\'s bound row):',
           '', '```text', sd5_row, '```', '', 'After:', '', '```text', conformed, '```', '',
           '## Effective table rows in the copy', '', '```text']
    out += copy_lines[copy_line_of[NOT_SELECTED_LINE] - 1:conformed_row_line + 1]
    out += ['```', '', '## Remedy overrides', '']
    for o in overrides:
        out += ['### `%s` line %d' % (o['parent']['path'], REMEDY_LINE), '', 'Before:', '', '```text', o['before'],
                '```', '', 'After:', '', '```text', o['after'], '```', '']
    return '\n'.join(out).encode('utf-8')


files[D + 'PASSAGES.md'] = render()
candidates = sorted([pin(p) for p in HAND] + [pin_bytes(p, files[p]) for p in
                    (COPY, D + 'evidence/copies-report.json', D + 'PASSAGES.md')], key=lambda r: r['path'])
record = {
    'schemaVersion': 1,
    'standing': ('PROPOSED SD-7 contract successor (law M3-D r5 successor SD-7, lead decisions LD-R4-1 and LD-R4-2): '
                 'native-evidence section 10. (a) SD-5\'s bound row conformed to M3-D r5 item 24: EE-3b keeps only its '
                 'capability form; EE-5a\'s root command is exactly the root-command predicate (a closure-only manifest '
                 'that declares commands; an analyzer whose tree has not exactly one parentless entry, or whose root '
                 'name differs from the manifest name; a reserved root name), an analyzer\'s own mounted root being '
                 'admitted; the remedy says "claim a project hook, a reserved or additional root command, or a probe". '
                 '(b) Item 25\'s request-class row: request-rejected 2, REQUEST.UNSATISFIABLE, PROVIDER.NOT_SELECTED, '
                 'subject excluded-form:<class>, no runId or executionId, with PUBLIC_ROUTE_REMEDIES["PROVIDER.NOT_SELECTED"] '
                 'widened, under NE\'s remedy-keying constraint, to stay true for the NOT-SELECTED cell and the three '
                 'request-class forms. Form: a complete successor copy of native-evidence.md, B-S9\'s form, being its '
                 'effective text under the product lock at ' + LOCK_REV + ' (every bound override applied) with exactly '
                 'those two hunks; and line-1159 overrides of B-S9\'s two native-model copies. The current selected '
                 'native-evidence contract becomes ' + COPY + '; the parent and every bound override\'s meaning on it '
                 'become historical, carried byte for byte except SD-5\'s row, and every later NE successor overrides the '
                 'copy. Existing codes only: no new public code, class, exit, D9 member, schema, WS, SL or product change. '
                 'The exact frozen candidate requires actual independent review and root assent.'),
    'parents': sorted([ne_pin, sd5_record_pin] + nem_parents, key=lambda r: r['path']),
    'passageOverrides': overrides,
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
    'independentReview': {'path': 'docs/implementation/m3/reviews/grok-sd-7-r1/review.json', 'bytes': None,
                          'sha256': None},
    'rootSubstantiveAssent': False,
    'requiredUnitFindings': [],
    'acceptedSuccessor': rpin,
    'rootAssessment': ('DRAFT. Completed by the lead after Grok\'s review: status ACCEPTED-DESIGN-UNIT, the review pin, '
                       'rootSubstantiveAssent true. SD-7 is M3-D r5\'s successor SD-7: SD-5\'s NE section 10 row conformed '
                       'to item 24\'s root-command predicate (LD-R4-1) and its remedy to "claim a project hook, a reserved '
                       'or additional root command, or a probe"; item 25\'s request-class row (LD-R4-2: request-rejected 2, '
                       'REQUEST.UNSATISFIABLE, PROVIDER.NOT_SELECTED, subject excluded-form:<class>); and the '
                       'PROVIDER.NOT_SELECTED remedy widened in B-S9\'s two model copies. Form: a complete successor copy '
                       'of native-evidence.md (its effective text at ' + LOCK_REV + ' with two hunks), which becomes the '
                       'selected NE, plus two line-1159 overrides. Bound in design-lock.json in a binding-only product '
                       'commit after acceptance; every later NE successor overrides the copy.'),
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
print(json.dumps({'mode': 'check' if CHECK else 'write', 'lockRev': LOCK_REV, 'neOverridesApplied': len(applied),
                  'neRecordsApplied': len({a['record']['path'] for a in applied}),
                  'effectiveParent': report['effectiveParent'], 'copy': report['copy'],
                  'copyLines': {'requestRow': request_row_line, 'conformedRow': conformed_row_line},
                  'remedyChars': len(REMEDY_NOT_SELECTED), 'successor': rpin, 'subject': spin}, indent=1))
