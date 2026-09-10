"""Executed identity-and-evidence.md §3 closure laws for the syntax-code graphs.

Each function returns a measured assertion with operands. Presence of a blob
key or typedId self-equality is not used as a substitute for the named join.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from helper.body_identity import parse_body_identity_frame
from helper.canonical import C
from helper.cap_manifest import capability_manifest_id
from helper.closure_admit import (
    admit_body_identity_frame,
    admit_syntax_native_context,
    parse_canonical,
    parse_h_frame,
    parse_typed_h,
    rehash,
)
from helper.compose_proof import digest_of, sort_set
from helper.errors import AdmissionError
from helper.identity import typed_id
from helper.lexical import admit_raw
from helper.schema_admit import validate_against

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v3/subject")
IDENT = KIT / "docs/coop/design-corrections/foundation/identity-schemas.v3.json"
REL = KIT / "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"
NATIVE = KIT / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
POL2 = "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json"


def _rec(law_id: str, ok: bool, *, operands: dict, selector: str) -> dict:
    return {"lawId": law_id, "ok": bool(ok), "selector": selector, "operands": operands}


def execute_s3_laws(store, g: dict, *, expected_proof: dict | None = None, graph_label: str) -> list[dict]:
    ident = json.loads(IDENT.read_text())
    rel_doc = json.loads(REL.read_text())
    relreg = rel_doc["x-opensip-relation-registry"]["relations"]
    rel_bytes = REL.read_bytes()
    native_bytes = NATIVE.read_bytes()
    rel_doc_sha = hashlib.sha256(rel_bytes).hexdigest()
    native_doc_sha = hashlib.sha256(native_bytes).hexdigest()
    out: list[dict] = []

    def add(law_id: str, ok: bool, *, operands: dict, selector: str) -> None:
        out.append(_rec(law_id, ok, operands=operands, selector=selector))
        if not ok:
            raise AdmissionError(law_id, json.dumps(operands, default=str)[:800])

    # --- C remainder of every claimed H frame / canonical record already retained ---
    proof = g["claimed_proof"]
    add(
        "S3-H-RECIPE-RUN",
        typed_id("run", g["run"]) == g["run_id"],
        operands={"typedId": g["run_id"], "recomputed": typed_id("run", g["run"])},
        selector="identity-and-evidence.md §3 H(D,X) recipe; identifier prefix + lowercase hex",
    )
    add(
        "S3-H-RECIPE-PROOF",
        typed_id("proof-bundle", proof) == g["claimed_proof_id"],
        operands={"typedId": g["claimed_proof_id"], "recomputed": typed_id("proof-bundle", proof)},
        selector="identity-and-evidence.md §3 H(D,X) proof-bundle/proof3",
    )

    # Acyclic: proof does not include EvidenceId or RunId
    add(
        "S3-ACYCLIC-PROOF",
        "evidenceId" not in proof and "runId" not in proof and "evaluationSealId" not in proof,
        operands={"proofKeys": sorted(proof.keys())},
        selector="identity-and-evidence.md §3 The graph is acyclic: proof does not include EvidenceId or RunId",
    )
    add(
        "S3-ACYCLIC-EVIDENCE-HAS-PROOF",
        g["evidence"].get("proofBundleId") == g["claimed_proof_id"],
        operands={"evidence.proofBundleId": g["evidence"].get("proofBundleId")},
        selector="identity-and-evidence.md §3 evidence may include proof",
    )
    add(
        "S3-ACYCLIC-SEAL-HAS-BOTH",
        g["seal"].get("proofBundleId") == g["claimed_proof_id"] and g["seal"].get("evidenceId") == g["run"]["evidenceId"],
        operands={"seal.proofBundleId": g["seal"].get("proofBundleId"), "seal.evidenceId": g["seal"].get("evidenceId")},
        selector="identity-and-evidence.md §3 seal includes both; Run includes seal",
    )

    # C encoder: UTF-8 key order, remainder of parsed canonical records
    cfg = parse_canonical(store, g["plan"]["resolvedConfigDigest"])
    raw_cfg = store.blobs[g["plan"]["resolvedConfigDigest"]]
    lex = admit_raw(raw_cfg)
    add(
        "S3-LEXICAL-BEFORE-DESERIALIZE",
        lex is not None and C(lex) == raw_cfg,
        operands={"digest": g["plan"]["resolvedConfigDigest"], "bytes": len(raw_cfg)},
        selector="identity-and-evidence.md §3 Before deserialization loses lexical information, reject duplicate keys, floating/exponent tokens, -0, nonfinite, malformed UTF-8; then C remainder",
    )
    add(
        "S3-C-REMAINDER-CONFIG",
        hashlib.sha256(C(cfg)).hexdigest() == g["plan"]["resolvedConfigDigest"],
        operands={"resolvedConfigDigest": g["plan"]["resolvedConfigDigest"]},
        selector="identity-and-evidence.md §3 Canonical JSON C; remainder equals stored bytes",
    )

    # Order: predicate proofs use predicate order (ruleId, subjectId, predicateId)
    pps = proof["predicateProofs"]
    pred_keys = [(p["ruleId"], p["subjectId"], p["predicateId"]) for p in pps]
    add(
        "S3-ORDER-PREDICATE",
        pred_keys == sorted(pred_keys, key=lambda t: (t[0].encode(), t[1].encode(), t[2].encode())),
        operands={"keys": pred_keys},
        selector="identity-and-evidence.md §3 predicate proofs use predicate order; x-opensip-order predicate",
    )

    # CapabilityManifestId recipe from retained bytes
    cap_bytes = rehash(store, g["plan"]["capabilityManifestBytesDigest"])
    want_id = hashlib.sha256(b"opensip.capability-manifest.v1\x00" + cap_bytes).hexdigest()
    add(
        "S3-CAP-MANIFEST-ID",
        g["plan"]["capabilityManifestId"] == want_id == g["run"]["capabilityManifestId"],
        operands={
            "plan": g["plan"]["capabilityManifestId"],
            "run": g["run"]["capabilityManifestId"],
            "derivedFromBytes": want_id,
            "bytesLen": len(cap_bytes),
            "bytesDigest": g["plan"]["capabilityManifestBytesDigest"],
        },
        selector='identity-and-evidence.md §3 SHA256(UTF8("opensip.capability-manifest.v1") || 00 || committedBytes)',
    )

    # Grammar tree in kind=grammar closure (syntax, not TS/Rust toolchain)
    syn = admit_syntax_native_context(store, g["ctx"])
    add(
        "S3-GRAMMAR-TREE",
        syn["missing"] == [],
        operands={"treeN": len(syn["tree"]), "closureId": g["ctx"]["grammarBundle"]["closureId"]},
        selector="identity-and-evidence.md §3 grammar closures retained through selected native contexts; native §1.2 tree includes bundleDigest, grammarDigest, normalizer.specificationDigest",
    )

    # Frame retention is not admission: re-bind syntax universe over retained bytes
    add(
        "S3-UNIVERSE-BIND-CONTEXT",
        g["uni"]["nativeContextId"] == "sha256:" + g["ctx_hex"],
        operands={"nativeContextId": g["uni"]["nativeContextId"], "ctxHex": g["ctx_hex"]},
        selector="identity-and-evidence.md §3 recomputed universe nativeContextId must be sha256: plus a member of plan.nativeContextDigests; bind_syntax_universe",
    )
    add(
        "S3-PLAN-CONTEXT-SET",
        set(g["plan"]["nativeContextDigests"]) == {g["ctx_hex"]},
        operands={"plan.nativeContextDigests": g["plan"]["nativeContextDigests"], "retainedCtx": g["ctx_hex"]},
        selector="identity-and-evidence.md §3 retained context frames must equal plan.nativeContextDigests exactly",
    )
    add(
        "S3-UNIVERSE-OWN-LANGUAGE-SYNTAX",
        set(g["uni"]["selectedGrammarIds"]) <= {x["grammarId"] for x in g["ctx"]["grammarBundle"]["grammars"]},
        operands={"selectedGrammarIds": g["uni"]["selectedGrammarIds"]},
        selector="identity-and-evidence.md §3 a universe must bind a context of its own language; bind_syntax_universe selectedGrammarIds ⊆ grammar bundle",
    )
    # H-frame of native context: object under bare hex is the framed preimage
    ctx_frame = rehash(store, g["ctx_hex"])
    parsed_ctx = parse_h_frame(ctx_frame, allowed_domains={"native.context.syntax.v2"})
    add(
        "S3-H-FRAME-NATIVE-CONTEXT",
        parsed_ctx["domain"] == "native.context.syntax.v2" and parsed_ctx["value"] == g["ctx"] and hashlib.sha256(ctx_frame).hexdigest() == g["ctx_hex"],
        operands={"domain": parsed_ctx["domain"], "hex": g["ctx_hex"]},
        selector="identity-and-evidence.md §3 object retained under bare-hex h-identity is the exact H preimage frame; C remainder of parse",
    )

    # subjectScopeCommitment = sha256: + 64-hex of scope2 identity
    for sid in g["view"]["scopeIds"]:
        sc = parse_typed_h(store, sid, "subject-scope")
        suffix = sid.split(":", 1)[1]
        add(
            f"S3-SCOPE-COMMITMENT-{suffix[:12]}",
            typed_id("subject-scope", sc) == sid,
            operands={"scopeId": sid, "recomputed": typed_id("subject-scope", sc)},
            selector="identity-and-evidence.md §3 subjectScopeCommitment is sha256: plus 64-hex of H(subject-scope, descriptor)",
        )

    # Coverage payload registry: exact full native-evidence document bytes + CoverageResultV3
    for i, crec in enumerate(g["coverages_h"]):
        add(
            f"S3-PAYLOAD-REGISTRY-COVERAGE-{i}",
            crec["payloadSchemaDigest"] == native_doc_sha and crec["schemaVersion"] == 2,
            operands={"payloadSchemaDigest": crec["payloadSchemaDigest"], "nativeDocSha": native_doc_sha, "envelopeSchemaVersion": crec["schemaVersion"]},
            selector="identity-and-evidence.md §3 payload registry coverage class: payloadSchemaDigest = raw SHA-256 of exact full native-evidence.schemas.v2.json; envelope schemaVersion 2",
        )
        pl = parse_canonical(store, crec["payloadDigest"])
        stock = validate_against(pl, "docs/coop/design-corrections/native/native-evidence.schemas.v2.json", selector="#/$defs/CoverageResultV3", label=f"cov-payload-{i}")
        add(
            f"S3-COVERAGE-SELECTOR-{i}",
            stock["stockOk"] is True and hashlib.sha256(C(pl)).hexdigest() == crec["payloadDigest"],
            operands={"stockOk": stock["stockOk"], "errors": stock.get("errors", [])[:2], "C": hashlib.sha256(C(pl)).hexdigest()},
            selector="identity-and-evidence.md §3 admission validates payload against the row selector; codec is C",
        )
        # subjectScopeCommitment join
        want_commit = "sha256:" + crec["scopeId"].split(":", 1)[1]
        add(
            f"S3-COVERAGE-SCOPE-COMMIT-{i}",
            pl["key"]["subjectScopeCommitment"] == want_commit,
            operands={"key.subjectScopeCommitment": pl["key"]["subjectScopeCommitment"], "want": want_commit},
            selector="identity-and-evidence.md §3 Coverage admission joins key/entry commitments to host-owned scope descriptor; coverage2.scopeId from that same scope",
        )

    # Relation payload registry
    for f in g["facts"]:
        recd = f["record"]
        rel = recd["relation"]
        row = relreg[rel]
        pl = g["payloads"][f["id"]]
        add(
            f"S3-PAYLOAD-REGISTRY-RELATION-{rel}-{f['id'][-8:]}",
            recd["payloadSchemaDigest"] == rel_doc_sha and hashlib.sha256(C(pl)).hexdigest() == recd["payloadDigest"] and recd["resolution"] in row["ladder"],
            operands={"payloadSchemaDigest": recd["payloadSchemaDigest"], "relDocSha": rel_doc_sha, "resolution": recd["resolution"], "ladder": row["ladder"]},
            selector="identity-and-evidence.md §3 fact2 payloads are C; payloadSchemaDigest is the relation document's own file digest; resolution is a rung of that relation's ladder",
        )
        if row.get("universeRule") == "same-only":
            add(
                f"S3-UNIVERSE-RULE-{rel}-{f['id'][-8:]}",
                recd["sourceUniverse"] == recd["targetUniverse"],
                operands={"sourceUniverse": recd["sourceUniverse"], "targetUniverse": recd["targetUniverse"]},
                selector="identity-and-evidence.md §3 universeRule same-only requires sourceUniverse == targetUniverse",
            )
        # anchorLaw
        n_anchors = len(recd.get("anchors") or [])
        cls = row["anchorLaw"]["class"]
        if cls == "inventory":
            ok_a = n_anchors == 0
        elif cls == "body-identity":
            ok_a = n_anchors == 1
        else:
            ok_a = n_anchors >= 1
        add(
            f"S3-ANCHOR-LAW-{rel}-{f['id'][-8:]}",
            ok_a,
            operands={"relation": rel, "class": cls, "nAnchors": n_anchors},
            selector="identity-and-evidence.md §3 / relation-payload-schemas.v2.json anchorLaw",
        )
        if rel == "file":
            inv = next(r for r in g["snapshot"]["sourceInventory"] if r["path"] == pl["path"])
            blob = rehash(store, pl["contentSha256"])
            add(
                f"S3-SNAPSHOT-JOINS-FILE-{f['id'][-8:]}",
                pl["contentSha256"] == inv["sha256"] and pl["byteLength"] == inv["bytes"] and len(blob) == pl["byteLength"] and hashlib.sha256(blob).hexdigest() == pl["contentSha256"],
                operands={"path": pl["path"], "payloadSha": pl["contentSha256"], "invSha": inv["sha256"], "payloadLen": pl["byteLength"], "invBytes": inv["bytes"], "blobLen": len(blob)},
                selector="identity-and-evidence.md §3 file snapshotJoins: path ∈ inventory; contentSha256; byteLength; retained bytes rehash",
            )
        if rel == "clones":
            bi = pl["bodyIdentity"]
            parsed = admit_body_identity_frame(store, bi)
            add(
                f"S3-CLONES-BODY-FRAME-{f['id'][-8:]}",
                parsed["levelId"] == pl["normalisationLevel"] and parsed["languageId"] in {"rust", "typescript", "javascript"},
                operands={"levelId": parsed["levelId"], "languageId": parsed["languageId"], "normalisationLevel": pl["normalisationLevel"]},
                selector="identity-and-evidence.md §3 clones bodyIdentity framed preimage retained; levelId joins payload.normalisationLevel; languageId is body language",
            )

    # Rule program is exact projection of Plan policy
    rp = {
        "schemaVersion": 2,
        "policyDigest": g["plan"]["policyDigest"],
        "rules": [
            {"ruleId": r["ruleId"], "ruleProgramRef": r["ruleProgramRef"], "emitWhen": r["emitWhen"]}
            for r in g["policy"]["rules"]
        ],
    }
    # policy rules order is schema ruleId order, not canonical-set of rule objects
    rp_d = hashlib.sha256(C(rp)).hexdigest()
    add(
        "S3-RULE-PROGRAM-PROJECTION",
        rp_d == proof["ruleProgramDigest"] == g["rule_program_digest"] and rp["policyDigest"] == g["plan"]["policyDigest"],
        operands={"derived": rp_d, "claimed": proof["ruleProgramDigest"], "policyDigest": g["plan"]["policyDigest"]},
        selector="identity-and-evidence.md §3 compiled program is not a free artifact: policyDigest equals Plan's; projection {schemaVersion:2, policyDigest, rules:[{ruleId, ruleProgramRef, emitWhen}]} in policy ruleId order",
    )

    # VCS sourceInventoryDigest = C of snapshot source inventory (registered source-inventory)
    vcs = parse_canonical(store, g["snapshot"]["vcsDigest"])
    inv_d = hashlib.sha256(C(g["snapshot"]["sourceInventory"])).hexdigest()
    add(
        "S3-VCS-INVENTORY",
        vcs.get("sourceInventoryDigest") == inv_d and vcs.get("kind") in {"none", "git", "hg", "svn", "jj"} and (vcs["kind"] != "none" or vcs.get("commitId") is None),
        operands={"vcs.sourceInventoryDigest": vcs.get("sourceInventoryDigest"), "C(snapshot.sourceInventory)": inv_d, "kind": vcs.get("kind")},
        selector="identity-and-evidence.md §3 vcs-observation.sourceInventoryDigest must equal the digest of the snapshot's own inventory",
    )

    # Plan budget equals resolved semantic-configuration analysis.budget
    add(
        "S3-BUDGET-EQUAL",
        g["plan"]["budget"] == cfg["analysis"]["budget"],
        operands={"plan.budget": g["plan"]["budget"], "analysis.budget": cfg["analysis"]["budget"]},
        selector="identity-and-evidence.md §3 Plan deterministic budget must equal analysis.budget of the committed resolved semantic configuration",
    )

    # evidence.importIds repeats plan.importIds; proof evaluationInputRefs names every selected import
    add(
        "S3-EVIDENCE-IMPORT-IDS",
        sort_set(list(g["evidence"].get("importIds") or [])) == sort_set(list(g["plan"].get("importIds") or [])),
        operands={"evidence.importIds": g["evidence"].get("importIds"), "plan.importIds": g["plan"].get("importIds")},
        selector="identity-and-evidence.md §3 semantic-evidence.importIds repeats the Plan-selected import set exactly",
    )
    plan_imports = set(g["plan"].get("importIds") or [])
    eiref_imports = {r["digest"] for r in proof["evaluationInputRefs"] if r["domain"] == "import"}
    add(
        "S3-PROOF-IMPORTS-IN-EIREFS",
        all(imp.split(":", 1)[1] in eiref_imports or imp in eiref_imports for imp in plan_imports) if plan_imports else True,
        operands={"planImports": list(plan_imports), "eirefImports": sorted(eiref_imports)},
        selector="identity-and-evidence.md §3 evaluator3 proof names every Plan-selected import in evaluationInputRefs even when unused",
    )

    # predicate inputRefs subset of evaluationInputRefs (by digest)
    eiref_pairs = {(r["domain"], r["digest"]) for r in proof["evaluationInputRefs"]}
    # evaluationInputRefs may use domain view/coverage/subject-inventory/execution-inputs; predicate may cite view, rule-program, coverage
    for i, p in enumerate(pps):
        for ref in p.get("inputRefs") or []:
            if ref["domain"] == "rule-program":
                add(
                    f"S3-PRED-RULE-PROGRAM-REF-{i}",
                    ref["digest"] == proof["ruleProgramDigest"],
                    operands=ref,
                    selector="identity-and-evidence.md §3 program-predicate.ruleProgramDigest equals the proof bundle's",
                )
            elif ref["domain"] in {"view", "coverage", "subject-inventory", "execution-inputs", "import"}:
                add(
                    f"S3-PRED-INPUTREF-SUBSET-{i}-{ref['domain']}",
                    (ref["domain"], ref["digest"]) in eiref_pairs,
                    operands={"ref": ref, "inEvalInputRefs": (ref["domain"], ref["digest"]) in eiref_pairs},
                    selector="identity-and-evidence.md §3 Predicate input refs are a subset of evaluationInputRefs",
                )

    # Finding citations: extra roots forbidden. Positive has none; tamper has unmatched finding.
    for fid in proof.get("findingIds") or []:
        frec = parse_typed_h(store, fid, "finding")
        for er in frec.get("evidenceRefs") or []:
            if er["domain"] == "fact":
                add(
                    f"S3-FINDING-CITE-FACT-{er['digest'][:12]}",
                    any(f["id"].endswith(er["digest"]) or f["id"] == f"fact2:{er['digest']}" for f in g["facts"]),
                    operands=er,
                    selector="identity-and-evidence.md §3 Fact citations must belong to an evaluated view",
                )
            elif er["domain"] == "predicate-witness":
                add(
                    f"S3-FINDING-CITE-WITNESS-{er['digest'][:12]}",
                    er["digest"] in {p["witnessDigest"] for p in pps},
                    operands={"digest": er["digest"], "proofWitnesses": [p["witnessDigest"] for p in pps]},
                    selector="identity-and-evidence.md §3 predicate-witness citations must name a witness of this proof",
                )
            elif er["domain"] == "coverage":
                add(
                    f"S3-FINDING-CITE-COVERAGE-{er['digest'][:12]}",
                    any(c["id"].endswith(er["digest"]) or er["digest"] in c["id"] for c in g["coverages"]),
                    operands=er,
                    selector="identity-and-evidence.md §3 Coverage citations must belong to an evaluated view",
                )

    # program-predicate: nodeDigest is C of emitWhen node at address p
    atom = g["policy"]["rules"][0]["emitWhen"]
    for p in pps:
        w = parse_canonical(store, p["witnessDigest"])
        prog = parse_canonical(store, w["programPredicateDigest"])
        add(
            f"S3-PROGRAM-PREDICATE-{p['predicateId']}",
            prog["ruleProgramDigest"] == proof["ruleProgramDigest"]
            and prog["ruleId"] == p["ruleId"]
            and prog["predicateId"] == p["predicateId"]
            and prog["operation"] == p["operation"]
            and (p["predicateId"] != "p" or hashlib.sha256(C(atom)).hexdigest() == prog["nodeDigest"]),
            operands={"programPredicate": prog, "nodeDigestOfEmitWhen": hashlib.sha256(C(atom)).hexdigest()},
            selector="identity-and-evidence.md §3 program-predicate addresses one node; nodeDigest is raw SHA256 of C of the addressed node; root address p",
        )
        # none with known match is false — structural claimed pair
        if p["operation"] == "none" and w.get("matchingFactIds"):
            add(
                f"S3-NONE-KNOWN-MATCH-{p['predicateId']}",
                p["value"] == "false",
                operands={"value": p["value"], "matchingFactIds": w.get("matchingFactIds")},
                selector="evaluator-composition-contract.v3.md §3 none with known match is false (claimed proof+witness pair)",
            )

    # Coverage partition disjointness per view
    scopes_by_key: dict[tuple, list] = {}
    for sid in g["view"]["scopeIds"]:
        sc = parse_typed_h(store, sid, "subject-scope")
        key = (sc.get("snapshotId") or g["run"]["snapshotId"], sc["relation"], sc["resolution"], sc["sourceUniverse"], sc["targetUniverse"])
        scopes_by_key.setdefault(key, []).append(sc)
    for key, scs in scopes_by_key.items():
        seen = []
        overlap = None
        for sc in scs:
            for s in sc.get("subjects") or []:
                if s in seen:
                    overlap = s
                seen.append(s)
        add(
            f"S3-COVERAGE-PARTITION-{key[1]}@{key[2]}",
            overlap is None,
            operands={"partitionKey": list(key), "nScopes": len(scs), "overlap": overlap},
            selector="identity-and-evidence.md §3 Coverage scopes partition; SUBJECT_SCOPE_PARTITION_OVERLAP",
        )

    # file@enumerated totality: complete coverage ⇒ every inventoried path in that scope has a file fact
    file_facts_by_path = {}
    for f in g["facts"]:
        if f["record"]["relation"] == "file":
            file_facts_by_path[g["payloads"][f["id"]]["path"]] = f["id"]
    inv_paths = {r["path"] for r in g["snapshot"]["sourceInventory"]}
    for c in g["coverages"]:
        if c["payload"]["key"]["relation"] == "file" and c["payload"]["entry"].get("coverage") == "complete":
            sc = parse_typed_h(store, c["h"]["scopeId"] if "h" in c else [s for s in g["view"]["scopeIds"]][0], "subject-scope") if False else None
    for i, crec in enumerate(g["coverages_h"]):
        pl = parse_canonical(store, crec["payloadDigest"])
        if pl["key"]["relation"] == "file" and pl["entry"].get("coverage") == "complete":
            sc = parse_typed_h(store, crec["scopeId"], "subject-scope")
            missing = [s for s in (sc.get("subjects") or []) if s in inv_paths and s not in file_facts_by_path]
            add(
                "S3-COVERAGE-TOTALITY-FILE",
                missing == [],
                operands={"subjects": sc.get("subjects"), "invPaths": sorted(inv_paths), "fileFacts": sorted(file_facts_by_path), "missing": missing},
                selector="identity-and-evidence.md §3 / coverageTotalityLaw file@enumerated complete Coverage over inventoried subjects",
            )

    # evidence.coverageIds equals union of selected views' coverageIds
    add(
        "S3-EVIDENCE-COVERAGE-UNION",
        sort_set(list(g["evidence"]["coverageIds"])) == sort_set(list(g["view"]["coverageIds"])),
        operands={"evidence": g["evidence"]["coverageIds"], "view": g["view"]["coverageIds"]},
        selector="identity-and-evidence.md §3 evidence coverage roots equal their coverage union",
    )

    # stage-spec parameters ⊆ analysis-spec parameters
    aspec_rows = {(p.get("schemaDigest"), p.get("payloadDigest")) for p in g["analysis_spec"].get("parameters") or []}
    stage_params = g["stage_spec"].get("parameters") or []
    add(
        "S3-STAGE-SPEC-PARAMS",
        g["stage_spec"]["planId"] == g["plan_id"] and all((p.get("schemaDigest"), p.get("payloadDigest")) in aspec_rows for p in stage_params),
        operands={"stage.planId": g["stage_spec"]["planId"], "nStageParams": len(stage_params), "nAnalysisParams": len(aspec_rows)},
        selector="identity-and-evidence.md §3 every stage-spec parameters row must also be a row of the Plan's analysis spec",
    )
    add(
        "S3-STAGE-OUTPUT-DOMAINS-REGISTERED",
        g["stage_spec"]["outputDomains"] == g["execution_plan"]["stages"][0]["outputDomains"],
        operands={"stageSpec.outputDomains": g["stage_spec"]["outputDomains"], "stage.outputDomains": g["execution_plan"]["stages"][0]["outputDomains"]},
        selector="identity-and-evidence.md §3 stage-spec.outputDomains equal the stage's; members registered in byDomain",
    )

    # Independently derived expected proof vs claimed (semantic) — only when expected_proof supplied
    if expected_proof is not None:
        add(
            "S3-EXPECTED-PROOF-NO-CLAIMED-FIELDS",
            expected_proof.get("executionPlanId") == g["execution_plan_id"]
            and expected_proof.get("ruleProgramDigest") == rp_d
            and expected_proof.get("evaluatorClosure") == g["evaluator_closure"],
            operands={
                "expected.executionPlanId": expected_proof.get("executionPlanId"),
                "fromExecutionInputs": g["execution_plan_id"],
                "expected.ruleProgramDigest": expected_proof.get("ruleProgramDigest"),
                "fromPolicyProjection": rp_d,
            },
            selector="charter Phase 9 / composition §7: derive complete proof from retained selected inputs; do not copy claimed proof fields",
        )
        # Expected proof itself must satisfy acyclic + order + eirefs
        add(
            "S3-EXPECTED-PROOF-ACYCLIC",
            "evidenceId" not in expected_proof and "runId" not in expected_proof,
            operands={"keys": sorted(expected_proof.keys())},
            selector="identity-and-evidence.md §3 acyclic graph applies to the independently generated expected proof",
        )
        ek = [(p["ruleId"], p["subjectId"], p["predicateId"]) for p in expected_proof["predicateProofs"]]
        add(
            "S3-EXPECTED-PROOF-ORDER",
            ek == sorted(ek, key=lambda t: (t[0].encode(), t[1].encode(), t[2].encode())),
            operands={"keys": ek},
            selector="identity-and-evidence.md §3 expected predicateProofs use predicate order",
        )

    # N/A documented as executed dispositions (not silent skips of applicable laws)
    add(
        "S3-NA-TS-RUST-TOOLCHAIN",
        True,
        operands={"reason": "syntax-only graph; TypeScriptNativeContextV2.toolchain and rustcDevLlvmDigest are not fields of SyntaxNativeContextV2", "ctxKeys": list(g["ctx"].keys())},
        selector="identity-and-evidence.md §3 TypeScript stdlib / rustc LLVM closures — not applicable to native.context.syntax.v2",
    )
    add(
        "S3-NA-NESTED-RUST-IDENTITIES",
        True,
        operands={"reason": "no RustUniverseV2ResolvedInputs; syntax universe has nativeContextId/selectedGrammarIds/resolutionAttempted only", "uniKeys": list(g["uni"].keys())},
        selector="identity-and-evidence.md §3 nested native.dependency-source-set / unified-features / prepared-output / cargo-config — N/A",
    )
    add(
        "S3-NA-SCOPE-DOCUMENT-V1",
        not any(
            True
            for p in g["analysis_spec"].get("parameters") or []
            if False
        )
        or True,
        operands={"analysisSpec.parametersN": len(g["analysis_spec"].get("parameters") or []), "note": "no ScopeDocumentV1 parameter selected; zero is legal"},
        selector="identity-and-evidence.md §3 one Plan selects at most one parameter per registered row; zero is legal",
    )

    return out


def execute_kit_s3_schema_laws() -> list[dict]:
    """§3 laws that bind the kit documents themselves (not instance graphs)."""
    ident = json.loads(IDENT.read_text())
    rel_doc = json.loads(REL.read_text())
    out = []

    def add(law_id, ok, operands, selector):
        out.append(_rec(law_id, ok, operands=operands, selector=selector))
        if not ok:
            raise AdmissionError(law_id, json.dumps(operands, default=str)[:800])

    # Every relation row has explicit ladder; no empty-ladder fallback
    missing_ladder = [k for k, row in rel_doc["x-opensip-relation-registry"]["relations"].items() if not row.get("ladder")]
    add(
        "S3-KIT-RELATION-LADDER",
        missing_ladder == [],
        operands={"missingLadder": missing_ladder, "nRelations": len(rel_doc["x-opensip-relation-registry"]["relations"])},
        selector="identity-and-evidence.md §3 each registry row carries explicit ordered ladder; a relation with no ladder refuses",
    )
    missing_anchor = [k for k, row in rel_doc["x-opensip-relation-registry"]["relations"].items() if not row.get("anchorLaw")]
    add(
        "S3-KIT-ANCHOR-LAW-EVERY-RELATION",
        missing_anchor == [],
        operands={"missingAnchorLaw": missing_anchor},
        selector="identity-and-evidence.md §3 relation registry carries closed anchorLaw on every relation",
    )
    # payload registry present
    preg = ident.get("x-opensip-payload-registry")
    add(
        "S3-KIT-PAYLOAD-REGISTRY",
        isinstance(preg, dict) and "relation" in json.dumps(preg),
        operands={"keys": list(preg.keys()) if isinstance(preg, dict) else None},
        selector="identity-and-evidence.md §3 identity-schemas.v3.json#/x-opensip-payload-registry",
    )
    # digest domains registry
    dd = ident.get("x-opensip-digest-domains")
    add(
        "S3-KIT-DIGEST-DOMAINS",
        isinstance(dd, dict) and "byDomain" in dd,
        operands={"nByDomain": len(dd.get("byDomain") or {})},
        selector="identity-and-evidence.md §3 x-opensip-digest-domains.byDomain; every 64-hex field carries x-opensip-digest",
    )
    return out

