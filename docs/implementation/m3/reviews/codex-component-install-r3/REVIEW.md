# Component release installation and tree custody — CI r3 review

Verdict: **REQUIRED-FINDINGS** — one required finding and two non-blocking observations. This is a law review only; no code, binding or qualification is accepted.

## Subject and verification

Manifest: 961 bytes, SHA-256 `6d9610db69ef71460881db947d6d52016a806a14bc347e293731a95b5d075e50`. All four members match their pinned lengths and hashes. PROPOSAL-r3.md is 49,811 bytes, SHA-256 `3f74b023b3cde759f7504ec4a78bc8900757fda62bb942dfb08c0fe22182eed4`. Both historical proposals and the input memo are unchanged. Live product HEAD `b7538549b727e13013f36d3b7c2e2917e767f3f2` and architecture HEAD `a87c1234b26544e65cd2d36b613f218da41b4e86` match the manifest bases.

Read the request, complete subject, round-2 findings/rulings and relevant primitive sources: same-parent publication, directory/file effects, WorkLedger::effect and ReservedPostchecks, snapshot buffer/read envelopes, D3a traversal pricing, and the registered installation budget route. Rehashed the PKG dependency at `8321d527843c63592d8e4fd49c3df0ace690da0bcbcd1e268464e578fe30424c` and confirmed the exact 15 archive-profile cases; verified the WORK.BUDGET_EXHAUSTED registration. No Cargo, rustc, builds, tests, lanes, shared lane lock, network, private fixtures, installation directory, keys, held trees, T2/cache/held-out material, other panes or delegation were used. Neither repository was edited.

## Required finding

### CI-R3-RF-1 — Complete the admission-bound recipe for the transaction and reader

P2; `docs/implementation/m3/component-install/PROPOSAL-r3.md:104`.

The table defines B as the sum of its terms and promises every actual charge is covered, but required operations have no term. D is explicitly the set of committed directory rows, so its per-dir terms do not cover creation of the extra tree/ container, its final fchmod/barrier, or the final stage-directory barrier (steps 2 and 4.4-4.5). The generation.json term prices its owned bytes and P-1/P-2/P-3, but omits its required exclusive create at step 4.2. private_directory_stage_cost covers neither these child operations nor recursive barriers. The enumeration row covers readdir/status calls, while the cited D3a discipline separately charges descend_cost for directory opens/duplicates, streams and stack/name storage; those setup costs are absent. The recipe likewise leaves archive opening, custody checks, and V2 association-record reading/validation without a complete charge derivation. Item 6 refers back to these prices for its own opens, records and pin capability. This is still a partial operation inventory rather than the claimed complete computable admission bound, so R2-RF-5 is not fully resolved.

Required change: Add explicit fixed/container and metadata terms, including create_exclusive_directory_cost("tree"), tree finalization and the stage barrier, create_exclusive_regular_cost("generation.json"), bounded V2 record read/admission, and the chosen open/custody/traversal setup and owned-storage prices. Publish a priced traversal helper or an equal conservative recipe that includes descent and stream/stack setup, not only READ_COST. Complete the no-op/read/transfer branch recipes or name their distinct bounded formulas, including pin descriptor/state checks. Define checked count/size arithmetic and the authenticated release fields needed for the record-length term; B need not depend solely on TreeCommitment bytes. Keep borrowed evidence uncharged and distinguish reserved charges from separately executed work. Extend CI-T22 with a valid file-only tree (D=0), nested directories, metadata-only operations and a preexisting-generation verification path, independently enumerating every charged call/owned representation so actual charges are demonstrably bounded by the published recipe.

## Non-blocking observations

### CI-R3-NBO-1 — Spell out the effect/postchecks split and the reservation-shortfall route

`docs/implementation/m3/component-install/PROPOSAL-r3.md:127`.

The suffix can be implemented with the selected API, but WorkLedger::effect charges effect + postchecks while ReservedPostchecks receives only postchecks. publish_exclusive_reserved itself spends the publication cost from that allowance. Assigning the rename cost only to effect would therefore leave it unavailable to the reserved helper, despite the outer charge. Also, this paragraph calls a suffix reservation shortfall install-budget, while item 8 and CI-T22 classify in-operation exhaustion through law 468. The initial B-versus-remaining admission check is a separate event.

Suggested change: Give an explicit mapping, for example effect = zero and postchecks = the complete suffix cost when both publication and barrier use _reserved, plus a priced allowance for the additional recheck. Do not charge publication twice. Keep pre-acquisition B rejection as install-budget/request-rejected, and an unexpected later reservation failure on the existing operational Budget route. Make CI-T26 assert both the argument split and the exact route.

### CI-R3-NBO-2 — Do not equate unconfirmed name durability with guaranteed absence after a crash

`docs/implementation/m3/component-install/PROPOSAL-r3.md:168`.

