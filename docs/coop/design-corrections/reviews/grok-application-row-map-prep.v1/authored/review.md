# Application row-map preparation review (read-only; not ACCEPT)

**Standing.** Bounded Grok coauthor preparation of prospective application assembler **input**, not a fresh application grade, not independent design acceptance, not blind reconstruction, and not implementation authorization. Final independent application review remains required and distinct.

**Write scope.** This directory only: `/tmp/opensip-design-corrections/grok-application-row-map-prep.v1`. No product, commit, push, frozen24, live source, or assembler edits.

**Python.** `/tmp/opensip-architecture-review-env/bin/python -I -B` used for hashes only.

---

## Verdict

Prospective **DR-104** wording is already corrected in application-draft.v5 markdown. The three identical row-map JSON inputs still say **blanket major2 identity names**. The successor assembler at `assemble-records.successor.v1.py:248` reads that old absolute JSON, **refreshes successor file hashes** from the frozen accepted subject, and **retains the stale disposition**. That would emit `readiness-row-map.v1.json` inconsistent with the copied draft register table.

This is a required prospective input/handling fix. It is **not** an application ACCEPT. Frozen24 historical preview cells and historical JSON bytes should be preserved as captured input.

---

## Read scope (exact)

**Read.**

| Artifact | Role |
|---|---|
| `/tmp/opensip-design-corrections/application-draft.v5/` | Prospective draft: `files/docs/v2/architecture/08-decision-and-readiness-register.md`, `readiness-row-map.proposed.json`, `identity-profile-wording-correction.v1.json`, `documentation-proposal.json`, `current-review-attribution-correction.v1.json` |
| `/tmp/opensip-design-corrections/application-assembly.v1/row-map-draft.json` | Actual assembler input (byte-identical to draft proposed JSON and successor-root copy) |
| `/tmp/opensip-design-corrections/application-successor-root.v1/assemble-records.successor.v1.py` | Line 248 hardcoded load; hash refresh; owner-sentence rewrite |
| `/tmp/opensip-design-corrections/application-successor-root.v1/coverage_contract.py` | `CONDITION2_IDS` (28), `OWNER_IDS` DR-201–205, excluded DR-108/116/128/129 |
| `/tmp/opensip-design-corrections/application-successor-root.v1/current-status.json` | `designSubjectSha256` `a70f5830…`; draft v5; `readyForAssembly=false`; `actualApplicationPerformed=false` |
| `/tmp/opensip-design-corrections/candidate-subject.v24/` | Frozen accepted24 selected contracts, identity-schemas.v3, command-inventory.v3, graph-query:3, architecture 02/05/08, `architecture-application.v1.json` |
| `/tmp/opensip-design-corrections/application-source-delta.v24.json` | Header pin of the same subject digest |
| `record-root-design-assent.v24.py` | Root readiness clarification only (condition-2 routing ≠ automatic qualification deferral) |

**Not read (forbidden / out of scope).** Active blind session `01a08369-9a7a-7101-8e58-4a4553987715`; consumer-B trees; independent-design.v24 review body/session; other coauthor private worktrees; live repo mutation; frozen24 edits.

**Not a complete grade.** All 28 JSON summaries were compared to the draft v5 register table and spot-checked against frozen24 selected contracts and existing inherited pins. This is not a line-by-line re-proof of every successor section, not a re-run of reference suites, and not substitution for final application review.

---

## Frozen24 current majors (selected source)

Subject digest (root status + source-delta header): `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb`.

| Axis | Frozen24 fact | Selectors |
|---|---|---|
| Output / evaluator3 identity | `finding3`, `subject3`, `proof3`, `evidence3`, `seal3`, `run3`, `policy-derivation3` | `identity-schemas.v3.json` `x-opensip-evaluator-profile.changedIdentifierMajors`; `identity-and-evidence.md` prefix table (`run / run3`); `workflows-and-surfaces.md` L23–35 |
| Unchanged native/input identity | `snapshot2`, `plan2`, `closure2`, `import2`, `fact2`, `coverage2`, `view2`, `exec-plan2`, `finding-key2` | same workflows L23–25; identity prefix table |
| Query owner | graph-query **major 3**; CLI `opensip query OPERATION [--view run3:…\|snapshot2:…\|latest]`; parity `resolved-view`, `availability`, `truncated`, `total-items`, `termination-class`, `query-response` | `workflows/schemas/evaluator3/graph-query.schema.json` `$id` `…graph-query:3`; `workflows-and-surfaces.md` **Query.**; `command-inventory.v3.json` command `query` |
| Policy / some workflow records | PolicyDocumentV2 `schemaMajor` 2; baseline/comparison major2; review/repair profile2 | workflows L33–37; `shared-profile-decisions.v1.md` |
| Native wire | `typescript-semantic` protocol major **2**; `rust-semantic` protocol major **3** | `native-evidence.md` L2529 |

