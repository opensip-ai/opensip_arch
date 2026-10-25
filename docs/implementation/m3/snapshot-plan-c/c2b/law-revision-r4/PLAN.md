# C2b snapshot edge-cap law revision, plan r4 (census-validated layout envelope)

Capability route: R3-FRONTIER
Codex: gpt-6-astra / high
Claude: claude-opus-5-5 / high
Claude long-horizon lead: claude-opus-5-5 / high
longHorizonLead: true; the Claude lead owns this plan through law acceptance and adoption.
Escalate when: measured maxima conflict with an accepted law that this plan does not amend, or the reviewer and lead disagree on whether the M2 matrix covers the layout domain.
Escalation route: R4-EXCEPTIONAL only with separate owner authorization; not selected.
Independent review: Codex gpt-6-astra/high (different vendor from the Claude lead) for this plan, the measurement procedure, its results and the law record.
De-escalate when: the successor law is accepted; adoption (M5) is local implementation at R1-BALANCED with deterministic tests.
Exceptional authorization: none; max/xhigh prohibited.

Status: lead draft r4, 2026-10-25. r2 (`PLAN-r2-as-reviewed.md`) drew
REQUIRED-CHANGES RC-1..RC-7 (`codex-review/REVIEW-r2.md`) and r3
(`PLAN-r3-as-reviewed.md`) drew R3-1..R3-3 (`codex-review/REVIEW-r3.md`); each
is answered below and in the closing tables. Replaces r1
(`/tmp/opensip-implementation/continuation-authority-refresh-2026-10-22/c2b-law-revision-r1/PLAN.md`,
sha256 6226f936…) once accepted. r1 and r2 stay as history.

## Owner decision and what it changes

**Owner decision, 2026-10-24:** revise the C2b snapshot edge cap by a
census-validated law revision, reviewed by a different vendor, instead of the
open-ended LR-2 source/ABI proof programme.

r1 required the layout term to be a *sound, source-priced* bound (LR-2/LR-3)
before any cap. r2 replaced it with a measured maximum but wrongly claimed to keep
r9's rule (Codex RC-1). r3 states the change plainly.

## The successor law (proposed text, amending r9 section 5 and LD-C2B0-7)

1. **Terms.** M1 assigns every charge of the selected operation, once, to exactly
   one of three families:
   - *T*: bounded non-layout work over item 5 (walk, session, sealing, C1b VCS, and
     C1c's read-set terms once accepted). Its owning semantics are r9's, but its
     numbers are re-derived by M1: wherever M1a adds or changes a charge in these
     families, *T*sound is a conservative updated bound on the existing bounded
     domain, with current source, model, anchor and vector correspondence, fixed
     before M3 runs and checked before M4 selects a cap. Existing terms are reused
     only where their prices and premises still hold.
   - *L*: C2's layout term (reach, graph state, captures, parses, record
     construction, sort, admission, retention, encoding).
   - *N*: the remaining non-row and refusal-domain work that r9 section 5 already
     leaves to the margin (directories entered, non-row names, link and special-file
     copies), unchanged in kind.
   If M1 finds a non-layout family that can only be bounded empirically, the law
   names it and amends its guarantee explicitly; it is never folded into *Lmax*.
2. **The layout envelope.** *L* is not priced by a source/ABI proof. Its bound is
   *Lmax*: the componentwise maximum charged layout work measured by the reviewed
   M3 run over the reviewed M2 matrix. *Lmax* is an empirical envelope, not a
   sound bound over the item-5 domain, and is recorded as such.
3. **The cap rule.** Componentwise, cap = the smallest power of two at least twice
   max(*T*sound + *Lmax*, eligible census maximum), computed by r1's `cap_rule.py`,
   with *T*sound as re-derived in M1.
   A cap is never lowered by this law: where the new value is below the current
   cap (2^21 objects, 2^24 edges, 2^33 bytes) the current cap stays.
