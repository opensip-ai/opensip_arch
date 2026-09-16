"""S7 follow-up after run after-edits-3 (preserved): structural non-selection is known non-emission on every side.

The first S7 law made a fingerprint that the current ScopeDocument does not select `null`; the selected control
wider-scope-does-not-false-absent-unselected-current-paths discriminated that as wrong (the scope axis removed the
selection). A side whose own policy does not enable the rule or whose ScopeDocument does not select the path cannot
emit the fingerprint. B/E0/E1 share the baseline selection, so this never yields CODE-FIXED.
"""
import hashlib, json, sys
from pathlib import Path
sys.path.insert(0, '/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v1/tools')
from textedit import apply, ROOT, RT  # noqa: E402

WPM = 'docs/coop/design-corrections/workflows/workflow_projection_model.v3.py'
WS = 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'
WPC = 'docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md'
CWP = 'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py'
CMP_SCHEMA = 'docs/coop/design-corrections/workflows/schemas/evaluator3/comparison-result.schema.json'
rows = []

rows.append(apply('S7 non-selection model', WPM, [
    ('''def rule_absence_knowledge(view, rule_id) -> str:
''', '''def selection_excludes(policy, scope_doc, rule_id, path) -> bool:
    """Structural non-emission at one side: its policy does not enable the rule, or its ScopeDocument does not
    select the path. This is not evaluated absence; it attributes the change to the policy or scope axis."""
    if rule_id and policy is not None:
        rule = policy_rule(policy, rule_id)
        if rule is None or not rule.get("enabled"):
            return True
    return bool(path and scope_doc and not path_in_scope_document(scope_doc, path))


def rule_absence_knowledge(view, rule_id) -> str:
'''),
    ('''    """Known absence of one non-emitted fingerprint: the law _bind_pivot_runs/compare_admitted_v3 apply to pivots.
''', '''    """Known non-emission of one fingerprint at one side: structural non-selection, or evaluated absence under the
    law _bind_pivot_runs/compare_admitted_v3 apply to pivots.
'''),
    ('''    if not rule_id or extent is None:
        return False
    try:
        complete = rule_has_complete_hit_set(knowledge_view, rule_id)''', '''    if selection_excludes(knowledge_view.get("policy"), (extent or {}).get("scopeDocument"), rule_id, path):
        return True
    if not rule_id or extent is None:
        return False
    try:
        complete = rule_has_complete_hit_set(knowledge_view, rule_id)'''),
    ('''            if fp in rec["hits"]:
                measured[axis] = True
                continue
            if not (rule_id and rec["prove_absence"].get(rule_id)):''', '''            if fp in rec["hits"]:
                measured[axis] = True
                continue
            if selection_excludes(rec.get("policy"), rec.get("scope_document"), rule_id, path):
                measured[axis] = False
                continue
            if not (rule_id and rec["prove_absence"].get(rule_id)):'''),
    ('''        knowledge["scope_document"] = pview["scopeDocument"]
''', '''        knowledge["scope_document"] = pview["scopeDocument"]
        knowledge["policy"] = pview["policy"]
'''),
    ('''def baseline_presence_knowledge(fp, rule_id, b_entries, b_rules):
    """B: True for a baseline entry; False only under recorded complete-hit-set absence knowledge; else None."""
    if fp in b_entries:
        return True
''', '''def baseline_presence_knowledge(fp, rule_id, b_entries, b_rules, baseline=None, path=None):
    """B: True for a baseline entry; False for non-selection by the embedded baseline policy/ScopeDocument or under
    recorded complete-hit-set absence knowledge; else None."""
    if fp in b_entries:
        return True
    docs = (baseline or {}).get("contextDocuments") or {}
    if selection_excludes(docs.get("policy"), docs.get("scope"), rule_id, path):
        return False
'''),
    ('''        pres["B"] = baseline_presence_knowledge(fp, rule_id, b_entries, b_rules)''',
     '''        pres["B"] = baseline_presence_knowledge(fp, rule_id, b_entries, b_rules, baseline, current.get("fingerprintPaths", {}).get(fp))'''),
    ('''    current_v1 = dict(stub, presence=presence, entryRules=entry_rules)''', '''    fingerprint_paths = {fp: e.get("subjectPath") for fp, e in b_entries.items()}
    for occ in occurrences:
        if occ["finding"]["fingerprint"]:
            fingerprint_paths[occ["finding"]["fingerprint"]] = occ["finding"]["subject"]["logicalPath"]
    current_v1 = dict(stub, presence=presence, entryRules=entry_rules, fingerprintPaths=fingerprint_paths)'''),
]))