Current profile is **output3 + native/input2**, not “all identities major2”. Query is **owner3**. Those are design facts already in frozen24. Unperformed release gates do not un-design them.

---

## Finding 1 — REQUIRED — DR-104 JSON still blanket-major2

**Selectors.**

- Draft markdown (corrected): `application-draft.v5/files/docs/v2/architecture/08-decision-and-readiness-register.md` SHA `06fb816e1c527edc666367ba6823794eff271ab7847abbbef36e69a30d63825c`, table **Existing row / Accepted design disposition**, row **DR-104**:
  > Retain namespace/alias ownership laws and collision cases; **the selected input and output identity majors** and a closed complete command registry select current authority.
- Authored correction record: `application-draft.v5/identity-profile-wording-correction.v1.json` SHA `e6ed0d352511ff0b910aafc1eea00f02e8c680f40c12b66af72f8cc7f15dd80a`
  - `beforeText`: `major2 identity names and a closed complete command registry select current authority.`
  - `afterText`: `the selected input and output identity majors and a closed complete command registry select current authority.`
  - `basis`: current output profile3 and unchanged input/native profile2 are separate axes.
- JSON inputs (stale, byte-identical, SHA `01e37c6f09053ff8885214c7a72a7715ce45b111cad0654ab9f19ee9bde75fcf`):
  - `application-draft.v5/readiness-row-map.proposed.json` `/rows` id `DR-104` `/disposition`
  - `application-assembly.v1/row-map-draft.json` same
  - `application-successor-root.v1/row-map-draft.json` same
  - text still: `…; **major2 identity names** and a closed complete command registry select current authority.`
- Frozen24 historical register (do **not** rewrite as if it were the prospective table): `candidate-subject.v24/docs/v2/architecture/08-decision-and-readiness-register.md` SHA `dfc3a929e40675039e660620878eea989065af2ad541f69399000245705f2fe3` — preview SATISFIED cell at the DR-104 source-obligation row (~L292). The prospective condition-2 disposition table is draft-only.

**Why it matters.** Frozen24 identity and workflows already split output3 vs input2. Query selects `run3` or `snapshot2`. A blanket “major2 identity names” in the **emitted application row map** is a current-description error, not a qualification deferral.

**Preserve historical JSON bytes.** The SHA `01e37c6f…` file is captured input. Do not silently destroy it. Overlay or replace **at assembly emit**, and record the historical input digest.

---

## Finding 2 — REQUIRED — assembler retains stale disposition

**Selector.** `application-successor-root.v1/assemble-records.successor.v1.py` SHA `57747f5a375d072cf2e645271ccc2faa9e93738d496d5071729c83f3b93d6bfd`, **L248–261**:

```python
rows = json.loads(Path('/tmp/opensip-design-corrections/application-assembly.v1/row-map-draft.json').read_text())['rows']
...
for s in row['productSuccessors']:
    s['sha256'] = accepted_files[s['path']]['sha256']
```

`--draft` is used to copy `draft/files` and rebase-check `documentation-proposal.json`. It is **not** used as the row-map source. Disposition, `proposedDesignGrade`, gates, and inherited fragments are copied verbatim. Only `productSuccessors[].sha256` is refreshed against the frozen accepted subject.

**Consequence.** Even after markdown DR-104 is correct, assembly would write `docs/coop/design-corrections/readiness-row-map.v1.json` with major2 identity names while the copied register table says selected input/output majors.

Assembler already rewrites the five owner sentences `This is a new subject-specific design review.` (L241–247) so owner markdown is not left as a self-grade. There is no analogous DR-104 overlay.

---

## Finding 3 — expected, not a second identity bug — captured successor hashes are pre-frozen24

All **76** `productSuccessors[].sha256` values in the JSON differ from frozen24 contract bytes. Unique current frozen24 hashes:

| Path | Frozen24 SHA-256 |
|---|---|
| `docs/v2/contracts/product-v1/admission-and-qualification.md` | `69cd6ba3cb41ed191e0a4e5cc20b191f4b8761625843b585426157873dbee6b3` |
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | `9261aff41cfe2c7a2f5e9b81c72cd3ab4aa96563a2732b9362ee53adfd683cf5` |
| `docs/v2/contracts/product-v1/native-evidence.md` | `af2d566f1e1e87c7280512cd9fbee6f9055dde9decea6cf35a7bb2dbabe65fa1` |
| `docs/v2/contracts/product-v1/security-and-lifecycle.md` | `12dcebea91fd7ede7af85c3cace29ee931fbfa2d3f55f1773960328526ec496b` |
| `docs/v2/contracts/product-v1/workflows-and-surfaces.md` | `3d89b511663fe9238ef42dca9625f18f0d38f64f9094cae1b3ddfd7a3c1d98cf` |