4. **The guarantee, stated honestly.** "Fits" means the operation's charged work
   stays within the snapshot ledger's caps; it never erases a required non-budget
   refusal. At the new caps, componentwise:
   - a tree within item 5 fits if its bounded work satisfies *T* ≤ *T*sound, its
     layout work *L* ≤ *Lmax*, and its remaining non-row work
     *N* ≤ cap − (*T*sound + *Lmax*), each charge counted once (this keeps r9
     section 5's margin condition, with the revised partition);
   - the fit claim covers the reviewed bounded positive cases of M2 and the
     *eligible*, successfully measured lead-readable census population only. Every
     other M2 row (one-byte-over Encoding, predicate refusals, stress cases) must
     reach its specified typed outcome, not a success. Readability and the 44-entry
     authorization manifest are not eligibility; authorized-but-ineligible, failed
     and incomplete cases stay visible and separate from the cap-selection maxima;
   - work beyond these refuses `WORK.BUDGET_EXHAUSTED`, typed and never
     truncated; the typed-refusal regime of r9 section 5 is unchanged.
   It does **not** guarantee that every item-5 tree's layout fits. That
   difference from r9's sound-subtotal guarantee is the explicit law change the
   owner decision authorizes.
5. **Unchanged.** The discovery and generic ledgers, B2's pre-walk discovery-ledger
   captures, r9's typed-refusal list and r9's other terms.

## Subject: the snapshot-pipeline candidate, frozen first (RC-2)

The 28,806,258-edge admission figure (21,026 rows, 183 padding bytes) belongs to
the C2b `node_modules_layout` fixture
`node_modules_layout_tests::the_record_admits_at_4_mib_and_refuses_one_byte_over`,
which uses `WorkLedger::new()`. r1 was right and r2's "correction" was wrong.
That code is in the unaccepted P+D snapshot pipeline (C2b-0 layout, C1c read set,
custody), not on main e39cee8.

On 2026-10-25 the lead split that pipeline off the configuration unit: it has
never compiled (E0599 `exclusion`, E0107 in `workspace_t2_link_tests.rs`, 25
warning-denied Clippy errors in security, the `LayoutBound` classification). It is
now its own unit, **SP-1**. This plan measures SP-1 only after SP-1 compiles,
passes its own tests and is frozen with an LR-1-style manifest: exact candidate,
schema/registry, model, authorities, toolchain, and accepted/unaccepted status.
The mandatory 4 MiB layout positive and its one-byte-over `LayoutRefusal::Encoding`
refusal are bound to that frozen subject unchanged. The seal and VCS 4 MiB tests
are separate controls, not substitutes.

## Work packages

### M0. SP-1 readiness and freeze (pre-cap)
SP-1 compiles, passes warning-denied Clippy, and every ordinary correctness failure
is fixed (lead-authored, Codex-reviewed) or dispositioned. Then freeze the complete
subject and its test population with the manifest above. The mandatory 4 MiB layout
positive cannot pass yet: under `WorkLedger::new()` its admission precharge alone
(64 + 128 × 21,026 = 2,691,392 edges before other admission work) exceeds the
131,072-edge cap, and the full admission figure exceeds the current snapshot cap.
M0 records it as the one explicit known cap-incompatibility failure, an unresolved
blocker to production acceptance. It is not ignored, relabelled as passing,
reduced or re-expected. No measurement before M0.

### M1. Charge coverage, isolation and harness (RC-3, RC-5, RC-6)

**M1a. Finite charge audit of the selected operation.** Every allocation and
input-proportional work family on SP-1's walk, layout, read-set, seal (with its
VCS observation) and reuse paths, including refusal and reservation paths, is
mapped to an existing or new covering charge. Conservative bounded envelopes are
acceptable; std ABI proofs are not required. Terminal error-path copies are priced
(their sizes are bounded by path and name limits), not exempted. Known items from
the lead's reconnaissance (`CHARGE-SITE-AUDIT.md`): seal descriptor
parse/schema/canonicalization (today bounded only by the evaluator work counter
`SCHEMA_BUDGET` at `snapshot_seal.rs:41-43`, a work unit, not bytes), SHA-256 over
inventory, VCS record and carrier, listing sort, per-child ignore/boundary scans,
the seal count pass, and the constant-edge `parse_cost`.
**Shared code:** `ListingConversion::finish` (`discovery_walk.rs:390`) serves both
discovery and the snapshot walk. New charges go on the snapshot side of an explicit
charging boundary, so discovery's totals, model, vectors and receipts do not
change. Any change that does move discovery's totals is a separate reviewed change
under discovery's law.

**M1b. Measurement isolation.** The raised-cap constructor
`WorkLedger::measurement_profile()` sits behind a `measurement` Cargo feature of
opensip-platform and also behind `#[cfg(debug_assertions)]`, and the crate carries
`#[cfg(all(feature = "measurement", not(debug_assertions)))] compile_error!(...)`,
so no release artifact can contain it under any feature selection, including
`--all-features`. Controls: a release build with `--features measurement` fails to
compile; the shipped artifact matrix (each release binary and package, default and
all-features where supported) is built and its feature graph pinned with
`cargo tree -e features`; a positive control shows the harness can use the profile
in a debug test build.

**M1c. Harness in the accepted order.** Per A-C2B0-1
(`snapshot-plan-c/c2b/PLAN-r3.md:154-167`): B2 pre-walk captures stay on the
discovery ledger; then on one snapshot ledger, in order, the walk, C2's layout,
C1c's read set, then the seal, which performs the single VCS observation through
its owner (`snapshot_seal.rs:424`). Capture sets, reuse and spent work are kept on
refusal, with no restart or hidden retry. Per-phase deltas are taken at phase
boundaries so nested seal/VCS work is counted once. `WorkLedger::used()` includes
unused reservations (`work_ledger.rs:192-194`), so the harness reports charged
totals and outstanding reservations separately and reconciles them with the final
ledger. Controls prove the order, the single VCS observation and the
reconciliation before any total is used.

