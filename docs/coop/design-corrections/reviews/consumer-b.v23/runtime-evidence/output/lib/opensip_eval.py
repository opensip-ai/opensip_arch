"""Independent evaluator3 implementation, from the normative kit only.

Owners read:
  foundation/evaluator-composition-contract.v3.md  sections 1-9 (field derivation)
  foundation/atom-evaluation-contract.v1.md        sections 1-9 (atom law)
  foundation/enumeration-contract.v1.md / enumeration-plan.schema.v1.json
  foundation/evaluator-projection-registry.v1.json (relations, owedPartitions, capabilityForRelation)
  foundation/relation-payload-schemas.v2.json      (ladders, subjectKind)
  native/native-evidence.schemas.v2.json           (CoverageResultV3, sufficiency inputs)
  product-v1/identity-and-evidence.md section 4    (determinate-evidence table, Kleene)
  product-v1/native-evidence.md section 4.6        (sufficiency_v2 ordered steps)

It reads ONLY retained inputs. It never reads a claimed finding, witness value, verdict,
count, or any caller-supplied truth flag.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_build as B

KIT = S.KIT

TRUE, FALSE, UNK = 'true', 'false', 'indeterminate'

POLICY_UNIVERSE_MAP = {
    'typescript': 'native.semantic-universe.typescript.v2',
    'rust': 'native.semantic-universe.rust.v2',
    'syntax': 'native.semantic-universe.syntax.v2',
}
RESOLVED_RUNGS = {'resolved-target', 'resolved-binding', 'resolved-callee', 'checked',
                  'from-resolved-calls'}


def _reg(path, key):
    return json.load(open(KIT + '/' + S.doc_path(path)))[key]


class EvalError(Exception):
    pass


class Inputs:
    """The admitted retained input closure handed to the evaluator."""

    def __init__(self, store, plan_id, plan, exec_plan_id, evaluator_closure,
                 policy, rule_program, waivers, emission_plan, enumeration_plan,
                 inventories, views, facts, scopes, coverages, coverage_payloads,
                 fact_payloads, universes, contexts, execution_inputs, imports=None,
                 import_payloads=None, import_observations=None, import_flags=None,
                 import_scopes=None, snapshot=None, detector_projection_closure=None):
        self.store = store
        self.plan_id = plan_id
        self.plan = plan
        self.exec_plan_id = exec_plan_id
        self.evaluator_closure = evaluator_closure
        self.policy = policy
        self.rule_program = rule_program
        self.waivers = waivers
        self.emission_plan = emission_plan
        self.enumeration_plan = enumeration_plan
        self.inventories = inventories          # list of (digest, SubjectInventoryV1)
        self.views = views                      # {view2 id: record}
        self.facts = facts                      # {fact2 id: record}
        self.scopes = scopes                    # {scope2 id: record}
        self.coverages = coverages              # {coverage2 id: record}
        self.coverage_payloads = coverage_payloads   # {coverage2 id: payload}
        self.fact_payloads = fact_payloads       # {fact2 id: payload}
        self.universes = universes               # {bare hex: (domain, record)}
        self.contexts = contexts                 # {bare hex: (domain, record)}
        self.execution_inputs = execution_inputs
        self.imports = imports or {}
        self.import_payloads = import_payloads or {}
        self.import_observations = import_observations or {}
        self.import_flags = import_flags or {}
        self.import_scopes = import_scopes or {}
        self.snapshot = snapshot
        self.detector_projection_closure = detector_projection_closure
        self.relreg = _reg(B.RELATION_DOC, 'x-opensip-relation-registry')
        self.projreg = json.load(open(KIT + '/' + S.doc_path(
            'foundation/evaluator-projection-registry.v1.json')))

    # ---------------- convenience
    def ladder(self, relation):
        row = self.relreg['relations'].get(relation)
        if not row or not row.get('ladder'):
            raise EvalError('RELATION_LADDER_ABSENT:%s' % relation)
        return row['ladder']

    def rung_index(self, relation, rung):
        lad = self.ladder(relation)
        if rung not in lad:
            raise EvalError('RUNG_NOT_IN_LADDER:%s@%s' % (relation, rung))
        return lad.index(rung)

    def subject_kind_of_relation(self, relation):
        return self.projreg['relations'][relation]['sourceSubjectKind']

    def source_field(self, relation):
        return self.projreg['relations'][relation]['sourceField']

    def capability_for_relation(self, relation):
        return self.projreg['capabilityForRelation'][relation]


# ---------------------------------------------------------------- node addressing
def address_nodes(node, addr='p'):
    """program-predicate address law: root `p`; i-th operand of and/or at `a` is `a.i`
    (zero-based, shortest decimal, no leading zero); the operand of `not` at `a` is `a.0`."""
    out = [(addr, node)]
    op = node['op']
    if op in ('and', 'or'):
        for i, ch in enumerate(node['operands']):
            out += address_nodes(ch, '%s.%d' % (addr, i))
    elif op == 'not':
        out += address_nodes(node['operand'], addr + '.0')
    return out


def child_addresses(node, addr):
    op = node['op']
    if op in ('and', 'or'):
        return ['%s.%d' % (addr, i) for i in range(len(node['operands']))]
    if op == 'not':
        return [addr + '.0']
    return []


def count_nodes(node):
    return len(address_nodes(node))


def count_atoms(node):
    return sum(1 for _, n in address_nodes(node)
               if n['op'] in ('exists', 'none', 'count-at-most', 'all-covered'))


# ---------------------------------------------------------------- subject enumeration
def subject_id(universe_hex, kind, native_id, manifest_path=None):
    rec = {'schemaVersion': 3, 'universe': universe_hex, 'kind': kind,
           'nativeSubjectId': native_id}
    if kind == 'package':
        rec['packageManifestPath'] = manifest_path
    return K.ID('evaluation-subject', rec), rec


def segment_match(seg, cand):
    """ONE ordinary pattern segment against ONE candidate segment, in full, per the portable
    glob contract: `*` matches zero or more Unicode SCALAR VALUES within the segment, `?` exactly
    one scalar (not one byte and not one displayed grapheme), every other character matches
    itself, braces and brackets are literal, and there is no escape syntax. Neither wildcard
    consumes `/` -- this function never sees one, because both sides are already split."""
    def m(i, j):
        if i == len(seg):
            return j == len(cand)
        ch = seg[i]
        if ch == '*':
            return any(m(i + 1, k) for k in range(j, len(cand) + 1))
        if ch == '?':
            return j < len(cand) and m(i + 1, j + 1)
        return j < len(cand) and cand[j] == ch and m(i + 1, j + 1)
    return m(0, 0)


def glob_match(pattern, candidate):
    """The normative predicate of foundation/glob-pattern-contract.v1.md, reconstructed from the
    published law and its required examples (generation 19; the kit that supplied it is the first
    one to decide terminal `**`).

    "Matching is case sensitive and anchored to the entire candidate string ... Split both pattern
    and candidate at every literal `/`, preserving empty segments ... A pattern segment that is
    exactly `**` instead matches zero or more whole candidate segments. This rule applies at the
    beginning, middle, and end, and may consume the final filename segment. It does not require a
    directory. A segment such as `a**b` is ordinary, and cannot consume a separator."

    Written as the published equivalence, which is stated as a RESULT and not as an algorithm:
    "A match at (i,j) succeeds at the end of P exactly when j is also at the end of S. For
    P[i] = **, it succeeds if any k from j through len(S), inclusive, makes (i+1,k) succeed.
    Otherwise it succeeds exactly when j < len(S), the ordinary segment matches S[j], and
    (i+1,j+1) succeeds. The predicate begins at (0,0)."

    No normalisation: `.`/`..` are not resolved, separators are not removed, nothing is rebased,
    case-folded or Unicode-normalised, and a trailing slash is an empty final segment rather than
    a directory flag.
    """
    P = pattern.split('/')
    S = candidate.split('/')

    def m(i, j):
        if i == len(P):
            return j == len(S)
        if P[i] == '**':
            return any(m(i + 1, k) for k in range(j, len(S) + 1))
        return j < len(S) and segment_match(P[i], S[j]) and m(i + 1, j + 1)
    return m(0, 0)


def in_scope(include, exclude, candidate):
    """Composition law of the same contract, for a ScopeDocument: "a candidate is selected if at
    least one `include` pattern matches and no `exclude` pattern matches. Exclusion wins a
    matching inclusion." Absent/empty-list behaviour stays with the OWNING field, which is why it
    is a parameter here rather than a default baked into the predicate."""
    if any(glob_match(g, candidate) for g in (exclude or [])):
        return False
    return any(glob_match(g, candidate) for g in (include or []))


def path_selected(rule, scope_doc, path):
    """include absent or [] means all paths; exclusion wins; optional ScopeDocumentV1
    intersects its include/exclude globs as well (composition section 2)."""
    se = rule['subjectEnumeration']
    inc, exc = se.get('include'), se.get('exclude') or []
    if inc:
        if not any(glob_match(g, path) for g in inc):
            return False
    if any(glob_match(g, path) for g in exc):
        return False
    if scope_doc:
        if scope_doc.get('include'):
            if not any(glob_match(g, path) for g in scope_doc['include']):
                return False
        if any(glob_match(g, path) for g in scope_doc.get('exclude') or []):
            return False
    return True


PRIMARY_KIND = {'file': 'file', 'symbol': 'symbol', 'package': 'package', 'export': 'symbol'}


def relevant_inventories(inp, rule):
    """Every retained inventory whose `kind` equals the rule primary kind and whose cell
    languageMode maps to the rule's portable universe domain (composition 9.5)."""
    want_kind = PRIMARY_KIND[rule['subjectEnumeration']['subjectKind']]
    want_domain = POLICY_UNIVERSE_MAP.get(rule['subjectEnumeration']['universe'])
    if want_domain is None:
        raise EvalError('POLICY_UNIVERSE_TOKEN_UNKNOWN:%s'
                        % rule['subjectEnumeration']['universe'])
    lm = _reg(B.IDENTITY_DOC, 'x-opensip-digest-domains')['languageModes']['map']
    cells = inp.enumeration_plan['cells']
    out = []
    for dig, invrec in inp.inventories:
        if invrec['kind'] != want_kind:
            continue
        cell = cells[invrec['cellOrdinal']]
        if lm.get(cell['languageMode']) != want_domain.split('.')[-2]:
            # map values are 'typescript'|'rust'|'syntax'; domain tail is e.g. 'syntax'
            pass
        mode_lang = lm.get(cell['languageMode'])
        if POLICY_UNIVERSE_MAP.get(mode_lang) != want_domain:
            continue
        out.append((dig, invrec, cell))
    return out, want_kind, want_domain


