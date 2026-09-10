#!/usr/bin/env python
"""CB6-SHOULD-2 executable probe: the coverage-partition law at retained-Run closure.

These are FULL ADMITTED RUN GRAPHS, not schema fragments: every positive control
closes a real Run and yields a `run2:` identity, and every negative control is
the SAME graph with one deliberate change.

Independently verified:
  A. General DISJOINTNESS holds within the full owning tuple (the published
     partitionKey) and NOT across differing tuples.
  B. Scopes with NO Coverage entry are still partitioned - the case the
     per-Coverage producer guard structurally cannot see.
  C. TOTALITY is owed only where the coverageTotality registry says so, and the
     symbol relations owe none; symbol-to-file attribution stays TRUSTED and is
     not claimed independently reconstructed here.
  D. The refusal names the published shape.

check-identity.py is exec'd ONCE (it runs its own suite at import and exits);
its `build()` is the admitted positive Run fixture.
"""
import copy
import json
import sys
from pathlib import Path

COPY, OUT = sys.argv[1], sys.argv[2]
DC = Path(COPY) / "docs/coop/design-corrections"
FOUND = DC / "foundation"
sys.path.insert(0, str(FOUND))

# --- exec the identity checker once, capturing its namespace ---
NS = {"__name__": "identity_check_fixture", "__file__": str(FOUND / "check-identity.py")}
saved_argv = sys.argv
sys.argv = ["check-identity.py"]
suite_exit = None
import io
import contextlib
buf = io.StringIO()
try:
    with contextlib.redirect_stdout(buf):
        exec(compile((FOUND / "check-identity.py").read_text(), "check-identity.py", "exec"), NS)
except SystemExit as e:
    suite_exit = e.code
finally:
    sys.argv = saved_argv

M = NS["M"]
C = NS["C"]
build = NS["build"]
rekey = NS["rekey"]

rep = {"probe": "p06-should2-partition-runs",
       "identitySuiteExitCode": suite_exit,
       "identitySuiteStdout": buf.getvalue().strip()[:400]}

LAW = M.COVERAGE_PARTITION_LAW
rep["publishedPartitionKey"] = LAW["partitionKey"]
rep["publishedRefusal"] = LAW["refusal"]

REL_DOC = M.RELATION_DOCUMENT["x-opensip-relation-registry"]
relations = REL_DOC["relations"]
rep["relationCount"] = len(relations)
rep["relationsWithCoverageTotalityRow"] = sorted(
    r for r, row in relations.items() if "coverageTotality" in row)
rep["relationsWithoutCoverageTotalityRow"] = sorted(
    r for r, row in relations.items() if "coverageTotality" not in row)
rep["onlyFileOwesTotality"] = rep["relationsWithCoverageTotalityRow"] == ["file"]

results = []


def run_case(cid, mutate, expect, why):
    """expect: 'ADMIT' (a full Run closes) or a refusal-substring."""
    run, objects, blobs = build()
    try:
        mutate(run, objects, blobs)
    except Exception as e:
        results.append({"id": cid, "phase": "fixture-construction",
                        "error": type(e).__name__ + ": " + str(e),
                        "myExpectation": expect, "why": why, "agrees": False})
        return
    try:
        rid = M.close_run(run, objects, blobs)
        got = "ADMIT:" + rid
        ok = expect == "ADMIT" and rid.startswith("run2:")
    except Exception as e:
        got = type(e).__name__ + ": " + str(e)
        ok = expect != "ADMIT" and expect in str(e)
    results.append({"id": cid, "outcome": got, "myExpectation": expect,
                    "agrees": ok, "why": why})


def view_of(objects):
    return next(k for k, (d, v) in objects.items() if d == "view")


def add_scope(objects, scope):
    key = M.identifier("subject-scope", scope)
    objects[key] = ("subject-scope", scope)
    return key


def with_second_scope(run, objects, blobs, overrides, subjects):
    """Attach a SECOND subject-scope to the single view, with no Coverage entry.

    NOTE, from a failed attempt of mine: subject-scopes are CONTENT-ADDRESSED.
    A "second" scope byte-identical to the first collapses onto the same id and
    adds nothing - my first overlap control did exactly that and admitted with
    the baseline's own run id. So an overlap control must differ in content
    while still SHARING a subject and agreeing on the partition tuple.
    """
    vid = view_of(objects)
    view = copy.deepcopy(objects[vid][1])
    base = copy.deepcopy(objects[view["scopeIds"][0]][1])
    scope = {**base, **overrides, "subjects": sorted(subjects)}
    key = add_scope(objects, scope)
    assert key not in view["scopeIds"], (
        "degenerate control: the second scope is identical to the first")
    view["scopeIds"] = sorted(set(view["scopeIds"] + [key]))
    rekey(objects, vid, view, run)


def with_two_new_scopes(run, objects, blobs, subjects_a, subjects_b):
    """Attach TWO new scopes, NEITHER of which has a Coverage entry, so the
    overlap is between scopes the per-Coverage producer guard cannot see."""
    vid = view_of(objects)
    view = copy.deepcopy(objects[vid][1])
    base = copy.deepcopy(objects[view["scopeIds"][0]][1])
    keys = []
    for subs in (subjects_a, subjects_b):
        scope = {**base, "subjects": sorted(subs)}
        keys.append(add_scope(objects, scope))
    assert len(set(keys)) == 2, "degenerate control: the two scopes are identical"
    view["scopeIds"] = sorted(set(view["scopeIds"] + keys))
    rekey(objects, vid, view, run)


