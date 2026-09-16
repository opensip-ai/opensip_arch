"""INDEPENDENT derivation #4 -- atom evaluation under foundation/atom-evaluation-contract.v1.md as
frozen for generation 23 (changed again: 36951 -> 48688 bytes, with the projection registry
59745 -> 60005 and the incoming-search schema 12930 -> 13052).

Written from the clauses, and deliberately NOT importing opensip_eval or opensip_compose: it uses
only the identity core (C, Cset, H), the store loader, and the reference Draft 2020-12 schema layer.
It re-derives, for every atomic predicate of every retained Run, the completeness result, the
value, the AtomCauseV1 list, the composition-9.5 evaluation-deficiency rows and the COMPLETE
predicate-witness record, admits each of those against its owning schema, and compares the whole
witness (and its digest) with the retained bytes.

CLAUSE -> CODE MAP (contract = atom-evaluation-contract.v1.md, composition =
evaluator-composition-contract.v3.md, registry = evaluator-projection-registry.v1.json)

 A1  s4 "Completeness result and its independence from truth": a return ends ONLY the completeness
     computation; a known match still decides exists/none/count-at-most; the negative answer needs
     complete=true AND unknown=false AND no uncertain match.            -> finish(), truth()
 A2  s4 "Selection order (both endpoints)": scopes ascending scope2; Coverage deduplicated and
     sorted ascending coverage2 AFTER pairing, never the scope-walk order.  -> ascending_coverage()
 A3  s4 "Cause representation (universe)" + registry $defs/AtomCauseV1: key carried only when a
     universe is reported; projection writes explicit null.            -> cause(), admit()
 A4  s4 shared prelude P1 (unavailable owed bindings, family law).       -> prelude()
 A5  s4 shared prelude P2 (no owed binding; shared return incoming takes). -> prelude()
 A6  s4 outgoing 1 selector-unbound (null) + return.                     -> outgoing()
 A7  s4 outgoing 2 uncovered-expected-source-subject (U) + return, about the CURRENT subject only
     ("Rule-level enumeration uncertainty is root, not this atom").     -> outgoing()
 A8  s4 outgoing 3: every containing scope in scopeIds; scope-without-coverage per unpaired scope;
     return with EMPTY coverageIds when any scope is unpaired or no pairing exists. -> outgoing()
 A9  s4 outgoing 4: per paired Coverage in selection order, cite it, evaluate the view, and emit
     coverage-unknown (universe = key.sourceUniverse) when unsatisfied; no return. -> outgoing()
 A10 s4 "Deterministic dependency view": position 0 primary; transitive DEPENDS_ON breadth-first,
     each relation once at first visit; no selected Coverage -> no position; same source kind
     pairs to current-source scopes, different kind is whole-source search of (S, T). -> view()
 A11 s4 fold field rules (coverage rank, confidence min, WHOLE resolutionCompleteness / closedWorld
     records only on strictly worse rank, ordered union of derivationKinds, typed carrier whole
     from the first partition carrying a deficiency, everything else first). -> fold()
 A12 s4 coverage-unknown nativeCause = first non-null nativeCause scanning positions. -> outgoing()
 A13 native-evidence s4.6 steps 1..6 per position, step 8 dependency posture, and step 1 for every
     relation of the dependency closure that occupies NO position ("Relation absent from the view
     -> required-relation-missing"; atom s4 "answers required-relation-missing, exactly as an
     absent relation does").                                            -> suff(), dep_closure()
 A14 s5 quantifier: universal-negative at resolved rungs for none/count-at-most/all-covered,
     examination completeness otherwise; exists is existential.        -> quantifier()
 A15 composition s9.5 atom-mapped rules 1..3; identity-schemas.v3 evaluation-deficiency and
     predicate-witness admission; registry membership per plane.       -> mapped(), witness()
 A16 s6 "Runtime polarity" + registry importQuantifiers.polaritySetR: an UNFILTERED exists is
     satisfied by observed-hit OR observable-unhit; an observability filter restricts the matching
     set; unobservable/unmapped never enter it and stay uncertain whatever the filter; completeness
     needs a consumable polarity row (either polarity) for every owed wrapper and the payload owner
     window/population.                                                  -> derive_imported()
 A17 s4 incoming: P2 shared return, no further early return, both cross-family routes, owed-family
     unavailable binding blocking, the three-row search-accounting table. LAW-LEVEL ONLY: no retained
     Run's policy has an endpoint=target atom.                          -> incoming()
 A18 s4 I1: the subject's own program is always an owed source; no available owed binding at U ->
     selector-unbound (projected universe null), blocking but NOT a return, at most once, order
     independent; known matches survive.                                -> incoming()
 A19 s4 "Admitted inputs for these cases": an IncomingSearchV1 for a scope-less provider group is a
     GLOBAL admission refusal (INCOMING_SEARCH_SCHEMA for empty scopeRefs, INCOMING_SEARCH_SCOPE_MISJOIN
     for a nonempty one); a scope with absent/null enumeratorClosure refuses ATOM_NATIVE_CARRIER when
     paired on either endpoint and when an attestation names it; an explicit empty-subject scope
     closes an empty selected program.                         -> admit_attestation(), carrier()
 A20 s4 dependency pairing: only exact (relation, rung, S) scopes, paired by mapping OR commitment;
     "There is no mapped-scope fallback" -- a mapping to a scope outside the selection pairs nothing.
                                                                        -> paired_coverage(), view()
 A21 s4 "Dependency totality (same kind)": an incoming view whose same-kind dependency leaves an owed
     subject uncovered is evaluated with and without the gap position; both native answers are kept
     and the view is satisfied only when both are.                     -> incoming_view()

WITHDRAWN AT GENERATION 23
 I-A1 (generation 22) read "A dependency contributing no selected Coverage occupies no position" as
      "an absent dependency adds no cause". Current s4 states the removed position "answers
      required-relation-missing, exactly as an absent relation does" and native s4.6 step 1 applies;
      the reading is withdrawn and the Rust Run's two affected clones atoms change (V23-D2).

DECLARED INTERPRETATIONS
 I-A2 The published DEPENDS_ON graph is the parenthetical in s4 ("reachability->calls@resolved-callee;
      clones->declares@syntactic"). This module verifies that the quote is present in the kit bytes
      before using it; the graph is acyclic and one edge deep, so the repeat guard is exercised only
      by construction.
"""
import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_store as ST

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'
RUNS = ['syntax-code', 'typescript', 'rust', 'rust-partial', 'syntax-data']
ATOM_MD = 'foundation/atom-evaluation-contract.v1.md'
PROJ_DOC = 'foundation/evaluator-projection-registry.v1.json'
IDENT_DOC = 'foundation/identity-schemas.v3.json'
REL_DOC = 'foundation/relation-payload-schemas.v2.json'
IMPORTED_DOC = 'workflows/schemas/imported-evidence.schema.json'
INCOMING_DOC = 'foundation/incoming-search.schema.v1.json'
PREDECESSOR_DIRS = ('predecessors.v22', 'predecessors.v20')


def kitjson(name):
    return json.load(open(S.KIT + '/' + S.doc_path(name)))


ATOM_TEXT = open(S.KIT + '/' + S.doc_path(ATOM_MD), encoding='utf-8').read()
PROJ = kitjson(PROJ_DOC)
RELREG = kitjson(REL_DOC)['x-opensip-relation-registry']['relations']
DEFREG = kitjson(IDENT_DOC)['x-opensip-evaluator-deficiency-registry']
EVREL = kitjson(IMPORTED_DOC)['x-opensip-evidence-relation-registry']['relations']
RESOLVED = set(PROJ['resolvedRungs'])
NON_BLOCKING = set(DEFREG['nonBlockingDisclosures'])

# exact kit bytes (atom contract s4, the sufficiency_v2 view paragraph): the targets are in
# backticks. The first draft of this literal omitted them and the guard refused to run, which is
# the guard doing its job -- the graph is only used when the quoted text is really in the kit.
DEPENDS_ON_QUOTE = 'reachability→`calls@resolved-callee`; clones→`declares@syntactic`'
DEPENDS_ON = {'reachability': [('calls', 'resolved-callee')],
              'clones': [('declares', 'syntactic')]}
RANK_QUOTES = ('complete < unknown',
               'complete/not-applicable < partial < incomplete < not-attempted',
               'closed < open < unknown')
# generation-23 clauses this module implements; verified present in the kit bytes before use
LAW_QUOTES = ('answers `required-relation-missing`, exactly as an absent relation does',
              'There is **no mapped-scope fallback**',
              'so either `observed-hit` or `observable-unhit` can satisfy it',
              "**I1 — the subject's own program is always an owed source.**",
              'is refused `ATOM_NATIVE_CARRIER` wherever it is',
              'Both native answers are retained in `nativeDeficiencies`')
PROVIDER = 'closure2:' + '9' * 64          # synthetic helper-only enumerator closure
RANK = {
    'coverage': {'complete': 0, 'unknown': 1},
    'state': {'complete': 0, 'not-applicable': 0, 'partial': 1, 'incomplete': 2,
              'not-attempted': 3},
    'exportsClosed': {'closed': 0, 'open': 1, 'unknown': 2},
}
RUNG_UNAVAILABLE = ('language-tier-unsupported', 'provider-unavailable',
                    'input-closure-incomplete', 'budget-exhausted')
PRECEDENCE = ('language-tier-unsupported', 'provider-unavailable', 'input-closure-incomplete',
              'budget-exhausted', 'confidence-floor-unmet', 'derivation-policy-unmet',
              'resolution-incomplete', 'external-consumers-unknown', 'required-relation-missing')


class NotExercised(Exception):
    pass


class Refusal(Exception):
    """an admission refusal the clauses name (ATOM_NATIVE_CARRIER, INCOMING_SEARCH_*)"""

    def __init__(self, code, detail=None):
        super().__init__('%s %s' % (code, detail))
        self.code, self.detail = code, detail


class F:
    def __init__(self):
        self.rows = []

    def need(self, cond, clause, check, detail=None):
        self.rows.append({'clause': clause, 'check': check,
                          'result': 'PASS' if cond else 'REFUSE', 'detail': detail})
        return bool(cond)

    @property
    def refusals(self):
        return [r for r in self.rows if r['result'] == 'REFUSE']


def admit(doc, selector, instance):
    errs = S.stock_validate(doc, selector, instance)
    return {'selector': selector, 'admitted': not errs, 'errors': errs[:3]}


# ------------------------------------------------------------------------------ law pieces
def cause(code, universe=None, native_cause=None, evidence_kind=None):
    c = {'code': code, 'evidenceKind': evidence_kind, 'nativeCause': native_cause}
    if universe is not None:
        c['universe'] = universe
    return c


def family_of_mode(mode):
    hits = [n for n, fam in PROJ['engineFamilies']['families'].items()
            if mode in fam['languageModes']]
    return hits[0] if len(hits) == 1 else None


def family_of_domain(domain):
    hits = [n for n, fam in PROJ['engineFamilies']['families'].items()
            if fam['universeDomain'] == domain]
    return hits[0] if len(hits) == 1 else None


def owed_family(a, b):
    return a is None or b is None or a == b


def owed_bindings(R, relation):
    cap = PROJ['capabilityForRelation'][relation]
    return [{'cell': ci, 'program': bi, 'languageMode': c['languageMode'],
             'universe': b.get('universe')}
            for ci, c in enumerate(R.ep['cells']) if c['capabilityId'] == cap
            for bi, b in enumerate(c['programBindings'])]


def prelude(R, relation, subject_family, endpoint):
    causes = []
    owed = owed_bindings(R, relation)
    for b in owed:
        if b['universe'] is not None:
            continue
        if not owed_family(family_of_mode(b['languageMode']), subject_family):
            causes.append(cause('cross-family-edge-not-owed'))
        elif endpoint == 'target':
            causes.append(cause('unavailable-program-binding'))
    if not owed:
        causes.append(cause('missing-relation-coverage'))
        return owed, causes, 'P2'
    return owed, causes, None


def ascending_coverage(pairing):
    return sorted({cid for cids in pairing.values() for cid in cids})


