#!/usr/bin/env python3
"""Read-only tabulator and checker for the Rust3 retained-field wire translation.

Opens every pinned source read-only (never writes to the architecture repository), refuses on any byte/hash drift,
asserts every rust-provider-protocol.v2 $.wireSchema member (and each external expansion) has exactly one row,
resolves every schema-native ref and the transitive $ref closure of the Rust3 successor records, cross-checks wire
types against resolved refs, compares inherited and successor member lists against declared expected deltas,
compares prose member lists to schemas, verifies every cited line anchor and semantic-owner function, runs
JSON-vs-CBOR probes, and writes fields.json, coverage.json and translation.md beside tools/.

    OPENSIP_ARCH=/Users/sb/code/opensip-ai/opensip_arch python3 tools/build.py            # build
    OPENSIP_ARCH=/Users/sb/code/opensip-ai/opensip_arch python3 tools/build.py --selftest # mutation controls
"""
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
REPO = os.environ.get("OPENSIP_ARCH", "/Users/sb/code/opensip-ai/opensip_arch")
sys.path.insert(0, HERE)

import common as C  # noqa: E402
import rows as RW  # noqa: E402


def abspath(path):
    return path if path.startswith("/") else os.path.join(REPO, path)


# ---------------------------------------------------------------------------------------------- sources
def read_sources():
    data, failures = {}, []
    for path, (sha, size) in C.SOURCES.items():
        with open(abspath(path), "rb") as handle:
            raw = handle.read()
        got = hashlib.sha256(raw).hexdigest()
        if got != sha or len(raw) != size:
            failures.append(f"SOURCE DRIFT {path}: sha256 {got} bytes {len(raw)} (pinned {sha} {size})")
        data[path] = raw
    return data, failures


def git_status(paths):
    try:
        out = subprocess.run(["git", "status", "--porcelain", "--"] + paths, cwd=REPO, capture_output=True, text=True, check=True).stdout
    except Exception as exc:  # noqa: BLE001
        return {"unavailable": str(exc)}
    status = {}
    for line in out.splitlines():
        status[line[3:]] = line[:2].strip()
    return status


DATA, SOURCE_FAILURES = read_sources()


def J(path):
    return json.loads(DATA[path].decode("utf-8"))


def lines(path):
    return DATA[path].decode("utf-8").split("\n")


def jsel(doc, selector):
    node = doc
    if selector != "$":
        for key in selector[2:].split("."):
            node = node[key]
    return node


RP2 = J(C.RP2)
WS = RP2["wireSchema"]
HSD, STD, NED, FBD, OCD, DBD, P3D = J(C.HSP), J(C.STP), J(C.NEP), J(C.FBP), J(C.OCP), J(C.DBP), J(C.P3P)
FPD, RID, RIJD, C2V3D, C2V4D, CTL2D, CTLS3D = J(C.FP), J(C.RI), J(C.RIJ), J(C.C2V3), J(C.C2V4), J(C.CTL2), J(C.CTLS3)
NEMD = lines(C.NEMD)
DOCS = {doc["$id"]: (path, doc) for path, doc in [(C.HSP, HSD), (C.STP, STD), (C.NEP, NED), (C.FBP, FBD), (C.OCP, OCD), (C.DBP, DBD)]}


# ---------------------------------------------------------------------------------------------- refs
def resolve(ref, base_id=None):
    id_part, frag = (ref.split("#", 1) + [""])[:2] if "#" in ref else (ref, "")
    doc_id = id_part or base_id
    if doc_id not in DOCS:
        raise KeyError("unknown $id " + str(doc_id))
    node = DOCS[doc_id][1]
    if frag:
        if not frag.startswith("/"):
            raise KeyError("non-pointer fragment " + frag)
        for token in frag[1:].split("/"):
            token = token.replace("~1", "/").replace("~0", "~")
            node = node[int(token)] if isinstance(node, list) else node[token]
    return doc_id, node


def closure(roots):
    seen, unresolved, count = set(), [], [0]

    def visit(doc_id, node, pointer):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "$ref" and isinstance(value, str):
                    count[0] += 1
                    try:
                        target_id, target = resolve(value, doc_id)
                    except (KeyError, IndexError, ValueError):
                        unresolved.append(f"{doc_id}{pointer}: {value}")
                        continue
                    mark = (target_id, value.split("#", 1)[1] if "#" in value else "")
                    if mark not in seen:
                        seen.add(mark)
                        visit(target_id, target, mark[1])
                elif not key.startswith("x-") and key not in ("description", "title"):
                    visit(doc_id, value, pointer + "/" + key)
        elif isinstance(node, list):
            for index, value in enumerate(node):
                visit(doc_id, value, pointer + "/" + str(index))

    for ref in roots:
        doc_id, node = resolve(ref)
        mark = (doc_id, ref.split("#", 1)[1] if "#" in ref else "")
        seen.add(mark)
        visit(doc_id, node, mark[1])
    return {"refsFollowed": count[0], "distinctTargets": len(seen), "unresolved": unresolved, "reached": sorted(f"{a}#{b}" for a, b in seen)}


def wire_of(node, base, depth=0):
    if depth > 30 or not isinstance(node, dict):
        return None
    if "$ref" in node:
        doc_id, target = resolve(node["$ref"], base)
        return wire_of(target, doc_id, depth + 1)
    if "const" in node:
        value = node["const"]
        return C.BOOL if isinstance(value, bool) else C.U if isinstance(value, int) else C.T if isinstance(value, str) else None
    if "oneOf" in node:
        parts = [wire_of(item, base, depth + 1) for item in node["oneOf"]]
        non_null = {p for p in parts if p != C.N}
        if len(non_null) != 1 or None in non_null:
            return None
        return non_null.pop() + ("|null" if C.N in parts else "")
    kind = node.get("type")
    table = {"integer": C.U, "string": C.T, "object": C.M, "array": C.A, "boolean": C.BOOL, "null": C.N}
    if isinstance(kind, str):
        return table.get(kind)
    if "enum" in node and all(isinstance(v, str) for v in node["enum"]):
        return C.T
    return None


# ---------------------------------------------------------------------------------------------- rows
def assemble():
    rows = {}
    env = WS["envelope"]["fields"]
    for member, row in RW.ENVELOPE.items():
        rows["envelope." + member] = dict(row, group="envelope", record="envelope", member=member,
                                          source={"path": C.RP2, "selector": "$.wireSchema.envelope.fields." + member, "originalText": env.get(member)})
    for name, spec in WS["payloadSchemas"].items():
        fields = spec.get("fields", {})
        for member, row in RW.PAYLOADS.get(name, {}).items():
            text = fields.get(member)
            selector = f"$.wireSchema.payloadSchemas.{name}." + ("fields." + member if member in fields else "required")
            if text is None and "all" in fields:
                text = "(record-level fields.all) " + fields["all"]
            rows[f"payloadSchemas.{name}.{member}"] = dict(row, group="payloadSchemas", record=name, member=member,
                                                          source={"path": C.RP2, "selector": selector, "originalText": text})
    for name, row in list(RW.STRING_DEFS.items()) + list(RW.RECORD_ONLY_DEFS.items()):
        spec = WS["definitions"].get(name, {})
        rows["definitions." + name] = dict(row, group="definitions", record=name, member=None,
                                           source={"path": C.RP2, "selector": "$.wireSchema.definitions." + name, "originalText": json.dumps(spec, sort_keys=True)})
    for name, members in RW.RECORD_DEFS.items():
        spec = WS["definitions"].get(name, {})
        fields = spec.get("fields", {})
        for member, row in members.items():
            text = fields.get(member)
            if text is None and "all" in fields:
                text = "(record-level fields.all) " + fields["all"]
            if text is None and "remaining" in fields and member != "protocolMajor":
                text = "(record-level fields.remaining) " + fields["remaining"]
            selector = f"$.wireSchema.definitions.{name}." + ("fields." + member if member in fields else "required")
            rows[f"definitions.{name}.{member}"] = dict(row, group="definitions", record=name, member=member,
                                                       source={"path": C.RP2, "selector": selector, "originalText": text})
    external_src = {
        "C2PlanStageV3": (C.C2V3, "$.stageSchemas.common / $.stageSchemas.kinds.fact-derivation"),
        "FactCandidateV1": (C.FP, "$.factRecordContractV1.candidateSchema.fields"),
        "AnchorRefV1": (C.FP, "$.factRecordContractV1.anchorSchema"),
        "RustUniverseV1": (C.RI, "$.planIdContract.semanticUniverseSchemas.rust-v1.required"),
        "RustUniverseV1.resolvedInputs": (C.RI, "$.planIdContract.semanticUniverseSchemas.rust-v1.resolvedInputs.required"),
    }
    cand_fields = FPD["factRecordContractV1"]["candidateSchema"]["fields"]
    for name, members in RW.EXTERNAL.items():
        path, selector = external_src[name]
        for member, row in members.items():
            text = cand_fields.get(member) if name == "FactCandidateV1" else None
            rows[f"external.{name}.{member}"] = dict(row, group="external", record=name, member=member,
                                                    source={"path": path, "selector": selector, "originalText": text})
    for key, row in RW.NEW.items():
        record, member = key.split(".", 1)
        ref = row["schemaNativeRef"]
        path = DOCS[ref.split("#", 1)[0]][0] if ref else C.NEMD
        selector = ("#" + ref.split("#", 1)[1]) if ref else "native-evidence.md:2877"
        rows["new." + key] = dict(row, group="new", record=record, member=member, source={"path": path, "selector": selector, "originalText": None})
    frames = {}
    for name, row in RW.FRAMES.items():
        frames["frameSchemas." + name] = dict(row, group="frameSchemas", name=name,
                                              source={"path": C.RP2, "selector": "$.wireSchema.frameSchemas." + name, "originalText": json.dumps(WS["frameSchemas"].get(name), sort_keys=True)})
    for name, row in RW.NEW_FRAMES.items():
        frames["newFrames." + name] = dict(row, group="newFrames", name=name, source={"path": C.NEMD, "selector": "§9.2 frame table", "originalText": None})
    return rows, frames


