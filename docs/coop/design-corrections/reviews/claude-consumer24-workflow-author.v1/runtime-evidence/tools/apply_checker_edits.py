"""Focused controls for the consumer24 corrections. Exact-once edits into the owner checkers."""
import json, sys
sys.path.insert(0, '/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v1/tools')
from textedit import apply  # noqa: E402

CWP = 'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py'
CQP = 'docs/coop/design-corrections/workflows/check-query-projection.v3.py'
CMP = 'docs/coop/design-corrections/foundation/check-composition.v3.py'
CRP = 'docs/coop/design-corrections/foundation/check-replay.v3.py'
rows = []

WORKFLOW_CONTROLS = r'''
# ----------------------------------------------------------------------------- consumer24 corrections (root-selected M4/S7/S5/S6/A13/A11/A12/A8/A14)
def _remint_baseline(artifact, mutate):
    out = copy.deepcopy(artifact)
    mutate(out["descriptor"])
    out["baselineId"] = P.wid("baseline2", "workflow.baseline", out["descriptor"])
    return out


def _m4_rename(desc):
    for row in desc["detectorClosure"]:
        row["detectorId"] = "renamed-detector"
    for e in desc["entries"]:
        e["detectorId"] = "renamed-detector"


def _m4_entry_outside(desc):
    for e in desc["entries"]:
        e["detectorId"] = "not-in-closure"


def _m4_duplicate_row(desc):
    row = copy.deepcopy(desc["detectorClosure"][0])
    row["semanticsMajor"] += 1
    desc["detectorClosure"].append(row)


def _m4_major(desc):
    for row in desc["detectorClosure"]:
        row["semanticsMajor"] += 1


_m4_art = P.adopt_admitted_baseline_v3(*scope_graph, CUSTODY)
_m4_desc = _m4_art["descriptor"]
check(
    "m4-admitted-detector-rows-are-emission-contributions",
    all(r["detectorId"] == r["contributionId"] for r in _m4_desc["detectorClosure"])
    and {e["detectorId"] for e in _m4_desc["entries"]} <= {r["detectorId"] for r in _m4_desc["detectorClosure"]}
    and {r["detectorId"] for r in _m4_desc["detectorClosure"]} == {row["contributionId"] for row in scope_view["emission"]["rules"]},
)
check("m4-admitted-baseline-admits", P.verify_baseline_artifact_v3(_m4_art) is True)
_m4_renamed = _remint_baseline(_m4_art, _m4_rename)
must_valid("m4-reminted-rename-is-schema-valid-so-schema-alone-cannot-decide", U + "baseline:2", _m4_renamed)
check("m4-reminted-rename-has-self-consistent-new-baselineId", _m4_renamed["baselineId"] != _m4_art["baselineId"])
reject("m4-reminted-rename-refused-at-baseline-admission", lambda: P.verify_baseline_artifact_v3(_m4_renamed), "CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED")
_m4_stale = copy.deepcopy(_m4_art)
_m4_rename(_m4_stale["descriptor"])
reject("m4-stale-hash-rename-is-artifact-corruption", lambda: P.verify_baseline_artifact_v3(_m4_stale), "CONFIG.INVALID", "IMPORT.ARTIFACT_CORRUPT")
reject("m4-reminted-entry-detector-outside-closure-refused", lambda: P.verify_baseline_artifact_v3(_remint_baseline(_m4_art, _m4_entry_outside)), "CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED")
_m4_dup = _remint_baseline(_m4_art, _m4_duplicate_row)
must_valid("m4-reminted-conflicting-contribution-row-is-schema-valid", U + "baseline:2", _m4_dup)
reject("m4-reminted-conflicting-contribution-row-refused", lambda: P.verify_baseline_artifact_v3(_m4_dup), "CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED")
reject("m4-reminted-detector-major-disagreeing-with-rule-refused", lambda: P.verify_baseline_artifact_v3(_remint_baseline(_m4_art, _m4_major)), "CONFIG.INVALID", "EVALUATION.FINDING_JOIN_REFUSED")

# S7: presence knowledge over full owner-admitted comparisons (retained graphs replayed through close_run).
_S7_X1 = {"nativeSubjectId": "symbol:x1"}
_S7_X2 = {"nativeSubjectId": "symbol:x2", "signatureTokens": ["function", "x", "(", "number", ")"]}


def _s7_host(art, graph):
    h = host_from_graph({"runId": art["descriptor"]["runId"]}, graph[1])
    h["pivotRunId"] = art["descriptor"]["runId"]
    return h


def _s7_compare(art, graph, host_):
    return P.compare_admitted_v3(baseline_artifact=art, current_run=graph[0], current_objects=graph[1], current_blobs=graph[2], host=host_, profile_name="code-regression")


def _s7_entry(res, fp):
    return next(e for e in res["descriptor"]["entries"] if e["fingerprint"] == fp)


for _gate in (True, False):
    _tag = "gating" if _gate else "nongating"
    _b = RC.positive(symbol_rows=[_S7_X1, _S7_X2], scope_document=SCOPE_ALL, gate=_gate)
    _art = P.adopt_admitted_baseline_v3(*_b, CUSTODY)
    _h = _s7_host(_art, _b)
    _fps = [e["fingerprint"] for e in _art["descriptor"]["entries"]]
    check("s7-%s-baseline-records-complete-absence-knowledge" % _tag, len(_fps) == 2 and all(r["absenceKnowledge"] == "complete-hit-set" for r in _art["descriptor"]["ruleCoverage"] if r["enabled"]))
    _complete = RC.positive(symbol_rows=[_S7_X2], scope_document=SCOPE_ALL, gate=_gate)
    _kept = {o["finding"]["fingerprint"] for o in P.project_admitted_run_v3(*_complete)["occurrences"]}
    _removed = [fp for fp in _fps if fp not in _kept]
    _res = _s7_compare(_art, _complete, _h)
    must_valid("s7-%s-complete-removal-comparison-schema" % _tag, U + "comparison:2", cmp_obj(_res))
    check(
        "s7-%s-complete-enumeration-row-removal-is-lawful-code-fixed" % _tag,
        len(_removed) == 1 and _s7_entry(_res, _removed[0])["classification"] == "CODE-FIXED" and _s7_entry(_res, _removed[0])["presence"]["E4"] is False,
        [(_s7_entry(_res, fp)["classification"], _s7_entry(_res, fp)["presence"]["E4"]) for fp in _fps],
    )
    for _name, _opts in (("partial-inventory", dict(symbol_rows=[_S7_X2], symbol_state="partial")), ("budget-exhausted", dict(symbol_rows=[_S7_X1, _S7_X2], budget_limit=1))):
        _cur = RC.positive(scope_document=SCOPE_ALL, gate=_gate, **_opts)
        _curv = P.project_admitted_run_v3(*_cur)
        _rid = _curv["policy"]["rules"][0]["ruleId"]
        _res = _s7_compare(_art, _cur, _h)
        must_valid("s7-%s-%s-comparison-schema" % (_tag, _name), U + "comparison:2", cmp_obj(_res))
        _ents = [_s7_entry(_res, fp) for fp in _fps]
        check(
            "s7-%s-%s-unknown-current-absence-is-indeterminate-not-code-fixed" % (_tag, _name),
            all(e["classification"] == "INDETERMINATE" and e["indeterminateReason"] == "current-absence-unknown" and e["presence"]["E4"] is None and e["gates"] is False for e in _ents),
            [(e["classification"], e.get("indeterminateReason"), e["presence"]["E4"]) for e in _ents],
        )
        check(
            "s7-%s-%s-current-law-equals-pivot-law" % (_tag, _name),
            P.axis_presence_knowledge(_curv)["prove_absence"][_rid] is False
            and P.fingerprint_absence_known(_curv, P.presence_absence_extent(_curv), _rid, None) is False,
        )
        if _gate:
            check(
                "s7-gating-%s-verdict-indeterminate-with-independent-deficiencies" % _name,
                _res["descriptor"]["verdict"] == "indeterminate" and bool(_res["descriptor"]["ruleDeficiencies"] or _res["descriptor"]["currentExecutionDeficiencies"]),
                _res["descriptor"]["verdict"],
            )
        else:
            check("s7-nongating-%s-never-fails" % _name, _res["descriptor"]["verdict"] in ("pass", "indeterminate"), _res["descriptor"]["verdict"])
    try:
        _ub = RC.positive(symbol_rows=[_S7_X1, _S7_X2], scope_document=SCOPE_ALL, gate=_gate, budget_limit=1)
        _uart = P.adopt_admitted_baseline_v3(*_ub, CUSTODY)
        check("s7-%s-budget-exhausted-baseline-records-unknown-absence" % _tag, _uart["descriptor"]["entries"] == [] and all(r["absenceKnowledge"] == "unknown" for r in _uart["descriptor"]["ruleCoverage"]))
        _ures = _s7_compare(_uart, _b, _s7_host(_uart, _ub))
        must_valid("s7-%s-unknown-baseline-comparison-schema" % _tag, U + "comparison:2", cmp_obj(_ures))
        check(
            "s7-%s-hit-over-unknown-baseline-is-not-code-net-new" % _tag,
            bool(_ures["descriptor"]["entries"])
            and all(e["classification"] == "INDETERMINATE" and e["indeterminateReason"] == "baseline-absence-unknown" and e["presence"]["B"] is None for e in _ures["descriptor"]["entries"])
            and _ures["descriptor"]["verdict"] != "fail",
            [(e["classification"], e.get("indeterminateReason")) for e in _ures["descriptor"]["entries"]],
        )
    except Exception as _exc:
        check("s7-%s-unknown-baseline-control-executed" % _tag, False, type(_exc).__name__ + ": " + str(_exc)[:200])

_kf_new = occurrence("s7-known-new", path="src/new.ts")
_kf_old = occurrence("s7-known-old", path="src/old.ts")
_kf_art = adopt(P.project_baseline_entries([_kf_old], {"r": BINDING}, []))


def _kf_compare(cur):
    res = P.compare_v3(baseline_artifact=_kf_art, current=cur, host=host(), profile_name="code-regression", current_detectors=detectors())
    return res, {e["fingerprint"]: e for e in res["descriptor"]["entries"]}


_kf_res, _kf_e = _kf_compare(make_current(occurrences=[_kf_new], rule_results=[rr(outcome="fail", enum=incomplete_enum(), findings=[_kf_new["findingId"]])]))
check(
    "s7-known-code-net-new-failure-dominates-unknown-current-absence",
    _kf_res["descriptor"]["verdict"] == "fail"
    and _kf_e[_kf_new["finding"]["fingerprint"]]["classification"] == "CODE-NET-NEW"
    and _kf_e[_kf_old["finding"]["fingerprint"]].get("indeterminateReason") == "current-absence-unknown",
    [(e["classification"], e.get("indeterminateReason")) for e in _kf_e.values()],
)
_kc_res, _kc_e = _kf_compare(make_current(occurrences=[_kf_new], rule_results=[rr(outcome="fail", findings=[_kf_new["findingId"]])]))
check("s7-complete-current-root-proofs-prove-code-fixed", _kc_e[_kf_old["finding"]["fingerprint"]]["classification"] == "CODE-FIXED" and _kc_e[_kf_old["finding"]["fingerprint"]]["presence"]["E4"] is False)
_kn_res, _kn_e = _kf_compare(make_current(occurrences=[_kf_new], rule_results=[rr(outcome="fail", findings=[_kf_new["findingId"]])], knowledge=False))
check("s7-current-without-admitted-root-proofs-has-no-absence-knowledge", _kn_e[_kf_old["finding"]["fingerprint"]].get("indeterminateReason") == "current-absence-unknown")
must_invalid("s7-e4-null-still-refused-for-missing-reason", U + "comparison:2#/$defs/Entry", dict(_kn_e[_kf_old["finding"]["fingerprint"]], classification="CODE-FIXED", direction="vanished", indeterminateReason=None))

# S5: argvDigest is raw SHA-256 of C(exact ordered argv); no shell-joined surrogate.
_te = json.loads((HERE / "workflow-cases.v1.json").read_text())["testExecution"]
_te_sub = {"$PRJ": PRJ, "$SNAP1": SNAP, "$GRANT": "security.repo-execution-grant.v2:" + token("grant"), "$TOOL0": DET}


def _te_resolve(value):
    if isinstance(value, dict):
        return {_te_sub.get(k, k): _te_resolve(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_te_resolve(v) for v in value]
    return _te_sub.get(value, value) if isinstance(value, str) else value


_te_params = _te_resolve(_te["params"])
_te_ctx = _te_resolve(_te["ctx"])


def _te_admit(argv, digest):
    ctx_ = copy.deepcopy(_te_ctx)
    ctx_["grant"]["argvDigest"] = digest
    return P.W.admit_test_execution(dict(_te_params, argv=argv), ctx_)


def _argv_digest(v):
    return hashlib.sha256(canonical.canonical(v)).hexdigest()


_te_argv = list(_te_params["argv"])
check("s5-exact-ordered-argv-canonical-digest-admits", _te_admit(_te_argv, _argv_digest(_te_argv))["admitted"] is True)
reject("s5-shell-joined-argv-surrogate-refused", lambda: _te_admit(_te_argv, hashlib.sha256(" ".join(_te_argv).encode()).hexdigest()), "REQUEST.PRECONDITION_FAILED", "TEST.PRINCIPAL_NOT_ADMITTED")
reject("s5-repeated-argument-is-a-different-argv", lambda: _te_admit(_te_argv + [_te_argv[-1]], _argv_digest(_te_argv)), "REQUEST.PRECONDITION_FAILED", "TEST.PRINCIPAL_NOT_ADMITTED")
check("s5-repeated-argument-admits-under-its-own-digest", _te_admit(_te_argv + [_te_argv[-1]], _argv_digest(_te_argv + [_te_argv[-1]]))["admitted"] is True)
reject("s5-reordered-arguments-refused", lambda: _te_admit(list(reversed(_te_argv)), _argv_digest(_te_argv)), "REQUEST.PRECONDITION_FAILED")
check(
    "s5-member-boundaries-and-empty-strings-change-the-digest-where-a-join-collides",
    _argv_digest(["run", "a b"]) != _argv_digest(["run", "a", "b"])
    and " ".join(["run", "a b"]) == " ".join(["run", "a", "b"])
    and _argv_digest(["run", "x", ""]) != _argv_digest(["run", "x"]),
)
check("s5-test-payload-uses-the-same-recipe", P.W.test_payload(_te_params, 0, b"", b"")["argvDigest"] == _argv_digest(_te_argv))

# S6 / A13: failure goldens carry actual detail; required-delivery detail binds the committed-Run reference.
_inv3 = json.loads((HERE / "command-inventory.v3.json").read_text())
_fault_for = {v: k for k, v in P.W.FAULT_TO_ERROR.items()}
_golden_envelopes = []
for _g in _inv3["goldens"]:
    if _g["class"] not in ("request-rejected", "operational-failed"):
        continue
    _d = {"code": _g["domainDetail"], "remedy": _g["remedy"]}
    _t = {"class": _g["class"], "errorCode": _g["errorCode"], "domainDetail": _d}
    if _g["class"] == "operational-failed":
        _t["faultCause"] = _fault_for[_g["errorCode"]]
        if _g["domainDetail"] == "DELIVERY.RENDERER_FAILED_AFTER_COMMIT":
            _t["runId"] = RUN
    _ok, _why = valid(U + "command-envelope:3", {"schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "failure", "requestId": "req1_" + "c" * 32, "termination": _t, "exitCode": _g["exitCode"], "errors": [_d]})
    _golden_envelopes.append((_g["id"], _ok, _why))
check("s6-every-v3-failure-golden-forms-a-lawful-failure-envelope", len(_golden_envelopes) >= 20 and all(ok for _, ok, _ in _golden_envelopes), [x for x in _golden_envelopes if not x[1]])
check(
    "s6-formerly-unconstructible-goldens-carry-owner-detail",
    {g["id"]: g.get("domainDetail") for g in _inv3["goldens"] if g["id"] in ("doctor-report-not-producible", "query-latest-empty", "envelope-major-unsupported")}
    == {"doctor-report-not-producible": "DOCTOR.REPORT_NOT_PRODUCIBLE", "query-latest-empty": "QUERY.VIEW_UNKNOWN", "envelope-major-unsupported": "OUTPUT.ENVELOPE_MAJOR_UNSUPPORTED"},
)
_qle = next(g for g in _inv3["goldens"] if g["id"] == "query-latest-empty")
check(
    "s6-query-latest-empty-detail-is-the-query-owner-row",
    "| empty, missing, stale, or mismatched latest/snapshot/run selector | request-rejected | `IDENTITY.UNKNOWN` | `QUERY.VIEW_UNKNOWN` |" in (HERE / "query-projection-contract.v3.md").read_text()
    and _qle["errorCode"] == "IDENTITY.UNKNOWN",
)
_qle_no_detail = {k: v for k, v in _qle.items() if k != "domainDetail"}
must_invalid("s6-failure-golden-without-detail-refused", U + "command-inventory:3#/$defs/Golden", _qle_no_detail)
must_valid("s6-failure-golden-with-named-composition-admitted", U + "command-inventory:3#/$defs/Golden", dict(_qle_no_detail, detailSuppliedBy="native-route-composition"))
must_invalid("s6-named-composition-and-detail-together-refused", U + "command-inventory:3#/$defs/Golden", dict(_qle, detailSuppliedBy="native-route-composition"))
for _label, _gid in (("doctor", "doctor-report-not-producible"), ("query-empty", "query-latest-empty"), ("envelope-major", "envelope-major-unsupported")):
    _g = next(g for g in _inv3["goldens"] if g["id"] == _gid)
    _t = {"class": _g["class"], "errorCode": _g["errorCode"]}
    if _g["class"] == "operational-failed":
        _t["faultCause"] = _fault_for[_g["errorCode"]]
    _env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "failure", "requestId": "req1_" + "c" * 32, "termination": _t, "exitCode": _g["exitCode"]}
    must_invalid("s6-%s-failure-envelope-without-errors-refused" % _label, U + "command-envelope:3", _env)
    _d = {"code": _g["domainDetail"], "remedy": _g["remedy"]}
    must_valid("s6-%s-failure-envelope-with-golden-detail-admitted" % _label, U + "command-envelope:3", dict(_env, termination=dict(_t, domainDetail=_d), errors=[_d]))
_new_details = {"DOCTOR.REPORT_NOT_PRODUCIBLE", "OUTPUT.ENVELOPE_MAJOR_UNSUPPORTED", "DELIVERY.REQUIRED_PROJECTION_FAILED"}
_registry_codes = {r["code"] for r in json.loads((HERE.parent / "public-detail-registry.v1.json").read_text())["records"]}
check(
    "s6-a13-new-details-registered-and-in-both-common-mirrors",
    _new_details <= _registry_codes
    and _new_details <= set(SCHEMAS[U + "common:3"]["$defs"]["DomainDetailCode"]["enum"])
    and _new_details <= set(SCHEMAS["urn:opensip:product-v1:workflows:common"]["$defs"]["DomainDetailCode"]["enum"])
    and _registry_codes == set(SCHEMAS["urn:opensip:product-v1:workflows:common"]["$defs"]["DomainDetailCode"]["enum"]),
)
_post = {"class": "operational-failed", "errorCode": "DELIVERY.REQUIRED_FAILED", "faultCause": "delivery-required", "domainDetail": {"code": "DELIVERY.RENDERER_FAILED_AFTER_COMMIT", "remedy": "r"}}
_pre = dict(_post, domainDetail={"code": "DELIVERY.REQUIRED_PROJECTION_FAILED", "remedy": "r"})
for _label, _ref, _run in (("current", U + "common:3#/$defs/StepTermination", RUN), ("retained", "urn:opensip:product-v1:workflows:common#/$defs/StepTermination", "run2:" + token("run"))):
    must_valid("a13-%s-postcommit-detail-with-committed-run-admitted" % _label, _ref, dict(_post, runId=_run))
    must_invalid("a13-%s-postcommit-detail-without-run-refused" % _label, _ref, _post)
    must_valid("a13-%s-precommit-detail-without-run-admitted" % _label, _ref, _pre)
    must_invalid("a13-%s-precommit-detail-with-run-refused" % _label, _ref, dict(_pre, runId=_run))
    must_invalid("a13-%s-precommit-detail-on-another-class-refused" % _label, _ref, {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED", "domainDetail": {"code": "DELIVERY.REQUIRED_PROJECTION_FAILED", "remedy": "r"}})
    must_valid("a13-%s-other-operational-failure-keeps-optional-run" % _label, _ref, {"class": "operational-failed", "errorCode": "DURABILITY.COMMIT_FAILED", "faultCause": "durability-commit", "runId": _run})
    must_invalid("a13-%s-termination-exclusivity-retained" % _label, _ref, dict(_pre, reasonCodes=["VERDICT.INDETERMINATE"]))

# A11: current test execution admits only the selected truth-table profile values.
_te_enum = SCHEMAS["urn:opensip:product-v1:workflows:test-execution"]["$defs"]["EnforcementValue"]
check("a11-selected-truth-table-profile-has-no-platform-primitive-row", "ENFORCED-PLATFORM" not in (HERE.parent.parent / "artifacts" / "permission-truth-tables.v9.json").read_text())
must_invalid(
    "a11-enforced-platform-effect-not-admissible-in-current-profile",
    "urn:opensip:product-v1:workflows:test-execution#/$defs/TestExecutionStepParams",
    dict(_te_params, effects=dict(_te_params["effects"], network="ENFORCED-PLATFORM:seatbelt")),
)
check("a11-enforcement-description-states-profile-law", "cannot be claimed" in _te_enum["description"] and "admitted only when" not in _te_enum["description"])
reject(
    "a11-schema-member-still-must-equal-truth-table-row",
    lambda: P.W.admit_test_execution(dict(_te_params, effects=dict(_te_params["effects"], network="ENFORCED-AT-HOST-BROKER")), copy.deepcopy(dict(_te_ctx, grant=dict(_te_ctx["grant"], argvDigest=_argv_digest(_te_argv))))),
    "REQUEST.PRECONDITION_FAILED",
    "TEST.CONFINEMENT_CLAIM_REFUSED",
)

# A12: the existing hidden reason covers any later axis; A8/A14 published selections.
_a12_rule = {"enabled": True, "gating": True, "evidenceUse": []}
_a12_entry, _a12_sig = P.W.classify(
    hid("finding-key2", "a12"), "r",
    {"B": False, "E0": True, "E1": False, "E2": False, "E3": False, "E4": False, "waivedB": False, "waivedC": False},
    _a12_rule, _a12_rule, empty_evidence(), empty_evidence(), {"detectorId": "fixture", "method": "identical-closure"}, P.AUDIT_PROFILES["code-regression"],
)
check("a12-detector-hidden-code-net-new-gates-with-hidden-reason", _a12_entry["gates"] and _a12_entry["gateReason"] == "code-net-new-policy-hidden" and _a12_entry["subsequentDeltas"] == ["detection"] and _a12_sig == "fail")
_chapter_ws = (HERE.parents[3] / "docs/v2/contracts/product-v1/workflows-and-surfaces.md").read_text()
check("a12-hidden-reason-defined-over-any-later-axis", "hidden by a later detector, policy or scope change" in _chapter_ws and "detector" in SCHEMAS[U + "comparison:2"]["$defs"]["Entry"]["properties"]["gateReason"]["description"])
check("a8-workflows-publishes-present-listing-refusal-route", "`REQUEST.PRECONDITION_FAILED` / `EVALUATION.PROJECTION_INPUT_INCOMPLETE`" in _chapter_ws)
reject("a8-present-listing-missing-blob-route", lambda: P.parse_detector_manifest_body({}, "f" * 64, present=True), "REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE")
check("a14-conservative-evidence-attribution-preserved", "Evidence-change attribution is deliberately conservative" in _chapter_ws and "A future evidence-pivot recipe requires its own reviewed successor." in _chapter_ws)

'''

