"""R1: absence requires correspondence knowledge on every side; replace the contradictory unmatched-baseline example;
current-source owners for two historical /tmp reads. Exact-once edits into the v2 work tree."""
import json, sys
sys.path.insert(0, '/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v2/tools')
from textedit import apply, edit_json  # noqa: E402

WPM = 'docs/coop/design-corrections/workflows/workflow_projection_model.v3.py'
WS = 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'
WPC = 'docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md'
CWP = 'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py'
CMP = 'docs/coop/design-corrections/workflows/schemas/evaluator3/comparison-result.schema.json'
rows = []

rows.append(apply('R1 model correspondence knowledge', WPM, [
    ('''    presence, entry_rules = derive_current_matched(view["occurrences"], view["waivedFindingIds"], view["emissionBindings"])
    hits = {fp: True for fp, rec in presence.items() if rec.get("E4")}
    prove = {rule["ruleId"]: rule_has_complete_hit_set(view, rule["ruleId"]) for rule in view["policy"]["rules"]}
    return {"hits": hits, "prove_absence": prove, "entry_rules": entry_rules}
''', '''    presence, entry_rules = derive_current_matched(view["occurrences"], view["waivedFindingIds"], view["emissionBindings"])
    hits = {fp: True for fp, rec in presence.items() if rec.get("E4")}
    prove = {rule["ruleId"]: rule_has_complete_hit_set(view, rule["ruleId"]) for rule in view["policy"]["rules"]}
    return {"hits": hits, "prove_absence": prove, "entry_rules": entry_rules,
            "unmatched": unmatched_correspondence_rows(view["occurrences"]), "subject_keys": fingerprint_subject_keys(view["occurrences"])}


def unmatched_correspondence_rows(occurrences) -> list:
    """Retained evidence of every unmatched occurrence at one side: rule, logical path and subject identity.
    No fingerprint is minted for these rows."""
    out = []
    for occ in occurrences or ():
        f = occ["finding"]
        if f["correspondence"]["state"] != "unmatched":
            continue
        out.append({"ruleId": f["ruleId"], "subjectPath": f["subject"]["logicalPath"], "kind": f["subject"]["kind"],
                    "language": f["subject"]["language"], "qualifiedName": f["subject"]["qualifiedName"]})
    return out


def fingerprint_subject_keys(occurrences) -> dict:
    """fingerprint -> admitted descriptor subjectKey, from matched occurrences only."""
    out = {}
    for occ in occurrences or ():
        f = occ["finding"]
        if f["fingerprint"] and occ.get("fingerprintDescriptor"):
            out[f["fingerprint"]] = occ["fingerprintDescriptor"]["subjectKey"]
    return out


def correspondence_barrier(rows, rule_id, path, subject_key=None) -> bool:
    """Correspondence knowledge for absence at one side (B, E0-E3 or E4).

    An unmatched occurrence of the same rule might be the fingerprint, so complete enumeration alone does not prove
    its absence. A row is provably unrelated only when its rule differs, both logical paths are known and differ, or
    the row's retained subject identity (kind, language, qualifiedName) and the fingerprint subjectKey are both known
    and differ. Otherwise absence at that side is unknown: the same-rule/same-path barrier applies where no stronger
    relation is retained (baseline unmatchedOccurrences retain rule and path only)."""
    for row in rows or ():
        if not rule_id or row.get("ruleId") != rule_id:
            continue
        if path and row.get("subjectPath") and row["subjectPath"] != path:
            continue
        if subject_key is not None and all(row.get(k) is not None for k in ("kind", "language", "qualifiedName")):
            if (row["kind"], row["language"], row["qualifiedName"]) != (subject_key.get("kind"), subject_key.get("language"), subject_key.get("qualifiedName")):
                continue
        return True
    return False
'''),
    ('''def fingerprint_absence_known(knowledge_view, extent, rule_id, path) -> bool:''',
     '''def fingerprint_absence_known(knowledge_view, extent, rule_id, path, subject_key=None) -> bool:'''),
    ('''    determinate, not budget-exhausted) and the path absence law over the attested extent. Missing admitted
    root predicate proofs or extent is unknown, never false.
    """''', '''    determinate, not budget-exhausted), the path absence law over the attested extent, and correspondence knowledge:
    no unmatched occurrence of that side that might be the fingerprint (correspondence_barrier). Missing admitted
    root predicate proofs or extent is unknown, never false.
    """'''),
    ('''    return path_absence_claim_allowed(
        path,
        examined=set(extent.get("examinedPaths") or []),
        scope_doc=extent.get("scopeDocument"),
        foundation_scope=extent.get("foundationScope"),
        extraction_complete=bool(extent.get("extractionComplete")),
    )


def current_absence_knowledge(current, b_entries, extra_rules):''', '''    if not path_absence_claim_allowed(
        path,
        examined=set(extent.get("examinedPaths") or []),
        scope_doc=extent.get("scopeDocument"),
        foundation_scope=extent.get("foundationScope"),
        extraction_complete=bool(extent.get("extractionComplete")),
    ):
        return False
    return not correspondence_barrier(unmatched_correspondence_rows(knowledge_view.get("occurrences")), rule_id, path, subject_key)


def current_absence_knowledge(current, b_entries, extra_rules):'''),
    ('''        "proof": {"predicateProofs": current.get("predicateProofs")},
    }
    extent = current.get("absenceExtent")''', '''        "proof": {"predicateProofs": current.get("predicateProofs")},
        "occurrences": current["occurrences"],
    }
    extent = current.get("absenceExtent")
    keys = fingerprint_subject_keys(current["occurrences"])'''),
    ('''    return lambda fp: fingerprint_absence_known(knowledge_view, extent, rules.get(fp), paths.get(fp))''',
     '''    return lambda fp: fingerprint_absence_known(knowledge_view, extent, rules.get(fp), paths.get(fp), keys.get(fp))'''),
    ('''    """B: True for a baseline entry; False for non-selection by the embedded baseline policy/ScopeDocument or under
    recorded complete-hit-set absence knowledge; else None."""
    if fp in b_entries:
        return True
    docs = (baseline or {}).get("contextDocuments") or {}
    if selection_excludes(docs.get("policy"), docs.get("scope"), rule_id, path):
        return False
    rule = b_rules.get(rule_id)
    return False if rule is not None and rule.get("absenceKnowledge") == "complete-hit-set" else None''',
     '''    """B: True for a baseline entry; False for non-selection by the embedded baseline policy/ScopeDocument, or under
    recorded complete-hit-set absence knowledge when no retained baseline unmatched occurrence might be the
    fingerprint (same rule and path; baseline rows retain no subject identity); else None. An empty entries[] never
    coerces unknown to False."""
    if fp in b_entries:
        return True
    docs = (baseline or {}).get("contextDocuments") or {}
    if selection_excludes(docs.get("policy"), docs.get("scope"), rule_id, path):
        return False
    rule = b_rules.get(rule_id)
    if rule is None or rule.get("absenceKnowledge") != "complete-hit-set":
        return None
    if correspondence_barrier((baseline or {}).get("unmatchedOccurrences"), rule_id, path):
        return None
    return False'''),
    ('''    current_extent = presence_absence_extent(view)
    for fp in fps_union:''', '''    current_extent = presence_absence_extent(view)
    subject_keys = fingerprint_subject_keys(view["occurrences"])
    for axis in bound:
        for fp, key in axis_measured[axis].get("subject_keys", {}).items():
            subject_keys.setdefault(fp, key)
    for fp in fps_union:'''),
    ('''            ):
                continue
            measured[axis] = False
        if e4_map.get(fp, {}).get("E4"):
            e4 = True
        elif fingerprint_absence_known(view, current_extent, rule_id, path):''', '''            ):
                continue
            if correspondence_barrier(rec.get("unmatched"), rule_id, path, subject_keys.get(fp)):
                continue
            measured[axis] = False
        if e4_map.get(fp, {}).get("E4"):
            e4 = True
        elif fingerprint_absence_known(view, current_extent, rule_id, path, subject_keys.get(fp)):'''),
]))

