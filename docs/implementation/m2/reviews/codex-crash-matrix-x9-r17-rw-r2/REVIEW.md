X9 r17 round 3, §RW, correction review r2: **ACCEPT**. X9-RW-RF-01 is closed; there are no required findings.

Codex is the single reviewer; Grok is the implementation lead. The subject is docs/implementation/m2/crash-matrix-x9/PROPOSAL.md, 332508 bytes, SHA-256 312f4de06b968d5a788672bf139f192748eca6dde819d3f4b27a856dd8ae553e. The previous subject is the request's PROPOSAL-r1-subject.md, 332138 bytes, SHA-256 118a9a9835933da722691d1477a3f574e7ffd9deca73f7c21af7c6217c581aff. The accepted S12 diff base is 278697 bytes, SHA-256 6b208ccf7d1b0ce5c18ec0329724fbc103de8b18d9abae0b02a6ac0856f397f3. All seven supplied pins match.

**Finding closure.**

RW.3 at line 2245 now says J4a's two repair start states add four census point names, each occurring twice: eight durability events and eight kill-set points. RW.7's J4e census gate at line 2523 repeats that same four-name/eight-kill-point delta. Two before/after names for RW-K4 plus two for RW-K7 give four names. For n=2, first/middle/last sampling selects #1 and #2, giving eight kill points. The eight RW-K4/RW-K7 rows stay unchanged.

Other units contribute only the names their own censuses add. The correction therefore fixes both the mistaken prediction and its dependent gate without inventing a total for unimplemented units or changing any row outcome. X9-RW-RF-01 is closed.

**Unchanged scope and decisions.**

The complete r1-to-r2 comparison changes exactly three lines: the round heading at 2141, the prediction at 2245 and the J4e gate at 2523. Every other line is identical, including row identities, expected objects, scripts, scope names, completion rules and LD-RW-1 through LD-RW-11. The r1 row-faithfulness and lead-decision assessments stand on unchanged text. No new disagreement was found.

Against PROPOSAL-r17-S12.md, the diff retains exactly the three declared hunks: the prior round's acceptance note, the existing NBO-1 arrivalPhases citation correction and the reserved RW section's replacement. No other r17 section's row changes. NBO-1 remains record-only, with the same A–E/O spelling and expected values.

**Carried nonblocking notes.**

X9-RW-NB-01 remains nonblocking. The unchanged release-absence explanation overstates the checker's explicit string list; r1's registered-prefix coverage and feature-disabled macro assessment still applies. The correction changes neither that passage nor its premise.

X9-RW-NB-02 remains nonblocking. LD-RW-11's unchanged deferral of L11 reason narrowing is still a conservative recording-policy refinement to carry into the owed J-RW revision. Its retirement gate remains unchanged. Neither note becomes false or a new required finding because of this correction.

**Validation and boundaries.**

Validation used read-only hash checks, full text comparisons and in-memory arithmetic. Python used /opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B at nice -n 19. No product execution or evidence rerun was needed.

Only review.json and REVIEW.md were written under /tmp/opensip-implementation/reviews/codex-crash-matrix-x9-r17-rw-r2/. The preexisting PROPOSAL-r1-subject.md there was preserved. The r1 review files were hash-checked before and after writing and remain unchanged; their REQUIRED-FINDINGS verdict stays attached to the original r1 subject.

No repository edits, commits, pushes, delegation, Cargo, lane-lock access, crash-matrix run or build/test lane occurred. The real OpenSIP home and private 413 UUID fixture were not accessed. This accepts the corrected law; future J4 traces, measured census totals and lead sets remain implementation gates.
