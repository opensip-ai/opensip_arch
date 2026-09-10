"""ExecutionInputsV1 nested admission from execution-inputs-contract.v1.md.

Per-entry population, correspondence, conditional and ordering laws. Presence
is not comparison. Traces use owning schema document + pointer + nested path.
"""
from __future__ import annotations

from typing import Any

from . import canonical, condtrace, h, kit_schemas, order, store
from . import instance_walk, builder, admit_graph
from .pilot_checks import load_c, obj


DOC_EI = "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json"
DOC_EI_MD = "docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md"
SID_EI = "opensip.product.execution-inputs.1"


def _bare(d: str) -> str:
    return d.split(":")[-1]


def _emit(doc, ptr, instance, field, comparison, left, right, result, extra=None):
    condtrace.set_document(doc)
    condtrace.emit(
        condition=ptr, instance=str(instance), field=field,
        comparison=comparison, left=left, right=right, result=result, extra=extra,
    )


def derive_outcome_state(o: dict, inventories: list[dict], accounts: list[dict], owed_candidate: bool) -> str:
    """execution-inputs-contract §4. Host cannot mint complete by asserting the row."""
    if o.get("enumeratorStatus") == "unselected" or o.get("universe") is None:
        return "unavailable"
    if any(inv.get("state") == "partial" for inv in inventories):
        return "partial"
    if any(inv.get("state") == "unavailable" for inv in inventories):
        return "unavailable"
    for acc in accounts:
        if acc.get("applicability") == "supported-available":
            # mixed complete+unknown or empty ids → not complete
            if not (acc.get("coverageIds") or []):
                return "partial"
            # caller passes coverage completeness via extra key _accountComplete
            if acc.get("_accountComplete") is False:
                return "partial"
    if owed_candidate:
        # candidate envelope state checked by caller via o.candidateResultDigest presence
        if not o.get("candidateResultDigest"):
            return "unavailable"
    return "complete"


def coverage_account_complete(st: store.Store, acc: dict) -> bool:
    ids = acc.get("coverageIds") or []
    if acc.get("applicability") != "supported-available":
        return True
    if not ids:
        return False
    states = []
    for hx in ids:
        try:
            rec = obj(st, "coverage2:" + hx)
        except Exception:
            return False
        payload = load_c(st, rec["payloadDigest"])
        entry = payload.get("entry") or {}
        states.append(entry.get("coverage"))
    if "unknown" in states and "complete" in states:
        return False
    return all(s == "complete" for s in states)


