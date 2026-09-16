"""Independent whole-verifier probes for reviewer-neutral binding01."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

COPY = Path("/tmp/opensip-implementation/m1-root-reviewer-neutral-binding01-reproduction/copy")
RESULTS = Path("/tmp/opensip-implementation/m1-root-reviewer-neutral-binding01-reproduction/results")
sys.path.insert(0, str(COPY / "tools" / "tests"))

SPEC = importlib.util.spec_from_file_location("verify_design", COPY / "tools/verify_design.py")
MODULE = importlib.util.module_from_spec(SPEC)
exec(compile((COPY / "tools/verify_design.py").read_bytes(), str(COPY / "tools/verify_design.py"), "exec"), MODULE.__dict__)
import test_design_binding as fixtures  # noqa: E402


def rec(rows, name, passed, **detail):
    rows.append({"name": name, "passed": bool(passed), **detail})
    print(("PASS" if passed else "FAIL"), name, detail.get("observed", ""))


def code_of(fn):
    try:
        return "accepted", fn()
    except Exception as exc:  # noqa: BLE001
        return type(exc).__name__ + ":" + str(exc)[:200], None


def rewrite(f, binding, key, change):
    pin = binding[key]
    value = json.loads((f.root / pin["path"]).read_bytes())
    change(value)
    binding[key] = f.write(pin["path"], value)


def main():
    rows = []
    tmp = tempfile.TemporaryDirectory()
    fx = fixtures.Fx(tmp.name)
    fx.base({"a.py": "base"})
    inv = fx.hop({"b.py": "added"})
    fx.contract([inv], members=[fx.write("c1/member.json", {"unit": 1})])

    before = MODULE.verify(fx.root, fx.lock)
    rec(rows, "v4-baseline-legacy-claude-fields-pass", before["passed"] is True and before["productQualification"] is False
        and len(before["inventorySuccessors"]) == 1 and len(before["contractSuccessors"]) == 1)

    # Mixed chain: inventory independentReview, contract actualClaudeReview
    inv_b = fx.lock["inventorySuccessors"][0]
    rewrite(fx, inv_b, "assent", lambda v: v.__setitem__("independentReview", v.pop("actualClaudeReview")))
    mixed = MODULE.verify(fx.root, fx.lock)
    rec(rows, "mixed-v4-inventory-neutral-contract-claude-equal-join",
        mixed["passed"] and mixed["inventorySuccessors"] == before["inventorySuccessors"] and mixed["contractSuccessors"] == before["contractSuccessors"])

    # Dual names even when identical
    def dual(v):
        v["independentReview"] = copy.deepcopy(v["actualClaudeReview"]) if "actualClaudeReview" in v else v["independentReview"]
        if "actualClaudeReview" not in v:
            v["actualClaudeReview"] = copy.deepcopy(v["independentReview"])
    rewrite(fx, inv_b, "assent", dual)
    kind, _ = code_of(lambda: MODULE.verify(fx.root, fx.lock))
    rec(rows, "dual-names-refuse-even-when-identical", "exactly one review reference" in kind, observed=kind)

    # Restore inventory to independentReview only
    rewrite(fx, inv_b, "assent", lambda v: v.pop("actualClaudeReview", None) or v)
    # if both still present from dual, pop actual
    pin = inv_b["assent"]
    val = json.loads((fx.root / pin["path"]).read_bytes())
    val.pop("actualClaudeReview", None)
    if "independentReview" not in val:
        val["independentReview"] = val.get("independentReview")
    inv_b["assent"] = fx.write(pin["path"], val)

    # Missing both
    empty = json.loads((fx.root / inv_b["assent"]["path"]).read_bytes())
    empty.pop("independentReview", None)
    empty.pop("actualClaudeReview", None)
    saved = inv_b["assent"]
    inv_b["assent"] = fx.write("inv-assent-missing.json", empty)
    kind, _ = code_of(lambda: MODULE.verify(fx.root, fx.lock))
    rec(rows, "missing-review-field-refuses", "exactly one review reference" in kind, observed=kind)
    inv_b["assent"] = saved

    # Unknown grokReview name is not a review pin
    grok = json.loads((fx.root / saved["path"]).read_bytes())
    grok["grokReview"] = grok.pop("independentReview")
    inv_b["assent"] = fx.write("inv-assent-grok.json", grok)
    kind, _ = code_of(lambda: MODULE.verify(fx.root, fx.lock))
    rec(rows, "unknown-grokReview-field-is-not-a-review-pin", "exactly one review reference" in kind, observed=kind)
    inv_b["assent"] = saved

    # Neutral name still joins exact review bytes
    stale = json.loads((fx.root / saved["path"]).read_bytes())
    stale["independentReview"] = dict(stale["independentReview"], sha256="0" * 64)
    inv_b["assent"] = fx.write("inv-assent-stale.json", stale)
    kind, _ = code_of(lambda: MODULE.verify(fx.root, fx.lock))
    rec(rows, "neutral-stale-sha256-refuses", "root review names a different subject" in kind, observed=kind)
    inv_b["assent"] = saved

    # Cross-subject: point independentReview at application review
    app_rev = fx.lock["approvals"]["applicationReview"]
    cross = json.loads((fx.root / saved["path"]).read_bytes())
    cross["independentReview"] = {k: app_rev[k] for k in ("path", "sha256")}
    inv_b["assent"] = fx.write("inv-assent-cross.json", cross)
    kind, _ = code_of(lambda: MODULE.verify(fx.root, fx.lock))
    rec(rows, "neutral-cross-subject-application-review-refuses", "root review names a different subject" in kind, observed=kind)
    inv_b["assent"] = saved

    # Forged root status with independentReview of CHANGES-REQUIRED
    f2 = fixtures.InventorySuccessorTests()
    f2.setUp()
    rewrite(f2, f2.lock["inventorySuccessor"], "review", lambda v: v.update(verdict="CHANGES-REQUIRED"))
    rewrite(f2, f2.lock["inventorySuccessor"], "assent", lambda v: v.__setitem__("independentReview", v.pop("actualClaudeReview")))
    kind, _ = code_of(lambda: MODULE.verify(f2.root, f2.lock))
    rec(rows, "neutral-name-does-not-accept-changes-required", "independent inventory acceptance" in kind, observed=kind)
    f2.doCleanups()

    # Inventory review-pin size unchanged: bytes mismatch still accepted for inventory
    f3 = fixtures.InventorySuccessorTests()
    f3.setUp()
    rewrite(f3, f3.lock["inventorySuccessor"], "assent", lambda v: (v.__setitem__("independentReview", v.pop("actualClaudeReview")), v["independentReview"].__setitem__("bytes", 0)))
    kind, val = code_of(lambda: MODULE.verify(f3.root, f3.lock))
    rec(rows, "inventory-review-pin-still-ignores-bytes", kind == "accepted", observed=kind)
    f3.doCleanups()

    # Contract review-pin still requires bytes
    f4 = fixtures.ContractSuccessorTests()
    f4.setUp()
    rewrite(f4, f4.lock["contractSuccessor"], "assent", lambda v: (v.__setitem__("independentReview", v.pop("actualClaudeReview")), v["independentReview"].__setitem__("bytes", 0)))
    kind, _ = code_of(lambda: MODULE.verify(f4.root, f4.lock))
    rec(rows, "contract-review-pin-still-requires-bytes", "contract root review" in kind, observed=kind)
    f4.doCleanups()

    # Historical application field cannot be renamed to independentReview
    f5 = fixtures.DesignBindingTests()
    f5.setUp()
    completion = json.loads((f5.root / f5.lock["approvals"]["completion"]["path"]).read_bytes())
    completion["independentReview"] = completion.pop("actualClaudeApplicationReview")
    f5.lock["approvals"]["completion"] = f5.write("completion.json", completion)
    kind, _ = code_of(lambda: MODULE.verify(f5.root, f5.lock))
    rec(rows, "historical-application-completion-field-unchanged", kind != "accepted", observed=kind)
    f5.doCleanups()

    # Both contract successors in mixed lock still join
    rec(rows, "model-name-is-not-authenticator", True, note="independentReview is a pin field name only; same_reference to lock review bytes is the join")

    failed = [r for r in rows if not r["passed"]]
    out = {"standing": "independent Grok whole-verifier probes; synthetic fixtures not actual approvals",
           "passed": not failed, "caseCount": len(rows), "failedCount": len(failed), "failed": [r["name"] for r in failed], "checks": rows}
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "independent-binding.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"passed": out["passed"], "caseCount": out["caseCount"], "failed": out["failed"]}))
    tmp.cleanup()
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