def carrier(R, scope_id):
    ec = R.scopes[scope_id].get('enumeratorClosure')
    if not (isinstance(ec, str) and ec.startswith('closure2:') and len(ec) == 73):
        raise Refusal('ATOM_NATIVE_CARRIER', {'scope': scope_id, 'enumeratorClosure': ec})


def paired_coverage(R, scope_id):
    """pairing by the coverageScopes MAPPING (the envelope scopeId) or, for a Coverage with no
    mapping, by native subject_scope_commitment. A mapping never falls back to the commitment."""
    out = []
    for c, rec in R.covs.items():
        mapped = rec.get('scopeId')
        if mapped is not None:
            if mapped == scope_id:
                out.append(c)
        elif R.cov_pay[c]['key'].get('subjectScopeCommitment') == \
                'sha256:' + scope_id.split(':', 1)[1]:
            out.append(c)
    return sorted(out)


def dep_closure(relation):
    out, queue, seen = [], list(DEPENDS_ON.get(relation, [])), {relation}
    while queue:
        rel, rung = queue.pop(0)
        if rel in seen:
            continue
        seen.add(rel)
        out.append((rel, rung))
        queue.extend(DEPENDS_ON.get(rel, []))
    return out


def fold(entries):
    out = copy.deepcopy(entries[0])
    for later in entries[1:]:
        if RANK['coverage'][later['coverage']] > RANK['coverage'][out['coverage']]:
            out['coverage'] = later['coverage']
        out['confidenceMillionths'] = min(out['confidenceMillionths'],
                                          later['confidenceMillionths'])
        for field, key in (('resolutionCompleteness', 'state'), ('closedWorld', 'exportsClosed')):
            if RANK[key][later[field][key]] > RANK[key][out[field][key]]:
                out[field] = copy.deepcopy(later[field])
        for k in later['derivationKinds']:
            if k not in out['derivationKinds']:
                out['derivationKinds'].append(k)
    for e in entries:
        if e['deficiency'] is not None:
            out['deficiency'], out['nativeCause'] = e['deficiency'], e['nativeCause']
            break
    return out


def view(R, relation, primary, subject):
    key = R.cov_pay[primary]['key']
    S_, T_ = key['sourceUniverse'], key['targetUniverse']
    positions = [{'relation': relation, 'rung': key['resolution'], 'coverageIds': [primary],
                  'entry': R.cov_pay[primary]['entry'], 'role': 'primary'}]
    kind = PROJ['relations'][relation]['sourceSubjectKind']
    seen, frontier = [relation], [relation]
    while frontier:
        nxt = []
        for r in frontier:
            for dep, rung in DEPENDS_ON.get(r, []):
                if dep in seen:
                    continue
                seen.append(dep)
                nxt.append(dep)
                if PROJ['relations'][dep]['sourceSubjectKind'] == kind:
                    # A20: exact (relation, rung, S) scopes only, paired by mapping or commitment;
                    # a mapping to any other scope pairs nothing (no mapped-scope fallback)
                    sc = sorted(sid for sid, s in R.scopes.items()
                                if (s['relation'], s['resolution'], s['sourceUniverse'])
                                == (dep, rung, S_)
                                and subject['nativeSubjectId'] in s['subjects'])
                    pairs = {s: [c for c in paired_coverage(R, s)
                                 if exact_key(R, c, dep, rung, S_, T_)] for s in sc}
                    for s in sc:
                        if pairs[s]:
                            carrier(R, s)
                    cids = sorted({c for s in sc for c in pairs[s]})
                else:
                    cids = sorted({c for c in R.covs
                                   if (R.cov_pay[c]['key']['relation'],
                                       R.cov_pay[c]['key']['resolution'],
                                       R.cov_pay[c]['key']['sourceUniverse'],
                                       R.cov_pay[c]['key']['targetUniverse'])
                                   == (dep, rung, S_, T_)})
                if cids:
                    positions.append({'relation': dep, 'rung': rung, 'coverageIds': cids,
                                      'entry': fold([R.cov_pay[c]['entry'] for c in cids]),
                                      'role': 'dependency'})
        frontier = nxt
    return positions


def ladder_index(relation, rung):
    return RELREG[relation]['ladder'].index(rung)


def suff(positions, quantifier, target_exported=False):
    found = []
    # A13: native s4.6 step 1 for every relation of the step-8 closure with no position
    present = {p['relation'] for p in positions}
    for dep, _rung in dep_closure(positions[0]['relation']):
        if dep not in present:
            found.append('required-relation-missing')
    for i, p in enumerate(positions):
        e = p['entry']
        completeness = 'complete' if i == 0 or quantifier == 'universal-negative' else 'partial-ok'
        if ladder_index(p['relation'], e['resolution']) < ladder_index(p['relation'], p['rung']):
            found.append(e['deficiency'] if e['deficiency'] in RUNG_UNAVAILABLE
                         else 'required-relation-missing')
        if completeness == 'complete' and e['coverage'] != 'complete':
            if e['deficiency'] is None:
                raise NotExercised('STEP5_ENTRY_WITHOUT_OWN_DEFICIENCY')
            found.append(e['deficiency'])
        if quantifier == 'universal-negative':
            if e['resolutionCompleteness']['state'] in ('partial', 'not-attempted', 'incomplete'):
                found.append('resolution-incomplete')
            if target_exported and e['closedWorld']['exportsClosed'] != 'closed':
                found.append('external-consumers-unknown')
    uniq = []
    for c in found:
        if c not in uniq:
            uniq.append(c)
    pick = next((d for d in PRECEDENCE if d in uniq), uniq[0] if uniq else None)
    return {'satisfied': not uniq, 'deficiency': pick, 'causes': uniq}


def finish(causes, scope_ids, cov_ids, nds, returned, views=None):
    blocking = [c for c in causes if c['code'] not in NON_BLOCKING]
    complete = returned is None and not blocking
    return {'complete': complete, 'unknown': not complete, 'causes': K.cset(causes),
            'scopeIds': sorted(scope_ids), 'coverageIds': list(cov_ids),
            'nativeDeficiencies': K.cset_strings(nds), 'returned': returned,
            'views': views or []}


def outgoing(R, relation, rung, subject, quantifier):
    U = subject['universe']
    fam = family_of_domain(R.universe_domain.get(U))
    owed, causes, ret = prelude(R, relation, fam, 'source')
    if ret:
        return finish(causes, [], [], [], ret)
    if U not in {b['universe'] for b in owed if b['universe'] is not None}:
        causes.append(cause('selector-unbound'))
        return finish(causes, [], [], [], 'outgoing-1')
    if RELREG[relation]['subjectKind'] not in ('source-path', 'package-name', 'symbol'):
        raise NotExercised('SUBJECT_KIND_LAW:%s' % RELREG[relation]['subjectKind'])
    containing = sorted(sid for sid, s in R.scopes.items()
                        if (s['relation'], s['resolution'], s['sourceUniverse']) == (relation, rung, U)
                        and subject['nativeSubjectId'] in s['subjects'])
    if not containing:
        causes.append(cause('uncovered-expected-source-subject', U))
        return finish(causes, [], [], [], 'outgoing-2')
    pairing = {sid: paired_coverage(R, sid) for sid in containing}
    for sid in containing:
        if pairing[sid]:
            carrier(R, sid)                                          # A19 on the source endpoint
    unpaired = [sid for sid in containing if not pairing[sid]]
    for _ in unpaired:
        causes.append(cause('scope-without-coverage', U))
    combined = ascending_coverage(pairing)
    if unpaired or not combined:
        return finish(causes, containing, [], [], 'outgoing-3')
    nds, cov_ids, views = [], [], []
    for cid in combined:
        cov_ids.append(cid)
        positions = view(R, relation, cid, subject)
        res = suff(positions, quantifier)
        first_nc = None
        for p in positions:
            if p['entry']['nativeCause'] is not None:
                first_nc = p['entry']['nativeCause']
                break
        views.append({'coverageId': cid, 'positions': [
            {k: p[k] for k in ('role', 'relation', 'rung', 'coverageIds')} for p in positions],
            'sufficiency': res, 'carrier': first_nc})
        if not res['satisfied']:
            nds.append(res['deficiency'])
            causes.append(cause('coverage-unknown', R.cov_pay[cid]['key']['sourceUniverse'],
                                first_nc))
    return finish(causes, containing, cov_ids, nds, None, views)


def quantifier(op, rung):
    return 'existential' if op == 'exists' or rung not in RESOLVED else 'universal-negative'


def truth(op, known, uncertain, comp, n=None):
    negative = comp['complete'] and not comp['unknown'] and not uncertain
    if op == 'exists':
        return 'true' if known else ('false' if negative else 'indeterminate')
    if op == 'none':
        return 'false' if known else ('true' if negative else 'indeterminate')
    if op == 'count-at-most':
        return 'false' if len(known) > n else ('true' if negative else 'indeterminate')
    if op == 'all-covered':
        return 'true' if negative else 'indeterminate'
    raise NotExercised('OP:%s' % op)


# ---------------------------------------------------------------------------- incoming (A17)
def exact_key(R, c, rel, rung, S_, T_):
    k = R.cov_pay[c]['key']
    return (k['relation'], k['resolution'], k['sourceUniverse'], k['targetUniverse']) == \
        (rel, rung, S_, T_)


def incoming_view(R, relation, rung, S_, T_, owed, primary_entry, target_exported=False):
    """A21: the incoming dependency view of one evaluated partition (or attestation) and its
    same-kind dependency totality. `owed` is the evaluated scope's subjects (or the union of the
    provider group's owned scopes' subjects for a whole-source attestation view)."""
    positions = [{'relation': relation, 'rung': rung, 'coverageIds': [], 'entry': primary_entry,
                  'role': 'primary'}]
    kind = PROJ['relations'][relation]['sourceSubjectKind']
    gaps, cited = [], []
    for dep, drung in dep_closure(relation):
        if PROJ['relations'][dep]['sourceSubjectKind'] == kind:
            sel = sorted(s for s, rec in R.scopes.items()
                         if (rec['relation'], rec['resolution'], rec['sourceUniverse'])
                         == (dep, drung, S_) and set(rec['subjects']) & set(owed))
            pairs = {s: [c for c in paired_coverage(R, s) if exact_key(R, c, dep, drung, S_, T_)]
                     for s in sel}
            for s in sel:
                if pairs[s]:
                    carrier(R, s)
            cids = sorted({c for s in sel for c in pairs[s]})
            covered = {x for s in sel if pairs[s] for x in R.scopes[s]['subjects']}
            if cids and set(owed) - covered:
                gaps.append(dep)
        else:
            cids = sorted(c for c in R.covs if exact_key(R, c, dep, drung, S_, T_))
        if cids:
            cited.extend(cids)
            positions.append({'relation': dep, 'rung': drung, 'coverageIds': cids,
                              'entry': fold([R.cov_pay[c]['entry'] for c in cids]),
                              'role': 'dependency'})
    actual = suff(positions, 'universal-negative', target_exported)
    nds = [] if actual['satisfied'] else [actual['deficiency']]
    satisfied, without = actual['satisfied'], None
    if gaps:
        without = suff([p for p in positions if p['relation'] not in gaps], 'universal-negative',
                       target_exported)
        if not without['satisfied']:
            nds.append(without['deficiency'])
        satisfied = satisfied and without['satisfied']
    nc = next((p['entry']['nativeCause'] for p in positions
               if p['entry']['nativeCause'] is not None), None)
    return {'satisfied': satisfied, 'nativeDeficiencies': nds, 'carrier': nc, 'gaps': gaps,
            'coverageIds': sorted(set(cited)), 'actual': actual, 'withoutGapPositions': without}


def admit_attestation(R, rec):
    """A19: global IncomingSearchV1 admission -- owning schema (reference validator), the carrier of
    every scope it names, then the exact owned-scope join."""
    a = admit(INCOMING_DOC, '#', rec)
    if not a['admitted']:
        raise Refusal('INCOMING_SEARCH_SCHEMA', a['errors'])
    for s in rec['scopeRefs']:
        if s in R.scopes:
            carrier(R, s)
    owned = sorted(s for s, x in R.scopes.items()
                   if x.get('enumeratorClosure') == rec['providerClosure']
                   and (x['relation'], x['resolution'], x['sourceUniverse'])
                   == (rec['relation'], rec['minResolution'], rec['sourceUniverse']))
    if sorted(rec['scopeRefs']) != owned:
        raise Refusal('INCOMING_SEARCH_SCOPE_MISJOIN', {'named': rec['scopeRefs'], 'owned': owned})
    return True