rows.append(apply('R1 prose workflows §3', WS, [
    ('''Evaluated absence is proved under the law above for that side's rule, including
the attested path extent.''', '''Evaluated absence is proved under the law above for that side's rule, including
the attested path extent and correspondence knowledge: an unmatched occurrence of the same rule
that might be the fingerprint leaves that side's presence `null`, because complete enumeration
with such an occurrence is not proof the fingerprint was fixed or never present. Such an
occurrence is related unless the paths differ or its retained subject kind, language and
qualified name provably differ from the fingerprint's subject key; where no stronger relation is
retained, the same-rule/same-path barrier applies. No fingerprint is ever minted for an unmatched
occurrence, and a known matched hit stays `true`.'''),
    ('''adoption by the same law; B non-selection is read from the embedded baseline policy and
ScopeDocument.''', '''adoption by the same law and no retained baseline `unmatchedOccurrences` row has the same rule
and path (those rows carry no subject identity); B non-selection is read from the embedded
baseline policy and ScopeDocument.'''),
    ('''classification, so a known `CODE-NET-NEW` still fails. Rule coverage, evidence and execution
deficiencies remain independent of this knowledge.
''', '''classification, so a known `CODE-NET-NEW` still fails. Rule coverage, evidence and execution
deficiencies remain independent of this knowledge.

**Indeterminate reason selection (closed).** An entry publishes exactly one
`indeterminateReason`, the first applicable in this order: (1) `pivot-reevaluation-unavailable`
when a changed axis's pivot presence is `null` (E0 for a changed detector map, E1 policy, E2
scope, E3 waivers), whether that pivot was not bound or was bound without presence knowledge,
including a correspondence barrier on that pivot; (2) the evidence axis, evaluated per declared
`evidenceUse` in declaration order: `required-evidence-unavailable`, then for a gating rule
`evidence-availability-changed` or `evidence-content-changed`; (3) the detector disposition's
own reason when its method is `indeterminate`; (4) `baseline-absence-unknown` when the first
attributable change rests on a `null` B; (5) `current-absence-unknown` when it rests on a `null`
E4. Whole-comparison reasons perform no comparison and emit no entries.

**An unmatched baseline occurrence is not proven absence.** A baseline that retains an unmatched
occurrence of a rule on a path (for example a symbol whose detector projection was unavailable)
does not prove that a fingerprint of that rule on that path was absent. A fingerprint present
only on a pivot stays in the comparison universe, the baseline's gating unmatched obligation
remains a `correspondence-incomplete` deficiency, and the entry is `INDETERMINATE`
(`baseline-absence-unknown`), not `CODE-NET-NEW`. A genuinely complete baseline that selects the
path, records complete absence knowledge and retains no such unmatched occurrence proves
`B=false`: a fingerprint present on a bound E1 pivot and hidden by disabling the rule in current is
`CODE-NET-NEW` with `subsequentDeltas=[policy]` and still gates (`code-net-new-policy-hidden`).
'''),
]))

