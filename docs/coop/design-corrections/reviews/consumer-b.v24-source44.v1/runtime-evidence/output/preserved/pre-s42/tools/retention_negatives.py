"""Independent retention/reference-class negatives (source39.v2 self-audit; composition s7 closure discipline).

The class vocabulary is the kit census (vectors/reference-census.json): typed-prefix identities, the x-opensip-digest representation/retention
pairs of identity-schemas.v3, native-evidence.schemas.v2 and relation-payload-schemas.v2, the x-opensip-digest-domains registry joins
(closureJoins, nestedIdentities, nestedRecords.blobJoins, snapshotJoins, contextAgreementFields), closureMembership and closureKinds.
For each applicable class, one negative is constructed from a corrected claimed-positive export by an exact byte mutation followed by an
independent remint of every enclosing identity: every canonical record or frame that names a changed digest is rewritten, re-ordered under
its own x-opensip-order and re-hashed until fixpoint, so no stale hash remains. Builder-owned input mutations are used only where the class
lives inside native owner inputs, and they are labelled as such.

Each negative is closed twice:
  post - ref/closure.close_run of this runtime (owner graph admission, independent retained closure, replay, reachable-set equality);
  pre  - preserved/pre-s41/tools/replay_run.py in a fresh process (HC-44: the unchanged ported helpers exactly as they ran against the
         source41 kit; the source39.v1 pre-hc33 copy is not part of this runtime), to show what the original helpers did.
Recorded: construction, pipeline first refusal and its stage, masked stages, owner-admission faults, the retained-closure first refusal
(obligation, code, path) and its masked later faults, and whether replay ran. No expected refusal CODE is asserted. The pass criterion is
structural: a refusal negative must REFUSE with replay not performed and must be refused by the independent retained closure; the
unreachable-output control must ADMIT with the extra frame listed unreachable; the unrecomputed-reachable control must REFUSE in replay.
Usage: python3 tools/seq.py v2-negatives tools/retention_negatives.py
"""
import base64
import copy
import hashlib
import json
import os
import re
import subprocess
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1/output/preserved/pre-s42"
REF = ["/tmp/opensip-architecture-review-env/bin/python", "-I", "-B"]
sys.path.insert(0, OUT + "/ref")

import canonical as K  # noqa: E402
import closure as CL  # noqa: E402
import retained_graph as RG  # noqa: E402
import schemas  # noqa: E402
from store import Store  # noqa: E402

KIT = schemas.kit()
ID = RG.ID
NEG_DIR = OUT + "/negatives"
PREFIXES = set(RG.PREFIX_DOMAIN) | {"sha256"}


def record_candidates():
    """Every registered canonical-record selector of the current graph, taken from the kit census and registries (never from builders)."""
    cands = []
    census = json.load(open(OUT + "/vectors/reference-census.json"))
    for a in census["digestAnnotations"]:
        t = a.get("target")
        if a["representation"] != "canonical-record" or "identity-schemas.v2" in a["document"] or not isinstance(t, dict):
            continue
        if "bundle" in t:
            cands.append((ID, t["selector"]))
        elif "document" in t and "selector" in t:
            cands.append((t["document"], t["selector"]))
    for row in RG.BYDOMAIN.values():
        rec = row.get("record") or {}
        if "bundle" in rec:
            cands.append((ID, rec["selector"]))
        elif "document" in rec:
            cands.append((rec["document"], rec["selector"]))
    for cls in ("coverage", "import", "parameter"):
        for row in RG.PAYREG[cls]["rows"].values():
            cands.append((row["document"], row["selector"]))
    for row in RG.RELREG.values():
        cands.append((RG.REL, row["selector"]))
    for rows in RG.SETS.values():
        for row in rows.values():
            for nr in row.get("nestedRecords", []):
                cands.append((nr["document"], nr["selector"]))
    out, seen = [], set()
    for c in cands:
        key = (schemas.norm_rel(c[0]), c[1])
        if key not in seen:
            seen.add(key)
            out.append(c)
    return out


RECORD_SELECTORS = record_candidates()
SELECTOR_CACHE = {}


def original_selector(hx, value):
    """The registered selector under which the ORIGINAL retained record admits (so re-ordering follows that record's own law)."""
    if hx not in SELECTOR_CACHE:
        SELECTOR_CACHE[hx] = next(((d, s) for d, s in RECORD_SELECTORS if not KIT.stock_errors(value, d, s) and KIT.admit(value, d, s)["ok"]), None)
    return SELECTOR_CACHE[hx]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def sfx(i):
    return i.split(":", 1)[1] if ":" in i else i