def enumerate_subjects(inp, rule, scope_doc):
    """composition section 2 + 9.5. Returns (selected, unresolved, inv_refs,
    incomplete_refs, deficiencies, state)."""
    rel_inv, want_kind, want_domain = relevant_inventories(inp, rule)
    defs_ = []
    inv_refs = [{'domain': 'subject-inventory', 'digest': d} for d, _, _ in rel_inv]
    incomplete = [{'domain': 'subject-inventory', 'digest': d}
                  for d, r, _ in rel_inv if r['state'] != 'complete']
    if not rel_inv:
        defs_.append({'source': 'enumeration', 'cause': 'no-covering-program',
                      'subjectId': None, 'predicateId': None, 'inputRefs': [],
                      'evidenceKind': None, 'nativeCause': None, 'universe': None})
    selected, unresolved = [], []
    want_exported = rule['subjectEnumeration']['subjectKind'] == 'export'
    for dig, invrec, cell in rel_inv:
        ref = {'domain': 'subject-inventory', 'digest': dig}
        if invrec['state'] != 'complete':
            defs_.append({'source': 'enumeration', 'cause': 'incomplete-inventory',
                          'subjectId': None, 'predicateId': None, 'inputRefs': [ref],
                          'evidenceKind': None, 'nativeCause': invrec.get('nativeCause'),
                          'universe': None})
            if invrec.get('deficiency') == 'source-syntax-invalid':
                defs_.append({'source': 'enumeration', 'cause': 'source-syntax-invalid',
                              'subjectId': None, 'predicateId': None, 'inputRefs': [ref],
                              'evidenceKind': None, 'nativeCause': None, 'universe': None})
        uni = cell['programBindings'][invrec['programOrdinal']]['universe']
        for row in invrec['rows']:
            if not path_selected(rule, scope_doc, row['path']):
                continue
            sid, srec = subject_id(uni, row['kind'], row['nativeSubjectId'],
                                   row['path'] if row['kind'] == 'package' else None)
            if want_exported:
                e = row.get('exported')
                if e == 'exported':
                    selected.append((sid, srec, row, uni, ref))
                elif e == 'unknown':
                    unresolved.append(sid)
                    defs_.append({'source': 'enumeration',
                                  'cause': 'unknown-export-membership',
                                  'subjectId': sid, 'predicateId': None,
                                  'inputRefs': [ref], 'evidenceKind': None,
                                  'nativeCause': None, 'universe': None})
                continue
            selected.append((sid, srec, row, uni, ref))
    # union duplicates only for the SAME (universe, kind, nativeSubjectId[, manifestPath])
    ded = {}
    for t in selected:
        ded.setdefault(t[0], t)
    selected = [ded[k] for k in sorted(ded, key=lambda s: K.C(s))]
    state = 'incomplete' if defs_ else 'complete'
    return selected, sorted(set(unresolved), key=lambda s: K.C(s)), \
        K.cset(inv_refs), K.cset(incomplete), defs_, state


# ---------------------------------------------------------------- native atom
def subject_occupies(inp, relation, fact_id, subject_rec):
    """Source occupancy: the registered payload field for this relation
    (evaluator-projection-registry relations[].sourceField)."""
    f = inp.facts[fact_id]
    pay = inp.fact_payloads[fact_id]
    field = inp.source_field(relation)
    if field == 'path':
        return pay.get('path') == subject_rec['nativeSubjectId']
    if field == 'anchors[0].path':
        return bool(f['anchors']) and f['anchors'][0]['path'] == subject_rec['nativeSubjectId']
    if field == 'declared':
        return pay.get('declared') == subject_rec['nativeSubjectId']
    if field == 'packageName':
        return (pay.get('packageName') == subject_rec['nativeSubjectId']
                and pay.get('manifestPath') == subject_rec.get('packageManifestPath'))
    if field == 'referrer':
        return pay.get('referrer') == subject_rec['nativeSubjectId']
    if field == 'importer':
        return pay.get('importer') == subject_rec['nativeSubjectId']
    if field == 'caller':
        return pay.get('caller') == subject_rec['nativeSubjectId']
    if field in ('symbol', 'subject', 'owner', 'origin'):
        # `subject` is types' registered sourceField; `owner` literal's; `origin` reachability's.
        # Generation 20 handled neither, which went unnoticed only because no Run used them.
        return pay.get(field) == subject_rec['nativeSubjectId']
    raise EvalError('UNHANDLED_SOURCE_FIELD:%s:%s' % (relation, field))


def filter_value(inp, relation, fact_id, field):
    f = inp.facts[fact_id]
    pay = inp.fact_payloads[fact_id]
    spec = inp.projreg['relations'][relation]['filters'][field]
    if spec == 'forbidden':
        raise EvalError('ATOM_FILTER_FIELD_FORBIDDEN:%s.%s' % (relation, field))
    if spec == 'fact.resolution':
        return f['resolution']
    if spec == 'fact.confidenceMillionths':
        return f['confidenceMillionths']
    if spec == 'endpoint-universe-domain':
        dom, _ = inp.universes[f['sourceUniverse']]
        return dom
    if spec.startswith('payload.'):
        return pay.get(spec[len('payload.'):])
    if spec == 'fact.anchors[0].path':
        return f['anchors'][0]['path'] if f['anchors'] else None
    raise EvalError('UNHANDLED_FILTER_SPEC:%s' % spec)


def apply_filters(inp, relation, fact_id, filters):
    for flt in filters:
        v = filter_value(inp, relation, fact_id, flt['field'])
        cmp_, want = flt['cmp'], flt['value']
        if cmp_ == 'eq':
            ok = v == want
        elif cmp_ == 'neq':
            ok = v != want
        elif cmp_ == 'in':
            ok = v in want
        elif cmp_ == 'prefix':
            ok = isinstance(v, str) and v.startswith(want)
        elif cmp_ == 'glob':
            ok = isinstance(v, str) and glob_match(want, v)
        elif cmp_ == 'gte':
            ok = isinstance(v, int) and v >= want
        elif cmp_ == 'lte':
            ok = isinstance(v, int) and v <= want
        else:
            raise EvalError('UNHANDLED_CMP:%s' % cmp_)
        if not ok:
            return False
    return True


