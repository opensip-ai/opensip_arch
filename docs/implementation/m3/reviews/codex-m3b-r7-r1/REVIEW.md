# M3-B-r7 review

Verdict: **ACCEPT**

Required findings: none. Non-blocking observations: none.

Independently verified `subject.json`: 440 bytes, SHA-256 `fa285053e588e1a0713deb307e94f9dc343565a60cdb4909862f9f203ab6e737`. Rehashed its sole member, `docs/implementation/m3/config-discovery-b/PROPOSAL-r7.md`: 119,707 bytes, SHA-256 `7e0e214fc2cf20e466a3390298d591da7ca7cc11739f0ce39cc94d4742d071af`.

Product main is clean at `79c816096310711663104a5e9217717718f8f510`; architecture is at `230c7df884a5584911aab0daf9af03369fd5cb78`. Compared the full candidate directly with the live, committed r6 law. Apart from the revision title/banner and new r7 recording section, exactly two inherited law lines change: item 12's caps bullet and the matching Not claimed line. The storage requirement, cap-selection rule, member-bound requirement and held-out gate are unchanged. This records the result of an accepted rule and makes no new policy choice.

Verified the bound B2-b3d r2 unit's accepted review and subject pins at the architecture base. The ACCEPT-UNIT review binds the exact subject manifest; its pinned product map binds the census bytes currently committed in the product. The product census SHA-256 is `1eda34ef8048061cf0b680e9c955676d21dfcf6adbd8f2b4fb405cc69c7c50a2`. Inventory v198 is bound; the product lock contains 158 inventory successors and 164 contract successors.

Independently parsed all 39 lead-readable repository rows and five workspace rows. Their maxima are exactly those recorded by r7, each attained by `rs-very-large-aws-sdk-rust`:

| Dimension | Maximum | Twice maximum | Smallest qualifying power of two |
| --- | ---: | ---: | ---: |
| Objects | 1,476,438 | 2,952,876 | 4,194,304 (2^22) |
| Edges | 1,007,224 | 2,014,448 | 2,097,152 (2^21) |
| Bytes at R=4,096 | 358,480,897 | 716,961,794 | 1,073,741,824 (2^30) |

For each dimension, the selected power meets twice the maximum and the preceding power is short. The byte formula is exactly `358,476,801 + 1 R`. Actual cap/maximum ratios are approximately 2.840826, 2.082111 and 2.995255. The displayed 2.84×, 2.08× and 2.99× are conservative two-decimal downward truncations; all exceed 2×. Every lead-readable repository row meets the recorded caps arithmetically in all three dimensions.

Verified the accepted subject pins for the supporting lead-probe log and throwaway diff. All four successful native probe measurements exactly equal their corresponding bound census rows in objects, edges and bytes evaluated at the measured root length. This is supporting evidence already accepted with B2-b3d, not a new execution or qualification result.

Workspace rows remain walker-only until B3-b supplies its reviewed full-ledger member-observation bound. Both the r7 recording section and the updated Not claimed line retain that limitation. The inherited measuring bullet and held-out requirements remain unchanged; held-out margins remain outstanding. No full workspace or held-out margin is inferred from the numerical walker maxima.

This is law acceptance only. The product still has provisional constants 2^20 objects, 2^21 edges and 2^30 bytes; B2-b4b3 must separately implement the recorded caps and update its checks. No code, binding, product qualification or B2-b completion follows from this review.

Used only read-only reading, hashing, JSON parsing and Git queries. No Cargo, tests, builds, lane or network was run; no delegation or other panes were used. No private fixture, installation directory, signing keys, held trees or held-out entry was accessed. Neither repository, the stage nor control files was edited. Only `REVIEW.md` and `review.json` in the requested directory were written.
