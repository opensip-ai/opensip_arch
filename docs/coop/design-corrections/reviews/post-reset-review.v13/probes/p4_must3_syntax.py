#!/usr/bin/env python
"""CB3-MUST-3 + ADV-3 independent probe.

I re-derive the released-v2 root counterexamples myself and assert on them
independently of the subject's own check names. Where a control can only be run
at the helper level I say so explicitly rather than reporting it as a Run result,
because the coauthor record itself flags that helper checks assume complete
Coverage.

Structure:
  A. Is the "compiler-free repository" claim true of the actual snapshot/Plan?
  B. Root counterexample 1  -- pure Markdown `declares` fact.
  C. Root counterexample 2  -- COMPLETE empty declares/clones Coverage.
  D. Root counterexample 3  -- code grammar minting references@resolved-binding
                               and claiming complete empty reference Coverage.
  E. Healthy syntax clone Coverage must carry NO Rust ownership cause.
  F. Selected-row suffix ownership (.ts legal, .tsx unowned refused).
  G. A non-TS/JS/Rust bundled DATA grammar Run exercising its published
     capability, plus malformed/foreign/missing/cross-language variants.
  H. Existing TS/Rust behaviour must remain valid.
"""
import copy
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

R = []


def rec(case, expect, got, cause=None, level="run-admission", detail=None):
    R.append({"case": case, "level": level, "expected": expect,
              "observed": got, "cause": cause, "detail": detail,
              "agrees": expect == got})


def syntax_graph(relation, path, has_match, resolved=True):
    return F.build(resolved=resolved, has_match=has_match,
                   universe_language="syntax", relation=relation,
                   source_path=path, pure_syntax=True)


def close(case, relation, path, has_match, expect, resolved=True,
          want_cause=None):
    try:
        graph = syntax_graph(relation, path, has_match, resolved)
    except Exception as exc:
        # A constructor that refuses is NOT an admission result; label it.
        rec(case, expect, "construction-refused", str(exc)[:160],
            level="fixture-construction")
        return None
    try:
        rid = M.close_run(*graph)
        rec(case, expect, "admits", None)
        return None
    except Exception as exc:
        cause = str(exc)[:200]
        ok = "refuses"
        if want_cause and not cause.startswith(want_cause):
            ok = "refuses-wrong-cause"
        rec(case, expect, ok, cause)
        return cause


def coverage_entry(relation, path, has_match, resolved=True):
    run, objects, blobs = syntax_graph(relation, path, has_match, resolved)
    key = next(v["payloadDigest"] for k, (d, v) in objects.items()
               if d == "coverage")
    return C.parse(blobs[key])["entry"]


def inject(relation, path, mutate, resolved=False):
    run, objects, blobs = syntax_graph(relation, path, False, resolved)
    key = next(k for k, (d, v) in objects.items() if d == "coverage")
    coverage = copy.deepcopy(objects[key][1])
    payload = C.parse(blobs[coverage["payloadDigest"]])
    mutate(payload["entry"])
    coverage["payloadDigest"] = F.put_blob(blobs, payload)
    F.rekey(objects, key, coverage, run)
    F.resync_witness(objects, blobs, run)
    return M.close_run(run, objects, blobs)


def inject_case(case, relation, path, mutate, want_cause):
    try:
        inject(relation, path, mutate)
        rec(case, "refuses", "admits", None)
    except Exception as exc:
        cause = str(exc)[:200]
        rec(case, "refuses",
            "refuses" if cause.startswith(want_cause) else "refuses-wrong-cause",
            cause)


