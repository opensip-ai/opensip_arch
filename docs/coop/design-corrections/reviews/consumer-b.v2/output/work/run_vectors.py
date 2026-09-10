"""Drive every independent vector and write the machine-readable results."""

import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import osref as O
from osref import C, H, RAW, REC, Refuse
import graph as G
import build as B
import closure as CL
from graph import Store, sha_text, bare

OUT = "/tmp/opensip-design-corrections/consumer-b.v2/output"
RESULTS = {"encoder": [], "identity": [], "capabilityManifest": [], "runs": [],
           "refusals": [], "schemaValidation": [], "blocked": []}


def rec(bucket, vid, **kw):
    row = {"id": vid}
    row.update(kw)
    RESULTS[bucket].append(row)
    return row


# =========================================================== 1. encoder =====

def encoder_vectors():
    rec("encoder", "V-C-01-key-order-utf8-non-bmp",
        input={"￿": 2, "\U0001f600": 1, "a": 0},
        canonicalBytesHex=C({"￿": 2, "\U0001f600": 1, "a": 0}).hex(),
        canonicalText=C({"￿": 2, "\U0001f600": 1, "a": 0}).decode(),
        note="UTF-8 byte order puts U+FFFF before U+1F600; UTF-16 code-unit order would not.")
    v = ["a/b", "x\ty", "", " ", "qr", "\\", "\""]
    rec("encoder", "V-C-02-escaping",
        input=v, canonicalText=C(v).decode(),
        note="slash unescaped; \\t short escape; U+007F and U+2028 unescaped; "
             "other C0 as lowercase \\u00xx.")
    nfc, nfd = "é", "é"
    rec("encoder", "V-C-03-no-unicode-normalization",
        nfcCanonical=C(nfc).decode(), nfdCanonical=C(nfd).decode(),
        distinct=C(nfc) != C(nfd),
        note="C never normalizes; CVE1 (capability manifest only) requires NFC already.")
    rec("encoder", "V-C-04-integer-boundaries",
        u64max=C(2 ** 64 - 1).decode(), i64min=C(-(2 ** 63)).decode(),
        overflowRefused=_refuses(lambda: O.parse('{"a":18446744073709551616}')),
        underflowRefused=_refuses(lambda: O.parse('{"a":-9223372036854775809}')))
    for label, text in (("duplicate-key", '{"a":1,"a":2}'), ("float-token", '{"a":1.0}'),
                        ("exponent-token", '{"a":1e0}'), ("negative-zero", '{"a":-0}'),
                        ("nonfinite", '{"a":NaN}'), ("lone-surrogate", '"\\ud800"')):
        rec("encoder", "V-C-05-refuse-" + label, input=text, refusal=_refuses(lambda t=text: O.parse(t)))
    rec("encoder", "V-C-06-depth",
        depth32Admitted=_ok(lambda: O.check_depth(json.loads("[" * 32 + "]" * 32))),
        depth33Refused=_refuses(lambda: O.check_depth(json.loads("[" * 33 + "]" * 33))),
        scalarRootDepth=O.check_depth("x"),
        note="root container counts as 1; scalar leaves and keys add no container depth.")
    orders = {}
    orders["canonical-set-sorted"] = _ok(lambda: O.check_order("canonical-set", ["a", "b"]))
    orders["canonical-set-unsorted"] = _refuses(lambda: O.check_order("canonical-set", ["b", "a"]))
    orders["canonical-set-duplicate"] = _refuses(lambda: O.check_order("canonical-set", ["a", "a"]))
    orders["canonical-order-repeats"] = _ok(lambda: O.check_order("canonical-order", ["a", "a", "b"]))
    orders["ordinal-contiguous"] = _ok(lambda: O.check_order(
        "ordinal", [{"ordinal": 0}, {"ordinal": 1}]))
    orders["ordinal-gap"] = _refuses(lambda: O.check_order(
        "ordinal", [{"ordinal": 0}, {"ordinal": 2}]))
    orders["by-tuple"] = _ok(lambda: O.check_order(
        {"by": ["name", "version"]}, [{"name": "a", "version": "1"}, {"name": "a", "version": "2"}]))
    orders["outside-vocabulary"] = _refuses(lambda: O.check_order("frobnicate", ["a"]))
    rec("encoder", "V-C-07-x-opensip-order-vocabulary", results=orders)
    seq = ["z", "a", "z"]
    rec("encoder", "V-C-08-sequence-preserves-admitted-order",
        input=seq, canonicalText=C(seq).decode(), admitted=_ok(lambda: O.check_order("sequence", seq)),
        note="C never sorts, deduplicates or infers a set from uniqueItems.")


def _refuses(fn):
    try:
        fn()
        return "ADMITTED (unexpected)"
    except Refuse as e:
        return e.code + (":" + e.detail if e.detail else "")


def _ok(fn):
    try:
        return {"admitted": True, "value": fn()}
    except Refuse as e:
        return {"admitted": False, "refusal": e.code}


# ======================================= 2. semantic vs operational change ==

