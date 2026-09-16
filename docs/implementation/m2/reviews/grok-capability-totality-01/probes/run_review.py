#!/usr/bin/env python3
"""Independent capability-totality advisory probes. Not product code."""
from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
import sys
import traceback
from pathlib import Path

PY = Path("/tmp/opensip-implementation/metadata-reference-env/bin/python")
REVIEW = Path("/tmp/opensip-implementation/m2-grok-capability-totality-01/review")
ARCH_NATIVE = Path(
    "/tmp/opensip-implementation/m2-recognition-derived-fix-candidate-01/archroot"
    "/docs/coop/design-corrections/native/native_evidence_model.v2.py"
)
ARCH_ROOT = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/native/native_evidence_model.v2.py")
CANDIDATE_SRC = Path("/tmp/opensip-implementation/m2-capability-totality-candidate-01/native_evidence_model.py")
CANDIDATE_LOAD = REVIEW / "overlay/native/native_evidence_model.v2.py"
FAULTS = Path("/tmp/opensip-implementation/m2-capability-totality-candidate-01/original-reference-faults.json")
ACCOUNT = Path("/tmp/opensip-implementation/m2-capability-totality-candidate-01/account.json")
DELIVERY = Path(
    "/tmp/opensip-implementation/m2-recognition-derived-fix-candidate-01/archroot"
    "/docs/coop/artifacts/delivery.v4.json"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_model(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def bind_candidate_admit(original_module, candidate_src: str):
    """Execute only candidate admit_capability_manifest in the original module globals.

    Candidate file HERE would not resolve the native overlay; the function body is
    the sole claimed change and uses the same CAPABILITY_DOMAINS / cve1_* names.
    """
    tree = ast.parse(candidate_src)
    fns = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "admit_capability_manifest"]
    if len(fns) != 1:
        raise RuntimeError("expected one admit_capability_manifest")
    code = compile(ast.Module(body=fns, type_ignores=[]), "<candidate-admit>", "exec")
    ns = dict(original_module.__dict__)
    exec(code, ns)

    class Bound:
        cve1_encode = staticmethod(original_module.cve1_encode)
        cve1_decode = staticmethod(original_module.cve1_decode)
        admit_capability_manifest = staticmethod(ns["admit_capability_manifest"])

    return Bound()


def top_level_dump(src: str):
    tree = ast.parse(src)
    out = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out[node.name] = ast.dump(node, include_attributes=False)
    return out


def classify(exc: BaseException) -> dict:
    return {"kind": "exception", "type": type(exc).__name__, "message": str(exc)}


def run_admit(mod, raw: bytes) -> dict:
    try:
        result = mod.admit_capability_manifest(raw)
        return {"kind": "result", "result": result}
    except Exception as exc:  # noqa: BLE001 — the original defect is an unexpected exception
        return classify(exc)


def main() -> int:
    pins = {
        "archNative": {"path": str(ARCH_ROOT), "bytes": ARCH_ROOT.stat().st_size, "sha256": sha256(ARCH_ROOT)},
        "overlayNative": {"path": str(ARCH_NATIVE), "bytes": ARCH_NATIVE.stat().st_size, "sha256": sha256(ARCH_NATIVE)},
        "candidate": {"path": str(CANDIDATE_SRC), "bytes": CANDIDATE_SRC.stat().st_size, "sha256": sha256(CANDIDATE_SRC)},
        "candidateLoad": {"path": str(CANDIDATE_LOAD), "bytes": CANDIDATE_LOAD.stat().st_size, "sha256": sha256(CANDIDATE_LOAD)},
        "faults": {"path": str(FAULTS), "bytes": FAULTS.stat().st_size, "sha256": sha256(FAULTS)},
        "account": {"path": str(ACCOUNT), "bytes": ACCOUNT.stat().st_size, "sha256": sha256(ACCOUNT)},
    }
    original_src = ARCH_NATIVE.read_text()
    candidate_src = CANDIDATE_SRC.read_text()
    orig_ast = top_level_dump(original_src)
    cand_ast = top_level_dump(candidate_src)
    only_orig = sorted(set(orig_ast) - set(cand_ast))
    only_cand = sorted(set(cand_ast) - set(orig_ast))
    changed = sorted(name for name in set(orig_ast) & set(cand_ast) if orig_ast[name] != cand_ast[name])
    identical = sorted(name for name in set(orig_ast) & set(cand_ast) if orig_ast[name] == cand_ast[name])
    cve1_same = orig_ast["cve1_encode"] == cand_ast["cve1_encode"] and orig_ast["cve1_decode"] == cand_ast["cve1_decode"] and orig_ast["_cve1_read"] == cand_ast["_cve1_read"]
    identity_same = orig_ast["capability_manifest_identity"] == cand_ast["capability_manifest_identity"]
    gate_same = orig_ast["capability_manifest_gate_vectors"] == cand_ast["capability_manifest_gate_vectors"]

    original = load_model(ARCH_NATIVE, "original_native")
    candidate = bind_candidate_admit(original, candidate_src)
    delivery = json.loads(DELIVERY.read_bytes())
    recipe = next(o["value"] for o in delivery["derivedFrom"]["operations"] if o["path"] == "capabilityManifestIdentity")
    gold = bytes.fromhex(recipe["vectors"]["byId"]["DCM-1-core"]["committedBytesHex"])
    base = original.cve1_decode(gold)
    assert candidate.cve1_decode(gold) == base
    assert original.cve1_encode(base) == gold
    assert candidate.cve1_encode(base) == gold

    recorded = json.loads(FAULTS.read_bytes())
    cases = [("golden", base)]
    for value in [None, False, True, 0, "text", []]:
        cases.append(("root-" + repr(value), value))
    for val in [False, 0, [], {}, None, ["file"]]:
        x = copy.deepcopy(base)
        x["providers"][0]["platformIds"] = ["all-supported", val]
        cases.append(("platform-" + repr(val), x))
    absent = {
        "providerId": "absent",
        "language": "rust",
        "relationIds": ["file"],
        "deficiency": "provider-unavailable",
        "coverageState": "unavailable",
    }
    for val in [False, 0, [], {}, None, ["file"]]:
        x = copy.deepcopy(base)
        a = copy.deepcopy(absent)
        a["relationIds"] = [val]
        x["coverageForAbsent"] = [a]
        cases.append(("absent-relation-" + repr(val), x))

    original_rows = []
    candidate_rows = []
    for label, value in cases:
        raw = original.cve1_encode(value)
        o = run_admit(original, raw)
        c = run_admit(candidate, raw)
        original_rows.append({"label": label, "committedHex": raw.hex(), **o})
        candidate_rows.append({"label": label, "committedHex": raw.hex(), **c})

    recorded_faults = {row["label"]: row for row in recorded["cases"]}
    independent_match = []
    for row in original_rows:
        rec = recorded_faults[row["label"]]
        if row["label"] == "golden":
            ok = row["kind"] == "result" and row["result"]["result"] == "ADMIT" and rec["result"]["result"] == "ADMIT"
            ok = ok and row["result"]["capabilityManifestId"] == rec["result"]["capabilityManifestId"]
        else:
            ok = row["kind"] == "exception" and rec.get("referenceFault") == row["type"] and rec.get("message") == row["message"]
        independent_match.append({"label": row["label"], "matchesRecordedFaults": ok})

    widened = []

    def add_wide(label, mutate):
        value = copy.deepcopy(base)
        mutate(value)
        raw = original.cve1_encode(value)
        widened.append({"label": label, "committedHex": raw.hex(), "original": run_admit(original, raw), "candidate": run_admit(candidate, raw)})

    add_wide("open-language-cobol", lambda v: v["providers"][0].__setitem__("language", "cobol"))
    add_wide("open-providerId-arbitrary", lambda v: v["providers"][0].__setitem__("providerId", "not-a-registry-member"))
    add_wide("open-schemaVersion-2", lambda v: v.__setitem__("schemaVersion", 2))
    add_wide("open-profile-other", lambda v: v.__setitem__("profile", "not-core"))
    add_wide("platform-mixed-bool", lambda v: v["providers"][0].__setitem__("platformIds", ["all-supported", False]))
    add_wide("platform-mixed-duplicate-and-bool", lambda v: v["providers"][0].__setitem__("platformIds", ["all-supported", False, "all-supported"]))
    add_wide("platform-unsorted-strings", lambda v: v["providers"][0].__setitem__("platformIds", ["linux-aarch64", "all-supported"]))
    add_wide("platform-empty", lambda v: v["providers"][0].__setitem__("platformIds", []))
    add_wide("absent-mixed-int", lambda v: v.__setitem__("coverageForAbsent", [{
        "providerId": "absent", "language": "rust", "relationIds": ["file", 0],
        "deficiency": "provider-unavailable", "coverageState": "unavailable",
    }]))
    add_wide("absent-mixed-nested-list", lambda v: v.__setitem__("coverageForAbsent", [{
        "providerId": "absent", "language": "rust", "relationIds": ["file", ["file"]],
        "deficiency": "provider-unavailable", "coverageState": "unavailable",
    }]))
    add_wide("absent-duplicate-strings", lambda v: v.__setitem__("coverageForAbsent", [{
        "providerId": "absent", "language": "rust", "relationIds": ["file", "file"],
        "deficiency": "provider-unavailable", "coverageState": "unavailable",
    }]))
    add_wide("root-extra-key", lambda v: v.__setitem__("extra", True))
    add_wide("platformIds-not-list", lambda v: v["providers"][0].__setitem__("platformIds", "all-supported"))
    add_wide("true-as-schemaVersion", lambda v: v.__setitem__("schemaVersion", True))

    open_positions = json.loads(
        (ARCH_NATIVE.parent / "capability-manifest-domains.v2.json").read_bytes()
    )["declaredOPEN"]

    out = {
        "pins": pins,
        "archEqualsOverlay": ARCH_ROOT.read_bytes() == ARCH_NATIVE.read_bytes(),
        "accountPredecessorMatches": pins["overlayNative"]["sha256"] == json.loads(ACCOUNT.read_bytes())["predecessor"]["sha256"],
        "accountCandidateMatches": pins["candidate"]["sha256"] == json.loads(ACCOUNT.read_bytes())["candidate"]["sha256"],
        "ast": {
            "onlyOriginal": only_orig,
            "onlyCandidate": only_cand,
            "changedFunctions": changed,
            "identicalFunctionCount": len(identical),
            "cve1Unchanged": cve1_same,
            "capabilityManifestIdentityUnchanged": identity_same,
            "gateVectorsUnchanged": gate_same,
            "admitCapabilityManifestChanged": "admit_capability_manifest" in changed,
        },
        "recordedCaseCount": len(recorded["cases"]),
        "independentOriginalMatchRecorded": independent_match,
        "allOriginalFaultsIndependentlyReproduced": all(r["matchesRecordedFaults"] for r in independent_match),
        "original19": original_rows,
        "candidate19": candidate_rows,
        "widened": widened,
        "declaredOPEN": open_positions,
        "goldenCandidateAdmits": candidate_rows[0]["kind"] == "result" and candidate_rows[0]["result"]["result"] == "ADMIT",
        "goldenIdUnchanged": (
            candidate_rows[0]["kind"] == "result"
            and original_rows[0]["kind"] == "result"
            and candidate_rows[0]["result"]["capabilityManifestId"] == original_rows[0]["result"]["capabilityManifestId"]
        ),
    }
    (REVIEW / "results/probes.json").write_text(json.dumps(out, indent=2, default=str) + "\n")
    summary = {
        "astChanged": changed,
        "cve1Unchanged": cve1_same,
        "originalFaultsReproduced": out["allOriginalFaultsIndependentlyReproduced"],
        "goldenCandidateAdmits": out["goldenCandidateAdmits"],
        "goldenIdUnchanged": out["goldenIdUnchanged"],
        "candidate19Exceptions": [r["label"] for r in candidate_rows if r["kind"] == "exception"],
        "openLanguage": next(w for w in widened if w["label"] == "open-language-cobol"),
        "openSchemaVersion": next(w for w in widened if w["label"] == "open-schemaVersion-2"),
        "openProfile": next(w for w in widened if w["label"] == "open-profile-other"),
    }
    print(json.dumps({
        "astChanged": changed,
        "identicalFunctions": len(identical),
        "cve1Unchanged": cve1_same,
        "originalFaultsReproduced": out["allOriginalFaultsIndependentlyReproduced"],
        "goldenCandidateAdmits": out["goldenCandidateAdmits"],
        "goldenIdUnchanged": out["goldenIdUnchanged"],
        "candidate19Exceptions": summary["candidate19Exceptions"],
        "candidate19Refuse": [
            {"label": r["label"], "refusals": r["result"]["refusals"]}
            for r in candidate_rows if r["kind"] == "result" and r["label"] != "golden"
        ],
        "open": {
            w["label"]: {
                "original": w["original"].get("type") or w["original"].get("result", {}).get("result"),
                "candidate": (w["candidate"].get("result") or {}).get("result"),
                "candidateRefusals": (w["candidate"].get("result") or {}).get("refusals"),
            }
            for w in widened
        },
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
