#!/usr/bin/env python3
"""Independent synthetic v4 probes (review02): old semantics, multi-hop,
aliases, reuse and malformed data. Fixtures are fully rebound so each refusal
reaches the intended guard; refusals are matched on diagnostic text.

usage: probe_v4.py VERIFIER [--no-write]
"""
import copy
import hashlib
import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("vd_probe", sys.argv[1])
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)


def srt(rows):
    return sorted(rows, key=lambda r: r["path"])


class F:
    def __init__(self, root):
        self.root = Path(root)

    def raw(self, path, raw):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        return {"path": path, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}

    def w(self, path, value, indent=2):
        return self.raw(path, (json.dumps(value, sort_keys=True, indent=indent) + "\n").encode())

    def doc(self, pin):
        return json.loads((self.root / pin["path"]).read_bytes())

    def base(self, rows, extra=()):
        inv = {"schemaVersion": 1, "standing": "s", "packages": [{"id": "t", "dependencies": []}], "pendingDecisions": [],
               "files": srt([{"path": p, "package": "t", "role": "r", "description": d} for p, d in rows.items()])}
        self.inv0 = self.w("arch/inv0.json", inv)
        extras = [self.w(p, v) if not isinstance(v, bytes) else self.raw(p, v) for p, v in extra]
        src = self.w("appr/source.json", {"files": [self.inv0, *extras]}, None)
        app = self.w("appr/app.json", {"files": [], "designSubject": src}, None)
        rev = self.w("appr/review.json", {"verdict": "ACCEPT", "subjectManifestSha256": app["sha256"], "newMustIssues": [], "newShouldIssues": []}, None)
        act = self.w("appr/activation.json", {"applicationManifest": app, "independentApplicationReview": rev}, None)
        ass = self.w("appr/assent.json", {"authority": {"rootApplicationAssent": True}, "subjectManifestSha256": app["sha256"], "review": rev}, None)
        comp = self.w("appr/completion.json", {"designApprovedForImplementation": True, "passed": True, "applicationManifest": app, "activation": act, "actualClaudeApplicationReview": rev, "codexApplicationAssent": ass}, None)
        self.lock = {"schemaVersion": 4, "architectureRepository": "probe",
                     "approvals": dict(sourceManifest=src, applicationManifest=app, activation=act, applicationReview=rev, rootAssent=ass, completion=comp),
                     "inputs": srt([self.inv0, *extras]), "inventorySuccessors": [], "contractSuccessors": [], "inventoryPassageInheritance": []}
        self.extras = extras
        self.invs = [self.inv0]
        return self.inv0

    def hop(self, added, path=None, parent=None):
        parent = parent or self.invs[-1]
        n = len(self.lock["inventorySuccessors"]) + 1
        d = self.doc(parent)
        d["files"] = srt(d["files"] + [{"path": p, "package": "t", "role": "r", "description": x} for p, x in added.items()])
        cand = self.w(path or f"arch/inv{n}.json", d)
        return self.bind_hop(parent, cand)

    def bind_hop(self, parent, cand):
        n = len(self.lock["inventorySuccessors"]) + 1
        rec = self.w(f"hop{n}/record.json", {"parent": parent, "candidate": cand, "parentArtifactBytesUnchanged": True, "inheritedRowsEqualByValue": True}, None)
        subj = hashlib.sha256(b"s%d" % n).hexdigest()
        rev = self.w(f"hop{n}/review.json", {"verdict": "ACCEPT-UNIT", "requiredFindings": [], "subjectManifestSha256": subj,
                     "inventoryCandidateAssessment": {**cand, "verdict": "ACCEPT", "requiredFindings": [], "parent": parent, "successorRecord": rec}}, None)
        ass = self.w(f"hop{n}/assent.json", {"status": "ACCEPTED-UNIT", "rootSubstantiveAssent": True, "requiredUnitFindings": [],
                     "actualClaudeReview": rev, "acceptedInventory": cand, "subjectManifest": {"sha256": subj}}, None)
        self.lock["inventorySuccessors"].append(dict(parent=parent, candidate=cand, record=rec, review=rev, assent=ass))
        self.invs.append(cand)
        return cand

    def unit(self, parents, overrides=(), members=None):
        n = len(self.lock["contractSuccessors"]) + 1
        members = members if members is not None else [self.w(f"unit{n}/member.json", {"unit": n})]
        rec = self.w(f"unit{n}/record.json", {"parents": srt(copy.deepcopy(parents)), "candidates": srt(members), "passageOverrides": list(overrides)}, None)
        man = self.w(f"unit{n}/manifest.json", {"files": srt([rec, *members])}, None)
        rev = self.w(f"unit{n}/review.json", {"verdict": "ACCEPT-DESIGN-UNIT", "requiredFindings": [], "subjectManifestSha256": man["sha256"]}, None)
        ass = self.w(f"unit{n}/assent.json", {"status": "ACCEPTED-DESIGN-UNIT", "rootSubstantiveAssent": True, "requiredUnitFindings": [],
                     "actualClaudeReview": rev, "subjectManifest": man, "acceptedSuccessor": rec}, None)
        self.lock["contractSuccessors"].append(dict(record=rec, subjectManifest=man, review=rev, assent=ass))
        return members

    def index(self, pin, path):
        return next(i for i, r in enumerate(self.doc(pin)["files"]) if r["path"] == path)

    def line(self, pin, needle):
        lines = (self.root / pin["path"]).read_text().splitlines()
        hits = [i for i, l in enumerate(lines) if needle in l]
        assert len(hits) == 1, hits
        return hits[0] + 1, lines[hits[0]]


