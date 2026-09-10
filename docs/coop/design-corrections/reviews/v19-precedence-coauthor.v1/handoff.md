# S1.2 scope-capability precedence — bounded source coauthor assessment

Source coauthorship, not independent acceptance. The contract under `inputs/` is a
**proposed snapshot** of the main coauthor's in-progress M1 work — not published,
released, frozen or accepted. Its active workspace was not read or modified.

## Assent: root is right, in two distinct ways

**1. "applied first at Run closure" is no longer accurate unqualified.** `close_run`
admits the Coverage record at the **producer** boundary before any of its own
prerequisites: `identity-model.py:1547` calls `admit_coverage_result_v3(…, _scope_dialect)`
and `:1549` raises `COVERAGE_PRODUCER_ADMISSION`; `coverage_dialect_prerequisite`
(`:1551`), `syntax_capability_prerequisite` (`:1552`) and
`coverage_source_variant_prerequisite` (`:1560`) all follow. The sentence is true only of
closure's *own* prerequisite sequence — where the grammar guard does still precede the
suffix backstop (`:1553-1559`) — and false as a claim about which boundary decides first.

**2. "keeps its own refusal names" is true only where scoped.** For a `clones` scope over
a path no dialect table lists, the deciding name is now `COVERAGE_PRODUCER_ADMISSION`
wrapping `native.coverage-source-variant-*`
(`native_evidence_model.v2.py:1381/1384/1387`), not `SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE`
(`identity-model.py:837`). `check-identity.py` documents the move at `:2502-2508` and
asserts both new names at `:2509-2516`; the grammar guard's own control was re-pointed at
`:2368-2373` to `declares`/`README.md` and `references`/`src/plain.rs`.

**Why the producer boundary gets there first is scope-shaped, not precedence-shaped.** It
judges one record and never sees the snapshot (`:1366-1371`), so it applies the
source-variant law only where the scope carries its own paths: `universe_dialect` present
**and** `bodyIdentityJoin` in the relation row **and** `subjectKind == source-path`
(`:1372-1374`) — i.e. `clones`. The `symbol` branch is deferred to closure by design.

**One refinement to root's framing.** "An unsupported suffix is now rejected earlier"
holds for that body-identity `source-path` case only — not for unsupported suffixes
generally. A `declares` scope over `README.md` is a `symbol` relation, reaches no producer
branch, and is still decided by the grammar guard under its own name. The replacement
states the enabling condition rather than a blanket "earlier".

**Fault class, as far as I checked:** the disclosed outcome is unchanged —
`check-identity.py:2491-2498` closes the mixed Markdown clone Run as `run2:` with
`coverage=unknown`, `language-tier-unsupported`, `capability-missing`. Both names are
internal `AdmissionError` strings, not public detail codes. I did not re-derive the S10
public projection and claim nothing beyond this. No precedence is altered by the new
text: it describes the order the sources already implement.

The paragraph's purpose is preserved — selected-grammar law versus the closed-suffix body
law at `scopeCapabilityLaw`, TypeScript as the only-such-law case, and the strictly-weaker
implication (corroborated by `:2533-2536`, where `.tsx` stays in the dialect table while
its grammar row is dropped).

## Paragraph

`native-evidence.md` lines 406–418, blank-line bounded, occurring exactly once.

| | bytes | chars | lines | max width | sha256 |
|---|---|---|---|---|---|
| `before-paragraph.md` | 905 | 900 | 13 | 80 | `8bd1d8fb6486319100217cd835ce3fae923091574df353cb3a2495630104e508` |
| `after-paragraph.md` | 2110 | 2099 | 28 | 80 | `5f51b7651387ae53a1c8a5f8930846990deeb0367e383a5bcee1b581327f47ea` |

Valid UTF-8; the only non-ASCII characters are the two the paragraph already used
(U+00A7 `§`, U+2014 `—`). `build.py` asserts the paragraph occurs once, that splicing
yields the replacement exactly once, and that reversing restores the input byte-for-byte.
Spliced-contract sha256 `e2950dec2ed31cafc694b2ab666e68c09aa4db2140dfd0e490711fa1e6a8e492`
is **rebase arithmetic only, not written here** — valid only if the surrounding bytes are
still the captured ones.

## Remaining concerns

- The producer branch is conditional on the caller supplying `universe_dialect`
  (`:1370-1371` states the honest extent). The replacement says "whenever the caller hands
  it the owning universe's dialect, as Run closure does" rather than asserting it always
  fires. Re-check that clause if the final bytes make it unconditional.
- Cited line numbers are snapshot-relative and will move; the function and refusal names
  are stable — re-locate by selector.

## Source hashes (all five match `input-custody.json`)

`native-evidence.md` `4a6e5c97…afa97` · `identity-model.py` `09e35a8c…fd0b1` ·
`check-identity.py` `74abe11e…c87d5` · `native_evidence_model.v2.py` `4b38cc66…1af8` ·
`identity-schemas.v2.json` `c0831e2b…97d1`

Wrote only `/tmp/opensip-design-corrections/v19-precedence-coauthor.v1`. No model,
checker, schema, S10, S14 or suffix table touched; no suite run, no environment created,
no execution claimed.
