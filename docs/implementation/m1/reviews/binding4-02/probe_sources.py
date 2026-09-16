#!/usr/bin/env python3
"""Independent --implementation source-preflight probes (review02).

The real architecture checkout and the adapter subject are only read. Probes
that change architecture bytes use a temporary mirror of every pinned file plus
the mapped sources; implementation probes use a temporary copy of schemas/.

usage: probe_sources.py VERIFIER [--no-write]
"""
import copy
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERIFIER = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("vd_src", VERIFIER)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
ADAPTER = Path("/tmp/opensip-implementation/m1-generator-adapter-subject-03")
LOCK = json.loads((HERE / "subject-copy/design-lock.json").read_bytes())
V3LOCK = json.loads((ADAPTER / "design-lock.json").read_bytes())
ROOT_RESULT = json.loads(Path("/tmp/opensip-implementation/m1-binding4-root-validation-02/source-preflight.json").read_bytes())
V1_INV = "docs/v2/architecture/repository-file-inventory.v1.json"
UNACCEPTED = "docs/implementation/m1/trials/cli-metadata-02/subject/schemas/sources/sarif.v2.schema.json"
EXTRA_ACCEPTED = "docs/coop/completion/security-schemas.v2/catalog.schema.json"
MD = "docs/v2/architecture/implementation-boundaries-and-build-plan.md"


def pins(value, found):
    if isinstance(value, dict):
        if set(value) == {"path", "sha256", "bytes"}:
            found.append(value)
        for item in value.values():
            pins(item, found)
    elif isinstance(value, list):
        for item in value:
            pins(item, found)
    return found


def effective():
    rows = {}
    for key in ("sourceManifest", "applicationManifest"):
        for row in json.loads((ARCH / LOCK["approvals"][key]["path"]).read_bytes())["files"]:
            rows[row["path"]] = row
    return rows


EFFECTIVE = effective()


def arch_paths():
    found = pins(LOCK, []) + pins(V3LOCK, [])
    for key in ("subjectManifest", "record"):
        pins(json.loads((ARCH / LOCK["contractSuccessors"][0][key]["path"]).read_bytes()), found)
    paths = {p["path"] for p in found}
    paths |= {r["architectureSource"]["path"] for r in json.loads((ADAPTER / "schemas/source-map.json").read_bytes())["sources"]}
    paths |= {V1_INV, EXTRA_ACCEPTED, MD, UNACCEPTED}
    return sorted(p for p in paths if (ARCH / p).is_file())


def digest_tree(root, paths):
    return {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in paths}


