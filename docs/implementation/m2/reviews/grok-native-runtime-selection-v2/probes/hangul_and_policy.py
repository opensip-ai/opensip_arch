#!/usr/bin/env python3
"""Independent Hangul range math, tinyvec_macros absence, and policy negatives."""
from __future__ import annotations
import hashlib, json, shutil, subprocess, tempfile
from pathlib import Path
import tomllib

PROD = Path("/tmp/opensip-implementation/m2-grok-native-runtime-selection-v2-review/review/copy/product")
ARCHIVES = Path("/Users/sb/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f")
SRC = Path("/Users/sb/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f")
OUT = Path("/tmp/opensip-implementation/m2-grok-native-runtime-selection-v2-review/review/results/hangul-policy.json")
CARGO = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
CHECK = PROD / "tools/check_identity_dependencies.py"
POLICY = PROD / "tools/identity/dependency-policy.json"


def hangul():
    S_BASE, L_BASE, V_BASE, T_BASE = 0xAC00, 0x1100, 0x1161, 0x11A7
    L_COUNT, V_COUNT, T_COUNT = 19, 21, 28
    N_COUNT = V_COUNT * T_COUNT
    S_COUNT = L_COUNT * N_COUNT
    S_LAST = S_BASE + S_COUNT - 1
    assert S_COUNT == 11172
    assert S_LAST == 0xD7A3
    # is_hangul_syllable: AC00 .. D7A3 inclusive
    assert S_BASE + S_COUNT - 1 == 0xD7A3
    # L/V/T outputs stay below D800
    max_l = L_BASE + (L_COUNT - 1)
    max_v = V_BASE + (V_COUNT - 1)
    max_t = T_BASE + (T_COUNT - 1)
    max_lv = S_BASE + (L_COUNT - 1) * N_COUNT + (V_COUNT - 1) * T_COUNT
    max_lvt = max_lv + (T_COUNT - 1)
    assert max_l == 0x1112 and max_v == 0x1175 and max_t == 0x11C2
    assert max_lv == 0xD788
    assert max_lvt == 0xD7A3
    for n in (max_l, max_v, max_t, max_lv, max_lvt, S_LAST):
        assert n < 0xD800
        assert not (0xD800 <= n <= 0xDFFF)
    # pin exact normalize.rs bytes from extracted crate
    pol = json.loads(POLICY.read_bytes())
    uni = next(d for d in pol["dependencies"] if d["name"] == "unicode-normalization")
    row = next(s for s in uni["sources"] if s["path"] == "src/normalize.rs")
    extracted = SRC / "unicode-normalization-0.1.24" / "src/normalize.rs"
    raw = extracted.read_bytes()
    assert len(raw) == row["bytes"] and hashlib.sha256(raw).hexdigest() == row["sha256"]
    text = raw.decode()
    assert "from_u32_unchecked" in text
    assert "S_BASE: u32 = 0xAC00" in text
    return {
        "sLast": hex(S_LAST),
        "maxLv": hex(max_lv),
        "maxLvt": hex(max_lvt),
        "allBelowD800": True,
        "normalizeRsPinMatch": True,
        "bytes": row["bytes"],
        "sha256": row["sha256"],
    }


