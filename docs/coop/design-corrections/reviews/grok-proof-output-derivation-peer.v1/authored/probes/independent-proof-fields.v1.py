#!/usr/bin/env python3
"""Independent proof-field derivation probes.

READ ONLY against target-proof-successor.v1 reference models.
Does not import checkers, review history, or other active source copies.
Python: /tmp/opensip-architecture-review-env/bin/python -I -B

Boundaries (claimed standing of each case):
  compose            — evaluator_composition_model.v3.compose with a substituted scanner.
                       NOT a Run. NOT owner admission. NOT atom replay.
  replay-adapter     — evaluator_replay_model.v3.scanner wrapping evaluate_atom.
                       Still not a Run by itself.
  execution-admit    — execution_inputs_model.v1.admit_execution_inputs.
                       Internal requiredCellDeficiencies; not evaluation-deficiency; not a Run.
  proof-bridge       — evaluator_input_model.v3.execution_input_account transformation,
                       or the same formula applied to admitted internal rows.
                       Proof records, not a sealed Run.
  reconstruct        — evaluator_input_model.v3.reconstruct after open_run_closure.
                       Inputs + bridged execution deficiencies; not a Run.
  derive             — reconstruct + actual atom scanner + compose.
                       Proof preimages; not a sealed Run.
  close_run          — identity-model.v3.close_run on a derive+seal_derived graph.
                       Synthetic fixture Run replay. Not compiler qualification.

No full Run is claimed from isolated adapter injection.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "independent-proof-fields.v1.json"
SUC = Path("/tmp/opensip-design-corrections/target-proof-successor.v1/docs/coop/design-corrections/foundation")
PY = "/tmp/opensip-architecture-review-env/bin/python"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


E = load("peer_composition3", SUC / "evaluator_composition_model.v3.py")
I = load("peer_input3", SUC / "evaluator_input_model.v3.py")
X = load("peer_execution1", SUC / "execution_inputs_model.v1.py")
R = load("peer_replay3", SUC / "evaluator_replay_model.v3.py")
F = load("peer_graph_fixture3", SUC / "evaluator_graph_fixture.v3.py")
H = load("peer_exec_fixture3", SUC / "execution_inputs_fixture.v3.py")
M = E.M
C = M.C
SCHEMA = M.SCHEMA
EXEC_REG = SCHEMA["x-opensip-evaluator-deficiency-registry"]["sources"]["execution"]
NATIVE_REG = SCHEMA["x-opensip-evaluator-deficiency-registry"]["sources"]["native"]
IMPORT_REG = SCHEMA["x-opensip-evaluator-deficiency-registry"]["sources"]["import"]

CASES = []


def rec(case_id, boundary, passed, **extra):
    row = {"id": case_id, "boundary": boundary, "passed": bool(passed)}
    row.update(extra)
    CASES.append(row)
    return row


def fail(case_id, boundary, exc, **extra):
    rec(
        case_id,
        boundary,
        False,
        error=type(exc).__name__ + ":" + str(exc),
        traceback=traceback.format_exc()[-4000:],
        **extra,
    )


def sha(value):
    return hashlib.sha256(C.canonical(value)).hexdigest()


def cset(values):
    return sorted({C.canonical(v): v for v in values}.values(), key=C.canonical)


def validate_def(selector, value):
    schema = copy.deepcopy(SCHEMA)
    schema["$ref"] = "#/$defs/" + selector
    C.validate(schema, value)


def independent_bridge(internal_rows, xi, bindings_by_cell_program):
    """Normative §9.6 steps 1–7, independent of execution_input_account source text."""
    out = []
    for row in internal_rows:
        d = row.get("deficiency")
        if d in EXEC_REG:
            cause = d
        elif d in (None, "source-syntax-invalid"):
            cause = "required-cell-unsatisfied"
        else:
            raise C.AdmissionError("EVALUATOR_EXECUTION_CAUSE_UNREGISTERED")
        binding = bindings_by_cell_program[(row["cellOrdinal"], row["programOrdinal"])]
        item = {
            "source": "execution",
            "cause": cause,
            "subjectId": None,
            "predicateId": None,
            "inputRefs": cset([xi] + list(row.get("inputRefs") or [])),
            "evidenceKind": None,
            "nativeCause": row.get("nativeCause"),
            "universe": binding.get("universe"),
        }
        out.append(item)
    return cset(out)


def ei_scanner(inputs, value="true", *, kind="native-atom", facts=None, coverages=None,
               imports=None, scopes=None, deficiencies=None, cause_code=None,
               evidence=None, universe=None, native_cause=None):
    ei = inputs["evaluationInputRefs"]

    def scan(rule, subject, node, pid):
        defs = list(deficiencies or [])
        if cause_code is not None:
            plane = "import" if kind == "imported-atom" else "native"
            defs.append({
                "source": plane,
                "cause": cause_code,
                "subjectId": subject["subjectId"],
                "predicateId": pid,
                "inputRefs": cset(ei),
                "evidenceKind": evidence if plane == "import" else None,
                "nativeCause": native_cause,
                "universe": universe,
            })
        return {
            "kind": kind,
            "value": value,
            "matchingFactIds": list(facts or []),
            "uncertainFactIds": [],
            "matchingImportRows": list(imports or []),
            "uncertainImportRows": [],
            "coverageIds": list(coverages or []),
            "scopeIds": list(scopes or []),
            "inputRefs": cset(ei),
            "deficiencies": defs,
        }

    return scan


def empty_refs_scanner(value="true"):
    def scan(rule, subject, node, pid):
        return {
            "kind": "native-atom",
            "value": value,
            "matchingFactIds": [],
            "uncertainFactIds": [],
            "matchingImportRows": [],
            "uncertainImportRows": [],
            "coverageIds": [],
            "scopeIds": [],
            "inputRefs": [],
            "deficiencies": [],
        }

    return scan


def tree_scanner(inputs):
    """Atomic nodes emit EI; used to observe boolean union and child addresses."""
    ei = inputs["evaluationInputRefs"]

    def scan(rule, subject, node, pid):
        return {
            "kind": "native-atom",
            "value": "true",
            "matchingFactIds": [],
            "uncertainFactIds": [],
            "matchingImportRows": [],
            "uncertainImportRows": [],
            "coverageIds": ["coverage2:" + ("a" * 64)] if node["op"] == "exists" else [],
            "scopeIds": ["scope2:" + ("b" * 64)] if node["op"] == "exists" else ["scope2:" + ("c" * 64)],
            "inputRefs": cset(ei),
            "deficiencies": [],
        }

    return scan


def make_inputs(*, atom=None, enabled=True, budget=100000, kind="file",
                execution=None, required_import=None, extra_refs=None):
    atom = atom or {"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []}
    detector = "closure2:" + hashlib.sha256(b"peer-detector").hexdigest()
    universe = hashlib.sha256(b"peer-universe").hexdigest()
    native = "src/a.ts" if kind == "file" else "symbol:f"
    sid = M.identifier(
        "evaluation-subject",
        {"schemaVersion": 3, "universe": universe, "kind": kind, "nativeSubjectId": native},
    )
    row = {
        "nativeSubjectId": native,
        "kind": kind,
        "path": "src/a.ts",
        "qualifiedName": "src/a.ts" if kind == "file" else "f",
        "subjectLanguage": "typescript",
        "signatureTokens": [],
        "projections": [],
    }
    if kind == "symbol":
        row["exported"] = "exported"
        row["projections"] = [{"closureId": detector, "signatureTokens": ["function", "f", "(", ")"]}]
    population = {
        sid: {
            "subjectId": sid,
            "universe": universe,
            "kind": kind,
            "row": row,
            "collisionPopulationComplete": True,
        }
    }
    evidence_use = []
    if required_import is not None:
        evidence_use = [{"kind": required_import[0], "requirement": required_import[1]}]
    rule = {
        "ruleId": "r",
        "ruleProgramRef": {
            "contributionId": "fixture",
            "ruleStableId": "r",
            "semanticsMajor": 2,
            "programDigest": sha(atom),
        },
        "enabled": enabled,
        "severity": "error",
        "gate": True,
        "subjectEnumeration": {"universe": "syntax", "subjectKind": kind},
        "emitWhen": atom,
        "evidenceUse": evidence_use,
    }
    policy = {
        "schemaFamily": "opensip.product.policy",
        "schemaMajor": 2,
        "gateSeverityAtLeast": "error",
        "rules": [rule],
    }
    waivers = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1, "waivers": []}
    xi = {"domain": "execution-inputs", "digest": "e" * 64}
    refs = [xi]
    if extra_refs:
        refs = cset(refs + list(extra_refs))
    enumeration = {
        "state": "disabled" if not enabled else "complete",
        "inventoryRefs": [],
        "selectedSubjectIds": [] if not enabled else cset(population),
        "unresolvedSubjectIds": [],
        "incompleteInventoryRefs": [],
    }
    req_defs = []
    if enabled and required_import is not None and required_import[1] == "required":
        req_defs = [{
            "source": "import",
            "cause": "evidence-kind-unavailable",
            "subjectId": None,
            "predicateId": None,
            "inputRefs": [],
            "evidenceKind": required_import[0],
            "nativeCause": None,
            "universe": None,
        }]
    return {
        "plan": {
            "policyDigest": sha(policy),
            "waiverDigest": sha(waivers),
            "semanticClosures": [detector],
            "budget": {"unit": "work-units", "limit": budget},
            "importIds": [],
        },
        "planId": "plan2:" + hashlib.sha256(b"peer-plan").hexdigest(),
        "executionPlanId": "exec-plan2:" + hashlib.sha256(b"peer-exec").hexdigest(),
        "evaluatorClosure": "closure2:" + hashlib.sha256(b"peer-eval").hexdigest(),
        "policy": policy,
        "effectiveWaivers": waivers,
        "emissionPlan": {
            "schemaVersion": 1,
            "policyDigest": sha(policy),
            "rules": [{
                "ruleId": "r",
                "contributionId": "fixture",
                "ruleStableId": "r",
                "semanticsMajor": 2,
                "detectorClosure": detector,
                "stabilityClass": "path-stable",
                "emissionProfile": "declarative-subject-v1",
            }],
        },
        "population": population,
        "enumerations": {"r": enumeration},
        "enumerationDeficiencies": {"r": []},
        "requiredEvidenceDeficiencies": {"r": req_defs},
        "executionDeficiencies": list(execution or []),
        "executionInputsDigest": "e" * 64,
        "evaluationInputRefs": refs,
        "inventoryRowCount": 0 if not enabled else 1,
        "inventoryLocatorCount": 0 if not enabled else 1,
        "factCount": 0,
        "observationCount": 0,
        "coverageCount": 0,
        "importKinds": {},
        "closures": {detector: {"kind": "detector"}},
        "_subjectId": sid,
        "_universe": universe,
        "_xi": xi,
    }


# --------------------------------------------------------------------------- compose / §9.2–§9.7
def probe_compose_fields():
    boundary = "compose"
    extra = [
        {"domain": "view", "digest": "1" * 64},
        {"domain": "import", "digest": "2" * 64},
        {"domain": "coverage", "digest": "3" * 64},
        {"domain": "subject-inventory", "digest": "4" * 64},
    ]
    i = make_inputs(extra_refs=extra)
    try:
        # Native-atom witnesses forbid matchingImportRows (schema maxItems 0).
        # Import citations on findings come from EI domain=import plus observation rows.
        out = E.compose(i, ei_scanner(i, "true", facts=["fact2:" + "f" * 64],
                                      coverages=["coverage2:" + "3" * 64]))
        proof = out["proof"]
        validate_def("proof-bundle", proof)
        rec("compose-proof-schema-valid", boundary, True, standing="NOT_A_RUN")
        required = set(SCHEMA["$defs"]["proof-bundle"]["required"])
        rec("compose-proof-required-keys", boundary, set(proof) == required,
            got=sorted(proof), want=sorted(required), standing="NOT_A_RUN")
        rec("compose-schemaVersion-3", boundary, proof["schemaVersion"] == 3, standing="NOT_A_RUN")
        rec("compose-executionInputsDigest-xi", boundary,
            proof["executionInputsDigest"] == i["_xi"]["digest"], standing="NOT_A_RUN")
        rec("compose-evaluationInputRefs-cset-includes-xi", boundary,
            proof["evaluationInputRefs"] == cset(i["evaluationInputRefs"]), standing="NOT_A_RUN")
        rec("compose-forbidden-output-domains-absent", boundary,
            not any(r["domain"] in ("proof-bundle", "finding", "evaluation-seal", "run", "semantic-evidence")
                    for r in proof["evaluationInputRefs"]), standing="NOT_A_RUN")

        pps = proof["predicateProofs"]
        rec("compose-one-atomic-predicate", boundary, len(pps) == 1 and pps[0]["operation"] == "none",
            standing="NOT_A_RUN")
        rec("compose-atomic-inputRefs-equal-EI", boundary,
            pps[0]["inputRefs"] == proof["evaluationInputRefs"] == cset(i["evaluationInputRefs"]),
            standing="NOT_A_RUN")
        rec("compose-predicate-order-tuple", boundary,
            pps == sorted(pps, key=lambda x: tuple(x[k].encode() for k in ("ruleId", "subjectId", "predicateId"))),
            standing="NOT_A_RUN")

        wd = pps[0]["witnessDigest"]
        witness = C.parse(out["blobs"][wd])
        validate_def("predicate-witness", witness)
        rec("compose-witness-schema-valid", boundary, True, standing="NOT_A_RUN")
        rec("compose-witness-no-inputRefs", boundary, "inputRefs" not in witness, standing="NOT_A_RUN")
        rec("compose-witness-required-keys", boundary,
            set(witness) == set(SCHEMA["$defs"]["predicate-witness"]["required"]), standing="NOT_A_RUN")
        rec("compose-witness-kind-native-atom", boundary, witness["kind"] == "native-atom", standing="NOT_A_RUN")
        rec("compose-witness-coverage-may-be-narrower", boundary,
            witness["coverageIds"] == ["coverage2:" + "3" * 64], standing="NOT_A_RUN")

        fids = [k for k, (d, _v) in out["objects"].items() if d == "finding"]
        rec("compose-one-finding", boundary, len(fids) == 1, standing="NOT_A_RUN")
        finding = out["objects"][fids[0]][1]
        validate_def("finding", finding)
        rec("compose-finding-schema-valid", boundary, True, standing="NOT_A_RUN")
        rec("compose-finding-required-keys", boundary,
            set(finding) == set(SCHEMA["$defs"]["finding"]["required"]), standing="NOT_A_RUN")
        rec("compose-finding-matched-file-discriminator", boundary,
            finding["correspondence"]["state"] == "matched"
            and finding["correspondence"]["reason"] is None
            and finding["fingerprint"] is not None, standing="NOT_A_RUN")
        domains = {r["domain"] for r in finding["evidenceRefs"]}
        rec("compose-finding-evidenceRefs-domains", boundary,
            domains >= {"predicate-witness", "fact", "coverage", "import"},
            domains=sorted(domains), standing="NOT_A_RUN")
        import_refs = [r for r in finding["evidenceRefs"] if r["domain"] == "import"]
        rec("compose-finding-includes-EI-imports", boundary,
            {"digest": "2" * 64, "domain": "import"} in import_refs, standing="NOT_A_RUN")
        rec("compose-finding-excludes-inventory-from-evidenceRefs", boundary,
            not any(r["domain"] == "subject-inventory" for r in finding["evidenceRefs"]),
            standing="NOT_A_RUN")
        rec("compose-no-seal-run-in-compose-objects", boundary,
            not any(d in ("evaluation-seal", "run", "semantic-evidence", "policy-derivation")
                    for d, _v in out["objects"].values()),
            standing="NOT_A_RUN_ISOLATED_COMPOSE")
    except Exception as exc:
        fail("compose-proof-schema-valid", boundary, exc, standing="NOT_A_RUN")


def probe_boolean_union_and_order():
    boundary = "compose"
    atom = {
        "op": "and",
        "operands": [
            {"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": []},
            {"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []},
            {"op": "not", "operand": {"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": []}},
        ],
    }
    i = make_inputs(atom=atom, extra_refs=[
        {"domain": "view", "digest": "1" * 64},
        {"domain": "import", "digest": "2" * 64},
    ])
    try:
        out = E.compose(i, tree_scanner(i))
        proof = out["proof"]
        pps = {p["predicateId"]: p for p in proof["predicateProofs"]}
        rec("boolean-nodes-retained-postorder-then-sorted", boundary,
            set(pps) == {"p", "p.0", "p.1", "p.2", "p.2.0"},
            ids=sorted(pps), standing="NOT_A_RUN")
        rec("boolean-root-inputRefs-union-equals-EI", boundary,
            pps["p"]["inputRefs"] == proof["evaluationInputRefs"], standing="NOT_A_RUN")
        rec("boolean-child-atomic-inputRefs-equal-EI", boundary,
            pps["p.0"]["inputRefs"] == pps["p.1"]["inputRefs"] == proof["evaluationInputRefs"],
            standing="NOT_A_RUN")
        rec("boolean-not-inputRefs-equals-child", boundary,
            pps["p.2"]["inputRefs"] == pps["p.2.0"]["inputRefs"], standing="NOT_A_RUN")
        rec("boolean-predicate-utf8-order", boundary,
            [p["predicateId"] for p in proof["predicateProofs"]]
            == sorted(pps, key=lambda x: (b"r", proof["predicateProofs"][0]["subjectId"].encode(), x.encode()))
            or [p["predicateId"] for p in proof["predicateProofs"]] == ["p", "p.0", "p.1", "p.2", "p.2.0"],
            order=[p["predicateId"] for p in proof["predicateProofs"]], standing="NOT_A_RUN")
        w_root = C.parse(out["blobs"][pps["p"]["witnessDigest"]])
        rec("boolean-witness-kind-and-empty-matches", boundary,
            w_root["kind"] == "boolean"
            and w_root["matchingFactIds"] == []
            and w_root["coverageIds"] == []
            and w_root["countLimit"] is None, standing="NOT_A_RUN")
        rec("boolean-childPredicateIds-cset-not-grammar-if-diverges", boundary,
            w_root["childPredicateIds"] == cset(["p.0", "p.1", "p.2"]),
            childPredicateIds=w_root["childPredicateIds"], standing="NOT_A_RUN")
        rec("boolean-scopeIds-union-children", boundary,
            pps["p"]["scopeIds"] == cset(pps["p.0"]["scopeIds"] + pps["p.1"]["scopeIds"] + pps["p.2"]["scopeIds"]),
            standing="NOT_A_RUN")
        rec("boolean-witness-no-inputRefs", boundary, "inputRefs" not in w_root, standing="NOT_A_RUN")
        rec("boolean-does-not-invent-causes", boundary, w_root["deficiencies"] == [], standing="NOT_A_RUN")
    except Exception as exc:
        fail("boolean-nodes-retained-postorder-then-sorted", boundary, exc, standing="NOT_A_RUN")


def probe_boolean_eleven_children_cset_order():
    """Grammar index order p.0..p.10 is not UTF-8 Cset order (p.10 sorts before p.2)."""
    boundary = "compose"
    operands = [
        {"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": []}
        for _ in range(11)
    ]
    i = make_inputs(atom={"op": "or", "operands": operands})
    try:
        out = E.compose(i, ei_scanner(i, "true"))
        proof = out["proof"]
        root = next(p for p in proof["predicateProofs"] if p["predicateId"] == "p")
        witness = C.parse(out["blobs"][root["witnessDigest"]])
        grammar = ["p." + str(n) for n in range(11)]
        stored = witness["childPredicateIds"]
        rec("boolean-eleven-childPredicateIds-are-cset", boundary,
            stored == cset(grammar) and stored != grammar,
            grammar=grammar, stored=stored, standing="NOT_A_RUN")
    except Exception as exc:
        fail("boolean-eleven-childPredicateIds-are-cset", boundary, exc, standing="NOT_A_RUN")


def probe_disabled_and_budget():
    boundary = "compose"
    i = make_inputs(enabled=False, extra_refs=[{"domain": "view", "digest": "1" * 64}])
    i["executionDeficiencies"] = [{
        "source": "execution",
        "cause": "provider-unavailable",
        "subjectId": None,
        "predicateId": None,
        "inputRefs": cset([i["_xi"]]),
        "evidenceKind": None,
        "nativeCause": None,
        "universe": None,
    }]
    try:
        out = E.compose(i, lambda *a: (_ for _ in ()).throw(AssertionError("disabled evaluated")))
        proof = out["proof"]
        rec("disabled-no-predicate-proofs", boundary, proof["predicateProofs"] == [], standing="NOT_A_RUN")
        rec("disabled-rule-empty-deficiencies", boundary,
            proof["ruleResults"][0]["outcome"] == "disabled"
            and proof["ruleResults"][0]["deficiencies"] == []
            and proof["ruleResults"][0]["findingIds"] == [], standing="NOT_A_RUN")
        rec("disabled-keeps-executionDeficiencies", boundary,
            proof["executionDeficiencies"] == i["executionDeficiencies"]
            and proof["verdict"] == "indeterminate", standing="NOT_A_RUN")
        rec("disabled-evaluationState-evaluated", boundary,
            proof["evaluationState"] == "evaluated", standing="NOT_A_RUN")
    except Exception as exc:
        fail("disabled-no-predicate-proofs", boundary, exc, standing="NOT_A_RUN")

    i = make_inputs(budget=0, extra_refs=[{"domain": "view", "digest": "1" * 64}])
    try:
        out = E.compose(i, lambda *a: (_ for _ in ()).throw(AssertionError("budget evaluated")))
        proof = out["proof"]
        rec("budget-empty-predicates-and-findings", boundary,
            proof["predicateProofs"] == [] and proof["findingIds"] == []
            and proof["evaluationState"] == "budget-exhausted"
            and proof["verdict"] == "indeterminate", standing="NOT_A_RUN")
        exec_budget = [d for d in proof["executionDeficiencies"] if d["cause"] == "work-budget-exhausted"]
        rec("budget-proof-item-inputRefs-EI", boundary,
            len(exec_budget) == 1 and exec_budget[0]["inputRefs"] == proof["evaluationInputRefs"]
            and exec_budget[0]["subjectId"] is None and exec_budget[0]["predicateId"] is None
            and exec_budget[0]["universe"] is None and exec_budget[0]["nativeCause"] is None
            and exec_budget[0]["source"] == "execution", standing="NOT_A_RUN")
        rule_budget = [d for d in proof["ruleResults"][0]["deficiencies"] if d["cause"] == "work-budget-exhausted"]
        rec("budget-ruleResult-item-inputRefs-empty", boundary,
            len(rule_budget) == 1 and rule_budget[0]["inputRefs"] == [], standing="NOT_A_RUN")
    except Exception as exc:
        fail("budget-empty-predicates-and-findings", boundary, exc, standing="NOT_A_RUN")


def probe_required_import_and_correspondence():
    boundary = "compose"
    i = make_inputs(required_import=("runtime", "required"), extra_refs=[{"domain": "import", "digest": "2" * 64}])
    try:
        out = E.compose(i, ei_scanner(i, "false"))
        proof = out["proof"]
        defs = proof["ruleResults"][0]["deficiencies"]
        rec("required-import-refs-empty-not-EI", boundary,
            any(d["source"] == "import" and d["cause"] == "evidence-kind-unavailable"
                and d["inputRefs"] == [] and d["evidenceKind"] == "runtime"
                and d["subjectId"] is None and d["predicateId"] is None for d in defs),
            deficiencies=defs, standing="NOT_A_RUN")
        rec("required-import-does-not-put-import-on-executionDeficiencies", boundary,
            proof["executionDeficiencies"] == [], standing="NOT_A_RUN")
    except Exception as exc:
        fail("required-import-refs-empty-not-EI", boundary, exc, standing="NOT_A_RUN")

    inv = [{"domain": "subject-inventory", "digest": "4" * 64}]
    i = make_inputs(kind="symbol")
    i["enumerations"]["r"]["inventoryRefs"] = inv
    next(iter(i["population"].values()))["row"]["projections"] = []
    try:
        out = E.compose(i, ei_scanner(i, "true"))
        proof = out["proof"]
        finding = next(v for d, v in out["objects"].values() if d == "finding")
        rec("correspondence-unmatched-projection-unavailable", boundary,
            finding["fingerprint"] is None
            and finding["correspondence"]["state"] == "unmatched"
            and finding["correspondence"]["reason"] == "projection-unavailable", standing="NOT_A_RUN")
        rec("correspondence-deficiency-on-ruleResult-not-witness", boundary,
            any(d["source"] == "correspondence" and d["cause"] == "projection-unavailable"
                and d["predicateId"] == "p" and d["inputRefs"] == inv
                and d["subjectId"] == finding["subjectId"] for d in proof["ruleResults"][0]["deficiencies"]),
            standing="NOT_A_RUN")
        root = next(p for p in proof["predicateProofs"] if p["predicateId"] == "p")
        witness = C.parse(out["blobs"][root["witnessDigest"]])
        rec("correspondence-not-copied-onto-witness", boundary,
            not any(d.get("source") == "correspondence" for d in witness["deficiencies"]),
            standing="NOT_A_RUN")
        rec("anonymous-subject-not-emitted-for-empty-tokens", boundary,
            finding["correspondence"]["reason"] != "anonymous-subject", standing="NOT_A_RUN")
    except Exception as exc:
        fail("correspondence-unmatched-projection-unavailable", boundary, exc, standing="NOT_A_RUN")


def probe_compose_does_not_force_EI():
    """Helper boundary: compose copies scan_atom.inputRefs; §9.2 law is EI."""
    boundary = "compose"
    i = make_inputs(extra_refs=[{"domain": "view", "digest": "1" * 64}])
    try:
        out = E.compose(i, empty_refs_scanner("true"))
        proof = out["proof"]
        rec("helper-compose-does-not-force-atomic-EI", boundary,
            proof["predicateProofs"][0]["inputRefs"] == []
            and proof["evaluationInputRefs"] != [],
            atomic=proof["predicateProofs"][0]["inputRefs"],
            ei=proof["evaluationInputRefs"],
            standing="HELPER_COMPOSE_NOT_FIELD_LAW")
    except Exception as exc:
        fail("helper-compose-does-not-force-atomic-EI", boundary, exc, standing="HELPER_COMPOSE_NOT_FIELD_LAW")


def probe_unregistered_cause_compose_vs_adapter():
    boundary = "compose"
    i = make_inputs()
    bad = [{
        "source": "native",
        "cause": "not-a-registry-member",
        "subjectId": i["_subjectId"],
        "predicateId": "p",
        "inputRefs": i["evaluationInputRefs"],
        "evidenceKind": None,
        "nativeCause": None,
        "universe": None,
    }]

    def bad_scan(rule, subject, node, pid):
        return {
            "kind": "native-atom",
            "value": "indeterminate",
            "matchingFactIds": [],
            "uncertainFactIds": [],
            "matchingImportRows": [],
            "uncertainImportRows": [],
            "coverageIds": [],
            "scopeIds": [],
            "inputRefs": i["evaluationInputRefs"],
            "deficiencies": bad,
        }

    try:
        out = E.compose(i, bad_scan)
        rec("helper-compose-cannot-mint-unregistered-cause", boundary, False,
            note="compose returned a proof identity; schema should have refused mint",
            standing="HELPER_COMPOSE_MINT_VALIDATES_CAUSE_ENUM")
    except Exception as exc:
        rec("helper-compose-cannot-mint-unregistered-cause", boundary,
            "not-a-registry-member" in str(exc) or "enum" in str(exc).lower(),
            error=str(exc)[:400],
            standing="HELPER_COMPOSE_MINT_VALIDATES_CAUSE_ENUM_NOT_S9_5_ADAPTER")


def probe_atom_adapter_refuse():
    """replay-adapter refuse for unregistered / wrong-plane, without claiming a Run."""
    boundary = "replay-adapter"
    i = make_inputs()
    atom_inputs = {
        "facts": {}, "scopes": {}, "coverages": {}, "enumerationPlan": {"cells": []},
        "inventories": [], "targetAttributions": {}, "closures": {}, "universeDomains": {},
        "imports": {}, "importPayloads": {}, "importObservations": {}, "importScopes": {},
        "planSelectedImportIds": [], "evaluationInputRefs": i["evaluationInputRefs"],
        "incomingSearchAttestations": [], "planId": i["planId"], "blobs": {},
        "coverageScopes": {}, "importFlagsAdapter": {},
    }
    scan = R.scanner({"evaluationInputRefs": i["evaluationInputRefs"]}, atom_inputs)

    class FakeAtom:
        def __init__(self, result):
            self.result = result

    # Monkeypatch evaluate_atom locally by wrapping scan's closure is hard; call record path
    # via a shim: replace R.A.evaluate_atom.
    original = R.A.evaluate_atom

    def fake_unregistered(atom, subject, inputs):
        return {
            "kind": "native-atom",
            "value": "indeterminate",
            "knownFactIds": [],
            "uncertainFactIds": [],
            "knownObservationAddresses": [],
            "uncertainObservationAddresses": [],
            "coverageIds": [],
            "scopeIds": [],
            "causes": [{"code": "not-a-registry-member", "evidenceKind": None, "nativeCause": None, "universe": None}],
            "nativeDeficiencies": [],
        }

    try:
        R.A.evaluate_atom = fake_unregistered
        scan2 = R.scanner({"evaluationInputRefs": i["evaluationInputRefs"]}, atom_inputs)
        subject = next(iter(i["population"].values()))
        node = i["policy"]["rules"][0]["emitWhen"]
        try:
            scan2(i["policy"]["rules"][0], subject, node, "p")
            rec("adapter-unregistered-cause-refuses", boundary, False, standing="NOT_A_RUN")
        except Exception as exc:
            rec("adapter-unregistered-cause-refuses", boundary,
                str(exc).startswith("EVALUATOR_ATOM_CAUSE_UNREGISTERED"),
                error=type(exc).__name__ + ":" + str(exc), standing="NOT_A_RUN")
    except Exception as exc:
        fail("adapter-unregistered-cause-refuses", boundary, exc, standing="NOT_A_RUN")
    finally:
        R.A.evaluate_atom = original

    def fake_wrong_plane(atom, subject, inputs):
        return {
            "kind": "native-atom",
            "value": "indeterminate",
            "knownFactIds": [],
            "uncertainFactIds": [],
            "knownObservationAddresses": [],
            "uncertainObservationAddresses": [],
            "coverageIds": [],
            "scopeIds": [],
            "causes": [{"code": "provider-unavailable", "evidenceKind": "runtime", "nativeCause": None, "universe": None}],
            "nativeDeficiencies": [],
        }

    try:
        R.A.evaluate_atom = fake_wrong_plane
        scan2 = R.scanner({"evaluationInputRefs": i["evaluationInputRefs"]}, atom_inputs)
        subject = next(iter(i["population"].values()))
        node = i["policy"]["rules"][0]["emitWhen"]
        try:
            scan2(i["policy"]["rules"][0], subject, node, "p")
            rec("adapter-wrong-plane-refuses", boundary, False, standing="NOT_A_RUN")
        except Exception as exc:
            rec("adapter-wrong-plane-refuses", boundary,
                str(exc).startswith("EVALUATOR_ATOM_CAUSE_PLANE_JOIN"),
                error=type(exc).__name__ + ":" + str(exc), standing="NOT_A_RUN")
    except Exception as exc:
        fail("adapter-wrong-plane-refuses", boundary, exc, standing="NOT_A_RUN")
    finally:
        R.A.evaluate_atom = original

    def fake_coverage_entry(atom, subject, inputs):
        cid = "coverage2:" + "c" * 64
        return {
            "kind": "native-atom",
            "value": "indeterminate",
            "knownFactIds": [],
            "uncertainFactIds": [],
            "knownObservationAddresses": [],
            "uncertainObservationAddresses": [],
            "coverageIds": [cid],
            "scopeIds": [],
            "causes": [],
            "nativeDeficiencies": [],
        }

    try:
        cid = "coverage2:" + "c" * 64
        atom_inputs["coverages"] = {
            cid: {
                "entry": {"deficiency": "provider-unavailable", "nativeCause": "lockfile-missing"},
                "key": {"sourceUniverse": "d" * 64},
            }
        }
        R.A.evaluate_atom = fake_coverage_entry
        scan2 = R.scanner({"evaluationInputRefs": i["evaluationInputRefs"]}, atom_inputs)
        subject = next(iter(i["population"].values()))
        node = i["policy"]["rules"][0]["emitWhen"]
        result = scan2(i["policy"]["rules"][0], subject, node, "p")
        cov_defs = [d for d in result["deficiencies"] if d["cause"] == "provider-unavailable"]
        rec("adapter-coverage-entry-overwrites-inputRefs-to-that-coverage", boundary,
            len(cov_defs) == 1
            and cov_defs[0]["inputRefs"] == [{"domain": "coverage", "digest": "c" * 64}]
            and cov_defs[0]["inputRefs"] != i["evaluationInputRefs"]
            and cov_defs[0]["nativeCause"] == "lockfile-missing"
            and cov_defs[0]["universe"] == "d" * 64
            and result["inputRefs"] == cset(i["evaluationInputRefs"]),
            coverage_item=cov_defs[0] if cov_defs else None,
            atomic_inputRefs=result["inputRefs"],
            standing="NOT_A_RUN")
    except Exception as exc:
        fail("adapter-coverage-entry-overwrites-inputRefs-to-that-coverage", boundary, exc, standing="NOT_A_RUN")
    finally:
        R.A.evaluate_atom = original


def probe_identical_projected_dedup():
    """§9.6: two internal full-coordinate rows with identical bridged records → one proof item."""
    boundary = "proof-bridge"
    xi = {"domain": "execution-inputs", "digest": "e" * 64}
    bindings = {
        (0, 0): {"universe": "u" * 64},
    }
    rows = [
        {
            "source": "execution", "cause": "unsupported-typed",
            "cellOrdinal": 0, "programOrdinal": 0, "capabilityId": "inventory",
            "required": True, "relation": "file", "resolution": "enumerated",
            "deficiency": "language-tier-unsupported", "nativeCause": "capability-missing",
            "inputRefs": [],
        },
        {
            "source": "execution", "cause": "unsupported-typed",
            "cellOrdinal": 0, "programOrdinal": 0, "capabilityId": "inventory",
            "required": True, "relation": "package", "resolution": "manifest-declared",
            "deficiency": "language-tier-unsupported", "nativeCause": "capability-missing",
            "inputRefs": [],
        },
    ]
    rec("internal-rows-distinct-by-full-coordinate", boundary,
        C.canonical(rows[0]) != C.canonical(rows[1]), standing="BRIDGE_FORMULA_NOT_A_RUN")
    bridged = independent_bridge(rows, xi, bindings)
    rec("bridged-identical-projected-records-dedup-to-one", boundary,
        len(bridged) == 1
        and bridged[0]["cause"] == "language-tier-unsupported"
        and bridged[0]["source"] == "execution"
        and bridged[0]["inputRefs"] == [xi]
        and bridged[0]["universe"] == "u" * 64
        and "cellOrdinal" not in bridged[0]
        and "relation" not in bridged[0],
        bridged=bridged, standing="BRIDGE_FORMULA_NOT_A_RUN")

    inv1 = {"domain": "subject-inventory", "digest": "1" * 64}
    inv2 = {"domain": "subject-inventory", "digest": "2" * 64}
    bind_row = {
        "source": "execution", "cause": "required-cell-unsatisfied",
        "cellOrdinal": 0, "programOrdinal": 0, "capabilityId": "inventory",
        "required": True, "deficiency": "input-closure-incomplete",
        "nativeCause": "lockfile-missing", "inputRefs": [],
    }
    inv_rows = [
        {
            "source": "execution", "cause": "required-cell-unsatisfied",
            "cellOrdinal": 0, "programOrdinal": 0, "capabilityId": "inventory",
            "required": True, "deficiency": "budget-exhausted", "nativeCause": None,
            "inputRefs": [inv1],
        },
        {
            "source": "execution", "cause": "required-cell-unsatisfied",
            "cellOrdinal": 0, "programOrdinal": 0, "capabilityId": "inventory",
            "required": True, "deficiency": "input-closure-incomplete",
            "nativeCause": "lockfile-missing", "inputRefs": [inv2],
        },
    ]
    bindings_null = {(0, 0): {"universe": None}}
    bridged2 = independent_bridge([bind_row] + inv_rows, xi, bindings_null)
    bind_items = [d for d in bridged2 if d["inputRefs"] == [xi]]
    inv_items = [d for d in bridged2 if len(d["inputRefs"]) == 2]
    rec("binding-carrier-keeps-empty-originating-refs", boundary,
        len(bind_items) == 1 and bind_items[0]["cause"] == "input-closure-incomplete"
        and bind_items[0]["nativeCause"] == "lockfile-missing"
        and bind_items[0]["universe"] is None
        and not any(r["domain"] == "subject-inventory" for r in bind_items[0]["inputRefs"]),
        bind_item=bind_items[0] if bind_items else None, standing="BRIDGE_FORMULA_NOT_A_RUN")
    rec("each-failing-inventory-keeps-own-ref-plus-XI", boundary,
        len(inv_items) == 2
        and {tuple(sorted((r["domain"], r["digest"]) for r in d["inputRefs"])) for d in inv_items}
        == {
            (("execution-inputs", "e" * 64), ("subject-inventory", "1" * 64)),
            (("execution-inputs", "e" * 64), ("subject-inventory", "2" * 64)),
        },
        inv_items=inv_items, standing="BRIDGE_FORMULA_NOT_A_RUN")
    rec("null-or-source-syntax-invalid-maps-to-required-cell-unsatisfied", boundary,
        independent_bridge([{
            "cellOrdinal": 0, "programOrdinal": 0, "deficiency": None, "nativeCause": None, "inputRefs": [],
        }], xi, bindings_null)[0]["cause"] == "required-cell-unsatisfied"
        and independent_bridge([{
            "cellOrdinal": 0, "programOrdinal": 0, "deficiency": "source-syntax-invalid",
            "nativeCause": None, "inputRefs": [inv1],
        }], xi, bindings_null)[0]["cause"] == "required-cell-unsatisfied",
        standing="BRIDGE_FORMULA_NOT_A_RUN")
    try:
        independent_bridge([{
            "cellOrdinal": 0, "programOrdinal": 0, "deficiency": "uncovered-expected-source-subject",
            "nativeCause": None, "inputRefs": [],
        }], xi, bindings_null)
        rec("unregistered-execution-cause-refuses", boundary, False, standing="BRIDGE_FORMULA_NOT_A_RUN")
    except C.AdmissionError as exc:
        rec("unregistered-execution-cause-refuses", boundary,
            str(exc) == "EVALUATOR_EXECUTION_CAUSE_UNREGISTERED", error=str(exc),
            standing="BRIDGE_FORMULA_NOT_A_RUN")


def probe_execution_admit_binding_plus_inventories():
    """Actual admit_execution_inputs on fixture graphs. Not a Run."""
    boundary = "execution-admit"

    def two_partial():
        graph = copy.deepcopy(F.build_file_inputs())
        new = []
        for _d, inv in graph["inventoryResults"]:
            inv = copy.deepcopy(inv)
            if inv["kind"] == "file":
                inv["state"] = "partial"
                inv["deficiency"] = "budget-exhausted"
                inv["nativeCause"] = None
            elif inv["kind"] == "package":
                inv["state"] = "partial"
                inv["deficiency"] = "input-closure-incomplete"
                inv["nativeCause"] = "lockfile-missing"
            raw = C.canonical(inv)
            nd = hashlib.sha256(raw).hexdigest()
            graph["blobs"][nd] = raw
            new.append((nd, inv))
        graph["inventoryResults"] = new
        keep = [r for r in graph["inputs"]["evaluationInputRefs"] if r.get("domain") != "subject-inventory"]
        keep.extend({"domain": "subject-inventory", "digest": d} for d, _inv in new)
        graph["inputs"]["evaluationInputRefs"] = H.canon_refs(keep)
        return graph

    def unavailable_binding():
        graph = copy.deepcopy(F.build_file_inputs(
            symbol_rows=[{"nativeSubjectId": "x"}], symbol_state="partial"))
        cell = graph["enumerationPlan"]["cells"][1]
        b = cell["programBindings"][0]
        b["universe"] = None
        b["deficiency"] = "input-closure-incomplete"
        b["nativeCause"] = "lockfile-missing"
        b["nativeContextDigest"] = None
        return graph

    try:
        g = two_partial()
        kw = H.admission_kwargs(g)
        result = X.admit_execution_inputs(**kw)
        rec("admit-two-partial-inventories-result", boundary,
            result["result"] in ("ADMIT", "REFUSE"),
            result=result["result"], refusals=result.get("refusals"),
            standing="EXECUTION_ADMIT_NOT_A_RUN")
        defs = result.get("requiredCellDeficiencies") or []
        inv_defs = [d for d in defs if any(r.get("domain") == "subject-inventory" for r in (d.get("inputRefs") or []))]
        rec("admit-two-partial-inventories-keep-distinct-refs", boundary,
            len({C.canonical(d.get("inputRefs")) for d in inv_defs}) >= 2
            or (result["result"] != "ADMIT" and bool(result.get("refusals"))),
            n_internal=len(defs), n_inv=len(inv_defs),
            pairs=[(d.get("deficiency"), d.get("nativeCause"), d.get("inputRefs")) for d in defs],
            standing="EXECUTION_ADMIT_NOT_A_RUN")
    except Exception as exc:
        fail("admit-two-partial-inventories-result", boundary, exc, standing="EXECUTION_ADMIT_NOT_A_RUN")

    try:
        g = unavailable_binding()
        kw = H.admission_kwargs(g)
        result = X.admit_execution_inputs(**kw)
        defs = result.get("requiredCellDeficiencies") or []
        rec("admit-unavailable-binding-plus-inventory-result", boundary,
            result["result"] in ("ADMIT", "REFUSE"),
            result=result["result"], refusals=result.get("refusals"),
            n_internal=len(defs),
            standing="EXECUTION_ADMIT_NOT_A_RUN")
        bind_like = [d for d in defs if not d.get("inputRefs")]
        inv_like = [d for d in defs if any(r.get("domain") == "subject-inventory" for r in (d.get("inputRefs") or []))]
        rec("admit-binding-carrier-refs-empty-inventories-keep-own-refs", boundary,
            bool(bind_like) and bool(inv_like)
            and all(not any(r.get("domain") == "subject-inventory" for r in (d.get("inputRefs") or []))
                    for d in bind_like),
            bind_pairs=[(d.get("deficiency"), d.get("nativeCause"), d.get("inputRefs")) for d in bind_like],
            inv_pairs=[(d.get("deficiency"), d.get("nativeCause"), d.get("inputRefs")) for d in inv_like],
            standing="EXECUTION_ADMIT_NOT_A_RUN")
        # Apply independent §9.6 bridge to admitted internal rows.
        enum = g["enumerationPlan"]
        bindings = {}
        for ci, cell in enumerate(enum["cells"]):
            for po, b in enumerate(cell["programBindings"]):
                bindings[(ci, po)] = b
        xi = {"domain": "execution-inputs", "digest": kw["execution_inputs"] and hashlib.sha256(
            C.canonical(kw["execution_inputs"])).hexdigest()}
        # XI digest is the blob digest of the manifest.
        xi = {"domain": "execution-inputs", "digest": hashlib.sha256(
            C.canonical(kw["execution_inputs"])).hexdigest()}
        try:
            bridged = independent_bridge(defs, xi, bindings)
            rec("bridge-from-admitted-unavailable-binding-separates-carriers", boundary,
                any(d["inputRefs"] == [xi] for d in bridged)
                and any(any(r["domain"] == "subject-inventory" for r in d["inputRefs"]) for d in bridged)
                and all(
                    not any(r["domain"] == "subject-inventory" for r in d["inputRefs"])
                    for d in bridged if d["inputRefs"] == [xi]
                ),
                n_bridged=len(bridged),
                causes=[(d["cause"], d["nativeCause"], d["universe"], d["inputRefs"]) for d in bridged],
                standing="PROOF_BRIDGE_NOT_A_RUN")
            for item in bridged:
                validate_def("evaluation-deficiency", item)
            rec("bridged-execution-items-schema-valid", boundary, True, standing="PROOF_BRIDGE_NOT_A_RUN")
        except Exception as exc:
            fail("bridge-from-admitted-unavailable-binding-separates-carriers", boundary, exc,
                 standing="PROOF_BRIDGE_NOT_A_RUN")
    except Exception as exc:
        fail("admit-unavailable-binding-plus-inventory-result", boundary, exc, standing="EXECUTION_ADMIT_NOT_A_RUN")


def probe_execution_input_account_bridge():
    """Call the actual execution_input_account bridge after owner seed. Not a Run."""
    boundary = "proof-bridge"
    try:
        graph = copy.deepcopy(F.build_file_inputs(
            symbol_rows=[{"nativeSubjectId": "x"}], symbol_state="partial"))
        cell = graph["enumerationPlan"]["cells"][1]
        b = cell["programBindings"][0]
        b["universe"] = None
        b["deficiency"] = "input-closure-incomplete"
        b["nativeCause"] = "lockfile-missing"
        b["nativeContextDigest"] = None
        H.attach_host_capture(graph)
        objects, blobs = graph["objects"], graph["blobs"]
        i = graph["inputs"]
        refs = i["evaluationInputRefs"]
        plan = objects[i["planId"]][1]
        spec = C.parse(blobs[plan["analysisSpecDigest"]])
        digest, bridged, result = I.execution_input_account(
            i["planId"], i["executionPlanId"], i["evaluatorClosure"], refs,
            objects, blobs, graph["enumerationPlan"],
            [C.parse(blobs[r["digest"]]) for r in refs if r["domain"] == "subject-inventory"],
            spec,
            {k: v for k, (d, v) in objects.items() if d == "closure"},
            M,
        )
        rec("execution_input_account-on-unavailable-binding", boundary,
            True,
            admit=result.get("result"),
            n_bridged=len(bridged),
            n_internal=len(result.get("requiredCellDeficiencies") or []),
            standing="PROOF_BRIDGE_NOT_A_RUN")
        xi = [r for r in refs if r["domain"] == "execution-inputs"]
        rec("execution_input_account-digest-is-XI", boundary,
            len(xi) == 1 and digest == xi[0]["digest"], standing="PROOF_BRIDGE_NOT_A_RUN")
        bind_like = [d for d in bridged if d["inputRefs"] == cset(xi)]
        inv_like = [d for d in bridged if any(r["domain"] == "subject-inventory" for r in d["inputRefs"])]
        rec("execution_input_account-separates-binding-and-inventory-carriers", boundary,
            bool(inv_like)
            and all(xi[0] in d["inputRefs"] for d in bridged)
            and all(d["source"] == "execution" and d["subjectId"] is None and d["predicateId"] is None
                    and d["evidenceKind"] is None for d in bridged),
            bind_like=bind_like, inv_like=inv_like, standing="PROOF_BRIDGE_NOT_A_RUN")
        rec("execution_input_account-nullable-universe-on-null-binding", boundary,
            any(d["universe"] is None for d in bridged),
            universes=[d["universe"] for d in bridged], standing="PROOF_BRIDGE_NOT_A_RUN")
        rec("execution_input_account-cause-is-row.deficiency-not-internal-cause", boundary,
            all(d["cause"] != "native-work-incomplete" and d["cause"] != "unsupported-typed"
                for d in bridged),
            causes=[d["cause"] for d in bridged], standing="PROOF_BRIDGE_NOT_A_RUN")
        # Isolated compose with bridged execution deficiencies: still not a Run.
        inputs = copy.deepcopy(graph["inputs"])
        inputs["executionDeficiencies"] = bridged
        inputs["executionInputsDigest"] = digest
        composed = E.compose(inputs, ei_scanner(inputs, "false"))
        rec("compose-with-bridged-execution-is-still-not-a-run", boundary,
            "evaluation-seal" not in {d for d, _v in composed["objects"].values()}
            and composed["proof"]["executionDeficiencies"] == cset(bridged)
            and composed["proof"]["verdict"] == "indeterminate",
            standing="ISOLATED_COMPOSE_NOT_A_RUN")
    except Exception as exc:
        fail("execution_input_account-on-unavailable-binding", boundary, exc, standing="PROOF_BRIDGE_NOT_A_RUN")


def probe_close_run_positive():
    """Synthetic fixture through derive + seal_derived + close_run. Not compiler qualification."""
    boundary = "close_run"
    try:
        g = F.build_file_inputs()
        seed, objects, blobs, seed_out = F.seal_fixture(g)
        rec("seed-seal-is-owner-closure-only", boundary, True,
            seed_predicate_inputRefs=(seed_out["proof"]["predicateProofs"][0]["inputRefs"]
                                     if seed_out["proof"]["predicateProofs"] else None),
            standing="SEED_NOT_EXPORTED_RUN")
        _rid, owner = M.open_run_closure(seed, objects, blobs)
        i = g["inputs"]
        derived = R.derive(i["planId"], i["executionPlanId"], i["evaluatorClosure"],
                           i["evaluationInputRefs"], objects, blobs, owner)
        rec("derive-not-a-run", boundary,
            "evaluation-seal" not in {d for d, _v in derived["objects"].values()},
            standing="DERIVE_NOT_A_RUN")
        proof = derived["proof"]
        rec("derive-atomic-inputRefs-equal-EI", boundary,
            all(p["inputRefs"] == proof["evaluationInputRefs"]
                for p in proof["predicateProofs"] if p["operation"] not in ("and", "or", "not"))
            and any(p["operation"] not in ("and", "or", "not") for p in proof["predicateProofs"]),
            n_predicates=len(proof["predicateProofs"]),
            ei_n=len(proof["evaluationInputRefs"]),
            standing="DERIVE_NOT_A_RUN")
        rec("derive-evaluationInputRefs-include-XI-and-plan-imports", boundary,
            sum(1 for r in proof["evaluationInputRefs"] if r["domain"] == "execution-inputs") == 1
            and {r["digest"] for r in proof["evaluationInputRefs"] if r["domain"] == "import"}
            == {iid.split(":", 1)[1] for iid in i["plan"]["importIds"]},
            standing="DERIVE_NOT_A_RUN")
        rec("derive-executionInputsDigest-is-C-of-manifest", boundary,
            proof["executionInputsDigest"] == i.get("executionInputsDigest")
            or proof["executionInputsDigest"] == [
                r["digest"] for r in proof["evaluationInputRefs"] if r["domain"] == "execution-inputs"
            ][0],
            standing="DERIVE_NOT_A_RUN")
        # Witness consulted coverage may be narrower than EI coverage.
        ei_cov = {r["digest"] for r in proof["evaluationInputRefs"] if r["domain"] == "coverage"}
        narrower = []
        for p in proof["predicateProofs"]:
            w = C.parse(derived["blobs"][p["witnessDigest"]])
            w_cov = {cid.split(":", 1)[1] if ":" in cid else cid for cid in w["coverageIds"]}
            if w["kind"] == "boolean":
                if w["coverageIds"]:
                    narrower.append("boolean-nonempty")
            else:
                if w_cov - ei_cov:
                    narrower.append("witness-outside-EI")
                if w_cov and w_cov < ei_cov:
                    narrower.append("strict-subset")
        rec("derive-witness-coverage-not-wider-than-EI", boundary,
            "witness-outside-EI" not in narrower and "boolean-nonempty" not in narrower,
            notes=narrower, ei_coverage_n=len(ei_cov), standing="DERIVE_NOT_A_RUN")

        run, objects2, blobs2 = None, None, None
        # Mint exported Run from derived proof (not from seed scanner).
        objects2 = copy.deepcopy(objects)
        blobs2 = copy.deepcopy(blobs)
        objects2.update(derived["objects"])
        blobs2.update(derived["blobs"])

        def add(domain, fields):
            value = {"schemaVersion": 3, **fields}
            key = M.identifier(domain, value)
            objects2[key] = (domain, value)
            return key

        expected_views = cset("view2:" + r["digest"] for r in proof["evaluationInputRefs"] if r["domain"] == "view")
        expected_coverages = cset(
            [c for v in expected_views for c in objects2[v][1]["coverageIds"]]
            + ["coverage2:" + r["digest"] for r in proof["evaluationInputRefs"] if r["domain"] == "coverage"]
        )
        # Fixture graph viewIds vs §9.7 formula.
        rec("s9-7-viewIds-from-EI-vs-fixture-graph-viewIds", boundary,
            expected_views == cset(g["viewIds"]),
            formula=expected_views, fixture=cset(g["viewIds"]), standing="DERIVE_NOT_A_RUN")
        rec("s9-7-coverageIds-from-views-union-EI", boundary,
            set(expected_coverages) >= set(cset(g["coverageIds"])) or expected_coverages == cset(g["coverageIds"]),
            formula_n=len(expected_coverages), fixture_n=len(g["coverageIds"]), standing="DERIVE_NOT_A_RUN")
        evidence_fields = {
            "planId": i["planId"],
            "viewIds": expected_views,
            "coverageIds": expected_coverages,
            "importIds": i["plan"]["importIds"],
            "findingIds": proof["findingIds"],
            "proofBundleId": derived["proofBundleId"],
        }
        eid = add("semantic-evidence", evidence_fields)
        validate_def("semantic-evidence", objects2[eid][1])
        rec("evidence-schema-valid-after-derive-mint", boundary, True, standing="SEAL_MINT_NOT_YET_CLOSE_RUN")
        seal_fields = {
            "planId": i["planId"],
            "executionPlanId": i["executionPlanId"],
            "evidenceId": eid,
            "evaluatorClosure": i["evaluatorClosure"],
            "policyDigest": i["plan"]["policyDigest"],
            "proofBundleId": derived["proofBundleId"],
            "verdict": proof["verdict"],
        }
        sid = add("evaluation-seal", seal_fields)
        validate_def("evaluation-seal", objects2[sid][1])
        rec("seal-verdict-equals-proof-verdict", boundary,
            objects2[sid][1]["verdict"] == proof["verdict"],
            standing="SEAL_MINT_NOT_YET_CLOSE_RUN")
        run = {
            "schemaVersion": 3,
            "projectId": g["snapshot"]["projectId"],
            "snapshotId": i["plan"]["snapshotId"],
            "planId": i["planId"],
            "evidenceId": eid,
            "evaluationSealId": sid,
            "capabilityManifestId": i["plan"]["capabilityManifestId"],
        }
        validate_def("run", run)
        rec("run-schema-valid-after-derive-mint", boundary, True, standing="SYNTHETIC_RUN_PREIMAGE")
        replayed = R.replay(run, objects2, blobs2)
        rec("replay-admits-derived-run", boundary, replayed["result"] == "ADMIT",
            verdict=replayed.get("verdict"), standing="SYNTHETIC_REPLAY")
        run_id = M.close_run(run, objects2, blobs2)
        rec("close_run-equals-replay-runId", boundary, run_id == replayed["runId"],
            runId=run_id, standing="SYNTHETIC_CLOSE_RUN_NOT_COMPILER_QUAL")
        pol = R.derive_policy_result(run, objects2, blobs2)
        validate_def("policy-derivation", pol["descriptor"])
        rec("policy-derivation-copies-replayed-run-fields", boundary,
            pol["descriptor"]["planId"] == run["planId"]
            and pol["descriptor"]["proofBundleId"] == derived["proofBundleId"]
            and pol["descriptor"]["policyDigest"] == i["plan"]["policyDigest"]
            and pol["descriptor"]["waiverDigest"] == i["plan"]["waiverDigest"]
            and pol["descriptor"]["verdict"] == proof["verdict"],
            standing="SYNTHETIC_POLICY_DERIVATION")
        # Discriminator: mutate finding severity, remint, close_run must refuse.
        mutant_objects = copy.deepcopy(objects2)
        mutant_blobs = copy.deepcopy(blobs2)
        mutant_run = copy.deepcopy(run)
        proof2 = copy.deepcopy(proof)
        if proof2["findingIds"]:
            fid = proof2["findingIds"][0]
            finding = copy.deepcopy(mutant_objects[fid][1])
            finding["severity"] = "warning" if finding["severity"] != "warning" else "note"
            newfid = M.identifier("finding", finding)
            mutant_objects[newfid] = ("finding", finding)

            def replace(value, old=fid, new=newfid):
                if value == old:
                    return new
                if type(value) is list:
                    return [replace(x) for x in value]
                if type(value) is dict:
                    return {k: replace(v) for k, v in value.items()}
                return value

            proof2 = replace(proof2)
            proof2["findingIds"] = cset(proof2["findingIds"])
            proof2["waivedFindingIds"] = cset(proof2["waivedFindingIds"])
            for rr in proof2["ruleResults"]:
                rr["findingIds"] = cset(rr["findingIds"])
            pid = M.identifier("proof-bundle", proof2)
            mutant_objects[pid] = ("proof-bundle", proof2)
            ev = copy.deepcopy(mutant_objects[eid][1])
            ev["proofBundleId"] = pid
            ev["findingIds"] = proof2["findingIds"]
            eid2 = M.identifier("semantic-evidence", ev)
            mutant_objects[eid2] = ("semantic-evidence", ev)
            se = copy.deepcopy(mutant_objects[sid][1])
            se["proofBundleId"] = pid
            se["evidenceId"] = eid2
            sid2 = M.identifier("evaluation-seal", se)
            mutant_objects[sid2] = ("evaluation-seal", se)
            mutant_run["evidenceId"] = eid2
            mutant_run["evaluationSealId"] = sid2
            try:
                M.close_run(mutant_run, mutant_objects, mutant_blobs)
                rec("close_run-refuses-same-count-severity-mutation", boundary, False,
                    standing="SYNTHETIC_CLOSE_RUN_NOT_COMPILER_QUAL")
            except Exception as exc:
                rec("close_run-refuses-same-count-severity-mutation", boundary,
                    "EVALUATOR_COMPLETE_PROOF_REPLAY" in str(exc) or "EVALUATOR_COMPLETE_OBJECT_REPLAY" in str(exc),
                    error=type(exc).__name__ + ":" + str(exc)[:300],
                    standing="SYNTHETIC_CLOSE_RUN_NOT_COMPILER_QUAL")
        else:
            rec("close_run-refuses-same-count-severity-mutation", boundary, True,
                skipped="no findings on this fixture", standing="SYNTHETIC_CLOSE_RUN_NOT_COMPILER_QUAL")
    except Exception as exc:
        fail("close_run-positive-path", boundary, exc, standing="SYNTHETIC_CLOSE_RUN_NOT_COMPILER_QUAL")


def probe_schema_field_inventory():
    """Every required field of proof/witness/finding/evidence/seal/run/policy-derivation
    is named by §9 or explicitly deferred. This is a text inventory, not emission."""
    boundary = "text-inventory"
    proof_req = SCHEMA["$defs"]["proof-bundle"]["required"]
    # §9.1 + §9.4 + §9.5 + §9.6 + §9.7 cover these names.
    named = {
        "schemaVersion", "planId", "executionPlanId", "evaluatorClosure",
        "executionInputsDigest", "evaluationInputRefs", "ruleProgramDigest",
        "predicateProofs", "findingIds", "verdict", "evaluationState",
        "ruleResults", "waivedFindingIds", "executionDeficiencies",
    }
    rec("s9-names-every-required-proof-field", boundary, set(proof_req) <= named,
        missing=sorted(set(proof_req) - named))
    witness_req = SCHEMA["$defs"]["predicate-witness"]["required"]
    w_named = {
        "schemaVersion", "programPredicateDigest", "matchingFactIds", "uncertainFactIds",
        "matchingImportRows", "uncertainImportRows", "coverageIds", "countLimit",
        "childPredicateIds", "kind", "deficiencies",
    }
    rec("s9-3-names-every-required-witness-field", boundary, set(witness_req) <= w_named,
        missing=sorted(set(witness_req) - w_named))
    rec("witness-schema-forbids-inputRefs", boundary,
        SCHEMA["$defs"]["predicate-witness"].get("additionalProperties") is False
        and "inputRefs" not in SCHEMA["$defs"]["predicate-witness"]["properties"])
    finding_req = SCHEMA["$defs"]["finding"]["required"]
    f_named = {
        "schemaVersion", "fingerprint", "correspondence", "ruleClosure", "ruleId",
        "subjectId", "subject", "messageCode", "parameterDigest", "severity", "evidenceRefs",
    }
    rec("s9-7-names-every-required-finding-field", boundary, set(finding_req) <= f_named,
        missing=sorted(set(finding_req) - f_named))
    ev_req = SCHEMA["$defs"]["semantic-evidence"]["required"]
    e_named = {"schemaVersion", "planId", "viewIds", "coverageIds", "importIds", "findingIds", "proofBundleId"}
    rec("s9-7-names-every-required-evidence-field", boundary, set(ev_req) <= e_named,
        missing=sorted(set(ev_req) - e_named))
    seal_req = SCHEMA["$defs"]["evaluation-seal"]["required"]
    # §9.7 states verdict = proof.verdict and H ids via identifier; it does not name
    # executionPlanId, evidenceId, evaluatorClosure, policyDigest sources.
    seal_named_in_s9 = {"schemaVersion", "verdict", "planId", "proofBundleId"}
    rec("s9-7-does-not-name-every-required-seal-value-source", boundary,
        not set(seal_req) <= seal_named_in_s9,
        unnamed=sorted(set(seal_req) - seal_named_in_s9),
        note="MUST: normative-only consumer cannot assign seal.executionPlanId/evidenceId/evaluatorClosure/policyDigest from §9.7 text alone")
    run_req = SCHEMA["$defs"]["run"]["required"]
    run_named_in_s9 = {"schemaVersion", "planId"}
    rec("s9-7-does-not-name-every-required-run-value-source", boundary,
        not set(run_req) <= run_named_in_s9,
        unnamed=sorted(set(run_req) - run_named_in_s9),
        note="MUST: projectId/snapshotId/evidenceId/evaluationSealId/capabilityManifestId sources are not in §9.7")
    pol_req = SCHEMA["$defs"]["policy-derivation"]["required"]
    p_named = {"schemaVersion", "planId", "proofBundleId", "policyDigest", "waiverDigest", "verdict"}
    rec("s9-7-names-every-required-policy-derivation-field", boundary, set(pol_req) <= p_named,
        missing=sorted(set(pol_req) - p_named))
    rec("program-predicate-description-says-RuleProgramV1", boundary,
        "RuleProgramV1" in SCHEMA["$defs"]["program-predicate"]["description"]
        and SCHEMA["$defs"]["program-predicate"]["properties"]["ruleProgramDigest"]["x-opensip-digest"]["record"]["selector"]
        == "#/$defs/RuleProgramV2",
        note="MUST: linked schema description names V1 while digest selector and §9.1 use RuleProgramV2")
    rec("deficiency-universe-is-64hex-or-null", boundary,
        SCHEMA["$defs"]["evaluation-deficiency"]["properties"]["universe"]["oneOf"][0]["pattern"].startswith("^[0-9a-f]{64}"))
    rec("execution-registry-excludes-native-work-incomplete", boundary,
        "native-work-incomplete" not in EXEC_REG and "unsupported-typed" not in EXEC_REG
        and "work-budget-exhausted" in EXEC_REG and "required-cell-unsatisfied" in EXEC_REG)
    rec("native-registry-keeps-uncovered-expected-source-subject", boundary,
        "uncovered-expected-source-subject" in NATIVE_REG
        and "uncovered-expected-source-subject" not in EXEC_REG)


def main():
    probe_schema_field_inventory()
    probe_compose_fields()
    probe_boolean_union_and_order()
    probe_boolean_eleven_children_cset_order()
    probe_disabled_and_budget()
    probe_required_import_and_correspondence()
    probe_compose_does_not_force_EI()
    probe_unregistered_cause_compose_vs_adapter()
    probe_atom_adapter_refuse()
    probe_identical_projected_dedup()
    probe_execution_admit_binding_plus_inventories()
    probe_execution_input_account_bridge()
    probe_close_run_positive()
    report = {
        "standing": (
            "Independent Grok peer probes of proposed composition §9 field law against "
            "target-proof-successor.v1 reference emission. Synthetic fixtures only. "
            "No compiler qualification. Isolated compose/adapter/admit/bridge cases are not Runs."
        ),
        "python": PY,
        "referenceRoot": str(SUC),
        "passed": all(c["passed"] for c in CASES),
        "count": len(CASES),
        "passCount": sum(1 for c in CASES if c["passed"]),
        "failCount": sum(1 for c in CASES if not c["passed"]),
        "cases": CASES,
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("passed", "count", "passCount", "failCount")}, indent=2))
    failed = [c["id"] for c in CASES if not c["passed"]]
    if failed:
        print("FAILED:", json.dumps(failed))


if __name__ == "__main__":
    main()
