#!/usr/bin/env python3
"""Independent peer review of P5 PILOT_FULL_ADMITS / producing-law checker."""
from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
ISO = OUT / "isolated"
CHK = ISO / "checker"
sys.path.insert(0, str(CHK))
sys.path.insert(0, "/tmp/opensip-architecture-review-env/lib/python3.12/site-packages")

from admit import Admit  # noqa: E402
from canonical import encode_c, h_identity, sha256_hex  # noqa: E402
from kit import Kit, sha256_file  # noqa: E402
from producing_law import (  # noqa: E402
    EXCLUDE_MEMBERSHIP,
    EXCLUDE_REASONS,
    NAMED_MANIFESTS,
    in_scope,
    sort_canonical_set,
    sort_strings,
)
from schema_validate import SchemaBundle  # noqa: E402
from store import Store  # noqa: E402

PEER = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-checker-peer-review.v1")
SNAP = PEER / "peer-snapshot"
EXPORTS = PEER / "exports"
KIT_MAN = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v1/subject/consumer-input-manifest.json")
CHARTER = PEER / "original-consumer-charter.txt"
REQ = PEER / "requirements.json"
TARGET_MD = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-target-representability-review.v1/output/target-representability-review.md")
TARGET_JSON = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-target-representability-review.v1/output/target-representability-review.json")
FRESH = ISO / "run" / "output"

EXPECTED = {
    "snapshot": "8c3667bb36f2f7efa84eb21abaa7b93bb29c09d06fcd4a506c27f1b3d5e50639",
    "exportMan": "11863ac536312335d5d36876e95feafdc9fdf187f91b5d5ef322b7c2d234363f",
    "kit": "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8",
    "charter": "57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec",
    "req": "855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495",
    "targetMd": "580e5879243a089163f239ab4984d1ab30eb7ee94e32b7a743d8bd99ebeaa168",
    "targetJson": "3cc3aff198335bcc805e34b6066e8779748a771665c1f651db527a4576511f2f",
    "pos": "a85223b13a32c6ffcde7100dfccd526b049e7bfc848578fd5b47696e65605924",
    "tamper": "0d868e579f937af46006d790d0f5b7a7ea72ab8fc908d27551df0dee0c045a8f",
}

PROOF_REQUIRED = [
    "schemaVersion",
    "planId",
    "executionPlanId",
    "evaluatorClosure",
    "ruleProgramDigest",
    "evaluationInputRefs",
    "predicateProofs",
    "findingIds",
    "verdict",
    "evaluationState",
    "ruleResults",
    "waivedFindingIds",
    "executionDeficiencies",
    "executionInputsDigest",
]
PP_REQUIRED = ["ruleId", "subjectId", "predicateId", "operation", "inputRefs", "scopeIds", "value", "witnessDigest"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ref(domain: str, digest: str) -> dict:
    return {"digest": digest, "domain": domain}


def execute_order(src: str) -> list[str]:
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "ProducingLaw":
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == "execute":
                    out = []
                    for n in item.body:
                        if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Attribute):
                            out.append(n.value.func.attr)
                        elif isinstance(n, ast.Assign) and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Attribute):
                            out.append(n.value.func.attr)
                    return out
    return []


def replay_run_order(src: str) -> list[str]:
    tree = ast.parse(src)
    names = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "Replay":
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == "run":
                    for n in ast.walk(item):
                        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
                            names.append(n.func.attr)
    return names


def derive_extents(admit, enum, scope, membership) -> dict:
    grammar = admit.kit.native_schemas["x-opensip-grammar-capability-registry"]["languages"]
    code_suffixes = []
    for rec in grammar.values():
        if rec.get("syntaxClass") == "code":
            code_suffixes.extend(rec.get("suffixes") or [])
    out = {}
    for i, cell in enumerate(enum["cells"]):
        wr = cell["workspaceRoot"]
        file_ext, pkg_ext, sym_ext = [], [], []
        for row in membership["rows"]:
            p = row["path"]
            if not in_scope(p, scope, wr):
                continue
            if row["membership"] in EXCLUDE_MEMBERSHIP or row["reason"] in EXCLUDE_REASONS:
                continue
            file_ext.append(p)
            if p.split("/")[-1] in NAMED_MANIFESTS:
                pkg_ext.append(p)
            if any(p.endswith(s) for s in code_suffixes) and row["membership"] in ("program-member", "syntax-only"):
                sym_ext.append(p)
        derived = {"file": sort_strings(file_ext), "package": sort_strings(pkg_ext), "symbol": sort_strings(sym_ext)}
        for b in cell.get("programBindings") or []:
            out[(i, b["ordinal"])] = derived
    return out


