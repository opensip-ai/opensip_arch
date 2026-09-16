"""Shared loader/mutation/recording helpers for the capture assessment (frozen41).

The tree is selected by env VA_TREE (a repo root). Default: the verified frozen41 snapshot, loaded
read-only (-I -B, nothing written there). A runtime copy (base or patched) is used for any before/
after comparison.

STANDING
  admission   admit_execution_inputs over a manifest (builder-built, or host-authored and so labelled).
  closed-run  the maintained check-execution-inputs.v1.full_run driver (owner ADMIT -> R.derive -> seal
              -> IDENTITY.close_run). `exactManifest` is true only when the proof's executionInputsDigest
              equals raw_digest of the very manifest the admission column admitted.
No standalone probe claims full Run admission.
"""
import copy
import hashlib
import importlib.util
import json
import os
import traceback
from pathlib import Path

TREE = Path(os.environ.get("VA_TREE", "/tmp/opensip-design-corrections/candidate-subject.v41"))
FOUNDATION = TREE / "docs/coop/design-corrections/foundation"
RUNTIME = Path("/private/tmp/opensip-design-corrections/claude-attribution-capture-assessment.v1")

_spec = importlib.util.spec_from_file_location("cap_check_execution_inputs", FOUNDATION / "check-execution-inputs.v1.py")
K = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(K)
M, F, H = K.M, K.F, K.H
C = M.C
NH = F.fixture_helpers()
COV_SCHEMA = NH.N.schema_document_digest(NH.N.NATIVE_SCHEMA_DOC)


def short(x):
    return None if x is None else str(x).split(":", 1)[-1][:10]


def build(**kwargs):
    return F.build_file_inputs(atom_override=K.NONE_ATOM, **kwargs)


def binding_universe(G, capability, program=0):
    for cell in G["enumerationPlan"]["cells"]:
        if cell["capabilityId"] == capability:
            return next(b["universe"] for b in cell["programBindings"] if b["ordinal"] == program)
    raise LookupError(capability)


def other_universe(G, uni):
    return next(b["universe"] for c in G["enumerationPlan"]["cells"] for b in c["programBindings"]
                if b["universe"] not in (None, uni))


def provider(G):
    return G["objects"][G["viewIds"][0]][1]["producerClosure"]


def rel_schema(G):
    return next(d for d in G["objects"][G["viewIds"][0]][1]["schemaDigests"] if d != COV_SCHEMA)


def single_view(G, relation, uni):
    for k in G["viewIds"]:
        v = G["objects"][k][1]
        if [(G["objects"][s][1]["relation"], G["objects"][s][1]["sourceUniverse"]) for s in v["scopeIds"]] == [(relation, uni)]:
            return k
    raise LookupError(relation + "@" + str(uni))


def mint_scope(G, relation, resolution, uni, subjects=()):
    return K._mint(G["objects"], "subject-scope", {
        "snapshotId": G["inputs"]["plan"]["snapshotId"], "sourceUniverse": uni, "targetUniverse": uni,
        "relation": relation, "resolution": resolution, "enumeratorClosure": provider(G),
        "subjects": M.canon_str_list(list(subjects)),
    })


def mint_coverage(G, sid, uni, resolved=True):
    paths = [r["path"] for r in G["snapshot"]["sourceInventory"]]
    scope = G["objects"][sid][1]
    payload = NH.coverage_result(scope, uni, resolved, G["blobs"], paths)
    admitted = NH.N.admit_coverage_result_v3(payload, scope, [], COV_SCHEMA)
    if admitted.get("result") != "ADMIT":
        raise RuntimeError("native owner refused probe coverage: " + str(admitted))
    return K._mint(G["objects"], "coverage", {"scopeId": sid, "payloadSchemaDigest": COV_SCHEMA,
                                             "payloadDigest": K._blob(G["blobs"], payload)})


def mint_view(G, scope_ids, facts=(), coverage_ids=()):
    return K._mint(G["objects"], "view", {
        "planId": G["inputs"]["planId"], "scopeIds": M.canon_str_list(list(scope_ids)),
        "facts": M.canon_str_list(list(facts)), "coverageIds": M.canon_str_list(list(coverage_ids)),
        "producerClosure": provider(G), "schemaDigests": M.canon_str_list([rel_schema(G), COV_SCHEMA]),
    })


def set_views(G, retire=(), add=(), *, in_view_ids=True, in_refs=True):
    """Apply explicit returned-view identifiers. `in_view_ids` edits graph['viewIds'] (the builder input and
    the Run's semantic-evidence view set); `in_refs` edits inputs.evaluationInputRefs view refs."""
    retire, add = set(retire), list(add)
    if in_view_ids:
        G["viewIds"] = M.canon_str_list([v for v in G["viewIds"] if v not in retire] + add)
    if in_refs:
        refs = [r for r in G["inputs"]["evaluationInputRefs"]
                if not (r["domain"] == "view" and "view2:" + r["digest"] in retire)]
        G["inputs"]["evaluationInputRefs"] = K.canon_refs(refs + [{"domain": "view", "digest": K.hx(a)} for a in add])
    kept = [G["objects"][v][1] for v in G["viewIds"]]
    G["coverageIds"] = M.canon_str_list([c for v in kept for c in v["coverageIds"]])
    G["scopeIds"] = M.canon_str_list([s for v in kept for s in v["scopeIds"]])
    G["inputs"]["coverageCount"] = len(G["coverageIds"])
    if G.get("viewId") in retire and add:
        G["viewId"] = add[0]


