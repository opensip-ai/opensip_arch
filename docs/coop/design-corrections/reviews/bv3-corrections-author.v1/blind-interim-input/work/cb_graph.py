"""Blind consumer-B: complete minimal positive Run descriptor graphs.

Three graphs are built end to end from synthetic trusted observations:
  RUN-TS      an ordinary TypeScript repository with four native contexts
              (node_modules-reading tsconfig project, synthesized configuration,
              explicitly selected custom-named config with repeated ordered
              bases, jsconfig inheriting a differently named shared base),
              a JavaScript clone body through the TypeScript engine universe,
              and a file fact with inventoried path/hash/length joins.
  RUN-RUST    a mixed-edition Cargo workspace with a target-specific edition
              override, a '#'-containing marker directory, the same physical
              source file analysed under two explicitly selected target
              editions, a large edition map, and clones at L0 and L1.
  RUN-RUST-P  the partial-ownership Run: an empty clone view that reports its
              incompleteness instead of claiming complete Coverage, with an
              indeterminate predicate and an indeterminate seal.

Every synthetic observation (file bytes, closure trees, provider output) is an
ASSUMPTION, never native enforcement proof. Nothing here executes a compiler,
Cargo, a provider, a repository or SQLite.
"""

import hashlib
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cb_canonical as K

SUBJECT = "/tmp/opensip-design-corrections/consumer-b.v3/subject"

# --------------------------------------------------------------------------
# Registered schema documents: raw-artifact digests of the EXACT full bytes.
# --------------------------------------------------------------------------
DOCS = {
    "relation": "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json",
    "native": "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
    "identity": "docs/coop/design-corrections/foundation/identity-schemas.v2.json",
    "policy": "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json",
    "common": "docs/coop/design-corrections/workflows/schemas/common.schema.json",
    "imported": "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json",
    "importsrc": "docs/coop/design-corrections/foundation/import-source-context.schema.json",
}
DOC_DIGEST = {k: K.raw_bytes_sha256(open(os.path.join(SUBJECT, v), "rb").read())
              for k, v in DOCS.items()}

# The 8 one-rung relations whose ladder the successor registry does not carry
# (see blind-review MUST-1); values taken from the inherited fact-plane.v1
# relationRegistry, under a stated assumption.
LADDER = K.RELATION_LADDERS_INHERITED

BLOBS = {}          # sha256 hex -> exact bytes (the content-addressed store)
FRAMES = {}         # bare hex   -> exact H preimage frame
RECORDS = {}        # raw sha256 -> exact C(record) bytes
NOTES = []


def retain_blob(b):
    h = K.raw_bytes_sha256(b)
    BLOBS[h] = b
    return h


def retain_record(rec):
    body = K.C(rec)
    h = hashlib.sha256(body).hexdigest()
    RECORDS[h] = body
    return h


def retain_frame(domain, descriptor):
    f = K.frame(domain, descriptor)
    h = hashlib.sha256(f).hexdigest()
    FRAMES[h] = f
    return h


def ident(domain, descriptor):
    """Mint a typed identity AND retain its exact H preimage frame."""
    h = retain_frame(domain, descriptor)
    return f"{K.PREFIX[domain]}:{h}", h


def native_ident(domain, descriptor):
    """Mint a native H identity in sha256: text form, retaining the frame."""
    h = retain_frame(domain, descriptor)
    return f"sha256:{h}", h


# --------------------------------------------------------------------------
# Closures.
# --------------------------------------------------------------------------
def make_closure(kind, files, version, protocol_major, platform):
    tree = K.ordered(
        [{"path": p, "sha256": retain_blob(b), "bytes": len(b)} for p, b in files],
        "path")
    manifest_body = ("{\"component\":\"%s\",\"version\":\"%s\"}" % (kind, version)).encode()
    desc = {"schemaVersion": 2, "kind": kind,
            "manifestDigest": retain_blob(manifest_body),
            "tree": tree, "semanticVersion": version,
            "protocolMajor": protocol_major, "platform": platform}
    cid, h = ident("closure", desc)
    return {"id": cid, "hex": h, "desc": desc, "tree": tree}


PLATFORM = "macos-aarch64"

CL_TS_TOOLCHAIN = make_closure(
    "toolchain",
    [("bin/node", b"cb-synthetic-node-runtime"),
     ("lib/tsc.js", b"cb-synthetic-typescript-compiler"),
     ("package.json", b'{"name":"typescript","version":"5.6.2"}')],
    "5.6.2", 2, PLATFORM)
CL_TS_STDLIB = make_closure(
    "stdlib",
    [("lib.dom.d.ts", b"cb-synthetic-lib-dom"),
     ("lib.es2022.d.ts", b"cb-synthetic-lib-es2022"),
     ("lib.esnext.d.ts", b"cb-synthetic-lib-esnext")],
    "5.6.2", 2, PLATFORM)
CL_RS_TOOLCHAIN = make_closure(
    "toolchain",
    [("bin/ar", b"cb-synthetic-ar"), ("bin/cargo", b"cb-synthetic-cargo"),
     ("bin/ld", b"cb-synthetic-linker"),
     ("bin/proc-macro-srv", b"cb-synthetic-proc-macro-server"),
     ("bin/rustc", b"cb-synthetic-rustc")],
    "1.83.0", 3, PLATFORM)
CL_RS_LLVM = make_closure(
    "rust-dev-llvm", [("lib/libLLVM.dylib", b"cb-synthetic-llvm")],
    "1.83.0", 3, PLATFORM)
CL_TS_PROVIDER = make_closure(
    "provider", [("bin/ts-provider", b"cb-synthetic-typescript-semantic")],
    "1.0.0", 2, PLATFORM)
CL_RS_PROVIDER = make_closure(
    "provider", [("bin/rust-provider", b"cb-synthetic-rust-semantic")],
    "1.0.0", 3, PLATFORM)
CL_EVALUATOR = make_closure(
    "evaluator", [("bin/evaluator", b"cb-synthetic-pure-evaluator")],
    "1.0.0", 1, PLATFORM)
CL_DETECTOR = make_closure(
    "detector", [("rules/cb.file.present", b"cb-synthetic-rule")],
    "1.0.0", 1, PLATFORM)
CL_ADAPTER = make_closure(
    "adapter", [("bin/cargo-adapter", b"cb-synthetic-cargo-adapter")],
    "1.0.0", 3, PLATFORM)

# The retained level specifications: normalisationVersion is the raw SHA-256 of
# the EXACT retained canonical level-specification bytes (never a label).
LEVEL_SPEC = {}
for lvl in ("L0-verbatim", "L1-lexical"):
    spec = json.dumps({
        "levelId": lvl, "specVersion": "cb-blind-1",
        "lexicalBoundaryRules": {"typescript": "cb-ts-lexer-1",
                                 "javascript": "cb-js-lexer-1",
                                 "rust": "cb-rs-lexer-1"},
        "tokenKindRegistry": ["ident", "kw", "op", "str", "num", "ws"],
        "directiveClassification": ["use-strict", "cfg", "ts-directive"],
        "transformOrder": ["strip-insignificant-whitespace"] if lvl != "L0-verbatim" else [],
        "replacementBytes": {},
    }, sort_keys=True, separators=(",", ":")).encode()
    LEVEL_SPEC[lvl] = {"bytes": spec, "hex": retain_blob(spec),
                       "raw32": hashlib.sha256(spec).digest()}


# --------------------------------------------------------------------------
# Snapshot helper.
# --------------------------------------------------------------------------
class Repo:
    def __init__(self, project_id):
        self.project_id = project_id
        self.files = {}

    def add(self, path, content):
        b = content if isinstance(content, bytes) else content.encode("utf-8")
        self.files[path] = b
        retain_blob(b)
        return b

    def digest(self, path):
        return K.raw_bytes_sha256(self.files[path])

    def inventory(self):
        return K.ordered([{"path": p, "sha256": K.raw_bytes_sha256(b),
                           "bytes": len(b)} for p, b in self.files.items()], "path")

    def snapshot(self, scope_digest, config_digest, commit):
        inv = self.inventory()
        inv_digest = retain_record(inv)
        vcs = {"schemaVersion": 2, "kind": "git", "commitId": commit,
               "dirty": False, "sourceInventoryDigest": inv_digest}
        vcs_digest = retain_record(vcs)
        snap = {"schemaVersion": 2, "projectId": self.project_id,
                "sourceInventory": inv, "resolvedConfigDigest": config_digest,
                "scopeDigest": scope_digest, "vcsDigest": vcs_digest}
        sid, h = ident("snapshot", snap)
        return {"id": sid, "hex": h, "desc": snap, "inventory": inv,
                "vcs": vcs, "inventoryDigest": inv_digest}


def scope_descriptor(roots, prefixes, excluded):
    d = {"schemaVersion": 2,
         "workspaceRoots": K.ordered(roots, "canonical-set"),
         "pathPrefixes": K.ordered(prefixes, "canonical-set"),
         "excludedPathPrefixes": K.ordered(excluded, "canonical-set")}
    return d, retain_record(d)


def semantic_configuration(profile, capabilities, limit):
    cfg = {"analysis": {"profileId": profile,
                        "capabilities": K.ordered(capabilities, "canonical-set"),
                        "budget": {"unit": "work-units", "limit": limit}},
           "components": {}, "discovery": {}, "policy": {}, "evidence": {}}
    return cfg, retain_record(cfg)


# --------------------------------------------------------------------------
# TypeScript native contexts and universes.
# --------------------------------------------------------------------------
TS_STDLIB_INVENTORY = K.ordered(
    [{"component": os.path.basename(row["path"]), "sha256": row["sha256"]}
     for row in CL_TS_STDLIB["tree"] if row["path"].endswith(".d.ts")],
    {"by": ["component"]})
TS_COMPILER_MEMBER = next(r["sha256"] for r in CL_TS_TOOLCHAIN["tree"]
                          if r["path"] == "lib/tsc.js")
TS_RUNTIME_MEMBER = next(r["sha256"] for r in CL_TS_TOOLCHAIN["tree"]
                         if r["path"] == "bin/node")
TS_PACKAGE_MEMBER = next(r["sha256"] for r in CL_TS_TOOLCHAIN["tree"]
                         if r["path"] == "package.json")


def ts_honored(allow_js, check_js, jsx=None, base_url=None, module="node16",
               resolution="node16", target="es2022", lib=("lib.es2022.d.ts",)):
    return {"allowJs": allow_js, "checkJs": check_js, "module": module,
            "moduleResolution": resolution, "target": target, "strict": True,
            "skipLibCheck": True, "noEmit": True, "types": None,
            "lib": list(lib), "baseUrl": base_url, "paths": [], "rootDirs": [],
            "resolveJsonModule": True, "allowSyntheticDefaultImports": True,
            "esModuleInterop": True, "customConditions": [], "jsx": jsx}