def main():
    # ---- A. Is the compiler-free claim actually true of the snapshot? -----
    run, objects, blobs = syntax_graph("file", "docs/guide.md", True, False)
    plan = objects[run["planId"]][1]
    snap = objects[plan["snapshotId"]][1]
    inv = sorted(r["path"] for r in snap["sourceInventory"])
    compiler_fixtures = [p for p in inv if Path(p).name in
                         ("Cargo.toml", "Cargo.lock", "tsconfig.json",
                          "package.json", "package-lock.json",
                          "tsconfig.base.json", "tsconfig.strict.json")
                         or p.endswith(".cargo/config.toml")]
    rec("A/snapshot-omits-compiler-context-fixtures", [], compiler_fixtures,
        detail=inv, level="snapshot-inspection")
    rec("A/plan-names-exactly-one-native-context", 1,
        len(plan.get("nativeContextDigests", [])), level="plan-inspection")
    rec("A/grammar-only-repository-closes-a-complete-run", "admits",
        "admits" if M.close_run(run, objects, blobs).startswith("run2:")
        else "no", level="run-admission")

    # ---- B. Root counterexample 1: Markdown `declares` fact. -------------
    close("B/root-cx1-markdown-declares-fact", "declares", "README.md", True,
          "refuses", want_cause="SYNTAX_CAPABILITY_UNSUPPORTED_FACT:")

    # ---- C. Root counterexample 2: COMPLETE empty declares/clones. -------
    for rel in ("declares", "clones"):
        e = None
        try:
            e = coverage_entry(rel, "README.md", False)
        except Exception as exc:
            rec(f"C/root-cx2-{rel}-empty-entry", "entry", "error",
                str(exc)[:150], level="producer")
        if e is not None:
            rec(f"C/root-cx2-{rel}-empty-scope-is-not-complete", "unknown",
                e.get("coverage"), level="producer-disclosure",
                detail=json.dumps(e))
            rec(f"C/root-cx2-{rel}-empty-scope-published-pair",
                ["language-tier-unsupported", "capability-missing"],
                [e.get("deficiency"), e.get("nativeCause")],
                level="producer-disclosure")
        inject_case(f"C/root-cx2-{rel}-injected-false-complete", rel,
                    "README.md",
                    lambda x: x.update(coverage="complete", deficiency=None,
                                       nativeCause=None),
                    "SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE:")

    # ---- D. Root counterexample 3: semantic rungs under a syntax universe.
    for rel in ("references", "imports", "calls", "types", "reachability"):
        close(f"D/root-cx3-{rel}-semantic-fact", rel, "src/plain.rs", True,
              "refuses", want_cause="SYNTAX_CAPABILITY_UNSUPPORTED_FACT:")
    e = coverage_entry("references", "src/plain.rs", False)
    rec("D/root-cx3-references-empty-scope-is-not-complete", "unknown",
        e.get("coverage"), level="producer-disclosure", detail=json.dumps(e))
    inject_case("D/root-cx3-injected-false-complete-references", "references",
                "src/plain.rs",
                lambda x: x.update(coverage="complete", deficiency=None,
                                   nativeCause=None),
                "SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE:")
    inject_case("D/root-cx3-injected-null-cause", "references",
                "src/plain.rs", lambda x: x.update(nativeCause=None),
                "SYNTAX_CAPABILITY_CAUSE_MISMATCH:")
    inject_case("D/root-cx3-injected-wrong-cause", "references",
                "src/plain.rs",
                lambda x: x.update(nativeCause="no-program-unit"),
                "SYNTAX_CAPABILITY_CAUSE_MISMATCH:")
    inject_case("D/root-cx3-injected-wrong-deficiency", "references",
                "src/plain.rs",
                lambda x: x.update(deficiency="budget-exhausted"),
                "SYNTAX_CAPABILITY_DEFICIENCY_MISMATCH:")

    # ---- E. Healthy syntax clone Coverage owes no Rust ownership cause. --
    for rel in ("declares", "clones"):
        e = coverage_entry(rel, "src/plain.rs", True)
        rec(f"E/healthy-syntax-{rel}-is-a-real-complete", ["complete", None, None],
            [e.get("coverage"), e.get("deficiency"), e.get("nativeCause")],
            level="producer-disclosure")
        rec(f"E/healthy-syntax-{rel}-carries-no-rust-ownership-cause", True,
            e.get("nativeCause") is None
            or "ownership" not in str(e.get("nativeCause")),
            level="producer-disclosure")

    # ---- F. Selected-row suffix ownership. -------------------------------
    reg = N.GRAMMAR_CAPABILITY_REGISTRY["languages"]

    def row(lang, suffixes):
        return {"grammarId": lang + ".v1", "grammarVersion": "1.0.0",
                "languageId": lang, "syntaxClass": reg[lang]["syntaxClass"],
                "suffixes": sorted(suffixes, key=lambda x: x.encode()),
                "grammarDigest": "a" * 64}

    checks_f = [
        ("F/ts-row-owning-only-.ts-supports-.ts", [row("typescript", [".ts"])],
         "a.ts", True),
        ("F/ts-row-owning-only-.ts-REFUSES-.tsx", [row("typescript", [".ts"])],
         "a.tsx", False),
        ("F/ts-row-owning-.tsx-supports-.tsx",
         [row("typescript", [".ts", ".tsx"])], "a.tsx", True),
        ("F/unselected-grammar-lends-no-capability",
         [row("markdown", [".md"])], "src/plain.rs", False),
        ("F/foreign-suffix-resolves-to-no-row",
         [row("typescript", [".ts"])], "a.py", False),
        ("F/anchorless-fact-is-not-vacuously-supported",
         [row("rust", [".rs"])], None, False),
    ]
    for case, rows, path, supported in checks_f:
        paths = [] if path is None else [path]
        got = N.syntax_capability_support(rows, "declares", "syntactic",
                                          paths, True)
        rec(case, "supported" if supported else "unsupported",
            "supported" if got is None else "unsupported",
            None if got is None else str(got)[:120],
            level="helper (assumes complete Coverage; not Run admission)")

    # ---- G. Data-grammar (non TS/JS/Rust) published capability. ----------
    data_paths = {"markdown": "docs/guide.md", "json": "data/settings.json",
                  "yaml": "config/app.yaml", "toml": "build/opts.toml"}
    for lang, p in sorted(data_paths.items()):
        close(f"G/data-grammar-inventory-{lang}", "file", p, True, "admits",
              resolved=False)
        close(f"G/data-grammar-declares-refused-{lang}", "declares", p, True,
              "refuses", want_cause="SYNTAX_CAPABILITY_UNSUPPORTED_FACT:")
    # A path no bundled grammar reads must still inventory.
    close("G/nonparseable-path-still-inventories", "file", "vendor/blob.bin",
          True, "admits", resolved=False)
    close("G/foreign-language-path-still-inventories", "file", "scripts/x.py",
          True, "admits", resolved=False)

    # ---- H. Compiler universes retain full capability. -------------------
    for lang in ("typescript", "rust"):
        for rel in ("references", "imports", "calls", "types", "reachability",
                    "declares", "clones", "file"):
            try:
                rid = M.close_run(*F.build(resolved=True, has_match=True,
                                           universe_language=lang,
                                           relation=rel))
                rec(f"H/compiler-universe-retains-{lang}.{rel}", "admits",
                    "admits" if rid.startswith("run2:") else "no")
            except Exception as exc:
                rec(f"H/compiler-universe-retains-{lang}.{rel}", "admits",
                    "refuses", str(exc)[:150])

    bad = [r for r in R if not r["agrees"]]
    print(json.dumps({"total": len(R), "disagreeingCount": len(bad),
                      "disagreeing": bad, "results": R}, indent=2))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
