# Retained failed attempts — fresh independent review of frozen v15

Every attempt that failed first is retained here with its exact refusal and an
attribution. Attribution matters: most were **my** harness or fixture errors,
and a careless reviewer would have scored several of them as candidate defects.

Corrected harness/fixture errors: **8**. Candidate defects found by them: **0**.

---

## A. Harness errors (mine)

### A1 — six reference commands exited 127 before any command ran
`zsh` treated the quoted `$P` (`/tmp/…/python -I -B`) as a single word:

```
(eval):5: no such file or directory: /tmp/opensip-architecture-review-env/bin/python -I -B
```

Nothing executed. `copy-run1` was re-verified against the v15 manifest
afterwards and was **byte-identical** (0 modified / 0 missing / 0 added), which
is what establishes that no partial run occurred. Re-run from a script
(`custody/run_six.sh`) into a **new** copy, `copy-run2`. Both copies are
retained.

### A2 — probe harness not importable under `-I`
`python -I` isolates `sys.path`, so `import harness` failed with
`ModuleNotFoundError`. Every probe now bootstraps its own directory.

### A3 — `probe_preserved_laws` read the cause registry's top level
I took `x-opensip-deficiency-cause-registry` itself as the row map, so the
totality check compared the 9 `DeficiencyV2` members against the registry's
**prose keys** (`standing`, `whyItIsNeeded`, `enforcedAt`, …). The rows live
under `deficiencies`. Fixed; the registry is genuinely total over the 9 members.

### A4 — `probe_preserved_laws` string-matched a comment
My strict-parity check asserted that `if k in envelope['parity']` does not
appear in `W.render`'s source. It **does** appear — inside the comment that
documents the weakened guard the v14 delta *removed*. A false negative entirely
of my own making. Replaced with a **behavioural** test: `render` with a declared
parity field missing must raise, and must never emit a silently shortened
output. It does.

---

## B. Fixture errors (mine) — the candidate's own laws refusing my input

### B1 — invented `languageMode` and row vocabulary
My first cardinality probe used `languageMode: "typescript"` / `"rust"` and a
three-key row. The real modes are `ts-tsconfig`, `js-allowjs`, `js-synthesized`,
`rust-cargo`, `rust-cargo-prepared`, `syntax-only`, and the schema requires all
four of `capabilityId`, `languageMode`, `workspaceRoot`, `required`. Refused
with `KeyError: 'status'` while I was recomputing per-mode counts from the
matrix — the cell state key is `state`, not `status`.

**This one mattered.** Recomputing the per-unit counts from the matrix instead
of trusting the prose is what let me confirm 11/11/11/10/10/10 independently.

### B2 — `x-opensip-order: utf8` on `languageModes`
```
array order utf8: strict unique order required
```
My release-registry fixture listed modes in matrix order. The array-order law
refused it.

### B3 — `x-opensip-order: canonical-set` on the registry array itself
```
array order canonical-set: strict unique order required
```
I fixed the inner `languageModes` but not the outer registry rows, and the same
law refused again. Also fired on `requestedCapabilities`, which is
`canonical-set` too.

### B4 — a release registry declaring a `NOT-SELECTED` cell
```
AdmissionError: native.release-capability-mode-not-selected:clones-cross-tsjs:rust-cargo
```
My "full registry" declared every capability for every mode. Three cells are
`NOT-SELECTED` (`clones-cross-tsjs` × `rust-cargo`, `rust-cargo-prepared`,
`syntax-only`). **This is the v14 CB4-SHOULD-2 safeguard firing on my input** —
a release may not redefine the selected product — so the failure is positive
evidence that the law still holds, not a defect.

### B5 — over-strong format expectation
I asserted every `requestClass: analysis` command declares all of
human/json/sarif/html. `fit` declares no `sarif` and `repair-verify` no `html`.
The published rule is that a **declared** format must be applicable to the
request class, not that every applicable format must be declared
(`check_workflows.v1.py:133`). My expectation was wrong; both declarations are
unchanged from v14 and lawful. Corrected to the accurate claim, with the two
declining commands recorded explicitly.

### B6 — corrupt-retained-payload case proved less than it claimed
My first retained-payload mutation only rewrote the blob bytes, so the content
digest join refused first:

```
AdmissionError: BLOB_DIGEST
```

A **correct and stronger** outcome — but it never reached the raw payload schema
validation the claim is actually about. Re-done as a **self-consistent** forgery:
the oversized spec is stored under its own digest and the Plan re-minted to name
it (`put_blob` + `rekey_plan`), so every digest join holds and the payload's own
schema validation is reached. It then refuses with a generic `ValidationError`
of **259,664 characters**. Both routes are now retained as distinct cases.

---

## C. What none of these were

None of the eight was a candidate defect. Five (B1–B5) were the candidate
refusing malformed input of mine, which is the laws working. Two (A3, A4) were
my own measurement bugs that would have produced **false accusations** had I
reported them without checking. One (A1) was a shell quoting fault that executed
nothing.

The single genuine mismatch I did find — the unqualified "everything a schema is
genuinely better at … still refuses at the schema step" sentence — was found by
a probe I wrote **specifically to falsify a published sentence**, and is raised
as **V15-ADV-1** at advisory severity with its consequences bounded, not as a
MUST or SHOULD.
