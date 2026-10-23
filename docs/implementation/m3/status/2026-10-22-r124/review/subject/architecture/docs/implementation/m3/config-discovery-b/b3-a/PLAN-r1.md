# B3-a implementation plan r1 (M3-B unit B3-a: `grants.rs`)

**Lead plan record, 2026-10-14; r1. Not law, not code.** B3-a may start at day 0: its dependencies, P0 and L, are met. B1-a and B1-b are bound (product `ec70009`, inventory v189). Codex reviews this plan before any code is written.

**Authority.**
- **M3-B r5** (`config-discovery-b/PROPOSAL.md`, cited as MB):
  - item 23: the table of the seven shared flags, and the `grants.rs` M3 scope with its in-scope, reserved and forbidden lists;
  - item 8's "Shared flags" row (an unknown value is the CLI's refusal, M4);
  - the B3-a row of "Units after the law".
- **SL:**
  - S3, for `--trust-group` and `--trust-project-owner` (SL:120-130);
  - S3.1, the backup custody choice (SL:317-331);
  - the workflow `consentSource` (SL:1110).
- **SLM:**
  - `storage_write_admission` (SLM:3104-3128), the S3.1 reference;
  - the waiver rules (SLM:632-680, SLM:832-833).
- **SLS** `authorizedGroupIds` (`maxItems: 64`, sequence).
- **CINV** `sharedFlags`, the seven flags with their classes; **CH14:401**, the `grants.rs` description.

## 0. What exists (product `ec70009`)

- **`crates/security/src/grants.rs`.** It is absent: a planned row of inventory v189 ("Bind and verify exact execution, mutation and recovery permissions").
- **Host invocation model (J2a, `invocation.rs`).** Already present:
  - `RequestFlags` holds the parsed `--project`, `--workspace-root`, `--trust-group` (a `Vec<u32>` in the given order), `--trust-project-owner` and `--allow-backup-custody`;
  - `--ephemeral` is the request itself (`AnalysisRequest::AnalyzeEphemeral`, `Durability::Ephemeral`);
  - `--yes-policy` is not in the M3 request flags; CINV gives it to M5's test and repair commands.
- **Security today.** `ProjectChainPolicy` takes the trust groups as a bare `&BTreeSet<u32>` (`project_chain.rs:80-84`). Project custody does not yet implement the owner waiver.
- **The backup classification** is `initial_installation::BackupClassification {BackedUp, NotBackedUp, Unknown}`. Under law 464 it is constant `Unknown`.
- **Generated codes.** `REQUEST.PRECONDITION_FAILED` and `storage.backup-choice-required`, and `PROJECT.EXPLICIT_PATH_INVALID`, exist; there is no new code.

## 1. What B3-a delivers

All of it lives in `crates/security/src/grants.rs` (new; library only, pure, no I/O), with its tests in `grants_tests.rs`.

### 1.1 The four authorization records (MB item 23)

| Record | Constructor (pure; from parsed invocation input only) | Refusal | Carries |
|---|---|---|---|
| `AuthorizedGroups` | `from_invocation(gids: &[u32])`. Duplicates collapse to one authorization; first-occurrence order is kept for provenance (SLS `sequence`). | More than 64 distinct gids is `GrantRefusal::TooManyGroups { count }` (see LD-B3A-2) | `contains(gid)`, `provenance() -> &[u32]`, `as_set()` for project custody |
| `ProjectOwnerWaiver` | `from_invocation(trust_project_owner: bool, explicit_project: Option<&Path>)`. `Some` only when the flag is set; the flag without `--project` refuses. | `GrantRefusal::OwnerWaiverWithoutExplicitProject`, which maps to the existing `PROJECT.EXPLICIT_PATH_INVALID` row (SLM:832-833; SL:129-130) | The explicit root's spelling. Applicability is typed but applied by its consumers (below). |
| `BackupCustodyAcknowledgement` | `from_invocation(allow_backup_custody: bool)`, `Some` when set. Per invocation. | none | Nothing; it is consumed only by the S3.1 choice |
| `ConsentSource` | `PreExistingPolicy { record: PolicyRecordId }` or `InteractiveConsent`. Typed, with no M3 consumer (M5). `PolicyRecordId` is 64 lowercase hex. | Malformed id: `GrantRefusal::PolicyRecordId` | The SL:1110 mapping: `policy-record` or `interactive-explicit` |

**Applicability is the consumer's.** B3-a carries it as documented, typed scope and applies none of it:
- `ProjectOwnerWaiver` waives only the owner check, on the explicit root's directories and its `opensip.json`, never on marker files (SLM:636, 665, 669-680). Per MB item 23's D15 column, it never applies to member Git evidence or `local.json`.
- `AuthorizedGroups` applies wherever `judge_project_object` applies trust groups.
- Custody consumes both: B2-b and B3-b. B3-a adds `ProjectChainPolicy::from_grants(..., &AuthorizedGroups)` only as a typed source of the existing `&BTreeSet<u32>`. The legacy constructor is unchanged.

**No configuration constructor (MB item 23; SL:127-129).**
- Each record has exactly one constructor, from primitive parsed values that only the invocation parse holds.
- There is no `From`, `TryFrom`, `Default`, `Deserialize`, or JSON or `ResolvedConfigurationV1` path.
- The records are not `Clone`, so a record is consumed where it is used.