def d(parent, index, before, after):
    return {"parent": parent, "selector": {"jsonPointer": f"/files/{index}/description"}, "before": before, "after": after}


def to_v3(lock):
    lock = copy.deepcopy(lock)
    lock["schemaVersion"] = 3
    lock["inventorySuccessor"] = lock.pop("inventorySuccessors")[0]
    lock["contractSuccessor"] = lock.pop("contractSuccessors")[0]
    del lock["inventoryPassageInheritance"]
    return lock


PROBES = []


def probe(name, expect, pattern=None):
    def reg(fn):
        PROBES.append((name, fn, expect, pattern))
        return fn
    return reg


# ---- old semantics / compatibility ------------------------------------------------
@probe("V01 v4 single hop and unit with no overrides verifies", "PASS")
def v01(f):
    b = f.base({"b.py": "B0"}); f.hop({"c.py": "C0"}); f.unit([b])


@probe("V02 v3 lock keeps JSON line selector compatibility", "PASS")
def v02(f):
    b = f.base({"b.py": "B0"}); fin = f.hop({"c.py": "C0"})
    n, line = f.line(fin, '"B0"')
    f.unit([fin], [{"parent": fin, "selector": {"line": n}, "before": line, "after": line.replace("B0", "B1")}])
    f.lock = to_v3(f.lock)


@probe("V03 same JSON line selector in v4 refuses", "DesignError", "require JSON Pointer")
def v03(f):
    b = f.base({"b.py": "B0"}); fin = f.hop({"c.py": "C0"})
    n, line = f.line(fin, '"B0"')
    f.unit([fin], [{"parent": fin, "selector": {"line": n}, "before": line, "after": line.replace("B0", "B1")}])


@probe("V04 v4 line selector on non-JSON text parent still verifies", "PASS")
def v04(f):
    f.base({"b.py": "B0"}, extra=[("arch/doc.md", b"# T\nold line\n")]); f.hop({"c.py": "C0"})
    md = f.extras[0]
    f.unit([md], [{"parent": md, "selector": {"line": 2}, "before": "old line", "after": "new line"}])


