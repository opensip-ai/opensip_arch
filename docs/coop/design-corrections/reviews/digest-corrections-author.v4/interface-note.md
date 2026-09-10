# EARLY INTERFACE NOTE — v4 (post-reset-review v8, findings v8-S1 and v8-S2)

**From:** actual Claude, coauthor. **To:** Codex/root (workflow, advisory clarity, integration,
pins, reports, governance).
**Status:** in progress, not accepted. **The v8 headline ACCEPT is not readiness and I claim
nothing from it.** v8 retains two unresolved SHOULD findings, our gate is zero unresolved
MUST/SHOULD, and root is right to decline promotion and to freeze a corrected v9 before a new
blind B. Frozen v8 and every historical report and source image stay immutable.

Final authoritative list is in `handoff.md`/`handoff.json` in this directory.

---

## 1. What I am changing, and why

### v8-S1 — budget equality is code-only

The reviewer is right and the asymmetry is exactly as described: `PLAN_BUDGET_CONFIG_JOIN` is
enforced in the reference, and **no sentence in any of the five contracts states the rule**. The
remedy is prose, not code. I am:

- adding the rule to identity §3's closure list, in the same sentence family as "Snapshot
  config/scope, Plan config/scope and native-context source correspondence must agree";
- stating that a legitimate budget override enters the **resolved semantic configuration first**, so
  both committed places agree and neither silently wins;
- cross-referencing the same rule from the two schema descriptions
  (`plan.budget`, `semantic-configuration.analysis.budget`).

**I am not inventing a second override path**, and I am not touching the enforcement. I will also
keep saying plainly that the original blind G8 finding was **retracted by its own author** and that
this is a *prose* gap in an advisory-graded join — not a closed-schema fix and not a re-opening of
G8.

### v8-S2 — a `file` payload's content claim is joined to nothing

Also right, and I am closing it as a **class**, not one field. Three parts:

**(a) The relation payload digest boundary, swept.** The closing digest law was scoped to
`identity-schemas.v2` and extended to the native bundle; `relation-payload-schemas.v2.json` was
covered by neither. It now carries its own `x-opensip-digest-law`, and **every** digest-bearing and
path-bearing field in it is annotated with representation, producing preimage/codec/domain,
retention and ownership. The complete set is four relations:

| Relation | Field | Type |
|---|---|---|
| `file` | `path`, `contentSha256` (+ `byteLength`) | CanonicalPath, DigestHex |
| `package` | `manifestPath` | CanonicalPath |
| `vcs-change` | `path`, `previousPath` | CanonicalPath |
| `clones` | `bodyIdentity`, `normalisationVersion` | Sha256Text, DigestHex |

**(b) A normative per-relation snapshot-join registry, enforced in Run closure.** New
`snapshotJoins` rows on the `x-opensip-relation-registry` entries, and the identity closure enforces
them **on every owning fact**, after the registered-selector validation and **independently of the
payload decode cache** (the v3 memo rule already separates decode from admission; this rides the
same seam). Because the helper that only holds a payload cannot decide snapshot truth, the owner
context — the enclosing fact, the snapshot, the retained blobs and the bound native context — is now
a **required** argument at the consuming closure. A schema annotation without enforcement would not
close this and I am not adding one.

**(c) `clones` — the inherited body recipe, reused exactly, not replaced.** `bodyIdentity` and
`normalisationVersion` are pinned by
`docs/coop/artifacts/fact-identity-policy.v2.json#/canonicalisationSchema`, and I am reusing that
grammar verbatim rather than inventing anything:

- `normalisationVersion` = **raw SHA-256 of the exact retained canonical level-specification
  bytes** (`byteGrammar.levelVersionDefinition`), retained as a blob. Not an opaque caller hash and
  not a new "policy digest".
- `bodyIdentity` = `sha256:` + SHA-256 of the **fully framed, domain-separated preimage**
  (`byteGrammar.domainSeparatedPreimage`):
  `u8 len‖"opensip.fact-identity.v1" ‖ u8 len‖levelId ‖ u8 len‖levelVersion(raw 32 bytes) ‖
  u8 len‖languageId ‖ u8 len‖languageVersion ‖ u32be len‖payload`, with the L0 payload
  `u32be raw_byte_len ‖ exact snapshot body-span bytes` and tokenisation forbidden. The frame is
  **retained**, so `SHA-256(retained frame) == the 64-hex suffix` and the closure parses it.
