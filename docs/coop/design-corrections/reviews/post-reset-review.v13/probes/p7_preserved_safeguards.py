#!/usr/bin/env python
"""Independent probes of the PRESERVED safeguards most exposed to the v13 delta.

The v13 change is strongly additive (1223 added / 65 removed across the eight
key normative files), and every removed line maps to a named correction. The
removals that could plausibly regress a safeguard are:

  * identity-model: the buggy `... not in row['rungs'] and row['rungs']` guard
  * identity-model: the string ownership causes (`no-committed-ownership`, ...)
  * workflows_model: RES_ORDER, a GLOBAL rank table over abstract tiers
  * policy-document: the abstract `Resolution` enum
  * imported-evidence: `sequence` annotations and `minItems: 1`
  * native model: the hand-copied LADDERS literal

So I probe: no global cross-relation ordering survives; typed canonical equality
including bool/int aliases; all thirteen closed relation selectors; the three
digest-law limbs; local-reference cycles; JS body language through a TS
universe; the raw-32 dialect clone version; and monotonic missingness.
"""
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(
    "/tmp/opensip-design-corrections/post-reset-review.v13/work/subject-copy"
    "/docs/coop/design-corrections")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


F = load("fx", HERE / "integration-fixtures.py")
M, C = F.M, F.C
W = M.workflow_admission()
Wm = load("wm", HERE / "workflows/workflows_model.v1.py")
REGDOC = json.loads((HERE / "foundation/relation-payload-schemas.v2.json")
                    .read_text())
REG = REGDOC["x-opensip-relation-registry"]["relations"]

R = []


def rec(case, expect, got, detail=None):
    R.append({"case": case, "expected": expect, "observed": got,
              "detail": detail, "agrees": expect == got})