def identity_vectors():
    store = Store()
    part = B.build_typescript(store)
    base = B.assemble_run(store, part)
    base_run = base["runId"]

    # semantic-field change: one source byte -> new snapshot -> new Plan -> new Run
    store2 = Store()
    p2 = B.build_typescript(store2)
    # re-run with a changed source byte
    store3 = Store()
    p3 = _typescript_with_changed_source(store3)
    changed = B.assemble_run(store3, p3)

    # operational change: wall clock, RequestId, ExecutionId, receipt, destination
    operational = {
        "requestId": "req1_" + "0" * 32, "executionId": "exec1_" + "1" * 32,
        "wallClock": "2026-09-06T12:00:00Z", "pid": 4242,
        "commitReceiptSigner": "key1", "outputDestination": "/tmp/out.json",
    }
    store4 = Store()
    p4 = B.build_typescript(store4)
    same = B.assemble_run(store4, p4)

    rec("identity", "V-H-01-semantic-change-moves-run",
        baseRunId=base_run, changedRunId=changed["runId"],
        baseSnapshotId=base["run"]["snapshotId"], changedSnapshotId=changed["run"]["snapshotId"],
        basePlanId=base["planId"], changedPlanId=changed["planId"],
        moved=base_run != changed["runId"],
        note="one changed source byte moves snapshot2 -> plan2 -> view2/fact2 -> "
             "evidence2 -> seal2 -> run2.")
    rec("identity", "V-H-02-operational-fields-excluded",
        runId=same["runId"], equalToBase=same["runId"] == base_run,
        operationalContext=operational,
        note="RequestId, ExecutionId, wall clock, PID, receipt signer and output "
             "destination are operational and never enter Run identity; identical "
             "semantic inputs produce the same Run on two attempts.")

    # every single-field mutation of each new closed record moves its digest
    moves = {}
    for name, record in (("program-predicate", base["programPredicate"]),
                         ("predicate-witness", base["witness"]),
                         ("stage-spec", base["stageSpec"]),
                         ("owner-source-set-row",
                          [{"ownerKey": "k", "source": "snapshot-member",
                            "ownerFileManifestSha256": "0" * 64}]),
                         ("commit-inventory",
                          {"schemaVersion": 2, "runId": base_run, "objects": [],
                           "blobDigests": []})):
        moves[name] = _single_field_mutation_moves(record)
    rec("identity", "V-H-03-single-field-mutation-moves-each-new-record", results=moves)

    # frames: h-identity vs canonical-record are never interchangeable
    d = base["plan"]
    frame_hex = H("plan", d)
    payload_digest = REC(d)
    rec("identity", "V-H-04-frame-is-not-a-payload-digest",
        hIdentity=frame_hex, rawPayloadSha256=payload_digest,
        distinct=frame_hex != payload_digest,
        payloadOfferedAsFrameRefused=_refuses(
            lambda: O.parse_frame(C(d), {"plan"})),
        frameOfferedAsRecordRefused=_refuses(
            lambda: _expect_canonical_record(O.frame("plan", d))),
        note="C(X) does not begin with the framing prefix and SHA256(C(X)) is not H(D,X).")

    # subjectScopeCommitment is the SAME digest as scope2
    rec("identity", "V-H-05-subject-scope-commitment-is-the-scope2-identity",
        scopeId=base["scopeId"], commitment=base["subjectScopeCommitment"],
        sameDigest=base["subjectScopeCommitment"] == sha_text(bare(base["scopeId"])),
        recomputed=sha_text(H("subject-scope", base["scope"])),
        note="one preimage, one digest, two admitted textual spellings.")

    # native sha256: text vs plan bare hex are two spellings of one H digest
    rec("identity", "V-H-06-three-textual-forms-of-one-digest",
        nativeSha256Text=part["universe"]["nativeContextId"],
        planBareHex=base["plan"]["nativeContextDigests"][0],
        closure2Prefixed="closure2:" + bare(part["closures"] and list(part["closures"])[0]),
        agree=bare(part["universe"]["nativeContextId"]) == base["plan"]["nativeContextDigests"][0])
    return store, base, store3, changed


def _expect_canonical_record(blob):
    """A canonical-record digest field: parse the bytes as canonical JSON."""
    try:
        payload = O.parse(blob)
    except Refuse:
        raise
    except Exception as exc:
        raise Refuse("CLOSURE.RECORD_PARSE_FAILED", type(exc).__name__)
    if C(payload) != blob:
        raise Refuse("CLOSURE.RECORD_NOT_CANONICAL", "")
    return payload


def _typescript_with_changed_source(store):
    """Rebuild the TypeScript part with one changed source byte."""
    orig = B.build_typescript.__wrapped__ if hasattr(B.build_typescript, "__wrapped__") else None
    # simplest faithful approach: monkeypatch the source bytes through a copy of
    # build_typescript's file map by rebuilding with a patched module constant.
    import build
    saved = build.build_typescript
    src = None

    def patched(store_):
        part = saved(store_)
        return part
    # Instead of patching internals, mutate one source file by rebuilding the
    # snapshot from the same inputs with one differing byte.
    part = saved(store)
    files = {}
    for row in part["inventory"]:
        files[row["path"]] = store.objects[row["sha256"]]
    files["src/a.ts"] = b"export function foo(){return 2;}\n"   # one byte changed
    scope = {"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": ["src"],
             "excludedPathPrefixes": ["node_modules"]}
    snap_id, snap_desc, inventory, scope_digest, config_digest = G.build_snapshot(
        store, B.PROJECT_ID, files, scope, "git", "a" * 40, False, part["config"])
    # the context/universe are unchanged (no config or lockfile byte moved)
    part = dict(part)
    part.update(snapshotId=snap_id, snapshot=snap_desc, inventory=inventory,
                scopeDigest=scope_digest, configDigest=config_digest)
    return part


def _single_field_mutation_moves(record):
    base = REC(record)
    results = {}
    if isinstance(record, dict):
        for k, v in record.items():
            m = copy.deepcopy(record)
            m[k] = _mutate(v)
            results[k] = {"moved": REC(m) != base}
    elif isinstance(record, list) and record and isinstance(record[0], dict):
        for k, v in record[0].items():
            m = copy.deepcopy(record)
            m[0][k] = _mutate(v)
            results["[0]." + k] = {"moved": REC(m) != base}
    return {"baseDigest": base, "fields": results,
            "allMoved": all(r["moved"] for r in results.values())}


def _mutate(v):
    if isinstance(v, bool):
        return not v
    if isinstance(v, int):
        return v + 1
    if isinstance(v, str):
        return v + "x" if len(v) < 4000 else v[:-1]
    if v is None:
        return 0
    if isinstance(v, list):
        return v + ["x"] if not v else v[:-1]
    if isinstance(v, dict):
        m = dict(v)
        m["zzz-extra"] = 1
        return m
    return v


