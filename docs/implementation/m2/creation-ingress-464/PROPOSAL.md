# Creation ingress and storage choice for the initial creator — proposal 464 r3

2026-09-26. Claude Opus 5.5, implementation lead. Law for unit 464 (`CreationIntent`), under owner.md §1a step 1, the first-creation storage choice paragraph, and §6. It closes the points owner.md leaves to the implementation and settles two textual conflicts. Not code, not creator authority. The creator stays disabled. r2 answers Grok 464 r1 RF-1 (the notice omitted retention origin) and RF-2 (StepId is a position, not a draw). r1 bytes are preserved in PROPOSAL-r1.md. ACCEPTED by Grok 464 r2 on 2026-09-26.

**r3 (2026-10-04) is an amendment: J1's successor S4.** It changes items 1 and 5, and item 7 gains a note on the code's unit. r2 bytes, as accepted (sha256 `a940ba50…`, 6,709 bytes, without the acceptance note), are preserved in PROPOSAL-r2.md. **Draft r3, not accepted.** Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the autonomous run. Not code.
- **Its sources.**
  - **J1 r5**, the accepted host-pipeline law, cited as J1 (`docs/implementation/m3/host-pipeline-j/PROPOSAL-r5.md`, sha256 `4ccb2320…`; accepted by Codex, `m3/reviews/codex-host-pipeline-j-r5`). Its successor row S4 gives this law "items 1 and 5: the lent RequestId; the prelude's ExecutionId reserved before P0 (item 2)" (J1:849). J1 item 3 states the amendment (J1:288). J1 item 2 states the identity rules (J1:190-218).
  - **X3d r9**, accepted by Grok, cited as X3D9 (`docs/implementation/m2/commit-session-x3d/PROPOSAL-r9.md`, sha256 `c727001a…`; `reviews/grok2-x3d-r9`). It is J1's successor S10. Its S10.1 reserves the analysis attempt's ExecutionId at `open`, in the same registry and under the same rule (X3D9:486-493). r3 agrees with it.
- **What it changes.**
  - Item 1: the intent holds the invocation's lent RequestId and a fresh ExecutionId, which it reserves before P0 is staged.
  - Item 5: the uniqueness check uses the process-custody registries, not "no ledger". The RequestId is the whole invocation's, and the prelude's ExecutionId is never reused.
  - Item 7: the code is J1 unit J3a's.
- **What it does not change.** Eligibility, the backup classification, the disclosure and its refuse-on-failure rule, StepId 0, item 6's conflicts, the forbidden substitutes and "Not claimed". Item 3's "a schema successor owed by 468" stands; 468 r6 item 7 records that J1's S13 lands it. No public code, row or subject is added.
- **Unchanged from r2:** everything else. No accepted outcome of r2 or of another law changes, except as S4 declares.

**r3 changes.**

| # | Change | Where | Source |
|---|---|---|---|
| 1 | **The lent RequestId.** The intent holds the host's `RequestIdentity` and draws no RequestId of its own. | items 1 and 5 | J1:194, :258, :288 |
| 2 | **The prelude's ExecutionId is reserved before P0.** `mint_intent` still draws it, and reserves it in `ExecutionIdReservations` before P0 is staged. The intent holds the `ReservedExecutionId`. | items 1 and 5 | J1:204-211; X3D9 S10.1 |
| 3 | **The uniqueness ledger is process custody** | item 5 | J1:195-198, :204-205, :217, :225; LD3-1 |
| 4 | **Item 5's last sentence** now reads: the RequestId is the whole invocation's, and the prelude's ExecutionId is never reused. | item 5 | J1:200, :223, :288 |
| 5 | **Refusals** stay on the existing host-I/O row | item 5 | J1:207; X3D9 S10.1 |
| 6 | **Units:** J3a | item 7 | J1:881; X3D9 S10.8 |

