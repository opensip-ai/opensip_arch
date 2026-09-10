#!/usr/bin/env python3
"""Independent kit-law probes of the consumer snapshot. Not an author oracle."""
from __future__ import annotations

import base64
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-scope-review.v1/subject")
SNAP = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-scope-review.v1/consumer-snapshot")
OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-scope-review.v1/output")

import jsonschema
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

SCHEMA_FILES = [
    "docs/coop/design-corrections/foundation/identity-schemas.v3.json",
    "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
    "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json",
    "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json",
    "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json",
    "docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json",
    "docs/coop/design-corrections/workflows/schemas/common.schema.json",
    "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json",
    "docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json",
    "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json",
    "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json",
    "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json",
    "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json",
    "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json",
    "docs/coop/design-corrections/workflows/schemas/evaluator3/comparison-result.schema.json",
    "docs/coop/design-corrections/workflows/schemas/evaluator3/baseline-artifact.schema.json",
    "docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json",
    "docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json",
    "docs/coop/artifacts/d9-exit-contract.v1.14.json",
]


def load_json(p: Path) -> Any:
    return json.loads(p.read_text())


def kit_doc(rel: str) -> dict:
    return load_json(KIT / rel)


def make_registry() -> Registry:
    resources = []
    for f in SCHEMA_FILES:
        p = KIT / f
        if not p.exists():
            continue
        doc = load_json(p)
        sid = doc.get("$id")
        if sid:
            resources.append((sid, Resource.from_contents(doc)))
    return Registry().with_resources(resources)


REG = make_registry()


def validate(instance: Any, schema_rel: str, selector: str | None = None) -> dict:
    doc = kit_doc(schema_rel)
    if selector:
        if not selector.startswith("#/$defs/"):
            return {"stockOk": False, "errors": [{"message": f"bad selector {selector}"}]}
        name = selector.split("/")[-1]
        schema = doc["$defs"][name]
        val_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": (doc.get("$id") or "urn:local") + "/inline-" + name,
            "$defs": doc.get("$defs", {}),
            **schema,
        }
    else:
        val_schema = doc
    errors = []
    try:
        v = Draft202012Validator(val_schema, registry=REG)
        for e in v.iter_errors(instance):
            errors.append(
                {
                    "path": list(e.absolute_path),
                    "message": e.message,
                    "validator": e.validator,
                }
            )
    except Exception as ex:
        errors.append({"path": [], "message": str(ex), "validator": "setup"})
    return {
        "schema": schema_rel,
        "selector": selector,
        "stockOk": not errors,
        "nErrors": len(errors),
        "errors": errors[:8],
    }


# --- independent C/H from identity-and-evidence §3 (not consumer helper) ---
def C_encode(value: Any, depth: int = 0) -> bytes:
    if depth > 32:
        raise ValueError("nesting")
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
    raise TypeError(type(value))


def H_hex(domain: str, value: Any) -> str:
    cx = C_encode(value)
    pre = b"opensip.product.v1\x00" + domain.encode("ascii") + b"\x00" + len(cx).to_bytes(8, "big") + cx
    return hashlib.sha256(pre).hexdigest()


def body_identity(*, level_id: str, level_spec_bytes: bytes, language_id: str, language_version: bytes, payload: bytes) -> str:
    def u8pref(b: bytes) -> bytes:
        return bytes([len(b)]) + b

    level_version = hashlib.sha256(level_spec_bytes).digest()
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


results: dict[str, Any] = {"probes": [], "failures": []}


def rec(name: str, **kwargs):
    results["probes"].append({"name": name, **kwargs})
    if kwargs.get("ok") is False:
        results["failures"].append(name)


# ========== schema inhabitance ==========
CE = "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json"
GQ = "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json"
CMP = "docs/coop/design-corrections/workflows/schemas/evaluator3/comparison-result.schema.json"
BASE = "docs/coop/design-corrections/workflows/schemas/evaluator3/baseline-artifact.schema.json"
REP = "docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json"
INV = "docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json"
IDENT = "docs/coop/design-corrections/foundation/identity-schemas.v3.json"
NATIVE = "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
COMMON = "docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json"

