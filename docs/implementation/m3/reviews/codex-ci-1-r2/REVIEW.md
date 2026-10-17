# CI-1 r2 review

**Verdict: ACCEPT-UNIT.** No required findings or non-blocking observations. Acceptance covers the pinned profile-1 codec unit only. It accepts no CI-2–CI-4 implementation, CI-A2 amendment, installation qualification or inventory successor.

## Subject and boundaries

Independently verified the 14,063-byte subject manifest, SHA-256 `7ca9cc207fa1ccf72acb6b4f868d7532b22912c088f452a2955e39d6c77a4771`, and all 61 members, including a final rehash. Checked the detached candidate at `01769e93db878836612d9e3d483a054f7ad1da94`, all four product-map candidate/archive pins, both edited parents, both new paths, source authority pins and the design-lock pin. The lock selects inventory v223 with 183 inventory successors and 176 contract successors.

Confirmed r2 is a mechanical rebase: the three non-lib candidate files are byte-identical to packaged r1; lib.rs is the current base plus exactly r1's same five-line, 206-byte append. The recorded pre-lane move from e770404 to 01769e9 changes only design-lock.json and no candidate path.

Ran only the expressly permitted source census and pure package scripts. Checker JSON was written temporarily to the permitted review.json path and replaced with this final verdict. No extra output file remains. No Cargo, rustc, build, test lane, shared lock, network, other pane or delegation was used. No prohibited fixture, key, installation, held tree, store, cache or held-out material was read. Neither repository nor the worktree was edited.

## Profile admission and length

The header builder matches PKG-AP's 17-field layout, zero fields, mode and size encodings, exact typeflags, magic/version and checksum algorithm. It computes the checksum with eight spaces and stores six octal digits, NUL and space. Admission compares every header octet, including terminator tails and reserved fields; it does not accept decoded-field equivalence. Differences outside chksum take reporting precedence over checksum differences, and a checksum-only difference reports Chksum. Re-checksummed noncanonical headers therefore still refuse at the relevant field.

ArchivePlan validates count, row text, strict full-path UTF-8 byte order and four profile capacities before providing a verifier. UTF-8 byte order agrees with code-point order for the admitted NFC paths. Matching header position to row position, exact body sizes/digests, exact pads and exact trailer establishes the member/row bijection. Missing, extra, reordered or substituted members cannot pass. No archive member name becomes an I/O path. Nothing is executed, decompressed or interpreted.

The length is exactly `512*N + sum_files(512*ceil(length/512)) + 1024`, accumulated with checked additions. The preceding count and file-size caps make the local padding arithmetic and length-plus-one safe: even the maximum tree is 858,993,510,401,024 bytes, below u64 and SHA-256's message domain. check_length provides the required observed-size comparison before reading; actual acquisition and read limits remain CI-2's responsibility. The stream refuses the first trailing byte, so a correctly driven reader needs at most L+1 bytes. Capacity tokens remain distinct from host Rows invariants and from work-budget failures.

## Streaming and emitter

The production verifier holds a fixed 512-byte expected header, fixed digest accumulators and scalar state. It allocates nothing proportional to either members or archive size. Body events borrow the caller's buffer. Header, body, padding and trailer progress survive arbitrary chunk boundaries, including empty files and exact-block bodies. File hashing excludes padding; whole-archive hashing includes headers, bodies, padding and both trailer blocks.

step consumes the verifier on every call and returns no verifier on refusal; there is no Clone or public constructor enabling continuation of that refused state. FileBytes are explicitly provisional until MemberEnd, which follows digest and pad validation. End supplies the whole-archive digest after the exact trailer. CI-2 must continue through input exhaustion, reject any trailing bytes, finish at EOF and compare the returned digest with the admitted artifact; End alone is not an I/O completeness or custody capability. The current API and controls support that contract.

The fixture emitter sorts rows by full-path byte order, checks payload keys for unknown/non-file/duplicate entries, validates every file's length and digest, and returns the exact header/body/pad/trailer representation. It returns the owned archive only after successful validation; errors expose no emitted archive. Both emit and EmitRefusal use exactly the requested joint fixture predicate.