class Graph:
    def __init__(self, base):
        self.base = base
        ex = json.load(open(f"{OUT}/runs/{base}.store.json"))
        self.blobs = {h: base64.b64decode(b) for h, b in ex["blobs"].items()}
        self.labels = ex.get("blobLabels", {})
        self.run_hex = sfx(ex["runId"])

    def frame(self, ident):
        dom, v, err = RG.parse_frame(self.blobs[sfx(ident)])
        assert err is None, err
        return dom, v

    def value(self, ident):
        return self.frame(ident)[1]

    def record(self, hx):
        return K.parse_raw(self.blobs[hx])

    def put_frame(self, dom, v):
        b = K.frame(dom, v)
        self.blobs[sha(b)] = b
        return sha(b)

    def put_record(self, v):
        b = K.C(v)
        self.blobs[sha(b)] = b
        return sha(b)

    # -------------------------------------------------------------- core graph
    def run(self):
        return self.value(self.run_hex)

    def plan(self):
        return self.value(self.run()["planId"])

    def seal(self):
        return self.value(self.run()["evaluationSealId"])

    def proof(self):
        return self.value(self.seal()["proofBundleId"])

    def findings(self):
        return [(f, self.value(f)) for f in self.proof()["findingIds"]]

    # -------------------------------------------------------------- independent remint
    def remint(self, mapping):
        m = dict(mapping)
        changed = True
        while changed:
            changed = False
            for h in sorted(self.blobs):
                b = self.blobs.get(h)
                if b is None or not any(k.encode() in b for k in m):
                    continue
                dom, v, err = RG.parse_frame(b)
                if err is None:
                    nv = subst(v, m)
                    sel = selector_for_domain(dom)
                    if sel:
                        nv = resort(nv, *sel)
                    nb = K.frame(dom, nv)
                else:
                    try:
                        v = K.parse_raw(b)
                        if K.C(v) != b:
                            continue
                    except (K.AdmissionError, ValueError):
                        continue
                    sel = original_selector(h, v)
                    nv = subst(v, m)
                    if sel:
                        nv = resort(nv, *sel)
                    nb = K.C(nv)
                nh = sha(nb)
                if nh == h:
                    continue
                self.blobs[nh] = nb
                del self.blobs[h]
                m[h] = nh
                changed = True
        while self.run_hex in m:
            self.run_hex = m[self.run_hex]
        return m

    def export(self):
        table = []
        for h, b in sorted(self.blobs.items()):
            dom, v, err = RG.parse_frame(b)
            if err is None and dom in RG.DOMAIN_PREFIX:
                table.append({"id": f"{RG.DOMAIN_PREFIX[dom]}:{h}", "domain": dom, "frameSha256": h, "frameBytes": len(b)})
        return {"format": "consumer-b.v24.store.v1", "objectTable": table,
                "blobs": {h: base64.b64encode(b).decode("ascii") for h, b in sorted(self.blobs.items())},
                "blobLabels": {h: lab for h, lab in sorted(self.labels.items()) if h in self.blobs},
                "runId": f"run3:{self.run_hex}", "variant": None}


def subst(v, m):
    if isinstance(v, str):
        if v in m:
            return m[v]
        if ":" in v:
            p, s = v.split(":", 1)
            if p in PREFIXES and s in m:
                return f"{p}:{m[s]}"
        return v
    if isinstance(v, list):
        return [subst(x, m) for x in v]
    if isinstance(v, dict):
        return {k: subst(x, m) for k, x in v.items()}
    return v


def selector_for_domain(dom):
    if dom in RG.DOMAIN_PREFIX:
        return ID, f"#/$defs/{dom}"
    row = RG.SET_ROWS.get(dom)
    if row and "selector" in row[1]:
        return row[1].get("document", RG.NE), row[1]["selector"]
    return None


def get_at(value, path):
    cur = value
    for name, idx in re.findall(r"\.([^.\[]+)|\[(\d+)\]", path[1:]):
        cur = cur[name] if name else cur[int(idx)]
    return cur


def resort(value, doc, sel):
    value = copy.deepcopy(value)
    for _ in range(8):
        try:
            viol = KIT.order_violations(value, doc, sel)
        except Exception:
            return value
        if not viol:
            return value
        for vi in viol:
            try:
                arr = get_at(value, vi["path"])
            except (KeyError, IndexError, TypeError):
                continue
            if not isinstance(arr, list):
                continue
            ann = vi["order"]
            if ann in ("canonical-set", "canonical-order"):
                arr.sort(key=K.C)
            elif ann == "path":
                arr.sort(key=lambda x: x["path"].encode())
            elif ann in ("ruleId", "waiverId"):
                arr.sort(key=lambda x, a=ann: x[a].encode())
            elif ann == "predicate":
                arr.sort(key=lambda x: (x["ruleId"].encode(), x["subjectId"].encode(), x["predicateId"].encode()))
            elif ann == "utf8":
                arr.sort(key=lambda s: s.encode())
            elif ann == "numeric":
                arr.sort()
            elif isinstance(ann, dict):
                arr.sort(key=lambda x, a=ann: tuple(x[k].encode() if isinstance(x[k], str) else x[k] for k in a["by"]))
    return value


