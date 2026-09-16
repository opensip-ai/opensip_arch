#!/usr/bin/env python3
"""Read-only tabulator for the TS2 wire translation inventory.

Reads pinned sources in the architecture repo (never writes there), asserts every
delivery.v2 wireSchema frameEnvelope/frameSchemas/definitions/payloadSchemas member has
exactly one translation row, resolves every schema-native ref, cross-checks wire types
against resolvable refs, compares original and successor member lists, and writes
fields.json, coverage.json and translation.md next to this tools/ directory.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
REPO = os.environ.get("OPENSIP_ARCH", "/Users/sb/code/opensip-ai/opensip_arch")
sys.path.insert(0, HERE)

from rows_common import (A, B, BOOL, GAPS, HANDWRITTEN_OWNERS, LINKS, M, MEMBER_CHANGES, N,  # noqa: E402
                         DISPOSITIONS, T, U, UNSTATED, WIRE_TYPES, WS)
from rows_defs import DEFS, ENVELOPE, FRAMES  # noqa: E402
from rows_payloads import NEW, PAYLOADS  # noqa: E402

SOURCES = {
    "delivery": ("docs/coop/artifacts/delivery.v2.json", "47b6cfd17338fafd407c554afe1951ab23d2896aac99bcfd272fc0894e3cabf3"),
    "native_md": ("docs/v2/contracts/product-v1/native-evidence.md", "83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0"),
    "audit": ("docs/implementation/m1/reviews/generation-owner-audit-01/audit.json", "86c84796a9ea294d6d571cc6f3b67caa4c3eec605f8db8adadd8166c02e42257"),
    "handshake": ("docs/coop/design-corrections/native/provider-handshake.schemas.v1.json", "9090e2ad51b767a176f51da09f201803d1cc82c047ade68102adcae1ee3a5f84"),
    "startup": ("docs/coop/design-corrections/native/provider-startup.schemas.v1.json", "1e35a77bae8d9c20171a934e9c16e4de4d7ce98bb024016d7e17cf9b0b38729c"),
    "factbatch3": ("docs/coop/design-corrections/native/fact-batch.schema.v3.json", "b0ebc133df8763f6cd5f3716542321eba21c69714fca368fbe31ba57677a24e0"),
    "companion": ("docs/coop/design-corrections/native/occupancy-companion.schema.v1.json", "d2bbbcc49adbb130d0bb010fee0b4cf25af7727f730fc329725fa62cd46ae14f"),
    "evidence": ("docs/coop/design-corrections/native/native-evidence.schemas.v2.json", "2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043"),
    "ts2order": ("docs/coop/design-corrections/native/typescript-protocol2-order.v1.json", "007ef7affce224c7bac6af3bb7897e86691085e2dd788f4a613e45c1fa5b8bbb"),
    "dispatch": ("docs/coop/design-corrections/native/dispatch-binding.schema.v1.json", "868c3cf241af9ecc205ba7d078354e38a7db5132974120c046ac23a2dd1df938"),
    "rust2": ("docs/coop/artifacts/rust-provider-protocol.v2.json", "6308a98c1183d75d671655b2a351334b62f4f2c00316983731ceabb86e90793b"),
    "factplane": ("docs/coop/artifacts/fact-plane.v1.json", "9057200822c5be59bcf8e691e3755cfa1acf2c89f0b1c2bc89237afaa0925b4d"),
    "c2v3": ("docs/coop/artifacts/c2-plan-stage-schema.v3.json", "3c488ff66a1ec9ab746e99e0701d59460aff3e1d66cd072d9d564a1382b9d285"),
}
ID_TO_SOURCE = {
    "opensip.product.provider-handshake.1": "handshake",
    "opensip.product.provider-startup.1": "startup",
    "opensip.product.fact-batch.3": "factbatch3",
    "opensip.product.occupancy-companion.1": "companion",
    "urn:opensip:product-v1:native:evidence-schemas:v2": "evidence",
}

FAIL = []


def check(cond, msg):
    if not cond:
        FAIL.append(msg)
    return cond


def load():
    docs, pins = {}, []
    for key, (rel, want) in SOURCES.items():
        raw = open(os.path.join(REPO, rel), "rb").read()
        got = hashlib.sha256(raw).hexdigest()
        check(got == want, f"sha mismatch {rel}: {got}")
        pins.append({"key": key, "path": rel, "sha256": got})
        docs[key] = raw.decode("utf-8") if rel.endswith(".md") else json.loads(raw)
    return docs, pins


def pointer(doc, ptr):
    node = doc
    for part in [p for p in ptr.split("/") if p]:
        part = part.replace("~1", "/").replace("~0", "~")
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node


def resolve(docs, ref, base=None):
    if ref.startswith("#"):
        return docs[base], pointer(docs[base], ref[1:]), base
    sid, _, frag = ref.partition("#")
    key = ID_TO_SOURCE[sid]
    return docs[key], pointer(docs[key], frag), key


def kinds(docs, node, base, depth=0):
    """Map a JSON Schema node to closedDataModel wire kinds (shape only)."""
    if depth > 20:
        return {"?"}
    if "$ref" in node:
        _, target, key = resolve(docs, node["$ref"], base)
        return kinds(docs, target, key, depth + 1)
    for comb in ("oneOf", "anyOf"):
        if comb in node:
            out = set()
            for alt in node[comb]:
                out |= kinds(docs, alt, base, depth + 1)
            return out
    if "const" in node:
        c = node["const"]
        return {BOOL} if isinstance(c, bool) else {U} if isinstance(c, int) else {T} if isinstance(c, str) else {N} if c is None else {"?"}
    t = node.get("type")
    if isinstance(t, list):
        return set().union(*[kinds(docs, {**node, "type": x}, base, depth + 1) for x in t])
    return {"integer": {U} if node.get("minimum", -1) >= 0 else {U, "negative-int64"}, "string": {T}, "array": {A},
            "object": {M}, "boolean": {BOOL}, "null": {N}}.get(t, {T} if "enum" in node else {"?"})


def enumerate_members(ws):
    """Every original member selector suffix, with record-level metadata."""
    members, records = [], {}
    env = ws["frameEnvelope"]
    records["frameEnvelope"] = {"required": env["required"], "optional": env["optional"], "fieldKeys": list(env["fields"])}
    members += [f"frameEnvelope.fields.{k}" for k in env["fields"]]
    members += [f"frameSchemas.{k}" for k in ws["frameSchemas"]]
    for group in ("definitions", "payloadSchemas"):
        for name, body in ws[group].items():
            if isinstance(body, str):
                members.append(f"{group}.{name}")
                records[f"{group}.{name}"] = {"stringDefinition": body}
                continue
            rec = {"required": body.get("required", []), "optional": body.get("optional"),
                   "fieldKeys": list(body.get("fields", {})),
                   "recordLevelText": {k: v for k, v in body.items() if k not in ("closed", "required", "optional", "fields")}}
            records[f"{group}.{name}"] = rec
            if "fields" in body:
                members += [f"{group}.{name}.fields.{k}" for k in body["fields"]]
            else:
                members += [f"{group}.{name}.required.{k}" for k in body["required"]]
    return members, records


def original_text(ws, key):
    parts = key.split(".")
    node = ws
    for i, p in enumerate(parts):
        if p == "required" and i == len(parts) - 2:
            return f"member of required list: {parts[-1]}"
        node = node[p]
    return node


def presence(records, key):
    parts = key.split(".")
    if parts[0] == "frameSchemas":
        return "n/a (frame table row)"
    rec = records[".".join(parts[:-2])] if len(parts) >= 3 else records.get(key)
    if rec is None or "required" not in rec:
        return "n/a (string definition)"
    if parts[-1] in rec["required"]:
        return "required"
    if rec.get("optional") and parts[-1] in rec["optional"]:
        return "optional"
    return "UNLISTED"


def main():
    docs, pins = load()
    ws = pointer(docs["delivery"], "/typescriptSemanticSubstrate/providerProtocol/wireSchema")
    members, records = enumerate_members(ws)
    rows_in = {**ENVELOPE, **FRAMES, **DEFS, **PAYLOADS}

    # 1. exhaustive, exact coverage
    missing = sorted(set(members) - set(rows_in))
    extra = sorted(set(rows_in) - set(members))
    check(not missing, f"members without rows: {missing}")
    check(not extra, f"rows without members: {extra}")
    check(len(members) == len(set(members)), "duplicate member selectors")

    # 2. required lists vs field maps (exhaustive)
    record_compare = []
    for rk, rec in records.items():
        if "required" not in rec:
            continue
        req, fk, opt = rec["required"], rec["fieldKeys"], rec.get("optional")
        entry = {"record": rk, "required": len(req), "fields": len(fk), "optional": opt,
                 "requiredEqualsFieldKeys": (set(req) == set(fk)) if fk else None,
                 "hasFieldMap": bool(fk)}
        if fk:
            check(set(req) | set(opt or []) == set(fk), f"required/optional != fields for {rk}")
            check(req == fk, f"required order != fields order for {rk}") if False else None
            entry["sameOrder"] = req == fk
        check(opt in (None, []), f"non-empty optional list for {rk}: {opt}")
        record_compare.append(entry)

    # 3. row invariants, ref resolution, wire-type cross-check
    rows, wire_checks = [], {"checked": 0, "skipped": 0, "mismatch": []}
    for key in members:
        row = dict(rows_in[key])
        wt = row["wireType"]
        if key.startswith("frameSchemas."):
            check(wt is None, f"frame row has wireType {key}")
        else:
            check(wt is not None and all(p in WIRE_TYPES for p in wt.split("|")), f"bad wireType {key}: {wt}")
        check(row["disposition"] in DISPOSITIONS, f"bad disposition {key}")
        check(row["successorMemberChange"] in MEMBER_CHANGES, f"bad member change {key}")
        if row["disposition"] == "replaced" and not key.startswith(("frameSchemas.", "definitions.")) :
            check(row["successorMemberChange"] is not None, f"replaced payload member without successorMemberChange {key}")
        for g in row["gaps"]:
            check(g in GAPS, f"unknown gap {g} in {key}")
        for h in row["handwrittenChecks"]:
            head = h.split(":")[0].split(" ")[0]
            check(head in HANDWRITTEN_OWNERS or head.startswith("TS2-G") or ":" not in h, f"unknown handwritten owner {head} in {key}")
        ref = row["schemaNativeRef"]
        if ref:
            try:
                _, node, base = resolve(docs, ref)
                row["schemaNativeRefResolves"] = True
            except Exception as exc:  # noqa: BLE001
                check(False, f"unresolvable ref {ref} in {key}: {exc}")
                node = None
            if node is not None and wt and not key.startswith("frameSchemas.") and row["successorMemberChange"] != "removed" and UNSTATED not in wt and B not in wt:
                got = kinds(docs, node, base)
                want = set(wt.split("|"))
                wire_checks["checked"] += 1
                if not want <= got | {N} or not got <= want | {"negative-int64"}:
                    wire_checks["mismatch"].append({"member": key, "row": sorted(want), "ref": sorted(got)})
            else:
                wire_checks["skipped"] += 1
        sel = WS + "." + (key.rsplit(".required.", 1)[0] + ".required" if ".required." in key else key)
        row = {"member": key, "presence": presence(records, key),
               "source": {"path": SOURCES["delivery"][0], "sha256": SOURCES["delivery"][1], "selector": sel,
                          "originalText": original_text(ws, key)}, **row}
        rows.append(row)
    check(not wire_checks["mismatch"], f"wire type mismatches: {wire_checks['mismatch']}")

    # 4. new members from schema-native records
    new_rows = []
    new_records = {"NativeContextVerifiedV1": "startup", "PreAnalyzeUnavailableV1": "startup"}
    for (rec, mem), row in NEW.items():
        _, node, base = resolve(docs, row["schemaNativeRef"])
        got = kinds(docs, node, base)
        want = set(row["wireType"].split("|"))
        check(want <= got | {N} and got <= want, f"new wire type mismatch {rec}.{mem}: {want} vs {got}")
        sid, _, frag = row["schemaNativeRef"].partition("#")
        key = ID_TO_SOURCE[sid]
        new_rows.append({"member": f"{rec}.{mem}", "presence": "required",
                         "source": {"path": SOURCES[key][0], "sha256": SOURCES[key][1], "selector": "#" + frag},
                         **row})
    for rec, key in new_records.items():
        req = docs[key]["$defs"][rec]["required"]
        check(sorted(req) == sorted(m for (r, m) in NEW if r == rec), f"NEW rows != required for {rec}")
    check(sorted(docs["factbatch3"]["required"]) == sorted(m for (r, m) in NEW if r == "FactBatchV3"), "NEW rows != FactBatchV3 required")

    # 5. successor member-list comparisons (exhaustive)
    succ = {
        "payloadSchemas.HelloV1": ("handshake", "/$defs/TypeScriptHelloV2"),
        "payloadSchemas.HelloAckV1": ("handshake", "/$defs/TypeScriptHelloAckV2"),
        "payloadSchemas.OpenUniverseV1": ("startup", "/$defs/TypeScriptOpenUniverseV2"),
        "payloadSchemas.UniverseAcceptedV1": ("startup", "/$defs/TypeScriptUniverseAcceptedV2"),
        "payloadSchemas.CoverageV1": ("startup", "/$defs/TypeScriptCoverageV2"),
        "payloadSchemas.UnavailableV1": ("startup", "/$defs/TypeScriptUnavailableV2"),
        "payloadSchemas.BudgetExhaustedV1": ("startup", "/$defs/TypeScriptBudgetExhaustedV2"),
        "payloadSchemas.FactBatchV1": ("handshake", "/$defs/TypeScriptFactBatchV1Vector"),
        "definitions.CoverageResultV1": ("evidence", "/$defs/CoverageResultV3"),
        "definitions.FactCandidateV1": ("factbatch3", "/properties/candidates/items"),
        "(FactBatchV1 vs negotiated) payloadSchemas.FactBatchV1": ("factbatch3", ""),
        "(PreAnalyze alternative) payloadSchemas.UnavailableV1": ("startup", "/$defs/PreAnalyzeUnavailableV1"),
    }
    comparisons = []
    for label, (key, ptr) in succ.items():
        rk = label.split(") ")[-1]
        orig = records[rk]["required"]
        new = pointer(docs[key], ptr)["required"]
        cmp_ = {"original": label, "successor": f"{SOURCES[key][0]}#{ptr}", "originalRequired": orig, "successorRequired": new,
                "kept": [m for m in orig if m in new], "removedOrMoved": [m for m in orig if m not in new], "added": [m for m in new if m not in orig],
                "sameOrder": [m for m in orig if m in new] == [m for m in new if m in orig]}
        comparisons.append(cmp_)
    by = {c["original"]: c for c in comparisons}
    check(by["payloadSchemas.HelloV1"]["added"] == ["expectedCapabilities", "identityVersions"] and not by["payloadSchemas.HelloV1"]["removedOrMoved"], "HelloV1 successor delta")
    check(by["payloadSchemas.HelloAckV1"]["added"] == ["identityVersions"] and not by["payloadSchemas.HelloAckV1"]["removedOrMoved"], "HelloAckV1 successor delta")
    for r in ("OpenUniverseV1", "UniverseAcceptedV1", "CoverageV1", "UnavailableV1", "BudgetExhaustedV1", "FactBatchV1"):
        c = by["payloadSchemas." + r]
        check(not c["added"] and not c["removedOrMoved"], f"{r} successor member names changed: {c}")
    for (rec, mem) in NEW:
        if rec in ("TypeScriptHelloV2", "TypeScriptHelloAckV2"):
            src = "payloadSchemas.HelloV1" if rec == "TypeScriptHelloV2" else "payloadSchemas.HelloAckV1"
            check(mem in by[src]["added"], f"NEW {rec}.{mem} not an added member")
    fc = by["definitions.FactCandidateV1"]
    check(fc["removedOrMoved"] == ["canonicalRelationPayload"] and fc["added"] == ["canonicalRelationPayloadHex", "decodedRelationPayload"], "FactCandidate vector delta")

    # 6. traces (G7) and links
    fp = docs["factplane"]["factRecordContractV1"]
    rust = docs["rust2"]["wireSchema"]["definitions"]
    c2key = [f["field"] for f in docs["c2v3"]["coverageKey"]["key"]]
    ts_ck = ws["definitions"]["CoverageKeyV1"]["required"]
    ne_ck = docs["evidence"]["$defs"]["CoverageKeyV2"]["required"]
    traces = {
        "FactCandidateV1": {
            "delivery.v2 TS required": ws["definitions"]["FactCandidateV1"]["required"],
            "fact-plane.v1 candidateSchema required": fp["candidateSchema"]["required"],
            "rust-provider-protocol.v2 FactCandidateV1": rust["FactCandidateV1"],
            "tsEqualsFactPlane": ws["definitions"]["FactCandidateV1"]["required"] == fp["candidateSchema"]["required"],
            "universeValueSupersession": {"typescript-semantic": "native-evidence.md:125 (TypeScriptSemanticUniverseKey-typed coordinates)", "rust-semantic": "native-evidence.md:128 (planAndDomainProjection algorithms)"},
            "finding": "Same member list; TS restates field texts, Rust references fact-plane with a bstr wireAdjustment. Universe-id value supersession is stated per language by different §0 rows; producer/language constants differ by provider. Not one shared generated record without root selection.",
        },
        "AnchorRefV1": {"delivery.v2 required": ws["definitions"]["AnchorRefV1"]["required"], "fact-plane anchorSchema required": fp["anchorSchema"]["required"],
                         "equal": ws["definitions"]["AnchorRefV1"]["required"] == fp["anchorSchema"]["required"]},
        "CoverageKey": {
            "delivery.v2 TS CoverageKeyV1 required": ts_ck,
            "c2-plan-stage-schema.v3 coverageKey.key fields": c2key,
            "rust-provider-protocol.v2 CoverageKeyV2 required": rust["CoverageKeyV2"]["required"],
            "native-evidence.schemas.v2 CoverageKeyV2 required": ne_ck,
            "tsEqualsC2v3": ts_ck == c2key,
            "tsEqualsRust2": ts_ck == rust["CoverageKeyV2"]["required"],
            "nativeV2OnlyMembers": [m for m in ne_ck if m not in ts_ck],
            "tsOnlyMembers": [m for m in ts_ck if m not in ne_ck],
            "finding": "TS CoverageKeyV1 and rust2 CoverageKeyV2 share c2 v3 membership but are distinct owners; native CoverageKeyV2 is a different 5-member entry key (bare-hex universes, no producer/producerVersion/schemaVersion). TS2 request keys remain CoverageKeyV1; entries use native CoverageKeyV2.",
        },
    }
    check(traces["FactCandidateV1"]["tsEqualsFactPlane"], "TS FactCandidateV1 != fact-plane candidateSchema")
    check(traces["AnchorRefV1"]["equal"], "AnchorRefV1 != anchorSchema")

    lim = {k: v for k, v in ws["limits"].items() if k != "limitRule"}
    hs_lim = {k: v["const"] for k, v in docs["handshake"]["$defs"]["TypeScriptProtocolLimitsV1"]["properties"].items()}
    check(lim == hs_lim, "limits != TypeScriptProtocolLimitsV1")
    tok = set(docs["handshake"]["$defs"]["TypeScriptCapabilityToken"]["enum"])
    check(tok <= set(docs["evidence"]["$defs"]["CapabilityToken"]["enum"]), "TS tokens not subset of CapabilityToken")
    frames_vocab = set(ws["frameSchemas"]) | {"NativeContextVerified"}
    order_frames = {r["frame"] for r in docs["ts2order"]["rules"]} - {"*", "*PROCESS_FAULT", "eof", "zero-exit"}
    check(frames_vocab == order_frames, f"frame vocabulary != order table frames: {frames_vocab ^ order_frames}")
    pp = pointer(docs["delivery"], "/typescriptSemanticSubstrate/providerProtocol")
    check(set(pp["closedHostToWorkerFrames"]) | set(pp["closedWorkerToHostFrames"]) == set(ws["frameSchemas"]), "closed frame lists != frameSchemas")
    link_extra = {"limitsValues": lim, "commitmentDomains": ws["commitments"]["domains"], "typescriptCapabilityTokens": sorted(tok)}

    # 7. coverage counts
    groups = {}
    for r in rows:
        g = r["member"].split(".")[0]
        groups.setdefault(g, {"rows": 0})
        groups[g]["rows"] += 1
    disp = {}
    for r in rows + new_rows:
        disp[r["disposition"]] = disp.get(r["disposition"], 0) + 1
    gap_use = {g: sorted({r["member"] for r in rows + new_rows if g in r["gaps"]}) for g in GAPS}
    coverage = {
        "originalMembers": len(members), "rows": len(rows), "newRows": len(new_rows),
        "byGroup": groups,
        "records": {"definitions": len(ws["definitions"]), "payloadSchemas": len(ws["payloadSchemas"]), "frameSchemas": len(ws["frameSchemas"])},
        "stringDefinitions": sum(1 for r in records.values() if "stringDefinition" in r),
        "dispositions": disp,
        "withSchemaNativeRef": sum(1 for r in rows if r["schemaNativeRef"]),
        "withHandwrittenChecks": sum(1 for r in rows + new_rows if r["handwrittenChecks"]),
        "withGaps": sum(1 for r in rows + new_rows if r["gaps"]),
        "wireTypeCrossChecks": {"checked": wire_checks["checked"], "skipped": wire_checks["skipped"], "mismatches": len(wire_checks["mismatch"])},
        "requiredListComparisons": len(record_compare),
        "successorComparisons": len(comparisons),
        "failures": FAIL,
    }

    fields = {
        "artifact": "m1-typescript-wire-translation-01/fields",
        "standing": "PROPOSED implementation input for root review. Not approval, not a wire change, not product code. typescript-semantic protocol major 2 translation of inherited delivery.v2 wireSchema.",
        "proposedEnvelopeImplementationName": {"name": "TypeScriptFrameV2", "isWireField": False, "isWireName": False},
        "sources": pins,
        "conventions": {
            "wireTypes": sorted(WIRE_TYPES), "unionSeparator": "|",
            "dispositions": {"retained": "inherited member carried unchanged in shape and value domain", "replaced": "schema-native successor record/definition owns the member (see successorMemberChange)",
                             "value-substituted": "inherited shape and name kept; value domain replaced by a stated supersession", "new": "member absent from delivery.v2, published by a schema-native owner"},
            "byteString": "recorded as wire type byte-string only; no JSON representation selected (TS2-G1)",
            "handwrittenOwners": HANDWRITTEN_OWNERS,
        },
        "records": record_compare,
        "rows": rows,
        "newRows": new_rows,
        "successorComparisons": comparisons,
        "traces": traces,
        "links": LINKS, "linkValues": link_extra,
        "gaps": {k: {**v, "rowsCiting": gap_use[k]} for k, v in GAPS.items()},
        "coverage": coverage,
    }
    with open(os.path.join(OUT, "fields.json"), "w") as fh:
        json.dump(fields, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    with open(os.path.join(OUT, "coverage.json"), "w") as fh:
        json.dump(coverage, fh, indent=1)
        fh.write("\n")
    write_md(fields)
    print(json.dumps(coverage, indent=1))
    return 1 if FAIL else 0


def esc(v):
    if v is None:
        return ""
    if not isinstance(v, str):
        v = json.dumps(v, ensure_ascii=False)
    return v.replace("|", "\\|").replace("\n", " ")


def write_md(f):
    head = open(os.path.join(HERE, "translation-head.md")).read()
    cov = f["coverage"]
    counts = (f"- original members tabulated: **{cov['originalMembers']}** (rows {cov['rows']}; frameSchemas {cov['byGroup']['frameSchemas']['rows']}, "
              f"frameEnvelope {cov['byGroup']['frameEnvelope']['rows']}, definitions {cov['byGroup']['definitions']['rows']}, payloadSchemas {cov['byGroup']['payloadSchemas']['rows']})\n"
              f"- new schema-native member rows: **{cov['newRows']}**\n- dispositions (rows+new): {esc(cov['dispositions'])}\n"
              f"- rows with schema-native ref: {cov['withSchemaNativeRef']}; with handwritten checks: {cov['withHandwrittenChecks']}; citing gaps: {cov['withGaps']}\n"
              f"- wire-type cross-checks against resolved refs: {cov['wireTypeCrossChecks']['checked']} checked, {cov['wireTypeCrossChecks']['mismatches']} mismatches\n"
              f"- required-list comparisons: {cov['requiredListComparisons']}; successor member-list comparisons: {cov['successorComparisons']}\n"
              f"- script failures: {len(cov['failures'])}\n")
    out = [head.replace("{{COUNTS}}", counts)]

    out.append("\n## 6. Frame table (TS2)\n\n| frame | TS2 payload / terminal | disposition | schema-native ref | notes |\n|---|---|---|---|---|\n")
    for r in f["rows"]:
        if r["member"].startswith("frameSchemas."):
            out.append(f"| {r['member'].split('.',1)[1]} | {esc(r['boundsOrVocabulary'])} | {r['disposition']} | {esc(r['schemaNativeRef'])} | {esc(r['note'])} {esc(' '.join(r['gaps']))} |\n")
    out.append("| NativeContextVerified | worker-to-host; payloadType NativeContextVerifiedV1; terminal false | new | opensip.product.provider-startup.1#/$defs/NativeContextVerifiedV1 | native-evidence.md:121, 2881 |\n")

    out.append("\n## 7. Field rows (every inherited member)\n\nColumns: member · presence · wire type · bounds / closed vocabulary · disposition (member change) · schema-native ref · derivation · handwritten checks · gaps. "
               "Source for every row: `docs/coop/artifacts/delivery.v2.json` sha256 `47b6cfd1…e3cabf3`, selector `" + WS + ".<member>`; exact original text is in fields.json `rows[].source.originalText`.\n")
    current = None
    for r in f["rows"]:
        if r["member"].startswith("frameSchemas."):
            continue
        parts = r["member"].split(".")
        rec = ".".join(parts[:2]) if parts[0] != "frameEnvelope" else "frameEnvelope"
        if parts[0] == "definitions" and len(parts) == 2:
            rec = "definitions (string definitions)"
        if rec != current:
            current = rec
            out.append(f"\n### {rec}\n\n| member | presence | wire | bounds / vocabulary | disposition | ref | derivation | handwritten | gaps |\n|---|---|---|---|---|---|---|---|---|\n")
        d = r["disposition"] + (f" ({r['successorMemberChange']})" if r["successorMemberChange"] else "")
        extra = "; ".join(x for x in [r["derivation"], r["note"]] if x)
        out.append(f"| {esc(parts[-1])} | {r['presence']} | {esc(r['wireType'])} | {esc(r['boundsOrVocabulary'])} | {esc(d)} | {esc(r['schemaNativeRef'])} | {esc(extra)} | {esc('; '.join(r['handwrittenChecks']))} | {esc(' '.join(r['gaps']))} |\n")

    out.append("\n## 8. New members (schema-native owners)\n\n| record.member | wire | bounds / vocabulary | source selector | handwritten | gaps |\n|---|---|---|---|---|---|\n")
    for r in f["newRows"]:
        out.append(f"| {r['member']} | {esc(r['wireType'])} | {esc(r['boundsOrVocabulary'])} | `{r['source']['path']}` {esc(r['source']['selector'])} | {esc('; '.join(r['handwrittenChecks']))} | {esc(' '.join(r['gaps']))} |\n")

    out.append("\n## 9. Successor member-list comparisons (exhaustive)\n\n| original | successor | kept | removed/moved | added | same order |\n|---|---|---|---|---|---|\n")
    for c in f["successorComparisons"]:
        out.append(f"| {esc(c['original'])} | `{esc(c['successor'])}` | {len(c['kept'])}/{len(c['originalRequired'])} | {esc(c['removedOrMoved'])} | {esc(c['added'])} | {c['sameOrder']} |\n")
    out.append("\nRequired list vs field map, every closed record: ")
    out.append("; ".join(f"{e['record']} {e['required']}/{e['fields'] if e['hasFieldMap'] else 'no-field-map'}{'' if e.get('sameOrder', True) else ' (order differs)'}" for e in f["records"]) + ".\n")

    out.append("\n## 10. Gap register\n\n")
    for k, g in f["gaps"].items():
        out.append(f"### {k} — {g['title']}\n\n{g['finding']}\n\n- action: {g['action']}\n- rows citing: {esc(', '.join(g['rowsCiting'])) or '(record-level)'}\n\n")

    out.append("## 11. Inherited links (not new wire fields)\n\n| link | source | disposition | authority | ref |\n|---|---|---|---|---|\n")
    for k, l in f["links"].items():
        out.append(f"| {k} | `{esc(l['source'])}` | {esc(l['disposition'])} | {esc(l['authority'])} | {esc(l.get('schemaNativeRef'))} |\n")
    out.append(f"\nLimit values (== TypeScriptProtocolLimitsV1 consts, asserted): {esc(f['linkValues']['limitsValues'])}\n\nCommitment domains (retained): {esc(f['linkValues']['commitmentDomains'])}\n")

    out.append("\n## 12. Source pins\n\n| path | sha256 |\n|---|---|\n")
    for p in f["sources"]:
        out.append(f"| `{p['path']}` | `{p['sha256']}` |\n")
    with open(os.path.join(OUT, "translation.md"), "w") as fh:
        fh.write("".join(out))


if __name__ == "__main__":
    sys.exit(main())
