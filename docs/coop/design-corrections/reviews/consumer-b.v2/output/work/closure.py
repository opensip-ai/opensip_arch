"""Run closure: re-derive every identity from retained bytes and re-run the
owning contract's own admission (identity-and-evidence section 3).

Nothing is re-executed: no compiler, cargo, provider, repository or filesystem
operation runs here; the admission is re-decided over retained descriptors alone.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import osref as O
from osref import C, H, RAW, REC, Refuse
import graph as G
from graph import sha_text, bare, admit_native_context, bind_typescript_universe, \
    bind_rust_universe, inventory_map, CONTEXT_DOMAIN, UNIVERSE_DOMAIN

PROOF_FORBIDDEN_DOMAINS = {"run", "semantic-evidence", "evaluation-seal", "proof-bundle"}
UNRESOLVABLE_ROOT_DOMAINS = {"coverage-payload", "import-payload", "fact-payload"}


def fetch_frame(store, domain_or_set, digest, label):
    blob = store.get(digest)
    domains = domain_or_set if isinstance(domain_or_set, (set, frozenset)) else {domain_or_set}
    domain, payload = O.parse_frame(blob, domains)
    if H(domain, payload) != digest:
        raise Refuse("CLOSURE.IDENTITY_MISMATCH", label)
    return domain, payload


def fetch_record(store, digest, label):
    blob = store.get(digest)
    payload = O.parse(blob)
    if C(payload) != blob:
        raise Refuse("CLOSURE.RECORD_NOT_CANONICAL", label)
    if REC(payload) != digest:
        raise Refuse("CLOSURE.RECORD_DIGEST_MISMATCH", label)
    return payload


def close_run(store, run_id, expected_language, trace=None):
    """Returns the closure trace; raises Refuse with a typed cause."""
    t = trace if trace is not None else []

    def note(step, ok="ok"):
        t.append((step, ok))

    _, run = fetch_frame(store, "run", bare(run_id), "run")
    note("run frame parsed and re-hashed")

    _, plan = fetch_frame(store, "plan", bare(run["planId"]), "plan")
    _, snapshot = fetch_frame(store, "snapshot", bare(run["snapshotId"]), "snapshot")
    if plan["snapshotId"] != run["snapshotId"]:
        raise Refuse("CLOSURE.CROSS_SOURCE", "plan.snapshotId != run.snapshotId")
    if snapshot["projectId"] != run["projectId"]:
        raise Refuse("CLOSURE.CROSS_TENANT", "snapshot.projectId")
    note("plan/snapshot joined to run")

    # ---- auxiliary canonical records of the snapshot
    inventory = snapshot["sourceInventory"]
    O.check_order("path", inventory, "source-inventory")
    seen = set()
    for row in inventory:
        if row["path"] in seen:
            raise Refuse("CLOSURE.DUPLICATE_INVENTORY_PATH", row["path"])
        seen.add(row["path"])
        blob = store.get(row["sha256"])
        if len(blob) != row["bytes"]:
            raise Refuse("CLOSURE.BLOB_LENGTH_MISMATCH", row["path"])
    vcs = fetch_record(store, snapshot["vcsDigest"], "vcs-observation")
    if vcs["sourceInventoryDigest"] != REC(inventory):
        raise Refuse("CLOSURE.INVENTORY_DIGEST_MISMATCH", "vcs-observation")
    fetch_record(store, snapshot["scopeDigest"], "scope-descriptor")
    fetch_record(store, snapshot["resolvedConfigDigest"], "semantic-configuration")
    note("snapshot inventory, vcs, scope and configuration re-derived")

    # snapshot config/scope and Plan config/scope must agree
    if plan["scopeDigest"] != snapshot["scopeDigest"]:
        raise Refuse("CLOSURE.SCOPE_DISAGREEMENT", "plan vs snapshot")
    if plan["resolvedConfigDigest"] != snapshot["resolvedConfigDigest"]:
        raise Refuse("CLOSURE.CONFIG_DISAGREEMENT", "plan vs snapshot")

    # ---- capability manifest: derived, never trusted
    cap_bytes = store.get(plan["capabilityManifestBytesDigest"])
    recomputed = O.capability_manifest_id(cap_bytes)
    if recomputed != plan["capabilityManifestId"]:
        raise Refuse("CLOSURE.CAPABILITY_MANIFEST_ID_MISMATCH", recomputed)
    if run["capabilityManifestId"] != plan["capabilityManifestId"]:
        raise Refuse("CLOSURE.CAPABILITY_MANIFEST_ID_MISMATCH", "run vs plan")
    note("capabilityManifestId recomputed from the committed CVE1 artifact")

    # ---- retained closures
    closures = {}
    for digest, blob in list(store.objects.items()):
        if blob.startswith(O.FRAME_PREFIX + b"\x00closure\x00"):
            _, desc = O.parse_frame(blob, {"closure"})
            closures["closure2:" + digest] = desc
    for cid in plan["semanticClosures"]:
        if cid not in closures:
            raise Refuse("CLOSURE.SEMANTIC_CLOSURE_UNRETAINED", cid)
        for row in closures[cid]["tree"]:
            store.get(row["sha256"])
        store.get(closures[cid]["manifestDigest"])
    note("Plan-selected semantic closures retained with complete trees")

    # ---- native contexts: re-run the owning contract's admission
    ctx_frames = {}
    for digest, blob in list(store.objects.items()):
        for dom in CONTEXT_DOMAIN.values():
            if blob.startswith(O.FRAME_PREFIX + b"\x00" + dom.encode() + b"\x00"):
                _, payload = O.parse_frame(blob, {dom})
                ctx_frames[digest] = (dom, payload)
    if set(ctx_frames) != set(plan["nativeContextDigests"]):
        raise Refuse("CLOSURE.CONTEXT_SET_MISMATCH",
                     "retained=%d plan=%d" % (len(ctx_frames), len(plan["nativeContextDigests"])))
    if not plan["nativeContextDigests"]:
        raise Refuse("CLOSURE.NO_NATIVE_CONTEXT_SELECTED", "non-empty set required by this run")
    note("retained context frame set equals plan.nativeContextDigests")

    nested = {}
    for digest, blob in list(store.objects.items()):
        for dom in ("native.dependency-source-set.v1", "native.unified-features.rust.v1",
                    "native.prepared-output-set.v3", "native.cargo-config-projection.v2",
                    "native.dependency-file-manifest.v1"):
            if blob.startswith(O.FRAME_PREFIX + b"\x00" + dom.encode() + b"\x00"):
                _, payload = O.parse_frame(blob, {dom})
                nested[sha_text(digest)] = {"domain": dom, "record": payload}
                nested[digest] = {"domain": dom, "record": payload}
    retained = {"closures": closures, "nested": nested, "blobs": set(store.objects)}

    admissions = {}
    for digest, (dom, ctx) in ctx_frames.items():
        language = "typescript" if dom.endswith("typescript.v2") else "rust"
        adm = admit_native_context(language, ctx, retained, inventory)
        if adm["contextId"] != digest:
            raise Refuse("CLOSURE.CONTEXT_IDENTITY_MISMATCH", digest)
        admissions[digest] = (language, adm, ctx)
        # nested dependency chain down to raw bytes
        if language == "rust":
            dep = nested[ctx["dependencySourceSetId"]]["record"]
            for pkg in dep["packages"]:
                man = nested.get(pkg["fileManifestSha256"])
                if man is None:
                    raise Refuse("CLOSURE.DEPENDENCY_FILE_MANIFEST_UNRETAINED", pkg["name"])
                if H("native.dependency-file-manifest.v1", man["record"]) != pkg["fileManifestSha256"]:
                    raise Refuse("CLOSURE.DEPENDENCY_FILE_MANIFEST_MISMATCH", pkg["name"])
                for row in man["record"]:
                    blob = store.get(row["contentSha256"])
                    if len(blob) != row["byteLength"]:
                        raise Refuse("CLOSURE.DEPENDENCY_MEMBER_LENGTH", row["path"])
            proj = ctx["configProjection"]
            store.get(proj["projectionSha256"])
    note("admit_native_context re-run over retained bytes for every context")

    # ---- native universes
    universes = {}
    for digest, blob in list(store.objects.items()):
        for dom in UNIVERSE_DOMAIN.values():
            if blob.startswith(O.FRAME_PREFIX + b"\x00" + dom.encode() + b"\x00"):
                _, payload = O.parse_frame(blob, {dom})
                universes[digest] = (dom, payload)
    for digest, (dom, uni) in universes.items():
        ctx_hex = bare(uni["nativeContextId"])
        if ctx_hex not in plan["nativeContextDigests"]:
            raise Refuse("CLOSURE.UNIVERSE_BINDS_UNSELECTED_CONTEXT", ctx_hex)
        language, adm, ctx = admissions[ctx_hex]
        if dom != UNIVERSE_DOMAIN[language]:
            raise Refuse("native.native-context-language-mismatch", dom)
        if language == "typescript":
            b = bind_typescript_universe(uni, adm, ctx)
        elif language == "rust":
            b = bind_rust_universe(uni, adm, ctx, retained, inventory)
            if b["requiredGrantOperation"] is not None:
                grant = fetch_record(store, plan["semanticGrantDigest"], "semantic-grant")
                if b["requiredGrantOperation"] not in grant["analysisOperations"]:
                    raise Refuse("CLOSURE.PREPARED_RESOLUTION_WITHOUT_GRANT",
                                 b["requiredGrantOperation"])
        else:
            raise Refuse("NATIVE_UNIVERSE_BINDING_UNAVAILABLE", dom)
        if b["universeId"] != digest:
            raise Refuse("CLOSURE.UNIVERSE_IDENTITY_MISMATCH", digest)
    if not universes:
        raise Refuse("CLOSURE.NO_UNIVERSE_RETAINED", "")
    langs = set(admissions[bare(u["nativeContextId"])][0] for _, u in universes.values())
    if langs != {expected_language}:
        raise Refuse("CLOSURE.WRONG_LANGUAGE_UNIVERSE_PATH", repr(sorted(langs)))
    note("bind_%s_universe re-run; universe language path exercised" % expected_language)

    # ---- Plan auxiliary records
    fetch_record(store, plan["analysisSpecDigest"], "analysis-spec")
    grant = fetch_record(store, plan["semanticGrantDigest"], "semantic-grant")
    if grant["projectId"] != run["projectId"] or grant["scopeDigest"] != plan["scopeDigest"]:
        raise Refuse("CLOSURE.GRANT_JOIN", "projectId/scope")
    policy = fetch_record(store, plan["policyDigest"], "PolicyDocumentV1")
    fetch_record(store, plan["waiverDigest"], "WaiverSetV1")
    for imp in plan["importIds"]:
        _, wrapper = fetch_frame(store, "import", bare(imp), "import")
        if "read-import" not in grant["analysisOperations"]:
            raise Refuse("CLOSURE.IMPORT_WITHOUT_READ_IMPORT_GRANT", imp)
    note("Plan policy, waivers, analysis spec and semantic grant re-derived")

    # ---- evidence / seal / proof
    _, evidence = fetch_frame(store, "semantic-evidence", bare(run["evidenceId"]), "evidence")
    _, seal = fetch_frame(store, "evaluation-seal", bare(run["evaluationSealId"]), "seal")
    _, proof = fetch_frame(store, "proof-bundle", bare(evidence["proofBundleId"]), "proof")
    for name, obj in (("evidence", evidence), ("seal", seal), ("proof", proof)):
        if obj["planId"] != run["planId"]:
            raise Refuse("CLOSURE.CROSS_PLAN", name)
    if seal["evidenceId"] != run["evidenceId"] or seal["proofBundleId"] != evidence["proofBundleId"]:
        raise Refuse("CLOSURE.SEAL_JOIN", "")
    if seal["verdict"] != proof["verdict"]:
        raise Refuse("CLOSURE.VERDICT_DISAGREEMENT", "")
    if seal["policyDigest"] != plan["policyDigest"]:
        raise Refuse("CLOSURE.SEAL_POLICY_JOIN", "")
    _, exec_plan = fetch_frame(store, "execution-plan", bare(proof["executionPlanId"]), "exec-plan")
    if exec_plan["planId"] != run["planId"]:
        raise Refuse("CLOSURE.CROSS_PLAN", "exec-plan")
    for stage in exec_plan["stages"]:
        spec = fetch_record(store, stage["stageSpecDigest"], "stage-spec")
        if spec["planId"] != run["planId"]:
            raise Refuse("CLOSURE.CROSS_PLAN", "stage-spec")
        if spec["producerClosure"] not in plan["semanticClosures"]:
            raise Refuse("CLOSURE.STAGE_PRODUCER_NOT_PLAN_SELECTED", spec["producerClosure"])
        if spec["outputDomains"] != stage["outputDomains"]:
            raise Refuse("CLOSURE.STAGE_OUTPUT_DOMAINS", "")
        aspec = fetch_record(store, plan["analysisSpecDigest"], "analysis-spec")
        for row in spec["parameters"]:
            if row not in aspec["parameters"]:
                raise Refuse("CLOSURE.STAGE_HIDDEN_INPUT", C(row).decode())
        store.get(spec["outputSchemaDigest"])
    note("derivation DAG stages joined; no stage takes a hidden input")

    # ---- compiled rule program is exactly the policy projection
    program = fetch_record(store, proof["ruleProgramDigest"], "RuleProgramV1")
    if program["policyDigest"] != plan["policyDigest"]:
        raise Refuse("CLOSURE.PROGRAM_POLICY_MISMATCH", "")
    expected = [{"ruleId": r["ruleId"], "ruleProgramRef": r["ruleProgramRef"],
                 "emitWhen": r["emitWhen"]} for r in policy["rules"]]
    if program["rules"] != expected:
        raise Refuse("CLOSURE.PROGRAM_NOT_POLICY_PROJECTION", "")
    note("RuleProgramV1 is exactly the policy projection in ruleId order")

    # ---- proof input vocabulary and roots
    input_set = set()
    for ref in proof["evaluationInputRefs"]:
        if ref["domain"] in PROOF_FORBIDDEN_DOMAINS:
            raise Refuse("CLOSURE.PROOF_REF_DOMAIN_FORBIDDEN", ref["domain"])
        if ref["domain"] in UNRESOLVABLE_ROOT_DOMAINS:
            raise Refuse("CLOSURE.PAYLOAD_DOMAIN_AS_AUTHORITATIVE_ROOT", ref["domain"])
        input_set.add((ref["domain"], ref["digest"]))
        if ref["domain"] == "native-context" and ref["digest"] not in plan["nativeContextDigests"]:
            raise Refuse("CLOSURE.PROOF_CONTEXT_NOT_PLAN_SELECTED", ref["digest"])
        if ref["domain"] == "import" and ("import2:" + ref["digest"]) not in plan["importIds"]:
            raise Refuse("CLOSURE.PROOF_IMPORT_NOT_PLAN_SELECTED", ref["digest"])
    O.check_order("canonical-set", proof["evaluationInputRefs"], "proof.evaluationInputRefs")
    named_views = sorted(["view2:" + d for (dom, d) in input_set if dom == "view"],
                         key=lambda s: C(s))
    if evidence["viewIds"] != named_views:
        raise Refuse("CLOSURE.EVIDENCE_VIEW_ROOTS", "evidence views != named views")
    note("proof input vocabulary closed; evidence view roots equal named views")

    # ---- views, facts, coverage
    coverage_union = set()
    for vid in evidence["viewIds"]:
        _, view = fetch_frame(store, "view", bare(vid), "view")
        if view["planId"] != run["planId"]:
            raise Refuse("CLOSURE.CROSS_PLAN", "view")
        if view["producerClosure"] not in plan["semanticClosures"]:
            raise Refuse("CLOSURE.VIEW_PRODUCER_NOT_PLAN_SELECTED", view["producerClosure"])
        rel_rung = set()
        universe_pairs = set()
        for fid in view["facts"]:
            _, fact = fetch_frame(store, "fact", bare(fid), "fact")
            if fact["snapshotId"] != run["snapshotId"]:
                raise Refuse("CLOSURE.CROSS_SOURCE", "fact")
            if fact["producerClosure"] != view["producerClosure"]:
                raise Refuse("CLOSURE.VIEW_PRODUCER_DISAGREEMENT", fid)
            if fact["sourceUniverse"] not in universes or fact["targetUniverse"] not in universes:
                raise Refuse("CLOSURE.FACT_UNIVERSE_UNRETAINED", fid)
            invmap = inventory_map(inventory)
            for a in fact["anchors"]:
                row = invmap.get(a["path"])
                if row is None or row["sha256"] != a["blobDigest"]:
                    raise Refuse("CLOSURE.ANCHOR_NOT_INVENTORIED", a["path"])
                if not (0 <= a["startByte"] <= a["endByte"] <= row["bytes"]):
                    raise Refuse("CLOSURE.ANCHOR_SPAN_OUT_OF_BOUNDS", a["path"])
            store.get(fact["payloadSchemaDigest"])
            fetch_record(store, fact["payloadDigest"], "fact payload")
            rel_rung.add((fact["relation"], fact["resolution"]))
            universe_pairs.add((fact["sourceUniverse"], fact["targetUniverse"]))
        scope_ids = set(view["scopeIds"])
        for cid in view["coverageIds"]:
            coverage_union.add(cid)
            _, cov = fetch_frame(store, "coverage", bare(cid), "coverage")
            if cov["scopeId"] not in scope_ids:
                raise Refuse("native.coverage-subject-scope-outside-view", cid)
            _, sc = fetch_frame(store, "subject-scope", bare(cov["scopeId"]), "subject-scope")
            if sc["snapshotId"] != run["snapshotId"]:
                raise Refuse("CLOSURE.CROSS_SOURCE", "subject-scope")
            if sc["enumeratorClosure"] not in plan["semanticClosures"]:
                raise Refuse("CLOSURE.ENUMERATOR_NOT_PLAN_SELECTED", sc["enumeratorClosure"])
            O.check_order("canonical-set", sc["subjects"], "subject-scope.subjects")
            payload = fetch_record(store, cov["payloadDigest"], "CoverageResultV3")
            store.get(cov["payloadSchemaDigest"])
            # the in-band commitment is the same digest as the scope it names
            if payload["key"]["subjectScopeCommitment"] != sha_text(bare(cov["scopeId"])):
                raise Refuse("native.subject-scope-commitment-mismatch", cid)
            if payload["entry"]["examinedUniverse"]["subjectCount"] != len(sc["subjects"]):
                raise Refuse("native.examined-universe-subject-count-mismatch", cid)
            rel_rung.add((sc["relation"], sc["resolution"]))
            universe_pairs.add((sc["sourceUniverse"], sc["targetUniverse"]))
        if len(rel_rung) > 1:
            raise Refuse("CLOSURE.VIEW_RELATION_RUNG_DISAGREEMENT", repr(sorted(rel_rung)))
        if len(universe_pairs) > 1:
            raise Refuse("CLOSURE.VIEW_UNIVERSE_DISAGREEMENT", "")
    if set(evidence["coverageIds"]) != coverage_union:
        raise Refuse("CLOSURE.EVIDENCE_COVERAGE_ROOTS", "")
    note("views/facts/Coverage agree on source, universes, relation/rung and producer")

    # ---- predicate proofs and witnesses
    for pp in proof["predicateProofs"]:
        for ref in pp["inputRefs"]:
            if (ref["domain"], ref["digest"]) not in input_set:
                raise Refuse("CLOSURE.PREDICATE_INPUT_NOT_IN_EVALUATION_INPUTS",
                             ref["domain"] + ":" + ref["digest"])
        witness = fetch_record(store, pp["witnessDigest"], "predicate-witness")
        prog_pred = fetch_record(store, witness["programPredicateDigest"], "program-predicate")
        if prog_pred["ruleProgramDigest"] != proof["ruleProgramDigest"]:
            raise Refuse("CLOSURE.PROGRAM_PREDICATE_WRONG_PROGRAM", "")
        if prog_pred["ruleId"] != pp["ruleId"] or prog_pred["predicateId"] != pp["predicateId"]:
            raise Refuse("CLOSURE.PROGRAM_PREDICATE_ADDRESS", "")
        if prog_pred["operation"] != pp["operation"]:
            raise Refuse("CLOSURE.PROGRAM_PREDICATE_OPERATION", "")
        rule = [r for r in program["rules"] if r["ruleId"] == pp["ruleId"]]
        if not rule:
            raise Refuse("CLOSURE.PROGRAM_PREDICATE_UNKNOWN_RULE", pp["ruleId"])
        node = address_node(rule[0]["emitWhen"], pp["predicateId"])
        if REC(node) != prog_pred["nodeDigest"]:
            raise Refuse("CLOSURE.PROGRAM_PREDICATE_NODE_DIGEST", pp["predicateId"])
        if node["op"] != pp["operation"]:
            raise Refuse("CLOSURE.PROGRAM_PREDICATE_NODE_OP", pp["predicateId"])
        children = operand_addresses(node, pp["predicateId"])
        if sorted(witness["childPredicateIds"], key=lambda s: C(s)) != sorted(children, key=lambda s: C(s)):
            raise Refuse("CLOSURE.WITNESS_CHILDREN", pp["predicateId"])
        want_limit = node.get("n") if node["op"] == "count-at-most" else None
        if witness["countLimit"] != want_limit:
            raise Refuse("CLOSURE.WITNESS_COUNT_LIMIT", pp["predicateId"])
        for fid in witness["matchingFactIds"]:
            store.get(bare(fid))
        for cid in witness["coverageIds"]:
            if cid not in coverage_union:
                raise Refuse("CLOSURE.WITNESS_COVERAGE_OUTSIDE_VIEWS", cid)
    note("predicate witnesses address real program nodes; children/limits agree")

    # ---- findings
    if proof["findingIds"] != evidence["findingIds"]:
        raise Refuse("CLOSURE.FINDING_SET_DISAGREEMENT", "")
    note("finding sets agree (a false emitWhen is a retained no-match proof)")
    return t


def address_node(root, address):
    """p; a.i for the i-th and/or operand; a.0 for the not operand."""
    if address == "p":
        return root
    if not address.startswith("p."):
        raise Refuse("CLOSURE.PREDICATE_ADDRESS_MALFORMED", address)
    node = root
    for part in address.split(".")[1:]:
        if part != "0" and part.startswith("0"):
            raise Refuse("CLOSURE.PREDICATE_ADDRESS_MALFORMED", address)
        i = int(part)
        if node.get("op") in ("and", "or"):
            node = node["operands"][i]
        elif node.get("op") == "not":
            if i != 0:
                raise Refuse("CLOSURE.PREDICATE_ADDRESS_MALFORMED", address)
            node = node["operand"]
        else:
            raise Refuse("CLOSURE.PREDICATE_ADDRESS_NOT_A_NODE", address)
    return node


def operand_addresses(node, address):
    if node.get("op") in ("and", "or"):
        return ["%s.%d" % (address, i) for i in range(len(node["operands"]))]
    if node.get("op") == "not":
        return [address + ".0"]
    return []
