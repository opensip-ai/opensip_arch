# Independent bounded review — published-migrated carrier population 155 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: `migrated155-20260919-REQUEST.md` (+ subject README and PLAN, read in full). Scope: the delta of frozen
`migrated-carrier-checkpoint-155` over frozen 154 — new `inherited_schema.rs`; `CurrentCarrierSnapshot::open`
recognising a **published** migrated carrier; `generation_population` over inherited + current + marker generations;
the anchor adapter's below-boundary route. **Not** unmigrated / {A} / {A,B} dispatch, INIT, migration writes, custody,
ledger join, leases, fences, writers or selection, and I infer none. No frozen/selected/product edit; scratch only,
`-I -B`, dedicated targets; no commit, push or delegation; no cumulative approval.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 4,234,592 bytes, SHA-256 `b32cc402ff7c205fb3e8f0fe9fbe5a7d1f4058971394be63af165d5c2c483e4e` = request = `archive-pin.json` |
| Members | 462/462 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified at the end |
| Product pins | 341/341; none unpinned |
| Parent | `parent-inputs.json` = **my own** verified 154 extraction (340/340); 337 unchanged; 3 changed (`journal_store.rs`, `generation_population.rs`, `generation_anchor.rs`); 1 added |
| Embedded pins | `parent154`, `reference153` equal the real archives; both DDL provenance sources equal my reference extraction |
| **Imported DDL identity** | the two **production** constants in `inherited_schema.rs` are byte-identical to the frozen sources (DDL2 = whole file `security-schemas.v2/grant-journal.sql`; DDL1 = the fenced block in `security-completion.v1.md`); `CURRENT_CARRIER_DDL` is byte-identical to the frozen `grant-journal.carrier.v3.sql` |
| Host pins | host98 receipt: 221 sources all equal the product pins; all commands exit 0 |
| Owner checks, fresh scratch | 109/109 security tests; strict workspace Clippy clean |

## 2. Assumptions against the selected law (read, not inferred)
- **Boundary.** `carrier-format.v3.md` §7 act 3 publishes `first_generation = max inherited + 1`; §8 rule 3 (F51) says
  only `max < first`. 155 requires the *equality*. That is the stricter reading and I agree with it: nothing lawful
  appends to the inherited table after act 1, so any other value is either F51 or a publication that never happened
  this way. An empty inherited table cannot be a migrated carrier (act 1 appends a TERMINAL; the CHECK forces
  `first ≥ 2`) — refused.
- **Closure.** §7 act 1 appends `TERMINAL/grantGenerationClosure`; the contract adds that a marker cannot substitute
  for act A/C. 155 requires the last inherited generation to be historical *and* end in exactly that cause.
- **Origin 1** for inherited history comes from v1 §5.4, not from `first_generation`; a carrier whose history starts at
  2 is refused.
- **F46.** §9 says the below-`first_generation` verdict "is decided from the object names alone and needs no witness
  comparison, so the witness and anchor rows … are not reported for that request. It is not a quarantine". 155 returns
  `unknown-carrier-incompatible` before looking at the files — that is the law, not a shortcut (§3.3).
- **Footprint.** The format law is a footprint of *named* objects with exact DDL. It does not forbid foreign objects
  (N-2).

## 3. Evidence
**3.1 Carriers built by an independent writer** (`probes/gen_migrated.py`, `rust_probe.rs.txt`, `compare.py`): Python
`sqlite3` executes the frozen inherited DDL, writes legacy history with the pinned v8 canonicalizer, then performs acts
B and C exactly as §7 describes (executes the frozen v3 SQL file, inserts the `carrier_format` row), optionally followed
by schema-3 SEAL rows. 166 scenarios, both formats × three encodings. **152 expectations: 0 mismatches; 14 recorded as
observations** (below). Covered: publication before the first current row; two inherited generations then current
rows; exact and one-under limits for generations, records and bytes; last inherited open / purged / open-but-marked
(→ `MigrationClosure`); purged+marked middle generation and marker-only middle generation (admitted, ends preserved);
broken marker; UTF-16 carrier with a marker (→ `MarkerUnavailable`, as the README says); first inherited open or purged
without marker (→ `PredecessorOpen`); gap; origin 2; `first = max + 2`; `first = max` (F51); `migrated_from` naming the
other format; empty inherited table; wrong project key; inherited chain disagreement (**admitted, `Unverifiable`**) vs
inherited body digest wrong (**refused**); extra trigger / dropped trigger / extra index on the inherited table
(refused); acts A+B only (→ `Unpublished`); a *fresh* format row beside an inherited table (refused). Totals are exact:
records, logical bytes (journal + markers) and additionally owned stored octets equal my arithmetic in every admitted
case, including 2× stored octets under UTF-16.

**3.2 Observations (no expectation asserted).**
- *Last inherited generation closed **and** marked* → **admitted** (both formats). See N-1.
- *Auxiliary tables dropped before act B, so v3's `IF NOT EXISTS` created them*: under DDL1 → `Definition` (its
  commented spelling differs from v3's — exactly the PLAN's point); under DDL2 → admitted, because DDL2's auxiliary
  text is byte-equal to v3's and the two histories are indistinguishable. Correct.
- *A foreign VIEW added after publication* → admitted (N-2; my first expectation was wrong).