envelope_files = sorted((SNAP / "envelopes").glob("*.json"))
for p in envelope_files:
    obj = load_json(p)
    r_ce = validate(obj, CE)
    r_st = validate(obj, COMMON, "#/$defs/StepTermination")
    rec(
        f"envelope.CommandEnvelope:{p.name}",
        ok=r_ce["stockOk"],
        nErrors=r_ce["nErrors"],
        firstError=(r_ce["errors"][0]["message"] if r_ce["errors"] else None),
        keys=sorted(obj.keys()) if isinstance(obj, dict) else type(obj).__name__,
        bytes=p.stat().st_size,
    )
    rec(
        f"envelope.StepTermination:{p.name}",
        ok=r_st["stockOk"],
        nErrors=r_st["nErrors"],
        firstError=(r_st["errors"][0]["message"] if r_st["errors"] else None),
    )

# nested receipt/availability
ra = load_json(SNAP / "envelopes/receipt-availability.json")
r_rec = validate(ra.get("receipt"), IDENT, "#/$defs/commit-receipt")
r_av = validate(ra.get("availability"), IDENT, "#/$defs/availability")
r_mut = validate(ra.get("receipt"), REP, "#/$defs/MutationReceiptV1")
rec("receipt-availability.commit-receipt", ok=r_rec["stockOk"], nErrors=r_rec["nErrors"], errors=r_rec["errors"][:3])
rec("receipt-availability.availability", ok=r_av["stockOk"], nErrors=r_av["nErrors"], errors=r_av["errors"][:3])
rec("receipt-availability.MutationReceiptV1", ok=r_mut["stockOk"], nErrors=r_mut["nErrors"], firstError=(r_mut["errors"][0]["message"] if r_mut["errors"] else None))

# public termination examples vs StepTermination
pt = load_json(SNAP / "envelopes/public-termination.json")
term_checks = []
for ex in pt.get("examples", []):
    term_checks.append(validate(ex, COMMON, "#/$defs/StepTermination"))
rec(
    "public-termination.examples-as-StepTermination",
    ok=all(t["stockOk"] for t in term_checks) if term_checks else False,
    per=[(t["stockOk"], t["errors"][:2]) for t in term_checks],
)

# comparison vectors
for name in [
    "comparison-missing.json",
    "comparison-evidence-changed.json",
    "comparison-empty-result.json",
    "comparison-scope-policy-only.json",
    "baseline-audit.json",
    "baseline-e0-e3.json",
    "pivot-only-fingerprints.json",
]:
    obj = load_json(SNAP / "vectors" / name)
    r = validate(obj, CMP)
    rec(f"comparison.ComparisonResult:{name}", ok=r["stockOk"], nErrors=r["nErrors"], firstError=(r["errors"][0]["message"] if r["errors"] else None), keys=sorted(obj.keys()) if isinstance(obj, dict) else None)
    rb = validate(obj, BASE)
    rec(f"comparison.BaselineArtifact:{name}", ok=rb["stockOk"], nErrors=rb["nErrors"], firstError=(rb["errors"][0]["message"] if rb["errors"] else None))

# config vectors vs TypeScriptConfigGraphV1
for name in ["config-synthesized.json", "config-custom-multi-base.json", "config-js-shared-base.json"]:
    obj = load_json(SNAP / "vectors" / name)
    r = validate(obj, NATIVE, "#/$defs/TypeScriptConfigGraphV1")
    rec(
        f"config.TypeScriptConfigGraphV1:{name}",
        ok=r["stockOk"],
        nErrors=r["nErrors"],
        firstError=(r["errors"][0]["message"] if r["errors"] else None),
        hasComputedIdentity=any(k in obj for k in ("tsconfigGraphHash", "identity", "H", "typedId", "contentSha256", "nodes")),
        keys=sorted(obj.keys()),
    )

# repair
for name in ["repair-descriptor.json", "repair-authority-per-target.json", "repair-apply-key.json", "test-prep-repair-authorization.json"]:
    obj = load_json(SNAP / "vectors" / name)
    r1 = validate(obj, REP, "#/$defs/RepairPlanV1")
    rec(f"repair.RepairPlanV1:{name}", ok=r1["stockOk"], nErrors=r1["nErrors"], firstError=(r1["errors"][0]["message"] if r1["errors"] else None), keys=sorted(obj.keys()) if isinstance(obj, dict) else None)

# graph query
for name, selector in [
    ("graph-neighbors.json", "#/$defs/GraphQueryRequestV1"),
    ("graph-path.json", "#/$defs/GraphQueryRequestV1"),
    ("graph-reach.json", "#/$defs/GraphQueryRequestV1"),
    ("measured-neighbors.json", "#/$defs/GraphQueryResponseV1"),
    ("failures.json", "#/$defs/GraphQueryRequestV1"),
    ("parity.json", "#/$defs/GraphQueryResponseV1"),
]:
    obj = load_json(SNAP / "query" / name)
    r = validate(obj, GQ, selector)
    rec(
        f"query.{selector.split('/')[-1]}:{name}",
        ok=r["stockOk"],
        nErrors=r["nErrors"],
        firstError=(r["errors"][0]["message"] if r["errors"] else None),
        keys=sorted(obj.keys()) if isinstance(obj, dict) else None,
    )