QSET = PROJ['importQuantifiers']['polaritySetR']
OBS_ENUM = PROJ['comparatorTable']['observability']['enum']


def observability_filter(relation, filters):
    """A16: validates the atom's filters and returns the membership test of the matching set."""
    spec = PROJ['relations'][relation]['filters']
    for flt in filters:
        if spec.get(flt['field'], 'forbidden') == 'forbidden':
            raise Refusal('ATOM_FILTER_FIELD_FORBIDDEN', flt)
        if flt['field'] != 'observability':
            raise NotExercised('IMPORTED_FILTER_FIELD:%s' % flt['field'])
        vals = flt['value'] if flt['cmp'] == 'in' else [flt['value']]
        if flt['cmp'] in ('eq', 'neq', 'in') and any(v not in OBS_ENUM for v in vals):
            raise Refusal('ATOM_FILTER_ENUM_LITERAL_UNKNOWN', flt)

    def passes(obs):
        for flt in filters:
            c, v = flt['cmp'], flt['value']
            if c == 'eq':
                ok = obs == v
            elif c == 'neq':
                ok = obs != v
            elif c == 'in':
                ok = obs in v
            elif c == 'prefix':
                ok = obs.startswith(v)
            else:
                raise NotExercised('IMPORTED_FILTER_CMP:%s' % c)
            if not ok:
                return False
        return True
    return passes


def incoming(model):
    """Law-level incoming completeness over a typed synthetic model (no Run carries one)."""
    R = model['R']
    U = model['U']
    fam = family_of_domain(R.universe_domain.get(U))
    owed, causes, ret = prelude(R, model['relation'], fam, 'target')
    if ret:
        return finish(causes, [], [], [], ret)
    # A18 I1: after P1/P2, before the per-universe accumulation; blocking, not a return
    if U not in {b['universe'] for b in owed if b['universe'] is not None}:
        causes.append(cause('selector-unbound'))
    scope_ids, cov_ids, nds = [], [], []
    for g in model['groups']:
        S_ = g['S']
        if not owed_family(family_of_domain(R.universe_domain.get(S_)), fam):
            causes.append(cause('cross-family-edge-not-owed', S_))
            continue
        if g.get('population') == 'unknown':
            causes.append(cause('population-unknown', S_))
        if g.get('expectedIdInNoScope'):
            causes.append(cause('uncovered-expected-source-subject', S_))
        att = g.get('attestation')
        qualifying = bool(att and att['completeSearch'] and att['coverage'] == 'complete'
                          and att['examinedExhaustive'] and att['rcExaminedExhaustive'])
        if not g['scopes'] and not qualifying:
            causes.append(cause('source-target-search-unattested', S_))
        for sc in g['scopes']:
            scope_ids.append(sc['id'])
            paired = sorted(sc['paired'], key=lambda c: c['id'])
            to_u = [c for c in paired if c['V'] == U]
            if not paired and not qualifying:
                causes.append(cause('scope-without-coverage', S_))
            elif paired and not to_u and not qualifying:
                causes.append(cause('source-target-search-unattested', S_))
            for c in paired:
                cov_ids.append(c['id'])
                v = incoming_view(R, model['relation'], model['rung'], S_, c['V'],
                                  sc.get('subjects', []), c['entry'],
                                  target_exported=model.get('targetExported'))
                cov_ids.extend(v['coverageIds'])
                if not v['satisfied']:
                    nds.extend(v['nativeDeficiencies'])
                    causes.append(cause('coverage-unknown', S_, v['carrier']))
        # "Its shared sufficiency view is still evaluated; qualification alone does not establish
        # sufficiency" -- whenever the attestation stands in for missing S->U search
        needs_att = not g['scopes'] or any(not [c for c in sc['paired'] if c['V'] == U]
                                           for sc in g['scopes'])
        if att is not None and qualifying and needs_att:
            owed_subjects = sorted({x for sc in g['scopes'] for x in sc.get('subjects', [])})
            v = incoming_view(R, model['relation'], model['rung'], S_, U, owed_subjects,
                              att['entry'], target_exported=model.get('targetExported'))
            cov_ids.extend(v['coverageIds'])
            if not v['satisfied']:
                nds.extend(v['nativeDeficiencies'])
                causes.append(cause('coverage-unknown', S_, v['carrier']))
    return finish(causes, scope_ids, sorted(set(cov_ids)), nds, None)


# --------------------------------------------------------------------------- the retained Run
class Run:
    def __init__(self, path, label):
        self.label, self.path = label, path
        self.st, self.doc = ST.Store.load(path)
        st = self.st
        j = lambda d: json.loads(st.get_blob(d).decode())
        self.j = j
        self.run_id = self.doc['claim']['runId']
        self.run = st.objects[self.run_id]
        self.seal = st.objects[self.run['evaluationSealId']]
        self.proof = st.objects[self.seal['proofBundleId']]
        self.evidence = st.objects[self.run['evidenceId']]
        self.plan = st.objects[self.run['planId']]
        self.policy = j(self.plan['policyDigest'])
        self.ep = j(st.labels['enumeration-plan'])
        self.ei = j(st.labels['execution-inputs'])
        self.EI = K.cset(list(self.ei['selectedRefs'])
                         + [{'domain': 'execution-inputs',
                             'digest': self.proof['executionInputsDigest']}])
        self.universe_domain = {t.split('#', 1)[1]: t.split('#', 1)[0] for t in st.objects
                                if t.startswith('native.semantic-universe.') and '#' in t}
        self.facts, self.scopes, self.covs = {}, {}, {}
        for vid in self.evidence['viewIds']:
            v = st.objects[vid]
            for fid in v['facts']:
                self.facts[fid] = st.objects[fid]
            for sid in v['scopeIds']:
                self.scopes[sid] = st.objects[sid]
            for cid in v['coverageIds']:
                self.covs[cid] = st.objects[cid]
        for r in self.proof['evaluationInputRefs']:
            if r['domain'] == 'coverage' and 'coverage2:' + r['digest'] in st.objects:
                self.covs['coverage2:' + r['digest']] = st.objects['coverage2:' + r['digest']]
        self.fact_pay = {f: j(rec['payloadDigest']) for f, rec in self.facts.items()}
        self.cov_pay = {c: j(rec['payloadDigest']) for c, rec in self.covs.items()}
        self.subjects = {t: r for t, r in st.objects.items() if t.startswith('subject3:')}
        self.inventories = [j(r['digest']) for r in self.ei['selectedRefs']
                            if r['domain'] == 'subject-inventory']
        self.witness_cache = {}

    def witness(self, digest):
        if digest not in self.witness_cache:
            self.witness_cache[digest] = self.j(digest)
        return self.witness_cache[digest]


def node_at(root, addr):
    node = root
    for part in addr.split('.')[1:]:
        node = node['operand'] if node['op'] == 'not' else node['operands'][int(part)]
    return node


def occupies(R, relation, fid, subject):
    fact, pay = R.facts[fid], R.fact_pay[fid]
    field = PROJ['relations'][relation]['sourceField']
    nid = subject['nativeSubjectId']
    if field == 'anchors[0].path':
        return bool(fact['anchors']) and fact['anchors'][0]['path'] == nid
    if field == 'packageName':
        return pay.get('packageName') == nid and \
            pay.get('manifestPath') == subject.get('packageManifestPath')
    if field in ('path', 'declared', 'referrer', 'importer', 'caller', 'owner', 'origin',
                 'subject'):
        return pay.get(field) == nid
    raise NotExercised('SOURCE_FIELD:%s' % field)


def mapped_native(R, sid, addr, comp):
    rows = []
    for c in comp['causes']:
        rows.append({'source': 'native', 'cause': c['code'], 'subjectId': sid, 'predicateId': addr,
                     'inputRefs': R.EI, 'evidenceKind': None, 'nativeCause': c['nativeCause'],
                     'universe': c.get('universe')})
    for d in comp['nativeDeficiencies']:
        rows.append({'source': 'native', 'cause': d, 'subjectId': sid, 'predicateId': addr,
                     'inputRefs': R.EI, 'evidenceKind': None, 'nativeCause': None,
                     'universe': None})
    for cid in comp['coverageIds']:
        e = R.cov_pay[cid]['entry']
        if e['deficiency'] is not None:
            rows.append({'source': 'native', 'cause': e['deficiency'], 'subjectId': sid,
                         'predicateId': addr,
                         'inputRefs': [{'domain': 'coverage', 'digest': cid.split(':', 1)[1]}],
                         'evidenceKind': None, 'nativeCause': e['nativeCause'],
                         'universe': R.cov_pay[cid]['key']['sourceUniverse']})
    return K.cset(rows)


def program_predicate_digest(R, rid, addr, node):
    return K.rec_digest({'schemaVersion': 2, 'ruleProgramDigest': R.proof['ruleProgramDigest'],
                         'ruleId': rid, 'predicateId': addr, 'operation': node['op'],
                         'nodeDigest': K.rec_digest(node)})


def derive_native(R, f, rid, sid, addr, node, subject):
    rel, rung, op = node['relation'], node['minResolution'], node['op']
    if node.get('endpoint', 'source') != 'source':
        raise NotExercised('ENDPOINT_TARGET_IN_A_RETAINED_RUN')
    if node.get('filters'):
        raise NotExercised('NON_EMPTY_FILTERS_IN_A_RETAINED_RUN')
    f.need(subject['kind'] == PROJ['relations'][rel]['sourceSubjectKind'],
           'contract s4 "Wrong subject.kind ... is ATOM_KIND_INCOMPATIBLE"', 'ATOM_KIND_COMPATIBLE',
           {'rule': rid, 'addr': addr})
    U = subject['universe']
    known = sorted(fid for fid, fr in R.facts.items()
                   if fr['relation'] == rel and fr['sourceUniverse'] == U
                   and ladder_index(rel, fr['resolution']) >= ladder_index(rel, rung)
                   and occupies(R, rel, fid, subject))
    comp = outgoing(R, rel, rung, subject, quantifier(op, rung))
    value = truth(op, known, [], comp, node.get('n'))
    defs = mapped_native(R, sid, addr, comp)
    wit = {'schemaVersion': 3, 'programPredicateDigest': program_predicate_digest(R, rid, addr, node),
           'matchingFactIds': K.cset_strings(known),
           'coverageIds': K.cset_strings(comp['coverageIds']),
           'countLimit': node['n'] if op == 'count-at-most' else None,
           'childPredicateIds': [], 'matchingImportRows': [],
           'uncertainFactIds': [], 'uncertainImportRows': [], 'deficiencies': defs,
           'kind': 'native-atom'}
    return {'value': value, 'scopeIds': K.cset_strings(comp['scopeIds']), 'witness': wit,
            'completeness': comp, 'causes': comp['causes'], 'plane': 'native'}


def staleness(R, wrapper):
    corr = R.j(wrapper['sourceCorrespondenceDigest'])
    if corr['kind'] == 'exact-snapshot':
        if corr['snapshotId'] == R.plan['snapshotId']:
            return {'consumable': True, 'staleness': 'current'}, 'snapshot-equal'
        return {'consumable': False, 'staleness': 'stale'}, 'snapshot-differs'
    raise NotExercised('STALENESS_BRANCH:%s' % corr['kind'])


def in_import_scope(desc, path):
    def under(prefix):
        return prefix == '.' or path == prefix or path.startswith(prefix.rstrip('/') + '/')
    return (any(under(w) for w in desc['workspaceRoots'])
            and (not desc['pathPrefixes'] or any(under(p) for p in desc['pathPrefixes']))
            and not any(under(x) for x in desc['excludedPathPrefixes']))


