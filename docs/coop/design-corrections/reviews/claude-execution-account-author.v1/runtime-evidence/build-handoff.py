#!/usr/bin/env python3
"""Assemble changed-file-handoff.json from the preserved BEFORE/AFTER images."""
from __future__ import annotations

import difflib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

PURPOSE = {
    "docs/coop/design-corrections/foundation/execution_inputs_model.v1.py": {
        "decisions": [1, 2, 4, 5],
        "purpose": "Reference admission. (D2) derived_applicability becomes an explicit FIRST-MATCH "
                   "order with unselected BEFORE null-universe, plus the APPLICABILITY_PRECEDENCE "
                   "table the schema annotation and the controls read. (D1) the account universe "
                   "selector becomes want_u = binding universe for every applicability, with the "
                   "external-join rationale in place. (D5) _primary_source_pair replaces the "
                   "`or \"provider-unavailable\"` fallback: the primary pair is the first retained "
                   "record that actually carries a typed pair, else explicit null/null; the "
                   "no-records branch derives null/null; the per-record requiredCellDeficiencies row "
                   "stops borrowing the account summary's deficiency for a record that has none.",
        "reachableBehaviourChange": "Applicability token for a lawful unselected binding "
                                    "(unavailable-null-universe -> unavailable-unselected); removal "
                                    "of the fabricated provider-unavailable carrier; primary pair now "
                                    "prefers a real typed record over a manufactured one. The "
                                    "sourceUniverse rule is a PUBLICATION: it agrees with the old "
                                    "expression on every lawful shape (probes/p8).",
    },
    "docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md": {
        "decisions": [1, 2, 3, 4, 5],
        "purpose": "Section 5 gains the normative FIRST-MATCH applicability table with the "
                   "sourceUniverse column and the reachability argument for unselected-before-null-U; "
                   "the external sourceUniverse join to EnumerationPlanV1 and the explicit statement "
                   "that JSON Schema cannot express it; the explicit non-constraint of targetUniverse; "
                   "the clause saying a selected-U UNSUPPORTED-TYPED cell's lawfully returned Coverage "
                   "stays retained/selected while the account names none of it, that derivedAccounts "
                   "and requiredCellDeficiencies (not the token alone) carry the disclosure, and that "
                   "a complete cell outcome means the account was answered rather than that the "
                   "capability became supported; and the derived-carrier clause (deterministic primary "
                   "pair, null/null for pure missing work, obligation kept through the proof bridge). "
                   "Section 4's primary-pair sentence is aligned with it.",
    },
    "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json": {
        "decisions": [1, 2, 4, 5],
        "purpose": "Annotations only; no type, enum, required or identity change. "
                   "NativeCoverageAccountV1 gains x-opensip-external-joins (publishing the "
                   "sourceUniverse join and the deliberately-unjoined targetUniverse) and "
                   "x-opensip-applicability-precedence (the first-match order); the document gains "
                   "x-opensip-derived-carrier-law. Per-field descriptions state the same. These "
                   "publish the external join instead of pretending a per-record schema compares an "
                   "external binding.",
    },
    "docs/coop/design-corrections/foundation/execution_inputs_fixture.v3.py": {
        "decisions": [1],
        "purpose": "The host-capture builder's mirror of the account universe rule becomes "
                   "sourceUniverse = binding universe for every applicability, with targetUniverse "
                   "documented as this fixture's own same-universe choice rather than a join. "
                   "Byte-neutral on every lawful shape, for the same reason as the model.",
    },
    "docs/coop/design-corrections/foundation/evaluator_graph_fixture.v3.py": {
        "decisions": [2, 3, 4, 5],
        "purpose": "Three keyword-only, default-OFF options so the controls run on GENUINE admitted "
                   "owner evidence rather than hand-made records: `unsupported_cell` "
                   "('required'/'optional') adds a selected-U references|syntax-only cell whose "
                   "unknown / language-tier-unsupported / capability-missing Coverage is DERIVED by "
                   "the native producer helper and admitted by admit_coverage_result_v3; "
                   "`optional_unselected_cell` adds the lawful optional-unselected binding shape of "
                   "enumeration-contract section 1; `file_coverage_subjects` narrows only the "
                   "returned partition's committed subjects so the expected-source census is short "
                   "while the partition stays honestly complete. Supporting change: cells are sorted "
                   "into the schema's required (capabilityId, languageMode, workspaceRoot) order and "
                   "cellOrdinal is read from that sorted map instead of a literal; "
                   "requestedCapabilities is canonicalised. Every existing caller is byte-identical "
                   "(probes/p9, 15 option shapes).",
    },
    "docs/coop/design-corrections/foundation/check-execution-inputs.v1.py": {
        "decisions": [1, 2, 3, 4, 5],
        "purpose": "New controls and oracles for all five decisions, including four FULL retained "
                   "Runs driven through the actual M.close_run on the same route "
                   "check-execution-replay.v3.py uses. Helper changes: "
                   "replace_file_view_with_one_subject gains complete/rebuild, and "
                   "rebuild_after_object_mutation gains an explicit view_ids override (with the "
                   "carried-ref filter that a retired view needs). 52 -> 71 cases.",
    },
    "docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md": {
        "decisions": [4, 5],
        "purpose": "Section 9.6's originating-refs table encoded the fabricated carrier in two rows "
                   "('empty returned partitions use provider-unavailable', and borrowing the account "
                   "summary deficiency for a Coverage record that has none). Both are corrected to "
                   "the exact per-record pair and to the null/null primary pair, and a paragraph "
                   "states that the existing null -> required-cell-unsatisfied route is the "
                   "load-bearing carrier for missing work, that uncovered-expected-source-subject is "
                   "NOT registered for source=execution and is not that carrier, and that the verdict "
                   "stays indeterminate.",
    },
    "docs/coop/design-corrections/foundation/enumeration-contract.v1.md": {
        "decisions": [3],
        "purpose": "Selection-versus-enumerator clarification: enumerator.status is about the PROVIDER "
                   "BINDING, the capability request/cell is a different selection, native's 'answered "
                   "by disclosure rather than omitted' is a rule about the cell's answer and needs no "
                   "selected enumerator or executed provider, and the first-match order keeps "
                   "unsupported-typed ahead of both unavailable tokens. Required-cell totality and "
                   "the required+unselected refusal are restated as unchanged. Added only because the "
                   "existing section 1 wording was the text the diagnosis read as conflicting with "
                   "native.",
    },
    "docs/v2/contracts/product-v1/native-evidence.md": {
        "decisions": [3, 4],
        "purpose": "One explanatory paragraph, no normative native change: where the lawfully answered "
                   "UNSUPPORTED-TYPED Coverage is accounted for (retained in its view and in "
                   "selectedRefs; named by no account; disclosed by applicability plus the derived "
                   "account pair; required cells still indeterminate; a complete cell outcome means "
                   "answered, not supported), with links to execution-inputs section 5 and to the "
                   "enumeration-contract selection distinction. Added because the chapter's own "
                   "'is answered' prose otherwise stops at the Coverage and says nothing about the "
                   "execution account, which is what the disagreement turned on.",
    },
}


