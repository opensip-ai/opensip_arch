The review is complete. Final state of this generation:

## Verdict: CHANGES_REQUIRED

**Not ACCEPT-RECONSTRUCTABLE** — not because work is missing, but because two SHOULD-level design gaps remain unresolved. All 131 non-future requirements are now executed (0 unexecuted), and all 3 future-qualification items are recorded as not-demanded.

## Binding

| | |
|---|---|
| sessionId | `79569ae1-10f4-4181-972b-334f7ed2f07a` |
| ancestry | consumer-b.v14 → v15 → v16, one continuous origin |
| subject manifest | `6aad82e65623c7204008c19fdbea0aee84c302c0ef225c57647cd3e75e4a3cc6`, 101/101 PASS |
| parent digest declared in it | `1d2fc1b9128c902cef092ef7c0b769b5cd6a2019010a1bcfd1adf33711c6c85b` — **declared-digest comparison only, not a whole-candidate verification** |
| only changed kit file | `native/native-evidence.schemas.v2.json` |
| from-scratch command | `…/bin/python -I -B …/consumer-b.v16/output/lib/verify_all.py` → **28 stages, 0 failed** |

All five Runs were **reconstructed and resealed from the new kit** (not relabelled): closure 616/778/844/508/549 checks passed with 0 refusals, fresh-process `REPLAY_MATCH` each, 14 tamper/identity controls each, plus 22 native-join, 11 policy-admission, 6 clone, 4 hidden/mismatch and 7 graph-query failure controls. Relocation controls prove the selected graph identities are location-free.

## What the v16 work added

- **Invalid-disabled-policy as a distinguishing control**: 1 positive (valid disabled rule admits, records `disabled` + empty arrays) and 10 negatives, each refusing at the *intended law at the intended boundary* — schema / evaluator-admission / retained-closure reported separately. This surfaced a masking defect in my own checker: an unregistered relation was being reported as a ladder failure, now split into `ATOM_RELATION_IS_REGISTERED` first.
- **Phase 4 completed**: 6/6 advertised modes have an admitted representable path (three only at record level — stated, not merged into the complete-positive claim).
- **Phases 6/7/8, hidden-mismatch, graph query** all built and measured.
- **Graph query found a real endpoint gap in my own Run**: it retained no `TargetAttributionV2`, so an endpoint=target query could only have been answered by parsing an opaque id the schema forbids parsing. The omission was *lawful* (occupancy-unknown); I added provider-attested sidecars and 34 new closure joins rather than guess.

## Honest findings

**0 MUST.** 2 SHOULD: the repair `closedWorld` projection doesn't say which Coverage entry owns it when a Run holds several (it changes `repairplan2` and the unsafe-edit gate); and `GlobPattern` doesn't decide whether a *trailing* `**` matches that directory's files (it changes edit-scope admission and subject enumeration). Both were measured around without inventing a rule. 2 advisories. My earlier `fragment` SHOULD is **withdrawn as over-broad** — measured: zero fragment sites.

Two helper bugs found and corrected from the kit alone (cross-document `$ref` base not followed; runtime path in a semantic label), with original failures preserved. No root admission, product qualification, implementation, commit or push is claimed; v14/v15 verified untouched.
