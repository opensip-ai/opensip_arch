#!/usr/bin/env python3
"""Emit wire-carriers.v1.json, successor.json and field-coverage.json for the native wire-carrier author candidate.

    OPENSIP_ARCH=/Users/sb/code/opensip-ai/opensip_arch PYTHONDONTWRITEBYTECODE=1 python3 -B tools/build.py

Reads only the pinned architecture snapshot files and the subject-local frozen inputs/ (no /tmp method inputs).
Refuses on pin drift, and fails if any inventory row is unmapped, maps to a missing carrier member, or cites a gap
without a resolution. Emits wire-carriers.v1.json, field-coverage.json, successor.json, p3-guard-successor.v1.json.
"""
import hashlib, json, os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
sys.path.insert(0, str(HERE))
import common as CM, records_ts2 as TS, records_rust3 as RS, rules as RU, succ as SU  # noqa: E402
import patterns as PT, public_routes as PR, owner_successor as OS  # noqa: E402

ARCH = CM.arch_root()
FAIL = []


def read_pinned(key):
    if key in CM.ARCH_PINS:
        path, want, size = CM.ARCH_PINS[key]
        raw = (ARCH / path).read_bytes()
    else:
        path, want, _ = CM.SUBJECT_INPUTS[key]
        raw = (OUT / path).read_bytes()
        size = len(raw)
    got = hashlib.sha256(raw).hexdigest()
    if got != want or len(raw) != size:
        sys.exit(f"PIN DRIFT {key} {path}: {got}")
    return raw


PIN_ROWS = []
for k, (p, h, n) in CM.ARCH_PINS.items():
    read_pinned(k)
    PIN_ROWS.append({"key": k, "path": p, "sha256": h, "bytes": n})
INPUT_ROWS = []
for k, (p, h, origin) in CM.SUBJECT_INPUTS.items():
    INPUT_ROWS.append({"key": k, "path": p, "sha256": h, "bytes": len(read_pinned(k)), "copiedFrom": origin})
OPTIONS = json.loads(read_pinned("generatorOptions"))

DOCS = {d["$id"]: d for d in (json.loads(read_pinned(key)) for key in ("handshake", "startup", "evidence", "occupancy", "factBatch3", "dispatch"))}
TSF = json.loads(read_pinned("tsFields"))
RSF = json.loads(read_pinned("rustFields"))


def resolve_extern(ref):
    sid, ptr = ref.split("#", 1)
    node = DOCS[sid]
    for part in [p for p in ptr.split("/") if p]:
        node = node[part]
    return node


def all_types(expr, acc):
    if isinstance(expr, dict):
        if expr.get("t") in ("ref", "extern"):
            acc.append(expr)
        for v in expr.values():
            all_types(v, acc)
    elif isinstance(expr, list):
        for v in expr:
            all_types(v, acc)
    return acc


LOCAL = {}
for mod in (TS, RS):
    for n, v in mod.SCALARS.items():
        LOCAL[n] = dict(v, kind="scalar")
    LOCAL.update(mod.RECORDS)

for e in all_types([TS.RECORDS, RS.RECORDS, TS.FRAMES, RS.FRAMES], []):
    if e["t"] == "ref" and e["ref"] not in LOCAL:
        FAIL.append("unresolved local ref " + e["ref"])
    if e["t"] == "extern":
        try:
            resolve_extern(e["schemaRef"])
        except KeyError:
            FAIL.append("unresolved extern " + e["schemaRef"])
for n, v in LOCAL.items():
    if v.get("sameShapeAs"):
        try:
            resolve_extern(v["sameShapeAs"])
        except KeyError:
            FAIL.append("unresolved sameShapeAs " + n)


def members_of(type_name):
    """Member names of a carrier type (local or extern generated name); None for scalars."""
    if type_name in LOCAL:
        v = LOCAL[type_name]
        if v["kind"] == "record":
            return [m["name"] for m in v["members"]]
        if v["kind"] == "variant-record":
            return list(v["memberOrder"])
        if v["kind"] == "alias":
            return members_of(v["target"]["generatedType"])
        return None
    for sid, ns in CM.EXTERN_NS.items():
        if type_name.startswith(ns) and sid in DOCS:
            d = DOCS[sid].get("$defs", {}).get(type_name[len(ns):])
            if d is not None:
                return list(d.get("properties", {}).keys()) or None
    raise KeyError(type_name)


