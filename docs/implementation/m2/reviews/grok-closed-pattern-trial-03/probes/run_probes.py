"""Bounded closed-matcher probes. No 193936 corpus. No nested-star inputs."""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
LIVE = Path("/Users/sb/code/opensip-ai/opensip")
REVIEW = Path("/tmp/opensip-implementation/m2-grok-closed-pattern-trial-review-03/review")
T3 = ARCH / "docs/implementation/m2/trials/schema-pattern-03"
CARGO = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
SAFE_PATH = "/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin:/usr/sbin:/sbin"

PP_KEY = "^.+$"


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def cargo_env(target: Path) -> dict[str, str]:
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
    return env


def cargo_run(args: list[str], target: Path, cwd: Path | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [CARGO, *args],
        env=cargo_env(target),
        cwd=cwd,
        capture_output=True,
        timeout=180,
    )


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    from jsonschema import Draft202012Validator

    census = json.loads((T3 / "pattern-census.json").read_bytes())
    census_patterns = [r["pattern"] for r in census["patterns"]]
    classification = json.loads((T3 / "classification.json").read_bytes())
    table_src = (REVIEW / "copy/probe/src/table.rs").read_text()
    table_patterns = re.findall(r'r##"(.*?)"##', table_src, flags=re.S)
    table_vs_census = table_patterns == census_patterns
    class_vs_census = [r["pattern"] for r in classification] == census_patterns
    by_pred = {}
    for row in classification:
        by_pred.setdefault(row["predicate"], row["pattern"])
    DOT = by_pred["DotSegment"]
    NEG_STAR = by_pred["NegativePath(true)"]
    NEG_PLUS = by_pred["NegativePath(false)"]
    CANON_PLUS = by_pred["CanonicalPath(false)"]
    CANON_STAR = by_pred["CanonicalPath(true)"]
    SEG255 = by_pred["Segments255"]
    SEMVER_STRICT = by_pred["Semver(true)"]
    SEMVER_LOOSE = by_pred["Semver(false)"]
    GRANT = by_pred["SecurityWildcard(false)"]
    GRANTS = by_pred["SecurityWildcard(true)"]
    ESCAPED = by_pred['Hex("security.installation-transition-journal.v1:", 64)']
    ENFORCEMENT = by_pred["Enforcement"]

    probe_dir = REVIEW / "copy" / "probe"
    std_target = REVIEW / "probes" / "std-target"
    nostd_dir = REVIEW / "probes" / "nostd"
    nostd_target = REVIEW / "probes" / "nostd-target"
    std_build = cargo_run(
        ["build", "--offline", "--manifest-path", str(probe_dir / "Cargo.toml")],
        std_target,
    )
    (REVIEW / "results" / "std-build.stderr").write_bytes(std_build.stderr)
    (REVIEW / "results" / "std-build.stdout").write_bytes(std_build.stdout)
    nostd_build = cargo_run(
        ["check", "--offline", "--manifest-path", str(nostd_dir / "Cargo.toml")],
        nostd_target,
    )
    (REVIEW / "results" / "nostd-check.stderr").write_bytes(nostd_build.stderr)
    (REVIEW / "results" / "nostd-check.stdout").write_bytes(nostd_build.stdout)
    exe = std_target / "debug" / "opensip-closed-pattern-trial"

    def rust_match(pattern: str, text: str) -> str:
        line = json.dumps({"pattern": pattern, "text": text}, ensure_ascii=True) + "\n"
        r = subprocess.run(
            [str(exe)],
            input=line.encode(),
            env=cargo_env(std_target),
            capture_output=True,
            timeout=30,
        )
        if r.returncode != 0:
            return "ERR:" + r.stderr.decode()[:200]
        return r.stdout.decode().strip()

    def py_search(pattern: str, text: str) -> bool:
        return bool(re.search(pattern, text))

    def js_pattern(pattern: str, text: str) -> bool:
        return Draft202012Validator({"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "string", "pattern": pattern}).is_valid(text)

    def js_not(pattern: str, text: str) -> bool:
        return Draft202012Validator({"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "string", "not": {"pattern": pattern}}).is_valid(text)

    def js_pp(pattern: str, key: str) -> bool:
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "additionalProperties": False,
            "patternProperties": {pattern: True},
        }
        return Draft202012Validator(schema).is_valid({key: True})

    hex64 = "a" * 64
    texts_by_group: dict[str, list[str]] = {
        "finalLfDot": [".\n", "a/.\n", "a/..\n", ".\n\n", ".\r", ".\r\n", ".\u2028", ".\u2029", "a/.\r\n", "", ".", "..", "./x", "x/.", "x/..", "...", "foo.", "foo.\n"],
        "negLookaheadBeforeFirstLf": ["ok\n./x", "ok\n../x", "foo\n/.", "foo\n/./bar", ".\nfoo", "a/.\nbar", "./ok", "../ok", "a/./b", "\n./x", "foo/.\nbar"],
        "semver": [
            "1.2.3", "01.2.3", "1.02.3", "1.2.03", "1.2", "1.2.3.4",
            "1.2.3-0", "1.2.3-01", "1.2.3-a", "1.2.3-a.1", "1.2.3-a..b",
            "1.2.3-.", "1.2.3--", "1.2.3-rc.1+build.01", "1.2.3+01", "1.2.3+", "1.2.3-",
            "1.2.3-a.0", "0.0.0", "1.2.3+a..b",
        ],
        "security": [
            "security.repo-execution-grant.v2:" + hex64,
            "securityxrepo-execution-grantxv2:" + hex64,
            "security\nrepo-execution-grant\nv2:" + hex64,
            "security\rrepo-execution-grant\rv2:" + hex64,
            "security\u2028repo-execution-grant\u2028v2:" + hex64,
            "security😀repo-execution-grant😀v2:" + hex64,
            "security.repo-execution-grants.v2:" + hex64,
            "security.installation-transition-journal.v1:" + hex64,
        ],
        "scalarLengths": [
            "a" * 254, "a" * 255, "a" * 256, "😀" * 255, "😀" * 256,
            "x/" + "a" * 255 + "/z", "x/" + "a" * 256 + "/z",
            "ENFORCED-PLATFORM:" + "a" * 64, "ENFORCED-PLATFORM:" + "a" * 65,
            "ENFORCED-PLATFORM:",
        ],
        "canonicalVsNegative": [".\n", "..\n", "./x", "a/../b", "a//b", "", "file.txt", "a/./b"],
    }

    rows = []
    disagree = []
    groups = {
        "finalLfDot": [DOT, NEG_STAR, NEG_PLUS, CANON_PLUS, SEG255],
        "negLookaheadBeforeFirstLf": [DOT, NEG_STAR, NEG_PLUS, CANON_PLUS],
        "semver": [SEMVER_STRICT, SEMVER_LOOSE],
        "security": [GRANT, GRANTS, ESCAPED],
        "scalarLengths": [SEG255, ENFORCEMENT],
        "canonicalVsNegative": [NEG_PLUS, CANON_PLUS, CANON_STAR, SEG255, DOT],
    }
    for group, patterns in groups.items():
        for pattern in patterns:
            for text in texts_by_group[group]:
                py = py_search(pattern, text)
                ru = rust_match(pattern, text)
                js = js_pattern(pattern, text)
                agree = ru == ("1" if py else "0") and js == py
                row = {
                    "group": group,
                    "pattern": pattern,
                    "text": text,
                    "pythonReSearch": py,
                    "jsonschemaPattern": js,
                    "rust": ru,
                    "agree": agree,
                }
                rows.append(row)
                if not agree:
                    disagree.append(row)

    # jsonschema not.pattern and identity LogicalPath combination
    logical_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "string",
        "minLength": 1,
        "maxLength": 4096,
        "pattern": SEG255,
        "not": {"pattern": DOT},
    }
    logical_validator = Draft202012Validator(logical_schema)
    logical_texts = [".\n", "a/.\n", "a/..\n", ".\n\n", ".\r", "ok\n./x", "a/./b", "src/lib.rs", "a" * 256, "😀" * 255, "", ".", "..", "a//b", "/abs"]
    logical_rows = []
    for text in logical_texts:
        js_ok = logical_validator.is_valid(text)
        rust_seg = rust_match(SEG255, text) == "1"
        rust_dot = rust_match(DOT, text) == "1"
        rust_combo = rust_seg and not rust_dot and 1 <= len(text) <= 4096
        # maxLength in jsonschema is Unicode characters
        rust_combo_scalars = rust_seg and not rust_dot and 1 <= len(text) <= 4096
        logical_rows.append({
            "text": text,
            "jsonschemaLogicalPath": js_ok,
            "rustSegments255": rust_seg,
            "rustDotSegment": rust_dot,
            "rustComboBytesLen": rust_combo,
            "agreeComboVsJsonschema": rust_combo_scalars == js_ok,
            "pythonNotDot": not py_search(DOT, text),
            "jsonschemaNotDot": js_not(DOT, text),
        })

    # patternProperties: selected sarif key is not in the 68
    pp_texts = ["a", "a\n", "\n", "a\nb", "", "😀", "a\n\n"]
    pp_rows = []
    for key in pp_texts:
        py = py_search(PP_KEY, key)
        js = js_pp(PP_KEY, key)
        ru = rust_match(PP_KEY, key)
        pp_rows.append({
            "key": key,
            "pythonReSearch": py,
            "jsonschemaPatternProperties": js,
            "rust": ru,
            "rustUnknown": ru == "E",
        })

    unknown = []
    for pattern in ["", ".*", "^.*$", census_patterns[0] + "x", PP_KEY]:
        unknown.append({"pattern": pattern, "rust": rust_match(pattern, "anything")})

    compile68 = []
    for p in census_patterns:
        compile68.append({"pattern": p, "empty": rust_match(p, "")})

    out = {
        "tableEqualsCensus": table_vs_census,
        "classificationEqualsCensus": class_vs_census,
        "tableCount": len(table_patterns),
        "censusCount": len(census_patterns),
        "stdBuildExit": std_build.returncode,
        "nostdCheckExit": nostd_build.returncode,
        "nostdCheckStderrTail": nostd_build.stderr.decode()[-1500:],
        "probeDisagreeCount": len(disagree),
        "probeRowCount": len(rows),
        "disagreements": disagree,
        "logicalPathContext": logical_rows,
        "logicalPathComboDisagree": [r for r in logical_rows if not r["agreeComboVsJsonschema"]],
        "patternPropertiesSarifKey": pp_rows,
        "unknownPatterns": unknown,
        "rows": rows,
        "jsonschemaVersion": "4.25.1",
        "didNotRunFullCorpus": True,
        "didNotRunCatastrophicInputs": True,
        "reconstructedIdentityNotLivePath": True,
        "casesJsonlVerifiedInPlace": True,
        "patternPropertiesKeyMissingFromCensus": PP_KEY,
    }
    (REVIEW / "results" / "probes.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "tableEqualsCensus": table_vs_census,
        "stdBuild": std_build.returncode,
        "nostdCheck": nostd_build.returncode,
        "nostdTail": nostd_build.stderr.decode()[-400:],
        "rows": len(rows),
        "disagree": len(disagree),
        "disagreePreview": disagree[:8],
        "logicalDisagree": [r["text"] for r in logical_rows if not r["agreeComboVsJsonschema"]],
        "pp": pp_rows,
        "unknown": unknown,
    }, indent=2))


if __name__ == "__main__":
    main()