def derive_imported(R, f, rid, sid, addr, node, subject):
    reg = EVREL[node['relation']]
    kind = reg['evidenceKind']
    passes = observability_filter(node['relation'], node.get('filters') or [])
    rows = [row for inv in R.inventories for row in inv['rows']
            if row['kind'] == subject['kind']
            and row['nativeSubjectId'] == subject['nativeSubjectId']]
    row = rows[0]
    owed = [iid for iid in R.plan['importIds']
            if R.st.objects[iid]['kind'] == kind
            and in_import_scope(R.j(R.st.objects[iid]['scopeDigest']), row['path'])]
    causes, known, uncertain, polarity = [], [], [], []
    if not owed:
        causes = [{'code': 'zero-owed-wrappers', 'evidenceKind': kind},
                  {'code': 'evidence-kind-unavailable', 'evidenceKind': kind}]
    for iid in owed:
        w = R.st.objects[iid]
        flags, _ = staleness(R, w)
        pay = R.j(w['payloadDigest'])
        hits = [(i, r) for i, r in enumerate(pay['subjects'])
                if r['path'] == row['path'] and (
                    ('symbol' not in r) if subject['kind'] == 'file'
                    else r.get('symbol') == row.get('qualifiedName'))]
        if not hits:
            if w['completeness'] != 'complete':
                causes.append({'code': 'wrapper-partial', 'evidenceKind': kind})
            causes.append({'code': 'unmapped-subject', 'evidenceKind': kind})
            continue
        i, r = hits[0]
        here = {'importId': iid, 'selector': 'runtime-subject', 'ordinal': i}
        if not flags['consumable']:
            causes += [{'code': 'import-unmapped-only', 'evidenceKind': kind},
                       {'code': 'no-consumable-row', 'evidenceKind': kind}]
            uncertain.append(here)
            continue
        if r['observability'] in QSET['neverInR']:
            causes.append({'code': 'unobservable-subject' if r['observability'] == 'unobservable'
                           else 'unmapped-subject', 'evidenceKind': kind})
            uncertain.append(here)
            continue
        if r['observability'] not in QSET[kind]:
            raise NotExercised('OBSERVABILITY_OUTSIDE_THE_POLARITY_SET:%s' % r['observability'])
        polarity.append(r['observability'])
        if passes(r['observability']):                              # A16: filtered R
            known.append(here)
        if w['completeness'] != 'complete':
            causes.append({'code': 'wrapper-partial', 'evidenceKind': kind})
        if pay.get('observationWindow') is None or pay.get('observedPopulation') in (None,
                                                                                       'unknown'):
            causes.append({'code': 'observation-window-insufficient', 'evidenceKind': kind})
    complete = bool(owed) and not causes and len(polarity) == len(owed) and not uncertain
    op = node['op']
    if op == 'exists':
        value = 'true' if known else ('false' if complete else 'indeterminate')
    elif op == 'none':
        value = 'false' if known else ('true' if complete else 'indeterminate')
    else:
        raise NotExercised('IMPORTED_OP:%s' % op)
    for c in causes:
        f.need(c['code'] in DEFREG['sources']['import'],
               'composition 9.5 rule 1 import-plane registry membership',
               'IMPORT_ATOM_CAUSE_REGISTERED', c)
    defs = K.cset([{'source': 'import', 'cause': c['code'], 'subjectId': sid,
                    'predicateId': addr, 'inputRefs': R.EI, 'evidenceKind': node['evidence'],
                    'nativeCause': None, 'universe': None} for c in causes])
    wit = {'schemaVersion': 3, 'programPredicateDigest': program_predicate_digest(R, rid, addr, node),
           'matchingFactIds': [], 'coverageIds': [], 'countLimit': None,
           'childPredicateIds': [], 'matchingImportRows': K.cset(known),
           'uncertainFactIds': [], 'uncertainImportRows': K.cset(uncertain),
           'deficiencies': defs, 'kind': 'imported-atom'}
    return {'value': value, 'scopeIds': [], 'witness': wit, 'plane': 'import',
            'causes': causes, 'polarityRows': polarity, 'filters': node.get('filters') or []}


def check_run(R, mutate=None):
    f = F()
    rules = {r['ruleId']: r for r in R.policy['rules']}
    rule_program = {'schemaVersion': 2, 'policyDigest': K.rec_digest(R.policy),
                    'rules': [{'ruleId': r['ruleId'], 'ruleProgramRef': r['ruleProgramRef'],
                               'emitWhen': r['emitWhen']} for r in R.policy['rules']]}
    f.need(K.rec_digest(rule_program) == R.proof['ruleProgramDigest'],
           'composition 9.1 RuleProgramV2 is the policy projection', 'RULE_PROGRAM_DIGEST_RECOMPUTES')
    rr = {x['ruleId']: x for x in R.proof['ruleResults']}
    records, schema_rows = [], {'AtomCauseV1': 0, 'evaluation-deficiency': 0,
                                'predicate-witness': 0}
    for pp in sorted(R.proof['predicateProofs'],
                     key=lambda p: (p['ruleId'], p['subjectId'], p['predicateId'])):
        rid, sid, addr = pp['ruleId'], pp['subjectId'], pp['predicateId']
        node = node_at(rules[rid]['emitWhen'], addr)
        if node['op'] in ('and', 'or', 'not'):
            continue
        subject = R.subjects.get(sid)
        where = {'rule': rid, 'subject': sid, 'addr': addr}
        if not f.need(subject is not None and K.ID('evaluation-subject', subject) == sid,
                      'identity-schemas.v3 evaluation-subject recomputes from the retained record',
                      'SUBJECT_IDENTITY_RECOMPUTES', where):
            continue
        f.need(any(row['kind'] == subject['kind']
                   and row['nativeSubjectId'] == subject['nativeSubjectId']
                   for inv in R.inventories for row in inv['rows']),
               'contract s1 subjects come from retained inventory rows',
               'SUBJECT_IS_A_RETAINED_INVENTORY_ROW', where)
        retained = copy.deepcopy(R.witness(pp['witnessDigest']))
        claimed = copy.deepcopy(pp)
        if mutate:
            retained, claimed = mutate(R, rid, sid, addr, node, retained, claimed)
        if node['relation'] in EVREL:
            d = derive_imported(R, f, rid, sid, addr, node, subject)
        else:
            d = derive_native(R, f, rid, sid, addr, node, subject)
            for c in d['causes']:
                a = admit(PROJ_DOC, '#/$defs/AtomCauseV1', c)
                schema_rows['AtomCauseV1'] += 1
                f.need(a['admitted'], 'registry $defs/AtomCauseV1 (reference validator)',
                       'ATOM_CAUSE_ADMITTED_BY_ITS_OWNING_SCHEMA', dict(where, cause=c, **a))
                f.need(c['code'] in DEFREG['sources']['native'] and c['evidenceKind'] is None,
                       'composition 9.5 rule 1 native-plane membership, evidenceKind null',
                       'NATIVE_ATOM_CAUSE_REGISTERED', dict(where, cause=c))
        for row in d['witness']['deficiencies']:
            a = admit(IDENT_DOC, '#/$defs/evaluation-deficiency', row)
            schema_rows['evaluation-deficiency'] += 1
            f.need(a['admitted'], 'identity-schemas.v3 evaluation-deficiency',
                   'DERIVED_DEFICIENCY_ADMITTED', dict(where, **a))
        a = admit(IDENT_DOC, '#/$defs/predicate-witness', d['witness'])
        schema_rows['predicate-witness'] += 1
        f.need(a['admitted'], 'identity-schemas.v3 predicate-witness', 'DERIVED_WITNESS_ADMITTED',
               dict(where, **a))
        f.need(d['value'] == claimed['value'], 'A1/A16 value', 'PREDICATE_VALUE_EQUALS_DERIVED',
               dict(where, derived=d['value'], retained=claimed['value']))
        f.need(d['scopeIds'] == claimed['scopeIds'], 'A8 scopeIds', 'PREDICATE_SCOPE_IDS_EQUAL_DERIVED',
               dict(where, derived=d['scopeIds'], retained=claimed['scopeIds']))
        same = K.C(d['witness']) == K.C(retained)
        diff = None
        if not same:
            diff = {k: {'derived': d['witness'][k], 'retained': retained.get(k)}
                    for k in d['witness'] if K.C(d['witness'][k]) != K.C(retained.get(k))}
        f.need(same, 'A2-A16 COMPLETE witness record equals the derivation',
               'WITNESS_RECORD_EQUALS_DERIVED', dict(where, fieldDifferences=diff))
        f.need(K.rec_digest(d['witness']) == claimed['witnessDigest'],
               'composition: witnessDigest names the derived record', 'WITNESS_DIGEST_EQUALS_DERIVED',
               where)
        rdefs = {K.C(x) for x in rr[rid]['deficiencies']}
        f.need(all(K.C(x) in rdefs for x in d['witness']['deficiencies']),
               'composition 9.5: atom rows are copied into the rule deficiencies',
               'RULE_DEFICIENCIES_CONTAIN_THE_ATOM_ROWS', where)
        records.append({'rule': rid, 'subject': sid, 'nativeSubjectId': subject['nativeSubjectId'],
                        'predicateId': addr, 'op': node['op'], 'relation': node['relation'],
                        'plane': d['plane'], 'value': d['value'], 'scopeIds': d['scopeIds'],
                        'causes': d['causes'],
                        'completeness': ({k: d['completeness'][k] for k in
                                          ('complete', 'unknown', 'returned', 'coverageIds',
                                           'scopeIds', 'nativeDeficiencies', 'views')}
                                         if d['plane'] == 'native' else None),
                        'polarityRows': d.get('polarityRows'), 'filters': d.get('filters'),
                        'witnessDigest': K.rec_digest(d['witness'])})
    return f, records, schema_rows


# ------------------------------------------------------------------------ synthetic law vectors
class Synth:
    """A typed synthetic input model -- a HELPER-ONLY observation, not a Run -- carrying exactly
    the attributes the derivation reads."""

    def __init__(self, cells, scopes=None, covs=None, domains=None):
        self.ep = {'cells': cells}
        self.scopes = scopes or {}
        for s in self.scopes.values():
            if s.pop('_absentCarrier', False):
                s.pop('enumeratorClosure', None)
            elif 'enumeratorClosure' not in s:
                s['enumeratorClosure'] = PROVIDER
        self.covs, self.cov_pay = {}, {}
        for cid, (scope_id, key, entry) in (covs or {}).items():
            self.covs[cid] = {'scopeId': scope_id}
            self.cov_pay[cid] = {'key': key, 'entry': entry}
        self.universe_domain = domains or {}


TS_U, RS_U, SX_U = 'a' * 64, 'b' * 64, 'c' * 64
DOMAINS = {TS_U: 'native.semantic-universe.typescript.v2', RS_U: 'native.semantic-universe.rust.v2',
           SX_U: 'native.semantic-universe.syntax.v2'}


def sid(n):
    return 'scope2:' + n * 64


def cid(n):
    return 'coverage2:' + n * 64


def entry(rel, rung, coverage='complete', deficiency=None, nc=None, state='not-applicable',
          attempted=False, count=0, exports='closed', kinds=(), conf=1000000, marker='first'):
    return {'relation': rel, 'resolution': rung, 'coverage': coverage,
            'examinedUniverse': {'subjectScopeCommitment': 'sha256:' + '0' * 64,
                                 'subjectCount': 1, 'marker': marker},
            'resolutionCompleteness': {'state': state, 'attempted': attempted,
                                       'examinedExhaustive': True, 'stageTerminal': 'complete',
                                       'unresolvedEdgeCount': count, 'unresolvedEdgeClasses': []},
            'closedWorld': {'exportsClosed': exports, 'marker': marker},
            'derivationKinds': list(kinds), 'confidenceMillionths': conf,
            'deficiency': deficiency, 'nativeCause': nc}


def key(rel, rung, S_, T_):
    return {'relation': rel, 'resolution': rung, 'sourceUniverse': S_, 'targetUniverse': T_,
            'subjectScopeCommitment': 'sha256:' + '0' * 64}