@probe("V05 v2 lock (no contract) still verifies", "PASS")
def v05(f):
    f.base({"b.py": "B0"}); f.hop({"c.py": "C0"}); f.unit([f.inv0])
    lock = to_v3(f.lock); del lock["contractSuccessor"]; lock["schemaVersion"] = 2
    f.lock = lock


# ---- multi-hop inheritance ---------------------------------------------------------
def three_hops(f):
    b = f.base({"m.py": "M0", "z.py": "Z0"})
    h1 = f.hop({"k.py": "K0"})   # m: 0 -> 1
    h2 = f.hop({"c.py": "C0"})   # m: 1 -> 2
    h3 = f.hop({"a.py": "A0"})   # m: 2 -> 3
    return b, h1, h2, h3


@probe("V06 three hops: base override projects to final index 3", "PASS")
def v06(f):
    b, h1, h2, h3 = three_hops(f)
    f.unit([b], [d(b, 0, "M0", "M1")])
    f.lock["inventoryPassageInheritance"] = [d(h3, 3, "M0", "M1")]
    assert f.index(h3, "m.py") == 3


@probe("V07 three hops: stale intermediate index 2 refuses", "DesignError", "inheritance differs")
def v07(f):
    b, h1, h2, h3 = three_hops(f)
    f.unit([b], [d(b, 0, "M0", "M1")])
    f.lock["inventoryPassageInheritance"] = [d(h3, 2, "M0", "M1")]


@probe("V08 three hops: entry pinned to intermediate parent refuses", "DesignError", "inheritance differs")
def v08(f):
    b, h1, h2, h3 = three_hops(f)
    f.unit([b], [d(b, 0, "M0", "M1")])
    f.lock["inventoryPassageInheritance"] = [d(h2, 2, "M0", "M1")]


@probe("V09 base and hop1 identical meanings collapse to one entry", "PASS")
def v09(f):
    b, h1, h2, h3 = three_hops(f)
    f.unit([b], [d(b, 0, "M0", "M1")])
    f.unit([h1], [d(h1, 1, "M0", "M1")])
    f.lock["inventoryPassageInheritance"] = [d(h3, 3, "M0", "M1")]


@probe("V10 base vs hop2 conflicting ancestor meanings refuse", "DesignError", "inherited inventory passage meanings conflict")
def v10(f):
    b, h1, h2, h3 = three_hops(f)
    f.unit([b], [d(b, 0, "M0", "M1")])
    f.unit([h2], [d(h2, 2, "M0", "M2")])
    f.lock["inventoryPassageInheritance"] = [d(h3, 3, "M0", "M2")]


@probe("V11 conflicting direct final override refuses", "DesignError", "conflicts with direct override")
def v11(f):
    b, h1, h2, h3 = three_hops(f)
    f.unit([b], [d(b, 0, "M0", "M1")])
    f.unit([h3], [d(h3, 3, "M0", "M9")])


@probe("V12 identical direct final override suppresses entry (empty list verifies)", "PASS")
def v12(f):
    b, h1, h2, h3 = three_hops(f)
    f.unit([b], [d(b, 0, "M0", "M1")])
    f.unit([h3], [d(h3, 3, "M0", "M1")])


@probe("V13 inheritance entry with an extra key refuses", "DesignError", "inheritance differs")
def v13(f):
    b, h1, h2, h3 = three_hops(f)
    f.unit([b], [d(b, 0, "M0", "M1")])
    f.lock["inventoryPassageInheritance"] = [{**d(h3, 3, "M0", "M1"), "note": "x"}]


@probe("V14 inventoryPassageInheritance null refuses", "DesignError", "inheritance differs")
def v14(f):
    f.base({"b.py": "B0"}); f.hop({"c.py": "C0"}); f.unit([f.inv0])
    f.lock["inventoryPassageInheritance"] = None