def expected_inherited_keys():
    keys = ["envelope." + m for m in WS["envelope"]["required"]]
    keys += ["frameSchemas." + f for f in WS["frameSchemas"]]
    for name, spec in WS["payloadSchemas"].items():
        keys += [f"payloadSchemas.{name}.{m}" for m in spec["required"]]
    for name, spec in WS["definitions"].items():
        keys += [f"definitions.{name}.{m}" for m in spec["required"]] if "required" in spec else ["definitions." + name]
    return keys


def expected_external_keys():
    rv1 = RID["planIdContract"]["semanticUniverseSchemas"]["rust-v1"]
    stage = C2V3D["stageSchemas"]
    c2 = stage["common"]["required"] + stage["common"]["optional"] + stage["kinds"]["fact-derivation"]["required"] + stage["kinds"]["fact-derivation"]["optional"]
    keys = ["external.C2PlanStageV3." + m for m in c2]
    keys += ["external.FactCandidateV1." + m for m in FPD["factRecordContractV1"]["candidateSchema"]["required"]]
    keys += ["external.AnchorRefV1." + m for m in FPD["factRecordContractV1"]["anchorSchema"]["required"]]
    keys += ["external.RustUniverseV1." + m for m in rv1["required"]]
    keys += ["external.RustUniverseV1.resolvedInputs." + m for m in rv1["resolvedInputs"]["required"]]
    return keys


# ---------------------------------------------------------------------------------------------- prose parsing
def prose_members(start, end, anchor):
    text = " ".join(NEMD[start - 1:end])
    at = text.index(anchor)
    open_at = text.index("{", at)
    depth, close_at = 0, None
    for index in range(open_at, len(text)):
        if text[index] in "{[":
            depth += 1
        elif text[index] in "}]":
            depth -= 1
            if depth == 0:
                close_at = index
                break
    inner = text[open_at + 1:close_at]
    top, nested, depth, buf = [], {}, 0, ""
    for ch in inner + ",":
        if ch in "[{":
            depth += 1
        if ch in "]}":
            depth -= 1
        if ch == "," and depth == 0:
            token = buf.strip().strip("`")
            name = re.match(r"[A-Za-z][A-Za-z0-9]*", token).group(0)
            top.append(name)
            if "[{" in token:
                nested[name] = [re.match(r"\s*([A-Za-z][A-Za-z0-9]*)", t).group(1) for t in token[token.index("[{") + 2:token.rindex("}]")].split(",")]
            buf = ""
        else:
            buf += ch
    return top, nested


def frame_table():
    table = {}
    for number in range(2876, 2885):
        cells = [c.strip() for c in NEMD[number - 1].strip().strip("|").split("|")]
        name = cells[0].strip("`")
        direction = {"host→worker": "host-to-worker", "worker→host": "worker-to-host"}.get(cells[1], cells[1])
        table[name] = {"line": number, "direction": direction, "terminal": cells[-1]}
    return table


def compare(label, original, successor, removed, added, note=""):
    kept = [m for m in original if m in successor]
    got_removed = [m for m in original if m not in successor]
    got_added = [m for m in successor if m not in original]
    same_order = kept == [m for m in successor if m in original]
    ok = sorted(got_removed) == sorted(removed) and sorted(got_added) == sorted(added)
    return {"label": label, "kept": len(kept), "originalCount": len(original), "removed": got_removed, "added": got_added,
            "sameOrder": same_order, "expectedRemoved": sorted(removed), "expectedAdded": sorted(added), "ok": ok, "note": note}


def comparisons():
    hs, st, ne = HSD["$defs"], STD["$defs"], NED["$defs"]
    pay, defs = WS["payloadSchemas"], WS["definitions"]
    rv1 = RID["planIdContract"]["semanticUniverseSchemas"]["rust-v1"]
    fb_items = FBD["properties"]["candidates"]["items"]["required"]
    new_limit_names = [n for n, _ in RW.NEW_LIMITS]
    out = [
        compare("payloadSchemas.HelloV2 -> provider-handshake HelloV3", pay["HelloV2"]["required"], hs["HelloV3"]["required"], [], ["protocolMajor", "identityVersions"]),
        compare("payloadSchemas.HelloAckV2 -> provider-handshake HelloAckV3", pay["HelloAckV2"]["required"], hs["HelloAckV3"]["required"], [], ["identityVersions"]),
        compare("definitions.ExpectedRustIdentityV2 -> ExpectedRustIdentityV3", defs["ExpectedRustIdentityV2"]["required"], hs["ExpectedRustIdentityV3"]["required"], [], []),
        compare("definitions.ProtocolLimitsV2 -> provider-handshake ProtocolLimitsV3", defs["ProtocolLimitsV2"]["required"], hs["ProtocolLimitsV3"]["required"], [], new_limit_names),
        compare("payloadSchemas.OpenUniverseV2 -> provider-startup OpenUniverseV3", pay["OpenUniverseV2"]["required"], st["OpenUniverseV3"]["required"], [], []),
        compare("payloadSchemas.UniverseAcceptedV2 -> UniverseAcceptedV3", pay["UniverseAcceptedV2"]["required"], st["UniverseAcceptedV3"]["required"], [], []),
        compare("payloadSchemas.CoverageV2 -> CoverageV3", pay["CoverageV2"]["required"], st["CoverageV3"]["required"], [], []),
        compare("payloadSchemas.UnavailableV2 -> UnavailableV3 (P3-25)", pay["UnavailableV2"]["required"], st["UnavailableV3"]["required"], [], []),
        compare("payloadSchemas.UnavailableV2 -> PreAnalyzeUnavailableV1 (P3-21)", pay["UnavailableV2"]["required"], st["PreAnalyzeUnavailableV1"]["required"],
                ["analysisOrdinal", "affectedStageIds", "coverage", "coverageCommitment"],
                ["executionId", "snapshotId", "planId", "nativeContextId", "recomputedNativeContextId"]),
        compare("payloadSchemas.BudgetExhaustedV2 -> BudgetExhaustedV3", pay["BudgetExhaustedV2"]["required"], st["BudgetExhaustedV3"]["required"], [], []),
        compare("payloadSchemas.FactBatchV2 -> RustFactBatchV2Vector (not negotiated)", pay["FactBatchV2"]["required"], hs["RustFactBatchV2Vector"]["required"], [], []),
        compare("payloadSchemas.FactBatchV2 -> fact-batch.3 (negotiated)", pay["FactBatchV2"]["required"], FBD["required"], [], ["schemaVersion", "occupancyCompanions"]),
        compare("definitions.CoverageResultV2 -> native-evidence CoverageResultV3", defs["CoverageResultV2"]["required"], ne["CoverageResultV3"]["required"],
                ["stageId", "entryOrdinal", "coverageState", "deficiency"], ["entry", "schemaVersion"]),
        compare("definitions.RepositoryResolutionV2 -> native-evidence RepositoryResolutionV3", defs["RepositoryResolutionV2"]["required"], ne["RepositoryResolutionV3"]["required"],
                defs["RepositoryResolutionV2"]["required"], ["authorizationId", "dependencySourceSetId", "effects", "preparedOutputSetId", "workerExecutesRepositoryCode"],
                "network -> effects is the only stated correspondence (native-evidence.md:2887-2888)"),
        compare("definitions.RustProviderCapabilityV2 -> RustCapabilitiesV3 (token array; no members)", defs["RustProviderCapabilityV2"]["required"], [],
                defs["RustProviderCapabilityV2"]["required"], []),
        compare("rust-v1 (RustUniverseV1) -> RustSemanticUniverseV2", rv1["required"], st["RustSemanticUniverseV2"]["required"], [], []),
        compare("rust-v1.resolvedInputs -> RustUniverseV2ResolvedInputs", rv1["resolvedInputs"]["required"], ne["RustUniverseV2ResolvedInputs"]["required"],
                ["cfg", "packageLockIdentity", "resolvedPackages", "buildScriptOutputs", "procMacroOutputs"],
                ["cfgSets", "configProjectionSha256", "dependencySourceSetId", "lockfileIdentity", "nativeContextId", "preparedOutputSetId", "preparedResolution",
                 "schemaVersion", "sourceUnitOwnershipId", "unifiedFeaturesId"]),
        compare("fact-plane candidateSchema (FactCandidateV1) -> fact-batch.3 JSON-vector candidate", FPD["factRecordContractV1"]["candidateSchema"]["required"], fb_items,
                ["canonicalRelationPayload"], ["canonicalRelationPayloadHex", "decodedRelationPayload"], "vector form, not a wire record"),
        compare("SUPERSEDED native-evidence HelloV3 -> provider-handshake HelloV3", ne["HelloV3"]["required"], hs["HelloV3"]["required"], [],
                ["hostBuildId", "expectedProtocolContractSha256", "expectedIdentity"]),
        compare("SUPERSEDED native-evidence HelloAckV3 -> provider-handshake HelloAckV3", ne["HelloAckV3"]["required"], hs["HelloAckV3"]["required"], [],
                ["providerBuildId", "rustCommitHash", "hostTriple", "targetTriple", "sysrootDigest"]),
        compare("SUPERSEDED native-evidence ProtocolLimitsV3 -> provider-handshake ProtocolLimitsV3", ne["ProtocolLimitsV3"]["required"], hs["ProtocolLimitsV3"]["required"], [],
                defs["ProtocolLimitsV2"]["required"]),
    ]
    prose = [
        ("§9.1 HelloV3 prose (native-evidence.md:2816-2818)", (2816, 2818, "`HelloV3` ="), hs["HelloV3"]["required"]),
        ("§9.1 ExpectedRustIdentityV3 prose (:2823-2826)", (2823, 2826, "ExpectedRustIdentityV3`) ="), hs["ExpectedRustIdentityV3"]["required"]),
        ("§9.1 HelloAckV3 prose (:2830-2831)", (2830, 2831, "`HelloAckV3` ="), hs["HelloAckV3"]["required"]),
        ("§9.2 DependencySourceManifest prose (:2876)", (2876, 2876, "`DependencySourceManifest`"), ne["DependencySourceManifestV3"]["required"]),
        ("§9.2 DependencySourceSeal prose (:2878)", (2878, 2878, "`DependencySourceSeal`"), ne["DependencySourceSealV3"]["required"]),
        ("§9.2 DependencySourceChunk prose (:2877) vs translation rows", (2877, 2877, "`DependencySourceChunk`"),
         [k.split(".", 1)[1] for k in RW.NEW if k.startswith("DependencySourceChunk(unnamed).")]),
        ("§9.2 NativeContextVerifiedV1 prose (:2881)", (2881, 2881, "`NativeContextVerifiedV1`"), st["NativeContextVerifiedV1"]["required"]),
        ("§9.2 CoverageV3 wrapper prose (:2884)", (2884, 2884, "wrapper"), st["CoverageV3"]["required"]),
        ("§9.2 RepositoryResolutionV3 prose (:2886-2887)", (2886, 2887, "`RepositoryResolutionV3` ="), ne["RepositoryResolutionV3"]["required"]),
        ("§9.7 OpenUniverseV3 prose (:3178-3179)", (3178, 3179, "`OpenUniverseV3` ="), st["OpenUniverseV3"]["required"]),
        ("§9.7 UniverseAcceptedV3 prose (:3188-3189)", (3188, 3189, "`UniverseAcceptedV3` ="), st["UniverseAcceptedV3"]["required"]),
        ("§9.7 PreAnalyzeUnavailableV1 prose (:3206-3207)", (3205, 3207, "`PreAnalyzeUnavailableV1` ="), st["PreAnalyzeUnavailableV1"]["required"]),
    ]
    for label, (start, end, anchor), schema in prose:
        top, nested = prose_members(start, end, anchor)
        out.append(compare(label, top, schema, [], []))
        if nested:
            for name, members in nested.items():
                out.append(compare(label + " entries[] items", members, ne["DependencySourceManifestV3"]["properties"][name]["items"]["required"], [], []))
    return out


