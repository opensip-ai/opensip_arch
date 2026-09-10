# bv3-corrections-author.v3 — focused M3 correction handoff

**Standing.** Design/schema/reference correction only. Not product implementation,
commit, push, publication, readiness or product qualification. I am the
correction author, not the independent reviewer and not the blind consumer, and I
confer no acceptance. Codex must recheck these final bytes and decide assent;
fresh independent review, a NEW blind consumer and the full application review
remain separate required acts. No synthetic fixture here is a real parser,
compiler or OS measurement.

- `sourceRoot`: `/tmp/opensip-design-corrections/bv3-corrections-author.v3/work`
- Started byte-identical to released v2 (2981 files, 0 differences).
- **`delta.aggregateVsFrozenV12`: 20 changed, 0 added, 0 deleted** — field keys
  `path`, `beforeSha256`, `afterSha256`, `afterBytes`. Integrate directly from v12.
- **`delta.thisTurnVsV2`: 6 changed** — field keys `path`, `v2Sha256`, `finalSha256`.
- All pins and generated reports in released work **equal frozen v12** (144 such
  files checked against the manifest file; 0 divergent). `integration-fixtures.py`
  is **not** in the delta.

## 0. Correcting my v2 claim, and the read-scope

My v2 handoff asserted that under the syntax universe a clone or code-construct
request against a data grammar is *"explicitly unavailable — never a complete
empty clone result"*. **That was false against my own final source.** I ran
root's inspectors on my released v2 and reproduced the opposite. I had enforced
the registry on grammar **descriptor class declarations** only and then wrote as
though that settled fact and Coverage admission. It does not.

I also confirm the custody point: my last full public-note Read was
**08:07:33.573 UTC**. The 08:16 M3 counterexamples and the emitted domain-count
item arrived afterwards and were **not** assessed in my v2 handoff, so that
handoff's broad no-disagreement statement is limited to the earlier bytes. The v2
handoff and all prior evidence stay byte-identical; this is the additive
correction.

## 1. CX-BV3-SYNTAX-CAPABILITY-1 — closed at both actual Run boundaries

**Reproduced first.** All eight cases on my own released v2, root's exact
inspectors: two valid controls, six defects.

**Root cause.** The closed registry was consulted only by `admit_native_context`,
which validates a **descriptor's declared `syntaxClass`**. Nothing consulted it
when a `fact2` or a requested-scope `coverage2` was admitted, so it constrained
what a bundle may *say about itself*, not what a Run may *claim*.

**The law now binds two boundaries.** Neither consults the claimed coverage
value, the caller-declared class, or whether facts exist:

- **Every admitted fact** — every **anchor path** must be read by a **selected**
  grammar **row** whose registry capabilities contain that `relation@rung`
  (`SYNTAX_CAPABILITY_UNSUPPORTED_FACT`). Anchors are the files the bodies were
  actually read from, so this refuses in a mixed repository too.
- **Every requested scope, including empty views** — judged on the scope's own
  extent, per the published `subjectKindLaw` (below). Inventory capabilities are
  **always** available and never grammar-gated.

**An unavailable request is disclosed, not answered, and not refused outright:**
`coverage: unknown`, `deficiency: language-tier-unsupported`,
`nativeCause: capability-missing` — existing vocabulary, now mapped in §10. A
false `complete`, a wrong or null cause and a wrong deficiency each refuse with
their own reason. The capability is **not** eliminated and no syntax Run is
blanket-indeterminate.

| root's case | released v2 | final |
|---|---|---|
| `README.md` `file`, fact | ADMIT complete | **ADMIT complete** (control held) |
| `src/plain.rs` `declares`, fact | ADMIT complete | **ADMIT complete** (control held) |
| `src/plain.rs` `clones`, fact | ADMIT complete + ownership cause | **ADMIT complete, no deficiency** |
| `README.md` `declares`, fact | ADMIT | **REFUSE** `…UNSUPPORTED_FACT` |
| `README.md` `declares`, empty | ADMIT **complete** | **ADMIT** `unknown`/`language-tier-unsupported`/`capability-missing` |
| `README.md` `clones`, empty | ADMIT **complete** + ownership cause | **ADMIT** disclosed indeterminate |
| `references@resolved-binding`, fact | ADMIT | **REFUSE** `…UNSUPPORTED_FACT` |
| `references@resolved-binding`, empty | ADMIT **complete** | **ADMIT** disclosed indeterminate |