def view_entry_for(inp, view_id, relation, rung, source_u):
    """The view's Coverage entries at exactly (relation, rung, sourceUniverse)."""
    out = []
    for cid in inp.views[view_id]['coverageIds']:
        pay = inp.coverage_payloads[cid]
        key = pay['key']
        if (key['relation'] == relation and key['resolution'] == rung
                and key['sourceUniverse'] == source_u):
            out.append((cid, pay))
    return out


def sufficiency_v2(inp, relation, min_rung, entries, quantifier, completeness,
                   min_confidence=0, derivation_policy='any',
                   unresolved_policy='forbid', external_policy='forbid'):
    """native-evidence section 4.6, evaluated IN ORDER; every applicable cause is
    collected. Returns {satisfied, deficiency, causes, disclosures}."""
    causes, disclosures = [], []
    if not entries:
        causes.append('required-relation-missing')
        return {'satisfied': False, 'deficiency': 'required-relation-missing',
                'causes': causes, 'disclosures': disclosures}
    for cid, pay in entries:
        e = pay['entry']
        # step 2: rung below minResolution -> "the rung-unavailable cause (language-tier-
        # unsupported, provider-unavailable, input-closure-incomplete, budget-exhausted) else
        # required-relation-missing". V22-D5: the generation-20 line took ANY entry deficiency
        # here, e.g. a resolution-incomplete carrier, which is not one of the four.
        if inp.rung_index(relation, e['resolution']) < inp.rung_index(relation, min_rung):
            causes.append(e.get('deficiency') if e.get('deficiency') in RUNG_UNAVAILABLE_CAUSES
                          else 'required-relation-missing')
        # step 3
        if e['confidenceMillionths'] < min_confidence:
            causes.append('confidence-floor-unmet')
        # step 4
        if relation == 'types' and derivation_policy == 'declared-only' \
                and 'compiler-inferred' in e['derivationKinds']:
            causes.append('derivation-policy-unmet')
        # step 5 -> "the entry's own deficiency". V22-D5: the generation-20 line fell back to
        # `coverage-unknown`, which is an ATOM cause, not a DeficiencyV2 member, so a sufficiency
        # result could have carried a value outside its own vocabulary. An entry that is not
        # complete and carries no deficiency now refuses instead of being given one.
        if completeness == 'complete' and e['coverage'] != 'complete':
            if e.get('deficiency') is None:
                raise EvalError('SUFFICIENCY_STEP5_ENTRY_CARRIES_NO_OWN_DEFICIENCY:%s' % cid)
            causes.append(e['deficiency'])
        # step 6
        if quantifier == 'universal-negative':
            st = e['resolutionCompleteness']['state']
            if st in ('partial', 'not-attempted'):
                causes.append('resolution-incomplete')
            elif st == 'incomplete':
                if unresolved_policy == 'forbid':
                    causes.append('resolution-incomplete')
                else:
                    disclosures.append({'unresolved-edges':
                                        e['resolutionCompleteness']['unresolvedEdgeCount'],
                                        'classes':
                                        e['resolutionCompleteness']['unresolvedEdgeClasses']})
        # step 7 is an INCOMING-only concern (atom contract section 4: target_exported /
        # target_affected apply only to endpoint=target); outgoing predicates do not
        # inherit unrelated incoming closed-world.
    uniq = [c for i, c in enumerate(causes) if c not in causes[:i]]
    if uniq:
        return {'satisfied': False, 'deficiency': precedence_pick(uniq), 'causes': uniq,
                'disclosures': disclosures}
    return {'satisfied': True, 'deficiency': None, 'causes': [], 'disclosures': disclosures}


DEFICIENCY_PRECEDENCE = ['language-tier-unsupported', 'provider-unavailable',
                         'input-closure-incomplete', 'budget-exhausted',
                         'confidence-floor-unmet', 'derivation-policy-unmet',
                         'resolution-incomplete', 'external-consumers-unknown',
                         'required-relation-missing']


def precedence_pick(causes):
    for d in DEFICIENCY_PRECEDENCE:
        if d in causes:
            return d
    return causes[0]


# ======================================================================== generation 22
# foundation/atom-evaluation-contract.v1.md section 4, successor text (kit manifest f98d3eb0...).
# Every rule below is a separately named clause of that section; the generation-20 function is
# kept underneath as evaluate_native_atom_v20_reading ONLY so a discriminating control can run the
# superseded reading over the same Run and show where the independent derivation refuses it.
#
#   COMPLETENESS RESULT   {complete, unknown, causes, coverageIds, scopeIds, nativeDeficiencies};
#                         a "return" ends ONLY that computation (complete=false, unknown=true, the
#                         accumulated causes/scopeIds/coverageIds kept as they stand). It never ends
#                         matching: a known match still makes exists true / none false.
#   SELECTION ORDER       scopes ascending scope2; Coverage deduplicated and sorted ascending
#                         coverage2 AFTER pairing (never the scope-walk order).
#   CAUSE REPRESENTATION  AtomCauseV1.universe optional+nullable; the key is carried only when a
#                         cause has a universe; the composition projection turns absence into null.
#   SHARED PRELUDE        P1 unavailable owed bindings: foreign family -> cross-family-edge-not-owed
#                         (universe null, non-blocking); owed family -> unavailable-program-binding
#                         for endpoint=target ONLY. P2 no owed binding at all ->
#                         missing-relation-coverage (null) and return.
#   OUTGOING 1..4         1 selector-unbound (null) + return; 2 uncovered-expected-source-subject
#                         (U) + return; 3 every containing scope in scopeIds, scope-without-coverage
#                         (U) per unpaired scope, return with EMPTY coverageIds if any unpaired or no
#                         pairing; 4 per paired Coverage in selection order: cite it, evaluate the
#                         dependency view, coverage-unknown (key.sourceUniverse, carrier nativeCause)
#                         when unsatisfied, no return.
#   DEPENDENCY VIEW       position 0 primary; then the transitive DEPENDS_ON closure breadth-first,
#                         each relation once at its first visit; no selected Coverage -> no position;
#                         several partitions fold into one position by the published field rules.
#
# "Rule-level enumeration uncertainty is root, not this atom": the generation-20 reading's
# inventory-wide uncovered_expected() census inside the atom is withdrawn (V22-D2).

# atom contract section 4 "(reachability->calls@resolved-callee; clones->declares@syntactic)"
DEPENDS_ON = {'reachability': (('calls', 'resolved-callee'),),
              'clones': (('declares', 'syntactic'),)}
COVERAGE_RANK = {'complete': 0, 'unknown': 1}
RC_STATE_RANK = {'complete': 0, 'not-applicable': 0, 'partial': 1, 'incomplete': 2,
                 'not-attempted': 3}
EXPORTS_CLOSED_RANK = {'closed': 0, 'open': 1, 'unknown': 2}
RUNG_UNAVAILABLE_CAUSES = ('language-tier-unsupported', 'provider-unavailable',
                           'input-closure-incomplete', 'budget-exhausted')
NON_BLOCKING_DISCLOSURES = ('cross-family-edge-not-owed',)


def atom_cause(code, universe=None, native_cause=None, evidence_kind=None):
    """AtomCauseV1. `universe` is carried only when the cause has one to report."""
    c = {'code': code, 'evidenceKind': evidence_kind, 'nativeCause': native_cause}
    if universe is not None:
        c['universe'] = universe
    return c


def engine_family_of_mode(inp, mode):
    for name, fam in sorted(inp.projreg['engineFamilies']['families'].items()):
        if mode in fam['languageModes']:
            return name
    return None


def engine_family_of_universe(inp, universe_hex):
    rec = inp.universes.get(universe_hex)
    if rec is None:
        return None
    for name, fam in sorted(inp.projreg['engineFamilies']['families'].items()):
        if fam['universeDomain'] == rec[0]:
            return name
    return None


def family_owed(a, b):
    """"A family is owed for the subject when either side is unknown or the two are equal.\""""
    return a is None or b is None or a == b


def owed_bindings(inp, relation):
    """EnumerationPlan bindings for capabilityForRelation[relation]."""
    cap = inp.capability_for_relation(relation)
    out = []
    for ci, cell in enumerate(inp.enumeration_plan['cells']):
        if cell['capabilityId'] != cap:
            continue
        for bi, b in enumerate(cell['programBindings']):
            out.append({'cellOrdinal': ci, 'programOrdinal': bi,
                        'languageMode': cell['languageMode'], 'universe': b.get('universe')})
    return out