# GraphQueryResponseV1 on measured-neighbors and request-shaped files
mn = load_json(SNAP / "query/measured-neighbors.json")
gq_required_response = ["schemaFamily", "schemaMajor", "operation", "context", "items"]
gq_ctx_required = [
    "projectId",
    "resolvedView",
    "factViewDigests",
    "availability",
    "truncated",
    "totalItems",
    "countBasis",
    "traversalCoverage",
    "visitedNodes",
    "producedItems",
    "advisory",
    "evidence",
]
rec(
    "query.measured-neighbors.required-response-fields",
    ok=all(k in mn for k in gq_required_response),
    present=[k for k in gq_required_response if k in mn],
    missing=[k for k in gq_required_response if k not in mn],
    hasEvidenceDisclosure=isinstance(mn.get("context"), dict) and "evidence" in mn.get("context", {}),
    hasGraphEvidenceFields=all(k in mn.get("evidence", {}) for k in ("coverageIds", "scopeIds", "deficiencyCitations", "resolutionLimitations")) if isinstance(mn.get("evidence"), dict) else False,
    limitations=mn.get("limitations"),
    nRows=len(mn.get("rows") or mn.get("items") or []),
)

for name in ["graph-neighbors.json", "graph-path.json", "graph-reach.json"]:
    obj = load_json(SNAP / "query" / name)
    req_fields = ["schemaFamily", "schemaMajor", "projectId", "view", "operation", "params", "completeness", "page"]
    rec(
        f"query.request-fields:{name}",
        ok=all(k in obj for k in req_fields),
        present=[k for k in req_fields if k in obj],
        missing=[k for k in req_fields if k not in obj],
        hasTypedItems="items" in obj,
        hasContext="context" in obj,
        hasEvidence="evidence" in obj or (isinstance(obj.get("context"), dict) and "evidence" in obj.get("context", {})),
        hasCursor=("nextCursor" in obj) or ("cursor" in (obj.get("page") or {})) or ("pagination" in obj),
        literalFlags={k: obj[k] for k in obj if type(obj[k]) is bool},
    )

# endpoint universe shape
gn = load_json(SNAP / "query/graph-neighbors.json")
ep = (gn.get("params") or {}).get("endpoint") or {}
uni = ep.get("universe")
rec(
    "query.graph-neighbors.endpoint-universe-is-64hex",
    ok=isinstance(uni, str) and len(uni) == 64 and all(c in "0123456789abcdef" for c in uni),
    universe=uni,
)

# D9 composition fields
d9 = kit_doc("docs/coop/artifacts/d9-exit-contract.v1.14.json")
# look at hostTerminationUnion / public composition
d9_keys = list(d9.keys())[:30]
rec("d9.contract-top-keys", ok=True, keys=d9_keys)

# public-from-internal vs DomainDetail
pfi = load_json(SNAP / "envelopes/public-from-internal.json")
r_dd = validate(pfi, COMMON, "#/$defs/DomainDetail")
rec("d9.public-from-internal.DomainDetail", ok=r_dd["stockOk"], nErrors=r_dd["nErrors"], firstError=(r_dd["errors"][0]["message"] if r_dd["errors"] else None), keys=sorted(pfi.keys()))

# pinned purge
pp = load_json(SNAP / "envelopes/pinned-purge.json")
rec("envelope.pinned-purge.completeEnvelope-literal", ok=pp.get("completeEnvelope") is not True, value=pp.get("completeEnvelope"), note="literal completeEnvelope true is not schema inhabitance")

# ========== store inspection ==========
def load_store(rel: str) -> dict:
    return load_json(SNAP / rel)


def blob_text_hits(store: dict, needles: list[str]) -> dict:
    hits = {n: 0 for n in needles}
    samples = {n: [] for n in needles}
    for digest, b64 in store.get("blobs", {}).items():
        raw = base64.b64decode(b64)
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = None
        for n in needles:
            if n.encode("utf-8") in raw:
                hits[n] += 1
                if text and len(samples[n]) < 2:
                    samples[n].append(digest)
    return {"hits": hits, "sampleDigests": {k: v for k, v in samples.items() if v}}


def ot_labels(store: dict) -> list[str]:
    labs = []
    for k, v in store.get("objectTable", {}).items():
        if isinstance(v, dict) and v.get("label"):
            labs.append(v["label"])
    return sorted(set(labs))