def law_vectors():
    rows = []

    def vec(name, clause, derived, expected, control=None):
        ok = all(K.C(derived.get(k)) == K.C(v) for k, v in expected.items())
        rows.append({'vector': name, 'clause': clause, 'standing': 'SYNTHETIC helper-only input',
                     'expected': expected,
                     'derived': {k: derived.get(k) for k in expected},
                     'result': 'PASS' if ok else 'FAIL', 'control': control})

    # LV1 selection order: the scope walk would hand the fold a DESCENDING Coverage order
    cells = [{'capabilityId': 'reachability', 'languageMode': 'rust-cargo',
              'programBindings': [{'universe': RS_U}]},
             {'capabilityId': 'calls', 'languageMode': 'rust-cargo',
              'programBindings': [{'universe': RS_U}]}]
    subj = {'universe': RS_U, 'kind': 'symbol', 'nativeSubjectId': 'rs:c::f'}
    scopes = {sid('1'): {'relation': 'reachability', 'resolution': 'from-resolved-calls',
                         'sourceUniverse': RS_U, 'subjects': ['rs:c::f']},
              sid('2'): {'relation': 'calls', 'resolution': 'resolved-callee',
                         'sourceUniverse': RS_U, 'subjects': ['rs:c::f']},
              sid('3'): {'relation': 'calls', 'resolution': 'resolved-callee',
                         'sourceUniverse': RS_U, 'subjects': ['rs:c::f']}}
    covs = {cid('9'): (sid('1'), key('reachability', 'from-resolved-calls', RS_U, RS_U),
                       entry('reachability', 'from-resolved-calls', state='complete',
                             attempted=True)),
            # the LOWER scope pairs the HIGHER Coverage
            cid('f'): (sid('2'), key('calls', 'resolved-callee', RS_U, RS_U),
                       entry('calls', 'resolved-callee', coverage='unknown',
                             deficiency='provider-unavailable', state='complete',
                             attempted=True, marker='f')),
            cid('0'): (sid('3'), key('calls', 'resolved-callee', RS_U, RS_U),
                       entry('calls', 'resolved-callee', coverage='unknown',
                             deficiency='input-closure-incomplete', nc='no-program-unit',
                             state='complete', attempted=True, marker='0'))}
    R = Synth(cells, scopes, covs, DOMAINS)
    comp = outgoing(R, 'reachability', 'from-resolved-calls', subj, 'universal-negative')
    walk = [c for s in sorted(scopes) if scopes[s]['relation'] == 'calls'
            for c in sorted(x for x, rec in R.covs.items() if rec['scopeId'] == s)]
    walk_fold = fold([R.cov_pay[c]['entry'] for c in walk])
    vec('selection-order-ascending-coverage2-after-pairing',
        'A2 + A10 + A11 + A12', {
            'dependencyCoverageOrder': comp['views'][0]['positions'][1]['coverageIds'],
            'causes': comp['causes'], 'nativeDeficiencies': comp['nativeDeficiencies']},
        {'dependencyCoverageOrder': [cid('0'), cid('f')],
         'causes': [cause('coverage-unknown', RS_U, 'no-program-unit')],
         'nativeDeficiencies': ['input-closure-incomplete']},
        control={'reading': 'fold in scope-walk order', 'walkOrder': walk,
                 'carrierItWouldPick': [walk_fold['deficiency'], walk_fold['nativeCause']],
                 'refused': [walk_fold['deficiency'], walk_fold['nativeCause']]
                 != ['input-closure-incomplete', 'no-program-unit'],
                 'firstRefusal': 'FOLD_CARRIER_IS_NOT_THE_ASCENDING_FIRST_PARTITION'})

    # LV2 fold field rules
    e1 = entry('calls', 'resolved-callee', state='complete', attempted=True, marker='one',
               kinds=['annotated'], conf=900000, exports='closed')
    e2 = entry('calls', 'resolved-callee', state='not-applicable', attempted=False, marker='two',
               deficiency='provider-unavailable', exports='unknown', kinds=['compiler-inferred',
                                                                            'annotated'])
    e3 = entry('calls', 'resolved-callee', state='incomplete', attempted=True, count=3,
               marker='three', deficiency='input-closure-incomplete', nc='no-program-unit',
               exports='open', conf=500000, coverage='unknown')
    e4 = entry('calls', 'resolved-callee', state='partial', attempted=True, count=9, marker='four')
    fo = fold([e1, e2, e3, e4])
    vec('fold-field-rules', 'A11', {
        'coverage': fo['coverage'], 'confidenceMillionths': fo['confidenceMillionths'],
        'resolutionCompleteness': fo['resolutionCompleteness'],
        'closedWorld': fo['closedWorld'], 'derivationKinds': fo['derivationKinds'],
        'carrier': [fo['deficiency'], fo['nativeCause']],
        'examinedUniverse': fo['examinedUniverse']},
        {'coverage': 'unknown', 'confidenceMillionths': 500000,
         'resolutionCompleteness': e3['resolutionCompleteness'],
         'closedWorld': e2['closedWorld'], 'derivationKinds': ['annotated', 'compiler-inferred'],
         'carrier': ['provider-unavailable', None], 'examinedUniverse': e1['examinedUniverse']},
        control={'reading': 'unzip the carrier / merge resolutionCompleteness field by field',
                 'unzippedCarrier': ['provider-unavailable', 'no-program-unit'],
                 'fieldMergedUnresolvedCount': 9,
                 'refused': fo['nativeCause'] != 'no-program-unit'
                 and fo['resolutionCompleteness']['unresolvedEdgeCount'] == 3,
                 'firstRefusal': 'FOLD_CARRIER_UNZIPPED_ACROSS_PARTITIONS'})
    tie = fold([e1, e2])
    vec('fold-tie-keeps-incumbent-record-whole', 'A11 "complete/not-applicable" tie',
        {'resolutionCompleteness': tie['resolutionCompleteness']},
        {'resolutionCompleteness': e1['resolutionCompleteness']})

    # LV3 unpaired sibling + completeness independent of truth
    cells = [{'capabilityId': 'clones-fact', 'languageMode': 'ts-tsconfig',
              'programBindings': [{'universe': TS_U}]}]
    subj = {'universe': TS_U, 'kind': 'file', 'nativeSubjectId': 'src/a.ts'}
    scopes = {sid('1'): {'relation': 'clones', 'resolution': 'normalized-body-hash',
                         'sourceUniverse': TS_U, 'subjects': ['src/a.ts']},
              sid('2'): {'relation': 'clones', 'resolution': 'normalized-body-hash',
                         'sourceUniverse': TS_U, 'subjects': ['src/a.ts']}}
    covs = {cid('1'): (sid('1'), key('clones', 'normalized-body-hash', TS_U, TS_U),
                       entry('clones', 'normalized-body-hash'))}
    R = Synth(cells, scopes, covs, DOMAINS)
    comp = outgoing(R, 'clones', 'normalized-body-hash', subj, 'existential')
    vec('unpaired-sibling-returns-with-every-scope-and-no-coverage', 'A8 + A1', {
        'causes': comp['causes'], 'scopeIds': comp['scopeIds'], 'coverageIds': comp['coverageIds'],
        'returned': comp['returned'],
        'existsWithAKnownFact': truth('exists', ['fact2:x'], [], comp),
        'noneWithAKnownFact': truth('none', ['fact2:x'], [], comp),
        'noneWithNoFact': truth('none', [], [], comp)},
        {'causes': [cause('scope-without-coverage', TS_U)], 'scopeIds': [sid('1'), sid('2')],
         'coverageIds': [], 'returned': 'outgoing-3', 'existsWithAKnownFact': 'true',
         'noneWithAKnownFact': 'false', 'noneWithNoFact': 'indeterminate'},
        control={'reading': 'cite the paired sibling Coverage and skip the unpaired scope',
                 'refused': comp['coverageIds'] == [] and len(comp['scopeIds']) == 2,
                 'firstRefusal': 'STEP3_RETURN_CITED_A_SIBLING_COVERAGE'})

    # LV4 P1 cross-family (non-blocking) and LV5 owed-family unavailable (outgoing silent,
    # incoming blocking)
    cells = [{'capabilityId': 'clones-fact', 'languageMode': 'ts-tsconfig',
              'programBindings': [{'universe': TS_U}]},
             {'capabilityId': 'clones-fact', 'languageMode': 'rust-cargo',
              'programBindings': [{'universe': None}]},
             {'capabilityId': 'clones-fact', 'languageMode': 'js-allowjs',
              'programBindings': [{'universe': None}]}]
    R = Synth(cells, scopes={sid('1'): scopes[sid('1')]},
              covs={cid('1'): covs[cid('1')],
                    # the clones view owes declares@syntactic (A13); declares is a different
                    # source kind, so its partition is whole-source (S, T)
                    cid('d'): ('scope2:' + 'd' * 64, key('declares', 'syntactic', TS_U, TS_U),
                               entry('declares', 'syntactic'))}, domains=DOMAINS)
    comp = outgoing(R, 'clones', 'normalized-body-hash', subj, 'existential')
    vec('p1-cross-family-disclosed-owed-family-silent-outgoing', 'A4', {
        'causes': comp['causes'], 'complete': comp['complete'],
        'none': truth('none', [], [], comp)},
        {'causes': [cause('cross-family-edge-not-owed')], 'complete': True, 'none': 'true'},
        control={'reading': 'treat the cross-family disclosure as blocking',
                 'wouldYield': 'indeterminate', 'refused': comp['complete'],
                 'firstRefusal': 'NON_BLOCKING_DISCLOSURE_TREATED_AS_BLOCKING'})
    inc = incoming({'R': R, 'U': TS_U, 'relation': 'clones', 'rung': 'normalized-body-hash',
                    'groups': []})
    vec('p1-owed-family-unavailable-blocks-incoming', 'A4 + A17', {
        'causeCodes': sorted(c['code'] for c in inc['causes']), 'complete': inc['complete']},
        {'causeCodes': ['cross-family-edge-not-owed', 'unavailable-program-binding'],
         'complete': False})

    # LV6 P2 shared return, both endpoints
    R = Synth([{'capabilityId': 'syntax', 'languageMode': 'ts-tsconfig',
                'programBindings': [{'universe': TS_U}]}], domains=DOMAINS)
    out_c = outgoing(R, 'clones', 'normalized-body-hash', subj, 'existential')
    in_c = incoming({'R': R, 'U': TS_U, 'relation': 'clones', 'rung': 'normalized-body-hash',
                     'groups': [{'S': TS_U, 'scopes': [], 'attestation': None}]})
    vec('p2-shared-return-taken-by-both-endpoints', 'A5 + A1 three-valued', {
        'outgoing': [out_c['causes'], out_c['returned']],
        'incoming': [in_c['causes'], in_c['returned']],
        'existsWithNoMatch': truth('exists', [], [], out_c),
        'noneWithNoMatch': truth('none', [], [], out_c)},
        {'outgoing': [[cause('missing-relation-coverage')], 'P2'],
         'incoming': [[cause('missing-relation-coverage')], 'P2'],
         'existsWithNoMatch': 'indeterminate', 'noneWithNoMatch': 'indeterminate'},
        control={'reading': 'incoming skips P2 and reports search accounting instead',
                 'refused': in_c['returned'] == 'P2',
                 'firstRefusal': 'INCOMING_DID_NOT_TAKE_THE_SHARED_P2_RETURN'})

    # LV7 step 1
    R = Synth([{'capabilityId': 'clones-fact', 'languageMode': 'ts-tsconfig',
                'programBindings': [{'universe': 'd' * 64}]}], domains=DOMAINS)
    comp = outgoing(R, 'clones', 'normalized-body-hash', subj, 'existential')
    vec('step1-selector-unbound-null-universe', 'A6 + A3', {'causes': comp['causes']},
        {'causes': [cause('selector-unbound')]})

    # LV8 cause representation
    reps = [admit(PROJ_DOC, '#/$defs/AtomCauseV1', c) for c in (
        {'code': 'selector-unbound', 'evidenceKind': None, 'nativeCause': None},
        {'code': 'selector-unbound', 'evidenceKind': None, 'nativeCause': None, 'universe': None},
        {'code': 'scope-without-coverage', 'evidenceKind': None, 'nativeCause': None,
         'universe': TS_U})]
    bad = admit(PROJ_DOC, '#/$defs/AtomCauseV1',
                {'code': 'selector-unbound', 'evidenceKind': None, 'nativeCause': 'untyped'})
    vec('cause-representation-omitted-null-and-hex-all-admit', 'A3',
        {'admitted': [r['admitted'] for r in reps],
         'projectedUniverse': [c.get('universe') for c in (
             cause('selector-unbound'), cause('scope-without-coverage', TS_U))],
         'untypedNativeCauseRefused': not bad['admitted']},
        {'admitted': [True, True, True], 'projectedUniverse': [None, TS_U],
         'untypedNativeCauseRefused': True})

    # LV9 incoming search-accounting table
    cells = [{'capabilityId': 'imports', 'languageMode': 'ts-tsconfig',
              'programBindings': [{'universe': TS_U}]},
             {'capabilityId': 'imports', 'languageMode': 'ts-tsconfig',
              'programBindings': [{'universe': 'e' * 64}]},
             {'capabilityId': 'imports', 'languageMode': 'rust-cargo',
              'programBindings': [{'universe': None}]}]
    doms = dict(DOMAINS, **{'e' * 64: 'native.semantic-universe.typescript.v2'})
    R = Synth(cells, domains=doms)
    ok_entry = entry('imports', 'resolved-target', state='complete', attempted=True)
    q = {'completeSearch': True, 'coverage': 'complete', 'examinedExhaustive': True,
         'rcExaminedExhaustive': True, 'entry': ok_entry}
    nq = dict(q, completeSearch=False)
    V = 'e' * 64

    def acct(groups):
        r = incoming({'R': R, 'U': TS_U, 'relation': 'imports', 'rung': 'resolved-target',
                      'groups': groups})
        # lists, not tuples: the vector is compared through canonical JSON, which refuses tuples
        return [sorted([c['code'], c.get('universe')] for c in r['causes']
                       if c['code'] != 'cross-family-edge-not-owed'), r['complete']]
    cases = {
        'no-source-scopes-no-attestation': acct([{'S': V, 'scopes': [], 'attestation': None}]),
        'no-source-scopes-qualifying-attestation': acct([{'S': V, 'scopes': [], 'attestation': q}]),
        'scope-paired-only-S-to-V-no-attestation': acct([{'S': V, 'attestation': None, 'scopes': [
            {'id': sid('4'), 'paired': [{'id': cid('4'), 'V': V, 'entry': ok_entry}]}]}]),
        'scope-paired-only-S-to-V-qualifying-attestation': acct([{'S': V, 'attestation': q,
                                                                  'scopes': [
            {'id': sid('4'), 'paired': [{'id': cid('4'), 'V': V, 'entry': ok_entry}]}]}]),
        'scope-no-coverage-no-attestation': acct([{'S': V, 'attestation': None, 'scopes': [
            {'id': sid('5'), 'paired': []}]}]),
        'scope-no-coverage-non-qualifying-attestation': acct([{'S': V, 'attestation': nq,
                                                               'scopes': [
            {'id': sid('5'), 'paired': []}]}]),
        'one-partition-S-to-U-does-not-skip-a-sibling-with-only-S-to-V': acct([{
            'S': V, 'attestation': None, 'scopes': [
                {'id': sid('6'), 'paired': [{'id': cid('6'), 'V': TS_U, 'entry': ok_entry}]},
                {'id': sid('7'), 'paired': [{'id': cid('7'), 'V': V, 'entry': ok_entry}]}]}]),
    }
    vec('incoming-search-accounting-table', 'A17 table rows 1-3 + "does not skip" + '
        '"non-qualifying is insufficient under the same cases as an absent one"', cases, {
            'no-source-scopes-no-attestation': [[['source-target-search-unattested', V]], False],
            'no-source-scopes-qualifying-attestation': [[], True],
            'scope-paired-only-S-to-V-no-attestation':
                [[['source-target-search-unattested', V]], False],
            'scope-paired-only-S-to-V-qualifying-attestation': [[], True],
            'scope-no-coverage-no-attestation': [[['scope-without-coverage', V]], False],
            'scope-no-coverage-non-qualifying-attestation': [[['scope-without-coverage', V]],
                                                             False],
            'one-partition-S-to-U-does-not-skip-a-sibling-with-only-S-to-V':
                [[['source-target-search-unattested', V]], False]},
        control={'reading': 'treat S->V Coverage as search of U',
                 'refused': cases['scope-paired-only-S-to-V-no-attestation'][1] is False,
                 'firstRefusal': 'S_TO_V_COVERAGE_TREATED_AS_SEARCH_OF_U'})
    cross = incoming({'R': Synth(cells + [{'capabilityId': 'imports', 'languageMode': 'rust-cargo',
                                           'programBindings': [{'universe': RS_U}]}],
                                 domains=doms),
                      'U': TS_U, 'relation': 'imports', 'rung': 'resolved-target',
                      'groups': [{'S': RS_U, 'scopes': [], 'attestation': None}]})
    vec('incoming-two-cross-family-routes-both-retained', 'A17',
        {'crossFamily': sorted([c.get('universe') or '' for c in cross['causes']
                                if c['code'] == 'cross-family-edge-not-owed'])},
        {'crossFamily': ['', RS_U]})

    # ============================================================ generation-23 clauses
    def refusal_of(fn):
        try:
            fn()
            return 'ADMITTED'
        except Refusal as e:
            return e.code

    def codes(r):
        return sorted([c['code'], c.get('universe') or ''] for c in r['causes'])

    # LV10 A13: an absent dependency answers required-relation-missing (withdraws I-A1)
    ccells = [{'capabilityId': 'clones-fact', 'languageMode': 'ts-tsconfig',
               'programBindings': [{'universe': TS_U}]}]
    csubj = {'universe': TS_U, 'kind': 'file', 'nativeSubjectId': 'src/a.ts'}
    R = Synth(ccells, {sid('1'): {'relation': 'clones', 'resolution': 'normalized-body-hash',
                                  'sourceUniverse': TS_U, 'subjects': ['src/a.ts']}},
              {cid('1'): (sid('1'), key('clones', 'normalized-body-hash', TS_U, TS_U),
                          entry('clones', 'normalized-body-hash'))}, DOMAINS)
    comp = outgoing(R, 'clones', 'normalized-body-hash', csubj, 'existential')
    vec('absent-dependency-answers-required-relation-missing', 'A13 (withdraws I-A1)', {
        'positions': [p['relation'] for p in comp['views'][0]['positions']],
        'causes': comp['causes'], 'nativeDeficiencies': comp['nativeDeficiencies'],
        'none': truth('none', [], [], comp),
        'noneWithAKnownFact': truth('none', ['fact2:x'], [], comp)},
        {'positions': ['clones'], 'causes': [cause('coverage-unknown', TS_U)],
         'nativeDeficiencies': ['required-relation-missing'], 'none': 'indeterminate',
         'noneWithAKnownFact': 'false'},
        control={'reading': 'I-A1 (generation 22): an absent dependency adds no cause',
                 'wouldYield': 'true', 'refused': comp['complete'] is False,
                 'firstRefusal': 'ABSENT_DEPENDENCY_READ_AS_NO_CAUSE'})

    # LV11 A20: exact dependency scopes pair by mapping or commitment; no mapped-scope fallback
    rcells = [{'capabilityId': 'reachability', 'languageMode': 'rust-cargo',
               'programBindings': [{'universe': RS_U}]},
              {'capabilityId': 'calls', 'languageMode': 'rust-cargo',
               'programBindings': [{'universe': RS_U}]}]
    rsubj = {'universe': RS_U, 'kind': 'symbol', 'nativeSubjectId': 'rs:c::f'}

    def base_scopes():
        return {sid('1'): {'relation': 'reachability', 'resolution': 'from-resolved-calls',
                           'sourceUniverse': RS_U, 'subjects': ['rs:c::f']},
                sid('2'): {'relation': 'calls', 'resolution': 'resolved-callee',
                           'sourceUniverse': RS_U, 'subjects': ['rs:c::f']},
                sid('3'): {'relation': 'calls', 'resolution': 'syntactic-callee-name',
                           'sourceUniverse': RS_U, 'subjects': ['rs:c::f']}}
    reach = (sid('1'), key('reachability', 'from-resolved-calls', RS_U, RS_U),
             entry('reachability', 'from-resolved-calls', state='complete', attempted=True))
    calls_entry = entry('calls', 'resolved-callee', state='complete', attempted=True)
    ckey = key('calls', 'resolved-callee', RS_U, RS_U)
    commit2 = dict(ckey, subjectScopeCommitment='sha256:' + '2' * 64)

    def reach_view(dep_covs, scopes_=None):
        R_ = Synth(rcells, scopes_ or base_scopes(), dict({cid('1'): reach}, **dep_covs), DOMAINS)
        c_ = outgoing(R_, 'reachability', 'from-resolved-calls', rsubj, 'universal-negative')
        return [[p['relation'] for p in c_['views'][0]['positions']], c_['nativeDeficiencies']]
    pairing = {
        'mapped-to-a-scope-outside-the-exact-selection':
            reach_view({cid('2'): (sid('3'), ckey, calls_entry)}),
        'mapped-to-the-exact-scope': reach_view({cid('2'): (sid('2'), ckey, calls_entry)}),
        'paired-by-commitment-to-the-exact-scope': reach_view({cid('2'): (None, commit2,
                                                                          calls_entry)}),
        'mapping-then-commitment': reach_view({cid('2'): (sid('2'), ckey, calls_entry),
                                               cid('3'): (None, commit2, calls_entry)}),
        'commitment-then-mapping': reach_view({cid('3'): (sid('2'), ckey, calls_entry),
                                               cid('2'): (None, commit2, calls_entry)}),
    }
    present = [['reachability', 'calls'], []]
    vec('dependency-pairing-no-mapped-scope-fallback', 'A20 + A13', pairing, {
        'mapped-to-a-scope-outside-the-exact-selection':
            [['reachability'], ['required-relation-missing']],
        'mapped-to-the-exact-scope': present, 'paired-by-commitment-to-the-exact-scope': present,
        'mapping-then-commitment': present, 'commitment-then-mapping': present},
        control={'reading': 'fall back to the mapped scope whatever its (relation, rung, S)',
                 'refused': pairing['mapped-to-a-scope-outside-the-exact-selection'][0]
                 == ['reachability'],
                 'firstRefusal': 'MAPPED_SCOPE_FALLBACK_PAIRED_A_NON_EXACT_SCOPE'})

    # LV12 A19 carrier on both endpoints and at attestation admission
    null_primary = base_scopes()
    null_primary[sid('1')]['enumeratorClosure'] = None
    absent_dep = base_scopes()
    absent_dep[sid('2')]['_absentCarrier'] = True
    V2 = 'e' * 64
    doms = dict(DOMAINS, **{V2: 'native.semantic-universe.typescript.v2'})
    rc = {'state': 'complete', 'attempted': True, 'examinedExhaustive': True,
          'stageTerminal': 'complete', 'unresolvedEdgeCount': 0, 'unresolvedEdgeClasses': []}
    cw = {'exportsClosed': 'closed', 'entryPointsRecognized': 'all', 'nonliteralLoading': 'none',
          'externalConsumers': 'none-declared', 'dynamicDispatch': 'resolved', 'reasons': [],
          'deadCodeRepairEligible': True}

    def ts_cell(u, mode='ts-tsconfig'):
        return {'capabilityId': 'imports', 'languageMode': mode, 'programBindings': [{'universe': u}]}

    def rs_cell(u):
        return ts_cell(u, 'rust-cargo')

    def att_record(scope_refs):
        return {'schemaVersion': 1, 'planId': 'plan2:' + '1' * 64, 'providerClosure': PROVIDER,
                'sourceUniverse': V2, 'targetUniverse': TS_U, 'relation': 'imports',
                'minResolution': 'resolved-target', 'scopeRefs': scope_refs,
                'expectedInventoryRefs': ['2' * 64], 'completeSearch': True,
                'examinedExhaustive': True, 'coverage': 'complete',
                'resolutionCompleteness': rc, 'closedWorld': cw}
    imp_scope = {'relation': 'imports', 'resolution': 'resolved-target', 'sourceUniverse': V2}
    carriers = {
        'outgoing-primary-scope-null': refusal_of(lambda: outgoing(
            Synth(rcells, null_primary, {cid('1'): reach}, DOMAINS), 'reachability',
            'from-resolved-calls', rsubj, 'universal-negative')),
        'outgoing-exact-dependency-scope-absent': refusal_of(lambda: outgoing(
            Synth(rcells, absent_dep, {cid('1'): reach, cid('2'): (sid('2'), ckey, calls_entry)},
                  DOMAINS), 'reachability', 'from-resolved-calls', rsubj, 'universal-negative')),
        'incoming-dependency-scope-null': refusal_of(lambda: incoming_view(
            Synth(rcells, {sid('2'): {'relation': 'calls', 'resolution': 'resolved-callee',
                                      'sourceUniverse': RS_U, 'subjects': ['rs:c::g'],
                                      'enumeratorClosure': None}},
                  {cid('2'): (sid('2'), ckey, calls_entry)}, DOMAINS),
            'reachability', 'from-resolved-calls', RS_U, RS_U, ['rs:c::g'], reach[2])),
        'attestation-names-a-null-carrier-scope-its-atom-never-pairs': refusal_of(
            lambda: admit_attestation(Synth([ts_cell(TS_U), ts_cell(V2)], {
                sid('7'): dict(imp_scope, subjects=['x'], enumeratorClosure=None)},
                domains=doms), att_record([sid('7')]))),
        'empty-scopeRefs-for-a-scope-less-group': refusal_of(
            lambda: admit_attestation(Synth([ts_cell(TS_U), ts_cell(V2)], domains=doms),
                                      att_record([]))),
        'nonempty-scopeRefs-for-a-scope-less-group': refusal_of(
            lambda: admit_attestation(Synth([ts_cell(TS_U), ts_cell(V2)], domains=doms),
                                      att_record([sid('8')]))),
        'attestation-naming-the-explicit-empty-subject-scope': refusal_of(
            lambda: admit_attestation(Synth([ts_cell(TS_U), ts_cell(V2)], {
                sid('6'): dict(imp_scope, subjects=[])}, domains=doms), att_record([sid('6')]))),
    }
    vec('admitted-input-shapes-carrier-and-attestation-admission', 'A19', carriers, {
        'outgoing-primary-scope-null': 'ATOM_NATIVE_CARRIER',
        'outgoing-exact-dependency-scope-absent': 'ATOM_NATIVE_CARRIER',
        'incoming-dependency-scope-null': 'ATOM_NATIVE_CARRIER',
        'attestation-names-a-null-carrier-scope-its-atom-never-pairs': 'ATOM_NATIVE_CARRIER',
        'empty-scopeRefs-for-a-scope-less-group': 'INCOMING_SEARCH_SCHEMA',
        'nonempty-scopeRefs-for-a-scope-less-group': 'INCOMING_SEARCH_SCOPE_MISJOIN',
        'attestation-naming-the-explicit-empty-subject-scope': 'ADMITTED'},
        control={'reading': 'a missing enumeratorClosure means "no commitment"',
                 'refused': carriers['outgoing-primary-scope-null'] == 'ATOM_NATIVE_CARRIER',
                 'firstRefusal': 'ATOM_NATIVE_CARRIER'})

    ok_imp = entry('imports', 'resolved-target', state='complete', attempted=True)

    def inc(cells_, groups):
        return incoming({'R': Synth(cells_, domains=doms), 'U': TS_U, 'relation': 'imports',
                         'rung': 'resolved-target', 'groups': groups})
    closes = {
        'explicit-empty-subject-scope-with-complete-S-to-U-coverage':
            inc([ts_cell(TS_U), ts_cell(V2)], [{'S': V2, 'attestation': None, 'scopes': [
                {'id': sid('6'), 'subjects': [], 'paired': [{'id': cid('6'), 'V': TS_U,
                                                             'entry': ok_imp}]}]}]),
        'explicit-empty-subject-scope-named-by-a-qualifying-attestation':
            inc([ts_cell(TS_U), ts_cell(V2)], [{'S': V2, 'attestation': q, 'scopes': [
                {'id': sid('6'), 'subjects': [], 'paired': []}]}]),
        'scope-less-group-with-no-admissible-attestation':
            inc([ts_cell(TS_U), ts_cell(V2)], [{'S': V2, 'attestation': None, 'scopes': []}]),
    }
    vec('explicit-empty-subject-scope-closes-an-empty-program', 'A19',
        {k: [codes(v), v['complete']] for k, v in closes.items()}, {
            'explicit-empty-subject-scope-with-complete-S-to-U-coverage': [[], True],
            'explicit-empty-subject-scope-named-by-a-qualifying-attestation': [[], True],
            'scope-less-group-with-no-admissible-attestation':
                [[['source-target-search-unattested', V2]], False]})

    # LV13 A18 I1
    grp_v2 = {'S': V2, 'attestation': None, 'scopes': [
        {'id': sid('4'), 'paired': [{'id': cid('4'), 'V': TS_U, 'entry': ok_imp}]}]}
    grp_v2b = {'S': V2, 'attestation': None, 'scopes': [
        {'id': sid('5'), 'paired': [{'id': cid('5'), 'V': TS_U, 'entry': ok_imp}]}]}
    rs_group = {'S': RS_U, 'scopes': [], 'attestation': None}
    i1 = {
        'same-family-U2-evidenced-only': inc([ts_cell(V2)], [grp_v2]),
        'foreign-family-only-available': inc([rs_cell(RS_U)], [rs_group]),
        'foreign-family-only-unavailable': inc([rs_cell(None)], []),
        'foreign-family-only-available-and-unavailable': inc([rs_cell(RS_U), rs_cell(None)],
                                                              [rs_group]),
        'beside-an-owed-family-unavailable-obligation':
            inc([ts_cell(V2), ts_cell(None, 'js-allowjs')], [grp_v2]),
        'beside-an-unknown-family-obligation':
            inc([ts_cell(V2), ts_cell(None, 'no-registered-mode')], [grp_v2]),
        'subject-universe-bound-unchanged': inc([ts_cell(TS_U)], [{'S': TS_U, 'attestation': None,
                                                                    'scopes': [
            {'id': sid('5'), 'paired': [{'id': cid('5'), 'V': TS_U, 'entry': ok_imp}]}]}]),
    }
    su = ['selector-unbound', '']
    vec('incoming-i1-subject-universe-unbound', 'A18',
        {k: [codes(v), v['complete'], v['returned']] for k, v in i1.items()}, {
            'same-family-U2-evidenced-only': [[su], False, None],
            'foreign-family-only-available':
                [[['cross-family-edge-not-owed', RS_U], su], False, None],
            'foreign-family-only-unavailable': [[['cross-family-edge-not-owed', ''], su], False, None],
            'foreign-family-only-available-and-unavailable':
                [[['cross-family-edge-not-owed', ''], ['cross-family-edge-not-owed', RS_U], su],
                 False, None],
            'beside-an-owed-family-unavailable-obligation':
                [[su, ['unavailable-program-binding', '']], False, None],
            'beside-an-unknown-family-obligation':
                [[su, ['unavailable-program-binding', '']], False, None],
            'subject-universe-bound-unchanged': [[], True, None]},
        control={'reading': 'a negative that cites only other programs\' Coverage',
                 'refused': i1['same-family-U2-evidenced-only']['complete'] is False,
                 'firstRefusal': 'SUBJECT_PROGRAM_NEVER_SEARCHED_YET_COMPLETE'})
    u2 = i1['same-family-U2-evidenced-only']
    order = [inc([ts_cell(V2), ts_cell(None, 'js-allowjs')], [grp_v2, grp_v2b]),
             inc([ts_cell(None, 'js-allowjs'), ts_cell(V2)], [grp_v2b, grp_v2])]
    vec('incoming-i1-known-matches-survive-and-order-independence', 'A18 + A1', {
        'exists': truth('exists', ['fact2:x'], [], u2), 'none': truth('none', ['fact2:x'], [], u2),
        'countAtMostExceeded': truth('count-at-most', ['fact2:x', 'fact2:y'], [], u2, 1),
        'noneWithNoMatch': truth('none', [], [], u2),
        'twoProvidersEitherOrder': [codes(order[0]) == codes(order[1]),
                                    order[0]['complete'] == order[1]['complete'],
                                    [c['code'] for c in order[0]['causes']].count(
                                        'selector-unbound')]},
        {'exists': 'true', 'none': 'false', 'countAtMostExceeded': 'false',
         'noneWithNoMatch': 'indeterminate', 'twoProvidersEitherOrder': [True, True, 1]})

    # LV14 A21 incoming dependency totality (reachability -> calls@resolved-callee, same kind)
    x, y = 'rs:c::x', 'rs:c::y'
    reach_ok = reach[2]

    def tot(dep_sets, primaries):
        scopes_, covs_ = {}, {}
        for ch, subs in zip('ab', dep_sets):
            scopes_[sid(ch)] = {'relation': 'calls', 'resolution': 'resolved-callee',
                                'sourceUniverse': RS_U, 'subjects': subs}
            covs_[cid(ch)] = (sid(ch), ckey, calls_entry)
        groups = [{'S': RS_U, 'attestation': None, 'scopes': [
            {'id': sid(ch), 'subjects': subs, 'paired': [{'id': cid(ch), 'V': RS_U,
                                                          'entry': reach_ok}]}
            for ch, subs in zip('cd', primaries)]}]
        return incoming({'R': Synth(rcells, scopes_, covs_, DOMAINS), 'U': RS_U,
                         'relation': 'reachability', 'rung': 'from-resolved-calls',
                         'groups': groups})
    totality = {
        'partial-cover-merged-primary': tot([[x]], [[x, y]]),
        'partial-cover-split-primary': tot([[x]], [[x], [y]]),
        'full-cover-merged-primary': tot([[x], [y]], [[x, y]]),
        'full-cover-split-primary': tot([[x, y]], [[x], [y]]),
        'empty-primary-scope-coverage-route-stays-conservative': tot([[x]], [[]]),
    }
    unk = [[['coverage-unknown', RS_U]], False, ['required-relation-missing']]
    vec('incoming-dependency-totality', 'A21 + A13',
        dict({k: [codes(v), v['complete'], v['nativeDeficiencies']] for k, v in totality.items()},
             knownMatchesSurvive=[truth('exists', ['fact2:x'], [],
                                        totality['partial-cover-merged-primary']),
                                  truth('count-at-most', ['fact2:x', 'fact2:y'], [],
                                        totality['partial-cover-merged-primary'], 1)],
             partialEvidenceRetained=cid('a') in totality['partial-cover-merged-primary'][
                 'coverageIds']), {
            'partial-cover-merged-primary': unk, 'partial-cover-split-primary': unk,
            'full-cover-merged-primary': [[], True, []], 'full-cover-split-primary': [[], True, []],
            'empty-primary-scope-coverage-route-stays-conservative': unk,
            'knownMatchesSurvive': ['true', 'false'], 'partialEvidenceRetained': True},
        control={'reading': 'a present dependency position covers every owed subject',
                 'refused': totality['partial-cover-merged-primary']['complete'] is False,
                 'firstRefusal': 'DEPENDENCY_TOTALITY_GAP_READ_AS_COVERED'})

    # LV15 A16 runtime polarity set and the observability filter
    unfiltered = observability_filter('runtime-observation', [])
    hit_only = observability_filter('runtime-observation',
                                    [{'field': 'observability', 'cmp': 'eq',
                                      'value': 'observed-hit'}])
    vec('runtime-polarity-unfiltered-and-filtered', 'A16', {
        'matches': {o: [o in QSET['runtime'] and unfiltered(o), o in QSET['runtime'] and hit_only(o)]
                    for o in OBS_ENUM},
        'unknownLiteral': refusal_of(lambda: observability_filter(
            'runtime-observation', [{'field': 'observability', 'cmp': 'eq', 'value': 'hit'}]))}, {
        'matches': {'observed-hit': [True, True], 'observable-unhit': [True, False],
                    'unobservable': [False, False], 'unmapped': [False, False]},
        'unknownLiteral': 'ATOM_FILTER_ENUM_LITERAL_UNKNOWN'},
        control={'reading': 'V22-D3 (generation 22): only observed-hit matches, whatever the filter',
                 'refused': unfiltered('observable-unhit') is True,
                 'firstRefusal': 'UNFILTERED_EXISTS_EXCLUDED_AN_OBSERVABLE_UNHIT_ROW'})
    return rows


