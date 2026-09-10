I'll start from the charter, requirements, and the 80-file kit, then derive a structural admission checker against the six exported graphs only. No agents, no other directories, write only into this output path.Hashes and kit custody first, then identity-and-evidence §3 and the current identity schemas.I'll verify every kit and export hash, then read identity-and-evidence §3 and the identity-schema annotations in full.Kit and export hashes match. Next I’ll finish identity-and-evidence §3 and extract the identity-schema digest/order annotations.I’ll extract digest/order annotations, domain sets, and the export-store shape so the checker can walk exact retained bytes.I'll pull domain prefixes, native admission, security canonical profiles, and remaining join laws next.I have the laws and store shape. Next I’ll implement the standalone checker and dump one decoded graph so the joins can be executed against exact bytes.I'll start the standalone checker: canonical encoding and H first, then kit loading, store frames, and the admission walk.All six graphs reported ADMIT in 0.4s — I’ll inspect law coverage and reached-record counts; that speed likely means parts of the walk never ran.The walk stopped after blob rehash: `AdmissionError` from later phases was swallowed without recording a first refusal. I’ll record those and re-run.Schema `$ref`s were resolving against the isolated `$defs/run` object instead of the full identity document. I’ll bind validators to the document root.Those refusals are checker-order and walker bugs, not graph faults. I’ll populate inventory first, expand `[]` nested identities, and scope the unannotated-digest law to identity-schemas.v3.**Verdict: `EXPORTED_STRUCTURAL_ADMISSION_REFUSED`**

All 80 kit files and all six export stores rehash to the declared SHA-256 values. Semantic replay is **UNEXECUTED** on every graph. This is not whole-consumer ACCEPT.

Each graph has one first structural refusal (later laws are `notReached`):

| Graph | First refusal | Owning law | Offending operands |
|---|---|---|---|
| syntax-code | `PREDICATE_INPUT_NOT_IN_EVALUATION` | identity-and-evidence §3: predicate `inputRefs` ⊆ `evaluationInputRefs` | `{domain: rule-program, digest: 77b07390…6b8e}` not in `evaluationInputRefs` |
| syntax-code-tamper | same | same | same `rule-program` digest (tamper was not judged as a structural truth law) |
| ts | same | same | `{domain: rule-program, digest: bfc39267…b615}` |
| syntax-data | same | same | `{domain: rule-program, digest: 71aaef89…1b40}` |
| rust | `native.native-context-compiler-version-not-from-manifest` | native-evidence §11 (both languages) + §2.3/§2.4, re-run at Run closure | `rustcVersion=1.80.0` vs toolchain closure `semanticVersion=1.0.0` (`closure2:e150a3e4…5352`) |
| rust-partial-clones | same native refusal | same | same `1.80.0` vs `1.0.0` |

Both families are **existing-law implementation misses**. The kit recipes exist and were executed; no absent/contradictory recipe was required. Literal subset/equality laws were not given per-domain exceptions.

Before those refusals, syntax/TS graphs did pass blob rehash, H-frame/C round-trip, inventory uniqueness, native context/universe binding, clones body-frame join, and coverage partition. Syntax-data clones Coverage is `unknown` / `language-tier-unsupported` / `capability-missing` over `notes.json`. Rust graphs never reached fact/coverage/clones laws.

Reproduce:

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-fresh-export-admission.v1/output/standalone-checker/check.py
```

Deliverables: `exported-admission-review.md`, `exported-admission-review.json`, `verified-input-hashes.json`, `standalone-checker/`.
