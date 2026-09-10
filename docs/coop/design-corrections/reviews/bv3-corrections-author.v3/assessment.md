# bv3-corrections-author.v3 — assessment written BEFORE edits

**Standing.** My substantive assessment of Codex's `CHANGES_REQUIRED`, written after
reading `codex-assessment.md`, `codex-assessment.json`, `complete-codex-note.md`
and every probe, report and custody file under `released-v2-rechecks` in full,
and after **reproducing each counterexample myself** on my own released v2 bytes.
It confers no acceptance and is not a review.

**Custody of what I checked.** `v3/work` is byte-identical to released v2 (2981
files, 0 differences) and differs from frozen v12 in exactly my 20 accumulated
changes. Root tested **my exact released bytes** — I verified all four hashes it
records: `check-identity.py b46c2178…`, `identity-model.py 894af9ec…`,
`native_evidence_model.v2.py d90d56fb…`, `workflows_model.v1.py ffc90360…`.

---

## 0. Scope correction on my v2 handoff — root is right, and I state it plainly

My v2 handoff's grammar section asserted that under the syntax universe
*"a clone or code-construct request against [data grammars] is explicitly
unavailable — never a complete empty clone result, which would read as a finding
of no clones."*

**That claim is false against my own final source.** I have now run root's
inspectors on my released v2 and reproduced the opposite. The claim described
what the published registry *says*, not what the Run boundary *enforces*. I had
enforced the registry on grammar **descriptor class declarations** only, and then
wrote as though that settled fact and Coverage admission. It does not.

I also confirm root's custody point: my last full public-note Read was
**08:07:33.573 UTC**; the concrete M3 counterexample section (08:16 UTC) and the
emitted domain-count wording item arrived afterwards and were **not** assessed in
my v2 handoff. My v2 "no substantive disagreement" statement applies only to the
material I had actually read by then. The v2 handoff stays byte-identical; this
is the additive correction, and I am not claiming agreement with anything I only
hashed or that post-dated my Read.

## 1. CX-BV3-SYNTAX-CAPABILITY-1 — **reproduced; root is correct**

Running root's `inspect-pure-syntax.py` and `inspect-semantic-capability.py`
against my own released v2:

| # | case | v2 result | standing |
|---|---|---|---|
| 1 | `README.md` `file@enumerated`, fact | ADMIT, complete/null | **valid control** |
| 2 | `src/plain.rs` `declares@syntactic`, fact | ADMIT, complete/null | **valid control** |
| 3 | `src/plain.rs` `clones`, fact | ADMIT, **complete + `input-closure-incomplete`/`body-language-ownership-missing`** | **defect (§2)** |
| 4 | `README.md` `declares@syntactic`, **with a fact** | ADMIT | **defect** — fabricated code capability on a data grammar |
| 5 | `README.md` `declares@syntactic`, **empty view** | ADMIT, **complete** | **defect** — false complete for an unavailable capability |
| 6 | `README.md` `clones`, **empty view** | ADMIT, **complete** + ownership cause | **defect** (capability *and* wrong disclosure) |
| 7 | `src/plain.rs` `references@resolved-binding`, **with a fact** | ADMIT, `factRungs:['resolved-binding']` | **defect** — semantic rung under `resolutionAttempted=false` |
| 8 | `src/plain.rs` `references@resolved-binding`, **empty view** | ADMIT, complete, `attempted:true, state:complete` | **defect** |

I accept root's exclusion: `imports`/`calls`/`types`/`reachability` fail at
`FIXTURE_RELATION_UNKNOWN` **before** Run admission. Those are fixture
construction limits, **not** findings and **not** successful negative controls,
and I will not count them as either. I also accept that the earlier `result.json`
used the wrong object-domain name (`'coverage-result'` instead of `'coverage'`),
producing empty `coveragePayloads`; the additive inspectors read the real domain
and the originals are preserved.

**Root cause.** The capability law is already published and closed — the registry
gives `markdown` exactly `file@enumerated`, `package@manifest-declared`,
`vcs-change@vcs-reported`, and gives no language `references@*` at all. But the
only place it is consulted is `admit_native_context`, which validates the
**descriptor's declared `syntaxClass`**. Nothing consults it when a `fact2` is
admitted or when a requested-scope `coverage2` is admitted, so the registry
constrains what a bundle may *say about itself* and not what a Run may *claim*.

**What I plan, and its exact derivation.** Two distinct guards, because two
distinct things are decidable from the retained record:

- **(B) per-fact support** — a fact under a syntax universe must have every
  **anchor path** map (longest-suffix) to a **selected** grammar whose registry
  capability set contains `relation@rung`. This closes 4 and 7 and it closes them
  in a mixed repository too, which is where the fabrication risk actually lives.