def require_scope_carrier(scope_rec, scope_id):
    """atom contract section 4 "A scope without enumeratorClosure ... is refused
    ATOM_NATIVE_CARRIER wherever it is paired"."""
    ec = scope_rec.get('enumeratorClosure')
    if not (isinstance(ec, str) and ec.startswith('closure2:') and len(ec) == 73):
        raise EvalError('ATOM_NATIVE_CARRIER:%s enumeratorClosure=%r' % (scope_id, ec))


def fold_partitions(entries):
    """Section 4 dependency-view step 3: one position folded over several partitions IN
    SELECTION ORDER, starting from the first partition's entire entry."""
    acc = json.loads(json.dumps(entries[0]))
    for e in entries[1:]:
        if COVERAGE_RANK[e['coverage']] > COVERAGE_RANK[acc['coverage']]:
            acc['coverage'] = e['coverage']
        acc['confidenceMillionths'] = min(acc['confidenceMillionths'], e['confidenceMillionths'])
        # the ENTIRE record, only on a strictly worse state; a tie keeps the incumbent whole
        if RC_STATE_RANK[e['resolutionCompleteness']['state']] > \
                RC_STATE_RANK[acc['resolutionCompleteness']['state']]:
            acc['resolutionCompleteness'] = json.loads(json.dumps(e['resolutionCompleteness']))
        if EXPORTS_CLOSED_RANK[e['closedWorld']['exportsClosed']] > \
                EXPORTS_CLOSED_RANK[acc['closedWorld']['exportsClosed']]:
            acc['closedWorld'] = json.loads(json.dumps(e['closedWorld']))
        acc['derivationKinds'] = acc['derivationKinds'] + [
            k for k in e['derivationKinds'] if k not in acc['derivationKinds']]
    # the typed carrier WHOLE from the first partition carrying a non-null deficiency
    carrier = next((e for e in entries if e['deficiency'] is not None), None)
    if carrier is not None:
        acc['deficiency'], acc['nativeCause'] = carrier['deficiency'], carrier['nativeCause']
    return acc


def dependency_view(inp, relation, primary_cid, subject_rec):
    pay = inp.coverage_payloads[primary_cid]
    S, T = pay['key']['sourceUniverse'], pay['key']['targetUniverse']
    positions = [{'role': 'primary', 'relation': relation,
                  'resolution': pay['key']['resolution'], 'coverageIds': [primary_cid],
                  'selection': 'the evaluated Coverage', 'entry': pay['entry']}]
    cur_kind = inp.projreg['relations'][relation]['sourceSubjectKind']
    visited, queue = {relation}, list(DEPENDS_ON.get(relation, ()))
    while queue:
        dep_rel, dep_rung = queue.pop(0)
        if dep_rel in visited:
            continue
        visited.add(dep_rel)
        queue.extend(DEPENDS_ON.get(dep_rel, ()))
        dep_kind = inp.projreg['relations'][dep_rel]['sourceSubjectKind']
        if dep_kind == cur_kind:
            # only exact (relation, rung, S) scopes containing the subject; a mapping to any
            # other scope contributes no pairing ("There is no mapped-scope fallback")
            scopes = {sid for sid, s in inp.scopes.items()
                      if s['relation'] == dep_rel and s['resolution'] == dep_rung
                      and s['sourceUniverse'] == S
                      and subject_rec['nativeSubjectId'] in s['subjects']}
            cids = sorted({cid for cid, c in inp.coverages.items() if c['scopeId'] in scopes
                           and inp.coverage_payloads[cid]['key']['targetUniverse'] == T})
            for sid in sorted({inp.coverages[c]['scopeId'] for c in cids}):
                require_scope_carrier(inp.scopes[sid], sid)
            how = 'same source kind: Coverage paired to current-source scopes'
        else:
            cids = sorted({cid for cid in inp.coverages
                           if inp.coverage_payloads[cid]['key']['relation'] == dep_rel
                           and inp.coverage_payloads[cid]['key']['resolution'] == dep_rung
                           and inp.coverage_payloads[cid]['key']['sourceUniverse'] == S
                           and inp.coverage_payloads[cid]['key']['targetUniverse'] == T})
            how = 'different source kind: whole-source search of (S, T)'
        if not cids:
            continue
        positions.append({'role': 'dependency', 'relation': dep_rel, 'resolution': dep_rung,
                          'coverageIds': cids, 'selection': how,
                          'entry': fold_partitions([inp.coverage_payloads[c]['entry']
                                                    for c in cids])})
    return positions


def dependency_closure(relation):
    """The transitive DEPENDS_ON closure of `relation`, breadth-first, each relation once
    (native-evidence section 4.6 step 8: recursively, depth <= 4)."""
    out, queue, seen = [], list(DEPENDS_ON.get(relation, ())), {relation}
    depth = {r: 1 for r, _ in queue}
    while queue:
        rel, rung = queue.pop(0)
        if rel in seen:
            continue
        seen.add(rel)
        out.append((rel, rung))
        for nxt in DEPENDS_ON.get(rel, ()):
            if depth[rel] < 4:
                depth.setdefault(nxt[0], depth[rel] + 1)
                queue.append(nxt)
    return out


def sufficiency_positions(inp, positions, quantifier, min_confidence=0,
                          derivation_policy='any', unresolved_policy='forbid'):
    """native-evidence section 4.6 over an ordered dependency view. Position 0 carries the atom's
    requirement; a dependency carries partial-ok for an existential parent and the parent's
    quantifier/policies for a universal negative (step 8). Steps 1..6 in order, every applicable
    cause collected; step 7 is incoming-only.

    V23-D2: step 1 "Relation absent from the view -> required-relation-missing" applies to every
    relation of the step-8 dependency closure that occupies no position. Generation 22 read "a
    dependency contributing no selected Coverage occupies no position" as "adds no cause"
    (declared interpretation I-A1); the atom contract as frozen for generation 23 states that a
    removed position "answers required-relation-missing, exactly as an absent relation does" and
    that for an empty selection "a required dependency remains absent and the answer
    conservative"."""
    causes, disclosures = [], []
    present = {p['relation'] for p in positions}
    for dep_rel, _dep_rung in dependency_closure(positions[0]['relation']):
        if dep_rel not in present:
            causes.append('required-relation-missing')
    for i, pos in enumerate(positions):
        e, rel = pos['entry'], pos['relation']
        completeness = 'complete' if (i == 0 or quantifier == 'universal-negative') \
            else 'partial-ok'
        if inp.rung_index(rel, e['resolution']) < inp.rung_index(rel, pos['resolution']):
            causes.append(e['deficiency'] if e['deficiency'] in RUNG_UNAVAILABLE_CAUSES
                          else 'required-relation-missing')
        if e['confidenceMillionths'] < min_confidence:
            causes.append('confidence-floor-unmet')
        if rel == 'types' and derivation_policy == 'declared-only' \
                and 'compiler-inferred' in e['derivationKinds']:
            causes.append('derivation-policy-unmet')
        if completeness == 'complete' and e['coverage'] != 'complete':
            if e['deficiency'] is None:
                raise EvalError('SUFFICIENCY_STEP5_ENTRY_CARRIES_NO_OWN_DEFICIENCY:%s'
                                % pos['coverageIds'])
            causes.append(e['deficiency'])
        if quantifier == 'universal-negative':
            st = e['resolutionCompleteness']['state']
            if st in ('partial', 'not-attempted'):
                causes.append('resolution-incomplete')
            elif st == 'incomplete':
                if unresolved_policy == 'forbid':
                    causes.append('resolution-incomplete')
                else:
                    disclosures.append({'unresolved-edges':
                                        e['resolutionCompleteness']['unresolvedEdgeCount'],
                                        'classes':
                                        e['resolutionCompleteness']['unresolvedEdgeClasses']})
    uniq = [c for i, c in enumerate(causes) if c not in causes[:i]]
    return {'satisfied': not uniq, 'deficiency': precedence_pick(uniq) if uniq else None,
            'causes': uniq, 'disclosures': disclosures}