# ---------------------------------------------------------------------------------------------- other checks
CITES = [(C.NEMD, n, s) for n, s in [
    (117, "preparedOwner"), (118, "RepositoryResolutionV2"), (118, "stateRecord.phaseValues"), (122, "HelloV2"), (123, "FactBatchV2"),
    (124, "ProtocolLimitsV3"), (128, "OpenUniverseV2"), (129, "CoverageV2"), (129, "StageResultV2"), (130, "rust-v1.resolvedInputs"),
    (136, "subjectScopeCommitment"), (1704, "### 3.2"), (1803, "### 3.6"), (1889, "### 4.1a"), (2799, "target-attribution-v2"),
    (2816, "Rust major-3 Hello/HelloAck"), (2872, "### 9.2"), (2876, "DependencySourceManifest"), (2877, "DependencySourceChunk"),
    (2879, "DependencySourceAccepted"), (2880, "as above for inert rows only"), (2881, "NativeContextVerified"), (2882, "Unavailable"),
    (2884, "CoverageV3"), (2886, "RepositoryResolutionV3"), (2889, "UnavailableReasonV3"), (2893, "State machine phases"), (2906, "34-rule"),
    (2929, "### 9.3"), (3024, "Stage correlation"), (3061, "Negotiated payload"), (3072, "Commitments and CBOR projection"), (3151, "### 9.7"),
    (3158, "OpenUniverse and UniverseAccepted"), (3178, "OpenUniverseV3"), (3188, "UniverseAcceptedV3"), (3205, "Pre-Analyze"),
    (3270, "Coverage frames"), (3283, "Commitments"), (3287, "StageResultV2.coverageCommitment"), (3302, "CancelledV2")]] + [
    (C.IDMD, 63, "exec1_"), (C.CHK1, 27, "rust-provider-protocol.v1.json"), (C.CHK1, 851, "stage-facts.v1"), (C.CHK1, 1048, "manifestSha256"),
    (C.CHK2, 35, "rust-provider-protocol.v2.json"), (C.CHK2, 64, "check-rust-provider-protocol.py"), (C.AUDIT, 250, "G4"), (C.AUDIT, 251, "G5"),
    (C.AUDIT, 252, "G6"), (C.AUDIT, 253, "G7"), (C.AUDIT, 254, "G8"),
    (C.GAPDIR + "resolutions.md", None, "c190ee7f"), (C.GAPDIR + "resolutions.md", None, "checkRust2 line 1048"),
    (C.GAPDIR + "resolutions.md", None, "checkRust2 lines 852–1129")]


def check_cites():
    results = []
    for path, number, needle in CITES:
        text = DATA[path].decode("utf-8")
        ok = needle in (text.split("\n")[number - 1] if number else text)
        results.append({"path": path, "line": number, "needle": needle, "ok": ok})
    return results


def check_owners():
    results = {}
    for key, (path, number, needle) in C.OWNERS.items():
        if number is None:
            try:
                jsel(J(path), needle)
                ok = True
            except (KeyError, TypeError):
                ok = False
        else:
            ok = needle in lines(path)[number - 1]
        results[key] = {"path": path, "line": number, "selectorOrNeedle": needle, "ok": ok}
    return results


def v2_rule_canonical_path(value):
    if not value or value.startswith("/") or "\\" in value or "\x00" in value or re.match(r"^[A-Za-z]:", value):
        return False
    return unicodedata.normalize("NFC", value) == value and all(seg not in ("", ".", "..") for seg in value.split("/"))


def probes():
    identity = HSD["$defs"]["IdentityText"]
    wide = "\u00e9" * identity["maxLength"]
    json_admits = len(wide) <= identity["maxLength"] and re.match(identity["pattern"], wide) is not None
    ne_path = NED["$defs"]["CanonicalPath"]["pattern"]
    path_cases = {}
    for case in ["a//b", "C:/x", "a/./b", "../x", "/x", "src/lib.rs"]:
        path_cases[case] = {"nativeEvidencePatternAdmits": re.match(ne_path, case) is not None, "v2RuleAdmits": v2_rule_canonical_path(case)}
    stage = HSD["$defs"]["StageIdText"]
    return {
        "identityTextJsonAdmitsOverByteBound": {"codePoints": len(wide), "utf8Bytes": len(wide.encode()), "jsonSchemaAdmits": json_admits,
                                               "v2ByteBound": 4096, "violatesV2": len(wide.encode()) > 4096},
        "canonicalPathPatternVsV2Rule": path_cases,
        "stageIdTextCodePointsVsBytes": {"maxLength": stage["maxLength"], "utf8BytesAtMax": len(("\u00e9" * stage["maxLength"]).encode())},
    }


def vocabularies():
    v2_reasons = WS["payloadSchemas"]["UnavailableV2"]["fields"]["reason"].split("|")
    adds_text = " ".join(NEMD[2888:2891])
    adds = re.findall(r"`([a-z-]+)`", adds_text[adds_text.index("adds"):])
    ne_reason = NED["$defs"]["UnavailableReasonV3"]["enum"]
    st_reason = STD["$defs"]["UnavailableV3"]["properties"]["reason"]["enum"]
    law = STD["x-opensip-startup-law"]["postAnalyzeReasons"]["rust-semantic"]
    derived = sorted((set(v2_reasons) | set(adds)) - {"native-context-mismatch"})
    tokens = HSD["$defs"]["RustCapabilityToken"]["enum"]
    ne_tokens = NED["$defs"]["CapabilityToken"]["enum"]
    phases_text = " ".join(NEMD[2892:2898])
    phases = [p.strip() for p in re.search(r"\(host side, 22\): `(.*?)`", phases_text).group(1).split(",")]
    limit_text = " ".join(NEMD[2930:2934])
    prose_limits = [(n, int(v)) for n, v in re.findall(r"`(max\w+) (\d+)`", limit_text)]
    hs_limits = HSD["$defs"]["ProtocolLimitsV3"]
    hs_pairs = [(n, hs_limits["properties"][n]["const"]) for n in hs_limits["required"]]
    return {
        "unavailableReason": {
            "v2": v2_reasons, "section92Adds": adds, "nativeEvidenceUnavailableReasonV3": ne_reason, "startupUnavailableV3": st_reason,
            "startupLawPostAnalyzeRust": law, "derivedV2PlusAddsMinusMismatch": derived,
            "okStartupEqualsLaw": sorted(st_reason) == sorted(law), "okStartupEqualsDerived": sorted(st_reason) == derived,
            "nativeEvidenceMinusStartup": sorted(set(ne_reason) - set(st_reason)), "startupMinusNativeEvidence": sorted(set(st_reason) - set(ne_reason)),
        },
        "rustCapabilityTokens": {"handshake": tokens, "ok": sorted(tokens) == sorted(set(ne_tokens) - {"typescript-semantic-facts-v1"})
                                 and HSD["$defs"]["RustCapabilitiesV3"]["maxItems"] == len(tokens)},
        "phases": {"section92": phases, "protocol3": P3D["phases"], "ok": phases == P3D["phases"] and len(phases) == 22,
                   "v2PhaseValues": RP2["orderingAndStateMachine"]["stateRecord"]["phaseValues"],
                   "added": [p for p in P3D["phases"] if p not in RP2["orderingAndStateMachine"]["stateRecord"]["phaseValues"]]},
        "limits": {
            "okV2EqualsRows": list(RP2["limits"].items()) == RW.V2_LIMITS,
            "okHandshakeFirst24EqualV2": hs_pairs[:24] == RW.V2_LIMITS,
            "okHandshakeLast8EqualSection93": hs_pairs[24:] == RW.NEW_LIMITS == prose_limits,
            "okSupersededNativeEvidenceNames": NED["$defs"]["ProtocolLimitsV3"]["required"] == sorted(n for n, _ in RW.NEW_LIMITS),
        },
        "contractPin": {"handshakeArtifact": HSD["x-opensip-wire-law"]["expectedProtocolContractSha256"]["artifact"],
                        "handshakeSha256": HSD["x-opensip-wire-law"]["expectedProtocolContractSha256"]["sha256"],
                        "ok": HSD["x-opensip-wire-law"]["expectedProtocolContractSha256"]["sha256"] == hashlib.sha256(DATA[C.RP2]).hexdigest()},
        "c2StageSelectorsV3EqualV4": {k: C2V3D["stageSchemas"][k] == C2V4D["stageSchemas"][k] for k in ("common",)} | {
            "kinds.fact-derivation": C2V3D["stageSchemas"]["kinds"]["fact-derivation"] == C2V4D["stageSchemas"]["kinds"]["fact-derivation"],
            "coverageKey.key": C2V3D["coverageKey"]["key"] == C2V4D["coverageKey"]["key"],
            "coverageKey.key field names and order": [f["field"] for f in C2V3D["coverageKey"]["key"]] == [f["field"] for f in C2V4D["coverageKey"]["key"]]},
    }