rows.append(apply('R1 prose projection contract §12', WPC, [
    ('''(the side's rule proves absence under the pivot predicate including the attested path extent; for B the baseline RuleCoverage records `absenceKnowledge=complete-hit-set`, recorded at adoption by the same predicate)''',
     '''(the side's rule proves absence under the pivot predicate including the attested path extent and the correspondence barrier: no unmatched occurrence of the same rule on the same path unless its retained subject kind, language and qualified name provably differ from the fingerprint subjectKey; for B the baseline RuleCoverage records `absenceKnowledge=complete-hit-set`, recorded at adoption by the same predicate, and no baseline `unmatchedOccurrences` row has the same rule and path)'''),
    ('''An entry whose first attributable change rests on `null` is `INDETERMINATE` (`current-absence-unknown` / `baseline-absence-unknown`); an earlier known change keeps its classification.''',
     '''An entry whose first attributable change rests on `null` is `INDETERMINATE` (`current-absence-unknown` / `baseline-absence-unknown`); an earlier known change keeps its classification. The closed per-entry reason order is workflows-and-surfaces §3 (pivot-reevaluation-unavailable, evidence, detector disposition, baseline-absence-unknown, current-absence-unknown). An unmatched occurrence never receives a fingerprint.'''),
    ('''A fingerprint that exists only on E0–E3 (disabled current, empty baseline, enabled E1) remains, with admitted pivot `(ruleId, detectorId)` metadata. A bug introduced and hidden by disabling the rule is `CODE-NET-NEW` with `subsequentDeltas` including policy, per workflows-and-surfaces §3.''',
     '''A fingerprint that exists only on E0–E3 (disabled current, enabled E1) remains, with admitted pivot `(ruleId, detectorId)` metadata. Over a genuinely complete empty baseline (complete absence knowledge and no unmatched occurrence of that rule on that path) a bug introduced and hidden by disabling the rule is `CODE-NET-NEW` with `subsequentDeltas` including policy, per workflows-and-surfaces §3. Over a baseline that retains an unmatched occurrence of the rule on that path (for example projection-unavailable) the same pivot-only fingerprint is `INDETERMINATE` (`baseline-absence-unknown`), not `CODE-NET-NEW`; this replaces the earlier selected example that treated such a baseline as empty.'''),
]))