def ts_context(language_mode, honored, stripped, config_graph_paths,
               module_resolution, package_module_type, layout_digest,
               lockfile_identity, lib_selection=("lib.es2022.d.ts",)):
    ctx = {
        "schemaVersion": 2,
        "languageMode": language_mode,
        "toolchain": {
            "compilerName": "typescript",
            "compilerVersion": CL_TS_TOOLCHAIN["desc"]["semanticVersion"],
            "compilerPackageDigest": TS_PACKAGE_MEMBER,
            "typescriptStdlibMerkleRoot": CL_TS_STDLIB["hex"],
            "standardLibraryComponentDigests": TS_STDLIB_INVENTORY,
            "libSelection": K.ordered(list(lib_selection), "utf8"),
        },
        "toolClosure": {"compiler": TS_COMPILER_MEMBER,
                        "runtime": TS_RUNTIME_MEMBER,
                        "closureId": CL_TS_TOOLCHAIN["id"]},
        "configProjection": {
            "schemaVersion": 2, "ancestorCarrierVerified": True,
            "environmentSanitized": True, "typeAcquisitionEnabled": False,
            "executableSelected": False, "honoredOptions": honored,
            "strippedOptions": stripped,
            "configGraphPaths": K.ordered(list(config_graph_paths), "utf8"),
        },
        "moduleResolutionMode": module_resolution,
        "packageModuleType": package_module_type,
        "nodeModulesLayoutDigest": layout_digest,
        "lockfileIdentity": lockfile_identity,
    }
    cid, h = native_ident("native.context.typescript.v2", ctx)
    return {"id": cid, "hex": h, "desc": ctx}


def ts_config_graph(entry, nodes):
    rec = {"schemaVersion": 1, "entryConfigPath": entry,
           "nodes": K.ordered(nodes, {"by": ["path"]})}
    return rec, retain_record(rec)


def derive_config_origin(graph):
    if graph["entryConfigPath"] is None and not graph["nodes"]:
        return "synthesized"
    entry = next(n for n in graph["nodes"] if n["path"] == graph["entryConfigPath"])
    return "jsconfig" if entry["kind"] == "jsconfig" else "tsconfig"


def ts_universe(ctx, graph, graph_digest, language_mode, package_module_type,
                allow_js, check_js, program_roots, js_roots, lockfile_kind,
                node_modules_in_read_set, synthesized=None):
    u = {
        "schemaVersion": 2, "languageMode": language_mode,
        "configOrigin": derive_config_origin(graph),
        "synthesizerVersion": 1 if synthesized else None,
        "synthesizedOptions": synthesized,
        "packageModuleType": package_module_type,
        "allowJs": allow_js, "checkJs": check_js,
        "jsAdmittedToProgram": allow_js, "jsDiagnosticsEnabled": check_js,
        "resolutionCompletenessImplied": False,
        "jsRootFiles": list(js_roots), "programRootFiles": list(program_roots),
        "lockfileKind": lockfile_kind,
        "nodeModulesInReadSet": node_modules_in_read_set,
        "executionCapableResolution": False,
        "tsconfigGraphHash": graph_digest,
        "nativeContextId": ctx["id"],
    }
    uid, h = native_ident("native.semantic-universe.typescript.v2", u)
    return {"id": uid, "hex": h, "desc": u, "ctx": ctx, "graph": graph}


def bind_typescript_universe(u, ctx, graph, inventory_paths, inventory_digests):
    """Reconstructed from native section 2.2/2.4 and the identity closure law."""
    if ctx is None:
        raise K.Refusal("native.universe-context-not-supplied")
    if u["desc"]["nativeContextId"] != ctx["id"]:
        raise K.Refusal("native.universe-context-binding-mismatch")
    if K.H("native.context.typescript.v2", ctx["desc"]) != ctx["hex"]:
        raise K.Refusal(
            "native.universe-context-binding-mismatch",
            "context-bytes-are-not-the-admitted-ones")
    c, d = ctx["desc"], u["desc"]
    for field, cv, uv in (
            ("languageMode", c["languageMode"], d["languageMode"]),
            ("packageModuleType", c["packageModuleType"], d["packageModuleType"]),
            ("allowJs", c["configProjection"]["honoredOptions"]["allowJs"], d["allowJs"]),
            ("checkJs", c["configProjection"]["honoredOptions"]["checkJs"], d["checkJs"]),
            ("lockfileKind",
             "none" if c["lockfileIdentity"] is None else c["lockfileIdentity"]["kind"],
             d["lockfileKind"]),
            ("nodeModulesInReadSet", c["nodeModulesLayoutDigest"] is not None,
             d["nodeModulesInReadSet"]),
            ("jsDiagnosticsEnabled", c["configProjection"]["honoredOptions"]["checkJs"],
             d["jsDiagnosticsEnabled"]),
            ("jsAdmittedToProgram", c["configProjection"]["honoredOptions"]["allowJs"],
             d["jsAdmittedToProgram"]),
            ("configOrigin", derive_config_origin(graph), d["configOrigin"]),
            ("extendsGraphEmpty", not c["configProjection"]["configGraphPaths"],
             not graph["nodes"]),
            ("synthesizedOptionsPresent",
             c["languageMode"] == "js-synthesized",
             d["synthesizedOptions"] is not None)):
        if cv != uv:
            raise K.Refusal("native.universe-context-field-mismatch", field)
    if retain_record(graph) != d["tsconfigGraphHash"]:
        raise K.Refusal("native.universe-config-graph-mismatch")
    node_paths = {n["path"] for n in graph["nodes"]}
    if node_paths != set(c["configProjection"]["configGraphPaths"]):
        raise K.Refusal("native.universe-config-graph-paths-mismatch")
    for n in graph["nodes"]:
        if n["path"] not in inventory_paths:
            raise K.Refusal("native.config-graph-path-outside-snapshot", n["path"])
        if inventory_digests[n["path"]] != n["contentSha256"]:
            raise K.Refusal("native.config-graph-digest-mismatch", n["path"])
        for e in n["extendsResolved"]:
            if e not in node_paths:
                raise K.Refusal("native.config-graph-edge-unknown", e)
    if graph["entryConfigPath"] is not None:
        seen, stack = set(), [graph["entryConfigPath"]]
        byp = {n["path"]: n for n in graph["nodes"]}
        while stack:
            p = stack.pop()
            if p in seen:
                continue
            seen.add(p)
            stack.extend(byp[p]["extendsResolved"])
        if seen != node_paths:
            raise K.Refusal("native.config-graph-node-unreachable")
    lf = c["lockfileIdentity"]
    if lf is not None:
        if lf["path"] not in inventory_paths:
            raise K.Refusal("native.lockfile-path-outside-snapshot", lf["path"])
        if inventory_digests[lf["path"]] != lf["contentSha256"]:
            raise K.Refusal("native.lockfile-digest-mismatch", lf["path"])
    return "ADMIT"


# --------------------------------------------------------------------------
# body-language-version and clone body identities.
# --------------------------------------------------------------------------
def ts_body_language_version(ctx, anchor_path):
    variant = K.ts_source_variant(anchor_path)
    rec = {"schemaVersion": 1,
           "languageId": K.TS_VARIANT_LANGUAGE[variant],
           "compilerName": ctx["desc"]["toolchain"]["compilerName"],
           "compilerVersion": ctx["desc"]["toolchain"]["compilerVersion"],
           "compilerBuild": ctx["desc"]["toolchain"]["compilerPackageDigest"],
           "dialect": {"sourceVariant": variant}}
    retain_record(rec)
    return rec, K.body_language_version_bytes(rec)


def rust_body_language_version(ctx, universe, ownership, anchor_path):
    """ctx and universe are the raw admitted Rust descriptor records."""
    edition = K.rust_effective_edition(ownership, universe["edition"], anchor_path)
    rec = {"schemaVersion": 1, "languageId": "rust", "compilerName": "rustc",
           "compilerVersion": ctx["toolchain"]["rustcVersion"],
           "compilerBuild": ctx["toolchain"]["rustCommitHash"],
           "dialect": {"edition": edition}}
    retain_record(rec)
    return rec, K.body_language_version_bytes(rec)


def clone_payload(level, span_bytes, tokens, language_id, lang_version_raw32):
    spec = LEVEL_SPEC[level]
    payload = (K.l0_payload(span_bytes) if level == "L0-verbatim"
               else K.framed_token_stream(tokens))
    bid, preimage = K.body_identity(level, spec["raw32"], language_id,
                                    lang_version_raw32, payload)
    BLOBS[bid.split(":", 1)[1]] = preimage      # the frame is retained
    return {"bodyIdentity": bid, "normalisationLevel": level,
            "normalisationVersion": spec["hex"]}, preimage, payload


# --------------------------------------------------------------------------
# fact2 / subject-scope / coverage2 / view2.
# --------------------------------------------------------------------------
def make_fact(snapshot_id, relation, rung, source_u, target_u, producer_closure,
              payload, anchors, confidence=1000000):
    if rung not in LADDER[relation]:
        raise K.Refusal("FACT_RUNG_NOT_IN_LADDER", f"{relation}/{rung}")
    reg = RELATION_REGISTRY["relations"][relation]
    if reg["universeRule"] == "same-only" and source_u != target_u:
        raise K.Refusal("FACT_UNIVERSE_RULE_SAME_ONLY", relation)
    if relation == "clones" and len(anchors) != 1:
        raise K.Refusal("CLONES_ANCHOR_CARDINALITY", str(len(anchors)))
    desc = {"schemaVersion": 2, "snapshotId": snapshot_id, "relation": relation,
            "resolution": rung, "sourceUniverse": source_u,
            "targetUniverse": target_u, "producerClosure": producer_closure,
            "payloadSchemaDigest": DOC_DIGEST["relation"],
            "payloadDigest": retain_record(payload),
            "anchors": K.ordered(anchors, "canonical-set"),
            "confidenceMillionths": confidence}
    fid, h = ident("fact", desc)
    return {"id": fid, "hex": h, "desc": desc, "payload": payload}


RELATION_REGISTRY = json.load(
    open(os.path.join(SUBJECT, DOCS["relation"])))["x-opensip-relation-registry"]


def make_scope(snapshot_id, source_u, target_u, relation, rung,
               enumerator_closure, subjects):
    desc = {"schemaVersion": 2, "snapshotId": snapshot_id,
            "sourceUniverse": source_u, "targetUniverse": target_u,
            "relation": relation, "resolution": rung,
            "enumeratorClosure": enumerator_closure,
            "subjects": K.ordered(subjects, "canonical-set")}
    sid, h = ident("subject-scope", desc)
    return {"id": sid, "hex": h, "desc": desc,
            "commitment": "sha256:" + h, "subjectCount": len(desc["subjects"])}