@probe("V15 two rows across 12-row base sort lexicographically (/files/10 < /files/3)", "PASS")
def v15(f):
    b = f.base({f"r{i:02d}.py": f"R{i}" for i in range(12)})
    h = f.hop({"a.py": "A0"})
    f.unit([b], [d(b, 2, "R2", "X2"), d(b, 9, "R9", "X9")])
    f.lock["inventoryPassageInheritance"] = [d(h, 10, "R9", "X9"), d(h, 3, "R2", "X2")]


@probe("V16 hop1 override inherited when hop1 is non-final (two hops)", "PASS")
def v16(f):
    b = f.base({"m.py": "M0"}); h1 = f.hop({"k.py": "K0"}); h2 = f.hop({"c.py": "C0"})
    f.unit([h1], [d(h1, f.index(h1, "k.py"), "K0", "K1")])
    f.lock["inventoryPassageInheritance"] = [d(h2, f.index(h2, "k.py"), "K0", "K1")]


# ---- aliases -------------------------------------------------------------------
@probe("V17 line selector on non-final inventory (JSON) refuses by content guard", "DesignError", "require JSON Pointer")
def v17(f):
    b, h1, h2, h3 = three_hops(f)
    n, line = f.line(h1, '"M0"')
    f.unit([h1], [{"parent": h1, "selector": {"line": n}, "before": line, "after": line.replace("M0", "M5")}])


@probe("V18 line selector on JSON contract member (not inventory) refuses", "DesignError", "require JSON Pointer")
def v18(f):
    b = f.base({"b.py": "B0"}); f.hop({"c.py": "C0"})
    mem = f.unit([b], members=[f.w("unit1/member.json", {"text": "old"})])[0]
    n, line = f.line(mem, '"old"')
    f.unit([mem], [{"parent": mem, "selector": {"line": n}, "before": line, "after": line.replace("old", "new")}])


@probe("V19 .json suffix with non-JSON content keeps line selectors", "PASS")
def v19(f):
    f.base({"b.py": "B0"}, extra=[("arch/notes.json", b"not json\nold\n")]); f.hop({"c.py": "C0"})
    p = f.extras[0]
    f.unit([p], [{"parent": p, "selector": {"line": 2}, "before": "old", "after": "new"}])


@probe("V20 .txt suffix with JSON scalar content refuses line selector", "DesignError", "require JSON Pointer")
def v20(f):
    f.base({"b.py": "B0"}, extra=[("arch/scalar.txt", b'"old"\n')]); f.hop({"c.py": "C0"})
    p = f.extras[0]
    f.unit([p], [{"parent": p, "selector": {"line": 1}, "before": '"old"', "after": '"new"'}])


@probe("V21 duplicate-key JSON parent is treated as text: line selector verifies", "PASS")
def v21(f):
    f.base({"b.py": "B0"}, extra=[("arch/dup.json", b'{"a": "old",\n "a": "x"}\n')]); f.hop({"c.py": "C0"})
    p = f.extras[0]
    f.unit([p], [{"parent": p, "selector": {"line": 1}, "before": '{"a": "old",', "after": '{"a": "new",'}])


@probe("V22 duplicate-key JSON parent cannot be addressed by pointer (no alias)", "DesignError", "duplicate JSON key")
def v22(f):
    f.base({"b.py": "B0"}, extra=[("arch/dup.json", b'{"a": "old",\n "a": "x"}\n')]); f.hop({"c.py": "C0"})
    p = f.extras[0]
    f.unit([p], [{"parent": p, "selector": {"jsonPointer": "/a"}, "before": "old", "after": "new"}])


@probe("V23 UTF-8 BOM JSON parent: line selector outcome recorded", "ANY")
def v23(f):
    f.base({"b.py": "B0"}, extra=[("arch/bom.json", b'\xef\xbb\xbf{"a":\n"old"}\n')]); f.hop({"c.py": "C0"})
    p = f.extras[0]
    f.unit([p], [{"parent": p, "selector": {"line": 2}, "before": '"old"}', "after": '"new"}'}])