def pivot_description(doc):
    pp = doc['$defs']['PivotPresence']
    old = 'path inside the attested extent). null = not known.'
    assert pp['description'].count(old) == 1
    pp['description'] = pp['description'].replace(old, 'path inside the attested extent, no unmatched occurrence at that side that might be the fingerprint). null = not known. No fingerprint is minted for an unmatched occurrence.')


rows.append(edit_json('R1 PivotPresence description', CMP, pivot_description))

R1_CONTROLS = r'''
# R1 (v2): absence requires correspondence knowledge. Collision under COMPLETE enumeration is not proof of a fix.
_R1_X3 = {"nativeSubjectId": "symbol:x3"}
_R1_X4 = {"nativeSubjectId": "symbol:x4", "qualifiedName": "z", "signatureTokens": ["function", "z", "(", ")"]}
for _gate in (True, False):
    _tag = "gating" if _gate else "nongating"
    _r1_base = RC.positive(symbol_rows=[_S7_X1, _S7_X2], scope_document=SCOPE_ALL, gate=_gate)
    _r1_art = P.adopt_admitted_baseline_v3(*_r1_base, CUSTODY)
    _r1_cur = RC.positive(symbol_rows=[_S7_X1, _S7_X2, _R1_X3], scope_document=SCOPE_ALL, gate=_gate)
    _r1_view = P.project_admitted_run_v3(*_r1_cur)
    _r1_unmatched = [o["finding"]["correspondence"]["reason"] for o in _r1_view["occurrences"] if o["finding"]["correspondence"]["state"] == "unmatched"]
    check("r1-%s-current-is-complete-enumeration-with-colliding-unmatched" % _tag,
          _r1_view["ruleResults"][0]["enumeration"]["state"] == "complete" and _r1_unmatched == ["signature-ambiguous", "signature-ambiguous"], _r1_unmatched)
    _r1_kept = {o["finding"]["fingerprint"] for o in _r1_view["occurrences"] if o["finding"]["fingerprint"]}
    _r1_fps = [e["fingerprint"] for e in _r1_art["descriptor"]["entries"]]
    _r1_lost = [fp for fp in _r1_fps if fp not in _r1_kept]
    _r1_res = _s7_compare(_r1_art, _r1_cur, _s7_host(_r1_art, _r1_base))
    must_valid("r1-%s-collision-comparison-schema" % _tag, U + "comparison:2", cmp_obj(_r1_res))
    check("r1-%s-collision-is-indeterminate-not-code-fixed" % _tag,
          len(_r1_lost) == 1 and _s7_entry(_r1_res, _r1_lost[0])["classification"] == "INDETERMINATE"
          and _s7_entry(_r1_res, _r1_lost[0])["indeterminateReason"] == "current-absence-unknown" and _s7_entry(_r1_res, _r1_lost[0])["presence"]["E4"] is None
          and _s7_entry(_r1_res, _r1_lost[0])["gates"] is False,
          [(e["classification"], e.get("indeterminateReason"), e["presence"]["E4"]) for e in _r1_res["descriptor"]["entries"]])
    check("r1-%s-known-matched-hit-stays-true" % _tag,
          len(_r1_kept & set(_r1_fps)) == 1 and all(_s7_entry(_r1_res, fp)["classification"] == "UNCHANGED" and _s7_entry(_r1_res, fp)["presence"]["E4"] is True for fp in _r1_kept & set(_r1_fps)))
    check("r1-%s-unmatched-occurrence-never-minted-into-entries" % _tag, {e["fingerprint"] for e in _r1_res["descriptor"]["entries"]} == set(_r1_fps))
    if _gate:
        _r1_new = RC.positive(symbol_rows=[_S7_X1, _S7_X2, _R1_X3, _R1_X4], scope_document=SCOPE_ALL, gate=_gate)
        _r1_new_res = _s7_compare(_r1_art, _r1_new, _s7_host(_r1_art, _r1_base))
        _r1_added = [e for e in _r1_new_res["descriptor"]["entries"] if e["fingerprint"] not in _r1_fps]
        check("r1-gating-unrelated-unknown-does-not-erase-separate-code-net-new",
              len(_r1_added) == 1 and _r1_added[0]["classification"] == "CODE-NET-NEW" and _r1_added[0]["gates"] is True and _r1_added[0]["presence"]["B"] is False
              and _s7_entry(_r1_new_res, _r1_lost[0])["indeterminateReason"] == "current-absence-unknown" and _r1_new_res["descriptor"]["verdict"] == "fail",
              [(e["classification"], e.get("indeterminateReason"), e["presence"]["B"]) for e in _r1_new_res["descriptor"]["entries"]])
        must_valid("r1-gating-separate-code-net-new-schema", U + "comparison:2", cmp_obj(_r1_new_res))
        _r1_rule = _r1_view["policy"]["rules"][0]["ruleId"]
        _r1_ext = P.presence_absence_extent(_r1_view)
        check("r1-law-same-rule-same-path-unmatched-is-a-barrier", P.fingerprint_absence_known(_r1_view, _r1_ext, _r1_rule, "src/index.ts") is False)
        check("r1-law-unrelated-path-is-not-a-barrier", P.fingerprint_absence_known(_r1_view, _r1_ext, _r1_rule, "README.md") is True)
        check("r1-law-provably-different-subject-identity-is-not-a-barrier",
              P.fingerprint_absence_known(_r1_view, _r1_ext, _r1_rule, "src/index.ts", {"kind": "symbol", "language": "typescript", "qualifiedName": "other"}) is True)
        check("r1-law-same-subject-identity-is-a-barrier",
              P.fingerprint_absence_known(_r1_view, _r1_ext, _r1_rule, "src/index.ts", {"kind": "symbol", "language": "typescript", "qualifiedName": "x"}) is False)
        check("r1-law-other-rule-unmatched-is-not-a-barrier", P.correspondence_barrier(P.unmatched_correspondence_rows(_r1_view["occurrences"]), "another-rule", "src/index.ts") is False)
# Pivot side: an E1 pivot whose complete enumeration retains a colliding unmatched occurrence cannot prove absence.
_r1p_base = RC.positive(symbol_rows=[_S7_X1, _S7_X2], scope_document=SCOPE_ALL)
_r1p_art = P.adopt_admitted_baseline_v3(*_r1p_base, CUSTODY)
_r1p_cur = RC.positive(symbol_rows=[_S7_X1, _S7_X2, _R1_X3], scope_document=SCOPE_ALL, enabled=False)
_r1p_e1 = RC.positive(symbol_rows=[_S7_X1, _S7_X2, _R1_X3], scope_document=SCOPE_ALL)
try:
    _r1p_res = P.compare_admitted_v3(baseline_artifact=_r1p_art, current_run=_r1p_cur[0], current_objects=_r1p_cur[1], current_blobs=_r1p_cur[2],
                                     host=_s7_host(_r1p_art, _r1p_base), profile_name="code-regression", pivot_runs={"E1": _r1p_e1})
    _r1p_kept = {o["finding"]["fingerprint"] for o in P.project_admitted_run_v3(*_r1p_e1)["occurrences"] if o["finding"]["fingerprint"]}
    _r1p_fps = [e["fingerprint"] for e in _r1p_art["descriptor"]["entries"]]
    _r1p_lost = [fp for fp in _r1p_fps if fp not in _r1p_kept]
    must_valid("r1-pivot-collision-comparison-schema", U + "comparison:2", cmp_obj(_r1p_res))
    check("r1-pivot-collision-is-pivot-reevaluation-unavailable-not-code-fixed",
          len(_r1p_lost) == 1 and _s7_entry(_r1p_res, _r1p_lost[0])["classification"] == "INDETERMINATE"
          and _s7_entry(_r1p_res, _r1p_lost[0])["indeterminateReason"] == "pivot-reevaluation-unavailable" and _s7_entry(_r1p_res, _r1p_lost[0])["presence"]["E1"] is None,
          [(e["classification"], e.get("indeterminateReason"), e["presence"]) for e in _r1p_res["descriptor"]["entries"]])
    check("r1-pivot-known-hit-is-policy-delta",
          all(_s7_entry(_r1p_res, fp)["classification"] == "POLICY-DELTA" and _s7_entry(_r1p_res, fp)["presence"]["E1"] is True for fp in _r1p_kept & set(_r1p_fps)) and bool(_r1p_kept & set(_r1p_fps)))
except Exception as _r1p_exc:
    check("r1-pivot-collision-is-pivot-reevaluation-unavailable-not-code-fixed", False, type(_r1p_exc).__name__ + ": " + str(_r1p_exc)[:200])
# Baseline side: retained unmatched rows (rule + path) are a barrier; an unrelated path is not.
_r1b_rules = {r["ruleId"]: r for r in art_un["descriptor"]["ruleCoverage"]}
_r1b_rule = art_un["descriptor"]["unmatchedOccurrences"][0]["ruleId"]
check("r1-baseline-same-rule-same-path-unmatched-row-is-a-barrier",
      _r1b_rules[_r1b_rule]["absenceKnowledge"] == "complete-hit-set"
      and P.baseline_presence_knowledge("finding-key2:" + "f" * 64, _r1b_rule, {}, _r1b_rules, art_un["descriptor"], art_un["descriptor"]["unmatchedOccurrences"][0]["subjectPath"]) is None
      and P.baseline_presence_knowledge("finding-key2:" + "f" * 64, _r1b_rule, {}, _r1b_rules, art_un["descriptor"], "src/other.ts") is False)
'''