class Ctx:
    def __init__(self, tmp):
        self.tmp = Path(tmp)
        self.impl = self.tmp / "impl"
        shutil.copytree(ADAPTER / "schemas", self.impl / "schemas", symlinks=True)
        (self.impl / "design-lock.json").write_bytes((ADAPTER / "design-lock.json").read_bytes())
        self.arch = ARCH
        self.lock = copy.deepcopy(LOCK)
        self.map = json.loads((self.impl / "schemas/source-map.json").read_bytes())
        self.reg = json.loads((self.impl / "schemas/registry.json").read_bytes())
        self.dirty = False

    def mirror(self):
        mirror = self.tmp / "arch"
        for p in arch_paths():
            (mirror / p).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ARCH / p, mirror / p)
        self.arch = mirror
        return mirror

    def save(self):
        (self.impl / "schemas/source-map.json").write_text(json.dumps(self.map, indent=2) + "\n")
        (self.impl / "schemas/registry.json").write_text(json.dumps(self.reg, indent=2) + "\n")

    def row(self, impl_path):
        m = next(r for r in self.map["sources"] if r["implementationPath"] == impl_path)
        g = next(r for r in self.reg["sources"] if r["sourcePath"] == impl_path)
        return m, g

    def add(self, impl_path, arch_path, schema_id, pin=None):
        raw = (self.arch / arch_path).read_bytes()
        pin = pin or {"path": arch_path, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
        meta = {"declaredMajor": 1, "profile": "opensip-exact-schema-reference-1", "semanticValidatorOwner": "probe"}
        if schema_id is not None:
            meta["schemaId"] = schema_id
        self.map["sources"].append({"implementationPath": impl_path, "architectureSource": pin, **meta})
        self.reg["sources"].append({"sourcePath": impl_path, "sourceSha256": pin["sha256"], **meta})
        (self.impl / impl_path).parent.mkdir(parents=True, exist_ok=True)
        (self.impl / impl_path).write_bytes(raw)


PROBES = []


def probe(name, expect, pattern=None):
    def reg(fn):
        PROBES.append((name, fn, expect, pattern))
        return fn
    return reg


FIRST = "schemas/sources/baseline.v2.schema.json"
ENV4 = "schemas/sources/envelope.v4.schema.json"


@probe("S01 real arch + adapter03 sources: 28 verified, equals root source-preflight result", "PASS")
def s01(c):
    def check(result):
        assert result["generationSources"] == {"sourcesVerified": 28, "executedGeneratorCode": False, "productQualification": False}
        assert result == ROOT_RESULT
    return check


@probe("S02 accepted path but arch bytes changed and local pin/registry/copy repinned refuses", "DesignError", "not selected by accepted design")
def s02(c):
    c.mirror()
    m, g = c.row(FIRST)
    target = c.arch / m["architectureSource"]["path"]
    raw = target.read_bytes().replace(b'"title"', b'"title" ', 1) + b" "
    target.write_bytes(raw)
    m["architectureSource"] = {**m["architectureSource"], "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
    g["sourceSha256"] = m["architectureSource"]["sha256"]
    (c.impl / FIRST).write_bytes(raw)
    c.save()


@probe("S03 accepted pin unchanged but arch bytes changed on disk refuses", "DesignError", "digest mismatch")
def s03(c):
    c.mirror()
    m, _ = c.row(FIRST)
    target = c.arch / m["architectureSource"]["path"]
    target.write_bytes(target.read_bytes() + b" ")
    (c.impl / FIRST).write_bytes(target.read_bytes())
    c.save()


@probe("S04 unaccepted on-disk architecture schema (trial copy) fully rebound refuses", "DesignError", "not selected by accepted design")
def s04(c):
    raw = (ARCH / UNACCEPTED).read_bytes()
    c.add("schemas/sources/unaccepted.json", UNACCEPTED, json.loads(raw).get("$id"))
    c.save()


@probe("S05 superseded source-manifest row (application changed its digest) refuses", "DesignError", "not selected by accepted design")
def s05(c):
    src = {r["path"]: r for r in json.loads((ARCH / LOCK["approvals"]["sourceManifest"]["path"]).read_bytes())["files"]}
    app = json.loads((ARCH / LOCK["approvals"]["applicationManifest"]["path"]).read_bytes())["files"]
    old = next(src[r["path"]] for r in app if r["path"] in src and src[r["path"]]["sha256"] != r["sha256"])
    m, g = c.row(FIRST)
    m["architectureSource"] = dict(old)
    g["sourceSha256"] = old["sha256"]
    c.save()


@probe("S06 previousCandidate metadata-v1 path (not accepted) refuses", "DesignError", "not selected by accepted design")
def s06(c):
    m, g = c.row(FIRST)
    m["architectureSource"] = {"path": "docs/implementation/m1/metadata-v1/successor.json", "sha256": "12e97497565d933f38e33bad68e24aaa5eebda253669134320ef2e379f437f92", "bytes": 2121}
    g["sourceSha256"] = m["architectureSource"]["sha256"]
    c.save()


@probe("S07 implementation copy differs by one byte refuses", "DesignError", "bytes differ")
def s07(c):
    (c.impl / FIRST).write_bytes((c.impl / FIRST).read_bytes() + b"\n")
    c.save()


@probe("S08 implementation source is symlink to the architecture file refuses", "DesignError", "missing or escaping")
def s08(c):
    m, _ = c.row(FIRST)
    (c.impl / FIRST).unlink()
    (c.impl / FIRST).symlink_to(ARCH / m["architectureSource"]["path"])
    c.save()


@probe("S09 schemas/sources directory symlinked to an outside identical copy refuses", "DesignError", "missing or escaping")
def s09(c):
    outside = c.tmp / "outside-sources"
    shutil.move(str(c.impl / "schemas/sources"), outside)
    (c.impl / "schemas/sources").symlink_to(outside, target_is_directory=True)
    c.save()


@probe("S10 source-map.json is a symlink refuses", "DesignError", "missing or escaping")
def s10(c):
    c.save()
    real = c.tmp / "map.json"
    shutil.move(str(c.impl / "schemas/source-map.json"), real)
    (c.impl / "schemas/source-map.json").symlink_to(real)


@probe("S11 registry row without a mapping refuses on coverage", "DesignError", "coverage differ")
def s11(c):
    c.reg["sources"].append({**c.reg["sources"][0], "sourcePath": "schemas/sources/unmapped.json"})
    c.save()


@probe("S12 mapping row missing from registry refuses", "DesignError", "registry digest differs")
def s12(c):
    c.reg["sources"] = [r for r in c.reg["sources"] if r["sourcePath"] != FIRST]
    c.save()


@probe("S13 duplicate registry sourcePath refuses", "DesignError", "duplicate registered source path")
def s13(c):
    c.reg["sources"].append(copy.deepcopy(c.reg["sources"][0]))
    c.save()


@probe("S14 semanticValidatorOwner differs between map and registry refuses", "DesignError", "differs from registry owner")
def s14(c):
    m, _ = c.row(FIRST)
    m["semanticValidatorOwner"] = "crates/other.rs"
    c.save()


@probe("S15 declaredMajor/profile/owner changed consistently in map and registry verifies (local claims, not architecture-bound)", "PASS")
def s15(c):
    m, g = c.row(FIRST)
    for row in (m, g):
        row.update(declaredMajor=99, profile="anything", semanticValidatorOwner="nowhere.rs")
    c.save()


@probe("S16 extra top-level source-map key refuses", "DesignError", "unsupported generation source map")
def s16(c):
    c.map["note"] = "x"
    c.save()


@probe("S17 extra keys in a mapping row and registry recipes are not closed (verifies)", "PASS")
def s17(c):
    m, g = c.row(FIRST)
    m["unreviewed"] = True
    g["alsoUnreviewed"] = True
    c.save()


@probe("S18 non-schema accepted JSON without $id (v1 inventory, a passage-override parent) mapped with schemaId omitted both sides verifies", "PASS")
def s18(c):
    c.add("schemas/sources/inventory-v1-as-source.json", V1_INV, None)
    c.save()


@probe("S19 other accepted overlay schema (not a lock input, not previously mapped) fully rebound verifies", "PASS")
def s19(c):
    raw = (ARCH / EXTRA_ACCEPTED).read_bytes()
    assert EXTRA_ACCEPTED in EFFECTIVE and EXTRA_ACCEPTED not in {r["path"] for r in LOCK["inputs"]}
    c.add("schemas/sources/extra.json", EXTRA_ACCEPTED, json.loads(raw)["$id"])
    c.save()


@probe("S20 two implementation paths mapping the same architecture source verify", "PASS")
def s20(c):
    m, g = c.row(FIRST)
    dup = "schemas/sources/baseline-copy.json"
    c.map["sources"].append({**copy.deepcopy(m), "implementationPath": dup})
    c.reg["sources"].append({**copy.deepcopy(g), "sourcePath": dup})
    shutil.copyfile(c.impl / FIRST, c.impl / dup)
    c.save()


@probe("S21 implementationPath outside schemas/ verifies (path not confined)", "PASS")
def s21(c):
    m, g = c.row(FIRST)
    new = "elsewhere/baseline.json"
    (c.impl / "elsewhere").mkdir()
    shutil.copyfile(c.impl / FIRST, c.impl / new)
    m["implementationPath"] = new
    g["sourcePath"] = new
    c.save()


@probe("S22 accepted non-JSON architecture file as source: exception type recorded", "ANY")
def s22(c):
    c.add("schemas/sources/doc.md", MD, None)
    c.save()


@probe("S23 map schemaVersion true refuses", "DesignError", "unsupported generation source map")
def s23(c):
    c.map["schemaVersion"] = True
    c.save()


@probe("S24 registry schemaVersion 1.0 refuses", "DesignError", "unsupported generation registry")
def s24(c):
    c.reg["schemaVersion"] = 1.0
    c.save()


@probe("S25 registry sourceSha256 uppercase refuses", "DesignError", "registry digest differs")
def s25(c):
    _, g = c.row(FIRST)
    g["sourceSha256"] = g["sourceSha256"].upper()
    c.save()


@probe("S26 accepted v3 adapter lock (singular contractSuccessor) + implementation verifies 28", "PASS")
def s26(c):
    c.lock = copy.deepcopy(V3LOCK)

    def check(result):
        assert result["generationSources"]["sourcesVerified"] == 28
    return check


@probe("S27 v2 lock (no contract unit) + implementation refuses metadata-v2 envelope4 source", "DesignError", "not selected by accepted design")
def s27(c):
    lock = copy.deepcopy(V3LOCK)
    del lock["contractSuccessor"]
    lock["schemaVersion"] = 2
    c.lock = lock


@probe("S28 invalid design (input digest) + valid implementation fails design first", "DesignError", "input is not selected|digest mismatch")
def s28(c):
    c.lock["inputs"][0] = {**c.lock["inputs"][0], "sha256": "0" * 64}


@probe("S29 missing implementation root refuses", "DesignError", "missing or escaping")
def s29(c):
    shutil.rmtree(c.impl)


@probe("S30 mapping row is a list refuses", "DesignError", "generation source mapping must be an object")
def s30(c):
    c.map["sources"].append([])
    c.save()


@probe("S31 architectureSource pin with extra key refuses", "DesignError", "pin must contain exactly")
def s31(c):
    m, _ = c.row(FIRST)
    m["architectureSource"]["note"] = "x"
    c.save()


@probe("S32 schema $id changed consistently in map and registry refuses against architecture", "DesignError", "schema ID differs")
def s32(c):
    m, g = c.row(ENV4)
    m["schemaId"] = g["schemaId"] = "urn:probe:other"
    c.save()


@probe("S33 implementation design-lock.json differs from --lock (adapter03 carries v3 lock) verifies: root lock not bound", "PASS")
def s33(c):
    assert (c.impl / "design-lock.json").read_bytes() != (HERE / "subject-copy/design-lock.json").read_bytes()


def cli(c):
    env = {"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin"}
    ok = subprocess.run([sys.executable, str(VERIFIER), "--architecture", str(ARCH), "--lock", str(HERE / "subject-copy/design-lock.json"), "--implementation", str(c.impl)], capture_output=True, text=True, env=env)
    bad = subprocess.run([sys.executable, str(VERIFIER), "--architecture", str(ARCH), "--lock", str(HERE / "subject-copy/design-lock.json"), "--implementation", str(c.tmp / "nope")], capture_output=True, text=True, env=env)
    return ok, bad


def run():
    watched = arch_paths()
    arch_before = digest_tree(ARCH, watched)
    adapter_files = sorted(str(p.relative_to(ADAPTER)) for p in ADAPTER.rglob("*") if p.is_file() and "node_modules" not in p.parts and "target" not in p.parts)
    adapter_before = digest_tree(ADAPTER, adapter_files)
    results = []
    for name, fn, expect, pattern in PROBES:
        with tempfile.TemporaryDirectory() as tmp:
            c = Ctx(tmp)
            try:
                check = fn(c)
                impl_before = {str(p): p.read_bytes() for p in c.impl.rglob("*") if p.is_file()} if c.impl.exists() else {}
                result = M.verify(c.arch, c.lock, c.impl)
                if callable(check):
                    check(result)
                impl_after = {str(p): p.read_bytes() for p in c.impl.rglob("*") if p.is_file()}
                assert impl_before == impl_after, "implementation changed"
                kind, msg = "PASS", None
            except M.DesignError as exc:
                kind, msg = "DesignError", str(exc)
            except AssertionError as exc:
                kind, msg = "ASSERTION", repr(exc)
            except Exception as exc:  # noqa: BLE001
                kind, msg = type(exc).__name__, str(exc)[:200]
        met = expect == "ANY" or (kind == expect and (pattern is None or re.search(pattern, msg or "") is not None))
        results.append({"probe": name, "expected": expect, "pattern": pattern, "actual": kind, "message": msg, "met": met})
    with tempfile.TemporaryDirectory() as tmp:
        c = Ctx(tmp)
        ok, bad = cli(c)
        met = ok.returncode == 0 and json.loads(ok.stdout) == ROOT_RESULT and bad.returncode == 1 and "Design verification failed" in bad.stderr
        results.append({"probe": "S34 CLI --implementation exit 0 with root-equal output; missing root exits 1", "expected": "PASS", "pattern": None,
                        "actual": f"exit {ok.returncode}/{bad.returncode}", "message": bad.stderr.strip()[:200], "met": met})
    same = digest_tree(ARCH, watched) == arch_before and digest_tree(ADAPTER, adapter_files) == adapter_before
    results.append({"probe": f"S35 real architecture ({len(watched)} watched files) and adapter03 ({len(adapter_files)} files) unchanged", "expected": "PASS",
                    "pattern": None, "actual": "PASS" if same else "CHANGED", "message": None, "met": same})
    return results


if __name__ == "__main__":
    rows = run()
    for r in rows:
        print(("ok   " if r["met"] else "MISS ") + r["probe"] + f" -> {r['actual']}: {r['message']}")
    print(f"{sum(r['met'] for r in rows)}/{len(rows)} expectations met")
    if "--no-write" not in sys.argv:
        (HERE / "probe-sources-results.json").write_text(json.dumps(rows, indent=2) + "\n")
    sys.exit(0 if all(r["met"] for r in rows) else 1)