rows.append(apply('checker workflow-projection', CWP, [
    ('''def rule_cov(gating=True, required="satisfied", rule_id="r"):
    return {
        "ruleId": rule_id,
        "requiredCoverage": required,
        "enabled": True,
        "gating": gating,
        "evidenceUse": [],
    }''', '''def rule_cov(gating=True, required="satisfied", rule_id="r", knowledge="complete-hit-set"):
    return {
        "ruleId": rule_id,
        "requiredCoverage": required,
        "enabled": True,
        "gating": gating,
        "evidenceUse": [],
        "absenceKnowledge": knowledge,
    }'''),
    ('''    bindings=None,
):
    pol = policy if policy is not None else POLICY''', '''    bindings=None,
    knowledge=True,
):
    pol = policy if policy is not None else POLICY'''),
    ('''        "boundPivots": [] if bound is None else bound,
        "pivotPresence": pivots if pivots is not None else pivot_true(fps),
    }''', '''        "boundPivots": [] if bound is None else bound,
        "pivotPresence": pivots if pivots is not None else pivot_true(fps),
        # Synthetic admitted proof projection: complete roots for the (empty) selected subjects and a covering
        # extent. knowledge=False models a projection without admitted root proofs (no absence knowledge).
        **({"predicateProofs": [], "absenceExtent": {"examinedPaths": [], "scopeDocument": SCOPE, "foundationScope": {"pathPrefixes": ["."], "excludedPathPrefixes": []}, "extractionComplete": True}} if knowledge else {}),
    }'''),
    ('''
def _sha256_file(path):''', WORKFLOW_CONTROLS + '''
def _sha256_file(path):'''),
]))