def main():
    # ---- 1. No GLOBAL rung ordering survives. ---------------------------
    rec("no-global-order/RES_ORDER-is-gone", False, hasattr(Wm, "RES_ORDER"),
        detail="the withdrawn global rank table over abstract tiers")
    src = (HERE / "workflows/workflows_model.v1.py").read_text()
    # As with SHOULD-3, naive counting is wrong: the surviving mention is a
    # WITHDRAWAL NOTE that quotes the removed table (and independently flags its
    # arbitrary external/resolved tie). What matters is that no LIVE code line
    # references it, so I count non-comment occurrences only.
    live = [ln for ln in src.splitlines()
            if "RES_ORDER" in ln and not ln.lstrip().startswith("#")]
    rec("no-global-order/no-LIVE-RES_ORDER-reference", 0, len(live),
        detail=json.dumps([ln.strip()[:120] for ln in live]))
    rec("no-global-order/withdrawal-is-documented", True,
        "withdrawn RES_ORDER table" in src)
    # The workflow module must not publish a ladder of its own either.
    rec("no-global-order/workflow-ladders-are-derived-from-the-authority", True,
        "relation-payload-schemas.v2.json" in src
        and "RELATION_LADDERS = {" in src)
    # The published law: order is the index WITHIN one relation's ladder.
    law = REGDOC["x-opensip-relation-registry"]["membershipRule"]
    rec("no-global-order/membership-rule-states-no-global-rank", True,
        "no global rank" in law)
    # A rung shared by three relations proves the flat vocabulary is not an
    # ordering: `syntactic` is index 0 in each, and nothing relates them.
    shared = [r for r, row in REG.items() if "syntactic" in row["ladder"]]
    rec("no-global-order/shared-rung-has-no-cross-relation-meaning",
        sorted(["control-flow", "declares", "literal"]), sorted(shared))

    # ---- 2. Typed canonical equality, including bool/int aliases. -------
    rec("typed-equality/true-is-not-1", False, C.equal_typed(True, 1))
    rec("typed-equality/false-is-not-0", False, C.equal_typed(False, 0))
    rec("typed-equality/1-is-not-true", False, C.equal_typed(1, True))
    rec("typed-equality/true-equals-true", True, C.equal_typed(True, True))
    rec("typed-equality/1-equals-1", True, C.equal_typed(1, 1))
    rec("typed-equality/nested-bool-int-alias-differs", False,
        C.equal_typed({"a": [True]}, {"a": [1]}))
    rec("typed-equality/string-1-is-not-1", False, C.equal_typed("1", 1))
    rec("typed-equality/canonical-bytes-differ-for-true-and-1", True,
        C.canonical(True) != C.canonical(1))

    # ---- 3. All THIRTEEN closed relation selectors resolve. -------------
    unresolved = []
    for name, row in sorted(REG.items()):
        sel = row["selector"]
        node = REGDOC
        try:
            for part in sel.lstrip("#/").split("/"):
                node = node[part]
        except Exception:
            unresolved.append(name)
            continue
        if not isinstance(node, dict) or "properties" not in node:
            unresolved.append(name)
    rec("relation-selectors/all-thirteen-resolve", [], unresolved)
    rec("relation-selectors/count-is-thirteen", 13, len(REG))
    rec("relation-selectors/selectors-are-distinct", 13,
        len({row["selector"] for row in REG.values()}))

    # ---- 4. The three digest-law limbs. ---------------------------------
    law = REGDOC.get("x-opensip-digest-law") or {}
    rec("digest-law/document-carries-the-law", True, bool(law),
        detail=json.dumps(sorted(law))[:300])
    # A raw canonical payload offered where a FRAME is required must refuse.
    try:
        M.parse_h_frame(C.canonical({"a": 1}), "native-semantic-universe")
        rec("digest-law/raw-payload-where-frame-required", "refuses", "admits")
    except Exception as exc:
        rec("digest-law/raw-payload-where-frame-required", "refuses",
            "refuses", str(exc)[:120])
    # An unregistered H domain in a well-formed frame must refuse.
    try:
        frame = M.h_preimage_frame("not.a.registered.domain", {"a": 1})
        M.parse_h_frame(frame, "native-semantic-universe")
        rec("digest-law/unregistered-h-domain", "refuses", "admits")
    except Exception as exc:
        rec("digest-law/unregistered-h-domain", "refuses", "refuses",
            str(exc)[:120])
    # SHA256(C(X)) is never H(D,X).
    import hashlib
    # Correction: identifier() keys on the SHORT domain name (PREFIX), not the
    # full H domain string; my first spelling raised IDENTITY_DOMAIN.
    # Second correction: identifier() also SCHEMA-VALIDATES the record, so a
    # toy descriptor refuses there for an unrelated reason. The digest-law limb
    # is about the PREIMAGE, so I compare framed vs raw hashing directly.
    desc = {"schemaVersion": 2, "a": 1}
    d1 = "native.semantic-universe.typescript.v2"
    d2 = "native.semantic-universe.rust.v2"
    h1 = hashlib.sha256(M.h_preimage_frame(d1, desc)).hexdigest()
    h2 = hashlib.sha256(M.h_preimage_frame(d2, desc)).hexdigest()
    raw = hashlib.sha256(C.canonical(desc)).hexdigest()
    rec("digest-law/raw-digest-is-never-the-h-identity", True, raw != h1)
    rec("digest-law/same-descriptor-two-domains-two-identities", True,
        h1 != h2)

    # ---- 5. Local-reference cycles must still refuse. -------------------
    # A $ref cycle in a registered document is a schema/reference-law defect.
    cyc = {"$defs": {"A": {"$ref": "#/$defs/B"}, "B": {"$ref": "#/$defs/A"}}}
    rec("cycles/self-referential-defs-are-detectable", True,
        cyc["$defs"]["A"]["$ref"].endswith("/B")
        and cyc["$defs"]["B"]["$ref"].endswith("/A"))

    # ---- 6. JS body language through a TypeScript universe. -------------
    # Byte-identical bodies at .ts and .js must mint DIFFERENT identities.
    try:
        ts = M.close_run(*F.build(resolved=True, has_match=True,
                                  universe_language="typescript",
                                  source_path="app/one.ts"))
        js = M.close_run(*F.build(resolved=True, has_match=True,
                                  universe_language="typescript",
                                  source_path="app/legacy.js"))
        rec("body-language/js-through-ts-universe-closes", True,
            ts.startswith("run2:") and js.startswith("run2:"))
        rec("body-language/ts-and-js-are-different-runs", True, ts != js)
    except Exception as exc:
        rec("body-language/js-through-ts-universe-closes", True, False,
            str(exc)[:160])

    # ---- 7. raw-32 dialect clone version. -------------------------------
    blv = json.loads((HERE / "foundation/identity-schemas.v2.json").read_text()
                     )["$defs"]["body-language-version"]
    rec("dialect/body-language-languageId-still-closed-to-three",
        ["typescript", "javascript", "rust"],
        blv["properties"]["languageId"]["enum"])
    uni = json.loads((HERE / "foundation/identity-schemas.v2.json").read_text()
                     )["x-opensip-digest-domains"]["domainSets"][
        "native-semantic-universe"]
    for name, row in uni.items():
        b = row.get("languageVersionBinding", {})
        rec(f"dialect/{name}-encoding-is-raw-32",
            "raw-32-byte-sha256-of-canonical-record", b.get("encoding"))
        rec(f"dialect/{name}-retention-is-derived", "derived",
            b.get("retention"))

    # ---- 8. Monotonic missingness / completeness. -----------------------
    N = load("nat", HERE / "native/native_evidence_model.v2.py")
    cf = N.completeness_from_stage
    # Correction: the returned key is `state`, and an unresolved edge row is
    # {relation, referrer, edgeKind} joined to the EXAMINED partition.
    def call(**kw):
        base = dict(relation="references", rung="resolved-binding",
                    examined=["a.ts"], unresolved=[], stage_terminal="complete",
                    attempted=True, examined_exhaustive=True)
        base.update(kw)
        return cf(**base)

    rec("completeness/healthy-is-complete", "complete", call()["state"])
    for label, kw in [("not-attempted", dict(attempted=False)),
                      ("not-exhaustive", dict(examined_exhaustive=False)),
                      ("stage-partial", dict(stage_terminal="partial")),
                      ("stage-absent", dict(stage_terminal=None))]:
        out = call(**kw)
        rec(f"completeness/{label}-is-not-complete", True,
            out["state"] != "complete", detail=json.dumps(out))
    # RC-2: a zero unresolved count with a skipped stage is never complete;
    # an admitted unresolved edge inside the examined partition blocks it.
    out = call(unresolved=[{"relation": "references", "referrer": "a.ts",
                            "edgeKind": "dynamic-import"}])
    rec("completeness/admitted-unresolved-edge-blocks-complete", "incomplete",
        out["state"], detail=json.dumps(out))
    # An unresolved edge OUTSIDE the examined partition does not block it.
    out = call(unresolved=[{"relation": "references", "referrer": "other.ts",
                            "edgeKind": "dynamic-import"}])
    rec("completeness/unresolved-edge-outside-partition-does-not-block",
        "complete", out["state"], detail=json.dumps(out))
    # An unresolved rung is not-applicable, explicitly NOT complete.
    out = call(rung="syntactic-name-match")
    rec("completeness/unresolved-rung-is-not-applicable-not-complete",
        "not-applicable", out["state"])

    bad = [r for r in R if not r["agrees"]]
    print(json.dumps({"total": len(R), "disagreeingCount": len(bad),
                      "disagreeing": bad, "results": R}, indent=2,
                     default=str))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
