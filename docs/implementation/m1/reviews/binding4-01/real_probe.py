#!/usr/bin/env python3
"""Probes on a mirror of the real pinned architecture bytes (arch is only read).

Rebinds the real metadata-v2 unit (record -> subject manifest -> review -> assent
-> lock) and adds synthetic inventory/contract hops so each refusal is isolated.
"""
import copy
import hashlib
import importlib.util
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
LOCK = json.loads((HERE / "copy/design-lock.json").read_bytes())
LIVE_LOCK = json.loads(Path("/Users/sb/code/opensip-ai/opensip/design-lock.json").read_bytes())
spec = importlib.util.spec_from_file_location("vd_real", HERE / "copy/tools/verify_design.py")
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

V1 = "docs/v2/architecture/repository-file-inventory.v1.json"
V3 = "docs/implementation/m1/repository-file-inventory.v3.json"
V4 = "docs/implementation/m1/repository-file-inventory.v4-probe.json"
ROW = "apps/cli/src/bootstrap.rs"


def pins_of(lock):
    found = []

    def walk(value):
        if isinstance(value, dict):
            if set(value) == {"path", "sha256", "bytes"}:
                found.append(value)
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)
    walk(lock)
    contract = lock["contractSuccessors"][0]
    for key in ("subjectManifest", "record"):
        walk(json.loads((ARCH / contract[key]["path"]).read_bytes()))
    return found