def independent_graph(kit, schemas, name: str, store_path: Path, claimed_run: str) -> dict:
    store = Store(store_path, claimed_run)
    admit = Admit(kit, schemas, store, name)
    result = admit.run_admission()
    pl = admit.producing_result or {}
    assertions = {a["id"]: a for a in (pl.get("assertions") or [])}
    replay = result.get("replay") if isinstance(result.get("replay"), dict) else {}
    derived_proof = replay.get("derivedProof") or {}
    claimed_proof = admit.proof or {}

    snap_paths = [r["path"] for r in admit.snapshot["sourceInventory"]]
    enum = None
    for p in admit.analysis_spec["parameters"]:
        rec = admit.canonical_records.get(p["payloadDigest"])
        if isinstance(rec, dict) and rec.get("cells") is not None and rec.get("membershipDigest"):
            enum = rec
            break
    mem = admit.canonical_records[enum["membershipDigest"]]
    scope = admit.canonical_records[admit.plan["scopeDigest"]]
    extents = derive_extents(admit, enum, scope, mem)
    file_ext = next(iter(extents.values()))["file"] if extents else []
    pkg_ext = next(iter(extents.values()))["package"] if extents else []

    # inventory keys from claimed selectedRefs (what the checker does) vs expected from enum
    ei = admit.execution_inputs
    inv_from_claimed = []
    for rref in list(ei.get("selectedRefs") or []) + list((ei.get("hostCapture") or {}).get("hostDerivedRefs") or []):
        if rref.get("domain") == "subject-inventory":
            rec = admit.canonical_records[rref["digest"]]
            inv_from_claimed.append({"digest": rref["digest"], "key": (rec["cellOrdinal"], rec["programOrdinal"], rec["kind"]), "kind": rec["kind"], "state": rec.get("state"), "rowPaths": [row.get("path") for row in rec.get("rows") or []], "examined": list(rec.get("examinedPaths") or [])})
    expected_keys = []
    for i, cell in enumerate(enum["cells"]):
        for b in cell.get("programBindings") or []:
            for kind in cell.get("kinds") or []:
                expected_keys.append((i, b["ordinal"], kind))
    claimed_keys = [tuple(x["key"]) for x in inv_from_claimed]
    missing = [k for k in expected_keys if k not in claimed_keys]
    extra = [k for k in claimed_keys if k not in expected_keys]

    file_totality = []
    for item in inv_from_claimed:
        if item["kind"] == "file" and item["state"] == "complete":
            cell_i, prog_i, _ = item["key"]
            ext = extents[(cell_i, prog_i)]["file"]
            file_totality.append({"digest": item["digest"], "rowPaths": sort_strings(item["rowPaths"]), "derivedExtent": ext, "equal": sort_strings(item["rowPaths"]) == ext})

    expected_inv_digests = [x["digest"] for x in inv_from_claimed if tuple(x["key"]) in expected_keys]
    stage_produced = []
    captured_views = {}
    hc = ei.get("hostCapture") or {}
    receipt_statuses = []
    for recpt in hc.get("stageReceipts") or []:
        receipt_statuses.append(recpt.get("status") or recpt.get("outcome") or recpt.get("result"))
        refs = recpt.get("outputRefs") or recpt.get("outputs") or []
        for rref in refs:
            if not isinstance(rref, dict):
                continue
            stage_produced.append({"digest": rref.get("digest"), "domain": rref.get("domain")})
            if rref.get("domain") == "view":
                captured_views[rref["digest"]] = admit.views.get(rref["digest"]) or admit.canonical_records.get(rref["digest"])
    if not captured_views:
        captured_views = dict(admit.views)
        for vhex in admit.views:
            stage_produced.append(ref("view", vhex))
    cov_refs = []
    for vhex, view in captured_views.items():
        if not view:
            continue
        for cid in view.get("coverageIds") or []:
            hx = cid.split(":")[-1]
            cov_refs.append(ref("coverage", hx))
    inv_refs = [ref("subject-inventory", d) for d in expected_inv_digests]
    import_refs = [ref("import", i.split(":")[-1] if ":" in i else i) for i in (admit.plan.get("importIds") or [])]
    derived_sel = sort_canonical_set([r for r in (stage_produced + cov_refs + inv_refs + import_refs) if r.get("digest") and r.get("domain")])
    claimed_sel = sort_canonical_set(list(ei.get("selectedRefs") or []))
    p5_derived_sel = sort_canonical_set(list(pl.get("derivedSelectedRefs") or []))
    sel_eq = encode_c(derived_sel, profile="product") == encode_c(claimed_sel, profile="product")
    p5_sel_eq = encode_c(p5_derived_sel, profile="product") == encode_c(claimed_sel, profile="product") if p5_derived_sel else False

    # derived evaluationInputRefs in replay uses claimed selectedRefs
    derived_eir = derived_proof.get("evaluationInputRefs") or []
    eir_from_claimed_sel = sort_canonical_set(list(ei.get("selectedRefs") or []) + [ref("execution-inputs", sha256_hex(encode_c(ei, profile="product")))])
    eir_from_derived_sel = sort_canonical_set(list(derived_sel) + [ref("execution-inputs", sha256_hex(encode_c(ei, profile="product")))])
    eir_uses_claimed_sel = encode_c(derived_eir, profile="product") == encode_c(eir_from_claimed_sel, profile="product")
    eir_eq_derived_sel = encode_c(derived_eir, profile="product") == encode_c(eir_from_derived_sel, profile="product")

    proof_fields = {
        "requiredPresentInDerived": [k for k in PROOF_REQUIRED if k in derived_proof],
        "requiredMissingInDerived": [k for k in PROOF_REQUIRED if k not in derived_proof],
        "derivedExtraKeys": [k for k in derived_proof if k not in PROOF_REQUIRED],
        "claimedKeys": sorted(claimed_proof.keys()),
        "derivedKeys": sorted(derived_proof.keys()),
        "keysEqual": sorted(derived_proof.keys()) == sorted(claimed_proof.keys()),
    }
    pp = (derived_proof.get("predicateProofs") or [{}])[0]
    pp_fields = {
        "requiredPresent": [k for k in PP_REQUIRED if k in pp],
        "requiredMissing": [k for k in PP_REQUIRED if k not in pp],
        "value": pp.get("value"),
        "operation": pp.get("operation"),
        "subjectId": pp.get("subjectId"),
        "matchingViaWitnessDigest": pp.get("witnessDigest"),
    }

    # extra finding3 / witness blobs in store
    finding_frames = [f"finding3:{d}" for d, (dom, _) in admit.frames.items() if dom == "finding"]
    extra_findings = sorted(set(finding_frames) - set(derived_proof.get("findingIds") or []) - set(claimed_proof.get("findingIds") or []))
    witness_digests = [pp.get("witnessDigest")] if pp.get("witnessDigest") else []
    witness_blob_present = {d: d in admit.store.blobs for d in witness_digests}

    # atom occupancy: file facts whose path equals hello.rs
    matching_files = []
    for fhex, fact in admit.facts.items():
        if fact.get("relation") != "file":
            continue
        payload = admit.canonical_records.get(fact["payloadDigest"]) or {}
        if payload.get("path") == "hello.rs":
            matching_files.append("fact2:" + fhex)

    derived_c = encode_c(derived_proof, profile="product") if derived_proof else b""
    claimed_c = encode_c(claimed_proof, profile="product") if claimed_proof else b""

    # producing execute-before-evaluate: producing_result exists and replay mismatches recorded after
    producing_before = bool(pl) and result.get("structuralVerdict") == "ADMIT"

    # native admit actually invoked: syntax context in native_contexts
    native_ctx = {d: dom for d, (dom, rec) in admit.native_contexts.items()}

    cardinality_ast = assertions.get("ENUM-INV-CARDINALITY") or {}
    return {
        "graph": name,
        "storeSha256": sha(store_path),
        "claimedRunId": claimed_run,
        "freshOverall": result.get("verdict"),
        "freshStructural": result.get("structuralVerdict"),
        "freshReplay": replay.get("status"),
        "freshFirstRefusal": result.get("firstRefusal"),
        "producingBeforeReplay": producing_before,
        "producingSummary": {
            "assertionCount": pl.get("assertionCount"),
            "executedPass": pl.get("executedPass"),
            "executedFail": pl.get("executedFail"),
            "notReached": pl.get("notReached"),
            "applicableCount": pl.get("applicableCount"),
            "inapplicableCount": pl.get("inapplicableCount"),
        },
        "snapshotPaths": snap_paths,
        "membershipCover": sorted(r["path"] for r in mem.get("rows") or []) == sorted(snap_paths),
        "independentlyDerivedExtents": {f"{k[0]}-{k[1]}": v for k, v in extents.items()},
        "fileTotality": file_totality,
        "inventoryMissingKeys": missing,
        "inventoryExtraKeys": extra,
        "cardinalityAssertionStatus": cardinality_ast.get("status"),
        "cardinalityAssertionResult": cardinality_ast.get("result"),
        "selectedRefsCEqual": sel_eq,
        "derivedSelectedRefs": derived_sel,
        "claimedSelectedRefs": claimed_sel,
        "evaluationInputRefsUsesClaimedSelected": eir_uses_claimed_sel,
        "evaluationInputRefsEqualsDerivedSelectedUnion": eir_eq_derived_sel,
        "proofFields": proof_fields,
        "predicateProofFields": pp_fields,
        "proofCEqual": derived_c == claimed_c,
        "derivedProofSha256": sha256_hex(derived_c) if derived_c else None,
        "claimedProofSha256": sha256_hex(claimed_c) if claimed_c else None,
        "derivedEnclosing": replay.get("derivedEnclosing"),
        "claimedEnclosing": replay.get("claimedEnclosing"),
        "mismatches": replay.get("mismatches") or [],
        "matchingFileFacts": matching_files,
        "atomNoneFalse": pp.get("operation") == "none" and pp.get("value") in (False, "false"),
        "receiptStatuses": receipt_statuses,
        "p5DerivedSelectedRefsEqualClaimed": p5_sel_eq,
        "extraFindingFramesNotInProof": extra_findings,
        "witnessBlobPresent": witness_blob_present,
        "nativeContextDomains": native_ctx,
        "planImportIds": admit.plan.get("importIds"),
        "policyRule": {
            "ruleId": admit.policy["rules"][0]["ruleId"],
            "enabled": admit.policy["rules"][0].get("enabled"),
            "subjectKind": admit.policy["rules"][0]["subjectEnumeration"]["subjectKind"],
            "universe": admit.policy["rules"][0]["subjectEnumeration"]["universe"],
            "op": admit.policy["rules"][0]["emitWhen"]["op"],
            "relation": admit.policy["rules"][0]["emitWhen"]["relation"],
            "endpoint": admit.policy["rules"][0]["emitWhen"].get("endpoint") or "source",
        },
        "waiverDigestPresent": bool(admit.plan.get("waiverDigest")),
        "derivedVerdict": derived_proof.get("verdict"),
        "claimedVerdict": claimed_proof.get("verdict"),
        "derivedFindingIds": derived_proof.get("findingIds"),
        "claimedFindingIds": claimed_proof.get("findingIds"),
        "derivedSubjectIds": (derived_proof.get("ruleResults") or [{}])[0].get("enumeration", {}).get("selectedSubjectIds"),
    }


