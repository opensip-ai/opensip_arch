None of the four proposals can be accepted as they stand: each gets a separate changes-required verdict, and the configuration one is narrow. `review.json` and `review.md` are written in the review directory, with probes, results, private copies and mutants under `probes/` and `runs/`.

**Custody:** for all four subjects the manifest SHA, exact file set, per-file hashes and external pins matched before and after my runs. No bytecode reached any subject, and the architecture `__pycache__` is unchanged. The root suites pass on private copies (10 + 10 + 8 + 9, exit 0). Those are reference tests over synthetic inputs, not runtime custody.

**Mutants:** 16 of 18 were killed. Two catalogue mutants survived: dropping the canonical byte cap, and letting capabilities skip the declaration check. Two "kills" prove little. CAT-M5 dies only because a root test pins the mixed-up absence label I criticise below. CFG-M4 dies on ID shape checks only.

**Two controls corrected:**
- CAT-C4 was meant to test a float-bearing listing but actually refused earlier on a digest mismatch, so I kept it as a digest-swap control. Float refusal is still covered by the reproduced root test.
- My own first history probe run crashed with a `NameError`. I fixed and reran it.

## 1. Presentation catalogue (RP-DO-01/06/07/08): changes-required
The closure association is sound: exact Blob, no embedded `closureId`, and an invalid listing never downgrades to absence.
- **Blocking:**
  - Capability descriptions are tied to whichever closure ships them. The native release capability registry actually owns capabilities (`native-evidence.md:1014-1022`), and two closures can currently describe `reachability` in contradictory ways.
  - A closure with no catalogue and a catalogue whose bytes weren't retained both show as `catalog-not-retained`.
- **Required:**
  - A row missing from a retained listing is labelled "not retained", and selection accepts keys outside the declaration index.
  - The receipt drops `tree`, `platform` and `protocolMajor` from the security receipt it claims to reuse.
  - The recipe `selector` is the same set of constants for every recipe.
  - Names and descriptions accept bidi overrides and control characters.

## 2. Configuration disclosure (RP-DO-04): changes-required (narrow)
The substance holds up:
- The pinned resolver's output projects with a matching digest and no leaks.
- A changed current configuration against an older Plan digest is refused, so there's no current-settings fallback.
- 32 variants differing only in redacted values produce identical output apart from the digest.

Required fixes:
- `planId` isn't tied to the admitted Plan (any valid ID is accepted), and the Plan itself isn't validated.
- The output has no `verifiedInDocument`/`hostAsserted` provenance split.
- Source failures aren't mapped to the report's existing unavailable, corrupt or incompatible panel states.

## 3. Attempt duration (RP-DO-11): changes-required
The lifecycle boundaries, retry and abandoned semantics, identity independence and floor arithmetic are right (20,000 random cases checked).
- **Blocking:** the v4 `Attempt` schema accepts abandoned+measured and completed+`supervisor-lost`. The outcome/reason rule exists only in `timing.py`.
- **Required:**
  - A malformed clock sample paired with a missing one returns `clock-unavailable` instead of refusing.
  - The step sum accepts duplicate ExecutionIds and negative values, and crashes on bad input.
  - Retained invocation major-1 records exist but have no report state; they should use the existing incompatible state rather than an unowned refusal.

## 4. Explicit history selection (RP-DO-12): changes-required
Argument order is kept, there's no `latest` fallback or silent baseline insertion, a requested ID equal to this invocation's Run fills its slot without a lookup, and the automatic no-flag mode is unchanged.
- **Blocking:**
  - The proposed refusal contradicts the existing route for a non-applicable format (`REQUEST.UNKNOWN_OPTION` / `OUTPUT.FORMAT_NOT_APPLICABLE`, `workflows-and-surfaces.md:1141-1142`). It also ignores the existing `EVALUATION.SELECTION_LIMIT` for more than four IDs.
  - It neither pins nor types the query owner that RP-DO-12 names (`query-projection-contract.v3` §1, `run.show`).
- **Required:**
  - Freeze the exact CLI flag record for all eight HTML commands.
  - A bad host-supplied current Run ID currently becomes a user-facing request rejection; it should be an internal fault.
  - Define when the read snapshot is taken, including for a pivot Run this same invocation creates.
  - Write the explicit-mode panel variant and its provenance list.
- The fixed selection overhead is 896 canonical bytes, plus 533 for four minimal unavailable rows.

Each verdict in the review lists its remaining integration work: report carriers, host, clock, store and catalogue implementation, and final browser leakage and accessibility tests. I didn't touch the author02 report evidence work or the interruption-envelope work.