def make_coverage(scope, entry):
    payload = {"schemaVersion": 3,
               "key": {"relation": scope["desc"]["relation"],
                       "resolution": scope["desc"]["resolution"],
                       "sourceUniverse": scope["desc"]["sourceUniverse"],
                       "targetUniverse": scope["desc"]["targetUniverse"],
                       "subjectScopeCommitment": scope["commitment"]},
               "entry": entry}
    # admit_coverage_result_v3 joins, reconstructed from native section 4.1a.
    e = payload["entry"]
    if e["examinedUniverse"]["subjectScopeCommitment"] != scope["commitment"]:
        raise K.Refusal("native.examined-universe-commitment-mismatch")
    if e["examinedUniverse"]["subjectCount"] != scope["subjectCount"]:
        raise K.Refusal("native.examined-universe-subject-count-mismatch")
    if e["relation"] != scope["desc"]["relation"] or \
            e["resolution"] != scope["desc"]["resolution"]:
        raise K.Refusal("native.coverage-entry-key-mismatch")
    desc = {"schemaVersion": 2, "scopeId": scope["id"],
            "payloadSchemaDigest": DOC_DIGEST["native"],
            "payloadDigest": retain_record(payload)}
    cid, h = ident("coverage", desc)
    return {"id": cid, "hex": h, "desc": desc, "payload": payload,
            "scope": scope}


def coverage_entry(relation, rung, coverage, scope, state, attempted,
                   exhaustive, terminal, edge_count, edge_classes,
                   deficiency=None, native_cause=None, closed_world=None,
                   confidence=1000000, derivation_kinds=()):
    cw = closed_world or {
        "exportsClosed": "closed", "entryPointsRecognized": "all",
        "nonliteralLoading": "none", "externalConsumers": "none-declared",
        "dynamicDispatch": "not-applicable", "reasons": [],
        "deadCodeRepairEligible": True}
    return {"relation": relation, "resolution": rung, "coverage": coverage,
            "examinedUniverse": {"subjectScopeCommitment": scope["commitment"],
                                 "subjectCount": scope["subjectCount"]},
            "resolutionCompleteness": {
                "state": state, "attempted": attempted,
                "examinedExhaustive": exhaustive, "stageTerminal": terminal,
                "unresolvedEdgeCount": edge_count,
                "unresolvedEdgeClasses": K.ordered(list(edge_classes), "utf8")},
            "closedWorld": cw,
            "derivationKinds": K.ordered(list(derivation_kinds), "utf8"),
            "confidenceMillionths": confidence,
            "deficiency": deficiency, "nativeCause": native_cause}


def make_view(plan_id, scopes, facts, coverages, producer_closure, schema_digests):
    desc = {"schemaVersion": 2, "planId": plan_id,
            "scopeIds": K.ordered([s["id"] for s in scopes], "canonical-set"),
            "facts": K.ordered([f["id"] for f in facts], "canonical-set"),
            "coverageIds": K.ordered([c["id"] for c in coverages], "canonical-set"),
            "producerClosure": producer_closure,
            "schemaDigests": K.ordered(list(schema_digests), "canonical-set")}
    vid, h = ident("view", desc)
    return {"id": vid, "hex": h, "desc": desc}


# --------------------------------------------------------------------------
# Policy, rule program, proof, evidence, seal, run.
# --------------------------------------------------------------------------
def make_policy(rule_id, message_code, atom, gate, severity):
    program_digest = K.raw_bytes_sha256(
        ("cb-rule-program:" + rule_id).encode())
    rule = {"ruleId": rule_id,
            "ruleProgramRef": {"contributionId": "cb-blind-consumer",
                               "ruleStableId": rule_id, "semanticsMajor": 1,
                               "programDigest": program_digest},
            "enabled": True, "severity": severity, "gate": gate,
            "subjectEnumeration": {"universe": "cb-universe",
                                   "subjectKind": "file"},
            "emitWhen": atom, "evidenceUse": [], "messageCode": message_code}
    policy = {"schemaFamily": "opensip.product.policy", "schemaMajor": 1,
              "gateSeverityAtLeast": "error",
              "rules": K.ordered([rule], "ruleId")}
    policy_digest = retain_record(policy)
    program = {"schemaVersion": 1, "policyDigest": policy_digest,
               "rules": K.ordered([{"ruleId": rule["ruleId"],
                                    "ruleProgramRef": rule["ruleProgramRef"],
                                    "emitWhen": rule["emitWhen"]}], "ruleId")}
    program_digest2 = retain_record(program)
    waivers = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1,
               "waivers": []}
    return {"policy": policy, "policyDigest": policy_digest,
            "program": program, "ruleProgramDigest": program_digest2,
            "waivers": waivers, "waiverDigest": retain_record(waivers),
            "rule": rule}


def address_node(root, address):
    """Total, deterministic node addressing (identity section 3 program-predicate)."""
    node = root
    parts = address.split(".")
    if parts[0] != "p":
        raise K.Refusal("PREDICATE_ADDRESS_ROOT")
    for step in parts[1:]:
        i = int(step)
        if node["op"] == "not":
            if i != 0:
                raise K.Refusal("PREDICATE_ADDRESS_NOT_OPERAND")
            node = node["operand"]
        elif node["op"] in ("and", "or"):
            node = node["operands"][i]
        else:
            raise K.Refusal("PREDICATE_ADDRESS_INTO_ATOM")
    return node


def make_predicate_proof(pol, rule_id, subject_id, address, value, facts,
                         coverages, children=()):
    node = address_node(pol["rule"]["emitWhen"], address)
    pp = {"schemaVersion": 2, "ruleProgramDigest": pol["ruleProgramDigest"],
          "ruleId": rule_id, "predicateId": address, "operation": node["op"],
          "nodeDigest": retain_record(node)}
    witness = {"schemaVersion": 2, "programPredicateDigest": retain_record(pp),
               "matchingFactIds": K.ordered([f["id"] for f in facts], "canonical-set"),
               "coverageIds": K.ordered([c["id"] for c in coverages], "canonical-set"),
               "countLimit": node.get("n") if node["op"] == "count-at-most" else None,
               "childPredicateIds": K.ordered(list(children), "canonical-set")}
    return {"ruleId": rule_id, "subjectId": subject_id, "predicateId": address,
            "operation": node["op"],
            "inputRefs": [], "scopeIds": K.ordered(
                [c["scope"]["id"] for c in coverages], "canonical-set"),
            "value": value, "witnessDigest": retain_record(witness)}, witness


def make_finding(pol, subject_key, message_code, parameters, severity,
                 evidence_refs):
    fp_desc = {"schemaVersion": 2,
               "ruleStableId": pol["rule"]["ruleProgramRef"]["ruleStableId"],
               "detectorSemanticsMajor": pol["rule"]["ruleProgramRef"]["semanticsMajor"],
               "subjectKey": subject_key, "relatedSubjectKeys": []}
    fp_id, _ = ident("finding-fingerprint", fp_desc)
    params = {"schemaVersion": 2, "messageCode": message_code,
              "parameters": parameters}
    desc = {"schemaVersion": 2, "fingerprint": fp_id,
            "ruleClosure": CL_DETECTOR["id"],
            "subjectId": subject_key["qualifiedName"],
            "messageCode": message_code,
            "parameterDigest": retain_record(params), "severity": severity,
            "evidenceRefs": K.ordered(list(evidence_refs), "canonical-set")}
    fid, h = ident("finding", desc)
    return {"id": fid, "hex": h, "desc": desc, "fingerprint": fp_id,
            "fingerprintDesc": fp_desc, "parameters": params}


def discriminator(tokens):
    """raw SHA256 of the canonical JSON ORDERED string array of declaration-
    signature tokens (grammar order, repeated tokens retained)."""
    return K.raw_sha256(list(tokens))


def make_execution_plan(plan_id, stages):
    desc = {"schemaVersion": 2, "planId": plan_id,
            "stages": K.ordered(stages, "ordinal")}
    eid, h = ident("execution-plan", desc)
    return {"id": eid, "hex": h, "desc": desc}


def make_stage_spec(plan_id, producer_closure, operation, parameters,
                    output_domains, output_schema_digest):
    spec = {"schemaVersion": 2, "planId": plan_id,
            "producerClosure": producer_closure, "operation": operation,
            "parameters": K.ordered(parameters, "canonical-set"),
            "outputDomains": K.ordered(list(output_domains), "canonical-set"),
            "outputSchemaDigest": output_schema_digest}
    return spec, retain_record(spec)