# ------------------------------------------------- min-resolution atom-level cross-check
class ModelRun:
    """The synthetic input closure RETAINED inside vectors/min-resolution.json, read back as
    data. The product evaluator produced that vector; this module re-derives every case."""

    def __init__(self, model):
        self.ep = {'cells': model['cells']}
        self.universe_domain = dict(model['universeDomains'])
        self.facts = {f['id']: f['record'] for f in model['facts']}
        self.fact_pay = {f['id']: f['payload'] for f in model['facts']}
        self.scopes = {s['id']: s['record'] for s in model['scopes']}
        self.covs = {c['id']: {'scopeId': c['scopeId']} for c in model['coverages']}
        self.cov_pay = {c['id']: c['payload'] for c in model['coverages']}


def min_resolution_cross_check():
    doc = json.load(open(OUT + '/vectors/min-resolution.json'))
    rows = []
    for lv in doc['atomLevelHalf']['levels']:
        for case in lv['cases']:
            M = ModelRun(case['inputs'])
            subj, node = case['inputs']['subject'], case['atom']
            rel, rung, op = node['relation'], node['minResolution'], node['op']
            known = sorted(fid for fid, fr in M.facts.items()
                           if fr['relation'] == rel and fr['sourceUniverse'] == subj['universe']
                           and ladder_index(rel, fr['resolution']) >= ladder_index(rel, rung)
                           and occupies(M, rel, fid, subj))
            try:
                comp = outgoing(M, rel, rung, subj, quantifier(op, rung))
            except Refusal as e:
                rows.append({'level': lv['level'], 'case': case['case'], 'op': op,
                             'derived': {'refusal': e.code}, 'productResult': case['productResult'],
                             'expectedByLaw': case['expected'], 'result': 'REFUSE'})
                continue
            derived = {'value': truth(op, known, [], comp, node.get('n')),
                       'causes': comp['causes'],
                       'nativeDeficiencies': comp['nativeDeficiencies'],
                       'coverageIds': sorted(comp['coverageIds']),
                       'scopeIds': sorted(comp['scopeIds'])}
            product = {k: case['productResult'][k] for k in derived}
            rows.append({'level': lv['level'], 'case': case['case'], 'op': op,
                         'derived': derived, 'productResult': product,
                         'expectedByLaw': case['expected'],
                         'result': 'PASS' if K.C(derived) == K.C(product)
                         and derived['value'] == case['expected']['value'] else 'REFUSE'})
        # the product's carrier controls, re-derived from their retained inputs
        for cc in lv.get('carrierControls') or []:
            M = ModelRun(cc['inputs'])
            node = cc['atom']
            try:
                outgoing(M, node['relation'], node['minResolution'], cc['inputs']['subject'],
                         quantifier(node['op'], node['minResolution']))
                code = None
            except Refusal as e:
                code = e.code
            rows.append({'level': lv['level'], 'case': cc['case'], 'op': node['op'],
                         'derived': {'refusal': code},
                         'productResult': {'refusal': cc['firstRefusal']},
                         'expectedByLaw': {'refusal': 'ATOM_NATIVE_CARRIER'},
                         'result': 'PASS' if code == cc['firstRefusal'] == 'ATOM_NATIVE_CARRIER'
                         else 'REFUSE'})
    return rows


