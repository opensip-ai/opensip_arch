# Creation ingress and storage choice for the initial creator — proposal 464 r2

2026-09-26. Claude Opus 5.5, implementation lead. Law for unit 464 (`CreationIntent`), under owner.md §1a step 1, the first-creation storage choice paragraph, and §6. It closes the points owner.md leaves to the implementation and settles two textual conflicts. Not code, not creator authority. The creator stays disabled. r2 answers Grok 464 r1 RF-1 (the notice omitted retention origin) and RF-2 (StepId is a position, not a draw). r1 bytes are preserved in PROPOSAL-r1.md. ACCEPTED by Grok 464 r2 on 2026-09-26.

## What owner.md already fixes (restated, unchanged)

- **Eligibility.** Only `default`, `analyze`, `fit` and `audit` may mint the intent. This is inventory v3's `authority == "authoritative-default"` minus `repair-verify`. It is a closed set: a new enum value or recipe cannot widen it.
- **Refusal for commands that cannot create.** `import`, `baseline-upgrade`, `repair-apply`, `test-run`, `native-prepare`, `repair-verify` and any read request that needs I refuse when I is positively absent. The refusal is request-rejected, exit 2, `REQUEST.PRECONDITION_FAILED`, domain detail `INSTALLATION.NOT_INITIALIZED`, with zero effects. Earlier admission failures keep their precedence. Metadata commands and explicit `--ephemeral` never enter this rule.
- **Positively backed-up storage.** `BACKED_UP` requires this invocation's `--allow-backup-custody` before any ancestor or stage effect. Otherwise the request refuses: request-rejected, exit 2, `REQUEST.PRECONDITION_FAILED`, detail `storage.backup-choice-required`. `--ephemeral` is not a creator path.

## Decisions

1. **The intent is not a record.** `CreationIntent` is a private, non-Clone, non-deserializable capability bound to one `InitialInstallationAttempt`, and it is consumed exactly once by the permit (owner step 6). It holds:
   - the command;
   - fresh RequestId and ExecutionId;
   - StepId 0 (see decision 5);
   - the account-derived target bytes;
   - the storage classification and whether this invocation passed `--allow-backup-custody`;
   - the disclosure-delivery receipt.

   Its only durable trace is `OperationInputV1.invocation` inside P0 (466).
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
5. **Request identity before I.** Identity §1 reserves RequestId and ExecutionId by a uniqueness check in the operational ledger. Before I exists there is no ledger. RequestId and ExecutionId are CSPRNG draws. StepId is not an id: workflows §1 defines it as the zero-based position in the command's step list (0..63). The creation effect is the initialization prelude of the command's first step, not a step of its own, so it records StepId 0. Every step list has a step 0. No step is added to any command. The winner's ledger begins with P0 and is empty before it, so uniqueness is established by construction. The loser route (EEXIST) writes nothing into the winner's I. If a later ordinary operation in the same process ever used these ids, it would have to perform the ordinary reservation first.
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

## Forbidden substitutes

A parsed `persistent` flag; a settings file or environment variable as storage policy; `NOT_BACKED_UP` from a missing detector; an acknowledgement inferred from a TTY or a prompt default; a disclosure written after an effect; a RequestId uniqueness claim from a ledger that does not exist; minting the intent for any command outside the closed set.

## Not claimed

Backup detection, cloud-sync detection, network isolation, CLI dispatch, or creator enablement.