# ==========================================================================
# GRAPH 1: RUN-TS
# ==========================================================================
def build_ts_run():
    repo = Repo("prj1-" + "7a" * 32)
    # --- app/: ordinary tsconfig project that reads node_modules -----------
    repo.add("app/base.a.json", '{"compilerOptions":{"strict":true}}')
    repo.add("app/package.json", '{"name":"cb-app","private":true,"version":"0.1.0"}')
    repo.add("app/pnpm-lock.yaml", "lockfileVersion: '9.0'\n")
    repo.add("app/src/legacy.js",
             "'use strict';\nfunction legacyAdd(a, b) {\n  return a + b;\n}\n"
             "module.exports = { legacyAdd };\n")
    repo.add("app/src/one.ts",
             "import { pad } from 'left-pad';\n\n"
             "export function add(a: number, b: number): number {\n"
             "  return a + b;\n}\n")
    repo.add("app/tsconfig.json",
             '{"extends":["./base.a.json"],"compilerOptions":{"module":"node16"}}')
    # --- custom/: explicitly selected custom-named config, repeated bases ---
    repo.add("custom/config/base.x.json", '{"compilerOptions":{"strict":false}}')
    repo.add("custom/config/base.y.json", '{"compilerOptions":{"target":"es2022"}}')
    repo.add("custom/src/c.ts", "export const c = 1;\n")
    repo.add("custom/tools/opensip.tsconfig.custom.json",
             '{"extends":["../config/base.x.json","../config/base.y.json",'
             '"../config/base.x.json"]}')
    # --- jsproj/: jsconfig inheriting a shared base with another filename ---
    repo.add("jsproj/jsconfig.json", '{"extends":["./shared/common-base.json"]}')
    repo.add("jsproj/shared/common-base.json", '{"compilerOptions":{"checkJs":true}}')
    repo.add("jsproj/src/j.mjs", "export const j = 2;\n")
    # --- synth/: no tsconfig or jsconfig, package.json present --------------
    repo.add("synth/package.json", '{"name":"cb-synth","version":"0.0.1"}')
    repo.add("synth/src/s.js", "module.exports = 3;\n")

    scope, scope_digest = scope_descriptor(
        ["app", "custom", "jsproj", "synth"], ["."],
        ["app/node_modules", "custom/node_modules", "jsproj/node_modules",
         "synth/node_modules", ".git"])
    cfg, cfg_digest = semantic_configuration(
        "default", ["clones", "declares", "file", "imports", "references", "types"],
        1000000)
    snap = repo.snapshot(scope_digest, cfg_digest, "a1" * 20)
    inv_paths = {r["path"] for r in snap["inventory"]}
    inv_digests = {r["path"]: r["sha256"] for r in snap["inventory"]}

    # node_modules layout: NOT snapshot inventory rows (pruned by segment);
    # retained resolution read-set observation joined by digest.
    nm = {}
    for path, manifest in (
            ("app/node_modules/left-pad",
             '{"name":"left-pad","version":"1.3.0"}'),
            ("app/node_modules/@acme/ui",
             '{"name":"@acme/ui","version":"1.2.3"}'),
            ("app/node_modules/.store/ui@1.2.3/node_modules/@acme/ui",
             '{"name":"@acme/ui","version":"1.2.3"}')):
        nm[path] = retain_blob(manifest.encode())
    layout = {"schemaVersion": 1, "entries": K.ordered([
        {"packageName": "@acme/ui", "packageVersion": "1.2.3",
         "installPath": "app/node_modules/@acme/ui",
         "realPath": "app/node_modules/.store/ui@1.2.3/node_modules/@acme/ui",
         "contentSha256": nm["app/node_modules/@acme/ui"]},
        {"packageName": "@acme/ui", "packageVersion": "1.2.3",
         "installPath": "app/node_modules/.store/ui@1.2.3/node_modules/@acme/ui",
         "realPath": "app/node_modules/.store/ui@1.2.3/node_modules/@acme/ui",
         "contentSha256": nm["app/node_modules/.store/ui@1.2.3/node_modules/@acme/ui"]},
        {"packageName": "left-pad", "packageVersion": "1.3.0",
         "installPath": "app/node_modules/left-pad",
         "realPath": "app/node_modules/left-pad",
         "contentSha256": nm["app/node_modules/left-pad"]},
    ], {"by": ["installPath"]})}
    layout_digest = retain_record(layout)
    # realPath of a linked row must itself be an installPath of this layout.
    install_paths = {e["installPath"] for e in layout["entries"]}
    for e in layout["entries"]:
        if e["realPath"] != e["installPath"] and e["realPath"] not in install_paths:
            raise K.Refusal("native.node-modules-layout-realpath-unbound",
                            e["realPath"])

    stripped_common = [{"option": "outDir", "reason": "emits-output"},
                       {"option": "typeRoots",
                        "reason": "acquires-types-from-the-network"}]

    # TS-A ordinary project with node_modules and a bare specifier.
    ctx_a = ts_context(
        "ts-tsconfig", ts_honored(False, False), stripped_common,
        ["app/base.a.json", "app/tsconfig.json"], "node16", "commonjs",
        layout_digest,
        {"kind": "pnpm-lock", "path": "app/pnpm-lock.yaml",
         "contentSha256": inv_digests["app/pnpm-lock.yaml"]})
    graph_a, graph_a_digest = ts_config_graph("app/tsconfig.json", [
        {"path": "app/tsconfig.json",
         "contentSha256": inv_digests["app/tsconfig.json"], "kind": "tsconfig",
         "extendsResolved": ["app/base.a.json"]},
        {"path": "app/base.a.json",
         "contentSha256": inv_digests["app/base.a.json"], "kind": "tsconfig",
         "extendsResolved": []}])
    uni_a = ts_universe(ctx_a, graph_a, graph_a_digest, "ts-tsconfig", "commonjs",
                        False, False, ["app/src/one.ts"], [], "pnpm-lock", True)

    # TS-B synthesized configuration.
    synth_opts = {"allowJs": True, "checkJs": False, "module": "node16",
                  "moduleResolution": "node16", "target": "es2022",
                  "strict": False, "skipLibCheck": True, "types": [],
                  "noEmit": True}
    ctx_b = ts_context(
        "js-synthesized",
        ts_honored(True, False, module="node16", resolution="node16",
                   target="es2022"),
        stripped_common, [], "node16", "absent", None, None)
    ctx_b["desc"]["configProjection"]["honoredOptions"]["strict"] = False
    ctx_b["desc"]["configProjection"]["honoredOptions"]["types"] = []
    ctx_b["id"], ctx_b["hex"] = native_ident("native.context.typescript.v2",
                                             ctx_b["desc"])
    graph_b, graph_b_digest = ts_config_graph(None, [])
    uni_b = ts_universe(ctx_b, graph_b, graph_b_digest, "js-synthesized", "absent",
                        True, False, ["synth/src/s.js"], ["synth/src/s.js"],
                        "none", False, synthesized=synth_opts)

    # TS-C explicitly selected custom-named config, three ordered bases with a
    # repeated base whose precedence must be retained (later wins).
    ctx_c = ts_context(
        "ts-tsconfig", ts_honored(False, False), stripped_common,
        ["custom/config/base.x.json", "custom/config/base.y.json",
         "custom/tools/opensip.tsconfig.custom.json"],
        "node16", "absent", None, None)
    graph_c, graph_c_digest = ts_config_graph(
        "custom/tools/opensip.tsconfig.custom.json", [
            {"path": "custom/tools/opensip.tsconfig.custom.json",
             "contentSha256": inv_digests["custom/tools/opensip.tsconfig.custom.json"],
             "kind": "other",
             "extendsResolved": ["custom/config/base.x.json",
                                 "custom/config/base.y.json",
                                 "custom/config/base.x.json"]},
            {"path": "custom/config/base.x.json",
             "contentSha256": inv_digests["custom/config/base.x.json"],
             "kind": "tsconfig", "extendsResolved": []},
            {"path": "custom/config/base.y.json",
             "contentSha256": inv_digests["custom/config/base.y.json"],
             "kind": "tsconfig", "extendsResolved": []}])
    uni_c = ts_universe(ctx_c, graph_c, graph_c_digest, "ts-tsconfig", "absent",
                        False, False, ["custom/src/c.ts"], [], "none", False)

    # TS-D jsconfig inheriting a shared base with another filename.
    ctx_d = ts_context(
        "js-allowjs", ts_honored(True, True), stripped_common,
        ["jsproj/jsconfig.json", "jsproj/shared/common-base.json"],
        "node16", "module", None, None)
    graph_d, graph_d_digest = ts_config_graph("jsproj/jsconfig.json", [
        {"path": "jsproj/jsconfig.json",
         "contentSha256": inv_digests["jsproj/jsconfig.json"], "kind": "jsconfig",
         "extendsResolved": ["jsproj/shared/common-base.json"]},
        {"path": "jsproj/shared/common-base.json",
         "contentSha256": inv_digests["jsproj/shared/common-base.json"],
         "kind": "other", "extendsResolved": []}])
    uni_d = ts_universe(ctx_d, graph_d, graph_d_digest, "js-allowjs", "module",
                        True, True, ["jsproj/src/j.mjs"], ["jsproj/src/j.mjs"],
                        "none", False)

    contexts = [ctx_a, ctx_b, ctx_c, ctx_d]
    universes = [uni_a, uni_b, uni_c, uni_d]
    bindings = []
    for u in universes:
        bindings.append(bind_typescript_universe(u, u["ctx"], u["graph"],
                                                 inv_paths, inv_digests))

    # --- Plan ------------------------------------------------------------
    manifest = {
        "schemaVersion": 1, "profile": "default",
        "providers": [
            {"providerId": "typescript-semantic", "language": "typescript",
             "providerVersionSource": "signed-release-manifest",
             "toolchainIdentitySource": "native-context-typescript-v2",
             "relations": {"clones": "normalized-body-hash",
                           "declares": "syntactic", "file": "enumerated",
                           "imports": "resolved-target",
                           "references": "resolved-binding",
                           "types": "checked"},
             "platformIds": ["macos-aarch64"]}],
        "coverageForAbsent": [],
    }
    cm_id, committed = K.capability_manifest_id(manifest)
    cm_bytes_digest = retain_blob(committed)

    analysis_spec = {
        "schemaVersion": 2,
        "requestedCapabilities": K.ordered([
            {"capabilityId": "clones", "languageMode": "ts-tsconfig",
             "workspaceRoot": "app", "required": True},
            {"capabilityId": "file", "languageMode": "ts-tsconfig",
             "workspaceRoot": "app", "required": True},
            {"capabilityId": "declares", "languageMode": "ts-tsconfig",
             "workspaceRoot": "custom", "required": True},
            {"capabilityId": "clones", "languageMode": "js-allowjs",
             "workspaceRoot": "jsproj", "required": False},
        ], "canonical-set"),
        "policyPackIds": ["cb.blind.pack"], "parameters": []}
    analysis_spec_digest = retain_record(analysis_spec)

    grant = {"schemaVersion": 2, "projectId": repo.project_id,
             "principals": K.ordered([
                 {"kind": "first-party", "closureId": CL_TS_PROVIDER["id"],
                  "ownerSourceDigest": None}], "canonical-set"),
             "analysisOperations": K.ordered(["read-source", "native-analysis"],
                                             "canonical-set"),
             "scopeDigest": scope_digest}
    grant_digest = retain_record(grant)

    pol = make_policy("cb.file.present", "cb.file.present",
                      {"op": "exists", "relation": "file",
                       "minResolution": "syntax", "filters": []},
                      gate=False, severity="note")

    plan_desc = {
        "schemaVersion": 2, "snapshotId": snap["id"], "capabilityManifestId": cm_id,
        "semanticClosures": K.ordered(
            [CL_TS_PROVIDER["id"], CL_EVALUATOR["id"], CL_DETECTOR["id"],
             CL_TS_TOOLCHAIN["id"], CL_TS_STDLIB["id"]], "canonical-set"),
        "analysisSpecDigest": analysis_spec_digest,
        "resolvedConfigDigest": cfg_digest,
        "nativeContextDigests": K.ordered([c["hex"] for c in contexts],
                                          "canonical-set"),
        "importIds": [], "policyDigest": pol["policyDigest"],
        "waiverDigest": pol["waiverDigest"], "scopeDigest": scope_digest,
        "budget": {"unit": "work-units", "limit": 1000000},
        "semanticGrantDigest": grant_digest,
        "capabilityManifestBytesDigest": cm_bytes_digest}
    # identity section 3: the Plan budget must equal analysis.budget exactly.
    if plan_desc["budget"] != cfg["analysis"]["budget"]:
        raise K.Refusal("PLAN_BUDGET_CONTRADICTS_CONFIGURATION")
    plan_id, plan_hex = ident("plan", plan_desc)

    # --- Facts -----------------------------------------------------------
    one_ts = repo.files["app/src/one.ts"]
    legacy_js = repo.files["app/src/legacy.js"]
    c_ts = repo.files["custom/src/c.ts"]

    file_fact = make_fact(
        snap["id"], "file", "enumerated", uni_a["hex"], uni_a["hex"],
        CL_TS_PROVIDER["id"],
        {"path": "app/src/one.ts",
         "contentSha256": inv_digests["app/src/one.ts"],
         "byteLength": len(one_ts)},
        [{"path": "app/src/one.ts", "blobDigest": inv_digests["app/src/one.ts"],
          "startByte": 0, "endByte": len(one_ts)}])
    # file snapshotJoins, applied over the OWNING fact (identity section 3).
    apply_file_join(file_fact, snap, inv_digests)

    # TypeScript body, L0-verbatim.
    ts_span = (one_ts.index(b"{\n  return a + b;\n}"),
               one_ts.index(b"{\n  return a + b;\n}") + len(b"{\n  return a + b;\n}"))
    blv_ts, blv_ts_raw = ts_body_language_version(ctx_a, "app/src/one.ts")
    payload_ts, frame_ts, _ = clone_payload(
        "L0-verbatim", one_ts[ts_span[0]:ts_span[1]], None,
        blv_ts["languageId"], blv_ts_raw)
    clone_ts = make_fact(snap["id"], "clones", "normalized-body-hash",
                         uni_a["hex"], uni_a["hex"], CL_TS_PROVIDER["id"],
                         payload_ts,
                         [{"path": "app/src/one.ts",
                           "blobDigest": inv_digests["app/src/one.ts"],
                           "startByte": ts_span[0], "endByte": ts_span[1]}])

    # JavaScript body through the SAME TypeScript engine universe: the body
    # language is javascript, the provider identity is the TypeScript engine.
    js_span = (legacy_js.index(b"{\n  return a + b;\n}"),
               legacy_js.index(b"{\n  return a + b;\n}") + len(b"{\n  return a + b;\n}"))
    blv_js, blv_js_raw = ts_body_language_version(ctx_a, "app/src/legacy.js")
    payload_js, frame_js, _ = clone_payload(
        "L0-verbatim", legacy_js[js_span[0]:js_span[1]], None,
        blv_js["languageId"], blv_js_raw)
    clone_js = make_fact(snap["id"], "clones", "normalized-body-hash",
                         uni_a["hex"], uni_a["hex"], CL_TS_PROVIDER["id"],
                         payload_js,
                         [{"path": "app/src/legacy.js",
                           "blobDigest": inv_digests["app/src/legacy.js"],
                           "startByte": js_span[0], "endByte": js_span[1]}])

    # A normalized (L1) TypeScript body under the same universe.
    tokens = [("punc", "{"), ("kw", "return"), ("ident", "a"), ("op", "+"),
              ("ident", "b"), ("punc", ";"), ("punc", "}")]
    payload_ts_l1, frame_ts_l1, stream = clone_payload(
        "L1-lexical", None, tokens, blv_ts["languageId"], blv_ts_raw)
    clone_ts_l1 = make_fact(snap["id"], "clones", "normalized-body-hash",
                            uni_a["hex"], uni_a["hex"], CL_TS_PROVIDER["id"],
                            payload_ts_l1,
                            [{"path": "app/src/one.ts",
                              "blobDigest": inv_digests["app/src/one.ts"],
                              "startByte": ts_span[0], "endByte": ts_span[1]}])

    declares_fact = make_fact(
        snap["id"], "declares", "syntactic", uni_c["hex"], uni_c["hex"],
        CL_TS_PROVIDER["id"],
        {"container": "module:custom/src/c.ts", "declared": "symbol:custom/src/c.ts#c",
         "declarationKind": "variable"},
        [{"path": "custom/src/c.ts", "blobDigest": inv_digests["custom/src/c.ts"],
          "startByte": 0, "endByte": len(c_ts)}])

    # --- Scopes and Coverage ---------------------------------------------
    scope_file = make_scope(snap["id"], uni_a["hex"], uni_a["hex"], "file",
                            "enumerated", CL_TS_PROVIDER["id"],
                            ["file:app/src/legacy.js", "file:app/src/one.ts"])
    cov_file = make_coverage(scope_file, coverage_entry(
        "file", "enumerated", "complete", scope_file, "not-applicable", False,
        True, "complete", 0, []))

    scope_clone = make_scope(snap["id"], uni_a["hex"], uni_a["hex"], "clones",
                             "normalized-body-hash", CL_TS_PROVIDER["id"],
                             ["body:app/src/legacy.js#31-52",
                              "body:app/src/one.ts#83-104"])
    cov_clone = make_coverage(scope_clone, coverage_entry(
        "clones", "normalized-body-hash", "complete", scope_clone,
        "not-applicable", False, True, "complete", 0, []))

    scope_decl = make_scope(snap["id"], uni_c["hex"], uni_c["hex"], "declares",
                            "syntactic", CL_TS_PROVIDER["id"],
                            ["module:custom/src/c.ts"])
    cov_decl = make_coverage(scope_decl, coverage_entry(
        "declares", "syntactic", "complete", scope_decl, "not-applicable", False,
        True, "complete", 0, []))

    view = make_view(plan_id,
                     [scope_file, scope_clone, scope_decl],
                     [file_fact, clone_ts, clone_js, clone_ts_l1, declares_fact],
                     [cov_file, cov_clone, cov_decl],
                     CL_TS_PROVIDER["id"],
                     [DOC_DIGEST["relation"], DOC_DIGEST["native"]])

    return finish_run(
        name="RUN-TS", repo=repo, snap=snap, plan_desc=plan_desc, plan_id=plan_id,
        pol=pol, view=view, facts=[file_fact, clone_ts, clone_js, clone_ts_l1,
                                   declares_fact],
        coverages=[cov_file, cov_clone, cov_decl],
        subject_facts=[file_fact], subject_coverages=[cov_file],
        subject_key={"language": "typescript", "kind": "file",
                     "logicalPath": "app/src/one.ts",
                     "qualifiedName": "app/src/one.ts",
                     "discriminator": discriminator(
                         ["typescript", "file", "app/src/one.ts"])},
        value="true", verdict="pass", capability_manifest_id=cm_id,
        analysis_spec=analysis_spec, imports=[],
        extra={
            "contexts": {c["id"]: c["desc"] for c in contexts},
            "universes": {u["id"]: u["desc"] for u in universes},
            "configGraphs": [graph_a, graph_b, graph_c, graph_d],
            "nodeModulesLayout": layout,
            "bodyLanguageVersions": {"typescript-body": blv_ts,
                                     "javascript-body": blv_js},
            "cloneFrames": {
                clone_ts["payload"]["bodyIdentity"]: frame_ts.hex(),
                clone_js["payload"]["bodyIdentity"]: frame_js.hex(),
                clone_ts_l1["payload"]["bodyIdentity"]: frame_ts_l1.hex()},
            "l1TokenStreamHex": stream.hex(),
            "universeBindings": bindings,
        })


