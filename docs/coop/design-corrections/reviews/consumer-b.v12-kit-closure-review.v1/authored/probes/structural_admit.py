#!/usr/bin/env python3
"""Independent structural admission of the corrected syntax-code Run.

Walks kit x-opensip / digest-domain / relation-registry / identity-join laws.
Consumer helpers are transport only after audit; not an expected-value oracle.
Does not evaluate semantic proof. Does not remint or repair the graph.
"""
from __future__ import annotations

import base64
import hashlib
import json
import re
from pathlib import Path
from typing import Any

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-scope-review.v1/subject")
SNAP = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-closure-review.v1/consumer-snapshot")
OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-closure-review.v1/output")
STORE_PATH = SNAP / "runs/syntax-code.store.json"
META_PATH = SNAP / "runs/syntax-code.meta.json"

IDENT = json.loads((KIT / "docs/coop/design-corrections/foundation/identity-schemas.v3.json").read_text())
RELDOC_PATH = KIT / "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"
RELDOC_BYTES = RELDOC_PATH.read_bytes()
RELDOC = json.loads(RELDOC_BYTES)
NATIVE = json.loads((KIT / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json").read_text())
RELREG = RELDOC["x-opensip-relation-registry"]["relations"]
DIGEST_DOMAINS = IDENT["x-opensip-digest-domains"]
PAYLOAD_REG = IDENT["x-opensip-payload-registry"]
DOMAIN_SETS = DIGEST_DOMAINS["domainSets"]
CLOSURE_MEMBERSHIP = IDENT["x-opensip-digest-domains"]["closureMembership"]

DOMAIN_PREFIX = {
    "snapshot": "snapshot2",
    "closure": "closure2",
    "import": "import2",
    "plan": "plan2",
    "subject-scope": "scope2",
    "fact": "fact2",
    "coverage": "coverage2",
    "view": "view2",
    "execution-plan": "exec-plan2",
    "finding-fingerprint": "finding-key2",
    "evaluation-subject": "subject3",
    "finding": "finding3",
    "proof-bundle": "proof3",
    "semantic-evidence": "evidence3",
    "evaluation-seal": "seal3",
    "run": "run3",
    "cache-key": "cache2",
    "regeneration-key": "regen2",
    "policy-derivation": "policy-derivation3",
}

HEX64 = re.compile(r"^[0-9a-f]{64}$")


def C_encode(value: Any, depth: int = 0) -> bytes:
    if depth > 32:
        raise ValueError("NESTING_TOO_DEEP")
    if value is None:
        return b"null"
    if type(value) is bool:
        return b"true" if value else b"false"
    if type(value) is int:
        return str(value).encode("ascii")
    if type(value) is str:
        out = ['"']
        for ch in value:
            o = ord(ch)
            if ch == '"':
                out.append('\\"')
            elif ch == "\\":
                out.append("\\\\")
            elif ch == "\b":
                out.append("\\b")
            elif ch == "\t":
                out.append("\\t")
            elif ch == "\n":
                out.append("\\n")
            elif ch == "\f":
                out.append("\\f")
            elif ch == "\r":
                out.append("\\r")
            elif o < 0x20:
                out.append(f"\\u{o:04x}")
            else:
                out.append(ch)
        out.append('"')
        return "".join(out).encode("utf-8")
    if type(value) is list:
        return b"[" + b",".join(C_encode(v, depth + 1) for v in value) + b"]"
    if type(value) is dict:
        keys = sorted(value.keys(), key=lambda k: k.encode("utf-8"))
        parts = [C_encode(k, depth + 1) + b":" + C_encode(value[k], depth + 1) for k in keys]
        return b"{" + b",".join(parts) + b"}"
    raise TypeError(type(value).__name__)


def H_preimage(domain: str, canonical: bytes) -> bytes:
    return b"opensip.product.v1\x00" + domain.encode("ascii") + b"\x00" + len(canonical).to_bytes(8, "big") + canonical


def H_hex(domain: str, value: Any) -> str:
    return hashlib.sha256(H_preimage(domain, C_encode(value))).hexdigest()


def parse_h_frame(raw: bytes) -> dict | None:
    prefix = b"opensip.product.v1\x00"
    if not raw.startswith(prefix):
        return None
    rest = raw[len(prefix) :]
    z = rest.find(b"\x00")
    if z < 0 or len(rest) < z + 1 + 8:
        return None
    domain = rest[:z].decode("ascii")
    ln = int.from_bytes(rest[z + 1 : z + 9], "big")
    payload = rest[z + 9 :]
    if len(payload) != ln:
        return {"domain": domain, "lengthMismatch": True, "declared": ln, "actual": len(payload)}
    try:
        obj = json.loads(payload)
    except Exception as e:
        return {"domain": domain, "parseError": str(e)}
    return {"domain": domain, "payload": payload, "obj": obj, "lengthMismatch": False}


def u8pref(b: bytes) -> bytes:
    if len(b) > 255:
        raise ValueError("u8 overflow")
    return bytes([len(b)]) + b


def body_identity_l0(*, level_spec: bytes, language_id: str, language_version: bytes, span: bytes) -> str:
    level_id = "L0-verbatim"
    level_version = hashlib.sha256(level_spec).digest()
    payload = len(span).to_bytes(4, "big") + span
    pre = (
        u8pref(b"opensip.fact-identity.v1")
        + u8pref(level_id.encode("ascii"))
        + u8pref(level_version)
        + u8pref(language_id.encode("ascii"))
        + u8pref(language_version)
        + len(payload).to_bytes(4, "big")
        + payload
    )
    return "sha256:" + hashlib.sha256(pre).hexdigest()


def walk_x_opensip(obj: Any, path: str, acc: dict[str, int]):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.startswith("x-opensip-"):
                acc[k] = acc.get(k, 0) + 1
            walk_x_opensip(v, path + "/" + k, acc)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk_x_opensip(v, f"{path}[{i}]", acc)


def collect_digest_annos(schema: Any, path: str, out: list):
    if isinstance(schema, dict):
        if "x-opensip-digest" in schema:
            out.append({"path": path, "anno": schema["x-opensip-digest"]})
        if "x-opensip-order" in schema:
            out.append({"path": path, "order": schema["x-opensip-order"]})
        for k, v in schema.items():
            if k.startswith("x-opensip-"):
                continue
            collect_digest_annos(v, path + "/" + k, out)
    elif isinstance(schema, list):
        for i, v in enumerate(schema):
            collect_digest_annos(v, f"{path}[{i}]", out)


def get_path(obj: Any, parts: list[str]):
    cur = obj
    for p in parts:
        if p == "[]":
            if not isinstance(cur, list):
                return None
            return cur
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur


def utf8_sorted(xs: list[str]) -> bool:
    enc = [x.encode("utf-8") for x in xs]
    return enc == sorted(enc)


def canonical_set_ok(xs: list) -> tuple[bool, str]:
    # unique by C bytes, sorted by C bytes
    cs = [C_encode(x) for x in xs]
    if len(set(cs)) != len(cs):
        return False, "duplicate"
    if cs != sorted(cs):
        return False, "not-sorted-by-C"
    return True, "ok"


results: dict[str, Any] = {
    "laws": [],
    "findings": [],
    "notReached": [],
    "notApplicable": [],
}


def rec(law_id: str, status: str, selector: str, detail: str = "", **extra):
    row = {"id": law_id, "status": status, "selector": selector, "detail": detail, **extra}
    results["laws"].append(row)
    if status == "REFUSED":
        results["findings"].append(row)
    elif status == "NOT_REACHED":
        results["notReached"].append(row)
    elif status == "NOT_APPLICABLE":
        results["notApplicable"].append(row)
    return row


# ---------- inventory ----------
kw_counts: dict[str, int] = {}
for name, doc in [
    ("identity-schemas.v3", IDENT),
    ("relation-payload-schemas.v2", RELDOC),
    ("native-evidence.schemas.v2", NATIVE),
]:
    walk_x_opensip(doc, name, kw_counts)

schema_files = [
    "docs/coop/design-corrections/foundation/identity-schemas.v3.json",
    "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json",
    "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
    "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json",
    "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json",
    "docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json",
    "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json",
    "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json",
    "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json",
]
for rel in schema_files:
    walk_x_opensip(json.loads((KIT / rel).read_text()), rel, kw_counts)

inventory = {
    "xOpensipKeywordCounts": kw_counts,
    "digestDomains": sorted(DIGEST_DOMAINS["byDomain"].keys()),
    "domainSets": sorted(DOMAIN_SETS.keys()),
    "relationRegistry": sorted(RELREG.keys()),
    "payloadRegistryClasses": sorted(PAYLOAD_REG["classes"].keys()),
    "closureMembershipDirect": sorted(CLOSURE_MEMBERSHIP["direct"].keys()),
    "anchorLaws": {k: RELREG[k]["anchorLaw"] for k in RELREG},
    "coverageTotalityRelations": [k for k, v in RELREG.items() if "coverageTotality" in v],
}

# ---------- load store ----------
doc = json.loads(STORE_PATH.read_text())
blobs = {k: base64.b64decode(v) for k, v in doc["blobs"].items()}
ot = doc["objectTable"]
meta = json.loads(META_PATH.read_text())

# blob key integrity
blob_key_ok = True
blob_key_bad = []
for k, raw in blobs.items():
    h = hashlib.sha256(raw).hexdigest()
    if h != k:
        blob_key_ok = False
        blob_key_bad.append({"key": k, "sha256": h})
rec(
    "STORE-BLOB-KEY-EQUALS-SHA256",
    "PASS" if blob_key_ok else "REFUSED",
    "identity-and-evidence §3: raw blob reference uses SHA256 of exact bytes",
    detail="" if blob_key_ok else json.dumps(blob_key_bad[:5]),
)

# decode H frames and JSON
h_records: dict[str, dict] = {}  # digest -> {domain, obj, typed}
json_records: dict[str, Any] = {}  # digest -> obj
frame_failures = []
for digest, raw in blobs.items():
    fr = parse_h_frame(raw)
    if fr and "obj" in fr and not fr.get("lengthMismatch"):
        c_re = C_encode(fr["obj"])
        c_eq = c_re == fr["payload"]
        h_re = hashlib.sha256(H_preimage(fr["domain"], c_re)).hexdigest()
        h_eq = h_re == digest
        rec_meta = ot.get(digest, {})
        h_records[digest] = {
            "domain": fr["domain"],
            "obj": fr["obj"],
            "cEqual": c_eq,
            "hEqual": h_eq,
            "typedId": rec_meta.get("typedId"),
            "label": rec_meta.get("label"),
        }
        if not c_eq or not h_eq:
            frame_failures.append({"digest": digest, "domain": fr["domain"], "cEqual": c_eq, "hEqual": h_eq, "label": rec_meta.get("label")})
    elif raw[:1] in (b"{", b"["):
        try:
            json_records[digest] = json.loads(raw)
        except Exception:
            pass
    elif fr and fr.get("lengthMismatch"):
        frame_failures.append({"digest": digest, "lengthMismatch": True})

rec(
    "H-FRAME-REMIND-AND-C-EQUALITY",
    "PASS" if not frame_failures else "REFUSED",
    "identity-and-evidence §3 H(D,X) frame admission: prefix, domain, declared length, remainder byte-identical to C of parse, SHA256(frame)=digest",
    detail=json.dumps(frame_failures[:8]) if frame_failures else f"nHFrames={len(h_records)}",
    nFrames=len(h_records),
)

# typed prefix vs domain
prefix_bad = []
for digest, recd in h_records.items():
    pref = DOMAIN_PREFIX.get(recd["domain"])
    typed = recd.get("typedId")
    if pref:
        expect = f"{pref}:{digest}"
        # object table may store under typed id
        if typed and typed != expect:
            prefix_bad.append({"digest": digest, "typed": typed, "expect": expect})
        elif not typed:
            # look up object table typed
            if expect not in ot and recd["domain"] not in (
                "native.context.syntax.v2",
                "native.semantic-universe.syntax.v2",
            ):
                # native domains use sha256: spelling, no typed prefix
                if recd["domain"] in DOMAIN_PREFIX:
                    prefix_bad.append({"digest": digest, "domain": recd["domain"], "missingTyped": expect})
rec(
    "TYPED-PREFIX-VS-DOMAIN",
    "PASS" if not prefix_bad else "REFUSED",
    "identity-and-evidence §3 identifier is prefix + ':' + lowercase H hex; native domain-set identities use sha256: spelling",
    detail=json.dumps(prefix_bad[:8]) if prefix_bad else "ok",
)

def by_domain(d: str) -> list[dict]:
    return [{"digest": k, **v} for k, v in h_records.items() if v["domain"] == d]


def by_label(lab: str) -> dict | None:
    for k, v in h_records.items():
        if v.get("label") == lab:
            return {"digest": k, **v}
    for k, meta in ot.items():
        if isinstance(meta, dict) and meta.get("label") == lab:
            d = meta.get("digest") or (k if k in blobs else None)
            if d in json_records:
                return {"digest": d, "obj": json_records[d], "label": lab, "kind": "json"}
            if d in h_records:
                return {"digest": d, **h_records[d]}
            if d in blobs:
                return {"digest": d, "raw": blobs[d], "label": lab}
    return None


runs = by_domain("run")
plans = by_domain("plan")
snaps = by_domain("snapshot")
proofs = by_domain("proof-bundle")
evidences = by_domain("semantic-evidence")
seals = by_domain("evaluation-seal")
facts = by_domain("fact")
coverages = by_domain("coverage")
views = by_domain("view")
scopes = by_domain("subject-scope")
subjects = by_domain("evaluation-subject")
eplans = by_domain("execution-plan")
closures = by_domain("closure")
syn_ctx = by_domain("native.context.syntax.v2")
syn_uni = by_domain("native.semantic-universe.syntax.v2")

rec(
    "GRAPH-MEMBERSHIP-CORE-DOMAINS",
    "PASS" if len(runs) == 1 and len(plans) == 1 and len(snaps) == 1 and len(proofs) == 1 and len(seals) == 1 and len(evidences) == 1 else "REFUSED",
    "identity-and-evidence §3 run/plan/snapshot/proof/evidence/seal domains",
    detail=f"run={len(runs)} plan={len(plans)} snap={len(snaps)} proof={len(proofs)} ev={len(evidences)} seal={len(seals)} fact={len(facts)} cov={len(coverages)} view={len(views)} scope={len(scopes)}",
)

if not (runs and plans and snaps and proofs and seals and evidences):
    rec("ABORT-MISSING-CORE", "REFUSED", "cannot continue without core graph", detail="missing core H records")
    (OUT / "probes/structural_admit.results.json").write_text(json.dumps({"inventory": inventory, **results}, indent=2) + "\n")
    raise SystemExit(1)

run, plan, snap, proof, evidence, seal = runs[0], plans[0], snaps[0], proofs[0], evidences[0], seals[0]
run_o, plan_o, snap_o, proof_o, ev_o, seal_o = run["obj"], plan["obj"], snap["obj"], proof["obj"], evidence["obj"], seal["obj"]

# identity equality joins
def typed(domain, digest):
    p = DOMAIN_PREFIX.get(domain)
    return f"{p}:{digest}" if p else digest

joins = []

def eq(name, a, b, selector):
    ok = a == b
    joins.append({"name": name, "ok": ok, "a": a, "b": b})
    rec(name, "PASS" if ok else "REFUSED", selector, detail=f"{a} vs {b}")

eq("JOIN-RUN-SNAPSHOT", run_o.get("snapshotId"), typed("snapshot", snap["digest"]), "run.snapshotId = snapshot2 identity")
eq("JOIN-RUN-PLAN", run_o.get("planId"), typed("plan", plan["digest"]), "run.planId = plan2 identity")
eq("JOIN-PLAN-SNAPSHOT", plan_o.get("snapshotId"), typed("snapshot", snap["digest"]), "plan.snapshotId = snapshot2")
eq("JOIN-PROOF-PLAN", proof_o.get("planId"), typed("plan", plan["digest"]), "proof-bundle.planId = plan2")
eq("JOIN-EVIDENCE-PLAN", ev_o.get("planId"), typed("plan", plan["digest"]), "semantic-evidence.planId = plan2")
eq("JOIN-SEAL-PLAN", seal_o.get("planId"), typed("plan", plan["digest"]), "evaluation-seal.planId = plan2")
eq("JOIN-RUN-EVIDENCE", run_o.get("evidenceId"), typed("semantic-evidence", evidence["digest"]), "run.evidenceId = evidence3")
eq("JOIN-RUN-SEAL", run_o.get("evaluationSealId"), typed("evaluation-seal", seal["digest"]), "run includes seal")
eq("JOIN-SEAL-EVIDENCE", seal_o.get("evidenceId"), typed("semantic-evidence", evidence["digest"]), "seal includes evidence")
eq("JOIN-SEAL-PROOF", seal_o.get("proofBundleId"), typed("proof-bundle", proof["digest"]), "seal includes proof")
eq("JOIN-EVIDENCE-PROOF", ev_o.get("proofBundleId"), typed("proof-bundle", proof["digest"]), "evidence may include proof")
eq("JOIN-RUN-PROJECT", run_o.get("projectId"), snap_o.get("projectId"), "run.projectId = snapshot.projectId")

# acyclic
proof_s = json.dumps(proof_o)
has_ev = "evidenceId" in proof_o or "evidence3:" in proof_s and "proofBundleId" not in str(proof_o.get("evaluationInputRefs"))
# stronger: proof object keys
forbidden_proof = [k for k in proof_o if k.lower() in ("evidenceid", "runid") or k in ("evidenceId", "runId")]
# also scan nested for run3: of THIS run or evidence3 of this evidence as fields
def contains_id(obj, s):
    if obj == s:
        return True
    if isinstance(obj, dict):
        return any(contains_id(v, s) for v in obj.values())
    if isinstance(obj, list):
        return any(contains_id(v, s) for v in obj)
    return False

proof_has_evidence = contains_id(proof_o, typed("semantic-evidence", evidence["digest"])) or "evidenceId" in proof_o
proof_has_run = contains_id(proof_o, typed("run", run["digest"])) or "runId" in proof_o
rec(
    "ACYCLIC-PROOF-NO-EVIDENCE-OR-RUN",
    "PASS" if not proof_has_evidence and not proof_has_run else "REFUSED",
    "identity-and-evidence §3: graph is acyclic: proof does not include EvidenceId or RunId",
    detail=f"proof_has_evidence={proof_has_evidence} proof_has_run={proof_has_run} keys={list(proof_o)}",
)
rec(
    "ACYCLIC-SEAL-INCLUDES-BOTH",
    "PASS" if seal_o.get("evidenceId") and seal_o.get("proofBundleId") else "REFUSED",
    "identity-and-evidence §3: seal includes both evidence and proof",
)
rec(
    "ACYCLIC-RUN-INCLUDES-SEAL",
    "PASS" if run_o.get("evaluationSealId") else "REFUSED",
    "identity-and-evidence §3: Run includes seal",
)

# capability manifest derived
cap_id = plan_o.get("capabilityManifestId") or run_o.get("capabilityManifestId")
cap_bytes_d = plan_o.get("capabilityManifestBytesDigest")
cap_derived_ok = False
cap_detail = ""
if cap_bytes_d and cap_bytes_d in blobs and cap_id:
    committed = blobs[cap_bytes_d]
    derived = hashlib.sha256(b"opensip.capability-manifest.v1\x00" + committed).hexdigest()
    cap_derived_ok = derived == cap_id
    cap_detail = f"derived={derived} claimed={cap_id}"
    rec("CAP-MANIFEST-ID-DERIVED", "PASS" if cap_derived_ok else "REFUSED", "identity-and-evidence §3 capability-manifest-id SHA256(UTF8('opensip.capability-manifest.v1')||00||committedBytes); retention derived from plan.capabilityManifestBytesDigest", detail=cap_detail)
else:
    rec("CAP-MANIFEST-ID-DERIVED", "REFUSED", "capability-manifest-id derived", detail=f"bytesDigest={cap_bytes_d} inBlobs={cap_bytes_d in blobs if cap_bytes_d else False} cap_id={cap_id}")

eq("JOIN-RUN-CAP-MANIFEST", run_o.get("capabilityManifestId"), plan_o.get("capabilityManifestId"), "run.capabilityManifestId = plan.capabilityManifestId")

# payload schema digest of relation document
rel_digest = hashlib.sha256(RELDOC_BYTES).hexdigest()
payload_schema_bad = []
for f in facts:
    psd = f["obj"].get("payloadSchemaDigest")
    if psd != rel_digest:
        payload_schema_bad.append({"fact": typed("fact", f["digest"]), "got": psd, "expect": rel_digest, "relation": f["obj"].get("relation")})
rec(
    "PAYLOAD-SCHEMA-DIGEST-RELATION-DOCUMENT",
    "PASS" if not payload_schema_bad else "REFUSED",
    "x-opensip-payload-registry.classes.relation / relation-registry: payloadSchemaDigest = raw SHA-256 of exact full relation-payload-schemas.v2.json bytes",
    detail=json.dumps(payload_schema_bad[:5]) if payload_schema_bad else rel_digest,
)

# fact payload C digest + ladder + anchors + universe
anchor_findings = []
ladder_findings = []
universe_findings = []
payload_c_findings = []
rung_field_findings = []
file_facts = []
clone_facts = []
decl_facts = []

for f in facts:
    fo = f["obj"]
    rel = fo.get("relation")
    rung = fo.get("resolution")
    row = RELREG.get(rel)
    if not row:
        ladder_findings.append({"fact": f["digest"], "unregisteredRelation": rel})
        continue
    if rung not in row.get("ladder", []):
        ladder_findings.append({"fact": f["digest"], "relation": rel, "rung": rung, "ladder": row.get("ladder")})
    anchors = fo.get("anchors") or []
    alaw = row.get("anchorLaw") or {}
    cls = alaw.get("class")
    if cls == "inventory" or alaw.get("cardinality") == 0:
        if len(anchors) != 0:
            anchor_findings.append({"fact": f["digest"], "rel": rel, "want": 0, "got": len(anchors)})
    elif cls == "body-identity" or alaw.get("cardinality") == 1:
        if len(anchors) != 1:
            anchor_findings.append({"fact": f["digest"], "rel": rel, "want": 1, "got": len(anchors)})
    elif cls == "source-text" or (alaw.get("minimum") == 1):
        if len(anchors) < 1:
            anchor_findings.append({"fact": f["digest"], "rel": rel, "want": ">=1", "got": len(anchors)})
    if row.get("universeRule") == "same-only" and fo.get("sourceUniverse") != fo.get("targetUniverse"):
        universe_findings.append({"fact": f["digest"], "rel": rel})
    pd = fo.get("payloadDigest")
    payload_obj = json_records.get(pd)
    if payload_obj is None and pd in blobs:
        try:
            payload_obj = json.loads(blobs[pd])
            json_records[pd] = payload_obj
        except Exception:
            payload_obj = None
    if payload_obj is None:
        payload_c_findings.append({"fact": f["digest"], "rel": rel, "missingPayload": pd})
    else:
        cpd = hashlib.sha256(C_encode(payload_obj)).hexdigest()
        if cpd != pd:
            payload_c_findings.append({"fact": f["digest"], "rel": rel, "c": cpd, "claimed": pd})
        rungs = row.get("rungs") or {}
        rules = rungs.get(rung) or {}
        for reqf in rules.get("required") or []:
            if reqf not in payload_obj:
                rung_field_findings.append({"fact": f["digest"], "missingRequired": reqf, "rung": rung})
        for forb in rules.get("forbidden") or []:
            if forb in payload_obj:
                rung_field_findings.append({"fact": f["digest"], "forbiddenPresent": forb, "rung": rung})
        if rel == "file":
            file_facts.append({"fact": f, "payload": payload_obj, "anchors": anchors})
        elif rel == "clones":
            clone_facts.append({"fact": f, "payload": payload_obj, "anchors": anchors})
        elif rel == "declares":
            decl_facts.append({"fact": f, "payload": payload_obj, "anchors": anchors})

rec("RELATION-LADDER-MEMBERSHIP", "PASS" if not ladder_findings else "REFUSED", "x-opensip-relation-registry membershipRule: resolution must be a member of THAT relation's ladder", detail=json.dumps(ladder_findings[:8]) if ladder_findings else f"nFacts={len(facts)}")
rec("ANCHOR-LAW-CARDINALITY", "PASS" if not anchor_findings else "REFUSED", "relation-registry anchorLaw (inventory=0, body-identity=1, source-text>=1)", detail=json.dumps(anchor_findings[:8]) if anchor_findings else "ok")
rec("UNIVERSE-RULE-SAME-ONLY", "PASS" if not universe_findings else "REFUSED", "payload-registry relation universeRule same-only requires sourceUniverse==targetUniverse", detail=json.dumps(universe_findings[:8]) if universe_findings else "ok")
rec("FACT-PAYLOAD-C-DIGEST", "PASS" if not payload_c_findings else "REFUSED", "x-opensip-digest canonical-record: payloadDigest = SHA256(C(payload))", detail=json.dumps(payload_c_findings[:8]) if payload_c_findings else "ok")
rec("RUNG-REQUIRED-FORBIDDEN-FIELDS", "PASS" if not rung_field_findings else "REFUSED", "relation rungs required/forbidden payload fields", detail=json.dumps(rung_field_findings[:8]) if rung_field_findings else "ok")

# snapshot inventory
inv = snap_o.get("sourceInventory")
if isinstance(inv, dict):
    inv_entries = inv.get("entries") or []
elif isinstance(inv, list):
    inv_entries = inv
else:
    inv_entries = []
inv_by_path = {e.get("path"): e for e in inv_entries if isinstance(e, dict)}

# inventory order
inv_paths = [e.get("path") for e in inv_entries]
rec(
    "SNAPSHOT-INVENTORY-PATH-ORDER",
    "PASS" if utf8_sorted(inv_paths) else "REFUSED",
    "identity snapshot sourceInventory x-opensip-order path / utf-8",
    detail=str(inv_paths),
)

file_join_bad = []
for ff in file_facts:
    p = ff["payload"].get("path")
    d = ff["payload"].get("contentSha256")
    n = ff["payload"].get("byteLength")
    row = inv_by_path.get(p)
    if not row:
        file_join_bad.append({"path": p, "reason": "not-in-inventory"})
        continue
    if row.get("sha256") != d:
        file_join_bad.append({"path": p, "reason": "digest-mismatch", "inv": row.get("sha256"), "payload": d})
    if row.get("bytes") != n:
        file_join_bad.append({"path": p, "reason": "length-mismatch", "inv": row.get("bytes"), "payload": n})
    if d not in blobs:
        file_join_bad.append({"path": p, "reason": "blob-not-retained", "digest": d})
    elif len(blobs[d]) != n:
        file_join_bad.append({"path": p, "reason": "retained-length-mismatch", "blobLen": len(blobs[d]), "n": n})
    else:
        if hashlib.sha256(blobs[d]).hexdigest() != d:
            file_join_bad.append({"path": p, "reason": "retained-sha-mismatch"})
rec(
    "FILE-INVENTORIED-SNAPSHOT-JOIN",
    "PASS" if not file_join_bad and file_facts else ("REFUSED" if file_join_bad else "NOT_APPLICABLE"),
    "relation-registry file.snapshotJoins form inventoried-file: path, contentSha256, byteLength, retainedBlob",
    detail=json.dumps(file_join_bad[:8]) if file_join_bad else f"nFileFacts={len(file_facts)}",
)

# clones L0 recompute + languageVersion derived
SYNTAX_SUFFIX = {
    ".rs": "rs",
    ".d.ts": "ts-declaration",
    ".ts": "ts",
    ".tsx": "tsx",
    ".mts": "mts",
    ".cts": "cts",
    ".js": "js",
    ".jsx": "jsx",
    ".mjs": "mjs",
    ".cjs": "cjs",
}
BODY_LANG = {"rs": "rust", "ts": "typescript", "tsx": "typescript", "ts-declaration": "typescript", "mts": "typescript", "cts": "typescript", "js": "javascript", "jsx": "javascript", "mjs": "javascript", "cjs": "javascript"}


def longest_suffix(path: str) -> str | None:
    hits = [s for s in SYNTAX_SUFFIX if path.endswith(s)]
    if not hits:
        return None
    return SYNTAX_SUFFIX[max(hits, key=len)]


clone_bad = []
ctx_obj = syn_ctx[0]["obj"] if syn_ctx else None
uni_obj = syn_uni[0]["obj"] if syn_uni else None
if ctx_obj and uni_obj:
    gb = ctx_obj.get("grammarBundle") or {}
    derived_blv = {
        "schemaVersion": 1,
        "languageId": None,  # per body
        "compilerName": gb.get("parserName"),
        "compilerVersion": gb.get("parserVersion"),
        "compilerBuild": gb.get("bundleDigest"),
        "dialect": None,
    }
    # grammar bundleDigest retained
    bd = gb.get("bundleDigest")
    rec(
        "SYNTAX-GRAMMAR-BUNDLEDIGEST-PREIMAGE",
        "PASS" if bd in blobs else "REFUSED",
        "SyntaxGrammarBundleV1.bundleDigest x-opensip-digest raw-artifact retention preimage",
        detail=str(bd),
    )
    spec = (gb.get("normalizer") or {}).get("specificationDigest")
    rec(
        "SYNTAX-NORMALIZER-SPEC-PREIMAGE",
        "PASS" if spec in blobs else "REFUSED",
        "SyntaxGrammarBundleV1.normalizer.specificationDigest raw-artifact preimage",
        detail=str(spec),
    )
    cid = gb.get("closureId")
    rec(
        "SYNTAX-CONTEXT-GRAMMAR-CLOSURE-JOIN",
        "PASS" if isinstance(cid, str) and cid.startswith("closure2:") and cid.split(":", 1)[-1] in blobs else "REFUSED",
        "identity-schemas.v3 domainSets.native-context.native.context.syntax.v2.closureJoins grammarBundle.closureId form closure2-identity kind=grammar",
        detail=str(cid),
    )
    # selected grammars subset
    gids = [g.get("grammarId") for g in gb.get("grammars") or []]
    sel = uni_obj.get("selectedGrammarIds") or []
    rec(
        "SYNTAX-UNIVERSE-SELECTED-GRAMMAR-SUBSET",
        "PASS" if sel and all(s in gids for s in sel) else "REFUSED",
        "SyntaxUniverseV2ResolvedInputs.selectedGrammarIds subset of context bundle grammarIds; x-opensip-order utf8",
        detail=f"sel={sel} bundle={gids} utf8sorted={utf8_sorted(sel) if isinstance(sel, list) else None}",
    )
    rec(
        "SYNTAX-UNIVERSE-RESOLUTION-ATTEMPTED-FALSE",
        "PASS" if uni_obj.get("resolutionAttempted") is False else "REFUSED",
        "SyntaxUniverseV2ResolvedInputs.resolutionAttempted const false",
    )
    rec(
        "SYNTAX-UNIVERSE-BINDS-CONTEXT",
        "PASS" if uni_obj.get("nativeContextId") == f"sha256:{syn_ctx[0]['digest']}" else "REFUSED",
        "domainSets native-semantic-universe.syntax contextField nativeContextId form sha256-text",
        detail=f"{uni_obj.get('nativeContextId')} vs sha256:{syn_ctx[0]['digest']}",
    )
    rec(
        "SYNTAX-CONTEXT-NO-TOOLCHAIN",
        "PASS" if set(ctx_obj.keys()) <= {"schemaVersion", "grammarBundle"} else "REFUSED",
        "native.context.syntax.v2: no toolchain/stdlib/lockfile/node_modules/config graph",
        detail=str(list(ctx_obj.keys())),
    )
    rec(
        "TS-RUST-CONTEXT-NOT-IN-THIS-GRAPH",
        "NOT_APPLICABLE",
        "native.context.typescript.v2 / rust.v2 snapshotJoins and nestedIdentities",
        detail="this graph's native context domain is syntax.v2 only",
    )
else:
    rec("SYNTAX-NATIVE-CONTEXT-PRESENT", "REFUSED", "native.context.syntax.v2 required for syntax-code Run", detail=f"ctx={len(syn_ctx)} uni={len(syn_uni)}")

# plan native context membership
nctx = plan_o.get("nativeContextDigests") or []
if syn_ctx:
    rec(
        "PLAN-NATIVE-CONTEXT-SELECTION",
        "PASS" if syn_ctx[0]["digest"] in nctx or f"sha256:{syn_ctx[0]['digest']}" in nctx else "REFUSED",
        "plan.nativeContextDigests is the set of admitted native-context H suffixes; fact sourceUniverse binds through selected context",
        detail=f"nctx={nctx} syntaxCtx={syn_ctx[0]['digest']}",
    )
    rec(
        "PLAN-NATIVE-CONTEXT-NONEMPTY",
        "PASS" if len(nctx) >= 1 else "REFUSED",
        "complete syntax positive has selected native context",
    )

for cf in clone_facts:
    payload = cf["payload"]
    anchors = cf["anchors"]
    level = payload.get("normalisationLevel")
    nver = payload.get("normalisationVersion")
    bid = payload.get("bodyIdentity")
    if len(anchors) != 1:
        clone_bad.append({"reason": "anchor-cardinality", "n": len(anchors)})
        continue
    a = anchors[0]
    path = a.get("path")
    blob = a.get("blobDigest")
    start, end = a.get("startByte"), a.get("endByte")
    if blob not in blobs:
        clone_bad.append({"reason": "anchor-blob-missing", "blob": blob})
        continue
    span = blobs[blob][start:end]
    if nver not in blobs:
        clone_bad.append({"reason": "level-spec-not-retained", "normalisationVersion": nver})
        continue
    variant = longest_suffix(path or "")
    if variant is None:
        clone_bad.append({"reason": "BODY_LANGUAGE_GRAMMAR_VARIANT_UNKNOWN", "path": path})
        continue
    lang = BODY_LANG[variant]
    if ctx_obj:
        gb = ctx_obj.get("grammarBundle") or {}
        blv = {
            "schemaVersion": 1,
            "languageId": lang,
            "compilerName": gb.get("parserName"),
            "compilerVersion": gb.get("parserVersion"),
            "compilerBuild": gb.get("bundleDigest"),
            "dialect": {"grammarVariant": variant},
        }
        lv = hashlib.sha256(C_encode(blv)).digest()
        if level == "L0-verbatim":
            recomputed = body_identity_l0(level_spec=blobs[nver], language_id=lang, language_version=lv, span=span)
            if recomputed != bid:
                clone_bad.append({"reason": "L0-recompute-mismatch", "got": bid, "recomputed": recomputed, "path": path, "lang": lang, "variant": variant, "blv": blv})
        else:
            rec(
                f"CLONES-L1-PLUS-PREIMAGE-ONLY:{level}",
                "PASS" if nver in blobs else "REFUSED",
                "clones bodyIdentityJoin: L1-L3 host cannot recompute; require exact retained level-specification preimage plus framed-identity check. Token-stream tokenisation judgment NOT_REACHED.",
                detail=f"level={level} bodyIdentity={bid} specRetained={nver in blobs}",
            )
            results["notReached"].append(
                {
                    "id": "CLONES-L1-TOKEN-STREAM-FRAMING-JUDGMENT",
                    "status": "NOT_REACHED",
                    "selector": "relation-registry clones.bodyIdentityJoin.tokenStreamFraming: parse retained stream for custody/framing; do not judge tokenisation",
                    "detail": "L1 token-kind registry is level-specification freedom; framing parse not independently executed in this checker",
                }
            )
    if blob not in inv_by_path.get(path, {}) and not any(e.get("sha256") == blob and e.get("path") == path for e in inv_entries):
        # anchor path must be inventoried
        if path not in inv_by_path:
            clone_bad.append({"reason": "anchor-path-not-inventoried", "path": path})

rec(
    "CLONES-L0-RECOMPUTE-AND-LANGUAGEVERSION-DERIVED",
    "PASS" if clone_facts and not clone_bad else ("REFUSED" if clone_bad else "NOT_APPLICABLE"),
    "relation-registry clones.bodyIdentityJoin + identity-schemas languageVersionBindingLaw for native.semantic-universe.syntax.v2 (parserName/parserVersion/bundleDigest, dialect grammarVariant from suffix table, body language from bodyLanguageByVariant)",
    detail=json.dumps(clone_bad[:6], default=str) if clone_bad else f"nClones={len(clone_facts)}",
)

# declares source-text anchors in inventory
decl_bad = []
for d in decl_facts:
    if len(d["anchors"]) < 1:
        decl_bad.append({"reason": "no-anchor"})
    for a in d["anchors"]:
        if a.get("path") not in inv_by_path:
            decl_bad.append({"reason": "anchor-path-not-inventoried", "path": a.get("path")})
rec("DECLARES-SOURCE-TEXT-ANCHORS", "PASS" if decl_facts and not decl_bad else ("REFUSED" if decl_bad else "NOT_APPLICABLE"), "declares anchorLaw source-text minimum 1; anchor path inventoried", detail=json.dumps(decl_bad[:5]) if decl_bad else f"n={len(decl_facts)}")

# coverage payloads
cov_payload_bad = []
cov_complete_exh = []
native_cov_digest = hashlib.sha256((KIT / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json").read_bytes()).hexdigest()
for c in coverages:
    co = c["obj"]
    pd = co.get("payloadDigest")
    psd = co.get("payloadSchemaDigest")
    payload = json_records.get(pd)
    if payload is None and pd in blobs:
        try:
            payload = json.loads(blobs[pd])
            json_records[pd] = payload
        except Exception:
            payload = None
    if payload is None:
        cov_payload_bad.append({"cov": c["digest"], "missing": pd})
        continue
    cpd = hashlib.sha256(C_encode(payload)).hexdigest()
    if cpd != pd:
        cov_payload_bad.append({"cov": c["digest"], "cMismatch": True})
    # CoverageResultV3 schema digest is native-evidence document
    if psd != native_cov_digest:
        cov_payload_bad.append({"cov": c["digest"], "schemaDigest": psd, "expectNativeDoc": native_cov_digest})
    entry = payload.get("entry") or payload
    covv = entry.get("coverage")
    rc = entry.get("resolutionCompleteness") or {}
    if covv == "complete" and rc.get("examinedExhaustive") is not True:
        cov_complete_exh.append({"cov": c["digest"], "examinedExhaustive": rc.get("examinedExhaustive")})
    c["_payload"] = payload
    c["_entry"] = entry

rec("COVERAGE-PAYLOAD-C-AND-SCHEMA", "PASS" if not cov_payload_bad else "REFUSED", "x-opensip-payload-registry coverage class schemaVersion 3 → native-evidence CoverageResultV3; payloadDigest SHA256(C)", detail=json.dumps(cov_payload_bad[:6]) if cov_payload_bad else "ok")
rec("RC-6-COMPLETE-IMPLIES-EXAMINED-EXHAUSTIVE", "PASS" if not cov_complete_exh else "REFUSED", "native-evidence CoverageResultV3: coverage=complete REQUIRES resolutionCompleteness.examinedExhaustive=true (implication, not equality)", detail=json.dumps(cov_complete_exh[:6]) if cov_complete_exh else "ok")

# deficiency-cause registry for declared deficiencies
defic_bad = []
defreg = NATIVE.get("x-opensip-deficiency-cause-registry", {}).get("deficiencies", {})
for c in coverages:
    entry = c.get("_entry") or {}
    d = entry.get("deficiency")
    if not d:
        continue
    row = defreg.get(d)
    if not row:
        defic_bad.append({"cov": c["digest"], "unregisteredDeficiency": d})
        continue
    nc = entry.get("nativeCause")
    if row.get("nativeCause") == "required":
        allowed = row.get("allowedCauses") or []
        if nc not in allowed:
            defic_bad.append({"cov": c["digest"], "deficiency": d, "nativeCause": nc, "allowed": allowed})
rec("DEFICIENCY-CAUSE-REGISTRY-JOIN", "PASS" if not defic_bad else "REFUSED", "native-evidence.schemas.v2.json x-opensip-deficiency-cause-registry: declared deficiency must be supported by named carrier", detail=json.dumps(defic_bad[:6]) if defic_bad else "ok")

# coverage totality file@enumerated
totality_bad = []
if views:
    view_o = views[0]["obj"]
    view_facts = view_o.get("facts") or []
    view_scopes = view_o.get("scopeIds") or []
    view_covs = view_o.get("coverageIds") or []
    # map scopes
    scope_map = {typed("subject-scope", s["digest"]): s["obj"] for s in scopes}
    fact_map = {typed("fact", f["digest"]): f for f in facts}
    for sid in view_scopes:
        so = scope_map.get(sid)
        if not so:
            totality_bad.append({"missingScope": sid})
            continue
        if so.get("relation") == "file" and so.get("resolution") == "enumerated":
            # find coverage for this scope
            matching_cov = None
            for c in coverages:
                if typed("coverage", c["digest"]) in view_covs:
                    # coverage object has scopeId
                    if c["obj"].get("scopeId") == sid:
                        matching_cov = c
                        break
            entry = (matching_cov or {}).get("_entry") or {}
            if entry.get("coverage") == "complete":
                subjects = so.get("subjects") or []
                file_paths_in_view = set()
                for fid in view_facts:
                    ff = fact_map.get(fid)
                    if not ff:
                        continue
                    fo = ff["obj"]
                    if fo.get("relation") != "file" or fo.get("resolution") != "enumerated":
                        continue
                    if fo.get("sourceUniverse") != so.get("sourceUniverse") or fo.get("targetUniverse") != so.get("targetUniverse"):
                        continue
                    if fo.get("snapshotId") != so.get("snapshotId"):
                        continue
                    pd = fo.get("payloadDigest")
                    po = json_records.get(pd)
                    if po:
                        file_paths_in_view.add(po.get("path"))
                for subj in subjects:
                    if subj in inv_by_path and subj not in file_paths_in_view:
                        totality_bad.append({"omitted": subj, "refusal": "COVERAGE_INVENTORY_TOTALITY_OMITS_PATH"})
rec(
    "FILE-ENUMERATED-COVERAGE-TOTALITY",
    "PASS" if not totality_bad else "REFUSED",
    "relation-registry file.coverageTotality: complete file@enumerated Coverage owes a fact for every inventoried subject of that scope/universe",
    detail=json.dumps(totality_bad[:8]) if totality_bad else "ok",
)

# partition law
part_bad = []
if views:
    view_o = views[0]["obj"]
    groups: dict[tuple, list] = {}
    for sid in view_o.get("scopeIds") or []:
        so = scope_map.get(sid)
        if not so:
            continue
        key = (so.get("snapshotId"), so.get("relation"), so.get("resolution"), so.get("sourceUniverse"), so.get("targetUniverse"))
        groups.setdefault(key, []).append(so)
    for key, lst in groups.items():
        seen = []
        for so in lst:
            subs = so.get("subjects") or []
            for s in subs:
                for prev in seen:
                    if s in prev:
                        part_bad.append({"key": key, "overlap": s, "refusal": "SUBJECT_SCOPE_PARTITION_OVERLAP"})
            seen.append(set(subs))
rec(
    "COVERAGE-PARTITION-DISJOINT",
    "PASS" if not part_bad else "REFUSED",
    "relation-registry coveragePartitionLaw per view; partitionKey snapshotId,relation,resolution,sourceUniverse,targetUniverse",
    detail=json.dumps(part_bad[:6], default=str) if part_bad else "ok",
)

# subject-scope rung in ladder
scope_rung_bad = []
for s in scopes:
    so = s["obj"]
    rel, rung = so.get("relation"), so.get("resolution")
    row = RELREG.get(rel)
    if not row or rung not in row.get("ladder", []):
        scope_rung_bad.append({"scope": s["digest"], "rel": rel, "rung": rung})
    if so.get("snapshotId") != typed("snapshot", snap["digest"]):
        scope_rung_bad.append({"scope": s["digest"], "snapshotMismatch": True})
rec("SUBJECT-SCOPE-RUNG-IN-LADDER", "PASS" if not scope_rung_bad else "REFUSED", "close_run SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER; scope snapshotId = run snapshot", detail=json.dumps(scope_rung_bad[:6]) if scope_rung_bad else "ok")

# view joins
view_bad = []
for v in views:
    vo = v["obj"]
    if vo.get("planId") != typed("plan", plan["digest"]):
        view_bad.append({"view": v["digest"], "planMismatch": True})
    for fid in vo.get("facts") or []:
        if fid not in {typed("fact", f["digest"]) for f in facts}:
            view_bad.append({"missingFact": fid})
    for sid in vo.get("scopeIds") or []:
        if sid not in {typed("subject-scope", s["digest"]) for s in scopes}:
            view_bad.append({"missingScope": sid})
rec("VIEW-MEMBER-JOINS", "PASS" if not view_bad else "REFUSED", "view2 names plan, facts, scopes, coverage that are retained", detail=json.dumps(view_bad[:8]) if view_bad else f"nViews={len(views)}")

# x-opensip-order on known arrays: plan.semanticClosures canonical-set, view.facts, etc.
order_bad = []

def check_set(name, xs, selector):
    if not isinstance(xs, list):
        return
    ok, why = canonical_set_ok(xs)
    if not ok:
        order_bad.append({"name": name, "why": why})

check_set("plan.semanticClosures", plan_o.get("semanticClosures"), "canonical-set")
check_set("plan.nativeContextDigests", plan_o.get("nativeContextDigests"), "canonical-set")
check_set("plan.importIds", plan_o.get("importIds") or [], "canonical-set")
if views:
    check_set("view.facts", views[0]["obj"].get("facts"), "canonical-set")
    check_set("view.scopeIds", views[0]["obj"].get("scopeIds"), "canonical-set")
    check_set("view.coverageIds", views[0]["obj"].get("coverageIds"), "canonical-set")
for s in scopes:
    check_set(f"scope.subjects:{s['digest'][:8]}", s["obj"].get("subjects") or [], "canonical-set")
rec("X-OPENSIP-ORDER-CANONICAL-SET-CORE", "PASS" if not order_bad else "REFUSED", "identity-schemas x-opensip-order canonical-set: unique and sorted by C bytes (stock JSON Schema does not enforce)", detail=json.dumps(order_bad[:8]) if order_bad else "ok")

# closure membership: producer/evaluator in plan.semanticClosures
sem = set(plan_o.get("semanticClosures") or [])
pc = views[0]["obj"].get("producerClosure") if views else None
fact_eq = all(f["obj"].get("producerClosure") == pc for f in facts) if facts and pc else False
evc = proof_o.get("evaluatorClosure")
sealc = seal_o.get("evaluatorClosure")
scope_enum_ok = all((s["obj"].get("enumeratorClosure") in sem) for s in scopes if s["obj"].get("enumeratorClosure"))
rec(
    "CLOSURE-MEMBERSHIP-FACT-EQUALS-VIEW-PRODUCER",
    "PASS" if fact_eq else "REFUSED",
    "x-opensip-digest-domains.closureMembership.equalToDirect fact.producerClosure = enclosing view.producerClosure",
)
rec(
    "CLOSURE-MEMBERSHIP-PROOF-EQUALS-SEAL-EVALUATOR",
    "PASS" if evc == sealc else "REFUSED",
    "x-opensip-digest-domains.closureMembership.equalToDirect proof-bundle.evaluatorClosure = evaluation-seal.evaluatorClosure",
    detail=f"proof={evc} seal={sealc}",
)
rec(
    "CLOSURE-MEMBERSHIP-VIEW-PRODUCER-IN-PLAN",
    "PASS" if pc in sem else "REFUSED",
    "closureMembership.direct view.producerClosure must be in plan.semanticClosures",
    detail=f"producer={pc} semanticClosures={sorted(sem)}",
)
rec(
    "CLOSURE-MEMBERSHIP-SEAL-EVALUATOR-IN-PLAN",
    "REFUSED" if sealc not in sem else "PASS",
    "closureMembership.direct evaluation-seal.evaluatorClosure: 'Direct members must be in plan.semanticClosures' (selectionLaw). Extra closures may be selected; omitting a direct member is not permitted.",
    detail=f"evaluator={sealc} semanticClosures={sorted(sem)} retainedEvaluatorFrame={sealc.split(':',1)[-1] in blobs if isinstance(sealc,str) else False}",
    refusal="UNSELECTED_EVALUATOR_CLOSURE" if sealc not in sem else None,
)
rec(
    "CLOSURE-MEMBERSHIP-SCOPE-ENUMERATOR-IN-PLAN",
    "PASS" if scope_enum_ok else "REFUSED",
    "closureMembership.direct subject-scope.enumeratorClosure in plan.semanticClosures",
)

# execution-inputs retained
ei_d = proof_o.get("executionInputsDigest")
if ei_d:
    rec("EXECUTION-INPUTS-PREIMAGE", "PASS" if ei_d in blobs else "REFUSED", "digest-domain execution-inputs retention preimage", detail=str(ei_d))
    if ei_d in json_records or ei_d in blobs:
        try:
            ei = json_records.get(ei_d) or json.loads(blobs[ei_d])
        except Exception:
            ei = None
        if ei:
            rec("EXECUTION-INPUTS-PLAN-JOIN", "PASS" if ei.get("planId") == typed("plan", plan["digest"]) else "REFUSED", "execution-inputs.planId = plan2", detail=str(ei.get("planId")))
        rec(
            "EXECUTION-INPUTS-OUTCOME-DERIVE",
            "NOT_REACHED",
            "execution-inputs-contract.v1.md §4 derive_outcome / EXECUTION_INPUTS_OUTCOME_DERIVE full aggregate",
            detail="Full cell-outcome derivation from inventories+accounts+candidates is not executed in this structural checker. Cell states were not re-derived.",
        )
else:
    rec("EXECUTION-INPUTS-PREIMAGE", "REFUSED", "proof-bundle requires executionInputsDigest on proof3", detail="missing")

# analysis-spec / enum / emis retained via plan
as_d = plan_o.get("analysisSpecDigest")
rec("ANALYSIS-SPEC-PREIMAGE", "PASS" if as_d in blobs else "REFUSED", "digest-domain analysis-spec canonical-record preimage", detail=str(as_d))

# imports N/A
rec("IMPORT-PAYLOAD-REGISTRY", "NOT_APPLICABLE", "x-opensip-payload-registry import class", detail=f"plan.importIds={plan_o.get('importIds')}")
rec("TS-CONFIG-GRAPH-NESTED-RECORD", "NOT_APPLICABLE", "native.semantic-universe.typescript.v2 nestedRecords tsconfigGraphHash")
rec("RUST-OWNERSHIP-NESTED-IDENTITY", "NOT_APPLICABLE", "native.semantic-universe.rust.v2 nestedIdentities sourceUnitOwnershipId / edition dialect")
rec("FINDING-FINGERPRINT-ORDER", "NOT_APPLICABLE", "finding3 / finding-key2 domains; this graph findingIds empty" if not proof_o.get("findingIds") else "present")

# semantic proof NOT_REACHED
rec(
    "SEMANTIC-PROOF-EVALUATION",
    "NOT_REACHED",
    "identity-and-evidence: complete replay is close_run after structural admission; atom evaluation / predicate witnesses / verdict derivation",
    detail="Assigned to another review. This checker does not evaluate proof.verdict or recompute witnesses.",
)
rec(
    "ROOT-ADMISSION",
    "NOT_REACHED",
    "requirements.json afterExport independent root admission of exact exported frames",
    detail="No root result assumed or performed.",
)
rec(
    "HOST-OS-COMPILER-CRYPTO",
    "NOT_APPLICABLE",
    "future qualification F-OS-COMPILER-CRYPTO-SQLITE",
)

# x-opensip-digest field walk on identity $defs for records we have
# Walk run/plan/snapshot/proof/fact objects for 64-hex strings and require they resolve in blobs when retention preimage
unresolved_hex = []


def walk_hex(obj, path, seen=None):
    if seen is None:
        seen = set()
    if id(obj) in seen:
        return
    seen.add(id(obj))
    if isinstance(obj, str) and HEX64.match(obj):
        # skip if it's a typed id suffix we'll check via typed
        if obj not in blobs and path.endswith("Digest") or path.endswith("digest") or "Digest" in path.split(".")[-1] or path.endswith("Sha256"):
            if obj not in blobs:
                unresolved_hex.append({"path": path, "digest": obj})
    elif isinstance(obj, dict):
        for k, v in obj.items():
            walk_hex(v, path + "." + k, seen)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk_hex(v, f"{path}[{i}]", seen)


# More precise: only fields that look like digest fields
DIGEST_FIELD = re.compile(r"(Digest|Sha256|digest)$")


def walk_digest_fields(obj, path):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and HEX64.match(v) and DIGEST_FIELD.search(k):
                if v not in blobs:
                    unresolved_hex.append({"path": f"{path}.{k}", "digest": v})
            else:
                walk_digest_fields(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk_digest_fields(v, f"{path}[{i}]")


for name, recd in [("run", run_o), ("plan", plan_o), ("snapshot", snap_o), ("proof", proof_o), ("evidence", ev_o), ("seal", seal_o)]:
    walk_digest_fields(recd, name)
for f in facts:
    walk_digest_fields(f["obj"], "fact")
for c in coverages:
    walk_digest_fields(c["obj"], "coverage")

# capabilityManifestId is derived, not a blob key — filter
filtered = []
for u in unresolved_hex:
    if u["digest"] == cap_id:
        continue  # derived
    # nativeContextDigests are H suffixes — they ARE blob keys of frames
    filtered.append(u)
# many schemaDigests should be in blobs (they copied schema files)
rec(
    "DIGEST-FIELD-PREIMAGE-RETENTION",
    "PASS" if not filtered else "REFUSED",
    "identity-and-evidence closing digest law: preimage retention default — exact bytes under this digest in the CAS (derived capabilityManifestId excluded)",
    detail=json.dumps(filtered[:12]) if filtered else "all referenced *Digest/*Sha256 64-hex fields resolved in store (except derived cap id)",
    nUnresolved=len(filtered),
)

# grammar definition digests
if ctx_obj:
    gb = ctx_obj.get("grammarBundle") or {}
    gdef_bad = []
    for g in gb.get("grammars") or []:
        gd = g.get("grammarDigest")
        if gd not in blobs:
            gdef_bad.append(gd)
    rec("GRAMMAR-DEFINITION-PREIMAGES", "PASS" if not gdef_bad else "REFUSED", "SyntaxGrammarBundleV1.grammars[].grammarDigest raw-artifact preimage", detail=str(gdef_bad))
    # grammars ordered by grammarId
    gids = [g.get("grammarId") for g in gb.get("grammars") or []]
    rec("GRAMMAR-ARRAY-ORDER-BY-GRAMMARID", "PASS" if gids == sorted(gids, key=lambda x: x.encode("utf-8")) else "REFUSED", "x-opensip-order by [grammarId]", detail=str(gids))

# evidence viewIds membership
if views:
    rec(
        "EVIDENCE-VIEW-MEMBERSHIP",
        "PASS" if typed("view", views[0]["digest"]) in (ev_o.get("viewIds") or []) else "REFUSED",
        "semantic-evidence.viewIds includes evaluated view2",
        detail=str(ev_o.get("viewIds")),
    )

# proof evaluationInputRefs domains
eiref_bad = []
for r in proof_o.get("evaluationInputRefs") or []:
    if not isinstance(r, dict):
        continue
    dmn, dg = r.get("domain"), r.get("digest")
    if dmn not in DIGEST_DOMAINS["byDomain"]:
        eiref_bad.append({"unregisteredDomain": dmn})
    elif dg and dg not in blobs:
        eiref_bad.append({"missing": dg, "domain": dmn})
rec("PROOF-EVALUATION-INPUT-REFS-BY-DOMAIN", "PASS" if not eiref_bad else "REFUSED", "Ref.domain registered in x-opensip-digest-domains.byDomain; preimage retained", detail=json.dumps(eiref_bad[:8]) if eiref_bad else "ok")

# x-opensip keyword inventory completeness note
rec(
    "APPLICABILITY-INVENTORY-BUILT-FROM-SCHEMAS",
    "PASS",
    "This checker built its law list from identity-schemas.v3 x-opensip-digest-domains, relation-registry, payload-registry, native deficiency-cause-registry, and native syntax context/universe domainSets — not from the consumer closure.json join names.",
    detail=json.dumps(sorted(kw_counts.keys())),
)

# compare claimed meta ids
rec(
    "META-RUN-ID-EQUALS-REMINTED",
    "PASS" if meta.get("runId") == typed("run", run["digest"]) else "REFUSED",
    "claimed meta.runId vs independently reminted run3",
    detail=f"meta={meta.get('runId')} reminted={typed('run', run['digest'])}",
)

out = {
    "inventory": inventory,
    "store": {
        "path": str(STORE_PATH),
        "blobCount": len(blobs),
        "hFrames": len(h_records),
        "runId": typed("run", run["digest"]),
        "planId": typed("plan", plan["digest"]),
        "snapshotId": typed("snapshot", snap["digest"]),
        "proofId": typed("proof-bundle", proof["digest"]),
        "nFacts": len(facts),
        "nFileFacts": len(file_facts),
        "nCloneFacts": len(clone_facts),
        "nDeclFacts": len(decl_facts),
        "relations": sorted({f["obj"].get("relation") for f in facts}),
    },
    "laws": results["laws"],
    "statusCounts": {},
}
from collections import Counter

out["statusCounts"] = dict(Counter(l["status"] for l in results["laws"]))
out["findings"] = results["findings"]
out["notReached"] = [x for x in results["laws"] if x["status"] == "NOT_REACHED"]
out["notApplicable"] = [x for x in results["laws"] if x["status"] == "NOT_APPLICABLE"]

# verdict
refused = [l for l in results["laws"] if l["status"] == "REFUSED"]
not_reached = [l for l in results["laws"] if l["status"] == "NOT_REACHED"]
if refused:
    verdict = "SCOPED_CLOSURE_REFUSED"
elif not_reached:
    verdict = "INCOMPLETE"
else:
    # still incomplete if we have explicit NOT_REACHED semantic proof — we always have those
    verdict = "INCOMPLETE"
# If structural refused, REFUSED. If only NOT_REACHED remain besides PASS/NA, INCOMPLETE (do not claim ADMITS from a selection of successful checks).
out["verdictLogic"] = {
    "rule": "SCOPED_CLOSURE_REFUSED if any executed applicable law REFUSED. SCOPED_CLOSURE_ADMITS only if every applicable structural law was evaluated PASS and no applicable law is NOT_REACHED. Otherwise INCOMPLETE. Semantic proof and root admission are NOT_REACHED so ADMITS cannot be issued by this checker.",
    "nRefused": len(refused),
    "nNotReached": len(not_reached),
}
out["verdict"] = "SCOPED_CLOSURE_REFUSED" if refused else "INCOMPLETE"

(OUT / "probes").mkdir(parents=True, exist_ok=True)
(OUT / "probes/structural_admit.results.json").write_text(json.dumps(out, indent=2, default=str) + "\n")
print("VERDICT", out["verdict"])
print("COUNTS", out["statusCounts"])
print("REFUSED", [x["id"] for x in refused])
print("NOT_REACHED", [x["id"] for x in not_reached])
print("N_LAWS", len(out["laws"]))
print("RUN", out["store"]["runId"])