rows.append(apply('R1 checker controls and current-source owners', CWP, [
    ('''clar = Path("/tmp/opensip-design-corrections/grok-workflow-projection.v8/root-clarification.txt")
check(
    "root-clarification-waived-matched-presence-is-honest-law",
    clar.is_file()
    and "Do NOT delete waived findings" in clar.read_text()
    and''', '''# v2: the historical /tmp root clarification is not a retained manifest file and is not this check's subject;
# the operative law is the current projection contract §11 plus the model derivation.
_contract_wpc = " ".join((HERE / "workflow-projection-contract.v3.md").read_text().split())
check(
    "waived-matched-presence-is-current-contract-law",
    "Waived matched findings remain present; waiver status is `waivedC`, not absence." in _contract_wpc
    and'''),
    ('''_chapter_s2 = Path("/tmp/opensip-design-corrections/evaluator-successor.v1/docs/v2/contracts/product-v1/workflows-and-surfaces.md").read_text()''',
     '''# v2: the current-source chapter owns declared-compatible law; no unrelated historical runtime tree is read.
_chapter_s2 = " ".join((HERE.parents[3] / "docs/v2/contracts/product-v1/workflows-and-surfaces.md").read_text().split())'''),
    ('''check(
    "pivot-only-fp-is-code-net-new-with-subsequent-policy",
    any(e["classification"] == "CODE-NET-NEW" and e.get("gates") and "policy" in e.get("subsequentDeltas", []) for e in net),
)
check("disabled-current-does-not-drop-pivot-only-fingerprint", bool(net))
check(
    "disabled-current-does-not-erase-baseline-unmatched-gating",
    any(d["gating"] and d["cause"] == "correspondence-incomplete" for d in cmp_dis["descriptor"]["ruleDeficiencies"])
    or cmp_dis["descriptor"]["verdict"] == "fail",
)
must_valid("disabled-e1-comparison-schema", U + "comparison:2", cmp_obj(cmp_dis))
''', '''# v2 root replacement of the contradictory selected example: this baseline retains a projection-unavailable
# unmatched x, so it is not an empty proven absence; the pivot-only fingerprint is baseline-absence-unknown.
check(
    "pivot-only-fp-over-unmatched-baseline-is-baseline-absence-unknown",
    bool(net) and all(e["classification"] == "INDETERMINATE" and e["indeterminateReason"] == "baseline-absence-unknown"
                      and e["presence"]["B"] is None and e["presence"]["E1"] is True and e["gates"] is False for e in net),
    [(e["classification"], e.get("indeterminateReason"), e["presence"]) for e in net],
)
check("disabled-current-does-not-drop-pivot-only-fingerprint", bool(net))
check(
    "disabled-current-does-not-erase-baseline-unmatched-gating",
    any(d["gating"] and d["cause"] == "correspondence-incomplete" for d in cmp_dis["descriptor"]["ruleDeficiencies"])
    and cmp_dis["descriptor"]["verdict"] != "pass",
    cmp_dis["descriptor"]["verdict"],
)
must_valid("disabled-e1-comparison-schema", U + "comparison:2", cmp_obj(cmp_dis))
# A genuinely complete baseline (path selected, complete absence knowledge, no unmatched occurrence that could be x)
# proves B=false: the pivot-only x is a real CODE-NET-NEW hidden by disabling the rule and still gates.
base_empty_x = RC.positive(symbol_rows=[{"nativeSubjectId": "symbol:y", "qualifiedName": "y", "signatureTokens": ["function", "y", "(", ")"]}], scope_document=SCOPE_DOC)
check("complete-empty-baseline-shares-policy-with-e1", base_empty_x[1][base_empty_x[0]["planId"]][1]["policyDigest"] == e1_enabled[1][e1_enabled[0]["planId"]][1]["policyDigest"])
art_empty_x = P.adopt_admitted_baseline_v3(*base_empty_x, CUSTODY)
check(
    "complete-empty-baseline-proves-absence-of-x",
    art_empty_x["descriptor"]["unmatchedOccurrences"] == []
    and all(r["absenceKnowledge"] == "complete-hit-set" for r in art_empty_x["descriptor"]["ruleCoverage"] if r["enabled"])
    and not any(e["fingerprint"] in e1_fps for e in art_empty_x["descriptor"]["entries"]),
)
host_empty_x = host_from_graph({"runId": art_empty_x["descriptor"]["runId"]}, base_empty_x[1])
host_empty_x["pivotRunId"] = art_empty_x["descriptor"]["runId"]
cmp_empty_x = P.compare_admitted_v3(
    baseline_artifact=art_empty_x,
    current_run=cur_disabled[0],
    current_objects=cur_disabled[1],
    current_blobs=cur_disabled[2],
    host=host_empty_x,
    profile_name="code-regression",
    pivot_runs={"E1": e1_enabled},
)
net_empty_x = [e for e in cmp_empty_x["descriptor"]["entries"] if e["fingerprint"] in e1_fps]
check(
    "complete-empty-baseline-pivot-only-fp-is-code-net-new-policy-hidden",
    bool(net_empty_x) and all(e["classification"] == "CODE-NET-NEW" and e["gates"] is True and e["gateReason"] == "code-net-new-policy-hidden"
                              and "policy" in e["subsequentDeltas"] and e["presence"]["B"] is False for e in net_empty_x)
    and cmp_empty_x["descriptor"]["verdict"] == "fail",
    [(e["classification"], e.get("gateReason"), e["presence"]) for e in net_empty_x],
)
must_valid("complete-empty-baseline-comparison-schema", U + "comparison:2", cmp_obj(cmp_empty_x))
'''),
    ('''    and P.selection_excludes(P.project_admitted_run_v3(*_ns_disabled)["policy"], SCOPE_ALL, _ns_rule, "README.md") is True,
)
''', '''    and P.selection_excludes(P.project_admitted_run_v3(*_ns_disabled)["policy"], SCOPE_ALL, _ns_rule, "README.md") is True,
)
''' + R1_CONTROLS),
]))
print(json.dumps(rows, indent=1))