@probe("V24 UTF-8 BOM JSON parent: pointer outcome recorded", "ANY")
def v24(f):
    f.base({"b.py": "B0"}, extra=[("arch/bom.json", b'\xef\xbb\xbf{"a":\n"old"}\n')]); f.hop({"c.py": "C0"})
    p = f.extras[0]
    f.unit([p], [{"parent": p, "selector": {"jsonPointer": "/a"}, "before": "old", "after": "new"}])


@probe("V25 pointer leading-zero alias /files/00/description refuses", "DesignError", "array index")
def v25(f):
    b = f.base({"b.py": "B0"}); h = f.hop({"c.py": "C0"})
    f.unit([h], [{"parent": h, "selector": {"jsonPointer": "/files/00/description"}, "before": "B0", "after": "B1"}])


@probe("V26 pointer escape alias of key 'a/b' only via ~1", "DesignError", "does not resolve")
def v26(f):
    f.base({"b.py": "B0"}, extra=[("arch/esc.json", {"a/b": "old", "a": {"b": "other"}})]); f.hop({"c.py": "C0"})
    p = f.extras[0]
    # /a/b resolves to a different value ("other"), so the before text for a/b does not match
    f.unit([p], [{"parent": p, "selector": {"jsonPointer": "/a~1b/"}, "before": "old", "after": "new"}])


@probe("V27 mixed selector keys refuse as unsupported", "DesignError", "unsupported passage selector")
def v27(f):
    b = f.base({"b.py": "B0"}); h = f.hop({"c.py": "C0"})
    f.unit([h], [{"parent": h, "selector": {"line": 1, "jsonPointer": "/files/0/description"}, "before": "B0", "after": "B1"}])


# ---- reuse -----------------------------------------------------------------------
@probe("V28 contract member at an inventory candidate path refuses", "DesignError", "contract candidate reuses")
def v28(f):
    b = f.base({"b.py": "B0"}); h = f.hop({"c.py": "C0"})
    f.unit([b], members=[h])


@probe("V29 inventory candidate at an accepted overlay path (not a lock input) refuses", "DesignError", "inventory candidate reuses")
def v29(f):
    f.base({"b.py": "B0"}, extra=[("arch/x.json", {"x": 1})])
    # Keep x.json accepted by the source manifest but unpinned by lock inputs, so
    # the reuse guard, not the base input digest check, is what must refuse.
    f.lock["inputs"] = [f.inv0]
    f.hop({"c.py": "C0"}, path="arch/x.json")
    f.unit([f.inv0])


@probe("V30 second unit member reusing first unit record path refuses", "DesignError", "reuses|digest mismatch")
def v30(f):
    b = f.base({"b.py": "B0"}); f.hop({"c.py": "C0"})
    f.unit([b])
    rec = f.lock["contractSuccessors"][0]["record"]
    f.unit([b], members=[rec])


@probe("V31 member whose bytes equal an inventory review file at its path (not tracked as accepted)", "ANY")
def v31(f):
    b = f.base({"b.py": "B0"}); f.hop({"c.py": "C0"})
    rev = f.lock["inventorySuccessors"][0]["review"]
    f.unit([b], members=[rev])


@probe("V32 unit parent is a later unit member (forward) refuses", "DesignError", "not an accepted base")
def v32(f):
    b = f.base({"b.py": "B0"}); f.hop({"c.py": "C0"})
    future = f.w("unit2/member.json", {"unit": 2})
    f.unit([future])
    f.unit([b], members=[future])


@probe("V33 hop parent repeated (branch from hop1 after hop2) refuses", "DesignError", "immediate predecessor")
def v33(f):
    b = f.base({"m.py": "M0"}); h1 = f.hop({"k.py": "K0"}); f.hop({"c.py": "C0"})
    f.hop({"a.py": "A0"}, parent=h1)
    f.unit([b])