### 1.2 The S3.1 choice function (pure)

`storage_write_choice(backup, ephemeral, acknowledgement, admitted_policy, ci) -> StorageWriteChoice` mirrors SLM `storage_write_admission` (SLM:3104-3128) exactly, in this order:
1. `ephemeral` → `Admit(Ephemeral)`.
2. `NotBackedUp` → `Admit(NotRequired)`; `Unknown` → `Admit(UnknownDisclosed)`. UNKNOWN is never rendered as not-backed-up and never requires the choice.
3. A `BackupCustodyAcknowledgement` → `Admit(InvocationFlag)`.
4. An admitted storage-policy record (`PolicyRecordId`) → `Admit(AdmittedPolicyRecord(id))`.
5. Otherwise `Refuse { ci }`. The termination is `request-rejected`, exit 2, `REQUEST.PRECONDITION_FAILED` / `storage.backup-choice-required`, with the choice `interactive-prompt-unavailable` in CI and `interactive-choice-required` otherwise.

`backup` is the existing `BackupClassification`. `ephemeral` is a `bool`: the host maps `Durability::Ephemeral` when J wires the first source-derived write.

The choice writes no policy file and changes no root identity. Its result says so (`policyFileWritten: false`, `rootIdentityChanged: false`, as the reference's do), and it has no I/O to do either.

### 1.3 `--ephemeral` (MB item 23 row)

J2a's `AnalysisRequest::AnalyzeEphemeral` and `Durability` already are the typed selection carried to J. B3-a adds no second type (lead decision LD-B3A-1). It pins the two remaining obligations:
- the selection is not configuration: `ResolverInputV1` has no durability, a pin already holds in B1-a's tests;
- it reaches S3.1 as the `ephemeral` input.

## 2. Lead decisions

**LD-B3A-1, no second `--ephemeral` type.**
- J2a's request type is the selection. A security-side duplicate would be two spellings of one fact. The choice function takes the `bool` the host derives from it.
- **Rejected:** a `grants.rs` enum mirroring `Durability`.

**LD-B3A-2, the group bound's public row is M4's.**
- `authorizedGroupIds` is not one of NE's seven bounded selection fields (NE:4276), so there is no published typed `PROJECT.SCOPE_LIMIT` refusal for it.
- MB item 8 gives shared-flag value refusals to the CLI (M4). B3-a types `TooManyGroups { count }` as an internal refusal and maps no public row.
- **Rejected:**
  - minting a `PROJECT.SCOPE_LIMIT` subject for it, which would extend NE's closed list;
  - truncating.

**LD-B3A-3, duplicates collapse.**
- A gid named twice authorizes once. The bound counts distinct gids. Provenance keeps first-occurrence order.
- **Rejected:** refusing duplicates, which no law requires and which would make `--trust-group 20 --trust-group 20` an error.

## 3. Tests (MB item 23 controls; COV:5268-5407)

- **Each record.**
  - `AuthorizedGroups`: 0, 1, 64 and 65 distinct gids; duplicates collapse; provenance order kept.
  - `ProjectOwnerWaiver`: without `--project` it refuses on the `PROJECT.EXPLICIT_PATH_INVALID` row; with it, it carries the root; without the flag it is `None`.
  - `BackupCustodyAcknowledgement`: present or absent.
  - `ConsentSource`: the record id's grammar, and the SL:1110 mapping.
- **S3.1.** Every row of the reference's decision table is reproduced, with the order pinned:
  - ephemeral beats everything;
  - UNKNOWN admits disclosed, without the flag;
  - the flag;
  - the record;
  - refusal in CI and interactively.

  Byte vectors come from SLM `storage_write_admission` at its accepted bytes (`tools/security/storage_choice_vectors.py`, the B1-a vector pattern), and the Rust test reproduces them.
- **No configuration path (compile-fail and pin).**
  - A pin test: `grants.rs` implements no `From`, `TryFrom`, `Default`, `Deserialize` or `Clone`, and `configuration.rs` and the resolver never name a grant type.
  - A compile check, in the host admission tests' existing rustc-snippet style: a snippet that builds any grant from a `JsonValue` or a configuration type fails to compile.
- **`--ephemeral`.** A pin: `ResolverInputV1` and `CompiledDefaultsV1` carry no durability, and the digest is unchanged across `Durability` values. The latter holds trivially, because no resolver input carries it.
- **Purity.** `grants.rs` reads no environment (it is under B1-b's lint) and does no I/O. A source pin forbids `std::fs`, `std::io` and `std::env`.

**Verification.** Security and host suites, base against candidate with equal failure sets; all-targets Clippy with warnings denied; rustfmt on new and base-clean edited files; the environment-exception pin (unchanged list); the operability census; verify_design.

## 4. Sequence

1. This plan, reviewed by Codex.
2. B3-a code: the stage, checks, Codex `ACCEPT-UNIT`, the architecture record, then the product code commit.
3. The inventory successor v190. `grants.rs` turns from planned-absent to present; the new paths are its tests and the vector tool.
4. A status round.

## 5. Not claimed

- No custody consumer of the waiver or groups (B2-b, B3-b).
- No CLI parsing (M4).
- No S3.1 caller (J's first source-derived write).
- No execution, mutation or recovery grant, which `grants.rs` forbids at M3.
- No law change and no qualification.