# ---------------------------------------------------------------------------------------------------------------- constructions
def subjects_only_in_proofs(g):
    finding_subjects = {v["subjectId"] for _, v in g.findings()}
    proof = g.proof()
    return [p["subjectId"] for p in proof["predicateProofs"] if p["subjectId"] not in finding_subjects] or [p["subjectId"] for p in proof["predicateProofs"]]


def native_context(g, domain):
    for hx in g.plan()["nativeContextDigests"]:
        dom, v = g.frame(hx)
        if dom == domain:
            return hx, v
    raise ValueError(f"no {domain} context")


def universe_of(g, domain):
    for hx, b in g.blobs.items():
        dom, v, err = RG.parse_frame(b)
        if err is None and dom == domain:
            return hx, v
    raise ValueError(f"no {domain} universe")


def c_subject_missing(g):
    sid = subjects_only_in_proofs(g)[0]
    del g.blobs[sfx(sid)]
    return {"mutated": sid, "detail": "subject3 descriptor referenced only by predicateProofs/enumeration removed from custody"}


def c_finding_missing(g):
    fid = g.proof()["findingIds"][0]
    del g.blobs[sfx(fid)]
    return {"mutated": fid, "detail": "finding3 frame referenced by proof/evidence/ruleResults removed"}


def c_fingerprint_missing(g):
    fp = next(v["fingerprint"] for _, v in g.findings() if v["fingerprint"])
    del g.blobs[sfx(fp)]
    return {"mutated": fp, "detail": "finding-key2 descriptor of a matched finding removed"}


def c_prefix_domain_mismatch(g):
    fid = g.proof()["findingIds"][0]
    sid = subjects_only_in_proofs(g)[0]
    g.remint({sfx(fid): sfx(sid)})
    return {"mutated": fid, "detail": f"every finding3 reference to {fid[:22]}... now carries the hex of an evaluation-subject frame; enclosing identities reminted"}


def c_prefix_record_refused(g):
    fid, f = g.findings()[0]
    nh = g.put_frame("finding", dict(f, unexpectedField=1))
    g.remint({sfx(fid): nh})
    return {"mutated": fid, "detail": "finding3 re-framed with a property its $defs/finding forbids (additionalProperties false); references reminted"}


def c_record_where_frame(g):
    sid = subjects_only_in_proofs(g)[0]
    nh = g.put_record(g.value(sid))
    g.remint({sfx(sid): nh})
    return {"mutated": sid, "detail": "subject3 references re-pointed at raw SHA-256(C(descriptor)) - a canonical record where an H frame is required"}


def c_historical_prefix(g):
    seal = g.seal()
    proof = g.proof()
    p2 = dict(proof, findingIds=sorted(["finding2:" + sfx(proof["findingIds"][0])] + proof["findingIds"][1:], key=K.C))
    nh = g.put_frame("proof-bundle", p2)
    g.remint({sfx(seal["proofBundleId"]): nh})
    return {"mutated": proof["findingIds"][0], "detail": "proof.findingIds[0] spelled with the historical finding2 prefix; proof/evidence/seal/run reminted"}


def c_universe_domain_set(g):
    sid = subjects_only_in_proofs(g)[0]
    desc = g.value(sid)
    ctx_hex = g.plan()["nativeContextDigests"][0]
    nh = g.put_frame("evaluation-subject", dict(desc, universe=ctx_hex))
    g.remint({sfx(sid): nh})
    return {"mutated": sid, "detail": "evaluation-subject.universe names a native-context frame (outside the native-semantic-universe domain set); reminted"}


def c_nested_identity_missing(g):
    _, ctx = native_context(g, "native.context.rust.v2")
    hx = sfx(ctx["dependencySourceSetId"])
    del g.blobs[hx]
    return {"mutated": ctx["dependencySourceSetId"], "detail": "rust context dependencySourceSetId frame (native-nested, preimage-frame) removed"}


def c_scope_missing(g):
    ev = g.value(g.run()["evidenceId"])
    view = g.value(ev["viewIds"][0])
    sid = view["scopeIds"][0]
    del g.blobs[sfx(sid)]
    return {"mutated": sid, "detail": "scope2 frame named by view.scopeIds removed (typed-prefix input reference)"}


def c_parameters_missing(g):
    _, f = g.findings()[0]
    del g.blobs[f["parameterDigest"]]
    return {"mutated": f["parameterDigest"], "detail": "finding.parameterDigest canonical-record preimage removed"}


def c_witness_not_canonical(g):
    pp = g.proof()["predicateProofs"][0]
    w = g.record(pp["witnessDigest"])
    b = json.dumps(w, sort_keys=True, separators=(", ", ": ")).encode()
    g.blobs[sha(b)] = b
    g.remint({pp["witnessDigest"]: sha(b)})
    return {"mutated": pp["witnessDigest"], "detail": "predicate-witness retained as non-canonical JSON (spaced separators) under its own new digest; references reminted"}


