"""Three-state discriminator for ADJ-2..5: frozen43, the wire43 handoff, and the corrected copy.

usage: before_after_startup.py <frozen43-root> <wire43-root> <work-root> <json-out>

Reads all three trees; writes only <json-out>. "Inherited rule" rows transcribe the exact inherited text of the
named selector into a check (labelled with the selector) because frozen43 and wire43 carry no executable owner for
them; the corrected state uses the published successor records and provider_startup_exchange. An earlier state
admitting or refusing something is recorded as what that state's owners determine, not as a consumer bug.
Reference evidence only.
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

frozen, wire43, work, out = (Path(p) for p in sys.argv[1:5])
DC = Path("docs/coop/design-corrections/native")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


frozen_model = load("disc_frozen_native", frozen / DC / "native_evidence_model.v2.py")
wire_model = load("disc_wire43_native", wire43 / DC / "native_evidence_model.v2.py")
final_model = load("disc_final_native", work / DC / "native_evidence_model.v2.py")
cases = json.loads((work / DC / "native-cases.v2.json").read_text(encoding="utf-8"))
fx = cases["fixtures"]
delivery = json.loads((frozen / "docs/coop/artifacts/delivery.v2.json").read_text(encoding="utf-8"))
rust_v2 = json.loads((frozen / "docs/coop/artifacts/rust-provider-protocol.v2.json").read_text(encoding="utf-8"))
TS_PS = delivery["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"]["payloadSchemas"]
TS_DEFS = delivery["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"]["definitions"]
TS_ORDER_TEXT = delivery["typescriptSemanticSubstrate"]["providerProtocol"]["ordering"]
RS_PS = rust_v2["wireSchema"]["payloadSchemas"]


def verdict(fn):
    try:
        value = fn()
        return {"admitted": True, "value": value}
    except Exception as exc:  # noqa: BLE001 - refusal is the observation
        return {"admitted": False, "error": type(exc).__name__, "detail": str(exc).splitlines()[0][:300]}


def inherited_closed(selector_name, record, payload):
    """Transcription of an inherited closed record: exactly its required members (selector named in the row)."""
    want, got = set(record["required"]), set(payload)
    if want != got:
        raise ValueError(f"{selector_name} closed members: missing {sorted(want - got)} extra {sorted(got - want)}")
    return "members match"


def ts_exchange(frames_name):
    frames = next(c for c in cases["cases"] if c["id"] == frames_name)["steps"][0]["args"]["frames"]
    return frames


def run_final_case(case_id):
    case = next(c for c in cases["cases"] if c["id"] == case_id)
    spec = importlib.util.spec_from_file_location("disc_checker", work / DC / "check_native_evidence.v2.py")
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    args = checker.resolve(case["steps"][0]["args"], {"fixtures": fx})
    result = getattr(final_model, case["steps"][0]["fn"])(**args)
    keep = ("finalPhase", "terminalKind", "trace", "refusal")
    summary = {k: result[k] for k in keep if isinstance(result, dict) and k in result} if isinstance(result, dict) else result
    if isinstance(result, dict) and result.get("hostConversion"):
        conv = result["hostConversion"]
        summary["hostConversion"] = {"coverageSource": conv.get("coverageSource"), "allAdmitted": conv.get("allAdmitted"),
                                     "d9": (conv.get("termination") or conv.get("stageAuthority") or {}).get("d9")}
    return summary


rows = []


def row(adj, label, frozen_state, wire_state, final_state, reading):
    rows.append({"finding": adj, "row": label, "frozen43": frozen_state, "wire43": wire_state, "final": final_state,
                 "reading": reading})


pre_ts = fx["startupTsPreAnalyzeUnavailable"]
row("ADJ-2", "TS pre-Analyze native-context mismatch payload against the inherited UnavailableV1 closed record",
    verdict(lambda: inherited_closed("delivery.v2 payloadSchemas.UnavailableV1", TS_PS["UnavailableV1"], pre_ts)),
    verdict(lambda: inherited_closed("delivery.v2 payloadSchemas.UnavailableV1", TS_PS["UnavailableV1"], pre_ts)),
    verdict(lambda: run_final_case("startup-ts2-pre-analyze-unavailable-host-derives-provider-unavailable-coverage")),
    "before: the only published Unavailable record needs analysisOrdinal/affectedStageIds/coverage from an Analyze the worker never received; after: PreAnalyzeUnavailableV1 admitted and coverage host-derived")
row("ADJ-2", "TS Unavailable before Analyze under the inherited ordering text",
    verdict(lambda: (_ for _ in ()).throw(ValueError("delivery.v2 ordering.unavailableTerminal: " + TS_ORDER_TEXT["unavailableTerminal"]))),
    verdict(lambda: (_ for _ in ()).throw(ValueError("no typescript-semantic order table published; inherited ordering.unavailableTerminal governs"))),
    verdict(lambda: final_model.typescript_protocol2_run([{"frame": "Hello"}, {"frame": "HelloAck", "capabilities": list(final_model.TS2_TOKENS)},
                                                           {"frame": "OpenUniverse"}, {"frame": "UniverseAccepted"},
                                                           {"frame": "SnapshotManifest"}, {"frame": "SnapshotSeal"},
                                                           {"frame": "SnapshotAccepted"},
                                                           {"frame": "Unavailable", "unavailablePayload": "pre-analyze"},
                                                           {"frame": "zero-exit"}, {"frame": "eof"}])["trace"]),
    "before: the inherited order forbids the Unavailable that native-evidence 2.4/9.4 require before Analyze; after: T2-10")
rust_post_shape = fx["startupRustPostAnalyzeUnavailable"]
pre_rust = fx["startupRustPreAnalyzeUnavailable"]
row("ADJ-2", "Rust P3-21 Unavailable: payload record available before Analyze",
    {"table": frozen_model.protocol3_run([{"frame": "Hello"}, {"frame": "HelloAck", "capabilities": list(frozen_model.RUST3_TOKENS)},
                                           {"frame": "OpenUniverse", "dependencyMode": True}, {"frame": "UniverseAccepted"},
                                           {"frame": "SnapshotManifest"}, {"frame": "SnapshotSeal"}, {"frame": "SnapshotAccepted"},
                                           {"frame": "DependencySourceManifest"}, {"frame": "DependencySourceSeal"},
                                           {"frame": "DependencySourceAccepted"}, {"frame": "Unavailable"}])["trace"][-1],
     "payload": verdict(lambda: inherited_closed("rust-provider-protocol.v2 payloadSchemas.UnavailableV2", RS_PS["UnavailableV2"], pre_rust))},
    {"payload": verdict(lambda: inherited_closed("rust-provider-protocol.v2 payloadSchemas.UnavailableV2", RS_PS["UnavailableV2"], pre_rust))},
    {"preAnalyze": verdict(lambda: run_final_case("startup-rust3-pre-analyze-unavailable-host-derives-provider-unavailable-coverage")),
     "postAnalyzeShapeInThatPhase": verdict(lambda: run_final_case("startup-rust3-post-analyze-payload-in-native-context-phase-refused"))},
    "before: the table admits the event but the only payload record needs Analyze-derived members; after: a phase-scoped payload")
open_rust = fx["startupRustOpenUniverse"]
payload_event = {"frame": "OpenUniverse", **{k: open_rust[k] for k in ("dependencyMode", "preparedMode") if k in open_rust}}
prefix = [{"frame": "Hello"}, {"frame": "HelloAck", "capabilities": list(frozen_model.RUST3_TOKENS)}, payload_event,
          {"frame": "UniverseAccepted"}, {"frame": "SnapshotManifest"}, {"frame": "SnapshotSeal"}, {"frame": "SnapshotAccepted"}]
row("ADJ-3", "Rust OpenUniverse event built from the payload's own members (stateUpdates 'from the frame's booleans')",
    {"eventFromPayload": payload_event, "trace": frozen_model.protocol3_run(prefix)["trace"][-1]},
    {"eventFromPayload": payload_event, "trace": wire_model.protocol3_run(prefix)["trace"][-1]},
    verdict(lambda: run_final_case("startup-rust3-empty-dependency-set-custody-then-complete")),
    "before: no payload member carries the booleans, so a payload-derived event skips dependency custody (P3-10) for a universe whose dependencySourceSetId is non-null; after: derived dependencyMode true, P3-08")
row("ADJ-3", "TS OpenUniverse planId plan2 text against the inherited PlanId definition",
    verdict(lambda: (_ for _ in ()).throw(ValueError("delivery.v2 definitions.PlanId: " + TS_DEFS["PlanId"])) if not fx["startupTsOpenUniverse"]["planId"].startswith("plan1:") else "match"),
    verdict(lambda: (_ for _ in ()).throw(ValueError("delivery.v2 definitions.PlanId: " + TS_DEFS["PlanId"]))),
    {"plan2": verdict(lambda: run_final_case("startup-ts2-open-universe-accepted-native-context-verified-complete")),
     "plan1": verdict(lambda: run_final_case("startup-ts2-open-universe-plan1-plan-id-refused"))},
    "before: the inherited pattern names plan1 while section 9.1 says OpenUniverse carries plan2; after: plan2 admitted, plan1 refused")
row("ADJ-4", "Rust coverage frame name",
    {"inheritedFrameSchemasKey": "Coverage" in rust_v2["wireSchema"]["frameSchemas"],
     "tableWithCoverage": frozen_model.protocol3_run(prefix[:2] + [{"frame": "OpenUniverse", "dependencyMode": False}, {"frame": "UniverseAccepted"},
                                                                   {"frame": "SnapshotManifest"}, {"frame": "SnapshotSeal"}, {"frame": "SnapshotAccepted"},
                                                                   {"frame": "NativeContextVerified"}, {"frame": "Analyze"}, {"frame": "Coverage"}])["trace"][-1],
     "tableWithCoverageV3": frozen_model.protocol3_run(prefix[:2] + [{"frame": "OpenUniverse", "dependencyMode": False}, {"frame": "UniverseAccepted"},
                                                                     {"frame": "SnapshotManifest"}, {"frame": "SnapshotSeal"}, {"frame": "SnapshotAccepted"},
                                                                     {"frame": "NativeContextVerified"}, {"frame": "Analyze"}, {"frame": "CoverageV3"}])["trace"][-1]},
    {"sameAsFrozen": True},
    {"CoverageV3": verdict(lambda: run_final_case("startup-rust3-empty-dependency-set-custody-then-complete")),
     "Coverage": verdict(lambda: run_final_case("startup-rust3-frame-named-coverage-faults"))},
    "before: P3-24 already requires CoverageV3 while the inherited frameSchemas key stays Coverage with no section 0 row; after: row added and the wrapper published")
row("ADJ-4", "TS Coverage entry: CoverageResultV3 against the inherited CoverageResultV1 closed record",
    verdict(lambda: inherited_closed("delivery.v2 definitions.CoverageResultV1", TS_DEFS["CoverageResultV1"], fx["startupTsCoverage"]["entries"][0])),
    verdict(lambda: inherited_closed("delivery.v2 definitions.CoverageResultV1", TS_DEFS["CoverageResultV1"], fx["startupTsCoverage"]["entries"][0])),
    {"v3Entry": verdict(lambda: run_final_case("startup-ts2-open-universe-accepted-native-context-verified-complete")),
     "v1Entry": verdict(lambda: run_final_case("startup-ts2-coverage-frame-with-coverage-result-v1-entry-refused")),
     "entryAsFrame": verdict(lambda: run_final_case("startup-ts2-coverage-entry-sent-as-the-whole-frame-refused"))},
    "before: the frame wrapper names CoverageResultV1 entries while section 9.4 adds CoverageV3; after: the inherited wrapper with CoverageResultV3 entries")
row("ADJ-5", "TS Cancelled.observedPhase for a Cancel in the NativeContextVerified interval",
    {"inheritedEnum": TS_PS["CancelledV1"]["fields"]["observedPhase"], "rule": "none: no interval existed"},
    {"inheritedEnum": TS_PS["CancelledV1"]["fields"]["observedPhase"], "rule": "none: interval inserted by section 9.4 without an observedPhase mapping"},
    {"snapshot": verdict(lambda: run_final_case("startup-ts2-cancel-in-native-context-interval-observes-snapshot")),
     "analysis": verdict(lambda: run_final_case("startup-ts2-cancel-in-native-context-interval-observing-analysis-refused"))},
    "before: either enum value is unconstrained in the inserted interval; after: snapshot, with no new enum member")
out.write_text(json.dumps({"standing": "reference-only three-state discriminator; not worker, process or compiler qualification",
                           "roots": {"frozen43": str(frozen), "wire43": str(wire43), "final": str(work)}, "rows": rows},
                          indent=1, default=str) + "\n", encoding="utf-8")
for r in rows:
    print(r["finding"], "|", r["row"][:90])
