"""READ-ONLY diagnostic (generation 22): shapes behind the claimed-positive audit refusals and a
summary of the measured read graph. Writes nothing."""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'


def J(rel):
    return json.load(open(OUT + '/' + rel))


def main():
    cap = J('vectors/capability-manifest-admission.json')['R-CAP-NAMED-GATES']
    print('CAP gateOrder', cap['gateOrder'])
    for i, n in enumerate(cap['negatives']):
        if 'firstRefusal' not in n or not any(k in n for k in ('masksLater', 'violationsInOrder', 'orderedRefusalChecks')):
            print(' cap neg', i, sorted(n), json.dumps(n)[:500])
    cve = J('vectors/cve1-eight-types.json')
    print('CVE1 negative keys', [sorted(n) for n in cve['negatives']][:3])
    print(' ', json.dumps(cve['negatives'][0])[:400])
    p1 = J('vectors/phase1-canonical-h-lexical.json')['R-LEXICAL-ADMISSION+R-RAW-VS-PARSED']
    print('descriptorByteCap', json.dumps(p1.get('descriptorByteCap'))[:600])
    print('phase1 raw keys', sorted(p1))
    import audit_claimed_positives as AU
    bad = AU._vector_walk(lambda n, _cls, covered: 'REFUSED_WITHOUT_FIRST_REFUSAL_OR_MASKING' if (
        n.get('refused') is True and not covered and (not n.get('firstRefusal') or not any(k in n for k in AU.MASKING_KEYS))) else None)
    by = collections.Counter(b.split(' ')[0] for b in bad)
    print('NEGATIVE-FIRST-REFUSAL bad rows by file', dict(by))
    seen = set()
    for b in bad:
        f = b.split(' ')[0]
        if f in seen:
            continue
        seen.add(f)
        path = b.split(' ')[1]
        node = J(f)
        for part in path.replace('[', '.[').split('.')[1:]:
            node = node[int(part[1:-1])] if part.startswith('[') else node[part]
        print(' ', b, '\n    keys', sorted(node), '\n    ', json.dumps(node)[:300])
    unc = AU._vector_walk(lambda n, cls, _c: 'UNCLASSIFIED' if any(k in n for k in ('refused', 'firstRefusal')) and not (
        isinstance(cls, str) and any(w in cls for w in ('valid', 'invalid', 'explanatory', 'measured'))) else None)
    print('UNCLASSIFIED', unc)
    rg = J('notes/v22-read-graph.json')
    print('READ GRAPH ORDER by (reader, laterWriter):',
          dict(collections.Counter((x['reader'], x['laterWriter']) for x in rg['orderViolations'])))
    for x in rg['orderViolations']:
        if not x['artifact'].startswith('checkpoints/'):
            print('  order', x)
    print('UNDECLARED'); [print('  ', x) for x in rg['undeclaredEdges']]
    print('UNKNOWN by (reader, top):', dict(collections.Counter(
        (x['reader'], x['artifact'].split('/')[0]) for x in rg['readsOfArtifactsNoStageWrote'])))
    for x in rg['readsOfArtifactsNoStageWrote']:
        if not x['artifact'].startswith(('lib.before-image', 'predecessors.v20')):
            print('  unknown', x['reader'], x['artifact'])
    print('ONESHOT', rg['oneShotRetainedNotesRead'][:20])


main()
