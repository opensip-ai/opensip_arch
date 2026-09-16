"""Compare live vs candidate lock/features; only platform libc edge should be new."""
from __future__ import annotations

import json
import sys
from pathlib import Path

REVIEW = Path("/tmp/opensip-implementation/m2-grok-foundation-primitives-selection-v1-review/review")


def index(meta: dict) -> dict:
    packages = {row["id"]: row for row in meta["packages"]}
    nodes = {row["id"]: row for row in meta["resolve"]["nodes"]}
    by_name = {}
    for pid, pkg in packages.items():
        node = nodes[pid]
        by_name[pkg["name"]] = {
            "id": pid,
            "name": pkg["name"],
            "version": pkg["version"],
            "source": pkg.get("source"),
            "features": sorted(node.get("features") or []),
            "deps": sorted(
                {
                    packages[edge["pkg"]]["name"]
                    for edge in node.get("deps") or []
                    if any(k.get("kind") != "dev" for k in edge.get("dep_kinds") or [{}])
                }
            ),
        }
    return by_name


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    cand = json.loads((REVIEW / "results" / "logs" / "metadata.stdout").read_bytes())
    live = json.loads((REVIEW / "results" / "logs" / "live-metadata.stdout").read_bytes())
    c = index(cand)
    l = index(live)
    names = sorted(set(c) | set(l))
    rows = []
    unexpected = []
    for name in names:
        a = c.get(name)
        b = l.get(name)
        if a is None or b is None:
            rows.append({"name": name, "inCandidate": a is not None, "inLive": b is not None})
            if name != "opensip-rust-provider":
                unexpected.append(name)
            continue
        feature_eq = a["features"] == b["features"]
        version_eq = a["version"] == b["version"] and a["source"] == b["source"]
        dep_eq = a["deps"] == b["deps"]
        allowed_dep_diff = name == "opensip-platform" and set(a["deps"]) - set(b["deps"]) == {"libc"} and set(b["deps"]) - set(a["deps"]) == set()
        ok = feature_eq and version_eq and (dep_eq or allowed_dep_diff)
        rows.append({
            "name": name,
            "versionEqual": version_eq,
            "featuresEqual": feature_eq,
            "depsEqual": dep_eq,
            "allowedPlatformLibcEdge": allowed_dep_diff,
            "candidateDeps": a["deps"],
            "liveDeps": b["deps"],
            "candidateFeatures": a["features"],
            "liveFeatures": b["features"],
            "ok": ok,
        })
        if not ok:
            unexpected.append(name)
    libc = c.get("libc", {})
    platform = c.get("opensip-platform", {})
    out = {
        "unexpected": unexpected,
        "allOkExceptDeclaredPlatformLibc": not unexpected,
        "libc": libc,
        "platformDeps": platform.get("deps"),
        "rows": rows,
        "candidatePackageCount": len(c),
        "livePackageCount": len(l),
    }
    (REVIEW / "results" / "lock-features.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "allOkExceptDeclaredPlatformLibc": out["allOkExceptDeclaredPlatformLibc"],
        "unexpected": unexpected,
        "platformDeps": platform.get("deps"),
        "livePlatformDeps": l.get("opensip-platform", {}).get("deps"),
        "libcVersion": libc.get("version"),
        "libcSource": libc.get("source"),
        "libcFeatures": libc.get("features"),
        "liveLibcFeatures": l.get("libc", {}).get("features"),
    }, indent=2))


if __name__ == "__main__":
    main()