def apply_file_join(fact, snap, inv_digests):
    """relation `file` snapshotJoins, applied over the OWNING fact."""
    p = fact["payload"]
    row = next((r for r in snap["inventory"] if r["path"] == p["path"]), None)
    if row is None:
        raise K.Refusal("FILE_PATH_NOT_INVENTORIED", p["path"])
    if row["sha256"] != p["contentSha256"]:
        raise K.Refusal("FILE_CONTENT_DIGEST_MISMATCH", p["path"])
    if row["bytes"] != p["byteLength"]:
        raise K.Refusal("FILE_BYTE_LENGTH_MISMATCH", p["path"])
    if p["contentSha256"] not in BLOBS:
        raise K.Refusal("EVIDENCE_UNAVAILABLE", p["contentSha256"])
    if K.raw_bytes_sha256(BLOBS[p["contentSha256"]]) != p["contentSha256"]:
        raise K.Refusal("RETAINED_BLOB_REHASH_MISMATCH")
    for a in fact["desc"]["anchors"]:
        if a["path"] != p["path"]:
            raise K.Refusal("FILE_ANCHOR_OUTSIDE_CLAIMED_FILE", a["path"])
    return "ADMIT"


# ==========================================================================
# Shared tail: execution plan -> proof -> evidence -> seal -> Run.
# ==========================================================================
def finish_run(name, repo, snap, plan_desc, plan_id, pol, view, facts, coverages,
               subject_facts, subject_coverages, subject_key, value, verdict,
               capability_manifest_id, analysis_spec, imports, extra,
               provider_closure=None, emit_finding=True):
    provider_closure = provider_closure or CL_TS_PROVIDER["id"]
    stage_spec, stage_spec_digest = make_stage_spec(
        plan_id, provider_closure, "native.analyze",
        analysis_spec["parameters"], ["fact", "coverage", "subject-scope"],
        DOC_DIGEST["native"])
    exec_plan = make_execution_plan(plan_id, [
        {"ordinal": 0, "stageSpecDigest": stage_spec_digest, "requires": [],
         "outputDomains": K.ordered(["coverage", "fact", "subject-scope"],
                                    "canonical-set")}])

    proof_pred, witness = make_predicate_proof(
        pol, pol["rule"]["ruleId"], subject_key["qualifiedName"], "p", value,
        subject_facts, subject_coverages)

    findings = []
    if emit_finding and value == "true":
        ev_refs = [{"domain": "fact", "digest": f["hex"]} for f in subject_facts]
        ev_refs += [{"domain": "coverage", "digest": c["hex"]}
                    for c in subject_coverages]
        ev_refs += [{"domain": "predicate-witness",
                     "digest": retain_record(witness)}]
        findings.append(make_finding(
            pol, subject_key, pol["rule"]["messageCode"],
            {"path": subject_key["logicalPath"]}, pol["rule"]["severity"],
            ev_refs))

    input_refs = K.ordered(
        [{"domain": "view", "digest": view["hex"]}]
        + [{"domain": "coverage", "digest": c["hex"]} for c in coverages]
        + [{"domain": "rule-program", "digest": pol["ruleProgramDigest"]},
           {"domain": "policy", "digest": pol["policyDigest"]},
           {"domain": "waiver", "digest": pol["waiverDigest"]},
           {"domain": "schema", "digest": DOC_DIGEST["relation"]},
           {"domain": "schema", "digest": DOC_DIGEST["native"]},
           {"domain": "configuration", "digest": plan_desc["resolvedConfigDigest"]},
           {"domain": "analysis-spec", "digest": plan_desc["analysisSpecDigest"]},
           {"domain": "capability-manifest", "digest": capability_manifest_id}]
        + [{"domain": "native-context", "digest": d}
           for d in plan_desc["nativeContextDigests"]]
        + [{"domain": "import", "digest": i["hex"]} for i in imports],
        "canonical-set")

    proof_desc = {"schemaVersion": 2, "planId": plan_id,
                  "executionPlanId": exec_plan["id"],
                  "evaluatorClosure": CL_EVALUATOR["id"],
                  "ruleProgramDigest": pol["ruleProgramDigest"],
                  "evaluationInputRefs": input_refs,
                  "predicateProofs": K.ordered([proof_pred], "predicate"),
                  "findingIds": K.ordered([f["id"] for f in findings],
                                          "canonical-set"),
                  "verdict": verdict}
    proof_id, proof_hex = ident("proof-bundle", proof_desc)

    evidence_desc = {"schemaVersion": 2, "planId": plan_id,
                     "viewIds": [view["id"]],
                     "coverageIds": K.ordered([c["id"] for c in coverages],
                                              "canonical-set"),
                     "importIds": K.ordered([i["id"] for i in imports],
                                            "canonical-set"),
                     "findingIds": K.ordered([f["id"] for f in findings],
                                             "canonical-set"),
                     "proofBundleId": proof_id}
    evidence_id, evidence_hex = ident("semantic-evidence", evidence_desc)

    seal_desc = {"schemaVersion": 2, "planId": plan_id,
                 "executionPlanId": exec_plan["id"], "evidenceId": evidence_id,
                 "evaluatorClosure": CL_EVALUATOR["id"],
                 "policyDigest": pol["policyDigest"], "proofBundleId": proof_id,
                 "verdict": verdict}
    seal_id, seal_hex = ident("evaluation-seal", seal_desc)

    run_desc = {"schemaVersion": 2, "projectId": repo.project_id,
                "snapshotId": snap["id"], "planId": plan_id,
                "evidenceId": evidence_id, "evaluationSealId": seal_id,
                "capabilityManifestId": capability_manifest_id}
    run_id, run_hex = ident("run", run_desc)

    # Acyclicity, checked rather than asserted: proof carries no evidence/seal/
    # Run reference, evidence carries proof, seal carries both, Run carries seal.
    for forbidden in (evidence_id, seal_id, run_id):
        if forbidden in K.C(proof_desc).decode():
            raise K.Refusal("PROOF_CITES_A_LATER_NODE", forbidden)
    if proof_id not in K.C(evidence_desc).decode():
        raise K.Refusal("EVIDENCE_MISSING_PROOF")

    # Citation closure (identity section 3): every finding citation must be a
    # fact/Coverage of an evaluated view, a Plan-selected import listed in
    # evaluationInputRefs, a witness of this proof, or an explicit blob input.
    view_facts = set(view["desc"]["facts"])
    view_cov = set(view["desc"]["coverageIds"])
    witness_digests = {retain_record(witness)}
    for f in findings:
        for ref in f["desc"]["evidenceRefs"]:
            if ref["domain"] == "fact" and f"fact2:{ref['digest']}" not in view_facts:
                raise K.Refusal("HIDDEN_FINDING_EVIDENCE", "fact")
            if ref["domain"] == "coverage" and \
                    f"coverage2:{ref['digest']}" not in view_cov:
                raise K.Refusal("HIDDEN_FINDING_EVIDENCE", "coverage")
            if ref["domain"] == "predicate-witness" and \
                    ref["digest"] not in witness_digests:
                raise K.Refusal("HIDDEN_FINDING_EVIDENCE", "predicate-witness")

    return {
        "name": name,
        "runId": run_id, "sealId": seal_id, "evidenceId": evidence_id,
        "proofId": proof_id, "planId": plan_id, "snapshotId": snap["id"],
        "executionPlanId": exec_plan["id"], "viewId": view["id"],
        "verdict": verdict,
        "descriptors": {
            "snapshot": snap["desc"], "plan": plan_desc,
            "executionPlan": exec_plan["desc"], "view": view["desc"],
            "proofBundle": proof_desc, "semanticEvidence": evidence_desc,
            "evaluationSeal": seal_desc, "run": run_desc,
            "stageSpec": stage_spec, "predicateWitness": witness,
            "analysisSpec": analysis_spec, "policy": pol["policy"],
            "ruleProgram": pol["program"], "waiverSet": pol["waivers"],
            "vcsObservation": snap["vcs"],
        },
        "facts": {f["id"]: f["desc"] for f in facts},
        "factPayloads": {f["id"]: f["payload"] for f in facts},
        "scopes": {c["scope"]["id"]: c["scope"]["desc"] for c in coverages},
        "coverages": {c["id"]: c["desc"] for c in coverages},
        "coveragePayloads": {c["id"]: c["payload"] for c in coverages},
        "findings": {f["id"]: f["desc"] for f in findings},
        "findingFingerprints": {f["fingerprint"]: f["fingerprintDesc"]
                                for f in findings},
        "findingParameters": {f["id"]: f["parameters"] for f in findings},
        "imports": {i["id"]: i["desc"] for i in imports},
        "extra": extra,
    }


