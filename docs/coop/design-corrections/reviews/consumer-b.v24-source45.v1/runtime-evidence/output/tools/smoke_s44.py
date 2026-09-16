"""Smoke run (prints only, writes nothing): source44 fixtures, handshake/startup admission and one complete exchange per language.
It is a development probe, not a vector; its log is retained under logs/ like every execution.
"""
import json
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source45.v1/output/"
sys.path.insert(0, OUT + "ref")
sys.path.insert(0, OUT + "vectors")
import payload_fixtures as PF  # noqa: E402
import provider_exchange as X  # noqa: E402
import provider_wire as W  # noqa: E402

print("limit cross-check", W.LIMIT_CROSS_CHECK)
for shape in ("ts", "rust"):
    tr = PF.trusted(shape)
    hp, ap = PF.hello_payload(shape), PF.ack_payload(shape)
    print(shape, "hello", W.admit_hello(shape, hp, tr), "ack", W.admit_hello_ack(shape, ap, hp, tr))
    ou, ev = PF.startup_events(shape)
    print(shape, "universe key", W.universe_identity(shape, ou["universe"]["resolvedInputs"]), "retained", PF.RET[shape]["universeHex"])
    snap = [{"frame": f} for f in ("SnapshotManifest", "SnapshotFileChunk", "SnapshotSeal", "SnapshotAccepted")]
    dep = [{"frame": f} for f in ("DependencySourceManifest", "DependencySourceSeal", "DependencySourceAccepted")] if shape == "rust" else []
    a = PF.analyze_event(shape)
    stages = [PF.coverage(shape, i) for i in range(a["stageCount"])]
    events = [PF.hello(shape), PF.ack(shape), ev["OpenUniverse"], ev["UniverseAccepted"]] + snap + dep + [ev["NativeContextVerified"], a] + stages + \
        [{"frame": "Complete"}, {"frame": "zero-exit"}, {"frame": "eof"}]
    res = X.ProviderExchange(shape, PF.exchange_ctx(shape)).run(events)
    print(shape, "rules", [t["rule"] for t in res["trace"]], "final", res["state"])
    print(shape, "faults", [(a_["step"], a_["frame"], a_["faults"][:2]) for a_ in res["admissions"] if a_["faults"]])
    conv = W.pre_analyze_conversion(X.requests_of(a, shape), PF.WORKER_TERMINAL_CLOSED_WORLD)
    print(shape, "conversion faults", conv["faults"][:4], "entries", len(conv["entries"]), "authority", json.dumps(conv["stageAuthority"]["d9"]))
