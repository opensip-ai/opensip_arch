"""Reviewer probe: independent worker/host race model for RUST3-PROVIDER-FAULT.

For lawful host transcripts, enumerate every cut the worker could have read (a prefix of host->worker frames sent
since the last worker frame), compute the worker-observed triple with an independent replay written here from the
published P3 rows (not the author's overlay_run), and check the author's reference admission admits exactly those
triples and refuses perturbations. Also confirm the owner protocol3_run admits each host-order trace as P3-28.
"""
import importlib.util, json, sys, itertools
from pathlib import Path

COPY = Path(__file__).resolve().parent / "copy"
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
sys.path.insert(0, str(COPY / "tools"))
import admission_ref as AR  # noqa: E402

doc = json.loads((COPY / "wire-carriers.v1.json").read_text())
p3 = json.loads((ARCH / "docs/coop/design-corrections/native/protocol3-transitions.v1.json").read_text())
spec = importlib.util.spec_from_file_location("ne", ARCH / "docs/coop/design-corrections/native/native_evidence_model.v2.py")
NE = importlib.util.module_from_spec(spec); spec.loader.exec_module(NE)
TOK = list(NE.IDENTITY_TOKENS)
EX = "exec1_" + "ab" * 16
H2W = AR.HOST_TO_WORKER

PRE = set(p3["wildcards"]["*PRE_COMPLETE"]["phases"])


def my_replay(frames, prepared):
    """Independent minimal replay of P3 rows for lawful frames (no guards beyond modes)."""
    ph = "START"
    for f in frames:
        rows = [r for r in p3["rules"] if r["frame"] == f and (r["phase"] == ph or (r["phase"] == "*PRE_COMPLETE" and ph in PRE))]
        rows = [r for r in rows if all({"dependencyMode": True, "preparedMode": prepared, "identityNegotiated": True}.get(k, v) == v for k, v in r.get("guard", {}).items())]
        assert rows, (ph, f)
        nx = rows[0]["next"]
        ph = "READY_COMPLETE" if nx == "ANALYZING_OR_READY_COMPLETE" else nx
    return ph


def ev(frame, prepared):
    if frame == "HelloAck":
        return {"frame": frame, "capabilities": TOK}
    if frame == "OpenUniverse":
        return {"frame": frame, "payload": {"executionId": EX}, "dependencyMode": True, "preparedMode": prepared}
    if frame == "Analyze":
        return {"frame": frame, "payload": {"analysisOrdinal": 0}}
    return {"frame": frame}


def full(prepared, chunks):
    s = ["Hello", "HelloAck", "OpenUniverse", "UniverseAccepted", "SnapshotManifest"] + ["SnapshotFileChunk"] * chunks + ["SnapshotSeal", "SnapshotAccepted",
         "DependencySourceManifest"] + ["DependencySourceChunk"] * chunks + ["DependencySourceSeal", "DependencySourceAccepted"]
    if prepared:
        s += ["PreparedOutputManifest"] + ["PreparedOutputChunk"] * chunks + ["PreparedOutputSeal", "PreparedOutputAccepted"]
    return s + ["NativeContextVerified", "Analyze", "FactBatch", "CoverageV3"]


results = {"cases": 0, "lawfulRefused": [], "perturbedAdmitted": [], "ownerNotP328": []}
for prepared, chunks in itertools.product([False, True], [0, 2]):
    seq = full(prepared, chunks)
    # host order: host sends frames up to position k (host transcript); worker read prefix j of host frames sent since W
    for k in range(1, len(seq) + 1):
        host = seq[:k]
        if host[-1] not in H2W and k < len(seq) and seq[k] in H2W:
            pass
        widx = max([i for i, f in enumerate(host) if f not in H2W], default=-1)
        # worker may have read any number of the trailing host frames (at least Hello)
        tail = list(range(max(widx + 1, 1), k + 1))
        if widx == -1:
            tail = list(range(1, k + 1))
        # skip host transcripts where the host would still be waiting for a worker frame but sends nothing more: fine
        for cut in tail:
            observed = host[:cut]
            phase = my_replay(observed, prepared)
            eid = EX if "OpenUniverse" in observed else None
            aord = 0 if "Analyze" in observed else None
            events = [ev(f, prepared) for f in host]
            if phase not in PRE:
                continue
            results["cases"] += 1
            fault = {"executionId": eid, "analysisOrdinal": aord, "phase": phase, "faultKind": "compiler-crash", "detailCode": "x"}
            try:
                AR.provider_fault(doc, p3, TOK, events, fault)
            except AR.Refuse as e:
                results["lawfulRefused"].append([host[-3:], cut, fault["phase"], str(e)])
            own = NE.protocol3_run(events + [{"frame": "ProviderFault"}], stage_count=1)
            if own["trace"][-1] != "P3-28":
                results["ownerNotP328"].append([host[-2:], own["trace"][-2:]])
            # perturbations: flip each null/echo and a wrong phase not reachable by any cut
            reachable = {(my_replay(host[:c], prepared), EX if "OpenUniverse" in host[:c] else None, 0 if "Analyze" in host[:c] else None) for c in tail}
            for alt in ({**fault, "executionId": None if eid else EX}, {**fault, "analysisOrdinal": None if aord is not None else 0},
                        {**fault, "phase": "WAIT_HELLO_ACK" if phase != "WAIT_HELLO_ACK" else "READY_ANALYZE"}):
                if (alt["phase"], alt["executionId"], alt["analysisOrdinal"]) in reachable:
                    continue
                try:
                    AR.provider_fault(doc, p3, TOK, events, alt)
                    results["perturbedAdmitted"].append([host[-3:], alt])
                except AR.Refuse:
                    pass
results["lawfulRefused"] = results["lawfulRefused"][:10]
results["perturbedAdmitted"] = results["perturbedAdmitted"][:10]
results["ownerNotP328"] = results["ownerNotP328"][:10]
# Two-stage: fault after first CoverageV3 (worker frame; no host frame in flight)
seq = full(False, 0) + ["CoverageV3"]
events = [ev(f, False) for f in full(False, 0)[:-1]]  # ... FactBatch, CoverageV3 (stage 1)
try:
    AR.provider_fault(doc, p3, TOK, events, {"executionId": EX, "analysisOrdinal": 0, "phase": "ANALYZING", "faultKind": "internal-invariant", "detailCode": "x"})
    results["midStreamAnalyzingAdmitted"] = True
except AR.Refuse as e:
    results["midStreamAnalyzingAdmitted"] = str(e)
# Worker that never read Hello writes START-phase fault after host sent Hello
try:
    AR.provider_fault(doc, p3, TOK, [ev("Hello", False)], {"executionId": None, "analysisOrdinal": None, "phase": "START", "faultKind": "internal-invariant", "detailCode": "x"})
    results["startPhaseFaultAdmitted"] = True
except AR.Refuse as e:
    results["startPhaseFaultAdmitted"] = str(e)
own = NE.protocol3_run([ev("Hello", False), {"frame": "ProviderFault"}])
results["ownerHelloThenFault"] = own["trace"]
print(json.dumps(results, indent=1))