# ==========================================================================
# GRAPH 2 and 3: Rust.
# ==========================================================================
LARGE_CRATES = ["cb-core", "cb-legacy", "cb-tools"] + [
    "cb-crate-%02d" % i for i in range(1, 19)]          # 21 crates total


def rust_common(repo_project_id, ownership_selection, enumeration="complete",
                extra_units=None):
    repo = Repo(repo_project_id)
    repo.add(".cargo/config.toml", "[build]\ntarget = \"aarch64-apple-darwin\"\n")
    repo.add("Cargo.lock", "version = 4\n\n[[package]]\nname = \"cb-core\"\n")
    repo.add("Cargo.toml", "[workspace]\nmembers = [\"crates/*\"]\n")
    repo.add("crates/core/.cargo/config.toml", "[build]\nrustflags = []\n")
    repo.add("crates/core/Cargo.toml",
             "[package]\nname = \"cb-core\"\nedition = \"2021\"\n")
    repo.add("crates/core/src/lib.rs", "pub mod shared;\n")
    repo.add("crates/core/src/shared.rs",
             "pub fn add(a: i32, b: i32) -> i32 {\n    a + b\n}\n")
    repo.add("crates/legacy#2015/Cargo.toml",
             "[package]\nname = \"cb-legacy\"\nedition = \"2015\"\n")
    repo.add("crates/legacy#2015/src/lib.rs", "pub fn old() -> i32 { 1 }\n")
    repo.add("crates/tools/Cargo.toml",
             "[package]\nname = \"cb-tools\"\nedition = \"2024\"\n")
    repo.add("crates/tools/src/main.rs", "fn main() {}\n")
    for c in LARGE_CRATES[3:]:
        repo.add("crates/%s/Cargo.toml" % c,
                 "[package]\nname = \"%s\"\nedition = \"2021\"\n" % c)
        repo.add("crates/%s/src/lib.rs" % c, "pub fn f() {}\n")

    scope, scope_digest = scope_descriptor(
        ["."], ["."], [".git", "target", "crates/core/target"])
    cfg, cfg_digest = semantic_configuration(
        "default", ["clones", "file"], 2000000)
    snap = repo.snapshot(scope_digest, cfg_digest, "b2" * 20)
    inv_digests = {r["path"]: r["sha256"] for r in snap["inventory"]}
    inv_paths = set(inv_digests)

    # --- nested semantic records, each an H identity over a retained frame ---
    manifest_rows = K.ordered([
        {"path": "src/lib.rs", "contentSha256": retain_blob(b"pub fn dep() {}\n"),
         "byteLength": len(b"pub fn dep() {}\n")},
        {"path": "Cargo.toml",
         "contentSha256": retain_blob(b"[package]\nname = \"serde_lite\"\n"),
         "byteLength": len(b"[package]\nname = \"serde_lite\"\n")},
    ], "path")
    fm_id, fm_hex = native_ident("native.dependency-file-manifest.v1", manifest_rows)
    tarball = b"cb-synthetic-crate-tarball-bytes"
    tarball_sha = retain_blob(tarball)
    dep_set = {
        "schemaVersion": 1, "language": "rust",
        "lockfileIdentity": {"path": "Cargo.lock",
                             "contentSha256": inv_digests["Cargo.lock"],
                             "lockfileVersion": 4},
        "packages": K.ordered([
            {"name": "serde_lite", "version": "1.0.0", "sourceKind": "registry",
             "sourceId": "registry+https://example.invalid/index",
             "lockChecksum": tarball_sha, "fileManifestSha256": fm_hex,
             "fileCount": len(manifest_rows),
             "totalBytes": sum(r["byteLength"] for r in manifest_rows),
             "acquisition": {"mode": "imported-descriptor", "descriptorId": None,
                             "vendorPath": None},
             "checksumVerification": "tarball-matched",
             "provenanceAssurance": "registry-authenticated"}],
            {"by": ["name", "version", "sourceId"]}),
        "completeness": {"state": "complete", "missing": []}}
    dep_id, dep_hex = native_ident("native.dependency-source-set.v1", dep_set)

    uf = {"schemaVersion": 1, "resolverVersion": 2,
          "targetTriple": "aarch64-apple-darwin",
          "activated": [{"packageKey": "serde_lite 1.0.0", "features": ["std"]}],
          "computedBy": {"producer": "opensip-cargo-adapter",
                         "producerBuildId": "cb-blind-1"}}
    uf_id, uf_hex = native_ident("native.unified-features.rust.v1", uf)

    projected_config = b"[build]\ntarget = \"aarch64-apple-darwin\"\nrustflags = []\n"
    ccp = {
        "schemaVersion": 2,
        "honoredKeys": ["build.target", "build.rustflags"],
        "strippedKeys": ["build.rustc", "target.*.linker", "net"],
        "replacedSnapshotConfigs": K.ordered(
            [".cargo/config.toml", "crates/core/.cargo/config.toml"], "utf8"),
        "rustflags": {"honored": ["--cfg=cb_blind"],
                      "stripped": [{"flag": "-C linker=cc",
                                    "reason": "codegen-option-not-allowlisted"}],
                      "executableSelected": False},
        "ancestorCarrierVerified": True, "cargoHome": "private-empty",
        "environmentProjection": "none", "claimsCargoSwitch": False,
        "projectionSha256": retain_blob(projected_config)}
    ccp_id, ccp_hex = native_ident("native.cargo-config-projection.v2", ccp)

    # --- the compilation-target ownership relation and its selection --------
    units = []
    u_core_lib = K.unit_id("crates/core/Cargo.toml", "lib", "cb_core")
    u_core_test = K.unit_id("crates/core/Cargo.toml", "test", "shared_it")
    u_legacy = K.unit_id("crates/legacy#2015/Cargo.toml", "lib", "cb_legacy")
    u_tools = K.unit_id("crates/tools/Cargo.toml", "bin", "cb-tools")
    units = [
        {"unitId": u_core_lib[0], "markerPath": "crates/core/Cargo.toml",
         "crateName": "cb-core", "targetKind": "lib", "targetName": "cb_core",
         "targetEdition": None},                      # defers to package 2021
        {"unitId": u_core_test[0], "markerPath": "crates/core/Cargo.toml",
         "crateName": "cb-core", "targetKind": "test", "targetName": "shared_it",
         "targetEdition": 2015},                      # target OVERRIDES package
        {"unitId": u_legacy[0], "markerPath": "crates/legacy#2015/Cargo.toml",
         "crateName": "cb-legacy", "targetKind": "lib", "targetName": "cb_legacy",
         "targetEdition": None},
        {"unitId": u_tools[0], "markerPath": "crates/tools/Cargo.toml",
         "crateName": "cb-tools", "targetKind": "bin", "targetName": "cb-tools",
         "targetEdition": None},
    ]
    if extra_units:
        units = units + extra_units
    ownership_rows = [
        {"path": "crates/core/src/lib.rs", "unitId": u_core_lib[0]},
        {"path": "crates/core/src/shared.rs", "unitId": u_core_lib[0]},
        {"path": "crates/core/src/shared.rs", "unitId": u_core_test[0]},
        {"path": "crates/legacy#2015/src/lib.rs", "unitId": u_legacy[0]},
        {"path": "crates/tools/src/main.rs", "unitId": u_tools[0]},
    ]
    ownership = {"schemaVersion": 1, "enumeration": enumeration,
                 "units": K.ordered(units, {"by": ["unitId"]}),
                 "selectedUnitIds": K.ordered(list(ownership_selection), "utf8"),
                 "ownership": K.ordered(ownership_rows, {"by": ["path", "unitId"]})}
    own_id, own_hex = native_ident("native.source-unit-ownership.v1", ownership)
    for u in ownership["units"]:
        if K.unit_id(u["markerPath"], u["targetKind"], u["targetName"])[0] != u["unitId"]:
            raise K.Refusal("sourceUnitOwnership.unitId", u["unitId"])
        if u["markerPath"] not in inv_paths:
            raise K.Refusal("OWNERSHIP_MARKER_NOT_INVENTORIED", u["markerPath"])
    for r in ownership["ownership"]:
        if r["path"] not in inv_paths:
            raise K.Refusal("OWNERSHIP_PATH_NOT_INVENTORIED", r["path"])

    ctx = {
        "schemaVersion": 2, "targetTriple": "aarch64-apple-darwin",
        "hostTriple": "aarch64-apple-darwin",
        "toolchain": {
            "rustCommitHash": "c" * 40, "rustcVersion": "1.83.0",
            "cargoVersion": "1.83.0",
            "sysrootDigest": retain_blob(b"cb-synthetic-sysroot-manifest"),
            "rustcDevLlvmDigest": CL_RS_LLVM["hex"],
            "standardLibraryComponentDigests": [
                {"component": "libstd", "sha256": retain_blob(b"cb-synthetic-libstd")}],
            "targetTriple": "aarch64-apple-darwin"},
        "toolClosure": {
            "rustc": next(r["sha256"] for r in CL_RS_TOOLCHAIN["tree"]
                          if r["path"] == "bin/rustc"),
            "cargo": next(r["sha256"] for r in CL_RS_TOOLCHAIN["tree"]
                          if r["path"] == "bin/cargo"),
            "linker": next(r["sha256"] for r in CL_RS_TOOLCHAIN["tree"]
                           if r["path"] == "bin/ld"),
            "ar": next(r["sha256"] for r in CL_RS_TOOLCHAIN["tree"]
                       if r["path"] == "bin/ar"),
            "procMacroServer": next(r["sha256"] for r in CL_RS_TOOLCHAIN["tree"]
                                    if r["path"] == "bin/proc-macro-srv"),
            "closureId": CL_RS_TOOLCHAIN["id"]},
        "baseCfg": ["target_arch=\"aarch64\"", "target_os=\"macos\""],
        "resolverVersion": 2, "dependencySourceSetId": dep_id,
        "unifiedFeaturesId": uf_id, "preparedOutputSetId": None,
        "configProjection": ccp}
    ctx_id, ctx_hex = native_ident("native.context.rust.v2", ctx)

    edition_map = {c: 2021 for c in LARGE_CRATES}
    edition_map["cb-legacy"] = 2015
    edition_map["cb-tools"] = 2024

    universe = {
        "schemaVersion": 2, "edition": edition_map,
        "lockfileIdentity": ctx["dependencySourceSetId"] and dep_set["lockfileIdentity"],
        "dependencySourceSetId": dep_id, "unifiedFeaturesId": uf_id,
        "nativeContextId": ctx_id,
        "cfgSets": [{"cfgSetId": "primary", "cfg": ctx["baseCfg"]},
                    {"cfgSetId": "primary+test",
                     "cfg": ctx["baseCfg"] + ["test"]}],
        "rustflags": ccp["rustflags"],
        "crateRootPaths": K.ordered(
            ["crates/core/src/lib.rs", "crates/legacy#2015/src/lib.rs",
             "crates/tools/src/main.rs"]
            + ["crates/%s/src/lib.rs" % c for c in LARGE_CRATES[3:]], "utf8"),
        "configProjectionSha256": ccp_hex,
        "executionCapableResolution": False, "preparedOutputSetId": None,
        "preparedResolution": "none", "sourceUnitOwnershipId": own_id}
    uni_id, uni_hex = native_ident("native.semantic-universe.rust.v2", universe)

    bind_rust_universe(universe, ctx, dep_set, uf, ownership, inv_digests)
    return {"repo": repo, "snap": snap, "inv": inv_digests, "scopeDigest": scope_digest,
            "cfg": cfg, "cfgDigest": cfg_digest, "ctx": ctx, "ctxId": ctx_id,
            "ctxHex": ctx_hex, "universe": universe, "uniId": uni_id,
            "uniHex": uni_hex, "ownership": ownership, "ownId": own_id,
            "depSet": dep_set, "depId": dep_id, "unifiedFeatures": uf,
            "ufId": uf_id, "configProjection": ccp, "ccpHex": ccp_hex,
            "fileManifest": manifest_rows, "fileManifestHex": fm_hex,
            "editionMap": edition_map, "tarballSha": tarball_sha}