def outgoing_completeness(inp, relation, rung, U, subject_rec, quantifier):
    causes, scope_ids, cov_ids, native_defs, views = [], [], [], [], []

    def result(returned_at):
        blocking = [c for c in causes if c['code'] not in NON_BLOCKING_DISCLOSURES]
        complete = returned_at is None and not blocking
        return {'complete': complete, 'unknown': not complete, 'causes': K.cset(causes),
                'coverageIds': list(cov_ids), 'scopeIds': list(scope_ids),
                'nativeDeficiencies': K.cset_strings(native_defs),
                'returnedAt': returned_at, 'dependencyViews': views}

    owed = owed_bindings(inp, relation)
    subject_family = engine_family_of_universe(inp, U)
    for b in owed:                                                     # P1
        if b['universe'] is not None:
            continue
        if not family_owed(engine_family_of_mode(inp, b['languageMode']), subject_family):
            causes.append(atom_cause('cross-family-edge-not-owed'))
        # an owed-family unavailable binding emits unavailable-program-binding for
        # endpoint=target only; outgoing emits nothing here
    if not owed:                                                       # P2
        causes.append(atom_cause('missing-relation-coverage'))
        return result('P2')
    if not any(b['universe'] == U for b in owed if b['universe'] is not None):   # 1
        causes.append(atom_cause('selector-unbound'))
        return result('outgoing-1')
    containing = sorted(sid for sid, s in inp.scopes.items()                     # 2
                        if s['relation'] == relation and s['resolution'] == rung
                        and s['sourceUniverse'] == U
                        and subject_in_scope(inp, relation, s, subject_rec))
    if not containing:
        causes.append(atom_cause('uncovered-expected-source-subject', universe=U))
        return result('outgoing-2')
    scope_ids.extend(containing)                                                 # 3
    paired = {sid: sorted(cid for cid, c in inp.coverages.items() if c['scopeId'] == sid)
              for sid in containing}
    # V23-D3: pairing validates the subject-scope carrier; a scope whose enumeratorClosure is
    # absent or null is refused ATOM_NATIVE_CARRIER, never read as "no commitment"
    for sid in containing:
        if paired[sid]:
            require_scope_carrier(inp.scopes[sid], sid)
    for sid in containing:
        if not paired[sid]:
            causes.append(atom_cause('scope-without-coverage', universe=U))
    combined = sorted({cid for sid in containing for cid in paired[sid]})
    if any(not paired[sid] for sid in containing) or not combined:
        return result('outgoing-3')
    for cid in combined:                                                         # 4
        key = inp.coverage_payloads[cid]['key']
        if (key['relation'], key['resolution'], key['sourceUniverse']) != (relation, rung, U):
            raise EvalError('PAIRED_COVERAGE_KEY_DISAGREES_WITH_ITS_SCOPE:%s' % cid)
        cov_ids.append(cid)
        positions = dependency_view(inp, relation, cid, subject_rec)
        suff = sufficiency_positions(inp, positions, quantifier)
        carrier = next((p['entry']['nativeCause'] for p in positions
                        if p['entry']['nativeCause'] is not None), None)
        views.append({'coverageId': cid,
                      'positions': [{k: p[k] for k in ('role', 'relation', 'resolution',
                                                       'coverageIds', 'selection')}
                                    for p in positions],
                      'sufficiency': suff, 'carrierNativeCause': carrier})
        if not suff['satisfied']:
            native_defs.append(suff['deficiency'])
            causes.append(atom_cause('coverage-unknown', universe=key['sourceUniverse'],
                                     native_cause=carrier))
    return result(None)


def evaluate_native_atom(inp, atom, subject_rec, subject_id_, view_ids, rule_inv_refs):
    """Atom contract sections 3-5 as frozen at generation 22, OUTGOING endpoint (the only
    endpoint any retained Run's policy uses; endpoint=target refuses rather than guessing)."""
    relation, rung = atom['relation'], atom['minResolution']
    if rung not in inp.ladder(relation):
        raise EvalError('ATOM_MIN_RESOLUTION_NOT_IN_LADDER:%s@%s' % (relation, rung))
    if atom.get('endpoint', 'source') != 'source':
        raise EvalError('ATOM_ENDPOINT_NOT_EXERCISED_BY_THIS_RECONSTRUCTION')
    want_kind = inp.subject_kind_of_relation(relation)
    if subject_rec['kind'] != want_kind:
        raise EvalError('ATOM_KIND_INCOMPATIBLE:%s expects %s got %s'
                        % (relation, want_kind, subject_rec['kind']))
    U = subject_rec['universe']
    min_i = inp.rung_index(relation, rung)
    known = []
    for fid, f in sorted(inp.facts.items()):
        if f['relation'] != relation or f['sourceUniverse'] != U:
            continue
        if inp.rung_index(relation, f['resolution']) < min_i:
            continue
        if not subject_occupies(inp, relation, fid, subject_rec):
            continue
        if not apply_filters(inp, relation, fid, atom.get('filters') or []):
            continue
        known.append(fid)
    known = K.cset_strings(known)
    uncertain = []
    op = atom['op']
    resolved = rung in RESOLVED_RUNGS
    # section 5: none / count-at-most / all-covered use universal-negative at resolved rungs and
    # examination completeness at non-resolved rungs; exists is existential
    quant = 'existential' if (op == 'exists' or not resolved) else 'universal-negative'
    comp = outgoing_completeness(inp, relation, rung, U, subject_rec, quant)
    negative_ok = comp['complete'] and not comp['unknown'] and not uncertain
    if op == 'exists':
        value = TRUE if known else (FALSE if negative_ok else UNK)
    elif op == 'none':
        value = FALSE if known else (TRUE if negative_ok else UNK)
    elif op == 'count-at-most':
        value = FALSE if len(known) > atom['n'] else (TRUE if negative_ok else UNK)
    elif op == 'all-covered':
        value = TRUE if negative_ok else UNK
    else:
        raise EvalError('UNHANDLED_ATOM_OP:%s' % op)
    return {'value': value, 'kind': 'native-atom',
            'knownFactIds': known, 'uncertainFactIds': K.cset_strings(uncertain),
            'coverageIds': K.cset_strings(comp['coverageIds']),
            'scopeIds': K.cset_strings(comp['scopeIds']),
            'causes': comp['causes'], 'nativeDeficiencies': comp['nativeDeficiencies'],
            'countLimit': atom['n'] if op == 'count-at-most' else None,
            'completeness': comp}


