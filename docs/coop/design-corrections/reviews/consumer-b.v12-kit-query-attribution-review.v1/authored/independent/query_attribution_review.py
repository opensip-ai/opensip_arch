#!/usr/bin/env python3
"""Bounded independent review of TS author query-attribution gaps and original query input suitability."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
sys.path.insert(0, str(OUT))

from independent.admit_run import Store, digest_of, hex_of  # noqa: E402
from independent.kit_core import C, parse_h_frame  # noqa: E402

NEW = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-query-attribution-review.v1/new-inputs")
SNAP_STORE = NEW / "runs/ts.store.json"
MAN = NEW / "input-manifest.json"
INV_CLAIM = NEW / "query-run-graph-inventory.json"
KIT_MANIFEST = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v1/subject/consumer-input-manifest.json")
REQ = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v1/requirements.json")
CHARTER = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-selfaudit.v3/original-consumer-charter.txt")
PYTHON = "/tmp/opensip-architecture-review-env/bin/python"

EXPECTED_MAN = "7ca1f3c9e8a68acecf23584998a90bd04ebac4c97f1310a6f076bb29c830003d"
EXPECTED_KIT = "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8"
EXPECTED_REQ = "855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495"
EXPECTED_CHARTER = "57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_graph(store: Store) -> dict:
    run_id = sorted(k for k in store.object_table if str(k).startswith("run3:"))[0]
    run = parse_h_frame(store.rehash(store.object_table[run_id]["digest"]), allowed_domains={"run"})["value"]
    plan = parse_h_frame(store.rehash(store.object_table[run["planId"]]["digest"]), allowed_domains={"plan"})["value"]
    seal = parse_h_frame(store.rehash(store.object_table[run["evaluationSealId"]]["digest"]), allowed_domains={"evaluation-seal"})["value"]
    proof = parse_h_frame(store.rehash(store.object_table[seal["proofBundleId"]]["digest"]), allowed_domains={"proof-bundle"})["value"]
    ei = store.parse_canonical(proof["executionInputsDigest"])
    view_ref = next(r for r in ei["selectedRefs"] if r["domain"] == "view")
    view = parse_h_frame(store.rehash(view_ref["digest"]), allowed_domains={"view"})["value"]
    snap = parse_h_frame(store.rehash(store.object_table[run["snapshotId"]]["digest"]), allowed_domains={"snapshot"})["value"]
    facts = []
    for fid in view["facts"]:
        rec = parse_h_frame(store.rehash(store.object_table[fid]["digest"]), allowed_domains={"fact"})["value"]
        pl = store.parse_canonical(rec["payloadDigest"])
        facts.append({"id": fid, "record": rec, "payload": pl})
    coverages = []
    for cid in view["coverageIds"]:
        crec = parse_h_frame(store.rehash(store.object_table[cid]["digest"]), allowed_domains={"coverage"})["value"]
        cpl = store.parse_canonical(crec["payloadDigest"])
        coverages.append({"id": cid, "h": crec, "payload": cpl})
    inventories = []
    seen = set()
    for r in ei["selectedRefs"]:
        if r["domain"] == "subject-inventory" and r["digest"] not in seen:
            seen.add(r["digest"])
            inventories.append({"digest": r["digest"], "record": store.parse_canonical(r["digest"])})
    attrs = []
    for r in ei["selectedRefs"]:
        if r["domain"] == "target-attribution":
            attrs.append({"digest": r["digest"], "record": store.parse_canonical(r["digest"])})
    for r in (ei.get("hostCapture") or {}).get("hostDerivedRefs") or []:
        if r["domain"] == "target-attribution" and r["digest"] not in {a["digest"] for a in attrs}:
            attrs.append({"digest": r["digest"], "record": store.parse_canonical(r["digest"])})
    return {
        "run_id": run_id,
        "run": run,
        "plan": plan,
        "seal": seal,
        "proof": proof,
        "ei": ei,
        "view": view,
        "view_digest": view_ref["digest"],
        "snapshot": snap,
        "facts": facts,
        "coverages": coverages,
        "inventories": inventories,
        "attributions": attrs,
        "store": store,
    }


def tree_shas(closure: dict) -> set[str]:
    return {row["sha256"] for row in (closure.get("tree") or [])}


def endpoint(universe: str, kind: str, native: str, pkg: str = "") -> dict:
    return {"universe": universe, "kind": kind, "nativeSubjectId": native, "packageManifestPath": pkg}


def tuple_key(e: dict) -> tuple:
    return (e["universe"], e["kind"], e["nativeSubjectId"], e.get("packageManifestPath") or "")


def main() -> int:
    probes = OUT / "probes"
    probes.mkdir(parents=True, exist_ok=True)
    man = json.loads(MAN.read_text())
    file_ok = []
    for e in man["files"]:
        p = NEW / e["path"]
        file_ok.append({"path": e["path"], "sha256": sha(p), "match": sha(p) == e["sha256"] and p.stat().st_size == e["bytes"]})
    claim = json.loads(INV_CLAIM.read_text())
    store = Store.load(SNAP_STORE)
    g = load_graph(store)

    uni = hex_of(g["facts"][0]["record"]["sourceUniverse"])
    snap_paths = [r["path"] for r in g["snapshot"]["sourceInventory"]]

    inv_rows = []
    for inv in g["inventories"]:
        rec = inv["record"]
        for row in rec.get("rows") or []:
            inv_rows.append(
                {
                    "inventoryDigest": inv["digest"],
                    "kind": row.get("kind"),
                    "nativeSubjectId": row.get("nativeSubjectId"),
                    "path": row.get("path"),
                    "cellOrdinal": rec.get("cellOrdinal"),
                    "programOrdinal": rec.get("programOrdinal"),
                }
            )
    file_inv_ids = sorted({r["nativeSubjectId"] for r in inv_rows if r["kind"] == "file"})
    symbol_inv_ids = sorted({r["nativeSubjectId"] for r in inv_rows if r["kind"] == "symbol"})

    imports_facts = [f for f in g["facts"] if f["record"]["relation"] == "imports" and f["record"]["resolution"] == "resolved-target"]
    attr_by_fact = {a["record"]["sourceFactId"]: a for a in g["attributions"]}

    projected = []
    unprojectable = []
    for f in imports_facts:
        pl = f["payload"]
        attr = attr_by_fact.get(f["id"])
        src = endpoint(uni, "symbol", pl.get("importer") or "")
        if attr is None:
            unprojectable.append({"factId": f["id"], "reason": "imports@resolved-target without TargetAttributionV1", "payload": {"importer": pl.get("importer"), "resolvedTarget": pl.get("resolvedTarget"), "specifier": pl.get("specifier")}})
            continue
        ar = attr["record"]
        tgt = endpoint(hex_of(ar.get("targetUniverse")) or uni, ar.get("kind"), pl.get("resolvedTarget") or "")
        # occupancy join: never parse SubjectIdV1; first-party iff targetNativeId equals an inventory nativeSubjectId of that kind
        matches = [r for r in inv_rows if r["kind"] == ar.get("kind") and r["nativeSubjectId"] == ar.get("targetNativeId")]
        ephemeral_first_party = len({(r["kind"], r["nativeSubjectId"], r["path"]) for r in matches}) == 1
        projected.append(
            {
                "factId": f["id"],
                "source": src,
                "target": tgt,
                "specifier": pl.get("specifier"),
                "attributionDigest": attr["digest"],
                "attributionKind": ar.get("kind"),
                "attributionOccupancy": ar.get("occupancy"),
                "targetNativeId": ar.get("targetNativeId"),
                "logicalPath": ar.get("logicalPath"),
                "payloadEqualsTargetNativeId": ar.get("targetNativeId") == pl.get("resolvedTarget"),
                "ephemeralFirstPartyByExactNativeId": ephemeral_first_party,
                "externalConsistent": (not ephemeral_first_party) and ar.get("occupancy") == "external",
                "firstPartyWouldRefuseWithoutParse": ar.get("occupancy") == "first-party" and not ephemeral_first_party,
            }
        )

    # query tuple vertices
    inv_vertices = []
    for r in inv_rows:
        pkg = r["path"] if r["kind"] == "package" else ""
        inv_vertices.append(endpoint(uni, r["kind"], r["nativeSubjectId"], pkg))
    proj_vertices = []
    for e in projected:
        proj_vertices.append(e["source"])
        proj_vertices.append(e["target"])
    vertex_keys = sorted({tuple_key(v) for v in inv_vertices + proj_vertices})

    # claimed path: module:src/app.ts -> file:node_modules/left-pad/index.js over two facts
    # under tuple law source kind is always symbol
    start = endpoint(uni, "symbol", "module:src/app.ts")
    claimed_target_file = endpoint(uni, "file", "file:node_modules/left-pad/index.js")
    # BFS on projected edges
    adj = {}
    for e in projected:
        adj.setdefault(tuple_key(e["source"]), []).append((tuple_key(e["target"]), e["factId"]))
    from collections import deque
    q = deque([(tuple_key(start), [])])
    seen = {tuple_key(start)}
    path_found = None
    while q:
        cur, path = q.popleft()
        if cur == tuple_key(claimed_target_file):
            path_found = path
            break
        for nxt, fid in adj.get(cur, []):
            if nxt not in seen:
                seen.add(nxt)
                q.append((nxt, path + [fid]))

    # neighbors at symbol/module:src/index.ts both
    neigh_key = tuple_key(endpoint(uni, "symbol", "module:src/index.ts"))
    neighbors_both = []
    for e in projected:
        if tuple_key(e["source"]) == neigh_key or tuple_key(e["target"]) == neigh_key:
            neighbors_both.append(e["factId"])
    # if someone strips to file/src/index.ts
    stripped_file = tuple_key(endpoint(uni, "file", "src/index.ts"))
    neighbors_stripped = []
    for e in projected:
        if tuple_key(e["source"]) == stripped_file or tuple_key(e["target"]) == stripped_file:
            neighbors_stripped.append(e["factId"])
    payload_file_tgt = tuple_key(endpoint(uni, "file", "file:src/index.ts"))
    neighbors_payload_file = [e["factId"] for e in projected if tuple_key(e["source"]) == payload_file_tgt or tuple_key(e["target"]) == payload_file_tgt]

    # scoped structural notes (not whole-run admission)
    ctx_hex = g["plan"]["nativeContextDigests"][0]
    ctx = parse_h_frame(store.rehash(ctx_hex))["value"]
    cid = ctx["toolClosure"]["closureId"]
    crec = parse_h_frame(store.rehash(store.object_table[cid]["digest"]), allowed_domains={"closure"})["value"]
    pkg = ctx["toolchain"].get("compilerPackageDigest")
    pkg_in_tree = pkg in tree_shas(crec)
    eir = {(r["domain"], r["digest"]) for r in g["proof"].get("evaluationInputRefs") or []}
    pred_extras = []
    for pp in g["proof"].get("predicateProofs") or []:
        for r in pp.get("inputRefs") or []:
            if (r["domain"], r["digest"]) not in eir:
                pred_extras.append(r)
    scoped_structural = {
        "compilerPackageDigestInToolchainTree": pkg_in_tree,
        "compilerPackageDigest": pkg,
        "toolchainTree": sorted(tree_shas(crec)),
        "predicateInputRefsSubset": not pred_extras,
        "predicateExtras": pred_extras,
        "note": "Author structural/replay claims are unverified whole-Run closure. These two identity-closure observations are scoped diagnoses from prior established MUSTs. Later query interpretation is diagnostic/not acceptance if either fails.",
    }
    earlier_refusal = None
    if not pkg_in_tree:
        earlier_refusal = "ts.compilerPackageDigest-is-toolchain-tree-member"
    elif pred_extras:
        earlier_refusal = "predicate-inputRefs-subset-of-evaluationInputRefs"

    # coverage imports
    imports_cov = [c for c in g["coverages"] if c["payload"]["key"]["relation"] == "imports"]
    scopes = []
    for sid in g["view"]["scopeIds"]:
        sc = parse_h_frame(store.rehash(store.object_table[sid]["digest"]), allowed_domains={"subject-scope"})["value"]
        scopes.append({"id": sid, "relation": sc.get("relation"), "subjects": sc.get("subjects")})

    obs = {
        "storeSha256": sha(SNAP_STORE),
        "runId": g["run_id"],
        "planId": g["run"]["planId"],
        "viewId": "view2:" + g["view_digest"],
        "universe": uni,
        "snapshotPaths": snap_paths,
        "inventoryRows": inv_rows,
        "fileInventoryNativeIds": file_inv_ids,
        "symbolInventoryNativeIds": symbol_inv_ids,
        "importsFacts": [
            {
                "id": f["id"],
                "importer": f["payload"].get("importer"),
                "resolvedTarget": f["payload"].get("resolvedTarget"),
                "specifier": f["payload"].get("specifier"),
                "hasAttribution": f["id"] in attr_by_fact,
            }
            for f in imports_facts
        ],
        "projectedEdges": projected,
        "unprojectable": unprojectable,
        "vertexDomainKeys": [list(k) for k in vertex_keys],
        "claimedPathExistsUnderTupleLaw": path_found is not None,
        "claimedPathWitness": path_found,
        "neighborsAtSymbolModuleIndex": neighbors_both,
        "neighborsAtStrippedFileSrcIndex": neighbors_stripped,
        "neighborsAtPayloadFileSrcIndex": neighbors_payload_file,
        "importsCoverage": [{"id": c["id"], "coverage": c["payload"]["entry"].get("coverage"), "key": c["payload"]["key"]} for c in imports_cov],
        "scopes": scopes,
        "attributionSelected": [a["digest"] for a in g["attributions"]],
        "evaluationInputRefDomains": sorted({r["domain"] for r in g["proof"].get("evaluationInputRefs") or []}),
        "targetAttributionInEvaluationInputRefs": any(r["domain"] == "target-attribution" for r in g["proof"].get("evaluationInputRefs") or []),
        "targetAttributionInSelectedRefs": any(r["domain"] == "target-attribution" for r in g["ei"]["selectedRefs"]),
        "authorClaim": claim,
        "scopedStructural": scoped_structural,
        "earlierStructuralRefusal": earlier_refusal,
    }
    (probes / "ts-query-graph-observation.json").write_text(json.dumps(obs, indent=2, default=str) + "\n")

    examples = {
        "standing": "kit-derived reasoning examples; not replacement graph admission",
        "gap1_jointly_satisfiable": {
            "inventoryFileNativeId": "src/index.ts",
            "payloadResolvedTarget": "file:src/index.ts",
            "exactEquality": False,
            "parseForbidden": True,
            "lawfulOccupancy": "external (or unknown if no sidecar). first-party would require targetNativeId to equal inventory nativeSubjectId without parsing.",
            "queryVerticesRemainDistinct": {
                "inventory": ["<U>", "file", "src/index.ts", ""],
                "projectedTarget": ["<U>", "file", "file:src/index.ts", ""],
                "projectedSource": ["<U>", "symbol", "module:src/app.ts", ""],
            },
        },
        "gap1_unsatisfiable_if_author_demands_first_party_and_no_parse": {
            "set": [
                "file inventory nativeSubjectId MUST be snapshot LogicalPath",
                "targetNativeId MUST equal payload resolvedTarget SubjectIdV1",
                "never parse SubjectIdV1 spelling to invent occupancy",
                "occupancy=first-party MUST mean targetNativeId is a first-party inventory subject",
            ],
            "result": "Those four cannot hold together for occupancy=first-party on a namespaced file SubjectIdV1. They CAN hold together if occupancy is external/unknown. Not a missing law.",
        },
    }
    (probes / "satisfiability-examples.json").write_text(json.dumps(examples, indent=2) + "\n")

    review = {
        "standing": "Bounded independent architecture/representation review of two alleged TS-author normative tensions and original query input suitability. Same P4 kit-only reviewer origin. Not whole-consumer ACCEPT. Author structural/replay claims unverified as whole-Run closure.",
        "command": f"{PYTHON} -I -B {HERE / 'query_attribution_review.py'}",
        "custody": {
            "inputManifestSha256": sha(MAN),
            "inputManifestMatch": sha(MAN) == EXPECTED_MAN,
            "files": file_ok,
            "kitManifestSha256": sha(KIT_MANIFEST),
            "kitMatch": sha(KIT_MANIFEST) == EXPECTED_KIT,
            "requirementsSha256": sha(REQ),
            "reqMatch": sha(REQ) == EXPECTED_REQ,
            "charterSha256": sha(CHARTER),
            "charterMatch": sha(CHARTER) == EXPECTED_CHARTER,
            "storeSha256": sha(SNAP_STORE),
        },
        "earlierStructuralRefusal": earlier_refusal,
        "queryInterpretationStanding": "diagnostic/not-acceptance" if earlier_refusal else "scoped-observation-not-whole-run-admission",
        "allegedGaps": [
            {
                "id": "G1-SubjectIdV1-vs-file-inventory-nativeSubjectId",
                "authorClaim": "Imports resolvedTarget is file:src/index.ts; file inventory native id is src/index.ts. First-party occupancy cannot match without namespace parsing.",
                "isRealContradiction": False,
                "isMissingLaw": False,
                "classification": "existing-law identity inequality; inconvenient for first-party occupancy on namespaced SubjectIdV1 file targets, not a gap",
                "owners": [
                    "foundation/relation-payload-schemas.v2.json#/$defs/SubjectIdV1",
                    "foundation/subject-inventory.schema.v1.json InventoryRowV1.nativeSubjectId (file=LogicalPath)",
                    "foundation/target-attribution.schema.v1.json occupancy/targetNativeId and x-opensip-join-law.derivation.never",
                    "foundation/atom-evaluation-contract.v1.md §2 Native-id compare is first",
                    "workflows/query-projection-contract.v3.md §2–3 tuple (universe,kind,nativeSubjectId,packageManifestPath)",
                ],
                "required": [
                    "File inventory nativeSubjectId is the snapshot path (equals path).",
                    "imports resolvedTarget is SubjectIdV1 (namespace:opaque).",
                    "targetNativeId equals payload resolvedTarget.",
                    "Never parse SubjectIdV1 spelling to invent kind or occupancy.",
                    "occupancy=first-party iff targetNativeId is a first-party inventory subject of targetUniverse (exact native id).",
                    "Sidecar occupancy=external is consistent when ephemeral is not first-party; occupancy=first-party then refuses TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY.",
                    "Query nativeSubjectId for a projected fact is payload[sourceField]/payload[targetField] as retained; kind is table sourceKind or attribution kind. No invented or stripped namespaces.",
                ],
                "permitted": [
                    "occupancy external|unknown when no exact inventory nativeId match",
                    "external resolved targets that are not first-party inventory remain lawful query vertices via projected-fact endpoints",
                    "logicalPath non-null only when occupancy is external or unknown",
                ],
                "observed": {
                    "fileInventoryNativeIds": file_inv_ids,
                    "projected": projected,
                    "unprojectable": unprojectable,
                },
                "guidance": "Keep occupancy=external (or unknown) for namespaced SubjectIdV1 file targets. Do not parse file: off the payload to force first-party. Do not treat inventory path src/index.ts and payload file:src/index.ts as one query vertex.",
            },
            {
                "id": "G2-TargetAttributionV1-draft-vs-execution-inputs-domain",
                "authorClaim": "Schema is DRAFT pending root ProofInputRef integration, but execution-inputs.schema.v1.json already names domain target-attribution.",
                "isRealContradiction": False,
                "isMissingLaw": False,
                "classification": "stale draft title on the record schema; current identity-schemas.v3 and execution-inputs already incorporate the domain. Draft/historical labels are not blanket authority.",
                "owners": [
                    "foundation/identity-schemas.v3.json#/x-opensip-digest-domains/byDomain/target-attribution (canonical-record, document foundation/target-attribution.schema.v1.json, retention preimage)",
                    "foundation/identity-schemas.v3.json#/$defs/ProofInputRef/properties/domain enum includes target-attribution",
                    "foundation/execution-inputs.schema.v1.json#/$defs/InputRefV1 domain enum includes target-attribution",
                    "foundation/execution-inputs-contract.v1.md §7 host-derived typed input",
                    "foundation/atom-evaluation-contract.v1.md §2 sidecar is provider attestation",
                    "query-projection-contract.v3.md §3 imports without TargetAttributionV1 are unprojectable",
                    "target-attribution.schema.v1.json title DRAFT; x-opensip-identity.proofInputRef.standing NEW pending root; x-opensip-new-internal-faults NEW/internal public-detail",
                ],
                "required": [
                    "When selected, target-attribution blobs are canonical-record preimages under identity-schemas.v3 byDomain.",
                    "Query projection of imports@resolved-target requires a retained TargetAttributionV1 for that sourceFactId.",
                    "Do not treat host.cache/host.targetAttributions as public graph evidence (query §8).",
                ],
                "permitted": [
                    "Schema-file title still says DRAFT; that does not un-register the identity-schemas.v3 domain.",
                    "Some public-detail/D9 routes remain NEW/internal; that does not make the record unusable as a selected blob input.",
                ],
                "observed": {
                    "targetAttributionInSelectedRefs": obs["targetAttributionInSelectedRefs"],
                    "targetAttributionInEvaluationInputRefs": obs["targetAttributionInEvaluationInputRefs"],
                    "attributionDigests": obs["attributionSelected"],
                },
                "guidance": "Treat TargetAttributionV1 as a current selected canonical-record input where identity-schemas.v3 and execution-inputs name it. Do not refuse or waive based on the schema file's DRAFT title. Remaining NEW/internal fault-route standing is not ProofInputRef absence.",
            },
        ],
        "queryTupleObservations": {
            "projectedEdges": projected,
            "unprojectableFacts": unprojectable,
            "claimedTwoFactPathExists": path_found is not None,
            "claimedPathWitness": path_found,
            "whyPathFails": "imports source kind is symbol and nativeSubjectId is payload.importer (e.g. module:src/app.ts). Target kind is attribution.kind=file and nativeSubjectId is payload.resolvedTarget (file:src/index.ts). The second fact source is symbol/module:src/index.ts, which is not the first fact's target file/file:src/index.ts. Tuple law does not identify those endpoints. Author hopCount>=1 over both facts invents a chain by stripping namespaces/kinds.",
            "neighborsSymbolModuleIndex": neighbors_both,
            "neighborsStrippedFilePath": neighbors_stripped,
            "neighborsPayloadFileId": neighbors_payload_file,
            "isolatedInventorySymbols": [r["nativeSubjectId"] for r in inv_rows if r["kind"] == "symbol"],
        },
        "originalQueryInputSuitability": {
            "notExecution": True,
            "charterNeeds": [
                "graph.neighbors / path / reach over admitted retained Run",
                "canonical units/order",
                "historical pagination / latest / cache-loss continuation bound to view.runId",
                "endpoint membership (known vs QUERY.ENDPOINT_UNKNOWN)",
                "evidence limitations vs stored-edge completion",
                "operation bounds vs page boundaries",
                "malformed/mismatched failure envelopes",
                "full six-key human/JSON/agent parity",
            ],
            "supportedIfAdmitted": [
                "Two projectable imports@resolved-target facts exist with TargetAttributionV1 — enough to form neighbor rows at their exact tuples.",
                "One stored imports fact without attribution is correctly unprojectable (limitation, not absence).",
                "Isolated symbol inventory ids (if present as evaluationInputRefs subject-inventory rows) are lawful empty-neighbor vertices.",
                "imports@syntactic-specifier is not a projectable request (QUERY.RELATION_UNSUPPORTED) — not a missing graph.",
                "calls@resolved-callee / three-endpoint counts are peer suggestions, not MUSTs.",
            ],
            "missingForDiscriminatingCharterInputs": [
                "Connected path/reach from module:src/app.ts to left-pad under tuple law: the two projectable facts do not share an endpoint tuple, so they are two stars not one path.",
                "Query cases themselves (neighbors/path/reach responses, cursors, host.latestRunId, host.runsForSnapshot, testBounds, failure envelopes, six-key parity) are not executed — author states queryCasesExecuted=false.",
                "historical pagination / latest / cache-loss need host observations not present in the store.",
                "malformed/mismatched envelopes are request/schema/host, not this store.",
                "Whole-Run close_run of this new store is not established here; compilerPackageDigest tree-membership and predicate-inputRefs subset still fail as scoped identity-closure observations.",
            ],
        },
        "examples": examples,
        "observation": obs,
        "wholeConsumerNotAccepted": True,
        "storesUnchanged": True,
        "queryCasesNotExecuted": True,
    }
    (OUT / "query-attribution-review.json").write_text(json.dumps(review, indent=2, default=str) + "\n")
    (OUT / "query-attribution-review.md").write_text(render_md(review))
    print("EARLIER", earlier_refusal)
    print("PATH", path_found)
    print("NEIGH module:src/index.ts", neighbors_both)
    print("NEIGH stripped file", neighbors_stripped)
    print("NEIGH payload file", neighbors_payload_file)
    print("projected", len(projected), "unproj", len(unprojectable))
    return 0


def render_md(s: dict) -> str:
    lines = []
    lines.append("# Query / attribution independent architecture review")
    lines.append("")
    lines.append("Same P4 kit-only reviewer origin. Bounded to the TS author's two alleged normative tensions and original query **input** suitability. Not query execution, not whole-Run admission, not whole-consumer ACCEPT.")
    lines.append("")
    if s.get("earlierStructuralRefusal"):
        lines.append(f"**Scoped identity-closure observation (not acceptance):** earlier structural MUST `{s['earlierStructuralRefusal']}` is still present on this new store. Query interpretation below is **diagnostic / not acceptance**.")
        lines.append("")
    lines.append("## Custody")
    lines.append("")
    c = s["custody"]
    lines.append(f"- new-inputs manifest `{c['inputManifestSha256']}` match={c['inputManifestMatch']}")
    for f in c["files"]:
        lines.append(f"- `{f['path']}` `{f['sha256']}` match={f['match']}")
    lines.append(f"- kit `{c['kitManifestSha256']}` match={c['kitMatch']}")
    lines.append(f"- charter `{c['charterSha256']}` match={c['charterMatch']}")
    lines.append(f"- this store `{c['storeSha256']}`")
    lines.append("")
    lines.append(f"Command: `{s['command']}`")
    lines.append("")
    lines.append("Author helper scripts, root checkers, and expected values were not read. Author completion MD/JSON/inventory/store are claims and retained bytes under review.")
    lines.append("")
    lines.append("## Constraint map (required vs permitted)")
    lines.append("")
    for g in s["allegedGaps"]:
        lines.append(f"### {g['id']}")
        lines.append("")
        lines.append(f"**Author claim:** {g['authorClaim']}")
        lines.append("")
        lines.append(f"**Real contradiction:** {g['isRealContradiction']}. **Missing law:** {g['isMissingLaw']}.")
        lines.append("")
        lines.append(f"Classification: {g['classification']}")
        lines.append("")
        lines.append("Owners:")
        for o in g["owners"]:
            lines.append(f"- `{o}`")
        lines.append("")
        lines.append("Required:")
        for r in g["required"]:
            lines.append(f"- {r}")
        lines.append("")
        lines.append("Permitted:")
        for r in g["permitted"]:
            lines.append(f"- {r}")
        lines.append("")
        lines.append(f"Guidance: {g['guidance']}")
        lines.append("")
    lines.append("## Current byte observations (TS store)")
    lines.append("")
    q = s["queryTupleObservations"]
    lines.append(f"- Projectable imports@resolved-target facts with TargetAttributionV1: {len(q['projectedEdges'])}")
    for e in q["projectedEdges"]:
        lines.append(f"  - `{e['factId']}` source `{e['source']}` → target `{e['target']}` occupancy={e['attributionOccupancy']} exactNativeIdFirstParty={e['ephemeralFirstPartyByExactNativeId']} externalConsistent={e['externalConsistent']}")
    lines.append(f"- Unprojectable stored imports facts: {q['unprojectableFacts']}")
    lines.append(f"- Author two-fact path exists under tuple law: **{q['claimedTwoFactPathExists']}** witness={q['claimedPathWitness']}")
    lines.append(f"- {q['whyPathFails']}")
    lines.append(f"- Neighbors at (symbol, `module:src/index.ts`): {q['neighborsSymbolModuleIndex']}")
    lines.append(f"- Neighbors at stripped (file, `src/index.ts`) — invented by dropping namespace: {q['neighborsStrippedFilePath']}")
    lines.append(f"- Neighbors at (file, `file:src/index.ts`) payload target form: {q['neighborsPayloadFileId']}")
    lines.append("")
    lines.append("## Original query input suitability (not execution)")
    lines.append("")
    u = s["originalQueryInputSuitability"]
    lines.append("Charter needs: " + "; ".join(u["charterNeeds"]))
    lines.append("")
    lines.append("Supported as retained graph *inputs* if a later close_run admitted this store:")
    for x in u["supportedIfAdmitted"]:
        lines.append(f"- {x}")
    lines.append("")
    lines.append("Missing for the original discriminating reconstruction:")
    for x in u["missingForDiscriminatingCharterInputs"]:
        lines.append(f"- {x}")
    lines.append("")
    lines.append("Peer `calls@resolved-callee` / three-endpoint preferences are not MUSTs.")
    lines.append("")
    lines.append("## Satisfiability examples (reasoning evidence, not Run admission)")
    lines.append("")
    ex = s["examples"]
    lines.append(json.dumps(ex, indent=2))
    lines.append("")
    lines.append("No normative design edit. No graph remint.")
    lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
