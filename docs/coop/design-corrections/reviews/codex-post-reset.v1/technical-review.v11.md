# Codex technical review of proposed v11 corrections

Standing: coauthor/integration assessment, **not independent acceptance or implementation readiness**. The actual completed v10 independent review is CHANGES_REQUIRED: zero MUST, one SHOULD v10-S1 and three advisories. Its exact JSON SHA is `64e15aff50d77f0f84b53c145acc6a46d208afe0a1e090272d5deaf25ca3e8f9`. The original reviewer custody.json is preserved verbatim; Codex's additional receipt is codex-retention-custody.json. All 2,502 frozen files verified before/after/final, and all six commands, logs and deterministic reports were reproduced byte-identically.

## Correction and actual collaboration

The independent review resolves v9-S1 and confirms the effective-annotation cases from v10, but finds a remaining same-path aggregation defect. `record()` merged incoming annotations before testing their absence. An annotated sighting followed by an unannotated sighting admitted, while the opposite order refused. The reviewer proved this both with referenced-container/local-property occurrences and with a pure JSON key-order swap between items and additionalProperties. Every hypothetical schema passed the metaschema, and positive controls discriminated. The full 661-check authored suite reached the merge zero times: the earlier oneOf fix separated branch paths, so passing those tests did not exercise this merge.

Actual Claude coauthor session `5dec928a-6357-4726-9ea8-49a3079fb726` corrected an isolated frozen-v10 copy while the independent reviewer completed its review. Neither live nor frozen candidate files changed during those passes. Codex retained the successful final coauthor response, exact released sources and public tool evidence, then applied only its two-file delta after both passes completed. Full before-images and source hashes are in `released-coauthor-delta.v11/`.

The corrected reference keeps missingness as an explicit monotonic fact alongside the accumulated annotations. Once an occurrence at a location lacks an annotation, no later annotation can erase that absence. The merge uses typed equality for annotation deduplication, matching conflict checks. All earlier missing-annotation, retention, join, alias, branch, terminal exclusion and join-addressing controls remain in force. New actual pre/post measurements discriminate four negative cases, and all-lawful controls remain admitted. This remains schema/reference consistency for reviewed future registry edits, not a current payload or Run attack: shipped closed selectors have no unannotated governed fields or same-path collisions.

## Normative wording, settled before the blind pass

Codex chose to address the independent v10-A1/A2 advisories now, preserving their original nonblocking severity. The supported inheritance and conflict rules must be discoverable from the normative subset supplied to the next blind consumer, without reading author Python. Codex proposed a paragraph in the existing identity-and-evidence contract. Claude substantively checked it, identifying that exemption reasons are an authoring disclosure expectation while reference admission validates retention rather than prose presence or content. No `reason` key was invented. Codex accepted that distinction and explicitly limited the non-governed-property clause to top-level selector properties, matching the direct second pass; Claude measured and acknowledged that correction too.

Claude then read the exact final 2,825-byte insertion, SHA `32db349536ffc74081b5081aa698f9966d100485268fc24822fde2a1a94cd13f`, and confirmed that it accurately states the corrected reference. Codex applied those exact bytes with full contract before/after custody in `normative-annotation-clarification.v11/`. Earlier draft notes and handoffs remain distinct evidence; no agreement is inferred from an earlier unread version. The coauthor did not read the full completed independent v10 review and does not claim to have done so; its substantive p02/p03 and exact wording assessments have their own retained scope.

The insertion states governed forms, supported local-reference/container/branch traversal, annotation inheritance with terminal-type exclusion, per-occurrence coverage, monotonic missingness, conflict refusal, declared retentions, top-level join addressing, and the distinction between schema coherence and owning-fact truth. The raw registered schema documents and registry bytes are unchanged, so this normative prose does not change their identity preimages. The prospective application tooling is separate and still requires independent application review.

## Final-source verification

Five Codex rechecks pass on the exact released source:

- `annotation-aggregation-final-recheck.v11/`: eight metaschema-valid cases cover both original order arrangements, all-annotated positive controls and single-occurrence controls; missing occurrences refuse with the intended cause.
- `annotation-coverage-final-recheck.v11/`: all 13 actual selectors admit; 39 injected governed fields and a removed existing annotation refuse; the two earlier residue rules retain their intended causes.
- `annotation-traversal-final-recheck.v11/`: referenced containers and both original branch orders refuse missing annotations while the actual document admits.
- `annotation-alias-final-recheck.v11/`: missing alias annotation refuses; field-local and intermediate-alias annotations admit.
- `annotation-inherited-limbs-final-recheck.v11/`: all nine field/alias/branch retention and join cases match their expected refusals and lawful exemptions.

The integration fixture is extracted from the released checker with its exact source hash and explicit declaration list; synthetic composition remains distinct from an independent oracle. All four consuming pin sets are refreshed against their current inputs. The six final executed commands pass, with logs, source hashes and scripts retained in `final-reference.v11/`; the validation summary records their measured counts. These are authored/reference results, not independent acceptance.

## Limits and remaining acts

The coauthor's failed insertion and incorrect first three-occurrence fixture remain disclosed. A duplicated comment already in frozen v10 was restored exactly rather than silently tidied. The corrected three-occurrence construction uses a two-level reference chain; an allOf branch would have a different location. Earlier failed neutralisation and reviewer harness attempts remain literal historical evidence. The reviewer initially checked 31 protected files against a scoped snapshot, then correctly checked them against the repository; all 31 are unchanged. Its p01 removal tally includes non-governed UInt64 byteLength, whose annotation removal is not a third-limb missing-governed-field refusal.

The 28 carried v5-v10 advisory dispositions are explicit. L1-L3 normalization and level-specification fixture assets remain unqualified. No clone facts alone exempts Coverage prerequisites. Complete-ledger comparison and actual host/renderer failure wiring remain implementation obligations. All AR/FW, inherited residual and scoped-review routing obligations remain accounted; all 32 qualification gates remain undemonstrated. D-371 already selects the complete intended-product scope; the remaining unapplied correction/readiness act is D-372. The v10 review's shorthand D371/D372-unapplied statement does not undo that existing selection.

A fresh independent review of frozen v11 at zero unresolved MUST/SHOULD, actual Codex assent, a NEW fresh blind consumer on those accepted normative bytes, and complete independently reviewed application/readiness reconciliation remain required. This technical assessment authorizes no product implementation, commit or push.
