# B2-b4b1 r1 review

Verdict: **REQUIRED-FINDINGS**. One correction is required in the platform size test. No non-blocking observations.

## Exact subject

Independently rehashed the 7,466-byte subject manifest to SHA-256 `0d10c6b27c026b4420848dd4d910e990357a7d823e5614d3bac69a435103d465` and verified all 33 members' lengths and hashes. Verified all eight authority pins, the product lock and every product-map parent/candidate/archive byte set. The candidate changed/untracked path set is exactly the six mapped paths, including the one new platform test path. Both HEADs match the requested bases. Inventory remains v196, contract successors 164.

## B2B4B1-R1-RF-1 — Make the libc size check an exact integer check

Location: crates/platform/tests/discovery_census_sizes_tests.rs:41-43.

recorded takes the leading ASCII digits after the key and parses that prefix without inspecting what follows. For example, `"libc::stat": 144.5` and `"libc::stat": 144e9` both return Some(144), so the platform test can claim equality with a 144-byte native stat although the recorded number is different. The same acceptance path is used for attrlist and statfs. Duplicate-key detection does not address this token-boundary issue.

Required correction: check the entire unsigned integer token and require the following whitespace/delimiter to be valid for this generated sizes object, or use a strict integer parser for that object. Preserve duplicate rejection. Add focused controls for exact integers and fractional, exponent and prefix-only values.

The security tests parse both complete records with the CAN parser, whose integer parser rejects fractions and exponents. Therefore this finding does not assert that such changed records pass the full candidate suite, or that the current generated sizes are wrong. It concerns the explicitly requested independent platform whole-number assertion, whose implementation currently checks only a prefix.

## Byte-model assessment

Checked the modeled byte arguments against the pinned native charge sites. The model includes owned record overhead; root copies and scope entries; absolute spelling allocations; raw names including dot entries; listed name/path/validator copies; observation tuples; new observed-entry records; classification segment/target terms; directory/file names and status buffers; Cargo/listed/verdict records; frames and depth probes; named-root/spec/chain work; marker captures; and gitdir custody/read/post-status/target work.

R-dependent absolute spellings use the root prefix plus the UTF-8 byte length of the relative suffix; root records use R alone. Fixed and relative-only terms form the base. The model counts transient allocations as cumulative ledger requests, including spell and repeated observations, and does not equate them with retained-memory RSS. Its affine coefficients and the native prediction evaluation use byte lengths consistently.

The 15 whole-file closure pins and 33 uniquely matching anchors verify. The ten size_of operands extracted from those anchors exactly equal the declared size inventory, including usize. Seven security-side sizes are checked as parsed integers against size_of; the three libc checks require RF-1's token correction. Adding the new platform integration test is an appropriate way to check libc types without adding a security dependency.

The capture model takes a componentwise maximum. At the recorded sizes FS is 2,368 bytes and the largest owned ACL-entry record is 128 * 16 + 128 = 2,176, so the filesystem branch bounds all three dimensions. The reader model follows the pinned CHUNK/doubling progression and charges each full requested buffer, including the larger EOF probe when length exactly fills a buffer, up to the ceiling. It retains the stated uninterrupted edge envelope. A parsed gitdir target is conservatively charged at the file length. T2 store integrity excludes .git components; the hypothetical read cases remain synthetic vectors.

The existing integrity, exact workspace mounts, held-out guard, reference population comparison and completed-walk checks remain in place. Workspaces are composed before modeling, through the same path as repositories.

## Probe, records and native controls

The tool pins the archived lead-probe log, requires four matching successful probe rows, checks object/edge equality and bounds measured bytes at each probe root length. All four current comparisons are equal in bytes as well, including aws-sdk-rust at 639,480,718 bytes with R=134. This is a pinned evidence cross-check, not a native probe executed during this review.

The soundness tests evaluate each affine prediction at the scratch root's actual byte length, compare all three ledger dimensions and retain the incomplete-walk refusal. The supplied log contains 56 comparisons, all bounded; 46 are exact in objects, edges and bytes. The supplied abort control remains passing. Margin controls evaluate bytes at every reported R against an independent fresh discovery ledger, verify the affine arithmetic and probe the byte-limit boundary. This preserves classification against code limits rather than trusting a JSON cap copy.

Independently compared every entry/workspace's objects, edges, counts and passes2x with bound B2-b4a: unchanged. The regenerated record has the same three object-margin failures and reports byte-margin failures exactly as follows:

- R=134: rs-very-large-aws-sdk-rust.
- R=1024: rs-very-large-aws-sdk-rust.
- R=4096: rs-very-large-aws-sdk-rust, ts-very-large-aws-sdk-js-v3 and mr-ts-very-large-smithy-sdk.

All recorded affine values and fitsTwiceAt classifications match their arithmetic against the current 2^30 byte limit. No byte margin is claimed, caps remain returned to law, and held-out margin stays outstanding.

## Verification and scope

Independently ran only expressly permitted Python commands:

- Source operability: 114 rows, no findings, passed.
- Environment-exception controls: 10 passed.
- FW-01 controls: seven passed.
- Census-tool controls: 18 passed.
- Full requested census --check: both generated records verified.

The supplied pinned evidence reports all 16 check rows successful. Security passes increase from 1123 to 1124 with the same 14 named baseline failures. The six census security tests and one platform size test report success. All five regenerated-model mutation logs contain their declared failing native tests, including dropped scope-entry bytes. Locked/offline all-targets Clippy includes host, security and platform with -D warnings and completes successfully. Both edited/new Rust files are format-clean with the inherited file base-clean and no exclusions. Supplied vector/configuration checks and verify_design report success, with inventory v196 selected and qualification false.

No Cargo, rustc, Rust tests, builds, lane, Clippy, rustfmt, other vector tools or verify_design were executed during review. Those outcomes are inspected evidence. No native store probe was executed.

No production caller, production environment read, profile-cap change or law change is added. The requested correction precedes unit acceptance and the separate inventory successor. B2-b4b2 and B2-b4b3 remain later reviewed amendment/cap steps; B2-b remains incomplete and no qualification is established.

Only REVIEW.md and review.json were written. Neither repository, candidate, stage nor controls were edited. No network, other panes or delegation were used; no private fixture, installation directory, signing keys, held trees or T2 held-out store/overlay was accessed.
