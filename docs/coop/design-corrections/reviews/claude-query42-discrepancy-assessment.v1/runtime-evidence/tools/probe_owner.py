"""Author diagnostic probe over EXACT consumer exports, requests and host observations (frozen source42).

Standing: author diagnosis, not independent acceptance and not a blind reconstruction.
- Transport: root's pinned reader /tmp/.../root-blind39-transport-preparation.v1/check-export.py (hash-checked).
- Owners: identity-model.v3.py and query_projection_model.v3.py loaded read-only from VA_TREE (default frozen42).
- Every Run is structurally and fully semantically admitted (close_run) before any query call.
- No cursor translation, no request/host rewrite for captured vectors; discriminating probes are labelled NEW-WORLD
  and only ever use the owner's OWN issued tokens or explicitly varied lawful host observations.
Receipt: receipts/<argv1>.
"""
import copy
import hashlib
import importlib.util
import json
import os
import sys
import traceback
from pathlib import Path

TREE = Path(os.environ.get("VA_TREE", "/tmp/opensip-design-corrections/candidate-subject.v42"))
RT = Path("/private/tmp/opensip-design-corrections/claude-query42-discrepancy-assessment.v1")
OUT = Path("/tmp/opensip-design-corrections/consumer-b.v24-source42.v2/output")
T_PATH = Path("/tmp/opensip-design-corrections/root-blind39-transport-preparation.v1/check-export.py")
T_SHA = "6fa376bb59548bd9d52dbc52a3a35f27e0d12e4a963a6730624467c3a8f63074"
VEC_SHA = "f47edb50affbab018390c6599d3aae5b780af826ad30a4f4b29b5e1416111884"
EXPORTS = {"cmp-base": ("runs/cmp-base.store.json", "f4039acfce5cfe79828a705c2aa2f60e8febace652456caadc3c7888f5c9530b",
                        "run3:88d6ffc50e2a8d517717056b7c0ccfa3c072be624f6919b733b17514fb987e54"),
           "cmp-code": ("runs/cmp-code.store.json", "a1e19ef79e0db5a27fa89dced840cd3f71a4c02ba9a3ae7802cd174b41c9fc8a",
                        "run3:a3bfb0189bb733319998b7e73b591c224af02ab5590807be1f77dc65eea621ee")}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


assert sha(T_PATH.read_bytes()) == T_SHA
TR = load("pq_transport", T_PATH)
M = load("pq_identity", TREE / "docs/coop/design-corrections/foundation/identity-model.v3.py")
Q = load("pq_query", TREE / "docs/coop/design-corrections/workflows/query_projection_model.v3.py")
VRAW = (OUT / "vectors/graph-query.json").read_bytes()
assert sha(VRAW) == VEC_SHA
V = TR.parse(VRAW)

RUNS = {}
for label, (rel, want, run_id) in EXPORTS.items():
    raw = (OUT / rel).read_bytes()
    assert sha(raw) == want, label
    objects, blobs, notes = TR.decode(raw, M)
    dom, run = objects[run_id]
    assert dom == "run"
    assert M.open_run_closure(run, objects, blobs)[0] == run_id
    assert M.close_run(run, objects, blobs) == run_id
    RUNS[label] = (run, objects, blobs)


def call(label, request, host):
    run, objects, blobs = RUNS[label]
    try:
        resp = Q.execute_graph_query(copy.deepcopy(request), copy.deepcopy(run), copy.deepcopy(objects),
                                     copy.deepcopy(blobs), host=copy.deepcopy(host))
        return {"outcome": "RETURNED", "response": resp}
    except Q.QueryRefusal as exc:
        env = exc.envelope(copy.deepcopy(host))
        return {"outcome": "REFUSED", "envelope": env, "termination": exc.termination(),
                "diagnostic": getattr(exc, "diagnostic", None), "exceptionMessage": str(exc)}
    except Q.ReferenceCallPrecondition as exc:
        return {"outcome": "REFERENCE_PRECONDITION", "missing": exc.missing, "remedy": exc.remedy}
    except Exception as exc:  # noqa: BLE001 - preserved verbatim
        return {"outcome": "EXCEPTION", "type": type(exc).__name__, "message": str(exc)[:800],
                "traceback": traceback.format_exc()[-1500:]}