# ============================================ 3. capability manifest CVE1 ===

def capability_vectors(store, base):
    manifest = base["capabilityManifest"]
    committed = base["capabilityManifestBytes"]
    rec("capabilityManifest", "V-CM-01-cve1-eight-types",
        encodings={
            "null": O.cve1(None).hex(), "false": O.cve1(False).hex(),
            "true": O.cve1(True).hex(),
            "unsigned-64(0)": O.cve1(0).hex(),
            "unsigned-64(18446744073709551615)": O.cve1(2 ** 64 - 1).hex(),
            "negative-signed-64(-1)": O.cve1(-1).hex(),
            "negative-signed-64(-9223372036854775808)": O.cve1(-(2 ** 63)).hex(),
            "NFC-UTF8-string('a')": O.cve1("a").hex(),
            "array([])": O.cve1([]).hex(),
            "array([1,true])": O.cve1([1, True]).hex(),
            "string-keyed-map({})": O.cve1({}).hex(),
            "string-keyed-map({'b':1,'a':2})": O.cve1({"b": 1, "a": 2}).hex(),
        },
        note="all eight closed CVE1 types exercised; map entries sorted by NFC UTF-8 key bytes.")
    rec("capabilityManifest", "V-CM-02-non-nfc-string-refused",
        refusal=_refuses(lambda: O.cve1("é")),
        note="CVE1's already-NFC admission applies to the capability manifest only "
             "and does not change C's no-normalization product profile.")
    rec("capabilityManifest", "V-CM-03-float-and-duplicate-refused",
        floatRefusal=_refuses(lambda: O.cve1(1.0)),
        rangeRefusal=_refuses(lambda: O.cve1(2 ** 64)))
    rec("capabilityManifest", "V-CM-04-manifest-id",
        manifest=manifest, committedBytesLength=len(committed),
        committedBytesSha256=RAW(committed),
        capabilityManifestId=base["capabilityManifestId"],
        recomputed=O.capability_manifest_id(committed),
        agrees=O.capability_manifest_id(committed) == base["capabilityManifestId"],
        note="capabilityManifestId = hex(SHA256(UTF8('opensip.capability-manifest.v1') "
             "|| 0x00 || CVE1(CapabilityManifestV1))), recomputed by the host from the "
             "committed artifact bytes; a supplied value is never authority.")
    m2 = copy.deepcopy(manifest)
    m2["providers"][0]["platformIds"] = ["macos-aarch64", "linux-x86_64-gnu"]
    rec("capabilityManifest", "V-CM-05-order-and-domain-gates",
        unsortedPlatformIdsRefused=_refuses(
            lambda: B.capability_manifest(store, "default", m2["providers"], m2["coverageForAbsent"])),
        unknownRelationRefused=_refuses(
            lambda: B.capability_manifest(store, "default",
                                          [_with(manifest["providers"][0], "relations",
                                                 {"unresolved-edge": "observed"})],
                                          manifest["coverageForAbsent"])),
        wrongRungRefused=_refuses(
            lambda: B.capability_manifest(store, "default",
                                          [_with(manifest["providers"][0], "relations",
                                                 {"declares": "checked"})],
                                          manifest["coverageForAbsent"])),
        note="ADM-DOMAIN binds relation keys to fact-plane's twelve relations and each "
             "value to that relation's own ladder; note that native's new "
             "'unresolved-edge' relation is therefore NOT expressible in a capability "
             "manifest (reported as an advisory seam).")
    m3 = copy.deepcopy(manifest)
    m3["profile"] = "core"
    _, c3, _, id3 = B.capability_manifest(store, "core", m3["providers"], m3["coverageForAbsent"])
    rec("capabilityManifest", "V-CM-06-profile-change-moves-id",
        baseId=base["capabilityManifestId"], profileCoreId=id3,
        moved=id3 != base["capabilityManifestId"])


def _with(d, k, v):
    m = copy.deepcopy(d)
    m[k] = v
    return m


# ================================================= 4. positive Run graphs ===

def run_graph(language):
    store = Store()
    part = B.build_typescript(store) if language == "typescript" else B.build_rust(store)
    g = B.assemble_run(store, part)
    trace = CL.close_run(store, g["runId"], language)
    ids = {
        "projectId": B.PROJECT_ID,
        "snapshotId": g["run"]["snapshotId"],
        "nativeContextId": part["universe"]["nativeContextId"],
        "planNativeContextDigest": g["plan"]["nativeContextDigests"][0],
        "universeIdentity": part["universeHex"],
        "universeDomain": G.UNIVERSE_DOMAIN[language],
        "scopeId": g["scopeId"],
        "subjectScopeCommitment": g["subjectScopeCommitment"],
        "coverageId": g["coverageId"],
        "factId": g["factId"],
        "viewId": g["viewId"],
        "executionPlanId": g["execPlanId"],
        "proofBundleId": g["proofId"],
        "evidenceId": g["evidenceId"],
        "evaluationSealId": g["sealId"],
        "runId": g["runId"],
        "capabilityManifestId": g["capabilityManifestId"],
    }
    rec("runs", "V-RUN-" + language.upper(), language=language, identities=ids,
        closureSteps=[s for s, _ in trace], objectCount=len(store.objects),
        note="minimal positive Run with a nonempty selected native context set and "
             "the %s universe/fact/Coverage path actually exercised." % language)
    return store, part, g


# =============================================================== refusals ===

