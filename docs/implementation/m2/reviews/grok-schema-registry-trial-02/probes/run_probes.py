"""Bounded owning-registry probes. No 486986/487156 corpus replay."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

REVIEW = Path("/tmp/opensip-implementation/m2-grok-schema-registry-trial-review-02/review")
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
    return subprocess.run(cmd, env=env_for(target), cwd=str(manifest.parent), capture_output=True, timeout=180)


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    import importlib.util
    from jsonschema import validators
    from referencing import Registry, Resource
    from attrs import fields

    spec = importlib.util.spec_from_file_location("canonical_oracle", CANON)
    ref = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ref)

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
        cargo_out[name] = {"exit": r.returncode, "tail": r.stderr.decode()[-600:]}
        if r.returncode != 0:
            raise SystemExit(name + " failed\n" + r.stderr.decode()[-2500:])

    consumer = REVIEW / "copy" / "consumer-probe"
    cons_target = REVIEW / "probes" / "consumer-target"
    pos = 'use opensip_schema_engine_trial::RegisteredSchemas;\npub fn requirements()->usize { RegisteredSchemas::source_requirements().len() }\n'
    neg = (consumer / "src" / "lib.rs").read_text()
    consumer_probes = []
    for name, src, ok in [("public-reader", pos, True), ("private-authority-forgery", neg, False)]:
        (consumer / "src" / "lib.rs").write_text(src)
        r = cargo(["check", "--offline", "--locked"], cons_target, consumer / "Cargo.toml")
        (logs / f"{name}.stderr").write_bytes(r.stderr)
        (logs / f"{name}.stdout").write_bytes(r.stdout)
        e0451 = b"E0451" in r.stderr and b"private" in r.stderr
        consumer_probes.append({
            "name": name,
            "exit": r.returncode,
            "expectedSuccess": ok,
            "ok": (r.returncode == 0) == ok,
            "e0451": e0451,
        })
        if ok and r.returncode != 0:
            raise SystemExit("public-reader failed\n" + r.stderr.decode()[-1500:])
        if not ok and not (r.returncode != 0 and e0451):
            raise SystemExit("expected E0451\n" + r.stderr.decode()[-1500:])
    (consumer / "src" / "lib.rs").write_text(neg)

    # pin table vs selected-sources
    pins = json.loads((REVIEW / "copy" / "registry-pins.json").read_bytes())
    schema_pins = json.loads((REVIEW / "copy" / "schema-source-pins.json").read_bytes())
    rs = (REVIEW / "copy" / "probe" / "src" / "registry_pins.rs").read_text()
    pin_rows = []
    for row in pins:
        p = REVIEW / "copy" / "selected-sources" / row["path"]
        b = p.read_bytes()
        digest = hashlib.sha256(b).digest()
        hexd = hashlib.sha256(b).hexdigest()
        doc = json.loads(b)
        pin_rows.append({
            "path": row["path"],
            "idMatch": doc["$id"] == row["id"],
            "bytesMatch": len(b) == row["bytes"],
            "shaMatch": hexd == row["sha256"],
            "rsHasId": json.dumps(row["id"]) in rs,
            "fileSha": hexd,
        })
    schema_pin_shas = {r["path"]: r["sha256"] for r in schema_pins}
    pins_eq_schema = all(schema_pin_shas[r["path"]] == r["sha256"] for r in pins)

    entries = 0
    for row in pins:
        d = json.loads((REVIEW / "copy" / "selected-sources" / row["path"]).read_bytes())
        entries += 1 + len(d.get("$defs", {}))

    # proposed oracle adapter control only
    Stable = validators.extend(ref.ExactValidator)

    def evolve(self, **changes):
        for f in fields(self.__class__):
            if f.init:
                changes.setdefault(f.alias, getattr(self, f.name))
        return self.__class__(**changes)

    Stable.evolve = evolve
    dialect = "https://json-schema.org/draft/2020-12/schema"
    doc = {"$id": "urn:exact-order:0", "$schema": dialect, "x-opensip-order": "numeric"}
    value = [1, True]
    reg = Registry().with_resources([(doc["$id"], Resource.from_contents(doc))])
    control = {
        "directExact": ref.ExactValidator(doc, registry=reg).is_valid(value),
        "refWrappedExact": ref.ExactValidator({"$ref": doc["$id"] + "#"}, registry=reg).is_valid(value),
        "profileStableRef": Stable({"$ref": doc["$id"] + "#"}, registry=reg).is_valid(value),
        "stableClassName": Stable.__name__,
        "exactClassName": ref.ExactValidator.__name__,
    }

    frozen01 = json.loads((REVIEW / "copy" / "previous-trial.json").read_bytes())
    out = {
        "cargo": cargo_out,
        "consumerProbes": consumer_probes,
        "pinCount": len(pins),
        "pinRowsAllMatch": all(r["idMatch"] and r["bytesMatch"] and r["shaMatch"] and r["rsHasId"] for r in pin_rows),
        "pinsMatchSchemaSourcePins": pins_eq_schema,
        "rootPlusDirectDefs": entries,
        "control": control,
        "controlExpected": control["directExact"] is False and control["refWrappedExact"] is True and control["profileStableRef"] is False,
        "frozen01SubjectSha": frozen01["manifest"]["sha256"],
        "frozen01Unchanged": frozen01["manifest"]["sha256"] == "b5dfe136de8e3fb3bb986252a7240f1fd65fbbad4b2c7b09db062e60f30475b6",
        "identityPathRewritten": True,
        "consumerPathRewritten": True,
        "didNotUseLiveIdentity": True,
        "didNotRunFullCorpus": True,
        "didNotReadSiblingNormativeSession": True,
        "census69": json.loads((REVIEW / "copy" / "complete-pattern-census.json").read_bytes())["standing"],
    }
    (logs / "probes.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "cargo": {k: v["exit"] for k, v in cargo_out.items()},
        "consumer": consumer_probes,
        "pins": len(pins),
        "pinOk": out["pinRowsAllMatch"],
        "entries": entries,
        "control": control,
        "controlOk": out["controlExpected"],
        "frozen01": out["frozen01Unchanged"],
    }, indent=2))


if __name__ == "__main__":
    main()