def tinyvec():
    crate = ARCHIVES / "tinyvec-1.13.3.crate"
    pol = json.loads(POLICY.read_bytes())
    tv = next(d for d in pol["dependencies"] if d["name"] == "tinyvec")
    assert hashlib.sha256(crate.read_bytes()).hexdigest() == tv["checksum"]
    toml = tomllib.loads((SRC / "tinyvec-1.13.3" / "Cargo.toml").read_text())
    orig = (SRC / "tinyvec-1.13.3" / "Cargo.toml.orig").read_text()
    features = toml.get("features", {})
    # empty default; feature name tinyvec_macros exists but is empty and not a dependency
    assert features.get("default") == []
    assert features.get("alloc") == []
    assert "tinyvec_macros" in features and features["tinyvec_macros"] == []
    deps = toml.get("dependencies", {})
    assert "tinyvec_macros" not in deps
    changelog = (SRC / "tinyvec-1.13.3" / "changelog.md").read_text()
    assert "no longer depended on by this crate" in changelog
    meta = json.loads(
        subprocess.check_output(
            [
                CARGO,
                "metadata",
                "--locked",
                "--offline",
                "--format-version",
                "1",
                "--filter-platform",
                "aarch64-apple-darwin",
                "--manifest-path",
                str(PROD / "Cargo.toml"),
            ]
        )
    )
    names = {p["name"] for p in meta["packages"]}
    assert "tinyvec_macros" not in names
    identity = next(p for p in meta["packages"] if p["name"] == "opensip-identity")
    unorm = next(p for p in meta["packages"] if p["name"] == "unicode-normalization")
    tiny = next(p for p in meta["packages"] if p["name"] == "tinyvec")
    assert identity.get("links") is None
    assert unorm.get("links") is None and tiny.get("links") is None
    def node_named(name):
        for n in meta["resolve"]["nodes"]:
            ident = n["id"]
            if ident == name or ident.startswith(name + " ") or f"#{name}@" in ident:
                return n
        raise KeyError(name)
    node = node_named("tinyvec")
    assert sorted(node["features"]) == ["alloc", "default"]
    unode = node_named("unicode-normalization")
    assert sorted(unode["features"]) == []
    return {
        "tinyvecMacrosPackageAbsent": True,
        "tinyvecMacrosFeatureEmptyNotDep": True,
        "defaultEmpty": True,
        "resolvedTinyvecFeatures": sorted(node["features"]),
        "resolvedUnormFeatures": sorted(unode["features"]),
        "checksum": tv["checksum"],
    }


def negatives():
    import importlib.util

    spec = importlib.util.spec_from_file_location("idcheck", CHECK)
    M = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(M)
    meta = json.loads(
        subprocess.check_output(
            [
                CARGO,
                "metadata",
                "--locked",
                "--offline",
                "--format-version",
                "1",
                "--filter-platform",
                "aarch64-apple-darwin",
                "--manifest-path",
                str(PROD / "Cargo.toml"),
            ]
        )
    )
    lock = tomllib.loads((PROD / "Cargo.lock").read_text())
    policy = json.loads(POLICY.read_bytes())
    results = []

    def run(label, pol):
        try:
            M.check(meta, lock, pol, ARCHIVES)
            results.append({"label": label, "ok": False, "detail": "unexpected pass"})
        except M.DependencyError as e:
            results.append({"label": label, "ok": True, "refusal": str(e)})

    p = json.loads(json.dumps(policy))
    next(d for d in p["dependencies"] if d["name"] == "unicode-normalization")["resolvedFeatures"] = ["std"]
    run("unicode-normalization-extra-feature", p)

    p = json.loads(json.dumps(policy))
    next(d for d in p["dependencies"] if d["name"] == "tinyvec")["resolvedFeatures"] = ["alloc", "default", "std"]
    run("tinyvec-extra-feature", p)

    p = json.loads(json.dumps(policy))
    p["dependencies"] = [d for d in p["dependencies"] if d["name"] != "unicode-normalization"]
    run("unlisted-dependency", p)

    p = json.loads(json.dumps(policy))
    next(d for d in p["dependencies"] if d["name"] == "unicode-normalization")["version"] = "0.1.25"
    run("Unicode17-version", p)

    p = json.loads(json.dumps(policy))
    next(d for d in p["dependencies"] if d["name"] == "tinyvec")["checksum"] = "00" * 32
    run("changed-lock-checksum", p)

    p = json.loads(json.dumps(policy))
    p["localSources"] = p["localSources"] + [
        {"path": "src/forged.rs", "bytes": 1, "sha256": "00" * 32}
    ]
    p["localSources"].sort(key=lambda r: r["path"])
    run("extra-local-source", p)

    p = json.loads(json.dumps(policy))
    p["rootFeatures"] = ["std"]
    run("root-extra-feature", p)

    return results


def main():
    report = {
        "hangul": hangul(),
        "tinyvec": tinyvec(),
        "negatives": negatives(),
    }
    report["negativesPassed"] = all(r["ok"] for r in report["negatives"])
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({
        "hangulBelowD800": report["hangul"]["allBelowD800"],
        "tinyvecMacrosAbsent": report["tinyvec"]["tinyvecMacrosPackageAbsent"],
        "negatives": [(r["label"], r["ok"], r.get("refusal")) for r in report["negatives"]],
    }, indent=2))
    if not report["negativesPassed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
