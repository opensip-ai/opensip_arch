"""Resume of apply_s7_nonselection.py (see receipts/edits/FAILED-ATTEMPT-apply_s7_nonselection.md).

Applies only the parts that attempt did not write: projection contract §12/§13 (corrected `subjectPath` anchor),
checker controls, and the guarded PivotPresence description.
"""
import hashlib, json, sys
sys.path.insert(0, '/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v1/tools')
from textedit import apply, ROOT, RT  # noqa: E402

WPC = 'docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md'
CWP = 'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py'
CMP_SCHEMA = 'docs/coop/design-corrections/workflows/schemas/evaluator3/comparison-result.schema.json'
rows = []

rows.append(apply('S7 non-selection prose projection contract (resume)', WPC, [
    ('''E4 is `true` for a matched current occurrence, `false` only when the current rule proves absence under the pivot predicate including the attested path extent, else `null`. B is `false` for a non-entry only when the baseline RuleCoverage records `absenceKnowledge=complete-hit-set` (recorded at adoption by the same predicate), else `null`.''',
     '''Every side is `true` for a matched occurrence; `false` for non-selection (that side's policy does not enable the rule or its ScopeDocument does not select the path; for B the embedded baseline documents) or for evaluated absence (the side's rule proves absence under the pivot predicate including the attested path extent; for B the baseline RuleCoverage records `absenceKnowledge=complete-hit-set`, recorded at adoption by the same predicate); else `null`.'''),
    ('''- Absence False is not claimed for a fingerprint whose `subjectPath` is outside the attested inventory examined extent or the pivot ScopeDocument, unless foundation `plan.scopeDigest` covers the path and inventories are complete (deleted under a covering census).''',
     '''- Evaluated absence False is not claimed for a fingerprint whose `subjectPath` is outside the attested inventory examined extent, unless foundation `plan.scopeDigest` covers the path and inventories are complete (deleted under a covering census). A path the pivot's own ScopeDocument does not select, or a rule its policy does not enable, is non-selection `false` on that pivot, not evaluated absence (§12).'''),
]))

rows.append(apply('S7 non-selection controls (resume)', CWP, [
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

p = ROOT / CMP_SCHEMA
raw = p.read_bytes()
doc = json.loads(raw)
assert (json.dumps(doc, indent=2, ensure_ascii=False) + '\n').encode() == raw, 'round-trip guard refused'
pp = doc['$defs']['PivotPresence']
assert pp['description'].startswith('Presence knowledge of the fingerprint at each pivot.')
pp['description'] = ('Presence knowledge of the fingerprint at each pivot. true = a known matched occurrence (waived included). false ='
                     " non-selection (that side's policy does not enable the rule or its ScopeDocument does not select the path; attributed"
                     " to the policy or scope axis, never CODE-FIXED) or evaluated absence proved by that side's rule under the"
                     ' complete-hit-set law (enabled rule, evaluated, complete enumeration, every selected emitWhen root determinate,'
                     ' fingerprint absent from the emitted matched set, path inside the attested extent). null = not known. B is'
                     ' evaluated-absent only when the baseline RuleCoverage absenceKnowledge is complete-hit-set. waivedB/waivedC record'
                     ' waiver status on the two real sides.')
new = (json.dumps(doc, indent=2, ensure_ascii=False) + '\n').encode()
p.write_bytes(new)
row = {'label': 'S7 non-selection PivotPresence description (resume)', 'path': CMP_SCHEMA, 'beforeSha256': hashlib.sha256(raw).hexdigest(), 'afterSha256': hashlib.sha256(new).hexdigest()}
with open(RT / 'receipts/edits/text-edits.jsonl', 'a') as f:
    f.write(json.dumps(row) + '\n')
rows.append(row)
print(json.dumps(rows, indent=1))