rows.append(apply('S7 non-selection prose workflows', WS, [
    ('''**One presence-knowledge law on every side.** B, E0–E3 and E4 are each `true` (a known
matched occurrence), `false` (absence proved under the law above for that side's rule,
including the attested path extent) or `null` (not known). The absence of a matched current
hit is not by itself a known `false`: incomplete or unknown enumeration, unknown roots,
disabled evaluation and an exhausted budget leave E4 `null`. B is `false` for a non-entry only
when the baseline's `RuleCoverage.absenceKnowledge` for that rule is `complete-hit-set`,
recorded at adoption by the same law; the baseline artifact records per-rule knowledge, not a
per-path extent.''', '''**One presence-knowledge law on every side.** B, E0–E3 and E4 are each `true` (a known
matched occurrence), `false` or `null` (not known). `false` is either non-selection or
evaluated absence. Non-selection holds when that side's own policy does not enable the rule or
its ScopeDocument does not select the path: the side cannot emit the fingerprint, so the change
is attributed to the policy or scope axis that removed the selection. It is not an evaluated
negative result, and because B, E0 and E1 share the baseline selection it never becomes
`CODE-FIXED`. Evaluated absence is proved under the law above for that side's rule, including
the attested path extent. The absence of a matched current hit is not by itself a known
`false`: for an enabled rule selecting the path, incomplete or unknown enumeration, unknown
roots and an exhausted budget leave E4 `null`. B is evaluated-absent for a non-entry only when
the baseline's `RuleCoverage.absenceKnowledge` for that rule is `complete-hit-set`, recorded at
adoption by the same law; B non-selection is read from the embedded baseline policy and
ScopeDocument. The baseline artifact records per-rule knowledge, not a per-path extent.'''),
]))

rows.append(apply('S7 non-selection prose projection contract', WPC, [
    ('''E4 is `true` for a matched current occurrence, `false` only when the current rule proves absence under the pivot predicate including the attested path extent, else `null`. B is `false` for a non-entry only when the baseline RuleCoverage records `absenceKnowledge=complete-hit-set` (recorded at adoption by the same predicate), else `null`.''',
     '''Every side is `true` for a matched occurrence; `false` for non-selection (that side's policy does not enable the rule or its ScopeDocument does not select the path; for B the embedded baseline documents) or for evaluated absence (the side's rule proves absence under the pivot predicate including the attested path extent; for B the baseline RuleCoverage records `absenceKnowledge=complete-hit-set`, recorded at adoption by the same predicate); else `null`.'''),
    ('''- Absence False is not claimed for a fingerprint whose subjectPath is outside the attested inventory examined extent or the pivot ScopeDocument, unless foundation `plan.scopeDigest` covers the path and inventories are complete (deleted under a covering census).''',
     '''- Evaluated absence False is not claimed for a fingerprint whose subjectPath is outside the attested inventory examined extent, unless foundation `plan.scopeDigest` covers the path and inventories are complete (deleted under a covering census). A path the pivot's own ScopeDocument does not select, or a rule its policy does not enable, is non-selection `false` on that pivot, not evaluated absence (§12).'''),
]))

