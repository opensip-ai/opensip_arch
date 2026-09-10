#!/usr/bin/env python
"""CB3-MUST-3: subjectKind extent law -- README-only and MIXED code/data clone
scopes, and an independent assessment of the coarser symbol-attribution limit.

The published law (relation registry subjectKindLaw, enforced in
syntax_capability_prerequisite) is asymmetric:

  source-path relations (file, vcs-change, clones)
      extent = the scope's OWN subjects, and EVERY one must be supported
      (require_all=True) -- a mixed scope cannot hide an unsupported member.

  symbol relations (declares, literal, control-flow, ... )
      extent = the whole committed snapshot inventory, ANY member suffices
      (require_all=False), because a SubjectIdV1 is opaque and the
      enumerator's symbol-to-file attribution is trusted, not re-derivable.

I test both halves at the scope boundary, and I probe the coarser limit's
actual boundary rather than accepting the prose: I check whether the symbol
path can be used to launder an unsupported FACT (it must not, because facts are
judged require_all=True on their own anchors).
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
N = load("nat", HERE / "native/native_evidence_model.v2.py")
REG = json.loads((HERE / "foundation/relation-payload-schemas.v2.json")
                 .read_text())["x-opensip-relation-registry"]["relations"]

R = []


def rec(case, expect, got, detail=None, level="helper"):
    R.append({"case": case, "level": level, "expected": expect,
              "observed": got, "detail": detail, "agrees": expect == got})


def rows_all():
    reg = N.GRAMMAR_CAPABILITY_REGISTRY["languages"]
    return [{"grammarId": l + ".v1", "grammarVersion": "1.0.0",
             "languageId": l, "syntaxClass": r["syntaxClass"],
             "suffixes": sorted(r["suffixes"], key=lambda x: x.encode()),
             "grammarDigest": "a" * 64}
            for l, r in sorted(reg.items())]


def supported(rows, relation, rung, paths, require_all):
    return N.syntax_capability_support(rows, relation, rung, paths,
                                       require_all) is None


def main():
    ROWS = rows_all()

    # ---- subjectKind declarations are what the law keys on. -------------
    kinds = {k: v.get("subjectKind") for k, v in REG.items()}
    rec("subjectKind/source-path-relations",
        {"clones", "file", "vcs-change"},
        {k for k, v in kinds.items() if v == "source-path"},
        detail=json.dumps(kinds), level="registry")

    # ---- source-path extent: EVERY named path must be supported. --------
    CODE, DATA = "src/plain.rs", "README.md"
    rec("clones/code-only-scope-supported", True,
        supported(ROWS, "clones", "normalized-body-hash", [CODE], True))
    rec("clones/README-only-scope-unsupported", False,
        supported(ROWS, "clones", "normalized-body-hash", [DATA], True))
    rec("clones/MIXED-code-and-data-scope-unsupported", False,
        supported(ROWS, "clones", "normalized-body-hash", [CODE, DATA], True),
        detail="a mixed scope must not hide its unsupported member behind the "
               "supported one")
    rec("clones/MIXED-order-independent", False,
        supported(ROWS, "clones", "normalized-body-hash", [DATA, CODE], True))
    # file inventory is never grammar-gated, so the same mixed scope is fine.
    rec("file/MIXED-scope-still-inventories", True,
        supported(ROWS, "file", "enumerated", [CODE, DATA, "vendor/blob.bin"],
                  True))

    # ---- symbol extent: the coarser trusted-enumerator limit. ------------
    # In a MIXED snapshot the coarser question is satisfied by ANY supported
    # member. That is the stated weakening; I record its exact shape.
    mixed_inventory = [DATA, "data/settings.json", CODE]
    data_only_inventory = [DATA, "data/settings.json"]
    rec("declares/symbol-extent-mixed-snapshot-supported", True,
        supported(ROWS, "declares", "syntactic", mixed_inventory, False),
        detail="ANY supported member suffices for an opaque-symbol scope")
    rec("declares/symbol-extent-data-only-snapshot-unsupported", False,
        supported(ROWS, "declares", "syntactic", data_only_inventory, False),
        detail="the limit is coarse, not vacuous: a data-only repository still "
               "refuses")
    rec("declares/symbol-extent-empty-inventory-unsupported", False,
        supported(ROWS, "declares", "syntactic", [], False),
        detail="an empty extent is not vacuously supported")

    # ---- Does the coarser scope limit let an unsupported FACT through? ---
    # This is the question that decides whether the limit is sound. Facts are
    # judged require_all=True on their OWN anchors, so a Markdown-anchored
    # declares fact must refuse even in a MIXED snapshot that also contains
    # a .rs file. Run-admission level, not helper level.
    def close(relation, path, has_match, resolved=True):
        try:
            return None, M.close_run(*F.build(
                resolved=resolved, has_match=has_match,
                universe_language="syntax", relation=relation,
                source_path=path, pure_syntax=True))
        except Exception as exc:
            return str(exc)[:200], None

    cause, rid = close("declares", DATA, True)
    rec("FACT/markdown-anchored-declares-refuses-in-mixed-snapshot",
        "refuses", "refuses" if rid is None else "admits", detail=cause,
        level="run-admission")
    rec("FACT/refusal-is-the-typed-capability-cause", True,
        bool(cause and cause.startswith("SYNTAX_CAPABILITY_UNSUPPORTED_FACT:")),
        detail=cause, level="run-admission")
    cause2, rid2 = close("declares", CODE, True)
    rec("FACT/code-anchored-declares-admits-in-same-snapshot", "admits",
        "admits" if rid2 else "refuses", detail=cause2, level="run-admission")

    # ---- The fact-level anchor law is require_all as well. ---------------
    rec("FACT/anchor-extent-mixed-anchors-unsupported", False,
        supported(ROWS, "declares", "syntactic", [CODE, DATA], True),
        detail="a fact anchored to both a code and a data file is unsupported")

    bad = [r for r in R if not r["agrees"]]
    print(json.dumps({"total": len(R), "disagreeingCount": len(bad),
                      "disagreeing": bad, "results": R}, indent=2,
                     default=list))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
