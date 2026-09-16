#!/usr/bin/env python3
"""Independent synthetic probes for design-lock v4 successor chains.

Usage: probe.py VERIFY_DESIGN_PY [RESULTS_JSON]
Every probe builds a fully rebound fixture (reviews, assents, manifests, lock),
so a refusal must come from the named guard, not an earlier digest failure.
"""
import copy
import hashlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path


def load(path):
    spec = importlib.util.spec_from_file_location("vd_probe", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def by_path(rows):
    return sorted(rows, key=lambda row: row["path"])


class Fx:
    def __init__(self, root):
        self.root = Path(root)

    def write(self, path, value, indent=None):
        raw = (json.dumps(value, sort_keys=True, indent=indent) + "\n").encode()
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        return {"path": path, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}

    def row(self, path, description):
        return {"path": path, "package": "tooling", "role": "r", "description": description}

    def base(self, rows, overlay=()):
        doc = {"schemaVersion": 1, "standing": "s", "packages": [{"id": "tooling", "dependencies": []}],
               "pendingDecisions": [], "files": by_path([self.row(p, d) for p, d in rows.items()])}
        inv0 = self.write("inv0.json", doc, indent=2)
        overlay_pins = [self.write(p, {"overlay": p}) for p in overlay]
        source = self.write("source.json", {"files": [inv0, *overlay_pins]})
        app = self.write("application.json", {"files": [], "designSubject": source})
        review = self.write("review.json", {"verdict": "ACCEPT", "subjectManifestSha256": app["sha256"], "newMustIssues": [], "newShouldIssues": []})
        activation = self.write("activation.json", {"applicationManifest": app, "independentApplicationReview": review})
        assent = self.write("assent.json", {"authority": {"rootApplicationAssent": True}, "subjectManifestSha256": app["sha256"], "review": review})
        completion = self.write("completion.json", {"designApprovedForImplementation": True, "passed": True, "applicationManifest": app, "activation": activation, "actualClaudeApplicationReview": review, "codexApplicationAssent": assent})
        self.lock = {"schemaVersion": 4, "architectureRepository": "fixture",
                     "approvals": dict(sourceManifest=source, applicationManifest=app, activation=activation, applicationReview=review, rootAssent=assent, completion=completion),
                     "inputs": [inv0], "inventorySuccessors": [], "contractSuccessors": [], "inventoryPassageInheritance": []}
        self.inv = [inv0]
        return inv0

    def hop(self, added, parent=None, candidate_path=None, append=True):
        parent = parent or self.inv[-1]
        n = len(self.lock["inventorySuccessors"]) + 1
        doc = json.loads((self.root / parent["path"]).read_bytes())
        doc["files"] = by_path(doc["files"] + [self.row(p, d) for p, d in added.items()])
        cand = self.write(candidate_path or f"inv{n}.json", doc, indent=2) if added is not None else parent
        rec = self.write(f"inv-record{n}.json", {"parent": parent, "candidate": cand, "parentArtifactBytesUnchanged": True, "inheritedRowsEqualByValue": True})
        subject = hashlib.sha256(f"inventory-subject-{n}".encode()).hexdigest()
        rev = self.write(f"inv-review{n}.json", {"verdict": "ACCEPT-UNIT", "requiredFindings": [], "subjectManifestSha256": subject,
                                                 "inventoryCandidateAssessment": {**cand, "verdict": "ACCEPT", "requiredFindings": [], "parent": parent, "successorRecord": rec}})
        ass = self.write(f"inv-assent{n}.json", {"status": "ACCEPTED-UNIT", "rootSubstantiveAssent": True, "requiredUnitFindings": [],
                                                 "actualClaudeReview": rev, "acceptedInventory": cand, "subjectManifest": {"sha256": subject}})
        binding = dict(parent=parent, candidate=cand, record=rec, review=rev, assent=ass)
        if not append:
            return binding
        self.lock["inventorySuccessors"].append(binding)
        self.inv.append(cand)
        return cand

    def rebind_hop(self, parent, candidate):
        """Rebind an inventory binding for an existing candidate pin (no file rewrite)."""
        n = len(self.lock["inventorySuccessors"]) + 1
        rec = self.write(f"inv-record{n}.json", {"parent": parent, "candidate": candidate, "parentArtifactBytesUnchanged": True, "inheritedRowsEqualByValue": True})
        subject = hashlib.sha256(f"inventory-subject-{n}".encode()).hexdigest()
        rev = self.write(f"inv-review{n}.json", {"verdict": "ACCEPT-UNIT", "requiredFindings": [], "subjectManifestSha256": subject,
                                                 "inventoryCandidateAssessment": {**candidate, "verdict": "ACCEPT", "requiredFindings": [], "parent": parent, "successorRecord": rec}})
        ass = self.write(f"inv-assent{n}.json", {"status": "ACCEPTED-UNIT", "rootSubstantiveAssent": True, "requiredUnitFindings": [],
                                                 "actualClaudeReview": rev, "acceptedInventory": candidate, "subjectManifest": {"sha256": subject}})
        binding = dict(parent=parent, candidate=candidate, record=rec, review=rev, assent=ass)
        self.lock["inventorySuccessors"].append(binding)
        return binding

    def contract(self, parents, overrides=(), members=None):
        n = len(self.lock["contractSuccessors"]) + 1
        if members is None:
            members = [self.write(f"c{n}/member.json", {"unit": n})]
        rec = self.write(f"c{n}/record.json", {"schemaVersion": 1, "parents": by_path(copy.deepcopy(parents)),
                                               "candidates": by_path(copy.deepcopy(members)), "passageOverrides": copy.deepcopy(list(overrides))})
        man = self.write(f"c{n}/manifest.json", {"files": by_path([rec, *members])})
        rev = self.write(f"c{n}/review.json", {"verdict": "ACCEPT-DESIGN-UNIT", "requiredFindings": [], "subjectManifestSha256": man["sha256"]})
        ass = self.write(f"c{n}/assent.json", {"status": "ACCEPTED-DESIGN-UNIT", "rootSubstantiveAssent": True, "requiredUnitFindings": [],
                                               "actualClaudeReview": rev, "subjectManifest": man, "acceptedSuccessor": rec})
        self.lock["contractSuccessors"].append(dict(record=rec, subjectManifest=man, review=rev, assent=ass))
        return {"members": members, "record": rec}

    def line_of(self, pin, needle):
        lines = (self.root / pin["path"]).read_text().splitlines()
        matches = [i for i, line in enumerate(lines) if needle in line]
        assert len(matches) == 1, matches
        return matches[0] + 1, lines[matches[0]]


def ov(parent, index, before, after):
    return {"parent": parent, "selector": {"jsonPointer": f"/files/{index}/description"}, "before": before, "after": after}


def pointer(parent, value, before, after):
    return {"parent": parent, "selector": {"jsonPointer": value}, "before": before, "after": after}


def proj(final, index, before, after):
    return ov(final, index, before, after)


ROWS = {"b.py": "B0", "d.py": "D0"}  # inv0: b=0 d=1


def single_hop(fx):
    inv0 = fx.base(ROWS)
    i1 = fx.hop({"c.py": "C0"})  # i1: b=0 c=1 d=2
    return inv0, i1


def two_hops(fx):
    inv0, i1 = single_hop(fx)
    i2 = fx.hop({"a.py": "A0"})  # i2: a=0 b=1 c=2 d=3
    return inv0, i1, i2


CASES = {}


def case(name, expect, pattern=None):
    def register(fn):
        CASES[name] = (fn, expect, pattern)
        return fn
    return register


@case("C01 single-hop inheritance reindexes by stable path", "PASS")
def c01(fx):
    inv0, i1 = single_hop(fx)
    fx.contract([inv0], [ov(inv0, 1, "D0", "D1")])
    fx.lock["inventoryPassageInheritance"] = [proj(i1, 2, "D0", "D1")]

    def check(result):
        assert result["inventoryPassageInheritance"][0]["selector"] == {"jsonPointer": "/files/2/description"}
        assert result["selectedInventory"] == i1
        raw = json.loads((fx.root / i1["path"]).read_bytes())
        assert raw["files"][2]["description"] == "D0", "final inventory bytes must stay historical"
    return check


@case("C02 inheritance omitted refuses", "DesignError", "passage inheritance differs")
def c02(fx):
    inv0, i1 = single_hop(fx)
    fx.contract([inv0], [ov(inv0, 1, "D0", "D1")])


@case("C03 inheritance with stale unshifted index refuses", "DesignError", "passage inheritance differs")
def c03(fx):
    inv0, i1 = single_hop(fx)
    fx.contract([inv0], [ov(inv0, 1, "D0", "D1")])
    fx.lock["inventoryPassageInheritance"] = [proj(i1, 1, "D0", "D1")]


@case("C03b inheritance naming ancestor parent pin refuses", "DesignError", "passage inheritance differs")
def c03b(fx):
    inv0, i1 = single_hop(fx)
    fx.contract([inv0], [ov(inv0, 1, "D0", "D1")])
    fx.lock["inventoryPassageInheritance"] = [proj(inv0, 2, "D0", "D1")]


@case("C04 direct identical final override needs no inheritance", "PASS")
def c04(fx):
    inv0, i1 = single_hop(fx)
    fx.contract([inv0, i1], [ov(inv0, 1, "D0", "D1"), ov(i1, 2, "D0", "D1")])


@case("C05 redundant inheritance beside direct identical override refuses", "DesignError", "passage inheritance differs")
def c05(fx):
    inv0, i1 = single_hop(fx)
    fx.contract([inv0, i1], [ov(inv0, 1, "D0", "D1"), ov(i1, 2, "D0", "D1")])
    fx.lock["inventoryPassageInheritance"] = [proj(i1, 2, "D0", "D1")]


@case("C06 inherited meaning conflicting with direct final override refuses", "DesignError", "conflicts with direct override")
def c06(fx):
    inv0, i1 = single_hop(fx)
    fx.contract([inv0], [ov(inv0, 1, "D0", "D1")])
    fx.contract([i1], [ov(i1, 2, "D0", "D2")])
    fx.lock["inventoryPassageInheritance"] = [proj(i1, 2, "D0", "D1")]


@case("C07 two-hop inheritance from base and intermediate ancestors", "PASS")
def c07(fx):
    inv0, i1, i2 = two_hops(fx)
    fx.contract([inv0], [ov(inv0, 1, "D0", "D1")])
    fx.contract([i1], [ov(i1, 0, "B0", "B1")])
    fx.lock["inventoryPassageInheritance"] = [proj(i2, 1, "B0", "B1"), proj(i2, 3, "D0", "D1")]

    def check(result):
        assert [r["selector"]["jsonPointer"] for r in result["inventoryPassageInheritance"]] == ["/files/1/description", "/files/3/description"]
        assert result["selectedInventory"] == i2
        assert len(result["inventorySuccessors"]) == 2
    return check


@case("C08 two-hop inheritance in non-canonical order refuses", "DesignError", "passage inheritance differs")
def c08(fx):
    inv0, i1, i2 = two_hops(fx)
    fx.contract([inv0], [ov(inv0, 1, "D0", "D1")])
    fx.contract([i1], [ov(i1, 0, "B0", "B1")])
    fx.lock["inventoryPassageInheritance"] = [proj(i2, 3, "D0", "D1"), proj(i2, 1, "B0", "B1")]


@case("C09 two ancestors with conflicting meanings for one row refuse", "DesignError", "inherited inventory passage meanings conflict")
def c09(fx):
    inv0, i1, i2 = two_hops(fx)
    fx.contract([inv0], [ov(inv0, 1, "D0", "D1")])
    fx.contract([i1], [ov(i1, 2, "D0", "D2")])
    fx.lock["inventoryPassageInheritance"] = [proj(i2, 3, "D0", "D2")]


@case("C09b conflicting ancestors refuse with other lock spelling", "DesignError", "inherited inventory passage meanings conflict")
def c09b(fx):
    inv0, i1, i2 = two_hops(fx)
    fx.contract([inv0], [ov(inv0, 1, "D0", "D1")])
    fx.contract([i1], [ov(i1, 2, "D0", "D2")])
    fx.lock["inventoryPassageInheritance"] = [proj(i2, 3, "D0", "D1")]


@case("C10 two ancestors with identical meaning collapse to one entry", "PASS")
def c10(fx):
    inv0, i1, i2 = two_hops(fx)
    fx.contract([inv0], [ov(inv0, 1, "D0", "D1")])
    fx.contract([i1], [ov(i1, 2, "D0", "D1")])
    fx.lock["inventoryPassageInheritance"] = [proj(i2, 3, "D0", "D1")]


@case("C11 ancestor /standing selector refuses as unsupported", "DesignError", "unsupported inherited inventory passage selector")
def c11(fx):
    inv0, i1 = single_hop(fx)
    fx.contract([inv0], [pointer(inv0, "/standing", "s", "t")])


@case("C12 ancestor line selector refuses as unsupported", "DesignError", "unsupported inherited inventory passage selector")
def c12(fx):
    inv0, i1 = single_hop(fx)
    number, line = fx.line_of(inv0, '"D0"')
    fx.contract([inv0], [{"parent": inv0, "selector": {"line": number}, "before": line, "after": line.replace("D0", "D1")}])


@case("C13 ancestor /files/N/path selector refuses as unsupported", "DesignError", "unsupported inherited inventory passage selector")
def c13(fx):
    inv0, i1 = single_hop(fx)
    fx.contract([inv0], [pointer(inv0, "/files/1/role", "r", "q")])


@case("C13b ancestor /packages/0/id selector refuses as unsupported", "DesignError", "unsupported inherited inventory passage selector")
def c13b(fx):
    inv0, i1 = single_hop(fx)
    fx.contract([inv0], [pointer(inv0, "/packages/0/id", "tooling", "host")])


@case("C14 non-description selector on final inventory is not inherited", "PASS")
def c14(fx):
    inv0, i1 = single_hop(fx)
    fx.contract([i1], [pointer(i1, "/standing", "s", "t")])


@case("C15 inheritance canonical order is lexicographic selector JSON", "PASS")
def c15(fx):
    rows = {f"r{i:02d}.py": f"R{i}" for i in range(11)}
    inv0 = fx.base(rows)
    i1 = fx.hop({"a.py": "A0"})
    fx.contract([inv0], [ov(inv0, 1, "R1", "X1"), ov(inv0, 9, "R9", "X9")])
    fx.lock["inventoryPassageInheritance"] = [proj(i1, 10, "R9", "X9"), proj(i1, 2, "R1", "X1")]


@case("C15b numeric inheritance order refuses", "DesignError", "passage inheritance differs")
def c15b(fx):
    rows = {f"r{i:02d}.py": f"R{i}" for i in range(11)}
    inv0 = fx.base(rows)
    i1 = fx.hop({"a.py": "A0"})
    fx.contract([inv0], [ov(inv0, 1, "R1", "X1"), ov(inv0, 9, "R9", "X9")])
    fx.lock["inventoryPassageInheritance"] = [proj(i1, 2, "R1", "X1"), proj(i1, 10, "R9", "X9")]


@case("C16 reordered inventory bindings refuse", "DesignError", "selected base input|immediate predecessor")
def c16(fx):
    inv0, i1, i2 = two_hops(fx)
    fx.contract([inv0])
    fx.lock["inventorySuccessors"].reverse()


@case("C17 inventory cycle back to earlier candidate refuses", "DesignError", "inventory candidate reuses an accepted path")
def c17(fx):
    inv0, i1, i2 = two_hops(fx)
    fx.rebind_hop(i2, i1)
    fx.contract([inv0])


@case("C18 inventory candidate at overlay-only accepted path refuses", "DesignError", "inventory candidate reuses an accepted path")
def c18(fx):
    fx.base(ROWS, overlay=["overlay.json"])
    fx.hop({"c.py": "C0"}, candidate_path="overlay.json")
    fx.contract([fx.inv[0]])


@case("C19 contract member at overlay-only accepted path refuses", "DesignError", "contract candidate reuses an accepted path")
def c19(fx):
    inv0 = fx.base(ROWS, overlay=["overlay.json"])
    fx.hop({"c.py": "C0"})
    fx.contract([inv0], members=[fx.write("overlay.json", {"new": True})])


@case("C20 contract member at selected inventory candidate path refuses", "DesignError", "contract candidate reuses an accepted path")
def c20(fx):
    inv0, i1 = single_hop(fx)
    fx.contract([inv0], members=[i1])


@case("C21 contract member reusing earlier contract member refuses", "DesignError", "contract candidate reuses an accepted path")
def c21(fx):
    inv0, i1 = single_hop(fx)
    first = fx.contract([inv0])
    fx.contract([inv0], members=first["members"])


@case("C21b contract member reusing earlier contract record refuses", "DesignError", "contract candidate reuses an accepted path")
def c21b(fx):
    inv0, i1 = single_hop(fx)
    first = fx.contract([inv0])
    fx.contract([inv0], members=[first["record"]])


@case("C22 base, intermediate, final and earlier contract pins remain parents", "PASS")
def c22(fx):
    inv0, i1, i2 = two_hops(fx)
    first = fx.contract([inv0])
    fx.contract([inv0, i1, i2, first["record"], *first["members"]])


@case("C23 contract forward/cyclic parent refuses", "DesignError", "not an accepted base")
def c23(fx):
    inv0, i1 = single_hop(fx)
    later_member = fx.write("c2/member.json", {"unit": 2})
    fx.contract([later_member])
    fx.contract([inv0])


@case("C24 identical passage override in two contracts is accepted once", "PASS")
def c24(fx):
    inv0, i1 = single_hop(fx)
    fx.contract([i1], [ov(i1, 2, "D0", "D1")])
    fx.contract([i1], [ov(i1, 2, "D0", "D1")])


@case("C25 ADVISORY line/pointer alias with different meaning on final inventory verifies", "PASS")
def c25(fx):
    inv0, i1 = single_hop(fx)
    number, line = fx.line_of(i1, '"D0"')
    fx.contract([i1], [ov(i1, 2, "D0", "D1")])
    fx.contract([i1], [{"parent": i1, "selector": {"line": number}, "before": line, "after": line.replace("D0", "D2")}])


@case("C26 non-list inheritance refuses", "DesignError", "passage inheritance differs")
def c26(fx):
    inv0, i1 = single_hop(fx)
    fx.contract([inv0])
    fx.lock["inventoryPassageInheritance"] = {}


@case("C26b extra inheritance entry without reviewed override refuses", "DesignError", "passage inheritance differs")
def c26b(fx):
    inv0, i1 = single_hop(fx)
    fx.contract([inv0])
    fx.lock["inventoryPassageInheritance"] = [proj(i1, 2, "D0", "D1")]


@case("C26c missing inheritance field refuses", "DesignError", "unsupported design lock")
def c26c(fx):
    inv0, i1 = single_hop(fx)
    fx.contract([inv0])
    del fx.lock["inventoryPassageInheritance"]


@case("C27 unhashable inventory candidate path fails closed but uncontrolled", "TypeError")
def c27(fx):
    inv0 = fx.base(ROWS)
    binding = fx.hop({"c.py": "C0"}, append=False)
    binding["candidate"] = {**binding["candidate"], "path": [binding["candidate"]["path"]]}
    fx.lock["inventorySuccessors"].append(binding)
    fx.contract([inv0])


@case("C27b non-object inventory chain entry refuses", "DesignError", "inventory chain binding must be an object")
def c27b(fx):
    inv0, i1 = single_hop(fx)
    fx.contract([inv0])
    fx.lock["inventorySuccessors"].append([])


@case("C28 non-object contract chain entry refuses", "DesignError", "four closed")
def c28(fx):
    inv0, i1 = single_hop(fx)
    fx.contract([inv0])
    fx.lock["contractSuccessors"].append([])


@case("C29 second hop parent pin with other digest refuses", "DesignError", "immediate predecessor")
def c29(fx):
    inv0, i1 = single_hop(fx)
    binding = fx.hop({"a.py": "A0"}, parent={**i1, "sha256": "0" * 64}, append=False)
    fx.lock["inventorySuccessors"].append(binding)
    fx.contract([inv0])


def v3_from_v4(fx, version):
    lock = fx.lock
    new = {k: lock[k] for k in ("architectureRepository", "approvals", "inputs")}
    new["schemaVersion"] = version
    if version >= 2:
        new["inventorySuccessor"] = lock["inventorySuccessors"][0]
    if version == 3:
        new["contractSuccessor"] = lock["contractSuccessors"][0]
    fx.lock = new


for version in (1, 2, 3):
    def make(version):
        def fn(fx):
            inv0, i1 = single_hop(fx)
            fx.contract([inv0], [ov(inv0, 1, "D0", "D1")])
            v3_from_v4(fx, version)
        return fn
    case(f"C30 compatibility v{version} lock still verifies", "PASS")(make(version))


@case("C31 v3 lock carrying v4 fields refuses", "DesignError", "unsupported design lock")
def c31(fx):
    inv0, i1 = single_hop(fx)
    fx.contract([inv0])
    chains = copy.deepcopy(fx.lock)
    v3_from_v4(fx, 3)
    fx.lock["inventorySuccessors"] = chains["inventorySuccessors"]


@case("C31b v4 lock carrying singular v3 slot refuses", "DesignError", "unsupported design lock")
def c31b(fx):
    inv0, i1 = single_hop(fx)
    fx.contract([inv0])
    fx.lock["inventorySuccessor"] = fx.lock["inventorySuccessors"][0]


for bad in (5, 4.0, True, "4"):
    def make(bad):
        def fn(fx):
            inv0, i1 = single_hop(fx)
            fx.contract([inv0])
            fx.lock["schemaVersion"] = bad
        return fn
    case(f"C32 schemaVersion {bad!r} refuses", "DesignError", "unsupported design lock")(make(bad))


def run(module_path):
    module = load(module_path)
    results = []
    for name, (fn, expect, pattern) in CASES.items():
        import re
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fx(tmp)
            check = fn(fx)
            try:
                result = module.verify(fx.root, fx.lock)
                kind, message = "PASS", None
                if callable(check):
                    try:
                        check(result)
                    except AssertionError as exc:
                        kind, message = "PASS-CHECK-FAILED", str(exc)
            except module.DesignError as exc:
                kind, message = "DesignError", str(exc)
            except Exception as exc:  # noqa: BLE001 - classify uncontrolled failures
                kind, message = type(exc).__name__, str(exc)
        ok = kind == expect and (pattern is None or kind == "PASS" or re.search(pattern, message or ""))
        results.append({"case": name, "expected": expect, "pattern": pattern, "actual": kind, "message": message, "met": bool(ok)})
    return results


if __name__ == "__main__":
    results = run(sys.argv[1])
    if len(sys.argv) > 2:
        Path(sys.argv[2]).write_text(json.dumps(results, indent=2) + "\n")
    for row in results:
        print(("ok   " if row["met"] else "MISS ") + row["case"] + f" -> {row['actual']}: {row['message']}")
    print(f"{sum(r['met'] for r in results)}/{len(results)} expectations met")
    sys.exit(0 if all(r["met"] for r in results) else 1)
