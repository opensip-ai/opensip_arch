# J1 successors S2–S6 — Codex review r1

2026-10-04. **ACCEPT for each of the five pinned law subjects.** No required findings, non-blocking findings or batch findings. `noAcceptedOutcomeChanged` is true for each law, judged apart from its declared amendments as REQUEST.md requires. The machine-readable verdicts, subject hashes and preserved snapshots are in `review.json`.

All 23 supplied pins match. Each diff base matches its accepting review: X1's preserved r1 includes the specified acceptance sentence; removing only that sentence gives Grok's accepted subject (`e47aff459a26d99b30faaf5380739987091c764cb3b7700ae71631dab860839b`, 8,758 bytes). J1 r5, X3d r9 and J-RW r4 also match their accepting reviews. I reviewed all 18 unified-diff hunks and the relevant pinned law and product passages. The seven cited product files at `d2c00a96c3136fe45b901bc067b6d0ca51f0c9c1` are byte-identical to their J1 base `3e64266` versions.

Read-only source, diff and hash inspection only. Scratch Python used `-I -B` at nice 19, with HOME and TMPDIR isolated inside this review directory. No tests, builds, Cargo, matrix runs, lead sets, delegation, repository writes, commits or pushes. The real OpenSIP home and the private 413 fixture were not accessed. All review output is under the requested directory.

## S2 — Existing-root admission, 468 r6

**Verdict: ACCEPT.** Subject: `docs/implementation/m2/existing-root-admission-468/PROPOSAL.md`, 20,223 bytes. SHA-256: `93f4d0145104c9b92850cf9f289527f6846aa7b41454febdc43b01b1dff94dca`.

Items 1, 2 and 6 carry J1 r5 item 3 and successor S2 faithfully (J1:259–267, :279, :847; subject:42–58, :95). `Published`, `LostRace` and `NotPristine` end the creator act. Attempt A, its core and its platform are dropped; that act enters no gate. Attempt B runs X1's ordinary admission with fresh producers, both receipt rechecks and the one process gate. Its platform lends the existing three-part capability. No standing, observation, lock or receipt from A authorizes B.

The value-only `created` record has the correct provenance and lifetime: the act's typed result supplies classification and disclosed target, and every later success or refusal retains it. LD6-1 correctly chooses `Some` for a post-rename budget failure. The product marks a successful publication at `installation_publication.rs:277–285`, wraps subsequent ledger failures in `AfterRename` at :370–376, and preserves their budget row at `installation_routing.rs:458–461`. J1:264's performed-rename criterion and J-C6b at :328 govern irrespective of that row. LD6-1's `None` for an indeterminate rename is also sound: the act returns before its success mark (:377–382), so its result cannot establish publication. It creates no positive assertion from an existence scan or the minted intent. The required pre-effect stderr notice remains the disclosure of intended creation.

LD6-2 correctly treats S2's “item 7 landed by S13” as an assigned successor, rather than evidence that the carrier has already landed. Subject:98–100 keeps the owner's deferral, names S13/J-BS and J3d, retains stderr, and repeats J1's `backupStatus`/`firstUse` presence relation (J1:697–704, :708–716). M3-PLAN r9:265 still requires J-BS's own ACCEPT-DESIGN-UNIT review. Declaring the carrier already implemented would contradict that gate; retaining the old CLI-only target would miss J1's M3 emitter.

The route and result changes belong to J3a (subject:14, :50; J1:881). Apart from the declared route, capability-source clarification, continue-row wording, deferral record and forbidden substitute, the accepted r5 body is preserved. The failure rows, public codes, classes, exits, details, subjects, remedies, gate order, custody predicates and budgets are unchanged. Preserved snapshot: `docs/implementation/m2/existing-root-admission-468/PROPOSAL-r5.md`, 11,373 bytes, SHA-256 `0959e3083f95841783d39d3d299960000b556d95ebbea18b8f237cefc8d5ccf7`.

## S3 — Ordinary platform owner, X1 r2

**Verdict: ACCEPT.** Subject: `docs/implementation/m2/ordinary-platform-x1/PROPOSAL.md`, 16,772 bytes. SHA-256: `1d03e1f7b38438b32d821de9235a15704dc5b17945e08d9380f162d47c8f9ef3`.

Items 1 and 7 implement S3, including its ephemeral clause (J1:247–262, :280–284, :442, :453, :848; subject:48–58, :87–98). The durable entry probes before sealing a receipt. `Present` seals A as Write and runs X1 item 2 steps 2–4; positive absence uses A's producers unsealed for the creator act, followed by B's ordinary admission. The entry produces no Read receipt and permits no purpose conversion or intent minted through a receipt. The read entry remains lawful with a session, or without one when I is positively absent.

