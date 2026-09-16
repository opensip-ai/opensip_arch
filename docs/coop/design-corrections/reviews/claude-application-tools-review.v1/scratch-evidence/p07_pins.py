"""P07: application_pins.prepare source-pin adaptation guard.

Allowed: exactly one added opening applicability paragraph naming D-372.
Refused: any inherited-body byte change, extra paragraphs, title change,
appended tail, accepted pin drift, unexpected changed pinned path.
All fixtures synthetic and disposable.
"""
import hashlib
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUTS = HERE.parent / 'inputs'
sys.path.insert(0, str(INPUTS))
import application_pins as A  # noqa: E402

sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
BODY = '# Chapter title\n\nInherited normative body paragraph one.\n\nParagraph two.\n'
ADD = 'Applicability: D-372 applies this chapter to the complete intended product contracts.'
rows = []


def build(base, *, mutate_after=None, pin_drift=False, extra_changed=False):
    base = Path(base)
    snap, files = base / 'snapshot', base / 'files'
    for rel in sorted(A.DOCS):
        p = snap / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(BODY)
        q = files / rel
        q.parent.mkdir(parents=True, exist_ok=True)
        first, tail = BODY.split('\n', 1)
        q.write_text(first + '\n\n' + ADD + '\n' + tail)
    extra_rel = A.DC + 'some-other-pinned-source.md'
    (snap / extra_rel).parent.mkdir(parents=True, exist_ok=True)
    (snap / extra_rel).write_text('unchanged pinned source\n')
    if extra_changed:
        (files / extra_rel).parent.mkdir(parents=True, exist_ok=True)
        (files / extra_rel).write_text('SEMANTIC DRIFT in a pinned source\n')
    if mutate_after:
        for rel in sorted(A.DOCS):
            (files / rel).write_text(mutate_after((files / rel).read_text()))

    def rowset(paths):
        return [{'path': r, 'sha256': sha(snap / r)} for r in paths]

    for bp in A.BASE_PINS:
        p = snap / bp
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({'files': rowset(sorted(A.DOCS) + [extra_rel])}, indent=2) + '\n')
    cur = snap / A.CURRENT_PIN
    cur.parent.mkdir(parents=True, exist_ok=True)
    cur.write_text(json.dumps(
        {'pins': rowset(sorted(A.DOCS) + list(A.BASE_PINS) + [extra_rel])}, indent=2) + '\n')
    if pin_drift:
        (snap / sorted(A.DOCS)[0]).write_text(BODY + 'drifted after pinning\n')
    return snap, files


def case(ident, expect, **kw):
    with tempfile.TemporaryDirectory(prefix='opensip-pins-') as td:
        snap, files = build(td, **kw)
        try:
            delta = A.prepare(snap, files)
            ok, detail = True, json.dumps({'sourceChanges': len(delta['sourceChanges']),
                                           'pinManifests': len(delta['pinManifests']),
                                           'intersections': len(delta['intersections']),
                                           'schemaChanges': delta['productContractModelSchemaChanges']})
            bodies_preserved = all(
                (files / c['path']).read_text().endswith(BODY.split('\n', 1)[1])
                for c in delta['sourceChanges'])
            detail += ' inheritedBodyPreserved=' + str(bodies_preserved)
        except Exception as e:  # noqa: BLE001
            ok, detail = False, f'{type(e).__name__}: {e}'[:150]
        rows.append({'id': ident, 'expected': expect,
                     'observed': 'ADMIT' if ok else 'REFUSE',
                     'asExpected': ok is (expect == 'ADMIT'), 'detail': detail})


case('control-single-opening-applicability-paragraph', 'ADMIT')
case('inherited-body-byte-changed', 'REFUSE',
     mutate_after=lambda t: t.replace('normative body paragraph one', 'ALTERED body'))
case('two-added-paragraphs', 'REFUSE',
     mutate_after=lambda t: t.replace(ADD, ADD + '\n\nA second smuggled paragraph.'))
case('title-line-changed', 'REFUSE',
     mutate_after=lambda t: t.replace('# Chapter title', '# Retitled chapter'))
case('text-appended-after-inherited-body', 'REFUSE', mutate_after=lambda t: t + '\nappended tail\n')
case('addition-omits-D-372', 'REFUSE', mutate_after=lambda t: t.replace('D-372', 'D-999'))
case('accepted-pin-drift-in-snapshot', 'REFUSE', pin_drift=True)
case('unexpected-extra-changed-pinned-path', 'REFUSE', extra_changed=True)

failed = [r['id'] for r in rows if not r['asExpected']]
print(json.dumps({'probe': 'P07-pins', 'cases': len(rows),
                  'asExpected': len(rows) - len(failed), 'unexpected': failed}, indent=2))
(HERE / 'p07_pins.result.json').write_text(json.dumps(rows, indent=2) + '\n')
for r in rows:
    print(('ok  ' if r['asExpected'] else 'DIFF'), r['id'], '->', r['observed'], '|', r['detail'])
