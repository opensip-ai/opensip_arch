#!/usr/bin/env python3
"""Assemble the v2 changed-file-handoff.json from the preserved BEFORE/AFTER images."""
from __future__ import annotations

import difflib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1 = Path("/tmp/opensip-design-corrections/claude-execution-account-author.v1")

PURPOSE = {
    "docs/coop/design-corrections/foundation/execution_inputs_model.v1.py": {
        "findings": ["DRAFT-P1", "DRAFT-P2", "candidate-carrier"],
        "purpose": "(P1) `_outcome_from_items` stops taking items[0] and takes the FIRST source that "
                   "actually carries a typed pair, so an earlier untyped missing-work source no "
                   "longer masks a later real carrier; (null, null) is still the answer when none "
                   "does. (P2) `derive_outcome`'s docstring and the new `SOURCE_ORDER` table "
                   "publish the cross-source order with its authority per leg. "
                   "(candidate) the candidate branch stops substituting `_binding_carrier`'s "
                   "`provider-unavailable` default; new `_declared_binding_carrier` reads the "
                   "binding's own declared pair with no default, and the branch falls to "
                   "(null, null). `_binding_carrier` itself is untouched.",
        "measuredDelta": "4 of 11 enumerated source shapes change their ROW pair; every state, "
                         "every inputRefs list and every nativeCauses list is unchanged; source "
                         "items change only in the two candidate shapes, which is the point of the "
                         "candidate correction (probes/q5).",
    },
    "docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md": {
        "findings": ["DRAFT-P1", "DRAFT-P2", "candidate-carrier"],
        "purpose": "§4 no longer delegates whole-row ordering to §5. It gains the normative "
                   "cross-source order table (binding/enumerator, inventories in canonical-set "
                   "`inventoryDigests` order, candidate, then accounts in the AUTHORED matrix "
                   "`relations` array order, §5 partition order inside each), a statement that the "
                   "order is owner-derived and not the host's `nativeCoverageAccounts` sequence, "
                   "the explicit no-masking rule, and the candidate no-manufacture clause with the "
                   "enumeration guards that keep `_binding_carrier`'s default unreachable.",
    },
    "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json": {
        "findings": ["DRAFT-P2", "candidate-carrier"],
        "purpose": "Annotations only. `x-opensip-derived-carrier-law` gains `crossSourceOrder` "
                   "(naming the authority for each leg, that the matrix arrays are authored and "
                   "not lexical, and that the host account array order is not read) and "
                   "`candidateCarrier`; `primaryPair` gains the no-masking sentence.",
    },
    "docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md": {
        "findings": ["candidate-carrier", "F4-qualification"],
        "purpose": "§9.6's candidate row now states the same no-manufacture rule and that a "
                   "required cell with no envelope refuses before the bridge. A new paragraph "
                   "records ON THE RECORD that this table previously PRESCRIBED the "
                   "`provider-unavailable` fallback, so the v1 change was resolving a contradiction "
                   "between two normative owners - not merely a reference-side invention, which is "
                   "how the historical diagnosis characterised it.",
    },
    "docs/coop/design-corrections/foundation/evaluator_graph_fixture.v3.py": {
        "findings": ["DRAFT-P1"],
        "purpose": "One keyword-only, default-OFF option `package_coverage_unknown`: mints the "
                   "required package partition as the producer helper's own honest UNKNOWN answer "
                   "(the helper DERIVES budget-exhausted/null for that non-resolved rung and the "
                   "native owner admits it). With `file_coverage_subjects` it produces the "
                   "discriminating shape - untyped file account owed BEFORE a typed package "
                   "account - on an admitted fixture that also closes a full Run. 12 existing "
                   "caller shapes verified byte-identical (probes/q5).",
    },
    "docs/coop/design-corrections/foundation/check-execution-inputs.v1.py": {
        "findings": ["DRAFT-P1", "DRAFT-P2", "reporting-standing", "independence-claim",
                     "control-naming", "candidate-carrier"],
        "purpose": "Reporting: every control now declares a `controlStanding` "
                   "(admission / closed-run / helper-unit / schema-unit); non-admission controls "
                   "report null for the admission columns instead of an invented complete cell; "
                   "`full_run_case` returns the REAL same-graph admission rows and cross-checks "
                   "them against the proof by bridging with §9.6 step 3. "
                   "`rebuild_after_object_mutation`'s independence claim is corrected to reference "
                   "self-consistency. `optional-unsupported-cell-does-not-execute-a-provider` is "
                   "renamed `optional-unsupported-cell-owes-no-required-cell-row` and qualified. "
                   "New controls: mixed-account first-typed-pair (admission + closed Run), "
                   "absent-candidate-envelope null pair, required-candidate still refuses, plus "
                   "oracles that the published order tables match the reference and that no "
                   "control invents an admission row. 71 -> 75 cases.",
    },
}