def c_witness_refused(g):
    pp = g.proof()["predicateProofs"][0]
    w = g.record(pp["witnessDigest"])
    nh = g.put_record(dict(w, unexpectedField=1))
    g.remint({pp["witnessDigest"]: nh})
    return {"mutated": pp["witnessDigest"], "detail": "predicate-witness canonical but outside its selector (extra property); references reminted"}


def c_payload_schema_join(g):
    ev = g.value(g.run()["evidenceId"])
    view = g.value(ev["viewIds"][0])
    fid = view["facts"][0]
    fact = g.value(fid)
    nh = g.put_frame("fact", dict(fact, payloadSchemaDigest=KIT.digest(RG.NE)))
    g.remint({sfx(fid): nh})
    return {"mutated": fid, "detail": "fact.payloadSchemaDigest names the native bundle, not the relation payload document of its payload class; reminted"}


def c_fragment_mismatch(g):
    proof = g.proof()
    for pp in proof["predicateProofs"]:
        w = g.record(pp["witnessDigest"])
        ppd = g.record(w["programPredicateDigest"])
        nh = g.put_record(dict(ppd, nodeDigest=sha(b"cb24.not-the-addressed-predicate-node")))
        g.remint({w["programPredicateDigest"]: nh})
        return {"mutated": w["programPredicateDigest"], "detail": "program-predicate.nodeDigest (fragment of RuleProgramV2) no longer the addressed node; witness/proof reminted"}


def c_tree_member_missing(g):
    _, f = g.findings()[0]
    clo = g.value(f["ruleClosure"])
    row = clo["tree"][0]
    del g.blobs[row["sha256"]]
    return {"mutated": row["sha256"], "detail": f"detector closure tree member {row['path']} bytes removed (raw-artifact preimage)"}


def c_blob_length(g):
    _, f = g.findings()[0]
    cid = f["ruleClosure"]
    clo = g.value(cid)
    tree = [dict(r, bytes=r["bytes"] + 1) if i == 0 else r for i, r in enumerate(clo["tree"])]
    nh = g.put_frame("closure", dict(clo, tree=tree))
    g.remint({sfx(cid): nh})
    return {"mutated": cid, "detail": "detector closure tree[0].bytes declares one more byte than the retained artifact; closure and Plan reminted"}


def c_schema_document_unregistered(g):
    ev = g.value(g.run()["evidenceId"])
    vid = ev["viewIds"][0]
    view = g.value(vid)
    doc = KIT.raw[schemas.norm_rel(ID)]
    g.blobs[sha(doc)] = doc
    nh = g.put_frame("view", dict(view, schemaDigests=sorted(set(view["schemaDigests"]) | {sha(doc)}, key=K.C)))
    g.remint({sfx(vid): nh})
    return {"mutated": vid, "detail": "view.schemaDigests adds the (retained) identity-schemas document, which is not on the payload registry list; reminted"}


def c_tree_member_absent(g):
    hx, ctx = native_context(g, "native.context.rust.v2")
    nh = g.put_frame("native.context.rust.v2", dict(ctx, toolClosure=dict(ctx["toolClosure"], rustc=sha(b"cb24.rustc-not-in-tree"))))
    g.remint({hx: nh})
    return {"mutated": hx, "detail": "ToolClosureV1.rustc names a digest outside the toolClosure tree (closure-tree-member); context, universes and Plan reminted"}


def c_capability_manifest_derived(g):
    run = g.run()
    g.run_hex = g.put_frame("run", dict(run, capabilityManifestId=sha(b"cb24.not-the-committed-manifest")))
    return {"mutated": "run.capabilityManifestId", "detail": "run.capabilityManifestId not the CVE1 recipe over plan.capabilityManifestBytesDigest; run reminted"}


def c_by_domain(g):
    for fid, f in g.findings():
        cov = next((r for r in f["evidenceRefs"] if r["domain"] == "coverage"), None)
        if cov is not None:
            refs = sorted([r for r in f["evidenceRefs"] if r != cov] + [{"domain": "fact", "digest": cov["digest"]}], key=K.C)
            nh = g.put_frame("finding", dict(f, evidenceRefs=refs))
            g.remint({sfx(fid): nh})
            return {"mutated": fid, "detail": "FindingEvidenceRef {domain: fact} carries a coverage2 digest (by-domain resolves to the fact frame domain); reminted"}
    raise ValueError("no finding with a coverage citation")


def c_snapshot_path(g):
    ev = g.value(g.run()["evidenceId"])
    view = g.value(ev["viewIds"][0])
    for fid in view["facts"]:
        fact = g.value(fid)
        if fact["relation"] == "file":
            payload = g.record(fact["payloadDigest"])
            np = g.put_record(dict(payload, path="cb24/not-in-snapshot.txt"))
            nh = g.put_frame("fact", dict(fact, payloadDigest=np))
            g.remint({sfx(fid): nh})
            return {"mutated": fid, "detail": "file fact payload path not an inventoried snapshot path (snapshot-path/snapshot-inventoried); reminted"}
    raise ValueError("no file fact")