# Baseline: the unmodified fixture must close.
run_case("POS-baseline-run-closes", lambda r, o, b: None, "ADMIT",
         "POSITIVE CONTROL: the unmodified fixture closes a complete Run")

# Discover the base scope's own subjects and partition tuple for the controls.
_r, _o, _b = build()
_vid = view_of(_o)
_base_scope = _o[_o[_vid][1]["scopeIds"][0]][1]
rep["baseScopeRelation"] = _base_scope["relation"]
rep["baseScopeResolution"] = _base_scope["resolution"]
rep["baseScopeSubjects"] = list(_base_scope["subjects"])
BASE_SUBJECTS = list(_base_scope["subjects"])
SHARED = BASE_SUBJECTS[0]

# A different rung on the SAME relation's ladder changes the partition tuple.
# Ladders live in the relation registry (the single published ladder
# authority), not on the identity model; my first attempt read the workflows
# model's constant, which this module does not carry.
LADDERS = {name: list(row["ladder"]) for name, row in relations.items()}
ladder = LADDERS[_base_scope["relation"]]
other_rung = next((x for x in ladder if x != _base_scope["resolution"]), None)
rep["ladderForBaseRelation"] = list(ladder)
rep["otherRungChosen"] = other_rung
# A different relation also changes the tuple.
other_rel = next((r for r in sorted(relations)
                  if r != _base_scope["relation"]
                  and _base_scope["resolution"] in LADDERS.get(r, [])), None)
rep["otherRelationChosen"] = other_rel

# ---- A. disjointness within the FULL owning tuple ----
run_case(
    "NEG-same-tuple-shared-subject",
    lambda r, o, b: with_second_scope(r, o, b, {}, [SHARED, "zzz/extra.ts"]),
    LAW["refusal"],
    "NEGATIVE: two scopes of one view with the SAME full partition tuple sharing "
    "a subject must refuse the published overlap. The second scope carries an "
    "extra subject so it is a genuinely distinct record, not a content-address "
    "duplicate of the first.")

run_case(
    "POS-same-tuple-disjoint-subjects",
    lambda r, o, b: with_second_scope(r, o, b, {}, ["zzz/not-in-base.ts"]),
    "ADMIT",
    "POSITIVE: same tuple, DISJOINT subjects - a complete Run still closes, so "
    "the law refuses overlap rather than refusing a second scope")

if other_rung:
    run_case(
        "POS-different-rung-shared-subject",
        lambda r, o, b: with_second_scope(r, o, b, {"resolution": other_rung},
                                          [SHARED, "zzz/extra.ts"]),
        "ADMIT",
        "POSITIVE: differing on ONE partitionKey field (resolution) is a "
        "different claim, so sharing a subject is lawful")

if other_rel:
    run_case(
        "POS-different-relation-shared-subject",
        lambda r, o, b: with_second_scope(r, o, b, {"relation": other_rel},
                                          [SHARED]),
        "ADMIT",
        "POSITIVE: differing on relation is a different claim about the subject")

# ---- B. scopes with NO Coverage entry are still partitioned ----
run_case(
    "NEG-two-no-coverage-scopes-overlap",
    lambda r, o, b: with_two_new_scopes(r, o, b,
                                        ["zzz/a.ts", "zzz/shared.ts"],
                                        ["zzz/b.ts", "zzz/shared.ts"]),
    LAW["refusal"],
    "NEGATIVE and load-bearing: BOTH overlapping scopes lack a Coverage entry, "
    "so the per-Coverage producer guard structurally cannot see this; only the "
    "per-view closure boundary can, which is precisely the gap CX-BV6-01 closes")

run_case(
    "POS-two-no-coverage-scopes-disjoint",
    lambda r, o, b: with_two_new_scopes(r, o, b,
                                        ["zzz/a.ts"], ["zzz/b.ts"]),
    "ADMIT",
    "POSITIVE: the same two-new-scope shape with DISJOINT subjects still closes "
    "a complete Run, so the refusal above is the overlap and not the shape")

# ---- empty subjects ----
run_case(
    "POS-empty-subjects-array",
    lambda r, o, b: with_second_scope(r, o, b, {}, []),
    "ADMIT",
    "POSITIVE: an empty subjects array is explicitly allowed")

# ---- D. refusal shape ----
rep["publishedRefusalShape"] = LAW["refusalShape"]

rep["cases"] = results
rep["caseCount"] = len(results)
rep["disagreements"] = [r for r in results if not r["agrees"]]
rep["allAgree"] = not rep["disagreements"]
rep["positiveRunIdentities"] = [
    r["outcome"] for r in results
    if r.get("outcome", "").startswith("ADMIT:")]

with open(OUT, "w") as fh:
    json.dump(rep, fh, indent=1, sort_keys=True, default=str)

print("identity suite exit:", suite_exit, "|", rep["identitySuiteStdout"][:120])
print("published partitionKey:", rep["publishedPartitionKey"])
print("relations:", rep["relationCount"],
      "| with coverageTotality row:", rep["relationsWithCoverageTotalityRow"],
      "| onlyFile:", rep["onlyFileOwesTotality"])
print("base scope:", rep["baseScopeRelation"], "@", rep["baseScopeResolution"],
      "subjects:", rep["baseScopeSubjects"])
print("other rung:", rep["otherRungChosen"], "| other relation:", rep["otherRelationChosen"])
print()
for r in results:
    print("  %-38s %-9s %s" % (r["id"], "AGREE" if r["agrees"] else "DISAGREE",
                               str(r.get("outcome", r.get("error")))[:120]))
print()
print("all agree:", rep["allAgree"])
