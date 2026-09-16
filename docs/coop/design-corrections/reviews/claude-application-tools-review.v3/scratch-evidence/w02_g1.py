"""W02: G1 - vendor-scoped private-name selection, plus an existence check of the one
external unpinned path the retain suite reads. Existence only; no contents read.
"""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUTS = HERE.parent / 'inputs'
sys.path.insert(0, str(INPUTS))
import retain_public as P  # noqa: E402

out = {'matrix': [], 'vendorGuard': [], 'external': {}}


def case(rel, stdout_name, vendor, expected, note):
    got = P.grok_source_is_private(rel, stdout_name, vendor)
    out['matrix'].append({'rel': rel, 'stdoutName': stdout_name, 'vendor': vendor,
                          'expectedPrivate': expected, 'observedPrivate': got,
                          'asExpected': got == expected, 'note': note})


# The two names G1 exempts for Claude only.
for v, exp in (('grok', True), ('claude', False)):
    case('summary.json', 'response.raw.json', v, exp, 'G1 exempt name')
    case('plan.json', 'response.raw.json', v, exp, 'G1 exempt name')

# Every other conservative private name must remain excluded for BOTH vendors.
OTHERS = sorted(P.GROK_PRIVATE_BASENAMES - {'summary.json', 'plan.json'})
for name in OTHERS:
    for v in ('grok', 'claude'):
        case(name, 'response.raw.json', v, True, 'conservative private name retained')

# Private directories at ANY component remain unconditional for both vendors.
for rel in ('compaction/x.json', 'work/compaction/note.txt', 'a/b/terminal/x.txt',
            'terminal/out.txt', 'deep/nest/compaction_checkpoints/c.json'):
    for v in ('grok', 'claude'):
        case(rel, 'response.raw.json', v, True, 'private dir at any component')

# Raw stdout basename remains unconditional - the Claude exemption must NOT defeat it.
case('summary.json', 'summary.json', 'claude', True, 'stdout basename beats G1 exemption')
case('plan.json', 'plan.json', 'claude', True, 'stdout basename beats G1 exemption')
case('nested/response.json', 'response.json', 'claude', True, 'nested stdout basename')
case('response.json', 'response.json', 'claude', True, 'claude default stdout')

# Authored outputs that must stay retained for both vendors.
for rel in ('review.json', 'review.md', 'probes/probe.json', 'work/probe.py', 'scratch/x.txt'):
    for v in ('grok', 'claude'):
        case(rel, 'response.raw.json', v, False, 'authored output retained')

# Helper contract: vendor is optional and defaults to grok; invalid vendor refuses.
two_arg = P.grok_source_is_private('summary.json', 'response.raw.json')
out['vendorGuard'].append({'id': 'default-arg-is-grok-behaviour', 'passed': two_arg is True,
                           'detail': f'2-arg call -> {two_arg}'})
for bad in ('claude ', 'CLAUDE', '', None, 'openai'):
    try:
        P.grok_source_is_private('summary.json', 'response.raw.json', bad)
        out['vendorGuard'].append({'id': f'invalid-vendor-{bad!r}-refuses', 'passed': False,
                                   'detail': 'accepted'})
    except AssertionError:
        out['vendorGuard'].append({'id': f'invalid-vendor-{bad!r}-refuses', 'passed': True,
                                   'detail': 'AssertionError'})

# Both retainer callsites must pass vendor through.
retain_src = (INPUTS / 'retain-application-review.successor.v1.py').read_text()
calls = [l.strip() for l in retain_src.splitlines() if 'grok_source_is_private' in l]
out['callsites'] = {'lines': calls,
                    'allPassVendor': all('vendor' in c for c in calls),
                    'count': len(calls)}

# Existence-only check of the one external absolute path the retain suite reads
# (check-retain-public.v1.py:608-611). Not in the manifest, not hash-pinned.
EXT = ('/tmp/opensip-design-corrections/grok-application-successor-preparation.v2/'
       'prepared/retain-application-review.successor.v1.py')
out['external'] = {'path': EXT, 'exists': os.path.exists(EXT),
                   'isFile': os.path.isfile(EXT),
                   'inV3Manifest': EXT in json.dumps(
                       json.load(open(HERE.parent / 'input-manifest.json')))}

bad = [r for r in out['matrix'] if not r['asExpected']]
badv = [r for r in out['vendorGuard'] if not r['passed']]
(HERE / 'w02_g1.result.json').write_text(json.dumps(out, indent=2) + '\n')
print('matrix cases:', len(out['matrix']), '| as expected:', len(out['matrix']) - len(bad))
for r in bad:
    print('  DIFF', r)
print('vendor guard:', len(out['vendorGuard']), '| passed:', len(out['vendorGuard']) - len(badv))
for r in badv:
    print('  DIFF', r)
print('callsites:', json.dumps(out['callsites'], indent=2))
print('external unpinned dependency:', json.dumps(out['external'], indent=2))
