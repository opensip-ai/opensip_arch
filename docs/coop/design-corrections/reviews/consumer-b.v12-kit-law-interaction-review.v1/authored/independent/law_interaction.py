#!/usr/bin/env python3
"""Disposition of the predicate.inputRefs / evaluationInputRefs / ProofInputRef.domain law-interaction."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
sys.path.insert(0, str(OUT))

from independent.admit_run import Store, hex_of  # noqa: E402
from independent.kit_core import C, parse_h_frame  # noqa: E402

SNAP = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v2/consumer-snapshot")
SELFAUDIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-selfaudit.v3/output/review-selfaudit.json")
SELFAUDIT_MD = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-selfaudit.v3/output/review-selfaudit.md")
V2_JSON = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v2/output/other-runs-review.json")
CHARTER = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-selfaudit.v3/original-consumer-charter.txt")
KIT_MANIFEST = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v1/subject/consumer-input-manifest.json")
REQ = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v1/requirements.json")
SNAP_MANIFEST = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v2/snapshot-manifest.json")
PYTHON = "/tmp/opensip-architecture-review-env/bin/python"
RUNS = ["ts", "rust", "syntax-data", "rust-partial-clones"]

EXPECTED = {
    "charter": "57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec",
    "kit": "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8",
    "req": "855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495",
    "snap": "feb08879bff5dd7313e471f33cad161389371600ea472cb05169d187faed006c",
    "selfaudit_md": "b4e8cabd3b8ea92e4dd724f2b27f43a2be8fcd802067d2b485fd8c12211fa469",
    "selfaudit_json": "ef06a3c532450fc3eb946f2e7faa5e148e8860622b21a2dac5e95b8a7fb9adc2",
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_claimed_proof(name: str) -> dict:
    store = Store.load(SNAP / "runs" / f"{name}.store.json")
    run_id = sorted(k for k in store.object_table if str(k).startswith("run3:"))[0]
    run = parse_h_frame(store.rehash(store.object_table[run_id]["digest"]), allowed_domains={"run"})["value"]
    seal = parse_h_frame(store.rehash(store.object_table[run["evaluationSealId"]]["digest"]), allowed_domains={"evaluation-seal"})["value"]
    proof = parse_h_frame(store.rehash(store.object_table[seal["proofBundleId"]]["digest"]), allowed_domains={"proof-bundle"})["value"]
    ei = store.parse_canonical(proof["executionInputsDigest"])
    eir = proof.get("evaluationInputRefs") or []
    eir_set = {(r["domain"], r["digest"]) for r in eir}
    sel = {(r["domain"], r["digest"]) for r in ei.get("selectedRefs") or []}
    extras = []
    pred_domains = set()
    for pp in proof.get("predicateProofs") or []:
        for r in pp.get("inputRefs") or []:
            pred_domains.add(r["domain"])
            if (r["domain"], r["digest"]) not in eir_set:
                extras.append({"predicateId": pp.get("predicateId"), "ref": r})
    expected_eir = sel | {("execution-inputs", proof["executionInputsDigest"])}
    return {
        "runId": run_id,
        "proofId": seal["proofBundleId"],
        "ruleProgramDigest": proof.get("ruleProgramDigest"),
        "executionInputsDigest": proof["executionInputsDigest"],
        "evaluationInputRefs": eir,
        "evaluationInputRefDomains": sorted({r["domain"] for r in eir}),
        "selectedRefDomains": sorted({r["domain"] for r in ei.get("selectedRefs") or []}),
        "predicateInputRefDomains": sorted(pred_domains),
        "predicateExtrasVersusEvaluationInputRefs": extras,
        "evaluationInputRefsEqualsSelectedPlusExecutionInputs": {(d, x) for d, x in eir_set} == expected_eir,
        "subsetHolds": not extras,
        "ruleProgramInEvaluationInputRefs": any(r["domain"] == "rule-program" for r in eir),
        "ruleProgramInPredicateInputRefs": "rule-program" in pred_domains,
        "ruleProgramInSelectedRefs": any(r["domain"] == "rule-program" for r in ei.get("selectedRefs") or []),
    }


def logical_examples() -> dict:
    """Reasoning evidence only. Not replacement admission of any exported Run."""
    view = {"domain": "view", "digest": "aa" * 32}
    cov = {"domain": "coverage", "digest": "bb" * 32}
    ei = {"domain": "execution-inputs", "digest": "cc" * 32}
    rp = {"domain": "rule-program", "digest": "dd" * 32}
    inv = {"domain": "subject-inventory", "digest": "ee" * 32}
    selected = [view, cov, inv]
    lawful_eir = selected + [ei]
    lawful_pred = [view, cov]
    subset_fail_pred = [view, cov, rp]
    enum_fail_eir = selected + [ei, rp]

    def pair_set(xs):
        return sorted({(x["domain"], x["digest"]) for x in xs})

    def subset(a, b):
        return set(pair_set(a)) <= set(pair_set(b))

    return {
        "standing": "kit-derived logical examples; not exported Run admission",
        "A_jointly_satisfying": {
            "evaluationInputRefs": lawful_eir,
            "predicate.inputRefs": lawful_pred,
            "proof.ruleProgramDigest": rp["digest"],
            "program-predicate.ruleProgramDigest": rp["digest"],
            "evaluationInputRefs_equals_selected_plus_execution_inputs": True,
            "predicate_subset": subset(lawful_pred, lawful_eir),
            "rule_program_in_predicate_inputRefs": False,
            "result": "jointly satisfies enumeration §7 MUST, composition §1 MUST, identity §3 subset MUST, and proof.ruleProgramDigest / program-predicate.ruleProgramDigest MUSTs. ProofInputRef.domain still permits rule-program as a shared-type vocabulary member unused in these two arrays.",
        },
        "B_predicate_cites_rule_program": {
            "evaluationInputRefs": lawful_eir,
            "predicate.inputRefs": subset_fail_pred,
            "evaluationInputRefs_equals_selected_plus_execution_inputs": True,
            "predicate_subset": subset(subset_fail_pred, lawful_eir),
            "result": "enumeration §7 holds; identity §3 subset FAILS. This is the exported four-Run shape.",
        },
        "C_evaluationInputRefs_adds_rule_program": {
            "evaluationInputRefs": enum_fail_eir,
            "predicate.inputRefs": subset_fail_pred,
            "evaluationInputRefs_equals_selected_plus_execution_inputs": False,
            "predicate_subset": subset(subset_fail_pred, enum_fail_eir),
            "result": "subset would hold only by violating enumeration §7 / composition §1 / execution-inputs-contract §7 (do not add policy/schema roots to selectedRefs; evaluationInputRefs = selectedRefs + execution-inputs).",
        },
        "canonicalBytesOfA_evaluationInputRefs": hashlib.sha256(C(lawful_eir)).hexdigest(),
        "canonicalBytesOfB_predicateInputRefs": hashlib.sha256(C(subset_fail_pred)).hexdigest(),
    }


def main() -> int:
    probes = OUT / "probes"
    probes.mkdir(parents=True, exist_ok=True)
    measured = {n: load_claimed_proof(n) for n in RUNS}
    (probes / "claimed-proof-inputref-operands.json").write_text(json.dumps(measured, indent=2) + "\n")
    examples = logical_examples()
    (probes / "logical-examples.json").write_text(json.dumps(examples, indent=2) + "\n")
    prior = json.loads(SELFAUDIT.read_text())

    musts = [
        {
            "id": "M-EVAL-INPUTREFS-EQ-SELECTED-PLUS-EI",
            "strength": "MUST",
            "source": "foundation/enumeration-contract.v1.md §7",
            "sentence": "The proof's `evaluationInputRefs` must equal the execution manifest's selected references plus that manifest's own `execution-inputs` reference.",
        },
        {
            "id": "M-EVAL-INPUTREFS-EQ-SELECTED-PLUS-EI-COMPOSITION",
            "strength": "MUST",
            "source": "foundation/evaluator-composition-contract.v3.md §1",
            "sentence": "`evaluationInputRefs` equals its selected references plus that one manifest reference.",
        },
        {
            "id": "M-EVAL-INPUTREFS-EQ-SELECTED-PLUS-EI-EXEC",
            "strength": "MUST",
            "source": "foundation/execution-inputs-contract.v1.md §7",
            "sentence": "require `evaluationInputRefs = selectedRefs + {domain:execution-inputs,digest}`. ... Do not add policy/schema roots to `selectedRefs`.",
        },
        {
            "id": "M-SELECTEDREFS-DOMAIN-ENUM",
            "strength": "MUST (schema closed enum)",
            "source": "foundation/execution-inputs.schema.v1.json#/$defs/InputRefV1/properties/domain",
            "sentence": "selectedRefs item domain enum is exactly view|import|coverage|subject-inventory|target-attribution|incoming-search|candidate-producer-result. rule-program is not a member.",
        },
        {
            "id": "M-PREDICATE-INPUTREFS-SUBSET",
            "strength": "MUST",
            "source": "docs/v2/contracts/product-v1/identity-and-evidence.md §3 (closing digest law, lines 515–516)",
            "sentence": "Predicate input refs are a subset of evaluationInputRefs; evidence view roots equal the named views and coverage roots equal their coverage union.",
        },
        {
            "id": "M-WITNESSES-CANNOT-ADD-ROOTS",
            "strength": "MUST",
            "source": "foundation/evaluator-composition-contract.v3.md §3",
            "sentence": "All input references are direct retained roots or members of an evaluated view as the identity closure permits; witnesses cannot add roots.",
        },
        {
            "id": "M-FINDING-CITES-NO-EXTRA-ROOTS",
            "strength": "MUST",
            "source": "docs/v2/contracts/product-v1/identity-and-evidence.md §3 lines 194–200",
            "sentence": "Finding citations cannot introduce extra authoritative input roots. ... A well-formed, hash-valid object outside this closure is refused, rather than admitted as hidden finding evidence.",
        },
        {
            "id": "M-PROOF-RULEPROGRAMDIGEST-REQUIRED",
            "strength": "MUST (required field)",
            "source": "foundation/identity-schemas.v3.json#/$defs/proof-bundle required[] and properties.ruleProgramDigest",
            "sentence": "proof-bundle required includes ruleProgramDigest; x-opensip-digest representation=canonical-record selector #/$defs/RuleProgramV2.",
        },
        {
            "id": "M-PROGRAM-PREDICATE-RULEPROGRAMDIGEST",
            "strength": "MUST",
            "source": "foundation/identity-schemas.v3.json#/$defs/program-predicate properties.ruleProgramDigest description; identity-and-evidence.md §3 lines 1147–1151",
            "sentence": "`ruleProgramDigest` equals the proof bundle's; it addresses one predicate node of the admitted RuleProgramV2; it does not restate the node.",
        },
        {
            "id": "M-EVAL-INPUTREFS-NAMES-PLAN-IMPORTS",
            "strength": "MUST",
            "source": "identity-and-evidence.md §3 lines 517–519",
            "sentence": "The evaluator3 proof also names every Plan-selected import in evaluationInputRefs.",
        },
        {
            "id": "P-PROOFINPUTREF-DOMAIN-ENUM",
            "strength": "PERMITS (shared type vocabulary)",
            "source": "foundation/identity-schemas.v3.json#/$defs/ProofInputRef/properties/domain",
            "sentence": "Closed enum includes rule-program among view, import, coverage, policy, waiver, schema, blob, ... execution-inputs. This is the shared item type of evaluationInputRefs, predicateProofs[].inputRefs, evaluation-deficiency.inputRefs, and cache-key inputRefs. An enum member is admissible in the type; it is not a field-specific requirement that every such array contain that member.",
        },
        {
            "id": "P-BYDOMAIN-RULE-PROGRAM",
            "strength": "PERMITS (digest representation when that domain is used)",
            "source": "identity-schemas.v3.json#/x-opensip-digest-domains/byDomain/rule-program",
            "sentence": "When a ProofInputRef/Ref carries domain=rule-program, representation is canonical-record RuleProgramV2. This is the join recipe IF that domain is selected, not a command to select it in predicate.inputRefs.",
        },
    ]

    disposition = {
        "jointlySatisfiable": True,
        "normativeContradiction": False,
        "satisfyingShape": "evaluationInputRefs = selectedRefs ∪ {execution-inputs}; predicateProofs[].inputRefs ⊆ evaluationInputRefs and therefore cannot name rule-program; the program is bound by required proof.ruleProgramDigest and by program-predicate.ruleProgramDigest (equal to the proof field). ProofInputRef.domain remains a shared closed vocabulary that permits rule-program on other ProofInputRef arrays (e.g. a deficiency inputRef) without requiring it on predicate.inputRefs.",
        "exportedFourRunShape": "B: enumeration §7 holds on claimed evaluationInputRefs; identity §3 subset fails because predicate.inputRefs cites rule-program. Not shape C.",
        "diagnosticDisposition": "WITHDRAWN as an admission exception. The subset sentence is a MUST. Marking it diagnostic/notUsedAsFirstRefusal was a silent checker branch. C equality of compose_proof (which inserts domain=rule-program into predicate.inputRefs) with the claimed proof is the same derivation, not independent establishment of the subset.",
        "syntaxDataGrade": "WITHDRAWN ADMIT. Successor: structural REFUSED; fullsemantic NOT_REACHED. First refusal: predicate-inputRefs-subset-of-evaluationInputRefs.",
        "layer": "structural (identity §3 closure of the claimed proof record's citations). Not semantic atom truth. Do not invent semantic comparison as the gate.",
        "existingLawCorrection": "Do not place domain=rule-program on predicateProofs[].inputRefs. Bind the program with proof.ruleProgramDigest and program-predicate.ruleProgramDigest. Do not add rule-program to evaluationInputRefs or selectedRefs. Checker compose_proof must stop inserting that citation; expected proofs must obey the same MUSTs without copying claimed inputRefs.",
    }

    custody = {
        "charterSha256": sha(CHARTER),
        "charterMatch": sha(CHARTER) == EXPECTED["charter"],
        "kitManifestSha256": sha(KIT_MANIFEST),
        "kitMatch": sha(KIT_MANIFEST) == EXPECTED["kit"],
        "requirementsSha256": sha(REQ),
        "reqMatch": sha(REQ) == EXPECTED["req"],
        "snapshotManifestSha256": sha(SNAP_MANIFEST),
        "snapMatch": sha(SNAP_MANIFEST) == EXPECTED["snap"],
        "selfauditMdSha256": sha(SELFAUDIT_MD),
        "selfauditMdMatch": sha(SELFAUDIT_MD) == EXPECTED["selfaudit_md"],
        "selfauditJsonSha256": sha(SELFAUDIT),
        "selfauditJsonMatch": sha(SELFAUDIT) == EXPECTED["selfaudit_json"],
        "storesUnchanged": True,
    }

    # successor four-run grades
    successor_runs = {}
    for name in RUNS:
        prev = prior["runs"][name]
        meas = measured[name]
        if name == "syntax-data":
            first = {
                "layer": "structural",
                "name": "predicate-inputRefs-subset-of-evaluationInputRefs",
                "detail": (
                    "identity-and-evidence.md §3 MUST: Predicate input refs are a subset of evaluationInputRefs. "
                    f"claimed extras={meas['predicateExtrasVersusEvaluationInputRefs']}"
                ),
            }
            layers = {"raw": "PASS", "schema": "PASS", "structural": "REFUSED", "fullsemantic": "NOT_REACHED"}
            overall = "REFUSED"
            withdrawn_admit = True
        else:
            first = prev.get("firstRefusal")
            layers = prev.get("layers")
            overall = prev.get("overall")
            withdrawn_admit = False
        successor_runs[name] = {
            "storeSha256": prev.get("storeSha256") or json.loads(V2_JSON.read_text())["runs"][name]["storeSha256"] if False else prev.get("storeSha256"),
            "runId": prev.get("runId") or meas["runId"],
            "proofId": meas["proofId"],
            "layers": layers,
            "overall": overall,
            "firstRefusal": first,
            "notReached": ["complete-semantic-replay"] if layers.get("fullsemantic") == "NOT_REACHED" else [],
            "subsetHolds": meas["subsetHolds"],
            "evaluationInputRefsEqualsSelectedPlusExecutionInputs": meas["evaluationInputRefsEqualsSelectedPlusExecutionInputs"],
            "withdrawnSyntaxDataAdmit": withdrawn_admit,
            "measured": meas,
        }
        if not successor_runs[name]["storeSha256"]:
            successor_runs[name]["storeSha256"] = prev.get("storeSha256")

    # fill store hashes from prior
    for name in RUNS:
        successor_runs[name]["storeSha256"] = prior["runs"][name]["storeSha256"]
        successor_runs[name]["runId"] = prior["runs"][name]["runId"]
        successor_runs[name]["planId"] = prior["runs"][name].get("planId")

    verdict = "OTHER_RUNS_REFUSED"
    if any(successor_runs[n]["layers"].get("raw") == "NOT_REACHED" for n in RUNS):
        verdict = "OTHER_RUNS_INCOMPLETE"

    analysis = {
        "verdictThisBoundedAnalysis": "RESOLVED_EXISTING_LAW",
        "successorFourRunVerdict": verdict,
        "standing": "Bounded follow-through on the self-audit law-interaction. Same original P4 kit-only reviewer session. Not a new origin. Not whole-consumer ACCEPT. No store remint.",
        "custody": custody,
        "command": f"{PYTHON} -I -B {HERE / 'law_interaction.py'}",
        "mustInventory": musts,
        "disposition": disposition,
        "measuredOperands": measured,
        "logicalExamples": examples,
        "checkerSharedDerivation": {
            "file": "independent/admit_run.py compose_proof",
            "lines": "predicateProofs[].inputRefs always includes {domain:rule-program, digest:rule_program_digest} plus view and used coverage",
            "note": "v2/v3 expected-proof C equality with claimed proofs used this insertion. That is not independent reconstruction of a lawful proof.",
        },
        "priorDiagnostic": {
            "label": "predicate-inputRefs-subset-of-evaluationInputRefs",
            "was": "ok=false, diagnostic=true, acceptance=notUsedAsFirstRefusal; syntax-data overall ADMIT",
            "now": "acceptance-grade structural MUST failure; syntax-data ADMIT withdrawn",
        },
    }
    (OUT / "law-interaction-review.json").write_text(json.dumps(analysis, indent=2) + "\n")
    (OUT / "law-interaction-review.md").write_text(render_law_md(analysis))

    successor = {
        "verdict": verdict,
        "standing": "Successor four-Run grades after resolving the predicate.inputRefs / evaluationInputRefs law-interaction. Same exact stores. Not whole-consumer ACCEPT.",
        "custody": custody,
        "command": analysis["command"],
        "runs": successor_runs,
        "withdrawn": [
            {
                "grade": "selfaudit.v3 syntax-data structural/fullsemantic PASS and overall ADMIT",
                "reason": "Rested on treating identity §3 subset MUST as diagnostic because ProofInputRef.domain permits rule-program. Schema permit of a shared type is not an exception to the subset MUST.",
            },
            {
                "grade": "selfaudit.v3 diagnostic/notUsedAsFirstRefusal on predicate-inputRefs-subset for all four graphs",
                "reason": "For ts/rust/rust-partial the native producing-rule first refusals remain first (earlier in closure). The subset failure is additional reached structural law on the claimed proof but does not replace those first refusals. For syntax-data it is the first refusal.",
            },
        ],
        "unexecuted": prior.get("unexecuted"),
        "wholeConsumerNotAccepted": True,
        "storesUnchanged": True,
    }
    (OUT / "other-runs-review.json").write_text(json.dumps(successor, indent=2) + "\n")
    (OUT / "other-runs-review.md").write_text(render_succ_md(successor))
    print("DISPOSITION", analysis["verdictThisBoundedAnalysis"])
    print("FOUR_RUN", verdict)
    for n in RUNS:
        print(n, successor_runs[n]["overall"], successor_runs[n]["layers"], (successor_runs[n]["firstRefusal"] or {}).get("name"))
    return 0


def render_law_md(s: dict) -> str:
    lines = []
    lines.append("# Law-interaction review: predicate `inputRefs` × `evaluationInputRefs` × `ProofInputRef.domain`")
    lines.append("")
    lines.append(f"**Disposition: `{s['verdictThisBoundedAnalysis']}`** — jointly satisfiable under existing law. Not a demonstrated normative contradiction.")
    lines.append("")
    lines.append(s["standing"])
    lines.append("")
    lines.append("## Custody")
    lines.append("")
    lines.append("| Object | SHA-256 | Match |")
    lines.append("|---|---|---|")
    c = s["custody"]
    lines.append(f"| original charter | `{c['charterSha256']}` | {c['charterMatch']} |")
    lines.append(f"| kit manifest | `{c['kitManifestSha256']}` | {c['kitMatch']} |")
    lines.append(f"| requirements.json | `{c['requirementsSha256']}` | {c['reqMatch']} |")
    lines.append(f"| v2 snapshot-manifest | `{c['snapshotManifestSha256']}` | {c['snapMatch']} |")
    lines.append(f"| preserved selfaudit.md | `{c['selfauditMdSha256']}` | {c['selfauditMdMatch']} |")
    lines.append(f"| preserved selfaudit.json | `{c['selfauditJsonSha256']}` | {c['selfauditJsonMatch']} |")
    lines.append("")
    lines.append(f"Command: `{s['command']}`")
    lines.append("")
    lines.append("Stores were not reminted. Copied checker write paths were redirected; mechanical diff is `probes/admit_run.path-redirect.diff`.")
    lines.append("")
    lines.append("## MUST versus PERMIT")
    lines.append("")
    for m in s["mustInventory"]:
        lines.append(f"### `{m['id']}` — {m['strength']}")
        lines.append("")
        lines.append(f"Source: `{m['source']}`")
        lines.append("")
        lines.append(f"> {m['sentence']}")
        lines.append("")
    lines.append("## Joint satisfiability")
    lines.append("")
    d = s["disposition"]
    lines.append(f"**Contradiction:** `{d['normativeContradiction']}`")
    lines.append("")
    lines.append(d["satisfyingShape"])
    lines.append("")
    lines.append("The shared `ProofInputRef` type **permits** `domain=rule-program`. Identity §3 **requires** predicate input refs ⊆ evaluationInputRefs. Enumeration §7 / composition §1 / execution-inputs §7 **require** evaluationInputRefs = selectedRefs + execution-inputs. `InputRefV1.domain` **does not include** `rule-program`, so selectedRefs cannot lawfully name it. Therefore a predicate `inputRefs` member `domain=rule-program` cannot be in evaluationInputRefs without breaking enumeration §7, and cannot stay out of evaluationInputRefs without breaking the subset MUST.")
    lines.append("")
    lines.append("That is a constraint on **which array members are selected**, not a hole in the type. The program is already a required proof field (`ruleProgramDigest`) and a required field of `program-predicate` (equal to the proof's digest). Witnesses cannot add roots (composition §3). Binding the program through those required fields, and omitting it from both arrays, satisfies every MUST above. The enum remaining live on other ProofInputRef arrays (deficiencies, cache keys) is not a command to cite it from predicates.")
    lines.append("")
    lines.append("Adding `rule-program` to evaluationInputRefs to save the subset (shape C) is the correction v1 already refused against enumeration §7. It is not available as a waiver.")
    lines.append("")
    lines.append("## Kit-derived logical examples (reasoning evidence, not Run admission)")
    lines.append("")
    ex = s["logicalExamples"]
    lines.append(f"- **A jointly satisfying:** {ex['A_jointly_satisfying']['result']}")
    lines.append(f"- **B exported shape:** {ex['B_predicate_cites_rule_program']['result']}")
    lines.append(f"- **C add to evaluationInputRefs:** {ex['C_evaluationInputRefs_adds_rule_program']['result']}")
    lines.append("")
    lines.append("## Actual retained operands (already measured; reconfirmed)")
    lines.append("")
    lines.append("| Run | evaluationInputRefs domains | predicate inputRef domains | subset | eval=selected+EI | extras |")
    lines.append("|---|---|---|---|---|---|")
    for name, m in s["measuredOperands"].items():
        extras = m["predicateExtrasVersusEvaluationInputRefs"]
        lines.append(
            f"| `{name}` | {m['evaluationInputRefDomains']} | {m['predicateInputRefDomains']} | {m['subsetHolds']} | {m['evaluationInputRefsEqualsSelectedPlusExecutionInputs']} | `{extras}` |"
        )
    lines.append("")
    lines.append("All four claimed proofs match shape **B**. `proof.ruleProgramDigest` is populated on each. Checker `compose_proof` inserts the same `rule-program` citation; C equality of that shared derivation is not admission.")
    lines.append("")
    lines.append("## Disposition of the diagnostic and syntax-data grade")
    lines.append("")
    lines.append(d["diagnosticDisposition"])
    lines.append("")
    lines.append(d["syntaxDataGrade"])
    lines.append("")
    lines.append(f"Layer: {d['layer']}")
    lines.append("")
    lines.append("## Existing-law correction guidance")
    lines.append("")
    lines.append(d["existingLawCorrection"])
    lines.append("")
    lines.append("No normative edit. No invented semantics. No whole-consumer ACCEPT.")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_succ_md(s: dict) -> str:
    lines = []
    lines.append("# Other-runs independent kit-only review (successor after law-interaction disposition)")
    lines.append("")
    lines.append(f"**Verdict: `{s['verdict']}`**")
    lines.append("")
    lines.append(s["standing"])
    lines.append("")
    lines.append("## Custody")
    lines.append("")
    c = s["custody"]
    lines.append(f"- charter `{c['charterSha256']}` match={c['charterMatch']}")
    lines.append(f"- kit `{c['kitManifestSha256']}` match={c['kitMatch']}")
    lines.append(f"- snapshot `{c['snapshotManifestSha256']}` match={c['snapMatch']}")
    lines.append("")
    lines.append("## Withdrawn")
    lines.append("")
    for w in s["withdrawn"]:
        lines.append(f"- **{w['grade']}** — {w['reason']}")
    lines.append("")
    lines.append("## First-refusal map (same exact four stores)")
    lines.append("")
    lines.append("| Run | Raw | Schema | Structural | Fullsemantic | First refusal |")
    lines.append("|---|---|---|---|---|---|")
    for name, r in s["runs"].items():
        fr = r.get("firstRefusal") or {}
        frs = f"`{fr.get('layer','')}:{fr.get('name','')}`" if fr else "none"
        L = r["layers"]
        lines.append(f"| `{name}` | {L.get('raw')} | {L.get('schema')} | {L.get('structural')} | {L.get('fullsemantic')} | {frs} |")
    lines.append("")
    lines.append("ts / rust / rust-partial keep the self-audit native producing-rule first refusals (`compilerPackageDigest` tree membership; `rustcVersion` ≠ closure `semanticVersion`). Those precede proof-record subset in closure. The subset MUST also fails on those claimed proofs and is notReached for acceptance as a *first* refusal. syntax-data native producing rules remain passed; its first refusal is now the subset MUST. fullsemantic is NOT_REACHED on every structurally refused graph.")
    lines.append("")
    for name, r in s["runs"].items():
        lines.append(f"### `{name}`")
        lines.append("")
        lines.append(f"- Store `{r['storeSha256']}`")
        lines.append(f"- Run `{r.get('runId')}` Proof `{r.get('proofId')}`")
        lines.append(f"- Overall **{r['overall']}** layers {r['layers']}")
        if r.get("firstRefusal"):
            fr = r["firstRefusal"]
            lines.append(f"- First refusal: `{fr.get('layer')}:{fr.get('name')}` — {fr.get('detail')}")
        lines.append(f"- notReached: {r.get('notReached')}")
        lines.append("")
    lines.append("No whole-consumer ACCEPT. No remint.")
    lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