# ---------------- inventory -> carrier maps ----------------
TS_MAP = {
    "frameEnvelope": "Ts2FrameV2", "definitions.DigestHex": "Ts2DigestHex", "definitions.Sha256Text": "Ts2Sha256Text",
    "definitions.ExecutionId": "Ts2ExecutionIdText", "definitions.SnapshotId": "Ts2SnapshotId2", "definitions.PlanId": "Ts2PlanId2",
    "definitions.PlanIntentCommitment": "Ts2Sha256Text", "definitions.TypeScriptSemanticUniverseV1": "Startup1TypeScriptSemanticUniverseV2",
    "definitions.TypeScriptSemanticUniverseKey": "Ts2Sha256Text", "definitions.CoverageResultV1": "Native2CoverageResultV3",
    "payloadSchemas.HelloV1": "Handshake1TypeScriptHelloV2", "payloadSchemas.HelloAckV1": "Handshake1TypeScriptHelloAckV2",
    "payloadSchemas.OpenUniverseV1": "Startup1TypeScriptOpenUniverseV2", "payloadSchemas.UniverseAcceptedV1": "Startup1TypeScriptUniverseAcceptedV2",
    "payloadSchemas.CoverageV1": "Startup1TypeScriptCoverageV2", "payloadSchemas.UnavailableV1": "Startup1TypeScriptUnavailableV2",
    "payloadSchemas.BudgetExhaustedV1": "Startup1TypeScriptBudgetExhaustedV2",
    "TypeScriptHelloV2": "Handshake1TypeScriptHelloV2", "TypeScriptHelloAckV2": "Handshake1TypeScriptHelloAckV2",
    "NativeContextVerifiedV1": "Startup1NativeContextVerifiedV1", "PreAnalyzeUnavailableV1": "Startup1PreAnalyzeUnavailableV1",
    "FactBatchV3": "Ts2FactBatchV3",
}
for n in ["SnapshotEntryV1", "ProviderWorkBudgetV1", "StageRequestV1", "SnapshotFileSubjectV1", "SubjectScopeV1",
          "RequestedCoverageDomainV1", "AnchorRefV1", "FactCandidateV1", "CoverageKeyV1", "StageResultV1"]:
    TS_MAP["definitions." + n] = "Ts2" + n
for n in ["SnapshotManifestV1", "SnapshotFileChunkV1", "SnapshotSealV1", "SnapshotAcceptedV1", "AnalyzeV1", "FactBatchV1",
          "CompleteV1", "CancelV1", "CancelledV1"]:
    TS_MAP["payloadSchemas." + n] = "Ts2" + n
MOVED = {  # (carrier, inherited member) -> carried at
    ("Native2CoverageResultV3", "stageId"): "Startup1TypeScriptCoverageV2.stageId | Startup1CoverageV3.stageId (wrapper attributes every entry)",
    ("Native2CoverageResultV3", "entryOrdinal"): "POSITIONAL: array index i of Startup1TypeScriptCoverageV2.entries / Startup1CoverageV3.entries (entries[i] answers keys[i]); no member",
    ("Native2CoverageResultV3", "coverageState"): "Native2CoverageResultV3.entry.coverage",
    ("Native2CoverageResultV3", "deficiency"): "Native2CoverageResultV3.entry.deficiency",
    ("Native2RepositoryResolutionV3", "network"): "Native2RepositoryResolutionV3.effects.network (EffectV1, disclosed effects)",
    ("Startup1RustSemanticUniverseV2", "resolvedInputs"): "Startup1RustSemanticUniverseV2.resolvedInputs",
}