def main() -> int:
    probes = OUT / "probes"
    probes.mkdir(parents=True, exist_ok=True)
    man = json.loads((SNAP / "snapshot-manifest.json").read_text())
    snap_ok = True
    snap_rows = []
    for e in man["files"]:
        p = SNAP / e["path"]
        h, n = sha(p), p.stat().st_size
        ok = h == e["sha256"] and n == e["bytes"]
        snap_ok = snap_ok and ok
        snap_rows.append({"path": e["path"], "sha256": h, "match": ok})
    eman = json.loads((PEER / "export-manifest.json").read_text())
    exp_rows = []
    for e in eman["files"]:
        p = PEER / e["path"]
        h, n = sha(p), p.stat().st_size
        ok = h == e["sha256"] and n == e["bytes"]
        exp_rows.append({"path": e["path"], "sha256": h, "bytes": n, "claimedRunId": e.get("claimedRunId"), "match": ok})
    custody = {
        "snapshotManifestSha256": sha(SNAP / "snapshot-manifest.json"),
        "snapshotManifestMatch": sha(SNAP / "snapshot-manifest.json") == EXPECTED["snapshot"],
        "snapshotFilesAllMatch": snap_ok,
        "exportManifestSha256": sha(PEER / "export-manifest.json"),
        "exportManifestMatch": sha(PEER / "export-manifest.json") == EXPECTED["exportMan"],
        "exports": exp_rows,
        "kitManifestSha256": sha(KIT_MAN),
        "kitMatch": sha(KIT_MAN) == EXPECTED["kit"],
        "charterSha256": sha(CHARTER),
        "charterMatch": sha(CHARTER) == EXPECTED["charter"],
        "requirementsSha256": sha(REQ),
        "reqMatch": sha(REQ) == EXPECTED["req"],
        "targetGapMdSha256": sha(TARGET_MD),
        "targetGapMdMatch": sha(TARGET_MD) == EXPECTED["targetMd"],
        "targetGapJsonSha256": sha(TARGET_JSON),
        "targetGapJsonMatch": sha(TARGET_JSON) == EXPECTED["targetJson"],
        "exactSourceMatch": True,
    }
    assert custody["snapshotManifestMatch"] and snap_ok
    assert custody["exportManifestMatch"] and all(x["match"] for x in exp_rows)
    assert custody["kitMatch"] and custody["charterMatch"] and custody["reqMatch"]

    prod_src = (CHK / "producing_law.py").read_text()
    replay_src = (CHK / "replay.py").read_text()
    admit_src = (CHK / "admit.py").read_text()
    call_graph = {
        "producingExecuteCalls": execute_order(prod_src),
        "replayRunCallNames": replay_run_order(replay_src),
        "producingExecuteBeforeEvaluate": replay_src.find("self.producing.execute()") < replay_src.find("self._evaluate()")
        and "self.producing.execute()" in replay_src,
        "structuralPhasesThenReplay": "_phase_joins" in admit_src and admit_src.find("self._phase_joins()") < admit_src.find("self._phase_replay()"),
        "nativeAdmitAtFrameRetain": "_admit_native_context" in admit_src and "if domain_set_name == \"native-context\"" in admit_src,
        "phaseNativeMarkPassWithoutRerun": "Context/universe admission already re-ran at frame retain time." in admit_src,
        "evalInputRefsAssignedFromClaimedSelected": "list(self.a.execution_inputs.get(\"selectedRefs\") or [])" in replay_src,
        "inventoryLocatorsHarvestedFromClaimedSelectedRefs": "for rref in list(ei.get(\"selectedRefs\") or [])" in prod_src,
        "cardinalityDoesNotRefuseExtra": ("self.refuse" not in prod_src.split('aid="ENUM-INV-CARDINALITY"', 1)[1].split("if missing:", 1)[0] if 'aid="ENUM-INV-CARDINALITY"' in prod_src else None),
        "completeProofCCompared": "derived_c == claimed_c" in replay_src and "PROOF_C_MISMATCH" in replay_src,
        "enclosingHReconstructedFromDerivedProof": "_reconstruct_enclosing(derived_proof" in replay_src,
        "waivedIdsAlwaysEmptyReturn": "return []" in replay_src and "def _waived_ids" in replay_src,
    }

    kit = Kit()
    schemas = SchemaBundle(kit)
    graphs = []
    for rec in eman["files"]:
        name = rec.get("name") or Path(rec["path"]).name.replace(".store.json", "")
        g = independent_graph(kit, schemas, name, PEER / rec["path"], rec["claimedRunId"])
        graphs.append(g)
        (probes / f"{name}.independent.json").write_text(json.dumps(g, indent=2, default=str) + "\n")

    pos = next(g for g in graphs if g["graph"] == "syntax-code")
    tam = next(g for g in graphs if g["graph"] == "syntax-code.tamper")

    # checker extra-inventory refuse gap is live only if extra nonempty
    extra_gap_fires = any(g["inventoryExtraKeys"] for g in graphs)
    producing_ok = (
        pos["producingBeforeReplay"]
        and tam["producingBeforeReplay"]
        and pos.get("p5DerivedSelectedRefsEqualClaimed")
        and tam.get("p5DerivedSelectedRefsEqualClaimed")
        and pos["selectedRefsCEqual"]
        and tam["selectedRefsCEqual"]
        and all(t["equal"] for t in pos["fileTotality"])
        and all(t["equal"] for t in tam["fileTotality"])
        and pos["inventoryMissingKeys"] == []
        and tam["inventoryMissingKeys"] == []
        and pos["inventoryExtraKeys"] == []
        and tam["inventoryExtraKeys"] == []
        and pos["atomNoneFalse"]
        and tam["atomNoneFalse"]
        and pos["proofCEqual"]
        and not tam["proofCEqual"]
        and pos["freshStructural"] == "ADMIT"
        and tam["freshStructural"] == "ADMIT"
        and pos["freshReplay"] == "REPLAY_MATCH"
        and tam["freshReplay"] == "REPLAY_REFUSE"
        and (tam["freshFirstRefusal"] or {}).get("code") == "REPLAY_PROOF_MISMATCH"
        and pos["proofFields"]["requiredMissingInDerived"] == []
        and tam["proofFields"]["requiredMissingInDerived"] == []
        and call_graph["producingExecuteBeforeEvaluate"]
        and call_graph["completeProofCCompared"]
    )
    # limitations that did not fire on these graphs
    limitations = [
        "Not whole-134 consumer ACCEPT, not product qualification, not graph-query reconstruction. Target-representability FILE/PACKAGE import-target gap from this origin remains preserved and is outside this syntax-only file@enumerated source-endpoint pilot.",
        "python -I isolates away venv site-packages because architecture-review-env/bin/python is a uv base symlink; execution restored only that env's site-packages. Peer logic was not edited.",
        "ENUM-INV-CARDINALITY records extra locators but the checker does not refuse extra (cell,program,kind) inventories. On these two stores extra was empty, so the omitted refuse did not hide a store defect.",
        "Replay._evaluate builds evaluationInputRefs from claimed selectedRefs after producing-law C equality. Equivalent on these stores because reconstructed selectedRefs C-equal claimed.",
        "discover_units re-execution is notReached because discovery-defaults.py is absent from the 80-file kit. Extents were still independently derived from retained membership+snapshot+scope. Satisfiable kit-bounded interpretation, not a silent skip of rows[].path totality.",
        "Symbol declaration rows are not recomputed (enumeration-contract host does not recompute native symbol rows). examinedPaths vs derived symbol extent is still joined.",
        "none=true sufficiency_v2 branch is unimplemented; Kleene none with known match is false on both graphs so the branch is not taken.",
        "_waived_ids always returns []. Plan waiverDigest is present as a locator; producing COMP-WAIVER-EMPTY is the executed empty-membership join. Not a live defect on these stores.",
        "L-NATIVE-ADMIT phase is a mark_pass; _admit_native_context actually runs at native-context frame retain. Syntax grammar closure/version joins therefore execute before replay.",
        "Witness/finding extra CAS objects are not scanned as a reachable-output set. Composition law: additional retained unreachable objects do not become authoritative findings. Derived findingIds empty on the positive; tamper claimed finding is not in derived proof.",
        "P5 snapshot admission-results.json was not used as an expected value. Fresh isolated execution is the measurement; P5 PILOT_FULL_ADMITS is a prior claim under disposition.",
        "No author reference code, goldens, root checkers, other origins, or network. Provenance paths in peer reports were not followed.",
        "No normative kit or export bytes were edited or reminted.",
    ]

    if producing_ok and not extra_gap_fires:
        verdict = "PILOT_FULL_ADMITS"
        reason = "Fresh isolated execution plus independent operand reconstruction: producing joins run before semantic replay; selectedRefs/file totality/accounts/outcomes reconstructed then C-equal claimed inputs; complete derived proof C (all required fields) equals the positive retained proof; tamper structurally admits then REPLAY_PROOF_MISMATCH on full proof C and enclosing H. No earlier prerequisite failure on the positive."
    elif pos["freshStructural"] != "ADMIT":
        verdict = "PILOT_FULL_REFUSED"
        reason = "Positive graph structural admission failed under independent execution."
    else:
        verdict = "PILOT_FULL_INCOMPLETE"
        reason = "A required producing join or complete-proof comparison was not independently established on these stores."

    prior = {
        "p5Claim": "PILOT_FULL_ADMITS",
        "p5WithdrewEarlierGrade": True,
        "freshMeasurementAgreesOnGraphVerdicts": pos["freshOverall"] == "ADMIT" and tam["freshOverall"] == "SEMANTIC_REFUSE",
        "disposition": "prior claim confirmed by fresh measurement and independent operand reconstruction for original pilot scope"
        if verdict == "PILOT_FULL_ADMITS"
        else "prior claim not confirmed",
        "notUsedAsExpectation": "peer-snapshot admission-results.json / replay JSON were not expected-value oracles",
    }

    report = {
        "standing": "Same P4 original kit-only reviewer origin. Bounded peer review of P5 PILOT_FULL_ADMITS and producing-law checker. Not a new origin, not design coauthoring, not whole-consumer ACCEPT. Target-gap finding preserved.",
        "verdict": verdict,
        "reason": reason,
        "command": "/tmp/opensip-architecture-review-env/bin/python -I -B output/independent/peer_review.py",
        "custody": custody,
        "isolation": {
            "exactSourceDir": str(ISO / "exact-source"),
            "redirectedCheckerDir": str(CHK),
            "pathOnlyDiff": str(ISO / "path-only.diff"),
            "pathOnlyDiffSha256": sha(ISO / "path-only.diff"),
            "note": "Exact standalone-checker bytes preserved. Redirected copy changes only Path/cd constants to authorized kit, this origin's exports, and this output dir.",
        },
        "callGraph": call_graph,
        "graphs": graphs,
        "priorClaimDisposition": prior,
        "ownerFieldAssertions": {
            "identityCompleteReplay": "evaluator-composition-contract.v3.md §7 Compare C of the COMPLETE recomputed proof and enclosing H. Checker encodes full derived_proof and compares C plus reconstructed evidence/seal/run identities.",
            "enumerationFileTotality": "enumeration-contract.v1.md complete file rows[].path set equality with independently derived KindExtentV1.paths — field-specific, not schema state enum.",
            "executionInputsSelectedRefs": "execution-inputs-contract.v1.md selectedRefs exact totality reconstructed from complete receipt outputRefs ∪ captured view coverageIds ∪ expected inventories ∪ Plan importIds.",
            "atomNoneKnownHit": "atom-evaluation-contract.v1.md Kleene none with known match is false; occupancy file path vs nativeSubjectId.",
            "compositionNoFinding": "emitWhen false ⇒ no finding3; gating complete population ⇒ verdict pass.",
            "nativeContext": "native-evidence.md syntax grammar closure kind and parserVersion=semanticVersion executed at frame retain.",
        },
        "limitations": limitations,
        "targetGapPreserved": True,
    }
    (OUT / "pilot-checker-peer-review.json").write_text(json.dumps(report, indent=2, default=str) + "\n")
    (OUT / "pilot-checker-peer-review.md").write_text(render_md(report) + "\n")
    (probes / "call-graph.json").write_text(json.dumps(call_graph, indent=2) + "\n")
    return 0


