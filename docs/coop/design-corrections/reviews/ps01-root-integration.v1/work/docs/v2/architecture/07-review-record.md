# V2 Architecture Review Record

> **Status:** REVIEW FINDINGS RECORDED — corrections require re-review
> **Authority:** Review evidence only; this record applies no V1 or V2 successor.
> **Active checklist:** [OpenSIP V2 Decision and Readiness Register](08-decision-and-readiness-register.md)

This document records the five independent review lenses and the correction
disposition taken in this pass. It contains no competing readiness checklist.
Actionable status, owners, evidence, and blueprint impact live only in register
entries DR-201 through DR-205 and, for the post-review correction below, DR-122
and DR-G17.

## Post-review correction: SARIF output surface

**Finding after the first five reviews.** Read-only comparison with the current
CLI prototype confirmed implemented SARIF 2.1.0 findings output, while the
corrected V2 documents named only generic human/machine projections. That wording
did not explicitly carry forward the SEALED V1 SARIF projection contract.

**Disposition.** Accepted for the second-review context. V2 now preserves SARIF
2.1.0 as an optional host-owned projection for applicable findings/results, not
as a format every command must emit and never as policy, evidence, or D9
authority. The semantic document and claim matrix pin the retained V1 field and
parity obligations; [DR-122 and DR-G17](08-decision-and-readiness-register.md)
own the V2 applicability, stable-machine, and parity/loss acceptance evidence.
This post-review correction has not been independently accepted and changes no
V1 standing.

## Semantic correctness review

**Finding.** The prior diagram collapsed distinct V1 phases into one happy path
and used Run/evidence names as if their exact recipes and final integration were
settled. It omitted RequestId-before-validation, rejected/stored-view branches,
pre-attempt identity exclusions, finalization refusal, failed commit, and
post-commit output failure. It also needed stronger host-only candidate admission.