def build_pristine(target):
    for pin in pins_of(LOCK) + pins_of({**LIVE_LOCK, "contractSuccessors": [LIVE_LOCK["contractSuccessor"]]}):
        raw = (ARCH / pin["path"]).read_bytes()
        if hashlib.sha256(raw).hexdigest() != pin["sha256"]:
            continue  # historical pin such as previousCandidate stale reference; verified by tool anyway
        dest = target / pin["path"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(raw)


class Mirror:
    def __init__(self, root):
        self.root = root
        self.lock = copy.deepcopy(LOCK)

    def load(self, path):
        return json.loads((self.root / path).read_bytes())

    def write(self, path, value):
        raw = (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()
        dest = self.root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(raw)
        return {"path": path, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}

    def rebind_metadata(self, mutate):
        binding = self.lock["contractSuccessors"][0]
        record = self.load(binding["record"]["path"])
        mutate(record)
        record_pin = self.write(binding["record"]["path"], record)
        manifest = self.load(binding["subjectManifest"]["path"])
        manifest["files"] = [record_pin if row["path"] == record_pin["path"] else row for row in manifest["files"]]
        manifest_pin = self.write(binding["subjectManifest"]["path"], manifest)
        review = self.load(binding["review"]["path"])
        review["subjectManifestSha256"] = manifest_pin["sha256"]
        review_pin = self.write(binding["review"]["path"], review)
        assent = self.load(binding["assent"]["path"])
        assent.update(subjectManifest=manifest_pin, actualClaudeReview=review_pin, acceptedSuccessor=record_pin)
        assent_pin = self.write(binding["assent"]["path"], assent)
        self.lock["contractSuccessors"][0] = dict(record=record_pin, subjectManifest=manifest_pin, review=review_pin, assent=assent_pin)

    def hop(self):
        parent = self.lock["inventorySuccessors"][-1]["candidate"]
        doc = self.load(parent["path"])
        template = next(row for row in doc["files"] if row["path"] == ROW)
        doc["files"] = sorted(doc["files"] + [{**template, "path": "apps/cli/src/aaa_probe.rs", "description": "probe addition"}], key=lambda r: r["path"])
        doc["standing"] = "synthetic probe successor"
        cand = self.write(V4, doc)
        rec = self.write("probe/inventory-record.json", {"parent": parent, "candidate": cand, "parentArtifactBytesUnchanged": True, "inheritedRowsEqualByValue": True})
        subject = "c" * 64
        rev = self.write("probe/inventory-review.json", {"verdict": "ACCEPT-UNIT", "requiredFindings": [], "subjectManifestSha256": subject,
                                                         "inventoryCandidateAssessment": {**cand, "verdict": "ACCEPT", "requiredFindings": [], "parent": parent, "successorRecord": rec}})
        ass = self.write("probe/inventory-assent.json", {"status": "ACCEPTED-UNIT", "rootSubstantiveAssent": True, "requiredUnitFindings": [],
                                                         "actualClaudeReview": rev, "acceptedInventory": cand, "subjectManifest": {"sha256": subject}})
        self.lock["inventorySuccessors"].append(dict(parent=parent, candidate=cand, record=rec, review=rev, assent=ass))
        return cand

    def contract(self, parents, overrides=(), members=None):
        members = members or [self.write("probe/contract/member.json", {"probe": True})]
        rec = self.write("probe/contract/record.json", {"schemaVersion": 1, "parents": sorted(parents, key=lambda r: r["path"]),
                                                        "candidates": sorted(members, key=lambda r: r["path"]), "passageOverrides": list(overrides)})
        man = self.write("probe/contract/manifest.json", {"files": sorted([rec, *members], key=lambda r: r["path"])})
        rev = self.write("probe/contract/review.json", {"verdict": "ACCEPT-DESIGN-UNIT", "requiredFindings": [], "subjectManifestSha256": man["sha256"]})
        ass = self.write("probe/contract/assent.json", {"status": "ACCEPTED-DESIGN-UNIT", "rootSubstantiveAssent": True, "requiredUnitFindings": [],
                                                        "actualClaudeReview": rev, "subjectManifest": man, "acceptedSuccessor": rec})
        self.lock["contractSuccessors"].append(dict(record=rec, subjectManifest=man, review=rev, assent=ass))

    def pin(self, path):
        for row in pins_of(self.lock):
            if row["path"] == path:
                return copy.deepcopy(row)
        raw = (self.root / path).read_bytes()
        return {"path": path, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def metadata_override(record, parent_path):
    return next(o for o in record["passageOverrides"] if o["parent"]["path"] == parent_path)


def real_meaning(mirror):
    record = mirror.load(mirror.lock["contractSuccessors"][0]["record"]["path"])
    return metadata_override(record, V1)


PROBES = []


def probe(name, expect, pattern=None):
    def register(fn):
        PROBES.append((name, fn, expect, pattern))
        return fn
    return register


@probe("R01 mirror baseline equals real-checkout result; accepted live v3 lock verifies on mirror", "PASS")
def r01(m):
    real = M.verify(ARCH, copy.deepcopy(LOCK))
    live = M.verify(m.root, copy.deepcopy(LIVE_LOCK))
    assert live["contractSuccessor"]["selected"] == "docs/implementation/m1/metadata-v2/successor.json"

    def check(result):
        assert result == real
        assert result["inventoryPassageInheritance"] == []
    return check


@probe("R02 real v3 direct override removed: v1 meaning must be inherited explicitly", "DesignError", "passage inheritance differs")
def r02(m):
    m.rebind_metadata(lambda r: r["passageOverrides"].remove(metadata_override(r, V3)))


@probe("R03 real v3 direct override removed + exact projected entry verifies", "PASS")
def r03(m):
    meaning = real_meaning(m)
    m.rebind_metadata(lambda r: r["passageOverrides"].remove(metadata_override(r, V3)))
    v3 = m.lock["inventorySuccessors"][-1]["candidate"]
    entry = {"parent": v3, "selector": {"jsonPointer": "/files/7/description"}, "before": meaning["before"], "after": meaning["after"]}
    m.lock["inventoryPassageInheritance"] = [entry]

    def check(result):
        assert result["inventoryPassageInheritance"] == [entry]
    return check


@probe("R04 real v3 direct override given conflicting meaning refuses", "DesignError", "conflicts with direct override")
def r04(m):
    m.rebind_metadata(lambda r: metadata_override(r, V3).update(after="conflicting probe meaning"))


@probe("R05 synthetic v4 hop shifting bootstrap row 7->8 without inheritance refuses", "DesignError", "passage inheritance differs")
def r05(m):
    m.hop()


@probe("R06 synthetic v4 hop with exact reindexed inheritance verifies; ancestors preserved", "PASS")
def r06(m):
    meaning = real_meaning(m)
    v4 = m.hop()
    doc = m.load(V4)
    assert doc["files"][8]["path"] == ROW and doc["files"][8]["description"] == meaning["before"]
    m.lock["inventoryPassageInheritance"] = [{"parent": v4, "selector": {"jsonPointer": "/files/8/description"}, "before": meaning["before"], "after": meaning["after"]}]
    before = {p: (m.root / p).read_bytes() for p in (V1, V3)}

    def check(result):
        assert result["selectedInventory"] == v4
        assert [r["selected"] for r in result["inventorySuccessors"]] == [V3, V4]
        assert len(result["contractSuccessors"][0]["passageOverrides"]) == 4
        assert all((m.root / p).read_bytes() == raw for p, raw in before.items())
    return check


@probe("R07 synthetic v4 hop with stale index-7 inheritance refuses", "DesignError", "passage inheritance differs")
def r07(m):
    meaning = real_meaning(m)
    v4 = m.hop()
    m.lock["inventoryPassageInheritance"] = [{"parent": v4, "selector": {"jsonPointer": "/files/7/description"}, "before": meaning["before"], "after": meaning["after"]}]


def hop_with_inheritance(m):
    meaning = real_meaning(m)
    v4 = m.hop()
    m.lock["inventoryPassageInheritance"] = [{"parent": v4, "selector": {"jsonPointer": "/files/8/description"}, "before": meaning["before"], "after": meaning["after"]}]
    return v4, meaning


@probe("R08 later contract may parent on v1, v3, v4, metadata-v2 member and record", "PASS")
def r08(m):
    v4, _ = hop_with_inheritance(m)
    parents = [m.pin(V1), m.pin(V3), v4, m.pin("docs/implementation/m1/metadata-v2/command-inventory.v4.json"), m.pin("docs/implementation/m1/metadata-v2/successor.json")]
    m.contract(parents)


@probe("R09 later contract member at overlay-only accepted path refuses", "DesignError", "contract candidate reuses an accepted path")
def r09(m):
    hop_with_inheritance(m)
    source = json.loads((m.root / LOCK["approvals"]["sourceManifest"]["path"]).read_bytes())
    inputs = {row["path"] for row in LOCK["inputs"]}
    overlay = next(row["path"] for row in sorted(source["files"], key=lambda r: r["path"]) if row["path"] not in inputs and not (m.root / row["path"]).exists())
    member = m.write(overlay, {"probe": "overwrite attempt"})
    m.contract([m.pin(V1)], members=[member])


@probe("R10 later contract direct v4 override with conflicting meaning refuses", "DesignError", "conflicts with direct override")
def r10(m):
    v4, meaning = hop_with_inheritance(m)
    m.contract([v4], [{"parent": v4, "selector": {"jsonPointer": "/files/8/description"}, "before": meaning["before"], "after": "conflicting probe meaning"}])


@probe("R11 later contract direct identical v4 override replaces inheritance entry", "PASS")
def r11(m):
    v4, meaning = hop_with_inheritance(m)
    m.lock["inventoryPassageInheritance"] = []
    m.contract([v4], [{"parent": v4, "selector": {"jsonPointer": "/files/8/description"}, "before": meaning["before"], "after": meaning["after"]}])


@probe("R12 later contract non-description override on real v1 ancestor refuses", "DesignError", "unsupported inherited inventory passage selector")
def r12(m):
    hop_with_inheritance(m)
    v1 = m.pin(V1)
    standing = m.load(V1)["standing"]
    m.contract([v1], [{"parent": v1, "selector": {"jsonPointer": "/standing"}, "before": standing, "after": standing + " (probe)"}])


@probe("R13 ADVISORY no hop: line selector aliasing real v3 bootstrap description with other meaning verifies", "PASS")
def r13(m):
    v3 = m.pin(V3)
    lines = (m.root / V3).read_text().splitlines()
    meaning = real_meaning(m)
    number = next(i for i, line in enumerate(lines) if json.dumps(meaning["before"], ensure_ascii=False) in line) + 1
    m.contract([v3], [{"parent": v3, "selector": {"line": number}, "before": lines[number - 1], "after": lines[number - 1].replace(json.dumps(meaning["before"], ensure_ascii=False), '"conflicting alias meaning"')}])


@probe("R14 no hop: later contract conflicting pointer override on real v3 refuses", "DesignError", "conflicting contract passage overrides")
def r14(m):
    v3 = m.pin(V3)
    meaning = real_meaning(m)
    m.contract([v3], [{"parent": v3, "selector": {"jsonPointer": "/files/7/description"}, "before": meaning["before"], "after": "conflicting probe meaning"}])


def main():
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        pristine = Path(tmp) / "pristine"
        build_pristine(pristine)
        for name, fn, expect, pattern in PROBES:
            root = Path(tmp) / "work"
            if root.exists():
                shutil.rmtree(root)
            shutil.copytree(pristine, root)
            mirror = Mirror(root)
            try:
                check = fn(mirror)
                result = M.verify(root, mirror.lock)
                kind, message = "PASS", None
                if callable(check):
                    check(result)
            except M.DesignError as exc:
                kind, message = "DesignError", str(exc)
            except AssertionError as exc:
                kind, message = "ASSERTION", repr(exc)
            except Exception as exc:  # noqa: BLE001
                kind, message = type(exc).__name__, str(exc)
            met = kind == expect and (pattern is None or kind == "PASS" or bool(re.search(pattern, message or "")))
            results.append({"probe": name, "expected": expect, "pattern": pattern, "actual": kind, "message": message, "met": met})
    (HERE / "real-probe-results.json").write_text(json.dumps(results, indent=2) + "\n")
    for row in results:
        print(("ok   " if row["met"] else "MISS ") + row["probe"] + f" -> {row['actual']}: {row['message']}")
    print(f"{sum(r['met'] for r in results)}/{len(results)} expectations met")
    sys.exit(0 if all(r["met"] for r in results) else 1)


if __name__ == "__main__":
    main()