def manifest_facts(manifest, view_id):
    h = K.hx(view_id)
    return {
        "inReceiptOutputRefs": any(r["domain"] == "view" and r["digest"] == h
                                   for rc in manifest["hostCapture"]["stageReceipts"] for r in rc["outputRefs"]),
        "inSelectedRefs": any(r["domain"] == "view" and r["digest"] == h for r in manifest["selectedRefs"]),
        "rowsNaming": [r["capabilityId"] + "#" + str(r["programOrdinal"]) for r in manifest["cellOutcomes"]
                       if h in r["viewDigests"]],
    }


def rows(manifest):
    return {r["capabilityId"] + "#" + str(r["programOrdinal"]): [short(v) for v in r["viewDigests"]]
            for r in manifest["cellOutcomes"]}


def attach_exact(G, manifest):
    """Host-authored manifest hashed into the graph exactly as attach_host_capture stores a manifest."""
    digest = M.raw_digest(manifest)
    G["blobs"][digest] = C.canonical(manifest)
    G["inputs"]["executionInputsDigest"] = digest
    G["inputs"]["evaluationInputRefs"] = K.canon_refs(
        list(manifest["selectedRefs"]) + [{"domain": "execution-inputs", "digest": digest}])
    G["executionInputs"] = manifest
    G["executionInputsDigest"] = digest
    return G


def closed_run(G, manifest):
    want = M.raw_digest(manifest)
    try:
        result, proof = K.full_run(copy.deepcopy(G))
    except Exception as exc:  # noqa: BLE001 - recorded verbatim
        return {"standing": "closed-run", "ran": False, "exception": type(exc).__name__ + ":" + str(exc)[:700]}
    return {"standing": "closed-run", "ran": True, "verdict": result.get("verdict"), "runId": result.get("runId"),
            "executionCauses": sorted(d["cause"] for d in proof.get("executionDeficiencies") or []),
            "proofExecutionInputsDigest": proof.get("executionInputsDigest"),
            "exactManifest": proof.get("executionInputsDigest") == want}


class Recorder:
    def __init__(self):
        self.order, self.results = [], {}

    def add(self, name, entry):
        self.order.append(name)
        self.results[name] = entry

    def world(self, name, G, *, watch=(), host_edit=None, run_closed=True, note=None):
        entry = {"note": note, "tree": str(TREE)}
        try:
            kw = K.manifest_from_owner(copy.deepcopy(G))
            manifest = kw["execution_inputs"]
            entry["manifestSource"] = "builder"
            if host_edit is not None:
                host_edit(manifest)
                kw["store_pointers"] = M.promised_pointers(manifest, kw["plan"], kw["execution_plan"], kw["enumeration_plan"],
                                                           objects=kw["objects"], blobs=kw["blobs"])["store_pointers"]
                entry["manifestSource"] = "host-authored (builder output edited)"
            entry["manifestDigest"] = M.raw_digest(manifest)
            entry["rows"] = rows(manifest)
            entry["graphViewIdCount"] = len(G["viewIds"])
            entry["receiptViewCount"] = sum(1 for rc in manifest["hostCapture"]["stageReceipts"] for r in rc["outputRefs"] if r["domain"] == "view")
            entry["selectedViewCount"] = sum(1 for r in manifest["selectedRefs"] if r["domain"] == "view")
            entry["watch"] = {short(v): dict(manifest_facts(manifest, v), inGraphViewIds=v in G["viewIds"],
                                             inGraphEvaluationInputRefs=any(r["domain"] == "view" and r["digest"] == K.hx(v)
                                                                            for r in G["inputs"]["evaluationInputRefs"]),
                                             inStoreCensus=v in G["objects"])
                              for v in watch}
            res = K.admit(kw)
            entry["admission"] = {"result": res.get("result"), "refusals": res.get("refusals"),
                                  "derivedOutcomeStates": [d.get("state") for d in res.get("derivedOutcomes") or []]}
            if run_closed:
                GG = copy.deepcopy(G)
                if host_edit is not None:
                    attach_exact(GG, manifest)
                entry["closedRun"] = closed_run(GG, manifest)
        except Exception as exc:  # noqa: BLE001 - failed attempts are preserved
            entry["probeError"] = type(exc).__name__ + ":" + str(exc)[:700]
            entry["traceback"] = traceback.format_exc()[-2500:]
        self.add(name, entry)
        return entry

    def report(self, rel):
        path = RUNTIME / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            raise SystemExit("refusing to overwrite receipt " + str(path))
        raw = json.dumps({"tree": str(TREE), "order": self.order, "worlds": self.results}, indent=2, sort_keys=True, default=str).encode() + b"\n"
        path.write_bytes(raw)
        for name in self.order:
            e = self.results[name]
            print("==", name, "[" + str(e.get("manifestSource")) + "]")
            if "probeError" in e:
                print("   PROBE ERROR", e["probeError"])
                continue
            for k in ("admission",):
                if k in e:
                    print("   admission", e[k]["result"], e[k]["refusals"])
            cr = e.get("closedRun")
            if cr:
                print("   closed-run", (cr.get("verdict"), cr.get("executionCauses"), "exactManifest", cr.get("exactManifest"))
                      if cr.get("ran") else "NOT CLOSED: " + cr.get("exception", "")[:400])
            if "graphViewIdCount" in e:
                print("   graph viewIds", e["graphViewIdCount"], "receipt views", e["receiptViewCount"], "selected views", e["selectedViewCount"])
            for k, v in (e.get("watch") or {}).items():
                print("   watch", k, v)
            if "rows" in e:
                print("   rows", e["rows"])
            for k, v in e.items():
                if k.startswith("x-"):
                    print("  ", k, v)
        print("receipt", rel, hashlib.sha256(raw).hexdigest())