def bind_rust_universe(u, ctx, dep_set, uf, ownership, inv_digests):
    """Reconstructed from native section 2.1 bind_rust_universe."""
    if ctx is None or dep_set is None or uf is None:
        raise K.Refusal("native.universe-retained-inputs-not-supplied")
    if u["nativeContextId"] != "sha256:" + K.H("native.context.rust.v2", ctx):
        raise K.Refusal("native.universe-context-binding-mismatch")
    for f in ("dependencySourceSetId", "unifiedFeaturesId", "preparedOutputSetId"):
        if u[f] != ctx[f]:
            raise K.Refusal("native.universe-context-field-mismatch", f)
    if u["rustflags"] != ctx["configProjection"]["rustflags"]:
        raise K.Refusal("native.universe-context-field-mismatch", "rustflags")
    if u["configProjectionSha256"] != K.H("native.cargo-config-projection.v2",
                                          ctx["configProjection"]):
        raise K.Refusal("native.universe-context-field-mismatch",
                        "configProjectionSha256")
    if u["executionCapableResolution"] != (u["preparedResolution"] != "none"):
        raise K.Refusal("native.universe-context-field-mismatch",
                        "executionCapableResolution")
    base = set(ctx["baseCfg"])
    seen = set()
    for s in u["cfgSets"]:
        if not base.issubset(set(s["cfg"])):
            raise K.Refusal("native.universe-cfg-set-drops-base-cfg", s["cfgSetId"])
        if s["cfgSetId"] in seen:
            raise K.Refusal("native.universe-cfg-set-id-repeated", s["cfgSetId"])
        seen.add(s["cfgSetId"])
    if u["dependencySourceSetId"] != "sha256:" + K.H(
            "native.dependency-source-set.v1", dep_set):
        raise K.Refusal("native.nested-identity-mismatch", "dependencySourceSet")
    if u["unifiedFeaturesId"] != "sha256:" + K.H("native.unified-features.rust.v1", uf):
        raise K.Refusal("native.nested-identity-mismatch", "unifiedFeatures")
    if uf["targetTriple"] != ctx["targetTriple"] or \
            uf["resolverVersion"] != ctx["resolverVersion"]:
        raise K.Refusal("native.unified-features-contradicts-context")
    if dep_set["lockfileIdentity"] != u["lockfileIdentity"]:
        raise K.Refusal("native.dependency-set-lockfile-mismatch")
    lf = u["lockfileIdentity"]
    if inv_digests.get(lf["path"]) != lf["contentSha256"]:
        raise K.Refusal("native.lockfile-outside-snapshot", lf["path"])
    for p in u["crateRootPaths"]:
        if p not in inv_digests:
            raise K.Refusal("native.crate-root-outside-snapshot", p)
    for p in ctx["configProjection"]["replacedSnapshotConfigs"]:
        if p not in inv_digests:
            raise K.Refusal("native.replaced-config-outside-snapshot", p)
    if u["sourceUnitOwnershipId"] is not None:
        if u["sourceUnitOwnershipId"] != "sha256:" + K.H(
                "native.source-unit-ownership.v1", ownership):
            raise K.Refusal("native.nested-identity-mismatch", "sourceUnitOwnership")
        declared = {x["unitId"] for x in ownership["units"]}
        for s in ownership["selectedUnitIds"]:
            if s not in declared:
                raise K.Refusal("native.ownership-selection-undeclared-unit", s)
        for r in ownership["ownership"]:
            if r["unitId"] not in declared:
                raise K.Refusal("native.ownership-row-undeclared-unit", r["unitId"])
        for x in ownership["units"]:
            if x["targetEdition"] is None and x["crateName"] not in u["edition"]:
                raise K.Refusal("native.ownership-deferring-unit-crate-not-in-edition-map",
                                x["crateName"])
    return "ADMIT"