Assembler already replaces those hashes from the accepted subject manifest. **Do not treat hash refresh as disposition refresh.** Historical JSON hashes should remain in the captured input file.

`originalEnumeratedObligation` and `additionalInheritedAccount.sourceSha256` **match frozen24** (DR-117 file 02 `04a6cfe2…`, DR-130 file 05 `1a57c9ca…`, COORDINATOR-DECISIONS `442bd9c7…`, control-protocol `c50a79fe…`, preview-boundary `8f34c92e…`, architecture-application `15b3932a…`). Leave those as historical resolve-against-accepted-snapshot pins.

---

## Finding 4 — SHOULD-CONSISTENCY — query owner3 not named in several surface-row summaries

Not a new product law. Frozen24 already owns query major3. These JSON/markdown summaries (identical) never mention `graph-query:3` / `run3` query selection, while their successor lists include `workflows-and-surfaces.md` §8:

| Row | Disposition (current) | Frozen24 already says |
|---|---|---|
| DR-123 | All45 commands, common schemas, D9/detail, required-output | 45 commands confirmed; query CLI `run3`/`snapshot2`/`latest`; graph-query:3; required parity includes `query-response` |
| DR-113 | Verification/regeneration distinct closures; expiry/purge change availability | Query is a retained-Run read; availability refuse-not-grant is query law as well as storage law |
| DR-131 | Authoritative analyze; preview identities historical | Query over `run3` is the read of that sealed Run (successor §8) |
| DR-133 | Provider-only fact/Coverage; host owns findings/output | Host-owned query/output, not provider graph authority (successor §8) |

**Recommendation.** Optional one-clause consistency on **DR-123** only (command-inventory owner): current query is graph-query major3 over selected `run3`/`snapshot2`. Do **not** invent new query semantics in the row map. DR-104 remains the only **false** major claim.

DR-102 `native TS major2/Rust major3` is **not** stale: `native-evidence.md` L2529 still states those **wire** majors. Do not “correct” it to identity majors.

---

## All 28 condition-2 rows (summaries vs selected source)

`CONDITION2_IDS` = DR-101–107, 109–115, 117–127, 130, 131, 133. Excluded by name: 108 credentials, 116 third-party, 128 untrusted, 129 TUI.

Every row: `proposedDesignGrade=SATISFIED-DESIGN`, `productQualified=false`, `independentGrade=PENDING` in the JSON. Markdown table matches JSON **except DR-104**. Assembler would stamp `independentGrade=ACCEPT-DESIGN` and `productQualification=false` at emit — a **design** stamp, not measured qualification. Unperformed DR-G01–32 tests do **not** by themselves move a designed row back to deferred-design.

| ID | JSON==MD | vs frozen24 selected source (this read) | Flag |
|---|---|---|---|
| DR-101 | yes | Signed TCB/profile/native closures; successors exist | OK as design summary; qualification remaining |
| DR-102 | yes | Byte-opaque control + TS wire2/Rust wire3 still current | OK (wire majors, not identity) |
| DR-103 | yes | Typed admission/registry; custody defaults | OK |
| DR-104 | **NO** | Output3/input2 + closed command registry; JSON says major2 names | **REQUIRED overlay** |
| DR-105 | yes | Platform auth/revocation; test consent ≠ sandbox | OK |
| DR-106 | yes | Signed closures, durable custody, typed absence | OK |
| DR-107 | yes | Fence/leases/pins/one-writer | OK |
| DR-109 | yes | Host storage-mechanics; no caller custody grant | OK |
| DR-110 | yes | Repair/rollback bind signed closures/profile/leases | OK |
| DR-111 | yes | Independent windows; policy still schemaMajor2 | OK |
| DR-112 | yes | Root continuity/revocation | OK |
| DR-113 | yes | Distinct verify vs regenerate; query not named | SHOULD-CONSISTENCY only |
| DR-114 | yes | Read-only doctor; command/detail schemas | OK |
| DR-115 | yes | Numeric bounds remain product-owned; D-006 fragment pinned | Design decided; measurement is qualification |
| DR-117 | yes | Admission §5 seven-item successor; preview v10 retained as history; file02 count pin matches frozen24 | OK |
| DR-118 | yes | Native capability cells; no silent syntax fallback | OK |
| DR-119 | yes | Self-contained closures; D-008 fragment pinned | OK |
| DR-120 | yes | Adapter/packaging + selected TS/JS/Rust | OK |
| DR-121 | yes | Isolated CI / independent producer reports | OK |
| DR-122 | yes | SARIF re-entry D372/G17; historical D077/D086 scoped | OK |
| DR-123 | yes | 45 commands confirmed in inventory.v3; query major3 omitted from sentence | SHOULD-CONSISTENCY |
| DR-124 | yes | Four state classes; Run identity is run3 in identity §2 | Summary OK; does not claim major2 |
| DR-125 | yes | Common SDK/control; no finding authority | OK |
| DR-126 | yes | Four machine IDs; TCB/loader; measured platform is qualification | OK |
| DR-127 | yes | Dual-channel / skew / EOF | OK |
| DR-130 | yes | S16 coexistence; 5/5/6 counts pinned to frozen24 file05 | OK |
| DR-131 | yes | Authoritative analyze vs preview identities | SHOULD-CONSISTENCY (query/run3 read) |
| DR-133 | yes | Provider facts/Coverage; host findings/output | SHOULD-CONSISTENCY |