# ------------------------------------------------------------------------------ controls
def m_add_rule_level_cause(R, rid, sid, addr, node, w, pp):
    if node.get('relation') == 'clones' and w['matchingFactIds']:
        w['deficiencies'] = K.cset(w['deficiencies'] + [
            {'source': 'native', 'cause': 'uncovered-expected-source-subject', 'subjectId': sid,
             'predicateId': addr, 'inputRefs': R.EI, 'evidenceKind': None, 'nativeCause': None,
             'universe': R.subjects[sid]['universe']}])
    return w, pp


def m_selector_unbound_with_universe(R, rid, sid, addr, node, w, pp):
    rows = []
    for d in w['deficiencies']:
        d = dict(d)
        if d['cause'] == 'selector-unbound':
            d['universe'] = R.subjects[sid]['universe']
        rows.append(d)
    w['deficiencies'] = K.cset(rows)
    return w, pp


def m_unhit_excluded_from_unfiltered(R, rid, sid, addr, node, w, pp):
    """the generation-22 reading (V22-D3) on the UNFILTERED rule: drop the observable-unhit row"""
    if node.get('relation') == 'runtime-observation' and not node.get('filters') and \
            R.subjects[sid]['nativeSubjectId'] == 'src/util.ts':
        w['matchingImportRows'] = [r for r in w['matchingImportRows'] if r['ordinal'] != 2]
        pp['value'] = 'false'
    return w, pp