def transition_divergences():
    ast = {r["id"]: r for r in RP2["orderingAndStateMachine"]["transitionAstV2"]["rules"]}
    p3 = {r["id"]: r for r in P3D["rules"]}
    pre_complete = P3D["wildcards"]["*PRE_COMPLETE"]["phases"]
    return {
        "section0Line118SupersedesOnlyPhaseValues": "stateRecord.phaseValues" in NEMD[117] and "transitionAstV2" not in NEMD[117],
        "cancelInStart": {"v2T023AllowsStart": "START" in ast["T023-CANCEL"]["phaseIn"], "p3PreCompleteIncludesStart": "START" in pre_complete},
        "unavailableGuard": {"v2T019Guard": ast["T019-UNAVAILABLE"]["guard"], "p3_25Guard": p3["P3-25"].get("guard")},
        "factBatchGuard": {"v2T016HasGuard": ast["T016-FACT-BATCH"]["guard"]["op"] != "true", "p3_23Guard": p3["P3-23"].get("guard")},
        "budgetGuard": {"v2T020HasGuard": ast["T020-BUDGET"]["guard"]["op"] != "true", "p3_26Guard": p3["P3-26"].get("guard")},
        "framePrecheckInP3": any("sequence" in json.dumps(v) for k, v in P3D.items() if k not in ("rules",)) ,
        "preparedCustodyOrderText": RP2["preparedOutputCustody"]["order"],
        "p3_08Next": p3["P3-08"]["next"], "p3_20Next": p3["P3-20"]["next"],
    }


def checker_facts():
    chk2 = DATA[C.CHK2].decode("utf-8")
    chk1 = DATA[C.CHK1].decode("utf-8")
    return {
        "v2CheckerTarget": re.search(r'^PROTOCOL = "(.*)"', chk2, re.M).group(1),
        "v1CheckerTarget": re.search(r'^PROTOCOL = "(.*)"', chk1, re.M).group(1),
        "v2CheckerExecutesDomains": sorted(set(re.findall(r"opensip\.rust-provider\.([a-z-]+)\.v2", chk2))),
        "v2CheckerLacks": [d for d in ("stage-facts", "stage-coverage", "fact-stream", "coverage-stream") if d in chk2],
        "v1CheckerDomains": sorted(set(re.findall(r"opensip\.rust-provider\.([a-z-]+\.v[0-9])", chk1))),
    }


def control_facts():
    return {
        "rustProviderTransport": RP2["protocolIdentity"]["transport"],
        "rustStdoutRule": RP2["framing"]["stdoutRule"],
        "controlContract": {k: CTL2.get(k) for k in ("artifact", "version", "status", "reviewStatus", "sealRecommendation", "binds", "registerRow")}
        if (CTL2 := CTL2D) else None,
        "controlDescriptorLayoutKeys": sorted(CTL2D["transportAndFraming"]["descriptorLayout"].keys()),
        "controlOwnVersionSurface": CTL2D["handshake"]["ownVersionSurface"][:160],
        "controlSchemaId": CTLS3D.get("$id"),
        "rustProtocolV2Status": {"status": RP2["status"], "reviewStatus": RP2["reviewStatus"]},
    }


def pins_crosscheck():
    pins = {p["path"]: p["sha256"] for p in J(C.PINS)["pins"] if isinstance(p, dict) and "path" in p}
    out = {}
    for path, (sha, _) in C.SOURCES.items():
        if path in pins:
            out[path] = {"nativeSourcePins": pins[path], "read": sha, "match": pins[path] == sha}
    return out


# ---------------------------------------------------------------------------------------------- core checks
def run_checks(rows, frames, comps):
    failures = []
    inherited = [k for k in rows if rows[k]["group"] in ("envelope", "payloadSchemas", "definitions")] + [k for k in frames if frames[k]["group"] == "frameSchemas"]
    expected = expected_inherited_keys()
    if sorted(inherited) != sorted(expected):
        failures.append("inherited coverage: missing %s extra %s" % (sorted(set(expected) - set(inherited)), sorted(set(inherited) - set(expected))))
    ext = [k for k in rows if rows[k]["group"] == "external"]
    if sorted(ext) != sorted(expected_external_keys()):
        failures.append("external coverage: missing %s extra %s" % (sorted(set(expected_external_keys()) - set(ext)), sorted(set(ext) - set(expected_external_keys()))))
    for name, spec in WS["payloadSchemas"].items():
        order = [k.split(".", 2)[2] for k in rows if k.startswith(f"payloadSchemas.{name}.")]
        if order != spec["required"]:
            failures.append(f"member order {name}")
        extra_fields = set(spec.get("fields", {})) - set(spec["required"]) - {"all"}
        if extra_fields:
            failures.append(f"{name} fields keys outside required: {sorted(extra_fields)}")
    for name, spec in WS["definitions"].items():
        extra_fields = set(spec.get("fields", {})) - set(spec.get("required", [])) - {"all", "remaining"}
        if extra_fields:
            failures.append(f"{name} fields keys outside required: {sorted(extra_fields)}")
    wire_checked, wire_skipped, mismatches, refs = 0, 0, [], 0
    for key, row in rows.items():
        if row["disposition"] not in C.DISPOSITIONS:
            failures.append(f"{key}: disposition {row['disposition']}")
        if row["successorMemberChange"] not in C.MEMBER_CHANGES:
            failures.append(f"{key}: member change")
        if row["resolutionClass"] not in C.CLASSES:
            failures.append(f"{key}: class")
        if not (C.wire_ok(row["inheritedWireType"]) and C.wire_ok(row["wireType"])):
            failures.append(f"{key}: wire spelling")
        if row["disposition"] == "replaced" and row["successorMemberChange"] is None:
            failures.append(f"{key}: replaced without member change")
        if (row["disposition"] == "removed" or row["successorMemberChange"] == "removed") and row["wireType"] is not None:
            failures.append(f"{key}: removed member has a major-3 wire type")
        if row["disposition"] not in ("removed",) and row["successorMemberChange"] != "removed" and row["wireType"] is None \
                and not key.startswith("external.RustUniverseV1.resolvedInputs.") and row["group"] != "definitions":
            failures.append(f"{key}: live member without wire type")
        if row["group"] != "new" and row["disposition"] == "new":
            failures.append(f"{key}: inherited row marked new")
        for gap in row["gaps"]:
            if gap not in C.GAPS:
                failures.append(f"{key}: unknown gap {gap}")
        if row["disposition"] == "unresolved" and not row["gaps"]:
            failures.append(f"{key}: unresolved without gap")
        if row["resolutionClass"] != "governed" and not row["gaps"]:
            failures.append(f"{key}: non-governed class without gap")
        for check in row["handwrittenChecks"]:
            owner = re.split(r"[ :]", check, maxsplit=1)[0]
            if owner not in C.OWNERS:
                failures.append(f"{key}: unknown semantic owner {owner}")
        ref = row["schemaNativeRef"]
        if ref:
            refs += 1
            try:
                doc_id, node = resolve(ref)
            except (KeyError, IndexError, ValueError):
                failures.append(f"{key}: unresolved ref {ref}")
                continue
            if row["wireType"] and C.X not in row["wireType"] and C.B not in row["wireType"]:
                got = wire_of(node, doc_id)
                if got is None:
                    wire_skipped += 1
                else:
                    wire_checked += 1
                    if got != row["wireType"]:
                        mismatches.append(f"{key}: row {row['wireType']} vs ref {got}")
    for key, frame in frames.items():
        for gap in frame["gaps"]:
            if gap not in C.GAPS:
                failures.append(f"{key}: unknown gap {gap}")
        if frame["schemaNativeRef"]:
            refs += 1
            try:
                resolve(frame["schemaNativeRef"])
            except (KeyError, IndexError, ValueError):
                failures.append(f"{key}: unresolved ref")
        rule_ids = {r["id"] for r in P3D["rules"]}
        for rule in frame["transitionRules"]:
            if rule not in rule_ids:
                failures.append(f"{key}: unknown transition rule {rule}")
        if frame["group"] == "frameSchemas":
            src = WS["frameSchemas"][frame["name"]]
            if src["direction"] != frame["direction"] or src["workerTerminal"] != frame["workerTerminal"]:
                failures.append(f"{key}: direction/terminal differs from v2 row")
    table = frame_table()
    for name in RW.NEW_FRAMES:
        row = table.get(name)
        if row is None or row["direction"] != RW.NEW_FRAMES[name]["direction"] or (row["terminal"] == "yes") != RW.NEW_FRAMES[name]["workerTerminal"]:
            failures.append(f"new frame {name} differs from §9.2 table {row}")
    p3_frames = {r["frame"] for r in P3D["rules"]} - {"zero-exit", "eof", "*", "*PROCESS_FAULT"}
    rust3_frames = {f for f in RW.FRAMES if f != "Coverage"} | set(RW.NEW_FRAMES)
    if p3_frames != rust3_frames:
        failures.append(f"frame vocabulary vs protocol3-transitions: {sorted(p3_frames ^ rust3_frames)}")
    if len(rust3_frames) != 26:
        failures.append("frame vocabulary is not 26")
    for comp in comps:
        if not comp["ok"]:
            failures.append("comparison drift: " + comp["label"] + f" removed={comp['removed']} added={comp['added']}")
    if mismatches:
        failures += ["wire mismatch " + m for m in mismatches]
    for gap in C.GAPS:
        if not any(gap in r["gaps"] for r in list(rows.values()) + list(frames.values())) and gap not in ("R3-G17", "R3-G18", "R3-G19", "R3-G2"):
            failures.append(f"gap {gap} cited by no row")
    return failures, {"wireTypeCrossChecks": {"checked": wire_checked, "skipped": wire_skipped, "mismatches": mismatches}, "rowRefs": refs,
                      "p3Frames": sorted(p3_frames)}


CLOSURE_ROOTS = [C.HS + n for n in ("HelloV3", "HelloAckV3", "ExpectedRustIdentityV3", "RustCapabilitiesV3", "ProtocolLimitsV3", "RustFactBatchV2Vector", "IdentityVersionsV1")] + \
    [C.ST + n for n in ("OpenUniverseV3", "UniverseAcceptedV3", "NativeContextVerifiedV1", "PreAnalyzeUnavailableV1", "CoverageV3", "UnavailableV3", "BudgetExhaustedV3",
                        "RustSemanticUniverseV2")] + \
    [C.NE + n for n in ("DependencySourceManifestV3", "DependencySourceSealV3", "RepositoryResolutionV3", "CoverageResultV3", "RustUniverseV2ResolvedInputs")] + \
    [C.FB, C.OC, C.DB]