def evaluate_native_atom_v20_reading(inp, atom, subject_rec, subject_id_, view_ids,
                                     rule_inv_refs):
    """SUPERSEDED at generation 22 (V22-D2). Generation 20's reading, kept verbatim for the
    discriminating control only; no Run is built with it.

    Atom contract sections 3-5, OUTGOING endpoint (the endpoint this reconstruction
    exercises). Returns a dict with value, known/uncertain fact ids, coverageIds,
    scopeIds, causes, nativeDeficiencies."""
    relation, rung = atom['relation'], atom['minResolution']
    if rung not in inp.ladder(relation):
        raise EvalError('ATOM_MIN_RESOLUTION_NOT_IN_LADDER:%s@%s' % (relation, rung))
    if atom.get('endpoint', 'source') != 'source':
        raise EvalError('ATOM_ENDPOINT_NOT_EXERCISED_BY_THIS_RECONSTRUCTION')
    want_kind = inp.subject_kind_of_relation(relation)
    if subject_rec['kind'] != want_kind:
        raise EvalError('ATOM_KIND_INCOMPATIBLE:%s expects %s got %s'
                        % (relation, want_kind, subject_rec['kind']))
    U = subject_rec['universe']
    min_i = inp.rung_index(relation, rung)

    known, uncertain = [], []
    for fid, f in sorted(inp.facts.items()):
        if f['relation'] != relation or f['sourceUniverse'] != U:
            continue
        if inp.rung_index(relation, f['resolution']) < min_i:
            continue
        if not subject_occupies(inp, relation, fid, subject_rec):
            continue
        if not apply_filters(inp, relation, fid, atom.get('filters') or []):
            continue
        known.append(fid)
    known = K.cset_strings(known)

    # ---- containing scopes at the EXACT requested rung for this source universe
    containing, cov_ids, scope_ids, causes = [], [], [], []
    for sid, srec in sorted(inp.scopes.items()):
        if (srec['relation'] != relation or srec['resolution'] != rung
                or srec['sourceUniverse'] != U):
            continue
        if subject_in_scope(inp, relation, srec, subject_rec):
            containing.append(sid)
    paired = {}
    for cid, crec in sorted(inp.coverages.items()):
        paired.setdefault(crec['scopeId'], []).append(cid)
    entries = []
    for sid in containing:
        if sid not in paired:
            causes.append({'code': 'scope-without-coverage', 'nativeCause': None,
                           'universe': U})
            continue
        for cid in paired[sid]:
            pay = inp.coverage_payloads[cid]
            if (pay['key']['relation'] == relation
                    and pay['key']['resolution'] == rung
                    and pay['key']['sourceUniverse'] == U):
                entries.append((cid, pay))
                cov_ids.append(cid)
                scope_ids.append(sid)
    if not containing and not entries:
        causes.append({'code': 'missing-relation-coverage', 'nativeCause': None,
                       'universe': U})

    # ---- examination: independently enumerated source subjects must be covered
    uncovered = uncovered_expected(inp, relation, rung, U, containing, rule_inv_refs)
    if uncovered:
        causes.append({'code': 'uncovered-expected-source-subject', 'nativeCause': None,
                       'universe': U})

    # ---- disclose the Coverage entries' own deficiencies
    native_defs = []
    for cid, pay in entries:
        e = pay['entry']
        if e['coverage'] != 'complete':
            pass   # carried by sufficiency_v2 below
    op = atom['op']
    resolved = rung in RESOLVED_RUNGS
    quant = 'universal-negative' if (op in ('none', 'count-at-most')) else 'existential'
    if op == 'all-covered':
        quant = 'universal-negative' if resolved else 'existential'

    suff = sufficiency_v2(inp, relation, rung, entries, quant, 'complete')
    if not suff['satisfied'] and suff['deficiency']:
        native_defs.append(suff['deficiency'])

    complete_examination = (bool(entries) and not uncovered and not causes
                           and suff['satisfied'])

    # ---- determinate-evidence table (identity section 4 / composition section 3)
    if op == 'exists':
        value = TRUE if known else (FALSE if complete_examination else UNK)
    elif op == 'none':
        value = FALSE if known else (TRUE if complete_examination else UNK)
    elif op == 'count-at-most':
        n = atom['n']
        if len(known) > n:
            value = FALSE
        elif complete_examination:
            value = TRUE
        else:
            value = UNK
    elif op == 'all-covered':
        value = TRUE if suff['satisfied'] and bool(entries) else UNK
        if not entries:
            value = UNK
    else:
        raise EvalError('UNHANDLED_ATOM_OP:%s' % op)

    return {'value': value, 'kind': 'native-atom',
            'knownFactIds': known, 'uncertainFactIds': K.cset_strings(uncertain),
            'coverageIds': K.cset_strings(cov_ids), 'scopeIds': K.cset_strings(scope_ids),
            'causes': causes, 'nativeDeficiencies': native_defs,
            'countLimit': atom['n'] if op == 'count-at-most' else None,
            'coverageEntryDeficiencies': [
                (cid, inp.coverage_payloads[cid]['entry']['deficiency'],
                 inp.coverage_payloads[cid]['entry']['nativeCause'],
                 inp.coverage_payloads[cid]['key']['sourceUniverse'])
                for cid, _ in entries
                if inp.coverage_payloads[cid]['entry']['deficiency'] is not None],
            'sufficiency': suff}


def derive_import_flags(store, wrapper, plan_snapshot_id):
    """`importFlagsAdapter` values are HOST PROJECTIONS from owner admission, never caller
    flags, and the projection is the published closed table:

      workflows-and-surfaces section 4 / imported-evidence #/$defs/StalenessRule --
      snapshot-equal -> current/consumable; snapshot-differs and commit-differs -> stale,
      unmapped-only; commit-equal-dirty -> unverifiable, unmapped-only;
      build-identity-differs -> wrong-build, unmapped-only; commit-equal-clean-MAPPED
      (an admitted SourceMappingV1 joining every generated path to the snapshot by digest)
      -> current/consumable; commit-equal-clean-UNMAPPED -> current/unmapped-only.

    So both values are DERIVED here from the retained SourceCorrespondence bytes and the
    Plan's own snapshot, not asserted. "Unmapped-only evidence may be listed and queried
    but never feeds a predicate."
    """
    corr_bytes = store.get_blob(wrapper['sourceCorrespondenceDigest'])
    if corr_bytes is None:
        raise EvalError('IMPORT_SOURCE_CORRESPONDENCE_NOT_RETAINED')
    corr = json.loads(corr_bytes.decode())
    if corr['kind'] == 'exact-snapshot':
        if corr['snapshotId'] == plan_snapshot_id:
            return {'consumable': True, 'staleness': 'current'}, 'snapshot-equal'
        return {'consumable': False, 'staleness': 'stale'}, 'snapshot-differs'
    rev = corr.get('vcsRevision') or {}
    if corr.get('buildIdentity') is not None and rev.get('buildIdentityMatches') is False:
        return {'consumable': False, 'staleness': 'wrong-build'}, 'build-identity-differs'
    if rev.get('dirty'):
        return {'consumable': False, 'staleness': 'unverifiable'}, 'commit-equal-dirty'
    if corr.get('sourceMappingDigest'):
        return {'consumable': True, 'staleness': 'current'}, 'commit-equal-clean-mapped'
    return {'consumable': False, 'staleness': 'current'}, 'commit-equal-clean-unmapped'


EVIDENCE_RELATIONS = None


def evidence_registry():
    global EVIDENCE_RELATIONS
    if EVIDENCE_RELATIONS is None:
        EVIDENCE_RELATIONS = _reg('workflows/schemas/imported-evidence.schema.json',
                                  'x-opensip-evidence-relation-registry')
    return EVIDENCE_RELATIONS


def runtime_filter_passes(inp, relation, filters, observability):
    """FieldFilter on an imported runtime atom. Only `observability` is exercised by this
    reconstruction; the registry projects it from RuntimeSubject.observability, and eq/neq/in
    values must be members of the closed comparator enum (ATOM_FILTER_ENUM_LITERAL_UNKNOWN)."""
    spec_row = inp.projreg['relations'][relation]['filters']
    enum = inp.projreg['comparatorTable']['observability']['enum']
    for flt in filters:
        field, cmp_, want = flt['field'], flt['cmp'], flt['value']
        if spec_row.get(field, 'forbidden') == 'forbidden':
            raise EvalError('ATOM_FILTER_FIELD_FORBIDDEN:%s.%s' % (relation, field))
        if field != 'observability':
            raise EvalError('IMPORTED_FILTER_FIELD_NOT_EXERCISED_BY_THIS_RECONSTRUCTION:%s' % field)
        if cmp_ in ('eq', 'neq') and want not in enum or \
                cmp_ == 'in' and any(w not in enum for w in want):
            raise EvalError('ATOM_FILTER_ENUM_LITERAL_UNKNOWN:%s=%r' % (field, want))
        if cmp_ == 'eq':
            ok = observability == want
        elif cmp_ == 'neq':
            ok = observability != want
        elif cmp_ == 'in':
            ok = observability in want
        elif cmp_ == 'prefix':
            ok = observability.startswith(want)
        elif cmp_ == 'glob':
            ok = glob_match(want, observability)
        else:
            raise EvalError('ATOM_FILTER_COMPARATOR_ILLEGAL:%s %s' % (field, cmp_))
        if not ok:
            return False
    return True