The sentence stating that a name not durably published is absent after a crash is stronger than the selected primitives establish. If the rename occurred but its parent barrier did not complete, the name can survive or disappear. The immediately surrounding uncertain-publication handling and three-way restart verification already provide the correct fail-closed behavior.

Suggested change: Say a rename whose durability was not confirmed may be absent or present after restart. Retain the existing full-verification requirement and all three restart outcomes.

## Requested dispositions

1. **R2-RF-1 resolved.** The private stage is a prefixed sibling directly under the store; publication and its final parent barrier address that same store. Generation lookup admits exactly 64 lowercase hex digits, excluding stage names. GC owns bounded fenced census/removal of inert siblings, never resumption or adoption. CI-T19 and CI-T23 cover the corrected layout. No cross-parent raw rename is selected.

2. **R2-RF-2 resolved.** V1 verifies archive metadata, structure, link text, bytes and staging modes. V2 verifies final modes, association record, pin state and unchanged path/type structure before publication. Neither constructs RetainedTree; the production constructor remains strict. CI-T24 names a successful nested installation and the relevant pre-rename failures.

3. **R2-RF-3 resolved as a law-level ordering and implementation obligation.** File and record final chmod precedes P-3; pin.lock is explicitly created empty at 0600 and barriered. Directory final chmod precedes its barrier, deepest first, including tree/, followed by the stage-directory barrier. P-1 through P-4 explicitly assign the missing native mechanisms to CI-2/platform, including a standalone file barrier rather than misuse of the existing whole-buffer writer. CI-T19 covers metadata changes, barriers, V2 and rename/parent-barrier prefixes. These are owed implementations and controls, not evidence they already exist or passed. Their prices must be included in the corrected recipe (RF-1).

4. **R2-RF-4 and LD-CI-13 accepted.** LostRace now ends the act with operational-failed/4, EXTENSION.INSTALL_IO_FAILED and extension-install-io; NotPerformed also ends it. No winner verification, ledger reset, retry, replacement or implicit cleanup follows. Only a later explicit operation may take the ordinary preexisting-generation no-op. CI-T25 covers this boundary.

5. **R2-RF-5 partially resolved; LD-CI-11 needs the remaining recipe correction.** A deterministic conservative B is the right replacement for an exact execution prediction, and comparing it with remaining allowance is appropriate. Reserving the complete publication suffix before rename and using reserved helpers addresses the previous post-rename budget hazard; NBO-1 clarifies the API split and routing. Post-rename barrier/recheck failure is now correctly publication uncertain, with no rollback or claim that no name became visible. CI-T22/CI-T26 express appropriate pre-rename exhaustion and funded-suffix obligations, but B omits required terms (RF-1).

   **LD-CI-12 accepted.** The installer does no cleanup; errors latch the existing ledger, and stages remain inert for GC. This avoids unfunded cleanup or ledger resets. **X-CI-1 is adequately owned/dispositioned:** the lead as DR-103 delivery owner owns the sourced-profile decision before first-party release qualification. Interim snapshot_profile reuse remains a finite selected policy, not census coverage or qualification. R10a’s separate D4/J1 profile remains independent.

6. **R2-NBO-1 resolved.** Authenticated modes remain in retained manifest/TreeCommitment evidence and archive-header comparisons. The closed generation.json association record is unchanged and claims no mode fields.

7. **Round-2 LD-CI-9 pin points addressed at law level.** R10a and ER10a take pins under their respective fences. Reads open existing pin.lock no-follow, never create or recreate it, and reject absent/non-regular/nonempty/wrong-mode pin state as Pin. Close-on-exec prevents pin inheritance through component execution. The returned capability owns the shared pin through the handoff; GC uses an exclusive non-blocking probe, busy meaning retain. Pin calls are explicitly charged, with their complete descriptor/state-check costs still belonging in RF-1’s reader recipe. Verified transfer, sink commit gating, Run-owned preimages before origin release, and independent retained-Run replay remain preserved.

8. **No other regression identified.** The full authenticated TreeCommitment remains the structural authority, generation.json remains association only, and extras/missing/type/link/mode/length/digest failures retain their causes. Owner-only usable modes and no symlink chmod are preserved. The no-follow offline regular-file source, same-octet profile-1 digest rule, closed platform-token lookup, bounded hostile archive parsing, pinned narrow PKG-AP adoption and 15 separated codec controls remain intact. The no-trust-view core path, RTC committed-Run authority, X-8 required-cell gate, and prohibition on placeholders, dropped cells or ephemeral detail remain explicit. Refuse-never-repair, fixture predicate, unchanged trust/signing authority and excluded network/update/migration scope remain intact.

Acceptance requires completing the published cost derivation and its control obligations. It does not require executing a prohibited implementation lane for this law review.
