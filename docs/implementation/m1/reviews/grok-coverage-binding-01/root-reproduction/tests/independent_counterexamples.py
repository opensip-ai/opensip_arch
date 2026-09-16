"""Independent Grok counterexamples for the coverage source-binding experiment.

Read-only against the frozen subject and pinned joint/owner trees. Writes only
under review/results/. Loads owner and experiment source by compiling file bytes
with Python -I -B semantics (this file is executed that way).
"""
from __future__ import annotations

import copy
import hashlib
import json
import traceback
import types
from pathlib import Path

from referencing import Resource
from referencing.jsonschema import DRAFT202012

REVIEW = Path(__file__).resolve().parents[1]
RESULTS = REVIEW / "results"
SUBJECT = Path("/tmp/opensip-implementation/m1-grok-coverage-review-01/subject")
JOINT = Path("/tmp/opensip-implementation/m1-report-joint-candidate-09")
PY = Path("/tmp/opensip-implementation/metadata-reference-env/bin/python")

RESULTS.mkdir(parents=True, exist_ok=True)


def load_bytes(path: Path, name: str):
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return module


def refuse_info(exc: BaseException):
    return {"type": type(exc).__name__, "module": type(exc).__module__, "detail": str(exc)}


class Cases:
    def __init__(self):
        self.rows = []

    def record(self, name, passed, **detail):
        row = {"name": name, "passed": bool(passed), **detail}
        self.rows.append(row)
        status = "PASS" if passed else "FAIL"
        print(f"{status} {name}")
        return passed

    def expect_raise(self, name, operation, classes, contains=None, **detail):
        try:
            operation()
        except classes as exc:
            text = str(exc)
            ok = True if contains is None else contains in text
            return self.record(
                name,
                ok,
                exception=refuse_info(exc),
                expectedContains=contains,
                **detail,
            )
        return self.record(name, False, exception=None, expectedContains=contains, **detail)

    def expect_equal(self, name, actual, expected, **detail):
        return self.record(name, actual == expected, **detail)


