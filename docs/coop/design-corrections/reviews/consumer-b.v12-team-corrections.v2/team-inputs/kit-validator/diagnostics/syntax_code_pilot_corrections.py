#!/usr/bin/env python3
"""Corrections and follow-up probes for the syntax-code pilot.

Preserves original diagnostics/syntax_code_pilot_probes.json. This file records
validator-diagnostic corrections (not repairs of the consumer graph).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from syntax_code_pilot_probes import (  # noqa: E402
    C,
    KIT,
    SNAP,
    STORE_PATH,
    admit_raw,
    load_json,
    load_store,
    parse_h_frame,
    sha256,
    PRODUCT_PREFIX,
    DOMAIN_PREFIX,
)

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/output/diagnostics")
ORIGINAL = OUT / "syntax_code_pilot_probes.json"


def validate_policy_with_registry(policy: dict) -> list:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource

    files = [
        KIT / "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json",
        KIT / "docs/coop/design-corrections/workflows/schemas/common.schema.json",
        KIT / "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json",
        KIT / "docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json",
    ]
    resources = []
    docs = {}
    for f in files:
        doc = json.loads(f.read_text())
        docs[f.name] = doc
        sid = doc.get("$id")
        if sid:
            resources.append((sid, Resource.from_contents(doc)))
    reg = Registry().with_resources(resources)
    pol = docs["policy-document.v2.schema.json"]
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": pol["$id"] + "/inline-PolicyDocumentV2",
        "$defs": pol.get("$defs", {}),
        **pol["$defs"]["PolicyDocumentV2"],
    }
    errors = []
    v = Draft202012Validator(schema, registry=reg)
    for e in v.iter_errors(policy):
        errors.append({"path": list(e.absolute_path), "message": e.message, "validator": e.validator})
    return errors


def u8pref(b: bytes) -> bytes:
    return bytes([len(b)]) + b


def main() -> int:
    orig = load_json(ORIGINAL)
    store = load_store(STORE_PATH)
    blobs = store["blobs"]
    table = store["objectTable"]
    frames = {}
    for d, b in blobs.items():
        if b.startswith(PRODUCT_PREFIX + b"\x00"):
            frames[d] = parse_h_frame(b)

    run_ids = [k for k in table if str(k).startswith("run3:")]
    run = frames[table[run_ids[0]]["digest"]]["value"]
    plan = frames[table[run["planId"]]["digest"]]["value"]
    snap = frames[table[run["snapshotId"]]["digest"]]["value"]
    ctx_d = plan["nativeContextDigests"][0]
    ctx = frames[ctx_d]["value"]
    gb = ctx["grammarBundle"]

    # Policy with registry
    policy = admit_raw(blobs[plan["policyDigest"]])
    pol_errs = validate_policy_with_registry(policy)
    policy_ok = not pol_errs

    # Independent L0 recompute from retained source bytes + derived languageVersionBinding
    hello = None
    hello_d = None
    for row in snap["sourceInventory"]:
        if row["path"] == "hello.rs":
            hello_d = row["sha256"]
            hello = blobs[hello_d]
    spec = blobs[gb["normalizer"]["specificationDigest"]]
    blv = {
        "schemaVersion": 1,
        "languageId": "rust",
        "compilerName": gb["parserName"],
        "compilerVersion": gb["parserVersion"],
        "compilerBuild": gb["bundleDigest"],
        "dialect": {"grammarVariant": "rs"},
    }
    lv = hashlib.sha256(C(blv)).digest()
    l0_payload = len(hello).to_bytes(4, "big") + hello
    pre = (
        u8pref(b"opensip.fact-identity.v1")
        + u8pref(b"L0-verbatim")
        + u8pref(hashlib.sha256(spec).digest())
        + u8pref(b"rust")
        + u8pref(lv)
        + len(l0_payload).to_bytes(4, "big")
        + l0_payload
    )
    recomputed_l0 = "sha256:" + sha256(pre)
    claimed_l0 = None
    for d, fr in frames.items():
        if fr["domain"] != "fact":
            continue
        rec = fr["value"]
        if rec.get("relation") != "clones":
            continue
        pl = admit_raw(blobs[rec["payloadDigest"]])
        if pl.get("normalisationLevel") == "L0-verbatim":
            claimed_l0 = pl.get("bodyIdentity")
    l0_match = recomputed_l0 == claimed_l0
    frame_retained = sha256(pre) in blobs

    # Declares payload values
    declares_payloads = []
    for d, fr in frames.items():
        if fr["domain"] != "fact":
            continue
        rec = fr["value"]
        if rec.get("relation") == "declares":
            declares_payloads.append(admit_raw(blobs[rec["payloadDigest"]]))

    # Consumer schemaChecks omit DeclaresPayloadV1
    meta = json.loads((SNAP / "runs" / "syntax-code.meta.json").read_text())
    labels = [c["label"] for c in meta.get("schemaChecks") or []]

    corrections = [
        {
            "id": "D-CORR-1-policy-schema-unresolvable-ref",
            "originalProbe": "schema-policy",
            "originalResult": "FAIL Unresolvable urn:opensip:product-v1:workflows:common#/$defs/CanonicalIdentifier",
            "correction": "Validator stock validator did not attach the workflow common/imported-evidence $id registry. Re-ran PolicyDocumentV2 against identity-and-evidence §3 owning schema with those documents registered.",
            "correctedOk": policy_ok,
            "errors": pol_errs[:6],
            "selector": "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json#/$defs/PolicyDocumentV2 plus $id registry common.schema.json and imported-evidence.schema.json",
            "standing": "diagnostic correction; not a consumer-graph repair",
        },
        {
            "id": "D-CORR-2-seven-languages-not-first-refusal",
            "originalProbe": "installed-bundle-seven-languages",
            "originalResult": "FAIL langs=['rust'] recorded as firstRefusal because it was the first closure-class fail in script order",
            "correction": "SyntaxGrammarBundleV1.grammars has minItems 1 and a closed languageId enum of seven values; native-evidence.md §1.2 states the product HOST bundles seven languages. No exact admission selector was reconstructed that refuses a synthetic kind=grammar component whose grammars array is a non-empty subset. Reclassified from first actual refusal to further static observation / algorithm-freedom vs product-host bundle. selectedGrammarIds⊆bundle still independently enforced.",
            "correctedClass": "further-static-observation",
            "notFirstRefusal": True,
            "selector": "native-evidence.schemas.v2.json#/$defs/SyntaxGrammarBundleV1 grammars minItems 1; native-evidence.md §1.2 host-bundled seven languages",
            "standing": "diagnostic correction of first-refusal ordering, not a consumer-graph repair",
        },
    ]

    followups = [
        {
            "name": "policy-schema-with-workflow-registry",
            "ok": policy_ok,
            "selector": "policy-document.v2.schema.json#/$defs/PolicyDocumentV2 with common+imported-evidence $id registry",
            "detail": {"nErrors": len(pol_errs), "errors": pol_errs[:6]},
        },
        {
            "name": "independent-L0-bodyIdentity-from-derived-languageVersionBinding",
            "ok": l0_match,
            "selector": "identity-and-evidence.md §3 clones L0 payload double length-prefix; identity-schemas.v3.json syntax languageVersionBinding compilerName/parserName, compilerVersion/parserVersion, compilerBuild/bundleDigest, dialect.grammarVariant from .rs suffix",
            "detail": {
                "recomputed": recomputed_l0,
                "claimed": claimed_l0,
                "equal": l0_match,
                "frameRetainedUnderSuffix": frame_retained,
                "derivedBlv": blv,
                "note": "Recipe match is not frame retention. The framed preimage is still absent from the store under the 64-hex suffix.",
            },
        },
        {
            "name": "consumer-schemaChecks-omit-DeclaresPayloadV1",
            "ok": "decl_payload" not in labels and "declares_payload" not in labels,
            "selector": "requirements.json R-VALIDATE-OWNING-SCHEMA every record of a claimed complete positive; consumer meta.schemaChecks has file_payload and cl0_payload but no DeclaresPayloadV1",
            "detail": {"labels": labels, "declaresPayloads": declares_payloads},
        },
    ]

    # Reconstruct first actual refusal after corrections
    first_actual = {
        "name": "grammar-artifacts-in-closure-tree",
        "order": "After H-frame parse (pass) and identity-record stock+order schema (pass), identity-and-evidence.md §3 requires Run closure to re-run native context admission over retained bytes. native-evidence.md §1.2 requires every grammar definition, the bundle manifest and the normalizer specification present in the retained kind=grammar closure tree. Observed: tree contains bin/grammar stub and grammars/rust.bin; bundleDigest and normalizer.specificationDigest are retained as blobs but are not members of closure.tree.",
        "selector": "native-evidence.md §1.2; identity-and-evidence.md §3 native context admission entryPoint admit_native_context; identity-schemas.v3.json domainSets native.context.syntax.v2 closureJoins",
        "class": "closure",
    }

    further = [
        {
            "name": "schema-payload-declares SubjectIdV1",
            "selector": "relation-payload-schemas.v2.json#/$defs/DeclaresPayloadV1 container/declared $ref SubjectIdV1 pattern ^[a-z][a-z0-9-]*:[^\\u0000-\\u001f\\u007f-\\u009f]+$",
            "observed": declares_payloads,
        },
        {
            "name": "clones bodyIdentity frames not retained",
            "selector": "identity-and-evidence.md §3 The frame itself is retained under that 64-hex suffix",
        },
        {
            "name": "invented syntax-only unit with unitOrdinal 0",
            "selector": "native-evidence.md §1.2 unitOrdinal null under U-4",
        },
        {
            "name": "ENUMERATION_INVENTORY_MISSING_RECORD",
            "selector": "enumeration-contract.v1.md §4",
        },
        {
            "name": "fresh-process complete proof replay omitted",
            "selector": "evaluator-composition-contract.v3.md §7; R-REPLAY-AFTER-ADMISSION; R-REPLAY-COMPARE-BUNDLE",
        },
    ]

    doc = {
        "originalResultsPath": str(ORIGINAL),
        "originalFailCount": orig["failCount"],
        "originalFirstRefusal": orig["firstRefusal"],
        "corrections": corrections,
        "followupProbes": followups,
        "reconstructedFirstActualRefusal": first_actual,
        "furtherIndependentStaticOmissions": further,
        "counterfactualBoundaries": [
            "Real compiler/parser/normalizer execution, OS, crypto, SQLite, and host authentication were not performed (futureQualification F-OS-COMPILER-CRYPTO-SQLITE / F-AUTH-HOST).",
            "A rust-only SyntaxGrammarBundleV1 is schema-admissible (minItems 1). Whether a product host must still ship the seven-language BUNDLED_GRAMMARS table is a product-host property, not reconstructed as a Run-closure MUST for this synthetic component.",
        ],
    }
    outp = OUT / "syntax_code_pilot_corrections.json"
    outp.write_text(json.dumps(doc, indent=2) + "\n")
    print(json.dumps({
        "policyOk": policy_ok,
        "l0Match": l0_match,
        "l0Claimed": claimed_l0,
        "l0Recomputed": recomputed_l0,
        "frameRetained": frame_retained,
        "written": str(outp),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