def schema_ok(ref, value):
    try:
        Q.validate_schema(ref, value)
        return True, None
    except Exception as exc:  # noqa: BLE001
        return False, (type(exc).__name__ + ":" + str(exc))[:400]


ROUTE_KEYS = ("class", "errorCode", "faultCause")


def route_view(env):
    term = env.get("termination") or {}
    detail = term.get("domainDetail") or {}
    errs = env.get("errors") or []
    return {"kind": env.get("kind"), "exitCode": env.get("exitCode"), "requestId": env.get("requestId"),
            "projectId": env.get("projectId"), "hasRun": "run" in env,
            **{k: term.get(k) for k in ROUTE_KEYS}, "termRunId": term.get("runId"),
            "detailCode": detail.get("code"), "errorsCodes": [e.get("code") for e in errs], "errorsCount": len(errs)}


def prose_view(env):
    detail = ((env.get("termination") or {}).get("domainDetail")) or {}
    errs = env.get("errors") or []
    return {"remedy": detail.get("remedy"), "subject": detail.get("subject"),
            "errorsRemedy": [e.get("remedy") for e in errs], "errorsSubject": [e.get("subject") for e in errs]}


report = {"tree": str(TREE), "queryOwnerSha256": sha((TREE / "docs/coop/design-corrections/workflows/query_projection_model.v3.py").read_bytes()),
          "identityOwnerSha256": sha((TREE / "docs/coop/design-corrections/foundation/identity-model.v3.py").read_bytes()),
          "vectorsSha256": VEC_SHA, "transportSha256": T_SHA,
          "runsAdmitted": {k: EXPORTS[k][2] for k in RUNS}, "vectors": {}, "newWorld": {}}

for row in V["vectors"]:
    if row["run"] not in RUNS:
        report["vectors"][row["vector"]] = {"run": row["run"], "skipped": "run label not in exported cmp-base/cmp-code (root accounting)"}
        continue
    got = call(row["run"], row["request"], row["hostObservations"])
    rec = {"run": row["run"], "classification": row.get("classification"), "owner": got}
    if "response" in row:
        rec["consumerKind"] = "response"
        rec["consumerResponseSchemaAdmitted"] = schema_ok(Q.SCHEMA_ID + "#/$defs/GraphQueryResponseV1", row["response"])
    else:
        rec["consumerKind"] = "failure"
        cenv = row["failureEnvelope"]
        rec["consumerEnvelopeSchemaAdmitted"] = schema_ok(Q.ENVELOPE_ID, cenv)
        if got["outcome"] == "REFUSED":
            o, c = route_view(got["envelope"]), route_view(cenv)
            rec["routeEqual"] = o == c
            rec["routeDiff"] = {k: [c[k], o[k]] for k in o if o[k] != c[k]}
            rec["proseConsumer"], rec["proseOwner"] = prose_view(cenv), prose_view(got["envelope"])
    report["vectors"][row["vector"]] = rec

# ---------------- NEW-WORLD 1: cursor preimages and owner self-continuation ----------------
vec = {r["vector"]: r for r in V["vectors"]}
p1 = vec["page1-latest-size1"]
own_p1 = call("cmp-base", p1["request"], p1["hostObservations"])
run_id = EXPORTS["cmp-base"][2]
eff = Q.effective_params(p1["request"]["operation"], p1["request"]["params"])
views = own_p1["response"]["context"]["factViewDigests"]
owner_record = {"factViewDigests": sorted(views), "operation": p1["request"]["operation"], "params": eff,
                "projectId": p1["request"]["projectId"], "runId": run_id}
owner_pre = Q.canonical.canonical(owner_record)
consumer_eff = dict(p1["request"]["params"])
consumer_record = {"projectId": p1["request"]["projectId"], "runId": run_id, "factViewDigests": views,
                   "operation": p1["request"]["operation"], "params": consumer_eff, "order": "query-projection-contract.v3 s3/s4"}