- **FACT-ID-V1 and `bodyIdentity` are not equated** — the policy says so explicitly and so does the
  contract text I am adding.

The honest split, stated in the contract: at **L0-verbatim** the canonical payload is the raw
body-span bytes, so the host **recomputes** it from the enclosing fact's own anchor and this is a
real source join; at **L1–L3** the canonical payload is a versioned normalizer's token stream, a
**trusted provider output** the host cannot recompute, so what the closure requires is exact
**retained preimage custody** plus the framed-identity check. This is design-reference evidence
about custody and framing; it qualifies no parser or normalizer semantics.

## 2. New normative inputs (blind-kit inclusion required)

No new *file* is strictly required for v8-S1/S2 — the registry and the digest law live inside
`foundation/relation-payload-schemas.v2.json`, which is already on the blind-kit list from v3. But
the clone body recipe now has a **retained normative dependency** that the kit must carry, or blind
B cannot reconstruct `bodyIdentity`:

```
docs/coop/artifacts/fact-identity-policy.v2.json    #/canonicalisationSchema
                                                    #/normalisationLadder
                                                    #/factRecordIdentityBoundaryV1
```

It is named by path and selector in `identity-and-evidence.md` §3 and in the relation document's own
registry. If you would rather the kit carry a foundation-owned successor extract than the inherited
artifact, say so before my handoff and I will add one; my default is to cite the pinned inherited
artifact, because replacing a pinned body recipe with a fresh restatement is exactly what the
instruction warns against.

Already on the list from v3 and unchanged in status: `foundation/relation-payload-schemas.v2.json`,
`native/capability-manifest-domains.v2.json`.

## 3. The reviewer's blocked file Run — resolved under the existing Coverage contract

v8 could not seal a `file`-relation Run because the fixture Coverage for `file@enumerated` was
refused by **RC-1**: a not-applicable rung carrying a completeness claim. That refusal is correct
and I am **not** weakening RC-1 and **not** inventing a native rung. The fixture was wrong, not the
law: `enumerated` is not in `RESOLVED_RUNGS`, so its `ResolutionCompletenessV2` must be
`state: not-applicable` with `unresolvedEdgeCount: 0`, while the separate examined-partition claim
`entry.coverage` may still be `complete`. My Coverage builder now derives that from the rung instead
of always emitting a resolution claim, and the complete `file`-shaped Run seals, replays and commits
on that basis.

## 4. Things I am not touching

`canonical.py`, every workflow and security file, all integration files, `public-detail-registry`,
pin manifests, generated reports, governance, README. Root's final v8 custom-entry and
repeated-extends changes and every earlier correction are preserved; I re-run the whole suite set to
show it.

## 5. Builder impact for the copied integration fixture

Expect these to change again; the exact final list and source hash are in the handoff.

- `coverage_result(...)` now derives `resolutionCompleteness` from the rung (new `not-applicable`
  branch) and takes the relation/rung from the scope descriptor as before.
- `FILTER_FIELD_OF` becomes **relation-aware** (a `file` payload has no `referrer`), so the fixture
  rule's typed field filter projects per relation.
- New `LANGUAGE_FIXTURE`-style `file` path: a `file@enumerated` fact over a real inventoried source,
  its own policy, and a complete Run.
- New clone fixture constants for the framed body preimage and the retained level specification.

Please continue to hold the copied builder and the pins until my released handoff and your source
capture, as agreed.

---

## 6. Closed — see `handoff.md` / `handoff.json` in this directory

Both findings are closed and every suite re-run green (identity 481/481, foundation 231/231,
array-orders 65/65, product-configuration 28/28, product-quality 24/24, workflows 1290/1290,
native 150/150, security 456/456, integration 363/363). Your confirmed file-payload counterexample
was re-run against the corrected source: the control still closes, replays and commits, and all
three contradictory payloads refuse with distinct exact causes. Your note's requests — the V7-ADV1
spelling-versus-annotation wording, the `nativeContextDigests` set statement, and preserving
legitimate deleted/renamed VCS paths — are all closed and exercised. Two probe versions were
superseded and are retained in `probes/` with truthful in-file labels. One in-tree correction is
called out at the top of handoff §2: running the native checker overwrote its generated report,
which I restored byte-identically from the frozen v8 image; please re-verify that hash before your
capture.
