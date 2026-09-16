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


def glob_match(pattern, path):
    """workflows_model.v1.glob_match semantics named by the atom contract: `**/*.ts`
    matches root `a.ts`. Implemented as a segment matcher where `**` matches zero or
    more segments and `*` matches within one segment."""
    import re as _re

    def seg_re(seg):
        out = ''
        for ch in seg:
            if ch == '*':
                out += '[^/]*'
            elif ch == '?':
                out += '[^/]'
            else:
                out += _re.escape(ch)
        return out

    parts = pattern.split('/')
    rx = []
    for i, seg in enumerate(parts):
        if seg == '**':
            rx.append('(?:[^/]+/)*')
        else:
            rx.append(seg_re(seg) + ('/' if i < len(parts) - 1 else ''))
    full = '^' + ''.join(rx) + '$'
    full = full.replace('(?:[^/]+/)*/', '(?:[^/]+/)*')
    return bool(_re.match(full, path))


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
    if field == 'symbol':
        return pay.get('symbol') == subject_rec['nativeSubjectId']
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
        # step 2: rung below minResolution
        if inp.rung_index(relation, e['resolution']) < inp.rung_index(relation, min_rung):
            causes.append(e.get('deficiency') or 'required-relation-missing')
        # step 3
        if e['confidenceMillionths'] < min_confidence:
            causes.append('confidence-floor-unmet')
        # step 4
        if relation == 'types' and derivation_policy == 'declared-only' \
                and 'compiler-inferred' in e['derivationKinds']:
            causes.append('derivation-policy-unmet')
        # step 5
        if completeness == 'complete' and e['coverage'] != 'complete':
            causes.append(e.get('deficiency') or 'coverage-unknown')
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


def evaluate_native_atom(inp, atom, subject_rec, subject_id_, view_ids, rule_inv_refs):
    """Atom contract sections 3-5, OUTGOING endpoint (the endpoint this reconstruction
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


def evaluate_imported_atom(inp, atom, subject_rec, subject_id_, row):
    """Atom contract section 6 (import completeness), RUNTIME plane, for the branches this
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
