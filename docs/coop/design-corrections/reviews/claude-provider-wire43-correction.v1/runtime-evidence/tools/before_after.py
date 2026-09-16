"""Before/after discriminator: the same vectors against frozen43 owners and against the corrected copy.

usage: before_after.py <frozen43-root> <work-candidate-root> <json-out>

Reads both trees; writes only <json-out>. BEFORE uses frozen43's registered native-evidence.schemas.v2.json
definitions (through the frozen native model's validate_native) and frozen43's occupancy token gate.
AFTER uses the corrected provider-handshake.schemas.v1.json and provider_wire_model.v1.py. Vectors are
the hashlib/cbor2-authored fixtures in the corrected native-cases.v2.json. Reference evidence only.
"""
import importlib.util
import json
import sys
from pathlib import Path

frozen, work, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
DC = Path("docs/coop/design-corrections")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


old_native = load("before_native", frozen / DC / "native" / "native_evidence_model.v2.py")
old_return = load("before_return", frozen / DC / "foundation" / "provider_attribution_return_model.v2.py")
new_native = load("after_native", work / DC / "native" / "native_evidence_model.v2.py")
new_return = load("after_return", work / DC / "foundation" / "provider_attribution_return_model.v2.py")
fx = json.loads((work / DC / "native" / "native-cases.v2.json").read_text(encoding="utf-8"))["fixtures"]


def outcome(fn):
    try:
        value = fn()
        return {"admitted": True, "value": value if isinstance(value, (dict, str, bool)) or value is None else "valid"}
    except Exception as exc:  # noqa: BLE001 - a refusal is the observation
        return {"admitted": False, "error": type(exc).__name__, "detail": str(exc).splitlines()[0][:240]}


def old_def(name, value):
    if name not in old_native.SCHEMAS["$defs"]:
        return {"admitted": False, "error": "UndefinedInFrozen43", "detail": name + " is not defined by any frozen43 owner"}
    return outcome(lambda: (old_native.validate_native(name, value), "valid")[1])


def new_def(name, value):
    return outcome(lambda: (new_native.validate_provider_wire(name, value), "valid")[1])


TS, RS = "typescript-semantic", "rust-semantic"
rows = []


def row(label, vector, before, after, expectation):
    rows.append({"row": label, "vector": vector, "before": before, "after": after, "expectation": expectation})


row("rust HelloV3 carrying HelloV2 identity, contract digest and 32 limits", "wireRustHello",
    old_def("HelloV3", fx["wireRustHello"]), new_def("HelloV3", fx["wireRustHello"]),
    "before refuses (identity/contract members and 24 inherited limits are unknown); after admits")
row("rust HelloV3 in the frozen 4-member shape (no identity, 8 limits)", "wireRustHelloSupersededShape",
    old_def("HelloV3", fx["wireRustHelloSupersededShape"]), new_def("HelloV3", fx["wireRustHelloSupersededShape"]),
    "before admits the unauthenticated shape; after refuses")
row("rust HelloAckV3 carrying HelloAckV2 identity echoes", "wireRustHelloAck",
    old_def("HelloAckV3", fx["wireRustHelloAck"]), new_def("HelloAckV3", fx["wireRustHelloAck"]),
    "before refuses the identity echoes; after admits")
bare_ack = {k: fx["wireRustHelloAck"][k] for k in ("protocolMajor", "capabilities", "identityVersions")}
row("rust HelloAckV3 without identity echoes", "wireRustHelloAck minus identity members",
    old_def("HelloAckV3", bare_ack), new_def("HelloAckV3", bare_ack),
    "before admits; after refuses")
row("ProtocolLimitsV3 as 24 inherited + 8 successor members", "wireRustProtocolLimitsV3",
    old_def("ProtocolLimitsV3", fx["wireRustProtocolLimitsV3"]), new_def("ProtocolLimitsV3", fx["wireRustProtocolLimitsV3"]),
    "before refuses the 24 retained members section 9.3 names; after admits")
eight = {k: v for k, v in fx["wireRustProtocolLimitsV3"].items() if k not in json.loads(
    (frozen / "docs/coop/artifacts/rust-provider-protocol.v2.json").read_text(encoding="utf-8"))["limits"]}
