I'll independently admit and replay the four reconstructed Runs from the exact consumer snapshot, reading only the allowed kit inputs and writing the review into this output directory. First I need the charter, requirements, snapshot inventory, and current contract dispatch.Next I’ll verify the kit, requirements, and snapshot hashes, then inventory the four Run stores and the kit’s admission/sealer/evaluator contracts.Hash verification and kit contract dispatch come first; then I’ll inspect the four stores and the consumer helper without treating them as oracles.Custody hashes match. Next I’ll extract current admission/dispatch law from the kit and inspect the four stores plus shared sealer/evaluator without treating consumer claims as oracles.The consumer helper points at another origin’s kit; I’ll rebuild admission against this snapshot’s subject and keep reading the remaining contract and join laws.I’ll pull the remaining kit owners and join laws, then write an independent checker that uses this origin’s subject instead of the consumer helper’s hardcoded path.I’ll probe the four stores’ actual graph shape first, then implement the independent admission checker against those records.Syntax-data’s clones account looks like a real law mismatch; I’ll encode independent admission, replay, and property checks next so that finding is measured rather than assumed.I’ll write an independent kit-only admission and replay checker in this output directory, then run it against all four stores.**Verdict: `OTHER_RUNS_REFUSED`**

This is a kit-only replay of the four reconstructed Runs, not whole-consumer ACCEPT and not root admission. Custody matched: kit manifest `ea2fa750…e6bf8` (80/80), parent `a70f5830…10bbb`, requirements `855a1464…f495`, snapshot manifest `385cacde…be33` (275/275).

Independent admission lived in this origin’s subject and `output/independent/`, not the consumer helper (that helper still points at another origin’s kit). Saved claim/evaluator bytes were locators for comparison, not expected-output oracles. Consumer stores were not reminted.

Reproduce:

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v1/output/independent/review_four.py
```

## Per-Run layers

| Run | Store SHA-256 | Raw | Schema | Structural first refusal | Fullsemantic |
|---|---|---|---|---|---|
| TypeScript | `af2238a6…b4ca` | PASS | PASS | `import-payload` — `RuntimePayloadV1` does not inhabit (`format=json`, null `observationWindow`) | proof C/identity mismatch; field `evaluationInputRefs` |
| Rust | `e6457494…fd4a` | PASS | PASS | `crateRootPaths` `#/a` not in snapshot inventory | same `evaluationInputRefs` extras |
| syntax-data | `e0508756…ec87` | PASS | PASS | `clones-fact` account `unsupported-typed` vs matrix `SUPPORTED-DESIGN` | `evaluationInputRefs` extras |
| rust-partial | `227856b1…1141` | PASS | PASS | same `#/a` crate-root join; toolchain tree `bin/proc-macro-srv` 13 vs 14 bytes | `evaluationInputRefs`, **`executionDeficiencies`, `verdict`** |

Claimed IDs matched the consumer export. Independently reconstructed proof IDs did not.

## Existing-law misses (not invented default-profile cells)

- **TypeScript import:** wrapper is in the graph (`import2:1bdd740b…0eaa`) but the payload is not a registered `RuntimePayloadV1`.
- **Rust crate roots / tree:** native-evidence requires every `crateRootPaths` entry to be inventoried; `#/a` is not. Closure tree length for `bin/proc-macro-srv` is 13 vs retained 14-byte `b'proc-macro-srv'`.
- **Rust dual edition in one selection:** `#/a/src/lib.rs` is owned at 2018 and 2021 in one `selectedUnitIds` set. Dialect law is `BODY_LANGUAGE_OWNER_AMBIGUOUS`; lawful form is one selection/universe at a time. A clones fact was still minted.
- **syntax-data clones:** Coverage `unknown` + `language-tier-unsupported` / `capability-missing` is the published unsupported-scope disclosure. The matrix cell is still `SUPPORTED-AVAILABLE` work, so the required cell derives **partial**, not complete via `unsupported-typed`.
- **rust-partial seal:** host `clones-fact` cell is correctly `partial` with `input-closure-incomplete` / `body-language-owner-unenumerated`, empty clone facts, not complete-empty. Composition §5 still requires `executionDeficiencies` and sealed **indeterminate**. Claimed proof is `verdict=pass` with empty deficiencies (false pass). Independent derived verdict is `indeterminate`.
- **All four proofs:** `evaluationInputRefs` include extra `policy` and `rule-program` members. Enumeration-contract §7 is `selectedRefs + execution-inputs` only. Adding those extras makes TS/Rust/syntax-data proof C match; rust-partial still differs on deficiencies/verdict.

Logical-result tamper vs stale-hash was executed separately on each claimed proof (C inequality plus semantic refuse). A foreign proof3 cannot join this Run’s seal. Root admission was not performed.

Deliverables: `other-runs-review.md`, `other-runs-review.json`, plus probes under `output/probes/`.