**r3 lead decision.** It is made under the owner's standing direction of 2026-09-30, and it names the alternative it rejects.
- **LD3-1. The uniqueness ledger before I is process custody.** r2's item 5 says: "Before I exists there is no ledger. RequestId and ExecutionId are CSPRNG draws", and "uniqueness is established by construction". J1 item 2 names process custody as "the corresponding operational ledger" of IE:77-81 for both ids (J1:195, :204-205). It also rejects "treating the CSPRNG draw, or the draw's ledger charge, as the ExecutionId reservation" (J1:225). The two texts conflict.
  - **Decision.** J1's wording governs. Item 5 names the host's `RequestAuthority` and `ExecutionIdReservations` as the ledgers. It keeps the fact that the winner's ledger in I begins with P0, but no longer as the uniqueness argument.
  - **Rejected:** keeping "no ledger before I", with uniqueness by construction. J1 rejects it, and X3d r9 S10.1 already reserves the analysis attempt's ExecutionId in the same registry.

## What owner.md already fixes (restated, unchanged)

- **Eligibility.** Only `default`, `analyze`, `fit` and `audit` may mint the intent. This is inventory v3's `authority == "authoritative-default"` minus `repair-verify`. It is a closed set: a new enum value or recipe cannot widen it.
- **Refusal for commands that cannot create.** `import`, `baseline-upgrade`, `repair-apply`, `test-run`, `native-prepare`, `repair-verify` and any read request that needs I refuse when I is positively absent. The refusal is request-rejected, exit 2, `REQUEST.PRECONDITION_FAILED`, domain detail `INSTALLATION.NOT_INITIALIZED`, with zero effects. Earlier admission failures keep their precedence. Metadata commands and explicit `--ephemeral` never enter this rule.
- **Positively backed-up storage.** `BACKED_UP` requires this invocation's `--allow-backup-custody` before any ancestor or stage effect. Otherwise the request refuses: request-rejected, exit 2, `REQUEST.PRECONDITION_FAILED`, detail `storage.backup-choice-required`. `--ephemeral` is not a creator path.

## Decisions

1. **The intent is not a record.** `CreationIntent` is a private, non-Clone, non-deserializable capability bound to one `InitialInstallationAttempt`, and it is consumed exactly once by the permit (owner step 6). It holds:
   - the command;
   - **(r3, J1 S4)** the invocation's RequestId, lent by the host as `&RequestIdentity`, and a fresh ExecutionId, which the intent draws and reserves before P0 is staged and holds as `ReservedExecutionId` (item 5; J1:288);
   - StepId 0 (see decision 5);
   - the account-derived target bytes;
   - the storage classification and whether this invocation passed `--allow-backup-custody`;
   - the disclosure-delivery receipt.

   Its only durable trace is `OperationInputV1.invocation` inside P0 (466). **(r3)** P0's writer takes the ExecutionId only as `ReservedExecutionId` or its read-only projection (J1:209).
2. **Backup classification, first version.** The pre-installation classifier returns `UNKNOWN` for every target. No selected law names a native backup API, the threat model's signed detector catalog does not exist, and the creator launches no helper (no `tmutil`). The law already admits `UNKNOWN` with a mandatory disclosure, and forbids inventing `BACKED_UP` or `NOT_BACKED_UP`. Consequences:
   - `--allow-backup-custody` is parsed and recorded, but only a positive `BACKED_UP` would require it.
   - Users are told their storage's backup status is unknown. They are never told it is not backed up.

   A positive detector, for example Time Machine configuration and exclusion state, is a later successor. It needs its own evidence and review, and it must fail to `UNKNOWN`, never to `NOT_BACKED_UP`.
