"""Bounded independent analysis of schema-pattern trials 01/02. No 74k corpus, no nested-star inputs."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
REVIEW = Path("/tmp/opensip-implementation/m2-grok-schema-pattern-trials-review-01/review")
T1 = ARCH / "docs/implementation/m2/trials/schema-pattern-01"
T2 = ARCH / "docs/implementation/m2/trials/schema-pattern-02"
ORIG1 = Path("/tmp/opensip-implementation/m2-schema-pattern-trial-01")
ORIG2 = Path("/tmp/opensip-implementation/m2-schema-pattern-trial-02")
CARGO = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
SAFE_PATH = "/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin:/usr/sbin:/sbin"


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def verify_manifest(manifest: Path, root: Path) -> dict:
    raw = manifest.read_bytes()
    data = json.loads(raw)
    mismatches = []
    skipped_target = 0
    for row in data["files"]:
        path = root / row["path"]
        if not path.is_file():
            mismatches.append(row["path"] + ":missing")
            continue
        actual = path.read_bytes()
        if len(actual) != row["bytes"] or sha256_bytes(actual) != row["sha256"]:
            mismatches.append(row["path"])
    pin = json.loads((manifest.parent / "archive-pin.json").read_bytes())
    archive = manifest.parent / "subject.tar.gz"
    ar = archive.read_bytes()
    return {
        "count": len(data["files"]),
        "sha256": sha256_bytes(raw),
        "membersMatch": not mismatches,
        "mismatches": mismatches[:20],
        "archiveMatch": sha256_bytes(ar) == pin["sha256"] and len(ar) == pin["bytes"],
        "archiveBytes": pin["bytes"],
        "skippedTargetNote": skipped_target,
    }


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
        raise ValueError("unclosed escape or class: " + pattern)
    return "".join(out)


def classify(pattern: str) -> dict:
    in_class = False
    escaped = False
    dollars = 0
    dots = 0
    for char in pattern:
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == "[":
            in_class = True
            continue
        if char == "]":
            in_class = False
            continue
        if not in_class and char == "$":
            dollars += 1
        if not in_class and char == ".":
            dots += 1
    return {"unescapedDollarOutsideClass": dollars, "unescapedDotOutsideClass": dots, "hasDotStar": ".*" in pattern}


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    (REVIEW / "results").mkdir(parents=True, exist_ok=True)
    (REVIEW / "copy").mkdir(parents=True, exist_ok=True)
    m1 = verify_manifest(T1 / "subject.json", ORIG1)
    m2 = verify_manifest(T2 / "subject.json", ORIG2)
    census = json.loads((T1 / "pattern-census.json").read_bytes())
    patterns = [r["pattern"] for r in census["patterns"]]
    claimed = json.loads((T2 / "adaptations.json").read_bytes())
    independent = {p: adapt(p) for p in patterns}
    adapt_mismatch = [p for p in patterns if independent[p] != claimed[p]]
    changed = [p for p in patterns if independent[p] != p]
    classes = {p: classify(p) for p in patterns}
    dollar_pats = [p for p, c in classes.items() if c["unescapedDollarOutsideClass"]]
    dot_pats = [p for p, c in classes.items() if c["unescapedDotOutsideClass"]]
    # Copy probe sources only (no target) for bounded rebuild.
    dest = REVIEW / "copy" / "probe"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(ORIG1 / "probe", dest, ignore=shutil.ignore_patterns("target"))
    target = REVIEW / "probes" / "probe-target"
    if target.exists():
        shutil.rmtree(target)
    env = {
        "HOME": os.environ["HOME"],
        "PATH": SAFE_PATH,
        "CARGO_TARGET_DIR": str(target),
        "CARGO_TERM_COLOR": "never",
        "CARGO_HOME": os.environ.get("CARGO_HOME", str(Path(os.environ["HOME"]) / ".cargo")),
        "TERM": "dumb",
    }
    try:
        env["SDKROOT"] = subprocess.check_output(
            ["/usr/bin/xcrun", "--sdk", "macosx", "--show-sdk-path"], text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        pass
    build = subprocess.run(
        [CARGO, "build", "--offline", "--manifest-path", str(dest / "Cargo.toml")],
        env=env, capture_output=True, timeout=180,
    )
    (REVIEW / "results" / "build.stderr").write_bytes(build.stderr)
    if build.returncode != 0:
        raise SystemExit(build.stderr.decode()[-1500:])
    exe = target / "debug" / "opensip-schema-pattern-trial"

    def probe(pattern: str, text: str) -> str:
        line = json.dumps({"pattern": pattern, "text": text}, ensure_ascii=True) + "\n"
        r = subprocess.run([str(exe)], input=line.encode(), env=env, capture_output=True, timeout=30)
        if r.returncode != 0:
            return "ERR:" + r.stderr.decode()[:200]
        return r.stdout.decode().strip()

    mismatch_texts = [".\n", "a/.\n", "a/..\n"]
    mismatch_patterns = sorted({row["pattern"] for row in json.loads((T1 / "mismatches.json").read_bytes())})
    rows = []
    for p in mismatch_patterns:
        for t in mismatch_texts:
            py = bool(re.search(p, t))
            raw = probe(p, t)
            adapted = probe(independent[p], t)
            rows.append({
                "pattern": p,
                "text": t,
                "python": py,
                "regressDirect": raw,
                "regressAdapted": adapted,
                "directAgreesPython": (raw == "1") == py,
                "adaptedAgreesPython": (adapted == "1") == py,
            })
    extras = []
    extra_texts = [".\r", ".\n\n", ".\r\n", ".\u2028", ".\u2029", "a/.\r\n", ""]
    p_dollar = r"(^|/)\.\.?(/|$)"
    for t in extra_texts:
        py = bool(re.search(p_dollar, t))
        adapted = probe(independent[p_dollar], t)
        extras.append({
            "text": t,
            "python": py,
            "adapted": adapted,
            "agree": (adapted == "1") == py,
        })
    sec = next(p for p in patterns if p.startswith("^security.repo-execution-grant.v2:"))
    grant = "security.repo-execution-grant.v2:" + "a" * 64
    wild = []
    for mid in [".", "\n", "\r", "x", "\u2028"]:
        text = "security" + mid + "repo-execution-grant" + mid + "v2:" + "a" * 64
        py = bool(re.search(sec, text))
        adapted = probe(independent[sec], text)
        wild.append({
            "mid": mid,
            "python": py,
            "adapted": adapted,
            "agree": (adapted == "1") == py,
            "literalGrantPython": bool(re.search(sec, grant)),
        })
    compile_orig = []
    compile_ad = []
    for p in patterns:
        compile_orig.append(probe(p, "") != "E")
        compile_ad.append(probe(independent[p], "") != "E")
    out = {
        "trial01Manifest": m1,
        "trial02Manifest": m2,
        "patternCount": len(patterns),
        "sourceCount": len(census["sources"]),
        "adaptIndependentEqualsArchived": not adapt_mismatch,
        "adaptMismatchCount": len(adapt_mismatch),
        "changedPatternCount": len(changed),
        "changedPatterns": changed,
        "dollarPatterns": dollar_pats,
        "unescapedDotPatterns": dot_pats,
        "trial01NineCases": rows,
        "trial01DirectDisagreeCount": sum(not r["directAgreesPython"] for r in rows),
        "trial01AdaptedAgreeCount": sum(r["adaptedAgreesPython"] for r in rows),
        "dollarExtras": extras,
        "dollarExtrasAllAgree": all(r["agree"] for r in extras),
        "securityWildcard": wild,
        "securityWildcardAllAgree": all(r["agree"] for r in wild),
        "all68OriginalCompile": all(compile_orig),
        "all68AdaptedCompile": all(compile_ad),
        "identityNoStd": True,
        "regressStdFeature": True,
        "didNotRunFullCorpus": True,
        "didNotRunCatastrophicInputs": True,
    }
    (REVIEW / "results" / "analysis.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "t1": {k: m1[k] for k in ("count", "sha256", "membersMatch", "archiveMatch")},
        "t2": {k: m2[k] for k in ("count", "sha256", "membersMatch", "archiveMatch")},
        "patterns": len(patterns),
        "sources": len(census["sources"]),
        "adaptEq": not adapt_mismatch,
        "changed": len(changed),
        "dollar": len(dollar_pats),
        "dots": len(dot_pats),
        "directDisagree": out["trial01DirectDisagreeCount"],
        "adaptedAgree9": out["trial01AdaptedAgreeCount"],
        "extrasAgree": out["dollarExtrasAllAgree"],
        "secAgree": out["securityWildcardAllAgree"],
        "compileOrig": out["all68OriginalCompile"],
        "compileAd": out["all68AdaptedCompile"],
        "extras": extras,
        "sec": wild,
    }, indent=2))


if __name__ == "__main__":
    main()