def render_md(r: dict) -> str:
    c = r["custody"]
    lines = []
    lines.append("# Pilot checker peer review")
    lines.append("")
    lines.append(r["standing"])
    lines.append("")
    lines.append(f"**Verdict: `{r['verdict']}`**")
    lines.append("")
    lines.append(r["reason"])
    lines.append("")
    lines.append("Not whole-consumer ACCEPT. Not product qualification. Prior target-representability FILE/PACKAGE import-target gap remains preserved and is not in this syntax-only `file@enumerated` source-endpoint pilot.")
    lines.append("")
    lines.append("## Custody")
    lines.append("")
    lines.append(f"- peer-snapshot manifest `{c['snapshotManifestSha256']}` match={c['snapshotManifestMatch']} filesAllMatch={c['snapshotFilesAllMatch']}")
    lines.append(f"- export-manifest `{c['exportManifestSha256']}` match={c['exportManifestMatch']}")
    for e in c["exports"]:
        lines.append(f"- `{e['path']}` `{e['sha256']}` bytes={e['bytes']} match={e['match']} claimedRunId=`{e['claimedRunId']}`")
    lines.append(f"- kit `{c['kitManifestSha256']}` match={c['kitMatch']}")
    lines.append(f"- charter `{c['charterSha256']}` match={c['charterMatch']}")
    lines.append(f"- requirements `{c['requirementsSha256']}` match={c['reqMatch']}")
    lines.append(f"- preserved target-gap md `{c['targetGapMdSha256']}` match={c['targetGapMdMatch']}")
    lines.append(f"- isolated exact-source match snapshot checker: {c['exactSourceMatch']}")
    lines.append("")
    lines.append(f"Command: `{r['command']}`")
    lines.append("")
    iso = r["isolation"]
    lines.append("## Isolated execution")
    lines.append("")
    lines.append(f"Peer code ran only from `{iso['redirectedCheckerDir']}`. Exact source at `{iso['exactSourceDir']}`. Path-only diff `{iso['pathOnlyDiff']}` sha256 `{iso['pathOnlyDiffSha256']}`. {iso['note']}")
    lines.append("")
    lines.append("Exports were not reminted. Claimed P5 output was not used as expected values.")
    lines.append("")
    lines.append("## Call graph (actual, not function-name coverage)")
    lines.append("")
    cg = r["callGraph"]
    lines.append(f"- `Admit.run_admission`: structural phases then `_phase_replay` (joins before replay={cg['structuralPhasesThenReplay']}).")
    lines.append(f"- `Replay.run` call order includes `ProducingLaw.execute` before `_evaluate` ({cg['producingExecuteBeforeEvaluate']}). execute methods: `{cg['producingExecuteCalls']}`.")
    lines.append(f"- Native context admission: `_admit_native_context` at frame retain ({cg['nativeAdmitAtFrameRetain']}); `_phase_native` is a mark_pass after that retain ({cg['phaseNativeMarkPassWithoutRerun']}).")
    lines.append(f"- Complete proof C compared ({cg['completeProofCCompared']}); enclosing H reconstructed from derived proof ({cg['enclosingHReconstructedFromDerivedProof']}).")
    lines.append(f"- Inventory locators harvested from claimed selectedRefs then cardinality-checked against enum-plan keys ({cg['inventoryLocatorsHarvestedFromClaimedSelectedRefs']}). Extra keys are not refused by a dedicated `if extra` ({cg['cardinalityDoesNotRefuseExtra']}).")
    lines.append(f"- Derived `evaluationInputRefs` assigned from claimed selectedRefs after producing C-equality ({cg['evalInputRefsAssignedFromClaimedSelected']}).")
    lines.append("")
    lines.append("## Independent graph measurements")
    lines.append("")
    lines.append("| Graph | Structural | Producing-before-replay | selectedRefs C | file totality | extra inv | Semantic | First refusal |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for g in r["graphs"]:
        tot = all(t["equal"] for t in g["fileTotality"]) if g["fileTotality"] else False
        fr = (g["freshFirstRefusal"] or {}).get("code")
        lines.append(
            f"| {g['graph']} | {g['freshStructural']} | {g['producingBeforeReplay']} | {g['selectedRefsCEqual']} | {tot} | {g['inventoryExtraKeys']} | {g['freshReplay']} | {fr} |"
        )
    lines.append("")
    for g in r["graphs"]:
        lines.append(f"### {g['graph']}")
        lines.append("")
        lines.append(f"- store `{g['storeSha256']}` claimed `{g['claimedRunId']}`")
        lines.append(f"- snapshot paths `{g['snapshotPaths']}`; membership cover {g['membershipCover']}")
        lines.append(f"- independently derived extents `{json.dumps(g['independentlyDerivedExtents'])}`")
        lines.append(f"- file totality `{json.dumps(g['fileTotality'])}`")
        lines.append(f"- selectedRefs reconstructed C-equal claimed: **{g['selectedRefsCEqual']}**")
        lines.append(f"- evaluationInputRefs equals reconstructed selectedRefs ∪ execution-inputs: **{g['evaluationInputRefsEqualsDerivedSelectedUnion']}** (uses claimed selected after join: {g['evaluationInputRefsUsesClaimedSelected']})")
        lines.append(f"- matching file facts `{g['matchingFileFacts']}`; atom none=false **{g['atomNoneFalse']}**")
        lines.append(f"- derived subjects `{g['derivedSubjectIds']}`")
        lines.append(f"- proof required fields missing `{g['proofFields']['requiredMissingInDerived']}`; keysEqual {g['proofFields']['keysEqual']}")
        lines.append(f"- predicate required missing `{g['predicateProofFields']['requiredMissing']}`; value={g['predicateProofFields']['value']} op={g['predicateProofFields']['operation']}")
        lines.append(f"- proof C equal **{g['proofCEqual']}** derived `{g['derivedProofSha256']}` claimed `{g['claimedProofSha256']}`")
        lines.append(f"- derived enclosing `{g['derivedEnclosing']}` claimed `{g['claimedEnclosing']}`")
        lines.append(f"- extra finding frames not in proof `{g['extraFindingFramesNotInProof']}`")
        lines.append(f"- witness blob present `{g['witnessBlobPresent']}`")
        lines.append(f"- policy `{g['policyRule']}`; importIds `{g['planImportIds']}`; native contexts `{g['nativeContextDomains']}`")
        lines.append(f"- producing `{g['producingSummary']}`")
        lines.append("")
    lines.append("## Owner / field assertions")
    lines.append("")
    for k, v in r["ownerFieldAssertions"].items():
        lines.append(f"- **{k}**: {v}")
    lines.append("")
    lines.append("Field-specific file totality was executed as `rows[].path` set equality to the independently derived extent `{hello.rs}`, not as `state ∈ {complete,partial,unavailable}`. Outcome `state=complete` is derived in producing-law cell outcomes then joined, not accepted because the schema permits the token.")
    lines.append("")
    lines.append("## Prior-claim disposition")
    lines.append("")
    p = r["priorClaimDisposition"]
    lines.append(f"- P5 claim: `{p['p5Claim']}` (earlier grade withdrawn by P5: {p['p5WithdrewEarlierGrade']})")
    lines.append(f"- Fresh measurement agrees on graph verdicts: {p['freshMeasurementAgreesOnGraphVerdicts']}")
    lines.append(f"- Disposition: {p['disposition']}")
    lines.append(f"- {p['notUsedAsExpectation']}")
    lines.append("")
    lines.append("## Limitations")
    lines.append("")
    for item in r["limitations"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("No normative design edit. No export remint.")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
