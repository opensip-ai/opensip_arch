# X12 r4 — ACCEPT

Subject: `docs/implementation/m2/policy-admission-x12/PROPOSAL.md`, 39,363 bytes, sha256 `adc9a88aed18fe55c45255a4d40ba4e85a29082b3d7ff4fab6beded4c5fd23e3`. Preserved r3: `PROPOSAL-r3.md`, 26,705 bytes, sha256 `11628912f6bb63de9c8255178f2b5833163179f114b6f7a563c32871d34822ff`. Read-only. No cargo. `~/Library/Application Support/OpenSIP` was absent.

Law amendment required by accepted M3-B r2 item 10 (successor S2), plus the marked first-use lead decision. M3-B's accepted quotes are in `PROPOSAL-r2.md` (`92e65825…`); the live M3-B file's two quoted paragraphs match those bytes.

## Decisions

**1. Item 8's new opening is S2's text, and X12:132-138 stands.** The format reconciliation holds. S2 writes `**8. Order: …**`. r4 writes `8. **Order: …**` and indents the withdrawal paragraph under item 8. After that format change, both paragraphs are byte-identical to M3-B item 10's quotes. The two passages marked "r4, lead decision" sit where the header places them: the first-use clause after S2's first paragraph, and the dependents immediately after "I1:383-386, stand."

r3 lines 132, 134 and 138 are unchanged (r4 lines 206, 208 and 212), including `AdmittedPack` as the Plan builder's only policy source and the rejection of admission inside Plan construction. r3 line 136 keeps its words. The r4 note is appended to that sentence.

**2. The first-use clause is sound.** The gap is real. 468 r5 item 1 ends the creator act on `Published`, `LostRace` or `NotPristine`, then continues through the durable write gate with a fresh installation fence. X2 r9 item 3a reads each carrier only after that fence, S3's selection walk, the placement check and the chain walk. X2:68 and X2:74 are r8 lines: selection stays S3's, and a project-root admission is produced under a held fence. On the creator route, pack admission cannot precede the creator's installation writes.

"Project-scoped effect" is closed by the list that follows it: registration (X2 item 6), any lease (X2 item 7), the project ledger and journal, and every later project effect. The creator's installation effects are the preceding step, which 468 item 1 already requires and which 468 does not extend to project leases or first registration. The control keeps that bound: a complete installation, and no registry row, namespace, `.opensip`, marker, lease or journal. On every other route, S2's "before any effect" stands as written.

"Nothing to clean up" remains true at project scope. X12:132 is unchanged: no core evaluation, no `policyOutcome`, no facts or Coverage consumption, and no semantic universe. A refused pack on first use leaves the creator's empty, valid installation. 464 item 3 already flushed the first-write disclosure before the first creation effect, and the refusal discloses that creation. There is no project row, lease or journal left behind. DR-G24 at `08-decision-and-readiness-register.md` line 369 still matches: pack-identity refusal before evaluation, and no waiver that would hide the refusal.

The clause follows 464 and 468. 464 item 3 places the disclosure before installation effects, which the third first-use bullet records. 468 item 1 places the creator's publication before the fresh fence, and pack admission follows that fence, the selection walk, the captures and resolution.

**3. The dependents are handled correctly.** X11 r1 item 1 gives four reasons, each sufficient on its own, for keeping `opensip`, `analyze`, `fit` and `audit` refused in M2. Item 1a is the order reason ("Creating I first would break item 8's order"). Reasons b, c and d sustain that M2 decision on their own. Routing item 1a's conflict with the first-use clause to the X11 successor that M3-J1 owns leaves X11's accepted M2 decision in place and names the reconciliation the successor has to write. X11's file stays as accepted.

I1:404 says "J2 calls `admit_policy_selection` first (X12:125-132)." The marked dependents passage records that J2 calls it in r4's order. That is the same method I1 used when it amended X12 by statement. S2's own withdrawal paragraph, byte-identical to M3-B, withdraws the clause "the order" from I1:388 ("Everything else in X12 r3 stands: rows 1 to 4, the order, …"). I1:383-386, the three row-count changes, and the rest of I1:388 stand. I1's file is not edited. X12:67, X12:160 and X12:169 are outside the diff, so those amendments still read on identical text.

**4. The X12:136 note and the reconciliations match M3-B, r3 and X2 r9.** The note says what M3-B item 10 and GROK2's r2 review already fixed: "it is pure and runs before any custody" means admission itself performs no custody, because S3's selection judgment precedes it; the ordering sense is superseded; the correction that X12 does not depend on X1 stands. X12:170 is unchanged: the refusal paths reach no evaluation, provider, facts, Coverage or custody call. The custody that precedes the call is S3's selection, which is not on `configuration.rs`'s refusal path. GROK2 r1 R2 is the basis the header cites: `ObservationSession::begin` and `DurableWriteGate::begin` write no registry row, RESERVED document, lease or journal.

X2 r9 item 3a runs item 2's placement check and item 3's chain walk after S3's selection and before the carrier reads. S2's "immediately after S3's selection walk and the configuration carrier captures" therefore means immediately after the captures. Both checks only read, under the fence. Pack admission still follows resolution and precedes X2 item 5.

"S3" in S2's text is the security contract's S3 (X2:68). In "(registration, item 6; any lease, item 7)" the items are X2's, as the preceding "X2 item 5" says. AQ:47-52 is §1.1's policy section, "registered pack/waiver IDs", which is Config2's `policy.packIds`. The forbidden-substitute "Order" bullets are byte-identical to r3 and still forbid admission after any provider spawn, snapshot, facts consumption or evaluation. r4 adds no bullet. On the first-use route, M3-B item 10's "effect" means a project-scoped effect.

**5. r4 changes nothing else in r3.** The diff has four sites. The title becomes r4. The header paragraph gains the sentence "r3 ACCEPTED by Grok on 2026-10-01." and is followed by the r4 header. Item 8's opening replaces r3 lines 125-130. The r4 note is appended to r3 line 136. Units after the law, the forbidden substitutes and "Not claimed" are byte-identical to r3. No public code, row, detail or remedy changes.

## Required findings

None.

## Non-blocking

**NBO-1.** The r4 header says row 1 of the order table in M3-C's draft still carries r3's order and will be updated in M3-C's next revision. The live `docs/implementation/m3/snapshot-plan-c/PROPOSAL.md` is M3-C r5, accepted in review by CODEX2, and it takes effect once M3-L and X12 r4 are accepted. Item 16 rows 1 to 4 already follow this order, including the first-use clause. Row 1 is X2's fenced selection, placement, chain walk and carrier captures. M3-C r5 also says that if this review changes r4's order, those rows follow the accepted text. The header sentence describes the table M3-C r2 had. It withdraws nothing and binds no behavior in X12.