RS_MAP = {
    "envelope": "Rust3ProviderFrameV3", "payloadSchemas.HelloV2": "Handshake1HelloV3", "payloadSchemas.HelloAckV2": "Handshake1HelloAckV3",
    "payloadSchemas.OpenUniverseV2": "Startup1OpenUniverseV3", "payloadSchemas.UniverseAcceptedV2": "Startup1UniverseAcceptedV3",
    "payloadSchemas.CoverageV2": "Startup1CoverageV3", "payloadSchemas.UnavailableV2": "Startup1UnavailableV3",
    "payloadSchemas.BudgetExhaustedV2": "Startup1BudgetExhaustedV3",
    "definitions.IdentityText": "Rust3IdentityText", "definitions.DigestHex": "Rust3DigestHex", "definitions.Sha256Text": "Rust3Sha256Text",
    "definitions.CanonicalPath": "Rust3CanonicalPath", "definitions.SnapshotId": "Rust3SnapshotId2", "definitions.PlanId": "Rust3PlanId2",
    "definitions.RustUniverseV1": "Startup1RustSemanticUniverseV2", "definitions.C2PlanStageV3": "Rust3C2PlanStageV3",
    "definitions.FactCandidateV1": "Rust3FactCandidateV1", "definitions.ProtocolLimitsV2": "Handshake1ProtocolLimitsV3",
    "definitions.ExpectedRustIdentityV2": "Handshake1ExpectedRustIdentityV3", "definitions.RustProviderCapabilityV2": "Handshake1RustCapabilitiesV3",
    "definitions.ToolPathV2": None, "definitions.RepositoryResolutionV2": "Native2RepositoryResolutionV3",
    "definitions.PreparedOutputBlobV2": None, "definitions.PreparedOutputEntryV2": "Rust3PreparedOutputEntryV3",
    "definitions.CoverageResultV2": "Native2CoverageResultV3",
    "external.C2PlanStageV3": "Rust3C2PlanStageV3", "external.FactCandidateV1": "Rust3FactCandidateV1", "external.AnchorRefV1": "Rust3AnchorRefV1",
    "external.RustUniverseV1": "Startup1RustSemanticUniverseV2", "external.RustUniverseV1.resolvedInputs": "Native2RustUniverseV2ResolvedInputs",
    "new.HelloV3": "Handshake1HelloV3", "new.HelloAckV3": "Handshake1HelloAckV3", "new.ProtocolLimitsV3": "Handshake1ProtocolLimitsV3",
    "new.RustUniverseV2ResolvedInputs": "Native2RustUniverseV2ResolvedInputs", "new.RepositoryResolutionV3": "Native2RepositoryResolutionV3",
    "new.DependencySourceManifestV3": "Native2DependencySourceManifestV3", "new.DependencySourceSealV3": "Native2DependencySourceSealV3",
    "new.DependencySourceChunk(unnamed)": "Rust3DependencySourceChunkV3", "new.DependencySourceAccepted(unnamed)": "Rust3DependencySourceAcceptedV3",
    "new.NativeContextVerifiedV1": "Startup1NativeContextVerifiedV1", "new.PreAnalyzeUnavailableV1": "Startup1PreAnalyzeUnavailableV1",
    "new.FactBatchV3": "Rust3FactBatchV3", "new.CoverageResultV3": "Native2CoverageResultV3", "new.CoverageKeyV2@native-evidence": "Native2CoverageKeyV2",
}
for n in ["SnapshotManifestV2", "SnapshotFileChunkV2", "SnapshotSealV2", "SnapshotAcceptedV2", "AnalyzeV2", "FactBatchV2",
          "CompleteV2", "ProviderFaultV2", "CancelV2", "CancelledV2"]:
    RS_MAP["payloadSchemas." + n] = "Rust3" + n
for x in ["Manifest", "Chunk", "Seal", "Accepted"]:
    RS_MAP[f"payloadSchemas.PreparedOutput{x}V2"] = f"Rust3PreparedOutput{x}V3"
for n in ["SnapshotEntryV2", "SubjectV2", "CoverageKeyV2", "StageAnalysisDomainV2", "StageRequestV2", "StageResultV2"]:
    RS_MAP["definitions." + n] = "Rust3" + n