row("ProtocolLimitsV3 as only the 8 successor members", "8-member map",
    old_def("ProtocolLimitsV3", eight), new_def("ProtocolLimitsV3", eight), "before admits; after refuses")
row("typescript-semantic major-2 Hello with every HelloV1 member", "wireTsHello",
    old_def("TypeScriptHelloV2", fx["wireTsHello"]), new_def("TypeScriptHelloV2", fx["wireTsHello"]),
    "before: no owner defines it; after admits")
row("typescript-semantic Hello projected onto frozen HelloV3 with major 2", "wireTsHelloAsSupersededRustShape",
    old_def("HelloV3", fx["wireTsHelloAsSupersededRustShape"]), new_def("TypeScriptHelloV2", fx["wireTsHelloAsSupersededRustShape"]),
    "before refuses (const 3) so reading A was not published either; after refuses as a TypeScript Hello")
row("typescript-semantic major-2 HelloAck with all 14 HelloAckV1 members", "wireTsHelloAck",
    old_def("TypeScriptHelloAckV2", fx["wireTsHelloAck"]), new_def("TypeScriptHelloAckV2", fx["wireTsHelloAck"]),
    "before: undefined; after admits")
row("typescript-semantic limits under the frozen ProtocolLimitsV3", "wireTsProtocolLimits",
    old_def("ProtocolLimitsV3", fx["wireTsProtocolLimits"]), new_def("TypeScriptProtocolLimitsV1", fx["wireTsProtocolLimits"]),
    "before refuses; after admits under the TypeScript definition")

ts_tokens, rust_tokens = fx["ts2"], fx["rust3"]
for label, language, vector, tokens, expect in [
        ("TS token-absent historical FactBatchV1", TS, "wireTsFactBatchV1", ts_tokens, "before omits without validation; after admits and verifies batchCommitment"),
        ("TS token-absent Rust FactBatchV2 shape", TS, "wireRustFactBatchV2", ts_tokens, "before omits identically; after refuses"),
        ("Rust token-absent historical FactBatchV2", RS, "wireRustFactBatchV2", rust_tokens, "before omits; after admits"),
        ("Rust token-absent TS FactBatchV1 shape", RS, "wireTsFactBatchV1", rust_tokens, "before omits identically; after refuses")]:
    before = outcome(lambda v=vector, t=tokens: old_return._token_gate(fx[v], t))
    gate_after = outcome(lambda v=vector, t=tokens: new_return._token_gate(fx[v], t))
    after = outcome(lambda l=language, v=vector, t=tokens: new_native.admit_provider_fact_batch(language=l, batch=fx[v], negotiated_tokens=t))
    rows.append({"row": label, "vector": vector, "before": before, "afterOccupancyGate": gate_after,
                 "after": after, "expectation": expect + "; the corrected occupancy gate stays a capture-only omission"})
bad = dict(fx["wireTsFactBatchV1"], batchCommitment="sha256:" + "00" * 32)
rows.append({"row": "TS token-absent FactBatchV1 with a wrong batchCommitment", "vector": "wireTsFactBatchV1 + wrong commitment",
             "before": outcome(lambda: old_return._token_gate(bad, ts_tokens)),
             "after": outcome(lambda: new_native.admit_provider_fact_batch(language=TS, batch=bad, negotiated_tokens=ts_tokens)),
             "expectation": "before omits; after refuses BATCH_COMMITMENT"})
junk = {"not": "a batch"}
rows.append({"row": "token-absent junk map", "vector": "{not: a batch}",
             "before": outcome(lambda: old_return._token_gate(junk, ts_tokens)),
             "after": outcome(lambda: new_native.admit_provider_fact_batch(language=TS, batch=junk, negotiated_tokens=ts_tokens)),
             "expectation": "before omits; after refuses"})

out.write_text(json.dumps({"standing": "reference-only before/after discriminator; not worker or compiler qualification",
                           "frozenRoot": str(frozen), "workRoot": str(work), "rows": rows}, indent=1) + "\n", encoding="utf-8")
for r in rows:
    print(f"{r['row'][:70]:70} before={'ADMIT' if r['before']['admitted'] else 'REFUSE'} after={'ADMIT' if r['after']['admitted'] else 'REFUSE'}")
