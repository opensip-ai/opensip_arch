# HANDOFF — actual Claude coauthor, v8 (one effective-annotation account across all three limbs)

**Standing: not accepted, not qualified, not promoted. No implementation authority claimed.** Root's
final source capture, all captured counterexample rechecks, the fixture-source SHA and pin refresh,
the six final commands, a v10 freeze, a FRESH actual independent review at zero unresolved
MUST/SHOULD, a NEW fresh blind B, and the complete independently reviewed application/readiness
reconciliation all remain required and are root's to run.

**Notes read in full, content inspected not merely hashed:**

| File | Bytes | SHA-256 |
|---|---|---|
| `digest-corrections-author.v7/CODEX-PUBLIC-NOTE.md` | **6015** | `a131e8f90cb0709161de60856ccda368432dc03c0012e87f2fd4a99052fabb94` |
| `digest-corrections-author.v8/CODEX-PUBLIC-NOTE.md` (read before this handoff) | **1360** | `ea932397461d7f271912214207dfdcc30e2105e6a8ecee4db8eeff50d8aafc56` |

The v7 note's final section, *"All three limbs must use the same inherited annotation"*, was appended
after the 4371-byte state my v7 handoff recorded. **I inferred no assessment of it from anything I
said in v7**; it is assessed here for the first time. Also read: root's captured
`reviews/codex-post-reset.v1/annotation-inherited-limbs-draft-counterexample.v10/` — probe, result,
model and schema — including root's own note that an initial exploratory command used system
`python3` and failed importing `jsonschema` before any model execution.

---

## 1. The finding is correct, and the inconsistency is mine

v7 gave **limb 3** an inherited notion of "annotated" — the property, an enclosing branch's parent,
or an intermediate alias `$def` — while **limbs 1 and 2** kept reading
`properties[field]['x-opensip-digest']` directly. So precisely at the locations my revised traversal
newly accepted, a field became invisible to retention validation and to the residue rule.

Root's nine vectors, on the v7 bytes: the three **field** cases behaved
(`RELATION_DIGEST_LAW_RESIDUE`, `RELATION_DIGEST_RETENTION`, admit), and **all six alias and branch
cases admitted** — including a dangling `preimage` with no join and an invented retention value.
Preserving my earlier top-level controls could never have caught it, because those controls only ever
exercised the direct location. **I dispute nothing.**

## 2. The correction: one account, used by every limb

`relation_digest_annotation_coverage` is now the single source of truth and returns **sightings**.
Each sighting is a governed leaf, or a directly annotated selector property:

| Key | Meaning |
|---|---|
| `path` | `relation.field`, plus `\|oneOf[i]` for a branch, `.sub` for a nested member, `[]` for array/`additionalProperties` |
| `form` | the governed form, or `null` for a directly annotated non-governed property |
| `field` | the **top-level selector property** owning the sighting — what a join row can address |
| `joinable` | whether a join naming `field` actually addresses this value |
| `annotations` | every annotation on the path, excluding the terminal governed `$def` |

`relation_annotation_closure` applies every limb to that same set, in this order:

1. no annotation → `RELATION_DIGEST_UNANNOTATED` *(v7, unchanged)*
2. more than one **distinct** annotation on one sighting → `RELATION_DIGEST_ANNOTATION_CONFLICT` *(new)*
3. retention outside the law's vocabulary → `RELATION_DIGEST_RETENTION` *(now reached at alias and branch)*
4. joinable, non-`not-joined`, owning field named by no join → `RELATION_DIGEST_LAW_RESIDUE` *(now reached at alias and branch)*
5. **un**joinable location claiming a joinable retention → `RELATION_DIGEST_UNJOINABLE_LOCATION` *(new)*
6. a join naming a field the selector lacks → `RELATION_JOIN_FIELD_UNKNOWN` *(unchanged)*

**Existing cause strings are byte-identical to root's captured expectations**:
`RELATION_DIGEST_LAW_RESIDUE:file:stray` and `RELATION_DIGEST_RETENTION:file.stray`.

**A directly annotated property stays a sighting whether or not it is governed.** The law's residue
and retention limbs are triggered by the annotation, not by the form — which is what keeps
`file.byteLength` (annotated, but a `UInt64`) inside those two limbs while correctly outside the
governed count of 7.

### The two boundaries, stated and enforced — root concurred in the v8 note

**(a) Join addressing is top-level properties only.** A join row reads `value[field]`. That reaches
a scalar at a property, and a scalar inside a `oneOf` branch of that property — but never a member of
a nested object or an array element, where `value[field]` yields an object or a list. So a governed
sighting reached through `.sub` or `[]` is unjoinable and must declare `not-joined`; claiming a
joinable retention there refuses. I would rather enforce the boundary of what I actually implement
than let a join row appear to address something it cannot reach. **No shipped field is affected** —
all seven governed fields are direct properties.

**(b) No invented precedence.** The law states no precedence between an annotation on a property and
one on the alias it refs, so I invent none: two that **disagree** refuse as a conflict; two that are
**identical** do not. **No shipped field carries two.**

**This is not "reject every alias or branch".** Each of the three locations keeps a lawful
`not-joined` control that admits, and a **joined** `preimage` control that admits at every location
— so the refusals are caused by the missing join and the bad retention, not by using an alias or a
branch at all.

## 3. Evidence

**Root's nine vectors, re-run** (`probes/rerun-root-inherited-limbs.v10.py`, their construction; only
the repository writes and source capture removed):

| Retention | field | alias | branch |
|---|---|---|---|
| `preimage`, no join | `RELATION_DIGEST_LAW_RESIDUE:file:stray` | same | same |
| `invented-retention` | `RELATION_DIGEST_RETENTION:file.stray` | same | same |
| `not-joined` | admits | admits | admits |