QUERY_CARRIER = r'''def surface_carrier_controls(response, project):
    """Retained-Run owner graph response through the public CommandEnvelope major 3 carrier and every renderer."""
    QS = load("query_surface_projection3_checker", HERE / "query_surface_projection.v3.py")
    inv = json.loads((HERE / "command-inventory.v3.json").read_text())
    command = next(c for c in inv["commands"] if c["name"] == "query")
    term = copy.deepcopy(response.get("termination") or {"class": "success"})
    env = {
        "schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "query", "requestId": host_obs()["requestId"],
        "projectId": project, "termination": term, "exitCode": QS.Wlegacy.EXIT[term["class"]],
        "query": QS.graph_query_result_summary(response), "querySurface": "graph-query-response", "queryResponse": copy.deepcopy(response),
    }
    must_valid("m5-retained-run-graph-response-in-public-envelope", U + "command-envelope:3", env)
    try:
        proj = QS.project_query_surface(response, term, envelope=env, command=command)
        rnd = QS.render_query_formats(proj["parity"], env, command, hints=["hint"])
        bodies = {r["format"]: r["body"] for r in rnd["renderings"]}
        check("m5-retained-run-all-advertised-renderers-hold-parity", rnd["ok"] and rnd["parityHolds"] and sorted(bodies) == ["agent", "human", "json"], rnd.get("ok"))
        check("m5-retained-run-json-rendering-is-the-schema-valid-envelope", bodies["json"] == env and valid(U + "command-envelope:3", bodies["agent"])[0] and "agentHints" not in bodies["json"])
        check("m5-retained-run-query-response-is-the-owner-response", proj["parity"]["query-response"] == response and proj["parity"]["total-items"] == response["context"]["totalItems"])
        partial = {k: v for k, v in proj["parity"].items() if k != "query-response"}
        failed = QS.render_query_formats(partial, env, command)
        dt = failed["deliveryTermination"] or {}
        check(
            "m5-a13-retained-run-missing-query-response-is-precommit-delivery-fault",
            failed["ok"] is False and "runId" not in dt and dt.get("domainDetail", {}).get("code") == "DELIVERY.REQUIRED_PROJECTION_FAILED" and valid(U + "common:3#/$defs/StepTermination", dt)[0],
            dt,
        )
    except Exception as exc:
        check("m5-retained-run-all-advertised-renderers-hold-parity", False, type(exc).__name__ + ": " + str(exc)[:200])
    missing = copy.deepcopy(env)
    del missing["queryResponse"]
    must_invalid("m5-retained-run-graph-envelope-cannot-omit-query-response", U + "command-envelope:3", missing)
    other_project = copy.deepcopy(env)
    other_project["projectId"] = project_id("elsewhere")
    try:
        QS.project_query_surface(response, term, envelope=other_project, command=command)
        check("m5-retained-run-envelope-project-join", False, "admitted")
    except QS.QuerySurfaceProjectionError as exc:
        check("m5-retained-run-envelope-project-join", exc.code == "QUERY_SURFACE_PROJECT_JOIN", exc.code)


def owner_controls():'''