def build_rust_run(name, selection, enumeration="complete", clone_paths=None,
                   partial_mode=False):
    """Build a complete Rust Run under one explicit compilation-target selection."""
    ctxdata = rust_common("prj1-" + "5c" * 32, selection, enumeration=enumeration)
    repo, snap, inv = ctxdata["repo"], ctxdata["snap"], ctxdata["inv"]
    ctx, universe = ctxdata["ctx"], ctxdata["universe"]
    uni_hex = ctxdata["uniHex"]
    ownership = ctxdata["ownership"]

    manifest = {
        "schemaVersion": 1, "profile": "default",
        "providers": [
            {"providerId": "rust-semantic", "language": "rust",
             "providerVersionSource": "signed-release-manifest",
             "toolchainIdentitySource": "native-context-rust-v2",
             "relations": {"clones": "normalized-body-hash", "file": "enumerated"},
             "platformIds": ["macos-aarch64"]}],
        "coverageForAbsent": []}
    cm_id, committed = K.capability_manifest_id(manifest)
    cm_bytes_digest = retain_blob(committed)

    # An admitted dependency import2, so the Plan carries a real import payload
    # and read-import must appear in the semantic grant.
    payload = {"schemaVersion": 1, "payloadDomain":
               "native.import-payload.dependency-source.v1",
               "set": ctxdata["depSet"],
               "acquisitionSourcePath": "vendor/serde_lite-1.0.0.crate",
               "tarballDigests": [{"packageKey": "serde_lite 1.0.0",
                                   "crateTarballSha256": ctxdata["tarballSha"]}]}
    correspondence = {"kind": "exact-snapshot", "snapshotId": snap["id"]}
    build_identity = {"schemaVersion": 1, "buildIdentity": None}
    observation = {"schemaVersion": 1, "kind": "dependency", "window": None,
                   "population": None, "selection": None, "revisionRange": None}
    import_scope, import_scope_digest = scope_descriptor(
        ["."], ["."], [".git", "target", "crates/core/target"])
    imp_desc = {
        "schemaVersion": 2, "kind": "dependency",
        "payloadSchemaDigest": DOC_DIGEST["native"],
        "payloadDigest": retain_record(payload),
        "sourceCorrespondenceDigest": retain_record(correspondence),
        "buildDigest": retain_record(build_identity),
        "producerClosure": CL_ADAPTER["id"], "adapterClosure": CL_ADAPTER["id"],
        "blobs": K.ordered([{"path": "vendor/serde_lite-1.0.0.crate",
                             "sha256": ctxdata["tarballSha"],
                             "bytes": len(BLOBS[ctxdata["tarballSha"]])}], "path"),
        "scopeDigest": import_scope_digest,
        "observationDigest": retain_record(observation),
        "completeness": "complete", "omissions": []}
    imp_id, imp_hex = ident("import", imp_desc)
    imports = [{"id": imp_id, "hex": imp_hex, "desc": imp_desc,
                "payload": payload}]

    analysis_spec = {
        "schemaVersion": 2,
        "requestedCapabilities": K.ordered([
            {"capabilityId": "clones", "languageMode": "rust-cargo",
             "workspaceRoot": ".", "required": True},
            {"capabilityId": "file", "languageMode": "rust-cargo",
             "workspaceRoot": ".", "required": True}], "canonical-set"),
        "policyPackIds": ["cb.blind.pack"], "parameters": []}
    analysis_spec_digest = retain_record(analysis_spec)

    grant = {"schemaVersion": 2, "projectId": repo.project_id,
             "principals": K.ordered([
                 {"kind": "first-party", "closureId": CL_RS_PROVIDER["id"],
                  "ownerSourceDigest": None}], "canonical-set"),
             # read-import is required because the Plan selects an import2.
             "analysisOperations": K.ordered(
                 ["read-source", "read-import", "native-analysis"], "canonical-set"),
             "scopeDigest": ctxdata["scopeDigest"]}
    grant_digest = retain_record(grant)

    atom = ({"op": "exists", "relation": "clones", "minResolution": "syntax",
             "filters": []} if not partial_mode else
            {"op": "all-covered", "relation": "clones", "minResolution": "syntax",
             "filters": []})
    pol = make_policy("cb.clone.present", "cb.clone.present", atom,
                      gate=True, severity="error")

    plan_desc = {
        "schemaVersion": 2, "snapshotId": snap["id"], "capabilityManifestId": cm_id,
        "semanticClosures": K.ordered(
            [CL_RS_PROVIDER["id"], CL_EVALUATOR["id"], CL_DETECTOR["id"],
             CL_RS_TOOLCHAIN["id"], CL_RS_LLVM["id"], CL_ADAPTER["id"]],
            "canonical-set"),
        "analysisSpecDigest": analysis_spec_digest,
        "resolvedConfigDigest": ctxdata["cfgDigest"],
        "nativeContextDigests": [ctxdata["ctxHex"]],
        "importIds": [imp_id], "policyDigest": pol["policyDigest"],
        "waiverDigest": pol["waiverDigest"], "scopeDigest": ctxdata["scopeDigest"],
        "budget": {"unit": "work-units", "limit": 2000000},
        "semanticGrantDigest": grant_digest,
        "capabilityManifestBytesDigest": cm_bytes_digest}
    if plan_desc["importIds"] and "read-import" not in grant["analysisOperations"]:
        raise K.Refusal("PLAN_IMPORT_WITHOUT_READ_IMPORT_OPERATION")
    plan_id, plan_hex = ident("plan", plan_desc)

    shared = repo.files["crates/core/src/shared.rs"]
    body = b"{\n    a + b\n}"
    span = (shared.index(body), shared.index(body) + len(body))

    file_fact = make_fact(
        snap["id"], "file", "enumerated", uni_hex, uni_hex, CL_RS_PROVIDER["id"],
        {"path": "crates/core/src/shared.rs",
         "contentSha256": inv["crates/core/src/shared.rs"],
         "byteLength": len(shared)},
        [{"path": "crates/core/src/shared.rs",
          "blobDigest": inv["crates/core/src/shared.rs"],
          "startByte": 0, "endByte": len(shared)}])
    apply_file_join(file_fact, snap, inv)

    facts = [file_fact]
    clone_records = {}
    scope_clone_subjects = ["body:crates/core/src/shared.rs#%d-%d" % span]
    if not partial_mode:
        blv, blv_raw = rust_body_language_version(
            ctx, universe, ownership, "crates/core/src/shared.rs")
        p0, f0, _ = clone_payload("L0-verbatim", shared[span[0]:span[1]], None,
                                  "rust", blv_raw)
        c0 = make_fact(snap["id"], "clones", "normalized-body-hash", uni_hex,
                       uni_hex, CL_RS_PROVIDER["id"], p0,
                       [{"path": "crates/core/src/shared.rs",
                         "blobDigest": inv["crates/core/src/shared.rs"],
                         "startByte": span[0], "endByte": span[1]}])
        tokens = [("punc", "{"), ("ident", "a"), ("op", "+"), ("ident", "b"),
                  ("punc", "}")]
        p1, f1, stream = clone_payload("L1-lexical", None, tokens, "rust", blv_raw)
        c1 = make_fact(snap["id"], "clones", "normalized-body-hash", uni_hex,
                       uni_hex, CL_RS_PROVIDER["id"], p1,
                       [{"path": "crates/core/src/shared.rs",
                         "blobDigest": inv["crates/core/src/shared.rs"],
                         "startByte": span[0], "endByte": span[1]}])
        facts += [c0, c1]
        clone_records = {"bodyLanguageVersion": blv,
                         "L0": {"payload": p0, "frameHex": f0.hex()},
                         "L1": {"payload": p1, "frameHex": f1.hex(),
                                "tokenStreamHex": stream.hex()}}

    scope_file = make_scope(snap["id"], uni_hex, uni_hex, "file", "enumerated",
                            CL_RS_PROVIDER["id"],
                            ["file:crates/core/src/shared.rs"])
    cov_file = make_coverage(scope_file, coverage_entry(
        "file", "enumerated", "complete", scope_file, "not-applicable", False,
        True, "complete", 0, []))

    scope_clone = make_scope(snap["id"], uni_hex, uni_hex, "clones",
                             "normalized-body-hash", CL_RS_PROVIDER["id"],
                             scope_clone_subjects)
    if partial_mode:
        # The empty clone view. Enumeration is `partial`, so NO body dialect is
        # admissible: the scope mints no body identity and its Coverage must
        # report the incompleteness rather than claim completeness.
        cov_clone = make_coverage(scope_clone, coverage_entry(
            "clones", "normalized-body-hash", "unknown", scope_clone,
            "not-applicable", False, False, "complete", 0, [],
            deficiency="input-closure-incomplete", native_cause=None,
            closed_world={"exportsClosed": "unknown",
                          "entryPointsRecognized": "partial",
                          "nonliteralLoading": "none",
                          "externalConsumers": "unknown",
                          "dynamicDispatch": "not-applicable",
                          "reasons": ["source-unit-ownership-enumeration-partial"],
                          "deadCodeRepairEligible": False}))
    else:
        cov_clone = make_coverage(scope_clone, coverage_entry(
            "clones", "normalized-body-hash", "complete", scope_clone,
            "not-applicable", False, True, "complete", 0, []))

    view = make_view(plan_id, [scope_file, scope_clone], facts,
                     [cov_file, cov_clone], CL_RS_PROVIDER["id"],
                     [DOC_DIGEST["relation"], DOC_DIGEST["native"]])

    if partial_mode:
        value, verdict, subject_facts = "indeterminate", "indeterminate", []
    else:
        value, verdict, subject_facts = "true", "fail", [facts[1]]

    result = finish_run(
        name=name, repo=repo, snap=snap, plan_desc=plan_desc, plan_id=plan_id,
        pol=pol, view=view, facts=facts, coverages=[cov_file, cov_clone],
        subject_facts=subject_facts, subject_coverages=[cov_clone],
        subject_key={"language": "rust", "kind": "symbol",
                     "logicalPath": "crates/core/src/shared.rs",
                     "qualifiedName": "cb_core::shared::add",
                     "discriminator": discriminator(
                         ["rust", "fn", "cb_core::shared::add", "(i32,i32)->i32"])},
        value=value, verdict=verdict, capability_manifest_id=cm_id,
        analysis_spec=analysis_spec, imports=imports,
        provider_closure=CL_RS_PROVIDER["id"],
        emit_finding=not partial_mode,
        extra={"context": ctx, "universe": universe,
               "sourceUnitOwnership": ownership,
               "dependencySourceSet": ctxdata["depSet"],
               "dependencyFileManifest": ctxdata["fileManifest"],
               "unifiedFeatures": ctxdata["unifiedFeatures"],
               "cargoConfigProjection": ctxdata["configProjection"],
               "editionMapCanonicalBytes": len(K.C(ctxdata["editionMap"])),
               "editionMapCrateCount": len(ctxdata["editionMap"]),
               "clones": clone_records,
               "importPayload": payload,
               "nestedIdentities": {
                   "dependencySourceSetId": ctxdata["depId"],
                   "dependencyFileManifestSha256": ctxdata["fileManifestHex"],
                   "unifiedFeaturesId": ctxdata["ufId"],
                   "configProjectionSha256": ctxdata["ccpHex"],
                   "projectionSha256": ctxdata["configProjection"]["projectionSha256"],
                   "sourceUnitOwnershipId": ctxdata["ownId"],
                   "nativeContextId": ctxdata["ctxId"],
                   "semanticUniverseId": ctxdata["uniId"]},
               })
    result["ownershipSelection"] = list(selection)
    result["universeHex"] = uni_hex
    result["cloneRecords"] = clone_records
    result["ctxdata"] = ctxdata
    return result


UNIT = {
    "core_lib": K.unit_id("crates/core/Cargo.toml", "lib", "cb_core")[0],
    "core_test": K.unit_id("crates/core/Cargo.toml", "test", "shared_it")[0],
    "legacy": K.unit_id("crates/legacy#2015/Cargo.toml", "lib", "cb_legacy")[0],
    "tools": K.unit_id("crates/tools/Cargo.toml", "bin", "cb-tools")[0],
}

SEL_2021 = [UNIT["core_lib"], UNIT["legacy"], UNIT["tools"]]
SEL_2015 = [UNIT["core_test"], UNIT["legacy"], UNIT["tools"]]
SEL_2021_NARROW = [UNIT["core_lib"], UNIT["legacy"]]     # dialect unchanged
SEL_AMBIGUOUS = [UNIT["core_lib"], UNIT["core_test"], UNIT["legacy"]]


def build_all():
    out = {}
    out["RUN-TS"] = build_ts_run()
    out["RUN-RUST-2021"] = build_rust_run("RUN-RUST-2021", SEL_2021)
    out["RUN-RUST-2015"] = build_rust_run("RUN-RUST-2015", SEL_2015)
    out["RUN-RUST-2021-NARROW"] = build_rust_run("RUN-RUST-2021-NARROW",
                                                 SEL_2021_NARROW)
    out["RUN-RUST-PARTIAL"] = build_rust_run("RUN-RUST-PARTIAL", SEL_2021,
                                             enumeration="partial",
                                             partial_mode=True)
    return out


if __name__ == "__main__":
    graphs = build_all()
    for k, g in graphs.items():
        print(k, g["runId"], "verdict=", g["verdict"])
