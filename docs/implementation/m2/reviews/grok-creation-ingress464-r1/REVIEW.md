# Review: creation ingress 464 r1

Grok is the single reviewer. Claude Opus 5.5 leads. Law review of `docs/implementation/m2/creation-ingress-464/PROPOSAL.md`. No repository edits. No product cargo.

The proposal is 6035 bytes, sha256 `83e9488d6ede74bfa3f65081a6aa1f26da5e2038e27032ed43a4f3fdf1411f52`, matching `hashes.txt`. Governing text is owner.md §1a step 1, the first-creation storage paragraph, and §6, with the effective override on identity §5, S3.1, the inventory, `storage_write_admission`, and `Invocation5RetentionDisclosure`.

## Verdict

**REQUIRED-FINDINGS.**

## Answers

Decision 2 is lawful. S3.1 admits `UNKNOWN` with the mandatory unknown disclosure, and that classification does not require the backup choice and is never rendered as not-backed-up. `storage_write_admission` returns `ADMIT` / `unknown-disclosed` for `UNKNOWN` without reading the flag. Owner.md gives backup classification to S3.1, forbids inventing `BACKED_UP` or consent, and forbids a helper on the creator. No selected passage in S3.1 or owner.md names a native backup API. A constant `UNKNOWN` result is the honest classifier for this unit. The flag is parsed onto the intent, and only a positive `BACKED_UP` classification would require it. Every target, including one Time Machine is backing up, is disclosed as unknown and is not asked for `--allow-backup-custody`. A later detector fails to `UNKNOWN`, never to `NOT_BACKED_UP`.

Decision 3 places delivery and the target recheck correctly, and it keeps stdout as one envelope. The notice is written to stderr and flushed before fixed ancestors, in every format. A write or flush error refuses before effects. `Invocation5RetentionDisclosure` already carries `storageRoot` and `policy`; it has no backup-status field (`deny_unknown_fields`), so `unknown` stays on stderr until the 468 schema successor. The target-equality recheck sits after that flush and before effects. With the classifier fixed at `UNKNOWN`, a stronger backup classification cannot appear in this unit. The notice content is the subject of RF-1.

Decisions 4 and 5 are sound for the acknowledgement and for RequestId and ExecutionId. `CreationInputV1` is closed and has no acknowledgement member. Owner.md forbids an outside-I policy store. Under permanent `UNKNOWN`, no acknowledgement is required, so this unit invents no retention record. Identity §1 reserves RequestId and ExecutionId by a ledger check. Before I exists there is no ledger. Those two ids are 16-byte CSPRNG draws (`req1_` / `exec1_` plus 32 lowercase hex). The winner's ledger begins empty at P0, so those first ids are unique there by construction. The loser writes nothing into the winner's I. A later ordinary use of the same ids in the process performs the ordinary reservation first. StepId is the subject of RF-2.

Decision 6 follows owner.md. The effective identity override states that the account root is fixed and that no outside-I policy record exists: the S3.1 "already-admitted host storage-policy record" cannot exist before I, and the alternative-root remedy does not apply. The golden `analyze-backup-choice-required-in-ci` still says "pass --allow-backup-custody, choose --ephemeral, or select another admitted root". That third limb is the conflict, and 468 owns the golden wording. This unit does not emit that situation, because it never classifies `BACKED_UP`.

Decision 7 is right. 464 is the eligibility table, the single-use intent, the storage decision, the `INSTALLATION.NOT_INITIALIZED` projection, and the disclosure writer. It wires no command to an effect. The creator stays disabled until 467. Today an empty `opensip` argv refuses with "Default analysis is not implemented in this development build.", and `analyze`, `fit`, and `audit` refuse with "Unknown command or arguments." Both refusals happen with no creation effect, and this unit leaves them in place.

The three completeness checks are already in the text:

- A TTY gets the same flushed stderr notice as every other format. The unit never classifies `BACKED_UP`, so the interactive backup choice does not arise. The forbidden list bars an acknowledgement inferred from a TTY or a prompt default. Owner.md still allows an interactive explanation only as words; the durable remedy remains restarting with the flag, and CI never prompts.
- `default` and `audit` have no `--ephemeral` flag. `analyze` and `fit` do. An unlisted flag fails inventory admission first. The restated rule says earlier admission failures keep their precedence, so `opensip --ephemeral` and `opensip audit --ephemeral` are that earlier refusal. On `analyze` and `fit`, an admitted `--ephemeral` is the separate no-creator path and does not mint the intent.
- The absence rule already says earlier admission failures keep their precedence, matching owner.md §6.

## Required findings

**RF-1.** The pre-effect notice does not report retention origin `DEFAULTED`. Identity §5 requires the host to report origin `DEFAULTED` and durable-unbounded posture before the first write, and the owner override adds the account-derived root to that same report. The golden `default-first-use-durable` records the disclosed phrase as "retention DEFAULTED durable-unbounded". Decision 3's notice names the root, the durable-unbounded posture, and `unknown`. The stdout envelope that carries `retentionDisclosure.provenance` is the single final envelope, so it is not the before-effect report.

**RF-2.** `StepId` is not a CSPRNG id. Workflows §1 defines it as the zero-based position in the command's step list, and `InvocationBinding.stepId` admits only an integer 0..63. Decision 1 puts a fresh StepId on the intent beside RequestId and ExecutionId, and decision 5 says the creator's ids are CSPRNG draws. Owner step 1 places the creation effect before the named steps, and the proposal names no position for that effect.

Do not commit.
