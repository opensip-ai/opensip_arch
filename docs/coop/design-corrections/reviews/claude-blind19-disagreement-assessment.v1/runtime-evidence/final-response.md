Bounded diagnosis complete. `assessment.md` and `assessment.json` are written; 17 probes, all exit 0, with full stdout/stderr receipts and 21 evidence hashes.

## Verification

Manifest `3897e8d1…10bf2` matches; all five exact exports recomputed to their declared hashes; every owner file I read matches its manifest row.

## The four execution-input differences

Three fault keys across five runs reduce to four root differences. **Two resolve against the frozen reference, not the consumer.**

**F1 — `inapplicable-vcs` account `sourceUniverse` (all five runs): missing normative law.** Applicability *agrees*; only the universe differs. The rule `want_u = None if want_app in (unavailable-unselected, unavailable-null-universe) else uni` lives at `execution_inputs_model.v1.py:1140` and in the synthetic fixture at `:273` — and **nowhere else**. Contract §5:81 governs envelopes only; `NativeCoverageAccountV1` makes the field required-and-nullable with no applicability conditional; a corpus search for any published tie returned **0 hits**. The consumer's rule ("null when there is no Coverage") is self-consistent across all 33 accounts. This difference alone refuses all five runs.

**F2 — UNSUPPORTED-TYPED *and* unselected (syntax-code): ambiguous.** The published precedence law (`absenceProjectionAndPrecedence`, §10) orders the **pair**, and the consumer's derived pair already matches it. No text orders the applicability **enum**. Separately, native says such cells are "answered by disclosure rather than **omitted**" — and the consumer omitted this one while *answering* the equivalent cell in syntax-data. It is internally inconsistent.

**F3 — UNSUPPORTED-TYPED with lawful Coverage (syntax-data): consumer defect, plus a doc gap.** Its native evidence is exactly right — `unknown` / `language-tier-unsupported` / `capability-missing`, precisely what `native-evidence.md:3183` prescribes. Only the account token is wrong; I confirmed executably that a conforming shape exists. The gap: under it, the lawfully minted Coverage is referenced by no account and the outcome discloses no carrier. The syntax-data `CAUSE_CARRIER` is purely derivative of this.

**F4 — `clones-fact` carrier (four cells): reference defect.** I computed the owner's own census: where expected subjects are missing *and* the Coverage record carries no pair, `_summarize_coverage_records:614` takes `… or "provider-unavailable"` and **invents** a carrier. Contract §4 says the pair "must actually occur on a source record… not a rewrite as generic `provider-unavailable`", and §5 says "do not manufacture a carrier". The discriminator is decisive: rust-partial and syntax-data don't fault *because* their Coverage carries a real pair. The consumer documented this deliberately (V18-D7/D8).

I corrected myself here: an early stub of mine suggested `clones-fact` derives `complete`. The frozen owner does implement the census, and root's preliminary reading was right.

## Query and mutation scope

Q1 `truncated=true` **confirmed** against §5's "Page fullness is `truncated-page`, `truncated=false`". Q2 cursor `ord:1` **confirmed substantive** — schema-valid but structurally unable to carry the published bind, so `QUERY.CURSOR_MISMATCH` is unimplementable. Q3 **confirmed** — the typescript Run has `ts:node_modules/left-pad/index.d.ts` as a resolved import target, absent from `admittedMembers`. Q4 **split**: **refuted** in the query artifact (`req1_abab…` matches the pattern; no `stepId` at all), **confirmed** in `mutation-keys.json`, where `requestId: "req-7f3a1c"` and `stepId: "step-2"` are schema-invalid against `MutationReplayScopeV1` — so the declared idempotency key is `H` over a preimage that cannot be admitted.

## Reopening

**Yes, bounded — F1 and F4**, both frozen32 owner defects. F3 is consumer-side but needs a doc fix; F2 needs a published decision. Root's scope-enumerator/foreign-U hypotheses found no support in anything I traced, and I make no claim either way.
