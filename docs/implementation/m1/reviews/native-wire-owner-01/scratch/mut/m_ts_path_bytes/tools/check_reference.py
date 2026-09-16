"""Reference-owner and wire-example checks. Runs the pinned reference models (native_evidence_model.v2,
provider_startup_model.v1, provider_wire_model.v1) where they apply; never claims product execution."""
import copy, hashlib, importlib.util, json, re
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

import common as CM
import wirecodec as W

Refuse = W.Refuse


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def C(domain, value):
    return "sha256:" + hashlib.sha256(domain.encode() + b"\x00" + W.encode(value)).hexdigest()


def raw_hex(value):
    return hashlib.sha256(W.encode(value)).hexdigest()


def find(o, key):
    if isinstance(o, dict):
        if key in o:
            return o
        for v in o.values():
            r = find(v, key)
            if r is not None:
                return r
    elif isinstance(o, list):
        for v in o:
            r = find(v, key)
            if r is not None:
                return r
    return None


def has_bytes(v):
    if isinstance(v, bytes):
        return True
    if isinstance(v, dict):
        return any(has_bytes(x) for x in v.values())
    if isinstance(v, list):
        return any(has_bytes(x) for x in v)
    return False


# ---- reference implementations of handwritten rules used by the examples (scaffolding, not product admission) ----
def admit_anchor(a, manifest, snapshot2):
    if a["kind"] == "fact-ref":
        raise Refuse("ANCHOR_FACT_REF_UNDER_FACT2")
    e = manifest.get(a["path"])
    if e is None or e["kind"] != "file" or e["contentSha256"] != a["contentSha256"] or a["snapshotId"] != snapshot2:
        raise Refuse("ANCHOR_SOURCE_JOIN")
    if not a["startByte"] < a["endByte"] <= e["byteLength"]:
        raise Refuse("ANCHOR_EMPTY_OR_OUT_OF_BOUNDS")


def admit_accepted(seal, accepted):
    if seal != accepted:
        raise Refuse("ACCEPTED_NOT_SEAL")


def admit_manifest_digest(manifest):
    if manifest["manifestSha256"] != raw_hex(manifest["entries"]):
        raise Refuse("MANIFEST_DIGEST")


def admit_depsrc_order(entries):
    keys = [(e["packageKey"].encode(), e["path"].encode()) for e in entries]
    if keys != sorted(set(keys)) or len(keys) != len(set(keys)):
        raise Refuse("DEPSRC_ORDER")


def admit_budget_observed(payload):
    if payload["observed"] != payload["limit"] + 1:
        raise Refuse("BUDGET_OBSERVED")