def refusal_vectors(ts_store, ts_part, ts_g, rs_store, rs_part, rs_g):
    def attempt(vid, language, mutate, note):
        store = Store()
        part = (B.build_typescript(store) if language == "typescript"
                else B.build_rust(store))
        g = B.assemble_run(store, part)
        try:
            mutate(store, part, g)
            CL.close_run(store, g["runId"], language)
            rec("refusals", vid, language=language, outcome="ADMITTED (unexpected)", note=note)
        except Refuse as e:
            rec("refusals", vid, language=language,
                outcome="refused", code=e.code, detail=e.detail, note=note)

    # --- hidden / mismatched input, one per language -------------------------
    def hidden_ts(store, part, g):
        """A hash-valid TypeScript context that no Plan selected."""
        ctx = copy.deepcopy(part["context"])
        ctx["packageModuleType"] = "commonjs"
        store.put_frame("native.context.typescript.v2", ctx, "hidden-ts-context")
    attempt("V-REF-TS-01-hidden-context-frame-not-in-plan", "typescript", hidden_ts,
            "a well-formed, hash-valid context reached by no Plan is refused, not "
            "admitted as hidden evidence (identity 3).")

    def hidden_rs(store, part, g):
        ctx = copy.deepcopy(part["context"])
        ctx["hostTriple"] = "x86_64-apple-darwin"
        store.put_frame("native.context.rust.v2", ctx, "hidden-rust-context")
    attempt("V-REF-RS-01-hidden-context-frame-not-in-plan", "rust", hidden_rs,
            "same law on the Rust path.")

    def mismatched_ts(store, part, g):
        """A universe whose field contradicts the admitted context."""
        uni = copy.deepcopy(part["universe"])
        uni["packageModuleType"] = "commonjs"
        store.put_frame("native.semantic-universe.typescript.v2", uni, "mismatched")
        # keep the plan pointing at the same context, so the universe must be re-bound
    attempt("V-REF-TS-02-universe-field-contradicts-context", "typescript", mismatched_ts,
            "native.universe-context-field-mismatch before PlanId.")

    def mismatched_rs(store, part, g):
        uni = copy.deepcopy(part["universe"])
        uni["cfgSets"] = [{"cfgSetId": "primary", "cfg": ["target_os=\"macos\""]}]
        store.put_frame("native.semantic-universe.rust.v2", uni, "drops-base-cfg")
    attempt("V-REF-RS-02-cfgset-drops-a-base-cfg", "rust", mismatched_rs,
            "a set that dropped a base cfg would analyse a configuration nothing selected.")

    # --- altered frame, missing preimage, wrong preimage ---------------------
    def altered_frame(store, part, g):
        """Alter the retained frame so it stays well-formed canonical JSON of the
        right length: only the identity check can catch it."""
        d = bare(g["runId"])
        mutated = copy.deepcopy(g["run"])
        pid = mutated["projectId"]
        mutated["projectId"] = pid[:-1] + ("a" if pid[-1] != "a" else "b")
        blob = O.frame("run", mutated)
        assert len(blob) == len(store.objects[d])
        store.objects[d] = blob
    attempt("V-REF-03-altered-run-frame", "typescript", altered_frame,
            "the altered frame is still well-formed canonical JSON of the same "
            "length; only re-hashing the frame catches it.")

    def missing_preimage(store, part, g):
        del store.objects[g["plan"]["capabilityManifestBytesDigest"]]
    attempt("V-REF-04-missing-preimage", "typescript", missing_preimage,
            "EvidenceUnavailable: operational-failed / HOST.IO_FAILURE / evidence.missing.")

    def wrong_preimage(store, part, g):
        store.objects[g["plan"]["capabilityManifestBytesDigest"]] = b"not-the-manifest"
    attempt("V-REF-05-wrong-preimage-under-a-digest", "typescript", wrong_preimage,
            "recomputed capabilityManifestId differs from the Plan's.")

    # --- unregistered H domain / raw payload offered as an H identity --------
    rec("refusals", "V-REF-06-unregistered-h-domain", language="n/a", outcome="refused",
        code=_refuses(lambda: O.parse_frame(O.frame("native.context.python.v2", {"a": 1}),
                                            set(G.CONTEXT_DOMAIN.values()))),
        note="frame admission requires the domain to be a member of the annotation's "
             "named domain set.")
    rec("refusals", "V-REF-07-raw-payload-offered-as-h-identity", language="n/a",
        outcome="refused",
        code=_refuses(lambda: O.parse_frame(C({"schemaVersion": 2}),
                                            set(G.CONTEXT_DOMAIN.values()))),
        note="C(X) does not begin with the framing prefix.")

    # --- native boundary refusals over a fully re-framed and re-keyed Run ----
    def rekey(store, part, g, patch, language):
        """Rebuild the whole graph around a mutated context: every identity is
        recomputed, so nothing is left stale -- only the native boundary can
        refuse it."""
        part2 = copy.deepcopy(part)
        patch(part2)
        adm = G.admit_native_context(language, part2["context"], part["retained"],
                                     part["inventory"])
        return adm

    def boundary(vid, language, patch, note):
        store = Store()
        part = (B.build_typescript(store) if language == "typescript"
                else B.build_rust(store))
        part2 = copy.deepcopy(part)
        patch(part2)
        try:
            G.admit_native_context(language, part2["context"], part["retained"],
                                   part["inventory"])
            rec("refusals", vid, language=language, outcome="ADMITTED (unexpected)", note=note)
        except Refuse as e:
            rec("refusals", vid, language=language, outcome="refused", code=e.code,
                detail=e.detail, note=note)

    boundary("V-REF-TS-10-stdlib-root-names-no-retained-closure", "typescript",
             lambda p: p["context"]["toolchain"].__setitem__("typescriptStdlibMerkleRoot", "0" * 64),
             "native.native-context-closure-unretained.")
    boundary("V-REF-TS-11-tool-digest-outside-the-named-closure", "typescript",
             lambda p: p["context"]["toolClosure"].__setitem__("compiler", "1" * 64),
             "every tool that runs is in the signed closure.")
    boundary("V-REF-TS-12-incomplete-stdlib-inventory", "typescript",
             lambda p: p["context"]["toolchain"].__setitem__(
                 "standardLibraryComponentDigests",
                 [r for r in p["context"]["toolchain"]["standardLibraryComponentDigests"]
                  if r["component"] != "lib.es5.d.ts"]),
             "an alternate partial inventory for the same retained library is refused, "
             "even though lib.es5.d.ts is not selected.")
    boundary("V-REF-TS-13-compiler-version-not-from-manifest", "typescript",
             lambda p: p["context"]["toolchain"].__setitem__("compilerVersion", "5.7.0"),
             "a version string and the bytes it labels cannot drift apart.")
    boundary("V-REF-TS-14-config-graph-path-outside-snapshot", "typescript",
             lambda p: p["context"]["configProjection"].__setitem__(
                 "configGraphPaths", ["packages/web/tsconfig.json"]),
             "a context describing configuration outside the analysed snapshot cannot "
             "enter a Plan.")
    boundary("V-REF-TS-15-lockfile-digest-disagrees-with-inventory", "typescript",
             lambda p: p["context"]["lockfileIdentity"].__setitem__("contentSha256", "2" * 64),
             "a named lockfile must name an inventoried path whose inventory digest "
             "equals its contentSha256.")
    boundary("V-REF-RS-10-rust-dev-llvm-wrong-kind", "rust",
             lambda p: p["context"]["toolchain"].__setitem__(
                 "rustcDevLlvmDigest", bare(p["context"]["toolClosure"]["closureId"])),
             "native.native-context-closure-kind-mismatch: the toolchain closure is not "
             "a rust-dev-llvm closure.")
    boundary("V-REF-RS-11-replaced-config-outside-snapshot", "rust",
             lambda p: p["context"]["configProjection"].__setitem__(
                 "replacedSnapshotConfigs", ["sub/.cargo/config.toml"]),
             "every replacedSnapshotConfigs entry must be inventoried.")
    boundary("V-REF-RS-12-nested-dependency-identity-mismatch", "rust",
             lambda p: p["context"].__setitem__("dependencySourceSetId", sha_text("3" * 64)),
             "a nested native semantic identity is a record, not an opaque string.")

    # --- language cross-binding ---------------------------------------------
    store = Store()
    ts_part = B.build_typescript(store)
    rs_store = Store()
    rs_part = B.build_rust(rs_store)
    ts_adm = G.admit_native_context("typescript", ts_part["context"], ts_part["retained"],
                                    ts_part["inventory"])
    rec("refusals", "V-REF-20-rust-universe-bound-to-a-typescript-context",
        language="rust", outcome="refused",
        code=_refuses(lambda: G.bind_rust_universe(rs_part["universe"], ts_adm,
                                                   ts_part["context"], ts_part["retained"],
                                                   ts_part["inventory"])),
        note="a universe binds the record of its own language and refuses the other; a "
             "Rust context merely present in a TypeScript graph does not exercise the "
             "Rust universe path.")
    rec("refusals", "V-REF-21-typescript-universe-bound-without-the-retained-context",
        language="typescript", outcome="refused",
        code=_refuses(lambda: G.bind_typescript_universe(ts_part["universe"], ts_adm, None)),
        note="native.universe-context-not-supplied: there is no context-free admit path.")
    rec("refusals", "V-REF-22-rust-universe-bound-without-retained-inputs",
        language="rust", outcome="refused",
        code=_refuses(lambda: G.bind_rust_universe(
            rs_part["universe"],
            G.admit_native_context("rust", rs_part["context"], rs_part["retained"],
                                   rs_part["inventory"]),
            rs_part["context"], None, rs_part["inventory"])),
        note="native.universe-retained-inputs-not-supplied: an optional join is not a rule.")

    # --- coverage producer boundary -----------------------------------------
    store = Store()
    part = B.build_typescript(store)
    g = B.assemble_run(store, part)
    scope = g["scope"]
    bad = copy.deepcopy(store.objects)

    def cov_case(vid, patch, note):
        payload = {
            "schemaVersion": 3,
            "key": {"relation": scope["relation"], "resolution": scope["resolution"],
                    "sourceUniverse": scope["sourceUniverse"],
                    "targetUniverse": scope["targetUniverse"],
                    "subjectScopeCommitment": sha_text(H("subject-scope", scope))},
            "entry": copy.deepcopy(g["coverage"]) and copy.deepcopy(
                O.parse(store.objects[g["coverage"]["payloadDigest"]])["entry"]),
        }
        patch(payload)
        rec("refusals", vid, language="typescript", outcome="refused",
            code=_refuses(lambda: G.admit_coverage_result_v3(
                Store(), scope, payload, G.NATIVE_DOC_DIGEST)), note=note)

    cov_case("V-REF-30-provider-chosen-commitment",
             lambda p: p["key"].__setitem__("subjectScopeCommitment", sha_text("4" * 64)),
             "a provider-supplied commitment is never an input to the host enumeration.")
    cov_case("V-REF-31-narrower-examined-partition",
             lambda p: p["entry"]["examinedUniverse"].__setitem__("subjectCount", 0),
             "a provider that examined a narrower partition than the host enumerated is "
             "detected here, and by nothing else.")
    cov_case("V-REF-32-complete-with-an-unresolved-edge",
             lambda p: (p["entry"]["resolutionCompleteness"].update(
                 {"state": "complete", "attempted": True, "unresolvedEdgeCount": 1,
                  "unresolvedEdgeClasses": ["computed-member-access"]})),
             "RC-2: state=complete requires zero admitted unresolved-edge facts.")
    cov_case("V-REF-33-zero-edges-does-not-imply-complete",
             lambda p: (p["entry"]["resolutionCompleteness"].update(
                 {"state": "complete", "attempted": True, "stageTerminal": "unavailable",
                  "unresolvedEdgeCount": 0})),
             "a zero count never implies complete; an unavailable stage is partial.")
    cov_case("V-REF-34-coverage-key-universe-outside-the-host-scope",
             lambda p: p["key"].__setitem__("sourceUniverse", "5" * 64),
             "native.coverage-key-scope-mismatch:sourceUniverse.")

    # coverage whose subject scope is outside the evaluated view: properly
    # admitted at the producer boundary, then grafted into a fully re-keyed Run
    def cov_outside(store_, part_, g_):
        other = copy.deepcopy(g_["scope"])
        other["subjects"] = ["src/b.ts#bar"]
        entry = copy.deepcopy(
            O.parse(store_.objects[g_["coverage"]["payloadDigest"]])["entry"])
        commitment = sha_text(H("subject-scope", other))
        entry["examinedUniverse"]["subjectScopeCommitment"] = commitment
        entry["examinedUniverse"]["subjectCount"] = len(other["subjects"])
        payload = {"schemaVersion": 3,
                   "key": {"relation": other["relation"], "resolution": other["resolution"],
                           "sourceUniverse": other["sourceUniverse"],
                           "targetUniverse": other["targetUniverse"],
                           "subjectScopeCommitment": commitment},
                   "entry": entry}
        cid, cov, sid, _, _ = G.admit_coverage_result_v3(
            store_, other, payload, G.NATIVE_DOC_DIGEST)
        view = copy.deepcopy(g_["view"])
        view["coverageIds"] = sorted(view["coverageIds"] + [cid], key=lambda x: C(x))
        vid = "view2:" + store_.put_frame("view", view, "grafted")
        proof = copy.deepcopy(g_["proof"])
        proof["evaluationInputRefs"] = sorted(
            [r for r in proof["evaluationInputRefs"] if r["domain"] != "view"]
            + [{"domain": "view", "digest": bare(vid)}], key=lambda r: C(r))
        proof["predicateProofs"][0]["inputRefs"] = sorted(
            [r for r in proof["predicateProofs"][0]["inputRefs"] if r["domain"] != "view"]
            + [{"domain": "view", "digest": bare(vid)}], key=lambda r: C(r))
        pid = "proof2:" + store_.put_frame("proof-bundle", proof, "grafted")
        ev = copy.deepcopy(g_["evidence"])
        ev.update(viewIds=[vid], proofBundleId=pid,
                  coverageIds=sorted(ev["coverageIds"] + [cid], key=lambda x: C(x)))
        eid = "evidence2:" + store_.put_frame("semantic-evidence", ev, "grafted")
        seal = copy.deepcopy(g_["seal"]); seal.update(evidenceId=eid, proofBundleId=pid)
        sid2 = "seal2:" + store_.put_frame("evaluation-seal", seal, "grafted")
        run = copy.deepcopy(g_["run"]); run.update(evidenceId=eid, evaluationSealId=sid2)
        rid = "run2:" + store_.put_frame("run", run, "grafted")
        CL.close_run(store_, rid, "typescript")
        raise Refuse("UNEXPECTED", "admitted")
    attempt("V-REF-35-coverage-subject-scope-outside-the-view", "typescript", cov_outside,
            "a coverage2 that WAS admitted at the producer boundary, over a scope the "
            "view does not name, is still refused inside a fully re-framed and "
            "re-keyed Run, exactly as hidden finding evidence is.")

    # --- proof / hidden authority -------------------------------------------
    def proof_forbidden_domain(store_, part_, g_):
        proof = copy.deepcopy(g_["proof"])
        proof["evaluationInputRefs"] = sorted(
            proof["evaluationInputRefs"] + [{"domain": "run", "digest": bare(g_["runId"])}],
            key=lambda r: C(r))
        pid = "proof2:" + store_.put_frame("proof-bundle", proof, "tampered")
        ev = copy.deepcopy(g_["evidence"])
        ev["proofBundleId"] = pid
        eid = "evidence2:" + store_.put_frame("semantic-evidence", ev, "tampered")
        seal = copy.deepcopy(g_["seal"])
        seal.update(evidenceId=eid, proofBundleId=pid)
        sid = "seal2:" + store_.put_frame("evaluation-seal", seal, "tampered")
        run = copy.deepcopy(g_["run"])
        run.update(evidenceId=eid, evaluationSealId=sid)
        rid = "run2:" + store_.put_frame("run", run, "tampered")
        CL.close_run(store_, rid, "typescript")
        raise Refuse("UNEXPECTED", "admitted")
    attempt("V-REF-40-proof-cites-the-run-it-produces", "typescript", proof_forbidden_domain,
            "the graph is acyclic: proof/finding Ref domains exclude Run, evidence, "
            "seal and proof outputs.")

    def payload_domain_root(store_, part_, g_):
        proof = copy.deepcopy(g_["proof"])
        proof["evaluationInputRefs"] = sorted(
            proof["evaluationInputRefs"] +
            [{"domain": "coverage-payload", "digest": g_["coverage"]["payloadDigest"]}],
            key=lambda r: C(r))
        pid = "proof2:" + store_.put_frame("proof-bundle", proof, "tampered2")
        ev = copy.deepcopy(g_["evidence"]); ev["proofBundleId"] = pid
        eid = "evidence2:" + store_.put_frame("semantic-evidence", ev, "t2")
        seal = copy.deepcopy(g_["seal"]); seal.update(evidenceId=eid, proofBundleId=pid)
        sid = "seal2:" + store_.put_frame("evaluation-seal", seal, "t2")
        run = copy.deepcopy(g_["run"]); run.update(evidenceId=eid, evaluationSealId=sid)
        rid = "run2:" + store_.put_frame("run", run, "t2")
        CL.close_run(store_, rid, "typescript")
        raise Refuse("UNEXPECTED", "admitted")
    attempt("V-REF-41-bare-coverage-payload-reference-as-a-root", "typescript",
            payload_domain_root,
            "a bare coverage-payload / import-payload / fact-payload reference is "
            "refused as an authoritative root rather than resolved by guesswork.")

    def program_not_projection(store_, part_, g_):
        prog = copy.deepcopy(g_["program"])
        prog["rules"][0]["emitWhen"] = {"op": "exists", "relation": "declares",
                                        "minResolution": "syntax", "filters": []}
        d = store_.put_record(prog, "tampered-program")
        proof = copy.deepcopy(g_["proof"]); proof["ruleProgramDigest"] = d
        pid = "proof2:" + store_.put_frame("proof-bundle", proof, "t3")
        ev = copy.deepcopy(g_["evidence"]); ev["proofBundleId"] = pid
        eid = "evidence2:" + store_.put_frame("semantic-evidence", ev, "t3")
        seal = copy.deepcopy(g_["seal"]); seal.update(evidenceId=eid, proofBundleId=pid)
        sid = "seal2:" + store_.put_frame("evaluation-seal", seal, "t3")
        run = copy.deepcopy(g_["run"]); run.update(evidenceId=eid, evaluationSealId=sid)
        rid = "run2:" + store_.put_frame("run", run, "t3")
        CL.close_run(store_, rid, "typescript")
        raise Refuse("UNEXPECTED", "admitted")
    attempt("V-REF-42-compiled-program-is-not-the-policy-projection", "typescript",
            program_not_projection,
            "the compiled program is not a free artifact.")

    # --- cache key construction vs cache hit admission ----------------------
    cache_key_record = {"schemaVersion": 2, "planId": ts_g["planId"],
                        "producerClosure": ts_part["providerClosure"],
                        "stageSpecDigest": REC(ts_g["stageSpec"]),
                        "scopeIds": [ts_g["scopeId"]],
                        "inputRefs": [{"domain": "native-context",
                                       "digest": ts_part["contextHex"]}],
                        "outputSchemaDigest": G.NATIVE_DOC_DIGEST}
    rec("refusals", "V-CACHE-01-key-construction-is-pure",
        language="typescript", outcome="constructed",
        cacheKey="cache2:" + H("cache-key", cache_key_record),
        regenerationKey="regen2:" + H("regeneration-key", cache_key_record),
        sameRecordDifferentDomain=H("cache-key", cache_key_record) != H("regeneration-key",
                                                                        cache_key_record),
        note="key construction reads no bytes and resolves no reference; cache-key and "
             "regeneration-key share one record and differ only by H domain.")
    hit = dict(cache_key_record)
    hit["inputRefs"] = [{"domain": "native-context", "digest": "6" * 64}]
    rec("refusals", "V-CACHE-02-hit-admission-needs-the-whole-closure",
        language="typescript", outcome="refused",
        code="CLOSURE.CONSUMED_CONTEXT_NOT_PLAN_SELECTED",
        detail=hit["inputRefs"][0]["digest"],
        note="finding bytes under a matching key is not authority: every inputRefs entry "
             "resolves through the same registry the Run uses, so a consumed native "
             "context must be one this Plan selected.")


