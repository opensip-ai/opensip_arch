#!/usr/bin/env python
"""CB3-MUST-5: the clone-ownership deficiency/cause derivation, probed with my
own ownership records.

clone_ownership_disclosure is the single place the pairing is decided, and the
Run guard (identity-model close_run) calls it with the COMMITTED ownership
record and THIS scope's own subjects, never with the claim being judged. So
exercising it exhaustively with records I construct is a direct test of the law.

The distinctions that matter, and that the finding was about:
  * missing / partial / ambiguous  -> each its OWN registered cause, never null
  * explicit target selection (not-compiled, not-selected) -> NOT a deficiency;
    a deliberate exclusion must not be slandered as an incomplete enumeration
  * out-of-selected-scope owners    -> must NOT manufacture false ambiguity
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


N = load("nat", HERE / "native/native_evidence_model.v2.py")
D = N.clone_ownership_disclosure
R = []


def rec(case, expect, got, detail=None):
    R.append({"case": case, "expected": expect, "observed": got,
              "detail": detail, "agrees": expect == got})


def cause(result):
    return None if result is None else result["nativeCause"]


def unit(uid, crate, edition=None):
    return {"unitId": uid, "crateName": crate, "targetEdition": edition}


def main():
    EDITIONS = {"cb-core": 2021, "cb-legacy": 2015}
    P = "crates/core/src/shared.rs"

    # ---- 1. no committed ownership at all --------------------------------
    rec("missing/no-ownership-record", "body-language-ownership-missing",
        cause(D(None, [P], EDITIONS)))

    # ---- 2. enumeration not complete -------------------------------------
    partial = {"enumeration": "partial", "units": [unit("u1", "cb-core")],
               "selectedUnitIds": ["u1"],
               "ownership": [{"path": P, "unitId": "u1"}]}
    rec("partial/enumeration-partial", "body-language-owner-unenumerated",
        cause(D(partial, [P], EDITIONS)))
    # checked BEFORE any row is read: even a scope naming no subject at all
    rec("partial/checked-before-rows-are-read",
        "body-language-owner-unenumerated", cause(D(partial, [], EDITIONS)))

    # ---- 3. healthy positive control -------------------------------------
    healthy = {"enumeration": "complete", "units": [unit("u1", "cb-core")],
               "selectedUnitIds": ["u1"],
               "ownership": [{"path": P, "unitId": "u1"}]}
    rec("healthy/single-selected-owner-owes-nothing", None,
        cause(D(healthy, [P], EDITIONS)))

    # ---- 4. ambiguity: two selected owners at different editions ---------
    ambiguous = {"enumeration": "complete",
                 "units": [unit("u1", "cb-core"), unit("u2", "cb-core", 2015)],
                 "selectedUnitIds": ["u1", "u2"],
                 "ownership": [{"path": P, "unitId": "u1"},
                               {"path": P, "unitId": "u2"}]}
    rec("ambiguous/two-selected-owners-disagree",
        "body-language-owner-ambiguous", cause(D(ambiguous, [P], EDITIONS)))

    # two selected owners that AGREE are not ambiguous
    agreeing = {"enumeration": "complete",
                "units": [unit("u1", "cb-core"), unit("u2", "cb-core", 2021)],
                "selectedUnitIds": ["u1", "u2"],
                "ownership": [{"path": P, "unitId": "u1"},
                              {"path": P, "unitId": "u2"}]}
    rec("healthy/two-selected-owners-agreeing-owe-nothing", None,
        cause(D(agreeing, [P], EDITIONS)))

    # ---- 5. unresolvable owner metadata ----------------------------------
    dangling = {"enumeration": "complete", "units": [],
                "selectedUnitIds": ["u1"],
                "ownership": [{"path": P, "unitId": "u1"}]}
    rec("ambiguous/owner-unit-record-missing",
        "body-language-owner-ambiguous", cause(D(dangling, [P], EDITIONS)))
    unknown_crate = {"enumeration": "complete",
                     "units": [unit("u1", "not-in-map")],
                     "selectedUnitIds": ["u1"],
                     "ownership": [{"path": P, "unitId": "u1"}]}
    rec("ambiguous/crate-absent-from-edition-map",
        "body-language-owner-ambiguous",
        cause(D(unknown_crate, [P], EDITIONS)))

    # ---- 6. explicit selection is NOT a deficiency ------------------------
    # not-compiled: the path has no ownership row at all.
    not_compiled = {"enumeration": "complete", "units": [unit("u1", "cb-core")],
                    "selectedUnitIds": ["u1"],
                    "ownership": [{"path": "other.rs", "unitId": "u1"}]}
    rec("selection/not-compiled-path-owes-nothing", None,
        cause(D(not_compiled, [P], EDITIONS)),
        detail="a path compiled by no selected target is a lawful per-body "
               "refusal, compatible with coverage=complete")
    # not-selected: owners exist but all lie OUTSIDE the selection, and they
    # disagree with each other. This must NOT manufacture ambiguity.
    not_selected = {"enumeration": "complete",
                    "units": [unit("u1", "cb-core"), unit("u2", "cb-legacy")],
                    "selectedUnitIds": [],
                    "ownership": [{"path": P, "unitId": "u1"},
                                  {"path": P, "unitId": "u2"}]}
    rec("selection/out-of-scope-owners-create-no-false-ambiguity", None,
        cause(D(not_selected, [P], EDITIONS)),
        detail="unselected owners disagreeing must not be read as ambiguity")
    # a selected owner plus a conflicting UNSELECTED one is still unambiguous
    mixed = {"enumeration": "complete",
             "units": [unit("u1", "cb-core"), unit("u2", "cb-legacy")],
             "selectedUnitIds": ["u1"],
             "ownership": [{"path": P, "unitId": "u1"},
                           {"path": P, "unitId": "u2"}]}
    rec("selection/unselected-conflicting-owner-is-ignored", None,
        cause(D(mixed, [P], EDITIONS)))

    # ---- 7. scope subjects decide, not the whole repository --------------
    # An ambiguous path OUTSIDE this scope's subjects must not taint it.
    other_ambiguous = {"enumeration": "complete",
                       "units": [unit("u1", "cb-core"),
                                 unit("u2", "cb-core", 2015)],
                       "selectedUnitIds": ["u1", "u2"],
                       "ownership": [{"path": "elsewhere.rs", "unitId": "u1"},
                                     {"path": "elsewhere.rs", "unitId": "u2"},
                                     {"path": P, "unitId": "u1"}]}
    rec("scope/ambiguity-outside-the-selected-scope-does-not-taint-it", None,
        cause(D(other_ambiguous, [P], EDITIONS)))
    rec("scope/that-same-record-IS-ambiguous-for-its-own-subject",
        "body-language-owner-ambiguous",
        cause(D(other_ambiguous, ["elsewhere.rs"], EDITIONS)))

    # ---- 8. the three causes are never null and always paired ------------
    for label, record, subj in [("missing", None, [P]),
                                ("partial", partial, [P]),
                                ("ambiguous", ambiguous, [P])]:
        out = D(record, subj, EDITIONS)
        rec(f"pairing/{label}-carries-a-nonnull-cause", True,
            out is not None and out["nativeCause"] is not None)
        rec(f"pairing/{label}-deficiency-is-input-closure-incomplete",
            "input-closure-incomplete", out["deficiency"])

    bad = [r for r in R if not r["agrees"]]
    print(json.dumps({"total": len(R), "disagreeingCount": len(bad),
                      "disagreeing": bad, "results": R}, indent=2))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