rows.append(apply('checker query-projection', CQP, [
    ('''def owner_controls():''', QUERY_CARRIER),
    ('''    cites = neigh["context"]["evidence"]["deficiencyCitations"]
    check("owner-deficiency-keeps-inputRefs", bool(cites) and all("inputRefs" in c and c["source"] in Q.DEFICIENCY_SOURCES for c in cites), cites[:2])
''', '''    cites = neigh["context"]["evidence"]["deficiencyCitations"]
    check("owner-deficiency-keeps-inputRefs", bool(cites) and all("inputRefs" in c and c["source"] in Q.DEFICIENCY_SOURCES for c in cites), cites[:2])
    surface_carrier_controls(neigh, project)
    refuse("a8-request-project-differs-from-admitted-run", lambda: ex(request("graph.neighbors", project_id("elsewhere"), {"runId": run_key}, {
        "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": foo_ep,
    })), "REQUEST.PRECONDITION_FAILED", "QUERY.PARAMS_MALFORMED")
    check("a8-query-contract-publishes-project-mismatch-route", "| request `projectId` differs from the admitted Run's project | request-rejected | `REQUEST.PRECONDITION_FAILED` | `QUERY.PARAMS_MALFORMED` |" in (HERE / "query-projection-contract.v3.md").read_text())
'''),
]))

