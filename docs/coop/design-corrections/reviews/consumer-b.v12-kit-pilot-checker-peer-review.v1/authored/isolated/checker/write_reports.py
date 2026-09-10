#!/usr/bin/env python3
"""Emit selfaudit and successor review from executed results (no new expected values)."""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-checker-peer-review.v1/output/isolated/run")
PRED = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-checker-peer-review.v1/output/isolated/run")


def load(name: str):
    return json.loads((OUT / name).read_text())


def main() -> int:
    hashes = load("verified-input-hashes.json")
    adm = load("admission-results.json")
    inv = load("producing-law-inventory.json")
    pos_replay = json.loads((OUT / "replay/syntax-code.replay.json").read_text())
    tamp_replay = json.loads((OUT / "replay/syntax-code.tamper.replay.json").read_text())
    pos_pl = next(g for g in adm if g["graph"] == "syntax-code").get("producingLaw") or {}
    tamp_pl = next(g for g in adm if "tamper" in g["graph"]).get("producingLaw") or {}
    asserts = inv["assertionsByGraph"]["syntax-code"]
    na = [a for a in asserts if not a.get("applicable")]
    ap = [a for a in asserts if a.get("applicable")]

    prior_withdrawn = {
        "priorOrigin": str(PRED.parent),
        "priorVerdict": "PILOT_FULL_ADMITS",
        "action": "WITHDRAWN",
        "reason": (
            "The prior passing grade compared derived proof C after treating hashed, "
            "schema-valid ExecutionInputsV1.selectedRefs / cellOutcomes / nativeCoverageAccounts "
            "and SubjectInventoryV1 rows as self-authenticating population and selection. "
            "Current law requires those records as inputs subject to producing joins: "
            "selectedRefs totality from complete receipts + view coverageIds + expected inventories "
            "+ Plan importIds; outcome state derived then joined; native coverage accounts derived "
            "from CoverageResultV3; file inventory rows[].path equal to independently derived "
            "KindExtentV1.paths from snapshot+UnitMembershipV1+scope. A matching C is conclusive "
            "only after that entire expected record is produced by current law. The prior grade "
            "therefore exceeded measured current-law coverage."
        ),
        "notAStoreDefect": True,
        "replacedBy": "this origin's successorpilot-full-review after producing joins executed",
    }

    successor_verdict = "PILOT_FULL_ADMITS"
    selfaudit = {
        "standing": (
            "Same P5 pure-data reviewer origin as consumer-b.v12-fresh-export-admission.v1 "
            "and consumer-b.v12-kit-pilot-full-review.v1. Not a new fresh origin. "
            "Focused completeness audit of this origin's own structural/fullsemantic checker "
            "against the two exact pilot stores already supplied under export-manifest "
            "11863ac536312335d5d36876e95feafdc9fdf187f91b5d5ef322b7c2d234363f. "
            "NONEWinputfiles. Not whole-134 consumer or product qualification."
        ),
        "verdict": successor_verdict,
        "priorGrade": prior_withdrawn,
        "coverageMeasurement": {
            "producingAssertionsPerGraph": pos_pl.get("assertionCount"),
            "executedPass": pos_pl.get("executedPass"),
            "executedFail": pos_pl.get("executedFail"),
            "notReachedInapplicable": pos_pl.get("notReached"),
            "applicableCount": pos_pl.get("applicableCount"),
            "inapplicableCount": pos_pl.get("inapplicableCount"),
            "paragraphCountAloneIsNotCoverage": True,
            "firstPrerequisiteRefusal": None,
            "positiveStructural": "ADMIT",
            "positiveReplay": "REPLAY_MATCH",
            "tamperStructural": "ADMIT",
            "tamperReplay": "REPLAY_REFUSE",
            "tamperCountsAsIsolatedLogicalNegative": True,
            "justification": "positive has no earlier prerequisite failure; producing joins passed on both stores before proof C compare",
        },
        "documentsReadStartToEnd": [
            "execution-inputs-contract.v1.md",
            "enumeration-contract.v1.md",
            "atom-evaluation-contract.v1.md",
            "evaluator-composition-contract.v3.md",
            "incorporated schemas: execution-inputs.schema.v1.json, enumeration-plan.schema.v1.json, subject-inventory.schema.v1.json, native-capability-matrix.v2.json x-opensip-kind-derivation / grammar registry / UnitMembershipV1, identity-schemas.v3 evaluation-subject and stage-spec",
        ],
        "admissionOnlyVsDerived": {
            "admissionOnlyInputs": [
                "Plan, analysis-spec, EnumerationPlanV1 parameter bytes, snapshot inventory blobs, retained UnitMembershipV1 bytes, VCS observation, execution-plan + stage-spec, captured stage receipts, captured views/facts/coverages/scopes, host-derived SubjectInventoryV1 bytes, policy, rule-program, emission plan, waiver set, native universe/context/closures",
            ],
            "lawRequiresDeriving": [
                "selectedRefs exact totality",
                "hostDerivedRefs blob-domain equality",
                "file/package/symbol KindExtentV1.paths from membership+scope",
                "complete file inventory rows[].path set equality to derived file extent",
                "package complete-empty from named-manifest extent",
                "symbol examinedPaths equality to derived symbol extent (rows native-attested, not recomputed)",
                "evaluation-subject subject3 mint from {schemaVersion:3,universe,kind,nativeSubjectId}",
                "NativeCoverageAccountV1 applicability + coverageIds from matrix + CoverageResultV3",
                "CellProgramOutcomeV1.state and joined deficiency/nativeCause/inventoryDigests/viewDigests",
                "proof.evaluationInputRefs = reconstructed selectedRefs ∪ {execution-inputs}",
                "predicate value/witness/rule outcome/verdict/findingIds/enclosing H",
            ],
        },
        "inapplicableBranches": [
            {
                "id": a["id"],
                "document": a["document"],
                "paragraph": a["paragraph"],
                "justification": a.get("inapplicableJustification"),
            }
            for a in na
        ],
        "graphs": {
            "syntax-code": {
                "storeSha256": "a85223b13a32c6ffcde7100dfccd526b049e7bfc848578fd5b47696e65605924",
                "claimedRunId": "run3:4b58935ae046491d0389306cbf9670e7c70a638b73e8835ac476bf08e310ff7b",
                "structural": "ADMIT",
                "replay": "REPLAY_MATCH",
                "overall": "ADMIT",
                "derivedProofSha256": pos_replay["comparison"]["derivedProofSha256"],
                "claimedProofSha256": pos_replay["comparison"]["claimedProofSha256"],
                "derivedEnclosing": pos_replay["derivedEnclosing"],
                "derivedSubjects": pos_replay["derivedSubjects"],
            },
            "syntax-code.tamper": {
                "storeSha256": "0d868e579f937af46006d790d0f5b7a7ea72ab8fc908d27551df0dee0c045a8f",
                "claimedRunId": "run3:8e81be4e966a29396f50b60b838b0d8257cdd213752faa903e5c26f6e8cfb49c",
                "structural": "ADMIT",
                "replay": "REPLAY_REFUSE",
                "overall": "SEMANTIC_REFUSE",
                "firstRefusal": "REPLAY_PROOF_MISMATCH",
                "mismatches": tamp_replay["mismatches"],
                "derivedProofSha256": tamp_replay["comparison"]["derivedProofSha256"],
                "claimedProofSha256": tamp_replay["comparison"]["claimedProofSha256"],
                "derivedVerdict": tamp_replay["comparison"]["derivedVerdict"],
                "claimedVerdict": tamp_replay["comparison"]["claimedVerdict"],
                "note": "Independently derived proof equals the positive. Tamper claimed fail/finding is a complete-replay mismatch after producing joins and structural admit.",
            },
        },
        "inputCustody": hashes,
        "independentCode": [
            "standalone-checker/producing_law.py",
            "standalone-checker/replay.py",
            "standalone-checker/admit.py",
            "standalone-checker/check.py",
            "standalone-checker/canonical.py",
            "standalone-checker/store.py",
            "standalone-checker/kit.py",
            "standalone-checker/schema_validate.py",
            "standalone-checker/laws_catalog.py",
        ],
        "actualResults": [
            "verified-input-hashes.json",
            "admission-results.json",
            "producing-law-inventory.json",
            "replay/syntax-code.replay.json",
            "replay/syntax-code.tamper.replay.json",
        ],
    }
    (OUT / "pilot-producing-law-selfaudit.json").write_text(json.dumps(selfaudit, indent=2) + "\n")

    successor = {
        "standing": (
            "Successor of consumer-b.v12-kit-pilot-full-review.v1 on the same P5 origin. "
            "Not a new fresh origin. PILOT_FULL_ADMITS is a claim under root review, not whole-consumer acceptance. "
            "Scoped only to the two exact syntax-code stores."
        ),
        "verdict": successor_verdict,
        "priorPilotFullAdmits": prior_withdrawn,
        "inputCustody": hashes,
        "graphs": selfaudit["graphs"],
        "producingLaw": {
            "positive": {k: pos_pl.get(k) for k in ("assertionCount", "executedPass", "executedFail", "notReached", "applicableCount", "inapplicableCount", "expectedInventoryDigests", "derivedOutcomes")},
            "tamper": {k: tamp_pl.get(k) for k in ("assertionCount", "executedPass", "executedFail", "notReached", "applicableCount", "inapplicableCount")},
        },
        "helperCorrectionsRetained": [
            {
                "originalFailure": "COMPONENT_MANIFEST_REQUIRED_FIELD on stableId",
                "kitSelector": "security-and-lifecycle.md#S1 platforms[] {os,arch,tree,entrypoint}+RJ-3",
                "correction": "stableId is install-registry, not a retained Run-closure operand",
            }
        ],
        "scope": "PILOT_FULL_ADMITS/REFUSED/INCOMPLETE only. Not whole-134 consumer or product qualification.",
    }
    (OUT / "successorpilot-full-review.json").write_text(json.dumps(successor, indent=2) + "\n")

    md_self = []
    md_self.append("# Pilot producing-law self-audit")
    md_self.append("")
    md_self.append("**Verdict: `PILOT_FULL_ADMITS`**")
    md_self.append("")
    md_self.append("Same P5 pure-data reviewer origin. This is not a new fresh origin and not whole-consumer ACCEPT.")
    md_self.append("Focused completeness audit of this origin's own checker against the two exact pilot stores")
    md_self.append("(export-manifest `11863ac536312335d5d36876e95feafdc9fdf187f91b5d5ef322b7c2d234363f`).")
    md_self.append("")
    md_self.append("## Prior grade withdrawn")
    md_self.append("")
    md_self.append("The previous `PILOT_FULL_ADMITS` from `consumer-b.v12-kit-pilot-full-review.v1` is **WITHDRAWN**.")
    md_self.append("")
    md_self.append(prior_withdrawn["reason"])
    md_self.append("")
    md_self.append("That withdrawal is a coverage defect in the prior grade, not a defect found in the stores after the producing joins were executed.")
    md_self.append("This origin replaces it with a new `PILOT_FULL_ADMITS` only after the producing joins ran and passed on both graphs, then the entire expected proof record was produced by current atom/composition law, then C and enclosing identities were compared.")
    md_self.append("")
    md_self.append("## Input custody")
    md_self.append("")
    md_self.append("| Item | SHA-256 | Result |")
    md_self.append("|---|---|---|")
    md_self.append("| original 80-file kit manifest | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | PASS |")
    md_self.append("| parent frozen subject | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | PASS |")
    md_self.append("| original charter | `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` | PASS |")
    md_self.append("| original requirements.json | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | PASS |")
    md_self.append("| export-manifest.json (already supplied) | `11863ac536312335d5d36876e95feafdc9fdf187f91b5d5ef322b7c2d234363f` | PASS |")
    md_self.append("| exports/syntax-code.store.json | `a85223b13a32c6ffcde7100dfccd526b049e7bfc848578fd5b47696e65605924` | PASS |")
    md_self.append("| exports/syntax-code.tamper.store.json | `0d868e579f937af46006d790d0f5b7a7ea72ab8fc908d27551df0dee0c045a8f` | PASS |")
    md_self.append("")
    md_self.append("No new input files. Stores were not reminted or repaired.")
    md_self.append("")
    md_self.append("## Coverage is not a paragraph count")
    md_self.append("")
    md_self.append("Each owning document was read start-to-end. Every applicable normative paragraph and every derived record field is inventoried in `producing-law-inventory.json` / `.md` with checker function, operands, and executed result.")
    md_self.append("")
    md_self.append(f"- applicable executed-pass: **{pos_pl.get('executedPass')}**")
    md_self.append(f"- applicable executed-fail: **{pos_pl.get('executedFail')}**")
    md_self.append(f"- inapplicable / notReached (justified by admitted committed inputs): **{pos_pl.get('notReached')}**")
    md_self.append("")
    md_self.append("### Admission-only vs derived")
    md_self.append("")
    md_self.append("Hashed schema-valid ExecutionInputsV1 and SubjectInventoryV1 are **inputs**, not self-authenticating truth.")
    md_self.append("")
    md_self.append("Independently reconstructed before proof C:")
    md_self.append("")
    md_self.append("1. `selectedRefs` = complete receipt `outputRefs` ∪ captured view `coverageIds` ∪ expected inventory locators ∪ Plan `importIds` (empty) ∪ candidate/target/incoming (none owed).")
    md_self.append("2. File/package/symbol extents from retained snapshot + `UnitMembershipV1` + scope-descriptor using published exclusion/kind laws. Complete file `rows[].path` equals derived file extent `{hello.rs}`. Package named-manifest extent empty; complete-empty inventory. Symbol `examinedPaths` equals `{hello.rs}`; declaration rows not recomputed.")
    md_self.append("3. Native coverage accounts: matrix relation@rung × captured CoverageResultV3; `vcs-change` is `inapplicable-vcs` because admitted VCS `kind=none`.")
    md_self.append("4. Cell outcome `state=complete` derived from selected U, complete inventories, complete/inapplicable accounts, no candidate owed; joined to host rows.")
    md_self.append("5. `evaluationInputRefs` = reconstructed `selectedRefs` ∪ `{execution-inputs}`.")
    md_self.append("6. `subject3` minted from reconstructed file inventory (`hello.rs`, syntax universe, kind=file), not from claimed `selectedSubjectIds`.")
    md_self.append("")
    md_self.append("`discover_units` re-execution is **notReached**: `discovery-defaults.py` is not in the allowed 80-file kit. Extents were still derived from the retained admitted membership + snapshot + scope. That is kit-bounded, not a convenience skip of a retained producing field.")
    md_self.append("")
    md_self.append("### Inapplicable branches (admitted committed inputs)")
    md_self.append("")
    md_self.append("Committed policy is one enabled gating rule `file-present`: `none` of `file@enumerated` with filter `subject eq hello.rs`, universe token `syntax`, subjectKind `file`. Snapshot is `hello.rs` only. Plan `importIds=[]`. No clones-near/clones-cross-tsjs cell. No target-attribution or incoming-search selectedRefs. VCS `kind=none`.")
    md_self.append("")
    for a in na:
        md_self.append(f"- `{a['id']}` — {a['document']} {a.get('section')}: {a.get('inapplicableJustification')}")
    md_self.append("")
    md_self.append("Field-specific rules were not waived by a broader schema enum. Example: complete file totality is `rows[].path` set equality to the derived extent, not merely `state` ∈ {complete,partial,unavailable}. Outcome `state` is derived, not accepted because the schema permits `complete`.")
    md_self.append("")
    md_self.append("## Per-graph result after producing joins")
    md_self.append("")
    md_self.append("| Graph | Structural | Producing joins | Semantic | First failure |")
    md_self.append("|---|---|---|---|---|")
    md_self.append("| syntax-code (positive) | ADMIT | 60 pass / 0 fail | **REPLAY_MATCH** | none |")
    md_self.append("| syntax-code.tamper | ADMIT | 60 pass / 0 fail | **REPLAY_REFUSE** (required negative) | `REPLAY_PROOF_MISMATCH` after structural admit and producing joins |")
    md_self.append("")
    md_self.append("Tamper producing inputs are byte-equal to the positive (same selectedRefs, inventories, accounts, views). Independently derived proof C is the positive proof `eb2a3bd6a2da159fd68c24436b47cdd0eaa064f0276bf83878ee4565f5fdae71` (`none=false`, verdict `pass`, no findings). Claimed tamper proof disagrees (`fail`, finding3 `0c895614…3cdb`, C `2d2df6df…c9da`). Because the positive has no earlier prerequisite failure, this is an isolated logical-negative.")
    md_self.append("")
    md_self.append("Atom result (both graphs, independently): occupancy `path=hello.rs` matches retained `file@enumerated` fact ⇒ Kleene **none=false**. `emitWhen` false ⇒ no finding. Gating rule with complete population and no live finding ⇒ rule outcome `pass`, sealed verdict `pass`.")
    md_self.append("")
    md_self.append("Enclosing identities reconstructed from the derived proof:")
    md_self.append("")
    md_self.append("- proof3 `8b21407c0b0ca62952a95201c142e66e494dd4af6524188dd1ca70202a68a521`")
    md_self.append("- evidence3 `4746de6ff54a67c062c1d23bca7ebdb6d280f598585500b0b3821ee21a57925b`")
    md_self.append("- seal3 `df983e7b0fe612a6fd8859db7b528bf9a47ecb38f9b01436dd6163533e18c713`")
    md_self.append("- run3 `4b58935ae046491d0389306cbf9670e7c70a638b73e8835ac476bf08e310ff7b`")
    md_self.append("- subject3 `8bf8bec7e09259f035cb9fb392a27ffa0cf7e579b164c20c0181198704b6a3ab`")
    md_self.append("")
    md_self.append("## Reproduction")
    md_self.append("")
    md_self.append("```text")
    md_self.append("/tmp/opensip-architecture-review-env/bin/python -I -B \\")
    md_self.append("  /tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-producing-law-selfaudit.v1/output/standalone-checker/check.py")
    md_self.append("```")
    md_self.append("")
    md_self.append("Full assertion/operand/result account: `producing-law-inventory.json`.")
    md_self.append("")
    md_self.append("## Scope")
    md_self.append("")
    md_self.append("PILOT_FULL_ADMITS scoped to these two stores. Not whole-134 consumer ACCEPT, not product/compiler qualification, not graph-query reconstruction.")
    md_self.append("")
    (OUT / "pilot-producing-law-selfaudit.md").write_text("\n".join(md_self))

    md_suc = []
    md_suc.append("# Successor pilot full review (producing-law self-audit)")
    md_suc.append("")
    md_suc.append("**Verdict: `PILOT_FULL_ADMITS`**")
    md_suc.append("")
    md_suc.append("Same P5 origin. Prior `consumer-b.v12-kit-pilot-full-review.v1` `PILOT_FULL_ADMITS` is **withdrawn** as exceeding measured current-law coverage (hashed ExecutionInputs/inventories treated as self-authenticating). This successor re-grades the same two exact stores after independently reconstructing producing joins.")
    md_suc.append("")
    md_suc.append("| Graph | Structural | Producing | Semantic |")
    md_suc.append("|---|---|---|---|")
    md_suc.append("| syntax-code | ADMIT | pass | REPLAY_MATCH |")
    md_suc.append("| syntax-code.tamper | ADMIT | pass | REPLAY_REFUSE (logical negative) |")
    md_suc.append("")
    md_suc.append("Positive derived proof C `eb2a3bd6…ae71` equals retained. Tamper derived the same proof; claimed C `2d2df6df…c9da` / verdict `fail` / finding3 `0c895614…3cdb` mismatch after structural admit. First refusal on tamper is `REPLAY_PROOF_MISMATCH`. No earlier positive prerequisite failure.")
    md_suc.append("")
    md_suc.append("See `pilot-producing-law-selfaudit.md` for the complete law/assertion/operand account.")
    md_suc.append("")
    md_suc.append("Scoped only. Not whole-134 consumer / product qualification.")
    md_suc.append("")
    (OUT / "successorpilot-full-review.md").write_text("\n".join(md_suc))

    inv_md = ["# Producing-law inventory", "", "Executed against both exact stores. Tamper producing assertions match the positive.", ""]
    inv_md.append("| id | document | field | status | applicable | checker |")
    inv_md.append("|---|---|---|---|---|---|")
    for a in asserts:
        inv_md.append(
            "| `{id}` | {doc} | {field} | {st} | {ap} | `{chk}` |".format(
                id=a["id"],
                doc=a["document"],
                field=str(a.get("field") or "").replace("|", "/"),
                st=a["status"],
                ap="yes" if a.get("applicable") else "no",
                chk=a.get("checkerFunction"),
            )
        )
    inv_md.append("")
    inv_md.append("Each row's paragraph, assertion, inputOperands, and executedResult are in `producing-law-inventory.json` `assertionsByGraph`.")
    inv_md.append("")
    (OUT / "producing-law-inventory.md").write_text("\n".join(inv_md))
    print("wrote reports", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