def c_body_frame_missing(g):
    for hx, b in list(g.blobs.items()):
        dom, fact, err = RG.parse_frame(b)
        if err is None and dom == "fact" and fact["relation"] == "clones":
            payload = g.record(fact["payloadDigest"])
            del g.blobs[sfx(payload["bodyIdentity"])]
            return {"mutated": payload["bodyIdentity"], "detail": "clones bodyIdentity framed preimage removed (framed-body-identity/provider-output-retained)"}
    raise ValueError("no clones fact")


def c_layout_blob(g):
    _, ctx = native_context(g, "native.context.typescript.v2")
    layout = g.record(ctx["nodeModulesLayoutDigest"])
    snapshot = g.value(g.plan()["snapshotId"])
    inventoried = {r["sha256"] for r in snapshot["sourceInventory"]}
    free = [e for e in layout["entries"] if e["contentSha256"] not in inventoried]
    entry = (free or layout["entries"])[0]
    del g.blobs[entry["contentSha256"]]
    shared = "" if free else " (every layout entry is also a snapshot source row: source retention masks the join)"
    return {"mutated": entry["contentSha256"], "detail": f"ResolvedNodeModulesLayoutV1 entry {entry.get('path', '?')} bytes removed (nestedRecords.blobJoins){shared}"}


def c_lockfile_digest(g):
    hx, ctx = native_context(g, "native.context.typescript.v2")
    lock = dict(ctx["lockfileIdentity"], contentSha256=sha(b"cb24.other-lockfile"))
    nh = g.put_frame("native.context.typescript.v2", dict(ctx, lockfileIdentity=lock))
    g.remint({hx: nh})
    return {"mutated": hx, "detail": "lockfileIdentity.contentSha256 differs from the inventoried package-lock row (snapshotJoins inventoried-path-and-digest); reminted"}


def c_closure_join_kind(g):
    hx, ctx = native_context(g, "native.context.typescript.v2")
    stdlib = "closure2:" + ctx["toolchain"]["typescriptStdlibMerkleRoot"]
    nh = g.put_frame("native.context.typescript.v2", dict(ctx, toolClosure=dict(ctx["toolClosure"], closureId=stdlib)))
    g.remint({hx: nh})
    return {"mutated": hx, "detail": "toolClosure.closureId names the retained stdlib closure (closureJoins closure2-identity kind toolchain); reminted"}


def c_context_agreement(g):
    uhex, uni = universe_of(g, "native.semantic-universe.rust.v2")
    _, ctx = native_context(g, "native.context.rust.v2")
    dom, feats = g.frame(ctx["unifiedFeaturesId"])
    changed = None
    if isinstance(feats.get("computedBy"), dict) and isinstance(feats["computedBy"].get("producerBuildId"), str):
        changed = dict(feats, computedBy=dict(feats["computedBy"], producerBuildId=feats["computedBy"]["producerBuildId"] + "-other"))
    if changed is None or not KIT.admit(changed, *selector_for_domain(dom))["ok"]:
        raise ValueError("no admissible UnifiedFeaturesV1 variant constructible")
    nf = g.put_frame(dom, changed)
    nu = g.put_frame("native.semantic-universe.rust.v2", dict(uni, unifiedFeaturesId="sha256:" + nf))
    g.remint({uhex: nu})
    return {"mutated": uhex, "detail": "rust universe unifiedFeaturesId names a different admitted features frame than its context (contextAgreementFields); reminted"}


def c_membership_direct(g):
    fid, f = g.findings()[0]
    clo = g.value(f["ruleClosure"])
    nc = g.put_frame("closure", dict(clo, semanticVersion=clo["semanticVersion"] + "-unselected"))
    nh = g.put_frame("finding", dict(f, ruleClosure="closure2:" + nc))
    g.remint({sfx(fid): nh})
    return {"mutated": fid, "detail": "finding.ruleClosure names a retained detector closure not in plan.semanticClosures (closureMembership.direct); reminted"}


def c_closure_kind(g):
    fid, f = g.findings()[0]
    nh = g.put_frame("finding", dict(f, ruleClosure=g.seal()["evaluatorClosure"]))
    g.remint({sfx(fid): nh})
    return {"mutated": fid, "detail": "finding.ruleClosure names the selected evaluator closure (closureKinds finding.ruleClosure = detector); reminted"}