class Reference:
    def __init__(self, arch, out, static):
        native = Path(arch) / "docs/coop/design-corrections/native"
        self.NE = load("ref_ne", native / "native_evidence_model.v2.py")
        self.ST = load("ref_st", native / "provider_startup_model.v1.py")
        self.WI = load("ref_wi", native / "provider_wire_model.v1.py")
        self.s = static
        self.wire = static.wire
        self.reg = Registry().with_resources([(d["$id"], Resource(contents=d, specification=DRAFT202012)) for d in static.docs.values()])
        self.K = W.Carriers(self.wire, self.extern)
        cases = json.loads((native / "native-cases.v2.json").read_text())
        self.fx = cases["fixtures"]
        self.cov_fx = find(cases, "scopeDescriptor")
        self.results = []

    def extern(self, gen, v, where):
        ref = None
        for sid, ns in CM.EXTERN_NS.items():
            if gen.startswith(ns) and sid in self.s.docs:
                name = gen[len(ns):]
                ref = sid + ("#" if name == "Root" else "#/$defs/" + name)
        if ref is None:
            raise Refuse("EXTERN_UNKNOWN", gen)
        if has_bytes(v):
            raise Refuse("EXTERN_BYTES", where)
        errs = list(Draft202012Validator({"$ref": ref}, registry=self.reg).iter_errors(v))
        if errs:
            raise Refuse("EXTERN_SCHEMA", where + ":" + errs[0].message[:100])

    def add(self, id_, ok, detail=""):
        self.results.append({"id": id_, "ok": bool(ok), "detail": detail if isinstance(detail, str) else json.dumps(detail, default=str)[:600]})

    def expect(self, id_, fn, code=None):
        try:
            fn()
            got = None
        except Refuse as exc:
            got = exc.code
        except Exception as exc:  # noqa: BLE001
            got = "EXCEPTION:" + type(exc).__name__ + ":" + str(exc)[:160]
        self.add(id_, got == code, {"expected": code, "got": got})

    # ------------------------------------------------------------------
    def scope2(self):
        NE, ST, K = self.NE, self.ST, self.K
        desc, payload = self.cov_fx["scopeDescriptor"], self.cov_fx["coveragePayload"]
        commit = NE.subject_scope_commitment(desc)
        src, tgt = "sha256:" + desc["sourceUniverse"], "sha256:" + desc["targetUniverse"]
        base = {"relation": desc["relation"], "resolution": desc["resolution"], "sourceUniverseId": src, "targetUniverseId": tgt,
                "subjectScopeCommitment": commit["subjectScopeCommitment"]}
        ts_key = dict(base, producer="typescript-semantic", producerVersion="typescript-provider 1.0.0", schemaVersion=1)
        rs_key = dict(base, producer="rust-semantic", producerVersion="rust-provider 1.0.0", schemaVersion=1)

        def ts():
            K.check({"t": "ref", "ref": "Ts2CoverageKeyV1"}, ts_key, "key")
            frame = {"analysisOrdinal": 0, "stageId": "s1", "entries": [payload],
                     "coverageCommitment": C("opensip.ts-provider.stage-coverage.v1", [payload])}
            K.frame_payload("typescript-semantic", "Coverage", frame)
            ST.admit_coverage_frame("typescript-semantic", frame, "s1", [ts_key])
            scope = {"scopeKind": "all-snapshot-files", "snapshotId": desc["snapshotId"], "subjectCount": 3,
                     "subjectScopeCommitment": C("opensip.coverage.subject-scope.v1", [])}
            domain = {"subjectScope": scope, "keys": [ts_key],
                      "domainCommitment": C("opensip.ts-provider.requested-coverage-domain.v1", {"subjectScope": scope, "keys": [ts_key]})}
            K.check({"t": "ref", "ref": "Ts2RequestedCoverageDomainV1"}, domain, "domain")
            if NE.admit_coverage_result_v3(payload, desc, [])["result"] != "ADMIT":
                raise Refuse("NOT_ADMITTED")
        self.expect("scope2-ts2-admits", ts)

        def rs():
            K.check({"t": "ref", "ref": "Rust3CoverageKeyV2"}, rs_key, "key")
            frame = {"analysisOrdinal": 0, "stageId": "s1", "entries": [payload],
                     "coverageCommitment": C("opensip.rust-provider.stage-coverage.v2", [payload])}
            K.frame_payload("rust-semantic", "CoverageV3", frame)
            ST.admit_coverage_frame("rust-semantic", frame, "s1", [rs_key])
            if NE.admit_coverage_result_v3(payload, desc, [])["result"] != "ADMIT":
                raise Refuse("NOT_ADMITTED")
        self.expect("scope2-rust3-admits", rs)
        refused = []
        for label, value in (("ts-inherited-per-stage", C("opensip.coverage.subject-scope.v1", [{"path": s} for s in desc["subjects"]])),
                             ("rust2-inherited-per-stage", C("opensip.rust-provider.subject-scope.v2", desc["subjects"]))):
            bad = copy.deepcopy(payload)
            bad["key"]["subjectScopeCommitment"] = value
            bad["entry"]["examinedUniverse"]["subjectScopeCommitment"] = value
            out = NE.admit_coverage_result_v3(bad, desc, [])
            refused.append(out["result"] == "REFUSE" and "native.subject-scope-commitment-mismatch" in out["refusals"])
        self.add("scope2-per-stage-value-refused", all(refused), refused)
        other_rung = NE.subject_scope_descriptor(desc["snapshotId"], desc["relation"], "syntactic-name-match", desc["sourceUniverse"],
                                                 desc["targetUniverse"], desc["enumeratorClosure"], desc["subjects"])
        other_target = NE.subject_scope_descriptor(desc["snapshotId"], desc["relation"], desc["resolution"], desc["sourceUniverse"],
                                                   "f" * 64, desc["enumeratorClosure"], desc["subjects"])
        vals = {NE.subject_scope_commitment(d)["subjectScopeCommitment"] for d in (desc, other_rung, other_target)}
        self.add("scope2-keys-differ", len(vals) == 3, sorted(vals))

    # ------------------------------------------------------------------
    def anchors(self):
        K = self.K
        snap = "snapshot2:" + "a" * 64
        manifest = {"src/a.ts": {"kind": "file", "byteLength": 10, "contentSha256": "1" * 64}}
        span = {"kind": "source-span", "snapshotId": snap, "path": "src/a.ts", "contentSha256": "1" * 64, "startByte": 2, "endByte": 5, "factId": None}
        ref = {"kind": "fact-ref", "snapshotId": None, "path": None, "contentSha256": None, "startByte": None, "endByte": None, "factId": "fact1:sha256:" + "2" * 64}

        def fact_ref():
            for rec in ("Ts2AnchorRefV1", "Rust3AnchorRefV1"):
                K.check({"t": "ref", "ref": rec}, ref, rec)
            admit_anchor(ref, manifest, snap)
        self.expect("anchor-fact-ref-refused", fact_ref, "ANCHOR_FACT_REF_UNDER_FACT2")
        self.expect("anchor-span-admits", lambda: (K.check({"t": "ref", "ref": "Rust3AnchorRefV1"}, span, "a"), admit_anchor(span, manifest, snap)))
        empty = dict(span, endByte=2)
        self.expect("anchor-empty-interval-refused-on-wire", lambda: (K.check({"t": "ref", "ref": "Ts2AnchorRefV1"}, empty, "a"), admit_anchor(empty, manifest, snap)),
                    "ANCHOR_EMPTY_OR_OUT_OF_BOUNDS")
        self.expect("anchor-mixed-variant-refused", lambda: K.check({"t": "ref", "ref": "Ts2AnchorRefV1"}, dict(span, factId="x"), "a"), "TYPE_NULL")
        line = self.s.lines("identityModel3")[1891]
        expr = re.search(r"if not (.+?):raise", line).group(1)
        permits = eval(expr, {}, {"a": 4, "b": 4, "raw": b"0123456789", "len": len})  # exact pinned source expression
        rejects_inverted = not eval(expr, {}, {"a": 5, "b": 4, "raw": b"0123456789", "len": len})
        self.add("fact2-anchor-range-permits-empty", permits and rejects_inverted, expr)
        a1 = dict(span, path="b", contentSha256="f" * 64, startByte=0, endByte=1)
        a2 = dict(span, path="aa", contentSha256="0" * 64, startByte=0, endByte=1)
        manifest.update({"b": {"kind": "file", "byteLength": 1, "contentSha256": "f" * 64}, "aa": {"kind": "file", "byteLength": 1, "contentSha256": "0" * 64}})
        cbor_order = [x["path"] for x in sorted([a1, a2], key=W.encode)]
        cve1_order = [x["path"] for x in sorted([a1, a2], key=W.cve1)]
        self.add("anchor-order-languages-differ", cbor_order != cve1_order, {"ts2-cbor": cbor_order, "rust3-cve1": cve1_order})

    # ------------------------------------------------------------------
    def manifests(self):
        K = self.K
        snap = "snapshot2:" + "a" * 64
        entries = [{"path": "src/a.ts", "kind": "file", "byteLength": 3, "contentSha256": hashlib.sha256(b"abc").hexdigest(), "linkTarget": None},
                   {"path": "src/z.ts", "kind": "symlink", "byteLength": 0, "contentSha256": None, "linkTarget": "src/a.ts"}]
        digest = raw_hex(entries)
        man = {"snapshotId": snap, "manifestSha256": digest, "entries": entries}

        def raw():
            if hashlib.sha256(self.WI.wire_cbor(entries)).hexdigest() != digest:
                raise Refuse("ENCODER_DISAGREES_WITH_WIRE_MODEL")
            K.frame_payload("typescript-semantic", "SnapshotManifest", W.decode(W.encode(man), "ts2-cbor"))
            admit_manifest_digest(man)
            seal = {"snapshotId": snap, "manifestSha256": digest, "entryCount": 2, "totalFileBytes": 3, "totalChunkCount": 1}
            K.frame_payload("typescript-semantic", "SnapshotSeal", seal)
            K.frame_payload("typescript-semantic", "SnapshotAccepted", seal)
            admit_accepted(seal, dict(seal))
        self.expect("ts2-manifest-digest-raw", raw)
        self.expect("ts2-manifest-domain-form-refused",
                    lambda: K.frame_payload("typescript-semantic", "SnapshotManifest", dict(man, manifestSha256=C("opensip.ts-provider.snapshot-manifest.v1", entries))), "TEXT_PATTERN")
        self.expect("manifest-digest-mismatch-refused", lambda: admit_manifest_digest(dict(man, manifestSha256="0" * 64)), "MANIFEST_DIGEST")
        seal = {"snapshotId": snap, "manifestSha256": digest, "entryCount": 2, "totalFileBytes": 3, "totalChunkCount": 1}
        self.expect("accepted-echo-mismatch-refused", lambda: admit_accepted(seal, dict(seal, totalChunkCount=2)), "ACCEPTED_NOT_SEAL")

    # ------------------------------------------------------------------
    def depsrc(self):
        NE, K, fx = self.NE, self.K, self.fx
        row = fx["vendoredRow"]
        key = f'{row["name"]} {row["version"]} {row["sourceId"]}'
        adm = NE.dependency_source_set_admit(fx["lock"], [row], [key])
        pkgs = adm["descriptor"]["packages"]
        set_id = adm["identity"]
        entries = []
        for p in pkgs:
            pk = f'{p["name"]} {p["version"]} {p["sourceId"]}'
            for path in sorted(row["files"], key=lambda x: x.encode()):
                f = row["files"][path]
                entries.append({"packageKey": pk, "path": path, "byteLength": f["byteLength"], "contentSha256": f["sha256"]})
        digest = raw_hex(entries)
        man = {"dependencySourceSetId": set_id, "manifestSha256": digest, "entries": entries}

        def join():
            if not adm["admitted"] or NE.file_manifest_identity(row["files"]) != pkgs[0]["fileManifestSha256"]:
                raise Refuse("FILE_MANIFEST_JOIN")
            if pkgs[0]["fileCount"] != len(entries) or pkgs[0]["totalBytes"] != sum(e["byteLength"] for e in entries):
                raise Refuse("FILE_MANIFEST_COUNTS")
            K.frame_payload("rust-semantic", "DependencySourceManifest", man)
            admit_manifest_digest(man)
            chunk = {"dependencySourceSetId": set_id, "packageKey": key, "path": "Cargo.toml", "chunkIndex": 0, "byteOffset": 0, "bytes": b"a" * 100}
            K.frame_payload("rust-semantic", "DependencySourceChunk", W.decode(W.encode(chunk), "rust3-cbor"))
            seal = {"dependencySourceSetId": set_id, "manifestSha256": digest, "entryCount": 2, "totalBytes": 2100, "totalChunkCount": 3}
            K.frame_payload("rust-semantic", "DependencySourceSeal", seal)
            K.frame_payload("rust-semantic", "DependencySourceAccepted", seal)
        self.expect("depsrc-file-manifest-join", join)

        def non_self_ref():
            first = raw_hex(man["entries"])
            for trial in ("0" * 64, "f" * 64, digest):
                if raw_hex(dict(man, manifestSha256=trial)["entries"]) != first:
                    raise Refuse("RECIPE_DEPENDS_ON_OWN_FIELD")
        self.expect("depsrc-digest-non-self-referential", non_self_ref)
        fixed, x = False, "0" * 64
        for _ in range(4):
            y = hashlib.sha256(W.encode(dict(man, manifestSha256=x))).hexdigest()
            fixed = fixed or y == x
            x = y
        self.add("depsrc-self-referential-iteration-no-fixed-point", not fixed, "SHA-256 of the frame including its own digest never reproduced the digest in 4 iterations")

        def order_and_key():
            admit_depsrc_order(entries)
            K.check({"t": "ref", "ref": "Rust3PackageKey"}, key, "packageKey")
        self.expect("depsrc-order-and-key", order_and_key)
        self.expect("depsrc-order-refused", lambda: admit_depsrc_order(list(reversed(entries))), "DEPSRC_ORDER")
        self.expect("depsrc-key-grammar-refused", lambda: K.check({"t": "ref", "ref": "Rust3PackageKey"}, "serde-1.0.200", "packageKey"), "TEXT_PATTERN")

        def empty():
            m = {"dependencySourceSetId": set_id, "manifestSha256": hashlib.sha256(b"\x80").hexdigest(), "entries": []}
            K.frame_payload("rust-semantic", "DependencySourceManifest", m)
            admit_manifest_digest(m)
            K.frame_payload("rust-semantic", "DependencySourceSeal", {"dependencySourceSetId": set_id, "manifestSha256": m["manifestSha256"], "entryCount": 0, "totalBytes": 0, "totalChunkCount": 0})
        self.expect("depsrc-empty-set", empty)

    # ------------------------------------------------------------------
    def prepared(self):
        NE, K, fx = self.NE, self.K, self.fx
        prep = fx["prepGenerated"]
        admitted = NE.prepared_output_set_admit(prep, fx["ctx"], True)
        entries = [{"outputOrdinal": i, "kind": r["kind"], "planRow": r,
                    "logicalPath": f".opensip/prepared/v3/{i}-{r['blob']['sha256']}.blob",
                    "blobByteLength": r["blob"]["byteLength"], "blobSha256": r["blob"]["sha256"],
                    "contentByteLength": r["blob"]["byteLength"], "contentSha256": r["blob"]["sha256"]} for i, r in enumerate(prep["rows"])]
        plan = "plan2:" + "b" * 64
        man = {"planId": plan, "manifestSha256": raw_hex(entries), "entries": entries}

        def build():
            if admitted["outcome"] != "admitted":
                raise Refuse("FIXTURE_SET_NOT_ADMITTED", admitted["outcome"])
            K.frame_payload("rust-semantic", "PreparedOutputManifest", man)
            admit_manifest_digest(man)
            for e in entries:
                if e["planRow"]["inputBinding"]["dependencySourceSetId"] != fx["ctx"]["dependencySourceSetId"]:
                    raise Refuse("PREPARED_BINDING")
            total = sum(e["blobByteLength"] for e in entries)
            seal = {"planId": plan, "manifestSha256": man["manifestSha256"], "entryCount": len(entries), "totalBlobBytes": total, "totalChunkCount": 1}
            K.frame_payload("rust-semantic", "PreparedOutputSeal", seal)
            K.frame_payload("rust-semantic", "PreparedOutputAccepted", seal)
            K.frame_payload("rust-semantic", "PreparedOutputChunk", {"planId": plan, "outputOrdinal": 0, "chunkIndex": 0, "byteOffset": 0, "bytes": b"x"})
        self.expect("prepared-v3-entries-from-set", build)
        gen = [e["planRow"] for e in entries if e["kind"] == "generated-file"]
        self.add("prepared-v3-generated-blob-equality", bool(gen) and all(r["generated"]["blob"] == r["blob"] for r in gen), str(len(gen)))
        rebuilt = {"schemaVersion": 3, "preparation": prep["preparation"], "rows": [e["planRow"] for e in entries]}
        self.add("prepared-v3-set-identity-join", NE.prepared_output_set_identity(rebuilt) == NE.prepared_output_set_identity(prep), "")
        v2 = copy.deepcopy(man)
        v2["entries"][0]["planRow"] = {"packageId": "p", "cfg": [], "outputDigest": "0" * 64}
        self.expect("prepared-v3-v2-planrow-refused", lambda: K.frame_payload("rust-semantic", "PreparedOutputManifest", v2), "EXTERN_SCHEMA")
        v2kind = copy.deepcopy(man)
        v2kind["entries"][0]["kind"] = "build-script"
        self.expect("prepared-v3-v2-kind-refused", lambda: K.frame_payload("rust-semantic", "PreparedOutputManifest", v2kind), "ENUM")

    # ------------------------------------------------------------------
    def overlay_run(self, events, stage_count=1):
        NE = self.NE
        rules = copy.deepcopy(NE.PROTOCOL3_RULES)
        for r in rules:
            r.setdefault("guard", {}).update(self.wire["protocols"]["rust-semantic"]["transitions"]["guardAdditions"].get(r["id"], {}))
        pre = set(self.s.p3["wildcards"]["*PRE_COMPLETE"]["phases"])
        pf = set(self.s.p3["wildcards"]["*PROCESS_FAULT"]["frames"])
        src = {f for u in self.s.p3["stateUpdates"] if "sourceBytesSent" in u["sets"] for f in u.get("onFrames", [])}
        state = dict(self.s.p3["initialState"], outputSeen=False)
        trace = []
        for ev in events:
            phase, frame = state["phase"], ev["frame"]
            if phase == "FAULT":
                trace.append("FAULT-absorb"); continue
            if phase in ("WAIT_ZERO_EXIT", "WAIT_EOF", "DONE") and frame not in ("zero-exit", "eof") and frame not in pf:
                state["phase"] = "FAULT"; trace.append("post-terminal-frame"); continue
            if frame in pf:
                state["phase"] = "FAULT"; trace.append("P3-33"); continue
            match = None
            for r in rules:
                if r["phase"] == "*ANY" or (r["phase"] == "*PRE_COMPLETE" and phase not in pre) or (r["phase"] not in ("*PRE_COMPLETE",) and r["phase"] != phase):
                    continue
                if r["frame"] == frame and all(state.get(k) == v for k, v in r.get("guard", {}).items()):
                    match = r; break
            if match is None:
                state["phase"] = "FAULT"; trace.append("P3-34"); continue
            if frame == "HelloAck":
                state["identityNegotiated"] = all(t in ev.get("capabilities", []) for t in NE.IDENTITY_TOKENS)
            if frame == "OpenUniverse":
                state["dependencyMode"], state["preparedMode"] = bool(ev.get("dependencyMode")), bool(ev.get("preparedMode"))
            if frame == "Analyze":
                state["stageCount"], state["stageIndex"], state["outputSeen"] = stage_count, 0, False
            if frame in ("FactBatch", "CoverageV3"):
                state["outputSeen"] = True
            if frame in src:
                state["sourceBytesSent"] = True
            nxt = match["next"]
            if nxt == "ANALYZING_OR_READY_COMPLETE":
                state["stageIndex"] += 1; state["stagesCompleted"] += 1
                nxt = "READY_COMPLETE" if state["stageIndex"] == state["stageCount"] else "ANALYZING"
            if "terminal" in match:
                state["terminalKind"] = match["terminal"]
            state["phase"] = nxt; trace.append(match["id"])
        return {"finalPhase": state["phase"], "terminalKind": state["terminalKind"], "trace": trace}

    def transitions(self):
        NE, ST = self.NE, self.ST
        f = lambda *names: [{"frame": n} for n in names]
        caps = {"frame": "HelloAck", "capabilities": list(NE.IDENTITY_TOKENS)}
        head = f("Hello") + [caps, {"frame": "OpenUniverse", "dependencyMode": True, "preparedMode": False}] + f(
            "UniverseAccepted", "SnapshotManifest", "SnapshotFileChunk", "SnapshotSeal", "SnapshotAccepted",
            "DependencySourceManifest", "DependencySourceChunk", "DependencySourceSeal", "DependencySourceAccepted")
        prepared_head = f("Hello") + [caps, {"frame": "OpenUniverse", "dependencyMode": True, "preparedMode": True}] + f(
            "UniverseAccepted", "SnapshotManifest", "SnapshotSeal", "SnapshotAccepted", "DependencySourceManifest", "DependencySourceSeal",
            "DependencySourceAccepted", "PreparedOutputManifest", "PreparedOutputChunk", "PreparedOutputSeal", "PreparedOutputAccepted")
        base = head + f("NativeContextVerified", "Analyze")
        tail = f("zero-exit", "eof")
        traces = {
            "complete": (base + f("FactBatch", "CoverageV3", "Complete") + tail, 1),
            "two-stage": (base + f("FactBatch", "CoverageV3", "CoverageV3", "Complete") + tail, 2),
            "prepared": (prepared_head + f("NativeContextVerified", "Analyze", "CoverageV3", "Complete") + tail, 1),
            "unavailable-before-output": (base + f("Unavailable") + tail, 1),
            "pre-analyze-unavailable": (head + f("Unavailable") + tail, 1),
            "budget": (base + f("FactBatch", "BudgetExhausted") + tail, 1),
            "fault": (head[:4] + f("ProviderFault") + tail, 1),
            "cancel": (head[:6] + f("Cancel", "Cancelled") + tail, 1),
            "cancel-start": (f("Cancel"), 1),
            "no-identity": (f("Hello", "HelloAck", "OpenUniverse"), 1),
            "post-terminal": (base + f("Unavailable", "FactBatch"), 1),
        }
        diffs = {}
        for name, (ev, n) in traces.items():
            a, b = NE.protocol3_run(ev, stage_count=n), self.overlay_run(ev, n)
            if (a["finalPhase"], a["terminalKind"], a["trace"]) != (b["finalPhase"], b["terminalKind"], b["trace"]):
                diffs[name] = [a["trace"], b["trace"]]
        self.add("p3-overlay-differential", not diffs, diffs or sorted(traces))
        after = base + f("FactBatch", "Unavailable")
        after_cov = base + f("CoverageV3", "Unavailable")
        m, o, o2 = NE.protocol3_run(after, 1), self.overlay_run(after, 1), self.overlay_run(after_cov, 2)
        self.add("p3-unavailable-after-output-faults", o["finalPhase"] == "FAULT" and o["trace"][-1] == "P3-34" and o2["finalPhase"] == "FAULT"
                 and m["trace"][-1] == "P3-25", {"publishedTable": m["trace"][-2:], "overlay": o["trace"][-2:]})
        ob = self.overlay_run(base + f("Unavailable") + tail, 1)
        self.add("p3-unavailable-before-output-admits", ob["finalPhase"] == "DONE" and "P3-25" in ob["trace"], ob["trace"][-3:])
        cs = NE.protocol3_run(f("Cancel"))
        self.add("p3-cancel-in-start-no-row", cs["trace"] == ["P3-34"] and self.overlay_run(f("Cancel"))["trace"] == ["P3-34"], cs["trace"])
        tcaps = {"frame": "HelloAck", "capabilities": list(ST.IDENTITY_TOKENS)}
        tbase = f("Hello") + [tcaps] + f("OpenUniverse", "UniverseAccepted", "SnapshotManifest", "SnapshotSeal", "SnapshotAccepted", "NativeContextVerified", "Analyze")
        post = {"frame": "Unavailable", "unavailablePayload": "post-analyze"}
        t_after = ST.typescript_protocol2_run(tbase + f("FactBatch") + [post])
        t_before = ST.typescript_protocol2_run(tbase + [post])
        t_start = ST.typescript_protocol2_run(f("Cancel"))
        self.add("ts2-order-unchanged", t_after["finalPhase"] == "FAULT" and t_before["trace"][-1] == "T2-14" and t_start["trace"] == ["T2-18"],
                 [t_after["trace"][-1], t_before["trace"][-1], t_start["trace"]])

    # ------------------------------------------------------------------
    def commitments(self):
        K, WI = self.K, self.WI
        payload = {"name": "x"}
        anchor = {"kind": "source-span", "snapshotId": "snapshot2:" + "a" * 64, "path": "src/a.ts", "contentSha256": "1" * 64, "startByte": 0, "endByte": 1, "factId": None}
        vec = {"candidateOrdinal": 0, "relation": "declares", "resolution": "syntactic", "layer": "syntax", "producer": "typescript-semantic",
               "producerVersion": "typescript-provider 1.0.0", "schemaVersion": 1, "language": "typescript", "sourceUniverseId": "sha256:" + "1" * 64,
               "targetUniverseId": "sha256:" + "1" * 64, "confidenceMillionths": 1000000, "relationSchemaId": "opensip.relation.declares.v1",
               "canonicalRelationPayloadHex": W.encode(payload).hex(), "decodedRelationPayload": payload, "anchors": [anchor]}
        wire_c = {k: v for k, v in vec.items() if k not in ("canonicalRelationPayloadHex", "decodedRelationPayload")}
        wire_c["canonicalRelationPayload"] = W.encode(payload)
        commit = C("opensip.ts-provider.fact-batch.v1", [wire_c])

        def fb():
            out = WI.admit_fact_batch("typescript-semantic", {"analysisOrdinal": 0, "stageId": "s1", "batchIndex": 0, "facts": [vec], "batchCommitment": commit}, [])
            if not out["batchCommitmentVerified"] or out["wireCandidatesCborHex"] != W.encode([wire_c]).hex():
                raise Refuse("WIRE_MODEL_DISAGREES")
            wire_batch = {"analysisOrdinal": 0, "stageId": "s1", "batchIndex": 0, "facts": [wire_c], "batchCommitment": commit}
            K.frame_payload("typescript-semantic", "FactBatch", W.decode(W.encode(wire_batch), "ts2-cbor"), "false")
        self.expect("commit-ts2-fact-batch-matches-wire-model", fb)
        self.add("commit-empty-stream", W.encode([]) == b"\x80" and C("opensip.rust-provider.stage-facts.v2", []) == "sha256:" + hashlib.sha256(b"opensip.rust-provider.stage-facts.v2\x00\x80").hexdigest(), "")
        rust_c = dict(wire_c, producer="rust-semantic", language="rust", producerVersion="rust-provider 1.0.0")
        rust_v3 = {"schemaVersion": 3, "analysisOrdinal": 0, "stageId": "s1", "batchIndex": 0, "candidates": [rust_c], "occupancyCompanions": []}
        self.expect("wire-fact-batch-v3-rust3", lambda: K.frame_payload("rust-semantic", "FactBatch", W.decode(W.encode(rust_v3), "rust3-cbor"), "true"))
        self.expect("wire-fact-batch-v3-without-token-refused", lambda: K.frame_payload("rust-semantic", "FactBatch", rust_v3, "false"), "UNKNOWN_MEMBER")
        self.expect("wire-hex-vector-member-refused", lambda: K.check({"t": "ref", "ref": "Rust3FactCandidateV1"}, dict(rust_c, canonicalRelationPayloadHex="00"), "c"), "UNKNOWN_MEMBER")
        self.expect("wire-ts-producer-const", lambda: K.check({"t": "ref", "ref": "Ts2FactCandidateV1"}, rust_c, "c"), "CONST")

    # ------------------------------------------------------------------
    def wire_examples(self):
        K = self.K
        snap = "snapshot2:" + "a" * 64
        chunk = {"snapshotId": snap, "path": "src/a.ts", "chunkIndex": 0, "byteOffset": 0, "bytes": b"abc"}
        self.expect("wire-ts2-chunk-roundtrip", lambda: K.frame_payload("typescript-semantic", "SnapshotFileChunk", W.decode(W.encode(chunk), "ts2-cbor")))
        neg = W.encode(dict(chunk, chunkIndex=-1))
        self.expect("wire-ts2-negative-int-decodes-then-type-refuses", lambda: K.frame_payload("typescript-semantic", "SnapshotFileChunk", W.decode(neg, "ts2-cbor")), "TYPE_UINT64")
        self.expect("wire-rust3-negative-int-forbidden", lambda: W.decode(neg, "rust3-cbor"), "NEGATIVE_INTEGER_FORBIDDEN")
        self.expect("wire-non-shortest", lambda: W.decode(b"\x18\x05", "rust3-cbor"), "NON_SHORTEST")
        self.expect("wire-map-order", lambda: W.decode(b"\xa2" + W.encode("b") + W.encode(1) + W.encode("a") + W.encode(1), "ts2-cbor"), "MAP_ORDER")
        self.expect("wire-length-first-map-order", lambda: W.decode(b"\xa2" + W.encode("aa") + W.encode(1) + W.encode("b") + W.encode(1), "rust3-cbor"), "MAP_ORDER")
        self.expect("wire-duplicate-key", lambda: W.decode(b"\xa2" + W.encode("a") + W.encode(1) + W.encode("a") + W.encode(1), "ts2-cbor"), "DUPLICATE_KEY")
        self.expect("wire-float", lambda: W.decode(b"\xf9\x00\x00", "ts2-cbor"), "FLOAT_OR_SIMPLE")
        self.expect("wire-tag", lambda: W.decode(b"\xc0\x60", "rust3-cbor"), "TAG")
        self.expect("wire-indefinite", lambda: W.decode(b"\x5f\xff", "ts2-cbor"), "INDEFINITE_OR_RESERVED")
        self.expect("wire-non-nfc", lambda: W.decode(W.encode("é"), "rust3-cbor"), "NON_NFC")
        self.expect("wire-bytes-as-hex-text", lambda: K.frame_payload("typescript-semantic", "SnapshotFileChunk", dict(chunk, bytes="616263")), "TYPE_BYTES")
        self.expect("wire-bytes-as-json-array", lambda: K.frame_payload("rust-semantic", "SnapshotFileChunk", dict(chunk, bytes=[97, 98, 99])), "TYPE_BYTES")
        self.expect("wire-bytes-empty", lambda: K.frame_payload("rust-semantic", "SnapshotFileChunk", dict(chunk, bytes=b"")), "BYTES_BOUND")
        self.expect("wire-unknown-member", lambda: K.frame_payload("rust-semantic", "SnapshotFileChunk", dict(chunk, extra=1)), "UNKNOWN_MEMBER")
        self.expect("wire-missing-member", lambda: K.frame_payload("rust-semantic", "SnapshotFileChunk", {k: v for k, v in chunk.items() if k != "path"}), "MISSING_MEMBER")
        cancel = {"executionId": None, "analysisOrdinal": None, "reason": "user-interrupt"}
        self.expect("wire-ts2-cancel-null-present", lambda: K.frame_payload("typescript-semantic", "Cancel", cancel))
        self.expect("wire-ts2-cancel-null-omitted-refused", lambda: K.frame_payload("typescript-semantic", "Cancel", {"analysisOrdinal": None, "reason": "user-interrupt"}), "MISSING_MEMBER")
        self.expect("wire-ts2-execution-id-grammar", lambda: K.frame_payload("typescript-semantic", "Cancel", dict(cancel, executionId="exec1_" + "0" * 32 + "\n")), "TEXT_PATTERN")

        def rust_cancel():
            K.frame_payload("rust-semantic", "Cancel", {"executionId": "exec1_" + "0" * 32, "analysisOrdinal": 0, "reason": "user-interrupt"})
            K.frame_payload("rust-semantic", "Cancelled", {"executionId": None, "analysisOrdinal": None, "observedPhase": "RECEIVING_DEPENDENCY"})
            K.frame_payload("rust-semantic", "ProviderFault", {"executionId": None, "analysisOrdinal": None, "phase": "WAIT_HELLO_ACK", "faultKind": "input-rejected", "detailCode": "x"})
        self.expect("rust3-cancel-types", rust_cancel)
        self.expect("rust3-cancel-host-shutdown-refused", lambda: K.frame_payload("rust-semantic", "Cancel", dict(cancel, reason="host-shutdown")), "CONST")
        self.expect("rust3-cancelled-start-phase-refused", lambda: K.frame_payload("rust-semantic", "Cancelled", {"executionId": None, "analysisOrdinal": None, "observedPhase": "START"}), "ENUM")
        stage = {"kind": "fact-derivation", "stageId": "s1", "relations": ["calls"], "operator": "semantic-provider"}
        self.expect("wire-optional-absent", lambda: K.check({"t": "ref", "ref": "Rust3C2PlanStageV3"}, stage, "planStage"))
        self.expect("wire-optional-null-refused", lambda: K.check({"t": "ref", "ref": "Rust3C2PlanStageV3"}, dict(stage, budget=None), "planStage"), "TYPE_MAP")
        pre = {"executionId": "exec1_" + "0" * 32, "snapshotId": snap, "planId": "plan2:" + "b" * 64, "reason": "native-context-mismatch",
               "nativeContextId": "sha256:" + "1" * 64, "recomputedNativeContextId": "sha256:" + "2" * 64}
        self.expect("wire-unavailable-pre-analyze-selected", lambda: K.frame_payload("rust-semantic", "Unavailable", pre, "WAIT_NATIVE_CONTEXT_VERIFIED"))
        self.expect("wire-unavailable-pre-analyze-in-analyzing-refused", lambda: K.frame_payload("rust-semantic", "Unavailable", pre, "ANALYZING"), "EXTERN_SCHEMA")
        self.expect("wire-unavailable-unlawful-selector", lambda: K.frame_payload("typescript-semantic", "Unavailable", pre, "READY_ANALYZE"), "SELECTOR_UNLAWFUL")
        self.expect("wire-ts2-no-coveragev3-frame", lambda: K.frame_payload("typescript-semantic", "CoverageV3", {}), "UNKNOWN_FRAME")
        self.expect("wire-rust3-no-coverage-frame", lambda: K.frame_payload("rust-semantic", "Coverage", {}), "UNKNOWN_FRAME")
        env = {"protocolMajor": 3, "direction": "host-to-worker", "sequence": 0, "frameType": "SnapshotFileChunk", "payload": chunk}
        self.expect("wire-rust3-envelope", lambda: K.check_record("Rust3ProviderFrameV3", W.decode(W.encode(env), "rust3-cbor")))
        self.expect("wire-ts2-envelope-major-refused", lambda: K.check_record("Ts2FrameV2", {"protocolMajor": 3, "frameType": "Hello", "sequence": 0, "payload": {}}), "CONST")
        file_e = {"path": "src/lib.rs", "kind": "file", "byteLength": 1, "contentSha256": "1" * 64, "executable": False, "targetBytes": None}
        link_e = {"path": "src/link.rs", "kind": "symlink", "byteLength": None, "contentSha256": None, "executable": None, "targetBytes": b"lib.rs"}
        self.expect("wire-rust3-snapshot-variants", lambda: [K.check_record("Rust3SnapshotEntryV2", e) for e in (file_e, link_e)])
        self.expect("wire-rust3-symlink-executable-refused", lambda: K.check_record("Rust3SnapshotEntryV2", dict(link_e, executable=False)), "TYPE_NULL")
        big = "é" * 4096
        schema_accepts = not list(Draft202012Validator({"$ref": CM.HS + "#/$defs/IdentityText"}, registry=self.reg).iter_errors(big))
        try:
            K.check({"t": "ref", "ref": "Rust3IdentityText"}, big, "id"); code = None
        except Refuse as exc:
            code = exc.code
        self.add("json-schema-maxlength-not-byte-bound", schema_accepts and code == "TEXT_UTF8_BYTES", {"schemaAccepts": schema_accepts, "carrier": code})
        budget = {"analysisOrdinal": 0, "triggerStageId": "s1", "unit": "work-units", "limit": 7, "observed": 8, "coverage": [], "coverageCommitment": C("opensip.rust-provider.coverage-stream.v2", [])}

        def observed():
            K.frame_payload("rust-semantic", "BudgetExhausted", budget)
            admit_budget_observed(budget)
            try:
                admit_budget_observed(dict(budget, observed=7))
            except Refuse:
                return
            raise Refuse("OBSERVED_EQUAL_LIMIT_ADMITTED")
        self.expect("rust3-observed-limit-plus-one", observed)

    def run(self):
        for step in (self.scope2, self.anchors, self.manifests, self.depsrc, self.prepared, self.transitions, self.commitments, self.wire_examples):
            try:
                step()
            except Exception as exc:  # noqa: BLE001
                self.add("step:" + step.__name__, False, type(exc).__name__ + ": " + str(exc)[:400])
        return self.results
