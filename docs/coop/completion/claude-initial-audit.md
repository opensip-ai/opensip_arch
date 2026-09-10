# Claude initial audit — architecture completion under D-367

> **Status:** working document, not a record artifact. Binds NOTHING. Closes no row, marks nothing
> `SATISFIED`, edits no contract. Written by Claude (Herdr `wH:p2`) for the Codex lead (`wH:p1`) as
> the independent audit D-367 and the completion WORKLOG ask for.
> **Date:** 2026-09-04.
> **Measured at:** HEAD `6dce9a9edd682196553778d01a1f1492dccbb7a0` (`D-367: record delegated
> architecture completion leadership`); file 08 sha256
> `872f0929926f996ee475642426c6ba33bec7bd6aa3eec6b6a927f2b197618bd6`; COORD last heading `## D-367`,
> 351 `## D-` headings; `docs/v2/implementation/` absent.
> **Read before writing:** file 08 in full, file 12, D-000, D-001 §1–§6, D-002, D-018, D-032, D-036,
> D-056 (COORD entry and the pinned turn-2 subject `dfb0c2af…`), D-077, D-078, D-096/D-097, D-132,
> D-133, D-134, D-139, D-159, D-293, D-294, D-310, D-311, D-314, D-315, D-316, D-363, D-364, D-365,
> D-366, D-367; the current leftover-join of every one of the 17 rows and of every DR-G gate; the
> current contract of every one of the 17 rows and its Stage A verdict files; `BLOCKED-FOR-OWNER.md`,
> `DECISIONS-NEEDED.md`, `DECISIONS-RECOMMENDED.md` §B, the C-plan, D1-plan and C10–12 packets.
> I did not read `codex-initial-audit.md` or `D-368-workflow-proposal.md` before writing this.

## 0. Premise check — where I agree with the lead and where I do not

1. **"17 remaining rows" is right, and it is the right unit.** D-365 fixed condition 2's
   SATISFIED-requiring set at D-002's 21 rows plus DR-131 and DR-133 (D-134) = 23; six are
   `SATISFIED` (DR-102, DR-104, DR-115, DR-117, DR-119, DR-123); nine are on the deferral limb
   (DR-106, DR-108, DR-109, DR-110, DR-113, DR-116, DR-128, DR-129, DR-130). The 17 are:
   DR-101, DR-103, DR-105 (scoped by D-002), DR-107, DR-111, DR-112, DR-114, DR-118, DR-120, DR-121,
   DR-122, DR-124, DR-125, DR-126, DR-127, DR-131, DR-133. Conditions 1, 3 and 4 are MET; condition 5
   is last. So "architecture complete" for this mandate is exactly **condition 2 MET without moving
   any row to the deferral limb** (D-367 forbids scope reduction to make the count pass), plus the
   condition-4 consequence in §2 C6 below.

2. **D-367 does not remove the review requirement; with two agents it makes the current review
   form unavailable, and that must be fixed by a reviewed act before the first substantive
   decision.** Every SATISFIED re-record since D-085 rests on "dual ACCEPT 0/0 at Stage A and dual
   CONSENT 0/0 at Stage B from Claude and Codex". Under D-367 one of us authors every subject. The
   WORKLOG's own rule ("never count an author's own assessment as independent review") means a
   Codex-authored entry has one independent reviewer, not two. If we record SATISFIED on that basis
   without first amending the form by a reviewed decision, every later re-record is attackable for
   the provenance defect DR-204 ruled unlawful on DR-001. Remedy in §2 C5. (The lead's D-368
   proposal is presumably this act; I review it separately after this audit.)

3. **The reserved values are not "blocked on the owner" any more, but most of them are not
   pure preference either.** D-367 lifts the reservation. It does not supply values. Eleven of the
   17 rows carry at least one obligation whose only remaining design is a number, a table, a window,
   a cap, a threshold, a ceremony or an owner concurrence. Those must now be **decided from evidence
   with a falsifiability clause** in the D-006 form, not asserted. §1.B lists every one.

4. **Four obligations are not values at all and can never be decided by architecture without
   turning it into implementation.** The adapter implementation (DR-120 OD-P1), the CI encodings
   (DR-121, classified by D-310), the seven lifecycle mechanisms (DR-107, classified by D-311) and
   the exact SDK API surface (DR-125, D-110) are all "reserved for the blueprint", and the blueprint
   is forbidden until the rows are SATISFIED. That is the one genuine circle in the register, and it
   is the reason the ceiling exists. It is fixed by one reviewed, scoped D-056 successor of the D-133
   form (§2 C1), not by choosing cargo or GitHub Actions in a design document.