def c_equal_to_direct(g):
    ev = g.value(g.run()["evidenceId"])
    view = g.value(ev["viewIds"][0])
    fid = view["facts"][0]
    fact = g.value(fid)
    clo = g.value(fact["producerClosure"])
    nc = g.put_frame("closure", dict(clo, semanticVersion=clo["semanticVersion"] + "-other"))
    nh = g.put_frame("fact", dict(fact, producerClosure="closure2:" + nc))
    g.remint({sfx(fid): nh})
    return {"mutated": fid, "detail": "fact.producerClosure differs from its view.producerClosure (closureMembership.equalToDirect); reminted"}


def c_unreachable_output(g):
    fid, f = g.findings()[0]
    extra = g.put_frame("finding", dict(f, severity="error" if f["severity"] != "error" else "warning"))
    return {"mutated": f"finding3:{extra}", "detail": "an extra finding3 frame retained but referenced by nothing reachable from run3"}


def c_unrecomputed_reachable(g):
    seal = g.seal()
    proof = g.proof()
    fid, f = g.findings()[0]
    extra = "finding3:" + g.put_frame("finding", dict(f, severity="error" if f["severity"] != "error" else "warning"))
    rr = [dict(r, findingIds=sorted(r["findingIds"] + [extra], key=K.C)) if r["ruleId"] == f["ruleId"] else r for r in proof["ruleResults"]]
    p2 = dict(proof, findingIds=sorted(proof["findingIds"] + [extra], key=K.C), ruleResults=rr)
    nh = g.put_frame("proof-bundle", p2)
    ev = g.value(seal["evidenceId"])
    ne = g.put_frame("semantic-evidence", dict(ev, findingIds=p2["findingIds"], proofBundleId="proof3:" + nh))
    ns = g.put_frame("evaluation-seal", dict(seal, proofBundleId="proof3:" + nh, evidenceId="evidence3:" + ne))
    g.run_hex = g.put_frame("run", dict(g.run(), evidenceId="evidence3:" + ne, evaluationSealId="seal3:" + ns))
    return {"mutated": extra, "detail": "a retained, schema-valid finding3 the evaluator does not produce is added to proof/ruleResults/evidence findingIds; all enclosing identities reminted"}


NEGATIVES = [
    # (id, class from the census vocabulary, base, construction, kind)
    ("typed-prefix-output-subject-missing", "typed-prefix identity (subject3) / retention", "ts-pass", c_subject_missing, "refuse"),
    ("typed-prefix-output-finding-missing", "typed-prefix identity (finding3) / retention", "ts-pass", c_finding_missing, "refuse"),
    ("typed-prefix-output-fingerprint-missing", "typed-prefix identity (finding-key2) / retention", "ts-pass", c_fingerprint_missing, "refuse"),
    ("typed-prefix-domain-mismatch", "typed-prefix identity / prefix-selected domain", "ts-pass", c_prefix_domain_mismatch, "refuse"),
    ("typed-prefix-record-refused", "typed-prefix identity / descriptor schema admission", "ts-pass", c_prefix_record_refused, "refuse"),
    ("typed-prefix-raw-record-not-frame", "typed-prefix identity / frame grammar (lexical)", "ts-pass", c_record_where_frame, "refuse"),
    ("typed-prefix-historical-major", "typed-prefix identity / current identity table (mixed output major)", "ts-pass", c_historical_prefix, "refuse"),
    ("typed-prefix-input-scope-missing", "typed-prefix identity (scope2 input) / retention", "ts-pass", c_scope_missing, "refuse"),
    ("h-identity-domain-set", "h-identity/preimage (domainSet native-semantic-universe)", "ts-pass", c_universe_domain_set, "refuse"),
    ("h-identity-preimage-frame-nested", "h-identity/preimage-frame (native) + registry nestedIdentities", "rust-mixed", c_nested_identity_missing, "refuse"),
    ("canonical-record-preimage-missing", "canonical-record/preimage (finding-parameters)", "ts-pass", c_parameters_missing, "refuse"),
    ("canonical-record-not-canonical", "canonical-record/preimage (lexical exact C)", "ts-pass", c_witness_not_canonical, "refuse"),
    ("canonical-record-selector-refused", "canonical-record/preimage (selector admission)", "ts-pass", c_witness_refused, "refuse"),
    ("canonical-record-payload-class-join", "canonical-record/preimage (payloadClass relation schemaDigestField join)", "ts-pass", c_payload_schema_join, "refuse"),
    ("canonical-record-fragment", "canonical-record/fragment (program-predicate.nodeDigest)", "ts-pass", c_fragment_mismatch, "refuse"),
    ("raw-artifact-preimage-missing", "raw-artifact/preimage (closure tree member bytes)", "ts-pass", c_tree_member_missing, "refuse"),
    ("raw-artifact-length", "raw-artifact/preimage (Blob.bytes exact length)", "ts-pass", c_blob_length, "refuse"),
    ("raw-artifact-registered-schema-document", "raw-artifact/preimage (artifactClass registered-schema-document)", "ts-pass", c_schema_document_unregistered, "refuse"),
    ("raw-artifact-closure-tree-member", "raw-artifact/closure-tree-member (native)", "rust-mixed", c_tree_member_absent, "refuse"),
    ("capability-manifest-id-derived", "capability-manifest-id/derived", "ts-pass", c_capability_manifest_derived, "refuse"),
    ("by-domain", "by-domain (FindingEvidenceRef)", "ts-pass", c_by_domain, "refuse"),
    ("snapshot-path-inventoried", "snapshot-path/snapshot-inventoried (relation)", "syntax-code", c_snapshot_path, "refuse"),
    ("framed-body-identity-retained", "framed-body-identity/provider-output-retained (relation)", "syntax-code", c_body_frame_missing, "refuse"),
    ("registry-nested-record-blob-join", "registry nestedRecords.blobJoins", "ts-pass", c_layout_blob, "refuse"),
    ("registry-snapshot-join-path-and-digest", "registry snapshotJoins inventoried-path-and-digest", "ts-pass", c_lockfile_digest, "refuse"),
    ("registry-closure-join-kind", "registry closureJoins closure2-identity kind", "ts-pass", c_closure_join_kind, "refuse"),
    ("registry-context-agreement", "registry contextAgreementFields", "rust-mixed", c_context_agreement, "refuse"),
    ("closure-membership-direct", "closureMembership.direct (finding.ruleClosure)", "ts-pass", c_membership_direct, "refuse"),
    ("closure-kinds", "closureKinds.byField (finding.ruleClosure detector)", "ts-pass", c_closure_kind, "refuse"),
    ("closure-membership-equal-to-direct", "closureMembership.equalToDirect (fact.producerClosure)", "ts-pass", c_equal_to_direct, "refuse"),
    ("reachable-set-unreachable-output", "exact reachable output set: extra unreferenced semantic output (control)", "ts-pass", c_unreachable_output, "admit-unreachable"),
    ("reachable-set-unrecomputed-output", "exact reachable output set: reachable output not recomputed", "ts-pass", c_unrecomputed_reachable, "refuse-in-replay"),
]
BUILDER_MUTATIONS = [
    ("closureMembership.selectedThroughOtherInput (UNSELECTED_EVALUATION_IMPORT)", "ts-pass~hidden-import"),
    ("h-identity/derived (SourceUnitOwnershipV1 unitId, owner binding)", "rust-mixed~unit-id-not-derived"),
    ("registry snapshotJoins inventoried-paths (configGraphPaths)", "ts-pass~config-graph-path-outside-snapshot"),
    ("registry blobJoins (cargo config projection)", "rust-mixed~config-projection-mismatch"),
]