def main() -> int:
    before = {r["path"]: r for r in json.loads((HERE / "before-hashes.json").read_text())}
    after = {r["path"]: r for r in json.loads((HERE / "after-hashes.json").read_text())}
    v1_after = {r["path"]: r for r in json.loads((V1 / "after-hashes.json").read_text())}
    changed, unchanged = [], []
    for path in before:
        b, a = before[path], after[path]
        row = {
            "path": path,
            "v1HandoffSha256": v1_after.get(path, {}).get("sha256"),
            "v2BeforeSha256": b["sha256"], "v2BeforeBytes": b["bytes"],
            "v2AfterSha256": a["sha256"], "v2AfterBytes": a["bytes"],
            "v2BeforeEqualsV1Handoff": b.get("equalsV1After"),
            "beforeImage": b["image"], "afterImage": a["image"],
        }
        if b["sha256"] == a["sha256"]:
            row["status"] = "unchanged-in-v2"
            unchanged.append(row)
            continue
        bl = Path(b["image"]).read_text().splitlines(keepends=True)
        al = Path(a["image"]).read_text().splitlines(keepends=True)
        diff = list(difflib.unified_diff(bl, al, n=0))
        row["addedLines"] = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
        row["removedLines"] = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))
        row["status"] = "changed-in-v2"
        row.update(PURPOSE[path])
        changed.append(row)

    tree = json.loads((HERE / "tree-delta.json").read_text())
    out = {
        "standing": "Bounded FOLLOW-UP source authorship (v2) on the same isolated exact32 "
                    "successor copy. NOT acceptance, NOT independent design or blind acceptance, "
                    "NOT product qualification. No frozen/live edit, no pin or planning edit, no "
                    "product implementation, no commit, no push. The v1 runtime and every v1 report "
                    "and image are preserved unchanged; all v2 output is under this runtime.",
        "respondsTo": [
            "root-execution-account-draft-review.v1/assessment.md (DRAFT-P1, DRAFT-P2, editorial)",
            "root-execution-account-draft-review.v2/assessment.md (reporting scope, independence "
            "claim, control naming, F4 qualification)",
            "root-execution-account-draft-review.v1/primary-pair-probe.json",
        ],
        "base": json.loads(Path("/tmp/opensip-design-corrections/execution-account-successor.v1/"
                                "base-custody.json").read_text()),
        "v2BeforeIsV1Handoff": all(r.get("equalsV1After") for r in before.values()),
        "beforeImagesPreservedIn": str(HERE / "before"),
        "afterImagesPreservedIn": str(HERE / "after"),
        "changedInV2": sorted(changed, key=lambda r: r["path"]),
        "unchangedInV2": sorted(unchanged, key=lambda r: r["path"]),
        "changedInV2Count": len(changed),
        "wholeTree": {
            "files": tree["frozen"]["files"],
            "changedVsFrozen32": tree["changedCount"],
            "added": tree["addedFiles"], "removed": tree["removedFiles"],
            "newFilesTouchedInV2BeyondV1": tree["newFilesTouchedInV2BeyondV1"],
        },
        "noNewFileOwnership": "v2 touched NO file beyond the nine v1 already named; three of those "
                              "nine are byte-unchanged since the v1 handoff.",
        "deliberatelyNotTouched": [
            "foundation/evaluator3-source-pins.v1.json and foundation/source-pins.v1.json - "
            "authoritative ledgers, read only. Both remain stale for exactly the same nine files. "
            "Root performs all authoritative pin/planning rebinds on final bytes.",
            "foundation/execution_inputs_model.v1.py `_binding_carrier` - its provider-unavailable "
            "default is preserved. Root's bounded assessment is confirmed by direct reading: "
            "enumeration_model.v1.py:679-683 refuses an unselected enumerator on an available "
            "binding or a required cell, and :752-754 refuses a null-universe binding whose "
            "deficiency is null, so on a lawful plan that default is unreachable and a real typed "
            "binding pair is what the unselected / null-U branches consume.",
            "foundation/evaluator_input_model.v3.py:136-144 - an inventory of the rule's subject "
            "kind in ANOTHER cell contributing to that rule's enumeration completeness is existing, "
            "deliberately conservative behaviour across all kind-matching inventories in the mode "
            "domain. Left unchanged and described as existing behaviour, NOT as a proved gap; the "
            "v1 optional-unselected control already avoids the interaction by using a symbol-kind "
            "cell against a file-kind rule.",
            "foundation/check-execution-replay.v3.py, check-composition.v3.py, "
            "evaluator_semantic_fixture.v3.py - unchanged, and green in the focused run.",
            "Every consumer/blind artefact, every other owner's admission boundary, and every "
            "historical review folder including the entire v1 runtime.",
        ],
    }
    (HERE / "changed-file-handoff.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "changedInV2Count": out["changedInV2Count"],
        "changed": [{"path": r["path"], "+": r["addedLines"], "-": r["removedLines"]}
                    for r in out["changedInV2"]],
        "unchangedInV2": [r["path"] for r in out["unchangedInV2"]],
        "wholeTree": out["wholeTree"],
        "v2BeforeIsV1Handoff": out["v2BeforeIsV1Handoff"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