5. **Three sub-obligations are already outside the preview by adopted bytes, and recording that
   is not scope reduction.** AL-3 core-release-byte rollback (DR-127) rides DR-110, which D-002
   deferred; the inherit-blocked evidence class (DR-124) is outside D-002's "touched classes";
   `FC-OUTFAIL.committed-run-preserved` (DR-122) needs a RunId recipe that D-077 keeps conceptual
   in preview. Making those rides legible on the sub-obligation is the deferral-limb work condition
   2 already allows for rows; today the record has no sub-row deferral limb (C-plan Q7). Same
   successor, second limb (§2 C1).

6. **Two working files are now wrong and should be retired, not consulted.** `BLOCKED-FOR-OWNER.md`
   says `preview-product-boundary-successor.v15` "discharges the successor D-364 clause 9 holds
   owed"; on disk that candidate is dual **REJECT** (Claude four MUST-FIX and four SHOULD-FIX, Codex
   four MUST-FIX, grade NOT SUSTAINED) with no COORD heading. It also lists seven owner asks that
   D-367 has now delegated. `DECISIONS-NEEDED.md` §G is likewise superseded. Neither is the record;
   both mislead a fresh reader.

## 1. The 17 rows — what design is actually missing

Legend for the "kind" column: **VALUE** a number/table/window/cap/threshold/ceremony that the
record says is undecided; **RECORD** a recording act the record says is owed (joint-owner, owner
concurrence); **ENCODING** an implementation encoding reserved past condition 5 (the circle);
**RIDE** a sub-obligation that is out of preview by an already-adopted disposition; **AUTHOR**
fixture/schema/corpus bytes that can be written today; **PROCESS** a D-000 act with no design
content. Every obligation id is the current leftover-join's, read from bytes at HEAD.