def evaluate_imported_atom(inp, atom, subject_rec, subject_id_, row):
    """Atom contract section 6 (import completeness), RUNTIME plane, `exists` / `none`, as frozen
    for generation 23.

    V23-D1: "an unfiltered `exists` tests whether a consumable mapped runtime observation exists,
    so either `observed-hit` or `observable-unhit` can satisfy it. An `observability` filter
    restricts the matching polarity set before applying the quantifier; unobservable and unmapped
    rows never enter that set" -- the projection registry importQuantifiers polaritySetR.runtime.
    Generation 22 (V22-D3) counted only `observed-hit` as a match whatever the filter; that reading
    is withdrawn. Completeness is unchanged: none/count-at-most true and all-covered need an exact
    consumable mapped polarity row (either polarity) for every owed wrapper, the payload owner
    window and population, and no uncertain row."""
    reg = evidence_registry()['relations']
    rel = atom['relation']
    if rel not in reg:
        raise EvalError('ATOM_EVIDENCE_RELATION_UNREGISTERED:%s' % rel)
    if atom['minResolution'] not in reg[rel]['ladder']:
        raise EvalError('ATOM_MIN_RESOLUTION_NOT_IN_LADDER:%s@%s'
                        % (rel, atom['minResolution']))
    kind = reg[rel]['evidenceKind']
    if atom.get('evidence') != kind:
        raise EvalError('ATOM_EVIDENCE_DECLARATION_MISMATCH:%s' % atom.get('evidence'))
    qset = inp.projreg['importQuantifiers']['polaritySetR']
    polarity_set, never_in = set(qset[kind]), set(qset['neverInR'])
    filters = atom.get('filters') or []
    owed, causes = [], []
    for iid in inp.plan['importIds']:
        w = inp.imports.get(iid)
        if w is None or w['kind'] != kind:
            continue
        scb = inp.store.get_blob(w['scopeDigest'])
        if scb is None:
            raise EvalError('ATOM_IMPORT_SCOPE_DESCRIPTOR_NOT_RETAINED:%s' % iid)
        if _in_import_scope(json.loads(scb.decode()), row['path']):
            owed.append(iid)
    if not owed:
        causes.append({'code': 'zero-owed-wrappers', 'evidenceKind': kind})
        causes.append({'code': 'evidence-kind-unavailable', 'evidenceKind': kind})
        return {'value': UNK, 'kind': 'imported-atom', 'knownRows': [], 'uncertainRows': [],
                'causes': causes, 'countLimit': None, 'polarityRows': []}
    known, uncertain, polarity = [], [], []
    for iid in owed:
        flags, _cond = derive_import_flags(inp.store, inp.imports[iid], inp.plan['snapshotId'])
        if set(flags) != {'consumable', 'staleness'}:
            raise EvalError('ATOM_IMPORT_FLAGS_ADAPTER_ABSENT_OR_EXTRA_KEYS:%s' % iid)
        pay = inp.import_payloads[iid]
        w = inp.imports[iid]
        hits = []
        for ordinal, r in enumerate(pay['subjects']):
            if subject_rec['kind'] == 'file':
                if r['path'] != row['path'] or 'symbol' in r:
                    continue
            elif subject_rec['kind'] == 'symbol':
                if r['path'] != row['path'] or r.get('symbol') != row['qualifiedName']:
                    continue
            else:
                raise EvalError('ATOM_KIND_INCOMPATIBLE:runtime plane %s' % subject_rec['kind'])
            hits.append((ordinal, r))
        if len(hits) > 1:
            raise EvalError('ATOM_IMPORT_AMBIGUOUS_ROWS:%s' % iid)
        addr = {'importId': iid, 'selector': 'runtime-subject'}
        if not hits:
            if w['completeness'] != 'complete':
                causes.append({'code': 'wrapper-partial', 'evidenceKind': kind})
            causes.append({'code': 'unmapped-subject', 'evidenceKind': kind})
            continue
        ordinal, r = hits[0]
        here = dict(addr, ordinal=ordinal)
        if not flags['consumable']:
            causes.append({'code': 'import-unmapped-only', 'evidenceKind': kind})
            causes.append({'code': 'no-consumable-row', 'evidenceKind': kind})
            uncertain.append(here)
            continue
        obs = r['observability']
        if obs in never_in:
            # never in R, and disclosed as uncertain independently of the observability filter
            causes.append({'code': 'unobservable-subject' if obs == 'unobservable'
                           else 'unmapped-subject', 'evidenceKind': kind})
            uncertain.append(here)
            continue
        if obs not in polarity_set:
            raise EvalError('IMPORT_OBSERVABILITY_OUTSIDE_THE_OWNER_ENUM:%s' % obs)
        polarity.append({'address': here, 'polarity': obs})
        if runtime_filter_passes(inp, rel, filters, obs):
            known.append(here)
        if w['completeness'] != 'complete':
            causes.append({'code': 'wrapper-partial', 'evidenceKind': kind})
        if pay.get('observationWindow') is None or pay.get('observedPopulation') in (
                None, 'unknown'):
            causes.append({'code': 'observation-window-insufficient', 'evidenceKind': kind})
    op = atom['op']
    complete = (not causes) and len(polarity) == len(owed) and not uncertain
    if op == 'exists':
        value = TRUE if known else (FALSE if complete else UNK)
    elif op == 'none':
        value = FALSE if known else (TRUE if complete else UNK)
    else:
        raise EvalError('IMPORTED_ATOM_OP_NOT_EXERCISED_BY_THIS_RECONSTRUCTION:%s' % op)
    return {'value': value, 'kind': 'imported-atom',
            'knownRows': cset_rows(known), 'uncertainRows': cset_rows(uncertain),
            'causes': causes, 'countLimit': None, 'polarityRows': polarity}


def evaluate_imported_atom_v22_reading(inp, atom, subject_rec, subject_id_, row):
    """SUPERSEDED at generation 23 (V23-D1). Generation 22's reading, kept verbatim for the
    discriminating control only; no Run is built with it.

    Atom contract section 6 (import completeness), RUNTIME plane, `exists` / `none`.

    V22-D3: the runtime observability enum is {observed-hit, observable-unhit, unobservable,
    unmapped}. Only `observed-hit` is a MATCH. `observable-unhit` is the other POLARITY row -- the
    subject was observable at the current grain and was not hit -- and section 6 names both as
    the "exact consumable mapped polarity row" that `none` / `count-at-most` true / `all-covered`
    need. Every retained library since generation 14 counted any consumable row that was not
    unobservable/unmapped as a known hit, so an observable-unhit subject was reported as observed.
    Completeness also reads the payload owner window/population for EVERY polarity row, not only
    for hits.
    """
    reg = evidence_registry()['relations']
    rel = atom['relation']
    if rel not in reg:
        raise EvalError('ATOM_EVIDENCE_RELATION_UNREGISTERED:%s' % rel)
    if atom['minResolution'] not in reg[rel]['ladder']:
        raise EvalError('ATOM_MIN_RESOLUTION_NOT_IN_LADDER:%s@%s'
                        % (rel, atom['minResolution']))
    kind = reg[rel]['evidenceKind']
    if atom.get('evidence') != kind:
        raise EvalError('ATOM_EVIDENCE_DECLARATION_MISMATCH:%s' % atom.get('evidence'))
    owed, causes = [], []
    for iid in inp.plan['importIds']:
        w = inp.imports.get(iid)
        if w is None or w['kind'] != kind:
            continue
        scb = inp.store.get_blob(w['scopeDigest'])
        if scb is None:
            raise EvalError('ATOM_IMPORT_SCOPE_DESCRIPTOR_NOT_RETAINED:%s' % iid)
        if _in_import_scope(json.loads(scb.decode()), row['path']):
            owed.append(iid)
    if not owed:
        causes.append({'code': 'zero-owed-wrappers', 'evidenceKind': kind})
        causes.append({'code': 'evidence-kind-unavailable', 'evidenceKind': kind})
        return {'value': UNK, 'kind': 'imported-atom', 'knownRows': [], 'uncertainRows': [],
                'causes': causes, 'countLimit': None, 'polarityRows': []}
    known, uncertain, polarity = [], [], []
    for iid in owed:
        flags, _cond = derive_import_flags(inp.store, inp.imports[iid], inp.plan['snapshotId'])
        if set(flags) != {'consumable', 'staleness'}:
            raise EvalError('ATOM_IMPORT_FLAGS_ADAPTER_ABSENT_OR_EXTRA_KEYS:%s' % iid)
        pay = inp.import_payloads[iid]
        w = inp.imports[iid]
        hits = []
        for ordinal, r in enumerate(pay['subjects']):
            if subject_rec['kind'] == 'file':
                if r['path'] != row['path'] or 'symbol' in r:
                    continue
            elif subject_rec['kind'] == 'symbol':
                if r['path'] != row['path'] or r.get('symbol') != row['qualifiedName']:
                    continue
            else:
                raise EvalError('ATOM_KIND_INCOMPATIBLE:runtime plane %s' % subject_rec['kind'])
            hits.append((ordinal, r))
        if len(hits) > 1:
            raise EvalError('ATOM_IMPORT_AMBIGUOUS_ROWS:%s' % iid)
        addr = {'importId': iid, 'selector': 'runtime-subject'}
        if not hits:
            if w['completeness'] != 'complete':
                causes.append({'code': 'wrapper-partial', 'evidenceKind': kind})
            causes.append({'code': 'unmapped-subject', 'evidenceKind': kind})
            continue
        ordinal, r = hits[0]
        here = dict(addr, ordinal=ordinal)
        if not flags['consumable']:
            causes.append({'code': 'import-unmapped-only', 'evidenceKind': kind})
            causes.append({'code': 'no-consumable-row', 'evidenceKind': kind})
            uncertain.append(here)
            continue
        obs = r['observability']
        if obs in ('unobservable', 'unmapped'):
            causes.append({'code': 'unobservable-subject' if obs == 'unobservable'
                           else 'unmapped-subject', 'evidenceKind': kind})
            uncertain.append(here)
            continue
        if obs == 'observed-hit':
            known.append(here)
        elif obs != 'observable-unhit':
            raise EvalError('IMPORT_OBSERVABILITY_OUTSIDE_THE_OWNER_ENUM:%s' % obs)
        polarity.append({'address': here, 'polarity': obs})
        if w['completeness'] != 'complete':
            causes.append({'code': 'wrapper-partial', 'evidenceKind': kind})
        if pay.get('observationWindow') is None or pay.get('observedPopulation') in (
                None, 'unknown'):
            causes.append({'code': 'observation-window-insufficient', 'evidenceKind': kind})
    op = atom['op']
    complete = (not causes) and len(polarity) == len(owed) and not uncertain
    if op == 'exists':
        value = TRUE if known else (FALSE if complete else UNK)
    elif op == 'none':
        value = FALSE if known else (TRUE if complete else UNK)
    else:
        raise EvalError('IMPORTED_ATOM_OP_NOT_EXERCISED_BY_THIS_RECONSTRUCTION:%s' % op)
    return {'value': value, 'kind': 'imported-atom',
            'knownRows': cset_rows(known), 'uncertainRows': cset_rows(uncertain),
            'causes': causes, 'countLimit': None, 'polarityRows': polarity}