LD2-1 preserves at most one receipt on every route. Steady state produces A's Write receipt; successful first use produces only B's Write receipt; a refused creator act produces neither a receipt nor a continuation token. Read entry uses the one Read receipt. The changed reason is necessary because the first-use sequence has two attempts. LD2-2 correctly replaces the M2 `run_initial_creator` composition as the Creator class's entry while keeping that function private and defined once as J-C1 requires (J1:185). Listing both entries would retain J1's rejected unconditional intent/creator route. LD2-3 is a necessary, limited correction to item 2's adjacent “route unchanged” sentence: both receipt rechecks must also bracket B's gate.

The two-slot rule preserves J1's budget and receipt constraints (J1:281–283, :303–309, :319–320, :942). B requires the non-Clone `CreatorActEnded` token after exactly the three permitted results. Other second allocations and every third allocation remain `Invariant`; a refused act permits no B. A is dropped before B; no receipt or authority is reused. Each attempt retains its own ledger and the gate retains its separate ledger. This is the expressly authorized sequence of distinct acts, with no retry or branch-local budget reset. Current `read_premise.rs:331–345` returns a Read receipt; the proposed unsealed producer stage is a J3a implementation obligation, not permission to convert that receipt.

Subject:106 assigns the new entry and allocation/token changes to J3a. The purpose types and lendings, item 2's steps, standing, budgets and refusal mappings are preserved. Preserved snapshot: `docs/implementation/m2/ordinary-platform-x1/PROPOSAL-r1.md`, 8,796 bytes, SHA-256 `d747adf076b698a053748dc52ee1e2e61d4ddbbf6643b6e298a0049bd5dcfd5d`, including its unchanged acceptance sentence.

## S4 — Creation ingress, 464 r3

**Verdict: ACCEPT.** Subject: `docs/implementation/m2/creation-ingress-464/PROPOSAL.md`, 12,481 bytes. SHA-256: `e0803ad9f1cc3b2f8a699f3bb7a739d056ee8df2495b17795e232674a3e9fbf3`.

Items 1 and 5 carry S4's lent RequestId and pre-P0 ExecutionId reservation exactly (J1:190–218, :288, :849; subject:42, :48, :61–66). The host reserves the invocation's sealed `RequestIdentity` before parsing, lends it to security, and the intent draws no second RequestId. P0, the envelope and operational records retain that same invocation identity. `mint_intent` reserves the prelude's own CSPRNG draw before P0 staging and holds the sealed `ReservedExecutionId`; P0 accepts only that type or its read-only projection.

The prelude uses the same process-custody `ExecutionIdReservations` and collision rule as X3d r9 S10.1: check every reservation, at most eight draws, the drawing owner's existing host-I/O row on draw failure or exhaustion, and no release or reuse (X3D9:486–493; J1:205–213). Its reservation remains distinct from the durable attempt row. The prelude is never bound to the analysis session, so the prelude/session/render distinction in J-C4b holds (J1:242). A prelude reservation already present at R10a does not violate that row's ban on drawing an analysis-attempt id (J1:365).

LD3-1 is necessary and correctly bounded. The old “no ledger before I” and empty-P0 uniqueness argument cannot satisfy J1's pre-use, process-wide reservation rule, which explicitly rejects a bare draw or budget charge as a reservation (J1:225). The replacement names process custody, retains the cross-process 128-bit limit, and keeps the winner's initially empty durable ledger as a fact rather than the uniqueness proof. `request.rs:28–41` supports the cited eight-draw discipline; `initial_installation.rs:591–599` supports the existing security-owned draw.

Subject:81 assigns these changes to J3a, agreeing with X3D9 S10.8 (:562–565). Eligibility, constant UNKNOWN classification, delivery before effects, storage-choice refusal, StepId 0, existing conflicts and forbidden substitutes remain unchanged. The StepId and loser-route sentences are preserved inside the rewritten item 5. Preserved snapshot: `docs/implementation/m2/creation-ingress-464/PROPOSAL-r2.md`, 6,709 bytes, SHA-256 `a940ba5015e99507293af73256fda9bfb5ec67b7dc28303cd1cfed64008e19c8`.

## S5 — Store endpoint admission, X3a r6

**Verdict: ACCEPT.** Subject: `docs/implementation/m2/store-admission-x3a/PROPOSAL.md`, 19,705 bytes. SHA-256: `cb2132614b469e9bd3f04f08c6175ba5c13acb0275da410718703d32da866e8a`.

Item 2 carries J1's consequence precisely: store work belongs to a separately admitted ordinary write operation, either a later invocation or this invocation's B (J1:285, :850; subject:58–67). The creator act itself still has no endpoint and enters no gate. B's endpoint comes from its own `OrdinaryWriteAdmission`, an already-listed producer, with its newly observed selected core. No creator closure is promoted or carried through `route`.

