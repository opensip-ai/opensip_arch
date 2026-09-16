"""Independently reproduce root's counterexamples against the completed v1 selectors.

Reads the v1 patterns from the v1 scratch tree (unchanged) rather than restating them.
"""
import json
import re
import sys

V1 = '/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch/src25'
SCHEMA = V1 + '/docs/coop/design-corrections/native/native-evidence.schemas.v2.json'
ROOTCX = '/private/tmp/opensip-design-corrections/claude-root-binding-correction.v2/root-counterexamples.json'

defs = json.loads(open(SCHEMA, encoding='utf-8').read())['$defs']
DIR_P = defs['CanonicalRelativeDirV1']['pattern']
ROOT_P = defs['InternalUnitRootV1']['pattern']
CANON_P = defs['CanonicalPath']['pattern']
print('v1 CanonicalRelativeDirV1:', DIR_P)
print('v1 InternalUnitRootV1    :', ROOT_P)
print()

rd = re.compile(DIR_P)
rr = re.compile(ROOT_P)


def true_dot_segment(value):
    """The STATED law, decided by splitting on '/' -- not by regex dot/$ behaviour."""
    return any(seg in ('.', '..') for seg in value.split('/'))


rows = json.loads(open(ROOTCX, encoding='utf-8').read())['rows']
allok = True
out = []
print('%-14s %-10s %-10s %-12s %-10s %s' % (
    'value', 'rootRE', 'rootClaim', 'trueDotSeg', 'claimDot', 'verdict'))
for r in rows:
    v = r['value']
    got = bool(rr.search(v))
    dot = true_dot_segment(v)
    ok = (got == r['rootPatternAccepts']) and (dot == r['containsDotSegment'])
    allok = allok and ok
    out.append({'value': v, 'segments': v.split('/'), 'v1RootAccepts': got,
                'v1DirAccepts': bool(rd.search(v)), 'trueDotSegment': dot,
                'rootClaimedAccepts': r['rootPatternAccepts'],
                'rootClaimedDotSegment': r['containsDotSegment'],
                'reproduced': ok,
                'defect': ('ACCEPTS-FORBIDDEN-SEGMENT' if (got and dot)
                           else 'REJECTS-LAWFUL-SEGMENT' if (not got and not dot and v != '')
                           else None)})
    print('%-14s %-10s %-10s %-12s %-10s %s' % (
        repr(v), got, r['rootPatternAccepts'], dot, r['containsDotSegment'],
        'reproduced' if ok else 'MISMATCH'))

print()
print('all root observations reproduced exactly:', allok)
print()
print('defect classification under the STATED law (split on "/"):')
for o in out:
    if o['defect']:
        print('   %-14s segments=%-26s -> %s' % (repr(o['value']), o['segments'], o['defect']))

json.dump({'standing': 'Independent reproduction of root counterexamples against completed v1 selectors.',
           'v1Patterns': {'CanonicalRelativeDirV1': DIR_P, 'InternalUnitRootV1': ROOT_P,
                          'CanonicalPath': CANON_P},
           'allReproduced': allok, 'rows': out},
          open(sys.argv[1], 'w'), indent=1)
