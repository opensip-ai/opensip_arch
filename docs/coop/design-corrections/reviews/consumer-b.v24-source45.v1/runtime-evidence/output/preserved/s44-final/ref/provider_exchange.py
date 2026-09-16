"""Provider exchange with payload admission before the published event machine (source44, HC-58).

The typescript-semantic machine is native/typescript-protocol2-order.v1.json (ref/protocol_ts2.py) and the rust-semantic machine is
native/protocol3-transitions.v1.json (ref/protocol3.py). Payload validation "is executed per frame ... before an event reaches this table" (TypeScript
table standing); protocol3-transitions#/ownedByProse leaves payloads to section 9 prose.

Order per event:
  1. an exchange already faulted absorbs the event;
  2. the payload of a payload-carrying frame is admitted (ref/provider_wire.py, ref/factbatch.py);
  3. the admitted event, with its derived observations (TypeScript eventObservations; Rust OpenUniverse derivedObservations), goes to the table.
FactBatch and Coverage payloads are correlated only when the host phase is ANALYZING, because the request/dispatch coordinates exist only there;
elsewhere the table decides alone and the payload is reported as not validated.

A payload refusal faults the exchange; the trace records `payload:<frame>-refused(<key>)`:
  - worker frames route PROVIDER.PROTOCOL_VIOLATION through the s10 fault projection;
  - host-authored frames route a host invariant.
Snapshot, dependency-source and prepared frames are abstract events, as in the kit's s9.7 reference scope.
"""
import copy

import factbatch as FB
import protocol3 as P3
import protocol_ts2 as TS2
import provider_wire as W

WORKER_FRAMES = {"HelloAck", "UniverseAccepted", "SnapshotAccepted", "DependencySourceAccepted", "PreparedOutputAccepted", "NativeContextVerified",
                 "FactBatch", "Coverage", "CoverageV3", "Unavailable", "BudgetExhausted", "Complete", "ProviderFault", "Cancelled"}


def requests_of(event, lang):
    """Current stage requests joined with the host-derived requested coverage domains the host fixed before spawn (event hostDomains, a host observation;
    delivery.v2 coverageDomain.authority, rust-provider-protocol.v2 planAndDomainProjection)."""
    analyze = event["analyze"]
    return [dict(FB.stage_request(analyze, lang, i), keys=dom["keys"], subjectCounts=dom["subjectCounts"]) for i, dom in enumerate(event["hostDomains"])]