GAP_RESOLUTION = {
    "TS2-G1": "privateRepresentation.bytes", "TS2-G2": "profiles.notProvedByJsonSchema", "TS2-G3": "falseGaps[TS2-G3]",
    "TS2-G4": "SUCC-PER-KEY-SCOPE2", "TS2-G5": "SUCC-ANCHOR-RULES + SUCC-FACT-REF-REFUSED", "TS2-G6": "privateRepresentation.selectors",
    "TS2-G7": "privateRepresentation.namespaces", "TS2-G8": "admission FRAME-LIMIT + derived request/stage bounds (handwritten)",
    "TS2-G9": "falseGaps[TS2-G9]", "TS2-G10": "SUCC-TS2-MANIFEST-DIGEST", "TS2-G11": "explicit carrier bounds (Ts2ExecutionIdText, Ts2ProjectPath, FRAME-LIMIT)",
    "TS2-G12": "SUCC-COMMIT-MAP",
    "R3-G1": "privateRepresentation.bytes", "R3-G2": "profiles.notProvedByJsonSchema + Rust3CanonicalPath", "R3-G3": "SUCC-DEPSRC-RECORDS + falseGaps[R3-G3]",
    "R3-G4": "SUCC-PER-KEY-SCOPE2", "R3-G5": "SUCC-ANCHOR-RULES + SUCC-FACT-REF-REFUSED", "R3-G6": "privateRepresentation.selectors",
    "R3-G7": "privateRepresentation.namespaces", "R3-G8": "admission FRAME-LIMIT + derived bounds (handwritten)", "R3-G9": "SUCC-PREPARED-V3",
    "R3-G10": "SUCC-DEPSRC-RECORDS", "R3-G11": "SUCC-DEPSRC-DIGEST", "R3-G12": "SUCC-COMMIT-MAP", "R3-G13": "falseGaps[R3-G13]",
    "R3-G14": "SUCC-RUST3-FAULT-CANCEL + SUCC-RUST3-OBSERVED", "R3-G15": "SUCC-RUST3-SNAPSHOT-ENTRY + falseGaps[R3-G15]",
    "R3-G16": "SUCC-ECHO-ENUMERATION", "R3-G17": "SUCC-TRANSITION-PRECEDENCE", "R3-G18": "falseGaps[R3-G18]", "R3-G19": "SUCC-TS2-MANIFEST-DIGEST (citation correction)",
}
if set(GAP_RESOLUTION) != set(TSF["gaps"]) | set(RSF["gaps"]):
    FAIL.append("gap register mismatch: " + str(sorted(set(TSF["gaps"]) ^ set(RSF["gaps"]) ^ set(GAP_RESOLUTION))))

FRAME_TS = {f[0] for f in TS.FRAMES}
FRAME_RS = {f[0] for f in RS.FRAMES}


def split(identifier, maps):
    for prefix in sorted(maps, key=len, reverse=True):
        if identifier == prefix:
            return prefix, None
        if identifier.startswith(prefix + "."):
            rest = identifier[len(prefix) + 1:]
            for marker in ("fields.", "required."):
                if rest.startswith(marker):
                    rest = rest[len(marker):]
            return prefix, rest
    return None, None


def map_row(identifier, row, maps, frames, protocol):
    out = {"inventory": identifier, "inheritedDisposition": row.get("disposition"),
           "memberChange": row.get("successorMemberChange"), "gaps": row.get("gaps", []),
           "gapResolutions": {g: GAP_RESOLUTION.get(g) for g in row.get("gaps", [])}}
    for g in row.get("gaps", []):
        if g not in GAP_RESOLUTION:
            FAIL.append(f"{identifier}: unresolved gap {g}")
    if identifier.startswith(("frameSchemas.", "newFrames.")):
        name = identifier.split(".", 1)[1]
        if protocol == "rust-semantic" and name == "Coverage":
            out.update(status="frame-renamed", carrier="frame CoverageV3")
        elif name in frames:
            out.update(status="frame", carrier="frame " + name)
        else:
            FAIL.append("unmapped frame " + identifier)
        return out
    prefix, member = split(identifier, maps)
    if prefix is None:
        FAIL.append("unmapped row " + identifier)
        return out
    carrier = maps[prefix]
    if carrier is None:
        out.update(status="not-carried", carrier=None, reason="no major-%s wire carrier: superseded record (see SUCC-PREPARED-V3 / RepositoryResolutionV3)" % protocol)
        return out
    if member is None:
        out.update(status="carried", carrier=carrier)
        return out
    if (carrier, member) in MOVED:
        where = MOVED[(carrier, member)]
        out.update(status="carried-positional" if where.startswith("POSITIONAL") else "carried-moved", carrier=where)
        return out
    if row.get("successorMemberChange") == "removed" or row.get("disposition") == "removed":
        out.update(status="not-carried", carrier=carrier, reason="member removed by the successor record")
        return out
    names = members_of(carrier)
    base = member.split(".")[0].replace("[]", "")
    if member.startswith("entries[]."):
        names = list(resolve_extern(CM.NE + "#/$defs/DependencySourceManifestV3/properties/entries/items")["properties"])
        base = member.split(".", 1)[1]
    if names is None:
        FAIL.append(f"{identifier}: carrier {carrier} has no members")
    elif base in names:
        out.update(status="carried", carrier=f"{carrier}.{base}")
    elif row.get("successorMemberChange") == "removed" or row.get("disposition") == "removed":
        out.update(status="not-carried", carrier=carrier, reason="member removed by the successor record")
    else:
        FAIL.append(f"{identifier}: member {base} not on {carrier}")
    return out


