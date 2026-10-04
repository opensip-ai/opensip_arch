"""Reference model of the `cycle-representative` atom: atom contract section 4a (contract
successor I1-L, law M3-I1 r2 items 2.1 to 2.9 plus the successor precisions P0 to P7).

Design evidence over synthetic trusted inputs. It is not product code, not a provider and not
full Run replay. It is the harness oracle for `module-import-cycle` (law M3-I1 r2 item 8, "I2").

It is built on the design encoder `docs/coop/design-corrections/foundation/canonical.py`
(identity-and-evidence section 3): canonical sets use its canonical bytes, and every synthetic
fact2/scope2/coverage2 identifier is its H identity of a synthetic descriptor.

Inputs are already admitted (owner joins, schemas and occupancy sidecars are out of scope):

    rule        the policy rule (PolicyDocumentV2 shape)
    selected    [{universe, path, language}]       the rule's selected file subjects V (COMP:26)
    enumeration {state: complete|incomplete, causes}  composition's own enumeration result (COMP:28)
    bindings    [{universe|None, providerClosure, family, inventories, required}]
                the EnumerationPlan bindings for capabilityForRelation[imports]
    inventories {id: {kind, universe, state: complete|partial|unavailable, rows:[{nativeSubjectId, path}]}}
    facts       imports facts {id, relation:'imports', resolution, sourceUniverse, importer,
                targetUniverse, attribution: None | {occupancy, kind, evaluationNativeId}}
                and unresolved edges {id, relation:'unresolved-edge', payloadRelation, sourceUniverse, referrer}
    scopes      {id: {relation, resolution, sourceUniverse, targetUniverse, subjects}}
    coverages   {id: {scopeId, relation, resolution, sourceUniverse, targetUniverse, sufficiency}}
                sufficiency = the native owner's answer under REQUIREMENT:
                {requirement, satisfied, nativeCause, deficiencies}
    waivers     [{ruleId, subjectPath}]
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ARCH = Path(__file__).resolve().parents[6]
ENCODER_PATH = ARCH / 'docs/coop/design-corrections/foundation/canonical.py'
REGISTRY_PATH = ARCH / 'docs/coop/design-corrections/foundation/evaluator-projection-registry.v1.json'

OP = 'cycle-representative'
RELATION = 'imports'
MIN_RUNG = 'resolved-target'
# Item 2.5(c): the fixed sufficiency requirement every paired Coverage answers.
REQUIREMENT = {'relation': RELATION, 'minResolution': MIN_RUNG, 'minConfidenceMillionths': 0,
               'completeness': 'complete', 'quantifier': 'universal-negative',
               'unresolvedEdgePolicy': 'forbid', 'externalConsumerPolicy': 'forbid'}
# The causes this atom can emit: existing members of the closed registry (ATOM:421-432).
CAUSE_CODES = {'missing-relation-coverage', 'selector-unbound', 'population-unknown',
               'uncovered-expected-source-subject', 'scope-without-coverage', 'coverage-unknown',
               'target-kind-unknown', 'cross-family-edge-not-owed'}
DISCLOSURES = {'cross-family-edge-not-owed'}
FAMILY = 'typescript'


class OpLawRefusal(ValueError):
    """Item 2.2: POLICY.UNKNOWN_RULE (row 4 for a bundled document)."""


class HostInvariant(RuntimeError):
    """Item 2.5: an indeterminate value with no blocking cause is an implementation defect."""


def load_encoder():
    spec = importlib.util.spec_from_file_location('opensip_design_canonical', ENCODER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


C = load_encoder()
_REGISTRY = json.loads(REGISTRY_PATH.read_bytes())
LADDER = _REGISTRY['relations'][RELATION]['ladder']
assert LADDER == ['syntactic-specifier', 'resolved-target'], LADDER
assert _REGISTRY['capabilityForRelation'][RELATION] == 'imports'


def cset(items):
    """Canonical set: strict ascending canonical bytes, duplicates collapsed (COMP:91)."""
    unique = {C.canonical(item): item for item in items}
    return [unique[key] for key in sorted(unique)]


def ident(domain, descriptor):
    return C.identity(domain, descriptor)


def order_key(vertex):
    """Item 2.3 representative order: path bytes, then universe bytes."""
    universe, path = vertex
    return (path.encode('utf-8'), universe.encode('utf-8'))


def cause(code, universe=None, native_cause=None):
    assert code in CAUSE_CODES, code
    record = {'code': code, 'evidenceKind': None, 'nativeCause': native_cause}
    if universe is not None:  # ATOM section 4, "Cause representation (universe)"
        record['universe'] = universe
    return record


# Item 2.2: admission (op law).
def admit_rule(rule):
    """Return the op-law violations of one rule; empty means admitted. Any violation refuses."""
    violations = []

    def walk(node, root):
        op = node.get('op')
        if op in ('and', 'or'):
            for child in node.get('operands', []):
                walk(child, False)
        elif op == 'not':
            walk(node['operand'], False)
        elif op == OP:
            if not root:
                violations.append('not-whole-emitWhen')
            if node.get('relation') != RELATION:
                violations.append('relation')
            if node.get('minResolution') != MIN_RUNG:
                violations.append('minResolution')
            if node.get('filters') != []:
                violations.append('filters')
            for key in ('endpoint', 'evidence', 'n'):
                if key in node:
                    violations.append(key)
            if rule['subjectEnumeration']['subjectKind'] != 'file':
                violations.append('subjectKind')

    walk(rule['emitWhen'], True)
    return violations


# Item 2.3: the graph, built once per rule evaluation.
class Graph:
    builds = 0

    def __init__(self, inputs):
        Graph.builds += 1
        self.vertices = {(s['universe'], s['path']) for s in inputs['selected']}
        self.universes = sorted({u for u, _ in self.vertices}, key=lambda u: u.encode('utf-8'))
        self.index = {u: self._symbol_index(inputs, u) for u in
                      {f['sourceUniverse'] for f in inputs['facts']} |
                      {f.get('targetUniverse') for f in inputs['facts'] if f.get('targetUniverse')}}
        self.edge_facts = {}      # (u, w) -> [fact ids]
        self.uncertain = []       # {fact, source, causes}
        self.unresolved = {}      # vertex -> [fact ids]
        rung = {name: i for i, name in enumerate(LADDER)}
        for fact in inputs['facts']:
            if fact['sourceUniverse'] not in self.universes:
                continue
            if fact['relation'] == RELATION:
                if rung[fact['resolution']] < rung[MIN_RUNG]:
                    continue  # a syntactic-specifier fact is never an edge (PAC:129-132)
                self._project(fact)
            elif fact['relation'] == 'unresolved-edge' and fact['payloadRelation'] == RELATION:
                referrer = self._place(fact['sourceUniverse'], fact['referrer'])
                if referrer in self.vertices:  # P4: otherwise in no witness
                    self.unresolved.setdefault(referrer, []).append(fact['id'])

    @staticmethod
    def _symbol_index(inputs, universe):
        """P3: exact nativeSubjectId over every retained symbol inventory of the universe."""
        rows = {}
        for inventory in inputs['inventories'].values():
            if inventory['kind'] == 'symbol' and inventory['universe'] == universe:
                for row in inventory['rows']:
                    rows.setdefault(row['nativeSubjectId'], set()).add(row['path'])
        return rows

    def _place(self, universe, native_id):
        paths = self.index.get(universe, {}).get(native_id, set())
        return (universe, next(iter(paths))) if len(paths) == 1 else None

    def _project(self, fact):
        source = self._place(fact['sourceUniverse'], fact['importer'])
        if source is not None and source not in self.vertices:
            return  # an edge entering V from outside is not read further
        attribution = fact.get('attribution') or {'occupancy': 'unknown'}
        if attribution['occupancy'] == 'external':
            return  # the host's explicit partition: not an edge (ATOM:52 known nomatch)
        causes, target = [], None
        if source is None:  # importer with no unique inventory row
            causes.append(cause('population-unknown', fact['sourceUniverse']))
        universe = fact['targetUniverse']
        if attribution['occupancy'] != 'first-party':
            causes.append(cause('target-kind-unknown', universe))  # P1
        elif attribution['kind'] == 'file':
            vertex = (universe, attribution['evaluationNativeId'])
            if vertex in self.vertices:
                target = vertex
            else:
                causes.append(cause('population-unknown', universe))
        elif attribution['kind'] == 'symbol':
            vertex = self._place(universe, attribution['evaluationNativeId'])
            if vertex is None:
                causes.append(cause('target-kind-unknown', universe))  # QP:84
            elif vertex in self.vertices:
                target = vertex
            else:
                causes.append(cause('population-unknown', universe))
        elif attribution['kind'] == 'package':
            causes.append(cause('population-unknown', universe))
        else:
            raise ValueError('unadmitted attribution kind')
        if causes:
            self.uncertain.append({'fact': fact['id'], 'source': source, 'causes': causes})
        else:
            self.edge_facts.setdefault((source, target), []).append(fact['id'])

    def successors(self):
        out = {v: set() for v in self.vertices}
        for (u, w) in self.edge_facts:
            out[u].add(w)
        return out


def scc_tarjan(vertices, succ):
    """Iterative Tarjan: strongly connected components as frozensets."""
    index, low, on, stack, out, counter = {}, {}, set(), [], [], [0]
    for root in sorted(vertices, key=order_key):
        if root in index:
            continue
        work = [(root, iter(sorted(succ[root], key=order_key)))]
        index[root] = low[root] = counter[0]; counter[0] += 1
        stack.append(root); on.add(root)
        while work:
            v, children = work[-1]
            advanced = False
            for w in children:
                if w not in index:
                    index[w] = low[w] = counter[0]; counter[0] += 1
                    stack.append(w); on.add(w)
                    work.append((w, iter(sorted(succ[w], key=order_key))))
                    advanced = True
                    break
                if w in on:
                    low[v] = min(low[v], index[w])
            if advanced:
                continue
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[v])
            if low[v] == index[v]:
                component = set()
                while True:
                    w = stack.pop(); on.discard(w); component.add(w)
                    if w == v:
                        break
                out.append(frozenset(component))
    return out


def scc_kosaraju(vertices, succ):
    """A second, independent SCC algorithm (item 2.9: the algorithm is free)."""
    pred = {v: set() for v in vertices}
    for v, ws in succ.items():
        for w in ws:
            pred[w].add(v)
    seen, order = set(), []
    for root in sorted(vertices, key=order_key, reverse=True):
        if root in seen:
            continue
        seen.add(root)
        work = [(root, iter(sorted(succ[root], key=order_key, reverse=True)))]
        while work:
            v, children = work[-1]
            for w in children:
                if w not in seen:
                    seen.add(w)
                    work.append((w, iter(sorted(succ[w], key=order_key, reverse=True))))
                    break
            else:
                work.pop()
                order.append(v)
    assigned, out = set(), []
    for root in reversed(order):
        if root in assigned:
            continue
        component, todo = set(), [root]
        assigned.add(root)
        while todo:
            v = todo.pop(); component.add(v)
            for w in pred[v]:
                if w not in assigned:
                    assigned.add(w); todo.append(w)
        out.append(frozenset(component))
    return out


def cyclic_components(graph, algorithm=scc_tarjan):
    succ = graph.successors()
    return [c for c in algorithm(graph.vertices, succ)
            if len(c) >= 2 or next(iter(c)) in succ[next(iter(c))]]


# Item 2.5: graph completeness, once per rule evaluation (precisions P2, P5, P7).
def graph_completeness(inputs, universes):
    causes, scope_ids, coverage_ids, deficiencies = [], [], [], []
    owed = inputs['bindings']
    if not owed:  # shared prelude P2: the only global return
        return {'complete': False, 'unknown': True, 'causes': [cause('missing-relation-coverage')],
                'coverageIds': [], 'scopeIds': [], 'nativeDeficiencies': []}
    available = [b for b in owed if b['universe'] is not None]
    for binding in owed:  # shared prelude P1 (outgoing emits nothing for an owed family)
        if binding['universe'] is None and binding['family'] not in (None, FAMILY):
            causes.append(cause('cross-family-edge-not-owed'))
    paired_all = []
    for universe in universes:  # P2: ascending universe bytes, accumulated, no cross-universe return
        bound = [b for b in available if b['universe'] == universe]
        if not bound:  # outgoing step 1 ends this universe's account
            causes.append(cause('selector-unbound'))
            continue
        # 2.5(b)2: the census, from the imports-cell inventories of the owed bindings only.
        inventories = [inputs['inventories'][i] for b in bound for i in b['inventories']]
        expected, census_unknown = set(), not inventories
        for inventory in inventories:
            assert inventory['kind'] == 'symbol'
            expected |= {row['nativeSubjectId'] for row in inventory['rows']}
            census_unknown |= inventory['state'] != 'complete'
        if census_unknown:
            causes.append(cause('population-unknown', universe))
        # 2.5(b)3: exact-id coverage by every exact scope of U, whatever its target universe.
        scopes = sorted((sid for sid, s in inputs['scopes'].items()
                         if s['relation'] == RELATION and s['resolution'] == MIN_RUNG
                         and s['sourceUniverse'] == universe), key=str.encode)
        present = set()
        for sid in scopes:
            present |= set(inputs['scopes'][sid]['subjects'])
        if not scopes or expected - present:
            causes.append(cause('uncovered-expected-source-subject', universe))
        # 2.5(b)4: pairing; every scope is cited, every unpaired scope is a cause.
        for sid in scopes:
            scope_ids.append(sid)
            paired = [cid for cid, cov in inputs['coverages'].items()
                      if cov['scopeId'] == sid and cov['relation'] == RELATION
                      and cov['resolution'] == MIN_RUNG and cov['sourceUniverse'] == universe]
            if not paired:
                causes.append(cause('scope-without-coverage', universe))
            paired_all.extend(paired)
    # 2.5(c): every paired Coverage, deduplicated and ascending by coverage2 (ATOM:95-103).
    for cid in sorted(set(paired_all), key=str.encode):
        coverage = inputs['coverages'][cid]
        answer = coverage['sufficiency']
        if answer['requirement'] != REQUIREMENT:
            raise ValueError('sufficiency answered under another requirement')
        coverage_ids.append(cid)
        if not answer['satisfied']:
            causes.append(cause('coverage-unknown', coverage['sourceUniverse'], answer['nativeCause']))
            deficiencies.extend(answer['deficiencies'])
    causes = cset(causes)
    blocking = [c for c in causes if c['code'] not in DISCLOSURES]
    return {'complete': not blocking, 'unknown': bool(blocking), 'causes': causes,
            'coverageIds': coverage_ids, 'scopeIds': scope_ids,
            'nativeDeficiencies': cset(deficiencies)}


def evaluate_rule(rule, inputs, algorithm=scc_tarjan):
    """Evaluate one gating rule whose emitWhen is the op: values, witnesses, findings, outcome."""
    violations = admit_rule(rule)
    if violations:
        raise OpLawRefusal('POLICY.UNKNOWN_RULE:' + ','.join(violations))
    graph = Graph(inputs)
    if not graph.vertices:  # S = 0: nothing is evaluated (item 2.8; COMP:26)
        return compose(rule, inputs, [], [])
    components = cyclic_components(graph, algorithm)
    completeness = graph_completeness(inputs, graph.universes)
    edge_causes = [c for edge in graph.uncertain for c in edge['causes']]
    all_causes = cset(completeness['causes'] + edge_causes)
    blocking = [c for c in all_causes if c['code'] not in DISCLOSURES]
    member_of = {v: comp for comp in components for v in comp}
    rep = {comp: min(comp, key=order_key) for comp in components}
    unplaced = [e['fact'] for e in graph.uncertain if e['source'] is None]
    subjects = []
    for vertex in sorted(graph.vertices, key=order_key):
        comp = member_of.get(vertex)
        if comp is not None:
            value = 'true' if rep[comp] == vertex else 'false'
        elif completeness['complete'] and not graph.uncertain:
            value = 'false'
        else:
            value = 'unknown'
        if value == 'unknown' and not blocking:
            raise HostInvariant('indeterminate value without a blocking cause')
        if comp is None:
            matching = []
        elif value == 'true':  # every edge with both ends in C
            matching = [f for (u, w), fs in graph.edge_facts.items() if u in comp and w in comp for f in fs]
        else:  # C's edges leaving this member
            matching = [f for (u, w), fs in graph.edge_facts.items() if u == vertex and w in comp for f in fs]
        uncertain = [e['fact'] for e in graph.uncertain if e['source'] == vertex]
        uncertain += graph.unresolved.get(vertex, [])
        if value == 'unknown':
            uncertain += unplaced
        subjects.append({'universe': vertex[0], 'path': vertex[1], 'value': value,
                         'matchingFactIds': cset(matching), 'uncertainFactIds': cset(uncertain),
                         'coverageIds': completeness['coverageIds'], 'scopeIds': completeness['scopeIds'],
                         'causes': all_causes, 'nativeDeficiencies': completeness['nativeDeficiencies']})
    findings = []
    endpoints = {f: (u, w) for (u, w), fs in graph.edge_facts.items() for f in fs}
    language = {(s['universe'], s['path']): s.get('language', FAMILY) for s in inputs['selected']}
    for subject in subjects:
        if subject['value'] != 'true':
            continue
        members = sorted({v for f in subject['matchingFactIds'] for v in endpoints[f]}, key=order_key)
        path = subject['path']
        parameters = {'schemaVersion': 2, 'messageCode': rule.get('messageCode', rule['ruleId']),
                      'parameters': {'ruleId': rule['ruleId'], 'subjectPath': path, 'qualifiedName': path,
                                     'subjectKind': 'file',
                                     'subjectLanguage': language[(subject['universe'], path)],
                                     'matchingFactCount': len(subject['matchingFactIds']),
                                     'matchingImportCount': 0}}
        findings.append({'universe': subject['universe'], 'subjectPath': path,
                         'members': [p for _, p in members], 'memberVertices': [list(v) for v in members],
                         'parameters': parameters,
                         'parameterDigest': ident('finding-parameters', parameters)})
    return compose(rule, inputs, subjects, findings, completeness=completeness,
                   components=[sorted([list(v) for v in c], key=lambda v: order_key(tuple(v)))
                               for c in sorted(components, key=lambda c: order_key(rep[c]))],
                   uncertainEdges=len(graph.uncertain))


def compose(rule, inputs, subjects, findings, **extra):
    """COMP:56 for one enabled gating rule (the pack's only rule)."""
    waived = {(w['ruleId'], w['subjectPath']) for w in inputs.get('waivers', [])}
    for finding in findings:
        finding['waived'] = (rule['ruleId'], finding['subjectPath']) in waived
    if any(not f['waived'] for f in findings):
        outcome = 'fail'
    elif inputs['enumeration']['state'] != 'complete':
        outcome = 'indeterminate'
    elif any(s['value'] == 'unknown' and any(c['code'] not in DISCLOSURES for c in s['causes'])
             for s in subjects):
        outcome = 'indeterminate'
    else:
        outcome = 'pass'
    return {'outcome': outcome, 'subjects': subjects, 'findings': findings,
            'enumeration': inputs['enumeration'], **extra}


def result_bytes(result):
    return C.canonical(result)


if __name__ == '__main__':
    sys.exit('import this module; evidence/check_cycle_representative.py runs the cases')
