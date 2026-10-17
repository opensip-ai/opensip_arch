# S-OP-2c r1 review

**Verdict: ACCEPT-DESIGN-UNIT.** No required findings. One non-blocking observation. No product qualification or binding is implied.

## Subject and form

Independently verified the 1,001-byte subject manifest, SHA-256 `5aec6280e1bd463679b9b453d8af881c3ac7083875b255a1d63358a1b8ec8ac8`, and all five members. The four candidate pins cover exactly the subject except the successor record itself. The parent is exactly 130,001 bytes with SHA-256 `ce8d3a4b783328915f0bf550dd111f227aa9901d5efddbcd9ccc8707cd4cb11d`.

The line-881 override changes only `provider.process.reaped.signal` from Signal to ChildSignal. The line-894 override preserves the closing sentence and inserts item 23a after it. Its inserted passage equals the marked PROPOSAL text byte for byte. Supersessions are empty. The bound S-OP-2b override selects line 429 of the same parent; neither new selector overlaps it.

Ran the exact permitted checker from the architecture checkout: `python3.14 -I -B docs/implementation/m3/operability/s-op-2c/evidence/check_sop2c.py`. It exited 0 and printed **CHECKS-OK**. It read product sources at `5de9fd4740ea17018d0bd3fbff9496c94ddacda9` and the libc 0.2.189 archive, whose checksum equals Cargo.lock: `3eaf3ede3fee6db1a4c2ee091bf8a8b4dccdc6d17f656fb07896ee72867612f2`. It wrote nothing.

A successor is justified by the descriptor-table replacement and the explicit resolution of item 23's previously ambiguous meanings. Ordinary registration still owns the later code declarations, field additions and exact output pins; acceptance here registers no event in the product. The inserted text adds the five table definitions, their value/presence semantics and their provenance rules. It changes no SafeField kind, privacy class, provenance class, sink, bound, level, identity requirement or event name. The only existing descriptor-field table replaced is the declared signal field. All members fit K1's grammar and existing encoded bound.

## Source and member review

Independently inspected the underlying carrier records, generated enums, startup reason schemas, transition tables and relevant laws, in addition to reviewing the checker.

- StageKind is exactly `semantic-provider`, the operator constant of both Ts2StageRequestV1 and Rust3C2PlanStageV3. The generated enums agree. The rejected operation, Rust-only kind, language and span alternatives do not supply the same common stage meaning. This does not resolve the in-host syntax/inventory operators by inference.
- ProviderState is P3T's ordered 22-member phase list. T2O's sixteen are a subset; the six additional P3T phases are the dependency/prepared transfer triples. Both files explicitly say NORMATIVE and CLOSED and retain historical PROPOSED labels. The accepted D2b table-engine law and pinned product copies provide the relevant acceptance context.
- Signal is COMMON4 D9Signal: SIGINT, SIGTERM, SIGHUP, exactly as Common4D9Signal and OPP's received-signal policy state. This is a different vocabulary from child termination signals.
- ChildSignal contains the declared twenty POSIX named terminating signals common to the supported platforms. The checksum-verified libc constants match the printed mapping. Linux x86_64-gnu and aarch64-gnu agree for all twenty. macOS differs for SIGBUS (10 versus Linux 7), SIGSYS (12 versus 31), SIGUSR1 (30 versus 10) and SIGUSR2 (31 versus 12); all other printed constants agree. The common Apple constant sources cover macOS x86_64 and aarch64. SIGPOLL is absent on macOS and deliberately excluded. The implementation rule must compare target constants, not reproduce this numeric table.
- ProviderReason is the exact union of PreAnalyzeUnavailableV1's singleton, TypeScriptUnavailableV2's six and UnavailableV3's nine reasons: eleven distinct members. Architecture/product reason schemas and the generated enums agree. Pre-Analyze native-context-mismatch is included; fault kinds and budget dimensions are excluded. Future producers must use the reason actually admitted for that protocol and terminal, rather than treating union membership alone as payload admission.

