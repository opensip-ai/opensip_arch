"""Static checks (candidate 03): inputs, grammar, member lists against owners, frames, literals, closed pattern sites and
structured dialect, rendered lexical rules and path member lists, owner accounting law, extern closure, map order,
citations, gap mappings, coverage and owner-derived rule parameters. Each check returns (id, ok, detail)."""
import hashlib, json, random, re
from pathlib import Path

import common as CM
import patterns as PT
import rules as RU
import wirecodec as W


class Static:
    def __init__(self, arch, subject):
        self.arch, self.out = Path(arch), Path(subject)
        self.results = []
        self.raw = {k: (self.arch / p).read_bytes() for k, (p, _, _) in CM.ARCH_PINS.items()}
        self.inputs = {}
        for k, (p, h, _) in CM.SUBJECT_INPUTS.items():
            b = (self.out / p).read_bytes()
            self.inputs[k] = b
            self.add("subject-inputs-pinned:" + k, hashlib.sha256(b).hexdigest() == h, p)
        j = lambda k: json.loads(self.raw[k])
        self.d2 = j("delivery2")["typescriptSemanticSubstrate"]["providerProtocol"]
        self.w2 = self.d2["wireSchema"]
        self.r2 = j("rust2")
        self.fp = j("factPlane")
        self.c2 = j("c2v3")
        self.p3 = j("p3")
        self.ri2 = j("resolvedInputs2")
        self.hs, self.st, self.ne, self.oc, self.fb3, self.dispatch = j("handshake"), j("startup"), j("evidence"), j("occupancy"), j("factBatch3"), j("dispatch")
        self.ids3 = j("identitySchemas3")
        rd = lambda n: json.loads((self.out / n).read_text())
        self.wire = rd("wire-carriers.v1.json")
        self.cov = rd("field-coverage.json")
        self.succ = rd("successor.json")
        self.vectors = rd("admission-vectors.json")
        self.p3guard = rd("p3-guard-successor.v1.json")
        self.docs = {d["$id"]: d for d in (self.hs, self.st, self.ne, self.oc, self.fb3, self.dispatch)}

    def add(self, id_, ok, detail=""):
        self.results.append({"id": id_, "ok": bool(ok), "detail": detail if isinstance(detail, str) else json.dumps(detail, default=str, ensure_ascii=False)[:900]})

    def lines(self, key):
        return self.raw[key].decode("utf-8").split("\n")

    def mem(self, rec, name):
        return next(m for m in self.wire["records"][rec]["members"] if m["name"] == name)["type"]

    def rule(self, rid):
        return next(r for r in self.wire["admission"] if r["id"] == rid)

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
        ids = [r["id"] for r in self.wire["admission"]]
        used = {a for r in self.wire["records"].values() for a in r.get("admission", [])}
        self.add("admission-ids-unique-and-used-ids-exist", len(ids) == len(set(ids)) and used <= set(ids), sorted(used - set(ids)))

    # ------------------------------------------------------------------
    def member_lists(self):
        rec = self.wire["records"]
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
        chunk = re.search(r"`\{([^}]*)\}`", self.lines("nativeMd")[2876]).group(1)
        owners["Rust3DependencySourceChunkV3"] = [m.strip() for m in chunk.split(",")]
        owners["Rust3C2StageBudgetV1"] = self.c2["planIntent"]["wireTypes"]["stageBudgetV1"]["required"]
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
        if not rec["Rust3DependencySourceAcceptedV3"]["target"]["schemaRef"].endswith("DependencySourceSealV3"):
            bad["Rust3DependencySourceAcceptedV3"] = "alias target"
        self.add("carrier-member-lists", not bad, bad)
        self.add("owners-compared", len(owners) >= 48, str(len(owners)))
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
        dir_ok = all(dirs[n] == ("host-to-worker" if n in self.d2["closedHostToWorkerFrames"] else "worker-to-host") for n in want)
        env_enum = self.mem("Ts2FrameV2", "frameType")["enum"]
        self.add("ts2-frame-set", sorted(names) == sorted(want) == sorted(env_enum) and dir_ok, names)
        order = json.loads(self.raw["ts2order"])
        term = {f["frameType"] for f in tsp["frames"] if f["workerTerminal"]}
        self.add("ts2-terminal-frames", term == {r["frame"] for r in order["rules"] if "terminal" in r}, sorted(term))
        rsp = self.wire["protocols"]["rust-semantic"]
        rnames = [f["frameType"] for f in rsp["frames"]]
        p3frames = {r["frame"] for r in self.p3["rules"]} - {"*", "*PROCESS_FAULT", "zero-exit", "eof"}
        self.add("rust3-frame-set", set(rnames) == p3frames == set(self.mem("Rust3ProviderFrameV3", "frameType")["enum"]) and len(rnames) == 26, sorted(p3frames ^ set(rnames)))
        rw = self.r2["wireSchema"]["frameSchemas"]
        mism = [f["frameType"] for f in rsp["frames"] if f["frameType"] in rw and (rw[f["frameType"]]["direction"] != f["direction"] or rw[f["frameType"]]["workerTerminal"] != f["workerTerminal"])]
        rterm = {f["frameType"] for f in rsp["frames"] if f["workerTerminal"]}
        self.add("rust3-frame-directions-terminals", not mism and rterm == {r["frame"] for r in self.p3["rules"] if "terminal" in r}, mism)
        rowp = {k: v.split(" ")[0].rstrip(",") for k, v in self.p3["rowPayloads"].items() if k.startswith("P3-")}
        ext = {}
        for f in rsp["frames"]:
            p = f["payload"]
            ext[f["frameType"]] = [a.get("generatedType", a.get("ref")) for a in (p["alternatives"].values() if "select" in p else [p])]
        bad = [(rid, n) for rid, n in rowp.items() if not any(x.endswith(n) for x in ext[next(r["frame"] for r in self.p3["rules"] if r["id"] == rid)])]
        self.add("rust3-row-payloads-match-p3", not bad, bad)
        sel = [f["payload"]["alternatives"] for p in (tsp, rsp) for f in p["frames"] if f["frameType"] == "Unavailable"]
        self.add("unavailable-selector-phases", all(set(a) == {"WAIT_NATIVE_CONTEXT_VERIFIED", "ANALYZING"} for a in sel), "")
        self.add("ts2-unavailable-selection-trace-difference-stated", "T2-23" in tsp["transitions"].get("unavailableSelection", ""), "")

    # ------------------------------------------------------------------
    def literals(self):
        rec = self.wire["records"]
        mem = self.mem
        tsl = {k: v["const"] for k, v in self.hs["$defs"]["TypeScriptProtocolLimitsV1"]["properties"].items()}
        rl = {k: v["const"] for k, v in self.hs["$defs"]["ProtocolLimitsV3"]["properties"].items()}
        prep_rule = self.rule("PREPARED-V3-WIRE-LIMIT")["params"]
        rep = self.rule("DEPSRC-WIRE-REPRESENTABILITY")["params"]
        req = self.rule("REQUEST-WIRE-ACCOUNTING")["params"]
        dep_path = self.ne["$defs"]["DependencyFileManifestV1"]["items"]["properties"]["path"]
        pairs = [
            ("ts2 facts", int(mem("Ts2FactBatchV1", "facts")["maxItems"]), tsl["maxFactBatchFacts"]),
            ("ts2 v3 candidates", int(mem("Ts2FactBatchV3", "candidates")["maxItems"]), tsl["maxFactBatchFacts"]),
            ("ts2 chunk", int(mem("Ts2SnapshotFileChunkV1", "bytes")["maxBytes"]), tsl["maxSnapshotChunkBytes"]),
            ("ts2 entries", int(mem("Ts2SnapshotManifestV1", "entries")["maxItems"]), tsl["maxSnapshotEntries"]),
            ("ts2 stages", int(mem("Ts2AnalyzeV1", "stageRequests")["maxItems"]), tsl["maxAnalyzeStages"]),
            ("ts2 relations", int(mem("Ts2StageRequestV1", "relations")["maxItems"]), tsl["maxRelationsPerStage"]),
            ("ts2 keys", int(mem("Ts2RequestedCoverageDomainV1", "keys")["maxItems"]), tsl["maxRequestedCoverageKeysPerStage"]),
            ("ts2 payload", int(mem("Ts2FactCandidateV1", "canonicalRelationPayload")["maxBytes"]), tsl["maxFactCandidatePayloadBytes"]),
            ("rust entries", int(mem("Rust3SnapshotManifestV2", "entries")["maxItems"]), rl["maxSnapshotEntries"]),
            ("rust chunk", int(mem("Rust3SnapshotFileChunkV2", "bytes")["maxBytes"]), rl["maxSnapshotChunkBytes"]),
            ("rust total file", int(mem("Rust3SnapshotSealV2", "totalFileBytes")["max"]), rl["maxSnapshotTotalFileBytes"]),
            ("rust dep chunk", int(mem("Rust3DependencySourceChunkV3", "bytes")["maxBytes"]), rl["maxDependencySourceChunkBytes"]),
            ("rust prep chunk", int(mem("Rust3PreparedOutputChunkV3", "bytes")["maxBytes"]), rl["maxPreparedOutputChunkBytes"]),
            ("rust prep blob total", int(mem("Rust3PreparedOutputSealV3", "totalBlobBytes")["max"]), rl["maxPreparedOutputTotalBlobBytes"]),
            ("rust prep entries retained", int(mem("Rust3PreparedOutputManifestV3", "entries")["maxItems"]), rl["maxPreparedOutputEntries"]),
            ("rust prep ordinal", int(mem("Rust3PreparedOutputEntryV3", "outputOrdinal")["max"]) + 1, rl["maxPreparedOutputEntries"]),
            ("rust prep chunk ordinal", int(mem("Rust3PreparedOutputChunkV3", "outputOrdinal")["max"]) + 1, rl["maxPreparedOutputEntries"]),
            ("prep rule entries", int(prep_rule["maxEntries"]), rl["maxPreparedOutputEntries"]),
            ("prep rule ordinal", int(prep_rule["maxOrdinal"]) + 1, rl["maxPreparedOutputEntries"]),
            ("prep rule blob", int(prep_rule["maxTotalBlobBytes"]), rl["maxPreparedOutputTotalBlobBytes"]),
            ("dep path scalars", int(rep["maxPathScalars"]), dep_path["maxLength"]),
            ("dep path carrier scalars", int(self.wire["scalars"]["Rust3DependencySourcePath"]["type"]["maxScalars"]), dep_path["maxLength"]),
            ("request prefix bytes", int(req["prefixBytes"]), self.r2["framing"]["prefixBytes"]),
            ("rust2 prepared entries text", "0..maxPreparedOutputEntries" in self.r2["wireSchema"]["payloadSchemas"]["PreparedOutputManifestV2"]["fields"]["entries"], True),
            ("rust stages", int(mem("Rust3AnalyzeV2", "stages")["maxItems"]), rl["maxAnalyzeStages"]),
            ("rust subjects", int(mem("Rust3StageAnalysisDomainV2", "subjects")["maxItems"]), rl["maxSubjectsPerStage"]),
            ("rust keys", int(mem("Rust3StageAnalysisDomainV2", "requestedCoverageDomain")["maxItems"]), rl["maxRequestedCoverageKeysPerStage"]),
            ("rust candidates", int(mem("Rust3FactBatchV2", "candidates")["maxItems"]), rl["maxFactBatchCandidates"]),
            ("rust payload", int(mem("Rust3FactCandidateV1", "canonicalRelationPayload")["maxBytes"]), rl["maxCanonicalRelationPayloadBytes"]),
            ("symlink target", int(rec["Rust3SnapshotEntryV2"]["variants"]["symlink"]["targetBytes"]["maxBytes"]), rl["maxFramePayloadBytes"]),
            ("anchors", int(mem("Ts2FactCandidateV1", "anchors")["maxItems"]), self.ids3["$defs"]["fact"]["properties"]["anchors"]["maxItems"]),
            ("anchor rule count", int(self.rule("ANCHOR-WIRE-SPAN")["params"]["maxCount"]), self.ids3["$defs"]["fact"]["properties"]["anchors"]["maxItems"]),
            ("anchor vector bound", self.fb3["properties"]["candidates"]["items"]["properties"]["anchors"]["maxItems"], 4096),
        ]
        bad = [p for p in pairs if p[1] != p[2]]
        self.add("limit-literals", not bad, bad)
        cancel = self.w2["payloadSchemas"]["CancelV1"]["fields"]["reason"]
        observed = self.w2["payloadSchemas"]["CancelledV1"]["fields"]["observedPhase"]
        fk = self.r2["wireSchema"]["payloadSchemas"]["ProviderFaultV2"]["fields"]["faultKind"]
        layers = sorted({v["layer"] for v in self.fp["relationRegistry"]["relations"].values()})
        pre = self.p3["wildcards"]["*PRE_COMPLETE"]["phases"]
        enum_ok = (sorted(mem("Ts2CancelV1", "reason")["enum"]) == sorted(cancel.split("enum ")[1].split("|"))
                   and sorted(mem("Ts2CancelledV1", "observedPhase")["enum"]) == sorted(observed.split("enum ")[1].split("|"))
                   and sorted(mem("Rust3ProviderFaultV2", "faultKind")["enum"]) == sorted(fk.split("|"))
                   and mem("Ts2FactCandidateV1", "layer")["enum"] == layers == mem("Rust3FactCandidateV1", "layer")["enum"]
                   and sorted(mem("Rust3ProviderFaultV2", "phase")["enum"]) == sorted(pre) == sorted(mem("Rust3CancelledV2", "observedPhase")["enum"])
                   and mem("Rust3CancelV2", "reason")["const"] == self.r2["wireSchema"]["payloadSchemas"]["CancelV2"]["fields"]["reason"].split("exact ")[1])
        self.add("enum-literals", enum_ok, "")
        self.add("rust3-phase-vocabulary", sorted(mem("Rust3CancelledV2", "observedPhase")["enum"]) == sorted(pre), "")
        bad = []
        for n, v in self.wire["scalars"].items():
            ref = v.get("sameShapeAs")
            if not ref:
                continue
            sid, ptr = ref.split("#")
            ext = self.docs[sid]
            for part in [p for p in ptr.split("/") if p]:
                ext = ext[part]
            t = v["type"]
            if ext.get("pattern") != t.get("pattern") or ("maxLength" in ext and str(ext["maxLength"]) != t.get("maxScalars")) or ("minLength" in ext and str(ext["minLength"]) != t.get("minScalars")):
                bad.append(n)
        self.add("scalar-shapes-match-externs", not bad, bad)
        ts_domains = set(self.w2["commitments"]["domains"].values())
        r_text = json.dumps([self.r2["commitments"], self.r2["planAndDomainProjection"]])
        bad = [r["domain"] for r in self.wire["commitmentMap"]["rows"] if r["domain"] and r["domain"] not in ts_domains and r["domain"] not in r_text]
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
    def owner_derived(self):
        """Rule parameters and commitment classes derived from owner text, so an edited parameter is caught."""
        rows = {r["field"]: r for r in self.wire["commitmentMap"]["rows"]}
        rc = self.r2["commitments"]
        ts_dom = self.w2["commitments"]["domains"]
        term_law = self.st["x-opensip-startup-law"]["coverageFrames"]["terminals"]
        expected = {}
        if "stageCoverageEntries" in rc["stageCoverage"] and "stage-major" in rc["coverageStream"] and "stage-major/key order" in term_law:
            for f in ("Startup1CoverageV3.coverageCommitment", "Rust3StageResultV2.coverageCommitment"):
                expected[f] = ("stage-entries", "opensip.rust-provider.stage-coverage.v2")
            for f in ("Rust3CompleteV2.coverageStreamCommitment", "Startup1UnavailableV3.coverageCommitment", "Startup1BudgetExhaustedV3.coverageCommitment"):
                expected[f] = ("stage-major-entries", "opensip.rust-provider.coverage-stream.v2")
            expected["Rust3StageResultV2.factCommitment"] = ("stage-candidates", "opensip.rust-provider.stage-facts.v2")
            expected["Rust3CompleteV2.factStreamCommitment"] = ("stage-major-candidates", "opensip.rust-provider.fact-stream.v2")
        ts_stage = "this stage's ordered" in self.w2["definitions"]["StageResultV1"]["fields"]["coverageCommitment"]
        ts_major = "from all stages" in self.w2["payloadSchemas"]["CompleteV1"]["fields"]["coverageStreamCommitment"]
        if ts_stage and ts_major:
            for f in ("Startup1TypeScriptCoverageV2.coverageCommitment", "Ts2StageResultV1.coverageCommitment"):
                expected[f] = ("stage-entries", ts_dom["stageCoverage"])
            for f in ("Ts2CompleteV1.coverageStreamCommitment", "Startup1TypeScriptUnavailableV2.coverageCommitment", "Startup1TypeScriptBudgetExhaustedV2.coverageCommitment"):
                expected[f] = ("stage-major-entries", ts_dom["coverageStream"])
        bad = {f: [rows.get(f, {}).get("valueClass"), rows.get(f, {}).get("domain"), want] for f, want in expected.items()
               if (rows.get(f, {}).get("valueClass"), rows.get(f, {}).get("domain")) != want}
        self.add("commit-map-value-classes-match-owner", len(expected) == 12 and not bad, {"checked": len(expected), "bad": bad})
        members = self.rule("PER-KEY-SCOPE2")["params"]["descriptorMembers"]
        self.add("scope2-descriptor-members-match-owner", members == self.ids3["$defs"]["subject-scope"]["required"], members)
        pk = self.ne["$defs"]["DependencyPackageSourceV1"]["properties"]
        key_max = self.ne["$defs"]["DependencySourceManifestV3"]["properties"]["entries"]["items"]["properties"]["packageKey"]["maxLength"]
        kp = self.rule("DEPSRC-SET-KEY-CONSTRAINTS")["params"]
        key_scalar = self.wire["scalars"]["Rust3PackageKey"]["type"]
        ok = (int(kp["maxKeyScalars"]) == key_max == int(key_scalar["maxScalars"])
              and pk["name"]["maxLength"] + pk["version"]["maxLength"] + pk["sourceId"]["maxLength"] + 2 > key_max
              and int(key_scalar["minScalars"]) == pk["name"]["minLength"] + pk["version"]["minLength"] + pk["sourceId"].get("minLength", 0) + 2
              and int(kp["forbidInNameVersionAtOrBelow"]) == 0x20)
        self.add("package-key-bounds-derived-from-owner", ok, {"ownerMax": pk["name"]["maxLength"] + pk["version"]["maxLength"] + pk["sourceId"]["maxLength"] + 2, "keyMax": key_max})
        rep = self.rule("DEPSRC-WIRE-REPRESENTABILITY")["params"]
        nfc_owner = sorted(k for k in ("name", "version", "sourceId") if pk[k].get("type") == "string")
        self.add("depsrc-representability-fields-derived-from-owner", sorted(rep["nfcFields"]) == nfc_owner and rep["pathLexical"] == self.rule("CANONICAL-PATH-ADMISSION")["params"]["lexical"]
                 and "NFC" in json.dumps(self.r2["canonicalCbor"]), rep)
        order = self.ne["$defs"]["DependencySourceSetV1"]["properties"]["packages"]["x-opensip-order"]["by"]
        dp = self.rule("DEPSRC-CUSTODY")["params"]["entryOrder"]
        self.add("depsrc-order-derived-from-owner", dp == order + ["path"] and self.ne["$defs"]["DependencyFileManifestV1"]["x-opensip-order"] == "path", dp)
        tr = self.wire["protocols"]["rust-semantic"]["transitions"]
        t2 = {r["id"]: r for r in self.r2["orderingAndStateMachine"]["transitionAstV2"]["rules"]}

        def sets_output(rid):
            return next((a["value"]["const"] for a in t2[rid]["actions"] if a.get("field") == "outputSeen"), None)
        want_updates = [{"onFrames": ["Analyze"], "sets": {"outputSeen": sets_output("T015-ANALYZE")}},
                        {"onFrames": ["FactBatch", "CoverageV3"], "sets": {"outputSeen": sets_output("T016-FACT-BATCH")}}]
        t019 = t2["T019-UNAVAILABLE"]["guard"]["items"]
        guard_ok = any(i.get("left") == "state.outputSeen" and i["right"]["const"] is False for i in t019) and tr["guardAdditions"] == {"P3-25": {"outputSeen": False}}
        cov_sets = sets_output("T017-COVERAGE-NEXT") is True and sets_output("T018-COVERAGE-LAST") is True
        self.add("p3-overlay-updates-match-rust2", tr["stateUpdateAdditions"] == want_updates and guard_ok and cov_sets and tr["stateAdditions"] == {"outputSeen": self.r2["orderingAndStateMachine"]["initialState"]["outputSeen"]}, tr["stateUpdateAdditions"])
        start_in = "START" in next(r for r in self.p3["rules"] if r["id"] == "P3-29")["phase"] or "START" in self.p3["wildcards"]["*PRE_COMPLETE"]["phases"]
        self.add("cancel-in-start-consistent-with-p3", tr["cancel"]["hostMaySendInStart"] is start_in, tr["cancel"]["hostMaySendInStart"])
        g = self.p3guard
        self.add("p3-guard-successor-file", g["guardAdditions"] == tr["guardAdditions"] and g["stateUpdateAdditions"] == tr["stateUpdateAdditions"]
                 and g["parent"]["sha256"] == CM.ARCH_PINS["p3"][1], "")
        prep = self.rule("PREPARED-V3-WIRE-LIMIT")["params"]
        md = self.lines("nativeMd")
        row = md[3524]
        self.add("prepared-refusal-row-family", "route" in prep and "refusal" not in prep
                 and "non-inert prepared row" in row and "`request-rejected` (2)" in row and "`REQUEST.PRECONDITION_FAILED`" in row
                 and prep["countScope"] == "all-inert-rows", row[:160])
        fault = self.rule("RUST3-PROVIDER-FAULT")["params"]
        self.add("provider-fault-semantics-declared", fault["phaseSemantics"] == "worker-observed" and fault["hostAdmission"] == "possible-phase-set" and fault["jointConsistency"] is True
                 and fault["nullLaw"] == {"executionId": "OpenUniverse", "analysisOrdinal": "Analyze"}, fault)
        req = self.rule("REQUEST-WIRE-ACCOUNTING")["params"]
        fr, agg = self.r2["framing"], self.r2["limitPolicy"]["aggregateAccounting"]
        with_totals = sorted(p for p, name in (("rust-semantic", "ProtocolLimitsV3"), ("typescript-semantic", "TypeScriptProtocolLimitsV1"))
                             if "maxRequestPayloadBytesTotal" in self.hs["$defs"][name]["properties"])
        law = {"lengthScope": fr["lengthScope"] == "payload bytes only" and "envelope payload bytes" in agg and req["lengthScope"] == "envelope-payload",
               "prefixExcluded": "exclude each 40-byte transport prefix" in agg and req["prefixIncluded"] is False and int(req["prefixBytes"]) == fr["prefixBytes"],
               "frameBound": "Reject length above maxFramePayloadBytes" in fr["allocationRule"],
               "totalsWhereDeclared": sorted(req["totalsApplyTo"]) == with_totals,
               "planTimeNoSpawn": "1. **Plan time (no spawn).**" in md[2847]}
        self.add("request-accounting-law-matches-owner", all(law.values()), law)

    # ------------------------------------------------------------------
    def patterns(self):
        d = self.wire["privateRepresentation"]["patternDialect"]
        comp = PT.closure(self.wire, self.docs)
        wire_sites = sum(1 for x in comp["sites"] if x["location"]["document"] == "wire-carriers.v1.json")
        self.add("pattern-sites-closed", d["patternSites"] == comp["sites"],
                 {"published": len(d["patternSites"]), "computed": len(comp["sites"]), "wireSites": wire_sites, "externSites": len(comp["sites"]) - wire_sites,
                  "distinctPatterns": len({x["pattern"] for x in comp["sites"]}), "externRootsReached": comp["externRootsReached"]})
        lower = [x for x in comp["sites"] if x["lower"]]
        look = [x for x in comp["sites"] if "(?=" in x["pattern"] or "(?!" in x["pattern"]]
        self.add("pattern-lowering-closed", d["loweringRequired"] == lower and all(x["lower"] for x in look) and len(look) > 0,
                 {"published": len(d["loweringRequired"]), "computed": len(lower), "lookaroundSites": len(look)})
        unsupported = []
        for x in comp["sites"]:
            try:
                W.ecma_to_python(x["pattern"], d["flags"])
            except W.UnsupportedPattern as exc:
                unsupported.append((x["pattern"], str(exc)))
        schemas = {sid: doc.get("$schema", "") for sid, doc in self.docs.items()}
        eng = d["referenceEngine"]
        ok = (d["engine"] == "ECMA-262 RegExp" and d["flags"] == "u" and not unsupported
              and eng["path"] == CM.NODE["path"] and eng["sha256"] == CM.NODE["sha256"] and int(eng["bytes"]) == CM.NODE["bytes"] and eng["versions"] == CM.NODE["versions"]
              and d["lineTerminators"] == ["U+000A", "U+000D", "U+2028", "U+2029"]
              and "MUST implement every loweringRequired site" in d["lowering"] and "normative" in d["supplementary"]
              and all("2020-12" in s for s in schemas.values()))
        self.add("pattern-dialect-structured", ok, {"flags": d["flags"], "unsupported": unsupported, "schemaDialects": schemas})

    def lexical_rules(self):
        lr = self.wire["privateRepresentation"]["lexicalRules"]
        bad = []
        for n, r in lr.items():
            try:
                if r.get("text") != RU.render_lexical(r):
                    bad.append(n)
            except KeyError as exc:
                bad.append(n + ": " + str(exc))
        self.add("lexical-rule-text-rendered", not bad and set(lr) == {"logical-path-segments", "canonical-path-segments", "package-key"}, bad)
        cp, lp, pk = lr["canonical-path-segments"], lr["logical-path-segments"], lr["package-key"]
        rust_rule = self.r2["wireSchema"]["definitions"]["CanonicalPath"]["rule"]
        model = self.raw["nativeModel"].decode("utf-8")
        derived = {
            "canonical": cp["separator"] == "/" and cp["forbiddenSegments"] == ["", ".", ".."] and set(cp["forbiddenScalars"]) == {"\u0000", "\\"}
                         and ("drive" in rust_rule) == ("firstSegmentForbiddenPattern" in cp) and cp.get("firstSegmentForbiddenPattern") == "^[A-Za-z]:" and "maxSegmentScalars" not in cp,
            "logical": lp["separator"] == "/" and "{1,255}" in self.ids3["$defs"]["LogicalPath"]["pattern"] and lp.get("maxSegmentScalars") == "255"
                       and lp["forbiddenSegments"] == ["", ".", ".."] and set(lp["forbiddenScalars"]) == {"\u0000", "\\"} and "firstSegmentForbiddenPattern" not in lp,
            "packageKey": pk["separator"] == " " and pk["nameVersionForbidAtOrBelow"] == self.rule("DEPSRC-SET-KEY-CONSTRAINTS")["params"]["forbidInNameVersionAtOrBelow"]
                          and "key = f'{row[\"name\"]} {row[\"version\"]} {row[\"sourceId\"]}'" in model,
        }
        self.add("lexical-rules-derived-from-owner", all(derived.values()), derived)

    def path_members(self):
        def uses(t, names):
            stack = [t]
            while stack:
                x = stack.pop()
                if x.get("t") == "ref" and x["ref"] in names:
                    return True
                stack.extend(x[k] for k in ("of", "items") if k in x)
            return False

        def members(names):
            out = []
            for rn, r in self.wire["records"].items():
                if r["kind"] == "record":
                    pairs = [(m["name"], m["type"]) for m in r["members"]]
                elif r["kind"] == "variant-record":
                    pairs = [(f"variants.{v}.{k}", t) for v, mm in r["variants"].items() for k, t in mm.items()]
                else:
                    continue
                out.extend(f"{rn}.{n}" for n, t in pairs if uses(t, names))
            return sorted(out)

        def extern_members(protocol):
            out = []
            for f in self.wire["protocols"][protocol]["frames"]:
                p = f["payload"]
                if p.get("t") != "extern" or not ("Manifest" in f["frameType"] or "Chunk" in f["frameType"]):
                    continue
                sid, ptr = p["schemaRef"].split("#", 1)
                node = self.docs[sid]
                for part in [x for x in ptr.split("/") if x]:
                    node = node[part]
                stack = [(node, "")]
                while stack:
                    n, pp = stack.pop()
                    for k, v in n.get("properties", {}).items():
                        if k == "path":
                            out.append({"generatedType": p["generatedType"], "pointer": pp + "/path"})
                        stack.append((v, pp + "/" + k))
                    if isinstance(n.get("items"), dict):
                        stack.append((n["items"], pp + "/*"))
            return sorted(out, key=lambda m: (m["generatedType"], m["pointer"]))

        want = {"CANONICAL-PATH-ADMISSION": (members({"Rust3CanonicalPath", "Rust3DependencySourcePath"}), extern_members("rust-semantic")),
                "TS2-LOGICAL-PATH-ADMISSION": (members({"Ts2ProjectPath"}), extern_members("typescript-semantic"))}
        bad = {}
        for rid, (m, e) in want.items():
            r = self.rule(rid)
            p = r["params"]
            if p["members"] != m or p["externMembers"] != e or r["rule"] != RU.render_path_members(p["lexical"], m, e):
                bad[rid] = {"published": [p["members"], p["externMembers"]], "computed": [m, e]}
        self.add("path-members-match-carrier-graph", not bad and want["CANONICAL-PATH-ADMISSION"][1], bad or {k: len(v[0]) + len(v[1]) for k, v in want.items()})

    def paths_and_codecs(self):
        paths = {n: v["type"] for n, v in self.wire["scalars"].items() if "Path" in n}
        self.add("path-scalars-lexical-no-pattern", all("lexical" in t and "pattern" not in t for t in paths.values()) and len(paths) == 3, sorted(paths))
        lex = self.wire["privateRepresentation"]["lexicalRules"]
        flags = self.wire["privateRepresentation"]["patternDialect"]["flags"]
        native = self.ne["$defs"]["CanonicalPath"]["pattern"]
        probes = ["a\n/../b", "a\n//b", "a//b", "a/", "C:x"]
        bypass = [p for p in probes if W.ecma_test(native, flags, p)]
        refused = []
        for p in bypass:
            try:
                W.lexical(lex, "canonical-path-segments", p, flags)
            except W.Refuse:
                refused.append(p)
        self.add("native2-canonical-path-pattern-weaker", bypass == refused == probes, bypass)
        members = {"Rust3SnapshotEntryV2": "path", "Rust3SnapshotFileChunkV2": "path", "Rust3SubjectV2": "path", "Rust3DependencySourceChunkV3": "path"}
        bad = []
        for rec, m in members.items():
            r = self.wire["records"][rec]
            t = r["variants"]["file"][m] if r["kind"] == "variant-record" else self.mem(rec, m)
            if t.get("ref") not in ("Rust3CanonicalPath", "Rust3DependencySourcePath") or "CANONICAL-PATH-ADMISSION" not in r["admission"]:
                bad.append(rec)
        for rec in ("Ts2SnapshotEntryV1", "Ts2SnapshotFileChunkV1", "Ts2SnapshotFileSubjectV1", "Ts2AnchorRefV1"):
            if "TS2-LOGICAL-PATH-ADMISSION" not in self.wire["records"][rec]["admission"]:
                bad.append(rec)
        tsp = self.wire["scalars"]["Ts2ProjectPath"]["type"]
        lp = self.ids3["$defs"]["LogicalPath"]
        self.add("ts2-path-bound-matches-owner", tsp.get("maxScalars") == str(lp["maxLength"]) and "maxUtf8Bytes" not in tsp and tsp.get("lexical") == "logical-path-segments"
                 and "{1,255}" in lp["pattern"], tsp)
        rcp = self.wire["scalars"]["Rust3CanonicalPath"]["type"]
        c2b = self.c2["planIntent"]["wireTypes"]["canonicalRelativePath"]["utf8Bytes"]
        self.add("rust3-path-bound-matches-owner", rcp.get("maxUtf8Bytes") == str(c2b["max"]) and rcp.get("lexical") == "canonical-path-segments"
                 and "drive prefix" in self.r2["wireSchema"]["definitions"]["CanonicalPath"]["rule"], rcp)
        link = self.wire["records"]["Ts2SnapshotEntryV1"]["variants"]["symlink"]["linkTarget"]
        self.add("path-members-bound-to-lexical-rules", not bad and "maxScalars" not in link and "lexical" not in link, bad)
        cve = self.ri2["planIdContract"]["canonicalValueEncoding"]["encodings"]
        probe = {"null": None, "false": False, "true": True, "unsigned-64": 5, "NFC-UTF8-string": "ab", "array": [1], "string-keyed-map": {"b": 1, "a": 2}, "negative-signed-64": -3}
        tag_ok = all(W.cve1(v)[:1].hex() == cve[k].split(" ")[0] for k, v in probe.items())
        self.add("cve1-tags-match-owner", tag_ok and "unsigned lexicographic order of NFC UTF-8 key bytes" in cve["string-keyed-map"], "")
        opts = json.loads(self.inputs["generatorOptions"])
        owners = {o["schemaId"]: o["namespace"] for o in opts["owners"]}
        self.add("extern-namespaces-match-generator-options", all(owners.get(k) == v for k, v in CM.EXTERN_NS.items()), "")

    # ------------------------------------------------------------------
    def extern_closure(self):
        seen, bad, stack = set(), [], []

        def push(ref):
            if ref not in seen:
                seen.add(ref)
                stack.append(ref)
        refs = []

        def collect(o):
            if isinstance(o, dict):
                if o.get("t") == "extern":
                    refs.append(o["schemaRef"])
                for v in o.values():
                    collect(v)
            elif isinstance(o, list):
                for v in o:
                    collect(v)
        collect([self.wire["records"], self.wire["protocols"]])
        for r in refs:
            push(r)
        while stack:
            ref = stack.pop()
            sid, ptr = ref.split("#", 1)
            node = self.docs[sid]
            for part in [p for p in ptr.split("/") if p]:
                node = node[part]

            def scan(o, base):
                if isinstance(o, dict):
                    o = {k: v for k, v in o.items() if not k.startswith("x-opensip")}
                    if o.get("type") == "number":
                        bad.append((ref, "number"))
                    if o.get("type") == "integer" and not (o.get("minimum", -1) >= 0 or "const" in o or ("enum" in o and all(x >= 0 for x in o["enum"]))):
                        bad.append((ref, "integer-may-be-negative"))
                    for k in o:
                        if k.endswith("Hex") and isinstance(o[k], dict):
                            bad.append((ref, "hex-vector-member " + k))
                    if "$ref" in o:
                        push((base + o["$ref"]) if o["$ref"].startswith("#") else o["$ref"])
                    for v in o.values():
                        scan(v, base)
                elif isinstance(o, list):
                    for v in o:
                        scan(v, base)
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
        keys = list(dict.fromkeys(list(names) + ["".join(rnd.choice("aZ09é一") for _ in range(rnd.randint(0, 40))) for _ in range(3000)]))
        enc = [W.encode(k) for k in keys]
        self.add("map-order-profiles-equivalent-for-text-keys", sorted(enc) == sorted(enc, key=lambda e: (len(e), e)), str(len(keys)))

    def citations(self):
        v1 = self.lines("checkRust1")
        v2 = self.raw["checkRust2"].decode()
        self.add("citation-v1-checker-is-v1", 'PROTOCOL = "rust-provider-protocol.v1.json"' in v1[26] and "manifestSha256" in v1[1047] and "sha256_bytes(encoded_entries)" in v1[1047]
                 and "manifestSha256" not in v2 and CM.ARCH_PINS["checkRust1"][1] in v2, "check-rust-provider-protocol.py line 27 targets v1; line 1048 is its manifest recipe; the v2 checker pins it in FROZEN_V1_HASHES and computes no manifestSha256")
        ident = self.lines("identityModel3")[1891]
        self.add("fact2-anchor-range-source", "0<=a<=b<=len(raw)" in ident and "ANCHOR_RANGE" in ident, ident.strip())
        self.add("wire-anchor-rule-source", "non-empty" in self.fp["factRecordContractV1"]["sourceSpanSchema"]["rule"], "")
        self.add("anchor-order-sources", "deterministic-CBOR" in self.w2["definitions"]["AnchorRefV1"]["ordering"] and "CVE1" in self.fp["factRecordContractV1"]["anchorSchema"]["ordering"]
                 and "field-for-field" in self.w2["definitions"]["AnchorRefV1"]["join"], "")
        order = {n: self.mem(n, "anchors")["order"] for n in ("Ts2FactCandidateV1", "Rust3FactCandidateV1")}
        params = self.rule("ANCHOR-WIRE-SPAN")["params"]["order"]
        self.add("anchor-order-tokens-follow-language-owner", order == {"Ts2FactCandidateV1": params["typescript-semantic"], "Rust3FactCandidateV1": params["rust-semantic"]}
                 and params == {"typescript-semantic": "cbor-bytes-strict", "rust-semantic": "cve1-bytes-strict"}, order)
        art = self.ne["$defs"]["DependencySourceManifestV3"]["properties"]["manifestSha256"]["x-opensip-digest"]["artifact"]
        self.add("depsrc-self-referential-unsatisfiable", "manifest frame bytes as sent" in art and "manifestSha256" in self.ne["$defs"]["DependencySourceManifestV3"]["required"], art)
        md = self.lines("nativeMd")
        self.add("native-md-anchors", "DependencySourceChunk" in md[2876] and "DependencySourceAccepted" in md[2878] and "phaseValues" in md[117]
                 and "StageResultV2" in md[128] and "4.1a" in md[1888] and "prepared custody (only when `preparedOutputSetId` is non-null)" in " ".join(md[2862:2866])
                 and "cancellation is `interrupted` (130)" in " ".join(md[3837:3844]), "")
        fact_anchor = self.ids3["$defs"]["fact"]["properties"]["anchors"]["items"]
        self.add("fact2-anchor-closed-shape", fact_anchor["additionalProperties"] is False and set(fact_anchor["required"]) == {"path", "blobDigest", "startByte", "endByte"}, "")
        self.add("d9join-interruption-timing-source", "interruption timing" in self.r2["d9Join"]["rule"], "")

    def gaps(self):
        rs = json.loads(self.inputs["rustFields"])
        g19, g18 = rs["gaps"]["R3-G19"], rs["gaps"]["R3-G18"]
        row = next(r for r in self.succ["rows"] if r["id"] == "SUCC-TS2-MANIFEST-DIGEST")
        rl = self.cov["recordLevelGaps"]
        self.add("gap-r3-g19-is-citation-defect", "check-rust-provider-protocol.py" in g19["finding"] and "line 27" in g19["finding"] and "Citation" in g19["title"]
                 and rl.get("R3-G19", "").startswith("SUCC-TS2-MANIFEST-DIGEST") and "R3-G19" in row["justification"] and "check-rust-provider-protocol.py is the v1 checker" in row["justification"],
                 {"title": g19["title"], "mapping": rl.get("R3-G19")})
        fg = next((f for f in self.succ["falseGaps"] if f["gap"].startswith("R3-G18")), {})
        self.add("gap-r3-g18-is-control-owner", "control" in g18["title"].lower() and rl.get("R3-G18") == "falseGaps[R3-G18]"
                 and CM.ARCH_PINS["controlRoute"][0] in fg.get("refutation", ""), {"title": g18["title"], "mapping": rl.get("R3-G18")})

    def coverage(self):
        t = self.cov["totals"]
        unmapped = [r for rows in self.cov["rows"].values() for r in rows if "status" not in r]
        self.add("field-coverage-totals", t == {"typescript-semantic": 200, "rust-semantic": 374} and not unmapped, [t, len(unmapped)])
        gaps = [g for rows in self.cov["rows"].values() for r in rows for g, v in r["gapResolutions"].items() if not v]
        ts = json.loads(self.inputs["tsFields"])
        rs = json.loads(self.inputs["rustFields"])
        all_gaps = set(ts["gaps"]) | set(rs["gaps"])
        attached = {g for rows in self.cov["rows"].values() for r in rows for g in r["gaps"]} | set(self.cov["recordLevelGaps"])
        self.add("field-coverage-gaps-resolved", not gaps and attached == all_gaps and all(self.cov["recordLevelGaps"].values()), sorted(all_gaps ^ attached))
        want = {"typescript-semantic": {r["member"] for r in ts["rows"]} | {r["member"] for r in ts["newRows"]},
                "rust-semantic": set(rs["envelope"]) | set(rs["rows"]) | set(rs["externalRows"]) | set(rs["newRows"]) | set(rs["frames"])}
        got = {p: {r["inventory"] for r in rows if r["group"] != "author-added"} for p, rows in self.cov["rows"].items()}
        self.add("field-coverage-matches-inputs", got == want, {p: len(want[p] ^ got[p]) for p in want})
        positional = [r for rows in self.cov["rows"].values() for r in rows if r.get("status") == "carried-positional"]
        self.add("field-coverage-positional-rows-explicit", all(r["carrier"].startswith("POSITIONAL") for r in positional) and len(positional) == 2, str(len(positional)))

    def vector_coverage(self):
        vec, exempt = self.vectors["vectors"], self.vectors["exempt"]
        ids = {r["id"] for r in self.wire["admission"]}
        no_vec = [i for i in ids if i not in vec and i not in exempt]
        thin = [k for k, v in vec.items() if not ({x["kind"] for x in v} >= {"accept", "refuse"})]
        named = ["PER-KEY-SCOPE2", "DEPSRC-CUSTODY", "PREPARED-V3-WIRE-LIMIT", "RUST3-PROVIDER-FAULT", "COMMIT-MAP", "CANONICAL-PATH-ADMISSION", "PACKAGE-KEY-JOIN",
                 "DEPSRC-SET-KEY-CONSTRAINTS", "DEPSRC-WIRE-REPRESENTABILITY", "REQUEST-WIRE-ACCOUNTING", "P3-OVERLAY"]
        self.add("vectors-cover-every-rule", not no_vec and not thin and all(n in vec for n in named) and set(exempt) <= ids and not (set(exempt) & set(vec)), {"noVector": no_vec, "thin": thin})

    def run(self, validator_cls):
        steps = [("grammar", lambda: self.grammar(validator_cls)), ("member_lists", self.member_lists), ("frames", self.frames),
                 ("literals", self.literals), ("owner_derived", self.owner_derived), ("patterns", self.patterns), ("lexical_rules", self.lexical_rules),
                 ("path_members", self.path_members), ("paths_and_codecs", self.paths_and_codecs), ("extern_closure", self.extern_closure),
                 ("map_order", self.map_order), ("citations", self.citations), ("gaps", self.gaps), ("coverage", self.coverage), ("vector_coverage", self.vector_coverage)]
        for name, step in steps:
            try:
                step()
            except Exception as exc:  # noqa: BLE001 - a malformed candidate is a failed named check, never a crash
                self.add("step:" + name, False, type(exc).__name__ + ": " + str(exc)[:300])
        return self.results