def typed_counts(store: dict) -> dict:
    c: dict[str, int] = {}
    for k in store.get("objectTable", {}):
        if isinstance(k, str) and ":" in k:
            pref = k.split(":", 1)[0]
            c[pref] = c.get(pref, 0) + 1
    return c


stores = {
    "ts": "runs/ts.store.json",
    "rust": "runs/rust.store.json",
    "syntax-code": "runs/syntax-code.store.json",
    "syntax-data": "runs/syntax-data.store.json",
    "rust-partial": "runs/rust-partial-clones.store.json",
}

for name, rel in stores.items():
    st = load_store(rel)
    rec(
        f"store.export-shape:{name}",
        ok="objectTable" in st and "blobs" in st,
        blobCount=st.get("blobCount") or len(st.get("blobs", {})),
        objectTableSize=len(st.get("objectTable", {})),
        typed=typed_counts(st),
        labels=ot_labels(st)[:40],
    )

ts = load_store("runs/ts.store.json")
ts_hits = blob_text_hits(
    ts,
    [
        "node_modules/left-pad",
        "left-pad",
        "tsconfig.json",
        "ScopeDocument",
        "opensip.product.scope",
        "import2:",
        "native.semantic-universe.typescript.v2",
        "javascript",
        "src/util.js",
        "nativeContextDigests",
        "configGraphPaths",
        "entryConfigPath",
        "TypeScriptConfigGraph",
        "extendsResolved",
    ],
)
rec("store.ts.property-hits", ok=True, **ts_hits)

rust = load_store("runs/rust.store.json")
rust_hits = blob_text_hits(
    rust,
    [
        "#/Cargo.toml",
        "#/a/src/lib.rs",
        "edition",
        "2018",
        "2021",
        "crate15",
        "source-unit-ownership",
        "targetEdition",
        "nativeContextDigests",
        "body-language",
        "L0-verbatim",
        "normalized-body-hash",
    ],
)
rec("store.rust.property-hits", ok=True, **rust_hits)

# decode rust universe/ownership JSON-ish blobs for edition map size and mixed editions
def decode_json_blobs(store: dict) -> list[dict]:
    out = []
    for digest, b64 in store.get("blobs", {}).items():
        raw = base64.b64decode(b64)
        if not raw.startswith(b"{") and not raw.startswith(b"opensip.product.v1"):
            continue
        payload = raw
        if raw.startswith(b"opensip.product.v1"):
            # H frame: prefix \0 domain \0 u64be len C(X)
            try:
                i = raw.find(b"\x00")
                j = raw.find(b"\x00", i + 1)
                ln = int.from_bytes(raw[j + 1 : j + 9], "big")
                payload = raw[j + 9 : j + 9 + ln]
            except Exception:
                continue
        try:
            obj = json.loads(payload)
        except Exception:
            continue
        if isinstance(obj, dict):
            out.append({"digest": digest, "obj": obj})
    return out


rust_json = decode_json_blobs(rust)
edition_maps = []
ownerships = []
inventories = []
plans = []
for recj in rust_json:
    o = recj["obj"]
    if "edition" in o and isinstance(o.get("edition"), dict) and "lockfileIdentity" in o:
        edition_maps.append({"digest": recj["digest"], "n": len(o["edition"]), "keys": sorted(o["edition"].keys())[:20], "editions": sorted(set(o["edition"].values()))})
    if o.get("schemaVersion") == 1 and "ownership" in o and "units" in o and "enumeration" in o:
        ownerships.append(
            {
                "digest": recj["digest"],
                "enumeration": o.get("enumeration"),
                "nUnits": len(o.get("units") or []),
                "nOwnership": len(o.get("ownership") or []),
                "selected": o.get("selectedUnitIds"),
                "targetEditions": [u.get("targetEdition") for u in o.get("units") or []],
                "paths": [r.get("path") for r in o.get("ownership") or []],
            }
        )
    if "sourceInventory" in o:
        paths = []
        si = o["sourceInventory"]
        if isinstance(si, list):
            paths = [e.get("path") for e in si]
        elif isinstance(si, dict) and "entries" in si:
            paths = [e.get("path") for e in si["entries"]]
        inventories.append(paths)
    if "nativeContextDigests" in o:
        plans.append({"nctx": len(o.get("nativeContextDigests") or []), "digests": o.get("nativeContextDigests")})

