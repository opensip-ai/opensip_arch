# SECHARDEN-RELEASE r2: consumers of a component's `release` revocation subject (successor record)

**Author:** SEC-HARDEN-1 (w3C:p1), Claude Opus 5.5 / high, R3-FRONTIER.
**Authority:** LD-Q-256 (`coordinator/msg-ldq256.txt`, `e512c6be…`), on REVIEW-r2 (`8931fc7b…`). The coordinator adopts it by receipt on an R3 ADOPTABLE score.
**Status:** proposed. Scored by `SECHARDEN-RELEASE-SUCCESSOR`. r2 is r1 (`9d0b5b69…`) with REVIEW-r3's amendments A to E applied verbatim (`69a9e4ab…`).
**Pins:** product dev base `bcd03cd47c4cab87f55992711ee11661496aff12`; architecture `5f328f32dc5fe026d0b044c487b1d2070ec4b863`.

## 1. The gap

COMPONENT-RELEASE-SUBJECT r1 fixed how a `release` entry names a component: byte-equal to the catalog row's lowercase 64-hex `manifestDigest`. It named one consumer, P-1. Everywhere else, such an entry is checked against the core only:

| Site | Today |
|---|---|
| Acceptance (`trust_bootstrap.rs` `revokes`) | Matches `release` for TR-CORE only, so it records TR-COMPONENT `ST-TRUSTED` |
| Read (`current_trust_admission.rs` `admit_revocation`) | Compares the core closure only |
| Observer (`live_observation.rs` `predicate`) | Its `releases` subjects are the core closure only |

## 2. The selection

Each item below adds to its parent. Every rule not named stays in force.

**S1. COMPONENT-RELEASE-SUBJECT r1 §3.5, and the owed security-completion.v2 §4.5 binding.** A component `release` subject has four consumers: P-1, X4T admission, X4B acceptance and the X4 observer. Unchanged:
- the exact byte-equal spelling;
- the core's `closure2:` spelling and handling;
- refusing the whole view, never filtering a component out;
- the schema and the other three subject kinds.

The §4.5 binding owed at SEC-PREDRAW-1's binding names all four consumers. If that binding has already been published, this record binds as its successor.

**S2. X4T r13 items 4 and 10: the read.** "A revoked component in the closure" includes every component of the read's current inventory.
- A `release` entry of the read's admitted list that is byte-equal to the `manifestDigest` of any such component refuses at admission, on `Continuation("release:<manifestDigest>")`. This is the existing revoked-component row of item 10.
- It applies to every read mode: fenced, report, confirming and reread.
- It sits in item 4's existing check, so it runs before policy and time, and entries are judged in list order as today.
- The first matching entry in the admitted list wins, considering both existing subjects and the newly recognized component releases. Consequently a newly recognized component entry can replace the subject of an earlier implementation's refusal when that entry precedes its old first match. If an old match precedes every new match, its result stays first. A new match also preempts the item-1 quorum-completeness guard and later policy/time/floor work that would otherwise be reached; it does not preempt authentication or other checks preceding this loop. No separate component-first pass or reordering is selected.
- Refusals that come before item 4 keep their precedence, including the stored-state join.
- P-1's step R stays as defence in depth.

**S3. X4B r6 item 4: acceptance.** A carried component manifest is a document of TR-COMPONENT for `Revoke` (item 4 step 3, `:114`).
- If the payload's verified list has a `release` entry byte-equal to the lowercase hex SHA-256 of a carried manifest's body, TR-COMPONENT's sequence is `Present`, then `Clock` where it applies, then `Revoke`, ending `ST-REVOKED`, with `conditionEvidence.revokedBy` naming the event. One match revokes the role, because the role is judged on all its manifests together (`:132`).
- The digest is SHA-256 of the carried manifest's exact raw stored body bytes, rendered as lowercase hexadecimal. It is not a canonicalized body, envelope digest, or metadata-preimage digest. Acceptance matches the authenticated carried body; this successor does not add a catalog-to-body join to acceptance. A successfully joined X4T inventory requires that digest to equal the corresponding catalog row's manifestDigest. If the row instead names D and the carried body hashes to H != D, a list naming H still causes the carried role's Revoke, while an entry naming only D does not revoke that different carried body. The mismatched inventory never becomes usable: X4T's existing join still refuses if reached, and a newly recorded noncontinuable state may refuse earlier. No malformed catalog or mismatched inventory is made admissible by this rule.
- The acceptance is recorded. Confirming admission retains its existing check order and core/index/component standing precedence. When those preceding checks pass, the recorded TR-COMPONENT Revoked state yields the continuation subject component:revoked before S2 is reached. An earlier core or index refusal remains that refusal, including an expired or stale core. An older stored Trusted record is not migrated and instead reaches S2's release:<digest> refusal when earlier checks pass. A role already revoked by another applicable subject receives the existing single Revoke event, not a second event for the added release match.
- Unchanged: threshold authentication, which still refuses a manifest below quorum before `Present` and writes nothing; a payload with no component manifests, which stays `Unbootstrapped`; and all other roles and subject kinds.

**S4. X4 r8 item 6 (`:205`), read with item 5: the observer.** The closure subjects also include the `manifestDigest` of every component in the fenced read's inventory.
- They are start subjects: immutable for the operation's lifetime, and kept even when a later catalog no longer lists the component. This is not a refresh of the guard.
- These identities come from the fenced read's authenticated and catalog-joined inventory and are present in its admitted view independently of optional P-0 retained-inventory output. In particular begin with retain:false must retain these closure subjects for its observer even though it retains no P-1 inventory. Capture them before the authenticated input is moved or dropped. Subsequent rereads do not replace the immutable start subjects. Required retention and copies remain subject to section 5's accounting obligation.
- They match only as `observe_revocation` already matches, against a list whose version is newer than the start's, with floors and monotonicity unchanged.
- A match is the existing revoked-during-operation result, subject `trust-revoked`.