**Measured across the two actual source images** (`probes/probe-v7-vs-v8-inherited-limbs.v1.py`),
the retained v7 image (`identity-model.py 77ff7d02…`, overlaid on a copy of the current tree so its
root-owned imports resolve; only the two owned files differ, verified file by file) versus the
current tree: the **four** alias/branch refusal vectors flipped from `ADMITTED` to refused, the three
field vectors are **unchanged**, and the lawful `not-joined` control admits at every location in
**both** images.

**A neutralisation attempt that did not work is retained, labelled**
(`result-unified-limbs-are-load-bearing.v1-STUB-COLLAPSED-LIMB3.json`): stubbing the coverage
function to empty a sighting's annotations blinds limb 3 as well, so the six vectors refused at
`RELATION_DIGEST_UNANNOTATED` instead of being admitted. The pre-v8 code held two notions at once,
which a single stub over one function cannot express. Its `loadBearing: false` is an artifact of my
stub, **not** a finding, and it is superseded by the two-image measurement rather than deleted.

**Every earlier retained counterexample re-run green on this source:** root's traversal vectors
(container ref, both branch orders), root's alias-location vectors including the terminal-def
boundary, the reviewer's p03/p04 (39/39 limb-3 injections refuse; shipped document coherent for all
13), the third-limb neutralisation probe (0/39 with enforcement, 39/39 without), and **no identity
churn** — every `RunId`, `PlanId`, fact payload digest, `bodyIdentity` and language-version component
identical across frozen v9 and this tree for `references`, `file`, `clones-typescript` and
`clones-rust`, with exactly two files differing.

**In-suite** (`check-identity.py`, 661 checks): all nine location×retention cases with their exact
causes; a **joined** `preimage` positive at each of the three locations; both unjoinable shapes
(`nested`, `array`) refusing a joinable retention and admitting `not-joined`; the identical-annotation
positive and the disagreeing-annotation conflict; and — root asked these stay explicit — the
**no-blanket-terminal-default** rule and the `previousPath` `not-joined` exemption, both still
passing.

## 4. Owned files changed, exact final hashes

| Path | SHA-256 |
|---|---|
| `docs/coop/design-corrections/foundation/identity-model.py` | `f200232b9cccc06f280db284280932646baaae050418521ee3f03eafece1b226` |
| `docs/coop/design-corrections/foundation/check-identity.py` | `a7f7d393d3b1c9284ce1109b0458b9cb63708794c371365be22e8c5afc4f053c` |

Base for the diff: my retained v7 images `77ff7d02…` and `3d3a1b70…`.

Verified **byte-identical to frozen v9** after this session, so root's "preserve current
contracts/schema/registry bytes" holds: `relation-payload-schemas.v2.json`,
`native-evidence-report.v2.json`, `native/source-pins.v2.json`, `security/source-pins.v1.json`,
`integration-fixtures.py`. No in-tree report or pin was regenerated; native and security ran in a
disposable copy. No integration edit — the fixture-source SHA line still names the v9 value and is
root's to refresh; the new `check-identity.py` value is above.

## 5. Development checks

| Suite | Result |
|---|---|
| `foundation/check-identity.py` | **661 / 661**, 0 failed (639 at v7; +22) |
| `foundation/check-foundation.py` | PASS, 231 / 231 |
| `foundation/check-array-orders.py` | 65 / 65 |
| `foundation/check-product-configuration.py` | 28 / 28 |
| `foundation/check-product-quality.py` | 24 / 24 |
| `workflows/check_workflows.v1.py` | 1290 / 1290 |
| `native/check_native_evidence.v2.py` | PASS, 151 / 151 — disposable copy, regenerated pins |
| `security/check-security-lifecycle.v1.py` | 456 / 456 — same copy |
| `check-integration.py` | 363 / 363, builder unedited |

## 6. Limitations, stated plainly

- **Still schema/reference validation, not a payload or Run attack.** The shipped relation selectors
  are closed and every governed field is annotated and joined, so reaching any of these causes needs
  a reviewed design-time edit to a registered document. I claim no runtime security property and no
  product qualification.
- **The unjoinable boundary is a statement about what I implement**, not a claim about what a future
  join vocabulary could address. If join rows ever gain path addressing, the boundary should be
  revisited rather than silently outgrown.
- **The conflict rule refuses rather than resolving.** If root later wants a precedence — property
  over alias, say — that is a law change, and I did not make one up.
- **Root's three annotation locations are the supported set.** Anything else that could carry an
  annotation is either unreachable by the traversal or lands on the terminal governed `$def`, which
  is deliberately not inherited.
- The coverage function is now called once per relation inside the closure. It is pure and small, but
  it is no longer a single pass per document; if that ever matters it is a memoisation question, not
  a correctness one.
- **My own controls did not find any of root's four counterexample classes** across v7 and v8 — the
  container ref, the branch-order collapse, the alias-annotation location, and now the inherited-limb
  inconsistency. The matrices are wider each time, but root's executed probes found what my authored
  controls did not, and I would rather record that than imply my coverage was adequate.
- One neutralisation attempt failed to reproduce the pre-v8 state and is retained labelled rather
  than deleted or quietly re-run until green.

---

**No acceptance, no readiness, no implementation authority.** Root captures the final source, runs
all four prepared rechecks, refreshes fixture provenance and pins, runs the six final commands,
freezes v10, then a fresh independent review at zero unresolved MUST/SHOULD, a new blind B, and the
complete independently reviewed application/readiness reconciliation. This bounded correction is
complete.