| Row | Lead label | Accepted contract (recording) | Current join (recording) | Obligations `leftoverDesign: true` | Kind | What must actually be decided or written |
|---|---|---|---|---|---|---|
| DR-101 | OPEN | `distribution-core-inventory-contract.v16` (D-114; dual ACCEPT 0/0) | `distribution-core-leftover-join.v10` (D-308) | OBL-D1, OBL-D2, OBL-2 | VALUE ×3 | OD-101-1 core implementation language with its candidate set (Route C per D-314 Q12); OD-101-2 code-signing ceremony and OS notarization (custody, thresholds, rotation, expiry, revocation), owned separately from DR-112; the G02 installed-tree accounting rule (what counts toward 80 MB) from the two authorities D-314 Q15 names. |
| DR-103 | OPEN | `component-manifest-schemas.v11` (D-104; dual ACCEPT-WITH-ADVISORIES 0/0); D-013 contract v2; fixture corpus v6 (D-106) | `component-manifest-leftover-join.v15` (D-312) | OBL-OD-1, OBL-WINDOWS-PATH, OBL-ENVELOPE-MISMATCH, OBL-UNICODE-NORM | VALUE, AUTHOR ×2, AUTHOR+schema | OD-1: manifest byte cap, tree-entry cap, path-length cap, alias cap plus the measurement method (D-006 pattern, owner DR-115's authority per D-312); three Windows-path fixtures (reserved device names, trailing dot, trailing space); the ENVELOPE_MISMATCH fixture; a schemas successor deciding the Unicode-normalization duplicate rule (NFC/NFD, case-fold on case-insensitive filesystems) so RJ-3 can score. |
| DR-105 (scoped) | OPEN | `permission-truth-tables.v9` (D-128; Claude ACCEPT-WITH-ADVISORIES, Codex ACCEPT) + `host-effect-authorization.v25` (D-126; dual ACCEPT 0/0) | `permission-leftover-join.v12` (D-283) | OBL-FC-C1, OBL-BLK-1..4, OBL-FX-AUTHORING, OBL-R10-AUTHORING, OBL-R6-AUTHORING | RECORD, RIDE ×2, VALUE ×2, AUTHOR ×3 | FC-C1 joint-owner recording (Operability + security with Security + platform). BLK-1 (CA-2 execute-anything) and BLK-2 (four tokenless CA-3 effects) are outside D-002's DR-105 scope "local read/write + consented doctor probes" and should ride that scope (RIDE). BLK-3 (host outcome vocabulary vs `doctor-contract.v4` `effectOutcome`) and BLK-4 (grant journal vs read-only doctor) are inside scope and must be decided. Fourteen FX decision-record fixtures, plus the R-10 expiry-materialization and R-6 process-death byte sets. |
| DR-107 | PROPOSED-CLOSED-FOR-REVIEW | `lifecycle-generation-contract.v2` (dual ACCEPT 0/0; seven mechanisms classified implementation encodings at D-311) | `lifecycle-leftover-join.v4` (D-275) | OBL-ENCODING-RESERVED, OBL-G18-FX-AUTHORING | ENCODING, AUTHOR (blocked) | Nothing decidable at architecture level remains except the encoding circle: journal format, lock grammar beyond DR-103 `lockSchema`, lease API, solver, layout, atomic-rename equivalent, quarantine format. G18 fixtures wait on the quarantine format. Remedy §2 C1. |
| DR-111 | OPEN | `compatibility-matrices-contract.v5` (D-103; dual ACCEPT 0/0) | `compatibility-leftover-join.v3` (D-303) | OBL-NUMERIC-WINDOWS, OBL-LOCK-JOIN | VALUE, dependent | The window **unit** and one coherent evaluable set for core/index/control, each provider major, component API and state schema (evidence formats are out of preview). OBL-LOCK-JOIN follows automatically and is consumed on DR-103. |
| DR-112 | OPEN | `signed-index-trust-contract.v14` (D-309; dual ACCEPT 0/0; OD-112-3 DECIDED fail-closed) | `signed-index-leftover-join.v8` (D-309) | OBL-RESERVED-NUMBERS, OBL-G08-FX-AUTHORING | VALUE ×3, AUTHOR | OD-112-1 quorum/threshold cardinality; OD-112-2 clock-skew tolerance and last-known-revocation freshness; OD-112-4 waiver maximum expiry. Four G08 recovery fixture classes (formerly owner-reserved under D-293 D1; delegated by D-367). |
| DR-114 | OPEN | `doctor-contract.v4` (D-035; single review ACCEPT-WITH-ADVISORIES) + `doctor-actor-join-integration-contract.v8` (D-129; dual ACCEPT 0/0) | `doctor-actor-leftover-join.v12` (D-285); `doctor-leftover-join.v1` is historical since D-164 | OBL-FC-C1, OBL-BLK-1..4, OBL-DOCTOR-FX-AUTHORING, OBL-JOIN-FX-AUTHORING | same as DR-105 + AUTHOR ×2 | The same FC-C1 / BLK-3 / BLK-4 decisions (one act, both joins); twelve doctor FC fixture implementations over the twelve accepted input corpora; thirteen actor-join fixture implementations over `doctor-fc-join-input-corpus.v2`. |
| DR-118 | DECIDED-V1-NOT-INTEGRATED | `language-quality-matrix-contract.v13` (D-113; dual ACCEPT 0/0) | `language-quality-leftover-join.v5` (D-273) | OBL-THRESHOLDS, OBL-MATRIX-CORPUS, OBL-G13-RESERVED | VALUE, AUTHOR, PROCESS | Per-row thresholds; the matrix and digest-pinned corpus (D-007 places their authoring "during qualification", which is the C2 circle); G13 must be named into condition 4's required set by a scoped D-002 successor plus a D-086 successor. Matrix authoring also waits on DR-125 (`OBL-DR125-ACTIVATION`). |
| DR-120 | OPEN | `component-packaging-contract.v14` (dual ACCEPT 0/0 / ACCEPT-WITH-ADVISORIES) | `packaging-leftover-join.v4` (D-266) | OBL-ADAPTER-IMPL, OBL-AT-FX-AUTHORING | ENCODING, AUTHOR (blocked) | OD-P1 "concrete packager, build tool, language toolchain, command line" is reserved with "owner after condition 5". 324 AT fixture cells wait on it. Remedy §2 C1; separately decide (D-314 G3-G15) that adapter-independent archive-identity fixture bytes may be authored now. |
| DR-121 | OPEN | `monorepo-ci-contract.v16` (dual ACCEPT 0/0; six members classified at D-310) | `monorepo-leftover-join.v4` (D-277) | OBL-CI-ENCODING-RESERVED, OBL-G16-FX-AUTHORING | ENCODING, AUTHOR (blocked) | CI provider/YAML/path filters/caches/commands/tooling: remedy §2 C1. G16 fixtures wait on an enumerated component axis: the preview has a finite set (distribution core, semantic host, one TypeScript closure, one pack) and the ownership record is the authority; enumerate it. |
| DR-122 | PROPOSED-CLOSED-FOR-REVIEW | `sarif-projection-contract.v15` (dual ACCEPT 0/0) | `sarif-leftover-join.v14` (D-347) | OBL-FC-OUTFAIL-FX | RIDE | One case, `FC-OUTFAIL.committed-run-preserved`, parked on the §7.1 RunId recipe that D-077 keeps conceptual in preview. Record the ride; nothing else is open on the row. |
| DR-124 | OPEN | `state-class-contract.v11` (dual ACCEPT 0/0) | `state-class-leftover-join.v5` (D-333) | OBL-GRANT-JOURNAL, OBL-MONOTONIC, OBL-INHERIT-BLOCKED | RECORD/VALUE, VALUE, RIDE | Owner concurrence on SUP-124-GRANT-JOURNAL (which class holds the grant journal, append-only and fsync order; ties to BLK-4); the monotonic trust-store class (where last-known-revocation and signed-index freshness live; ties to DR-112 OD-112-2); SC-EVIDENCE rides D-002's "touched classes" scope. |
| DR-125 | OPEN | `component-sdk-contract.v4` (dual ACCEPT 0/0; envelope families specified, API surface reserved) | `sdk-leftover-join.v9` (D-329) | OBL-SDK-API-RESERVED | ENCODING | "Exact SDK APIs and frameworks" reserved (D-110). Remedy §2 C1. Note DR-118's matrix authoring is gated on this row's closure, so it sits on the critical path. |
| DR-126 | OPEN | `platform-tcb-contract.v48` (D-361; dual ACCEPT 0/0, application-grade, selector grammar governing) | `platform-tcb-leftover-join.v11` (D-362) | OBL-RESERVED-TABLES, OBL-G22-FX-AUTHORING | VALUE (tables), AUTHOR (blocked) | Complete per-OS profiles against the v48 grammar for macOS arm64/x86_64 and Linux x86_64/arm64: the four filesystem selectors, the four version/build selectors, loader/libc/framework/cert/font/ICU allowlists, identity rules. The population packet owner is Security + release + platform (D-341). One G22 fixture class waits on the tables. |
| DR-127 | OPEN | `anti-lockstep-contract.v7` (dual ACCEPT 0/0) | `anti-lockstep-leftover-join.v6` (D-326) | OBL-HOSTILE-GOLDENS, OBL-AL1-AL2-AL5, OBL-AL3-CORE-ROLLBACK | VALUE, VALUE/route, RIDE | Per-class totals for the seven within-class universal sets (or a reviewed ruling that the D-300 witness floor discharges); the execution route for AL-1/AL-2/AL-5 cases G16 does not cover; AL-3 rides D-002's DR-110 deferral. |
| DR-131 | OPEN | `preview-analyze-contract.v2` (D-138 candidate; dual ACCEPT 0/0) | gate joins G24–G28 (D-249..D-253): NT-1,2,3,5,6,7,8 leftover | PROCESS, AUTHOR ×5 | The D-314 item 2 sequence: shared gate-2 entry with a distinct DR-131 finding, fresh application-grade dual review of the exact final bytes, Class A opening; then G24–G28 fixture authoring (2+3+3+4+4 payloads); then SATISFIED-GRADE + MF-6. No design content is missing from the contract itself. |
| DR-133 | OPEN | `provider-only-output-contract.v3` (D-136 candidate; dual ACCEPT 0/0) | `provider-only-nt-gate-join.v6`; G20 join now `leftoverDesign: []`, G21 join carries OBL-G21-FX-AUTHORING | PROCESS, AUTHOR, disposition | The D-314 item 3 sequence; a separate reviewed disposition of the candidate's proposed file-01 preview-role delta (or removal of reliance); NT-6 authoring at G21 after the opening; NT-4/NT-7 standing at G20 appears byte-resolved by D-330 and should be confirmed in the gate-2 entry. |

### 1.A Rows that are one process act from Class A eligibility

DR-131, DR-133. DR-101, DR-111, DR-112, DR-126, DR-127 become eligible the moment their values are
recorded in a successor and the join is remeasured. DR-103, DR-105, DR-114 become eligible when
values plus fixture bytes exist. DR-118 becomes Class B eligible once thresholds are decided, the
matrix/corpus is authored, and G13 is named. DR-107, DR-120, DR-121, DR-125 cannot become eligible
under D-056 as read today, whatever we author (§2 C1). DR-122 and DR-124 need only the ride limb
plus, for DR-124, two decisions.

### 1.B The consolidated decision list (formerly owner-reserved; now ours under D-367)

Values, each needing a D-006-form entry (evidence, falsifiability clause, overturn cheaper than the
decision), batched per row where the D-006 precedent allows:

1. DR-101 OD-101-1 core language and candidate set.
2. DR-101 OD-101-2 signing ceremony and notarization.
3. DR-101 / DR-G02 installed-tree accounting rule.
4. DR-103 OD-1 four caps and measurement method.
5. DR-103 Unicode-normalization duplicate rule (schema successor).
6. DR-105/DR-114 FC-C1 recording; BLK-3 outcome-vocabulary mapping; BLK-4 grant-journal placement.
7. DR-111 window unit and values (four surfaces).
8. DR-112 OD-112-1, OD-112-2, OD-112-4.
9. DR-118 per-row threshold rule (parity with the pinned prototype baseline is already the D-007
   item 7 rule; what is undecided is the tolerance and the corpus digest set).
10. DR-124 grant-journal class; monotonic trust-store class.
11. DR-126 complete per-OS profiles (measured, see §4).
12. DR-127 per-class totals; AL-1/2/5 route.
13. OQ-G21-4 (quoted-type envelope vs per-type schema) — unblocks five G21 injections.
14. DR-G07 filesystem coverage list; DR-G16 component axis.
15. D-314 G3-G15: whether adapter-independent fixture bytes may be authored before an adapter exists.

Sub-obligation rides (need the §2 C1 successor first): DR-127 AL-3; DR-124 SC-EVIDENCE; DR-122
committed-run case; DR-105/DR-114 BLK-1, BLK-2 (keychain part already routed to DR-108).

Encoding remainders (need the §2 C1 successor first): DR-107 seven mechanisms; DR-120 adapter;
DR-121 six encodings; DR-125 API surface.

## 2. Circular obligations, and the remedy that preserves acceptance

**C1 — "reserved for the blueprint" versus "no blueprint until SATISFIED".** D-056 gate 2 (pinned
turn-2 subject) excludes "still-UNDECIDED numbers" and "missing design" from the remainder; D-310 and
D-311 classified the DR-121 and DR-107 reservations as implementation encodings but expressly gave
that "no Condition-2 or D-056 eligibility effect without a separate reviewed scope/eligibility
successor"; D-315 Q7 ruled the label alone cannot satisfy gate 2. Nobody has authored that successor.
DR-120's OD-P1 says its owner is "after condition 5". Condition 5 requires condition 2. Four rows are
therefore unsatisfiable by any amount of authoring.

*Remedy (one reviewed, scoped D-056 successor of the D-133 form — property, not names):*

- **Limb E, implementation-encoding remainder.** An obligation is a gate-2 remainder, not design,
  when all four hold from bytes: (i) a reviewed COORD act has classified it an implementation
  encoding (D-310, D-311 exist; DR-120 and DR-125 need equivalents); (ii) the row's accepted
  contract states, as testable classes, the properties every concrete encoding must satisfy
  (DR-107 P-1..P-8 and `mechanismReservation.failureRule`; DR-120 the AT-* classes; DR-121 the
  ownership record as sole impact authority and the G16-* classes; DR-125 the standardized envelope
  families and forbidden component acts); (iii) a named condition-4 gate with an owner executes
  those classes against whatever encoding the blueprint chooses (G18, G15, G16, G20); (iv) the
  contract's failure rule says an encoding that cannot prove the classes fails the row. The
  remainder is then "execution of the property classes against a later-chosen encoding", which is
  execution.
- **Limb D, sub-obligation deferral ride.** An obligation is on the deferral limb, not a
  SATISFIED-bar, when it is outside the preview by the terms of an already-adopted row-level
  disposition (a D-002 deferral or scope, a D-077/D-078 Route B disposition), the join names the
  ride and its re-entry trigger, and no scope is newly removed.
- **Exclusions that stay design:** undecided numbers, tables, windows, caps, thresholds; owed
  recordings (FC-C1, grant journal); fixture bytes determinable today; schema successors.
- **Why acceptance is preserved:** gates 3, 4 and 5 are untouched; each dedicated SATISFIED-GRADE
  review must verify (i)–(iv) from bytes; a bad encoding still fails the row at its gate at
  qualification rather than being waved through; the D-018 "not MVP, no authoritative gate" naming
  is unaffected; overturn restores the current reading (D-133 precedent).
- **Rejected alternative:** choosing the encodings in architecture (cargo, GitHub Actions, sqlite
  leases). That converts architecture into the blueprint condition 5 forbids and would be re-decided
  by the blueprint anyway. Numbers are different: D-006 shows pre-blueprint numeric decisions are
  lawful and reversible, so numbers stay on the VALUE path.

**C2 — DR-118 thresholds and matrix.** D-007 says the matrix and corpus are "acceptance evidence
authored during qualification" and thresholds are "product approval at matrix acceptance"; D-056
clause 5 and gate 2 say authoring and undecided numbers are design. Read together the row cannot be
SATISFIED before qualification, which condition 5 forbids. Remedy: author the matrix structure and
corpus now against the pinned prototype `opensip-cli` @ `a62509d6…` (D-007 item 5 makes it the only
admissible baseline; measuring it is lawful design work), decide the threshold rule as
parity-or-improvement against that baseline with a stated tolerance in the D-006 regress-only form,
record it as the Class B decision, and name G13 into required-now by a scoped D-002 successor with a
D-086 successor in the same act. Matrix rows that ride DR-006 recipes stay conceptual per D-002's
symmetry clause and D-077. DR-125 must reach eligibility first (`OBL-DR125-ACTIVATION`).

**C3 — DR-127 AL-3 rides a deferred row.** `OBL-AL3-CORE-ROLLBACK` waits for "a reviewed DR-110
owning contract"; DR-110 is on D-002's deferral limb (install is a fresh signed download). A
SATISFIED-requiring row cannot wait on a deferred one. Remedy: Limb D ride with trigger "when DR-110
enters a slice" — this is D-002's own scope, not new scope.

**C4 — DR-122's last case rides condition 1.** `FC-OUTFAIL.committed-run-preserved` needs a bound
RunId recipe; D-077 keeps §7.1 recipes conceptual in preview; D-314 item 25 keeps it parked.
Remedy: Limb D ride on D-077, trigger "binding RunId recipe accepted". The row then has an empty
leftover partition and is one SATISFIED-GRADE cycle from `SATISFIED`.

**C5 — D-000 review form under a two-agent topology.** D-000 clause 1 requires adversarial review
of every decision that would have needed the user; clause 2 batches a three-turn deadlock to the
user; D-367 says the user should see almost nothing, and the lead authors most entries. Remedy, as a
reviewed D-000 amendment recorded before any SATISFIED re-record: (a) the author never reviews;
(b) the second independent review comes from a **fresh instance** of the author's own model in a new
Herdr pane with no session context, so "dual ACCEPT/CONSENT 0/0" keeps its meaning; (c) after three
turns the frozen subject and both positions go to a fresh third instance for a binding adjudication
limited to the surviving MUST-FIX; only a still-contested result is batched to the user; (d) one
entry may decide several values for one row (the D-006 precedent decided six numbers and a
regression rule in one act), so the count in §3 is tractable. (The lead's D-368 proposal — "author
assent plus one genuinely independent peer review, per-row verdicts preserved in integrated
batches" — is the same problem; my verdict on it follows separately.)

**C6 — condition 4 moves when DR-118 does.** DR-118's Class B remainder must be "named at a
condition-4 obligation with an owner" (gate 3). G13 is reserved, not named, and outside required-now
(28). Naming it changes D-002's condition-4 required-gate set, which is a scoped D-002 successor plus
a D-086 successor. Condition 4's "28 of 28" becomes "29 of 29" and must be re-measured in the same
MF-6. Not a circle, but a dependency the finish line must include.

**Not a circle, recorded so nobody re-litigates it:** D-002's "SARIF advertised for analyze" versus
D-077's drop is reconciled inside `preview-analyze-contract.v2` (`d002SarifReconciliation`) and G17 is
inapplicable; the D-364 reading lets a citation-refresh successor (the rejected v15 lineage) stay
outstanding without blocking DR-117.

## 3. Recommended finish line and dependency sequence

**Finish line (proposed, to be recorded as the D-139 successor the WORKLOG's step 3 needs):**

1. File 08 conditions 1–4 MET by lead labels: condition 2 at **23 of 23** SATISFIED-requiring rows
   `SATISFIED`, the nine deferral-limb rows unchanged; condition 4 re-measured after G13 naming.
2. Every `SATISFIED` row's remainder is named at a condition-4 gate that has, at the recording
   commit, (a) a harness-specification occupancy, (b) either an authored fixture corpus or a Limb E
   encoding remainder, and (c) a retained checker that validates the corpus (today **zero** of the
   144 `check-*` scripts targets a V2 corpus).
3. A dated measurement act at a known commit regenerating the condition-2 snapshot from bytes.
4. A blind implementer litmus (§5) passed by two fresh instances with zero invented values.
5. The seal entry (D-293 F1 form), then the docs rewrite. Condition 5 stays a separate act and is
   one of the "1%" the user should see, because it is the implementation authorization D-367
   withholds.

**Sequence (waves; items inside a wave are independent and can be split author/reviewer between
us):**

| Wave | Acts | Unblocks |
|---|---|---|
| 0 — process | D-000 amendment (C5); the D-056 successor with Limbs E and D (C1); retire `BLOCKED-FOR-OWNER.md`, `DECISIONS-NEEDED.md` §G and the stale `HANDOFF` as superseded working files (no record effect) | everything below |
| 1 — values | §1.B items 1–15, batched per row: DR-101 (three values, one entry); DR-103 (caps + Unicode rule); DR-105/114 (FC-C1, BLK-3, BLK-4, one joint entry); DR-111; DR-112; DR-118 threshold rule; DR-124 (two classes); DR-126 profiles (measured first, §4); DR-127; OQ-G21-4; G07 list; G16 axis; G3-G15 ruling | every VALUE-kind obligation |
| 2 — successors and authoring | contract successors carrying wave-1 values with join remasurements (DR-101, 103, 111, 112, 124, 126, 127 and the DR-105/114 pair); Limb D rides on DR-122/124/127/105/114 joins; Limb E classifications for DR-120 and DR-125; fixtures now unblocked (DR-103 ×3 + ENVELOPE, DR-105 FX/R10/R6, DR-114 FC ×12 and join ×13, G08 ×4, G22, G21 ×5, G16 with the axis, G15 archive-identity subset) each with a checker | Class A eligibility for 13 rows; Class B for DR-118 after matrix |
| 3 — DR-131/DR-133 programme | shared gate-2 entry (distinct findings for both rows), fresh application-grade reviews of the exact final bytes (Codex-fresh reviews the Claude-authored contract and vice versa), the two Class A openings, the file-01 delta disposition, G24–G28 corpora, NT-6 | the two file-12 rows |
| 4 — DR-118 | matrix + corpus authored against the prototype pin; scoped D-002 successor naming G13 + D-086 successor; Class B decision | the last DECIDED-V1-NOT-INTEGRATED row |
| 5 — re-records | 17 dedicated SATISFIED-GRADE cycles + MF-6, batched by owner where the reviewers accept batching; condition-2 and condition-4 snapshot re-measure in each MF-6 | condition 2 MET |
| 6 — close | measurement act; implementer litmus ×2; seal; F1; condition 5 as a separate reported act | done |

Critical path: Wave 0 → DR-125 Limb E → DR-118 matrix → G13 naming → DR-118 re-record. Everything
else is parallel to it. Rough size: roughly 70 reviewed acts at one act per value, roughly 40 with
per-row batching; each act has cost one to three review turns in this record, so batching is not
optional if "do not stop" is to mean days rather than weeks.

## 4. Remaining useful technical work (evidence-producing, not paperwork)

1. **DR-126 profile population by measurement.** Run loader traces of a minimal native binary on
   each of the four platforms (this Mac for arm64 and x86_64 via a native Intel runner or a clean VM,
   Linux x86_64/arm64 containers with glibc and musl): `otool -L`, `dyld` shared-cache membership,
   `ldd`/`LD_DEBUG=libs`, `/etc/ssl` and Security.framework cert-store paths, ICU and font presence.
   The tables then cite measurements, not guesses, and the glibc-floor versus static-musl question
   for Linux is answered from bytes. This is the single largest block of genuinely technical design
   left.
2. **DR-101 language decision spike.** A scratch (not `docs/`) measurement of a hello-world static
   binary per candidate against D-006's 25 MB / 80 MB / 100 ms / 40 MB bars on the four platforms
   turns OD-101-1 from taste into evidence. The lead's draft already proposes Rust 2024; the spike
   should be the entry's falsifiability evidence, not a debate.
3. **DR-118 baseline measurement of the prototype.** D-007 items 1, 3 and 5 require prototype
   behavior and performance baselines at `a62509d6…` per capability row. Nobody has measured them.
   This is real analysis-quality work and it produces the matrix.
4. **DR-112 + DR-124 security state machine.** OD-112-1/2/4 plus the monotonic trust-store class
   and the grant journal are one coherent design (freshness, revocation, quorum, waiver expiry, and
   where each byte lives with what write ordering). I am drafting it as `security-completion.v1.md`
   at the lead's request, with primary-source checks on signing and notarization.
5. **Fixture generators with checkers.** Every corpus recorded in the last three weeks was produced
   by a generator under `tools/orchestrator/` and has no retained validator. A `check-<corpus>.py`
   per corpus family (digest set, per-platform copy identity, envelope conformance to the governing
   contract's declared shapes) is cheap and is the only thing that makes "authored" mean more than
   "typed".
6. **DR-103 Unicode rule and DR-111 windows** are small, real design tasks: one schema successor and
   one N/N+1 skew table per surface with the unit stated.
7. **A machine-readable readiness measurement.** A script that regenerates the condition-1/2/4
   snapshot from file 08 lead labels and the D-134 set, run in every MF-6, removes the class of
   arithmetic errors D-363/D-365 spent turns on.

## 5. Preventing a paper-only completion

1. **No SATISFIED re-record without an executable check.** Add to the gate-3 evidence the retained
   checker of (2) above, run green at the recording commit and pinned by digest, for every fixture
   corpus the remainder names. Where the remainder is a Limb E encoding, the checker validates the
   property classes' fixture shapes instead.
2. **Blind implementer litmus before the seal.** Two fresh instances, no session context, given
   only the final contracts, file 08 and file 02–04, each produce a build plan for the D-002 preview
   and list every value they had to invent. Any invented value re-opens the owning row. The record
   already has the shape (`implementer-litmus.v4`, `consumer-b-implementer-litmus.v3`, DR-011-R10).
3. **Prototype cross-check.** Every contract claim about the prototype is re-verified against the
   `opensip-cli` pin at re-record time (DR-203 discipline), so the design stays anchored to running
   code that exists.
4. **Falsifiability clause on every decided value** (D-006 form): the harness that measures it and
   the successor path if it proves infeasible. A value with no harness is not a decision.
5. **Condition 5's entry defines the first executable milestone**: the `--help`/`--version`
   skeleton in the chosen language with the G01–G05 harnesses run on the four platforms, and the
   G23/G21 admission corpora executed against the host's admission code. If the blueprint cannot
   start there, the architecture was paper.
6. **Honest naming survives the seal.** The seal entry states what is not proven: no execution, no
   qualification, no authoritative Run, no upgrade continuity (D-018), G17 dropped, identities
   conceptual (D-077/D-078).
7. **One truth.** Retire the superseded working files; keep COORD + file 08 + `docs/coop/artifacts/`
   as the only record, as D-293 already states.

## 6. Record-hygiene findings (verify before citing)

- `preview-product-boundary-successor.v15` is dual REJECT and unrecorded; the D-364 clause 9
  successor on the g29/g30 grounds is still owed; off the critical path.
- `doctor-leftover-join.v1` is historical (D-164 moved DR-114 to the doctor-actor lineage); the
  current DR-114 join is `doctor-actor-leftover-join.v12`.
- `gate-harness-naming.v8`, `core-gate-harness-specifications.v4` and `versioning-policy.v17` have
  zero COORD mentions under those names; check their recording headings before relying on them.
- `g21-fixture-corpus.v34`/`.v35` are on disk (generators exist under `tools/orchestrator/`) with no
  recording heading found for either; the last recorded G21 corpus is `.v33` (D-358) and the current
  join is `leftover-join.v45` (D-359).
- `doctor-contract.v4` carries a single pre-dual-era review; D-056 Class A needs "an independently
  accepted design contract at 0 blockers", which it has, but the dedicated SATISFIED-GRADE review
  should say so explicitly rather than recite "dual ACCEPT".
- File 12 §7 step 4's D-036 successor exists as D-139 (H/L/W lanes); the finish-line entry proposed
  in §3 should succeed D-139 rather than sit beside it.
