"""Runtime-only world mutation helpers (a verbatim extraction of the stage-2 helpers, kept separate so
the already-recorded stage-2 receipt keeps its own provenance). Standing is identical to stage 2."""
import copy
import traceback

import probe_common as P

K, M, F = P.K, P.M, P.F
C = M.C
NH = F.fixture_helpers()
COV_SCHEMA = NH.N.schema_document_digest(NH.N.NATIVE_SCHEMA_DOC)


def build(**kwargs):
    return F.build_file_inputs(atom_override=K.NONE_ATOM, **kwargs)


def views_of(G):
    return {k: v for k, (d, v) in G["objects"].items() if d == "view" and k in G["viewIds"]}


def sc(G, sid):
    return G["objects"][sid][1]


def single_view(G, relation, uni):
    for k, v in views_of(G).items():
        scopes = [sc(G, s) for s in v["scopeIds"]]
        if len(scopes) == 1 and scopes[0]["relation"] == relation and scopes[0]["sourceUniverse"] == uni:
            return k
    raise LookupError("no single-scope view " + relation + "@" + str(uni))


def binding_universe(G, capability, program=0):
    for cell in G["enumerationPlan"]["cells"]:
        if cell["capabilityId"] == capability:
            return next(b["universe"] for b in cell["programBindings"] if b["ordinal"] == program)
    raise LookupError(capability)


def other_universe(G, uni):
    return next(b["universe"] for c in G["enumerationPlan"]["cells"] for b in c["programBindings"]
                if b["universe"] not in (None, uni))


def provider(G):
    return next(iter(views_of(G).values()))["producerClosure"]


def rel_schema(G):
    return next(d for d in next(iter(views_of(G).values()))["schemaDigests"] if d != COV_SCHEMA)


def mint_scope(G, relation, resolution, uni, subjects):
    return K._mint(G["objects"], "subject-scope", {
        "snapshotId": G["inputs"]["plan"]["snapshotId"], "sourceUniverse": uni, "targetUniverse": uni,
        "relation": relation, "resolution": resolution, "enumeratorClosure": provider(G),
        "subjects": M.canon_str_list(subjects),
    })


def mint_coverage(G, sid, uni):
    paths = [r["path"] for r in G["snapshot"]["sourceInventory"]]
    scope = sc(G, sid)
    payload = NH.coverage_result(scope, uni, True, G["blobs"], paths)
    admitted = NH.N.admit_coverage_result_v3(payload, scope, [], COV_SCHEMA)
    if admitted.get("result") != "ADMIT":
        raise RuntimeError("native owner refused probe coverage: " + str(admitted))
    pd = K._blob(G["blobs"], payload)
    return K._mint(G["objects"], "coverage", {"scopeId": sid, "payloadSchemaDigest": COV_SCHEMA, "payloadDigest": pd})


def mint_view(G, scope_ids, facts, coverage_ids):
    return K._mint(G["objects"], "view", {
        "planId": G["inputs"]["planId"], "scopeIds": M.canon_str_list(scope_ids),
        "facts": M.canon_str_list(facts), "coverageIds": M.canon_str_list(coverage_ids),
        "producerClosure": provider(G), "schemaDigests": M.canon_str_list([rel_schema(G), COV_SCHEMA]),
    })


def replace_views(G, retire, add):
    retire = set(retire)
    G["viewIds"] = M.canon_str_list([v for v in G["viewIds"] if v not in retire] + list(add))
    refs = [r for r in G["inputs"]["evaluationInputRefs"]
            if not (r["domain"] == "view" and "view2:" + r["digest"] in retire)]
    refs += [{"domain": "view", "digest": K.hx(a)} for a in add]
    G["inputs"]["evaluationInputRefs"] = K.canon_refs(refs)
    live = [G["objects"][v][1] for v in G["viewIds"]]
    G["coverageIds"] = M.canon_str_list([c for v in live for c in v["coverageIds"]])
    G["scopeIds"] = M.canon_str_list([s for v in live for s in v["scopeIds"]])
    G["inputs"]["coverageCount"] = len(G["coverageIds"])
    if G.get("viewId") in retire:
        G["viewId"] = add[0]


