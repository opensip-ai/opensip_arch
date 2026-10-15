# B3-A-r1 review

Verdict: **ACCEPT-UNIT**

Required findings: none. Non-blocking observations: none.

Verified the 8,188-byte subject manifest, SHA-256 `057c982301bf98043b6287fb32de502a70ca2c5a2b5e6b1fdbf167a4e44b9d12`, and all 37 members by byte count and SHA-256. All seven product-map paths match their candidate worktree and archived bytes. Parent pins match the product base; new paths are absent there. The map equals the entire changed/untracked candidate path set. All source authority pins match architecture `70950d53ce1ab79c99c51c5340b5d101b397801b`. Product and candidate HEADs are `ec70009de1490449a6173c238a7eaf0a03e106c4`; the main product is clean. The lock is byte-identical to base, retaining inventory 189 and 162 contract successors.

## Records and choice

The records match M3-B item 23 and the accepted plan. AuthorizedGroups collapses duplicates, preserves first-occurrence provenance, exposes the same immutable set to custody, and refuses more than 64 distinct gids with the complete distinct count. It neither truncates nor invents a public group-limit row. The waiver carries the exact explicit-root spelling, returns None without its flag, and maps a set flag without an explicit project to the existing ProjectExplicitPath termination. Applicability remains documented for later consumers rather than introducing a custody waiver implementation here.

The backup acknowledgement is per invocation and passed by value to the choice. PolicyRecordId has a private field and validates precisely 64 lowercase ASCII hex bytes. ConsentSource preserves the workflow and grant-mode spellings from SL:1110. Its policy id is a typed identifier, not a new policy-record authenticator; storage_write_choice explicitly takes an already-admitted policy input. The module is private, records are not Clone/Copy, and the current source has no conversion, default, serde or configuration constructor. No host file changes.

storage_write_choice follows SLM's representable input order exactly: ephemeral; NotBackedUp/Unknown; invocation acknowledgement; admitted policy record; refusal. Choice spellings, UNKNOWN disclosure basis, CI distinction and the two false policy/root-effect facts agree with the reference. Refuse maps to the existing BackupChoiceRequired row; the unchanged host projection supplies request-rejected, exit 2, REQUEST.PRECONDITION_FAILED / storage.backup-choice-required. No public code is added.

The 144 vectors cover the full selected Cartesian product of three backup states, ephemeral, acknowledgement, six policy inputs and CI. The vector tool pins the accepted SLM and its architecture dependencies and validates the provisioned package closure before import. Its check reproduces the exact JSON bytes; Rust checks branch/choice and refusal fields, including ten refusals and two policy-record admissions. Direct ordering controls complement those vectors.

LD-B3A-5 is sound. The accepted plan requires exactly 64 lowercase hex digits. The pinned SLS Hex64 definition has minLength/maxLength 64 and a strict end assertion, `^[0-9a-f]{64}(?![\s\S])`. A newline suffix violates that grammar even though SLM's Python `$` accepts it. The tool explicitly excludes that reference quirk from cross-implementation vectors, and a product grammar test rejects it. This does not change the accepted id grammar or the S3.1 decision order.

ProjectChainPolicy::from_grants delegates directly to the unchanged new constructor with groups.as_set(). Its test checks pointer identity of the lent set. The adapter has no production caller and does not implement waiver/group applicability or replace legacy callers. initial_installation::storage_choice remains unchanged.

## Construction and purity controls

LD-B3A-4 is sound. In-crate negative trait probes inspect the real private types rather than obtaining an irrelevant external-module privacy failure. Each probe has one applicable blanket implementation in the accepted build; a forbidden implementation adds the second and produces ambiguity. All five record types are covered against the stated 21 traits, including JSON conversions, Clone/Copy/Default and FromStr. Four archived compile controls independently trigger E0283 for Clone, Default, FromStr and From<bool>. Successful unmodified builds provide the positive control.

Complementary pins restrict module conversions/derives, foreign record implementations, exports, resolver references and serde. Purity pins constrain the imports and forbid filesystem, I/O, environment, process, networking, platform and unsafe code. The actual module satisfies them and remains under the existing security environment lint. The foreign-impl and I/O mutations and planted environment read are caught. No execution, mutation or recovery grant is introduced.

## Evidence and scope

Independently ran only the expressly permitted offline commands:

- `python3 -I -B tools/tests/test_environment_exceptions.py`: ten tests passed; the exception list is unchanged.
- `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip-b3a`: passed, no findings, 114 rows.
- `python3 -I -B tools/security/storage_choice_vectors.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`: reproduced the vectors from SLM at its accepted bytes without writing output.

Verified all 15 archived raw control logs against controls.json: ten behavioral/source mutations have their named failing tests, four compile controls show E0283 and compilation failure, and the planted read triggers disallowed_methods. The corrected real foreign-impl control is caught; the earlier unsuccessful control is not counted as evidence.

The submitted comparison records equal exact failure sets and suite counts: security retains 14 failures, with passes increasing from 1,062 to 1,072; host retains eight failures and 336 passes. Full-suite transcripts are not subject members, so those full-run results are supported by the submitted comparison and runner rather than an independent replay or raw-suite reconstruction. Archived command/log evidence supports all-targets warning-denied Clippy. All five Rust files are format-classified: the two new files passed the recorded check and three edited files have explicit base-dirty exclusions. The tools/census and design-verification evidence agree with checks.json; design verification selects inventory 189/contracts 162. The fresh successful lane r2 is the acceptance evidence.

Acceptance covers this pure private library unit and its controls. No ordinary public API, production caller, host change, environment read, CLI parsing, custody consumer, first-write caller or qualification is added. Inventory v190, lead assent, architecture publication and the product code commit remain separate steps. The whole plan/project is not complete.

This review ran no Cargo, rustc, builds, other tests, lane or network. No private fixture, installation directory, signing keys, held trees, other panes or delegation were used. Neither repository, candidate worktree, stage, controls nor prior reviews was edited. Persistent review writes are limited to this directory's REVIEW.md and review.json; the permitted environment checker creates and cleans its own temporary copies.