The site-list extension is in the correct existing authority path: X9-1's crash_matrix_sites.rs pin, as X8 r3 item 4b specifies. Accepted plan LD-CIP-3 supplies this emitter's fixture-predicate selection; shared gate 6 records both sites by name and count, with no second list or widened predicate. The recorded release symbol check finds the codec's field_at symbol and no emit symbol; the scenario-fixtures positive control finds both. This corrects the earlier item-name check, which could confuse cfg-stripped metadata with code.

## Controls and recorded lane

The permitted live PKG-AP check passed all 12 checks, including the source digest, layout, capacities, refusal tokens and exact 15 CI-T1 case names. The independent Python encoder reads no Rust implementation and computes the pinned 8,704-byte, ten-member vector with digest `47fd5fd72177201dbe3aaff23ea649ead391e98d77dae6eb3391ac0ac16f6795`. Its tarfile cross-read passed live. Reviewed the recorded system tar listing and its successful lane row; no system tar was rerun during this review.

Reviewed all 28 new tests: the 15 PKG-AP cases, pre-read length and capacity controls, chunked events, truncation samples and boundaries, pads/trailer, PAX/GNU and prefix alternatives, octets after terminators, numeric alternatives, row invariants, formula, emitter inputs, layout and source pins. Mode-max and size-max are explicitly metadata-only capacity cases, not signed-installation positives. The truncation test samples cuts across the vector plus important boundaries; the implementation's finish condition covers every incomplete state.

Independently matched raw test-log failure names to the comparison record: security has 1,212 base versus 1,240 candidate passes, the identical 14 base-environment failures and equal suite counts. All 28 focused tests pass. This is equal-failure-set evidence, not a green full suite.

All 23 mutation logs contain the expected failing tests and no compilation failure. They cover the plan's five controls and the additional checksum, digest, capacity, order, length, trailer and emitter mutations. The length mutation disables the comparison; CI-2 must still verify the actual acquisition ordering when its caller is implemented.

Recorded warning-denied all-target Clippy, workspace all-targets check, both feature checks, release and fixture builds, release/positive symbol checks, ten environment-exception tests, operability, census-closure check and verify_design pass. The three base-clean/new edited files are rustfmt-clean; lib.rs is base-dirty and independently verified append-only. Lane metadata and runner agree on private 0700 TMPDIR, niceness 10 and lane ownership. These recorded operations were not rerun.

Checked r1's attempt history: attempt 1 stopped on the moved-main assertion; attempt 2 had the candidate-only unlisted-site failure, confirmed in isolated runs, and the invalid name-based release check. The explicit gate-6 list entry and code-symbol check with positive control address those defects. Attempt 3 at caa71e2 and the packaged r1 lane at 813d559 report all rows passed. This review is the first submitted review of the unit; no r1 acceptance is inferred.

## Receipts, CI-A2 and integration limits

CI-PT-4 passed live: 23 discovery-bound and 37 companion-bound product files, no candidate intersection, and all four public census/receipt files byte-equal to base. Checked the derived sets against receipt_bindings, companion bindings/sources and their constants. Caps, sizes and anchored sources are covered through their owning files. No bound product file, census tool or relevant reference source is changed by CI-1.

This is sufficient for the narrow claim that CI-1 leaves both receipts and their bound inputs unchanged. It does not establish current receipt freshness, recompute generated census outputs or claim either census --check ran. Avoiding those modes is appropriate under this review's cache boundary; SCOPE records the substitution and limits explicitly. The permitted operability source census passes 114 rows with no findings. The four-file diff adds no dependency, mint authority call, environment read or ignored-result pattern.

SCOPE section 7 correctly identifies the missing step-2 byte-order-index price. CM admits tree entries in arbitrary order, while the archive profile needs full-path byte order; CI-A1-b prices step 4's component-order index, which is different (`a-x` versus `a/b`). ArchiveRows' positional interface can borrow through CI-2's funded order index, and Rows/Order rejects a missing or incorrectly ordered index. CI-A2's pricing and controls remain a future CI-2 law-amendment review; this verdict does not approve them.

Two new inventory rows remain to be reviewed and bound after unit acceptance. Installer work charging, artifact acquisition and digest comparison, filesystem effects, failure routing, retained-tree authority and production composition retain their later owners.