def everything():
    rows, frames = assemble()
    comps = comparisons()
    failures, stats = run_checks(rows, frames, comps)
    failures = SOURCE_FAILURES + failures
    clos = closure(CLOSURE_ROOTS)
    if clos["unresolved"]:
        failures.append("closure unresolved: %s" % clos["unresolved"])
    superseded_reached = [t for t in clos["reached"] if any(t.endswith("/$defs/" + n) and t.startswith(C.NE.split("#")[0]) for n in ("HelloV3", "HelloAckV3", "ProtocolLimitsV3", "UnavailableReasonV3"))]
    if superseded_reached:
        failures.append("superseded native-evidence defs reached: %s" % superseded_reached)
    cites = check_cites()
    failures += ["cite anchor " + json.dumps(c) for c in cites if not c["ok"]]
    owners = check_owners()
    failures += ["owner anchor " + k for k, v in owners.items() if not v["ok"]]
    vocab = vocabularies()
    for label, ok in [("unavailable reason startup==law", vocab["unavailableReason"]["okStartupEqualsLaw"]),
                      ("unavailable reason startup==v2+adds-mismatch", vocab["unavailableReason"]["okStartupEqualsDerived"]),
                      ("capability tokens", vocab["rustCapabilityTokens"]["ok"]), ("phases", vocab["phases"]["ok"]),
                      ("contract pin", vocab["contractPin"]["ok"])] + [("limits " + k, v) for k, v in vocab["limits"].items()] + \
            [("c2 v3==v4 " + k, v) for k, v in vocab["c2StageSelectorsV3EqualV4"].items() if k != "coverageKey.key"]:
        if not ok:
            failures.append("vocabulary check failed: " + label)
    return rows, frames, comps, failures, stats, clos, cites, owners, vocab


# ---------------------------------------------------------------------------------------------- selftest
def selftest():
    base_rows, base_frames = assemble()
    base_comps = comparisons()
    base_fail, _ = run_checks(base_rows, base_frames, base_comps)
    assert not base_fail, base_fail
    mutations = []

    def mutate(label, fn):
        rows, frames, comps = copy.deepcopy(base_rows), copy.deepcopy(base_frames), copy.deepcopy(base_comps)
        fn(rows, frames, comps)
        fails, _ = run_checks(rows, frames, comps)
        mutations.append({"mutation": label, "detected": bool(fails), "firstFailure": fails[0] if fails else None})

    mutate("drop inherited row payloadSchemas.HelloV2.limits", lambda r, f, c: r.pop("payloadSchemas.HelloV2.limits"))
    mutate("add extra inherited row", lambda r, f, c: r.__setitem__("payloadSchemas.HelloV2.bogus", dict(r["payloadSchemas.HelloV2.limits"], member="bogus")))
    mutate("unresolvable schema ref", lambda r, f, c: r["payloadSchemas.HelloV2.limits"].__setitem__("schemaNativeRef", C.HS + "Nope"))
    mutate("wrong wire type vs resolved ref", lambda r, f, c: r["definitions.ProtocolLimitsV2.maxScratchBytes"].__setitem__("wireType", C.T))
    mutate("unknown gap id", lambda r, f, c: r["envelope.payload"]["gaps"].append("R3-G99"))
    mutate("unknown semantic owner", lambda r, f, c: r["envelope.payload"]["handwrittenChecks"].append("nobody.admit"))
    mutate("unexpected successor delta", lambda r, f, c: c.__setitem__(0, compare("HelloV2", ["a"], ["b"], [], [])))
    mutate("drop external expansion row", lambda r, f, c: r.pop("external.FactCandidateV1.anchors"))
    mutate("frame direction drift", lambda r, f, c: f["frameSchemas.Cancel"].__setitem__("direction", "worker-to-host"))
    mutate("unknown transition rule", lambda r, f, c: f["frameSchemas.Complete"]["transitionRules"].append("P3-99"))
    mutate("non-governed row without gap", lambda r, f, c: r["envelope.direction"].__setitem__("resolutionClass", "owner-missing"))
    mutate("removed member keeps wire type", lambda r, f, c: r["definitions.RepositoryResolutionV2.mode"].__setitem__("wireType", C.T))
    return mutations


# ---------------------------------------------------------------------------------------------- output
def cell(value):
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        value = "; ".join(str(v) for v in value)
    return str(value).replace("|", "\\|").replace("\n", " ")


def main():
    if "--selftest" in sys.argv:
        results = selftest()
        for item in results:
            print(("DETECTED " if item["detected"] else "MISSED   ") + item["mutation"] + " :: " + str(item["firstFailure"]))
        missed = [m for m in results if not m["detected"]]
        print(f"selftest mutations: {len(results)}, detected: {len(results) - len(missed)}, missed: {len(missed)}")
        return 1 if missed else 0

    rows, frames, comps, failures, stats, clos, cites, owners, vocab = everything()
    probe = probes()
    trans = transition_divergences()
    chk = checker_facts()
    ctl = control_facts()
    pins = pins_crosscheck()
    status = git_status([p for p in C.SOURCES if not p.startswith("/")])

    groups = {}
    for row in rows.values():
        groups.setdefault(row["group"], 0)
        groups[row["group"]] += 1
    dispositions, classes = {}, {}
    for row in list(rows.values()) + list(frames.values()):
        dispositions[row["disposition"]] = dispositions.get(row["disposition"], 0) + 1
        classes[row["resolutionClass"]] = classes.get(row["resolutionClass"], 0) + 1
    gap_members = {g: sorted([k for k, r in rows.items() if g in r["gaps"]] + [k for k, r in frames.items() if g in r["gaps"]]) for g in C.GAPS}
    inherited_members = sum(1 for r in rows.values() if r["group"] in ("envelope", "payloadSchemas", "definitions")) + \
        sum(1 for f in frames.values() if f["group"] == "frameSchemas")

    coverage = {
        "inheritedGrammarMembers": inherited_members,
        "byGroup": {"envelope": groups.get("envelope", 0), "frameSchemas": len(RW.FRAMES), "payloadSchemas": groups.get("payloadSchemas", 0),
                    "definitions": groups.get("definitions", 0)},
        "externalExpansionRows": groups.get("external", 0),
        "newSchemaNativeMemberRows": groups.get("new", 0),
        "newFrameRows": len(RW.NEW_FRAMES),
        "rust3FrameVocabulary": len(stats["p3Frames"]),
        "dispositions": dict(sorted(dispositions.items())),
        "resolutionClasses": dict(sorted(classes.items())),
        "rowsWithUnstatedWireType": sum(1 for r in rows.values() if r["wireType"] and C.X in r["wireType"]),
        "rowsWithSchemaNativeRef": sum(1 for r in list(rows.values()) + list(frames.values()) if r["schemaNativeRef"]),
        "rowsWithHandwrittenChecks": sum(1 for r in rows.values() if r["handwrittenChecks"]),
        "rowsCitingGaps": sum(1 for r in list(rows.values()) + list(frames.values()) if r["gaps"]),
        "wireTypeCrossChecks": stats["wireTypeCrossChecks"],
        "refClosure": {k: v for k, v in clos.items() if k != "reached"},
        "memberListComparisons": len(comps),
        "citationAnchors": {"checked": len(cites), "failed": sum(1 for c in cites if not c["ok"])},
        "semanticOwnerAnchors": {"checked": len(owners), "failed": sum(1 for v in owners.values() if not v["ok"])},
        "vocabularies": vocab,
        "jsonVsCborProbes": probe,
        "transitionDivergences": trans,
        "checkerFacts": chk,
        "controlOwner": ctl,
        "nativeSourcePinsCrosscheck": pins,
        "gitStatusOfPinnedSources": status,
        "failures": failures,
    }
    fields = {
        "artifact": "opensip.m1.rust3-wire-translation",
        "version": 1,
        "standing": "PROPOSED implementation artifact for root review. Not an approval, not a wire change, not a schema document, not product code. Authored by actual Claude; every unaccepted proposal remains a proposal.",
        "protocol": {"providerId": "rust-semantic", "protocolMajor": 3, "inheritedBase": C.RP2 + " $.wireSchema"},
        "conventions": {
            "wireTypes": sorted(C.WIRE_BASE), "nullable": "X|null means present null (rust2 schemaLanguage.maps); no Rust3 member is omitted except the optional C-2 planStage members",
            "dispositions": sorted(C.DISPOSITIONS), "memberChanges": sorted(m for m in C.MEMBER_CHANGES if m), "resolutionClasses": sorted(C.CLASSES),
            "typeSource": "where the wire type comes from: field-text, definition, echo, rust2 commitments/algorithms, derived (labeled), successor schema, external owner, or UNSTATED",
            "schemaNativeRef": "an $id#pointer into a pinned owner document; fact-batch.3 candidate refs are JSON-vector mirrors, not wire records",
        },
        "sources": [{"path": p, "sha256": s, "bytes": n, "gitStatus": status.get(p) if isinstance(status, dict) else None} for p, (s, n) in C.SOURCES.items()],
        "semanticOwners": owners,
        "envelope": {k: v for k, v in rows.items() if v["group"] == "envelope"},
        "frames": frames,
        "rows": {k: v for k, v in rows.items() if v["group"] in ("payloadSchemas", "definitions")},
        "externalRows": {k: v for k, v in rows.items() if v["group"] == "external"},
        "newRows": {k: v for k, v in rows.items() if v["group"] == "new"},
        "gaps": {g: dict(spec, citedBy=gap_members[g]) for g, spec in C.GAPS.items()},
        "memberListComparisons": comps,
    }
    with open(os.path.join(OUT, "fields.json"), "w", encoding="utf-8") as handle:
        json.dump(fields, handle, indent=1, sort_keys=False, ensure_ascii=False)
        handle.write("\n")
    with open(os.path.join(OUT, "coverage.json"), "w", encoding="utf-8") as handle:
        json.dump(coverage, handle, indent=1, sort_keys=False, ensure_ascii=False)
        handle.write("\n")
    with open(os.path.join(OUT, "translation.md"), "w", encoding="utf-8") as handle:
        handle.write(render_md(rows, frames, comps, coverage))
    print(json.dumps({k: coverage[k] for k in ("inheritedGrammarMembers", "byGroup", "externalExpansionRows", "newSchemaNativeMemberRows", "newFrameRows",
                                               "dispositions", "resolutionClasses", "rowsWithUnstatedWireType", "wireTypeCrossChecks", "refClosure",
                                               "memberListComparisons", "citationAnchors", "semanticOwnerAnchors")}, indent=1))
    print("failures:", len(failures))
    for failure in failures:
        print("  FAIL", failure)
    return 1 if failures else 0