@probe("V34 cycle back to base inventory path refuses", "DesignError", "inventory candidate reuses")
def v34(f):
    b = f.base({"m.py": "M0"}); h1 = f.hop({"k.py": "K0"})
    f.bind_hop(h1, b)
    f.unit([b])


# ---- malformed -------------------------------------------------------------------
@probe("V35 inventory chain element is a string", "DesignError", "inventory chain binding must be an object")
def v35(f):
    b = f.base({"b.py": "B0"}); f.hop({"c.py": "C0"}); f.unit([b])
    f.lock["inventorySuccessors"] = ["x"]


@probe("V36 candidate path noncanonical '../x.json'", "DesignError", "noncanonical")
def v36(f):
    b = f.base({"b.py": "B0"}); f.hop({"c.py": "C0"}); f.unit([b])
    f.lock["inventorySuccessors"][0]["candidate"]["path"] = "../x.json"


@probe("V37 candidate is a list", "DesignError", "candidate must be an object")
def v37(f):
    b = f.base({"b.py": "B0"}); f.hop({"c.py": "C0"}); f.unit([b])
    f.lock["inventorySuccessors"][0]["candidate"] = []


@probe("V38 contract chain element is null", "DesignError", "four closed")
def v38(f):
    b = f.base({"b.py": "B0"}); f.hop({"c.py": "C0"}); f.unit([b])
    f.lock["contractSuccessors"] = [None]


@probe("V39 override parent path is a list (carried contract code)", "ANY")
def v39(f):
    b = f.base({"b.py": "B0"}); f.hop({"c.py": "C0"})
    f.unit([b], [{"parent": {"path": ["x"], "sha256": "0" * 64, "bytes": 1}, "selector": {"jsonPointer": "/standing"}, "before": "s", "after": "t"}])


@probe("V40 v4 lock missing inventoryPassageInheritance", "DesignError", "unsupported design lock")
def v40(f):
    b = f.base({"b.py": "B0"}); f.hop({"c.py": "C0"}); f.unit([b])
    del f.lock["inventoryPassageInheritance"]


@probe("V41 ancestor override on /files/N/description/extra refuses", "DesignError", "does not resolve|unsupported")
def v41(f):
    b, h1, h2, h3 = three_hops(f)
    f.unit([b], [{"parent": b, "selector": {"jsonPointer": "/files/0/description/x"}, "before": "M0", "after": "M1"}])


@probe("V42 version 4 with a float 4.0 refuses", "DesignError", "unsupported design lock")
def v42(f):
    b = f.base({"b.py": "B0"}); f.hop({"c.py": "C0"}); f.unit([b])
    f.lock["schemaVersion"] = 4.0


def run():
    results = []
    for name, fn, expect, pattern in PROBES:
        with tempfile.TemporaryDirectory() as tmp:
            f = F(tmp)
            try:
                fn(f)
                out = M.verify(f.root, f.lock)
                kind, msg = "PASS", None
                assert out["passed"] is True
            except M.DesignError as exc:
                kind, msg = "DesignError", str(exc)
            except AssertionError as exc:
                kind, msg = "ASSERTION", repr(exc)
            except Exception as exc:  # noqa: BLE001
                kind, msg = type(exc).__name__, str(exc)
        met = expect == "ANY" or (kind == expect and (pattern is None or re.search(pattern, msg or "") is not None))
        results.append({"probe": name, "expected": expect, "pattern": pattern, "actual": kind, "message": msg, "met": met})
    return results


if __name__ == "__main__":
    rows = run()
    for r in rows:
        print(("ok   " if r["met"] else "MISS ") + r["probe"] + f" -> {r['actual']}: {r['message']}")
    print(f"{sum(r['met'] for r in rows)}/{len(rows)} expectations met")
    if "--no-write" not in sys.argv:
        (HERE / "probe-v4-results.json").write_text(json.dumps(rows, indent=2) + "\n")
    sys.exit(0 if all(r["met"] for r in rows) else 1)