def evaluate_imported_atom_v20_reading(inp, atom, subject_rec, subject_id_, row):
    """SUPERSEDED at generation 22 (V22-D3); kept for the discriminating control only.

    Atom contract section 6 (import completeness), RUNTIME plane, for the branches this
    reconstruction exercises: `exists` and `none` over `runtime-observation`.

    Owed wrappers = Plan-SELECTED imports of the evidenceKind whose DECLARED WRAPPER SCOPE
    is relevant, decided BEFORE reading listed rows. Zero owed wrappers is
    `zero-owed-wrappers` / `evidence-kind-unavailable` (unknown), never vacuous true.
    Consumable/staleness have no default: they come from the owner importFlagsAdapter.
    """
    reg = evidence_registry()['relations']
    rel = atom['relation']
    if rel not in reg:
        raise EvalError('ATOM_EVIDENCE_RELATION_UNREGISTERED:%s' % rel)
    if atom['minResolution'] not in reg[rel]['ladder']:
        raise EvalError('ATOM_MIN_RESOLUTION_NOT_IN_LADDER:%s@%s'
                        % (rel, atom['minResolution']))
    kind = reg[rel]['evidenceKind']
    if atom.get('evidence') != kind:
        raise EvalError('ATOM_EVIDENCE_DECLARATION_MISMATCH:%s' % atom.get('evidence'))

    owed, causes = [], []
    for iid in inp.plan['importIds']:
        w = inp.imports.get(iid)
        if w is None or w['kind'] != kind:
            continue
        # the declared wrapper scope is the OWNER scope-descriptor its own scopeDigest
        # names, fetched from the retained store -- not a caller-supplied map
        scb = inp.store.get_blob(w['scopeDigest'])
        if scb is None:
            raise EvalError('ATOM_IMPORT_SCOPE_DESCRIPTOR_NOT_RETAINED:%s' % iid)
        sc = json.loads(scb.decode())
        if _in_import_scope(sc, row['path']):
            owed.append(iid)
    if not owed:
        causes.append({'code': 'zero-owed-wrappers', 'evidenceKind': kind})
        causes.append({'code': 'evidence-kind-unavailable', 'evidenceKind': kind})
        return {'value': UNK, 'kind': 'imported-atom', 'knownRows': [], 'uncertainRows': [],
                'causes': causes, 'countLimit': None}

    known, uncertain = [], []
    for iid in owed:
        flags, _cond = derive_import_flags(inp.store, inp.imports[iid],
                                           inp.plan['snapshotId'])
        if set(flags) != {'consumable', 'staleness'}:
            raise EvalError('ATOM_IMPORT_FLAGS_ADAPTER_ABSENT_OR_EXTRA_KEYS:%s' % iid)
        pay = inp.import_payloads[iid]
        w = inp.imports[iid]
        hits = []
        for ordinal, r in enumerate(pay['subjects']):
            if subject_rec['kind'] == 'file':
                if r['path'] != row['path'] or 'symbol' in r:
                    continue
            elif subject_rec['kind'] == 'symbol':
                if r['path'] != row['path'] or r.get('symbol') != row['qualifiedName']:
                    continue
            else:
                raise EvalError('ATOM_KIND_INCOMPATIBLE:runtime plane %s'
                                % subject_rec['kind'])
            hits.append((ordinal, r))
        if len(hits) > 1:
            raise EvalError('ATOM_IMPORT_AMBIGUOUS_ROWS:%s' % iid)
        addr_of = (lambda o: {'importId': iid, 'selector': 'runtime-subject',
                              'ordinal': o})
        if not hits:
            if w['completeness'] != 'complete':
                causes.append({'code': 'wrapper-partial', 'evidenceKind': kind})
            causes.append({'code': 'unmapped-subject', 'evidenceKind': kind})
            continue
        ordinal, r = hits[0]
        if not flags['consumable']:
            causes.append({'code': 'import-unmapped-only', 'evidenceKind': kind})
            causes.append({'code': 'no-consumable-row', 'evidenceKind': kind})
            uncertain.append(addr_of(ordinal))
            continue
        if r['observability'] in ('unobservable', 'unmapped'):
            causes.append({'code': 'unobservable-subject' if r['observability']
                           == 'unobservable' else 'unmapped-subject',
                           'evidenceKind': kind})
            uncertain.append(addr_of(ordinal))
            continue
        known.append(addr_of(ordinal))
        if w['completeness'] != 'complete':
            causes.append({'code': 'wrapper-partial', 'evidenceKind': kind})
        if pay.get('observationWindow') is None or pay.get('observedPopulation') in (
                None, 'unknown'):
            causes.append({'code': 'observation-window-insufficient', 'evidenceKind': kind})

    op = atom['op']
    complete = bool(known) and not causes
    if op == 'exists':
        value = TRUE if known else (FALSE if complete else UNK)
    elif op == 'none':
        value = FALSE if known else (TRUE if complete else UNK)
    else:
        raise EvalError('IMPORTED_ATOM_OP_NOT_EXERCISED_BY_THIS_RECONSTRUCTION:%s' % op)
    return {'value': value, 'kind': 'imported-atom',
            'knownRows': cset_rows(known), 'uncertainRows': cset_rows(uncertain),
            'causes': causes, 'countLimit': None}


def cset_rows(rows):
    return K.cset(rows)


def _in_import_scope(scope_desc, path):
    """Owner scope-descriptor law: a path is in scope only if it is under a workspaceRoots
    member AND under a pathPrefixes member (empty prefixes admit all remaining paths) and
    not under excludedPathPrefixes. Concatenating the two arrays as one OR-prefix list is
    forbidden."""
    def under(prefix, p):
        return prefix == '.' or p == prefix or p.startswith(prefix.rstrip('/') + '/')
    if not any(under(w, path) for w in scope_desc['workspaceRoots']):
        return False
    if scope_desc['pathPrefixes'] and not any(under(x, path)
                                              for x in scope_desc['pathPrefixes']):
        return False
    if any(under(x, path) for x in scope_desc['excludedPathPrefixes']):
        return False
    return True


def subject_in_scope(inp, relation, scope_rec, subject_rec):
    """relation registry subjectKindLaw: what a scope's `subjects` entries identify."""
    kind = inp.relreg['relations'][relation]['subjectKind']
    n = subject_rec['nativeSubjectId']
    if kind in ('source-path', 'package-name', 'symbol'):
        return n in scope_rec['subjects']
    raise EvalError('UNHANDLED_SUBJECT_KIND:%s' % kind)


def uncovered_expected(inp, relation, rung, U, containing, rule_inv_refs):
    """Missing expected source subjects of this universe (owedPartitions.outgoing
    examination). Expected source subjects come from the retained inventories of the
    relation's own source kind for this universe."""
    want_kind = inp.subject_kind_of_relation(relation)
    expected = set()
    cells = inp.enumeration_plan['cells']
    for dig, inv in inp.inventories:
        if inv['kind'] != want_kind:
            continue
        cell = cells[inv['cellOrdinal']]
        binding = cell['programBindings'][inv['programOrdinal']]
        if binding.get('universe') != U:
            continue
        if inp.capability_for_relation(relation) != cell['capabilityId']:
            continue
        for row in inv['rows']:
            expected.add(row['nativeSubjectId'])
    covered = set()
    for sid in containing:
        covered |= set(inp.scopes[sid]['subjects'])
    return sorted(expected - covered)