ROW_HEAD = "| member | presence | v2 wire | Rust3 wire | bounds / vocabulary | disposition (change) | class | schema-native ref | type source | semantic-owner checks | gaps |\n|---|---|---|---|---|---|---|---|---|---|---|\n"


def row_line(member, r):
    change = f" ({r['successorMemberChange']})" if r["successorMemberChange"] else ""
    return "| " + " | ".join(cell(v) for v in [member, r["presence"], r["inheritedWireType"], r["wireType"], r["boundsOrVocabulary"],
                                                r["disposition"] + change, r["resolutionClass"], r["schemaNativeRef"], r["typeSource"],
                                                r["handwrittenChecks"], r["gaps"]]) + " |\n"


def render_md(rows, frames, comps, cov):
    out = []
    w = out.append
    w(HEAD.format(**{"inherited": cov["inheritedGrammarMembers"], "ext": cov["externalExpansionRows"], "new": cov["newSchemaNativeMemberRows"],
                     "newframes": cov["newFrameRows"], "disp": json.dumps(cov["dispositions"]), "cls": json.dumps(cov["resolutionClasses"]),
                     "unstated": cov["rowsWithUnstatedWireType"], "wc": cov["wireTypeCrossChecks"]["checked"], "wm": len(cov["wireTypeCrossChecks"]["mismatches"]),
                     "ws": cov["wireTypeCrossChecks"]["skipped"], "refs": cov["rowsWithSchemaNativeRef"], "cr": cov["refClosure"]["refsFollowed"],
                     "ct": cov["refClosure"]["distinctTargets"], "cu": len(cov["refClosure"]["unresolved"]), "cmp": cov["memberListComparisons"],
                     "cites": cov["citationAnchors"]["checked"], "owners": cov["semanticOwnerAnchors"]["checked"], "fail": len(cov["failures"]),
                     "env": cov["byGroup"]["envelope"], "fr": cov["byGroup"]["frameSchemas"], "pay": cov["byGroup"]["payloadSchemas"], "defs": cov["byGroup"]["definitions"]}))
    w(STATIC_SECTIONS)
    w("\n## 7. Frame table (Rust3, 26 names)\n\n| frame | direction | worker terminal | Rust3 payload | disposition | class | ref | P3 rules | notes | gaps |\n|---|---|---|---|---|---|---|---|---|---|\n")
    for key, f in frames.items():
        w("| " + " | ".join(cell(v) for v in [f["name"] + (" (inherited)" if f["group"] == "frameSchemas" else " (new)"), f["direction"], f["workerTerminal"],
                                             f["payload"], f["disposition"], f["resolutionClass"], f["schemaNativeRef"], f["transitionRules"], f["derivation"], f["gaps"]]) + " |\n")
    w("\n## 8. Field rows: every inherited member\n\nSource for every row: `" + C.RP2 + "` sha256 `" + C.SOURCES[C.RP2][0] + "`; the exact selector and original field text are in `fields.json` (`rows[].source`).\n")
    w("\n### envelope (`RustProviderEnvelopeV2`; no published major-3 record name, R3-G3)\n\n" + ROW_HEAD)
    for key, r in rows.items():
        if r["group"] == "envelope":
            w(row_line(r["member"], r))
    current = None
    for key, r in rows.items():
        if r["group"] not in ("payloadSchemas", "definitions"):
            continue
        label = f"{r['group']}.{r['record']}" if r["member"] is not None else f"{r['group']} (records without a member list)"
        if label != current:
            current = label
            spec = (WS[r["group"]].get(r["record"], {}) if r["member"] is not None else {})
            extra = ""
            if spec.get("variants"):
                extra = "\n\nInherited variants: " + cell(json.dumps(spec["variants"], ensure_ascii=False))
            if spec.get("external"):
                extra += "\n\nInherited external: `" + spec["external"] + "`"
            w(f"\n### {label}{extra}\n\n" + ROW_HEAD)
        w(row_line(r["member"] if r["member"] is not None else r["record"], r))
    w("\n## 9. External expansions (members reached through `external` definitions)\n")
    current = None
    for key, r in rows.items():
        if r["group"] != "external":
            continue
        if r["record"] != current:
            current = r["record"]
            w(f"\n### {current} (source `{r['source']['path']}` {r['source']['selector']})\n\n" + ROW_HEAD)
        w(row_line(r["member"], r))
    w("\n## 10. New schema-native members on the Rust3 wire\n\n| record.member | Rust3 wire | bounds / vocabulary | class | ref / source | semantic-owner checks | gaps |\n|---|---|---|---|---|---|---|\n")
    for key, r in rows.items():
        if r["group"] == "new":
            w("| " + " | ".join(cell(v) for v in [key[4:], r["wireType"], r["boundsOrVocabulary"], r["resolutionClass"], r["schemaNativeRef"] or r["source"]["selector"],
                                                 r["handwrittenChecks"], r["gaps"]]) + " |\n")
    w("\n## 11. Member-list comparisons (mechanical; each has a declared expected delta, and drift fails the build)\n\n| comparison | kept | removed | added | same order | ok | note |\n|---|---|---|---|---|---|---|\n")
    for c in comps:
        w("| " + " | ".join(cell(v) for v in [c["label"], f"{c['kept']}/{c['originalCount']}", json.dumps(c["removed"]), json.dumps(c["added"]), c["sameOrder"], c["ok"], c["note"]]) + " |\n")
    v = cov["vocabularies"]
    w("\n## 12. Vocabulary, limit and pin checks\n\n")
    w(f"- Unavailable reasons: v2 {v['unavailableReason']['v2']}; §9.2 adds {v['unavailableReason']['section92Adds']}; startup `UnavailableV3` = startup law = (v2 ∪ adds) − native-context-mismatch: "
      f"{v['unavailableReason']['okStartupEqualsLaw'] and v['unavailableReason']['okStartupEqualsDerived']}. native-evidence `UnavailableReasonV3` − startup: {v['unavailableReason']['nativeEvidenceMinusStartup']}; "
      f"startup − native-evidence: {v['unavailableReason']['startupMinusNativeEvidence']} (R3-G7; not referenced by any Rust3 carrier).\n")
    w(f"- `RustCapabilityToken` = native `CapabilityToken` − typescript-semantic-facts-v1 and maxItems = count: {v['rustCapabilityTokens']['ok']}.\n")
    w(f"- 22 phases, §9.2 prose == protocol3-transitions: {v['phases']['ok']}; phases added over v2 `phaseValues`: {v['phases']['added']}.\n")
    w(f"- Limits: {json.dumps(v['limits'])}.\n")
    w(f"- `expectedProtocolContractSha256` pin equals the bytes read: {v['contractPin']['ok']}.\n")
    w(f"- C-2 selectors v3 vs v4: {json.dumps(v['c2StageSelectorsV3EqualV4'])}. Where `coverageKey.key` is unequal while its field names and order are equal, "
      "v4 adds per-field annotations (jsonType/checked/wireType/boundHere); rust2 references v3, and §0:136 names only v4.\n")
    t = cov["transitionDivergences"]
    w("\n## 13. Ordering: protocol3-transitions vs retained v2 transitionAstV2 (R3-G17)\n\n")
    w(f"- §0:118 supersedes only `stateRecord.phaseValues`: {t['section0Line118SupersedesOnlyPhaseValues']}.\n")
    w(f"- Cancel in START: v2 T023 allows {t['cancelInStart']['v2T023AllowsStart']}; P3 `*PRE_COMPLETE` includes START {t['cancelInStart']['p3PreCompleteIncludesStart']}.\n")
    w(f"- Unavailable: v2 T019 guard `{json.dumps(t['unavailableGuard']['v2T019Guard'])}`; P3-25 guard `{t['unavailableGuard']['p3_25Guard']}`.\n")
    w(f"- FactBatch: v2 T016 guarded {t['factBatchGuard']['v2T016HasGuard']}, P3-23 guard `{t['factBatchGuard']['p3_23Guard']}`; BudgetExhausted: v2 T020 guarded {t['budgetGuard']['v2T020HasGuard']}, P3-26 guard `{t['budgetGuard']['p3_26Guard']}`.\n")
    w(f"- v2 `preparedOutputCustody.order`: \"{t['preparedCustodyOrderText']}\"; P3-08 next `{t['p3_08Next']}`, P3-20 next `{t['p3_20Next']}`.\n")
    k = cov["checkerFacts"]
    w("\n## 14. Executable-owner facts\n\n")
    w(f"- `check-rust-provider-protocol-v2.py` targets `{k['v2CheckerTarget']}` and executes rust-provider domains {k['v2CheckerExecutesDomains']}; it contains none of stage-facts/stage-coverage/fact-stream/coverage-stream: {k['v2CheckerLacks'] == []}.\n")
    w(f"- `check-rust-provider-protocol.py` targets `{k['v1CheckerTarget']}` with domains {k['v1CheckerDomains']}; it is not a v2 owner (R3-G19).\n")
    ctl = cov["controlOwner"]
    w("\n## 15. Common-control separation\n\n")
    w(f"- Rust provider plane: transport \"{ctl['rustProviderTransport']}\"; stdout rule \"{ctl['rustStdoutRule']}\". Provider frames are CBOR on fd0/fd1 only.\n")
    w(f"- Candidate control owner `{C.CTL2}` in-file fields: {json.dumps(ctl['controlContract'], ensure_ascii=False)}; descriptor layout keys {ctl['controlDescriptorLayoutKeys']}; "
      f"control schema `$id` `{ctl['controlSchemaId']}`. Its own-version surface text begins: \"{ctl['controlOwnVersionSurface']}...\".\n")
    w("- Translation consequence: no control member, discriminator or framing byte enters any Rust3 carrier; `controlMajor` is a separate axis from provider protocolMajor 3; "
      "the owner selection is R3-G18 (proposal-pending). Rust v2 itself is in-file `" + json.dumps(ctl["rustProtocolV2Status"]) + "` yet is the pinned inherited base "
      "(`HelloV3.expectedProtocolContractSha256`; audit §3.2).\n")
    p = cov["jsonVsCborProbes"]
    w("\n## 16. JSON Schema is not CBOR admission (probes, R3-G2)\n\n")
    w(f"- IdentityText: a {p['identityTextJsonAdmitsOverByteBound']['codePoints']}-code-point NFC string of {p['identityTextJsonAdmitsOverByteBound']['utf8Bytes']} UTF-8 bytes is admitted by the JSON Schema: "
      f"{p['identityTextJsonAdmitsOverByteBound']['jsonSchemaAdmits']}; violates the v2 4096-byte bound: {p['identityTextJsonAdmitsOverByteBound']['violatesV2']}.\n")
    w("- native-evidence `CanonicalPath` pattern vs the v2 CanonicalPath rule: " + json.dumps(p["canonicalPathPatternVsV2Rule"]) + ".\n")
    w(f"- StageIdText maxLength {p['stageIdTextCodePointsVsBytes']['maxLength']} counts code points ({p['stageIdTextCodePointsVsBytes']['utf8BytesAtMax']} UTF-8 bytes possible).\n")
    w("- Not checkable by any pinned JSON Schema: NFC; shortest-form integers and lengths; absence of floats, tags, negative integers and indefinite items; duplicate or non-text keys; "
      "length-first map key order; decode-once/re-encode byte equality; byte-string lengths; x-opensip-order utf8/candidateOrdinal/sequence; cross-record echoes and joins; commitments; "
      "the frame digest prefix. `Uint64` as a JSON integer also cannot express the CBOR major-type-0 encoding.\n")
    w("\n## 17. Gap register\n\n| id | class | title | action | cited by |\n|---|---|---|---|---|\n")
    for gap, spec in C.GAPS.items():
        cited = [kk for kk, r in list(rows.items()) + list(frames.items()) if gap in r["gaps"]]
        w("| " + " | ".join(cell(x) for x in [gap, spec["class"], spec["title"], spec["action"], f"{len(cited)} rows"]) + " |\n")
    for gap, spec in C.GAPS.items():
        w(f"\n### {gap}: {spec['title']} ({spec['class']})\n\n{spec['finding']}\n")
    w(TAIL)
    w("\n## 21. Source pins (bytes read)\n\n| path | sha256 | bytes | git |\n|---|---|---|---|\n")
    status = cov["gitStatusOfPinnedSources"]
    for path, (sha, size) in C.SOURCES.items():
        w(f"| `{path}` | `{sha}` | {size} | {cell(status.get(path, '') if isinstance(status, dict) else '')} |\n")
    w("\n`docs/implementation/README.md` changed on disk during authoring (first read sha256 `e1204151c30bff15e541c927afc03e3f671b43e0f760c11e49388022b14f8572`, 14955 bytes); "
      "the pin above is the re-read. Its new text records the common-control owner chain as under root verification and changes no Rust3 disposition.\n")
    w("\nnative/source-pins.v2.json agreement for pinned paths: " + json.dumps({k: v["match"] for k, v in cov["nativeSourcePinsCrosscheck"].items()}) + "\n")
    return "".join(out)


