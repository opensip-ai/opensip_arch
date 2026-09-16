"""Bounded schema-engine-03 probes. No 26540 corpus replay."""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REVIEW = Path("/tmp/opensip-implementation/m2-grok-schema-registry-review-03/review")
CARGO = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
SAFE_PATH = "/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin:/usr/sbin:/sbin"
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
LIVE = Path("/Users/sb/code/opensip-ai/opensip")


def env_for(target: Path) -> dict[str, str]:
    env = {
        "HOME": os.environ["HOME"],
        "PATH": SAFE_PATH,
        "CARGO_TARGET_DIR": str(target),
        "CARGO_TERM_COLOR": "never",
        "CARGO_HOME": os.environ.get("CARGO_HOME", str(Path.home() / ".cargo")),
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
    return subprocess.run(cmd, env=env_for(target), cwd=str(manifest.parent), capture_output=True, timeout=180)


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("need isolated python")
    probe = REVIEW / "copy" / "probe"
    target = REVIEW / "probes" / "probe-target"
    logs = REVIEW / "results"
    logs.mkdir(exist_ok=True)
    cargo_out = {}
    for name, args in [
        ("fmt", ["fmt", "--check"]),
        ("clippy", ["clippy", "--locked", "--offline", "--all-targets", "--", "-D", "warnings"]),
        ("test", ["test", "--locked", "--offline"]),
        ("build", ["build", "--locked", "--offline", "--bins"]),
    ]:
        r = cargo(args, target, probe / "Cargo.toml")
        (logs / f"{name}.stdout").write_bytes(r.stdout)
        (logs / f"{name}.stderr").write_bytes(r.stderr)
        cargo_out[name] = {"exit": r.returncode, "tail": r.stderr.decode()[-800:]}
        if r.returncode != 0:
            raise SystemExit(name + " failed\n" + r.stderr.decode()[-2500:])

    cons = REVIEW / "probes" / "consumer"
    (cons / "src").mkdir(parents=True, exist_ok=True)
    (cons / "Cargo.toml").write_text(
        "[workspace]\n[package]\nname=\"schema-api-consumer03\"\nversion=\"0.0.0\"\nedition=\"2024\"\n"
        f"[dependencies]\nopensip-schema-engine-trial={{path={json.dumps(str(probe))}}}\n"
    )
    (cons / "src" / "lib.rs").write_text("use opensip_schema_engine_trial::Program;\n")
    r = cargo(["check", "--offline"], REVIEW / "probes" / "consumer-target", cons / "Cargo.toml")
    (logs / "program-export.stderr").write_bytes(r.stderr)
    program_hidden = r.returncode != 0 and (b"E0432" in r.stderr or b"unresolved import" in r.stderr or b"Program" in r.stderr)
    (cons / "src" / "lib.rs").write_text("use opensip_schema_engine_trial::RegisteredSchemas;\npub fn n()->usize{RegisteredSchemas::source_requirements().len()}\n")
    r2 = cargo(["check", "--offline"], REVIEW / "probes" / "consumer-target", cons / "Cargo.toml")
    public_ok = r2.returncode == 0

    pins_rs = (probe / "src" / "registry_pins.rs").read_text()
    pin_count = pins_rs.count("SourcePin {")
    alias_count = pins_rs.count("foundation/") + pins_rs.count("native/") + pins_rs.count("workflows/")
    # DOCUMENT_ALIASES rows
    alias_rows = len(re.findall(r'\("[^"]+",\s*"[^"]+"\)', pins_rs.split("DOCUMENT_ALIASES")[1]))
    table = (probe / "src" / "table.rs").read_text()
    kind_count = table.count("Kind::")
    entries = 0
    copy = REVIEW / "copy"
    adm = json.loads((copy / "schemas" / "admission-registry.json").read_bytes())
    for row in adm["sources"]:
        d = json.loads((copy / row["sourcePath"]).read_bytes())
        assert d["$id"] == row["schemaId"]
        assert hashlib.sha256((copy / row["sourcePath"]).read_bytes()).hexdigest() == row["sha256"]
        entries += 1 + len(d.get("$defs", {}))

    # sample new patterns vs python
    import re as pre
    samples = [
        ("^[^\u0000-\u001f\u007f-\u009f]*(?![\\s\\S])", "", True),
        ("^[^\u0000-\u001f\u007f-\u009f]*(?![\\s\\S])", "ok", True),
        ("^[^\u0000-\u001f\u007f-\u009f]*(?![\\s\\S])", "ok\n", False),
        ("^[^\u0000-\u001f\u007f-\u009f]*(?![\\s\\S])", "\x7f", False),
        ("^[^\u0000-\u001f\u007f-\u009f]+(?![\\s\\S])", "", False),
        ("^[a-z][a-z0-9-]*:[^\u0000-\u001f\u007f-\u009f]+(?![\\s\\S])", "a:b", True),
        ("^[a-z][a-z0-9-]*:[^\u0000-\u001f\u007f-\u009f]+(?![\\s\\S])", "A:b", False),
        ("^[a-z][a-z0-9-]*:[^\u0000-\u001f\u007f-\u009f]+(?![\\s\\S])", "ab", False),
        ("^[a-z][a-z0-9-]*:[^\u0000-\u001f\u007f-\u009f]+(?![\\s\\S])", "a:\n", False),
        ("^[a-z][a-z0-9-]*:[^\u0000-\u001f\u007f-\u009f]+(?![\\s\\S])", "a:\x80", False),
    ]
    sample_ok = all(bool(pre.search(p, v)) == exp for p, v, exp in samples)

    lock = json.loads((LIVE / "design-lock.json").read_bytes())
    ss = [s for s in lock["contractSuccessors"] if "source-selection-v3" in s["record"]["path"]]
    gen = json.loads((LIVE / "schemas" / "registry.json").read_bytes())
    hist_n = hashlib.sha256((ARCH / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json").read_bytes()).hexdigest()
    cur_n = hashlib.sha256((copy / "schemas/sources/native-v2.schema.json").read_bytes()).hexdigest()
    hist_p = hashlib.sha256((ARCH / "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json").read_bytes()).hexdigest()
    cur_p = hashlib.sha256((copy / "schemas/sources/policy-v2.schema.json").read_bytes()).hexdigest()

    test_stdout = (logs / "test.stdout").read_text()
    passed = len(re.findall(r"^test result: ok\. (\d+) passed", test_stdout, re.M))
    # sum passed from ok lines
    totals = [int(m) for m in re.findall(r"test result: ok\. (\d+) passed", test_stdout)]
    out = {
        "cargo": cargo_out,
        "programImportExit": r.returncode,
        "programHiddenFromPublicApi": program_hidden,
        "registeredSchemasPublicOk": public_ok,
        "sourcePinCount": pin_count,
        "aliasCount": alias_rows,
        "patternKindCount": kind_count,
        "admissionSources": len(adm["sources"]),
        "entries": entries,
        "newPatternSamplesAgreePython": sample_ok,
        "generationRegistryCount": len(gen["sources"]),
        "sourceSelectionV3InLiveLock": bool(ss),
        "sourceSelectionV3SuccessorSha": ss[0]["record"]["sha256"] if ss else None,
        "sourceSelectionV3AssentSha": ss[0]["assent"]["sha256"] if ss else None,
        "nativeCurrentSha": cur_n,
        "nativeHistoricalSha": hist_n,
        "nativeShaDiffer": cur_n != hist_n,
        "policyCurrentSha": cur_p,
        "policyHistoricalSha": hist_p,
        "policyShaDiffer": cur_p != hist_p,
        "testPassedGroups": totals,
        "testPassedSum": sum(totals),
        "didNotRunFullCorpus": True,
        "didNotReadSiblingGrokSession": True,
    }
    (logs / "probes.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: out[k] for k in out if k != "cargo"}, indent=2))
    print("cargo", {k: v["exit"] for k, v in cargo_out.items()})


if __name__ == "__main__":
    main()
