# B2-B4C2-inventory-v200 review

Verdict: **ACCEPT-UNIT**

Required findings: none. Non-blocking observations: none.

Independently rehashed the 704-byte subject manifest, SHA-256 `ae1f01b1f1a9af273faef493eb262bb66506a35d7d5ba1a8dd5be4b68a567083`, and all three members. Every size and hash matches. Product main is clean at `c0bbdc86affecf3ed68f077452ea38831c5b5d89`; architecture HEAD is `c4f99bfe4285ea66e32bd2e4fe04c84c19d52497`.

## Inventory

The v200 candidate is 688635 bytes, SHA-256 `0dc71badf5178f531e4b23d8f0c9bf4ce7e98b32f6bfb8d18b55ac0232b43134`. The architecture parent v199 is exactly 687868 bytes, SHA-256 `239f95f58513c0d8573c7b837ba460acee1099fc3bf329124f70460d63eadb90`.

Parsed comparison confirms that only the files array changes: all 1255 inherited rows remain equal by value, including the existing census and blind-test rows. All 20 packages and 9 pending decisions remain equal. The candidate is sorted and unique, with 1256 rows: exactly one addition, `crates/security/src/custody/discovery_census_held_out.json`. It covers all 1157 tracked product paths. The 99 absent planned paths are all inherited unchanged and exactly equal the successor record's retained-path list; no implementation is claimed for them.

The new row correctly assigns package `opensip-security`, role `fixture` and `generated: true`. Its description accurately identifies the accepted blind-generated receipt, its limited per-entry verdict/margin output, public bindings, derived state and ordinary-mode composition while current. It explicitly excludes qualification and claims nothing beyond B2-b4c2. The path had no parent row.

## Accepted-unit and integration bindings

Rehashed the successor record: 5476 bytes, SHA-256 `62959b59e6aa775b812f413b013b34903adf895ed3e32c23bd31e1cedc93f23f`. Its parent, candidate, integration-census, accepted-code-review and accepted-code-subject pins all match their actual artifacts. The accepted review is ACCEPT-UNIT with no required findings and binds the same accepted subject digest. Main's new receipt matches the accepted subject's product-map candidate bytes. This is an inventory review; the closed code was not re-reviewed.

The integration census is 747 bytes, SHA-256 `7254d69620988b9d6864db7941f343c7bdfea958ff8f59fc214444ae0e473d31`. Its product commit and checker/exception pins are exact. Independently ran the expressly permitted command:

`python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip`

Result: passed, 114 rows, no findings. Read the checker's source to confirm this command also compares the actual lexical mint census with the audited rows. The mint-audit record has 439 rows and is equal to the accepted code base's record. No mint authority is added or implied by that lexical audit.

The successor's addedFiles and inheritedPlannedFilesRetained lists are exact. Product qualification is false. Lead assent/publication and the separate inventory-lock binding with fresh verify_design remain subsequent steps; this acceptance does not claim those have occurred.

## Boundaries

Wrote only REVIEW.md and review.json in the requested review directory. Used read-only hashing, JSON parsing, file inspection, Git queries and the one expressly permitted source check. Neither repository, stage nor control files were edited. No compiler, Cargo, tests, lane, network, other panes or delegation were used. No private fixture, installation directory, signing keys or held trees were read.
