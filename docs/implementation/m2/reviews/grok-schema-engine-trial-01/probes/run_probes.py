"""Bounded schema-engine probes. No 486986 corpus. No nested-star inputs."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

REVIEW = Path("/tmp/opensip-implementation/m2-grok-schema-engine-trial-review-01/review")
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
CARGO = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
SAFE_PATH = "/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin:/usr/sbin:/sbin"
CANON = ARCH / "docs/coop/design-corrections/foundation/canonical.py"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def env_for(target: Path) -> dict[str, str]:
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


def cargo(args: list[str], target: Path, manifest: Path) -> subprocess.CompletedProcess[bytes]:
    cmd = [CARGO, args[0], "--manifest-path", str(manifest), *args[1:]]
    return subprocess.run(
        cmd,
        env=env_for(target),
        cwd=str(manifest.parent),
        capture_output=True,
        timeout=180,
    )


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    import importlib.util

    spec = importlib.util.spec_from_file_location("reference_canonical", CANON)
    ref = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ref)
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource

    probe = REVIEW / "copy" / "probe"
    target = REVIEW / "probes" / "target"
    manifest = probe / "Cargo.toml"
    logs = REVIEW / "results"
    logs.mkdir(parents=True, exist_ok=True)
    results = {}
    for name, args in [
        ("fmt", ["fmt", "--check"]),
        ("clippy", ["clippy", "--locked", "--offline", "--all-targets", "--", "-D", "warnings"]),
        ("test", ["test", "--locked", "--offline"]),
        ("build", ["build", "--locked", "--offline"]),
    ]:
        r = cargo(args, target, manifest)
        (logs / f"{name}.stdout").write_bytes(r.stdout)
        (logs / f"{name}.stderr").write_bytes(r.stderr)
        results[name] = {"exit": r.returncode, "stderrTail": r.stderr.decode()[-800:]}
        if r.returncode != 0:
            raise SystemExit(name + " failed\n" + r.stderr.decode()[-2000:])

    exe = target / "debug" / "opensip-schema-engine-trial"
    dialect = "https://json-schema.org/draft/2020-12/schema"

    def run_program(documents: list[dict], entries: list[str], cases: list[dict], compile_budget=1_000_000):
        init = json.dumps({"documents": documents, "entries": entries}, separators=(",", ":"))
        payload = [init]
        for c in cases:
            payload.append(json.dumps(c, separators=(",", ":")))
        raw = ("\n".join(payload) + "\n").encode()
        r = subprocess.run(
            [str(exe)],
            input=raw,
            env=env_for(target),
            capture_output=True,
            timeout=30,
        )
        if r.returncode != 0:
            return {"exit": r.returncode, "stderr": r.stderr.decode()[:500], "lines": []}
        lines = r.stdout.decode().splitlines()
        return {"exit": 0, "lines": lines}

    def doc(body: dict, ident="urn:probe") -> dict:
        return {"$id": ident, "$schema": dialect, **body}

    rows = []

    def add(name, body, value, expect, entry="urn:probe#"):
        documents = [doc(body)]
        out = run_program(documents, [entry], [{"ref": entry, "value": value, "budget": 10000}])
        rust = out["lines"][1] if len(out["lines"]) > 1 else out["lines"][0] if out["lines"] else "NO"
        py_ok = None
        py_err = None
        try:
            refmod = Registry().with_resources(
                [(d["$id"], Resource.from_contents(d)) for d in documents]
            )
            ref.ExactValidator({"$ref": entry}, registry=refmod).validate(value)
            py_ok = True
        except Exception as e:
            py_err = type(e).__name__
            py_ok = False
        rows.append(
            {
                "name": name,
                "rust": rust,
                "pythonExactAdmitted": py_ok,
                "pythonErr": py_err,
                "expect": expect,
                "agreeExpect": rust == expect,
            }
        )

    add("const-int-admits-1", {"const": 1}, 1, "1")
    add("const-int-refuses-true", {"const": 1}, True, "0")
    add("const-int-refuses-false", {"const": 1}, False, "0")
    add("type-integer-refuses-true", {"type": "integer"}, True, "0")
    add("type-boolean-admits-true", {"type": "boolean"}, True, "1")
    add("prefix-items-and-tail-string", {"type": "array", "prefixItems": [{"const": 0}, {"type": "boolean"}], "items": {"type": "string"}}, [0, False, "a"], "1")
    add("prefix-items-tail-wrong-type", {"type": "array", "prefixItems": [{"const": 0}, {"type": "boolean"}], "items": {"type": "string"}}, [0, False, 1], "0")
    add("prefix-items-false-extra", {"prefixItems": [True], "items": False}, [0, 1], "0")
    add("prefix-items-false-exact", {"prefixItems": [True], "items": False}, [0], "1")
    add("unique-true-and-one", {"uniqueItems": True}, [True, 1], "1")
    add("unique-key-order", {"uniqueItems": True}, [{"a": 1, "b": 2}, {"b": 2, "a": 1}], "0")
    add("numeric-order-true-not-int", {"x-opensip-order": "numeric"}, [1, True], "0")
    add("caret-dot-plus-a", {"pattern": "^.+$"}, "a", "1")
    add("caret-dot-plus-a-lf", {"pattern": "^.+$"}, "a\n", "1")
    add("caret-dot-plus-cr", {"pattern": "^.+$"}, "\r", "1")
    add("caret-dot-plus-only-lf", {"pattern": "^.+$"}, "\n", "0")
    add("caret-dot-plus-internal-lf", {"pattern": "^.+$"}, "a\nb", "0")
    add("xmaxutf8-ignored-emoji", {"type": "string", "maxLength": 1, "x-maxUtf8Bytes": 1}, "😀", "1")
    add("pattern-props-cr-key", {"patternProperties": {"^.+$": {"type": "integer"}}, "additionalProperties": False}, {"a\r": 1}, "1")
    add("pattern-props-empty-key", {"patternProperties": {"^.+$": {"type": "integer"}}, "additionalProperties": False}, {"": 1}, "0")

    # compile-time refusals
    compile_cases = []
    for name, body in [
        ("unknown-keyword", {"unknown": True}),
        ("type-number", {"type": "number"}),
        ("unselected-pattern", {"pattern": ".*"}),
        ("empty-allOf", {"allOf": []}),
        ("bad-order", {"x-opensip-order": "unknown"}),
        ("array-pointer", {"$ref": "#/0"}),
        ("percent-fragment", {"$ref": "#/%61"}),
        ("tilde-2", {"$ref": "#/~2"}),
    ]:
        out = run_program([doc(body)], ["urn:probe#"], [])
        compile_cases.append({"name": name, "lines": out["lines"], "refused": out["lines"] and out["lines"][0].startswith("COMPILE:")})

    # unselected entry
    out = run_program([doc({"type": "null"})], ["urn:probe#"], [{"ref": "urn:probe", "value": None, "budget": 1000}])
    unselected = {"lines": out["lines"], "isUnselected": any("UnselectedEntry" in x for x in out["lines"])}

    # cyclic limit
    cyclic = []
    for body in [
        {"not": {"$ref": "#"}},
        {"anyOf": [{"$ref": "#"}, True]},
        {"if": {"$ref": "#"}, "else": True},
    ]:
        out = run_program([doc(body)], ["urn:probe#"], [{"ref": "urn:probe#", "value": 0, "budget": 1_000_000}])
        cyclic.append({"body": body, "lines": out["lines"], "isLimit": any("Limit" in x for x in out["lines"])})

    # budget 0 is Limit not false
    out = run_program([doc({"const": 1})], ["urn:probe#"], [{"ref": "urn:probe#", "value": 1, "budget": 0}])
    budget0 = {"lines": out["lines"], "isLimit": any("Limit" in x for x in out["lines"])}

    # -0 is JSON fault
    # send through matches_json with raw... binary uses canonical_bytes of parsed value so -0 cannot be represented in Python True JSON number after parse. Skip if Python json won't emit -0.
    minus = {"note": "identity parse of -0 is Json; covered by crate test"}

    # duplicate $id
    d = doc({"type": "null"})
    out = run_program([d, dict(d)], ["urn:probe#"], [])
    dup = {"lines": out["lines"], "refused": out["lines"] and out["lines"][0].startswith("COMPILE:")}

    # 40 source pin vs included selected-sources
    pins = json.loads((REVIEW / "copy" / "schema-source-pins.json").read_bytes())
    pin_ok = []
    for row in pins:
        p = REVIEW / "copy" / "selected-sources" / row["path"]
        b = p.read_bytes()
        pin_ok.append(len(b) == row["bytes"] and sha(p) == row["sha256"])

    census = json.loads((REVIEW / "copy" / "complete-pattern-census.json").read_bytes())
    patterns = [r["pattern"] if isinstance(r, dict) else r for r in census["patterns"]]

    out = {
        "cargo": results,
        "identityPathRewritten": True,
        "didNotUseLiveIdentity": True,
        "didNotRunFullCorpus": True,
        "rows": rows,
        "rowDisagree": [r for r in rows if not r["agreeExpect"]],
        "compileRefusals": compile_cases,
        "compileAllRefused": all(c["refused"] for c in compile_cases),
        "unselectedEntry": unselected,
        "cyclicLimit": cyclic,
        "cyclicAllLimit": all(c["isLimit"] for c in cyclic),
        "budgetZeroIsLimit": budget0,
        "duplicateIdRefused": dup,
        "schemaSourcePinsOk": all(pin_ok),
        "schemaSourceCount": len(pins),
        "censusPatternCount": len(patterns),
        "censusHasCaretDotPlus": "^.+$" in patterns,
        "minusZero": minus,
        "draft202012Available": Draft202012Validator is not None,
    }
    (logs / "probes.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "cargoExits": {k: v["exit"] for k, v in results.items()},
        "rows": len(rows),
        "disagree": out["rowDisagree"],
        "compileAllRefused": out["compileAllRefused"],
        "compile": [{k: c[k] for k in ("name", "refused", "lines")} for c in compile_cases],
        "unselected": unselected,
        "cyclicAllLimit": out["cyclicAllLimit"],
        "cyclic": cyclic,
        "budget0": budget0,
        "dup": dup,
        "pins": len(pins),
        "census": len(patterns),
        "caret": "^.+$" in patterns,
    }, indent=2))


if __name__ == "__main__":
    main()