LD6-1 correctly amends the adjacent sentences that otherwise deny this same-process route. The old invocation-wide prohibition, old 468/X1 constraints, X11 termination instruction and rejection of a second attempt all become false under J1:260–270, :279–283. Updating them within this one paragraph is necessary; leaving them for another revision would contradict the newly inserted consequence. The second-attempt rejection is explicitly withdrawn, while the rejection of carrying creator core values remains. Endpoint retention, rechecks, chain limits, joins and admission itself are untouched.

The record about B's commit agrees with 464 r3 and X3d r9: `open` draws and reserves its own ExecutionId, never the prelude's (subject:63; X3D9:486–493; J1:223, :242, :365). It adds neither an endpoint producer nor X3a-specific code. Any route code belongs to J3a (subject:15; J1:881).

All text outside the declared creator paragraph and revision header is preserved, including public mappings, budgets, units and forbidden substitutes. Preserved snapshot: `docs/implementation/m2/store-admission-x3a/PROPOSAL-r5.md`, 14,850 bytes, SHA-256 `310197d33f4851eb0c198073e2516a6ea14192cebde751f64a0861f5f98f8ba3`.

## S6 — First trust acceptance, X4B r6, with RW-S5's record note

**Verdict: ACCEPT.** Subject: `docs/implementation/m2/trust-bootstrap-x4b/PROPOSAL.md`, 27,900 bytes. SHA-256: `c8c541544d7e48d8deea4fa7bf3f79c387bda2fd97fb08bc1d479fb402ed4991`.

S6 is faithfully confined to the rejected creator bullet and forbidden substitute (J1:286, :851; subject:90, :212). Acceptance is forbidden in the creator act. On first use B is an ordinary writer, so its fenced first read reaches the existing lazy trigger. The monitor, clock sample, single confirming admission, payload, transitions, pointer ordering, rows and budgets are preserved. J1's route places that read at R10 (:348); the route code belongs to J3a (:881).

LD6-2 is sound with the interpretation it expressly records (subject:41–43). Item 1's first bullet names `admit_ordinary_writer`, but its material precondition is the returned `OrdinaryWriteAdmission` with the fence held. On steady state J1's durable entry seals A and runs the same recheck/gate/recheck steps, producing that same admission (J1:256; X1 r2:54). It adds no alternative store or trust authority and bypasses no admission check. The unchanged function-name wording does not require the steady-state path to run a second producer or gate.

RW-S5's separate record row and notes are faithful to accepted J-RW r4 (JRW:242–246, :373–415, :683, :705–708; subject:151, :157–161). C-TRUST completes only the missing canonical suffix at a name this publication writes, with the specified ACL completion first. It neither rewrites an admitted record nor visits unrelated torn leaves. C-TDIR concerns only permitted `may_create` parents, including `trust/objects`, with the empty/private crash-prefix predicate and barriers. The references import J-RW's complete predicates and actions, including native-open success, retained-handle checks and read-back; the short record is not an alternative completion algorithm. Nothing is deleted.

LD6-1 correctly combines S6 and RW-S5's record because both accepted sources explicitly name X4B r6. It does not absorb X4T's rule amendment. The header and item 6 leave that rule to X4T r13 and its code to J4d, which waits for that successor (subject:25–26, :161; JRW:683). X4B decides no new narrowing of incomplete rows, completion predicate or clocked-path outcome. Those remain J-RW/X4T's and are not accepted as implemented here.

Apart from these declared amendments and their record, accepted r5 text is preserved, including the no-deletion rule and all public outcomes. Preserved snapshot: `docs/implementation/m2/trust-bootstrap-x4b/PROPOSAL-r5.md`, 21,552 bytes, SHA-256 `97c2eef3f0ad374b2004ce31d0c34fc593cba5de321f926cfe2d83aff77229a3`.

Across the batch, the references resolve consistently: 468 supplies the A/B boundary and value-only creation result; X1 supplies fresh B admission and the one-receipt/two-slot exception; 464 supplies the invocation identity and separate prelude reservation; X3a admits B's endpoint; X4B accepts only at the ordinary writer's fenced read. All S2–S6 assignments are covered. Necessary adjacent corrections are declared and confined to their own contradictory sentences. No additional public code, class, exit, detail, row, subject or remedy changes. Acceptance covers these five law subjects only; J3a, J-BS/S13, J3d, X4T r13 and J4d retain their own acceptance gates.

Evidence files: `pin-verification-initial.json`, `pin-verification-final.json`, `snapshot-acceptance-checks.json`, `preservation-audit.json`, the five law `.diff` files, `product-source-pins.json`, `product-base.json` and `artifact-validation.json`. Source snapshots are under `arch-pins/` and `product-d2c00a9/` in this review directory.