rows.append(apply('S7 non-selection controls', CWP, [
    ('''check("a12-hidden-reason-defined-over-any-later-axis", "hidden by a later detector, policy or scope change" in _chapter_ws and''',
     '''check("a12-hidden-reason-defined-over-any-later-axis", "hidden by a later detector, policy or scope change" in " ".join(_chapter_ws.split()) and'''),
    ('''must_invalid("s7-e4-null-still-refused-for-missing-reason", U + "comparison:2#/$defs/Entry", dict(_kn_e[_kf_old["finding"]["fingerprint"]], classification="CODE-FIXED", direction="vanished", indeterminateReason=None))
''', '''_kn_unknown = _kn_e[_kf_old["finding"]["fingerprint"]]
must_valid("s7-entry-with-null-e4-and-absence-reason-admitted", U + "comparison:2#/$defs/Entry", _kn_unknown)
must_invalid("s7-indeterminate-entry-without-reason-refused", U + "comparison:2#/$defs/Entry", {k: v for k, v in _kn_unknown.items() if k != "indeterminateReason"})
must_invalid("s7-unknown-reason-outside-closed-enum-refused", U + "comparison:2#/$defs/Entry", dict(_kn_unknown, indeterminateReason="absence-unknown"))

# S7 non-selection: a side that does not select the fingerprint cannot emit it; attributed to policy/scope, never CODE-FIXED.
_ns_base = RC.positive(symbol_rows=[_S7_X1, _S7_X2], scope_document=SCOPE_ALL)
_ns_art = P.adopt_admitted_baseline_v3(*_ns_base, CUSTODY)
_ns_host = _s7_host(_ns_art, _ns_base)
_ns_disabled = RC.positive(symbol_rows=[_S7_X1, _S7_X2], scope_document=SCOPE_ALL, enabled=False)
try:
    _ns_with_e1 = P.compare_admitted_v3(baseline_artifact=_ns_art, current_run=_ns_disabled[0], current_objects=_ns_disabled[1], current_blobs=_ns_disabled[2], host=_ns_host, profile_name="code-regression", pivot_runs={"E1": _ns_base})
    must_valid("s7-disabled-current-with-bound-e1-comparison-schema", U + "comparison:2", cmp_obj(_ns_with_e1))
    check(
        "s7-disabled-current-rule-with-bound-e1-is-policy-delta-not-code-fixed",
        bool(_ns_with_e1["descriptor"]["entries"])
        and all(e["classification"] == "POLICY-DELTA" and e["direction"] == "vanished" and e["presence"]["E4"] is False and e["presence"]["E1"] is True for e in _ns_with_e1["descriptor"]["entries"]),
        [(e["classification"], e.get("indeterminateReason"), e["presence"]) for e in _ns_with_e1["descriptor"]["entries"]],
    )
except Exception as _ns_exc:
    check("s7-disabled-current-rule-with-bound-e1-is-policy-delta-not-code-fixed", False, type(_ns_exc).__name__ + ": " + str(_ns_exc)[:200])
_ns_without = P.compare_admitted_v3(baseline_artifact=_ns_art, current_run=_ns_disabled[0], current_objects=_ns_disabled[1], current_blobs=_ns_disabled[2], host=_ns_host, profile_name="code-regression")
check(
    "s7-disabled-current-rule-without-e1-is-pivot-unavailable-not-code-fixed",
    bool(_ns_without["descriptor"]["entries"]) and all(e["classification"] == "INDETERMINATE" and e["indeterminateReason"] == "pivot-reevaluation-unavailable" for e in _ns_without["descriptor"]["entries"]),
    [(e["classification"], e.get("indeterminateReason")) for e in _ns_without["descriptor"]["entries"]],
)
_ns_policy = _ns_art["descriptor"]["contextDocuments"]["policy"]
_ns_rule = _ns_art["descriptor"]["entries"][0]["ruleId"]
check(
    "s7-non-selection-is-structural-scope-and-policy",
    P.selection_excludes(_ns_policy, SCOPE_DOC, _ns_rule, "README.md") is True
    and P.selection_excludes(_ns_policy, SCOPE_ALL, _ns_rule, "README.md") is False
    and P.selection_excludes(P.project_admitted_run_v3(*_ns_disabled)["policy"], SCOPE_ALL, _ns_rule, "README.md") is True,
)
'''),
]))

# Guarded JSON description update for PivotPresence.
p = ROOT / CMP_SCHEMA
raw = p.read_bytes()
doc = json.loads(raw)
assert (json.dumps(doc, indent=2, ensure_ascii=False) + '\n').encode() == raw, 'round-trip guard refused'
pp = doc['$defs']['PivotPresence']
assert pp['description'].startswith('Presence knowledge of the fingerprint at each pivot.')
pp['description'] = ('Presence knowledge of the fingerprint at each pivot. true = a known matched occurrence (waived included). false ='
                     " non-selection (that side's policy does not enable the rule or its ScopeDocument does not select the path; attributed"
                     ' to the policy or scope axis, never CODE-FIXED) or evaluated absence proved by that side\'s rule under the'
                     ' complete-hit-set law (enabled rule, evaluated, complete enumeration, every selected emitWhen root determinate,'
                     ' fingerprint absent from the emitted matched set, path inside the attested extent). null = not known. B is'
                     ' evaluated-absent only when the baseline RuleCoverage absenceKnowledge is complete-hit-set. waivedB/waivedC record'
                     ' waiver status on the two real sides.')
new = (json.dumps(doc, indent=2, ensure_ascii=False) + '\n').encode()
p.write_bytes(new)
row = {'label': 'S7 non-selection PivotPresence description', 'path': CMP_SCHEMA, 'beforeSha256': hashlib.sha256(raw).hexdigest(), 'afterSha256': hashlib.sha256(new).hexdigest()}
with open(RT / 'receipts/edits/text-edits.jsonl', 'a') as f:
    f.write(json.dumps(row) + '\n')
rows.append(row)
print(json.dumps(rows, indent=1))
