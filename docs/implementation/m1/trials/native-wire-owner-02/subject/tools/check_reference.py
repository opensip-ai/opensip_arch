"""Reference-owner, admission-vector and wire-example checks (candidate 02). Runs the pinned reference models
(native_evidence_model.v2, provider_startup_model.v1, provider_wire_model.v1) where they apply; never claims product
execution. Architecture pins are verified by check.py before this module imports any model."""
import copy, hashlib, importlib.util, json, re
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

import admission_ref as AR
import common as CM
import wirecodec as W

Refuse = W.Refuse
SNAP = "snapshot2:" + "a" * 64
PLAN = "plan2:" + "b" * 64


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


C, raw_hex = AR.C, AR.raw_hex


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


class Reference:
    def __init__(self, arch, subject, static):
        native = Path(arch) / "docs/coop/design-corrections/native"
        self.NE = load("ref_ne", native / "native_evidence_model.v2.py")
        self.ST = load("ref_st", native / "provider_startup_model.v1.py")
        self.WI = load("ref_wi", native / "provider_wire_model.v1.py")
        self.s = static
        self.wire = static.wire
        self.p3 = static.p3
        self.reg = Registry().with_resources([(d["$id"], Resource(contents=d, specification=DRAFT202012)) for d in static.docs.values()])
        self.K = W.Carriers(self.wire, self.extern)
        cases = json.loads(static.raw["nativeCases"])
        self.fx = cases["fixtures"]
        self.cov_fx = find(cases, "scopeDescriptor")
        self.tokens = list(self.NE.IDENTITY_TOKENS)
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
        if gen == "Native2DependencySourceManifestV3":
            for e in v["entries"]:
                W.lexical("canonical-path-segments", e["path"], where + ".entries.path")
                W.split_package_key(e["packageKey"])

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
        return got == code

    # ------------------------------------------------------------------ vectors
    def expand(self, x):
        if isinstance(x, dict):
            if "$bytesHex" in x:
                return bytes.fromhex(x["$bytesHex"])
            if "$repeat" in x:
                item = self.expand(x["$repeat"]["item"])
                return [item] * x["$repeat"]["n"]
            if "$concat" in x:
                return [e for part in x["$concat"] for e in self.expand(part)]
            if "$scopeDescriptor" in x:
                d = dict(self.cov_fx["scopeDescriptor"], **x["$scopeDescriptor"])
                return self.NE.subject_scope_descriptor(d["snapshotId"], d["relation"], d["resolution"], d["sourceUniverse"],
                                                        d["targetUniverse"], d["enumeratorClosure"], d["subjects"])
            if "$ownerCommit" in x:
                o = x["$ownerCommit"]
                if o["doc"] == "rust2":
                    domain = re.search(r"UTF8\(([^)]+)\)", self.s.r2["commitments"][o["recipe"]]).group(1)
                else:
                    domain = self.s.w2["commitments"]["domains"][o["recipe"]]
                return {"$domain": domain, "value": o["value"]}
            if "$inheritedTsPerStage" in x:
                return C("opensip.coverage.subject-scope.v1", [{"path": s} for s in self.cov_fx["scopeDescriptor"]["subjects"]])
            return {k: self.expand(v) for k, v in x.items()}
        if isinstance(x, list):
            return [self.expand(v) for v in x]
        return x

    def run_vector(self, rid, inp):
        doc, NE = self.wire, self.NE
        if rid in ("CANONICAL-PATH-ADMISSION", "TS2-LOGICAL-PATH-ADMISSION"):
            return AR.path_admission(doc, rid, inp["path"])
        if rid == "PACKAGE-KEY-JOIN":
            return AR.package_key_join(doc, inp["packages"], inp["key"])
        if rid == "DEPSRC-SET-KEY-CONSTRAINTS":
            return AR.depsrc_set_key_constraints(doc, inp["packages"])
        if rid == "DEPSRC-CUSTODY":
            return AR.depsrc_custody(doc, inp["packages"], inp["manifest"])
        if rid == "PREPARED-V3-WIRE-LIMIT":
            return AR.prepared_wire_limit(doc, inp["set"], PLAN)
        if rid == "PREPARED-V3-ENTRY":
            prep = copy.deepcopy(self.fx[inp["setFixture"]])
            mut = inp.get("mutate", {})
            if "generatedBlobSha256" in mut:
                next(r for r in prep["rows"] if r["kind"] == "generated-file")["generated"]["blob"]["sha256"] = mut["generatedBlobSha256"]
            entries = AR.prepared_entries(prep["rows"])
            if "entry" in mut:
                entries[mut["entry"]]["contentSha256"] = mut["contentSha256"]
            self.K.frame_payload("rust-semantic", "PreparedOutputManifest", {"planId": PLAN, "manifestSha256": raw_hex(entries), "entries": entries})
            return AR.prepared_entry_join(entries)
        if rid == "RUST3-PROVIDER-FAULT":
            self.K.frame_payload("rust-semantic", "ProviderFault", inp["fault"])
            return AR.provider_fault(doc, self.p3, self.tokens, inp["events"], inp["fault"])
        if rid == "P3-OVERLAY":
            res = AR.overlay_run(doc, self.p3, self.tokens, inp["events"], inp["stageCount"])
            if res["finalPhase"] == "FAULT":
                raise Refuse(res["trace"][-1])
            if inp.get("tail") not in res["trace"]:
                raise Refuse("OVERLAY_TAIL_MISSING")
            return None
        if rid == "COMMIT-MAP":
            want = inp["commitment"]
            stages = inp["stages"]
            value = stages[-1] if want["value"] == "stage" else [e for s in stages for e in s]
            if AR.commit_value(doc, inp["field"], stages) != C(want["$domain"], value):
                raise Refuse("COMMIT_MISMATCH")
            return None
        if rid in ("ANCHOR-WIRE-SPAN", "ANCHOR-FACT-REF-REFUSED"):
            return AR.anchor_admission(doc, inp["language"], inp["anchors"], inp["manifest"], SNAP, W.cve1)
        if rid in ("TS2-MANIFEST-DIGEST", "RAW-MANIFEST-DIGEST"):
            return AR.manifest_digest(inp["manifest"])
        if rid == "ACCEPTED-EQUALS-SEAL":
            return AR.accepted_equals_seal(inp["seal"], inp["accepted"])
        if rid == "CHUNK-CUSTODY":
            return AR.chunk_custody(inp["entry"], inp["chunks"])
        if rid == "SEAL-AGGREGATES":
            return AR.seal_aggregates(inp["entries"], inp["chunkCount"], inp["seal"], inp["total"])
        if rid == "CANCEL-NULLABILITY":
            return AR.cancel_nullability(inp["sent"], inp["cancel"])
        if rid == "CANCELLED-ECHO":
            return AR.cancelled_echo(inp["cancel"], inp["cancelled"])
        if rid == "RUST3-CANCEL-TYPES":
            self.K.frame_payload("rust-semantic", "Cancelled", inp["cancelled"])
            return AR.cancelled_echo(inp["cancel"], inp["cancelled"], inp["hostSendPhase"])
        if rid == "RUST3-BUDGET-EXHAUSTED":
            return AR.budget_observed(doc, inp["payload"], inp["planBudget"])
        if rid == "OCCUPANCY-JOIN":
            return AR.occupancy_join(inp["batch"])
        if rid == "PER-KEY-SCOPE2":
            desc = inp["descriptor"]
            commitment = inp["commitment"] if "commitment" in inp else NE.subject_scope_commitment(inp["commitmentOf"])["subjectScopeCommitment"]
            return AR.per_key_scope2(doc, NE.C.identity, desc, commitment)
        raise Refuse("NO_VECTOR_HANDLER", rid)

    def vectors(self):
        for rid, vecs in self.s.vectors["vectors"].items():
            oks = []
            for vec in vecs:
                inp = self.expand(vec["input"])
                code = vec["expect"] if vec["kind"] == "refuse" else None
                oks.append(self.expect(f"vector:{rid}:{vec['id']}", lambda: self.run_vector(rid, inp), code))
            self.add("vectors:" + rid, all(oks) and len(oks) >= 2, f"{sum(oks)}/{len(oks)}")

    # ------------------------------------------------------------------ owner runs
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
            frame = {"analysisOrdinal": 0, "stageId": "s1", "entries": [payload], "coverageCommitment": C("opensip.ts-provider.stage-coverage.v1", [payload])}
            K.frame_payload("typescript-semantic", "Coverage", frame)
            ST.admit_coverage_frame("typescript-semantic", frame, "s1", [ts_key])
            if NE.admit_coverage_result_v3(payload, desc, [])["result"] != "ADMIT":
                raise Refuse("NOT_ADMITTED")
            AR.per_key_scope2(self.wire, NE.C.identity, desc, ts_key["subjectScopeCommitment"])
        self.expect("scope2-ts2-admits", ts)

        def rs():
            K.check({"t": "ref", "ref": "Rust3CoverageKeyV2"}, rs_key, "key")
            frame = {"analysisOrdinal": 0, "stageId": "s1", "entries": [payload], "coverageCommitment": C("opensip.rust-provider.stage-coverage.v2", [payload])}
            K.frame_payload("rust-semantic", "CoverageV3", frame)
            ST.admit_coverage_frame("rust-semantic", frame, "s1", [rs_key])
            if NE.admit_coverage_result_v3(payload, desc, [])["result"] != "ADMIT":
                raise Refuse("NOT_ADMITTED")
        self.expect("scope2-rust3-admits", rs)
        refused = []
        for value in (C("opensip.coverage.subject-scope.v1", [{"path": s} for s in desc["subjects"]]), C("opensip.rust-provider.subject-scope.v2", desc["subjects"])):
            bad = copy.deepcopy(payload)
            bad["key"]["subjectScopeCommitment"] = value
            bad["entry"]["examinedUniverse"]["subjectScopeCommitment"] = value
            out = NE.admit_coverage_result_v3(bad, desc, [])
            refused.append(out["result"] == "REFUSE" and "native.subject-scope-commitment-mismatch" in out["refusals"])
        self.add("scope2-per-stage-value-refused", all(refused), refused)
        other = [NE.subject_scope_descriptor(desc["snapshotId"], desc["relation"], r, desc["sourceUniverse"], t, desc["enumeratorClosure"], desc["subjects"])
                 for r, t in (("syntactic-name-match", desc["targetUniverse"]), (desc["resolution"], "f" * 64))]
        self.add("scope2-keys-differ", len({NE.subject_scope_commitment(d)["subjectScopeCommitment"] for d in [desc] + other}) == 3, "")

    def anchors(self):
        line = self.s.lines("identityModel3")[1891]
        expr = re.search(r"if not (.+?):raise", line).group(1)
        permits = eval(expr, {}, {"a": 4, "b": 4, "raw": b"0123456789", "len": len})  # exact pinned source expression
        self.add("fact2-anchor-range-permits-empty", permits and not eval(expr, {}, {"a": 5, "b": 4, "raw": b"0123456789", "len": len}), expr)
        span = {"kind": "source-span", "snapshotId": SNAP, "path": "b", "contentSha256": "1" * 64, "startByte": 0, "endByte": 1, "factId": None}
        a1, a2 = dict(span, contentSha256="f" * 64), dict(span, path="aa", contentSha256="0" * 64)
        cb, cv = [x["path"] for x in sorted([a1, a2], key=W.encode)], [x["path"] for x in sorted([a1, a2], key=W.cve1)]
        self.add("anchor-order-languages-differ", cb != cv, {"ts2-cbor": cb, "rust3-cve1": cv})
        p1, p2 = dict(span), dict(span, path="aa")
        self.add("anchor-order-path-only-same", [x["path"] for x in sorted([p1, p2], key=W.encode)] == [x["path"] for x in sorted([p1, p2], key=W.cve1)], "")
        self.expect("anchor-fact-ref-refused", lambda: AR.anchor_admission(self.wire, "rust-semantic", [{"kind": "fact-ref", "snapshotId": None, "path": None, "contentSha256": None, "startByte": None, "endByte": None, "factId": "x"}], {}, SNAP, W.cve1), "ANCHOR_FACT_REF_UNDER_FACT2")
        self.expect("anchor-empty-interval-refused-on-wire", lambda: AR.anchor_admission(self.wire, "typescript-semantic", [dict(span, endByte=0)], {"b": {"kind": "file", "byteLength": 1, "contentSha256": "1" * 64}}, SNAP, W.cve1), "ANCHOR_EMPTY_OR_OUT_OF_BOUNDS")

    def manifests(self):
        K = self.K
        entries = [{"path": "src/a.ts", "kind": "file", "byteLength": 3, "contentSha256": hashlib.sha256(b"abc").hexdigest(), "linkTarget": None},
                   {"path": "src/z.ts", "kind": "symlink", "byteLength": 0, "contentSha256": None, "linkTarget": "../outside/" + "x" * 5000}]
        man = {"snapshotId": SNAP, "manifestSha256": raw_hex(entries), "entries": entries}

        def raw():
            if hashlib.sha256(self.WI.wire_cbor(entries)).hexdigest() != man["manifestSha256"]:
                raise Refuse("ENCODER_DISAGREES_WITH_WIRE_MODEL")
            K.frame_payload("typescript-semantic", "SnapshotManifest", W.decode(W.encode(man), "ts2-cbor"))
            AR.manifest_digest(man)
        self.expect("ts2-manifest-digest-raw", raw)
        self.expect("ts2-manifest-domain-form-refused", lambda: K.frame_payload("typescript-semantic", "SnapshotManifest", dict(man, manifestSha256=C("opensip.ts-provider.snapshot-manifest.v1", entries))), "TEXT_PATTERN")
        v = dict(entries[0])
        big = dict(v, path="a\n/../b")
        self.expect("wire-ts2-path-newline-dotdot-refused", lambda: K.check_record("Ts2SnapshotEntryV1", big), "PATH_LEXICAL")

    def depsrc(self):
        NE, K, fx = self.NE, self.K, self.fx
        row = fx["vendoredRow"]
        key = f'{row["name"]} {row["version"]} {row["sourceId"]}'
        adm = NE.dependency_source_set_admit(fx["lock"], [row], [key])
        pkgs = adm["descriptor"]["packages"]
        entries = [{"packageKey": key, "path": p, "byteLength": row["files"][p]["byteLength"], "contentSha256": row["files"][p]["sha256"]}
                   for p in sorted(row["files"], key=lambda x: x.encode())]
        man = {"dependencySourceSetId": adm["identity"], "manifestSha256": raw_hex(entries), "entries": entries}

        def join():
            if not adm["admitted"]:
                raise Refuse("FIXTURE_NOT_ADMITTED")
            AR.depsrc_custody(self.wire, pkgs, man, NE.file_manifest_identity)
            K.frame_payload("rust-semantic", "DependencySourceManifest", man)
            chunk = {"dependencySourceSetId": adm["identity"], "packageKey": key, "path": "Cargo.toml", "chunkIndex": 0, "byteOffset": 0, "bytes": b"a" * 100}
            K.frame_payload("rust-semantic", "DependencySourceChunk", W.decode(W.encode(chunk), "rust3-cbor"))
            seal = {"dependencySourceSetId": adm["identity"], "manifestSha256": man["manifestSha256"], "entryCount": 2, "totalBytes": 2100, "totalChunkCount": 3}
            K.frame_payload("rust-semantic", "DependencySourceSeal", seal)
            K.frame_payload("rust-semantic", "DependencySourceAccepted", seal)
        self.expect("depsrc-file-manifest-join", join)
        self.expect("depsrc-file-manifest-mismatch-refused", lambda: AR.depsrc_custody(self.wire, [dict(pkgs[0], fileManifestSha256="0" * 64)], man, NE.file_manifest_identity), "DEPSRC_FILE_MANIFEST")

        def non_self_ref():
            first = raw_hex(man["entries"])
            for trial in ("0" * 64, "f" * 64):
                if raw_hex(dict(man, manifestSha256=trial)["entries"]) != first:
                    raise Refuse("RECIPE_DEPENDS_ON_OWN_FIELD")
        self.expect("depsrc-digest-non-self-referential", non_self_ref)
        self.expect("depsrc-empty-set", lambda: AR.depsrc_custody(self.wire, [], {"dependencySourceSetId": adm["identity"], "manifestSha256": hashlib.sha256(b"\x80").hexdigest(), "entries": []}))
        self.expect("wire-depsrc-manifest-native-pattern-bypass-refused", lambda: K.frame_payload("rust-semantic", "DependencySourceManifest", dict(man, entries=[dict(entries[0], path="a\n//b")])), "PATH_LEXICAL")
        self.expect("wire-depsrc-chunk-empty-sourceid-key", lambda: K.frame_payload("rust-semantic", "DependencySourceChunk", {"dependencySourceSetId": adm["identity"], "packageKey": "a 1 ", "path": "src/lib.rs", "chunkIndex": 0, "byteOffset": 0, "bytes": b"x"}))

    def prepared(self):
        NE, K, fx = self.NE, self.K, self.fx
        prep = fx["prepGenerated"]
        admitted = NE.prepared_output_set_admit(prep, fx["ctx"], True)
        entries = AR.prepared_entries(prep["rows"])
        man = {"planId": PLAN, "manifestSha256": raw_hex(entries), "entries": entries}

        def build():
            if admitted["outcome"] != "admitted":
                raise Refuse("FIXTURE_SET_NOT_ADMITTED")
            AR.prepared_wire_limit(self.wire, prep, PLAN)
            K.frame_payload("rust-semantic", "PreparedOutputManifest", man)
            AR.prepared_entry_join(entries)
            seal = {"planId": PLAN, "manifestSha256": man["manifestSha256"], "entryCount": len(entries), "totalBlobBytes": sum(e["blobByteLength"] for e in entries), "totalChunkCount": 1}
            K.frame_payload("rust-semantic", "PreparedOutputSeal", seal)
            K.frame_payload("rust-semantic", "PreparedOutputAccepted", seal)
        self.expect("prepared-v3-entries-from-set", build)
        gen = [e["planRow"] for e in entries if e["kind"] == "generated-file"]
        self.add("prepared-v3-generated-blob-equality", bool(gen) and all(r["generated"]["blob"] == r["blob"] for r in gen), str(len(gen)))
        rebuilt = {"schemaVersion": 3, "preparation": prep["preparation"], "rows": [e["planRow"] for e in entries]}
        self.add("prepared-v3-set-identity-join", NE.prepared_output_set_identity(rebuilt) == NE.prepared_output_set_identity(prep), "")
        v2 = copy.deepcopy(man)
        v2["entries"][0]["planRow"] = {"packageId": "p", "cfg": [], "outputDigest": "0" * 64}
        self.expect("prepared-v3-v2-planrow-refused", lambda: K.frame_payload("rust-semantic", "PreparedOutputManifest", v2), "EXTERN_SCHEMA")
        big = {"planId": PLAN, "manifestSha256": "0" * 64, "entries": [dict(entries[0], outputOrdinal=i, logicalPath=f".opensip/prepared/v3/{i}-{entries[0]['blobSha256']}.blob") for i in range(257)]}
        self.expect("wire-prepared-257-entries-refused", lambda: K.frame_payload("rust-semantic", "PreparedOutputManifest", big), "ARRAY_BOUND")
        chunk = {"planId": PLAN, "outputOrdinal": 256, "chunkIndex": 0, "byteOffset": 0, "bytes": b"x"}
        self.expect("wire-prepared-ordinal-256-refused", lambda: K.frame_payload("rust-semantic", "PreparedOutputChunk", chunk), "UINT_BOUND")
        small = [{"packageId": 1}]
        self.add("encoded-length-exact", all(W.encoded_length(v) == len(W.encode(v)) for v in (man, small, {"x": [b"\x00" * 300, -70000, "é" * 70]})), "")

    def transitions(self):
        NE, ST = self.NE, self.ST
        vecs = self.s.vectors["vectors"]
        f = lambda *names: [{"frame": n} for n in names]
        caps = {"frame": "HelloAck", "capabilities": self.tokens}
        head = f("Hello") + [caps, {"frame": "OpenUniverse", "dependencyMode": True, "preparedMode": False}] + f(
            "UniverseAccepted", "SnapshotManifest", "SnapshotFileChunk", "SnapshotSeal", "SnapshotAccepted",
            "DependencySourceManifest", "DependencySourceChunk", "DependencySourceSeal", "DependencySourceAccepted")
        prepared_head = f("Hello") + [caps, {"frame": "OpenUniverse", "dependencyMode": True, "preparedMode": True}] + f(
            "UniverseAccepted", "SnapshotManifest", "SnapshotSeal", "SnapshotAccepted", "DependencySourceManifest", "DependencySourceSeal",
            "DependencySourceAccepted", "PreparedOutputManifest", "PreparedOutputChunk", "PreparedOutputSeal", "PreparedOutputAccepted")
        base = head + f("NativeContextVerified", "Analyze")
        tail = f("zero-exit", "eof")
        traces = {"complete": (base + f("FactBatch", "CoverageV3", "Complete") + tail, 1),
                  "two-stage": (base + f("FactBatch", "CoverageV3", "CoverageV3", "Complete") + tail, 2),
                  "prepared": (prepared_head + f("NativeContextVerified", "Analyze", "CoverageV3", "Complete") + tail, 1),
                  "unavailable-before-output": (base + f("Unavailable") + tail, 1),
                  "pre-analyze-unavailable": (head + f("Unavailable") + tail, 1),
                  "budget": (base + f("FactBatch", "BudgetExhausted") + tail, 1),
                  "fault": (head[:4] + f("ProviderFault") + tail, 1),
                  "cancel": (head[:6] + f("Cancel", "Cancelled") + tail, 1),
                  "cancel-start": (f("Cancel"), 1),
                  "no-identity": (f("Hello", "HelloAck", "OpenUniverse"), 1),
                  "post-terminal": (base + f("Unavailable", "FactBatch"), 1)}
        diffs = {}
        for name, (ev, n) in traces.items():
            a, b = NE.protocol3_run(ev, stage_count=n), AR.overlay_run(self.wire, self.p3, self.tokens, ev, n)
            if (a["finalPhase"], a["terminalKind"], a["trace"]) != (b["finalPhase"], b["terminalKind"], b["trace"]):
                diffs[name] = [a["trace"], b["trace"]]
        self.add("p3-overlay-differential", not diffs, diffs or sorted(traces))
        after = base + f("FactBatch", "Unavailable")
        m, o = NE.protocol3_run(after, 1), AR.overlay_run(self.wire, self.p3, self.tokens, after, 1)
        self.add("p3-unavailable-after-output-faults", o["finalPhase"] == "FAULT" and o["trace"][-1] == "P3-34" and m["trace"][-1] == "P3-25",
                 {"publishedTable": m["trace"][-2:], "overlay": o["trace"][-2:]})
        ob = AR.overlay_run(self.wire, self.p3, self.tokens, base + f("Unavailable") + tail, 1)
        self.add("p3-unavailable-before-output-admits", ob["finalPhase"] == "DONE" and "P3-25" in ob["trace"], ob["trace"][-3:])
        self.add("p3-cancel-in-start-no-row", NE.protocol3_run(f("Cancel"))["trace"] == ["P3-34"] and AR.overlay_run(self.wire, self.p3, self.tokens, f("Cancel"))["trace"] == ["P3-34"], "")
        race = [x["input"]["events"] for x in vecs["RUST3-PROVIDER-FAULT"] if x["id"] in ("fault-inflight-snapshot-manifest-unread", "fault-inflight-analyze-unread")]
        owner = [NE.protocol3_run(ev + [{"frame": "ProviderFault"}]) for ev in race]
        overlay = [AR.overlay_run(self.wire, self.p3, self.tokens, ev + [{"frame": "ProviderFault"}]) for ev in race]
        self.add("p3-race-traces-admitted-by-owner-table", len(race) == 2 and all(r["trace"][-1] == "P3-28" and r["terminalKind"] == "provider-fault" for r in owner + overlay),
                 [r["trace"][-2:] for r in owner])
        tcaps = {"frame": "HelloAck", "capabilities": list(ST.IDENTITY_TOKENS)}
        tbase = f("Hello") + [tcaps] + f("OpenUniverse", "UniverseAccepted", "SnapshotManifest", "SnapshotSeal", "SnapshotAccepted", "NativeContextVerified", "Analyze")
        post = {"frame": "Unavailable", "unavailablePayload": "post-analyze"}
        t_after, t_before, t_start = ST.typescript_protocol2_run(tbase + f("FactBatch") + [post]), ST.typescript_protocol2_run(tbase + [post]), ST.typescript_protocol2_run(f("Cancel"))
        self.add("ts2-order-unchanged", t_after["finalPhase"] == "FAULT" and t_before["trace"][-1] == "T2-14" and t_start["trace"] == ["T2-18"], [t_after["trace"][-1], t_before["trace"][-1], t_start["trace"]])

    def commitments(self):
        K, WI = self.K, self.WI
        payload = {"name": "x"}
        anchor = {"kind": "source-span", "snapshotId": SNAP, "path": "src/a.ts", "contentSha256": "1" * 64, "startByte": 0, "endByte": 1, "factId": None}
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
            K.frame_payload("typescript-semantic", "FactBatch", W.decode(W.encode({"analysisOrdinal": 0, "stageId": "s1", "batchIndex": 0, "facts": [wire_c], "batchCommitment": commit}), "ts2-cbor"), "false")
        self.expect("commit-ts2-fact-batch-matches-wire-model", fb)
        self.add("commit-empty-stream", W.encode([]) == b"\x80" and C("opensip.rust-provider.stage-facts.v2", []) == "sha256:" + hashlib.sha256(b"opensip.rust-provider.stage-facts.v2\x00\x80").hexdigest(), "")
        rust_c = dict(wire_c, producer="rust-semantic", language="rust", producerVersion="rust-provider 1.0.0")
        rust_v3 = {"schemaVersion": 3, "analysisOrdinal": 0, "stageId": "s1", "batchIndex": 0, "candidates": [rust_c], "occupancyCompanions": []}
        self.expect("wire-fact-batch-v3-rust3", lambda: K.frame_payload("rust-semantic", "FactBatch", W.decode(W.encode(rust_v3), "rust3-cbor"), "true"))
        self.expect("wire-fact-batch-v3-without-token-refused", lambda: K.frame_payload("rust-semantic", "FactBatch", rust_v3, "false"), "UNKNOWN_MEMBER")
        self.expect("wire-hex-vector-member-refused", lambda: K.check({"t": "ref", "ref": "Rust3FactCandidateV1"}, dict(rust_c, canonicalRelationPayloadHex="00"), "c"), "UNKNOWN_MEMBER")
        self.expect("wire-ts-producer-const", lambda: K.check({"t": "ref", "ref": "Ts2FactCandidateV1"}, rust_c, "c"), "CONST")
        self.expect("wire-rust3-anchor-path-lexical", lambda: K.check({"t": "ref", "ref": "Rust3FactCandidateV1"}, dict(rust_c, anchors=[dict(anchor, path="x\n/..")]), "c"), "PATH_LEXICAL")

    def wire_examples(self):
        K = self.K
        chunk = {"snapshotId": SNAP, "path": "src/a.ts", "chunkIndex": 0, "byteOffset": 0, "bytes": b"abc"}
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
        self.expect("wire-rust3-path-newline-dotdot", lambda: K.frame_payload("rust-semantic", "SnapshotFileChunk", dict(chunk, path="a\n/../b")), "PATH_LEXICAL")
        self.expect("wire-rust3-path-newline-plain", lambda: K.frame_payload("rust-semantic", "SnapshotFileChunk", dict(chunk, path="a\nb")))
        self.expect("wire-rust3-path-4097-bytes", lambda: K.frame_payload("rust-semantic", "SnapshotFileChunk", dict(chunk, path="é" * 2049)), "TEXT_UTF8_BYTES")
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
        pre = {"executionId": "exec1_" + "0" * 32, "snapshotId": SNAP, "planId": PLAN, "reason": "native-context-mismatch",
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
            AR.budget_observed(self.wire, budget, {"unit": "work-units", "limit": 7})
        self.expect("rust3-observed-limit-plus-one", observed)

    def run(self):
        for step in (self.vectors, self.scope2, self.anchors, self.manifests, self.depsrc, self.prepared, self.transitions, self.commitments, self.wire_examples):
            try:
                step()
            except Exception as exc:  # noqa: BLE001
                self.add("step:" + step.__name__, False, type(exc).__name__ + ": " + str(exc)[:400])
        return self.results