**M1d. Measurement-only positive.** A separately reviewed measurement test drives
the same unchanged 4 MiB case through the harness under the measurement profile, to
measure it. It does not replace or relabel the original test, which stays the known
failure until M5.

M1 deliverables: M1a source changes with controls, the measurement feature and
harness, the measurement-only positive, the complete charge assignment to *T*, *L*
and *N* with the re-derived *T*sound (model, anchors and vectors current), the
re-verified charge-site table, and independent Codex review.

### M2. Coverage and outcome matrix, and population (RC-4)
A table, reviewed before M3, with one row per relevant limit or branch: its
source authority, exact parameter, physical construction (or, where a physical
tree is infeasible, the lower-level predicate control), expected success or
refusal, and whether its total participates in *Lmax*. Rows include at least:
- the 4 MiB layout record and its one-byte-over refusal; the 100,000-row predicate
  versus the largest jointly feasible 4 MiB layout (`c2b/PLAN-r3.md:136-144`);
- the 8 GiB total-file-byte bound (`snapshot_seal.rs:38-40`) and read-attempt
  boundaries;
- path length with long common prefixes, UTF-8 and escaping; depth, separating
  LogicalPath limits from filesystem limits; components per path;
- listing entry-count and name-byte limits, and wide listings against ignore,
  boundary and member scans;
- layout aliases, cycles, reuse, exclusions and changed observations;
- r9 section 1.1's joint descriptor constraint, so that independently unattainable
  maxima are not combined.
Bounded positive cases are separate from refusal-domain stress cases; a stress tree
that refuses is a correct refusal, not a reason to raise a cap. Jointly feasible and
uncovered combinations are listed explicitly.
**Population:** r9 section 4's 44 lead-readable entries (39 repository entries
plus 5 workspaces), reconciled against current authorization metadata without
opening held-out stores. Blind mode and its receipt interval are frozen separately;
blind margins never select caps. No private413, real-home, installation, key or
held-tree access.

### M3. One bounded, reviewed run (RC-7)
Before the run, a reviewed execution envelope: memory (RSS) limit, disk limit for
fixtures and targets, wall-time limit, and fixture size limits. An external
resource stop is recorded as an incomplete failure, never as a maximum. A case that
reaches the measurement profile's caps is a finding. Toolchain, source and fixture
pins are frozen; ordinary failures stay failures.

### M4. Successor law record (RC-1, RC-7)
*Lmax*, *T*sound, census maximum and the resulting caps per component; which case
set each maximum; the guarantee text above with its non-claims. Exposure is stated
with consistent definitions: the largest fixture's measured charged totals, peak
RSS and wall time are *representative exposure at its own usage*; exposure near the
proposed caps is a separate bounded analysis (charged bytes are accounting, not
peak RSS; file-content bytes are a third quantity). Reviewed by Codex; accepted by
the lead under the owner decision.

### M5. Adoption
As r1 LR-5, kept whole: the new constants with a comment citing the successor law;
the unchanged 4 MiB layout positive moved onto the production snapshot profile and
now passing, with its exact size, digest, canonical agreement and early
one-byte-over Encoding refusal, in the complete final test population; C1-T27
updated; the 17 controls and the full30/full39 ordered procedure with its
mutations, restorations and model/anchor/vector coherence; fresh preflight and
assent; frozen-result review; receipt baseline/delta/blind refresh; inventory,
contract and description binding. Commit and push only the accepted integration.

## Sequencing
M0 first. M1 and the M2 table can be prepared in parallel once SP-1 compiles. M3
needs M1 and M2 reviewed, M4 needs M3, M5 needs M4 accepted. The configuration unit
and other units are not blocked by this one.

## Response to review r2

| Finding | Where answered |
| --- | --- |
| RC-1 law change stated, not "keeps r9" | Successor law 1-5 |
| RC-2 provenance manifest, correct fixture identity, candidate not HEAD | Subject; M0 |
| RC-3 accepted order, single VCS, charged vs reserved | M1c |
| RC-4 coverage matrix and pinned population | M2 |
| RC-5 enforceable isolation incl. explicit/all features | M1b |
| RC-6 finite audit, terminal copies priced, shared-sort boundary, SCHEMA_BUDGET unit | M1a |
| RC-7 bounded execution, honest exposure | M3, M4 |

## Response to review r3

| Finding | Where answered |
| --- | --- |
| R3-1 circular M0 gate | M0 (known cap-incompatibility kept as an explicit blocker); M1d measurement-only positive; M5 unchanged positive must pass |
| R3-2 *T*sound tied to the post-audit charge model | Successor law 1 (*T*, *L*, *N* assignment; *T*sound re-derived before M3/M4); law 3; M1 deliverables |
| R3-3 fit guarantee and outcome domains | Successor law 4 (explicit margin condition, eligible census only, typed outcomes for other rows, "fits" defined) |