consumer_pre = Q.canonical.canonical(consumer_record)
ctok = p1["response"]["context"]["nextCursor"]
otok = own_p1["response"]["context"]["nextCursor"]
report["newWorld"]["cursorPreimages"] = {
    "ownerRecord": owner_record, "ownerPreimageUtf8": owner_pre.decode(), "ownerHash": sha(owner_pre),
    "ownerTokenHash": otok.split(".")[2], "ownerHashReproduced": sha(owner_pre) == otok.split(".")[2],
    "consumerRecordAsImplemented": consumer_record, "consumerPreimageUtf8": consumer_pre.decode(), "consumerHash": sha(consumer_pre),
    "consumerTokenHash": ctok.split(".")[2], "consumerHashReproducedWithOwnerCanonical": sha(consumer_pre) == ctok.split(".")[2],
    "effectiveParamsEqualRequestParams": eff == p1["request"]["params"],
    "recordDifference": sorted(set(consumer_record) ^ set(owner_record)),
}
p2 = vec["page2-after-newer-latest-bound-run"]
own_req = copy.deepcopy(p2["request"])
own_req["page"]["cursor"] = otok
report["newWorld"]["ownerSelfContinuation"] = call("cmp-base", own_req, p2["hostObservations"])
pc = vec["page2-with-host-cache-present"]
own_req_c = copy.deepcopy(pc["request"])
own_req_c["page"]["cursor"] = otok
report["newWorld"]["ownerSelfContinuationWithCache"] = call("cmp-base", own_req_c, pc["hostObservations"])
a, b = report["newWorld"]["ownerSelfContinuation"], report["newWorld"]["ownerSelfContinuationWithCache"]
report["newWorld"]["cacheInvariant"] = a.get("response") == b.get("response") and a.get("outcome") == "RETURNED"
report["newWorld"]["ownerPage2VsConsumerPage2Items"] = (a.get("response") or {}).get("items") == p2["response"]["items"]

# ---------------- NEW-WORLD 2: path / neighbor orientation with lawful admitted endpoints ----------------
pb = vec["path-both-direction"]


def with_params(req, **over):
    r = copy.deepcopy(req)
    r["params"].update(over)
    return r


orient = {}
for label, req in (("path-both-helper-to-main", pb["request"]),
                   ("path-incoming-helper-to-main", with_params(pb["request"], direction="incoming")),
                   ("path-outgoing-main-to-helper", with_params(pb["request"], direction="outgoing",
                                                             start=pb["request"]["params"]["target"], target=pb["request"]["params"]["start"])),
                   ("path-outgoing-helper-to-main", with_params(pb["request"], direction="outgoing"))):
    got = call("cmp-code", req, pb["hostObservations"])
    item = ((got.get("response") or {}).get("items") or [None])[0]
    chain = None
    if item:
        chain = all(item["edges"][i]["source"] == item["nodes"][i] and item["edges"][i]["target"] == item["nodes"][i + 1]
                    for i in range(len(item["edges"])))
    orient[label] = {"outcome": got["outcome"], "item": item, "edgesChainNodes": chain}
nb_req = {"completeness": "best-effort", "operation": "graph.neighbors", "page": {"size": 100},
          "params": {"direction": "both", "endpoint": pb["request"]["params"]["start"], "minResolution": "resolved-callee", "relation": "calls"},
          "projectId": pb["request"]["projectId"], "schemaFamily": "opensip.product.query", "schemaMajor": 3, "view": pb["request"]["view"]}
nb = call("cmp-code", nb_req, pb["hostObservations"])
orient["neighbors-both-helper"] = {"outcome": nb["outcome"], "items": (nb.get("response") or {}).get("items")}
cons_item = pb["response"]["items"][0]
orient["consumerPathEdgesChainNodes"] = all(cons_item["edges"][i]["source"] == cons_item["nodes"][i] and cons_item["edges"][i]["target"] == cons_item["nodes"][i + 1]
                                            for i in range(len(cons_item["edges"])))
orient["consumerPathResponseSchemaAdmitted"] = schema_ok(Q.SCHEMA_ID + "#/$defs/GraphQueryResponseV1", pb["response"])
report["newWorld"]["orientation"] = orient