- **(A) requested-scope availability** — for a scope under a syntax universe, the
  capability must be available in the **examined extent**: inventory capabilities
  (`file`/`package`/`vcs-change`) are **always** available and are never
  grammar-gated, so ordinary non-parseable inventory keeps its promised meaning;
  a **code** capability requires at least one path in the committed snapshot
  inventory to map to a selected `code` grammar; anything no selected grammar
  lists is unavailable. This closes 5, 6 and 8, and applies to **empty views**
  because it never looks at whether facts exist.

Neither guard trusts the claimed `coverage` value, the caller-declared
`syntaxClass`, or the presence/absence of facts.

**Honest boundary I will state rather than paper over.** For `declares` the
subject-scope's `subjects` are symbols (`symbol:foo`), not paths, and an empty
view has no anchors — so in a **mixed** repository an empty `declares` scope
remains admissible under (A), because that extent genuinely does support the
capability. The pure-repository cases root listed are closed; the mixed empty
case is not decidable from the retained record without inventing a path linkage
that does not exist, and I will say so explicitly instead of claiming more.

**Disclosure vocabulary — existing, not new.** An unavailable request must
disclose `deficiency: language-tier-unsupported` with `nativeCause:
capability-missing`. Both already exist: the matrix already uses
`language-tier-unsupported` for exactly these cells (`imports@resolved-target` ×
syntax-only is `✗ language-tier-unsupported`; "no bundled grammar at all is
`language-tier-unsupported`"), and `capability-missing` is already a
`NativeCause` member. I will add the §10 mapping row for that pairing. No new
enum member, no data-language tokenisation, no Python.

## 2. CX-BV3-SYNTAX-DISCLOSURE-1 — **reproduced; root is correct**

Cases 3 and 6 emit `complete` **plus** `input-closure-incomplete` /
`body-language-ownership-missing` for a **syntax** clone scope. That is wrong
twice over: a grammar-only interpretation has no Rust compilation ownership
obligation at all — my own syntax-universe contract says the mode has no
compilation unit — and `ownership-missing` is not the disclosure for an
unsupported grammar capability. The pair is also internally incoherent
(`complete` with a non-null deficiency).

**Exact mechanism.** The Run-closure guard is already correct: it returns early
when the universe's dialect has no `ownership` key, which is the case for the
syntax universe. The fault is in the **fixture producer helper**
`coverage_result`, which I wrote in v2: for `relation == 'clones'` it recovers
ownership and, finding no `sourceUnitOwnershipId` on a syntax universe, passes
`ownership=None` to `clone_ownership_disclosure` — and `None` is defined there as
*"no committed ownership"*, a genuine Rust fault. So a missing **axis** was read
as a missing **record**.

**Plan.** Derive the prerequisite from the **actual universe kind**: only consult
the ownership disclosure when the universe carries the ownership dialect axis.
The Rust missing/partial/ambiguous guards added in v2 stay exactly as they are —
this narrows *where* they apply, never *what* they enforce.

## 3. Emitted reference limit wording — **root is correct**

`check-identity.py` still emits *"both registered native-context domains AND both
registered native semantic-universe domains"*. There are now **three** of each.
I will correct the wording and preserve every synthetic-observation and
no-native/platform-qualification caution in that same limit string.

---

## Positions

| item | position |
|---|---|
| CX-BV3-SYNTAX-CAPABILITY-1 | **Agree** — reproduced all 6 admission defects on my own bytes |
| CX-BV3-SYNTAX-DISCLOSURE-1 | **Agree** — reproduced; fixture helper, not the closure guard |
| CX-BV3-CUSTODY-2 | **Agree** — my v2 claim was false against my own source; corrected additively |
| emitted domain-count wording | **Agree** |
| `FIXTURE_RELATION_UNKNOWN` cases are not findings | **Agree** — will not count them either way |
| earlier `result.json` wrong-domain inspection | **Agree** — not used as coverage evidence |

**No substantive disagreement.** Every point is supported by source I re-read and
by results I reproduced independently. The capability claim in my v2 handoff was
wrong about my own final source, and I correct it rather than defend it.

## Preserved, because root's rechecks confirm them on my released bytes

16 policy-helper cases (with their explicitly assumed Coverage limit); 13 mirror
cases including lawful zero assets and refusal at 4097; 5 ScopeDocument
registration controls; 4 partial-Rust-ownership cases; the original runtime
`none`-predicate evidenceUse counterexample matching at **both** admission
boundaries; and the `pure_syntax` compiler-free snapshot/Plan shape. Relation
ladders, policy evidenceUse admission and the compilation join, mirrors 0..4096,
the ScopeDoc registry and composition, Rust ownership selections, and all earlier
typed-annotation / body-identity / source joins are preservation targets, not
subjects of this pass. No synthetic fixture here is a real parser, compiler or OS
measurement.