**The four relations that were "not findings" are now real controls.**
`imports`/`calls`/`types`/`reachability` previously failed at
`FIXTURE_RELATION_UNKNOWN` **before** admission. I did not count them either way;
instead I gave each its registered payload and top rung so the guard is actually
**reached**. All four now refuse at `…UNSUPPORTED_FACT` with a fact and disclose
correctly when empty. One case is honestly excluded: `README.md` + `clones` +
fact fails at `FIXTURE_NO_ADMISSIBLE_PAYLOAD` during construction, and a
constructor refusing to build a graph is not evidence about admission — it is
recorded as the construction limit it is, with the guard exercised directly.

**Compiler universes are untouched.** All eight relations, including all five
semantic ones, still close under both `typescript` and `rust` — asserted as
sixteen explicit controls.

## 2. The two concerns in the v3 public note — both reproduced and closed

**Selected-row suffix ownership.** `syntax_universe_selection` reduced the
admitted rows to a set of `languageId`s, losing the rows' own `suffixes`. The
descriptor lets a row own a **subset** of its language's bundled suffixes and
lets two rows of one language own disjoint suffixes; admission only checks that a
claimed suffix belongs to that language and is not claimed twice. I confirmed the
information loss directly: `syntax_capability_support({typescript}, declares,
syntactic, ['a.tsx'])` returned supported. Support is now decided by the **actual
selected rows and their own suffixes**, longest match over their union so `.d.ts`
still resolves through a `.ts` row. Full Runs through the **admitted retained
context**: a `.tsx` fact with a `.tsx`-owning row admits; a `.ts` fact still
admits when `.tsx` is unowned; a `.tsx` fact **refuses** when no selected row owns
`.tsx`. I did not adopt the alternative compatibility change (requiring every row
to own its language's full suffix set) and say so rather than relying on the
fixture happening to list them all.

**Scope path law.** A `README.md`-only clone scope in a **mixed** snapshot
admitted `complete` because the whole-snapshot `any(readable)` was satisfied by an
unrelated `src/plain.rs`. Guard A now uses the scope's **own** paths where the
published law supplies them. The relation registry publishes `subjectKind` per
relation plus a `subjectKindLaw`: `source-path` for `clones`, `file` and
`vcs-change` — bound through their `snapshotJoins` `pathField` or, for `clones`,
the single `bodyIdentityJoin` anchor — `package-name` for `package`, `symbol` for
the rest. For a `source-path` relation **every** named subject must be supported,
so a mixed scope cannot hide its unsupported part. Verified end to end: that
scope now yields the disclosed indeterminate, in a snapshot that demonstrably
still contains a `.rs`/`.ts` file.

**The symbol limit is stated, not worked around.** For `symbol` relations the
subjects are opaque `SubjectIdV1` values the record associates with no path; the
enumerator's symbol-to-file attribution is **trusted** and not re-derivable from
the retained Run. So only the coarser extent question is answerable, and a
mixed-repository empty `declares` scope remains admissible. Treating a symbol id
as a path would reject lawful code scopes; inventing symbol-to-path parsing would
be fabricated evidence. This is published in `subjectKindLaw` and in §1.2.

Also per the note: an **unanchored** code fact is not vacuously supported —
`all([])` does not admit it — while inventory positives with unknown-suffix files
are preserved, since inventory capabilities are never grammar-gated.

## 3. CX-BV3-SYNTAX-DISCLOSURE-1 — prerequisite derived by universe kind

The Run-closure guard was already correct (it returns early when the dialect has
no `ownership` axis). The fault was in my v2 **producer helper**: for
`relation == 'clones'` it recovered ownership, found no `sourceUnitOwnershipId`
on a syntax universe, and passed `ownership=None` — which
`clone_ownership_disclosure` defines as *"no committed ownership"*, a genuine Rust
fault. A missing **axis** was read as a missing **record**. The helper now
consults the ownership disclosure only when the universe carries the ownership
dialect axis. The healthy compiler-free clone control emits `complete` with **no**
deficiency and **no** cause. Every Rust missing/partial/ambiguous guard is
unchanged and still verified by root's four ownership cases.

## 4. Emitted reference limit

Updated from *"both registered native-context domains AND both registered native
semantic-universe domains"* to **all three of each**, naming them, adding that the
syntax pair also closes a grammar-only repository with no compiler context, and
extending the synthetic-input caution to grammars: no compiler, cargo, **parser**,
OS or repository code is executed, no real toolchain **or grammar** is measured,
no platform is qualified.

## 5. Checks run

Whole-suite runs use a **further disposable copy** with an **explicit measured pin
refresh**. Those pins exist only in that copy, are not candidate bytes, and are
**not** accepted-candidate pin proof.

| checker | v2 | v3 final |
|---|---|---|
| `check-foundation.py` | 231/231 | **231/231** |
| `check-identity.py` | 903/903 | **977/977** |
| `check-product-quality.py` | 24/24 | **24/24** |
| `check-product-configuration.py` | 28/28 | **28/28** |
| `check-array-orders.py` | 65/65 | **65/65** |
| `check_workflows.v1.py` | 1598/1598 | **1598/1598** |
| `check_native_evidence.v2.py` | 346 cases/66 cells | **346/66** |

All exit 0. **Root's preserved probes on final bytes:** ownership 4/4 as required
(`producer-control` admits; `CAUSE_MISMATCH`, `DEFICIENCY_MISMATCH`,
`PREREQUISITE` refuse), mirrors 13 cases / 0 mismatches, scope 5/5, policy helper
16/16, policy-declaration declared→admits at both boundaries and undeclared→
refuses at both with `POLICY_RULE_NOT_ADMISSIBLE:policy:no-consumer`.

**Root's fixture-extraction interface:** 54/54 declarations, imports cleanly, and
the inventory / base / import Runs all close.

## 6. Limits and open items

1. **No acceptance conferred.** Codex recheck and assent, fresh independent
   review, a NEW blind consumer and the full application review all remain.
2. **Pins intentionally stale and untouched**; all equal frozen v12. Root
   refreshes pins after all recording edits, then runs the six commands and seals.
3. **The symbol-subject attribution limit is real and stated.** A mixed-repository
   empty `declares` scope remains admissible because the record carries no
   symbol-to-path association. It is published in `subjectKindLaw`, not hidden.
4. **Root's grammar-domain probe tests descriptor vocabulary**, not admission; the
   class law is enforced at `admit_native_context` and by my own controls.
5. **Integration dependency unchanged:** the native unit consumes
   `foundation/relation-payload-schemas.v2.json`; the native pin manifest needs
   that row at refresh. I did not edit the manifest.
6. **Not attempted:** no product host, no compiler/parser/provider execution, no
   security or admission-contract change, no data-language tokenisation, no
   Python, no report re-derivation.

## 7. Failed development attempts (retained)

- **`README.md` + `clones` + fact** — expected an admission refusal; it fails at
  `FIXTURE_NO_ADMISSIBLE_PAYLOAD` during construction. Removed from the fact-level
  admission controls and recorded as a construction limit, per root's own rule.
- **`check()` arity, twice** — passed a third detail argument to a two-argument
  helper; both corrected.
- **Language-set capability check (first cut)** — reduced selected rows to
  `languageId`s and could not see row suffix ownership; replaced with row-based
  support after the note's counterexample 3.
- **Whole-snapshot `any(readable)` for every scope (first cut)** — let an
  unrelated code file serve a Markdown-scoped clone request; replaced with the
  per-relation `subjectKind` law after counterexample 4.
- **Leftover scratch expression** in the suffix-control helper (an unused
  comprehension over fact frames), removed.
- **Log-capture confusion** — `FINAL-semantic.json` looked as though coverage were
  empty; root's script deliberately omits `coverage` from stdout. Verified against
  the details file and by direct inspection; not a defect.
