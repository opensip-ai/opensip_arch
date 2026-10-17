# C1b implementation plan r2: the VCS observation (M3-C r8 item 4, VCS-1, M3-B successor S4)

**Lead plan, 2026-10-17. Proposed; it needs Codex review.** Round 2 answers Codex `codex-c1b-plan-r1` (REQUIRED-FINDINGS: two RFs and two NBOs, with rulings on Q1 to Q4). r1 (`PLAN-r1.md`) is history.

**Bases:**
- product main `3d1d771` (the v221 lock): C1a4 integrated at `57e5c48` (the snapshot ledger profile and its classification remedies), with inventory v221; D2b-2 integrated;
- the current architecture head, and the files the subject manifest names.

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
| **C1b-0** | **S4's materialization** (BS2-F2), then a reviewed blind refresh (LD-C1B-7):<br>- B-S2's merge rule applied to `schemas/sources/identity-v3.schema.json`;<br>- the regenerated carriers (`crates/contracts/src/generated/identity.rs` and the TS output);<br>- the registry, admission-registry, admission-source-map and identity `SourcePin` re-pins, and `tools/contracts/generator-closure.json`;<br>- the evaluator's member joins beside `VCS_KIND_JOIN` (`run_links.rs`:364-373, `import_joins.rs`:205), which stays at the top level;<br>- **(r2)** the census batch opens: the generator-closure pin and the census artifacts it regenerates, after which the receipts are stale (LD-C1B-7). | B-S2's three byte vectors (README:42-48) admitted and byte-equal; its negatives (`check_b_s2.py`) refused at identity admission and at Run closure; schema-2 samples admitted under the merged `oneOf` with identical bytes; the generator's check mode | — (B-S2 bound) |
| **C1b-1** | **The Git reads** (security, new module `crates/security/src/snapshot_vcs.rs`, plus append-only `pub(crate)` helpers in the base-dirty `custody/git_tracking.rs`):<br>- the lending carries the tracking proof (LD-C1B-1);<br>- HEAD resolution in the closed forms (LD-C1B-2);<br>- per-read custody and the evidence recheck (LD-C1B-4);<br>- the members, reached as item 6b reaches them (LD-C1B-5);<br>- every step charged to the caller's ledger (LD-C1B-6);<br>- **(r2)** `git_tracking.rs`'s whole-file census pin (`discovery_census.py`:87) re-pinned and its census artifacts regenerated, within the batch. | C1-T15's six cases; member resolution through a loose ref and `packed-refs`; each closed-form refusal; custody refusals; evidence changed; the charge exactness | C1a (integrated) |
| **C1b-2** | **Sealing** (host, `crates/host/src/snapshot_seal.rs`):<br>- the schema-2 `kind: git` record and the schema-3 record, hand-encoded to identity's canonical bytes as C1a3's encoders are, charged first, with no temporaries (C1a3 r2's allocation rule);<br>- step 4 of item 6's order;<br>- `VcsPending` narrowed to the ephemeral route;<br>- the member set taken as `AdmittedBoundaries`, not as strings (LD-C1B-3);<br>- **(r2)** the VCS term in `snapshot_ledger_model.py` (LD-C1B-6), changing the companion snapshot receipt's recipe. This closes the batch's inputs, and **the batch's one reviewed blind validation and refresh follows C1b-2's integration** (LD-C1B-7). | C1-T16, C1-T17; B-S2's controls owed by C1b (README:127-132); the encoders against the identity crate's canonical encoder; the allocation pin extended | C1b-0, C1b-1 |

**Order (r2):** C1b-0, then C1b-1, then C1b-2, **then the batch's refresh** (LD-C1B-7). C1b-1 may be built and reviewed in parallel with C1b-0 (disjoint files), but it integrates after C1b-0, and C1b-2 needs both. Between C1b-0's integration and the refresh's post-run review, the receipts are stale, and no lane, census check or unit outside the batch relies on them. LD-C1B-6's ledger evidence uses C1a4's final model and recipe.

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
  - **The size bound (r2, the ruling on Q1).** No source gives a separate bound for `HEAD`, a loose ref or `packed-refs`. Each file's read cap reuses X2's sourced per-record ceiling, `INDEX_CAP` = 4 MiB (`git_tracking.rs`:37-38; X2 item 9). This is a new, reviewed application of an existing ceiling, not a claim that the index rule already covers these files. A file at exactly the cap is read, and one byte over refuses `vcs-unsupported:<file>-oversized` before any byte past the cap is kept. Parsing is bounded by the bytes read: no per-line allocation beyond the charged buffer.
  - **The term (r2):** at most 1 enclosing repository plus 64 members (`workspace_declarations.rs`:30). For each, the term counts:
    - the member's reach, at most 256 segments (`git_tracking.rs`:1212);
    - the `.git` reopen and its custody capture;
    - `HEAD`'s open, capture and read buffer;
    - the ref segments' no-follow opens and captures, bounded by `HEAD`'s capped length;
    - the loose ref's read;
    - `packed-refs`'s capture and read;
    - the parsed and retained values.

    Every term is priced under its existing owner's pricing, exactly as the model prices the walk's. It is added to `snapshot_ledger_model.py` on C1a4's final model. That makes it a recipe change for the companion snapshot receipt (LD-C1B-7). C1b-1's evidence must show that r9's caps (2^21 objects, 2^24 edges, 2^33 bytes) still hold by r9's own 2× rule. If they do not, C1b-1 stops for a law-record revision; it never raises a cap itself.
  - **Rejected:** a separate VCS ledger, which is a second ledger item 2 does not allow; an uncharged read.
- **LD-C1B-7 (r2, RF-1). One reviewed, combined census batch.** Three of C1b's changes are census inputs:
  - **C1b-0** changes a generator source, and the generator closure is a file the discovery census binds (`tools/security/discovery_census.py`:1067);
  - **C1b-1** appends to `custody/git_tracking.rs`, which the census's CLOSURE pins whole (`discovery_census.py`:87), so even append-only helpers change its pin;
  - **C1b-2** adds the VCS term to the snapshot ledger model, which changes the recipe the companion snapshot receipt binds.

  Under the ruling on Q3, one physical blind run may serve a reviewed batch of frozen final inputs. So:
  - **Each sub-unit re-pins and regenerates its own census artifacts** when it integrates: the closure pin, and the census records its change regenerates.
  - **The receipts are explicitly stale** from C1b-0's integration until the batch's refresh. During that interval, no lane, census check or unit may rely on them. Each sub-unit's lane records the census `--check` failure as the expected stale receipt, for exactly its own closure or recipe reason, and fails on any other difference.
  - **The refresh follows C1b-2's integration** and covers both the discovery receipt and the companion snapshot receipt together. That is the complete cost-source closure, as C1a4's NBO-1 requires.
  - **Its sequence is B2-b4c3's** (as D2b plan r3 LD-D2B-1 describes, `supervisor-d/d2b/PLAN-r3.md`:86-87): a pre-run review of the batch's frozen inputs, their integration order and the blind mode; the mechanical blind run (the owner's standing answer); then a post-run review. All three complete before any dependent lane relies on a current census.
  - **C1a4's own blind refresh** is a separate, earlier unit, planned now. C1b's batch is a later refresh and does not stand in for it.
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
  - a read uncharged.
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
- **the census `--check` (r2):** while the batch is open, recorded as the expected stale receipt, for exactly the sub-unit's own closure or recipe reason (LD-C1B-7); after the batch's refresh, current;
- verify_design.

## 7. Open questions

r1's Q1 to Q4 are ruled (r2 changes table) and folded into LD-C1B-2, -6, -7 and -8.
- **Q5 (r2).** The batch's pre-run review will judge the frozen inputs. Should it also re-confirm C1a4's refreshed receipt as its baseline, since the batch's comparison starts from that receipt?

## 8. Not delivered

- **The ephemeral route's observation:** J2c; `Unobserved` stays `VcsPending`.
- **Any Git object reading, exact `dirty`, or per-path change set:** rejected by item 4. `vcs-change@vcs-reported` stays unminted, as item 4's LD8-3 requires.
- **A `vcs-revision` correspondence:** M5 (BS2-F1; VCS-1).
- **The read set:** C1c.
- **The snapshot ledger's constructor and caps:** C1a4. C1b-1 adds its term to their evidence (LD-C1B-6).
- **Composition:** J2b and J2c.

## 9. Not claimed

- No code. No caller, no qualification, and no completion of C1 or M3-C.