3. **Disclosure delivery before effects.** In every output format, the host writes the first-write disclosure to standard error and flushes it before the first creation effect (owner step 5, before fixed ancestors). The disclosure names:
   - retention origin `DEFAULTED` and the durable-unbounded posture, as identity §5 and the golden `default-first-use-durable` disclose them ("retention DEFAULTED durable-unbounded");
   - the actual account-derived storage root (the owner override's addition to that same report);
   - the backup classification (`unknown`).

   A write or flush error refuses the act before effects. That is owner step 1's "failed required delivery refuses". Standard output keeps the single-envelope rule. The envelope's existing `retentionDisclosure` member carries the root and posture. It has no backup-status field, so carrying `unknown` in the envelope is a schema successor owed by 468. Until then the stderr notice carries it. Immediately before effects the host rechecks that the target it disclosed equals the target it will create. A difference refuses.
4. **Acknowledgement retention.** Identity §5 says the backup acknowledgement is kept as operational custody metadata. P0's closed `CreationInputV1` has no member for it, and owner.md forbids a policy store outside I. With classification always `UNKNOWN`, no acknowledgement is ever required. The retention member is owed by the same schema successor as the positive detector. No record invents it now.
5. **Request identity before I.** Identity §1 reserves RequestId and ExecutionId by a uniqueness check in the operational ledger. **(r3, J1 S4; LD3-1)** That is "the corresponding operational ledger", checked before use (IE:77-81). Before I exists, that ledger is process custody (J1 item 2):
   - **RequestId.** The host's process-custody `RequestAuthority` draws it at ingress, before parsing, and reserves it in its registry (J1:190, :195). The host lends it to the creator-class entry as a sealed `&RequestIdentity`, which only the CSPRNG draw mints (J1:194). The intent records it and draws no RequestId of its own.
   - **ExecutionId.** `mint_intent` draws it from the CSPRNG, as before (`crates/security/src/initial_installation.rs:591`). It reserves it in the process-custody `ExecutionIdReservations` before P0 is staged (J1:211). The draw is checked against every ExecutionId already reserved in the process, and a collision redraws, at most eight draws in all. Exhaustion, or a failed draw, refuses on the host-I/O row (468 item 6), as a failed draw does today. The reservation is never released or reused (J1:206-208). This is the registry and rule of X3d r9's reservation at `open` (X3D9 S10.1).
   - **Stated limit.** M3 keeps no durable RequestId or ExecutionId registry. Across processes, uniqueness rests on the 128-bit draw (J1:196, :217). In I, the winner's ledger begins with P0 and is empty before it.

   StepId is not an id: workflows §1 defines it as the zero-based position in the command's step list (0..63). The creation effect is the initialization prelude of the command's first step, not a step of its own, so it records StepId 0. Every step list has a step 0. No step is added to any command. The loser route (EEXIST) writes nothing into the winner's I. **(r3, J1:288)** The RequestId is the whole invocation's: the envelope, every operational record and P0 carry the same one (J1:191-193). The prelude's ExecutionId names the creation act in P0 only, and is never reused. No later operation of the invocation uses it, and it is never bound to the analysis attempt (J1:200, :223, :365).
6. **Two conflicts settled in favour of owner.md, which governs the first creation:**
   - S3.1's "already-admitted host storage-policy record" cannot exist before I.
   - The golden `analyze-backup-choice-required-in-ci` remedy "or select another admitted root" does not apply to the fixed account root.

   The golden wording is corrected by 468's formal diagnostic successors.
7. **Scope of the implementation unit.** 464 delivers, as library code with tests:
   - the closed eligibility table;
   - the single-use intent;
   - the storage decision;
   - the `NOT_INITIALIZED` projection, with security exposing positive absence as a typed, sealed outcome;
   - the disclosure writer with its refuse-on-failure rule.

   It wires no CLI command to an effect. Until 467 composes the creator, `opensip`, `analyze`, `fit` and `audit` keep their present not-implemented refusal. The CLI changes in the unit that enables the creator.

   **(r3)** Items 1 and 5's changes are code in J1 unit J3a: `RequestIdentity`, `ExecutionIdReservations`, and `mint_intent`'s use of them, with J1's tests J-C2, J-C4 and J-C4b (J1:881). X3d r9 places `open`'s reservation in the same unit (X3D9 S10.8).

## Forbidden substitutes

A parsed `persistent` flag; a settings file or environment variable as storage policy; `NOT_BACKED_UP` from a missing detector; an acknowledgement inferred from a TTY or a prompt default; a disclosure written after an effect; a RequestId uniqueness claim from a ledger that does not exist; minting the intent for any command outside the closed set.

## Not claimed

Backup detection, cloud-sync detection, network isolation, CLI dispatch, or creator enablement.