rec(
    "store.rust.edition-maps",
    ok=any(e["n"] >= 2 and len(e["editions"]) > 1 for e in edition_maps),
    maps=edition_maps,
)
rec(
    "store.rust.ownership-records",
    ok=len(ownerships) >= 1,
    n=len(ownerships),
    records=ownerships,
    mixedTargetEdition=any(
        None in (r.get("targetEditions") or []) and 2021 in (r.get("targetEditions") or []) for r in ownerships
    ),
    samePathTwoUnits=any(len(set(r.get("paths") or [])) == 1 and r.get("nOwnership") == 2 for r in ownerships),
)
rec(
    "store.rust.inventory-hash-marker",
    ok=any(any(isinstance(p, str) and p.startswith("#/") for p in inv) for inv in inventories),
    inventories=inventories,
)
rec(
    "store.rust.nonempty-native-context",
    ok=any(p["nctx"] > 0 for p in plans),
    plans=plans,
)

# two ownership identities vs tautological pair vector
pair = load_json(SNAP / "vectors/rust-body-identity-pair.json")
rec(
    "rust-pair.stable-ownership-is-literal-same-assignment",
    ok=False
    if (
        pair.get("libOnlySelectionIdentity") == pair.get("edition2018_L0")
        and pair.get("libAndSameEditionExtraTargetWouldMatch") == pair.get("edition2018_L0")
        and pair.get("stableWhenOnlyOwnershipChangesWithoutDialect") is True
    )
    else True,
    edition2018=pair.get("edition2018_L0"),
    edition2021=pair.get("edition2021_L0"),
    distinctDialect=pair.get("edition2018_L0") != pair.get("edition2021_L0"),
    libOnly=pair.get("libOnlySelectionIdentity"),
    extra=pair.get("libAndSameEditionExtraTargetWouldMatch"),
    literalStable=pair.get("stableWhenOnlyOwnershipChangesWithoutDialect"),
    largeMapSize=pair.get("largeEditionMapSize"),
)

# independently recompute L0 from retained rust lib.rs bytes
lib_bytes = None
for digest, b64 in rust["blobs"].items():
    raw = base64.b64decode(b64)
    if raw.startswith(b"pub fn ") or b"fn " in raw[:80]:
        lib_bytes = raw
        lib_digest = digest
        break
# also try exact inventory sha
rec("store.rust.lib-bytes-found", ok=lib_bytes is not None, n=len(lib_bytes) if lib_bytes else 0, digest=lib_digest if lib_bytes else None, preview=(lib_bytes[:80].decode("utf-8", "replace") if lib_bytes else None))

# TS store properties
ts_json = decode_json_blobs(ts)
ts_inv = []
ts_cfg = []
ts_nm = []
ts_scope = []
ts_imp = []
ts_plans = []
ts_js_bodies = []
for recj in ts_json:
    o = recj["obj"]
    if "sourceInventory" in o:
        si = o["sourceInventory"]
        entries = si if isinstance(si, list) else si.get("entries", [])
        ts_inv.append([e.get("path") for e in entries])
    if "entryConfigPath" in o and "nodes" in o:
        ts_cfg.append(
            {
                "entry": o.get("entryConfigPath"),
                "nodes": [
                    {"path": n.get("path"), "kind": n.get("kind"), "extends": n.get("extendsResolved")}
                    for n in o.get("nodes") or []
                ],
            }
        )
    if "installPath" in str(o) or (isinstance(o, dict) and "entries" in o and any("node_modules" in str(x) for x in o.get("entries") or [])):
        ts_nm.append(o if len(str(o)) < 2000 else {"keys": list(o.keys())})
    if o.get("schemaFamily") == "opensip.product.scope":
        ts_scope.append(o)
    if o.get("payloadDomain") or o.get("schemaVersion") == 2 and "kind" in o and o.get("kind") in ("runtime", "test", "history"):
        ts_imp.append({k: o.get(k) for k in ("schemaVersion", "kind", "payloadDomain", "payloadDigest") if k in o})
    if "nativeContextDigests" in o:
        ts_plans.append({"nctx": len(o.get("nativeContextDigests") or []), "importIds": o.get("importIds")})
    if any(str(v).endswith(".js") for v in o.values() if isinstance(v, str)) and "javascript" in json.dumps(o):
        ts_js_bodies.append(list(o.keys()))

