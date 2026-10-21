# D2b-4a r2 independent review

## Verdict

**ACCEPT-UNIT**

The frozen 20-path Rust3 receive unit satisfies the accepted D2b law, PLAN-r3, A1, and A2 boundaries. Those authorities already select contextual receive admission and the base Rust3 subject-count rule, so this correction requires no new design selection. This verdict accepts this code unit only. It does not establish integration, inventory v236, descriptions, status publication, push, or product qualification.

## D2B4A-R1-RF-1 disposition

The R1 finding is closed. Each requested key now retains a checked `u64` count of its immutable host stage's `analysisDomain.subjects`. The shared echo check compares that count with `examinedUniverse.subjectCount` for ordinary `CoverageV3` and stage-major terminal `Unavailable` and `BudgetExhausted` entries. These comparisons occur before response accounting, P3T admission, retention, or publication.

The corrected control uses distinct stage counts of one and two. It supplies six valid cases and 18 well-formed forgeries spanning both stages, all three coverage-bearing frame kinds, and values zero, expected plus one, and `u64::MAX`. Each forged frame has a recomputed valid outer received-entry commitment, so the refusal is attributable to the subject-count echo rather than stale commitment bytes. The refusal assertions cover the admission result, latched refusal, unchanged public totals, unchanged phase, unchanged retention, and refusal of a later valid frame. The compiled guard-removal mutation establishes that this control observes the intended production branch.

The preserved evidence correctly treats the first R1 red attempt as invalid evidence because duplicate subject paths caused earlier schema rejection. The replacement red evidence uses the old receiver with the corrected test and observes all 18 missing-guard publications; the green evidence refuses all 18. Only `receive.rs` and `receive_tests.rs` changed from the rejected R1 subject, and the other 18 product paths remain byte-identical.

## Complete-unit assessment

I independently checked the frozen manifest and product map: all 772 members reconstruct with their declared hashes, all 20 candidate files match the frozen product bytes, their 10-existing/10-new classifications are correct, and the candidate and current product parent are the requested `82be07e21dedefb2bd928339ce22c88e97db21ff`. The parent advance from R1 changes only the separately accepted CLI creator test guard and does not alter this receiver, its schemas, dependencies, or authorities.

The receive path preserves strict profile proof; closed envelope, payload, direction, sequence, and depth admission; immutable host context; startup, Hello, Seal, native, optional-token, and cancellation echoes; stage, ordinal, batch, candidate, relation, anchor, and occupancy correlation; normal and terminal coverage admission; received-slice commitment and provenance checks; the joint ProviderFault window; full response and wrapper-spool accounting before allocation and publication; retained RPP/T016/T020 checks; actual table events; and all 13 generated worker conversions.

The archived boundary evidence covers the maximum frame, relation, and batch limits; all 32 fixed limits; seeded 1 GiB and one-million accounting edges; all seven commitment rows with 21 domain/class/order substitutions; the pointer/provenance control against re-encoding; and the source-derived 936-credit coefficient over the exact 16 selected roots. The 11 compiled receiver mutations each fail their intended control and restore all 20 source pins before the positive run. The completed paired evidence records 318 component tests and 86 identity tests for the candidate, against 270 and 81 for the accepted base, with empty failure sets.

The complete workspace evidence also preserves two failures outside these 20 paths: the inherited doctor source guard and the platform library descriptor abort. They are neither repaired nor accepted by this verdict. Their preservation, attribution, and continuation under the no-fail-fast run do not invalidate the isolated passing evidence for this unit.

Sender, scheduling, and participant work remains in D2b-4b. FA2, reference scope, successor vectors, replay, and raw-float work remains in D2b-4c. H/C4 admission, production wiring, source39, platform, privacy, owner work, and full product qualification remain open. These are scope boundaries rather than defects in this frozen D2b-4a unit.

## Findings

None.

## Non-blocking observations

None.