HEAD = """# Rust3 wire translation inventory: `rust-semantic` provider protocol major 3

**Standing.** This is a proposed implementation artifact for root review, authored by actual Claude. It is not approval, not a wire change, not a schema document and not product code. It supplies audit `m1-generation-owner-audit-01` item T2 (the Rust3 projection of `rust-provider-protocol.v2` retained selectors), as the TS2 inventory did for T1. No architecture, product or other candidate file was modified. Every unaccepted proposal cited here stays a proposal.

**Scope.** Every member of `docs/coop/artifacts/rust-provider-protocol.v2.json` `$.wireSchema` (`envelope`, `frameSchemas`, `payloadSchemas`, `definitions`), the members reached through its `external` definitions, and the schema-native members that replace them. Dispositions come from `native-evidence.md` §0 rows 117-130, §3.2, §3.6, §4.1a and §9.1-§9.7. Field-level successors come from `native/provider-handshake.schemas.v1.json`, `native/provider-startup.schemas.v1.json`, `native/native-evidence.schemas.v2.json` (non-superseded defs), `native/fact-batch.schema.v3.json`, `native/occupancy-companion.schema.v1.json`, `native/dispatch-binding.schema.v1.json` and `native/protocol3-transitions.v1.json`. `rust-provider-protocol` v1/v3/v4 and their checkers are not owners. `rust-provider-protocol.v2` stays the inherited base: `HelloV3.expectedProtocolContractSha256` pins its bytes. The TS2 translation and the gap-resolution proposals were read for method and cross-reference only.

**Machine form.** `fields.json` holds every row, with source path, pinned sha256, selector and exact original field text. `coverage.json` holds counts, every check result, probes and pins. `tools/build.py` regenerates all three from `tools/common.py` and `tools/rows.py`. It opens sources read-only and fails on:
- source byte drift;
- an uncovered or extra member;
- an unresolvable ref or `$ref`;
- a wire-type mismatch against a resolvable ref;
- an unexpected successor delta;
- a prose/schema member mismatch;
- a moved citation anchor.

`--selftest` applies mutation controls. Logs are in `logs/`.

```
OPENSIP_ARCH=/Users/sb/code/opensip-ai/opensip_arch python3 tools/build.py
OPENSIP_ARCH=/Users/sb/code/opensip-ai/opensip_arch python3 tools/build.py --selftest
```

## 1. Coverage

- inherited grammar members tabulated: **{inherited}** (envelope {env}, frameSchemas {fr}, payloadSchemas {pay}, definitions {defs})
- external expansion rows: **{ext}**; new schema-native member rows: **{new}**; new frame rows: **{newframes}**
- dispositions (rows + frames): {disp}
- resolution classes (rows + frames): {cls}
- rows whose Rust3 wire type is UNSTATED: {unstated}
- rows/frames with schema-native ref: {refs}; wire-type cross-checks: {wc} checked, {ws} not derivable, **{wm} mismatches**
- transitive `$ref` closure of the Rust3 successor records: {cr} refs followed, {ct} distinct targets, **{cu} unresolved**
- member-list comparisons: {cmp}; citation anchors verified: {cites}; semantic-owner anchors verified: {owners}
- build failures: **{fail}**
"""

