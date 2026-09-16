"""Independent JSON-schema + segment oracle vs Rust LogicalPath public API."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

CARGO = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
REVIEW = Path("/tmp/opensip-implementation/m2-grok-logical-path-selection-v1-review/review")
COPY = REVIEW / "copy" / "frozen-subject"
LIVE_PY = Path("/Users/sb/code/opensip-ai/opensip/tools/contracts/python-packages")
SAFE_PATH = "/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin:/usr/sbin:/sbin"
SCHEMA_SHA = "311c1feb09ff8cd0b207233d2ec0d7440bb1c72fc0470de277ee1891c24bb68f"


def env_for(target: Path) -> dict[str, str]:
    env = {
        "HOME": os.environ["HOME"],
        "PATH": SAFE_PATH,
        "CARGO_TARGET_DIR": str(target),
        "CARGO_TERM_COLOR": "never",
        "CARGO_HOME": os.environ.get("CARGO_HOME", str(Path(os.environ["HOME"]) / ".cargo")),
        "TMPDIR": str(REVIEW / "probes" / "tmp"),
        "TERM": "dumb",
    }
    try:
        env["SDKROOT"] = subprocess.check_output(
            ["/usr/bin/xcrun", "--sdk", "macosx", "--show-sdk-path"], text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        pass
    return env


def schema_ok(validator, value: str) -> bool:
    return validator.is_valid(value)


def scalar_count(value: str, limit: int) -> int:
    n = 0
    for _ in value:
        n += 1
        if n > limit:
            return n
    return n


def imperative(value: str) -> bool:
    if value == "":
        return False
    if scalar_count(value, 4096) > 4096:
        return False
    if "\\" in value or "\0" in value:
        return False
    for part in value.split("/"):
        if part in ("", ".", ".."):
            return False
        if scalar_count(part, 255) > 255:
            return False
    # Python `re` `$` also matches before one final LF.
    if value.endswith("\n"):
        last = value[:-1].rsplit("/", 1)[-1]
        if last in (".", ".."):
            return False
    return True


def python_not_pattern(value: str) -> bool:
    """Selected not.pattern using Python re `$` (not ECMA-262)."""
    return re.search(r"(^|/)\.\.?(/|$)", value) is not None


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    sys.path.insert(0, str(LIVE_PY))
    import jsonschema

    schema_path = COPY / "product/schemas/sources/identity-v3.schema.json"
    raw = schema_path.read_bytes()
    import hashlib
    sha = hashlib.sha256(raw).hexdigest()
    if sha != SCHEMA_SHA:
        raise SystemExit("schema copy sha mismatch " + sha)
    schema = json.loads(raw)
    logical = {
        "$schema": schema["$schema"],
        **schema["$defs"]["LogicalPath"],
    }
    validator = jsonschema.Draft202012Validator(logical)

    cases_path = COPY / "oracle-input.jsonl"
    values = []
    for line in cases_path.read_text().splitlines():
        values.append(json.loads(line))

    target = REVIEW / "probes" / "probe-target"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    env = env_for(target)
    build = subprocess.run(
        [CARGO, "build", "--locked", "--offline"],
        env=env, cwd=COPY / "probe", capture_output=True, timeout=180,
    )
    (REVIEW / "results" / "logs").mkdir(parents=True, exist_ok=True)
    (REVIEW / "results" / "logs" / "oracle-build.stderr").write_bytes(build.stderr)
    if build.returncode != 0:
        raise SystemExit(build.stderr.decode()[-800:])
    exe = target / "debug" / "opensip-logical-path-probe"
    payload = cases_path.read_bytes()
    rust = subprocess.run(
        [str(exe)], input=payload, env=env, capture_output=True, timeout=60,
    )
    if rust.returncode != 0:
        raise SystemExit("probe failed: " + rust.stderr.decode()[-800:])
    rust_bits = [line.strip() for line in rust.stdout.decode().splitlines() if line.strip() != ""]
    if len(rust_bits) != len(values):
        raise SystemExit(f"rust rows {len(rust_bits)} != cases {len(values)}")

    mismatches = []
    schema_vs_rust = []
    imperative_vs_rust = []
    not_pattern_vs_rust = []
    for i, value in enumerate(values):
        rust_ok = rust_bits[i] == "1"
        js_ok = schema_ok(validator, value)
        imp_ok = imperative(value)
        if rust_ok != js_ok:
            schema_vs_rust.append({"i": i, "value": value, "rust": rust_ok, "jsonschema": js_ok})
        if rust_ok != imp_ok:
            imperative_vs_rust.append({"i": i, "value": value, "rust": rust_ok, "imperative": imp_ok})
        if (not python_not_pattern(value)) != rust_ok and value not in ("",) and "\\" not in value and "\0" not in value:
            # only note when not-pattern is the interesting axis; skip empty/backslash already refused
            pass
        if rust_ok != js_ok or rust_ok != imp_ok:
            mismatches.append({"i": i, "value": value, "rust": rust_ok, "jsonschema": js_ok, "imperative": imp_ok})

    extras = []

    def check(name, value, expect_ok):
        rust_one = subprocess.run(
            [str(exe)],
            input=(json.dumps(value) + "\n").encode(),
            env=env, capture_output=True, timeout=30,
        )
        rust_ok = rust_one.stdout.decode().strip() == "1"
        js_ok = schema_ok(validator, value)
        extras.append({
            "name": name,
            "value": value,
            "expectOk": expect_ok,
            "rust": rust_ok,
            "jsonschema": js_ok,
            "imperative": imperative(value),
            "agree": rust_ok == expect_ok == js_ok == imperative(value),
        })

    check("empty", "", False)
    check("dot-scope-root", ".", False)
    check("dotdot", "..", False)
    check("absolute", "/a", False)
    check("trailing-slash", "a/", False)
    check("empty-segment", "a//b", False)
    check("backslash", "a\\b", False)
    check("nul", "a\0b", False)
    check("final-lf-dot", ".\n", False)
    check("final-lf-dotdot", "..\n", False)
    check("nested-final-lf-dot", "a/.\n", False)
    check("double-final-lf", ".\n\n", True)
    check("crlf-dot", "a/.\r\n", True)
    check("ls-dot", ".\u2028", True)
    check("newline-filename", "a\nb/c", True)
    check("space-and-colon", " a ", True)
    check("colon", "a:b", True)
    check("ellipsis", "...", True)
    check("emoji-255", "😀" * 255, True)
    check("emoji-256", "😀" * 256, False)
    check("nfc", "é/file", True)
    check("nfd", "e\u0301/file", True)
    check("src-lib", "src/lib.rs", True)
    # fingerprint/scope would allow '.' ; this primitive must not
    check("scope-dot-must-refuse", ".", False)

    out = {
        "schemaSha256": sha,
        "schemaSelector": "#/$defs/LogicalPath",
        "jsonschemaVersion": getattr(jsonschema, "__version__", "unknown"),
        "cases": len(values),
        "rustRows": len(rust_bits),
        "mismatches": mismatches[:20],
        "mismatchCount": len(mismatches),
        "schemaVsRustCount": len(schema_vs_rust),
        "imperativeVsRustCount": len(imperative_vs_rust),
        "schemaVsRustSample": schema_vs_rust[:10],
        "imperativeVsRustSample": imperative_vs_rust[:10],
        "counterexamples": extras,
        "counterexamplesAllAgree": all(row["agree"] for row in extras),
        "probeNotInstalled": True,
    }
    (REVIEW / "results" / "oracle.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "cases": len(values),
        "mismatchCount": len(mismatches),
        "schemaVsRust": len(schema_vs_rust),
        "imperativeVsRust": len(imperative_vs_rust),
        "jsonschemaVersion": out["jsonschemaVersion"],
        "counterexamplesAllAgree": out["counterexamplesAllAgree"],
        "counterFail": [r["name"] for r in extras if not r["agree"]],
        "sampleMismatch": mismatches[:5],
    }, indent=2))


if __name__ == "__main__":
    main()
