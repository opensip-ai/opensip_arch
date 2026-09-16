# Bounded assessment — D9 successor-artifact obligation and its application-facing account

**Assessor:** actual Claude, bounded application/design coauthor assessor. **Not** the fresh
independent20 reviewer, **not** blind consumer9, **not** final application acceptance. No product
implementation, no commit, no publication. All source/history/staging read only; writes confined to
`/tmp/opensip-design-corrections/v20-d9-application-assessment.v1`.

**Subject:** frozen source20 at `/tmp/opensip-design-corrections/candidate-subject.v20`, manifest
`candidate-subject.v20.json` sha256 `878e5beb…f3c` — **verified by recomputation**. 11932 files,
`reviewPending: true`, `applicationPending: true`. Not accepted; nothing here assumes acceptance.

## Scope actually read (every byte verified against the manifest entry)

| Path | sha256 | Why |
|---|---|---|
| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` | `f20b8353…1e31` | anchor: `/x-opensip-public-route-registry/successorArtifactObligation` and the whole registry |
| `docs/coop/design-corrections/workflows/schemas/common.schema.json` | `d379c2e6…1ae3` | actual selected admission schema: `$defs/D9FaultCause`, `StepTermination` |
| `docs/coop/artifacts/d9-exit-contract.v1.14.json` | `8dd33038…7da31` | inherited artifact; enum, codeMaps, codeVocabulary, goldens |
| `docs/coop/design-corrections/check-integration.py` | `6102bfdf…1e31`* | CB6-ADV-3 enforcement block (lines 374–405) |
| `docs/coop/design-corrections/inherited-residuals.proposed.md` | `4b2b992b…62d5` | DR-007 parent, DR-011-R08 residual |
| `docs/coop/design-corrections/current-source-map.proposed.md` | `397ba583…78f1` | full file; the application's designated navigation instrument |
| `docs/v2/contracts/product-v1/workflows-and-surfaces.md` | `8d4d9c89…6b1d` | §0 superseded-selector table, §9 D9 goldens/branch contract |
| `docs/v2/contracts/product-v1/native-evidence.md` | `bf2cf6e9…e499` | §2755–2810 selected D9 composition and origin-routing table |
| `docs/coop/design-corrections/post-reset-dispositions.v20.proposed.json` | (manifest-listed) | v20 item ledger |

*digest as listed in the manifest. Read-only staged tools: `assemble-records.py` `aadf2dd9…3769`,
`apply-v20-advisory-records.py` `508b0855…6bdc`, `check-finalizer.py` `f93a17e1…2379`,
`row-map-draft.json` `01e37c6f…5fcf`, `launch-application-review.py` `b858bfdd…4565`; draft
afterimages `08-decision-and-readiness-register.md` `193c82ad…7c3c` and `09-v1-to-v2-claim-matrix.md`
`cfd685c8…5886`. I did not read the other active review's output or private thinking.

## The source claims, checked against actual selectors

Every normative assertion in the registry block holds:

- The inherited artifact's `$.scenarioAxesSchema.properties.faultCause.enum` has **11** members
  (`none` + 10 causes) and no `host-invariant`; `codeMaps.faultCauseToErrorCode` has no such key.
- `SYSTEM.OUTCOME.ILLEGAL_STATE` **is already** in the inherited `codeVocabulary.errorCodes` and has
  no preimage in the cause map. So the extension genuinely adds no error code, class, exit code or
  reason code, and the "total and injective" precision note is correct: totality is over the declared
  cause domain, so a preimage-free code was never a violation.
- The selected `common.schema.json#/$defs/D9FaultCause` has **12** members — exactly the inherited set
  plus `host-invariant`. `check-integration.py` asserts precisely that set equality, plus that the
  inherited artifact still omits it, plus that the disclosure text is present and attributed. The
  three halves really are held at once, not asserted in prose.
- The inherited artifact is byte-exact: its live digest equals its manifest digest, and the same
  digest is already pinned by the draft application in both DR-007 and the D9 claim-matrix row.