COMPOSITION = r'''check('strong-kleene-known-or-true',E.truth('or',['indeterminate','true'])=='true')
# A6: first-applicable correspondence precedence; one deficiency per unmatched finding, reason equals it.
def corr_rows(b):
    fs=[v for d,v in b['objects'].values() if d=='finding'];rr=b['proof']['ruleResults'][0]
    return sorted((f['subjectId'],f['correspondence']['reason']) for f in fs if f['fingerprint'] is None),sorted((d['subjectId'],d['cause']) for d in rr['deficiencies'] if d['source']=='correspondence')
def peer(i,native):
    first=next(iter(i['population'].values()));row=copy.deepcopy(first['row']);row['nativeSubjectId']=native
    sid=E.M.identifier('evaluation-subject',{'schemaVersion':3,'universe':first['universe'],'kind':'symbol','nativeSubjectId':native})
    i['population'][sid]={'subjectId':sid,'universe':first['universe'],'kind':'symbol','row':row,'collisionPopulationComplete':first['collisionPopulationComplete']}
    i['enumerations']['r']['selectedSubjectIds']=E.cset(i['population']);i['inventoryRowCount']=i['inventoryLocatorCount']=len(i['population'])
seen=set()
i=make(kind='symbol');s=next(iter(i['population'].values()));s['row']['projections']=[];s['collisionPopulationComplete']=False
got,defs=corr_rows(E.compose(i,scanner()));seen|={r for _,r in got}|{c for _,c in defs};check('a6-projection-unavailable-precedes-population-incomplete',[r for _,r in got]==['projection-unavailable'] and got==defs)
i=make(kind='symbol');s=next(iter(i['population'].values()));s['row']['projections'][0]['signatureTokens']=[];s['collisionPopulationComplete']=False
got,defs=corr_rows(E.compose(i,scanner()));seen|={r for _,r in got}|{c for _,c in defs};check('a6-empty-signature-tokens-are-projection-unavailable',[r for _,r in got]==['projection-unavailable'] and got==defs)
i=make(kind='symbol');peer(i,'symbol:g')
for s in i['population'].values():s['collisionPopulationComplete']=False
got,defs=corr_rows(E.compose(i,scanner()));seen|={r for _,r in got}|{c for _,c in defs};check('a6-population-incomplete-precedes-signature-ambiguous',[r for _,r in got]==['population-incomplete','population-incomplete'] and got==defs)
i=make(kind='symbol');peer(i,'symbol:g')
got,defs=corr_rows(E.compose(i,scanner()));seen|={r for _,r in got}|{c for _,c in defs};check('a6-complete-shared-signature-is-signature-ambiguous',[r for _,r in got]==['signature-ambiguous','signature-ambiguous'] and got==defs)
i=make(kind='symbol');peer(i,'symbol:g');next(iter(i['population'].values()))['row']['projections']=[]
got,defs=corr_rows(E.compose(i,scanner()));seen|={r for _,r in got}|{c for _,c in defs};check('a6-mixed-population-one-cause-per-unmatched-finding',len(got)==1 and got==defs and got[0][1]=='projection-unavailable')
check('a6-composed-causes-are-the-three-published-causes-only',seen=={'projection-unavailable','population-incomplete','signature-ambiguous'})
# A9: a required declared evidence kind unavailable in the Plan applies independently of the root branch.
RUNTIME_NONE={'op':'none','relation':'runtime-observation','minResolution':'observed','filters':[],'evidence':'runtime'}
MISSING=[{'source':'import','cause':'evidence-kind-unavailable','subjectId':None,'predicateId':None,'inputRefs':[],'evidenceKind':'runtime','nativeCause':None,'universe':None}]
i=make(atom=RUNTIME_NONE,requirement='required');i['requiredEvidenceDeficiencies']['r']=copy.deepcopy(MISSING)
b=E.compose(i,scanner('false'));check('a9-required-import-unavailable-under-determinate-false-root-is-indeterminate',b['proof']['ruleResults'][0]['outcome']=='indeterminate' and b['proof']['verdict']=='indeterminate' and b['proof']['predicateProofs'][0]['value']=='false')
b=E.compose(i,scanner('true'));check('a9-known-live-failure-dominates-missing-required-import',b['proof']['ruleResults'][0]['outcome']=='fail' and b['proof']['verdict']=='fail')
i['policy']['rules'][0]['gate']=False;rebind(i);b=E.compose(i,scanner('false'));check('a9-advisory-rule-with-missing-required-import-passes',b['proof']['ruleResults'][0]['outcome']=='pass' and b['proof']['verdict']=='pass')
i=make(atom=RUNTIME_NONE,requirement='optional');b=E.compose(i,scanner('false'));check('a9-optional-evidence-use-adds-no-required-deficiency',b['proof']['ruleResults'][0]['outcome']=='pass' and not any(d['source']=='import' for d in b['proof']['ruleResults'][0]['deficiencies']))
'''