**Disposition.** Accepted. The semantic document now separates phase/branch
flows, marks identity recipes structural-only where V1 is parked, distinguishes
verdict from HostTermination, and closes component authority to candidates and
intermediates. The second-review correction also moves public command exit
mapping after required output handling: D9 v1.14's exact serialization golden
preserves an already settled Run while returning
`OUTPUT.SERIALIZATION_FAILED`/exit 4. See
[DR-201](08-decision-and-readiness-register.md#five-review-findings-and-dispositions).

## Delivery and operations review

**Finding.** The earlier V2 prose deferred architecture-critical multi-version,
generation, storage, recovery, trust, repair, replay, and gate requirements to a
future blueprint. It could allow a nominal offline analysis closure without the
durable mechanics required by current product posture.

**Disposition.** Accepted. Architecture now requires immutable coexisting
installs, lock-selected generations, leases/refcounts, fail-closed recovery,
mandatory storage for authoritative analysis, and a centralized release-gate
registry. Concrete mechanisms remain open, but the properties are hard gates.
See [DR-202](08-decision-and-readiness-register.md#five-review-findings-and-dispositions).

## Prototype-lessons review

**Finding.** Prototype lessons were accurately named but insufficiently tied to
single-lifecycle, no-lockstep, no-reuse, crash-safety, and conformance outcomes.

**Disposition.** Accepted. The V1 relationship and distribution/operations
documents now map each retained or rejected lesson to the component, protocol,
generation, and conformance boundaries. See
[DR-203](08-decision-and-readiness-register.md#five-review-findings-and-dispositions).

## V1/coop invariant-coverage review

**Finding.** “Advanced heads win” was unsafe. It did not require exact selector,
derivation, checker, claim, freeze, and product-disposition resolution; broad
“preserved” labels could promote passed-but-unapplied identity/evidence material.
Retention product posture and inherited freeze conditions needed exact treatment.

**Disposition.** Accepted. V2 now has a reproducible baseline manifest, a
reviewed claim matrix, stop-on-conflict rule, inherited prerequisite ledger, and
precise preserved/proposed/open labels. See
[DR-204](08-decision-and-readiness-register.md#five-review-findings-and-dispositions).

## Small-core and component-boundary review

**Finding.** “Core” conflated distribution, semantic host, and pure evaluation;
“small” lacked a falsifiable closure/TCB and gates. Compatibility implied shared
version windows. The component proposal also exceeded P-1/P-2/G3 without naming
required product successors, and persistence could be read as optional for
authoritative analysis.

**Disposition.** Accepted. The distribution document separates all three cores,
requires a published mandatory closure/TCB, keeps per-surface compatibility
matrices, names product-boundary successors, and makes verified storage mandatory
for authoritative offline analysis. It also makes language-native analysis
quality a product/readiness requirement without requiring Rust implementations
for every analyzer or inventing a supported-language list, and proposes a
self-contained signed runtime/tool closure rule so users do not manage ambient
language dependencies. A common component packaging contract now normalizes
different language build adapters without selecting their implementation tools.
The monorepo model now selects isolated per-component lanes while retaining
separate shared-core and cross-component integration/release qualification.
See
[DR-205](08-decision-and-readiness-register.md#five-review-findings-and-dispositions).

## Review standing

The corrections are `PROPOSED-CLOSED-FOR-REVIEW`, not independently accepted.
Each lane must re-review the corrected documents and record its disposition in
the central register. No review may clear inherited V1 blockers through a
V2-local finding disposition.

## Second-review correction disposition

The narrow second-review pass accepted these additional findings without
changing V1 authority:

- authority reproducibility now separates artifact bytes from pinned review,
  adjudication, closure, and checker standing; VERSIONING, FACT-IDENTITY/R-1
  closures, evaluation-proof v8/v13 dual heads, R2-FINAL-03, FACT-PLANE closure
  items, and CFG-6/TM v3 status are explicit;
- pre-admission rejection and post-commit output serialization now match the
  exact V1 identity/finalization order;
- blueprint entry uses DR-001–011 plus applicable V2 decisions, while DR-012
  remains release/authoritative-launch qualification only;
- lifecycle crash points, grant revocation lineage, platform loader/ABI TCB,
  anti-lockstep skew, state ownership, control/data races, and component failure
  containment have named gates;
- prototype lessons use a clean source commit; language-quality corpus,
  capability, measurement, and parity evidence is explicitly OPEN rather than
  inferred from that commit;
- common component SDK/operability, standard CLI plus optional non-authoritative
  TUI, and applicable SARIF projection are explicit; and
- MVP trusted-component fault containment is separate from deferred third-party
  sandbox/marketplace scope.

All are `PROPOSED-CLOSED-FOR-REVIEW` or `OPEN` in the central register; none is
qualified or demonstrated.

## Targeted third-review correction disposition

The final narrow pass accepted the targeted findings as documentation
corrections, without changing V1:

- CFG-6, evaluation-proof v13, FACT-PLANE/FACT-IDENTITY checkers, and the
  VERSIONING v14–v17 review/successor lineage now have exact pins, selectors,
  and recorded execution standing rather than symbolic status claims;
- DR-011 now has an exhaustive per-residual subledger and cannot pass while any
  row is open, partial, stale, rejected, or unreviewed;
- DR-201–205 require acceptance or evidence-backed individual routing/closure
  of every rejecting finding;
- laws 1–19 are explicitly preserved, including laws 3 and 11;
- DR-123 now makes standard CLI/machine-output evidence mandatory for every
  first slice, while optional TUI evidence is isolated at DR-129; and
- DR-105/DR-G09 now require a deterministic durable revocation/effect-commit
  linearization, including already accepted requests and irreversible effects.

These corrections remain non-binding and unaccepted until the corresponding
review/decision owners record evidence in the central register.

### Surgical EP13 standing correction

The targeted follow-up found that the prior evaluation-proof v13 summary pinned
the artifact/review/checker and four headline selectors, but did not reproduce
the complete residual standing behind `PASS-WITH-RESIDUALS`.

**Disposition.** Accepted as a documentation correction only. The status
manifest now pins canonical selector digests for all seven independent-review
observations (`IR-EP13-NB-01..07`), all nineteen candidate limitations
(`RES-EP13-01..19`), the AX6/AX9/MD5/RX2c per-variant rows, and both four-member
escape-set arrays. It also retains measured default execution exit 0 and
`--selftest` exit 0 with `SELFTEST-PASS` for 75 mutations, including stdout
digests and line counts. The claim matrix and DR-011-R12 route the complete set
with scope and required disposition.

This evidence reproduces what the pinned checker accepted and what its
independent review left open. It does **not** prove semantic correctness, close
an observation or limitation, defeat the four measured escapes, apply or seal
v13, supersede evaluation-proof v8's V10 claim-shape obligation, or clear
Phase-1A/V10 dependencies.

## Targeted third-review scope

The next review should be narrow and adversarial:

1. reproduce both authority/status manifests and every matrix standing selector,
   including evaluation-proof dual-head and VERSIONING divergence;
2. compare pre-admission, Run sealing, required postconditions, output failure,
   and public exit ordering against D9 v1.14 goldens;
3. challenge DR-G18–G22 with crash/race/revocation/loader/state-class/component-
   failure mutations and anti-lockstep version skew;
4. verify prototype source claims are commit-pinned, quality/parity claims stay
   OPEN until backed by a digest-pinned corpus and accepted measurements, and
   CLI/SARIF/TUI/common-SDK behavior never acquires semantic authority; and
5. confirm MVP/future scope preserves current product exclusions and does not
   turn deferred sandboxing into an MVP gate.
