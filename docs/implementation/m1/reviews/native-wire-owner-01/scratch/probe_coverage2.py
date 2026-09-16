"""Independent set comparison: field-coverage.json vs prior TS2/Rust3 inventories and gap lists; carrier targets vs IDL."""
import json, re, sys
B = "/tmp/opensip-implementation/"
fc = json.load(open(B + "m1-native-wire-owner-subject-01/field-coverage.json"))
idl = json.load(open(B + "m1-native-wire-owner-subject-01/wire-carriers.v1.json"))
ts = json.load(open(B + "m1-typescript-wire-translation-01/fields.json"))
rs = json.load(open(B + "m1-rust-wire-translation-01/fields.json"))
out = {}

ts_inv = [r["member"] for r in ts["rows"]] + [r["member"] for r in ts["newRows"]]
rs_inv = list(rs["envelope"].keys()) + list(rs["rows"]) + list(rs["externalRows"]) + list(rs["newRows"]) + list(rs["frames"])
for proto, inv in (("typescript-semantic", ts_inv), ("rust-semantic", rs_inv)):
    got = [r["inventory"] for r in fc["rows"][proto]]
    out[proto] = {"inventoryRows": len(inv), "uniqueInventory": len(set(inv)), "coverageRows": len(got),
                  "missingFromCoverage": sorted(set(inv) - set(got))[:20], "extraInCoverage": sorted(set(got) - set(inv))[:20]}

records, scalars = idl["records"], idl["scalars"]


def member_names(rec):
    r = records[rec]
    if r["kind"] == "record":
        return {m["name"] for m in r["members"]}
    if r["kind"] == "variant-record":
        return set(r["memberOrder"])
    return None  # alias: members come from extern


frame_types = {p: {f["frameType"] for f in idl["protocols"][p]["frames"]} for p in idl["protocols"]}
bad, statuses, notcarried = [], {}, []
for proto in fc["rows"]:
    for r in fc["rows"][proto]:
        statuses.setdefault(proto, {}).setdefault(r["status"], 0)
        statuses[proto][r["status"]] += 1
        c = r.get("carrier")
        if r["status"] == "not-carried":
            notcarried.append({"protocol": proto, "inventory": r["inventory"], "reason": r.get("reason") or r.get("carrier") or r.get("note")})
            continue
        if not isinstance(c, str):
            bad.append({"inventory": r["inventory"], "carrier": c, "why": "non-string carrier"}); continue
        head = c.split(" ")[0]
        m = re.match(r"^([A-Za-z0-9]+)(?:\.([A-Za-z0-9]+))?", head)
        rec, mem = m.group(1), m.group(2)
        if rec in records:
            names = member_names(rec)
            if mem and names is not None and mem not in names:
                bad.append({"inventory": r["inventory"], "carrier": c, "why": "member absent"})
        elif rec in scalars or re.match(r"^(Handshake1|Startup1|Native2|Occupancy1)", rec):
            pass
        elif rec in frame_types[proto] or rec.startswith("frame"):
            pass
        else:
            bad.append({"inventory": r["inventory"], "carrier": c, "why": "unknown carrier head"})
out["statuses"] = statuses
out["unresolvableCarrierTargets"] = bad[:40]
out["unresolvableCount"] = len(bad)
out["notCarried"] = notcarried

# every IDL record member reachable from some coverage row (reverse direction)
covered = {(r.get("carrier") or "").split(" ")[0] for p in fc["rows"] for r in fc["rows"][p]}
uncovered = []
for rec, r in records.items():
    names = member_names(rec)
    for n in sorted(names or []):
        if rec + "." + n not in covered:
            uncovered.append(rec + "." + n)
out["idlMembersWithoutCoverageRow"] = uncovered

gaps_seen = {}
for p in fc["rows"]:
    for r in fc["rows"][p]:
        for g, v in r["gapResolutions"].items():
            gaps_seen.setdefault(g, set()).add(v if isinstance(v, str) else json.dumps(v)[:60])
out["tsGapsMissing"] = [g for g in ts["gaps"] if g not in gaps_seen]
out["rsGapsMissing"] = [g for g in rs["gaps"] if g not in gaps_seen]
out["gapResolutionMap"] = {g: sorted(v) for g, v in sorted(gaps_seen.items())}
out["tsGapText"] = {g: json.dumps(v, ensure_ascii=False)[:260] for g, v in ts["gaps"].items()}
out["rsGapText"] = {g: json.dumps(v, ensure_ascii=False)[:260] for g, v in rs["gaps"].items()}
json.dump(out, sys.stdout, indent=1, ensure_ascii=False)