rec(
    "store.ts.inventory-node-modules",
    ok=any(any(isinstance(p, str) and "node_modules" in p for p in inv) for inv in ts_inv),
    inventories=ts_inv,
)
rec("store.ts.config-graph", ok=len(ts_cfg) > 0, graphs=ts_cfg)
rec("store.ts.scope-document", ok=len(ts_scope) > 0, docs=ts_scope)
rec("store.ts.plan-native-context-and-imports", ok=any(p["nctx"] > 0 for p in ts_plans), plans=ts_plans)
rec("store.ts.js-clone-body-through-ts", ok=False, note="search only; see hits", jsBodyHits=ts_hits["hits"].get("src/util.js"), javascriptHits=ts_hits["hits"].get("javascript"))

# syntax-code clones / file facts
sc = load_store("runs/syntax-code.store.json")
sc_hits = blob_text_hits(
    sc,
    [
        "normalized-body-hash",
        "L0-verbatim",
        "L1",
        "enumerated",
        "native.context.syntax.v2",
        "typescript",
        "native.context.typescript",
        "native.context.rust.v2",
        "clones",
        "byteLength",
        "contentSha256",
    ],
)
rec("store.syntax-code.property-hits", ok=True, **sc_hits)
sc_meta = load_json(SNAP / "runs/syntax-code.meta.json")
rec(
    "store.syntax-code.claimed-ids-in-object-table",
    ok=all(
        sc_meta.get(k) in sc["objectTable"]
        for k in ("runId", "planId", "snapshotId", "proofId", "fileFact", "clonesL0", "clonesL1")
        if sc_meta.get(k)
    ),
    present={k: (sc_meta.get(k) in sc["objectTable"]) for k in ("runId", "planId", "fileFact", "clonesL0", "clonesL1")},
)

# syntax-data deficiency pairing inside store vs meta
sd = load_store("runs/syntax-data.store.json")
sd_hits = blob_text_hits(
    sd,
    [
        "language-tier-unsupported",
        "capability-missing",
        "unknown",
        "complete",
        "clones",
        "data-document",
        "json",
    ],
)
rec("store.syntax-data.property-hits", ok=True, **sd_hits)
sd_json = decode_json_blobs(sd)
sd_cov = []
for recj in sd_json:
    o = recj["obj"]
    if o.get("relation") == "clones" or o.get("coverage") in ("unknown", "complete", "partial"):
        if "coverage" in o or "deficiency" in o:
            sd_cov.append({k: o.get(k) for k in ("relation", "coverage", "deficiency", "nativeCause", "state") if k in o})
rec("store.syntax-data.coverage-records", ok=any(c.get("coverage") == "unknown" for c in sd_cov), records=sd_cov[:10])

# rust partial
rp = load_store("runs/rust-partial-clones.store.json")
rp_json = decode_json_blobs(rp)
rp_own = []
rp_cov = []
rp_facts_clones = 0
for recj in rp_json:
    o = recj["obj"]
    if o.get("schemaVersion") == 1 and "ownership" in o and "enumeration" in o:
        rp_own.append({"enumeration": o.get("enumeration"), "nOwnership": len(o.get("ownership") or [])})
    if "deficiency" in o or "nativeCause" in o:
        rp_cov.append({k: o.get(k) for k in ("relation", "coverage", "deficiency", "nativeCause", "enumeration") if k in o})
    if o.get("relation") == "clones":
        rp_facts_clones += 1
rec(
    "store.rust-partial.deficiency-pairing",
    ok=any(c.get("deficiency") == "input-closure-incomplete" for c in rp_cov)
    or any(c.get("nativeCause") == "body-language-owner-unenumerated" for c in rp_cov),
    ownership=rp_own,
    coverage=rp_cov[:12],
    cloneFactRecords=rp_facts_clones,
)

# replay exports present?
replay_files = {
    "syntax-code": (SNAP / "runs/syntax-code.replay.json").exists(),
    "ts": (SNAP / "runs/ts.replay.json").exists(),
    "rust": (SNAP / "runs/rust.replay.json").exists(),
    "syntax-data": (SNAP / "runs/syntax-data.replay.json").exists(),
    "rust-partial": (SNAP / "runs/rust-partial-clones.replay.json").exists(),
}
rec("replay.export-per-claimed-positive", ok=all(replay_files.values()), present=replay_files)

# ========== independent H remint of snapshot-A ==========
hvec = load_json(SNAP / "vectors/h-helper.json")
snapA = None
for v in hvec["vectors"]:
    if v["name"] == "snapshot-A":
        snapA = v
        break
c_bytes = bytes.fromhex(snapA["C_hex"])
# reconstruct object from C bytes
snapA_obj = json.loads(c_bytes)
h_indep = H_hex("snapshot", snapA_obj)
c_indep = C_encode(snapA_obj)
rec(
    "h-helper.independent-remint-snapshot-A",
    ok=h_indep == snapA["H"] and c_indep.hex() == snapA["C_hex"],
    claimedH=snapA["H"],
    independentH=h_indep,
    cEqual=c_indep.hex() == snapA["C_hex"],
)

