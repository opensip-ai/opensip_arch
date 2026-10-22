# Independent review — C2a3 accepted-plan publication r1

**Verdict: `ACCEPT-PUBLICATION`**

The supplied `subject.json` has SHA-256 `a7f3335a6667179eb86f44cb9c81d55d24af2ebd722b6da5bbfde43b081c4b3f`. All 111 declared members under its exact `frozenRoot` match their recorded byte lengths and SHA-256 values.

## Publication fidelity

The two archived review histories are complete and independently reconstructable through the relative `archivedFrozenRoot` mappings in `lead-assent.json:19-35`:

- Round 1 retains the original manifest hash `7df3f5d5595bb3ff9d0a88d0ed03ba62f831fe173cb9d3cec8d8259815c3b7bb`, its original absolute frozen root as provenance, and all 45 manifest members byte-exact under `review-r1/subject`.
- Round 2 retains the original manifest hash `109757bcea029cb018604b1ba7b848a7e5136fdf8058c5fb13c50ebfb408e62c`, its original absolute frozen root as provenance, and all 49 manifest members byte-exact under `review-r2/subject`.

The mappings are distinct, relative to the publication root, and identify one complete archive for each unchanged original manifest. Every archived member is also declared by the publication manifest.

The seven published plan documents are byte-identical to their counterparts in the accepted round-2 subject: `AMENDMENTS-AND-SURFACES-r1.md`, `DESIGN-DECISIONS-r1.md`, `EXPORT-MAP-r1.md`, `FAILURE-CONVERSIONS-r2.md`, `M-BOUND-r1.md`, `M-STORAGE-PROOF-r1.md`, and `WORKING-PLAN-r1.md`.

The archived round-2 `review.json` has SHA-256 `802e006d8f7ac0e145c978d8adcee3953f22463eadbe8e095e05475bb63ac57e`, exactly matching `lead-assent.json:8`. It records `ACCEPT-PLAN`, the exact round-2 subject-manifest hash, and no findings. Round 1 remains a byte-exact `REQUIRED-FINDINGS` history; its review hashes match the preserved r2 verification record and its archived copies. `C2A3-PLAN-R1-RF-1` is closed only by the accepted r2 successor, with the payload-free `Invariant`, private collector fault, exhaustive in-scope Budget normalization, cause preservation, and precedence controls intact.

## Standing and boundaries

`README.md:3-12` and `lead-assent.json:9-14,37-53` establish plan standing only. The lead assent selects the proposed M representation/accounting design while explicitly leaving actual source, ABI, allocation, charge evidence, final aggregate census, and fit open. The CORE amendment remains a single-use handoff on the existing receipt attempt ledger, before the separate admission ledger, with no raw-id or new-ledger authority. The SINK amendment selects the payload-free invariant and fixed record key while leaving the actual J2/C2a-4 carrier addition and production envelope controls owed to their owners.

The publication adds no cap, source rule, public detail/code, production analyzer selector, production caller, field-use permission, or partial admission path. It does not claim product code, native execution, unit acceptance, inventory binding, integration, production admission, full SD9 census/fit, or qualification. The remaining-gate list preserves all of those obligations.

## Evidence limits

This review establishes publication fidelity and safe plan-level standing only. I performed ordinary reads and hashes; I did not execute builds, tests, compilers, native code, fixtures, arithmetic scripts, or receipt lanes. No implementation behavior, source/ABI/charge conformance, inventory binding, integration, root implementation assent, or product qualification follows from this verdict.