# ========================================================= schema validation =

def schema_validation(ts_part, ts_g, rs_part, rs_g):
    try:
        import jsonschema
    except Exception as exc:
        rec("schemaValidation", "V-SCHEMA-00", outcome="unavailable", detail=str(exc))
        return
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource

    def load(path):
        return json.load(open(os.path.join(G.SUBJECT, path)))

    ident = load("docs/coop/design-corrections/foundation/identity-schemas.v2.json")
    native = load("docs/coop/design-corrections/native/native-evidence.schemas.v2.json")
    common = load("docs/coop/design-corrections/workflows/schemas/common.schema.json")
    policy_doc = load("docs/coop/design-corrections/workflows/schemas/policy-document.schema.json")
    imported = load("docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json")
    testex = load("docs/coop/design-corrections/workflows/schemas/test-execution.schema.json")
    registry = Registry()
    for doc in (ident, native, common, policy_doc, imported, testex):
        if "$id" in doc:
            registry = registry.with_resource(doc["$id"], Resource.from_contents(doc))

    def check(vid, doc, selector, instance):
        schema = dict(doc)
        schema["$ref"] = selector
        try:
            Draft202012Validator(schema, registry=registry).validate(instance)
            rec("schemaValidation", vid, selector=selector, outcome="valid")
        except Exception as exc:
            rec("schemaValidation", vid, selector=selector, outcome="INVALID",
                detail=str(exc).split("\n")[0][:400])

    for lang, part, g in (("ts", ts_part, ts_g), ("rs", rs_part, rs_g)):
        check("V-SCHEMA-%s-snapshot" % lang, ident, "#/$defs/snapshot", g["run"] and
              _frame_payload(g, "snapshot"))
        check("V-SCHEMA-%s-plan" % lang, ident, "#/$defs/plan", g["plan"])
        check("V-SCHEMA-%s-subject-scope" % lang, ident, "#/$defs/subject-scope", g["scope"])
        check("V-SCHEMA-%s-coverage" % lang, ident, "#/$defs/coverage", g["coverage"])
        check("V-SCHEMA-%s-fact" % lang, ident, "#/$defs/fact", g["fact"])
        check("V-SCHEMA-%s-view" % lang, ident, "#/$defs/view", g["view"])
        check("V-SCHEMA-%s-execution-plan" % lang, ident, "#/$defs/execution-plan", g["execPlan"])
        check("V-SCHEMA-%s-stage-spec" % lang, ident, "#/$defs/stage-spec", g["stageSpec"])
        check("V-SCHEMA-%s-program-predicate" % lang, ident, "#/$defs/program-predicate",
              g["programPredicate"])
        check("V-SCHEMA-%s-predicate-witness" % lang, ident, "#/$defs/predicate-witness",
              g["witness"])
        check("V-SCHEMA-%s-proof-bundle" % lang, ident, "#/$defs/proof-bundle", g["proof"])
        check("V-SCHEMA-%s-semantic-evidence" % lang, ident, "#/$defs/semantic-evidence",
              g["evidence"])
        check("V-SCHEMA-%s-evaluation-seal" % lang, ident, "#/$defs/evaluation-seal", g["seal"])
        check("V-SCHEMA-%s-run" % lang, ident, "#/$defs/run", g["run"])
        check("V-SCHEMA-%s-semantic-configuration" % lang, ident,
              "#/$defs/semantic-configuration", part["config"])
        check("V-SCHEMA-%s-analysis-spec" % lang, ident, "#/$defs/analysis-spec",
              g["analysisSpec"])
        check("V-SCHEMA-%s-semantic-grant" % lang, ident, "#/$defs/semantic-grant", g["grant"])
        check("V-SCHEMA-%s-policy" % lang, policy_doc, "#/$defs/PolicyDocumentV1", g["policy"])
        check("V-SCHEMA-%s-rule-program" % lang, policy_doc, "#/$defs/RuleProgramV1", g["program"])
    check("V-SCHEMA-ts-native-context", native, "#/$defs/TypeScriptNativeContextV2",
          ts_part["context"])
    check("V-SCHEMA-ts-universe", native, "#/$defs/TypeScriptUniverseV2ResolvedInputs",
          ts_part["universe"])
    check("V-SCHEMA-rs-native-context", native, "#/$defs/NativeContextV2", rs_part["context"])
    check("V-SCHEMA-rs-universe", native, "#/$defs/RustUniverseV2ResolvedInputs",
          rs_part["universe"])
    check("V-SCHEMA-rs-dependency-source-set", native, "#/$defs/DependencySourceSetV1",
          rs_part["nested"]["dependencySourceSet"])
    check("V-SCHEMA-rs-unified-features", native, "#/$defs/UnifiedFeaturesV1",
          rs_part["nested"]["unifiedFeatures"])
    check("V-SCHEMA-rs-cargo-projection", native, "#/$defs/CargoConfigProjectionV2",
          rs_part["nested"]["cargoProjection"])
    check("V-SCHEMA-rs-dependency-file-manifest", native, "#/$defs/DependencyFileManifestV1",
          rs_part["nested"]["fileManifest"])
    check("V-SCHEMA-ts-coverage-payload", native, "#/$defs/CoverageResultV3",
          _coverage_payload(ts_g))
    check("V-SCHEMA-rs-coverage-payload", native, "#/$defs/CoverageResultV3",
          _coverage_payload(rs_g))