class ProviderExchange:
    def __init__(self, lang, ctx):
        self.lang, self.ctx = lang, ctx
        self.m = TS2.TypeScriptProtocol2() if lang == "ts" else P3.Protocol3()

    def run(self, events):
        lang, ctx = self.lang, self.ctx
        derived, trace, states, admissions, payloads = [], [], [], [], []
        adm = {"hello": None, "ack": None, "openUniverse": None, "analyze": None, "requests": None, "cancelPhase": None, "cancel": None}
        stream, fault_state, refusal = {}, None, None
        for i, e in enumerate(events):
            frame = e["frame"]
            if fault_state is not None:
                trace.append({"frame": frame, "rule": "FAULT-absorb", "phase": "FAULT"})
                states.append(copy.copy(fault_state))
                continue
            before = self.m.run(derived)["state"]
            ev = {k: v for k, v in e.items()}
            p = e.get("payload")
            faults, obs, note = [], {}, None
            if frame == "Hello":
                faults = W.admit_hello(lang, p, ctx["trusted"])
                adm["hello"] = p if not faults else None
            elif frame == "HelloAck":
                faults = W.admit_hello_ack(lang, p, adm["hello"], ctx["trusted"])
                adm["ack"] = p if not faults else None
                obs["capabilities"] = (p or {}).get("capabilities")
            elif frame == "OpenUniverse" and p is not None:
                faults, derived_obs = W.admit_open_universe(lang, p, dict(ctx["startup"], hello=adm["hello"], helloAck=adm["ack"]))
                adm["openUniverse"] = p if not faults else None
                if derived_obs is not None:
                    ev["derivedObservations"] = derived_obs
            elif frame == "UniverseAccepted" and p is not None:
                faults = W.admit_universe_accepted(lang, p, adm["openUniverse"])
            elif frame == "NativeContextVerified" and p is not None:
                faults = W.admit_native_context_verified(p, adm["openUniverse"])
            elif frame == "Unavailable" and p is not None:
                faults, kind = W.admit_unavailable(lang, p, before["phase"], adm["openUniverse"], adm["requests"])
                obs["unavailablePayload"] = kind
            elif frame == "Analyze" and "analyze" in e:
                rf = FB.analyze_request_faults(e["analyze"], lang, ctx["retained"], e["stageCount"])
                faults = [W.fault("cb24.ANALYZE_REQUEST", x) for x in rf]
                adm["analyze"], adm["requests"] = e["analyze"], requests_of(e, lang)
            elif frame == "FactBatch" and p is not None:
                if before["phase"] == "ANALYZING" and adm["analyze"] is not None:
                    request = FB.stage_request(adm["analyze"], lang, before["stageIndex"])
                    dispatch = FB.derive_dispatch(ctx["retained"], request, stream) if e.get("dispatch", "derive") == "derive" else e["dispatch"]
                    hc = (adm["hello"] or {}).get("expectedCapabilities")
                    ac = (adm["ack"] or {}).get("capabilities")
                    res = FB.buffer_fact_batch_occupancy(p, hc, ac, dispatch, ctx["retained"], request, ctx["host"], lang)
                    payloads.append({"step": i, "payloadChecked": True, "request": request, **res})
                    faults = [W.fault(v["key"], v["detail"]) for v in res["violations"]]
                else:
                    payloads.append({"step": i, "payloadChecked": False,
                                     "reason": f"FactBatch arrives in phase {before['phase']}; the table decides before request/batch correlation exists"})
            elif frame in ("Coverage", "CoverageV3") and p is not None:
                if before["phase"] == "ANALYZING" and adm["requests"] is not None and before["stageIndex"] < len(adm["requests"]):
                    faults = W.admit_coverage(lang, p, adm["requests"][before["stageIndex"]], adm["analyze"]["analysisOrdinal"])
                else:
                    note = f"Coverage arrives in phase {before['phase']}; the table decides"
            elif frame == "BudgetExhausted" and p is not None:
                faults = W.admit_budget_exhausted(lang, p, adm["requests"], (adm["analyze"] or {}).get("analysisOrdinal"))
            elif frame == "Cancelled" and p is not None:
                if before["phase"] == "WAIT_CANCELLED":
                    faults = W.admit_cancelled(lang, p, adm["cancelPhase"], adm["cancel"])
                else:
                    note = f"Cancelled arrives in phase {before['phase']}; the table decides"
            if frame == "Cancel":
                adm["cancelPhase"], adm["cancel"] = before["phase"], p
            if obs:
                ev["observations"] = obs
            admissions.append({"step": i, "frame": frame, "hostPhase": before["phase"], "faults": faults, "observations": obs or None, "note": note})
            if faults:
                origin = "provider-return" if frame in WORKER_FRAMES else "host-internal"
                fault_state = dict(before, phase="FAULT")
                refusal = {"step": i, "frame": frame, "firstRefusal": faults[0]["key"], "origin": origin,
                           "route": P3.stage_authority(None, True)["d9"] if origin == "provider-return" else
                           dict(W.FB.ROUTES["input-schema-invalid:host-internal"]["termination"], detail="HOST.INVARIANT_VIOLATED")}
                trace.append({"frame": frame, "rule": f"payload:{frame}-refused({faults[0]['key']})", "phase": "FAULT"})
                states.append(copy.copy(fault_state))
                continue
            if frame == "FactBatch" and payloads and payloads[-1]["step"] == i and payloads[-1]["payloadChecked"]:
                FB.advance(stream, p)
            derived.append(ev)
            step = self.m.run(derived)
            trace.append(step["trace"][-1])
            states.append(step["state"])
        final = copy.copy(fault_state) if fault_state is not None else self.m.run(derived)["state"]
        return {"language": lang, "machine": "typescript-protocol2-order.v1.json" if lang == "ts" else "protocol3-transitions.v1.json",
                "trace": trace, "states": states, "state": final, "admissions": admissions, "payloads": payloads, "refusal": refusal,
                "negotiated": FB.negotiated((adm["hello"] or {}).get("expectedCapabilities"), (adm["ack"] or {}).get("capabilities")),
                "openUniverse": adm["openUniverse"]}