The checker validates the listed POSIX subset against pinned libc; its POSIX default-action list is a literal input, not an independently fetched standards table. No network was used. The explicit excluded-number rule preserves the signaled exit classification for native signals outside the named projection.

## SOP2C-R1-NBO-1 — Qualify the ChildSignal rationale

**Location:** `PROPOSAL.md:76-79`.

The phrases “the observable set is POSIX's terminating signals” and “smallest closed set” should be qualified. Native signaled exits include the real-time and platform-specific cases the proposal itself lists at line 83; Linux SIGPOLL is excluded for portability. The platform's wait-status observation does not derive this twenty-member logging projection, and the checker does not prove an exhaustive observable set.

Suggested change: call it exactly the POSIX named T/A signals defined on every supported target, with minimality relative to that chosen coverage criterion. The normative list and explicit absent rule already define the intended behavior, so this wording observation does not block acceptance or require a smaller table.

## Rulings

**Q1:** Accepted. The two selectable protocols pin semantic-provider as their stage operator, so it is a sound common StageKind source. Operation is open, kind is Rust-specific, and language/span names classify different things. Syntax and host-inventory reuse records remain blocked until their own closed operator members are pinned and registered; they must not be mislabeled semantic-provider.

**Q2:** Accepted. The phase arrays are finite, ordered, pinned protocol vocabularies consumed by the host table engine. Both source documents explicitly say NORMATIVE and CLOSED, while retaining historical PROPOSED status labels; their authority here rests on the accepted D2b law and pinned vendored bytes, not the standing string alone. T2O has 16 phases, all in P3T's 22; the overlay adds no phase.

**Q3:** Accepted. An explicitly enumerated union of named pinned closed enums remains protocol-enum provenance; it creates no new provenance class. C-2 must compare the exact union and preserve each source binding. A TS2 event may use only an applicable T2O phase or admitted TS2 reason, even though the shared table has Rust-only members.

**Q4:** Accepted. D9Signal and its generated Common4D9Signal enum fit generated-contract provenance. The exact generated module output must be pinned when registered, as item 3 requires. Replacing only provider.process.reaped.signal's table with ChildSignal is an appropriate narrow successor; host.signal.received retains the three-member D9 vocabulary.

**Q5:** Accepted as the chosen portable registry-literal projection: the 21 POSIX named T/A signals less SIGPOLL give the listed 20 constants common to all four targets. No smaller set satisfies that chosen coverage criterion. Map using the target's pinned libc constants, never copied numeric values. Other terminating signals remain signaled with signal absent. This is not an exhaustive native signal vocabulary or a platform-proven minimum logging requirement; see NBO-1.

**Q6:** Accepted. The admitted pre-Analyze singleton and TS2/Rust3 post-Analyze Unavailable enums have exactly the listed eleven-member union. Reason is the admitted payload's reason and is present only for unavailable. Fault kinds and budget dimensions/units belong to their own namespaces and are correctly excluded.

**Q7:** Accepted. supervision.child.settled is D3's ordinary registration conforming to the three-segment grammar. Correcting M3-D's prose belongs to its next accepted revision; this S-OP-2 successor has no M3-D parent or override. No cross-law name change is silently bound here.

## Binding and remaining work

The record can bind directly after exact-subject independent acceptance and root substantive assent. Product base 5de9fd4 already binds S-OP-2-R, whose accepted candidates include the exact r6 parent, and S-OP-2b already uses that parent. No preliminary successor is needed to select it again. Before appending, the normal verifier must confirm the current chain, exact parent/candidate/manifest/review/assent pins and absence of an intervening overlapping override. The assent must identify these exact bytes and resolve or carry NBO-1 explicitly. If the proposal or record is revised, the changed subject requires its own matching review binding.

D3's next code unit still owns table and event registration, reader descriptors, emission and C-2 checks, including the generated module output pin for Signal. In-host StageKind additions and M3-D's name correction retain their stated owners. Acceptance does not mean the four events have been implemented or emitted.

Only REVIEW.md and review.json were written in the requested directory. No repository, worktree, control file or design lock was edited; no Cargo, rustc, build, lane, bind, network, prohibited private material or delegation was used.
