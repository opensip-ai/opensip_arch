# B1-B-r4 review

Verdict: **ACCEPT-UNIT**

Required findings: none. Non-blocking observations: none. All findings from rounds 1–3 are resolved for this scoped unit.

Verified the 12,046-byte subject manifest, SHA-256 `956bd8d6cebcdeb9a2923bc3e9282b028db4e5ca2030c081ac03e9443384924f`, and all 53 members by byte count and SHA-256. All 27 product-map files match their archived and candidate worktree bytes. Parent pins match product base `c0151bc6b7fdb6db9157124fa068c8be5061f5d4`; new paths are absent there. The map equals the complete candidate changed/untracked path set. Source authorities match architecture base `b98932720200253f671814d9cb728ba0615c1085`. Both product HEADs match the requested base; the main product is clean. The product lock is byte-identical to base: inventory 188 and 162 contract successors remain unchanged.

## Remaining finding resolved

Round-3 RF-01 is resolved. The checker no longer treats an integration-test path as an unconditional test-only exemption. It starts with non-included production roots outside tests/, propagates production reachability along non-test-scoped include edges, and classifies a reached integration-test file as production. Include edges are found on blanked code with their paths recovered at matching source offsets. The new control adds a real include of host/tests/admission_tests.rs from host/src/lib.rs while retaining its integration-test role; RUSTC correctly becomes production-classified. Without that inclusion the same exception remains test-only.

The earlier controls remain: mixed production/test inclusion of a src test file, include text in comments/literals, changed constant values and an allowed helper moved outside its test module. They pass in the expressly permitted checker run. The scanner's actual current exceptions still match the accepted r5 list by file, function and resolved variable name, with allowances attached to their audited functions.

Compared every mapped product file against round 3: only tools/tests/test_environment_exceptions.py changed. The custody, mode, wrapper and composition implementations and Rust controls retain their reviewed bytes.

## Whole-unit assessment

Project selection retains both the judged descriptor and the metadata sample on which custody passed. Local judgment does the same. Capture reads that descriptor within the 4 MiB ceiling, charges the operation ledger, and requires full sample equality to the judgment before and after the read. The held-fence recheck covers captured carriers and explicit negative observations for project/local files and the interactive local parent. CI never probes the local carrier. The judgment-to-read rewrite/custody controls and post-capture replacement controls remain in place.

The analysis carrier phase performs placement/chain checks before carrier reads and precedes registry capture. The host's resolution/X12 admission fits between phases. Legacy admission remains non-capturing, with unchanged reads, charges, refusals, rechecks and latching; carrier rechecks are skipped on that path. The original wrapper bodies remain intact, with separate analysis methods mirroring session/gate ledger and settlement behavior. Five matched base/candidate core-admission probe states corroborate unchanged charges and classification.

Optional global capture shares required capture's private walk and settlement. Existing parents receive private-custody, exact-name and filesystem judgments. Positive absence retains the original parent samples and absent component; full recheck re-judges the same parent identities/samples and repeats the absence. Changed, replaced, detached or wrong-custody parents refuse. Capture creates neither global settings nor its parent.

InvocationModeV1 is unified with invocation.rs. Interactive mode is exactly stdin-terminal AND stderr-terminal. The observer uses IsTerminal, reads no environment and has no production caller. The single added operability stdio row, count one, has owner output and terminal.

The identical crate-local Clippy configurations prohibit the four environment methods in host and security. Thirteen audited item-level allowances cover exactly the 17 existing authorized sites. The only production read remains refusal-only Git environment observation. LD-B1B-5 is sound: ignored children selected by exact test name need no marker read, so the unused allowance remains unused. LD-B1B-4 is sound: the crate-split children compare capture facts and complete semantic/operational resolution and provenance under cleared/hostile environments; the permitted Git refusal is separately asserted.

Round-2 RF-02 remains resolved. The test-only local counter asserts zero lookups in CI and two interactively across capture and recheck. The ignored charged CI lookup mutation is caught. The host composition control uses real captured project bytes, the resolver and X12 admission through the existing scenario-fixtures test seam. The refused project pack reaches no second-phase registry capture; registry bytes, member sets/sizes and writer release establish no RESERVED row, new lease, journal or marker. The bundled-pack control reaches registry capture. The scenario additions remain behind the existing doc-hidden test-feature/dev-dependency boundary; no ordinary production public API or caller is added.

Refusals map to existing public codes. Tests cover custody races, absence appearances, CI/interactive behavior, ordering, legacy compatibility, optional settings, mode, environment enforcement/equivalence and no-write behavior. Acceptance is for the exact B1-b unit, not J1 wiring, discovery, member carriers, S-OP-5, qualification or project completion. Inventory v189 remains a separate subsequent review/binding.

## Verification and limits

Independently ran only the two expressly permitted offline commands:

- `python3 -I -B tools/tests/test_environment_exceptions.py`: ten tests passed.
- `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip-b1b`: passed, no findings, 114 rows.

Validated the fresh checks-r6 evidence. All nine raw control logs match controls.json: seven mutations have the named failing tests, and both planted reads trigger disallowed_methods with compilation failure. The legacy probe's five states match both archived raw probe logs and one another.

The submitted full-suite comparison has equal exact failure-name sets and suite counts: security retains 14 failures, with passes increasing from 1,046 to 1,062; host retains eight failures, with passes increasing from 330 to 336. Full-suite transcripts are not subject members, so those suite results are supported by the submitted comparison record and runner, not an independent replay or raw-suite reconstruction. Archived command/log evidence supports warning-denied all-targets Clippy for both crates. All 23 mapped Rust files are format-classified: 13 new/base-clean files passed the recorded check, with ten explicit base-dirty exclusions. Tools/census and design-verification evidence agree with checks.json; design verification selects inventory 188 and 162 contract successors. Earlier failed attempts and stale historical lane wording are not acceptance evidence.

No Cargo, rustc, builds, other tests, lane or network was run by this review. No private fixture, installation directory, signing keys, held trees, other panes or delegation were used. Neither repository, the candidate worktree, stage, controls nor prior reviews was edited. Persistent review writes are limited to this directory's REVIEW.md and review.json; the permitted checker creates and cleans its own temporary copies. Lead assent, architecture publication, the product code commit and the later inventory binding remain separate steps.
