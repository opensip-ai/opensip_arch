# C1b implementation plan r5: the VCS observation (M3-C r8 item 4, VCS-1, M3-B successor S4)

**Lead plan, 2026-10-17. Proposed; it needs Codex review.** Round 5 answers Codex `codex-c1b-plan-r4` (REQUIRED-FINDINGS: C1BPLAN-R4-RF-1, with rulings on Q6 and Q7). Round 4 revised the accepted r3 (`codex-c1b-plan-r3`, ACCEPT) after C1b-1's own derivation found that r3's VCS term did not fit r9's caps. r1 to r4 (`PLAN-r1.md` to `PLAN-r4.md`) are history.

**Bases:**
- product main `813d559`: C1c-0 integrated, which joined the C1b census batch, on D3a-2 and the v222 lock, with C1b-0 at `c9c18f7` (contract successor 176, lock `9ea2d4a`);
- architecture `fa875bfd`, and the files the subject manifest names.

## r5 changes

| Finding or ruling | r5 | Where |
| --- | --- | --- |
| **R4-RF-1** (price the VCS record's canonical encoding, including escaped member paths) | **The record allocation is its canonical encoded length, not raw length plus slack.** r4 priced it as `owned(64 × (4,096 + 128))`, 270,336 bytes. r5 derives it from the schema-3 canonical encoding, by C2a r3/r4's method (`c2a/PLAN-r4.md`:113-119: fixed syntax counted from the real encoder, plus e(x) for each string's escaped payload and d(n) for each integer's digits):<br>- **e(x)** counts 2 for `"` and `\`, 2 for each of `\b \f \n \r \t`, 6 for every other control below U+0020, and raw UTF-8 (1 to 4 bytes) otherwise (`canonical.rs`, `Encoder::string`; C1a3's `string_len`, `snapshot_seal.rs`:133-142);<br>- **schema 3** is **167 + Σ(91 + e(Pᵢ)) + (n − 1)** bytes for n members. Keys are in byte order. 167 is the top level's keys, `null`, `false`, `"none"`, the single-digit `schemaVersion` and the 64-hex digest. 91 is a member's keys, its 40-hex `commitId`, `true` and `"git"`. No other integer appears, so d(·) is the constant 1. B-S2's two-member vector (`serde`, `serde-json`; README:42-48) checks it: 167 + (91 + 5) + (91 + 10) + 1 = 365 bytes;<br>- **schema 2 `kind: git`** is a fixed **190** bytes, and `kind: none` is **154** (B-S2's vectors, README:42-48);<br>- **the largest e(P):** a `LogicalPath` has at most 4,096 scalars, each segment at most 255, and no `\` or NUL. So no scalar's payload exceeds 6. With s separators, at most min(4,096 − s, 255(s + 1)) other scalars. The maximum over every s is **24,496**, at s = 16 (4,080 six-byte controls), found exhaustively in `vcs_term_r5.py`;<br>- **the largest record** is 167 + 64 × (91 + 24,496) + 63 = **1,573,798** bytes. With the 128-byte record overhead the charge is 1,573,926 bytes, 1,303,462 more than r4's 270,464.<br>**Verified against the real encoder** by a scratch program run under the lane lock (`r5-evidence/record-size-check/`, `run.log`). It builds records with every escape class, DEL, C1 and non-ASCII paths, and the maximal record: 64 distinct, sorted 4,096-scalar paths of six-byte controls. Each record's `canonical_bytes` length equals the formula's. The identity registry admits the maximal record as a `vcs-observation`, and a 4,097-scalar path is refused as a `LogicalPath`. | LD-C1B-6; `r5-evidence/` |
| (R4-RF-1) ownership | **One owned buffer, and nothing else.** C1b-2 computes the record's exact length D first, charges `owned_record(D)`, and hand-encodes into `Vec::with_capacity(D)`, with keys in byte order and the C1a3 escapes. The member paths are **borrowed** from `AdmittedBoundaries`, and the commit ids from C1b-1's `VcsObservation`, which retains and charges them (LD-C1B-6's retained commit). The digest is raw SHA-256 over the buffer, with its hex in a stack array (`hex_digits`). There is no temporary string or integer. The buffer must equal `canonical_bytes` of the same record, or it refuses `Internal`. The term prices that one buffer at 1,573,798 bytes. | LD-C1B-6; C1b-2 |
| (R4-RF-1) the re-run, on the new base | **D* and H* are unchanged**, re-derived with the corrected charge on product `813d559` (`r5-evidence/vcs_term_r5.output.json`). The cost constants are read from a clean export of `813d559`, after `costs` verifies its re-pinned closure. **The subtotal is now cumulative:** r9's adopted subtotal plus C1c-0's accepted retention term, 64 objects and 1,056,768 bytes (`c1c-0-r2/evidence/c1c0-checks-r2/retention-cap-evidence.json`, whose r9 subtotal the script requires to equal r9's). That is 776,740 objects, 6,218,464 edges and 2,539,929,154 bytes.<br>- **D* = 226 and H* = 1,048,575.** The term is 173,770 objects, 2,165,048 edges and **1,645,202,534** bytes. The total is 950,510 objects, 8,383,512 edges and **4,185,131,688** bytes, and twice the total is 1,901,020, 16,767,024 and **8,370,263,376**, each within its cap;<br>- **one directory more:** twice the edges is 16,783,794, over 2^24;<br>- **one `HEAD` byte more:** twice the bytes is **8,642,893,526**, over 2^33.<br>Edges are the binding term for D*, and the read buffer's doubling past 1 MiB is the binding term for H*. Neither moves with the record's 1.3 MB or C1c-0's 1.06 MB. The caps and the law gate are unaffected. | LD-C1B-6 |
| (R4-RF-1) controls | **Encoded-length and allocation controls**, for C1b-1 and C1b-2:<br>- **C1b-1:** the model's record-length function equals `canonical_bytes` for paths with `"`, every short escape, a six-byte control, DEL, C1 and 2-, 3- and 4-byte UTF-8, and at the maximal record;<br>- **C1b-2:** for each of those records, the charge equals the exact encoded length and the hand encoding equals `canonical_bytes`. A scope one byte short refuses `Budget` before the buffer is allocated. The allocation pin covers the record. | §4 |
| **Q6 ruling** (no law-record revision needed) | **Adopted, with the qualifications the review asks for:**<br>- **D* and H* are evidence-envelope coordinates, not runtime thresholds.** Exceeding either requires no refusal and does not by itself prove exhaustion. "One more fails" shows the loss of this 2× envelope, not that the ledger runs out;<br>- **The 4 MiB read cap does bound `HEAD`'s length** (Q1). r4's claim that no owner bounds it is withdrawn. That refusal bound is distinct from a guaranteed 2× fit: it does not promise that all associated work fits;<br>- **r9's guarantee stays conditional,** with all work that is not a row counted together, VCS included. The VCS charge consumes part of r9's margin. The residual margin is arithmetic, not a reservation or a separate ledger;<br>- **Exhaustion may come first.** Operational exhaustion may occur before a malformed or oversized file is classified. It is typed `WORK.BUDGET_EXHAUSTED`, with no partial observation and never `unborn-head`;<br>- **A broader unconditional guarantee, or any cap change, would need a reviewed law-record revision.** r5 claims neither. | LD-C1B-6; §7 |
| **Q7 ruling** | **Adopted:** `INDEX_CAP` stays the reviewed 4 MiB read and refusal bound for `HEAD`, loose refs and `packed-refs`. The exact-cap and one-over controls are kept. A budget failure is never a partial observation or an unborn HEAD. | LD-C1B-6; §7 |
| Disposition 4 (`ENAMETOOLONG`) | **Adopted, with the member projection kept:** for a member, it refuses `member-vcs-unsupported:ref-name` (`MemberRefusal::VcsUnsupported("ref-name")`). | LD-C1B-2 |

## r4 changes (history; r5 above governs where they differ)

| What r3 said | r4 | Where |
| --- | --- | --- |
| LD-C1B-6, the size bound: "Each file's read cap reuses X2's sourced per-record ceiling, `INDEX_CAP` = 4 MiB … A file at exactly the cap is read, and one byte over refuses `vcs-unsupported:<file>-oversized`." The Q1 ruling (r3 changes table): "a reviewed reuse of the 4 MiB ceiling". | **The read caps are unchanged, and the term no longer prices `HEAD` and the loose ref at them.** Every Git file's read still stops at `INDEX_CAP` and refuses `<file>-oversized` one byte over, with the Q1 controls unchanged. But the VCS term prices `HEAD` and the loose ref at their **exact Git formats**, not at 4 MiB:<br>- the loose ref is LD-C1B-2's closed form, 40 hex + LF, **41 bytes**;<br>- `HEAD` is `ref: ` + the target + LF, or 40 hex + LF.<br>The shapes are Git's documented formats: gitrepository-layout(5), `HEAD` ("a symref … HEAD can also record a specific commit directly") and `refs/heads/name` ("records tip-of-the-tree commit objects"); git-symbolic-ref(1): "A symbolic ref is a regular file that stores a string that begins with ref: refs/." The 40 hex is the SHA-1 name length, because X2 refuses `extensions.*` (B-S2 LD-3). **`packed-refs` stays priced at 4 MiB** (the Q1 ruling). | LD-C1B-6 |
| LD-C1B-6, the term: "the ref segments' no-follow opens and captures, bounded by `HEAD`'s capped length". | **The term prices ref-directory work in full up to the depth r9's 2× rule supports, derived, not set: 226 directories per repository** (`r4-evidence/vcs_term_r4.output.json`, `derived.refDirectories`). At that depth, the same derivation supports a `HEAD` of up to **1,048,575 bytes** (`derived.headBytes`). The target's directory names are a part of `HEAD`'s bytes, and so are priced within them. Neither number is a product constant, and no code branches on either. | LD-C1B-6 |
| (none) | **Work past the derived bounds falls under r9's typed-refusal regime.** It is charged as performed, and at the snapshot ledger's caps it refuses `WORK.BUDGET_EXHAUSTED`, typed, never truncated. r9's record already places unbounded per-entry work there: "The typed-refusal regime. Work bounded by no item-5 or owner limit … Beyond the margin they refuse `WORK.BUDGET_EXHAUSTED`, typed and never truncated" (`c1a-r9/RECORD-r9.md`:191-197), under the law's "Exhaustion is `WORK.BUDGET_EXHAUSTED`, never truncation" (`PROPOSAL.md`:261). r9's caps are unchanged. **Codex is asked to judge this placement against r9, and to confirm that no law-record revision is needed** (Q6). | LD-C1B-6; §7 |
| (none) | **One clarification to LD-C1B-2.** A target component that the platform refuses as too long for a name (`ENAMETOOLONG` on a no-follow open) refuses `vcs-unsupported:ref-name`. It is never treated as absent, and the OS decides it, not a constant in C1b. | LD-C1B-2 |
| §4's C1b-1 controls | Two controls are added: a ref target whose directory work exceeds a ledger's remaining budget refuses `WORK.BUDGET_EXHAUSTED` with no partial observation; and a too-long target component refuses `ref-name`. One mutation is added: the budget refusal turned into a truncated or `unborn-head` result. | §4; §5 |

**The evidence** (`r4-evidence/`, all in the subject):
- `vcs_term_feasibility.py` and its output: r3's term as written, run by C1b-1 before its model change. With every Git file at 4 MiB, it is about 682 million objects, 18.7 billion edges and 1.79 TB, and fails all three caps. Even with exact formats and a `HEAD` target up to PATH_MAX, the edges fail: twice 10,929,692 is over 2^24. It shows that ref directories are the binding term, at 137 edges each (an ACL capture is 131), and that edges hold up to 226 directories.
- `vcs_term_r4.py` and its output: r4's pricing, with D* and H* found by search, and asserting that they hold and that one more of either fails:
  - **at D* = 226 and H* = 1,048,575:** the term is 173,770 objects, 2,165,048 edges and 1,643,899,072 bytes. The total is 950,446 objects, 8,383,512 edges and 4,182,771,458 bytes. Twice the total is 1,900,892, 16,767,024 and 8,365,542,916, each within 2^21, 2^24 and 2^33;
  - **one directory more:** twice the edges is 16,783,794, over 2^24;
  - **one `HEAD` byte more:** the read buffer doubles past 1 MiB, and twice the bytes is 8,638,173,066, over 2^33.
- Both scripts read the census's constants from a clean export of product `caa71e2` (`git archive caa71e2 crates tools`), after `costs` verifies the whole cost closure, and r9's adopted subtotal from `c1a-r9/evidence/option3_r2.output.json`. They are design evidence for the plan. **C1b-1's model change, its vectors and the full derivation are still owed before C1b-1's acceptance**, and C1b-1 must reproduce D* and H* or report the difference.

**What r4 leaves to r9's guarantee.** r9 guarantees that every tree within item 5 fits, with members, provided its work that is not a row stays within the margin over the subtotal (`RECORD-r9.md`:188). The VCS term uses part of that margin. At the derived bounds, what remains is 2^21 − 950,446 = 1,146,706 objects, 2^24 − 8,383,512 = 8,393,704 edges and 2^33 − 4,182,771,458 = 4,407,163,134 bytes. r9's figures were 1,320,476, 10,558,752 and 6,051,062,206.

## r3 changes (history; r4 above governs where they differ)

| Finding | Change | Where |
| --- | --- | --- |
| **R2-RF-1** (regenerated-output checks are not freshness assertions) | **The generated-output checks must pass, and the stale receipt is recorded apart from them** (LD-C1B-7, §6).<br>- **The checks:** after each sub-unit's re-pin and regeneration, `discovery_census.py --check` and `snapshot_ledger_census.py --check` must **pass**. Each compares regenerated bytes with the checked-in output (`discovery_census.py`:1373-1379; `snapshot_ledger_census.py`:283-303).<br>- **The stale record** is a separate evidence row, from public receipt fields only and never from held-out contents. It names the exact changed bindings: the receipt's `bindings` against the current inputs, entry by entry. It cites the rendered rows `outstanding: held-out (blind receipt stale)` and the published `heldOutMargin: outstanding`, which a valid receipt bound to other inputs renders (`discovery_census.py`:1205-1218), and the companion snapshot receipt's published status, as C1a4's refresh unit defines it (no companion receipt exists on main `3d1d771`; `snapshot_ledger_census.py` today publishes only lead-readable margins).<br>- **Still failures:** a malformed receipt, a bad pin, a missing artifact or any output difference.<br>- **Freshness**, where it is needed, is its own check: the receipt's bindings equal the current ones, and the rendered rows carry the `blind-census` status. It is never `--check`. After the batch's refresh, both receipts must be current and every output check must pass. | LD-C1B-7; §6 |
| **R2-RF-2** (one owner and one gate for the full VCS term) | **C1b-1 owns the complete VCS term** (LD-C1B-6, rewritten). That is its model change in `snapshot_ledger_model.py` (traversal, custody captures, read buffers, parsing and retained values), the regenerated vectors, and the full derivation showing r9's fixed caps hold by its 2× rule. All of it is evidence for C1b-1's own acceptance (the Q1 ruling). The term also prices the VCS record's sealing allocation at its maximum. **C1b-2 adds no model term.** Its only new sealing charge replaces the fixed `owned_record(160)` (`snapshot_seal.rs`:365, which `snapshot_ledger_census.py`:109 reads) with the VCS record's exact canonical length. C1b-1's term already prices that length at its maximum: schema 3 with 64 members, each at the longest `LogicalPath`. C1b-2's lane asserts that its charge sites equal those the derivation priced. C1b-2 is still a census input, because the census pins `snapshot_seal.rs` and reads its anchor (`snapshot_ledger_census.py`:48, :109, :262). It re-pins and regenerates within the batch, but changes no model term. | §2; LD-C1B-6; LD-C1B-7; §8 |
| **R2-NBO-1** (the C1b-0 row) | The C1b-0 row now says it **opens** the census batch, and refers to the single refresh after C1b-2. | §2 |
| **Q5 ruling** | **The batch-entry baseline** is C1a4's accepted refresh: its exact inputs, receipt pins and post-run review, current for those inputs before C1b opens the stale interval. After that it is historical baseline evidence only, not proof of the batch's freshness. The batch's pre-run review binds all final discovery and snapshot cost-source and recipe inputs, and its post-run review verifies both resulting receipts against them. No extra blind run and no held-out read. | LD-C1B-7; §7 |

## r2 changes

| Finding | Change | Where |
| --- | --- | --- |
| **R1-RF-1** (C1b-1 changes the census closure too) | **One reviewed, combined census batch** (LD-C1B-7, rewritten). Each sub-unit that changes a census input re-pins and regenerates its own census artifacts when it integrates, and the receipts are **explicitly stale** from C1b-0's integration until one reviewed blind validation and refresh after C1b-2 integrates. The three census inputs:<br>- **C1b-0:** the generator closure (`discovery_census.py`:1067);<br>- **C1b-1:** `custody/git_tracking.rs`, which the census's CLOSURE pins whole (`discovery_census.py`:87), so append-only helpers change its pin too;<br>- **C1b-2:** the VCS term in the snapshot ledger model, which changes the recipe the companion snapshot receipt binds.<br>During the interval no lane, census check or unit may rely on the receipts. Each sub-unit's lane records the census `--check` failure as the expected stale receipt, for exactly its closure or recipe reason. The refresh covers the discovery receipt and the companion snapshot receipt together: the complete cost-source closure, as C1a4's NBO-1 requires. It is a pre-run review of the batch's frozen inputs, its order and the blind mode, then the mechanical blind run, then a post-run review, all before any dependent lane needs a current census. C1a4's own blind refresh is a separate, earlier unit, and C1b's batch is a later refresh. | §2; LD-C1B-6; LD-C1B-7; §6; Q3 |
| **R1-RF-2** (the ref grammar admitted invalid names) | **The ref-name grammar is a closed subset of Git's `git-check-ref-format` rules, and admits nothing they reject** (LD-C1B-2, rewritten). It refuses `..` anywhere (`refs/heads/a..b`), a trailing `.` (`refs/heads/topic.`), a component beginning with `.`, a component ending `.lock`, control characters and DEL, space, `~ ^ : ? * [ \`, `@{`, the lone name `@`, and empty components (a leading, trailing or doubled `/`). The same grammar applies to `HEAD`'s target and to every name in `packed-refs`. Each rule is a control, including the two examples. A malformed name refuses `vcs-unsupported:ref-name`, which stays distinct from `unborn-head`. | LD-C1B-2; §4 |
| **R1-NBO-1** (bind the member record to this root) | **The same-root join is an explicit C1b/J2 composition precondition** (LD-C1B-3, extended). For a non-empty member set, the `AdmittedBoundaries` sealing reads must be the record of the discovery that ran over this very lent root, under its `NoRepository` (W2) proof. C1b-1 checks what it can: the record's `selected_root`, and that the lent `VcsSubject` is `NoRepository` whenever there are members. J2 binds the rest. A cross-root record control is added. | LD-C1B-3; §4 |
| **R1-NBO-2** (byte preservation compares the same inputs) | **The S4 preservation controls compare each fixed input before and after materialization.** For no repository, one repository and nested repositories, with the tracking observation, tree and inputs fixed, the schema-2 VCS record's bytes and digest, the full descriptor and `snapshot2` must be equal under the pre-S4 and the post-S4 schema. The expected changes across observation kinds (`kind`, `commitId`, `dirty` and the derived digests) are tested separately. | §4 |
| **Q1 to Q4 rulings** | Q1 is accepted as a reviewed reuse of the 4 MiB ceiling, with exact-cap and one-over controls and bounded parsing. The VCS term covers traversal, custody captures, read buffers and parsing, not only file lengths (LD-C1B-6). Q2: projection stays with J2's reviewed composition, and no route is inferred from shared spelling (LD-C1B-8). Q3 is answered by the RF-1 batch above. Q4: one symbolic level is an explicit conservative supported layout, not a claim about Git (LD-C1B-2). | LD-C1B-2, -6, -7, -8; §7 |

**What precedes it.** M3-C r8's units table gives C1b as "the VCS observation (item 4)", depending on C1a and VCS-1, size S (`snapshot-plan-c/PROPOSAL.md`:1181). VCS-1 must be accepted before C1b (:1173). Item 4 says "C1b lands S4 after B-S2 is accepted" (:334).
- **Met:** C1a1, C1a2 and C1a3 are integrated (C1a3 at `a68be52`). VCS-1 is accepted and bound (`vcs-1-r1-unit.json`; contract successor in `design-lock.json`). B-S2, which is S4, is accepted and bound (`config-discovery-b/b-s2-unit.json`; reviews/codex-b-s2-r1).
- **Met since r1:** **C1a4** is integrated at `57e5c48`: `WorkLedger::snapshot_profile` at r9's caps, with (a) and (b′). Its own blind refresh is a separate unit being planned now. LD-C1B-6's evidence extends C1a4's final model and recipe.
- **Open, and needed:**
  - **C1c** (the read set): it shares `snapshot_seal.rs` with C1b, but it is not a semantic dependency (LD-C1B-9).

**Authority:**
- **The law:** M3-C r8 item 4 (`PROPOSAL.md`:323-347), with controls C1-T15, C1-T16 and C1-T17 (:344-347); item 6's sealing order, step 4 (:378-384); item 2's one snapshot ledger (:250-257). Short names are as the law gives them (:126-135).
- **VCS-1** (`vcs-1-r1/CONTRACT.md`; IE:546's added passage): `dirty: true` for every Git observation means "cleanliness not established". It is never `false` from index stat data. `NoRepository` keeps `none`, `null`, `false`. The same meaning applies to each D15 member.
- **B-S2 / S4** (`config-discovery-b/b-s2/README.md`; its fragment `schemas/identity-schemas.v3.b-s2-additions.json`):
  - `vcs-observation` is schema 2 or schema 3. Schema 3 applies exactly when the project has an admitted member (LD-5).
  - Schema 3's top level is fixed at `none`, `null`, `false` (LD-2).
  - Members are 1 to 64, `kind: "git"`, `commitId` 40 lowercase hex, in `path` order (LD-3, LD-4).
  - The "Controls owed by C1b" list (README:127-132) and finding BS2-F2.
- **X2 r9** (`docs/implementation/m2/project-root-x2/PROPOSAL.md`:22, :157):
  - X2 itself admits `.git`, `config` and `index` only, for the enclosing repository and for each member.
  - "Any further Git object, such as `HEAD`, refs or `packed-refs`, is admitted only by C1's VCS-observation law, for every repository alike."
  - X2 refuses `extensions.*` (`git_tracking.rs`:303-304), linked worktrees (:902) and a gitfile `.git` (:892).
- **M3-B** item 21 (`config-discovery-b/PROPOSAL.md`:904) and item 19 / item 24 row 5: at most 64 members (`workspace_declarations.rs`:30) and 256 segments each (`git_tracking.rs`:1212).
- **SL**'s per-read custody, which item 4 cites as SL:313-315.

## 1. What C1b delivers

The sealed snapshot's `vcsDigest` for every tracking state the durable route can lend:
- **No repository and no member:** schema 2 `kind: none`, as C1a3 seals today (`snapshot_seal.rs`:254-262). Unchanged.
- **One or more enclosing Git repositories:** schema 2, `kind: git`. `commitId` is the **innermost** repository's HEAD, resolved through `HEAD`, a loose ref or `packed-refs` only. `dirty: true` (item 4; VCS-1).
- **A `NoRepository` root W with at least one admitted D15 member:** schema 3. The top level is `none`, `null`, `false`. `members` lists, in `path` order, each member's `{path, kind: "git", commitId, dirty: true}`, each resolved the same way (S4; VCS-1's second paragraph).
- **Refusals:**
  - an unborn HEAD (`vcs-unsupported:unborn-head`, item 4);
  - any HEAD, ref or `packed-refs` outside the closed forms (LD-C1B-2);
  - a custody failure;
  - evidence changed since X2's observation (LD-C1B-4).

  Each is typed. The public mapping is J2's (LD-C1B-8).
- **The ephemeral route stays `VcsPending`.** It still carries no tracking observation (`snapshot_source.rs`:70-77), and J2c brings one. C1b removes `VcsPending` only for the states it now observes.

**No Git object is read.** No zlib, no pack index, no delta, no tree comparison (item 4, "Rejected"). No environment, `$HOME` or global Git configuration is read (item 4, forbidden substitutes). X2's global and system sources are already judged at admission, and C1b reads none.

## 2. The split

| Sub-unit | Owns | Controls | Depends on |
| --- | --- | --- | --- |
| **C1b-0** | **S4's materialization** (BS2-F2). It **opens** the census batch, whose single refresh follows C1b-2 (LD-C1B-7, r3):<br>- B-S2's merge rule applied to `schemas/sources/identity-v3.schema.json`;<br>- the regenerated carriers (`crates/contracts/src/generated/identity.rs` and the TS output);<br>- the registry, admission-registry, admission-source-map and identity `SourcePin` re-pins, and `tools/contracts/generator-closure.json`;<br>- the evaluator's member joins beside `VCS_KIND_JOIN` (`run_links.rs`:364-373, `import_joins.rs`:205), which stays at the top level;<br>- **(r2)** the census batch opens: the generator-closure pin and the census artifacts it regenerates, after which the receipts are stale (LD-C1B-7). | B-S2's three byte vectors (README:42-48) admitted and byte-equal; its negatives (`check_b_s2.py`) refused at identity admission and at Run closure; schema-2 samples admitted under the merged `oneOf` with identical bytes; the generator's check mode | — (B-S2 bound) |
| **C1b-1** | **The Git reads** (security, new module `crates/security/src/snapshot_vcs.rs`, plus append-only `pub(crate)` helpers in the base-dirty `custody/git_tracking.rs`):<br>- the lending carries the tracking proof (LD-C1B-1);<br>- HEAD resolution in the closed forms (LD-C1B-2);<br>- per-read custody and the evidence recheck (LD-C1B-4);<br>- the members, reached as item 6b reaches them (LD-C1B-5);<br>- every step charged to the caller's ledger (LD-C1B-6);<br>- **(r2)** `git_tracking.rs`'s whole-file census pin (`discovery_census.py`:87) re-pinned and its census artifacts regenerated, within the batch;<br>- **(r3, R2-RF-2) the complete VCS term:** its model change in `snapshot_ledger_model.py`, the regenerated vectors, and the full derivation with r9's fixed caps and the 2× margin, all before C1b-1's acceptance (LD-C1B-6). | C1-T15's six cases; member resolution through a loose ref and `packed-refs`; each closed-form refusal; custody refusals; evidence changed; the charge exactness; the model `--check` and the derivation's cap evidence | C1a and C1a4 (integrated) |
| **C1b-2** | **Sealing** (host, `crates/host/src/snapshot_seal.rs`):<br>- the schema-2 `kind: git` record and the schema-3 record, hand-encoded to identity's canonical bytes as C1a3's encoders are, charged first, with no temporaries (C1a3 r2's allocation rule);<br>- step 4 of item 6's order;<br>- `VcsPending` narrowed to the ephemeral route;<br>- the member set taken as `AdmittedBoundaries`, not as strings (LD-C1B-3);<br>- **(r3)** **no model term**. Its only new charge is the VCS record at its exact canonical length, replacing `owned_record(160)` (`snapshot_seal.rs`:365), which C1b-1's term prices at its maximum. Its re-pin of `snapshot_seal.rs` and the census anchor at `snapshot_ledger_census.py`:109, with their regenerated artifacts, close the batch's inputs. **The batch's one reviewed blind validation and refresh follows C1b-2's integration** (LD-C1B-7). | C1-T16, C1-T17; the charge-site equality with C1b-1's derivation; B-S2's controls owed by C1b (README:127-132); the encoders against the identity crate's canonical encoder; the allocation pin extended | C1b-0, C1b-1 |

**Order (r2, r3):** C1b-0, then C1b-1 (accepted only with its complete VCS term and the cap derivation), then C1b-2, **then the batch's refresh** (LD-C1B-7). C1b-1 may be built and reviewed in parallel with C1b-0 (disjoint files), but it integrates after C1b-0, and C1b-2 needs both. Between C1b-0's integration and the refresh's post-run review, the receipts are stale, and no lane, census check or unit outside the batch relies on them. LD-C1B-6's ledger evidence uses C1a4's final model and recipe.

## 3. Lead decisions

- **LD-C1B-1. The lending carries the tracking proof, not a flag.** `SnapshotTracking` (`snapshot_source.rs`:40-49) is a public `Copy` enum and says only *whether* the root is in a repository. C1b needs *which* repository, so `SnapshotRoot::from_operation` (:57-66) records a crate-private `VcsSubject`, built only from the operation's own `TrackingObservation` over its own retained chain. It is constructed as `NoRepository::retained` is (`git_tracking.rs`:1114-1124; `operation_handoff.rs`:391), and has three forms:
  - `NoRepository`: the existing proof;
  - `Repository`: the chain index of the innermost directory whose `.git` X2 observed, with X2's metadata sample for that `.git`. The append-only helper derives it from X2's evidence labels; no caller can name a directory;
  - `Unobserved`: the ephemeral route.

  `tracking()` keeps its public answer.
  - **Rejected:** passing a repository path or descriptor from the caller, which is a caller assertion (LD-C1A3-2's rule); re-walking upward for `.git`, which is a second observation that could disagree with X2's.
- **LD-C1B-2. HEAD resolution: one closed form per file, fail closed.**
  - **`HEAD`** is exactly `<40 lowercase hex>\n` (detached; the hash is the `commitId`) or `ref: refs/<name>\n`. Anything else refuses `vcs-unsupported:head-malformed`.
  - **The symbolic target** is resolved one level only: a loose ref that is itself `ref: …` refuses `vcs-unsupported:symbolic-ref-chain`.
  - **The ref-name grammar (r2, RF-2)** is a closed subset of Git's documented `git-check-ref-format` rules. It admits only names that those rules accept, and `vcs-unsupported:ref-name` refuses anything else. The name begins `refs/`, and it is refused when it:
    - contains `..` anywhere, as in `refs/heads/a..b`;
    - ends with `.`, as in `refs/heads/topic.`;
    - has a component beginning with `.`;
    - has a component ending in `.lock`;
    - contains a byte below 0x20 or DEL (0x7f), or a space;
    - contains any of `~ ^ : ? * [ \`;
    - contains `@{`;
    - is the lone name `@`;
    - has an empty component (a leading, trailing or doubled `/`).

    The same grammar applies to `HEAD`'s target and to every name in `packed-refs`. A malformed name is never treated as absent: it refuses `ref-name`, never `unborn-head`.
    - **(r4)** A target component that the platform refuses as too long for a name (`ENAMETOOLONG` on a no-follow open) also refuses `ref-name`, and is never treated as absent. The OS decides it, not a constant in C1b. **(r5)** For a member it is `member-vcs-unsupported:ref-name`, the member projection every other refusal keeps.
  - **The loose ref**, reached segment by segment from `.git` with no-follow opens, is exactly `<40 lowercase hex>\n`. If it is absent, `packed-refs` decides.
  - **`packed-refs`:** an optional first line `# pack-refs with:` followed by space-separated traits, then lines `<40 hex> <refname>` and peel lines `^<40 hex>`. Any other line, a duplicate name, or a peel line not following a ref refuses `vcs-unsupported:packed-refs-malformed`. A loose ref present wins over `packed-refs`, as in Git.
  - **Unborn:** the name is in neither place. This refuses `vcs-unsupported:unborn-head` (item 4).
  - The hash is 40 hex because X2 refuses `extensions.*`, so `objectformat=sha256` never reaches C1b (B-S2 LD-3).
  - **One symbolic level** is an explicit, conservative supported layout for M3 (r2, the ruling on Q4), not a claim about Git. A symbolic loose ref, or a cycle, refuses without further traversal.
  - **Rejected:** following symbolic chains (an unbounded loop without a sourced depth); case-folding or trimming (it accepts bytes Git would not write); reading `logs/` or `ORIG_HEAD` (not item 4's files).
- **LD-C1B-3. The member set is discovery's own record.** C1a3's `SealInputs.members` is `&[String]` (`snapshot_seal.rs`, `SealInputs`), which a caller fills. C1b-2 takes `Option<&AdmittedBoundaries>` (`discovery_export.rs`:169-205; constructor `pub(crate)`, built by security's composition), and reads its `member_repositories()` (:224). Schema 3 applies exactly when that list is non-empty (B-S2 LD-5). The member's `path` is that relative path, which is IDS `LogicalPath`.
  - **(r2, NBO-1) The same-root join is a composition precondition.** A typed record is not, by itself, proof that it describes this root. For a non-empty member set, the `AdmittedBoundaries` passed must be the record of the discovery that ran over this very lent root, under that root's `NoRepository` (W2) proof (M3-B item 21's precondition; `operation_handoff.rs`:391). C1b checks what the types allow: the record's `selected_root` (`discovery_export.rs`:209) against the lent root's discovery spelling, and that the lent `VcsSubject` is `NoRepository` whenever members are present. A mismatch refuses as `Internal`. J2's composition owns the full join, which is the same discovery result, lent subject and observation, as it owns C1a3's walk-report provenance (C1A3-R1-NBO-1).
  - **Rejected:** strings from the caller, which is the provenance gap Codex raised for C1a3 (C1A3-R1-NBO-1).
- **LD-C1B-4. Per-read custody, and the evidence recheck for the enclosing repository.** Every Git object C1b reads is opened from a retained descriptor with no-follow opens, and judged before any byte is read:
  - files with X2's file custody (`judge_file`, `git_tracking.rs`:936: owner the invoking user or root, no group or other write, one link, ACL readable or omitted under the premise, on H's volume);
  - directories (`refs`, each ref segment) as `ProjectObject::Directory`.

  For the enclosing repository, `.git` is reopened from the lent chain directory, and its metadata sample must equal X2's evidence sample. Otherwise it refuses `vcs-unsupported:evidence-changed`, X2's own reason (:892, :806).
  - **Rejected:** trusting X2's descriptor across the fence release; skipping custody for HEAD because it is small.
- **LD-C1B-5. Members are reached as item 6b reaches them.** Each admitted member is reached from W's retained descriptor by no-follow opens on W's device. This is item 6b's path (`git_tracking.rs`:1274-1290), through an append-only helper exposing its reach step. Its `.git` is then judged and read under LD-C1B-2 and LD-C1B-4. Item 6b retained no member evidence for a recheck: "C1's per-read custody covers the snapshot" (:1272). So a member whose placement no longer holds refuses `member-vcs-unsupported:<reason>` or `member-outside-volume` (`MemberRefusal`, :1238-1252), with no second policy.
- **LD-C1B-6. The reads are charged to the snapshot ledger, and the r9 derivation gains a bounded VCS term.**
  - Item 2 charges the walk to one snapshot ledger per invocation (:250). Item 6 makes the VCS observation a step of sealing (:381). C1b's reads therefore take the caller's `WorkScope`, the snapshot ledger in production.
  - **The size bound (r2, the ruling on Q1; r4).** No source gives a separate bound for `HEAD`, a loose ref or `packed-refs`. Each file's read cap reuses X2's sourced per-record ceiling, `INDEX_CAP` = 4 MiB (`git_tracking.rs`:37-38; X2 item 9). This is a new, reviewed application of an existing ceiling, not a claim that the index rule already covers these files. A file at exactly the cap is read, and one byte over refuses `vcs-unsupported:<file>-oversized` before any byte past the cap is kept. Parsing is bounded by the bytes read: no per-line allocation beyond the charged buffer. **(r4)** The read cap is a refusal bound only. The term prices `HEAD` and the loose ref at their exact formats (below).
  - **The term (r2; r4).** At most 1 enclosing repository plus 64 members (`workspace_declarations.rs`:30). For each, the term counts:
    - the member's reach, at most 256 segments (`git_tracking.rs`:1212), at most one `LogicalPath` of names;
    - the `.git` reopen and its custody capture;
    - `HEAD`'s open and capture, and its read buffer, parse and retained target at its exact format: `ref: ` + the target + LF, of length H (gitrepository-layout(5), `HEAD`; git-symbolic-ref(1));
    - `refs` and the target's directories, D of them, each opened no-follow and judged as a directory on H's volume, their names within `HEAD`'s H bytes;
    - the loose ref's open, capture, read and parse at its exact format, 40 hex + LF, 41 bytes (LD-C1B-2's closed form; gitrepository-layout(5), `refs/heads/name`);
    - `packed-refs`'s capture, read and parse at `INDEX_CAP` (the Q1 ruling);
    - the retained commit, and the VCS record's sealing allocation at its maximum canonical length, **(r5)** 167 + Σ(91 + e(Pᵢ)) + (n − 1) bytes for schema 3. With n = 64 and every path at the largest e(P) of 24,496, that is 1,573,798 bytes, one owned buffer (the r5 changes table: e(·), the fixed parts, the verification and the ownership).

    Every term is priced under its existing owner's pricing, exactly as the model prices the walk's.
  - **(r4) The derived bounds, and the typed-refusal regime past them.** D and H are not set. They are the largest values for which r9's 2× rule holds in every component: **D* = 226** directories per repository, and at D*, **H* = 1,048,575** `HEAD` bytes (`r5-evidence/vcs_term_r5.py`, re-run in r5 with the record's canonical length). The term prices every repository in full up to D* and H*. Neither is a product constant, and no code branches on either. **(r5, the Q6 ruling)** They are evidence-envelope coordinates, not runtime thresholds. Exceeding either requires no refusal and does not by itself prove exhaustion: one more of either shows the loss of the 2× envelope, not that the ledger runs out.
    - **Past them,** the work is charged as performed. At the snapshot ledger's caps it refuses `WORK.BUDGET_EXHAUSTED`, typed and never truncated: r9's typed-refusal regime (`c1a-r9/RECORD-r9.md`:191-197; `PROPOSAL.md`:261). r9's caps are unchanged. **(r5)** `HEAD`'s length is bounded, by the Q1 read cap at 4 MiB, but that refusal bound is not a guaranteed 2× fit. r9's guarantee stays conditional on all work that is not a row, VCS included, fitting together in its margin (`RECORD-r9.md`:188).
    - **The same holds for a `HEAD` or loose ref outside its closed form,** read up to the 4 MiB read cap. It refuses anyway, under LD-C1B-2, or under the budget if the ledger is reached first: operational exhaustion may come before the file is classified. Either way it is typed, with no partial observation and never `unborn-head`.
    - **What r9's guarantee keeps (r5):** at D* and H*, the caps less the cumulative subtotal (with C1c-0's retention) and the VCS term leave 1,146,642 objects, 8,393,704 edges and 4,404,802,904 bytes (r9 had 1,320,476, 10,558,752 and 6,051,062,206). This is arithmetic, not a reservation or a separate ledger. Every other kind of work that is not a row shares it with the VCS work.
  - **(r3, R2-RF-2) The owner and the gate.** C1b-1 owns the complete term:
    - its model change in `snapshot_ledger_model.py`, on C1a4's final model;
    - the regenerated vectors;
    - the full derivation, showing that r9's caps (2^21 objects, 2^24 edges, 2^33 bytes) hold by r9's own 2× rule.

    These are evidence for C1b-1's acceptance. **(r4)** C1b-1's derivation reproduces D* and H* from its own model, or reports the difference before acceptance. The term also prices the VCS record's sealing allocation at its maximum **canonical encoded length** (r5): schema 3 with 64 member rows, each path at the largest escaped payload a `LogicalPath` admits, with the fixed syntax and separators. So C1b-2 adds no term, and its lane asserts that its new charge equals what the term priced. If the caps do not hold, C1b-1 stops for a law-record revision; it never raises a cap itself. **(r4)** C1b-1 did stop here once: r3's term, priced at 4 MiB with ref directories bounded only by `HEAD`'s capped length, failed all three caps (`r4-evidence/vcs_term_feasibility.output.json`). r4 is a plan revision that keeps r9's caps. Codex ruled (Q6) that no law-record revision is needed; a broader unconditional guarantee or any cap change would need one.
  - **Rejected:** a separate VCS ledger, which is a second ledger item 2 does not allow; an uncharged read.
- **LD-C1B-7 (r2, RF-1). One reviewed, combined census batch.** Three of C1b's changes are census inputs:
  - **C1b-0** changes a generator source, and the generator closure is a file the discovery census binds (`tools/security/discovery_census.py`:1067);
  - **C1b-1** appends to `custody/git_tracking.rs`, which the census's CLOSURE pins whole (`discovery_census.py`:87), so even append-only helpers change its pin;
  - **C1b-1** also owns the VCS term in the snapshot ledger model (r3), which changes the recipe the companion snapshot receipt binds;
  - **C1b-2** changes `snapshot_seal.rs`'s VCS-record charge site. The snapshot census pins that file and reads its anchor (`snapshot_ledger_census.py`:48, :109, :262), so it re-pins and regenerates, but it changes no model term.

  Under the ruling on Q3, one physical blind run may serve a reviewed batch of frozen final inputs. So:
  - **Each sub-unit re-pins and regenerates its own census artifacts** when it integrates: the closure pin, and the census records its change regenerates.
  - **The receipts are explicitly stale** from C1b-0's integration until the batch's refresh. During that interval, no lane, census check or unit may rely on them.
  - **(r3, R2-RF-1) The output checks pass; the stale state is recorded separately.**
    - **The checks:** after each sub-unit's re-pin and regeneration, `discovery_census.py --check` and `snapshot_ledger_census.py --check` must pass. They compare regenerated bytes with the checked-in output (`discovery_census.py`:1373-1379; `snapshot_ledger_census.py`:283-303); they do not assert freshness.
    - **The stale record:** each lane writes a separate stale-receipt row from public receipt fields only, never held-out contents. It names the exact changed bindings (the receipt's `bindings` against the current inputs, entry by entry). It cites the rendered `outstanding: held-out (blind receipt stale)` rows and the published `heldOutMargin: outstanding`, which a valid receipt bound to other inputs renders (`discovery_census.py`:1205-1218), and the companion snapshot receipt's published status, as C1a4's refresh unit defines it (no companion receipt exists on main `3d1d771`; `snapshot_ledger_census.py` today publishes only lead-readable margins). The changed bindings must be exactly the sub-unit's own inputs and those of the sub-units before it.
    - **Still failures:** a malformed receipt, a bad pin, a missing artifact and any output difference.
    - **Freshness** is its own check where a unit needs it: the receipt's bindings equal the current inputs, and the rendered rows carry `blind-census`. After the batch's refresh, both receipts must pass it and every output check must pass.
  - **The refresh follows C1b-2's integration** and covers both the discovery receipt and the companion snapshot receipt together. That is the complete cost-source closure, as C1a4's NBO-1 requires.
  - **Its sequence is B2-b4c3's** (as D2b plan r3 LD-D2B-1 describes, `supervisor-d/d2b/PLAN-r3.md`:86-87): a pre-run review of the batch's frozen inputs, their integration order and the blind mode; the mechanical blind run (the owner's standing answer); then a post-run review. All three complete before any dependent lane relies on a current census.
  - **C1a4's own blind refresh** is a separate, earlier unit, planned now. C1b's batch is a later refresh and does not stand in for it.
  - **(r3, the Q5 ruling) The batch-entry baseline** is C1a4's accepted refresh: its exact inputs, receipt pins and post-run review, and that its receipts were current for those inputs before C1b opened the stale interval. Once C1b changes the bindings, that receipt is historical baseline evidence only. The batch's pre-run review binds all final discovery and snapshot cost-source and recipe inputs, and its post-run review verifies both resulting receipts against them. This adds no blind run and reads no held-out tree, store or result.
  - **Rejected:** refreshing after C1b-0 alone (C1b-1 and C1b-2 would make that receipt stale at once); one refresh that silently covers edits made after it.
- **LD-C1B-8. Refusals are typed; the route is J2's.**
  - C1b-1 returns `VcsRefusal {Unsupported(reason), Member(MemberRefusal), Io}`, with reasons spelled as X2's (`vcs-unsupported:<reason>`, `member-vcs-unsupported:<reason>`).
  - C1b-2 wraps it as `SealError::Vcs`.
  - Item 4 names the subject (`vcs-unsupported:unborn-head`) but no code. Under the ruling on Q2, the projection is J2's reviewed composition, under its owning law's phase-appropriate no-Plan/no-Run route. No route is inferred from X2's shared subject spelling. C1b preserves the exact subject, and keeps work exhaustion and I/O distinct from refusal.
- **LD-C1B-9. C1b and C1c touch disjoint steps of one file.** Step 2 (the read set) is C1c's, and step 4 (VCS) is C1b's. Whichever lands second rebases its sealing edit onto the other. Neither needs the other's semantics, and C4a needs both (:1189).
- **LD-C1B-10. `dirty` is a constant, by law.** Every Git observation, enclosing or member, records `dirty: true` (item 4; VCS-1). The code has no branch that computes it, and a source pin asserts that `dirty` is written only as `true` for Git and `false` for `none`. The index already read by X2 is never used to decide it (item 4, "Rejected").

## 4. Controls

- **C1b-0:**
  - B-S2's three vectors (154, 190 and 365 bytes, README:42-48) admitted and byte-equal;
  - schema-2 records admitted under the merged `oneOf` with unchanged bytes;
  - B-S2's negatives refused at identity admission and at Run closure (`run_links.rs`);
  - the generator's check mode, the registry re-pins and verify_design;
  - the census `--check` passing after the refresh.
- **C1b-1:**
  - **C1-T15:** no repository; HEAD through a loose ref; HEAD through `packed-refs` (with and without the header, with peel lines); detached HEAD; unborn HEAD refusing `unborn-head`; the innermost of nested enclosing repositories;
  - a loose ref winning over `packed-refs`;
  - each LD-C1B-2 refusal (`head-malformed`, `symbolic-ref-chain`, `ref-name`, `packed-refs-malformed`);
  - **(r2, RF-2) one control per grammar rule**, each as `HEAD`'s target and as a `packed-refs` name: `refs/heads/a..b`; `refs/heads/topic.`; a component beginning with `.`; a `.lock` component; a control byte; DEL; a space; each of `~ ^ : ? * [ \`; `@{`; the lone `@`; a leading, a trailing and a doubled `/`. Each refuses `ref-name`, never `unborn-head`;
  - a symlinked ref segment refusing under custody;
  - **(r2, Q1) the caps:** each Git file at exactly 4 MiB is read, and one byte over refuses `<file>-oversized` with nothing kept past the cap;
  - **(r4) the regime:** a ref target whose directory work exceeds the ledger's remaining budget refuses `WORK.BUDGET_EXHAUSTED`, with no partial observation and never `unborn-head`; a target component too long for the platform refuses `ref-name` (for a member, `member-vcs-unsupported:ref-name`). These exercise the actual remaining allowance, never D* or H*;
  - **(r5, R4-RF-1) the record length:** the model's record-length function equals `canonical_bytes` for paths with `"`, every short escape, a six-byte control, DEL, C1 and 2-, 3- and 4-byte UTF-8, and at the maximal record (64 paths at e(P) = 24,496);
  - **(r2, NBO-1) a cross-root record:** an `AdmittedBoundaries` whose `selected_root` is another root's, and a non-empty member set under a `Repository` subject, each refusing;
  - **custody (LD-C1B-4):** a group-writable `HEAD`, a hard-linked `packed-refs`, and a symlinked `refs` directory each refuse;
  - **evidence changed:** `.git` replaced between X2's observation and the read;
  - **members (LD-C1B-5):** two members resolved, one by a loose ref and one by `packed-refs`; a member whose placement changed refusing with `MemberRefusal`'s subject;
  - **charges:** the ledger's charge equals the recorded calls' price (C1a2's and D3a-0's method), and an over-cap file refuses before it is read beyond the cap;
  - no environment read, by source pin.
- **C1b-2:**
  - **C1-T16:** `dirty` is `true` for every Git case, and the source pin of LD-C1B-10;
  - **C1-T17:** `sourceInventoryDigest` is the inventory's canonical SHA-256, unchanged in schema 3;
  - **B-S2's controls owed by C1b (r2, NBO-2):**
    - **preservation, the same inputs on both sides:** for each of no repository, one repository and nested repositories, with the tracking observation, tree and inputs fixed, the schema-2 VCS record's bytes and digest, the full descriptor and `snapshot2` are equal under the pre-S4 and the post-S4 schema (C1b-0 records the pre-S4 side);
    - **separately, the changes across observation kinds:** `kind`, `commitId` and `dirty` change exactly as item 4 says, and the derived `vcsDigest` and `snapshot2` change with them;
    - a two-member and a 64-member workspace recording schema 3 in path order;
    - a workspace whose candidates were all excluded recording schema 2 `kind: none`;
  - the hand encoders against the identity crate's canonical encoder;
  - **(r5, R4-RF-1) the record's charge:** for each of C1b-1's record-length cases, the charge equals the exact encoded length and the hand encoding equals `canonical_bytes`. A scope one byte short refuses `Budget` before the buffer is allocated. The member paths are borrowed and the buffer is the only allocation;
  - the allocation pin, extended to the new records;
  - `VcsPending` only for `Unobserved`.

## 5. Mutations

- **C1b-0:** the `oneOf` admitting an empty `members`; the member `commitId` pattern relaxed; `VCS_KIND_JOIN` dropped at the top level.
- **C1b-1:**
  - a symbolic chain followed;
  - `packed-refs` read before the loose ref;
  - an unborn HEAD taken as a null commit;
  - custody skipped for `HEAD`;
  - the evidence recheck skipped;
  - the outermost repository taken instead of the innermost;
  - a read uncharged;
  - **(r4)** the budget refusal turned into a truncated or `unborn-head` result.
- **C1b-2:**
  - `dirty` computed (taken as `false`) for one Git case;
  - schema 3 written for a zero-member project;
  - members out of path order;
  - the inventory digest recomputed per member.

## 6. Checks

Each sub-unit's lane, as C1a3's and D3a-0's do:
- the host and security suites at base and candidate, with equal failure sets and the new passing tests;
- for C1b-0, also identity, contracts and evaluator;
- rustfmt on new and base-clean files only (`git_tracking.rs` and `git_tracking_tests.rs` are base-dirty: append only);
- warning-denied all-targets Clippy;
- the operability source census, with the mint census by its own audit (no new `from(`, `into(`, `line(`, `pid(` or `issue(` calls);
- the environment exceptions (no new environment read, tests included);
- FW-01;
- **(r3) the census output checks:** `discovery_census.py --check` and `snapshot_ledger_census.py --check` pass in every lane, after the sub-unit's own re-pin and regeneration (LD-C1B-7);
- **(r3) the stale-receipt record**, separate from them: the exact changed bindings and the published stale rows and status, from public receipt fields only, while the batch is open;
- **(r3) the freshness check**, after the batch's refresh: both receipts current for the final inputs;
- verify_design.

## 7. Open questions

r1's Q1 to Q4 are ruled (r2 changes table) and folded into LD-C1B-2, -6, -7 and -8.
- **Q5 (r2)** is ruled (r3 changes table) and folded into LD-C1B-7.

- **Q6 (r4)** is ruled (`codex-c1b-plan-r4`): no law-record revision is needed. The VCS charge consumes r9's conditional margin, and D* and H* are evidence-envelope coordinates. The qualifications are folded into LD-C1B-6 (r5 changes table).
- **Q7 (r4)** is ruled: `INDEX_CAP` stays the 4 MiB read and refusal bound for all three files.

No question is open in r5.

## 8. Not delivered

- **The ephemeral route's observation:** J2c; `Unobserved` stays `VcsPending`.
- **Any Git object reading, exact `dirty`, or per-path change set:** rejected by item 4. `vcs-change@vcs-reported` stays unminted, as item 4's LD8-3 requires.
- **A `vcs-revision` correspondence:** M5 (BS2-F1; VCS-1).
- **The read set:** C1c.
- **The snapshot ledger's constructor and caps:** C1a4. C1b-1 adds the complete VCS term, its vectors and the cap derivation (LD-C1B-6). C1b-2 adds no term.
- **Composition:** J2b and J2c.

## 9. Not claimed

- **(r4)** No change to r9's caps, and no new product constant: D* and H* are derived evidence only.
- **(r5)** No unconditional fit guarantee: r9's guarantee stays conditional on all work that is not a row fitting its margin.

- No code. No caller, no qualification, and no completion of C1 or M3-C.