**3.3 Physical anchor boundary** (`io/anchor.txt`, real files through `generation_anchor::read`): current generation 3
with its SEAL → `Consistent`; a query naming historical generation 1 by its **true** digest and operation → `Unknown
unknown-carrier-incompatible`, one capture — also with a malformed witness and with an unreadable witness, while the
same files give the *current* query `QuarantineCondition witnessMalformed` and `UnavailableBusy` (two captures). History
never satisfies a SEAL join and never produces a quarantine condition.

**3.4 Mutants** (`mutation.py`, 15, all compiled, baseline green; narrower than the owner's nine): 8 killed by the
owner's tests. 7 survive them: **3 detected by my carriers (T-1)**; 4 equivalent or unobservable (disclosed).

## 4. Findings
- **T-1 (low) — three regressions pass all 109 tests; my carriers catch each.**
  | Surviving mutant | Isolating carrier |
  |---|---|
  | an **empty** inherited table is accepted as a migrated carrier | `*-inherited-table-empty` (6) |
  | stored-octet budget not carried across generations (each inherited generation gets the full `max_body_bytes`) | UTF-16, `max_body_bytes` = logical total (4) |
  | inherited logical bytes not counted at all | every admitted migrated carrier (45: `body_bytes` differs) |
- **N-1 (note, law that population cannot enforce)** The contract says a carrier whose highest inherited generation
  has a quarantine marker "is NOT migratable … Act C refuses … even if a synthetic inherited TERMINAL … [is] presented
  alongside that marker". 155 admits a last inherited generation that is closed *and* marked. I think that is right
  *for a reader*: the same state arises lawfully after publication (witnessless restore before the first v3 row marks
  the highest generation, which is then the inherited one — contract "empty and migrated dispatch"). The two histories
  are indistinguishable in SQL, so the rule stays with whoever performs or verifies act C; it should be named in the
  README's open list so nobody reads population admission as evidence that act C was lawful.
- **N-2 (note)** `carrier_definitions` and `inherited_schema::definitions` compare objects whose `tbl_name` is one of
  the five known tables. Foreign tables/views are outside the footprint and are tolerated — consistent with the format
  law, unchanged since 96, and harmless to this reader (`query_only`, `trusted_schema=OFF`, defensive, fixed statement
  text). Worth one sentence, because "exact definitions" reads broader than it is.
- **N-3 (note, inherited from 154 F-1)** The strict NULL-iff-absent mirror rule now refuses the **whole carrier**
  (`Historical(RowBinding)`), e.g. a DDL1 GRANT row with a NULL `token`, which DDL1 itself permits. The decision asked
  for in my 154 review matters more here.
- **N-4 (note)** Under UTF-16 the retained stored octets are about twice the logical bytes and are bounded by the same
  `max_body_bytes`; a caller sizing the budget from logical totals gets `Bound`. Stated in the README; confirmed.
- **N-5 (note)** A missing origin is reported as `Gap { expected: 1, observed: 2 }` — same refusal, and arguably the
  clearer name; mentioned only because the request speaks of "origin" as its own check.
- **Disclosed, mutants that prove nothing:** "format binding only when `migrated_from` is present" is caught one layer
  later by the population guard `(1,false)|(2..,true)` with the same error (defence in depth — but `open` alone would
  accept it); "stored aggregate not bounded" is redundant with the per-call historical limit; "incompatible only when
  the generation exists" is equivalent because origin + contiguity make every generation below the boundary exist;
  "stability always true" is unobservable in any standing (first `Unknown` is final) — the README's "preserves observed
  endpoint stability" is true and currently unpinned, while the tail half is pinned by the owner's mutant.

No behavioural defect found.

## 5. Bounded verdict
**155: reviewed, no blocking finding and no behavioural defect. The production inherited DDL constants and the current
DDL are byte-identical to the frozen sources; a published migrated carrier is recognised only with the exact inherited
table and triggers, the matching `migrated_from`, `max inherited + 1 == first_generation`, origin 1, contiguity,
closed-or-marked predecessors and an actual `grantGenerationClosure` on the last inherited generation; inherited chain
disagreement stays diagnostic while inherited body disagreement refuses; all three aggregates are exact on 166
independently built carriers in both formats and three encodings (0 mismatches); below the boundary the anchor answers
`unknown-carrier-incompatible` from one capture without consulting the files, as §9/F46 prescribes, and history never
joins a SEAL. T-1: three narrow regressions (empty inherited table; stored-octet and logical-byte accounting) are
unpinned by the owner's tests. N-1: "marked highest inherited generation is not migratable" cannot be decided by a
reader and remains act C's obligation.** Not approval of unmigrated or partial-prefix dispatch, migration writes, INIT,
custody, ledger join, writers, selection or any cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `product-pins.json`, `diffs/`, `owner/`,
`probes/{gen_migrated.py (r3), rust_probe.rs.txt (r2), compare.py, mutation.py, mutation.json, mutation.log}`,
`io/{scenarios.json, rust.ndjson, compare.txt, compare.json, anchor.txt, compare-r2-before-oracle-label-fix.txt, r1-symlink-path-slip/}`
(`io/dbs/` holds the databases; regenerate with `gen_migrated.py`, which reuses the 154 writer), `hashes.txt`.
Harness slips, preserved: r1 opened carriers through macOS's `/tmp` symlink and every open failed `NOFOLLOW`
(`CannotOpen`) — nothing was tested; r2 had two wrong oracle labels (origin named `Gap`; foreign view).