rows.append(apply('checker composition', CMP, [
    ('''check('strong-kleene-known-or-true',E.truth('or',['indeterminate','true'])=='true')
''', COMPOSITION),
]))

REPLAY = r'''  exports[name]=graph;rows.append({'case':name,'ownerAdmission':'ADMIT','replay':actual,'unmatchedFindings':unmatched_count})
 # A6 on complete replayed Runs: co-occurring correspondence conditions publish the first applicable cause once.
 for name,options,want_reasons in [
  ('correspondence-projection-unavailable-precedes-population-incomplete',{'symbol_rows':[{'nativeSubjectId':'symbol:x','projectionAvailable':False}],'symbol_state':'partial'},['projection-unavailable']),
  ('correspondence-population-incomplete-precedes-signature-ambiguous',{'symbol_rows':[{'nativeSubjectId':'symbol:x1'},{'nativeSubjectId':'symbol:x2'}],'symbol_state':'partial'},['population-incomplete','population-incomplete']),
 ]:
  graph=positive(**options);actual=R.replay(*graph);run,objects,blobs=graph;proof=objects[objects[run['evaluationSealId']][1]['proofBundleId']][1]
  findings=[objects[fid][1] for fid in proof['findingIds']]
  reasons=sorted((f['subjectId'],f['correspondence']['reason']) for f in findings if f['fingerprint'] is None)
  corr=sorted((d['subjectId'],d['cause']) for r in proof['ruleResults'] for d in r['deficiencies'] if d['source']=='correspondence')
  assert [c for _,c in reasons]==want_reasons and corr==reasons,(name,reasons,corr)
  exports[name]=graph;rows.append({'case':name,'ownerAdmission':'ADMIT','replay':actual,'correspondenceReasons':[c for _,c in reasons]})
 # A9 on complete replayed Runs: required evidence kind absent from the Plan applies regardless of the root value.
 none_file={'op':'none','relation':'file','minResolution':'enumerated','filters':[]}
 for name,options,want in [
  ('required-import-unavailable-false-root-gating-indeterminate',{'atom_override':none_file,'evidence_use':[{'kind':'runtime','requirement':'required'}]},'indeterminate'),
  ('required-import-unavailable-known-live-failure-dominates',{'evidence_use':[{'kind':'runtime','requirement':'required'}]},'fail'),
  ('required-import-unavailable-advisory-pass',{'atom_override':none_file,'evidence_use':[{'kind':'runtime','requirement':'required'}],'gate':False},'pass'),
 ]:
  graph=positive(**options);actual=R.replay(*graph);run,objects,blobs=graph;proof=objects[objects[run['evaluationSealId']][1]['proofBundleId']][1];rr=proof['ruleResults'][0]
  roots={p['value'] for p in proof['predicateProofs'] if p['predicateId']=='p'}
  assert actual['verdict']==want and rr['outcome']==want and any(d['source']=='import' and d['cause']=='evidence-kind-unavailable' for d in rr['deficiencies']),(name,actual,rr['outcome'])
  assert want!='indeterminate' or roots=={'false'},(name,roots)
  exports[name]=graph;rows.append({'case':name,'ownerAdmission':'ADMIT','replay':actual,'ruleOutcome':rr['outcome'],'rootValues':sorted(roots)})
'''

rows.append(apply('checker replay', CRP, [
    ('''  exports[name]=graph;rows.append({'case':name,'ownerAdmission':'ADMIT','replay':actual,'unmatchedFindings':unmatched_count})
''', REPLAY),
]))
print(json.dumps(rows, indent=1))
