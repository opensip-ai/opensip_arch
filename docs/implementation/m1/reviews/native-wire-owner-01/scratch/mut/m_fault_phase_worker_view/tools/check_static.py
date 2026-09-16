"""Static checks: pins, input grammar, member lists against owners, frames, literals, extern closure, map order,
citations and coverage. Each check returns (id, ok, detail)."""
import hashlib, json, random, re
from pathlib import Path

import common as CM
import wirecodec as W


def jpath(doc, path):
    node = doc
    for part in path.split("."):
        node = node[part]
    return node


class Static:
    def __init__(self, arch, out):
        self.arch, self.out = Path(arch), Path(out)
        self.results = []
        self.raw = {}
        for k, (p, h) in CM.PINS.items():
            b = (Path(p) if p.startswith("/") else self.arch / p).read_bytes()
            self.raw[k] = b
            self.add("pin:" + k, hashlib.sha256(b).hexdigest() == h, p)
        j = lambda k: json.loads(self.raw[k])
        self.d2 = j("delivery2")["typescriptSemanticSubstrate"]["providerProtocol"]
        self.w2 = self.d2["wireSchema"]
        self.r2 = j("rust2")
        self.fp = j("factPlane")
        self.c2 = j("c2v3")
        self.p3 = j("p3")
        self.hs, self.st, self.ne, self.oc, self.fb3 = j("handshake"), j("startup"), j("evidence"), j("occupancy"), j("factBatch3")
        self.ids3 = j("identitySchemas3")
        self.wire = json.loads((self.out / "wire-carriers.v1.json").read_text())
        self.cov = json.loads((self.out / "field-coverage.json").read_text())
        self.succ = json.loads((self.out / "successor.json").read_text())
        self.docs = {self.hs["$id"]: self.hs, self.st["$id"]: self.st, self.ne["$id"]: self.ne, self.oc["$id"]: self.oc}

    def add(self, id_, ok, detail=""):
        self.results.append({"id": id_, "ok": bool(ok), "detail": detail if isinstance(detail, str) else json.dumps(detail)[:600]})

    def lines(self, key):
        return self.raw[key].decode("utf-8").split("\n")

    # ------------------------------------------------------------------
    def grammar(self, validator_cls):
        meta = json.loads((self.out / "wire-carriers.meta.schema.json").read_text())
        errs = [e.message for e in validator_cls(meta).iter_errors(self.wire)]
        self.add("input-grammar", not errs, errs[:5])
        names = list(self.wire["records"]) + list(self.wire["scalars"])
        bare = [n for n in names if re.fullmatch(r"(CoverageKeyV\d|FactCandidateV\d|AnchorRefV\d|FactBatchV\d|StageResultV\d)", n)]
        self.add("namespaced-type-names", not bare and all(n.startswith(("Ts2", "Rust3")) for n in names), bare)
        ints = []

        def walk(o, path):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k in ("min", "max", "const", "minItems", "maxItems", "minBytes", "maxBytes", "minScalars", "maxScalars", "maxUtf8Bytes") and isinstance(v, int) and not isinstance(v, bool):
                        ints.append(path + "." + k)
                    walk(v, path + "." + k)
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    walk(v, f"{path}[{i}]")
        walk(self.wire["records"], "records")
        self.add("integer-literals-are-decimal-strings", not ints, ints[:5])

    # ------------------------------------------------------------------
    def member_lists(self):
        rec = self.wire["records"]
        D = "definitions."
        P = "payloadSchemas."
        owners = {
            "Ts2FrameV2": list(self.w2["frameEnvelope"]["required"]),
            "Ts2FactBatchV3": self.fb3["required"], "Rust3FactBatchV3": self.fb3["required"],
            "Rust3ProviderFrameV3": self.r2["wireSchema"]["envelope"]["required"],
            "Rust3FactCandidateV1": self.fp["factRecordContractV1"]["candidateSchema"]["required"],
            "Rust3AnchorRefV1": self.fp["factRecordContractV1"]["anchorSchema"]["required"],
        }
        for n in ["SnapshotEntryV1", "ProviderWorkBudgetV1", "StageRequestV1", "SnapshotFileSubjectV1", "SubjectScopeV1",
                  "RequestedCoverageDomainV1", "AnchorRefV1", "FactCandidateV1", "CoverageKeyV1", "StageResultV1"]:
            owners["Ts2" + n] = self.w2["definitions"][n]["required"]
        for n in ["SnapshotManifestV1", "SnapshotFileChunkV1", "SnapshotSealV1", "SnapshotAcceptedV1", "AnalyzeV1", "FactBatchV1",
                  "CompleteV1", "CancelV1", "CancelledV1"]:
            owners["Ts2" + n] = self.w2["payloadSchemas"][n]["required"]
        rw = self.r2["wireSchema"]
        for n in ["SnapshotEntryV2", "SubjectV2", "CoverageKeyV2", "StageAnalysisDomainV2", "StageRequestV2", "StageResultV2"]:
            owners["Rust3" + n] = rw["definitions"][n]["required"]
        for n in ["SnapshotManifestV2", "SnapshotFileChunkV2", "SnapshotSealV2", "SnapshotAcceptedV2", "AnalyzeV2", "FactBatchV2",
                  "CompleteV2", "ProviderFaultV2", "CancelV2", "CancelledV2"]:
            owners["Rust3" + n] = rw["payloadSchemas"][n]["required"]
        for x in ["Manifest", "Chunk", "Seal", "Accepted"]:
            owners[f"Rust3PreparedOutput{x}V3"] = rw["payloadSchemas"][f"PreparedOutput{x}V2"]["required"]
        owners["Rust3PreparedOutputEntryV3"] = rw["definitions"]["PreparedOutputEntryV2"]["required"]
        line = self.lines("nativeMd")[2876]
        chunk = re.search(r"`\{([^}]*)\}`", line).group(1)
        owners["Rust3DependencySourceChunkV3"] = [m.strip() for m in chunk.split(",")]
        bad = {}
        for name, want in owners.items():
            r = rec[name]
            got = r["memberOrder"] if r["kind"] == "variant-record" else [m["name"] for m in r["members"]]
            if got != list(want):
                bad[name] = {"carrier": got, "owner": want}
        c2c, c2k = self.c2["stageSchemas"]["common"], self.c2["stageSchemas"]["kinds"]["fact-derivation"]
        plan = {m["name"]: m["presence"] for m in rec["Rust3C2PlanStageV3"]["members"]}
        want = {**{k: "required" for k in c2c["required"] + c2k["required"]}, **{k: "optional" for k in c2c["optional"] + c2k["optional"]}}
        if plan != want:
            bad["Rust3C2PlanStageV3"] = {"carrier": plan, "owner": want}
        alias = rec["Rust3DependencySourceAcceptedV3"]["target"]["schemaRef"]
        seal = self.ne["$defs"]["DependencySourceSealV3"]["required"]
        if not alias.endswith("DependencySourceSealV3"):
            bad["Rust3DependencySourceAcceptedV3"] = alias
        self.add("carrier-member-lists", not bad, bad)
        self.add("owners-compared", len(owners) >= 40, str(len(owners)))
        self.add("depsrc-accepted-is-seal-members", set(seal) == {"dependencySourceSetId", "manifestSha256", "entryCount", "totalBytes", "totalChunkCount"}, seal)
        # identity-echo coverage of snapshotId/planId members
        missing = []
        for name, r in rec.items():
            members = r.get("memberOrder") or [m["name"] for m in r.get("members", [])]
            adm = set(r.get("admission", []))
            if "snapshotId" in members and not adm & {"ECHO-SNAPSHOT2", "ECHO-OPEN-UNIVERSE", "ACCEPTED-EQUALS-SEAL"}:
                missing.append(name)
            if "planId" in members and not adm & {"ECHO-PLAN2", "ECHO-OPEN-UNIVERSE", "ACCEPTED-EQUALS-SEAL"}:
                missing.append(name)
        self.add("echo-rules-present", not missing, missing)

    # ------------------------------------------------------------------
    def frames(self):
        tsp = self.wire["protocols"]["typescript-semantic"]
        names = [f["frameType"] for f in tsp["frames"]]
        want = self.d2["closedHostToWorkerFrames"] + self.d2["closedWorkerToHostFrames"] + ["NativeContextVerified"]
        dirs = {f["frameType"]: f["direction"] for f in tsp["frames"]}
        fs = self.w2["frameSchemas"]
        dir_ok = all(dirs[n] == ("host-to-worker" if n in self.d2["closedHostToWorkerFrames"] else "worker-to-host") for n in want)
        env_enum = self.wire["records"]["Ts2FrameV2"]["members"][1]["type"]["enum"]
        self.add("ts2-frame-set", sorted(names) == sorted(want) == sorted(env_enum) and dir_ok and set(fs) <= set(names), names)
        term = {f["frameType"] for f in tsp["frames"] if f["workerTerminal"]}
        order = json.loads(self.raw["ts2order"])
        ts_term = {r["frame"] for r in order["rules"] if "terminal" in r}
        self.add("ts2-terminal-frames", term == ts_term, [sorted(term), sorted(ts_term)])
        rsp = self.wire["protocols"]["rust-semantic"]
        rnames = [f["frameType"] for f in rsp["frames"]]
        p3frames = {r["frame"] for r in self.p3["rules"]} - {"*", "*PROCESS_FAULT", "zero-exit", "eof"}
        renum = self.wire["records"]["Rust3ProviderFrameV3"]["members"][3]["type"]["enum"]
        self.add("rust3-frame-set", set(rnames) == p3frames == set(renum) and len(rnames) == 26, sorted(p3frames ^ set(rnames)))
        rw = self.r2["wireSchema"]["frameSchemas"]
        mism = [n for f in rsp["frames"] for n in [f["frameType"]] if n in rw and (rw[n]["direction"] != f["direction"] or rw[n]["workerTerminal"] != f["workerTerminal"])]
        p3term = {r["frame"] for r in self.p3["rules"] if "terminal" in r}
        rterm = {f["frameType"] for f in rsp["frames"] if f["workerTerminal"]}
        self.add("rust3-frame-directions-terminals", not mism and rterm == p3term, [mism, sorted(rterm ^ p3term)])
        rowp = {k: v.split(" ")[0].rstrip(",") for k, v in self.p3["rowPayloads"].items() if k.startswith("P3-")}
        byframe = {r["frame"]: r["id"] for r in self.p3["rules"]}
        ext = {}
        for f in rsp["frames"]:
            p = f["payload"]
            alts = p["alternatives"].values() if "select" in p else [p]
            ext[f["frameType"]] = [a.get("generatedType", a.get("ref")) for a in alts]
        bad = []
        for rid, name in rowp.items():
            frame = next(r["frame"] for r in self.p3["rules"] if r["id"] == rid)
            if not any(x.endswith(name) for x in ext[frame]):
                bad.append((rid, name, ext[frame]))
        self.add("rust3-row-payloads-match-p3", not bad, bad)
        law = self.st["x-opensip-startup-law"]["preAnalyzeUnavailable"]["phase"]
        sel = [f["payload"]["alternatives"] for p in (tsp, rsp) for f in p["frames"] if f["frameType"] == "Unavailable"]
        self.add("unavailable-selector-phases", all(set(a) == {"WAIT_NATIVE_CONTEXT_VERIFIED", "ANALYZING"} for a in sel) and "WAIT_NATIVE_CONTEXT_VERIFIED" in law, "")

    # ------------------------------------------------------------------
    def literals(self):
        rec, sc = self.wire["records"], self.wire["scalars"]
        tsl = {k: v["const"] for k, v in self.hs["$defs"]["TypeScriptProtocolLimitsV1"]["properties"].items()}
        rl = {k: v["const"] for k, v in self.hs["$defs"]["ProtocolLimitsV3"]["properties"].items()}

        def mem(r, m):
            return next(x for x in rec[r]["members"] if x["name"] == m)["type"]

        pairs = [
            (int(mem("Ts2FactBatchV1", "facts")["maxItems"]), tsl["maxFactBatchFacts"]),
            (int(mem("Ts2FactBatchV3", "candidates")["maxItems"]), tsl["maxFactBatchFacts"]),
            (int(mem("Ts2SnapshotFileChunkV1", "bytes")["maxBytes"]), tsl["maxSnapshotChunkBytes"]),
            (int(mem("Ts2SnapshotManifestV1", "entries")["maxItems"]), tsl["maxSnapshotEntries"]),
            (int(mem("Ts2AnalyzeV1", "stageRequests")["maxItems"]), tsl["maxAnalyzeStages"]),
            (int(mem("Ts2StageRequestV1", "relations")["maxItems"]), tsl["maxRelationsPerStage"]),
            (int(mem("Ts2RequestedCoverageDomainV1", "keys")["maxItems"]), tsl["maxRequestedCoverageKeysPerStage"]),
            (int(mem("Ts2FactCandidateV1", "canonicalRelationPayload")["maxBytes"]), tsl["maxFactCandidatePayloadBytes"]),
            (int(mem("Rust3SnapshotManifestV2", "entries")["maxItems"]), rl["maxSnapshotEntries"]),
            (int(mem("Rust3SnapshotFileChunkV2", "bytes")["maxBytes"]), rl["maxSnapshotChunkBytes"]),
            (int(mem("Rust3SnapshotSealV2", "totalFileBytes")["max"]), rl["maxSnapshotTotalFileBytes"]),
            (int(mem("Rust3DependencySourceChunkV3", "bytes")["maxBytes"]), rl["maxDependencySourceChunkBytes"]),
            (int(mem("Rust3PreparedOutputChunkV3", "bytes")["maxBytes"]), rl["maxPreparedOutputChunkBytes"]),
            (int(mem("Rust3PreparedOutputSealV3", "totalBlobBytes")["max"]), rl["maxPreparedOutputTotalBlobBytes"]),
            (int(mem("Rust3PreparedOutputManifestV3", "entries")["maxItems"]), rl["maxPreparedOutputEntries"] + rl["maxExpansionRows"] + rl["maxGeneratedFileRows"]),
            (int(mem("Rust3AnalyzeV2", "stages")["maxItems"]), rl["maxAnalyzeStages"]),
            (int(mem("Rust3StageAnalysisDomainV2", "subjects")["maxItems"]), rl["maxSubjectsPerStage"]),
            (int(mem("Rust3StageAnalysisDomainV2", "requestedCoverageDomain")["maxItems"]), rl["maxRequestedCoverageKeysPerStage"]),
            (int(mem("Rust3FactBatchV2", "candidates")["maxItems"]), rl["maxFactBatchCandidates"]),
            (int(mem("Rust3FactCandidateV1", "canonicalRelationPayload")["maxBytes"]), rl["maxCanonicalRelationPayloadBytes"]),
            (int(rec["Rust3SnapshotEntryV2"]["variants"]["symlink"]["targetBytes"]["maxBytes"]), rl["maxFramePayloadBytes"]),
            (int(mem("Ts2FactCandidateV1", "anchors")["maxItems"]), self.ids3["$defs"]["fact"]["properties"]["anchors"]["maxItems"]),
        ]
        bad = [p for p in pairs if p[0] != p[1]]
        self.add("limit-literals", not bad, bad)
        cancel = self.w2["payloadSchemas"]["CancelV1"]["fields"]["reason"]
        observed = self.w2["payloadSchemas"]["CancelledV1"]["fields"]["observedPhase"]
        fk = self.r2["wireSchema"]["payloadSchemas"]["ProviderFaultV2"]["fields"]["faultKind"]
        layers = sorted({v["layer"] for v in self.fp["relationRegistry"]["relations"].values()})
        pre = self.p3["wildcards"]["*PRE_COMPLETE"]["phases"]
        enum_ok = (
            sorted(mem("Ts2CancelV1", "reason")["enum"]) == sorted(cancel.split("enum ")[1].split("|")) and
            sorted(mem("Ts2CancelledV1", "observedPhase")["enum"]) == sorted(observed.split("enum ")[1].split("|")) and
            sorted(mem("Rust3ProviderFaultV2", "faultKind")["enum"]) == sorted(fk.split("|")) and
            mem("Ts2FactCandidateV1", "layer")["enum"] == layers == mem("Rust3FactCandidateV1", "layer")["enum"] and
            sorted(mem("Rust3ProviderFaultV2", "phase")["enum"]) == sorted(pre) == sorted(mem("Rust3CancelledV2", "observedPhase")["enum"]) and
            mem("Rust3CancelV2", "reason")["const"] == self.r2["wireSchema"]["payloadSchemas"]["CancelV2"]["fields"]["reason"].split("exact ")[1]
        )
        self.add("enum-literals", enum_ok, "")
        self.add("rust3-phase-vocabulary", sorted(mem("Rust3CancelledV2", "observedPhase")["enum"]) == sorted(pre), "")
        bad = []
        for n, v in sc.items():
            ref = v.get("sameShapeAs")
            if not ref:
                continue
            sid, ptr = ref.split("#")
            ext = self.docs[sid]
            for part in [p for p in ptr.split("/") if p]:
                ext = ext[part]
            t = v["type"]
            if ext.get("pattern") != t.get("pattern") or ("maxLength" in ext and str(ext["maxLength"]) != t.get("maxScalars")):
                bad.append(n)
            if "minLength" in ext and str(ext["minLength"]) != t.get("minScalars"):
                bad.append(n)
        self.add("scalar-shapes-match-externs", not bad, bad)
        ts_domains = set(self.w2["commitments"]["domains"].values())
        r_text = json.dumps([self.r2["commitments"], self.r2["planAndDomainProjection"]])
        bad = [r["domain"] for r in self.wire["commitmentMap"]["rows"] if r["domain"] and r["domain"].startswith("opensip.") and r["domain"] not in ts_domains and r["domain"] not in r_text]
        self.add("commit-domains-exist", not bad, bad)
        fields = " ".join(r["field"] for r in self.wire["commitmentMap"]["rows"])
        need = ["Startup1TypeScriptCoverageV2.coverageCommitment", "Ts2StageResultV1.coverageCommitment", "Ts2CompleteV1.coverageStreamCommitment",
                "Startup1TypeScriptUnavailableV2.coverageCommitment", "Startup1TypeScriptBudgetExhaustedV2.coverageCommitment", "Ts2StageResultV1.factCommitment",
                "Ts2CompleteV1.factStreamCommitment", "Ts2FactBatchV1.batchCommitment", "Ts2RequestedCoverageDomainV1.domainCommitment",
                "Ts2SubjectScopeV1.subjectScopeCommitment", "Ts2CoverageKeyV1.subjectScopeCommitment", "Ts2SnapshotManifestV1.manifestSha256",
                "Startup1CoverageV3.coverageCommitment", "Rust3StageResultV2.coverageCommitment", "Rust3CompleteV2.coverageStreamCommitment",
                "Startup1UnavailableV3.coverageCommitment", "Startup1BudgetExhaustedV3.coverageCommitment", "Rust3StageResultV2.factCommitment",
                "Rust3CompleteV2.factStreamCommitment", "Rust3StageAnalysisDomainV2.domainCommitment", "Rust3CoverageKeyV2.subjectScopeCommitment",
                "Rust3SnapshotManifestV2", "Native2DependencySourceManifestV3", "Rust3PreparedOutputManifestV3", "Rust3SubjectV2.subjectId"]
        self.add("commit-map-complete", all(n in fields for n in need), [n for n in need if n not in fields])

    # ------------------------------------------------------------------
    def extern_closure(self):
        seen, bad, stack = set(), [], []

        def push(ref):
            if ref not in seen:
                seen.add(ref)
                stack.append(ref)

        for f in [f for p in self.wire["protocols"].values() for f in p["frames"]]:
            pass
        W_refs = []

        def collect(o):
            if isinstance(o, dict):
                if o.get("t") == "extern":
                    W_refs.append(o["schemaRef"])
                for v in o.values():
                    collect(v)
            elif isinstance(o, list):
                for v in o:
                    collect(v)
        collect([self.wire["records"], self.wire["protocols"]])
        for r in W_refs:
            push(r)
        while stack:
            ref = stack.pop()
            sid, ptr = ref.split("#", 1)
            node = self.docs[sid]
            for part in [p for p in ptr.split("/") if p]:
                node = node[part]

            def scan(o, base_sid):
                if isinstance(o, dict):
                    if o.get("type") == "number":
                        bad.append((ref, "number"))
                    if o.get("type") == "integer" and not (o.get("minimum", -1) >= 0 or "const" in o or ("enum" in o and all(x >= 0 for x in o["enum"]))):
                        bad.append((ref, "integer-may-be-negative"))
                    o = {k: v for k, v in o.items() if not k.startswith("x-opensip")}
                    for k in o:
                        if k.endswith("Hex") and isinstance(o[k], dict):
                            bad.append((ref, "hex-vector-member " + k))
                    if "$ref" in o:
                        target = o["$ref"]
                        push((base_sid + target) if target.startswith("#") else target)
                    for v in o.values():
                        scan(v, base_sid)
                elif isinstance(o, list):
                    for v in o:
                        scan(v, base_sid)
            scan(node, sid)
        self.add("extern-closure-byte-free-nonnegative", not bad, bad[:10])
        self.add("extern-closure-size", len(seen) > 20, str(len(seen)))

    def map_order(self):
        names = set()

        def collect(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k == "name" and isinstance(v, str):
                        names.add(v)
                    if k == "properties" and isinstance(v, dict):
                        names.update(v)
                    collect(v)
            elif isinstance(o, list):
                for v in o:
                    collect(v)
        collect([self.wire["records"], self.docs])
        rnd = random.Random(7)
        keys = list(names) + ["".join(rnd.choice("aZ09é一") for _ in range(rnd.randint(0, 40))) for _ in range(3000)]
        keys = list(dict.fromkeys(keys))
        enc = [W.encode(k) for k in keys]
        a = sorted(enc)
        b = sorted(enc, key=lambda e: (len(e), e))
        self.add("map-order-profiles-equivalent-for-text-keys", a == b, str(len(keys)))

    def citations(self):
        v1 = self.lines("checkRust1")
        v2 = self.raw["checkRust2"].decode()
        l1048 = v1[1047]
        self.add("citation-v1-checker-is-v1", 'PROTOCOL = "rust-provider-protocol.v1.json"' in v1[26] and "manifestSha256" in l1048 and "sha256_bytes(encoded_entries)" in l1048
                 and "manifestSha256" not in v2 and CM.PINS["checkRust1"][1] in v2 and "opensip.rust-provider.stage-coverage.v1" in self.raw["checkRust1"].decode(),
                 "check-rust-provider-protocol.py line 27 targets v1; line 1048 is its manifest recipe; the v2 checker pins it in FROZEN_V1_HASHES and computes no manifestSha256")
        ident = self.lines("identityModel3")[1891]
        self.add("fact2-anchor-range-source", "0<=a<=b<=len(raw)" in ident and "ANCHOR_RANGE" in ident, ident.strip())
        self.add("wire-anchor-rule-source", "non-empty" in self.fp["factRecordContractV1"]["sourceSpanSchema"]["rule"], "")
        order = {n: next(m for m in self.wire["records"][n]["members"] if m["name"] == "anchors")["type"]["order"]
                 for n in ("Ts2FactCandidateV1", "Rust3FactCandidateV1")}
        self.add("anchor-order-tokens-follow-language-owner", order == {"Ts2FactCandidateV1": "cbor-bytes-strict", "Rust3FactCandidateV1": "cve1-bytes-strict"}, order)
        self.add("anchor-order-sources","deterministic-CBOR" in self.w2["definitions"]["AnchorRefV1"]["ordering"] and "CVE1" in self.fp["factRecordContractV1"]["anchorSchema"]["ordering"], "")
        art = self.ne["$defs"]["DependencySourceManifestV3"]["properties"]["manifestSha256"]["x-opensip-digest"]["artifact"]
        self.add("depsrc-self-referential-unsatisfiable", "manifest frame bytes as sent" in art and "manifestSha256" in self.ne["$defs"]["DependencySourceManifestV3"]["required"], art)
        md = self.lines("nativeMd")
        self.add("native-md-anchors", "DependencySourceChunk" in md[2876] and "DependencySourceAccepted" in md[2878] and "phaseValues" in md[117]
                 and "StageResultV2" in md[128] and "4.1a" in md[1888] and "prepared custody (only when `preparedOutputSetId` is non-null)" in " ".join(md[2862:2866]), "")
        fact_anchor = self.ids3["$defs"]["fact"]["properties"]["anchors"]["items"]
        self.add("fact2-anchor-closed-shape", fact_anchor["additionalProperties"] is False and set(fact_anchor["required"]) == {"path", "blobDigest", "startByte", "endByte"}, "")

    def coverage(self):
        t = self.cov["totals"]
        unmapped = [r for rows in self.cov["rows"].values() for r in rows if "status" not in r]
        self.add("field-coverage-totals", t == {"typescript-semantic": 200, "rust-semantic": 372} and not unmapped, [t, len(unmapped)])
        gaps = [g for rows in self.cov["rows"].values() for r in rows for g, v in r["gapResolutions"].items() if not v]
        self.add("field-coverage-gaps-resolved", not gaps, gaps[:5])

    def run(self, validator_cls):
        steps = [lambda: self.grammar(validator_cls), self.member_lists, self.frames, self.literals, self.extern_closure,
                 self.map_order, self.citations, self.coverage]
        names = ["grammar", "member_lists", "frames", "literals", "extern_closure", "map_order", "citations", "coverage"]
        for name, step in zip(names, steps):
            try:
                step()
            except Exception as exc:  # noqa: BLE001 - a malformed candidate is a failed named check, never a crash
                self.add("step:" + name, False, type(exc).__name__ + ": " + str(exc)[:300])
        return self.results