def m_absent_dependency_silent(R, rid, sid, addr, node, w, pp):
    """the generation-22 reading I-A1: an absent dependency adds no required-relation-missing"""
    if node.get('relation') == 'clones':
        w['deficiencies'] = K.cset([d for d in w['deficiencies']
                                    if d['cause'] != 'required-relation-missing'])
    return w, pp


def m_unhit_as_hit(R, rid, sid, addr, node, w, pp):
    if node.get('relation') == 'runtime-observation' and node.get('filters') and \
            R.subjects[sid]['nativeSubjectId'] == 'src/util.ts':
        imp = R.plan['importIds'][0]
        w['matchingImportRows'] = [{'importId': imp, 'ordinal': 2, 'selector': 'runtime-subject'}]
        pp['value'] = 'true'
    return w, pp


def m_drop_carrier(R, rid, sid, addr, node, w, pp):
    rows = []
    for d in w['deficiencies']:
        d = dict(d)
        if d['cause'] == 'coverage-unknown':
            d['nativeCause'] = None
        rows.append(d)
    w['deficiencies'] = K.cset(rows)
    return w, pp


TAMPER = [('syntax-code', 'a rule-level uncovered-expected-source-subject copied into the atom',
           m_add_rule_level_cause, 'A7'),
          ('syntax-code', 'selector-unbound carrying the subject universe',
           m_selector_unbound_with_universe, 'A6/A3'),
          ('typescript', 'an observable-unhit runtime row counted as a hit under an '
                         'observability=observed-hit filter', m_unhit_as_hit, 'A16'),
          ('typescript', 'an observable-unhit runtime row excluded from an UNFILTERED exists '
                         '(the generation-22 V22-D3 reading)', m_unhit_excluded_from_unfiltered,
           'A16'),
          ('rust', 'an absent dependency answered with no required-relation-missing (the '
                   'generation-22 I-A1 reading)', m_absent_dependency_silent, 'A13'),
          ('rust-partial', 'coverage-unknown with its typed nativeCause carrier dropped',
           m_drop_carrier, 'A12')]


def main():
    assert DEPENDS_ON_QUOTE in ATOM_TEXT, 'DEPENDS_ON quote not found in the kit contract'
    for q in RANK_QUOTES + LAW_QUOTES:
        assert q in ATOM_TEXT, 'quote not found in the kit contract: ' + q
    doc = {'standing': __doc__,
           'kitQuotesVerified': [DEPENDS_ON_QUOTE] + list(RANK_QUOTES) + list(LAW_QUOTES),
           'runs': {}, 'predecessorControls': [], 'tamperControls': [], 'lawVectors': [],
           'claimLimits': [
               'no retained Run has an endpoint=target atom: A17-A19 incoming rules and A21 '
               'dependency totality are measured on typed synthetic models only and are labelled so',
               'the published DEPENDS_ON closure is one edge deep (reachability->calls, '
               'clones->declares), so "at every depth of the dependency closure" is measured at '
               'depth 1 only; no deeper edge is invented',
               'the only atom filter any retained Run carries is observability=observed-hit on the '
               'TypeScript runtime atom; no retained Run has a NATIVE atom filter, an imported '
               'count-at-most/all-covered atom, or a vcs-revision staleness correspondence: each '
               'raises NotExercised if met',
               'subject SELECTION (composition s2) is not re-derived here; every subject checked '
               'is recomputed from its retained record and joined to a retained inventory row',
               'the product evaluator is not imported; agreement is measured only by comparing '
               'the retained witness bytes with this derivation']}
    failed = []
    for label in RUNS:
        R = Run(OUT + '/runs/%s.store.json' % label, label)
        f, records, schema_rows = check_run(R)
        doc['runs'][label] = {'checks': len(f.rows), 'passed': len(f.rows) - len(f.refusals),
                              'refusals': f.refusals, 'schemaAdmissions': schema_rows,
                              'atoms': records}
        if f.refusals:
            failed.append(label)
        print('%-13s atoms %-3d checks %-4d refused %d  schema %s'
              % (label, len(records), len(f.rows), len(f.refusals), schema_rows))
        for r in f.refusals[:6]:
            print('   REFUSE %s %s' % (r['check'], json.dumps(r['detail'])[:260]))
    # the PREDECESSORS: generation 22's and generation 20's exact exported bytes, through the same
    # path. A predecessor may be ADMITTED under current law (its Run is untouched by the changed
    # clauses); that is a measured standing, not a failure of this instrument.
    for pdir in PREDECESSOR_DIRS:
        for label in RUNS:
            rel = '%s/runs/%s.store.json' % (pdir, label)
            try:
                R = Run(OUT + '/' + rel, label)
                f, records, _ = check_run(R)
                refusals = f.refusals
            except (Refusal, NotExercised) as e:
                refusals = [{'check': 'DERIVATION_REFUSED_OR_NOT_EXERCISED', 'detail': str(e)}]
            row = {'predecessor': rel, 'generationOfTheBytes': pdir.split('.')[-1],
                   'refused': bool(refusals),
                   'firstRefusal': refusals[0] if refusals else None,
                   'orderedRefusalChecks': [r['check'] for r in refusals][:20],
                   'refusalCount': len(refusals)}
            doc['predecessorControls'].append(row)
            print('predecessor %-30s refused=%s first=%s'
                  % (rel, row['refused'], row['firstRefusal'] and row['firstRefusal']['check']))
    for label, name, fn, clause in TAMPER:
        R = Run(OUT + '/runs/%s.store.json' % label, label)
        f, _, _ = check_run(R, mutate=fn)
        row = {'run': label, 'control': name, 'clause': clause, 'refused': bool(f.refusals),
               'firstRefusal': f.refusals[0] if f.refusals else None,
               'orderedRefusalChecks': [r['check'] for r in f.refusals][:12]}
        doc['tamperControls'].append(row)
        if not row['refused']:
            failed.append('control:' + name)
        print('tamper %-13s %-60s refused=%s first=%s'
              % (label, name[:60], row['refused'],
                 row['firstRefusal'] and row['firstRefusal']['check']))
    doc['lawVectors'] = law_vectors()
    for v in doc['lawVectors']:
        print('law %-66s %s control-refused=%s' % (v['vector'][:66], v['result'],
                                                   (v['control'] or {}).get('refused')))
        if v['result'] != 'PASS' or (v['control'] and not v['control']['refused']):
            failed.append('law:' + v['vector'])
    doc['minResolutionAtomLevelCrossCheck'] = min_resolution_cross_check()
    for r in doc['minResolutionAtomLevelCrossCheck']:
        if r['result'] != 'PASS':
            failed.append('min-resolution:%s:%s:%s' % (r['level'], r['case'], r['op']))
    print('min-resolution atom-level cross-check: %d cases, %d refused'
          % (len(doc['minResolutionAtomLevelCrossCheck']),
             sum(1 for r in doc['minResolutionAtomLevelCrossCheck'] if r['result'] != 'PASS')))
    changed = [r['predecessor'] for r in doc['predecessorControls'] if r['refused']]
    doc['summary'] = {'currentRunsAdmitted': [l for l in RUNS if l not in failed],
                      'predecessorsRefused': changed,
                      'tamperControlsRefused': sum(1 for r in doc['tamperControls'] if r['refused']),
                      'lawVectorsPassed': sum(1 for v in doc['lawVectors'] if v['result'] == 'PASS'),
                      'failed': failed}
    with open(OUT + '/vectors/indep-atom-law.json', 'w') as fh:
        json.dump(doc, fh, indent=1)
    print('summary', json.dumps(doc['summary']))
    raise SystemExit(1 if failed else 0)


if __name__ == '__main__':
    main()