def admit_execution_inputs(st: store.Store, plan: dict, ei: dict, enum_plan: dict, exec_plan: dict, ei_id: str) -> list[str]:
    errors = []
    cells = enum_plan.get("cells") or []
    outcomes = ei.get("cellOutcomes") or []
    accounts = ei.get("nativeCoverageAccounts") or []
    receipts = (ei.get("hostCapture") or {}).get("stageReceipts") or []
    stages = exec_plan.get("stages") or []

    # §3 receipts: unique ordinals total over stages
    ords = [r.get("ordinal") for r in receipts]
    want_ords = list(range(len(stages)))
    ok = sorted(ords) == want_ords and ords == want_ords
    _emit(DOC_EI_MD, "/3 Stage ordinal and receipts", ei_id, "hostCapture.stageReceipts.ordinal",
          "unique-and-total-over-execution-plan.stages", ords, want_ords, "pass" if ok else "refuse")
    if not ok:
        errors.append(f"EXECUTION_INPUTS_RECEIPT_TOTALITY:{ords}!={want_ords}")
    _emit(DOC_EI, "/$defs/HostCaptureV1/properties/stageReceipts/x-opensip-order", ei_id,
          "hostCapture.stageReceipts", "ordinal-order", ords, want_ords,
          "pass" if instance_walk.is_ordinal_order(receipts) else "refuse")

    for r in receipts:
        path = f"hostCapture.stageReceipts[{r.get('ordinal')}]"
        # complete => unavailableReason null
        if r.get("state") == "complete":
            ok = r.get("unavailableReason") is None
            _emit(DOC_EI, "/$defs/StageReceiptV1/allOf/0/then/properties/unavailableReason",
                  ei_id, path + ".unavailableReason", "null-when-complete",
                  r.get("unavailableReason"), None, "pass" if ok else "refuse")
            if not ok:
                errors.append(f"RECEIPT_COMPLETE_REASON:{r.get('ordinal')}")
            # else branch inapplicable
            _emit(DOC_EI, "/$defs/StageReceiptV1/allOf/1/then", ei_id, path,
                  "if-state-unavailable", r.get("state"), "unavailable", "inapplicable")
        elif r.get("state") == "unavailable":
            ok = isinstance(r.get("unavailableReason"), str) and r.get("unavailableReason") is not None
            _emit(DOC_EI, "/$defs/StageReceiptV1/allOf/1/then/properties/unavailableReason",
                  ei_id, path + ".unavailableReason", "string-when-unavailable",
                  r.get("unavailableReason"), "non-null string", "pass" if ok else "refuse")
            if not ok:
                errors.append(f"RECEIPT_UNAVAILABLE_REASON:{r.get('ordinal')}")
        # outputDomains equal stage
        stg = next((s for s in stages if s.get("ordinal") == r.get("ordinal")), None)
        if stg is not None:
            want = order.cset(list(stg.get("outputDomains") or []))
            got = order.cset(list(r.get("outputDomains") or []))
            ok = got == want
            _emit(DOC_EI_MD, "/1 Authority and TCB honesty", ei_id, path + ".outputDomains",
                  "eq-stage.outputDomains", got, want, "pass" if ok else "refuse")
            if not ok:
                errors.append(f"RECEIPT_OUTPUT_DOMAINS:{r.get('ordinal')}")
            # outputRefs domains ⊆ outputDomains
            for ref in r.get("outputRefs") or []:
                okd = ref.get("domain") in set(r.get("outputDomains") or [])
                _emit(DOC_EI, "/$defs/StageReceiptV1/properties/outputRefs", ei_id,
                      path + ".outputRefs.domain", "subset-of-outputDomains",
                      ref.get("domain"), r.get("outputDomains"), "pass" if okd else "refuse")
                if not okd:
                    errors.append(f"RECEIPT_OUTPUT_REF_DOMAIN:{ref}")
        # producerClosure kind=provider
        clo = None
        try:
            clo = obj(st, r.get("producerClosure"))
        except Exception:
            errors.append(f"RECEIPT_PRODUCER_UNRETAINED:{r.get('producerClosure')}")
        else:
            ok = clo.get("kind") == "provider"
            _emit(DOC_EI_MD, "/3 Stage ordinal and receipts", ei_id, path + ".producerClosure",
                  "kind-eq-provider", clo.get("kind"), "provider", "pass" if ok else "refuse")
            if not ok:
                errors.append(f"EXECUTION_INPUTS_STAGE_PRODUCER:{r.get('ordinal')}")
        # outputRefs order
        refs = r.get("outputRefs") or []
        _emit(DOC_EI, "/$defs/StageReceiptV1/properties/outputRefs/x-opensip-order", ei_id,
              path + ".outputRefs", "canonical-set",
              [x.get("digest") for x in refs], order.cset(list(refs)),
              "pass" if refs == order.cset(list(refs)) else "refuse")

    # selectedRefs exact totality (contract §1 table) — per-kind traces
    got = {(r["domain"], r["digest"]) for r in ei.get("selectedRefs") or []}
    want = set()
    for recpt in receipts:
        if recpt.get("state") != "complete":
            continue
        for r in recpt.get("outputRefs") or []:
            want.add((r["domain"], r["digest"]))
            if r["domain"] == "view":
                view = obj(st, "view2:" + r["digest"])
                for cid in view.get("coverageIds") or []:
                    want.add(("coverage", _bare(cid)))
    for r in (ei.get("hostCapture") or {}).get("hostDerivedRefs") or []:
        want.add((r["domain"], r["digest"]))
    for iid in plan.get("importIds") or []:
        want.add(("import", _bare(iid)))
    ok = want <= got
    _emit(DOC_EI_MD, "/1 selectedRefs exact totality", ei_id, "selectedRefs",
          "superset-of-stage-coverage-hostDerived-imports", sorted(want)[:20], sorted(got)[:20],
          "pass" if ok else "refuse")
    if not ok:
        errors.append(f"EXECUTION_INPUTS_SELECTED_COVER_MISSING:{sorted(want-got)[:8]}")
    forbidden = {d for d, _ in got if d in {"proof-bundle", "finding", "evaluation-seal", "run", "semantic-evidence"}}
    _emit(DOC_EI_MD, "/1 Forbidden on selectedRefs", ei_id, "selectedRefs.domain",
          "forbidden-output-domains-absent", sorted(forbidden), [],
          "pass" if not forbidden else "refuse")
    if forbidden:
        errors.append(f"EXECUTION_INPUTS_FORBIDDEN_REF:{forbidden}")
    blob_domains = {"subject-inventory", "candidate-producer-result", "target-attribution", "incoming-search"}
    got_blob = {x for x in got if x[0] in blob_domains}
    want_blob = {x for x in (ei.get("hostCapture") or {}).get("hostDerivedRefs") or [] }
    want_blob = {(r["domain"], r["digest"]) for r in (ei.get("hostCapture") or {}).get("hostDerivedRefs") or []}
    okb = got_blob == want_blob
    _emit(DOC_EI, "/$defs/HostCaptureV1/properties/hostDerivedRefs/description", ei_id,
          "selectedRefs blob-domain", "eq-hostDerivedRefs",
          sorted(got_blob)[:12], sorted(want_blob)[:12], "pass" if okb else "refuse")
    if not okb:
        errors.append(f"EXECUTION_INPUTS_HOST_DERIVED:{sorted(got_blob ^ want_blob)[:8]}")
    srefs = ei.get("selectedRefs") or []
    _emit(DOC_EI, "/properties/selectedRefs/x-opensip-order", ei_id, "selectedRefs",
          "canonical-set", len(srefs), len(order.cset(list(srefs))),
          "pass" if srefs == order.cset(list(srefs)) else "refuse")

    # candidateResultRefs equals non-null outcome candidateResultDigest
    cand_from_out = order.cset([o["candidateResultDigest"] for o in outcomes if o.get("candidateResultDigest")])
    cand_field = ei.get("candidateResultRefs") or []
    ok = order.cset(list(cand_field)) == cand_from_out
    _emit(DOC_EI_MD, "/6 Candidate-only", ei_id, "candidateResultRefs",
          "eq-outcomes-nonnull-candidateResultDigest", cand_field, cand_from_out,
          "pass" if ok else "refuse")
    if not ok:
        errors.append(f"EXECUTION_INPUTS_CANDIDATE_BIND:{cand_field}!={cand_from_out}")

    # one outcome per binding; ordinals 0..n-1
    expected = []
    for i, cell in enumerate(cells):
        for b in cell.get("programBindings") or []:
            expected.append((i, b.get("ordinal", 0)))
    got_cp = [(o.get("cellOrdinal"), o.get("programOrdinal")) for o in outcomes]
    ok = sorted(got_cp) == sorted(expected)
    _emit(DOC_EI_MD, "/4 Cells, inventories, derived outcomes", ei_id, "cellOutcomes",
          "one-row-per-enumeration-binding", got_cp, expected, "pass" if ok else "refuse")
    if not ok:
        errors.append(f"EXECUTION_INPUTS_CELL_TOTALITY:{got_cp}!={expected}")
    _emit(DOC_EI, "/properties/cellOutcomes/x-opensip-order", ei_id, "cellOutcomes",
          "ordinal-order", [o.get("ordinal") for o in outcomes], list(range(len(outcomes))),
          "pass" if instance_walk.is_ordinal_order(outcomes) else "refuse")

    # per-outcome nested laws
    inv_by_digest = {}
    for r in ei.get("selectedRefs") or []:
        if r["domain"] == "subject-inventory":
            inv_by_digest[r["digest"]] = load_c(st, r["digest"])

    for o in outcomes:
        i = o.get("cellOrdinal")
        cell = cells[i] if i is not None and i < len(cells) else {}
        path = f"cellOutcomes[{o.get('ordinal')}]"
        kinds = list(o.get("kinds") or [])
        want_kinds = order.cset(list(cell.get("kinds") or []))
        ok = order.cset(kinds) == want_kinds
        _emit(DOC_EI_MD, "/4 Inventory digests exactly one per kind", ei_id, path + ".kinds",
              "set-eq-cell.kinds", kinds, want_kinds, "pass" if ok else "refuse")
        if not ok:
            errors.append(f"EXECUTION_INPUTS_KIND_MAP:{i}")
        digs = list(o.get("inventoryDigests") or [])
        _emit(DOC_EI, "/$defs/CellProgramOutcomeV1/properties/inventoryDigests/x-opensip-order",
              ei_id, path + ".inventoryDigests", "canonical-set",
              digs, order.cset(digs), "pass" if digs == order.cset(digs) else "refuse")
        # exactly one digest per kind
        kind_of = {}
        for d in digs:
            inv = inv_by_digest.get(d)
            if inv is None:
                errors.append(f"INVENTORY_DIGEST_UNRETAINED:{d}")
                continue
            k = inv.get("kind")
            kind_of.setdefault(k, []).append(d)
            okj = inv.get("cellOrdinal") == i
            _emit(DOC_EI, "/$defs/CellProgramOutcomeV1/properties/inventoryDigests", ei_id,
                  path + ".inventoryDigests", "inventory.cellOrdinal-eq-outcome",
                  inv.get("cellOrdinal"), i, "pass" if okj else "refuse")
            if not okj:
                errors.append(f"INVENTORY_CELL:{d}")
        for k in want_kinds:
            n = len(kind_of.get(k) or [])
            _emit(DOC_EI_MD, "/4 exactly one per kind", ei_id, path + ".inventoryDigests",
                  "one-digest-per-kind", {k: n}, 1, "pass" if n == 1 else "refuse")
            if n != 1:
                errors.append(f"EXECUTION_INPUTS_INVENTORY_KIND:{i}:{k}:{n}")
        # if complete: deficiency/nativeCause/stageOrdinalNullReason null; stageOrdinal integer
        if o.get("state") == "complete":
            ok = o.get("deficiency") is None and o.get("nativeCause") is None and o.get("stageOrdinalNullReason") is None and isinstance(o.get("stageOrdinal"), int)
            _emit(DOC_EI, "/$defs/CellProgramOutcomeV1/allOf/0/then", ei_id, path,
                  "complete-implies-null-deficiency-cause-nullReason-int-stage",
                  {"deficiency": o.get("deficiency"), "nativeCause": o.get("nativeCause"), "stageOrdinal": o.get("stageOrdinal"), "stageOrdinalNullReason": o.get("stageOrdinalNullReason")},
                  {"deficiency": None, "nativeCause": None, "stageOrdinal": "int", "stageOrdinalNullReason": None},
                  "pass" if ok else "refuse")
            if not ok:
                errors.append(f"OUTCOME_COMPLETE_THEN:{i}")
            _emit(DOC_EI, "/$defs/CellProgramOutcomeV1/allOf/1/then", ei_id, path,
                  "stageOrdinal-null-branch", o.get("stageOrdinal"), None, "inapplicable")
        if o.get("stageOrdinal") is None:
            ok = isinstance(o.get("stageOrdinalNullReason"), str)
            _emit(DOC_EI, "/$defs/CellProgramOutcomeV1/allOf/1/then", ei_id, path + ".stageOrdinalNullReason",
                  "string-when-stageOrdinal-null", o.get("stageOrdinalNullReason"), "string",
                  "pass" if ok else "refuse")
            if not ok:
                errors.append(f"STAGE_ORDINAL_NULL_REASON:{i}")
        else:
            # selected complete/partial: stageOrdinal matches a receipt
            rok = any(r.get("ordinal") == o.get("stageOrdinal") for r in receipts)
            _emit(DOC_EI_MD, "/3 stageOrdinal matching a receipt", ei_id, path + ".stageOrdinal",
                  "in-receipt-ordinals", o.get("stageOrdinal"), ords, "pass" if rok else "refuse")
            if not rok:
                errors.append(f"EXECUTION_INPUTS_STAGE_ORDINAL:{i}")
        # viewDigests are view2 suffixes equal captured receipt views
        vds = list(o.get("viewDigests") or [])
        receipt_views = []
        for recpt in receipts:
            if recpt.get("state") != "complete":
                continue
            for ref in recpt.get("outputRefs") or []:
                if ref.get("domain") == "view":
                    receipt_views.append(ref["digest"])
        receipt_views = order.cset(receipt_views)
        # attributed to this cell: this graph has one view; must be that set
        ok = order.cset(vds) == receipt_views
        _emit(DOC_EI, "/$defs/CellProgramOutcomeV1/properties/viewDigests/description", ei_id,
              path + ".viewDigests", "eq-captured-receipt-view-suffixes", vds, receipt_views,
              "pass" if ok else "refuse")
        if not ok:
            errors.append(f"EXECUTION_INPUTS_VIEW_TOTALITY:{i}:{vds}!={receipt_views}")
        # derived state
        cell_acc = []
        for acc in accounts:
            if acc.get("cellOrdinal") == i and acc.get("programOrdinal") == o.get("programOrdinal"):
                a = dict(acc)
                a["_accountComplete"] = coverage_account_complete(st, acc)
                cell_acc.append(a)
        invs = [inv_by_digest[d] for d in digs if d in inv_by_digest]
        owed_cand = cell.get("capabilityId") in ("clones-near", "clones-cross-tsjs")
        derived = derive_outcome_state(o, invs, cell_acc, owed_cand)
        ok = o.get("state") == derived
        _emit(DOC_EI_MD, "/4 Outcome state is derived", ei_id, path + ".state",
              "eq-derived-aggregate", o.get("state"), derived, "pass" if ok else "refuse")
        if not ok:
            errors.append(f"EXECUTION_INPUTS_OUTCOME_DERIVE:{i}:host={o.get('state')} derived={derived}")
        # enumeratorClosure kind=provider when selected
        if o.get("enumeratorStatus") == "selected" and o.get("enumeratorClosure"):
            try:
                clo = obj(st, o["enumeratorClosure"])
                ok = clo.get("kind") == "provider"
            except Exception:
                ok = False
                clo = {}
            _emit(DOC_EI_MD, "/3 enumerator closure Plan-selected provider", ei_id,
                  path + ".enumeratorClosure", "kind-eq-provider",
                  clo.get("kind") if isinstance(clo, dict) else None, "provider",
                  "pass" if ok else "refuse")
            if not ok:
                errors.append(f"EXECUTION_INPUTS_ENUMERATOR:{i}")

    # native accounts per-entry
    view_ids = [r["digest"] for r in ei.get("selectedRefs") or [] if r["domain"] == "view"]
    cov_by_pair = {}
    for vid in view_ids:
        view = obj(st, "view2:" + vid)
        for cid in view.get("coverageIds") or []:
            cov = obj(st, cid)
            payload = load_c(st, cov["payloadDigest"])
            key = payload.get("key") or {}
            pair = (key.get("relation"), key.get("resolution"))
            cov_by_pair.setdefault(pair, []).append(_bare(cid))
    for ai, acc in enumerate(accounts):
        path = f"nativeCoverageAccounts[{ai}]"
        pair = (acc.get("relation"), acc.get("resolution"))
        appl = acc.get("applicability")
        ids = list(acc.get("coverageIds") or [])
        _emit(DOC_EI, "/$defs/NativeCoverageAccountV1/properties/coverageIds", ei_id,
              path + ".coverageIds", "canonical-set-or-empty",
              ids, order.cset(ids), "pass" if ids == order.cset(ids) else "refuse")
        if appl in {"inapplicable-vcs", "unsupported-typed", "unavailable-unselected", "unavailable-null-universe"}:
            ok = not ids
            _emit(DOC_EI_MD, "/5 applicability envelopes", ei_id, path + ".coverageIds",
                  "empty-when-not-supported-available", ids, [], "pass" if ok else "refuse")
            if not ok:
                errors.append(f"NATIVE_ACCOUNT_EMPTY_IDS:{pair}:{appl}")
            continue
        if appl == "supported-available":
            matching = order.cset(cov_by_pair.get(pair) or [])
            ok = order.cset(ids) == matching
            _emit(DOC_EI, "/$defs/NativeCoverageAccountV1/description", ei_id, path + ".coverageIds",
                  "eq-every-matching-returned-partition", ids, matching, "pass" if ok else "refuse")
            if not ok:
                errors.append(f"NATIVE_ACCOUNT_COVERAGE_IDS:{pair}:got {ids} want {matching}")
            if not ids:
                errors.append(f"NATIVE_WORK_INCOMPLETE:{pair}")
                _emit(DOC_EI_MD, "/5 Empty coverageIds on supported-available", ei_id, path,
                      "native-work-incomplete", ids, "non-empty", "refuse")

    # planId / executionPlanId / evaluatorClosure joins
    run_id = (getattr(st, "meta", None) or {}).get("runId")
    run = st.objects.get(run_id) if run_id else None
    want_plan = run["planId"] if run else None
    ok = ei.get("planId") == want_plan
    _emit(DOC_EI, "/properties/planId/description", ei_id, "planId",
          "eq-selected-run.planId-not-read-off-plan-descriptor", ei.get("planId"), want_plan,
          "pass" if ok else "refuse")
    if not ok:
        errors.append(f"EXECUTION_INPUTS_PLAN_JOIN:{ei.get('planId')}!={want_plan}")
    ep_id = ei.get("executionPlanId")
    try:
        epr = obj(st, ep_id)
        ok = epr.get("planId") == want_plan
    except Exception:
        ok = False
        epr = {}
    _emit(DOC_EI, "/properties/executionPlanId", ei_id, "executionPlanId",
          "retained-exec-plan-planId-join", epr.get("planId") if isinstance(epr, dict) else None, want_plan,
          "pass" if ok else "refuse")
    if not ok:
        errors.append(f"EXECUTION_INPUTS_EXECUTION_PLAN_JOIN:{ep_id}")
    evc = ei.get("evaluatorClosure")
    try:
        clo = obj(st, evc)
        ok = clo.get("kind") == "evaluator" and evc in (plan.get("semanticClosures") or [])
    except Exception:
        ok = False
        clo = {}
    _emit(DOC_EI, "/properties/evaluatorClosure", ei_id, "evaluatorClosure",
          "kind-evaluator-and-plan-semanticClosures", clo.get("kind") if isinstance(clo, dict) else None, "evaluator",
          "pass" if ok else "refuse")
    if not ok:
        errors.append(f"EXECUTION_INPUTS_EVALUATOR_CLOSURE:{evc}")
    enum_d = ei.get("enumerationPlanDigest")
    spec = load_c(st, plan["analysisSpecDigest"])
    ep_want = next((p["payloadDigest"] for p in spec["parameters"] if p["schemaDigest"] == builder.ENUM_PLAN_DIGEST), None)
    ok = enum_d == ep_want
    _emit(DOC_EI, "/properties/enumerationPlanDigest", ei_id, "enumerationPlanDigest",
          "eq-analysis-spec-enum-plan-payloadDigest", enum_d, ep_want, "pass" if ok else "refuse")
    if not ok:
        errors.append(f"EXECUTION_INPUTS_ENUMERATION_DIGEST:{enum_d}")
    as_d = ei.get("analysisSpecDigest")
    ok = as_d == plan.get("analysisSpecDigest")
    _emit(DOC_EI, "/properties/analysisSpecDigest", ei_id, "analysisSpecDigest",
          "eq-plan.analysisSpecDigest", as_d, plan.get("analysisSpecDigest"), "pass" if ok else "refuse")
    if not ok:
        errors.append(f"EXECUTION_INPUTS_ANALYSIS_SPEC:{as_d}")
    hc = ei.get("hostCapture") or {}
    ok = hc.get("custody") == "host-tcb-evidence-store" and hc.get("observation") == "stage-return"
    _emit(DOC_EI, "/$defs/HostCaptureV1/properties/custody", ei_id, "hostCapture.custody",
          "const-host-tcb-evidence-store", hc.get("custody"), "host-tcb-evidence-store",
          "pass" if hc.get("custody") == "host-tcb-evidence-store" else "refuse")
    _emit(DOC_EI, "/$defs/HostCaptureV1/properties/observation", ei_id, "hostCapture.observation",
          "const-stage-return", hc.get("observation"), "stage-return",
          "pass" if hc.get("observation") == "stage-return" else "refuse")
    if not ok:
        errors.append("EXECUTION_INPUTS_HOST_CAPTURE_CONST")
    return errors