# semantic vs operational claimed H
svo = load_json(SNAP / "vectors/semantic-vs-operational.json")
rec(
    "semantic-vs-operational.has-measured-ids",
    ok=bool(svo.get("semanticChangeMovesIdentity", {}).get("equal") is False)
    and bool(svo.get("operationalChangeDoesNotMoveIdentity", {}).get("equal") is True),
    measured=svo.get("measured"),
    semantic=svo.get("semanticChangeMovesIdentity"),
    operational=svo.get("operationalChangeDoesNotMoveIdentity"),
)

# lexical firstRefusal
lex = load_json(SNAP / "vectors/lexical-admission.json")
lex_neg = [v for v in lex["vectors"] if v.get("classification") == "invalid"]
rec(
    "lexical.negatives-have-firstRefusal",
    ok=all("firstRefusal" in v for v in lex_neg) and len(lex_neg) >= 3,
    nNeg=len(lex_neg),
    nPos=sum(1 for v in lex["vectors"] if v.get("classification") == "valid"),
    names=[v["name"] for v in lex_neg],
)

# cap named gates
cg = load_json(SNAP / "vectors/cap-named-gates.json")
rec(
    "cap-named-gates.firstRefusal-and-masksLater",
    ok=all(v.get("firstRefusal") and "masksLater" in v for v in cg["vectors"]),
    n=len(cg["vectors"]),
    gates=[v.get("gate") or v.get("expectedGate") for v in cg["vectors"]],
)

# clones negatives: declared vs executed helper
cln = load_json(SNAP / "vectors/clones-negatives.json")
rec(
    "clones-negatives.declared-firstRefusal-no-instance",
    ok=False,
    n=len(cln["vectors"]),
    hasFirstRefusal=all("firstRefusal" in v for v in cln["vectors"]),
    hasInputInstance=any("input" in v or "record" in v or "payload" in v for v in cln["vectors"]),
    note="firstRefusal objects are declared; no clone-record instance or helper process status",
)

# min-resolution: string table vs facts
mr = load_json(SNAP / "vectors/min-resolution.json")
rec(
    "min-resolution.cases-are-strings",
    ok=False,
    cases=mr.get("cases"),
    hasFactIds=any(isinstance(c.get("qualifying"), dict) or str(c.get("qualifying", "")).startswith("fact2:") for c in mr.get("cases", [])),
)

# mutation/repair keys computed?
rk = load_json(SNAP / "vectors/repair-apply-key.json")
ms = load_json(SNAP / "vectors/mutation-replay-scope.json")
rec(
    "repair-apply-key.computed-inequality",
    ok=False,
    measuredInequality=rk.get("measuredInequality"),
    hasHexKey=any(isinstance(v, str) and len(v) == 64 for v in rk.values()),
    keys=list(rk.keys()),
)
rec("mutation-replay-scope.is-narrative", ok=False, keys=list(ms.keys()), values=ms)

# authorization
auth = load_json(SNAP / "vectors/test-prep-repair-authorization.json")
rec("auth.vector-is-three-labels", ok=False, obj=auth)

# hidden mismatch
hm = load_json(SNAP / "vectors/hidden-mismatch.json")
rec(
    "hidden-mismatch.declared-not-executed",
    ok=isinstance(hm.get("typescript", {}).get("firstRefusal"), str),
    obj=hm,
    note="firstRefusal is a selector string, not an executed refusal object from a helper",
)

# d9 extension precedence
d9e = load_json(SNAP / "vectors/d9-extension-precedence.json")
rec("d9-extension-precedence.narrative", ok=False, obj=d9e)

# subsystem owners
so = load_json(SNAP / "vectors/subsystem-owners.json")
rec("subsystem-owners.four-labels", ok=False, obj=so)

# replay three-valued
rtv = load_json(SNAP / "vectors/replay-three-valued.json")
rec("replay-three-valued.literals", ok=False, obj=rtv)

# js body through ts
jsb = load_json(SNAP / "vectors/js-body-through-ts.json")
rec("js-body-through-ts.narrative-flags", ok=False, obj=jsb, notRelabelledLiteral=jsb.get("notRelabelledAsTypescript"))

# detector compat
dc = load_json(SNAP / "vectors/detector-compat-file.json")
rec("detector-compat.narrative", ok=False, obj=dc)

# host captured
hc = load_json(SNAP / "vectors/host-captured-vs-candidate.json")
rec("host-captured.narrative", ok=False, obj=hc)