No other JSON disposition uses the false phrase `major2 identity names`.

---

## Five owner rows (DR-201–205) — not qualification dumping

Draft register L326–330 currently says each owner is **Current intended product — ACCEPTED under D-372** and **This is a new subject-specific design review.** Assembler L241–247 replaces that second sentence with a requirement that **fresh final application review** bind the outcome; independent design accepted **routing only**.

That split is the right one for this prep:

- Independent design review of frozen24 is **not** final application.
- Unperformed release tests are **condition 4 / productQualified=false**, not a license to mark designed owner rows as “deferred because unqualified”.
- Authors must not self-ACCEPT application.
- This review does **not** grade DR-201–205. It only records that they must be substantively assessed at final application, not bulk-deferred.

---

## Proposed narrow assembler input handling (no edits here)

Keep it self-contained. Do not invent a second row-map product.

1. **Pin historical input.** Record `historicalRowMapInput.sha256 = 01e37c6f09053ff8885214c7a72a7715ce45b111cad0654ab9f19ee9bde75fcf` and path `application-assembly.v1/row-map-draft.json` (same bytes as draft `readiness-row-map.proposed.json` today). Do not rewrite frozen24.

2. **Stop using a hidden absolute path as the only source.** `assemble-records.successor.v1.py` should load the row map from `--draft/readiness-row-map.proposed.json` **or** keep the absolute file only as the historical pin and apply an explicit overlay. `--draft` is already the documentation source of truth.

3. **DR-104 overlay already authored.** Apply `identity-profile-wording-correction.v1.json` (`e6ed0d35…`) to `rows[id=DR-104].disposition` at emit:
   - replace `major2 identity names and a closed complete command registry select current authority.`
   - with `the selected input and output identity majors and a closed complete command registry select current authority.`
   - Fail if the `beforeText` is absent (so a later JSON fix does not double-apply).
   - Assert equality with the draft markdown DR-104 table cell.

4. **Keep hash refresh.** Continue replacing `productSuccessors[].sha256` from the frozen accepted subject. Continue **not** mutating inherited `sourceSha256` / `originalEnumeratedObligation.sha256` (they already match frozen24).

5. **Fail closed on markdown/JSON drift.** After overlay, every `CONDITION2_IDS` disposition must equal the draft register table “Accepted design disposition” cell. That is how DR-104 was caught; it should not be a one-off.

6. **Do not auto-defer design to qualification.** Leave `productQualified=false` / `productQualification=false`. Do not rewrite SATISFIED-DESIGN to a qualification-deferred grade because G-gates are unrun. Optional DR-123 query-major3 clause is consistency with frozen24 §8, not a new obligation.

7. **Owner path unchanged in substance.** Keep the five-sentence rewrite that forbids treating independent design routing as final application ACCEPT.

Root integrates only these prospective fixes. This document is not an assembler patch and not an application record.

---

## Limits

- Did not execute assembler, finalizer, or reference suites.
- Did not re-read every successor section byte-for-byte; contract spot-checks used the cited selectors.
- Did not read the independent design review body or the active blind.
- Frozen24 graph-query/contract bytes (`graph-query.schema.json` `ca1e2bae…`, query-projection-contract `9635e810…`) are the authoritative query owner for this review, not any isolated successor worktree.
- `current-status.json` shows new blind11 active and `readyForAssembly=false`. This prep must not race that work.

**acceptanceClaimed:** false.