def main() -> int:
    before = {r["path"]: r for r in json.loads((HERE / "before-hashes.json").read_text())}
    after = {r["path"]: r for r in json.loads((HERE / "after-hashes.json").read_text())}
    changed, unchanged = [], []
    for path in before:
        b, a = before[path], after[path]
        row = {
            "path": path,
            "beforeSha256": b["sha256"], "beforeBytes": b["bytes"],
            "afterSha256": a["sha256"], "afterBytes": a["bytes"],
            "beforeImage": b["image"], "afterImage": a["image"],
        }
        if b["sha256"] == a["sha256"]:
            unchanged.append(row)
            continue
        bl = Path(b["image"]).read_text().splitlines(keepends=True)
        al = Path(a["image"]).read_text().splitlines(keepends=True)
        diff = list(difflib.unified_diff(bl, al, n=0))
        row["addedLines"] = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
        row["removedLines"] = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))
        row.update(PURPOSE[path])
        changed.append(row)

    out = {
        "standing": "Bounded corrective source authorship on the isolated exact32 successor copy "
                    "(execution-account-successor.v1/source). NOT acceptance, NOT product "
                    "implementation, no commit, no push, no source pin or planning update.",
        "base": json.loads(Path("/tmp/opensip-design-corrections/execution-account-successor.v1/base-custody.json").read_text()),
        "beforeImagesPreservedIn": str(HERE / "before"),
        "afterImagesPreservedIn": str(HERE / "after"),
        "changedFiles": sorted(changed, key=lambda r: r["path"]),
        "inspectedButUnchanged": sorted(unchanged, key=lambda r: r["path"]),
        "changedFileCount": len(changed),
        "additionalFilesBeyondTheBoundedList": [
            {
                "path": "docs/coop/design-corrections/foundation/evaluator_graph_fixture.v3.py",
                "status": "WITHIN the bounded list ('minimal changes to existing "
                          "evaluator_graph_fixture.v3.py when necessary for coherent current "
                          "full-Run controls'). Named here because the change is larger than the "
                          "others: three default-OFF options plus the cell-order/cellOrdinal "
                          "rewiring those options force. Existing callers verified byte-identical.",
            },
            {
                "path": "docs/coop/design-corrections/foundation/enumeration-contract.v1.md",
                "status": "WITHIN the bounded list ('enumeration-contract.v1.md may receive minimal "
                          "explanatory links / selection-versus-enumerator clarification if their "
                          "current prose conflicts with the decisions'). Section 1's unselected "
                          "allowance was the exact prose the diagnosis read against native.",
            },
            {
                "path": "docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md",
                "status": "WITHIN the bounded list ('minimal changes ... when necessary'). Necessary: "
                          "section 9.6's table literally specified the fabricated "
                          "provider-unavailable carrier that decision 5 removes, so leaving it would "
                          "have left the contract self-contradictory.",
            },
        ],
        "notEditedAlthoughNamedInTheBoundedList": [
            {
                "path": "docs/coop/design-corrections/foundation/evaluator_semantic_fixture.v3.py",
                "reason": "No change needed; its graphs are unaffected by the corrections and its "
                          "checker case still admits.",
            },
            {
                "path": "docs/coop/design-corrections/foundation/check-composition.v3.py",
                "reason": "The task named `check-evaluator-composition.v3.py`; no such file exists in "
                          "this source. The composition checker is `check-composition.v3.py`. It "
                          "needed no change and still exits 0.",
            },
        ],
        "deliberatelyNotTouched": [
            "foundation/evaluator3-source-pins.v1.json and foundation/source-pins.v1.json "
            "(authoritative ledgers; root owns the rebinding). Both are now STALE for exactly the "
            "nine changed files; the disposable rebinding used to execute the suites lives only in "
            "this runtime and is labelled DISPOSABLE.",
            "foundation/evaluator_input_model.v3.py (owns the proof bridge; the existing null -> "
            "required-cell-unsatisfied route was verified to carry the obligation and needed no "
            "change).",
            "foundation/check-execution-replay.v3.py (not in the bounded list; unchanged and still "
            "exits 0, now recording required-cell-unsatisfied instead of the fabricated carrier).",
            "Any consumer/blind artefact, any admission boundary of another owner, and every "
            "historical review folder.",
        ],
    }
    (HERE / "changed-file-handoff.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "changedFileCount": out["changedFileCount"],
        "changed": [{"path": r["path"], "decisions": r["decisions"],
                     "+": r["addedLines"], "-": r["removedLines"]} for r in out["changedFiles"]],
        "unchanged": [r["path"] for r in out["inspectedButUnchanged"]],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
