#!/usr/bin/env python
"""Cross-check the declared 17-file sourceDelta against the measured v16->v17
delta, and audit every transitive source-pin registry.

The repin risk this probe addresses: a pin registry whose bytes are re-issued to
match a changed source would make a check pass without the check ever having
agreed with the reviewed bytes. So for every pin registry we assert
  pinned sha == actual frozen sha of the pinned file
and we separately report which pins MOVED between v16 and v17, and whether each
moved pin's target also moved (legitimate) or not (suspicious).
"""
import hashlib
import json
import os
import sys

REV = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews"
ROOT17 = "/tmp/opensip-design-corrections/candidate-subject.v17"
ASSESS = os.path.join(
    ROOT17,
    "docs/coop/design-corrections/reviews/codex-post-reset.v1/"
    "successor-source-assessment.v17.json",
)


def jload(p):
    with open(p, "rb") as fh:
        return json.loads(fh.read())


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    out = sys.argv[1]
    m16 = jload(os.path.join(REV, "candidate-subject.v16.json"))
    m17 = jload(os.path.join(REV, "candidate-subject.v17.json"))
    a = {f["path"]: f["sha256"] for f in m16["files"]}
    b = {f["path"]: f["sha256"] for f in m17["files"]}
    changed = {p for p in set(a) & set(b) if a[p] != b[p]}
    added = set(b) - set(a)

    assess = jload(ASSESS)
    declared = {s["path"]: s for s in assess["sourceDelta"]}

    rep = {"declaredSourceDeltaCount": len(declared)}

    # 1. Every declared source-delta row must match frozen reality.
    rows = []
    for p, s in declared.items():
        full = os.path.join(ROOT17, p)
        actual = sha_file(full) if os.path.isfile(full) else None
        rows.append(
            {
                "path": p,
                "declaredBefore": s["beforeSha256"],
                "declaredAfter": s["afterSha256"],
                "coauthorSha256": s.get("coauthorSha256"),
                "actualV16Sha": a.get(p),
                "actualV17Sha": b.get(p),
                "beforeMatchesV16": a.get(p) == s["beforeSha256"],
                "afterMatchesV17": b.get(p) == s["afterSha256"],
                "afterMatchesFrozenBytes": actual == s["afterSha256"],
                "coauthorEqualsAfter": s.get("coauthorSha256") == s["afterSha256"],
            }
        )
    rep["sourceDeltaRows"] = rows
    rep["sourceDeltaFullyConsistent"] = all(
        r["beforeMatchesV16"] and r["afterMatchesV17"]
        and r["afterMatchesFrozenBytes"] and r["coauthorEqualsAfter"]
        for r in rows
    )

    # 2. Changed files NOT declared in the 17-file source delta.
    def scaffold(p):
        return "/reviews/" in p
    undeclared_changed = sorted(
        p for p in changed if not scaffold(p) and p not in declared
    )
    rep["changedNonScaffoldNotInSourceDelta"] = [
        {"path": p, "v16": a[p], "v17": b[p],
         "byteDelta": next(f["bytes"] for f in m17["files"] if f["path"] == p)
         - next(f["bytes"] for f in m16["files"] if f["path"] == p)}
        for p in undeclared_changed
    ]
    rep["changedNonScaffoldNotInSourceDeltaCount"] = len(undeclared_changed)
    rep["addedNonScaffold"] = sorted(p for p in added if not scaffold(p))

    # 3. Pin registry audit.
    pin_files = sorted(
        p for p in b
        if p.startswith("docs/coop/design-corrections/")
        and os.path.basename(p).startswith("source-pins")
        and not scaffold(p)
    )
    pin_report = []
    for pf in pin_files:
        doc = jload(os.path.join(ROOT17, pf))
        base = os.path.dirname(pf)
        entries = []
        # tolerate several shapes
        cand = doc if isinstance(doc, list) else None
        if cand is None:
            for k, v in doc.items():
                if isinstance(v, list) and v and isinstance(v[0], dict):
                    cand = v
                    break
                if isinstance(v, dict):
                    # mapping path->sha or path->{sha256:..}
                    if all(isinstance(x, (str, dict)) for x in v.values()):
                        cand = [
                            {"path": kk,
                             "sha256": vv if isinstance(vv, str) else vv.get("sha256")}
                            for kk, vv in v.items()
                        ]
                        break
        if cand is None:
            pin_report.append({"pinFile": pf, "parseShape": "UNRECOGNISED",
                               "raw": json.dumps(doc)[:400]})
            continue
        for e in cand:
            if not isinstance(e, dict):
                continue
            path = e.get("path") or e.get("file") or e.get("source")
            sha = e.get("sha256") or e.get("sha") or e.get("digest")
            if not path or not sha:
                continue
            # resolve relative to repo root, else relative to pin dir
            for candidate in (path, os.path.join(base, path),
                              os.path.normpath(os.path.join(base, path))):
                full = os.path.join(ROOT17, candidate)
                if os.path.isfile(full):
                    resolved = candidate
                    break
            else:
                entries.append({"pinnedPath": path, "pinnedSha": sha,
                                "resolved": None, "targetExists": False,
                                "pinMatchesFrozen": False})
                continue
            actual = sha_file(os.path.join(ROOT17, resolved))
            entries.append(
                {
                    "pinnedPath": path,
                    "resolved": resolved,
                    "pinnedSha": sha,
                    "actualFrozenSha": actual,
                    "targetExists": True,
                    "pinMatchesFrozen": actual == sha,
                    "targetChangedV16toV17": resolved in changed,
                }
            )
        pin_report.append(
            {
                "pinFile": pf,
                "pinFileChangedV16toV17": pf in changed,
                "entryCount": len(entries),
                "allPinsMatchFrozen": all(x["pinMatchesFrozen"] for x in entries),
                "staleOrMismatched": [x for x in entries
                                      if not x["pinMatchesFrozen"]],
                "movedPinsWhoseTargetDidNotChange": [
                    x for x in entries
                    if x.get("targetChangedV16toV17") is False
                    and pf in changed
                ][:5],
                "entries": entries,
            }
        )
    rep["pinRegistries"] = pin_report
    rep["pinRegistryCount"] = len(pin_report)
    rep["allPinRegistriesConsistent"] = all(
        r.get("allPinsMatchFrozen") for r in pin_report if "allPinsMatchFrozen" in r
    )

    with open(out, "w") as fh:
        json.dump(rep, fh, indent=1, sort_keys=True)

    print("declaredSourceDeltaCount:", rep["declaredSourceDeltaCount"])
    print("sourceDeltaFullyConsistent:", rep["sourceDeltaFullyConsistent"])
    for r in rows:
        if not (r["beforeMatchesV16"] and r["afterMatchesV17"]
                and r["afterMatchesFrozenBytes"] and r["coauthorEqualsAfter"]):
            print("  INCONSISTENT:", json.dumps(r))
    print("\nchanged non-scaffold NOT in 17-file sourceDelta:",
          rep["changedNonScaffoldNotInSourceDeltaCount"])
    for r in rep["changedNonScaffoldNotInSourceDelta"]:
        print("   %+7d %s" % (r["byteDelta"], r["path"]))
    print("\nadded non-scaffold:", rep["addedNonScaffold"])
    print("\n--- PIN REGISTRIES (%d) ---" % rep["pinRegistryCount"])
    for r in pin_report:
        print(r["pinFile"], "| changed:", r.get("pinFileChangedV16toV17"),
              "| entries:", r.get("entryCount"),
              "| allMatchFrozen:", r.get("allPinsMatchFrozen"))
        for s in r.get("staleOrMismatched", []):
            print("     MISMATCH:", json.dumps(s))
    print("\nallPinRegistriesConsistent:", rep["allPinRegistriesConsistent"])


if __name__ == "__main__":
    main()
