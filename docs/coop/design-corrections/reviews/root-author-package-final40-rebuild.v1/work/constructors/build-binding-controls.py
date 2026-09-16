"""F-05 / F-06 program-binding controls, reminted from scratch on the declared source.

PORTABLE. Declared inputs only (--source/--package/--out, optional --helpers/--kit).

Each variant is a COMPLETE fresh construction: the binding value is set before the graph is
minted, so every downstream identity is derived, never search/replaced in a serialized store.

  ts-lawful-default              provenance=default-unit,           programEntry=null
  ts-invalid-default-entry       provenance=default-unit,           programEntry='tsconfig.json'  (F-05)
  ts-lawful-explicit-selection   provenance=explicit-plan-selection, programEntry='tsconfig.json' (F-06)

F-05 must reach structural ADMIT and then the semantic enumeration boundary
ENUMERATION_BINDING_PROGRAM_ENTRY: enumeration_model admits a non-null programEntry only when
the binding's provenance is not `default-unit`.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import author_portable as AP

_a = AP.arguments(__doc__.splitlines()[0])
SOURCE = _a.source
PACKAGE = _a.package
OUTROOT = AP.fresh_out(_a.out)
AP.load_helpers(PACKAGE, _a.helpers, kit=_a.kit, out=OUTROOT)

VARIANTS = [('ts-lawful-default', None, 'default-unit'),
            ('ts-invalid-default-entry', 'tsconfig.json', 'default-unit'),
            ('ts-lawful-explicit-selection', 'tsconfig.json', 'explicit-plan-selection')]


def build(tag, entry, provenance):
    for m in list(sys.modules):
        if m == 'helpers' or m.startswith('helpers.'):
            del sys.modules[m]
    AP.load_helpers(PACKAGE, _a.helpers, kit=_a.kit, out=OUTROOT)
    from helpers import ts_pilot
    name = '_default_unit_binding' if hasattr(ts_pilot, '_default_unit_binding') else '_binding'
    original = getattr(ts_pilot, name)

    def patched(*args, **kw):
        b = original(*args, **kw)
        b['programEntry'] = entry
        b['provenance'] = provenance
        return b

    setattr(ts_pilot, name, patched)
    g = ts_pilot.build_ts_run()
    export = g['store'].export()
    (OUTROOT / (tag + '.store.json')).write_text(json.dumps(export, indent=2, sort_keys=True) + '\n')
    return {'name': tag, 'path': tag + '.store.json', 'runId': g['runId'],
            'programEntry': entry, 'provenance': provenance,
            'objects': len(export['objectTable']), 'patchedHelper': name}


rows = [build(*v) for v in VARIANTS]
(OUTROOT / 'claims.json').write_text(
    json.dumps([{'name': r['name'], 'path': r['path'], 'runId': r['runId']} for r in rows],
               indent=2) + '\n')
(OUTROOT / 'variants.json').write_text(json.dumps(
    {'standing': 'AUTHOR binding controls; freshly minted, no serialized-id substitution.',
     'distinctRunIds': len({r['runId'] for r in rows}) == len(rows), 'variants': rows},
    indent=2) + '\n')
for r in rows:
    print('%-30s %-72s objects=%s' % (r['name'], r['runId'], r['objects']))
print('distinct runIds:', len({r['runId'] for r in rows}) == len(rows))
AP.write_provenance(_a)