def main():
    cases = Cases()
    source_path = SUBJECT / "coverage_source.py"
    schema_path = SUBJECT / "coverage-panel.experimental.schema.json"
    source_raw = source_path.read_bytes()
    schema_raw = schema_path.read_bytes()
    cases.record(
        "frozen-coverage-source-hash",
        hashlib.sha256(source_raw).hexdigest()
        == "e2f4e9a283144aef896efb23a7b7814a191c06ac79fd2cf57323a13b7e368a32"
        and len(source_raw) == 4593,
        sha256=hashlib.sha256(source_raw).hexdigest(),
        bytes=len(source_raw),
    )
    cases.record(
        "frozen-schema-hash",
        hashlib.sha256(schema_raw).hexdigest()
        == "ce5557a19130ed1413dcfa08f525068aa61c0f39fdb3406f5f5e6e81c6b677c8"
        and len(schema_raw) == 2874,
        sha256=hashlib.sha256(schema_raw).hexdigest(),
        bytes=len(schema_raw),
    )

    S = types.ModuleType("coverage_source")
    exec(compile(source_raw, str(source_path), "exec"), S.__dict__)
    V = load_bytes(JOINT / "check_model_carriers.py", "carriers")
    R = load_bytes(JOINT / "retained_fixture.py", "retained")
    schema = json.loads(schema_raw)
    cases.record("schema-provenance-const-matches-source", schema["properties"]["provenance"]["const"] == S.PROVENANCE)
    cases.record(
        "schema-identity-and-native-refs",
        schema["properties"]["entries"]["items"]["properties"]["descriptor"]["$ref"]
        == "urn:opensip:product-v1:identity:v3#/$defs/coverage"
        and schema["properties"]["entries"]["items"]["properties"]["result"]["$ref"]
        == "urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CoverageResultV3"
        and schema["$id"] == "urn:opensip:implementation:report-coverage-binding:experiment:1",
    )
    cases.record("schema-item-cap-3956", schema["properties"]["entries"]["maxItems"] == 3956)
    budget_cap = V.report["$defs"]["BudgetProfileV1"]["properties"]["maxEvidenceEntries"]["const"]
    cases.record("pinned-report-maxEvidenceEntries-is-3956", budget_cap == 3956, maxEvidenceEntries=budget_cap)
    cases.record(
        "standalone-projection-omits-byte-budget-cause",
        schema["properties"]["entriesProjection"]["properties"]["omissionCause"]["enum"] == ["none", "item-cap"]
        and "rejectedByteDelta" not in schema["properties"]["entriesProjection"]["properties"],
    )

    registry = V.registry.with_resource(schema["$id"], Resource(contents=schema, specification=DRAFT202012))

    def validate(value):
        V.C.ExactValidator(schema, registry=registry).validate(value)

    findings = []
    with R.world(V.read_unit, V.subjects) as world:
        O = world["M"]
        run = world["run"]
        objects = world["objects"]
        blobs = world["blobs"]
        rid = O.close_run(run, objects, blobs)
        evidence_id = run["evidenceId"]
        evidence = objects[evidence_id][1]
        coverage_ids = evidence["coverageIds"]
        originals = copy.deepcopy((run, objects, blobs))
        cases.record("actual-run-has-two-distinct-coverage-ids", len(coverage_ids) == 2 and coverage_ids == sorted(set(coverage_ids)))
        cases.record(
            "actual-run-id-matches-checkpoint-result",
            rid == "run3:4af491e7199ec451ef4159a0e9d2b16e7be3ef5288e1e9a8b0e6347532bbff02",
            runId=rid,
        )

        panels = {}
        for cap in (0, 1, 2, 3956):
            panel = S.project(rid, run, objects, blobs, cap, O)
            S.verify_against_source(panel, rid, run, objects, blobs, cap, O, validate)
            panels[cap] = panel
            cases.record(
                f"independent-prefix-{cap}",
                [row["coverageId"] for row in panel["entries"]] == coverage_ids[:cap]
                and panel["entriesProjection"]["total"] == 2
                and panel["entriesProjection"]["omitted"] == 2 - len(panel["entries"])
                and panel["source"] == {"runId": rid, "evidenceId": evidence_id},
            )
        cases.record("cap-2-and-3956-are-byte-identical-panels", O.C.canonical(panels[2]) == O.C.canonical(panels[3956]))
        cases.record("caller-source-unmutated-after-project", (run, objects, blobs) == originals)

        # Mutate the actual returned panel, not a deepcopy. Author check.py copies first.
        returned = panels[2]
        before_source = copy.deepcopy((run, objects, blobs))
        before_blob = blobs[returned["entries"][0]["descriptor"]["payloadDigest"]]
        returned["entries"][0]["result"]["entry"]["confidenceMillionths"] = 0
        returned["entries"][0]["descriptor"]["scopeId"] = "scope2:" + ("a" * 64)
        aliased = (run, objects, blobs) != before_source or blobs[returned["entries"][0]["descriptor"]["payloadDigest"]] != before_blob
        cases.record(
            "mutating-actual-returned-panel-does-not-alias-caller-source",
            not aliased,
            aliased=aliased,
        )
        # Restore local panel for later use.
        panels[2] = S.project(rid, run, objects, blobs, 2, O)

        # Decode path: json.loads vs owner C.parse on admitted blobs.
        decode_ok = True
        decode_detail = []
        for cid in coverage_ids:
            descriptor = objects[cid][1]
            raw = blobs[descriptor["payloadDigest"]]
            parsed = O.C.parse(raw)
            loaded = json.loads(raw)
            same_typed = O.C.equal_typed(parsed, loaded)
            roundtrip = O.C.canonical(loaded) == raw == O.C.canonical(parsed)
            decode_detail.append(
                {
                    "coverageId": cid,
                    "equalTyped": same_typed,
                    "canonicalRoundtrip": roundtrip,
                    "payloadDigest": descriptor["payloadDigest"],
                    "blobBytes": len(raw),
                }
            )
            decode_ok = decode_ok and same_typed and roundtrip
        cases.record("admitted-payload-json-loads-matches-owner-parse-and-roundtrips", decode_ok, rows=decode_detail)

        # One descriptor / one payload: each retained coverage2 mints from the bound payload.
        native = O.native_admission()
        registered = native.schema_document_digest(native.NATIVE_SCHEMA_DOC)
        one_to_one = True
        for cid in coverage_ids:
            descriptor = objects[cid][1]
            raw = blobs[descriptor["payloadDigest"]]
            if hashlib.sha256(raw).hexdigest() != descriptor["payloadDigest"]:
                one_to_one = False
            if O.identifier("coverage", descriptor) != cid:
                one_to_one = False
            if descriptor["payloadSchemaDigest"] != registered:
                one_to_one = False
        cases.record("retained-coverage2-is-one-descriptor-one-payload", one_to_one, registeredSchemaDigest=registered)

        # --- Wrong source joins ---
        cases.expect_raise(
            "wrong-expected-run-id",
            lambda: S.project("run3:" + "0" * 64, run, objects, blobs, 2, O),
            S.ProjectionRefusal,
            "SOURCE_RUN_MISMATCH",
        )
        other_evidence = next(
            i for i, (kind, _) in objects.items() if kind == "semantic-evidence" and i != evidence_id
        )
        wrong_join = copy.deepcopy(panels[2])
        wrong_join["source"]["evidenceId"] = other_evidence
        S.verify_embedded(wrong_join, O, validate)
        cases.expect_raise(
            "other-retained-evidence-anchor-fails-source-join",
            lambda: S.verify_against_source(wrong_join, rid, run, objects, blobs, 2, O, validate),
            S.ProjectionRefusal,
            "SOURCE_PROJECTION_MISMATCH",
            otherEvidenceId=other_evidence,
            embeddedPassed=True,
        )
        wrong_run = copy.deepcopy(panels[2])
        wrong_run["source"]["runId"] = "run3:" + "f" * 64
        S.verify_embedded(wrong_run, O, validate)
        cases.expect_raise(
            "wrong-run-anchor-fails-source-join",
            lambda: S.verify_against_source(wrong_run, rid, run, objects, blobs, 2, O, validate),
            S.ProjectionRefusal,
            "SOURCE_PROJECTION_MISMATCH",
            embeddedPassed=True,
        )
        # A valid cap-1 panel is not a source join at cap 2.
        cases.expect_raise(
            "honest-prefix-verified-at-wrong-cap",
            lambda: S.verify_against_source(panels[1], rid, run, objects, blobs, 2, O, validate),
            S.ProjectionRefusal,
            "SOURCE_PROJECTION_MISMATCH",
        )

        # --- Non-prefix selections ---
        nonprefix = copy.deepcopy(panels[1])
        nonprefix["entries"][0] = copy.deepcopy(panels[2]["entries"][1])
        S.verify_embedded(nonprefix, O, validate)
        cases.expect_raise(
            "sorted-singleton-second-id-is-not-prefix",
            lambda: S.verify_against_source(nonprefix, rid, run, objects, blobs, 1, O, validate),
            S.ProjectionRefusal,
            "SOURCE_PROJECTION_MISMATCH",
            selected=nonprefix["entries"][0]["coverageId"],
            sourcePrefix=coverage_ids[:1],
            embeddedPassed=True,
        )
        reversed_rows = copy.deepcopy(panels[2])
        reversed_rows["entries"].reverse()
        cases.expect_raise(
            "reversed-two-rows-fail-embedded-order",
            lambda: S.verify_embedded(reversed_rows, O, validate),
            S.ProjectionRefusal,
            "ENTRY_ORDER_OR_DUPLICATE",
        )
        # Subset of size 2 with first replaced by a duplicate of second: duplicate id.
        dup = copy.deepcopy(panels[2])
        dup["entries"][0] = copy.deepcopy(dup["entries"][1])
        cases.expect_raise(
            "duplicate-coverage-id-fails-embedded",
            lambda: S.verify_embedded(dup, O, validate),
            S.ProjectionRefusal,
            "ENTRY_ORDER_OR_DUPLICATE",
        )

        # --- Self-consistent wrong identities ---
        rehashed = copy.deepcopy(panels[2])
        row = rehashed["entries"][0]
        row["result"]["entry"]["confidenceMillionths"] = 999999
        row["descriptor"]["payloadDigest"] = hashlib.sha256(O.C.canonical(row["result"])).hexdigest()
        row["coverageId"] = O.identifier("coverage", row["descriptor"])
        rehashed["entries"].sort(key=lambda item: item["coverageId"])
        S.verify_embedded(rehashed, O, validate)
        cases.record(
            "self-rehashed-unselected-coverage-passes-embedded",
            True,
            newCoverageId=row["coverageId"],
            inSource=row["coverageId"] in coverage_ids,
        )
        cases.expect_raise(
            "self-rehashed-unselected-coverage-fails-source-join",
            lambda: S.verify_against_source(rehashed, rid, run, objects, blobs, 2, O, validate),
            S.ProjectionRefusal,
            "SOURCE_PROJECTION_MISMATCH",
        )
        extra = next(item for item in rehashed["entries"] if item["coverageId"] not in coverage_ids)
        stuffed = copy.deepcopy(objects)
        stuffed_blobs = copy.deepcopy(blobs)
        stuffed[extra["coverageId"]] = ("coverage", extra["descriptor"])
        stuffed_blobs[extra["descriptor"]["payloadDigest"]] = O.C.canonical(extra["result"])
        projected_with_extra = S.project(rid, run, stuffed, stuffed_blobs, 2, O)
        cases.record(
            "unlinked-hash-valid-coverage-does-not-expand-run-set",
            projected_with_extra == panels[2]
            and extra["coverageId"] not in [item["coverageId"] for item in projected_with_extra["entries"]],
            extraCoverageId=extra["coverageId"],
        )

        # Identity-consistent scope/commitment mismatch: descriptor.scopeId disagrees
        # with payload subjectScopeCommitment, but digests and coverageId recompute.
        mismatched = copy.deepcopy(panels[2])
        victim = mismatched["entries"][0]
        other_scope = panels[2]["entries"][1]["descriptor"]["scopeId"]
        victim["result"]["key"]["subjectScopeCommitment"] = "sha256:" + other_scope.split(":", 1)[1]
        victim["result"]["entry"]["examinedUniverse"]["subjectScopeCommitment"] = victim["result"]["key"]["subjectScopeCommitment"]
        victim["descriptor"]["payloadDigest"] = hashlib.sha256(O.C.canonical(victim["result"])).hexdigest()
        victim["coverageId"] = O.identifier("coverage", victim["descriptor"])
        mismatched["entries"].sort(key=lambda item: item["coverageId"])
        S.verify_embedded(mismatched, O, validate)
        cases.record("identity-consistent-scope-commitment-mismatch-passes-embedded", True)
        cases.expect_raise(
            "identity-consistent-scope-commitment-mismatch-fails-source-join",
            lambda: S.verify_against_source(mismatched, rid, run, objects, blobs, 2, O, validate),
            S.ProjectionRefusal,
            "SOURCE_PROJECTION_MISMATCH",
        )
        scope = objects[panels[2]["entries"][0]["descriptor"]["scopeId"]][1]
        mutated_payload = copy.deepcopy(panels[2]["entries"][0]["result"])
        mutated_payload["key"]["subjectScopeCommitment"] = "sha256:" + other_scope.split(":", 1)[1]
        mutated_payload["entry"]["examinedUniverse"]["subjectScopeCommitment"] = mutated_payload["key"]["subjectScopeCommitment"]
        native_mismatch = native.admit_coverage_result_v3(mutated_payload, scope, [], registered)
        cases.record(
            "native-producer-refuses-scope-commitment-mismatch",
            native_mismatch["result"] == "REFUSE",
            nativeResult=native_mismatch,
        )

        # --- Lost / corrupt records must not become empty success ---
        first = coverage_ids[0]
        descriptor = objects[first][1]
        missing_cov = copy.deepcopy(objects)
        del missing_cov[first]
        cases.expect_raise(
            "missing-coverage-is-not-empty-success",
            lambda: S.project(rid, run, missing_cov, blobs, 2, O),
            O.EvidenceUnavailable,
            first,
        )
        missing_ev = copy.deepcopy(objects)
        del missing_ev[evidence_id]
        cases.expect_raise(
            "missing-evidence-is-not-empty-success",
            lambda: S.project(rid, run, missing_ev, blobs, 2, O),
            O.EvidenceUnavailable,
            evidence_id,
        )
        missing_blob = copy.deepcopy(blobs)
        del missing_blob[descriptor["payloadDigest"]]
        cases.expect_raise(
            "missing-payload-is-not-empty-success",
            lambda: S.project(rid, run, objects, missing_blob, 2, O),
            O.EvidenceUnavailable,
            descriptor["payloadDigest"],
        )
        corrupt = copy.deepcopy(blobs)
        corrupt[descriptor["payloadDigest"]] = b"{}"
        cases.expect_raise(
            "corrupt-payload-is-not-empty-success",
            lambda: S.project(rid, run, objects, corrupt, 2, O),
            O.C.AdmissionError,
            "BLOB_DIGEST",
        )
        truncated = copy.deepcopy(blobs)
        truncated[descriptor["payloadDigest"]] = blobs[descriptor["payloadDigest"]][:-8]
        cases.expect_raise(
            "truncated-payload-is-not-empty-success",
            lambda: S.project(rid, run, objects, truncated, 2, O),
            O.C.AdmissionError,
        )
        wrong_kind = copy.deepcopy(objects)
        wrong_kind[first] = ("fact", wrong_kind[first][1])
        cases.expect_raise(
            "wrong-record-kind-is-not-empty-success",
            lambda: S.project(rid, run, wrong_kind, blobs, 2, O),
            O.C.AdmissionError,
            "REFERENCE_IDENTITY",
        )
        # Unadmitted run graph: drop a required run pointer.
        broken_run = copy.deepcopy(run)
        broken_run["evidenceId"] = "evidence3:" + "0" * 64
        try:
            S.project(rid, broken_run, objects, blobs, 2, O)
            cases.record("unadmitted-run-is-not-empty-success", False, exception=None)
        except Exception as exc:
            empty = False
            cases.record(
                "unadmitted-run-is-not-empty-success",
                not isinstance(exc, S.ProjectionRefusal) or "ENTRY" not in str(exc),
                exception=refuse_info(exc),
                yieldedEmpty=empty,
            )

        # --- Misleading empty results ---
        false_empty = copy.deepcopy(panels[2])
        false_empty["entries"] = []
        false_empty["entriesProjection"].update(total=0, omitted=0, omissionCause="none")
        S.verify_embedded(false_empty, O, validate)
        cases.expect_raise(
            "false-empty-source-fails-source-join",
            lambda: S.verify_against_source(false_empty, rid, run, objects, blobs, 2, O, validate),
            S.ProjectionRefusal,
            "SOURCE_PROJECTION_MISMATCH",
            embeddedPassed=True,
        )
        honest_empty = panels[0]
        cases.record(
            "honest-item-cap-zero-row-is-not-false-empty",
            honest_empty["entries"] == []
            and honest_empty["entriesProjection"]["total"] == 2
            and honest_empty["entriesProjection"]["omitted"] == 2
            and honest_empty["entriesProjection"]["omissionCause"] == "item-cap",
        )
        S.verify_against_source(honest_empty, rid, run, objects, blobs, 0, O, validate)
        cases.record("honest-item-cap-zero-row-joins-source-at-cap-0", True)

        # --- Shape vs native authority ---
        contradiction = copy.deepcopy(panels[2])
        victim = contradiction["entries"][0]
        victim["result"]["entry"]["resolutionCompleteness"]["examinedExhaustive"] = False
        victim["descriptor"]["payloadDigest"] = hashlib.sha256(O.C.canonical(victim["result"])).hexdigest()
        victim["coverageId"] = O.identifier("coverage", victim["descriptor"])
        contradiction["entries"].sort(key=lambda item: item["coverageId"])
        S.verify_embedded(contradiction, O, validate)
        cases.record("self-rehashed-rc6-contradiction-passes-embedded-shape-and-identity", True)
        cases.expect_raise(
            "self-rehashed-rc6-contradiction-fails-source-join",
            lambda: S.verify_against_source(contradiction, rid, run, objects, blobs, 2, O, validate),
            S.ProjectionRefusal,
            "SOURCE_PROJECTION_MISMATCH",
        )
        rc6_scope = objects[panels[2]["entries"][0]["descriptor"]["scopeId"]][1]
        rc6_payload = copy.deepcopy(panels[2]["entries"][0]["result"])
        rc6_payload["entry"]["resolutionCompleteness"]["examinedExhaustive"] = False
        rc6_native = native.admit_coverage_result_v3(rc6_payload, rc6_scope, [], registered)
        cases.record(
            "actual-native-producer-refuses-rc6-contradiction",
            rc6_native["result"] == "REFUSE"
            and any(str(fault.get("fault", "")).startswith("RC-6:") for fault in rc6_native.get("faults", [])),
            nativeResult=rc6_native,
        )
        cases.record(
            "rc6-scope-is-not-a-resolved-rung",
            rc6_scope["resolution"] not in native.RESOLVED_RUNGS,
            resolution=rc6_scope["resolution"],
        )

        # Historical shape/join fixture: CoverageResultV3 shape passes, native local faults exist.
        hist_path = JOINT / "parent-bases.fixture.json"
        hist_raw = hist_path.read_bytes()
        hist_doc = json.loads(hist_raw)["audit-full"]
        hist_payload = hist_doc["panels"]["evidence"]["data"]["entries"][0]
        V.validate("urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CoverageResultV3", hist_payload)
        cases.record(
            "historical-audit-full-entry-passes-coverage-result-shape",
            True,
            fixtureSha256=hashlib.sha256(hist_raw).hexdigest(),
            fixtureBytes=len(hist_raw),
        )
        hist_native = world["load"](
            "coverage_audit_native",
            world["scratch"] / "docs/coop/design-corrections/native/native_evidence_model.v2.py",
        )
        hist_entry = copy.deepcopy(hist_payload["entry"])
        hist_faults = hist_native.coverage_bijection([hist_entry], [])
        hist_causes = hist_native.deficiency_cause_faults(hist_entry)
        cases.record(
            "historical-fixture-has-rc1-and-rc6-and-is-not-the-admitted-run",
            any(str(row["fault"]).startswith("RC-6:") for row in hist_faults)
            and any(str(row["fault"]).startswith("RC-1:") for row in hist_faults)
            and hist_entry["resolution"] not in hist_native.RESOLVED_RUNGS,
            nativeLocalFaults=hist_faults,
            nativeCauseFaults=hist_causes,
        )
        old_panel_shape = hist_doc["panels"]["evidence"]["data"]
        cases.record(
            "historical-evidence-panel-still-uses-single-coverageId-stream",
            "coverageId" in old_panel_shape and "source" not in old_panel_shape,
            keys=sorted(old_panel_shape),
        )

        # --- Source mutation / order ---
        unsorted = copy.deepcopy(objects)
        unsorted_evidence = copy.deepcopy(evidence)
        unsorted_evidence["coverageIds"] = list(reversed(coverage_ids))
        unsorted[evidence_id] = ("semantic-evidence", unsorted_evidence)
        try:
            S.project(rid, run, unsorted, blobs, 2, O)
            cases.record("unsorted-source-coverage-ids-do-not-project", False)
        except Exception as exc:
            # After close_run, SOURCE_COVERAGE_ORDER is likely unreachable because
            # identity ordered() refuses first. Either owner refusal is required.
            cases.record(
                "unsorted-source-coverage-ids-do-not-project",
                True,
                exception=refuse_info(exc),
                sourceCoverageOrderReachable=isinstance(exc, S.ProjectionRefusal) and str(exc) == "SOURCE_COVERAGE_ORDER",
            )

        for cap in (-1, 3957, True, 1.0, "2", None, 2**64):
            cases.expect_raise(
                f"invalid-entry-limit-{cap!r}",
                lambda c=cap: S.project(rid, run, objects, blobs, c, O),
                S.ProjectionRefusal,
                "ENTRY_LIMIT",
            )

        # Schema exact-integer: bool total must not validate.
        bool_total = copy.deepcopy(panels[0])
        bool_total["entriesProjection"]["total"] = True
        try:
            validate(bool_total)
            cases.record("bool-total-rejected-by-exact-integer-schema", False)
        except Exception as exc:
            cases.record("bool-total-rejected-by-exact-integer-schema", True, exception=refuse_info(exc))

        # Embedded count/omission laws.
        wrong_total = copy.deepcopy(panels[2])
        wrong_total["entriesProjection"]["total"] = 3
        cases.expect_raise(
            "wrong-total-fails-embedded",
            lambda: S.verify_embedded(wrong_total, O, validate),
            S.ProjectionRefusal,
            "ENTRY_COUNTS",
        )
        false_omission = copy.deepcopy(panels[2])
        false_omission["entriesProjection"]["omissionCause"] = "item-cap"
        cases.expect_raise(
            "false-omission-fails-embedded",
            lambda: S.verify_embedded(false_omission, O, validate),
            S.ProjectionRefusal,
            "ENTRY_OMISSION",
        )
        payload_sub = copy.deepcopy(panels[2])
        payload_sub["entries"][0]["result"]["entry"]["confidenceMillionths"] = 0
        cases.expect_raise(
            "payload-substitution-fails-embedded",
            lambda: S.verify_embedded(payload_sub, O, validate),
            S.ProjectionRefusal,
            "ENTRY_PAYLOAD_IDENTITY",
        )
        desc_sub = copy.deepcopy(panels[2])
        desc_sub["entries"][0]["descriptor"]["scopeId"] = "scope2:" + "f" * 64
        cases.expect_raise(
            "descriptor-substitution-fails-embedded",
            lambda: S.verify_embedded(desc_sub, O, validate),
            S.ProjectionRefusal,
            "ENTRY_DESCRIPTOR_IDENTITY",
        )
        schema_sub = copy.deepcopy(panels[2])
        schema_sub["entries"][0]["descriptor"]["payloadSchemaDigest"] = "f" * 64
        cases.expect_raise(
            "schema-substitution-fails-embedded",
            lambda: S.verify_embedded(schema_sub, O, validate),
            S.ProjectionRefusal,
            "ENTRY_SCHEMA_IDENTITY",
        )

        # Author non-alias test is vacuous: mutating a deepcopy cannot affect source.
        vacuous = copy.deepcopy(panels[2])
        vacuous["entries"][0]["result"]["entry"]["confidenceMillionths"] = 0
        cases.record(
            "author-returned-values-test-is-vacuous-deepcopy",
            True,
            note="check.py mutates copy.deepcopy(panels['2']), which cannot alias caller source even if project returned aliases",
        )

        # Old report carrier still treats one coverageId as a stream of CoverageResultV3.
        old_panel = V.report["$defs"]["EvidencePanelV1"]
        cases.record(
            "report08-evidence-panel-still-has-single-coverageId-and-result-stream",
            old_panel["required"] == ["coverageId", "entries", "entriesProjection", "provenance"]
            and old_panel["properties"]["entries"]["items"]["$ref"].endswith("CoverageResultV3")
            and "entries-are-retained-stream-prefix-of-coverage-id"
            in old_panel["properties"]["provenance"]["const"]["hostAsserted"],
        )

    # Byte/depth estimates against the actual estimator, without running measure_integration.py
    # (that script writes beside itself).
    B = load_bytes(JOINT / "derive_budget.py", "derive_budget")
    D = load_bytes(JOINT / "derive_depth.py", "derive_depth")
    docs = copy.deepcopy(B.docs)
    docs[schema["$id"]] = schema
    D.V.schemas[schema["$id"]] = schema
    old_entry = B.report["$defs"]["EvidencePanelV1"]["properties"]["entries"]["items"]
    new_schema = copy.deepcopy(schema)
    new_schema.pop("$id")
    new_schema.pop("$schema")
    new_schema.pop("description")
    new_entry = new_schema["properties"]["entries"]["items"]
    old_size = B.bound(docs, B.rid, old_entry)
    new_size = B.bound(docs, schema["$id"], new_entry)
    cases.record(
        "structural-row-bound-delta-is-390",
        old_size == 100328 and new_size == 100718 and new_size - old_size == 390,
        old=old_size,
        new=new_size,
        delta=new_size - old_size,
    )
    before_depth = D.depth(B.rid, D.V.report)
    successor = copy.deepcopy(D.V.report)
    successor["$defs"]["EvidencePanelV1"] = new_schema
    D.V.schemas[B.rid] = successor
    D.memo.clear()
    D.seen_caps.clear()
    after_depth = D.depth(B.rid, successor)
    cases.record(
        "conditional-document-depth-remains-39",
        before_depth == 39 and after_depth == 39,
        current=before_depth,
        withProposedEvidenceCarrier=after_depth,
        profileDepth=B.report["$defs"]["BudgetProfileV1"]["properties"]["maxJsonDepth"]["const"],
    )
    cases.record(
        "shared-exploration-and-document-caps",
        B.report["$defs"]["BudgetProfileV1"]["properties"]["explorationMaxCanonicalBytes"]["const"] == 4194304
        and B.report["$defs"]["BudgetProfileV1"]["properties"]["documentMaxBytes"]["const"] == 27829365,
        exploration=B.report["$defs"]["BudgetProfileV1"]["properties"]["explorationMaxCanonicalBytes"]["const"],
        document=B.report["$defs"]["BudgetProfileV1"]["properties"]["documentMaxBytes"]["const"],
    )

    frozen_panels = json.loads((SUBJECT / "panels.json").read_bytes())
    codec = B.V.C
    actual_rows = []
    for row in frozen_panels["2"]["entries"]:
        old_payload = len(codec.canonical(row["result"]))
        bound_row = len(codec.canonical(row))
        actual_rows.append(
            {
                "coverageId": row["coverageId"],
                "oldPayloadBytes": old_payload,
                "boundRowBytes": bound_row,
                "rowOverheadBytes": bound_row - old_payload,
            }
        )
    cases.record(
        "actual-retained-row-overhead-is-390",
        actual_rows
        == [
            {
                "coverageId": "coverage2:6c1803534378981891c21dc080c2425247cad60a19d7371a348ec91bb60c09ce",
                "oldPayloadBytes": 1046,
                "boundRowBytes": 1436,
                "rowOverheadBytes": 390,
            },
            {
                "coverageId": "coverage2:c96e33f4ab90977b4b741e2c4e47a7b312adf739e5bf8ddf04bf1d6062222ff0",
                "oldPayloadBytes": 1026,
                "boundRowBytes": 1416,
                "rowOverheadBytes": 390,
            },
        ],
        actualRetainedRows=actual_rows,
    )
    wrapped = {cap: len(codec.canonical({"state": "present", "data": value})) for cap, value in frozen_panels.items()}
    cases.record(
        "actual-prefix-panel-bytes-match-measure02",
        wrapped == {"0": 671, "1": 2107, "2": 3520, "3956": 3520} and wrapped["0"] < wrapped["1"] < wrapped["2"] == wrapped["3956"],
        actualPrefixPanelBytes=wrapped,
    )
    identity_codec_sizes = {cap: len(V.C.canonical({"state": "present", "data": value})) for cap, value in frozen_panels.items()}
    cases.record(
        "report-and-identity-canonical-codecs-agree-on-panel-bytes",
        identity_codec_sizes == wrapped,
        identityCodecSizes=identity_codec_sizes,
    )

    claimed = json.loads((SUBJECT / "result.json").read_bytes())
    cases.record("claimed-check-count-is-32", claimed["checkCount"] == 32 and len(claimed["checks"]) == 32)
    cases.record("claimed-passed-true-is-not-taken-as-proof-without-rerun", True)

    failed = [row for row in cases.rows if not row["passed"]]
    output = {
        "standing": "Independent Grok counterexamples; not product acceptance",
        "passed": not failed,
        "caseCount": len(cases.rows),
        "failedCount": len(failed),
        "failed": [row["name"] for row in failed],
        "checks": cases.rows,
        "findings": findings,
    }
    (RESULTS / "independent-counterexamples.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"passed": output["passed"], "caseCount": output["caseCount"], "failed": output["failed"]}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        Path("/tmp/opensip-implementation/m1-grok-coverage-review-01/root-reproduction/results").mkdir(parents=True, exist_ok=True)
        Path("/tmp/opensip-implementation/m1-grok-coverage-review-01/root-reproduction/results/independent-counterexamples.exc").write_text(
            traceback.format_exc()
        )
        raise