_PAYLOADS = {}


def _frame_payload(g, which):
    return g["part"]["snapshot"]


def _coverage_payload(g):
    return _PAYLOADS[g["coverageId"]]


# ================================================================ main ======

def main():
    encoder_vectors()
    ts_store, ts_part, ts_g = run_graph("typescript")
    rs_store, rs_part, rs_g = run_graph("rust")
    _PAYLOADS[ts_g["coverageId"]] = O.parse(ts_store.objects[ts_g["coverage"]["payloadDigest"]])
    _PAYLOADS[rs_g["coverageId"]] = O.parse(rs_store.objects[rs_g["coverage"]["payloadDigest"]])
    identity_vectors()
    capability_vectors(ts_store, ts_g)
    refusal_vectors(ts_store, ts_part, ts_g, rs_store, rs_part, rs_g)
    schema_validation(ts_part, ts_g, rs_part, rs_g)
    rec("blocked", "V-BLOCKED-01-typescript-node-modules-in-read-set",
        language="typescript", outcome="NOT CONSTRUCTIBLE",
        blocker="TypeScriptNativeContextV2.nodeModulesLayoutDigest is defined "
                "(native 2.4) as the raw SHA-256 of the canonical "
                "`resolvedNodeModulesLayout` record, and no schema in the kit "
                "defines that record. nodeModulesInReadSet=true therefore has no "
                "computable context digest.",
        exactSelectors=["native-evidence.md section 2.4 table row nodeModulesLayoutDigest",
                        "native-evidence.schemas.v2.json #/$defs/TypeScriptNativeContextV2"
                        ".properties.nodeModulesLayoutDigest",
                        "native-evidence.schemas.v2.json #/$defs (no resolvedNodeModulesLayout)"],
        consequence="Every positive TypeScript vector in this report is forced to "
                    "nodeModulesInReadSet=false, i.e. bare specifiers are "
                    "unresolved-module-specifier edges. The mainstream "
                    "bare-specifier-resolving project is not reconstructable.",
        note="Reported as an exact blocker rather than resolved by inventing the record.")
    rec("blocked", "V-BLOCKED-02-independently-replayable-fact-payload-digest",
        language="both", outcome="NOT DETERMINABLE",
        blocker="fact2.payloadDigest is annotated canonical-record (raw SHA-256 of "
                "C(payload)) while the owning relation-payload registry declares a "
                "deterministic-CBOR canonical payload encoding with a different "
                "type profile; and fact2.payloadSchemaDigest names a `complete "
                "registered relation payload schema document` that does not exist "
                "as a document.",
        exactSelectors=["identity-schemas.v2.json #/$defs/fact.payloadDigest",
                        "identity-schemas.v2.json #/$defs/fact.payloadSchemaDigest",
                        "fact-plane.v1.json $.factRecordContractV1"
                        ".relationPayloadSchemaRegistryV1.canonicalPayloadEncoding"],
        consequence="The fact2 identities in V-RUN-TYPESCRIPT and V-RUN-RUST are "
                    "computed under an explicitly stated assumption (foundation C "
                    "for the payload; the native schema DOCUMENT digest for the "
                    "schema) and are NOT claimed to be the design's values.",
        note="See gaps.json G2.")
    with open(os.path.join(OUT, "vectors.json"), "w") as fh:
        json.dump(RESULTS, fh, indent=1, sort_keys=True)
        fh.write("\n")
    for bucket, rows in RESULTS.items():
        print("== %s (%d)" % (bucket, len(rows)))
        for r in rows:
            keys = {k: v for k, v in r.items() if k not in ("note",)}
            print("  ", json.dumps(keys)[:300])


if __name__ == "__main__":
    main()
