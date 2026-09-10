#!/usr/bin/env python3
"""Independent reconstruction of original phases 0–4 and R-IMPORTED-OBSERVATION-BOUNDARY.

Writes ONLY under foundation/. Does not overwrite five Run stores or
scope-v2 vectors/envelopes/traces. Assertion failures exit nonzero.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-foundation-corrections.v1/output")
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-foundation-corrections.v1/subject")
sys.path.insert(0, str(OUT))

from helper.canonical import C  # noqa: E402
from helper.cap_manifest import capability_manifest_id, first_refusal  # noqa: E402
from helper.cve1 import CLOSED_TYPES, decode, encode, round_trip  # noqa: E402
from helper.errors import AdmissionError  # noqa: E402
from helper.identity import DOMAIN_PREFIX, H, h_frame, parse_h_frame, typed_id  # noqa: E402
from helper.lexical import first_refusal as lexical_first  # noqa: E402
from helper.protocol3 import IDENTITY_TOKENS, run_trace  # noqa: E402
from helper.schema_admit import validate_against  # noqa: E402
from helper.store import Store  # noqa: E402

FOUND = OUT / "foundation"
IDENT = "docs/coop/design-corrections/foundation/identity-schemas.v3.json"
REL = "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"
NATIVE = "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
IMP = "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json"
MATRIX = KIT / "docs/coop/design-corrections/native/native-capability-matrix.v2.json"


def dump(rel: str, obj) -> Path:
    p = FOUND / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2) + "\n")
    return p


def die(msg: str) -> None:
    print("FOUNDATION_ASSERTION_FAILED", msg, file=sys.stderr)
    raise SystemExit(1)


def sha_file(p: Path) -> dict:
    b = p.read_bytes()
    return {"path": str(p.relative_to(OUT)), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}


def must_ok(rs: dict, label: str) -> dict:
    if not rs["stockOk"]:
        die(f"{label} not schema-valid {rs['errors'][:5]}")
    return rs


def freeze_check() -> dict:
    rec = json.loads((OUT / "frozen-this-pass.foundation.json").read_text())
    mismatches = []
    checked = []
    for rel, meta in {**rec["runs"], **rec["historicalSharedPaths"]}.items():
        p = OUT / rel
        b = p.read_bytes()
        h = hashlib.sha256(b).hexdigest()
        checked.append({"path": rel, "sha256": h, "bytes": len(b)})
        if h != meta["sha256"] or len(b) != meta["bytes"]:
            mismatches.append({"path": rel, "got": {"sha256": h, "bytes": len(b)}, "frozen": meta})
    if mismatches:
        die(f"frozen artifact mutated {mismatches[:3]}")
    return {"ok": True, "nChecked": len(checked)}


# ---------------------------------------------------------------------------
# Phase 0
# ---------------------------------------------------------------------------
kit_man = json.loads((KIT / "consumer-input-manifest.json").read_text())
kit_files_ok = True
for f in kit_man["files"]:
    b = (KIT / f["path"]).read_bytes()
    if hashlib.sha256(b).hexdigest() != f["sha256"] or len(b) != f["bytes"]:
        kit_files_ok = False
        die(f"kit file mismatch {f['path']}")

cve1_sel = "docs/coop/artifacts/resolved-inputs.v2.json#planIdContract.canonicalValueEncoding"
if len(CLOSED_TYPES) != 8:
    die("CVE1 closed types != 8")

five = [
    "docs/v2/contracts/product-v1/identity-and-evidence.md",
    "docs/v2/contracts/product-v1/security-and-lifecycle.md",
    "docs/v2/contracts/product-v1/native-evidence.md",
    "docs/v2/contracts/product-v1/workflows-and-surfaces.md",
    "docs/v2/contracts/product-v1/admission-and-qualification.md",
]
for rel in five:
    if not (KIT / rel).is_file():
        die(f"missing contract {rel}")

phase0 = {
    "phase": 0,
    "kind": "standingRule",
    "fiveContracts": five,
    "successorOverInherited": "Apply successor contracts where they explicitly replace an inherited selector. Unchanged native/input keep declared major2 recipes.",
    "sourceMap": "docs/coop/design-corrections/current-source-map.proposed.md — readiness/review records excluded; not used as recipes.",
    "governanceStandingNotUsedAsRecipe": True,
    "cve1TypesFromKit": list(CLOSED_TYPES),
    "cve1Selector": cve1_sel,
    "kitManifestSha256": hashlib.sha256((KIT / "consumer-input-manifest.json").read_bytes()).hexdigest(),
    "parentSubjectSha256": kit_man["parentSubjectSha256"],
    "kitFiles": {"count": len(kit_man["files"]), "pass": kit_files_ok},
}
dump("phase-0.json", phase0)

# ---------------------------------------------------------------------------
# R-H-HELPER — schema-valid snapshot, published H recipe
# ---------------------------------------------------------------------------
store = Store()
src_inv = [{"path": "src/main.ts", "sha256": "aa" * 32, "bytes": 12}]
src_inv = sorted(src_inv, key=lambda r: r["path"].encode())
inv_d = hashlib.sha256(C(src_inv)).hexdigest()
store.put_canonical(src_inv, label="source-inventory")
must_ok(validate_against(src_inv, IDENT, selector="#/$defs/source-inventory", label="source-inventory"), "source-inventory")
vcs_a = {"schemaVersion": 2, "kind": "none", "commitId": None, "dirty": False, "sourceInventoryDigest": inv_d}
vcs_b = {"schemaVersion": 2, "kind": "git", "commitId": "c" * 40, "dirty": False, "sourceInventoryDigest": inv_d}
must_ok(validate_against(vcs_a, IDENT, selector="#/$defs/vcs-observation", label="vcs-a"), "vcs-a")
must_ok(validate_against(vcs_b, IDENT, selector="#/$defs/vcs-observation", label="vcs-b"), "vcs-b")
vcs_a_d = hashlib.sha256(C(vcs_a)).hexdigest()
vcs_b_d = hashlib.sha256(C(vcs_b)).hexdigest()
scope = {"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": [], "excludedPathPrefixes": []}
must_ok(validate_against(scope, IDENT, selector="#/$defs/scope-descriptor", label="scope"), "scope")
scope_d = hashlib.sha256(C(scope)).hexdigest()
cfg = {"analysis": {"profileId": "core", "capabilities": ["inventory"], "budget": {"unit": "work-units", "limit": 1}}, "components": {}, "discovery": {}, "policy": {}, "evidence": {}}
cfg["analysis"]["capabilities"] = sorted(cfg["analysis"]["capabilities"])
must_ok(validate_against(cfg, IDENT, selector="#/$defs/semantic-configuration", label="cfg"), "cfg")
cfg_d = hashlib.sha256(C(cfg)).hexdigest()
project_id = "prj1-" + "ab" * 32
snap_a = {
    "schemaVersion": 2,
    "projectId": project_id,
    "sourceInventory": src_inv,
    "resolvedConfigDigest": cfg_d,
    "scopeDigest": scope_d,
    "vcsDigest": vcs_a_d,
}
snap_b = dict(snap_a)
snap_b["vcsDigest"] = vcs_b_d
must_ok(validate_against(snap_a, IDENT, selector="#/$defs/snapshot", label="snap-a"), "snap-a")
must_ok(validate_against(snap_b, IDENT, selector="#/$defs/snapshot", label="snap-b"), "snap-b")

h_a = H("snapshot", snap_a)
h_b = H("snapshot", snap_b)
id_a = typed_id("snapshot", snap_a)
id_b = typed_id("snapshot", snap_b)
if h_a == h_b:
    die("semantic vcsDigest change did not move snapshot H")
frame_a = h_frame("snapshot", snap_a)
parsed_a = parse_h_frame(frame_a, allowed_domains={"snapshot"})
if parsed_a["digest"] != h_a:
    die("H frame digest mismatch")
if C(parsed_a["value"]) != C(snap_a):
    die("H frame remainder not C(snapshot)")

# operational IDs are NOT snapshot/run fields
request_id = "req1_" + "cd" * 16
execution_id = "exec1_" + "ef" * 16
wall = "2026-09-08T00:00:00Z"
# same snapshot hashed again after inventing operational envelope beside it
if H("snapshot", snap_a) != h_a:
    die("rehash of same snapshot moved")

h_helper = {
    "kind": "standaloneCanonicalVector",
    "classification": "valid",
    "recipe": 'H(D,X)=SHA256(ASCII("opensip.product.v1")||00||ASCII(D)||00||uint64BE(len(C(X)))||C(X))',
    "selector": "docs/v2/contracts/product-v1/identity-and-evidence.md §3",
    "schemaSelector": "identity-schemas.v3.json#/$defs/snapshot",
    "domainPrefixMap": DOMAIN_PREFIX,
    "helperCorrection": {
        "originalFailure": "Historical h-helper snapshot used an invented sourceInventory object {schemaVersion,entries} rather than identity-schemas.v3 source-inventory (Blob array).",
        "selector": "identity-schemas.v3.json#/$defs/snapshot and #/$defs/source-inventory",
        "change": "This exhibit inhabits the published snapshot record. Historical vectors/h-helper.json is preserved unread as a shared-path scope artifact.",
    },
    "vectors": [
        {
            "name": "snapshot-A",
            "classification": "valid",
            "domain": "snapshot",
            "record": snap_a,
            "stockOk": True,
            "C_hex": C(snap_a).hex(),
            "H": h_a,
            "typedId": id_a,
            "frameSha256": hashlib.sha256(frame_a).hexdigest(),
            "frameByteLength": len(frame_a),
        },
        {
            "name": "snapshot-B-semantic-vcsDigest-change",
            "classification": "valid",
            "domain": "snapshot",
            "changedField": "vcsDigest",
            "H": h_b,
            "typedId": id_b,
            "identityMoved": h_a != h_b,
            "expectedIdentityMoved": True,
        },
        {
            "name": "operational-envelope-does-not-enter-H",
            "classification": "explanatory",
            "selector": "identity-and-evidence.md §2: RequestId/ExecutionId/wall clocks/PIDs excluded from Run identity",
            "requestId": request_id,
            "executionId": execution_id,
            "wallClock": wall,
            "H_snapshot": h_a,
            "equalsSnapshotA": True,
            "note": "These operational strings are not snapshot fields. Hashing a descriptor that illegally contains them would move identity; the recipe excludes them by omitting the fields, not by hashing-and-ignoring.",
        },
    ],
}
dump("h-helper.json", h_helper)

# ---------------------------------------------------------------------------
# R-SEMANTIC-VS-OPERATIONAL — paired measured identities on published recipes
# ---------------------------------------------------------------------------
# Run identity fields are the run descriptor, not requestId.
run_like = {
    "schemaVersion": 3,
    "projectId": project_id,
    "snapshotId": id_a,
    "planId": "plan2:" + "11" * 32,
    "evidenceId": "evidence3:" + "22" * 32,
    "evaluationSealId": "seal3:" + "33" * 32,
    "capabilityManifestId": "44" * 32,
}
must_ok(validate_against(run_like, IDENT, selector="#/$defs/run", label="run-min"), "run-min")
h_run = H("run", run_like)
run_with_illegal_ops = dict(run_like)
# additionalProperties false: cannot add requestId. Demonstrate schema refusal.
run_illegal = dict(run_like)
run_illegal["requestId"] = request_id
ril = validate_against(run_illegal, IDENT, selector="#/$defs/run", label="run-illegal-requestId")
if ril["stockOk"]:
    die("run additionalProperties should refuse requestId")

sem_vs_op = {
    "kind": "standaloneCanonicalVector",
    "selector": "identity-and-evidence.md §2–3",
    "semanticChangeMovesIdentity": {
        "classification": "valid",
        "recipe": "H(snapshot, SnapshotV2)",
        "before": id_a,
        "after": id_b,
        "changedField": "vcsDigest",
        "equal": False,
        "expectedEqual": False,
        "measured": True,
    },
    "operationalChangeDoesNotMoveIdentity": {
        "classification": "valid",
        "recipe": "RequestId/ExecutionId/wallClock are not Run/snapshot fields",
        "requestId": request_id,
        "executionId": execution_id,
        "wallClock": wall,
        "snapshotHUnchanged": h_a,
        "runH": h_run,
        "runHAfterRecompute": H("run", run_like),
        "equal": H("run", run_like) == h_run,
        "expectedEqual": True,
        "illegalRequestIdOnRunRefusedBySchema": not ril["stockOk"],
        "measured": True,
    },
    "helperCorrection": {
        "originalFailure": "After scope-v2 overwrite, vectors/semantic-vs-operational.json retained only a two-sentence distinct:true claim without measured H. The earlier phase-1 pair hashed a non-schema snapshot.",
        "selector": "identity-and-evidence.md §2; identity-schemas.v3.json#/$defs/snapshot and #/$defs/run",
        "change": "Paired H(snapshot) on schema-valid records; operational IDs omitted from the recipe and refused if stuffed into run.",
    },
}
dump("semantic-vs-operational.json", sem_vs_op)

# ---------------------------------------------------------------------------
# R-CVE1-EIGHT-TYPES
# ---------------------------------------------------------------------------
cve1_cases = []
samples = [
    ("null", None),
    ("false", False),
    ("true", True),
    ("unsigned-64", 0),
    ("unsigned-64", 1),
    ("unsigned-64", 18446744073709551615),
    ("negative-signed-64", -1),
    ("negative-signed-64", -9223372036854775808),
    ("NFC-UTF8-string", ""),
    ("NFC-UTF8-string", "opensip"),
    ("NFC-UTF8-string", "café"),
    ("array", []),
    ("array", [None, True, False, 2, "x"]),
    ("string-keyed-map", {}),
    ("string-keyed-map", {"b": 1, "a": 0}),
]
seen = set()
for expected, value in samples:
    rt = round_trip(value)
    if rt["type"] != expected or not rt["reencodeEquals"] or not rt["decodedEquals"]:
        die(f"CVE1 round-trip {expected}")
    seen.add(expected)
    cve1_cases.append({"inputKind": expected, "pythonRepr": repr(value), **rt})
if seen != set(CLOSED_TYPES):
    die(f"CVE1 types missing {set(CLOSED_TYPES)-seen}")
m1, m2 = encode({"z": 1, "a": 2}), encode({"a": 2, "z": 1})
if m1 != m2:
    die("CVE1 map key order not independent")
cve1_cases.append({"inputKind": "string-keyed-map-key-order-independence", "hex": m1.hex(), "equalRegardlessOfInsertion": True})
try:
    encode("e\u0301")
    die("non-NFC string admitted")
except AdmissionError as e:
    cve1_cases.append({"inputKind": "non-NFC-string-negative", "ok": False, "firstRefusal": e.as_dict(), "classification": "invalid"})
try:
    encode(1.0)  # type: ignore
    die("float admitted")
except AdmissionError as e:
    cve1_cases.append({"inputKind": "float-negative", "ok": False, "firstRefusal": e.as_dict(), "classification": "invalid"})
dump(
    "cve1-eight-types.json",
    {
        "kind": "standaloneCanonicalVector",
        "selector": cve1_sel,
        "closedTypes": list(CLOSED_TYPES),
        "vectors": cve1_cases,
    },
)

# ---------------------------------------------------------------------------
# R-LEXICAL-ADMISSION + R-RAW-VS-PARSED
# ---------------------------------------------------------------------------
raw_vectors = []


def add_raw(name, raw: bytes, expect_ok: bool, expect_code: str | None = None):
    r = lexical_first(raw)
    rec = {
        "name": name,
        "rawUtf8": raw.decode("utf-8", "replace"),
        "rawHex": raw.hex(),
        "classification": "valid" if expect_ok else "invalid",
        **r,
    }
    raw_vectors.append(rec)
    if expect_ok and r["ok"] is not True:
        die(f"lexical expected ok {name} {r}")
    if not expect_ok:
        if r["ok"] is not False:
            die(f"lexical expected refuse {name}")
        if expect_code and r["firstRefusal"]["code"] != expect_code:
            die(f"lexical expected {expect_code} got {r['firstRefusal']} for {name}")


add_raw("integer-zero", b"0", True)
add_raw("integer-positive", b"42", True)
add_raw("integer-negative", b"-7", True)
add_raw("integer-u64-max", b"18446744073709551615", True)
add_raw("integer-i64-min", b"-9223372036854775808", True)
add_raw("bool-true", b"true", True)
add_raw("object-ok", b'{"a":1,"b":2}', True)
add_raw("duplicate-key", b'{"a":1,"a":2}', False, "DUPLICATE_KEY")
add_raw("float-1.0", b"1.0", False, "FLOAT_FORBIDDEN")
add_raw("exponent", b"1e2", False, "EXPONENT_FORBIDDEN")
add_raw("neg-zero", b"-0", False, "NEG_ZERO_FORBIDDEN")
add_raw("leading-zero", b"01", False, "LEADING_ZERO")
add_raw("out-of-range-high", b"18446744073709551616", False, "INTEGER_OUT_OF_RANGE")
add_raw("out-of-range-low", b"-9223372036854775809", False, "INTEGER_OUT_OF_RANGE")
add_raw("unpaired-surrogate", '{"x":"\\uD800"}'.encode(), False, "NON_SCALAR_UNICODE")
add_raw("bom", b"\xef\xbb\xbf{}", False, "BOM_FORBIDDEN")
add_raw("unescaped-control", b'"\x01"', False, "UNESCAPED_CONTROL")

dump(
    "lexical-admission.json",
    {
        "kind": "standaloneCanonicalVector",
        "selector": "identity-and-evidence.md §3 lexical admission",
        "note": "RAW bytes. Python json.loads is not used.",
        "vectors": raw_vectors,
    },
)

raw_dup = lexical_first(b'{"a":1,"a":2}')
if raw_dup["ok"] or C(True) == C(1):
    die("raw-vs-parsed controls failed")
dump(
    "raw-vs-parsed.json",
    {
        "kind": "standaloneCanonicalVector",
        "selector": "identity-and-evidence §3: reject duplicate keys before deserialization loses lexical information",
        "parsedObjectEncode": {"classification": "valid", "object": {"a": 1}, "C_hex": C({"a": 1}).hex()},
        "rawDuplicate": {"classification": "invalid", "raw": '{"a":1,"a":2}', **raw_dup},
        "rawFloat": lexical_first(b"1.0"),
        "parsedBoolIsNotInt": {"C_true": C(True).decode(), "C_one": C(1).decode(), "distinct": True},
        "distinctFromObjectEncode": True,
    },
)

# ---------------------------------------------------------------------------
# R-ACYCLIC-JOINS — schema-valid typed records, published H domains
# ---------------------------------------------------------------------------
# Nested digest preimages are themselves C-canonical records retained here.
policy = {"schemaFamily": "opensip.product.policy", "schemaMajor": 2, "gateSeverityAtLeast": "error", "rules": []}
policy_d = hashlib.sha256(C(policy)).hexdigest()
waiver = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1, "waivers": []}
waiver_d = hashlib.sha256(C(waiver)).hexdigest()
grant = {
    "schemaVersion": 2,
    "projectId": project_id,
    "principals": [{"kind": "first-party", "closureId": "closure2:" + "bb" * 32, "ownerSourceDigest": None}],
    "analysisOperations": ["native-analysis"],
    "scopeDigest": scope_d,
}
grant["analysisOperations"] = sorted(grant["analysisOperations"])
grant_d = hashlib.sha256(C(grant)).hexdigest()
aspec = {"schemaVersion": 2, "requestedCapabilities": [{"capabilityId": "inventory", "languageMode": "syntax-only", "workspaceRoot": ".", "required": True}], "policyPackIds": [], "parameters": []}
as_d = hashlib.sha256(C(aspec)).hexdigest()
plan_desc = {
    "schemaVersion": 2,
    "snapshotId": id_a,
    "capabilityManifestId": "aa" * 32,
    "semanticClosures": ["closure2:" + "bb" * 32],
    "analysisSpecDigest": as_d,
    "resolvedConfigDigest": cfg_d,
    "nativeContextDigests": ["dd" * 32],
    "importIds": [],
    "policyDigest": policy_d,
    "waiverDigest": waiver_d,
    "scopeDigest": scope_d,
    "budget": {"unit": "work-units", "limit": 1},
    "semanticGrantDigest": grant_d,
    "capabilityManifestBytesDigest": "14" * 32,
}
must_ok(validate_against(grant, IDENT, selector="#/$defs/semantic-grant", label="grant"), "grant")
must_ok(validate_against(aspec, IDENT, selector="#/$defs/analysis-spec", label="analysis-spec"), "analysis-spec")
must_ok(validate_against(plan_desc, IDENT, selector="#/$defs/plan", label="plan"), "plan")
plan_id = typed_id("plan", plan_desc)
view_desc = {
    "schemaVersion": 2,
    "planId": plan_id,
    "scopeIds": ["scope2:" + "21" * 32],
    "facts": ["fact2:" + "22" * 32],
    "coverageIds": ["coverage2:" + "23" * 32],
    "producerClosure": "closure2:" + "bb" * 32,
    "schemaDigests": ["24" * 32],
}
must_ok(validate_against(view_desc, IDENT, selector="#/$defs/view", label="view"), "view")
view_id = typed_id("view", view_desc)
proof_desc = {
    "schemaVersion": 3,
    "planId": plan_id,
    "executionPlanId": "exec-plan2:" + "31" * 32,
    "evaluatorClosure": "closure2:" + "32" * 32,
    "ruleProgramDigest": "33" * 32,
    "evaluationInputRefs": [],
    "predicateProofs": [],
    "findingIds": [],
    "verdict": "pass",
    "evaluationState": "evaluated",
    "ruleResults": [],
    "waivedFindingIds": [],
    "executionDeficiencies": [],
    "executionInputsDigest": "34" * 32,
}
must_ok(validate_against(proof_desc, IDENT, selector="#/$defs/proof-bundle", label="proof"), "proof")
if "evidenceId" in proof_desc or "runId" in proof_desc:
    die("proof illegally contains evidence/run")
proof_id = typed_id("proof-bundle", proof_desc)
# cycle attempt: stuffing evidenceId
proof_cycle = dict(proof_desc)
proof_cycle["evidenceId"] = "evidence3:" + "55" * 32
rpc = validate_against(proof_cycle, IDENT, selector="#/$defs/proof-bundle", label="proof-cycle")
if rpc["stockOk"]:
    die("proof with evidenceId should refuse additionalProperties")
evidence = {
    "schemaVersion": 3,
    "planId": plan_id,
    "viewIds": [view_id],
    "coverageIds": ["coverage2:" + "23" * 32],
    "importIds": [],
    "findingIds": [],
    "proofBundleId": proof_id,
}
must_ok(validate_against(evidence, IDENT, selector="#/$defs/semantic-evidence", label="evidence"), "evidence")
ev_id = typed_id("semantic-evidence", evidence)
seal = {
    "schemaVersion": 3,
    "planId": plan_id,
    "executionPlanId": proof_desc["executionPlanId"],
    "evidenceId": ev_id,
    "evaluatorClosure": proof_desc["evaluatorClosure"],
    "policyDigest": policy_d,
    "proofBundleId": proof_id,
    "verdict": "pass",
}
must_ok(validate_against(seal, IDENT, selector="#/$defs/evaluation-seal", label="seal"), "seal")
seal_id = typed_id("evaluation-seal", seal)
run_desc = {
    "schemaVersion": 3,
    "projectId": project_id,
    "snapshotId": id_a,
    "planId": plan_id,
    "evidenceId": ev_id,
    "evaluationSealId": seal_id,
    "capabilityManifestId": plan_desc["capabilityManifestId"],
}
must_ok(validate_against(run_desc, IDENT, selector="#/$defs/run", label="run-chain"), "run-chain")
run_id = typed_id("run", run_desc)

dump(
    "acyclic-joins.json",
    {
        "kind": "standaloneCanonicalVector",
        "selector": "identity-and-evidence §3: proof has no evidenceId/runId; evidence may include proof; seal includes both; run includes seal",
        "helperCorrection": {
            "originalFailure": "Historical acyclic vector used view.factIds/schemaDigest (not facts/schemaDigests) and hashed non-schema snapshots.",
            "selector": "identity-schemas.v3.json#/$defs/view, proof-bundle, semantic-evidence, evaluation-seal, run",
            "change": "Chain members inhabit published records; cycle is additionalProperties refusal of proof.evidenceId.",
        },
        "positive": {
            "classification": "valid",
            "chain": [
                {"domain": "snapshot", "id": id_a},
                {"domain": "plan", "id": plan_id, "refs": {"snapshotId": id_a}},
                {"domain": "view", "id": view_id, "refs": {"planId": plan_id}},
                {"domain": "proof-bundle", "id": proof_id, "refs": {"planId": plan_id}, "doesNotContain": ["evidenceId", "runId"]},
                {"domain": "semantic-evidence", "id": ev_id, "refs": {"proofBundleId": proof_id, "viewIds": [view_id]}},
                {"domain": "evaluation-seal", "id": seal_id, "refs": {"evidenceId": ev_id, "proofBundleId": proof_id}},
                {"domain": "run", "id": run_id, "refs": {"evaluationSealId": seal_id, "snapshotId": id_a, "planId": plan_id}},
            ],
            "stockOk": True,
        },
        "cycle": {
            "classification": "invalid",
            "attempt": "proof-bundle additionalProperties evidenceId",
            "stockOk": False,
            "expectedRefuse": True,
            "errors": rpc["errors"][:3],
        },
    },
)

# ---------------------------------------------------------------------------
# Phase 2 capability admission
# ---------------------------------------------------------------------------

def provider(**kw):
    base = {
        "providerId": "typescript-semantic",
        "language": "typescript",
        "providerVersionSource": "release.typescript-provider",
        "toolchainIdentitySource": "release.typescript-runtime",
        "relations": {
            "calls": "resolved-callee",
            "clones": "normalized-body-hash",
            "control-flow": "syntactic",
            "declares": "syntactic",
            "file": "enumerated",
            "imports": "resolved-target",
            "literal": "syntactic",
            "package": "manifest-declared",
            "reachability": "from-resolved-calls",
            "references": "resolved-binding",
            "types": "checked",
            "unresolved-edge": "observed",
            "vcs-change": "vcs-reported",
        },
        "platformIds": ["linux-aarch64-gnu", "linux-x86_64-gnu", "macos-aarch64", "macos-x86_64"],
    }
    base.update(kw)
    return base


good = {
    "schemaVersion": 1,
    "profile": "core",
    "providers": [provider(providerId="rust-semantic", language="rust"), provider(providerId="typescript-semantic", language="typescript")],
    "coverageForAbsent": [],
}
if good["providers"][0]["providerId"] >= good["providers"][1]["providerId"]:
    die("providers not sorted")
pos = capability_manifest_id(good)
if not pos["ok"]:
    die("positive cap manifest refused")
# recipe check
committed = bytes.fromhex(pos["committedBytesHex"])
recomputed = hashlib.sha256(b"opensip.capability-manifest.v1\x00" + committed).hexdigest()
if recomputed != pos["capabilityManifestId"]:
    die("CAP-MANIFEST-ID-V1 recompute mismatch")

gates = []


def neg(name, manifest, expect_gate, hypothesized_later):
    r = first_refusal(manifest)
    if r["ok"] is not False:
        die(f"expected refuse {name}")
    if r["gate"] != expect_gate:
        die(f"{name} expected {expect_gate} got {r['gate']}")
    rec = {
        "name": name,
        "classification": "invalid",
        "expectedGate": expect_gate,
        "firstRefusal": r["firstRefusal"],
        "gate": r["gate"],
        "masksLater": r["masksLater"],
        "remainingGatesMasked": r.get("remainingGatesMasked", []),
        "hypothesizedLaterChecksMasked": hypothesized_later,
        "note": "First observed refusal only; later gates not executed.",
    }
    if rec["remainingGatesMasked"] != hypothesized_later:
        die(f"{name} remainingGatesMasked {rec['remainingGatesMasked']} != {hypothesized_later}")
    if bool(hypothesized_later) != r["masksLater"]:
        die(f"{name} masksLater {r['masksLater']} vs later {hypothesized_later}")
    gates.append(rec)


t1 = dict(good)
t1["schemaVersion"] = True
neg("ADM-TYPE-boolean-schemaVersion", t1, "ADM-TYPE", ["ADM-CLOSED", "ADM-DOMAIN", "ADM-ORDER"])
t2 = dict(good)
t2["schemaVersion"] = "1"
neg("ADM-TYPE-string-schemaVersion", t2, "ADM-TYPE", ["ADM-CLOSED", "ADM-DOMAIN", "ADM-ORDER"])
c1 = {**good, "comment": "no"}
neg("ADM-CLOSED-undeclared-key", c1, "ADM-CLOSED", ["ADM-DOMAIN", "ADM-ORDER"])
c2 = {k: v for k, v in good.items() if k != "coverageForAbsent"}
neg("ADM-CLOSED-missing-key", c2, "ADM-CLOSED", ["ADM-DOMAIN", "ADM-ORDER"])
d1 = json.loads(json.dumps(good))
d1["providers"][0]["platformIds"] = ["linux-aarch64-gnu", "linux-x86_64-gnu", "macos-aarch64", "ALL-SUPPORTED"]
neg("ADM-DOMAIN-platform-case", d1, "ADM-DOMAIN", ["ADM-ORDER"])
d2 = json.loads(json.dumps(good))
d2["providers"][0]["relations"]["calls"] = "enumerated"
neg("ADM-DOMAIN-cross-ladder-rung", d2, "ADM-DOMAIN", ["ADM-ORDER"])
o1 = json.loads(json.dumps(good))
o1["providers"][0]["platformIds"] = ["linux-x86_64-gnu", "linux-aarch64-gnu", "macos-aarch64", "macos-x86_64"]
neg("ADM-ORDER-platformIds", o1, "ADM-ORDER", [])
o2 = json.loads(json.dumps(good))
o2["providers"] = list(reversed(o2["providers"]))
neg("ADM-ORDER-providers", o2, "ADM-ORDER", [])
combo = json.loads(json.dumps(good))
combo["schemaVersion"] = True
combo["comment"] = "no"
neg("ADM-TYPE-masks-later-closed", combo, "ADM-TYPE", ["ADM-CLOSED", "ADM-DOMAIN", "ADM-ORDER"])

dump(
    "cap-admission.json",
    {
        "kind": "standaloneCanonicalVector",
        "classification": "valid",
        "recipe": "CAP-MANIFEST-ID-V1",
        "selectors": [
            "docs/coop/artifacts/delivery.v4.json capabilityManifestIdentity CAP-MANIFEST-ID-V1",
            "docs/coop/design-corrections/native/capability-manifest-domains.v2.json",
            "docs/coop/artifacts/resolved-inputs.v2.json#planIdContract.canonicalValueEncoding",
        ],
        "gateOrder": ["ADM-TYPE", "ADM-CLOSED", "ADM-DOMAIN", "ADM-ORDER"],
        "positive": {"manifest": good, **pos, "recomputedEquals": recomputed == pos["capabilityManifestId"]},
        "admissionBeforeEncoding": True,
    },
)
dump(
    "cap-named-gates.json",
    {
        "kind": "standaloneCanonicalVector",
        "classification": "invalid",
        "gateOrder": ["ADM-TYPE", "ADM-CLOSED", "ADM-DOMAIN", "ADM-ORDER"],
        "helperCorrection": {
            "originalFailure": "Historical helper walked ADM-CLOSED via _closed_record before ADM-TYPE, so a combined boolean-schemaVersion plus extra-key input would have named ADM-CLOSED first.",
            "selector": "capability-manifest-domains.v2.json gateOrder; delivery.v4 CAP-MANIFEST-ID-V1 admission.gateOrder",
            "change": "admit() now runs ADM-TYPE, ADM-CLOSED, ADM-DOMAIN, ADM-ORDER as four separate passes. first_refusal.masksLater is false only for ADM-ORDER.",
        },
        "vectors": gates,
    },
)

# ---------------------------------------------------------------------------
# Phase 3 traces
# ---------------------------------------------------------------------------
FULL_CAPS = list(IDENTITY_TOKENS) + [
    "sealed-vfs-v1",
    "multi-stage-analyze-v1",
    "rust-semantic-facts-v1",
    "resolution-completeness-v2",
    "unresolved-edge-v1",
    "dependency-source-v1",
    "prepared-output-v3",
    "native-context-v2",
]
complete_events = [
    {"frame": "Hello"},
    {"frame": "HelloAck", "capabilities": FULL_CAPS},
    {"frame": "OpenUniverse", "dependencyMode": True, "preparedMode": False},
    {"frame": "UniverseAccepted"},
    {"frame": "SnapshotManifest"},
    {"frame": "SnapshotFileChunk"},
    {"frame": "SnapshotSeal"},
    {"frame": "SnapshotAccepted"},
    {"frame": "DependencySourceManifest"},
    {"frame": "DependencySourceChunk"},
    {"frame": "DependencySourceSeal"},
    {"frame": "DependencySourceAccepted"},
    {"frame": "NativeContextVerified"},
    {"frame": "Analyze", "stageCount": 1},
    {"frame": "FactBatch"},
    {"frame": "CoverageV3"},
    {"frame": "Complete"},
    {"frame": "zero-exit"},
    {"frame": "eof"},
]
tr_complete = run_trace(complete_events, stage_count=1)
if tr_complete["final"]["phase"] != "DONE" or tr_complete["final"]["terminalKind"] != "complete":
    die(f"complete trace {tr_complete['final']}")
if tr_complete["final"]["identityNegotiated"] is not True:
    die("complete identityNegotiated")
hello_idx = next(i for i, t in enumerate(tr_complete["trace"]) if t["event"]["frame"] == "HelloAck")
open_idx = next(i for i, t in enumerate(tr_complete["trace"]) if t["event"]["frame"] == "OpenUniverse")
if not (hello_idx < open_idx and tr_complete["trace"][hello_idx]["identityNegotiated"] and not tr_complete["trace"][hello_idx]["sourceBytesSent"]):
    die("identity-before-source on complete")
if not tr_complete["trace"][open_idx]["sourceBytesSent"]:
    die("OpenUniverse should set sourceBytesSent")

no_id = [{"frame": "Hello"}, {"frame": "HelloAck", "capabilities": ["sealed-vfs-v1"]}, {"frame": "OpenUniverse", "dependencyMode": False, "preparedMode": False}]
tr_noid = run_trace(no_id)
if tr_noid["final"]["phase"] != "FAULT" or tr_noid["trace"][-1]["traceId"] != "P3-34":
    die(f"no-identity OpenUniverse {tr_noid['final']} {tr_noid['trace'][-1]}")
if tr_noid["final"]["sourceBytesSent"] is not False:
    die("unmatched OpenUniverse must not mark sourceBytesSent")

unavail_events = complete_events[:12] + [{"frame": "Unavailable"}, {"frame": "zero-exit"}, {"frame": "eof"}]
tr_unavail = run_trace(unavail_events)
if tr_unavail["final"]["terminalKind"] != "unavailable" or tr_unavail["final"]["phase"] != "DONE":
    die(f"unavailable {tr_unavail['final']}")

cancel_events = complete_events[:14] + [{"frame": "Cancel"}, {"frame": "Cancelled"}, {"frame": "zero-exit"}, {"frame": "eof"}]
tr_cancel = run_trace(cancel_events)
if tr_cancel["final"]["terminalKind"] != "cancelled":
    die(f"cancel {tr_cancel['final']}")

fault_events = [{"frame": "Hello"}, {"frame": "HelloAck", "capabilities": FULL_CAPS}, {"frame": "deadline"}]
tr_fault = run_trace(fault_events)
if tr_fault["final"]["phase"] != "FAULT":
    die(f"fault {tr_fault['final']}")

post = complete_events + [{"frame": "FactBatch"}]
tr_post = run_trace(post)
if tr_post["trace"][-1]["traceId"] != "post-terminal-frame":
    die(f"post-terminal {tr_post['trace'][-1]}")

for name, tr, extra in [
    ("complete.json", tr_complete, {"kind": "standaloneTraceVector", "classification": "valid", "expectedTerminal": "complete"}),
    ("unavailable.json", tr_unavail, {"kind": "standaloneTraceVector", "classification": "valid", "expectedTerminal": "unavailable"}),
    ("cancel.json", tr_cancel, {"kind": "standaloneTraceVector", "classification": "valid", "expectedTerminal": "cancelled"}),
    ("fault.json", tr_fault, {"kind": "standaloneTraceVector", "classification": "invalid", "expectedPhase": "FAULT"}),
    ("identity-before-source.json", {"complete": {"helloAckBeforeOpenUniverse": hello_idx < open_idx, "identityNegotiatedBeforeSource": True, "helloAckSourceBytesSent": False, "openUniverseSourceBytesSent": True}, "openUniverseWithoutIdentity": {"finalPhase": tr_noid["final"]["phase"], "traceId": tr_noid["trace"][-1]["traceId"], "sourceBytesSent": False}}, {"kind": "standaloneTraceVector"}),
    ("terminal.json", tr_post, {"kind": "standaloneTraceVector", "classification": "invalid", "expectedTraceId": "post-terminal-frame"}),
]:
    body = {"kind": "standaloneTraceVector", "selector": "docs/coop/design-corrections/native/protocol3-transitions.v1.json", "executedVsHost": "executed — state machine reconstructed; frame payload schema and native process spawn are future-host assumptions", **extra}
    if isinstance(tr, dict) and "trace" in tr:
        body["final"] = tr["final"]
        body["trace"] = tr["trace"]
    else:
        body.update(tr)
    dump("traces/" + name, body)

dump(
    "traces/executed-vs-host.json",
    {
        "kind": "standingRule",
        "everyTraceLabeled": True,
        "executed": "transition matching against protocol3-transitions.v1.json",
        "futureHostAssumption": "actual provider process, OS pipes, frame codec bytes",
    },
)

# ---------------------------------------------------------------------------
# Phase 4 registries
# ---------------------------------------------------------------------------
rel_doc = json.loads((KIT / REL).read_text())
relations = rel_doc["x-opensip-relation-registry"]["relations"]
rung_table = []
for name, row in sorted(relations.items()):
    rung_table.append(
        {
            "relation": name,
            "ladder": row["ladder"],
            "subjectKind": row.get("subjectKind"),
            "universeRule": row.get("universeRule"),
            "anchorClass": (row.get("anchorLaw") or {}).get("class"),
        }
    )
file_row = relations["file"]
if file_row["ladder"] != ["enumerated"]:
    die(f"file ladder {file_row['ladder']}")
dump(
    "relation-rung-table.json",
    {
        "kind": "standaloneCanonicalVector",
        "selector": "relation-payload-schemas.v2.json#/x-opensip-relation-registry",
        "nRelations": len(rung_table),
        "rows": rung_table,
        "fileLadder": ["enumerated"],
        "fileResolvedRungInvented": False,
    },
)

# RC-1 closed five-member resolved set. Every other registered rung is not-applicable.
RESOLVED_PAIRS = {
    ("imports", "resolved-target"),
    ("references", "resolved-binding"),
    ("calls", "resolved-callee"),
    ("types", "checked"),
    ("reachability", "from-resolved-calls"),
}


def apply_rc(relation: str, resolution: str, *, facts_present: bool, unresolved_edge_count: int = 0, stage_terminal: str = "complete", examined_exhaustive: bool = True) -> dict:
    ladders = json.loads((KIT / REL).read_text())["x-opensip-relation-registry"]["relations"]
    if relation not in ladders or resolution not in ladders[relation]["ladder"]:
        die(f"unregistered coverage pair {relation}@{resolution}")
    if (relation, resolution) not in RESOLVED_PAIRS:
        # RC-1 / RC-6: file@enumerated and the other twelve non-resolved rungs.
        return {"state": "not-applicable", "attempted": False, "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}
    # RC-2 on a resolved rung. Zero edges is never complete by itself (not-attempted if skipped).
    if unresolved_edge_count > 0:
        return {"state": "incomplete", "attempted": True, "unresolvedEdgeCount": unresolved_edge_count}
    if stage_terminal != "complete":
        return {"state": "partial", "attempted": True, "stageTerminal": stage_terminal}
    if not examined_exhaustive:
        return {"state": "partial", "attempted": True, "examinedExhaustive": False}
    if not facts_present:
        # Attempted exhaustive resolved scan that found no facts and no unresolved edges.
        return {"state": "complete", "attempted": True, "examinedExhaustive": True, "factsPresent": False}
    return {"state": "complete", "attempted": True, "examinedExhaustive": True}


count_cases = [
    {"name": "file-enumerated-with-fact", "relation": "file", "resolution": "enumerated", "factsPresent": True, "expected": {"state": "not-applicable", "attempted": False}},
    {"name": "file-enumerated-fact-absent", "relation": "file", "resolution": "enumerated", "factsPresent": False, "expected": {"state": "not-applicable", "attempted": False}},
    {"name": "imports-resolved-zero-unresolved-complete", "relation": "imports", "resolution": "resolved-target", "factsPresent": True, "unresolvedEdgeCount": 0, "expected": {"state": "complete", "attempted": True, "examinedExhaustive": True}},
    {"name": "imports-resolved-unresolved-edges-incomplete", "relation": "imports", "resolution": "resolved-target", "factsPresent": True, "unresolvedEdgeCount": 1, "expected": {"state": "incomplete", "attempted": True}},
]
count_vecs = []
for case in count_cases:
    observed = apply_rc(
        case["relation"],
        case["resolution"],
        facts_present=case["factsPresent"],
        unresolved_edge_count=case.get("unresolvedEdgeCount", 0),
    )
    rec = {**case, "observed": {k: observed[k] for k in case["expected"]}, "ok": all(observed.get(k) == v for k, v in case["expected"].items())}
    if not rec["ok"]:
        die(f"count-class-attempt {case['name']} expected {case['expected']} observed {observed}")
    count_vecs.append(rec)
dump(
    "count-class-attempt.json",
    {
        "kind": "standaloneCanonicalVector",
        "selector": "native-evidence.md §4.3 RC-0/RC-1/RC-2/RC-6",
        "resolvedRungs": ["checked", "from-resolved-calls", "resolved-binding", "resolved-callee", "resolved-target"],
        "vectors": count_vecs,
    },
)

native = json.loads((KIT / NATIVE).read_text())
gcap = native["x-opensip-grammar-capability-registry"]
code_vs_data = {
    "kind": "standaloneCanonicalVector",
    "selector": "native-evidence.schemas.v2.json#/x-opensip-grammar-capability-registry",
    "classLaw": gcap["classLaw"],
    "codeLanguages": sorted(k for k, v in gcap["languages"].items() if v["syntaxClass"] == "code"),
    "dataLanguages": sorted(k for k, v in gcap["languages"].items() if v["syntaxClass"] == "data-document"),
    "jsonHasNoBodyIdentity": "json" in gcap["languages"] and gcap["languages"]["json"]["syntaxClass"] == "data-document",
    "typescriptHasClones": "clones@normalized-body-hash" in gcap["languages"]["typescript"]["capabilities"],
}
if not code_vs_data["jsonHasNoBodyIdentity"] or not code_vs_data["typescriptHasClones"]:
    die("code-vs-data matrix mismatch")
if "clones@normalized-body-hash" in gcap["languages"]["json"]["capabilities"]:
    die("json must not bear clones body identity")
code_vs_data["frozenSyntaxRunsCitedReadOnly"] = {
    "syntax-code": "runs/syntax-code.store.json",
    "syntax-data": "runs/syntax-data.store.json",
    "note": "syntax-only uses SyntaxGrammarBundleV1; json data-document files in the syntax-data Run mint no body identity.",
}
dump("code-vs-data-matrix.json", code_vs_data)

# enum-vs-resolution: inspect frozen stores read-only
from helper.store import Store as S

file_rungs = []
for stem in ["syntax-code", "ts", "rust", "syntax-data", "rust-partial-clones"]:
    st = S.load(OUT / "runs" / f"{stem}.store.json")
    invented = []
    for k, rec in st.object_table.items():
        if not str(k).startswith("fact2:"):
            continue
        frame = st.get(rec["digest"])
        parsed = parse_h_frame(frame, allowed_domains={"fact"})
        if parsed["value"].get("relation") == "file":
            res = parsed["value"].get("resolution")
            if res != "enumerated":
                invented.append({"store": stem, "id": k, "resolution": res})
            file_rungs.append({"store": stem, "id": k, "resolution": res})
if invented:
    die(f"invented file resolved rung {invented}")
by_store = {stem: [r for r in file_rungs if r["store"] == stem] for stem in ["syntax-code", "ts", "rust", "syntax-data", "rust-partial-clones"]}
missing = [s for s, rows in by_store.items() if not rows]
if missing:
    die(f"no file@enumerated facts observed in frozen stores {missing}")
dump(
    "enum-vs-resolution.json",
    {
        "kind": "standingRule",
        "selector": "relation-payload-schemas.v2 file.ladder; native-evidence RC-6",
        "fileRung": "enumerated",
        "fileResolvedRungInvented": False,
        "observedFileFacts": file_rungs,
        "nFileFacts": len(file_rungs),
        "storesInspectedReadOnly": True,
    },
)

matrix = json.loads(MATRIX.read_text())
modes = list(matrix["languageModes"])
mode_paths = []
for m in modes:
    if m.startswith("ts-") or m.startswith("js-"):
        path = "native.context.typescript.v2 + native.semantic-universe.typescript.v2"
    elif m.startswith("rust-"):
        path = "native.context.rust.v2 + native.semantic-universe.rust.v2"
    elif m == "syntax-only":
        path = "native.context.syntax.v2 + native.semantic-universe.syntax.v2 (grammar bundle)"
    else:
        path = None
    mode_paths.append({"mode": m, "analysisPath": path, "representable": path is not None})
if any(not r["representable"] for r in mode_paths):
    die("unrepresentable advertised mode")
dump(
    "advertised-mode-paths.json",
    {
        "kind": "standingRule",
        "selector": "native-capability-matrix.v2.json languageModes; identity-schemas.v3 domainSets native-context",
        "modes": mode_paths,
        "chosenGrammar": "syntax-only uses SyntaxGrammarBundleV1; ts/js use TypeScriptNativeContextV2; rust uses NativeContextV2",
    },
)

# ---------------------------------------------------------------------------
# R-IMPORTED-OBSERVATION-BOUNDARY — retained import2, not a native fact
# ---------------------------------------------------------------------------
rt_payload = {
    "payloadDomain": "workflow.import-payload.runtime.v1",
    "format": "istanbul-json",
    "observationWindow": {"startUtc": "2026-09-01T00:00:00Z", "endUtc": "2026-09-01T00:00:01Z"},
    "observedPopulation": "synthetic",
    "subjects": [],
    "mappingGaps": [],
}
must_ok(validate_against(rt_payload, IMP, selector="#/$defs/RuntimePayloadV1", label="runtime-payload"), "RuntimePayloadV1")
rt_pd = hashlib.sha256(C(rt_payload)).hexdigest()
store.put_canonical(rt_payload, label="RuntimePayloadV1")
imp_schema_d = hashlib.sha256((KIT / IMP).read_bytes()).hexdigest()
store.put_raw((KIT / IMP).read_bytes(), label="imported-evidence.schema.json")
COMMON = "docs/coop/design-corrections/workflows/schemas/common.schema.json"
sc = {"kind": "exact-snapshot", "snapshotId": id_a}
must_ok(validate_against(sc, COMMON, selector="#/$defs/SourceCorrespondence", label="source-correspondence"), "SourceCorrespondence")
sc_d = hashlib.sha256(C(sc)).hexdigest()
build = {"schemaVersion": 1, "buildIdentity": "synthetic-build"}
must_ok(validate_against(build, IMP, selector="#/$defs/BuildIdentityV1", label="build"), "BuildIdentityV1")
build_d = hashlib.sha256(C(build)).hexdigest()
obs = {"schemaVersion": 1, "kind": "runtime", "window": None, "population": None, "selection": None, "revisionRange": None}
must_ok(validate_against(obs, IMP, selector="#/$defs/ImportObservationV1", label="observation"), "ImportObservationV1")
obs_d = hashlib.sha256(C(obs)).hexdigest()
imp_rec = {
    "schemaVersion": 2,
    "kind": "runtime",
    "payloadSchemaDigest": imp_schema_d,
    "payloadDigest": rt_pd,
    "sourceCorrespondenceDigest": sc_d,
    "buildDigest": build_d,
    "producerClosure": "closure2:" + "aa" * 32,
    "adapterClosure": "closure2:" + "aa" * 32,
    "blobs": [],
    "scopeDigest": scope_d,
    "observationDigest": obs_d,
    "completeness": "complete",
    "omissions": [],
}
must_ok(validate_against(imp_rec, IDENT, selector="#/$defs/import", label="import"), "import")
imp_id = typed_id("import", imp_rec)
imp_h = H("import", imp_rec)
# not a fact
if imp_id.startswith("fact2:"):
    die("import minted as fact")
dump(
    "imported-observation-boundary.json",
    {
        "kind": "standaloneCanonicalVector",
        "selector": "workflows-and-surfaces.md imported observation limits; native-evidence §7; atom-evaluation-contract §6; identity-and-evidence §3 selection never turns imported observations into native facts",
        "helperCorrection": {
            "originalFailure": "vectors/imported-observation-boundary.json after scope-v2 was a mayProve/mayNotProve list with no retained import2 record.",
            "selector": "identity-schemas.v3.json#/$defs/import; imported-evidence.schema.json#/$defs/RuntimePayloadV1",
            "change": "Retained C(RuntimePayloadV1) and H(import, ImportedEvidenceRecordV2). Explicitly not fact2. Frozen TS Run import is cited read-only.",
        },
        "retainedImport": {
            "classification": "valid",
            "typedId": imp_id,
            "H": imp_h,
            "record": imp_rec,
            "payload": rt_payload,
            "payloadDigest": rt_pd,
            "isFact2": False,
            "isNativeCoverage": False,
            "stockOk": True,
        },
        "mayProve": [
            "runtime hit/miss at mapped subject (observed-hit / observable-unhit)",
            "test process result when the imported wrapper is a test execution",
            "history path presence inside the observation window",
        ],
        "mayNotProve": [
            "static Coverage completeness",
            "native resolution completeness",
            "universal non-use / closed world",
            "unsafe delete/replace authorization",
            "native fact2 identity",
        ],
        "frozenTsRunImportCitedReadOnly": {
            "store": "runs/ts.store.json",
            "importIds": sorted(k for k in S.load(OUT / "runs" / "ts.store.json").object_table if str(k).startswith("import2:")),
            "note": "The TypeScript complete Run retains an import2; this exhibit does not modify that store. Imported observation is not native fact2.",
        },
    },
)

# ---------------------------------------------------------------------------
# ID mapping + reconstruction results
# ---------------------------------------------------------------------------
mapping = {
    "standing": "Original IDs mapped to NEW foundation exhibits because vectors/ and traces/ are shared with frozen scope-v2 evidence.",
    "historicalSharedPathPreserved": "preserved-failures/foundation-shared-path-original/",
    "ids": {
        "S-FRESH-ORIGIN": "foundation/phase-0.json",
        "S-NOT-PRODUCT": "foundation/phase-0.json",
        "S-KIT-ONLY": "foundation/phase-0.json",
        "S-MANIFEST-VERIFY": "foundation/phase-0.json",
        "S-NO-ORACLE": "foundation/phase-0.json",
        "S-MISSING-DEP-IS-CUSTODY": "foundation/phase-0.json",
        "S-PROFILE-CURRENT": "foundation/phase-0.json",
        "S-CONTINUATION": "foundation/phase-0.json",
        "R-FIVE-CONTRACTS-INDEX": "foundation/phase-0.json",
        "R-SOURCE-MAP-SCOPE": "foundation/phase-0.json",
        "R-CVE1-TYPES-AVAILABLE": "foundation/phase-0.json",
        "R-H-HELPER": "foundation/h-helper.json",
        "R-CVE1-EIGHT-TYPES": "foundation/cve1-eight-types.json",
        "R-LEXICAL-ADMISSION": "foundation/lexical-admission.json",
        "R-SEMANTIC-VS-OPERATIONAL": "foundation/semantic-vs-operational.json",
        "R-RAW-VS-PARSED": "foundation/raw-vs-parsed.json",
        "R-ACYCLIC-JOINS": "foundation/acyclic-joins.json",
        "R-CAP-ADMISSION": "foundation/cap-admission.json",
        "R-CAP-NAMED-GATES": "foundation/cap-named-gates.json",
        "R-TRACE-COMPLETE": "foundation/traces/complete.json",
        "R-TRACE-UNAVAILABLE": "foundation/traces/unavailable.json",
        "R-TRACE-CANCEL": "foundation/traces/cancel.json",
        "R-TRACE-FAULT": "foundation/traces/fault.json",
        "R-TRACE-IDENTITY-BEFORE-SOURCE": "foundation/traces/identity-before-source.json",
        "R-TRACE-TERMINAL": "foundation/traces/terminal.json",
        "R-TRACE-EXECUTED-VS-HOST": "foundation/traces/executed-vs-host.json",
        "R-RELATION-RUNG-TABLE": "foundation/relation-rung-table.json",
        "R-COUNT-CLASS-ATTEMPT": "foundation/count-class-attempt.json",
        "R-CODE-VS-DATA-MATRIX": "foundation/code-vs-data-matrix.json",
        "R-ENUM-VS-RESOLUTION": "foundation/enum-vs-resolution.json",
        "R-ADVERTISED-MODE-PATHS": "foundation/advertised-mode-paths.json",
        "R-IMPORTED-OBSERVATION-BOUNDARY": "foundation/imported-observation-boundary.json",
    },
    "pendingOutsideThisTask": "Phases 5–11 complete Runs, workflow envelopes, query, remaining standalone vectors. Previous other-four-Runs verdict remains a recheck request.",
}
dump("id-mapping.json", mapping)
dump(
    "helper-corrections.json",
    [
        {
            "id": "R-H-HELPER",
            "originalFailure": "Historical h-helper snapshot used an invented sourceInventory object {schemaVersion,entries} rather than identity-schemas.v3 source-inventory (Blob array).",
            "selector": "identity-schemas.v3.json#/$defs/snapshot and #/$defs/source-inventory",
            "change": "Exhibit inhabits the published snapshot record under foundation/h-helper.json.",
        },
        {
            "id": "R-SEMANTIC-VS-OPERATIONAL",
            "originalFailure": "After scope-v2 overwrite, vectors/semantic-vs-operational.json retained only a two-sentence distinct:true claim without measured H.",
            "selector": "identity-and-evidence.md §2–3; identity-schemas.v3.json#/$defs/snapshot and #/$defs/run",
            "change": "Paired H(snapshot) on schema-valid records; operational IDs omitted from the recipe and refused if stuffed into run.",
        },
        {
            "id": "R-ACYCLIC-JOINS",
            "originalFailure": "Historical acyclic vector used view.factIds/schemaDigest (not facts/schemaDigests) and hashed non-schema snapshots.",
            "selector": "identity-schemas.v3.json#/$defs/view, proof-bundle, semantic-evidence, evaluation-seal, run",
            "change": "Chain members inhabit published records; cycle is additionalProperties refusal of proof.evidenceId.",
        },
        {
            "id": "R-CAP-NAMED-GATES",
            "originalFailure": "Historical helper walked ADM-CLOSED before ADM-TYPE.",
            "selector": "capability-manifest-domains.v2.json gateOrder",
            "change": "Four-pass admit(); combined boolean-schemaVersion plus extra-key first-refuses ADM-TYPE.",
        },
        {
            "id": "R-IMPORTED-OBSERVATION-BOUNDARY",
            "originalFailure": "vectors/imported-observation-boundary.json after scope-v2 was a mayProve/mayNotProve list with no retained import2 record.",
            "selector": "identity-schemas.v3.json#/$defs/import; imported-evidence.schema.json#/$defs/RuntimePayloadV1",
            "change": "Retained C(RuntimePayloadV1) and H(import, ImportedEvidenceRecordV2). Explicitly not fact2.",
        },
    ],
)

frozen = freeze_check()
arts = sorted(p for p in FOUND.rglob("*.json") if p.name != "reconstruction-results.json")
art_hashes = [sha_file(p) for p in arts]
dump(
    "reconstruction-results.json",
    {
        "command": "/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-team-foundation-corrections.v1/output/scripts/foundation_reconstruct.py",
        "exit": 0,
        "frozenThisPass": frozen,
        "artifacts": art_hashes,
    },
)

print(json.dumps({"ok": True, "nArtifacts": len(art_hashes), "nIds": len(mapping["ids"])}, indent=2))