STATIC_SECTIONS = """
## 2. Conventions

- **Wire type** uses rust2 `canonicalCbor.closedDataModel`: `null`, `bool`, `uint64`, `UTF-8-NFC-text`, `byte-string`, `definite-array`, `definite-text-keyed-map`. Negative integers are forbidden on the Rust wire. `X|null` means present-and-null; rust2 `schemaLanguage.maps` says nullable is never omission. `UNSTATED` means no bounded owner states the CBOR type. Such a row cites a gap and makes no guess.
- **Two wire columns.** `v2 wire` is the inherited type and `Rust3 wire` the major-3 type. A type change (map -> array for capabilities) is visible.
- **Type source** says where the type comes from:
  - field text or a definition;
  - an echo of a typed member;
  - a rust2 algorithm or commitment;
  - a labeled derivation, such as `rust2 limitPolicy.arithmetic` for counts and offsets;
  - the successor schema, or an external owner.

  Derivations are never presented as owner text.
- **Disposition:**
  - `retained`: unchanged.
  - `replaced`: a successor owns the member, with member change `unchanged`, `value-changed`, `moved` or `removed`.
  - `value-substituted`: same name and shape, with a stated supersession of the value domain.
  - `new`: schema-native and absent from v2.
  - `removed`: no Rust3 wire carrier.
  - `unresolved`: no consistent major-3 owner.
- **Resolution class:**
  - `governed`: an owner states the answer.
  - `owner-missing`: no bounded owner states it.
  - `owner-contradictory`: owners disagree.
  - `proposal-pending`: only an unaccepted proposal answers it.
  - `implementation-choice`: no wire question.
- **Shape vs semantic owner.** A schema-native ref owns shape only. The `semantic-owner checks` column names the law that shape cannot express. That law may be a rust2 selector, a reference-model function verified at its line, the dispatch schema, fact-plane or C-2. Those models are executable law within their stated scope. They are not implementation admission code.

## 3. Envelope

The major-3 envelope keeps the five inherited members `{protocolMajor, direction, sequence, frameType, payload}`. All are required and closed. `direction` is Rust-only; the TS2 envelope has no such member.
- **protocolMajor** is exactly 3 (native-evidence.md:122; handshake law `frameAndMajor.rust-semantic`).
- **frameType** is the closed 26-name vocabulary. `Coverage` is renamed `CoverageV3` (:129, :2884). DependencySource{Manifest,Chunk,Seal,Accepted} and NativeContextVerified are added (§9.2). The vocabulary equals the frame set of `protocol3-transitions.v1.json` (checked).
- **sequence and direction** keep the v2 frame precheck. §0 does not supersede it; see R3-G17.
- **payload** is selected by `frameType`, except FactBatch (negotiated token) and Unavailable (phase) (R3-G6).

Framing is 8-byte big-endian length, 32 raw SHA-256 bytes, then the canonical-CBOR payload (rust2 `framing`, 40-byte prefix). It is not CBOR members. No major-3 envelope record name is published (R3-G3). The wire carries none, and this translation proposes no published name.

## 4. Stage identity: C-2 text vs Analyze ordinal vs Plan ordinal

| carrier | member | wire | meaning |
|---|---|---|---|
| `StageRequestV2` | `stageOrdinal` | uint64 | contiguous 0..n-1 in **this** Analyze (= `DispatchBindingV1.analyzeRequestOrdinal`) |
| `StageRequestV2.planStage` | `stageId` | text | exact C-2 stageId text inside the nested, byte-exact C-2 stage; 1..255 through `DispatchBindingV1.expectedStageId`, which names `StageRequestV2.planStage.stageId` |
| `FactBatchV2` / `FactBatchV3` | `stageId` | text (StageIdText) | echo of `planStage.stageId`; never `stageOrdinal`, never `retainedStageOrdinal` |
| `CoverageV3` | `stageId` | text | attributes every `CoverageResultV3` entry (entries carry no stageId/entryOrdinal) |
| `UnavailableV3` | `affectedStageIds` | array of text | all requested stageIds, request order |
| `BudgetExhaustedV3` | `triggerStageId` | text | the stage whose budget unit was exhausted |
| `StageResultV2` | `stageId` | text | exact requested stageId. **No `stageOrdinal` and no `factBatchCount`**, unlike TS `StageResultV1` |
| `PreAnalyzeUnavailableV1` | none | none | no stage member; host derives affected stages from `planAndDomainProjection.selectedStageRule` |
| host only | `retainedStageOrdinal` | none | `execution-plan.stages[].ordinal`; never on the wire (native-evidence.md:3024-3043) |

Differences from TS2:
- Rust nests the C-2 stage (`planStage`), so optional C-2 members (`dependsOn`, `budget`, `capabilityGrants`, `providerId`) are **present only when present in the ExecutionPlan**. A carrier must preserve absence.
- Rust `analysisOrdinal` is `Uint64` with no exact value stated (TS2 fixes 0).
- Rust Analyze carries a host-derived `analysisDomain` (`subjects` + 8-member request keys + `domainCommitment`) instead of TS `requestedCoverageDomain`.

## 5. FactBatch: historical V2 vs negotiated V3

| aspect | historical `FactBatchV2` (`target-attribution-v2` not in both arrays) | negotiated `FactBatchV3` (token in Hello **and** HelloAck) |
|---|---|---|
| owner | rust2 `payloadSchemas.FactBatchV2` (retained, :123); JSON vector `provider-handshake.1#/$defs/RustFactBatchV2Vector` | `opensip.product.fact-batch.3` |
| members | `analysisOrdinal, stageId, batchIndex, candidates` | `schemaVersion(3), analysisOrdinal, stageId, batchIndex, candidates, occupancyCompanions` |
| per-batch commitment | none | none |
| cap | `maxFactBatchCandidates` 4096 | same; companions <= len(candidates) |
| wrong payload for negotiation | `PROVIDER.PROTOCOL_VIOLATION` | `PROVIDER.PROTOCOL_VIOLATION` |
| stage/stream commitments | `stageFacts` / `factStream` over the ordered `FactCandidateV1` stream, whichever payload carried it (handshake law `commitments.rust-semantic`) | same |

`FactCandidateV1` is unchanged under both payloads and has no occupancy member. On the wire, `canonicalRelationPayload` is a CBOR byte string. The fact-batch.3 `canonicalRelationPayloadHex`/`decodedRelationPayload` pair is a JSON-vector transcription and observation.

## 6. Coverage and batch streams

- **Per-stage output order.** Each stage emits zero or more FactBatch frames, then exactly one CoverageV3 (P3-23, P3-24). P3-24 increments `stageIndex`/`stagesCompleted` and resolves to READY_COMPLETE only after the last stage.
- **Candidate stream.** `batchIndex` is contiguous from 0 per stage. `candidateOrdinal` is contiguous from 0 across the batches of a stage and resets at the next stage (v2 T016/T017; `DispatchBindingV1.expectedFirstCandidateOrdinal`). Array order in V3 is `candidateOrdinal` strictly increasing (occupancy vocabulary). Contiguity is a separate stream law.
- **Spool and aggregates.** Each candidate is spooled as deterministic-CBOR of `{analysisOrdinal, stageId, candidate}`. Its exact bytes are checked-added against `maxCandidateSpoolBytes` 1073741824, and one entry against `maxFactCandidatesTotal` 1000000, before allocation (rust2 `limitPolicy.candidateSpoolAccounting`). Request and response payload totals and frame counts are `max{Request,Response}{PayloadBytesTotal,Frames}`.
- **Admission atomicity.** The complete candidate set and Coverage are admitted only after valid Complete, custody, order, bijection, recomputed commitments, zero exit and EOF. Every other outcome discards all candidates. Unavailable and BudgetExhausted may admit terminal exhaustive-unknown Coverage only (rust2 `candidateAtomicity`).
- **Coverage entries.** `CoverageV3.entries[i]` answers `analysisDomain.requestedCoverageDomain[i]`, and the count equals the key count. `key.relation/resolution/subjectScopeCommitment` equal the request key. `key.sourceUniverse/targetUniverse` are the 64-hex suffixes of the request key's universe ids. The request key's `producer`, `producerVersion` and `schemaVersion` stay request coordinates (startup law `coverageFrames.entries`).
- **Terminal coverage.** UnavailableV3 and BudgetExhaustedV3 `coverage` lists CoverageResultV3 in stage-major/key order. Entry k belongs to the stage whose cumulative key range contains k. The pre-Analyze Unavailable carries no coverage; the host mints it after DONE (`pre_analyze_unavailable_conversion`).
- **Commitments (rust2 `commitments`):**
  - Retained: `stageFacts` (`opensip.rust-provider.stage-facts.v2`) and `factStream` (`...fact-stream.v2`).
  - Recipes unchanged over CoverageResultV3 values: `stageCoverage` (`...stage-coverage.v2`) and `coverageStream` (`...coverage-stream.v2`).
  - `subjectScope`, `analysisDomain`, `snapshotManifest` and `preparedOutputBlob/Manifest` are stated.
  - The field-to-domain map for the wrapper and terminal `coverageCommitment` members is not stated (R3-G12).
  - The subject-scope recipe is contested (R3-G4).
- **Budget.** Units work-units/items/bytes use checked increments. Milliseconds is a host deadline and never BudgetExhausted. Overflow is a protocol fault (rust2 `deterministicBudget`).
"""

TAIL = """
## 18. Same-name trace (never merge by bare name)

- **CoverageKeyV2 twice on the Rust3 wire.**
  - The rust2 `definitions.CoverageKeyV2` is the 8-member request key in `StageAnalysisDomainV2.requestedCoverageDomain` (external c2 v3 `coverageKey.key`). Its `sourceUniverseId`/`targetUniverseId` are Sha256Text native identities.
  - native-evidence `CoverageKeyV2` is the 5-member entry key inside `CoverageResultV3`: bare-hex universes and no producer, producerVersion or schemaVersion. Rows keyed `CoverageKeyV2@native-evidence.*` are that record.
  - TS `CoverageKeyV1` is a third record and is not on this wire.
- **FactCandidateV1** is one fact-plane shape. Per language, `producer` (`rust-semantic`), `language` (`rust`), `producerVersion` (HelloV3 identity) and universe-id supersession (:128 for Rust, :125 for TS) differ.
- **StageResultV2** (5 members) is not TS `StageResultV1` (7). **UnavailableReasonV3** (native-evidence, 7 values) is not the startup `UnavailableV3.reason` enum (9).

## 19. Unaccepted proposals and their Rust3 standing

| proposal (m1-protocol-gap-resolution-01) | Rust3 applicability | standing here |
|---|---|---|
| TS2-G1 ByteString / Uint8Array carrier | same question for Rust bstr members | not assumed; R3-G1 implementation choice |
| TS2-G3 StageIdText via dispatch | `dispatch-binding.schema.v1.json` `expectedStageId` itself names `StageRequestV2.planStage.stageId` | this translation cites the schema text directly, not the proposal |
| P-1 per-key scope2 (typescript-semantic only) | does not address rust2 `commitments.subjectScope` | R3-G4 open |
| P-2 fact-ref refusal (names rust-semantic major 3) | would close the fact-ref half of R3-G5 | PROPOSAL; R3-G5 open |
| P-3 manifestSha256 raw DigestHex (TS) | Rust already governed: rust2 `commitments.snapshotManifest` | no proposal needed for Rust |
| P-4 coverage field->domain map (typescript-semantic only) | Rust equivalent absent | R3-G12 open |
| P-5 report projection | not provider wire | out of scope |
| G9 control owner found / P-6 | control is a separate plane (§15) | R3-G18 proposal-pending |
| citations to `check-rust-provider-protocol.py` as "checkRust2" | that file is the v1 checker | R3-G19 citation defect |

## 20. Final account: genuine unresolved issues

Only an owner can close the following. None is closed here, and no carrier should be generated for a contradictory item until it is closed.
1. **R3-G9 PreparedOutput frames (owner-contradictory).** The four frames exist in the major-3 machine (P3-16..19), but their inherited payloads join rust-v1 rows that §0:130 supersedes. No field-level successor exists.
2. **R3-G4 subjectScopeCommitment (owner-contradictory).** rust2 uses one per-stage `subject-scope.v2` value for all keys; §4.1a and startup coverage correspondence require the per-key scope2. `domainCommitment` and `subjectCount` depend on it.
3. **R3-G17 ordering (owner-contradictory).** protocol3-transitions diverges from the non-superseded v2 transition rules: Cancel in START, the Unavailable-before-output guard, and v2 prepared-custody order text.
4. **R3-G11 DependencySourceManifestV3.manifestSha256 (owner-contradictory).** The digest preimage is self-referential and no recipe is given; the entry order and packageKey grammar are unstated.
5. **R3-G10 / R3-G3 (owner-missing).** DependencySourceChunk has no field types; DependencySourceAccepted, DependencySourceChunk and the envelope have no record names.
6. **R3-G12 / R3-G13 (owner-missing).** The coverage commitment field-to-domain map is unstated. StageResultV2 is "superseded" with no successor record.
7. **R3-G14 / R3-G15 / R3-G16 (owner-missing).** ProviderFault/Cancel/Cancelled member types, nullability and phase vocabulary are unstated. SnapshotEntryV2 variant types are unstated. Echo substitutions are not enumerated for chunk/seal/anchor and subject-id preimages.
8. **R3-G5 AnchorRefV1 (owner-missing types; fact-ref contradicts fact2).** P-2 remains an unaccepted proposal.
9. **R3-G18 / R3-G19 (proposal-pending).** The control owner route needs root confirmation, and the gap-resolution proposal's Rust checker citations are wrong.

Governed but not expressible in JSON Schema (handwritten admission, not gaps in ownership): R3-G2, R3-G6, R3-G7, R3-G8. Carrier representation: R3-G1.
"""


if __name__ == "__main__":
    sys.exit(main())