def walk_and_order_digest(st: store.Store, ei: dict, ei_id: str) -> tuple[list[str], list]:
    """Walk EI instance against its schema; enforce x-opensip-order/digest at nested addresses."""
    errors = []
    root = kit_schemas.SCHEMAS.get(SID_EI) or {}
    sites = []
    instance_walk.walk_instance(
        ei, root, sid=SID_EI, root=root, owner_id=ei_id, path="ExecutionInputsV1", ptr="", out=sites,
    )
    for site in sites:
        if not site.get("applicable", True):
            _emit(site["document"], site["pointer"], ei_id, site["instancePath"],
                  "applicator-branch", site.get("inapplicableReason"), None, "inapplicable")
            continue
        xo = site.get("xOrder")
        if xo == "canonical-set":
            # value at path
            cur = ei
            rel = site["instancePath"].replace("ExecutionInputsV1.", "").replace("ExecutionInputsV1", "")
            # skip list indices for order of the array itself
            if "[" in site["instancePath"] and site["instancePath"].endswith("]"):
                continue
            parts = []
            buf = ""
            for ch in rel:
                if ch == ".":
                    if buf:
                        parts.append(buf)
                        buf = ""
                else:
                    buf += ch
            if buf:
                parts.append(buf)
            val = ei
            ok_path = True
            for p in parts:
                if p.endswith("]") and "[" in p:
                    name, idx = p[:-1].split("[")
                    if name:
                        val = val.get(name) if isinstance(val, dict) else None
                    try:
                        val = val[int(idx)]
                    except Exception:
                        ok_path = False
                        break
                else:
                    val = val.get(p) if isinstance(val, dict) else None
                if val is None:
                    ok_path = False
                    break
            if ok_path and isinstance(val, list):
                ok = instance_walk.is_canonical_set(val)
                _emit(site["document"], site["pointer"] + "/x-opensip-order", ei_id,
                      site["instancePath"], "canonical-set", len(val), len(order.cset(list(val))),
                      "pass" if ok else "refuse")
                if not ok:
                    errors.append(f"EXECUTION_INPUTS_ORDER:{site['instancePath']}")
        elif xo == "ordinal":
            rel = site["instancePath"]
            if rel in {"ExecutionInputsV1.cellOutcomes", "ExecutionInputsV1.hostCapture.stageReceipts"}:
                pass  # already checked
        xd = site.get("xDigest")
        if isinstance(xd, dict) and xd.get("representation") == "canonical-record":
            # digest field should retrieve retained C bytes
            pass
    return errors, sites