def summarize(rep):
    rc = rep.get("retainedClosure", {})
    return {"result": rep["result"], "firstRefusal": rep.get("firstRefusal"), "maskedStages": rep.get("maskedStages"),
            "ownerGraphAdmissionFaults": rep["graphAdmission"].get("faults", [])[:5],
            "retainedClosure": {"result": rc.get("result"), "firstRefusal": rc.get("firstRefusal"),
                                "maskedLaterFaults": (rc.get("faults") or [])[1:6], "faultCount": len(rc.get("faults") or []),
                                "unreachableSemanticOutputs": (rc.get("unreachableRetained") or {}).get("semanticOutputs")},
            "semanticReplayPerformed": rep["semanticReplay"].get("performed", False),
            "replayFaults": (rep["semanticReplay"].get("faults") or [])[:5],
            "reachableOutputSet": rep["semanticReplay"].get("reachableOutputSet")}


def masking(rep):
    """R-NEGATIVE-FIRST-REFUSAL observable: the first refusal of the stage-ordered pipeline and what it masks (later stage-ordered faults and
    stages that never ran)."""
    ordered = rep.get("faultsInStageOrder") or []
    return {"firstRefusal": rep.get("firstRefusal"),
            "masksLater": ordered[1:11] + [f"masked-stage:{s}" for s in (rep.get("maskedStages") or [])]}


def pre_close(store_path, name):
    dst = f"{NEG_DIR}/{name}.pre-s41.replay.json"
    p = subprocess.run(REF + [f"{OUT}/preserved/pre-s41/tools/replay_run.py", store_path, dst], capture_output=True, text=True)
    if not os.path.exists(dst):
        return {"exit": p.returncode, "stderr": p.stderr[-400:]}
    rep = json.load(open(dst))
    faults = rep["graphAdmission"]["faults"] + (rep["semanticReplay"].get("faults") or [])
    return {"result": rep["result"], "firstFault": faults[0] if faults else None,
            "stage": "graph-admission" if rep["graphAdmission"]["faults"] else ("semantic-replay" if rep["semanticReplay"].get("faults") else None),
            "replayPerformed": rep["semanticReplay"].get("performed", False), "artifact": os.path.relpath(dst, OUT)}


