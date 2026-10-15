# B3A-PLAN-r1 review

Verdict: **ACCEPT**

Required findings: none. Non-blocking observations: none. Acceptance covers the implementation plan, not completed code or controls.

Verified the 448-byte subject.json, SHA-256 `ddd2790c7cb77bebf46f55e717b276ede7134c09ff90225e6def6fad7894a3bc`, and its sole member, PLAN-r1.md: 9,777 bytes, SHA-256 `8adcae11b80fb1ae5eed06c4b7276cfab84b6616eb978e02835b4d281aa5e27c`. Product HEAD matches the requested clean `ec70009de1490449a6173c238a7eaf0a03e106c4`; architecture HEAD matches `127a6429fd378957c9621bbb65cc73a18bcc0ad4`, with no tracked differences.

## Scope and existing facts

The plan matches M3-B item 23 and the B3-a units row: four authorization records, invocation-only constructors, pure S3.1 choice and the existing ephemeral selection. It retains the reserved C4/X4/M5 work and forbids execution, mutation or recovery grants, configuration constructors and I/O. Applicability and downstream wiring remain with their owning consumers.

Section 0 agrees with the product. grants.rs remains a planned-absent inventory v189 path. RequestFlags carries the stated paths, ordered Vec<u32> groups and two authorization booleans; AnalysisRequest::AnalyzeEphemeral and Durability already represent ephemeral selection. The analysis flags do not include yes-policy. ProjectChainPolicy currently consumes a borrowed BTreeSet<u32> and does not implement an owner waiver. BackupClassification has the three stated variants, and the law-464 classifier returns Unknown. The cited refusal codes/details already exist.

## Records and constructors

AuthorizedGroups admits parsed u32 gids only, exposes membership and bounded provenance, and supplies the existing custody set through a typed adapter. Deduplicating while preserving first-occurrence order produces at most 64 sequence entries without truncation or an invented duplicate refusal. The SLS authorizedGroupIds definitions have maxItems 64 and sequence ordering, without a duplicate-refusal requirement.

ProjectOwnerWaiver is optional when the flag is absent and refuses a set flag without an explicit project on the existing PROJECT.EXPLICIT_PATH_INVALID row, matching SLM. It carries the explicit spelling without performing custody. Its documented applicability waives only ownership on explicit-root directories/config, including member directories as MB specifies; marker files, member Git evidence and local.json remain excluded. Consumers apply that scope rather than this unit introducing a waiver consumer.

BackupCustodyAcknowledgement is per invocation and consumed only by the choice function, without creating a policy. ConsentSource remains a typed future-M5 value, with the 64-lowercase-hex policy identifier checked and the stated SL:1110 policy-record / interactive-explicit mapping. No signature verification or policy-record admission is claimed by merely checking identifier grammar; the choice's policy input is explicitly already admitted.

The planned private construction surface has no From/TryFrom/Default/Deserialize or JSON/resolved-configuration constructor and no Clone implementation. Its primitive inputs represent parsed invocation data; the resolver is separately pinned not to name grant types. There is no new configuration authorization path.

## S3.1 and lead decisions

The choice order mirrors SLM storage_write_admission: ephemeral first; NotBackedUp and Unknown next; invocation acknowledgement; admitted policy record; otherwise refusal. The typed BackupClassification removes the reference's invalid-vocabulary branch from representable inputs. Unknown admits with mandatory unknown-disclosed semantics, never as not-backed-up and never requiring acknowledgement. Refusal retains request-rejected, exit 2, REQUEST.PRECONDITION_FAILED / storage.backup-choice-required and the CI-versus-interactive choice spelling. The result preserves policyFileWritten:false and rootIdentityChanged:false, and the function has no I/O. Sync/shared/upload classifications are not waived.

LD-B3A-1 is sound: J2a's existing request/durability selection meets the typed-selection obligation without a duplicate security enum; the host supplies its ephemeral boolean to the choice at later wiring. It remains outside configuration and its digest.

LD-B3A-2 is sound: authorizedGroupIds is not one of NE:4276's seven bounded-selection fields. Keeping TooManyGroups internal and leaving its public CLI routing to M4 avoids extending PROJECT.SCOPE_LIMIT or inventing a code, while refusing rather than truncating. LD-B3A-3's distinct-gid bound and first-occurrence provenance agree with authorization-set semantics and the published sequence cap.

## Controls and acceptance boundary

The control plan sufficiently covers empty/single/boundary/overflow group sets and duplicates, waiver flag/project combinations, acknowledgement presence, consent identifier grammar/mapping, every S3.1 decision branch and precedence, no-configuration construction, ephemeral exclusion and purity. Byte vectors are to be derived from the accepted SLM function and reproduced in Rust; those checks are planned, not executed evidence.

The proposed compile check follows the existing host admission snippet style. Its current harness requires a compiling positive control before assessing the misuse and its annotated diagnostic. That standard must be retained when implementing the grant cases, so a general privacy/import failure cannot substitute for the claimed absence of a configuration constructor. The complementary constructor/trait and resolver source pins address the actual construction surface. Deferred consumer applicability tests do not become a new B3-a custody implementation.

The verification sequence requires base/candidate suite failure comparison, all-targets warning-denied Clippy, appropriate formatting, the unchanged environment-exception list, operability census and design verification. Code acceptance, architecture publication, the later v190 inventory transition/binding and status reconciliation remain separate. No CLI parser, S3.1 caller, custody consumer, execution/mutation/recovery grant, law amendment or qualification is accepted here.

This review used only read-only reading, hashing, JSON parsing and Git queries. No Cargo, tests, builds, lane or network was run. No private fixture, installation directory, signing keys, held trees, other panes or delegation were used. Neither repository, the stage, controls nor prior reviews was edited. Only this directory's REVIEW.md and review.json were written.