coverage = {"typescript-semantic": [], "rust-semantic": []}
for r in TSF["rows"]:
    coverage["typescript-semantic"].append(dict(map_row(r["member"], r, TS_MAP, FRAME_TS, "typescript-semantic"), group="inherited"))
for r in TSF["newRows"]:
    coverage["typescript-semantic"].append(dict(map_row(r["member"], r, TS_MAP, FRAME_TS, "typescript-semantic"), group="new"))
for group in ("envelope", "rows", "externalRows", "newRows", "frames"):
    for k, r in RSF[group].items():
        coverage["rust-semantic"].append(dict(map_row(k, r, RS_MAP, FRAME_RS, "rust-semantic"),
                                              group={"envelope": "inherited", "rows": "inherited", "externalRows": "external", "newRows": "new", "frames": "frame"}[group]))


def count(rows):
    c = {}
    for r in rows:
        c[(r["group"], r.get("status"))] = c.get((r["group"], r.get("status")), 0) + 1
    return {f"{g}:{s}": n for (g, s), n in sorted(c.items(), key=str)}


for sid, ns in CM.EXTERN_NS.items():
    owners = {o["schemaId"]: o["namespace"] for o in OPTIONS["owners"]}
    if owners.get(sid) != ns:
        FAIL.append(f"extern namespace {sid} -> {ns} differs from generator options {owners.get(sid)}")


def frames_doc(frames):
    return [{"frameType": n, "direction": d, "workerTerminal": w, "payload": p} for n, d, w, p in frames]


wire = {
    "artifact": "opensip.m1.native-wire-carriers", "version": "1",
    "standing": "AUTHOR candidate 06 for independent review. A finite declarative carrier input for one registry recipe generating crates/contracts/src/generated/protocol.rs and providers/typescript/src/generated/protocol.ts. Not approval, not a production wire decoder, not semantic admission.",
    "sourcePins": PIN_ROWS,
    "subjectInputs": INPUT_ROWS,
    "typeGrammar": "wire-carriers.meta.schema.json",
    "profiles": RU.PROFILES,
    "privateRepresentation": RU.PRIVATE_REPRESENTATION,
    "scalars": {**TS.SCALARS, **RS.SCALARS},
    "records": {**TS.RECORDS, **RS.RECORDS},
    "preimageOnlyRecords": sorted(TS.PREIMAGE_ONLY | RS.PREIMAGE_ONLY),
    "protocols": {
        "typescript-semantic": {"major": "2", "profile": "ts2-cbor", "envelope": "Ts2FrameV2", "frames": frames_doc(TS.FRAMES),
                                "limits": CM.HS + "#/$defs/TypeScriptProtocolLimitsV1", "transitions": RU.TRANSITIONS["typescript-semantic"]},
        "rust-semantic": {"major": "3", "profile": "rust3-cbor", "envelope": "Rust3ProviderFrameV3", "frames": frames_doc(RS.FRAMES),
                          "limits": CM.HS + "#/$defs/ProtocolLimitsV3", "transitions": RU.TRANSITIONS["rust-semantic"]},
    },
    "admission": RU.ADMISSION,
    "commitmentMap": RU.COMMITMENT_MAP,
}
rule_ids = {r["id"] for r in RU.ADMISSION}

# RF-3: closed pattern site list and lowering subset over the carrier graph and every reachable extern pattern.
OSUCC = OS.successor_document(read_pinned, PIN_ROWS)
EFFECTIVE = OS.effective_docs(DOCS, OSUCC["schemaPatternRows"])
_closure = PT.closure(wire, EFFECTIVE)
RU.PATTERN_DIALECT["patternSites"] = _closure["sites"]
RU.PATTERN_DIALECT["loweringRequired"] = [x for x in _closure["sites"] if x["lower"]]
for x in _closure["sites"]:
    try:
        __import__("wirecodec").ecma_to_python(x["pattern"], RU.PATTERN_DIALECT["flags"])
    except Exception as exc:  # noqa: BLE001
        FAIL.append("pattern outside the finite ECMA translation: " + x["pattern"] + " " + str(exc))


