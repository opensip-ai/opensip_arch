"""Run the I1-L discriminating cases (UNITS.md r2: the corpus projects and cases 1 to 19) on the
reference model, and check every expectation.

Each case also checks two invariants of item 2.9: the result bytes do not depend on input
encounter order (five seeded permutations), and an independent SCC algorithm gives the same bytes.

Run with the pinned interpreter and the offline jsonschema wheels the design encoder imports:
    python3.14 -I -B evidence/check_cycle_representative.py --deps DIR [--write]
--write rewrites evidence/cases-report.json; otherwise the report is compared byte for byte.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCH = HERE.parents[5]
LAW = ARCH / 'docs/implementation/m3/preview-pack-i1/PROPOSAL-r2.md'
LAW_SHA256 = '1eb47d1e292660b15cb0016a280899a384364f2c3d99ab61d18f12b133eba2c7'
REPORT = HERE / 'cases-report.json'
U1, U2 = 'ts-program-1', 'ts-program-2'


def pack_rule():
    """The one rule of law item 5.2, read from the accepted law bytes."""
    raw = LAW.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == LAW_SHA256, 'law bytes changed'
    text = raw.decode('utf-8')
    start = text.index('**5.2 The bundled document.**')
    block = text[text.index('```\n', start) + 4:]
    document = json.loads(block[:block.index('\n```')])
    assert len(document['rules']) == 1
    return document['rules'][0]


class Project:
    """A synthetic admitted project: one imports cell per universe, complete by default."""

    def __init__(self, M, files, universe=U1):
        self.M = M
        self.n = 0
        self.inputs = {'selected': [], 'enumeration': {'state': 'complete', 'causes': []},
                       'bindings': [], 'inventories': {}, 'facts': [], 'scopes': {},
                       'coverages': {}, 'waivers': []}
        self.universe(universe, files)

    def sym(self, universe, path):
        return f'{universe}#{path}#module'

    def universe(self, universe, files, select=True):
        inv = f'inventory:{universe}:imports'
        self.inputs['inventories'][inv] = {
            'kind': 'symbol', 'universe': universe, 'state': 'complete',
            'rows': [{'nativeSubjectId': self.sym(universe, p), 'path': p} for p in files]}
        self.inputs['bindings'].append({'universe': universe, 'providerClosure': 'closure2:ts',
                                        'family': 'typescript', 'inventories': [inv], 'required': True})
        if select:
            self.inputs['selected'] += [{'universe': universe, 'path': p, 'language': 'typescript'}
                                        for p in files]
        self.scope(universe, [self.sym(universe, p) for p in files])
        return self

    def mint(self, domain, prefix, body):
        self.n += 1
        return prefix + self.M.ident(domain, {**body, 'serial': self.n})

    def scope(self, universe, subjects, target=None, coverage=True):
        sid = self.mint('subject-scope', 'scope2:', {'u': universe, 's': subjects})
        self.inputs['scopes'][sid] = {'relation': 'imports', 'resolution': 'resolved-target',
                                      'sourceUniverse': universe, 'targetUniverse': target or universe,
                                      'subjects': list(subjects)}
        if coverage:
            self.cover(sid)
        return sid

    def cover(self, sid, satisfied=True, native_cause=None, deficiencies=()):
        scope = self.inputs['scopes'][sid]
        cid = self.mint('coverage', 'coverage2:', {'scope': sid})
        self.inputs['coverages'][cid] = {
            'scopeId': sid, 'relation': 'imports', 'resolution': 'resolved-target',
            'sourceUniverse': scope['sourceUniverse'], 'targetUniverse': scope['targetUniverse'],
            'sufficiency': {'requirement': dict(self.M.REQUIREMENT), 'satisfied': satisfied,
                            'nativeCause': native_cause, 'deficiencies': list(deficiencies)}}
        return cid

    def degrade(self, native_cause=None, deficiency='resolution-incomplete'):
        """RC-2: an unresolved, dynamic or unparsed import leaves every Coverage incomplete."""
        for cov in self.inputs['coverages'].values():
            cov['sufficiency'].update(satisfied=False, nativeCause=native_cause, deficiencies=[deficiency])
        return self

    def edge(self, a, b, universe=U1, target_universe=None, occupancy='first-party', kind='file',
             native=None, importer=None, resolution='resolved-target'):
        tu = target_universe or universe
        attribution = None if occupancy is None else {
            'occupancy': occupancy, 'kind': kind if occupancy == 'first-party' else None,
            'evaluationNativeId': (native if native is not None else b) if occupancy == 'first-party' else None}
        fid = self.mint('fact', 'fact2:', {'a': a, 'b': b})
        self.inputs['facts'].append({'id': fid, 'relation': 'imports', 'resolution': resolution,
                                     'sourceUniverse': universe,
                                     'importer': importer or self.sym(universe, a),
                                     'targetUniverse': tu, 'attribution': attribution})
        return fid

    def unresolved(self, a, universe=U1):
        fid = self.mint('fact', 'fact2:', {'unresolved': a})
        self.inputs['facts'].append({'id': fid, 'relation': 'unresolved-edge', 'payloadRelation': 'imports',
                                     'sourceUniverse': universe, 'referrer': self.sym(universe, a)})
        return fid

    def edges(self, *pairs):
        for a, b in pairs:
            self.edge(a, b)
        return self


def cases(M):
    """Yield (name, source, inputs, rule, expectation)."""
    rule = pack_rule()

    def p(files, *pairs):
        return Project(M, files).edges(*pairs)

    # The corpus (QCM:7-124; LQM:232's target).
    yield 'corpus-cycle', 'QCM cycle', p(['cycle/a.ts', 'cycle/b.ts'], ('cycle/a.ts', 'cycle/b.ts'),
                                         ('cycle/b.ts', 'cycle/a.ts')).inputs, rule, {
        'outcome': 'fail', 'findings': [('cycle/a.ts', ['cycle/a.ts', 'cycle/b.ts'], 2)]}
    yield 'corpus-self', 'QCM self', p(['self/self.ts'], ('self/self.ts', 'self/self.ts')).inputs, rule, {
        'outcome': 'fail', 'findings': [('self/self.ts', ['self/self.ts'], 1)]}
    for name, files, pairs in (('acyclic', ['acyclic/a.ts', 'acyclic/b.ts'], [('acyclic/a.ts', 'acyclic/b.ts')]),
                               ('empty', ['empty/a.ts'], []), ('shadow', ['shadow/a.ts'], [])):
        yield f'corpus-{name}', f'QCM {name}', p(files, *pairs).inputs, rule, {
            'outcome': 'pass', 'values': {f: 'false' for f in files}, 'noCauses': True}
    prj = p(['unresolved/a.ts'])
    prj.unresolved('unresolved/a.ts')
    yield 'corpus-unresolved', 'QCM unresolved', prj.degrade().inputs, rule, {
        'outcome': 'indeterminate', 'values': {'unresolved/a.ts': 'unknown'}, 'causes': {'coverage-unknown'},
        'uncertainAt': {'unresolved/a.ts': 1}}
    for name in ('malformed', 'dynamic'):
        yield f'corpus-{name}', f'QCM {name}', p([f'{name}/a.ts']).degrade().inputs, rule, {
            'outcome': 'indeterminate', 'values': {f'{name}/a.ts': 'unknown'}, 'causes': {'coverage-unknown'}}
    prj = Project(M, [])
    yield 'corpus-zero-subjects', 'S = 0 (item 2.8; COMP:26 complete-empty)', prj.inputs, rule, {
        'outcome': 'pass', 'findings': []}

    # UNITS cases 1 to 14.
    yield 'case-01-two-disjoint-cycles', 'UNITS 1', p(['a.ts', 'b.ts', 'c.ts', 'd.ts'],
        ('a.ts', 'b.ts'), ('b.ts', 'a.ts'), ('c.ts', 'd.ts'), ('d.ts', 'c.ts')).inputs, rule, {
        'outcome': 'fail', 'findings': [('a.ts', ['a.ts', 'b.ts'], 2), ('c.ts', ['c.ts', 'd.ts'], 2)]}
    yield 'case-02-three-file-scc-duplicate-edges', 'UNITS 2', p(['a.ts', 'b.ts', 'c.ts'],
        ('a.ts', 'b.ts'), ('a.ts', 'b.ts'), ('b.ts', 'c.ts'), ('c.ts', 'a.ts'), ('c.ts', 'a.ts')).inputs, rule, {
        'outcome': 'fail', 'findings': [('a.ts', ['a.ts', 'b.ts', 'c.ts'], 5)],
        'values': {'a.ts': 'true', 'b.ts': 'false', 'c.ts': 'false'}, 'matchingAt': {'b.ts': 1, 'c.ts': 2}}
    yield 'case-03a-uppercase-first', 'UNITS 3: B.ts precedes a.ts', p(['B.ts', 'a.ts'],
        ('a.ts', 'B.ts'), ('B.ts', 'a.ts')).inputs, rule, {
        'outcome': 'fail', 'findings': [('B.ts', ['B.ts', 'a.ts'], 2)]}
    yield 'case-03b-dot-before-slash', 'UNITS 3: a.ts precedes a/b.ts', p(['a/b.ts', 'a.ts'],
        ('a/b.ts', 'a.ts'), ('a.ts', 'a/b.ts')).inputs, rule, {
        'outcome': 'fail', 'findings': [('a.ts', ['a.ts', 'a/b.ts'], 2)]}
    prj = Project(M, ['x.ts']).universe(U2, ['x.ts'])
    prj.edge('x.ts', 'x.ts', universe=U2, target_universe=U1)
    prj.edge('x.ts', 'x.ts', universe=U1, target_universe=U2)
    yield 'case-03c-path-tie-universe', 'UNITS 3: a path tie is broken by the universe id', prj.inputs, rule, {
        'outcome': 'fail', 'findings': [('x.ts', ['x.ts', 'x.ts'], 2)], 'findingUniverse': U1,
        'valuesByVertex': {(U1, 'x.ts'): 'true', (U2, 'x.ts'): 'false'}}
    prj = p(['a.ts', 'b.ts'], ('a.ts', 'b.ts'))
    prj.edge('a.ts', 'node:fs', occupancy='external')
    yield 'case-04-external-target', 'UNITS 4', prj.inputs, rule, {
        'outcome': 'pass', 'values': {'a.ts': 'false', 'b.ts': 'false'}, 'noCauses': True}
    prj = p(['a.ts', 'b.ts'], ('a.ts', 'b.ts'))
    prj.edge('b.ts', 'opaque', occupancy='unknown')
    yield 'case-05-unknown-occupancy', 'UNITS 5', prj.inputs, rule, {
        'outcome': 'indeterminate', 'values': {'a.ts': 'unknown', 'b.ts': 'unknown'},
        'causes': {'target-kind-unknown'}, 'causeUniverse': {'target-kind-unknown': U1}, 'uncertainAt': {'b.ts': 1}}
    prj = p(['a.ts', 'b.ts'], ('a.ts', 'b.ts'))
    prj.edge('b.ts', 'workspace-pkg', kind='package')
    yield 'case-06-first-party-package', 'UNITS 6', prj.inputs, rule, {
        'outcome': 'indeterminate', 'values': {'a.ts': 'unknown', 'b.ts': 'unknown'},
        'causes': {'population-unknown'}}
    prj = p(['a.ts', 'b.ts', 'c.ts'], ('a.ts', 'b.ts'), ('b.ts', 'a.ts'))
    prj.unresolved('c.ts')
    yield 'case-07-known-cycle-unresolved-elsewhere', 'UNITS 7', prj.degrade().inputs, rule, {
        'outcome': 'fail', 'findings': [('a.ts', ['a.ts', 'b.ts'], 2)],
        'values': {'a.ts': 'true', 'b.ts': 'false', 'c.ts': 'unknown'}, 'causes': {'coverage-unknown'},
        'findingCauses': {'coverage-unknown'}}
    prj = p(['b.ts', 'c.ts', 'd.ts', 'e.ts'], ('b.ts', 'c.ts'), ('c.ts', 'b.ts'), ('d.ts', 'e.ts'), ('e.ts', 'd.ts'))
    prj.edge('c.ts', 'opaque-1', occupancy='unknown')
    prj.edge('e.ts', 'opaque-2', occupancy='unknown')
    yield 'case-08-components-unknown-edges-might-merge', 'UNITS 8', prj.inputs, rule, {
        'outcome': 'fail', 'findings': [('b.ts', ['b.ts', 'c.ts'], 2), ('d.ts', ['d.ts', 'e.ts'], 2)],
        'causes': {'target-kind-unknown'}}
    prj = Project(M, ['a.ts', 'b.ts', 'x.ts'])
    prj.inputs['selected'] = [s for s in prj.inputs['selected'] if s['path'] != 'x.ts']
    prj.edges(('a.ts', 'b.ts'), ('x.ts', 'a.ts'))
    yield 'case-09-edge-entering-from-unselected', 'UNITS 9', prj.inputs, rule, {
        'outcome': 'pass', 'values': {'a.ts': 'false', 'b.ts': 'false'}, 'noCauses': True}
    prj = p(['a.ts', 'b.ts', 'c.ts'], ('a.ts', 'b.ts'), ('b.ts', 'a.ts'))
    prj.inputs['inventories'][f'inventory:{U1}:imports']['rows'] += [
        {'nativeSubjectId': 'dup', 'path': 'a.ts'}, {'nativeSubjectId': 'dup', 'path': 'c.ts'}]
    for scope in prj.inputs['scopes'].values():
        scope['subjects'].append('dup')
    unplaced = prj.edge('?', 'c.ts', importer='dup')
    yield 'case-10-importer-without-unique-row', 'UNITS 10', prj.inputs, rule, {
        'outcome': 'fail', 'findings': [('a.ts', ['a.ts', 'b.ts'], 2)],
        'values': {'a.ts': 'true', 'b.ts': 'false', 'c.ts': 'unknown'}, 'causes': {'population-unknown'},
        'unplacedIn': {'c.ts': True, 'a.ts': False, 'b.ts': False}, 'unplacedFact': unplaced}
    prj = p(['a.ts', 'b.ts', 'c.ts'], ('a.ts', 'b.ts'))
    prj.inputs['inventories'][f'inventory:{U1}:imports']['rows'] += [
        {'nativeSubjectId': 'dup', 'path': 'a.ts'}, {'nativeSubjectId': 'dup', 'path': 'c.ts'}]
    for scope in prj.inputs['scopes'].values():
        scope['subjects'].append('dup')
    unplaced = prj.edge('?', 'c.ts', importer='dup')
    yield 'case-10b-importer-without-unique-row-acyclic', 'UNITS 10, no known cycle', prj.inputs, rule, {
        'outcome': 'indeterminate', 'values': {'a.ts': 'unknown', 'b.ts': 'unknown', 'c.ts': 'unknown'},
        'causes': {'population-unknown'}, 'unplacedIn': {'a.ts': True, 'b.ts': True, 'c.ts': True},
        'unplacedFact': unplaced}
    prj = p(['a.ts', 'b.ts'], ('a.ts', 'b.ts'))
    prj.inputs['bindings'] = []
    yield 'case-11-no-imports-binding', 'UNITS 11 (DR-G25 path)', prj.inputs, rule, {
        'outcome': 'indeterminate', 'values': {'a.ts': 'unknown', 'b.ts': 'unknown'},
        'causes': {'missing-relation-coverage'}, 'exactCauses': True}
    prj = p(['w/a.ts', 'w/b.ts'], ('w/a.ts', 'w/b.ts'), ('w/b.ts', 'w/a.ts'))
    prj.inputs['waivers'] = [{'ruleId': 'module-import-cycle', 'subjectPath': 'w/a.ts'}]
    yield 'case-12a-waiver-matches-representative', 'UNITS 12', prj.inputs, rule, {
        'outcome': 'pass', 'findings': [('w/a.ts', ['w/a.ts', 'w/b.ts'], 2)], 'waived': [True]}
    prj = p(['w/0.ts', 'w/a.ts', 'w/b.ts'], ('w/a.ts', 'w/b.ts'), ('w/b.ts', 'w/0.ts'), ('w/0.ts', 'w/a.ts'))
    prj.inputs['waivers'] = [{'ruleId': 'module-import-cycle', 'subjectPath': 'w/a.ts'}]
    yield 'case-12b-smaller-member-moves-representative', 'UNITS 12, a later Run', prj.inputs, rule, {
        'outcome': 'fail', 'findings': [('w/0.ts', ['w/0.ts', 'w/a.ts', 'w/b.ts'], 3)], 'waived': [False]}
    chain = [f'm{i:03d}.ts' for i in range(1000)]
    yield 'case-14-linear-chain-1000', 'UNITS 14 (QCM:127-131)', p(
        chain, *zip(chain, chain[1:])).inputs, rule, {
        'outcome': 'pass', 'findings': [], 'noCauses': True, 'oneGraph': True, 'summaryOnly': True}

    # UNITS r2 cases 15 to 19.
    for required in (True, False):
        prj = Project(M, ['A.ts', 'B.ts'])
        prj.inputs['bindings'][0]['required'] = required
        prj.inputs['scopes'].clear(); prj.inputs['coverages'].clear()
        prj.scope(U1, [prj.sym(U1, 'A.ts')])
        yield f'case-15-subset-partition-required-{str(required).lower()}', 'UNITS 15 (CODEX2 I1-RF-1)', \
            prj.inputs, rule, {'outcome': 'indeterminate', 'values': {'A.ts': 'unknown', 'B.ts': 'unknown'},
                               'causes': {'uncovered-expected-source-subject'}, 'exactCauses': True,
                               'causeUniverse': {'uncovered-expected-source-subject': U1}}
    prj = Project(M, ['A.ts', 'B.ts'])
    inv = prj.inputs['inventories'][f'inventory:{U1}:imports']
    inv['state'], inv['rows'] = 'partial', inv['rows'][:1]
    yield 'case-16a-partial-census-known-rows-covered', 'UNITS 16', prj.inputs, rule, {
        'outcome': 'indeterminate', 'causes': {'population-unknown'}, 'exactCauses': True}
    prj = Project(M, ['A.ts', 'B.ts'])
    inv = prj.inputs['inventories'][f'inventory:{U1}:imports']
    inv['state'], inv['rows'] = 'partial', inv['rows'][:1]
    for scope in prj.inputs['scopes'].values():
        scope['subjects'] = []
    yield 'case-16b-partial-census-known-row-uncovered', 'UNITS 16: known rows are still checked', \
        prj.inputs, rule, {'outcome': 'indeterminate',
                           'causes': {'population-unknown', 'uncovered-expected-source-subject'},
                           'exactCauses': True}
    prj = Project(M, ['A.ts', 'B.ts', 'C.ts', 'D.ts'])
    prj.inputs['scopes'].clear(); prj.inputs['coverages'].clear()
    prj.scope(U1, [prj.sym(U1, 'A.ts'), prj.sym(U1, 'B.ts')])
    prj.scope(U1, [prj.sym(U1, 'C.ts'), prj.sym(U1, 'D.ts')])
    prj.edges(('A.ts', 'B.ts'), ('C.ts', 'D.ts'), ('B.ts', 'C.ts'))
    yield 'case-17-broad-partitions', 'UNITS 17', prj.inputs, rule, {
        'outcome': 'pass', 'noCauses': True, 'scopes': 2}
    prj = Project(M, ['a.ts'])
    prj.inputs['inventories'][f'inventory:{U1}:imports']['rows'] = []
    for scope in prj.inputs['scopes'].values():
        scope['subjects'] = []
    yield 'case-18a-complete-empty-census-explicit-empty-scope', 'UNITS 18', prj.inputs, rule, {
        'outcome': 'pass', 'values': {'a.ts': 'false'}, 'noCauses': True}
    prj = Project(M, ['a.ts'])
    prj.inputs['inventories'][f'inventory:{U1}:imports']['rows'] = []
    prj.inputs['scopes'].clear(); prj.inputs['coverages'].clear()
    yield 'case-18b-complete-empty-census-no-scope', 'UNITS 18: no scope at all', prj.inputs, rule, {
        'outcome': 'indeterminate', 'values': {'a.ts': 'unknown'},
        'causes': {'uncovered-expected-source-subject'}, 'exactCauses': True}
    prj = Project(M, ['a.ts', 'b.ts'])
    prj.inputs['selected'] = [s for s in prj.inputs['selected'] if s['path'] == 'a.ts']
    prj.inputs['enumeration'] = {'state': 'incomplete', 'causes': [
        {'source': 'enumeration', 'cause': 'incomplete-inventory'}]}
    yield 'case-19-population-only-partial-file-inventory', 'UNITS 19 (I1-RF-3; COMP:162)', prj.inputs, rule, {
        'outcome': 'indeterminate', 'values': {'a.ts': 'false'}, 'noCauses': True}

    # Discriminating checks beyond the UNITS list (precisions P1, P3, P4).
    prj = p(['a.ts', 'b.ts'], ('a.ts', 'b.ts'))
    prj.edge('b.ts', 'a.ts', resolution='syntactic-specifier')
    yield 'extra-syntactic-specifier-never-an-edge', 'item 2.3 facts read (PAC:129-132)', prj.inputs, rule, {
        'outcome': 'pass', 'noCauses': True}
    prj = p(['a.ts', 'b.ts'], ('a.ts', 'b.ts'))
    prj.edge('b.ts', prj.sym(U1, 'a.ts'), kind='symbol', native=prj.sym(U1, 'a.ts'))
    yield 'extra-first-party-symbol-target-closes-cycle', 'item 2.3 first-party symbol target', \
        prj.inputs, rule, {'outcome': 'fail', 'findings': [('a.ts', ['a.ts', 'b.ts'], 2)]}
    prj = p(['a.ts', 'b.ts'], ('a.ts', 'b.ts'))
    prj.edge('b.ts', 'nowhere', kind='symbol', native='no-such-symbol')
    yield 'extra-unmapped-symbol-target', 'item 2.3 (QP:84) and P1', prj.inputs, rule, {
        'outcome': 'indeterminate', 'causes': {'target-kind-unknown'}, 'exactCauses': True}
    prj = Project(M, ['a.ts', 'b.ts', 'x.ts'])
    prj.inputs['selected'] = [s for s in prj.inputs['selected'] if s['path'] != 'x.ts']
    prj.edges(('a.ts', 'b.ts'), ('b.ts', 'x.ts'))
    yield 'extra-edge-leaving-to-unselected-file', 'item 2.3 unplaceable endpoint', prj.inputs, rule, {
        'outcome': 'indeterminate', 'causes': {'population-unknown'}, 'exactCauses': True,
        'uncertainAt': {'b.ts': 1}}
    prj = p(['a.ts', 'b.ts'], ('a.ts', 'b.ts'), ('b.ts', 'a.ts'))
    prj.inputs['inventories']['inventory:copy'] = copy.deepcopy(prj.inputs['inventories'][f'inventory:{U1}:imports'])
    prj.inputs['inventories']['inventory:copy']['kind'] = 'symbol'
    yield 'extra-identical-rows-are-one-row', 'P3 (ATOM section 9: identical lookup not ambiguous)', \
        prj.inputs, rule, {'outcome': 'fail', 'findings': [('a.ts', ['a.ts', 'b.ts'], 2)], 'noCauses': True}
    prj = p(['a.ts', 'b.ts'], ('a.ts', 'b.ts'))
    prj.inputs['bindings'].append({'universe': None, 'providerClosure': 'closure2:rs', 'family': 'rust',
                                   'inventories': [], 'required': False})
    yield 'extra-foreign-family-unavailable-is-disclosure', 'shared prelude P1', prj.inputs, rule, {
        'outcome': 'pass', 'causes': {'cross-family-edge-not-owed'}, 'exactCauses': True}
    prj = Project(M, ['a.ts']).universe(U2, ['z.ts'])
    prj.inputs['bindings'] = [b for b in prj.inputs['bindings'] if b['universe'] == U1]
    prj.inputs['bindings'].append({'universe': None, 'providerClosure': 'closure2:ts2', 'family': 'typescript',
                                   'inventories': [], 'required': True})
    yield 'extra-second-universe-unbound', 'P2 (selector-unbound ends that universe only)', prj.inputs, rule, {
        'outcome': 'indeterminate', 'causes': {'selector-unbound'}, 'exactCauses': True}


def op_law_cases(M):
    rule = pack_rule()
    atom = rule['emitWhen']
    variants = {
        'nested-under-not': {**rule, 'emitWhen': {'op': 'not', 'operand': atom}},
        'filters-present': {**rule, 'emitWhen': {**atom, 'filters': [{'field': 'resolution', 'cmp': 'eq',
                                                                      'value': 'resolved-target'}]}},
        'endpoint-target': {**rule, 'emitWhen': {**atom, 'endpoint': 'target'}},
        'subject-kind-symbol': {**rule, 'subjectEnumeration': {**rule['subjectEnumeration'], 'subjectKind': 'symbol'}},
        'relation-references': {**rule, 'emitWhen': {**atom, 'relation': 'references'}},
    }
    out = {}
    for name, variant in variants.items():
        try:
            M.evaluate_rule(variant, Project(M, ['a.ts']).inputs)
        except M.OpLawRefusal as exc:
            out[name] = str(exc)
        else:
            raise AssertionError(f'op law admitted {name}')
    assert M.admit_rule(rule) == []
    return out


def shuffled(inputs, seed):
    rnd = random.Random(seed)
    out = copy.deepcopy(inputs)
    for key in ('selected', 'facts', 'bindings'):
        rnd.shuffle(out[key])
    for inv in out['inventories'].values():
        rnd.shuffle(inv['rows'])
    for key in ('inventories', 'scopes', 'coverages'):
        items = list(out[key].items()); rnd.shuffle(items); out[key] = dict(items)
    for scope in out['scopes'].values():
        rnd.shuffle(scope['subjects'])
    return out


def check(M, name, inputs, rule, expect, result):
    def fail(msg):
        raise AssertionError(f'{name}: {msg}')
    if result['outcome'] != expect['outcome']:
        fail(f"outcome {result['outcome']} != {expect['outcome']}")
    if 'findings' in expect:
        got = [(f['subjectPath'], f['members'], f['parameters']['parameters']['matchingFactCount'])
               for f in result['findings']]
        if got != [tuple(x) for x in expect['findings']]:
            fail(f'findings {got}')
    if 'findingUniverse' in expect and result['findings'][0]['universe'] != expect['findingUniverse']:
        fail('finding universe')
    if 'waived' in expect and [f['waived'] for f in result['findings']] != expect['waived']:
        fail('waived')
    values = {s['path']: s['value'] for s in result['subjects']}
    for path, value in expect.get('values', {}).items():
        if values.get(path) != value:
            fail(f'value at {path}: {values.get(path)}')
    by_vertex = {(s['universe'], s['path']): s['value'] for s in result['subjects']}
    for vertex, value in expect.get('valuesByVertex', {}).items():
        if by_vertex.get(vertex) != value:
            fail(f'value at {vertex}')
    codes = {c['code'] for s in result['subjects'] for c in s['causes']}
    if expect.get('noCauses') and codes:
        fail(f'unexpected causes {codes}')
    if 'causes' in expect:
        if not expect['causes'] <= codes or (expect.get('exactCauses') and codes != expect['causes']):
            fail(f'causes {codes}')
    for code, universe in expect.get('causeUniverse', {}).items():
        found = {c.get('universe') for s in result['subjects'] for c in s['causes'] if c['code'] == code}
        if found != {universe}:
            fail(f'{code} universe {found}')
    subjects = {s['path']: s for s in result['subjects']}
    for path, count in expect.get('uncertainAt', {}).items():
        if len(subjects[path]['uncertainFactIds']) != count:
            fail(f'uncertain at {path}')
    for path, count in expect.get('matchingAt', {}).items():
        if len(subjects[path]['matchingFactIds']) != count:
            fail(f'matching at {path}')
    for path, present in expect.get('unplacedIn', {}).items():
        if (expect['unplacedFact'] in subjects[path]['uncertainFactIds']) != present:
            fail(f'unplaced fact at {path}')
    if 'findingCauses' in expect:
        rep = subjects[result['findings'][0]['subjectPath']]
        if not expect['findingCauses'] <= {c['code'] for c in rep['causes']}:
            fail('finding witness lost a dominated cause (ATOM:415)')
    if 'scopes' in expect and len(result['subjects'][0]['scopeIds']) != expect['scopes']:
        fail('scope citations')
    for subject in result['subjects']:  # item 2.5: every indeterminate value carries a blocking cause
        if subject['value'] == 'unknown' and not [c for c in subject['causes'] if c['code'] not in M.DISCLOSURES]:
            fail('indeterminate without a blocking cause')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--deps', help='directory holding jsonschema 4.25.1 and its dependencies')
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    if args.deps:
        sys.path.insert(0, args.deps)
    sys.path.insert(0, str(HERE))
    import cycle_representative_model as M
    report = {'schemaVersion': 1, 'law': {'path': str(LAW.relative_to(ARCH)), 'sha256': LAW_SHA256},
              'model': {'path': 'docs/implementation/m3/preview-pack-i1/i1-l/evidence/cycle_representative_model.py',
                        'sha256': hashlib.sha256((HERE / 'cycle_representative_model.py').read_bytes()).hexdigest()},
              'encoder': {'path': str(M.ENCODER_PATH.relative_to(ARCH)),
                          'sha256': hashlib.sha256(M.ENCODER_PATH.read_bytes()).hexdigest()},
              'cases': []}
    for name, source, inputs, rule, expect in cases(M):
        M.Graph.builds = 0
        result = M.evaluate_rule(rule, copy.deepcopy(inputs))
        if expect.get('oneGraph') and M.Graph.builds != 1:
            raise AssertionError(f'{name}: graph built {M.Graph.builds} times')
        check(M, name, inputs, rule, expect, result)
        raw = M.result_bytes(result)
        for seed in range(5):
            if M.result_bytes(M.evaluate_rule(rule, shuffled(inputs, seed))) != raw:
                raise AssertionError(f'{name}: result depends on encounter order (seed {seed})')
        if M.result_bytes(M.evaluate_rule(rule, copy.deepcopy(inputs), algorithm=M.scc_kosaraju)) != raw:
            raise AssertionError(f'{name}: SCC algorithms disagree')
        entry = {'case': name, 'source': source, 'outcome': result['outcome'],
                 'resultSha256': hashlib.sha256(raw).hexdigest(),
                 'findings': [{'universe': f['universe'], 'subjectPath': f['subjectPath'], 'members': f['members'],
                               'matchingFactCount': f['parameters']['parameters']['matchingFactCount'],
                               'waived': f['waived']} for f in result['findings']],
                 'causeCodes': sorted({c['code'] for s in result['subjects'] for c in s['causes']})}
        if not expect.get('summaryOnly'):
            entry['values'] = [[s['universe'], s['path'], s['value']] for s in result['subjects']]
        else:
            entry['subjects'] = len(result['subjects'])
            entry['valueCounts'] = {v: sum(s['value'] == v for s in result['subjects'])
                                    for v in ('true', 'false', 'unknown')}
        report['cases'].append(entry)
    report['opLaw'] = op_law_cases(M)
    report['invariants'] = ['every expectation held', 'five seeded input permutations gave identical bytes',
                            'Tarjan and Kosaraju gave identical bytes', 'no indeterminate value lacked a blocking cause',
                            'the 1000-module chain built its graph once']
    raw = (json.dumps(report, indent=1, sort_keys=True, ensure_ascii=True) + '\n').encode('ascii')
    if args.write:
        REPORT.write_bytes(raw)
    elif REPORT.read_bytes() != raw:
        raise SystemExit('cases-report.json differs from this run')
    print(json.dumps({'cases': len(report['cases']), 'opLawRefusals': len(report['opLaw']),
                      'reportSha256': hashlib.sha256(raw).hexdigest(), 'written': args.write}))


if __name__ == '__main__':
    main()
