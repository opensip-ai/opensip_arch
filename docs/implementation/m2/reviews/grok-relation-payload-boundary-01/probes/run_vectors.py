"""Bounded relation-payload vectors using the selected identity model and current schema bytes.

Does not mint native ADMIT, ReplayedRun, or a caller-chosen registry.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import sys
import unicodedata
from pathlib import Path

if not sys.flags.isolated:
    raise SystemExit("need isolated python")

REVIEW = Path("/tmp/opensip-implementation/m2-grok-relation-payload-boundary-01/review")
FOUND = REVIEW / "overlay" / "docs" / "coop" / "design-corrections" / "foundation"
LIVE = Path("/Users/sb/code/opensip-ai/opensip")
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
MODEL = FOUND / "identity_model.py"
HEX = "a" * 64
SID = "sym:main"
TEXT = "name"
PATH = "src/a.ts"
U1 = "u" * 64
U2 = "v" * 64
SHA = "sha256:" + HEX
DOC = "foundation/relation-payload-schemas.v2.json"
ANCHOR = {"path": PATH, "blobDigest": HEX, "startByte": 0, "endByte": 1}


def pin(p: Path) -> dict:
    b = p.read_bytes()
    return {"path": str(p), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}


def load_model():
    spec = importlib.util.spec_from_file_location("selected_identity_model", MODEL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def extract_anchor_law(mod):
    tree = ast.parse(MODEL.read_text())
    parent = next(
        n
        for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name == "open_run_closure"
    )
    fn = next(
        n
        for n in parent.body
        if isinstance(n, ast.FunctionDef) and n.name == "anchor_law"
    )
    ns = {"C": mod.C}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), str(MODEL), "exec"), ns)
    return ns["anchor_law"]


def extract_pure_payload_rules(mod, anchor_law):
    """Actual relation_payload_rules statements minus native/source owner calls."""
    tree = ast.parse(MODEL.read_text())
    parent = next(
        n
        for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name == "open_run_closure"
    )
    fn = next(
        n
        for n in parent.body
        if isinstance(n, ast.FunctionDef) and n.name == "relation_payload_rules"
    )
    body = []
    for stmt in fn.body:
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
            func = stmt.value.func
            if isinstance(func, ast.Name) and func.id in (
                "syntax_capability_supported",
                "relation_source_joins",
            ):
                continue
        body.append(stmt)
    fn2 = ast.FunctionDef(
        name="pure_relation_payload_rules",
        args=fn.args,
        body=body,
        decorator_list=[],
        returns=fn.returns,
        type_params=[],
    )
    ast.fix_missing_locations(fn2)
    ns = {"C": mod.C, "unicodedata": unicodedata, "anchor_law": anchor_law}
    exec(compile(ast.Module(body=[fn2], type_ignores=[]), str(MODEL), "exec"), ns)
    return ns["pure_relation_payload_rules"]


def fact(relation, resolution, payload_ok=True, anchors=None, source=U1, target=U1, extra=None):
    row = {
        "relation": relation,
        "resolution": resolution,
        "sourceUniverse": source,
        "targetUniverse": target,
        "anchors": [] if anchors is None else anchors,
        "snapshotId": "snapshot2:" + HEX,
        "payloadSchemaDigest": HEX,
    }
    if extra:
        row.update(extra)
    return row


def payloads():
    return {
        ("calls", "syntactic-callee-name"): {"caller": SID, "calleeText": TEXT},
        ("calls", "resolved-callee"): {
            "caller": SID,
            "calleeText": TEXT,
            "resolvedCallee": "sym:other",
        },
        ("clones", "normalized-body-hash"): {
            "bodyIdentity": SHA,
            "normalisationLevel": "L0-verbatim",
            "normalisationVersion": HEX,
        },
        ("control-flow", "syntactic"): {
            "edgeKind": "return",
            "from": SID,
            "to": "sym:x",
        },
        ("declares", "syntactic"): {
            "container": SID,
            "declarationKind": "function",
            "declared": "sym:f",
        },
        ("file", "enumerated"): {
            "path": PATH,
            "contentSha256": HEX,
            "byteLength": 1,
        },
        ("imports", "syntactic-specifier"): {"importer": SID, "specifier": TEXT},
        ("imports", "resolved-target"): {
            "importer": SID,
            "specifier": TEXT,
            "resolvedTarget": "sym:t",
        },
        ("literal", "syntactic"): {
            "literalKind": "string",
            "owner": SID,
            "valueText": TEXT,
        },
        ("package", "manifest-declared"): {
            "manifestPath": "package.json",
            "packageName": TEXT,
            "packageVersion": "1.0.0",
        },
        ("reachability", "from-resolved-calls"): {
            "origin": SID,
            "reachable": "sym:x",
        },
        ("references", "syntactic-name-match"): {"name": TEXT, "referrer": SID},
        ("references", "resolved-binding"): {
            "name": TEXT,
            "referrer": SID,
            "resolvedBinding": "sym:b",
        },
        ("types", "annotated"): {"subject": SID, "typeText": TEXT},
        ("types", "checked"): {
            "subject": SID,
            "typeText": TEXT,
            "checkedType": "sym:T",
        },
        ("unresolved-edge", "observed"): {
            "detail": "",
            "edgeKind": "dynamic-import-nonliteral",
            "referrer": SID,
            "relation": "imports",
            "targetModule": None,
            "targetScope": "unknown",
        },
        ("vcs-change", "vcs-reported"): {"changeKind": "modified", "path": PATH},
    }


def anchors_for(row):
    law = row["anchorLaw"]
    if law.get("cardinality") == 0:
        return []
    if law.get("cardinality") == 1:
        return [ANCHOR]
    return [ANCHOR]


def run_case(mod, pure, value, row, f):
    steps = []
    try:
        mod.validate_registered_record(DOC, row["selector"], value)
        steps.append("schema")
    except Exception as exc:
        return {"ok": False, "stop": "schema", "error": type(exc).__name__ + ":" + str(exc), "steps": steps}
    try:
        pure(value, row, f)
        steps.append("pure-payload-rules")
        return {"ok": True, "stop": None, "error": None, "steps": steps}
    except mod.C.AdmissionError as exc:
        return {"ok": False, "stop": "pure-payload-rules", "error": str(exc), "steps": steps}


def main() -> None:
    pins = {
        "identityModel": pin(
            ARCH
            / "docs/implementation/m2/recognition-derived-reference-selection-v1/reference/identity_model.py"
        ),
        "overlayModel": pin(MODEL),
        "canonical": pin(FOUND / "canonical.py"),
        "relation": pin(FOUND / "relation-payload-schemas.v2.json"),
        "liveRelation": pin(LIVE / "schemas/sources/relation-payload-v2.schema.json"),
        "identityV3": pin(FOUND / "identity-schemas.v3.json"),
        "liveIdentityV3": pin(LIVE / "schemas/sources/identity-v3.schema.json"),
    }
    assert pins["overlayModel"]["sha256"] == pins["identityModel"]["sha256"]
    assert pins["relation"]["sha256"] == pins["liveRelation"]["sha256"]
    assert pins["identityV3"]["sha256"] == pins["liveIdentityV3"]["sha256"]
    assert pins["identityModel"]["sha256"] == (
        "619d6e3cf49d0cd58967688e35c1598c92eaeb32b95fd30bb67f634271c141e6"
    )
    assert pins["relation"]["sha256"] == (
        "53380a2455490e07028e1872557044fb1b69d062143deeeec0f44006f0b2be9a"
    )
    assert pins["canonical"]["sha256"] == (
        "ad88e58fe90fe66531dbe39f4694f20ad3bc6ce2099ae4fc762c0251468496f7"
    )
    assert pins["identityV3"]["sha256"] == (
        "311c1feb09ff8cd0b207233d2ec0d7440bb1c72fc0470de277ee1891c24bb68f"
    )

    mod = load_model()
    assert mod.RELATION_SCHEMA_DOCUMENT == DOC
    assert hashlib.sha256((FOUND / "relation-payload-schemas.v2.json").read_bytes()).hexdigest() == pins[
        "relation"
    ]["sha256"]
    names = list(mod.RELATIONS)
    assert names == [
        "calls",
        "clones",
        "control-flow",
        "declares",
        "file",
        "imports",
        "literal",
        "package",
        "reachability",
        "references",
        "types",
        "unresolved-edge",
        "vcs-change",
    ]
    closures = {}
    for name in names:
        row = mod.relation_annotation_closure(name)
        closures[name] = {
            "selector": row["selector"],
            "universeRule": row["universeRule"],
            "ladder": row["ladder"],
            "rungs": row["rungs"],
            "subjectKind": row["subjectKind"],
            "anchorLaw": row["anchorLaw"],
            "snapshotJoins": row.get("snapshotJoins") or [],
            "bodyIdentityJoin": bool(row.get("bodyIdentityJoin")),
            "coverageTotality": row.get("coverageTotality"),
            "inheritedRequired": row["inheritedRequired"],
            "inheritedOptional": row["inheritedOptional"],
        }
        # registry_row relation branch: unregistered vs closed
        assert name in mod.RELATIONS

    unregistered = None
    try:
        if "not-a-relation" not in mod.RELATIONS:
            unregistered = "PAYLOAD_RELATION_UNREGISTERED"
        mod.relation_annotation_closure("not-a-relation")
        unregistered_error = "UNEXPECTED_SUCCESS"
    except KeyError as exc:
        unregistered_error = "KeyError:" + str(exc)
    except mod.C.AdmissionError as exc:
        unregistered_error = str(exc)

    anchor_law = extract_anchor_law(mod)
    pure = extract_pure_payload_rules(mod, anchor_law)
    built = payloads()
    vectors = []

    # Happy path: every closed rung.
    for name, info in closures.items():
        for rung in info["ladder"]:
            key = (name, rung)
            value = built[key]
            f = fact(name, rung, anchors=anchors_for(info))
            result = run_case(mod, pure, value, info, f)
            vectors.append(
                {
                    "id": f"{name}@{rung}:schema-rung-universe-anchor",
                    "relation": name,
                    "rung": rung,
                    "kind": "positive-pure",
                    "payload": value,
                    "universe": {"source": U1, "target": U1},
                    "anchorCount": len(f["anchors"]),
                    **result,
                }
            )

    # Cross-relation rung (the ladder-vs-rungs defect class).
    declares = closures["declares"]
    value = built[("declares", "syntactic")]
    f = fact("declares", "resolved-callee", anchors=anchors_for(declares))
    vectors.append(
        {
            "id": "declares@resolved-callee:foreign-rung",
            "relation": "declares",
            "rung": "resolved-callee",
            "kind": "negative-pure",
            "expect": "RELATION_RUNG_NOT_IN_LADDER",
            **run_case(mod, pure, value, declares, f),
        }
    )

    # Weak-rung forbidden field.
    calls = closures["calls"]
    weak = dict(built[("calls", "syntactic-callee-name")])
    weak["resolvedCallee"] = "sym:other"
    f = fact("calls", "syntactic-callee-name", anchors=anchors_for(calls))
    vectors.append(
        {
            "id": "calls@syntactic-callee-name:forbidden-resolvedCallee",
            "relation": "calls",
            "rung": "syntactic-callee-name",
            "kind": "negative-pure",
            "expect": "RELATION_RUNG_FORBIDDEN_FIELD",
            **run_case(mod, pure, weak, calls, f),
        }
    )

    # Strong-rung missing required field: schema may refuse first (optional field omitted).
    strong = {"caller": SID, "calleeText": TEXT}
    f = fact("calls", "resolved-callee", anchors=anchors_for(calls))
    vectors.append(
        {
            "id": "calls@resolved-callee:missing-resolvedCallee",
            "relation": "calls",
            "rung": "resolved-callee",
            "kind": "negative-pure",
            "expect": "RELATION_RUNG_REQUIRED_FIELD or schema",
            **run_case(mod, pure, strong, calls, f),
        }
    )

    # same-only universe mismatch (file).
    file_row = closures["file"]
    value = built[("file", "enumerated")]
    f = fact("file", "enumerated", anchors=[], source=U1, target=U2)
    vectors.append(
        {
            "id": "file@enumerated:same-only-mismatch",
            "relation": "file",
            "rung": "enumerated",
            "kind": "negative-pure",
            "expect": "RELATION_UNIVERSE_RULE:same-only",
            **run_case(mod, pure, value, file_row, f),
        }
    )

    # admitted-target mismatch is NOT refused by pure rules.
    imports = closures["imports"]
    value = built[("imports", "syntactic-specifier")]
    f = fact("imports", "syntactic-specifier", anchors=anchors_for(imports), source=U1, target=U2)
    vectors.append(
        {
            "id": "imports@syntactic-specifier:admitted-target-not-checked-here",
            "relation": "imports",
            "rung": "syntactic-specifier",
            "kind": "limit-pure-does-not-check-admitted-target",
            "universeRule": "admitted-target",
            **run_case(mod, pure, value, imports, f),
        }
    )

    # inventory anchors forbidden.
    f = fact("file", "enumerated", anchors=[ANCHOR])
    vectors.append(
        {
            "id": "file@enumerated:inventory-anchor-forbidden",
            "relation": "file",
            "rung": "enumerated",
            "kind": "negative-pure",
            "expect": "FACT_ANCHOR_CARDINALITY",
            **run_case(mod, pure, built[("file", "enumerated")], file_row, f),
        }
    )

    # source-text unanchored.
    f = fact("declares", "syntactic", anchors=[])
    vectors.append(
        {
            "id": "declares@syntactic:unanchored-source-text",
            "relation": "declares",
            "rung": "syntactic",
            "kind": "negative-pure",
            "expect": "FACT_ANCHOR_CARDINALITY",
            **run_case(mod, pure, built[("declares", "syntactic")], declares, f),
        }
    )

    # clones wrong cardinality.
    clones = closures["clones"]
    f = fact("clones", "normalized-body-hash", anchors=[])
    vectors.append(
        {
            "id": "clones@normalized-body-hash:zero-anchors",
            "relation": "clones",
            "rung": "normalized-body-hash",
            "kind": "negative-pure",
            "expect": "FACT_ANCHOR_CARDINALITY",
            **run_case(mod, pure, built[("clones", "normalized-body-hash")], clones, f),
        }
    )

    # NFC refusal.
    bad = dict(built[("declares", "syntactic")])
    bad["container"] = "sym:" + "e\u0301"
    f = fact("declares", "syntactic", anchors=anchors_for(declares))
    vectors.append(
        {
            "id": "declares@syntactic:not-nfc",
            "relation": "declares",
            "rung": "syntactic",
            "kind": "negative-pure",
            "expect": "RELATION_PAYLOAD_NOT_NFC or schema",
            **run_case(mod, pure, bad, declares, f),
        }
    )

    # negative integer (file byteLength). Schema UInt64 also refuses.
    neg = dict(built[("file", "enumerated")])
    neg["byteLength"] = -1
    f = fact("file", "enumerated", anchors=[])
    vectors.append(
        {
            "id": "file@enumerated:negative-byteLength",
            "relation": "file",
            "rung": "enumerated",
            "kind": "negative-pure",
            "expect": "schema or RELATION_PAYLOAD_NEGATIVE_INTEGER",
            **run_case(mod, pure, neg, file_row, f),
        }
    )

    # vcs deleted still zero anchors; path not inventoried is owner remaining.
    vcs = closures["vcs-change"]
    deleted = {"changeKind": "deleted", "path": PATH}
    f = fact("vcs-change", "vcs-reported", anchors=[])
    vectors.append(
        {
            "id": "vcs-change@vcs-reported:deleted-pure",
            "relation": "vcs-change",
            "rung": "vcs-reported",
            "kind": "positive-pure-owner-unless-remaining",
            **run_case(mod, pure, deleted, vcs, f),
        }
    )

    owner = []
    for name, info in closures.items():
        owner.append(
            {
                "relation": name,
                "syntaxCapabilitySupported": "native syntax-universe grammar capability; no-op if sourceUniverse is not a syntax universe",
                "snapshotJoins": info["snapshotJoins"],
                "bodyIdentityJoin": info["bodyIdentityJoin"],
                "admittedTargetUniverse": info["universeRule"] == "admitted-target",
                "coverageTotality": info["coverageTotality"] is not None,
                "pureDoesNotEstablishNativeEvidence": True,
            }
        )

    positives = [v for v in vectors if v.get("ok") and v["kind"].startswith("positive")]
    negatives = [v for v in vectors if v["kind"].startswith("negative")]
    out = {
        "pins": pins,
        "relationCount": len(names),
        "names": names,
        "closures": closures,
        "unregistered": {
            "name": "not-a-relation",
            "inRelations": False,
            "registryRowWouldRefuse": unregistered,
            "annotationClosure": unregistered_error,
        },
        "payloadSchemaDigestLaw": "raw SHA-256 of exact full relation document bytes",
        "payloadSchemaDigest": pins["relation"]["sha256"],
        "pureObligations": [
            "relation_annotation_closure (schema digest-law coherence)",
            "registry_row relation branch: RELATIONS membership then annotation closure",
            "validate_registered_record against row selector",
            "ladder membership (never rungs-as-ladder)",
            "anchor_law cardinality",
            "per-rung required/forbidden fields",
            "universeRule same-only",
            "NFC text and no negative integers",
        ],
        "ownerRemaining": [
            "syntax_capability_supported (native grammar capability on fact anchors/extent)",
            "relation_source_joins snapshot inventory/retained bytes/anchorPathField",
            "body_identity_join (clones: frame, universe, context, L0 recompute)",
            "universeRule admitted-target (not implemented in relation_payload_rules)",
            "coverage_inventory_totality (file@enumerated complete Coverage vs snapshot)",
            "coverage_dialect_prerequisite / coverage_source_variant_prerequisite / syntax_capability_prerequisite",
            "native context/universe frame admission and replay",
        ],
        "vectors": vectors,
        "summary": {
            "total": len(vectors),
            "positivePureOk": sum(1 for v in positives if v["ok"]),
            "positivePureFail": sum(1 for v in positives if not v["ok"]),
            "negativeRefused": sum(1 for v in negatives if not v["ok"]),
            "negativeUnexpectedOk": sum(1 for v in negatives if v["ok"]),
            "admittedTargetLimitOk": next(
                v["ok"]
                for v in vectors
                if v["id"] == "imports@syntactic-specifier:admitted-target-not-checked-here"
            ),
        },
        "ownerClassification": owner,
        "standing": "Advisory relation-payload boundary vectors. Passing pure rules is not native evidence ADMIT and not ReplayedRun.",
    }
    dest = REVIEW / "results" / "vectors.json"
    dest.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "relationCount": out["relationCount"],
                "summary": out["summary"],
                "unregistered": out["unregistered"],
                "positiveIds": [v["id"] for v in vectors if v["kind"].startswith("positive")],
                "negativeFailures": [
                    {"id": v["id"], "error": v.get("error"), "ok": v["ok"]}
                    for v in negatives
                ],
            },
            indent=2,
        )
    )
    if out["summary"]["positivePureFail"] or out["summary"]["negativeUnexpectedOk"]:
        raise SystemExit("vector expectations failed")


if __name__ == "__main__":
    main()