def row_by_cap(kw, capability, program=0):
    return next(r for r in kw["execution_inputs"]["cellOutcomes"]
                if r["capabilityId"] == capability and r["programOrdinal"] == program)


def closed_run(G):
    try:
        result, proof = K.full_run(copy.deepcopy(G))
    except Exception as exc:  # noqa: BLE001
        return {"standing": "closed-run", "ran": False, "exception": type(exc).__name__ + ":" + str(exc)[:600]}
    return {
        "standing": "closed-run", "ran": True, "verdict": result.get("verdict"), "runId": result.get("runId"),
        "executionCauses": sorted(d["cause"] for d in proof.get("executionDeficiencies") or []),
        "executionInputsDigest": proof.get("executionInputsDigest"),
    }


def attach_manifest(G, manifest):
    digest = M.raw_digest(manifest)
    G["blobs"][digest] = C.canonical(manifest)
    G["inputs"]["executionInputsDigest"] = digest
    G["inputs"]["evaluationInputRefs"] = K.canon_refs(
        list(manifest["selectedRefs"]) + [{"domain": "execution-inputs", "digest": digest}])
    G["executionInputs"] = manifest
    G["executionInputsDigest"] = digest
    return G


class Recorder:
    def __init__(self):
        self.order, self.results = [], {}

    def world(self, name, G, *, host_edit=None, run_closed=True, note=None):
        self.order.append(name)
        entry = {"note": note}
        try:
            kw = K.manifest_from_owner(copy.deepcopy(G))
            if host_edit is not None:
                host_edit(kw)
                promised = M.promised_pointers(kw["execution_inputs"], kw["plan"], kw["execution_plan"],
                                               kw["enumeration_plan"], objects=kw["objects"], blobs=kw["blobs"])
                kw["store_pointers"] = promised["store_pointers"]
            entry["describe"] = P.describe(kw)
            entry["admission"] = P.admit_summary(kw)
            if run_closed:
                GG = copy.deepcopy(G)
                if host_edit is not None:
                    attach_manifest(GG, kw["execution_inputs"])
                entry["closedRun"] = closed_run(GG)
                if entry["closedRun"].get("ran"):
                    entry["closedRun"]["digestEqualsAdmission"] = (
                        entry["closedRun"]["executionInputsDigest"] == entry["admission"]["executionInputsDigest"])
        except Exception as exc:  # noqa: BLE001
            entry["probeError"] = type(exc).__name__ + ":" + str(exc)[:600]
            entry["traceback"] = traceback.format_exc()[-2000:]
        self.results[name] = entry

    def closed_only(self, name, G, note=None):
        self.order.append(name)
        self.results[name] = {"note": note, "closedRun": closed_run(G)}

    def report(self, receipt_rel):
        digest = P.write_json(receipt_rel, {"order": self.order, "worlds": self.results})
        for name in self.order:
            e = self.results[name]
            print("==", name)
            if "probeError" in e:
                print("   PROBE ERROR", e["probeError"])
                continue
            if "admission" in e:
                print("   admission", e["admission"]["result"], e["admission"]["refusals"])
            cr = e.get("closedRun")
            if cr:
                print("   closed-run", cr.get("verdict") if cr.get("ran") else "NOT RUN: " + cr.get("exception", "")[:300],
                      cr.get("executionCauses"), "digest==admission", cr.get("digestEqualsAdmission"))
            for c in (e.get("describe") or {}).get("cells", []):
                print("   row", c["cell"], c["capabilityId"], "U", c["universe"], c["rowState"], "viewDigests", c["viewDigests"])
            for v in (e.get("describe") or {}).get("views", []):
                if len(v["scopes"]) > 1 or v["coverageCount"] != 1:
                    print("   view", v["view"], v["scopes"], "cov", v["coverageCount"], "receipt", v["inReceipt"],
                          "selected", v["inSelected"])
        print("receipt sha256", digest)
        return digest
