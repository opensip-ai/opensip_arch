"""Bounded classification of the exact 68 selected patterns. No 74k corpus."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
LIVE = Path("/Users/sb/code/opensip-ai/opensip")
REVIEW = Path("/tmp/opensip-implementation/m2-grok-schema-pattern-trials-review-01/review")
T1 = ARCH / "docs/implementation/m2/trials/schema-pattern-01"
T2 = ARCH / "docs/implementation/m2/trials/schema-pattern-02"
ORIG1 = Path("/tmp/opensip-implementation/m2-schema-pattern-trial-01")
ORIG2 = Path("/tmp/opensip-implementation/m2-schema-pattern-trial-02")
CARGO = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
RUSTC = "/opt/homebrew/Cellar/rust/1.95.0/bin/rustc"
PY = "/tmp/opensip-implementation/metadata-reference-env/bin/python"


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def pin(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": sha256_bytes(raw)}


def adapt(pattern: str) -> str:
    out = []
    in_class = False
    escaped = False
    for char in pattern:
        if escaped:
            out.append(char)
            escaped = False
            continue
        if char == "\\":
            out.append(char)
            escaped = True
            continue
        if char == "[":
            in_class = True
        elif char == "]":
            in_class = False
        if not in_class and char == "$":
            out.append(r"(?=\n?(?![\s\S]))")
        elif not in_class and char == ".":
            out.append(r"[^\n]")
        else:
            out.append(char)
    if escaped or in_class:
        raise ValueError("unclosed escape or class")
    return "".join(out)


def features(pattern: str) -> dict:
    in_class = False
    escaped = False
    dollars = 0
    dots = 0
    first_rbracket_class = False
    classes = 0
    i = 0
    chars = list(pattern)
    while i < len(chars):
        char = chars[i]
        if escaped:
            escaped = False
            i += 1
            continue
        if char == "\\":
            escaped = True
            i += 1
            continue
        if char == "[":
            in_class = True
            classes += 1
            nxt = chars[i + 1] if i + 1 < len(chars) else ""
            if nxt == "^":
                nxt2 = chars[i + 2] if i + 2 < len(chars) else ""
                if nxt2 == "]":
                    first_rbracket_class = True
            elif nxt == "]":
                first_rbracket_class = True
            i += 1
            continue
        if char == "]":
            in_class = False
            i += 1
            continue
        if not in_class and char == "$":
            dollars += 1
        if not in_class and char == ".":
            dots += 1
        i += 1
    return {
        "unescapedDollarOutsideClass": dollars,
        "unescapedDotOutsideClass": dots,
        "characterClasses": classes,
        "firstRbracketClass": first_rbracket_class,
        "hasDotStar": ".*" in pattern,
        "hasLookahead": "(?" in pattern,
        "hasNegativeLookahead": "(?!" in pattern,
        "hasAbsoluteEndAssertion": "(?![\\s\\S])" in pattern or "(?![\\s\\S])" in pattern,
        "anchoredCaret": pattern.startswith("^"),
        "usesSearchNotFullmatch": not pattern.startswith("^"),
    }


def closed_kind(pattern: str) -> str:
    if pattern in (
        "(^|/)\\.\\.?(/|$)",
        "^(?!/)(?!.*(^|/)\\.\\.?(/|$))[^\\u0000\\\\]*(?![\\s\\S])",
        "^(?!/)(?!.*(^|/)\\.\\.?(/|$))[^\\u0000\\\\]+(?![\\s\\S])",
    ):
        return "logical-path-family-already-has-closed-predicate-precedent"
    if "security.repo-execution-grant" in pattern:
        return "unescaped-wildcard-security-id-selected-bytes-widen"
    if pattern.startswith("^security\\."):
        return "escaped-literal-security-id"
    if "[0-9a-f]{" in pattern and "(?![\\s\\S])" in pattern and ".*" not in pattern and "(?!" not in pattern.replace("(?![\\s\\S])", ""):
        return "hex-or-prefixed-digest-closed"
    if pattern.startswith("^(0|[1-9][0-9]*)\\."):
        return "semver-closed-possible"
    if "(?!\\.\\.?" in pattern or "(?:" in pattern and "[^\\u0000\\\\/]+" in pattern:
        return "segment-path-closed-possible"
    if "\\u0000" in pattern and ".*" not in pattern:
        return "codepoint-class-scan-closed-possible"
    if pattern.startswith("^--") or pattern.startswith("^[A-Z_") or pattern.startswith("^[a-z]") or pattern.startswith("^[A-Za-z0-9_.-]"):
        return "identifier-class-closed-possible"
    if "DIRECTORY_CUSTODY" in pattern or "DISCLOSURE-ONLY" in pattern:
        return "closed-enum-or-tagged"
    if pattern.startswith("^[0-9]{4}-"):
        return "date-or-datetime-closed"
    if pattern.startswith("^#/\\$defs/"):
        return "defs-pointer-closed"
    if pattern.startswith("^(/[A-Za-z0-9-]+)+"):
        return "slash-path-closed"
    if pattern.startswith("^[0-9a-f]{8}-[0-9a-f]{4}-"):
        return "uuid-closed"
    return "needs-manual-classification"


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    census = json.loads((T1 / "pattern-census.json").read_bytes())
    patterns = [r["pattern"] for r in census["patterns"]]
    claimed = json.loads((T2 / "adaptations.json").read_bytes())
    independent = {p: adapt(p) for p in patterns}
    profile_raw = (LIVE / "tools/contracts/runtime/pattern-profile.json").read_bytes()
    profile = json.loads(profile_raw)
    profile_map = {r["source"]: r["ecma262Unicode"] for r in profile["patterns"]}
    registry = json.loads((LIVE / "schemas/registry.json").read_bytes())
    identity_pins = json.loads((ORIG1 / "identity-source-pins.json").read_bytes())
    identity_live = []
    for row in identity_pins["files"]:
        path = LIVE / row["path"]
        raw = path.read_bytes()
        identity_live.append(
            {
                "path": row["path"],
                "pinBytes": row["bytes"],
                "pinSha256": row["sha256"],
                "liveBytes": len(raw),
                "liveSha256": sha256_bytes(raw),
                "equal": len(raw) == row["bytes"] and sha256_bytes(raw) == row["sha256"],
            }
        )
    kinds: dict[str, list[str]] = {}
    rows = []
    for p in patterns:
        kind = closed_kind(p)
        kinds.setdefault(kind, []).append(p)
        feat = features(p)
        adapted = independent[p]
        profile_adapted = profile_map.get(p)
        rows.append(
            {
                "pattern": p,
                "occurrences": len(next(r["occurrences"] for r in census["patterns"] if r["pattern"] == p)),
                "kind": kind,
                **feat,
                "adaptedEqualsSource": adapted == p,
                "independentEqualsArchived": adapted == claimed[p],
                "inProposedPatternProfile": p in profile_map,
                "profileAdapterEqualsTrial02": profile_adapted == adapted if profile_adapted is not None else None,
                "profileAdapterEquivalentNewlineClass": (
                    profile_adapted.replace("[^\\n]", "[^\n]") == adapted.replace("[^\\n]", "[^\n]")
                    if profile_adapted is not None
                    else None
                ),
            }
        )
    profile_only = sorted(set(profile_map) - set(patterns))
    census_only = sorted(set(patterns) - set(profile_map))
    cargo_v = subprocess.check_output([CARGO, "--version"], text=True).strip()
    rustc_v = subprocess.check_output([RUSTC, "--version"], text=True).strip()
    py_v = subprocess.check_output([sys.executable, "-c", "import sys; print(sys.version.split()[0])"], text=True).strip()
    lock = (ORIG1 / "probe/Cargo.lock").read_text()
    regress_checksum = None
    for line in lock.splitlines():
        if "32eef8b2" in line or (regress_checksum is None and line.strip().startswith("checksum =") and "regress" in lock):
            pass
    # parse lock package regress checksum
    import re as _re

    m = _re.search(r'name = "regress"\nversion = "0.12.0"\nsource = .*\nchecksum = "([0-9a-f]+)"', lock)
    regress_checksum = m.group(1) if m else None
    descriptors_live = (LIVE / "crates/identity/src/descriptors.rs").exists()
    out = {
        "python": py_v,
        "cargo": cargo_v,
        "rustc": rustc_v,
        "registrySourceCount": len(registry["sources"]),
        "censusSourceCount": len(census["sources"]),
        "censusPatternCount": len(patterns),
        "occurrenceTotal": sum(len(r["occurrences"]) for r in census["patterns"]),
        "kinds": {k: len(v) for k, v in sorted(kinds.items())},
        "kindPatterns": kinds,
        "rewrittenCount": sum(1 for p in patterns if independent[p] != p),
        "independentEqualsArchivedAll": all(independent[p] == claimed[p] for p in patterns),
        "unescapedDollarCount": sum(1 for r in rows if r["unescapedDollarOutsideClass"]),
        "unescapedDotCount": sum(1 for r in rows if r["unescapedDotOutsideClass"]),
        "hasDotStarCount": sum(1 for r in rows if r["hasDotStar"]),
        "hasLookaheadCount": sum(1 for r in rows if r["hasLookahead"]),
        "firstRbracketClassCount": sum(1 for r in rows if r["firstRbracketClass"]),
        "unanchoredCount": sum(1 for r in rows if not r["anchoredCaret"]),
        "profileStanding": profile["standing"],
        "profilePatternCount": len(profile["patterns"]),
        "profileOnlyPatterns": profile_only,
        "censusNotInProfile": census_only,
        "profileAdapterEquivalentCount": sum(1 for r in rows if r["profileAdapterEquivalentNewlineClass"]),
        "identityPinsMatchLive": all(r["equal"] for r in identity_live),
        "identityLiveRows": identity_live,
        "liveHasDescriptorsRs": descriptors_live,
        "regressChecksum": regress_checksum,
        "regressDefaultFeatures": ["backend-pikevm", "std"],
        "trialFeatures": {"defaultFeatures": False, "features": ["std", "prohibit-unsafe"]},
        "identityNoStd": True,
        "identityForbidUnsafe": True,
        "identityMaxBytes": 4 * 1024 * 1024,
        "jsonschemaPatternUsesReSearch": True,
        "jsonschemaVersionPinnedInWheels": "4.25.1",
        "proposedPatternProfilePin": pin(LIVE / "tools/contracts/runtime/pattern-profile.json"),
        "frozen": {
            "t1Subject": pin(T1 / "subject.json"),
            "t1Archive": pin(T1 / "subject.tar.gz"),
            "t1Result": pin(T1 / "result.json"),
            "t1Census": pin(T1 / "pattern-census.json"),
            "t1Mismatches": pin(T1 / "mismatches.json"),
            "t1Run": pin(T1 / "run-trial.py"),
            "t2Subject": pin(T2 / "subject.json"),
            "t2Archive": pin(T2 / "subject.tar.gz"),
            "t2Result": pin(T2 / "result.json"),
            "t2Adaptations": pin(T2 / "adaptations.json"),
            "t2Run": pin(T2 / "run-trial.py"),
        },
        "originalsExist": {"trial01": ORIG1.is_dir(), "trial02": ORIG2.is_dir()},
        "rows": rows,
    }
    dest = REVIEW / "results" / "classification.json"
    dest.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    summary = {
        "patterns": len(patterns),
        "sources": len(census["sources"]),
        "registry": len(registry["sources"]),
        "kinds": out["kinds"],
        "rewritten": out["rewrittenCount"],
        "profileOnly": profile_only,
        "censusNotInProfile": census_only,
        "identityMatch": out["identityPinsMatchLive"],
        "descriptors": descriptors_live,
        "regressChecksum": regress_checksum,
        "unanchored": [r["pattern"] for r in rows if not r["anchoredCaret"]],
        "dollar": [r["pattern"] for r in rows if r["unescapedDollarOutsideClass"]],
        "dots": [r["pattern"] for r in rows if r["unescapedDotOutsideClass"]],
        "dotStar": [r["pattern"] for r in rows if r["hasDotStar"]],
        "cargo": cargo_v,
        "rustc": rustc_v,
        "python": py_v,
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