def main():
    os.makedirs(NEG_DIR, exist_ok=True)
    rows = []
    for nid, cls, base, fn, kind in NEGATIVES:
        g = Graph(base)
        row = {"id": nid, "class": cls, "base": base, "baseStoreSha256": sha(open(f"{OUT}/runs/{base}.store.json", "rb").read()), "expectKind": kind}
        try:
            row["construction"] = fn(g)
        except Exception as exc:  # a negative that cannot be constructed is reported, never silently skipped
            row.update(constructed=False, error=f"{type(exc).__name__}: {exc}", firstRefusal=None, masksLater=[], classification="invalid", **{"pass": False})
            rows.append(row)
            print(nid, "NOT CONSTRUCTED", row["error"])
            continue
        ex = g.export()
        ex["variant"] = f"negative:{nid}"
        path = f"{NEG_DIR}/{nid}.store.json"
        with open(path, "w") as fh:
            json.dump(ex, fh, sort_keys=True)
        row.update(constructed=True, store=os.path.relpath(path, OUT), storeSha256=sha(open(path, "rb").read()), runId=ex["runId"])
        rep = CL.close_run(Store.load(ex), ex["runId"])
        json.dump(rep, open(f"{NEG_DIR}/{nid}.replay.json", "w"), indent=1, sort_keys=True)
        post = summarize(rep)
        row["post"] = post
        row["pre"] = pre_close(path, nid)
        if kind == "refuse":
            ok = post["result"] == "REFUSE" and not post["semanticReplayPerformed"] and post["retainedClosure"]["result"] == "REFUSE"
        elif kind == "admit-unreachable":
            ok = post["result"] == "ADMIT" and row["construction"]["mutated"] in (post["retainedClosure"]["unreachableSemanticOutputs"] or [])
        else:
            ok = post["result"] == "REFUSE" and post["semanticReplayPerformed"] and post["retainedClosure"]["result"] == "ADMIT"
            row["reachableSetInequalityReported"] = any("REACHABLE_OUTPUT_NOT_RECOMPUTED" in f for f in rep["semanticReplay"].get("faults", []))
        row["pass"] = ok
        row.update(masking(rep))
        row["classification"] = "valid" if kind == "admit-unreachable" else "invalid"
        rows.append(row)
        print(nid, "post", post["result"], (post["firstRefusal"] or {}).get("stage"), str((post["firstRefusal"] or {}).get("fault"))[:110],
              "| pre", row["pre"].get("result"), str(row["pre"].get("firstFault"))[:60], "| pass", ok)
    builder_rows = []
    for cls, run in BUILDER_MUTATIONS:
        rp = f"{OUT}/runs/{run}.replay.json"
        if not os.path.exists(rp):
            builder_rows.append({"class": cls, "run": run, "available": False})
            continue
        rep = json.load(open(rp))
        builder_rows.append({"class": cls, "run": run, "available": True, "source": "builder input mutation (builders/*.py MUTATIONS), closed by tools/replay_all.py",
                             "post": summarize(rep), "classification": "invalid", **masking(rep),
                             "pass": rep["result"] == "REFUSE" and not rep["semanticReplay"].get("performed", False)})
    census = json.load(open(OUT + "/vectors/reference-census.json"))
    walked = {}
    for run in ("ts-pass", "rust-mixed", "syntax-code"):
        fsr = json.load(open(f"{OUT}/runs/{run}.replay.fromscratch.json"))
        for k, v in fsr["retainedClosure"]["referenceClassesWalked"].items():
            walked[k] = walked.get(k, 0) + v
    walked_pairs = {("by-domain/preimage" if k.startswith("by-domain:") else k) for k in walked}
    not_reached = [f"{p['representation']}/{p['retention']}" for p in census["representationRetentionPairs"]
                   if f"{p['representation']}/{p['retention']}" not in walked_pairs]
    doc = {"standing": __doc__.strip().splitlines()[0], "negatives": rows, "builderMutationRows": builder_rows,
           "allPass": all(r.get("pass") for r in rows) and all(r.get("pass") for r in builder_rows if r.get("available")),
           "constructed": sum(1 for r in rows if r.get("constructed")), "notConstructed": [r["id"] for r in rows if not r.get("constructed")],
           "censusPairsNotReachedByConstructedPositives": not_reached,
           "classesWalkedOnBases": walked,
           "notApplicableNote": ("A census pair listed as not reached is a vocabulary class that no constructed claimed-positive graph contains (for example owner-retained "
                                 "exemptions of repository-execution grants, snapshot-path not-joined on vcs-change previousPath, h-identity/derived outside Rust "
                                 "ownership); no negative is claimed for it.")}
    json.dump(doc, open(OUT + "/vectors/retention-negatives.json", "w"), indent=1, sort_keys=True)
    print(json.dumps({k: doc[k] for k in ("allPass", "constructed", "notConstructed", "censusPairsNotReachedByConstructedPositives")}, indent=1))
    return 0 if doc["allPass"] else 1


if __name__ == "__main__":
    sys.exit(main())
