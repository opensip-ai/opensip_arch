"""Area 1, the three programEntry provenances: DEFAULT, EXPLICIT and SYNTHESIZED.

The Run-level instrument (indep_enumeration_binding.py) measures the default and explicit
provenances on the five exported positives: the TypeScript Run carries a default-unit binding with
`programEntry: null` (the V18-D3 correction) and an explicit extra program naming an inventoried
`tsconfig.json`. No positive Run carries a `js-synthesized` CELL, so the SYNTHESIZED provenance is
measured here at the LAW level over synthetic EnumerationPlanV1 / TypeScriptConfigGraphV1
parameters. That is stated plainly: these are law-branch measurements over synthetic parameters,
not Runs and not admitted records.

The clause, quoted in full, is the only authority used:

  enumeration-plan.schema.v1.json #/$defs/AvailableProgramBindingV1/properties/programEntry --
  "TS/JS extra program: non-null LogicalPath of the selected inventoried config (snapshot member).
   U-1 default uses null; admission derives the actual U-1 marker/synthesized entry and compares
   it to retained TypeScriptConfigGraphV1.entryConfigPath (the graph entry need not be null).
   Rust extra programs are distinct universe H values (cfg/features/ownership); programEntry is
   not a complete program key. Resolved-input H remains authority."

and native-evidence.md section 1.4 U-1 for the marker precedence
(tsconfig.json > jsconfig.json > package.json; Cargo.toml yields a rust unit).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_schema as S

OUT = '/tmp/opensip-design-corrections/consumer-b.v19/output'

MARKER_PRECEDENCE = ['tsconfig.json', 'jsconfig.json', 'package.json']
MODE_OF_MARKER = {'tsconfig.json': 'ts-tsconfig', 'jsconfig.json': 'js-allowjs',
                  'package.json': 'js-synthesized'}


def u1_marker(paths):
    """U-1, for the ENTRY program: the marker that the retained TypeScriptConfigGraphV1 names as
    its `entryConfigPath`, which is the ROOT-most marker under the published precedence. U-1's
    "deepest unit" rule assigns a FILE to a unit (U-3); it does not make a nested config the
    entry of the graph, so depth is ordered root-first here and the precedence
    tsconfig.json > jsconfig.json > package.json breaks a tie within one directory."""
    hits = [p for p in paths if p.rsplit('/', 1)[-1] in MARKER_PRECEDENCE]
    if not hits:
        return None
    return sorted(hits, key=lambda p: (p.count('/'),
                                       MARKER_PRECEDENCE.index(p.rsplit('/', 1)[-1]),
                                       p.encode()))[0]


def derived_entry(paths):
    """The "actual U-1 marker/synthesized entry": the marker itself for a configured program, and
    for a SYNTHESIZED program the marker that caused the synthesis -- there is no config file to
    name, so the entry is the package manifest the synthesizer keyed on."""
    m = u1_marker(paths)
    return m, (MODE_OF_MARKER.get(m.rsplit('/', 1)[-1]) if m else None)


def judge(binding, paths, config_graph):
    """Returns the ordered refusals for ONE binding under the clause above."""
    ref = []
    prov = binding['provenance']
    entry = binding['programEntry']
    marker, mode = derived_entry(paths)
    if prov == 'default-unit':
        if entry is not None:
            ref.append({'code': 'ENUMERATION_BINDING_PROGRAM_ENTRY:'
                                'U1_DEFAULT_USES_NULL',
                        'detail': {'programEntry': entry}})
    else:
        if entry is None:
            ref.append({'code': 'ENUMERATION_BINDING_PROGRAM_ENTRY:'
                                'EXTRA_PROGRAM_NAMES_THE_SELECTED_INVENTORIED_CONFIG',
                        'detail': 'an extra TS/JS program carries a non-null LogicalPath'})
        elif entry not in paths:
            ref.append({'code': 'ENUMERATION_BINDING_PROGRAM_ENTRY:'
                                'ENTRY_IS_A_SNAPSHOT_MEMBER',
                        'detail': {'programEntry': entry}})
    # the derived entry is compared to the RETAINED graph, in both provenances
    if config_graph is not None and config_graph.get('entryConfigPath') != marker:
        ref.append({'code': 'ENUMERATION_BINDING_PROGRAM_ENTRY:'
                            'DERIVED_U1_ENTRY_EQUALS_THE_RETAINED_CONFIG_GRAPH_ENTRY',
                    'detail': {'derivedMarker': marker,
                               'graphEntryConfigPath': config_graph.get('entryConfigPath')}})
    return ref, {'derivedMarker': marker, 'derivedMode': mode}


CASES = [
    ('default-unit-binding-carries-a-null-programEntry', 'valid',
     {'provenance': 'default-unit', 'programEntry': None},
     ['package.json', 'src/a.js'], {'entryConfigPath': 'package.json'}, None),
    ('default-unit-binding-naming-a-program-entry', 'invalid',
     {'provenance': 'default-unit', 'programEntry': 'package.json'},
     ['package.json', 'src/a.js'], {'entryConfigPath': 'package.json'},
     'U1_DEFAULT_USES_NULL'),
    ('explicit-extra-program-names-the-inventoried-config', 'valid',
     {'provenance': 'explicit-plan-selection', 'programEntry': 'packages/x/tsconfig.json'},
     ['tsconfig.json', 'packages/x/tsconfig.json', 'src/a.ts'],
     {'entryConfigPath': 'tsconfig.json'}, None),
    ('explicit-extra-program-with-a-null-programEntry', 'invalid',
     {'provenance': 'explicit-plan-selection', 'programEntry': None},
     ['tsconfig.json', 'src/a.ts'], {'entryConfigPath': 'tsconfig.json'},
     'EXTRA_PROGRAM_NAMES_THE_SELECTED_INVENTORIED_CONFIG'),
    ('explicit-extra-program-naming-a-path-outside-the-snapshot', 'invalid',
     {'provenance': 'explicit-plan-selection', 'programEntry': 'elsewhere/tsconfig.json'},
     ['tsconfig.json', 'src/a.ts'], {'entryConfigPath': 'tsconfig.json'},
     'ENTRY_IS_A_SNAPSHOT_MEMBER'),
    # the SYNTHESIZED provenance: no tsconfig and no jsconfig, so U-1 falls to package.json and
    # the program is js-synthesized. The derived entry is that marker, and the retained graph must
    # agree with it.
    ('synthesized-program-derived-entry-agrees-with-the-retained-config-graph', 'valid',
     {'provenance': 'default-unit', 'programEntry': None},
     ['package.json', 'src/a.js', 'src/b.mjs'], {'entryConfigPath': 'package.json'}, None),
    ('synthesized-program-whose-graph-entry-disagrees-with-the-derived-marker', 'invalid',
     {'provenance': 'default-unit', 'programEntry': None},
     ['package.json', 'src/a.js'], {'entryConfigPath': 'tsconfig.json'},
     'DERIVED_U1_ENTRY_EQUALS_THE_RETAINED_CONFIG_GRAPH_ENTRY'),
    ('synthesized-program-with-a-tsconfig-present-is-not-synthesized-at-all', 'valid',
     {'provenance': 'default-unit', 'programEntry': None},
     ['tsconfig.json', 'package.json', 'src/a.ts'], {'entryConfigPath': 'tsconfig.json'}, None),
]


def main():
    rows, bad = [], []
    for label, cls, binding, paths, graph, expect in CASES:
        ref, info = judge(binding, paths, graph)
        admitted = not ref
        row = {'case': label, 'classification': cls, 'binding': binding,
               'snapshotPaths': paths, 'retainedConfigGraph': graph,
               'derived': info, 'refusals': ref, 'admitted': admitted,
               'expectedOwnerJoin': expect,
               'firstRefusal': ref[0] if ref else None}
        if expect:
            row['firstRefusalIsTheIntendedJoin'] = expect in json.dumps(ref[0] if ref else {})
        rows.append(row)
        ok = admitted == (cls == 'valid') and (cls == 'valid'
                                               or row.get('firstRefusalIsTheIntendedJoin'))
        if not ok:
            bad.append(label)
        print('%-62s %-8s admitted=%-5s derived=%-14s first=%s'
              % (label[:62], cls, admitted, info['derivedMode'],
                 (ref[0]['code'].split(':')[-1] if ref else '')))
    doc = {'standing': __doc__, 'clause': (
        'enumeration-plan.schema.v1.json #/$defs/AvailableProgramBindingV1/properties/'
        'programEntry + native-evidence.md section 1.4 U-1 marker precedence'),
        'provenancesMeasuredHere': ['default-unit', 'explicit-plan-selection',
                                    'synthesized (js-synthesized via the package.json marker)'],
        'provenancesAlsoMeasuredOnRealRuns': {
            'default-unit': 'typescript, rust, rust-partial, syntax-code, syntax-data',
            'explicit-plan-selection': 'typescript (packages/x/tsconfig.json extra program)',
            'synthesized': ('NOT exercised by any positive Run -- no Run declares a '
                            'js-synthesized CELL -- which is why it is measured here and '
                            'recorded as a law-branch measurement rather than a Run result')},
        'cases': rows}
    with open(OUT + '/vectors/program-entry-law.json', 'w') as f:
        json.dump(doc, f, indent=1)
    print('\ncases %d, failures %s' % (len(rows), bad))
    assert not bad, bad


main()