## 3. Behaviour changes and precedence

No other trust-semantic change is selected. Existing authentication, stored-standing, custody, budget, floor and list-version rules retain their order except for the newly recognized matches at S2/S3/S4. The following consequences are explicit; examples of a particular row assume all preceding checks pass.

- At otherwise admissible new acceptance, a carried-body release match now makes TR-COMPONENT Revoked after Present and any applicable Clock. Previously that role could finish Trusted, Expired or StaleRevocation. If another applicable subject already caused Revoke, no second Revoke is added. Acceptance remains durable even if the confirming read refuses. With continuable core and index the confirming subject is component:revoked; an earlier noncontinuable core/index or other preceding failure still wins.
- An existing on-disk Trusted role is not rewritten. A current-inventory release match now refuses every admission mode at item 4, with the first matching list entry's subject. Stores that previously reached begin, policy, time, floor publication or P-1 can now stop there, without the later work. A previously refused store can change subject when a newly recognized entry precedes the old first match, or change from a later failure to this earlier release refusal.
- During an operation, a successful current-store reread is still required as a whole view. A release-revoked component in that current inventory causes the S2 refusal and existing trust-revoked classification, whether or not that component was in the operation's start inventory. If an earlier stored-standing or authentication/custody failure prevents S2, its existing fail-stop classification remains in force.
- After a successful reread, a genuinely newer list naming a start component causes S4's trust-revoked result even when the current catalog has dropped it. Thus behavior can change although the current store's list names none of its own components. Same-version behavior of the predicate is unchanged; that does not exempt a current view from S2 or other admission checks.
- Acceptance may have authenticated bodies that do not join to their catalog rows. S3's explicit H/D rule applies: a carried-body match may now record Revoke and yield a standing refusal before X4T's former inventory-join refusal. An entry naming only a different catalog digest does not revoke the carried body; the unchanged join still prevents its use.
- Added retention/copy work remains subject to the existing budgets. Section 5 requires the implementation review to establish charged-or-covered bounds and state any changed budget-boundary outcomes; this record grants no uncharged-work exemption.

Reach today remains the bounded source assessment: no production command/publisher execution is established by this record. Future list publication and release-tool reachability remain unproved here. No stored-record migration or publisher is added.

## 4. Not selected

- **Refusing at acceptance:** X4B's sequence treats a document at quorum as `Present` then `Revoke`, and records it honestly. A refusal would be a new exception (REVIEW-r2).
- **No change at acceptance:** the store would record `Trusted` for a role its own signed list revokes (LD-Q-256).
- **Refreshing the observer's subjects from each reread:** a component dropped from the catalog would then escape, which is the case S4 exists for.

## 5. What this leaves open

- No budget constant changes. The added digest retention and its copies must be charged or proven covered, with a bound, a control and `size_of` sizes, in item 2's implementation review (REVIEW-r2 finding 3, LD-Q-256).
- CP-X4T-CEILING-1 is separate (SEC-HARDEN-2).

## 6. Controls owed by item 2's code

All run on scratch fixtures, with envelope and preimage digests distinct from `manifestDigest`, as the adoption receipt requires:

- **C-SR-1, read:** C-CRS-1 to C-CRS-5 repeated at the read, in fenced, report and reread modes.
- **C-SR-2, acceptance:** real acceptance of a payload naming its own component ends `ST-REVOKED`, records `revokedBy`, and the confirming read refuses on `component:revoked`. Expired and stale variants record their `Clock` step. A below-quorum manifest in the same payload still refuses and writes nothing. An unrelated `release` entry leaves `ST-TRUSTED`.
- **C-SR-3, already on disk:** a hand-built `ST-TRUSTED` store refuses on `release:<digest>` through `begin` and the durable path, before P-1, with `state.v1` unchanged.
- **C-SR-4, observer, component still listed:** a newer list stops the operation with `trust-revoked`.
- **C-SR-5, observer, component dropped:** first a lawful later store without the component, and then a newer list naming it. Without the start subjects the operation continues; with them it stops. A same-version list and an unrelated release do not stop it.
- **C-SR-6, funding:** the digest accounting above, with an over-limit witness.

Amendments to these controls:

- C-SR-1 also crosses a new component-release match with an existing namespace or core-release match in both entry orders, asserting the exact returned subject; crosses a new match with a later policy/time refusal and checks absence of later floor publication; and verifies an earlier stored-standing refusal still wins. The confirming-read mode is covered through C-SR-2.
- C-SR-2 tests distinct H/D mismatches in both directions: a list naming carried-body H records Revoke, whereas a list naming only different catalog digest D does not revoke that body; neither confirming path yields a usable view. It also tests an already-revoked component role for no duplicate Revoke event and an earlier noncontinuable core/index. Expired/stale variants must assert their actual earlier standing row as well as the component event sequence, rather than always expecting component:revoked. Keep no-components typed absence and below-quorum/no-write controls.
- C-SR-4 includes a current component absent from the start inventory, proving the inherited whole-view reread refusal and classification.
- C-SR-5 runs the dropped-component lifetime case through both retain:false begin and the retaining durable path. Equal-version and unrelated-release negatives apply to the start-subject predicate after successful current-view admission, with no other revoking match; they do not override S2 or earlier failures. Retain the mutant comparison showing that omitting start digests would continue.
- C-SR-6 covers start-subject retention and every copy/set construction, including nonretaining begin, report/reread paths as applicable, and both observation attempts, using measured size_of sizes and an over-limit witness or proof of existing charge coverage.