# pivot fingerprints
pf = load_json(SNAP / "vectors/pivot-only-fingerprints.json")
rec("pivot-only.literals", ok=False, obj=pf)

# e0 e3
e0 = load_json(SNAP / "vectors/baseline-e0-e3.json")
rec("baseline-e0-e3.literals", ok=False, obj=e0)

# query failures vs CommandEnvelope kind=failure
qf = load_json(SNAP / "query/failures.json")
r_fail_env = validate(qf, CE)
rec("query.failures.as-CommandEnvelope", ok=r_fail_env["stockOk"], nErrors=r_fail_env["nErrors"], firstError=(r_fail_env["errors"][0]["message"] if r_fail_env["errors"] else None), keys=sorted(qf.keys()))

# parity literals
qp = load_json(SNAP / "query/parity.json")
rec("query.parity.literals", ok=False, obj=qp)

# classification field coverage
status = load_json(SNAP / "requirement-status.json")
vec_dir = SNAP / "vectors"
classified = 0
unclassified = []
for p in sorted(vec_dir.glob("*.json")):
    obj = load_json(p)
    has = False
    if isinstance(obj, dict):
        if obj.get("classification") in ("valid", "invalid", "explanatory"):
            has = True
        if any(isinstance(x, dict) and x.get("classification") in ("valid", "invalid", "explanatory") for x in obj.get("vectors", []) if isinstance(obj.get("vectors"), list)):
            has = True
        if any(isinstance(x, dict) and x.get("classification") in ("valid", "invalid", "explanatory") for x in obj.get("cases", []) if isinstance(obj.get("cases"), list)):
            has = True
    if has:
        classified += 1
    else:
        unclassified.append(p.name)
rec("classification-field.coverage", ok=True, nClassifiedFiles=classified, nUnclassified=len(unclassified), unclassified=unclassified)

# helperCorrections present
br = load_json(SNAP / "blind-review.json")
rec(
    "helperCorrections.preserved",
    ok=bool(br.get("helperCorrections")),
    items=br.get("helperCorrections"),
)

# claimed verdict vs empty must issues
rec("consumer.claimed-verdict", ok=True, verdict=br.get("verdict"), must=br.get("newMustIssues"), should=br.get("newShouldIssues"))

# single-step / multi-step vs invocation
ss = load_json(SNAP / "envelopes/single-step.json")
msv = load_json(SNAP / "envelopes/multi-step.json")
r_inv = validate(ss, INV)
rec("single-step.as-invocation-record", ok=r_inv["stockOk"], nErrors=r_inv["nErrors"], firstError=(r_inv["errors"][0]["message"] if r_inv["errors"] else None), obj=ss)
r_inv2 = validate(msv, INV)
rec("multi-step.as-invocation-record", ok=r_inv2["stockOk"], nErrors=r_inv2["nErrors"], firstError=(r_inv2["errors"][0]["message"] if r_inv2["errors"] else None), obj=msv)

# measured-neighbors fact id in TS store?
mn_fact = None
rows = mn.get("rows") or []
if rows:
    mn_fact = rows[0].get("factId")
rec(
    "query.measured-neighbors.fact-in-ts-store",
    ok=bool(mn_fact) and mn_fact in ts.get("objectTable", {}),
    factId=mn_fact,
    inStore=mn_fact in ts.get("objectTable", {}) if mn_fact else False,
    runIdMatch=mn.get("view", {}).get("runId") == load_json(SNAP / "runs/ts.meta.json").get("runId"),
)

# decode that fact if present
if mn_fact and mn_fact in ts.get("objectTable", {}):
    recj = None
    # find blob
    meta = ts["objectTable"][mn_fact]
    digest = meta.get("digest")
    raw = base64.b64decode(ts["blobs"][digest]) if digest in ts["blobs"] else None
    rec("query.measured-neighbors.fact-meta", ok=True, meta=meta, rawPrefix=(raw[:80].hex() if raw else None))

outp = OUT / "probes" / "scope_probe.results.json"
outp.write_text(json.dumps(results, indent=2, default=str) + "\n")
print("PROBES", len(results["probes"]))
print("FAILURES_MARKED", len(results["failures"]))
print("WROTE", outp)
# print compact summary of ok flags
for p in results["probes"]:
    flag = "OK " if p.get("ok") else "NO "
    extra = p.get("firstError") or p.get("missing") or p.get("note") or ""
    if extra:
        extra = " :: " + str(extra)[:160]
    print(f"{flag}{p['name']}{extra}")