**No admitted current consumer is forced to the inherited 11-cause enum.** I checked the path a
consumer actually takes. `workflows-and-surfaces.md` §0 succeeds `$.hostTerminationUnion` field
closure with `common.schema.json#/$defs/StepTermination` (12 causes via `$ref`), and retains v1.14
only for the class/code/exit table — which the extension does not touch. §9 then enumerates all
eleven non-`none` causes **including** `host-invariant` in the branch contract. `native-evidence.md`
§2764 routes the host-generated internal layer to `SYSTEM.OUTCOME.ILLEGAL_STATE` / `host-invariant`.
The only reader that gets 11 is one validating against the historical artifact alone, which the
product contract explicitly marks superseded for field closure. That is the disclosed residue, not a
live defect. **No product behavior choice is left open, and I invented none.**

## Disposition of the mandatory obligation

**It belongs later, not now — and the basis is structural, not convenience.** What is owed is a
*successor artifact published by the D9 exit-contract unit*. That is a new normative source artifact.
Publishing it inside this application would mean minting reviewed-normative bytes that independent20
never saw, forcing a new freeze and a new independent design review of an artifact whose owning unit
has not authored it. The existing normative rules already assign it: `owedBy` "the D9 exit-contract
unit"; `neverDischargedByRepinning` "Publishing the successor D9 artifact belongs to that unit";
`whatIsNotOwed` "Nothing in the product source. The selected composition above is complete." Nothing
in the design is incomplete pending that artifact. Implementation readiness at *design* level does
not depend on it. Its later *qualification* is release-gate work, separately unperformed (32 gates).

## Finding

**D9-APP-1, severity SHOULD, application-only.** The current prepared application does **not** falsely
discharge the obligation — DR-007 and DR-011-R08 stay open, DR-007 remains HARD-BLOCKED in the
historical table and names "D9 successor to v1.14" as remaining independently required work, and
condition 5 stays NOT MET. But **no applied record names the obligation at all.** `host-invariant`
appears nowhere in `application-assembly.v1`, nowhere in the 17 draft afterimages, and nowhere in
`post-reset-dispositions.v20.proposed.json` except an unrelated V20-ROOT-4 routing item.
`current-source-map.proposed.md` — which every inherited chapter is instructed to be read through,
and whose middle column is literally "Potentially misleading selector" — has **no row for
`d9-exit-contract.v1.14.json`**. Meanwhile condition 1 is asserted MET via the applied inherited
dispositions covering all DR-001–011 and all sixteen residuals. The registry's own stated purpose is
that "a later pass reading this registry alone cannot mistake the obligation for a closed item"; the
applied records, not the native route registry, are what a later pass will read. The obligation is
therefore *true but invisible* at the application surface. That is an omission, not a false claim.

## Remedy

`proposed-addendum/assemble-records.d9-obligation.patch` — exact, minimal, style-matched: a
`carriedCrossUnitObligation` field on exactly two rows of `inherited-residuals.applied.v1.json`
(DR-007, DR-011-R08), pinned by JSON-pointer `ref()` into the frozen snapshot, standing
`LIVE, MANDATORY, CROSS-UNIT AND UNDISCHARGED AT APPLICATION`, with an explicit `notDischargedBy`
naming condition 1, ACCEPT-DESIGN, activation and the final application review. Three `assert`s guard
minting on the accepted bytes still carrying the obligation. It is **not** a vague future gate: owner,
owed artifact, exact member, exact target code and exact evidence selectors are all named.

**No additional source freeze or new independent design review is required** for this remedy — it
touches only generated application records. Adding the missing v1.14 row to `current-source-map.proposed.md`
*would* be a source change requiring re-freeze and re-review; I do **not** recommend it, because the
product contract already routes consumers correctly and the applied-record pin closes the visibility
gap at lower cost.

## Limitations

Bounded read; I did not assess the other product contracts, the six checks, or the 32 gates. I did
not execute `check-integration.py` (I read its assertions against the actual selectors instead). The
patch is unapplied and untested against a real assembly run — no accepted inputs exist to run one.
Codex agreement and root review are still required; this is one assessor's account, not acceptance.