# ---------------- NEW-WORLD 3: availability observation reflected in the successful response ----------------
av = vec["availability-partial-does-not-grant-or-refuse"]
avail = {}
for label, obs in (("omitted", None), ("retained", "retained"), ("partial", "partial")):
    host = copy.deepcopy(av["hostObservations"])
    host.pop("availability", None)
    if obs is not None:
        host["availability"] = obs
    got = call("cmp-code", av["request"], host)
    r = got.get("response") or {}
    avail[label] = {"outcome": got["outcome"], "contextAvailability": (r.get("context") or {}).get("availability"),
                    "itemsSha256": sha(json.dumps(r.get("items"), sort_keys=True).encode()) if r else None}
partial_resp = copy.deepcopy((call("cmp-code", av["request"], av["hostObservations"]).get("response")))
if partial_resp:
    partial_resp["context"]["availability"] = "partial"
    avail["ownerResponseWithPartialSchemaAdmitted"] = schema_ok(Q.SCHEMA_ID + "#/$defs/GraphQueryResponseV1", partial_resp)
report["newWorld"]["availability"] = avail

# ---------------- NEW-WORLD 4: optional termination / note are schema-optional ----------------
single = vec["single-page-reference"]
stripped = copy.deepcopy(call("cmp-base", single["request"], single["hostObservations"])["response"])
stripped.pop("termination", None)
for lim in stripped["context"]["evidence"]["resolutionLimitations"]:
    lim.pop("note", None)
report["newWorld"]["ownerResponseWithoutTerminationSchemaAdmitted"] = schema_ok(Q.SCHEMA_ID + "#/$defs/GraphQueryResponseV1", stripped)
imp = vec["neighbors-imports-multi-kind-occupancy"]
imp_resp = copy.deepcopy(call("cmp-code", imp["request"], imp["hostObservations"])["response"])
for lim in imp_resp["context"]["evidence"]["resolutionLimitations"]:
    lim.pop("note", None)
imp_resp.pop("termination", None)
report["newWorld"]["ownerImportsResponseWithoutNotesSchemaAdmitted"] = schema_ok(Q.SCHEMA_ID + "#/$defs/GraphQueryResponseV1", imp_resp)

label = sys.argv[1] if len(sys.argv) > 1 else "probe-owner-base.json"
path = RT / "receipts" / label
path.parent.mkdir(parents=True, exist_ok=True)
if path.exists():
    raise SystemExit("refusing to overwrite " + str(path))
raw = json.dumps(report, indent=2, sort_keys=True, default=str).encode() + b"\n"
path.write_bytes(raw)
for name, rec in report["vectors"].items():
    o = rec.get("owner") or {}
    line = [name, rec.get("run"), rec.get("consumerKind"), o.get("outcome")]
    if o.get("outcome") == "REFUSED":
        t = o["termination"]
        line += [t.get("class"), t.get("errorCode"), (t.get("domainDetail") or {}).get("code"), "diag=" + str(o.get("diagnostic"))[:90]]
    if "routeEqual" in rec:
        line += ["routeEqual", rec["routeEqual"], rec["routeDiff"]]
    if "consumerEnvelopeSchemaAdmitted" in rec:
        line += ["consumerEnvSchema", rec["consumerEnvelopeSchemaAdmitted"][0]]
    if "consumerResponseSchemaAdmitted" in rec:
        line += ["consumerRespSchema", rec["consumerResponseSchemaAdmitted"][0]]
    print(*line)
nw = report["newWorld"]
print("cursor", json.dumps({k: v for k, v in nw["cursorPreimages"].items() if k.endswith(("Hash", "Reproduced", "ReproducedWithOwnerCanonical", "Difference", "RequestParams"))}))
print("ownerSelfContinuation", nw["ownerSelfContinuation"]["outcome"], "cacheInvariant", nw["cacheInvariant"], "page2ItemsEqualConsumer", nw["ownerPage2VsConsumerPage2Items"])
print("orientation", json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk != "item"}) for k, v in nw["orientation"].items()})[:2500])
print("availability", json.dumps(nw["availability"]))
print("optional termination/note schema", nw["ownerResponseWithoutTerminationSchemaAdmitted"], nw["ownerImportsResponseWithoutNotesSchemaAdmitted"])
print("receipt", label, sha(raw))