def _all_patterns(o, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "pattern" and isinstance(v, str):
                acc.add(v)
            _all_patterns(v, acc)
    elif isinstance(o, list):
        for v in o:
            _all_patterns(v, acc)
    return acc


_owner_patterns = _all_patterns([json.loads(read_pinned(k)) for k in OS.EVALUATED_DOC_KEYS + ["startup", "handshake", "factBatch3"]], set()) | {r["to"] for r in OSUCC["schemaPatternRows"]}
for _p in sorted(_owner_patterns):
    try:
        __import__("wirecodec").ecma_to_python(_p, RU.PATTERN_DIALECT["flags"])
    except Exception as exc:  # noqa: BLE001
        FAIL.append("owner pattern outside the finite ECMA translation: " + _p + " " + str(exc))


# A-3: path member lists computed from the carrier graph; rule text rendered from them.
def _uses(t, names):
    stack = [t]
    while stack:
        x = stack.pop()
        if x.get("t") == "ref" and x["ref"] in names:
            return True
        stack.extend(x[k] for k in ("of", "items") if k in x)
    return False


def path_members(names):
    out = []
    for rn, r in wire["records"].items():
        if r["kind"] == "record":
            pairs = [(m["name"], m["type"]) for m in r["members"]]
        elif r["kind"] == "variant-record":
            pairs = [(f"variants.{v}.{k}", t) for v, mm in r["variants"].items() for k, t in mm.items()]
        else:
            pairs = []
        out.extend(f"{rn}.{n}" for n, t in pairs if _uses(t, names))
    return sorted(out)


def extern_path_members(protocol):
    out = []
    for f in wire["protocols"][protocol]["frames"]:
        p = f["payload"]
        if p.get("t") != "extern" or not any(w in f["frameType"] for w in ("Manifest", "Chunk")):
            continue

        def walk(node, ptr):
            for k, v in node.get("properties", {}).items():
                if k == "path":
                    out.append({"generatedType": p["generatedType"], "pointer": ptr + "/path"})
                walk(v, ptr + "/" + k)
            if isinstance(node.get("items"), dict):
                walk(node["items"], ptr + "/*")
        walk(resolve_extern(p["schemaRef"]), "")
    return sorted(out, key=lambda m: (m["generatedType"], m["pointer"]))


for r in RU.ADMISSION:
    if r["id"] == "CANONICAL-PATH-ADMISSION":
        r["params"]["members"] = path_members({"Rust3CanonicalPath", "Rust3DependencySourcePath"})
        r["params"]["externMembers"] = extern_path_members("rust-semantic")
    elif r["id"] == "TS2-LOGICAL-PATH-ADMISSION":
        r["params"]["members"] = path_members({"Ts2ProjectPath"})
        r["params"]["externMembers"] = extern_path_members("typescript-semantic")
    else:
        continue
    r["rule"] = RU.render_path_members(r["params"]["lexical"], r["params"]["members"], r["params"]["externMembers"])
    if not r["params"]["members"]:
        FAIL.append("no path members for " + r["id"])
# review-03 RF-1: closed path-site set with author bindings; rule text rendered from it.
_sites = PT.path_sites(wire, EFFECTIVE, RU.PATTERN_DIALECT["flags"])
wire["pathSites"] = [dict(s_, bindings=RU.path_site_bindings(s_)) for s_ in _sites]
for s_ in wire["pathSites"]:
    if not s_["bindings"]:
        FAIL.append("unbound path site " + json.dumps(s_["location"]))
for r in RU.ADMISSION:
    if r["id"] == "PATH-SITE-SEGMENT-LAW":
        r["params"]["sites"] = str(len(wire["pathSites"]))
        r["rule"] = RU.render_path_sites(wire["pathSites"])
# review-04 RF-3: relation-payload CanonicalPath sites (fact payloads, opaque to the carriers) recomputed from the pinned document.
for r in RU.ADMISSION:
    if r["id"] == "RELATION-PAYLOAD-PATH-LAW":
        r["params"]["sites"] = OSUCC["relationPayloadPathSites"]
        if not r["params"]["sites"]:
            FAIL.append("no relation payload path sites")
# RF-1: every refusal is a reference to a published successor route key.
for r in RU.ADMISSION:
    rk = r.get("params", {}).get("route", {}).get("routeKey")
    if rk is not None and rk not in PR.ROUTE_KEYS:
        FAIL.append(f"{r['id']}: route key {rk} not in the public route successor")
for n, v in wire["records"].items():
    for a in v.get("admission", []):
        if a not in rule_ids:
            FAIL.append(f"{n}: unknown admission rule {a}")

succ_ids = {r["id"] for r in SU.ROWS}
for v in GAP_RESOLUTION.values():
    for token in v.replace("+", " ").split():
        if token.startswith("SUCC-") and token not in succ_ids:
            FAIL.append("gap resolution cites unknown " + token)

RECORD_LEVEL_GAPS = {
    "TS2-G2": GAP_RESOLUTION["TS2-G2"], "TS2-G9": GAP_RESOLUTION["TS2-G9"],
    "R3-G18": GAP_RESOLUTION["R3-G18"], "R3-G19": GAP_RESOLUTION["R3-G19"],
}
attached = {g for rows in coverage.values() for r in rows for g in r["gaps"]}
unattached = sorted(set(GAP_RESOLUTION) - attached)
if sorted(RECORD_LEVEL_GAPS) != unattached:
    FAIL.append("record-level gap set mismatch: " + str(unattached))
AUTHOR_ADDED_ROWS = [
    {"inventory": "author02.Rust3C2StageBudgetV1.unit", "group": "author-added", "status": "carried", "carrier": "Rust3C2StageBudgetV1.unit",
     "source": {"pin": "c2v3", "selector": "$.planIntent.wireTypes.stageBudgetV1.unit"}, "gaps": [], "gapResolutions": {}},
    {"inventory": "author02.Rust3C2StageBudgetV1.limit", "group": "author-added", "status": "carried", "carrier": "Rust3C2StageBudgetV1.limit",
     "source": {"pin": "c2v3", "selector": "$.planIntent.wireTypes.stageBudgetV1.limit"}, "gaps": [], "gapResolutions": {}},
]
for r in AUTHOR_ADDED_ROWS:
    if r["carrier"].split(".")[1] not in members_of(r["carrier"].split(".")[0]):
        FAIL.append("author-added row carrier missing " + r["carrier"])
coverage["rust-semantic"].extend(AUTHOR_ADDED_ROWS)

coverage_doc = {
    "standing": "AUTHOR candidate 06 field coverage: every TS2 (182 inherited + 18 new) and Rust3 (231 inherited + 59 external + 76 new + 27 frame) row of the frozen inputs/ inventories mapped to a carrier member, a moved or positional location, a frame, or an explicit not-carried reason; plus 2 author-added rows (C-2 stageBudgetV1 members nested in Rust3C2PlanStageV3). Every gap is attached either to rows or to recordLevelGaps.",
    "inputs": INPUT_ROWS[:2],
    "recordLevelGaps": RECORD_LEVEL_GAPS,
    "counts": {p: count(rows) for p, rows in coverage.items()},
    "totals": {p: len(rows) for p, rows in coverage.items()},
    "rows": coverage,
}

parents = PIN_ROWS
successor = {
    "schemaVersion": 1,
    "standing": "AUTHOR candidate 06 proposed scoped successor for root and fresh independent review; not approval; effective as selected semantics only after root acceptance and source-bridge promotion. Parent bytes are unchanged; rows name exact selectors and scopes. Architecture acceptance uses exact snapshot pins (no commit required).",
    "supersedesCandidate": {"path": "/tmp/opensip-implementation/m1-native-wire-owner-subject-05", "manifestSha256": "7b9d94c31df9aa41d83599400e6beb9b5451bb39b9c0e174858f2fde4c686f1d", "review": "/tmp/opensip-implementation/m1-native-wire-owner-review-05", "rootValidation": "/tmp/opensip-implementation/m1-native-wire-owner-root-validation-05", "preservedEvidence": "prior/"},
    "ownerPatternSuccessor": "owner-pattern-successor.v1.json",
    "publicRouteSuccessor": "public-route-successor.v1.json",
    "selectors": {"proposedPath": "docs/implementation/m1/native-wire-v1/", "wireInput": "wire-carriers.v1.json",
                  "unchanged": ["every parent byte", "every registered schema document and its raw digest", "protocolMajor values 2 and 3", "all wire member names, CBOR types and identity recipes except the scoped value statements below"]},
    "parents": parents,
    "subjectInputs": INPUT_ROWS,
    "provenanceOnly": CM.PROVENANCE_ONLY,
    "reviewResolutions": SU.REVIEW_RESOLUTIONS,
    "rows": SU.ROWS,
    "falseGaps": SU.FALSE_GAPS,
    "remainingContradictions": [],
    "futureQualification": ["M2 admission implementation of every handwritten rule (admission-vectors.json are reference vectors, not admission code)", "M3 provider/host codecs and analyzers", "generator support for bytes/variant-record/alias/frame-payload/optional kinds, lexical rules and pattern lowering (root renderer trial is separate)",
                           "source-bridge promotion of the in-memory owner pattern rows and their closed scope (owner-pattern-successor.v1.json) into the owner source documents",
                           "production Rust/TypeScript matchers with ECMA-262 semantics for [\\s\\S]* inside a lookahead (regex-crate lowering)",
                           "an M3 sender implementing HOST-SEND-SCHEDULE, including per-slot payloadSha256 binding, entry content binding over the bytes actually sent and the typed-bytes Cancel echo of the sent correlation",
                           "renderer rebase",
                           "the D9 exit-contract successor",
                           "relation-registry / fact-plane unit: promotion of the relation-payload CanonicalPath lookahead correction; the relation v2 CanonicalPath path-normalization gap (empty segments such as 'a//b.rs' and 'a/', and C0 controls, admitted although the inherited fact-plane.v1 sharedTypes.CanonicalPath forbids empty segments), the FilePayloadV1.path snapshot-inventory join and the PackagePayloadV1.manifestPath and VcsChangePayloadV1.previousPath join laws; a full retained-closure (admit_frame over a retained Run bundle) run; identity LogicalPath evaluation stays owned, unchanged, by the identity unit",
                           "M3 host and worker PREPARED-V3-READ-AUTHORITY: the host never selects a prepared set with a stale row; the worker reads exactly the entries whose carried planRow.status is ok and never a failed row"],
}

if FAIL:
    print("\n".join(FAIL[:80]))
    sys.exit(f"BUILD FAILED: {len(FAIL)}")


def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


dump("wire-carriers.v1.json", wire)
dump("field-coverage.json", coverage_doc)
dump("successor.json", successor)
p3_guard = {
    "artifact": "opensip.native-evidence.protocol3-transitions.guard-successor", "version": "1",
    "standing": "AUTHOR candidate 06 scoped successor to docs/coop/design-corrections/native/protocol3-transitions.v1.json for conformance harnesses; parent bytes unchanged; not approval.",
    "parent": next(r for r in PIN_ROWS if r["key"] == "p3"),
    **{k: wire["protocols"]["rust-semantic"]["transitions"][k] for k in ("stateAdditions", "stateUpdateAdditions", "guardAdditions", "equivalence", "cancel", "precedence", "terminalGuards", "custodyOrder")},
    "applicationOrder": "Apply stateAdditions to initialState; evaluate guardAdditions together with each row's own guard at match time; after a match apply parent stateUpdates then stateUpdateAdditions, before resolving next.",
}
dump("p3-guard-successor.v1.json", p3_guard)
dump("public-route-successor.v1.json", PR.successor_document(PIN_ROWS, read_pinned("nativeModel").decode("utf-8"), OS.source_closure))
dump("owner-pattern-successor.v1.json", OSUCC)
print(json.dumps({"totals": coverage_doc["totals"], "counts": coverage_doc["counts"], "records": len(wire["records"]),
                  "scalars": len(wire["scalars"]), "admissionRules": len(RU.ADMISSION), "successorRows": len(SU.ROWS),
                  "patternSites": len(RU.PATTERN_DIALECT["patternSites"]), "loweringRequired": len(RU.PATTERN_DIALECT["loweringRequired"]),
                  "externRootsReached": _closure["externRootsReached"], "pathSites": len(wire["pathSites"]),
                  "ownerPatternRows": len(OSUCC["schemaPatternRows"]), "ownerPatternsTranslated": len(_owner_patterns)}, indent=1))
