# Independent bounded review — reader 232 r4 (W1) and envelope index 234 r1

ROOT working bytes. **Not cumulative approval, not source selection, not native or crypto
authority.** 233 r2 is used only as a hash-verified overlay for 234's carrier helper; its prose and
unrelated owner files are not re-reviewed. The 71/476/132 AUTHOR coverage fixtures are not treated
as independent decoder evidence. Previous completed review
`/tmp/opensip-implementation/reviews/grok-trust230r3-20260920-r1/` is untouched. No repo, product,
or candidate edit.

The 232 reader is per-record extraction and target shape/byte/locator validation. The 234 index
locates listed envelope bytes. Neither walks a complete graph, admits signatures as held authority,
or supplies native custody.

## Verification and reproduction

- 232 r4 `26bf1187…e2e9` (59724 B, 58 members), 234 r1 `8ad2d813…1c66` (67660 B, 63 members), and
  optional 233 r2 `0e5564d5…291e` (283024 B, 379 members): archive pin and EVERY subject member
  verified from the tar before extraction; 232 and 234 extracted copies re-verified after the runs.
- Python 3.12.13 reference env, `-I -B`. OpenSSL 3.6.3 for 234 crypto. Scripts that print JSON write
  nothing else; mutation runners were executed from output-local work copies so frozen result
  directories were not overwritten.
- 201 sibling symlink to the already-verified reference-201 extraction. Canonical `d47f25db…b442`,
  kernel `df45c9c5…2299`. 234 crypto: output-local overlay = that 201 `candidate/` plus 233 r2
  `candidate/`. `check_crypto.py` hard-codes a live 203 path; the one-line redirect is
  `grok-out/io/crypto-runner-redirect.diff`. Frozen `check_crypto.py` in the 234 extract is
  unchanged.
- 232: regenerated `reader-check-r5.json` **byte-identical** (63 cases). Mutants r3: 11 variants,
  core fields (name/assertion/sha256/baseline 63/sourceSha256) equal the frozen report; frozen adds
  a `classification` annotation the runner does not emit. Coverage 71 fixtures / 476 assertions /
  132/132 rows equals `coverage-report-root-r2.json` except the reader path.
- 234: regenerated `index-check-r4.json` **byte-identical** (58 cases). Variants r2 **byte-identical**
  (8/8). Crypto: 14 outcomes equal frozen `crypto-check-r1/report.json` (3 ordinary VERIFIED, 4
  recovery VERIFIED, recovery threshold-shortfall, tampered catalog `RJ-4 ENVELOPE_MISMATCH`);
  `sourceBindings` 1298 keys equal; `indexSha256` equal; `testScriptSha256` differs because of the
  redirect.

232 before-source-binding reader is byte-equal to the r3 file the W1 finding was demonstrated on
(`6f2a7497…cfea`). r4 reader `c365187a…42cd`. Schema still `a3a0b4f4…8520`.

---

# Part 1 — reference reader 232 r4 (W1)

## Confirmed

The public consumer is now `decode_edge(source_type, source_raw, source_pointer, target_raw)`. It
re-extracts the source, requires a unique instance edge at that pointer, and only then calls the
row validator. Caller-supplied schema rows are not parameters.

Independent probes on the unmodified r4 reader vs the frozen r3-before API:

| probe | r3-before `decode_edge(edge, raw)` | r4 public consumer |
|---|---|---|
| Whole-row BlobRef relabel of `/operation` | **ADMITS**, 0 edges (W1) | old arity: `TypeError` (missing `source_pointer`, `target_raw`) |
| Whole-row StoreMarker relabel of `/operation` | **ADMITS** | same TypeError |
| Honest source + BlobRef/marker *target bytes* for `/operation` | n/a | `reference-bytes` |
| Source record whose `/operation` *is* a marker or opaque blob | n/a | `record-shape` |
| Actual history `/list/body` BlobRef | n/a | **ADMITS**, 0 edges (opaque remains lawful) |
| Lying `source_type=StoreMarkerV1` over a role-event record | n/a | `record-shape` |

So a whole-row relabel cannot be fed to the public consumer: there is no row argument. Substituting
target bytes without changing the source fails the rehash. Putting marker/opaque bytes into the
source's `/operation` still extracts as `NodeRef → OperationInputV1` and then fails shape. Expected
`source_type` remains an internal owner premise; picking another registered root type does not mint
a StoreMarker decode of an operation field.

New corpus negatives (12 added vs r4's 51 → 63) cover those substitutions, missing/non-string/
schema-pointer-as-instance pointers, noncanonical source, target tamper, array index vs prefix, and
clock-vs-creation. Internal helper tests remain separate (`_decode_extracted_edge`).

Mutants: 10 unsafe-source changes plus `source-pointer-ignored`. The latter replaces
`if edge['sourcePointer'] == source_pointer` with `if True`, so a multi-edge source yields
`source-edge-selection` even for a legitimate unique pointer. That is an **over-refusal**, not
unsafe admission, matching the frozen classification. Secondary refusal tuples (e.g. rehash) are
preserved.

## Remaining (232)

#### W-1 remainder (FYI, stated) — the private helper still admits a consistent whole-row relabel

`_decode_extracted_edge` on a BlobRef or StoreMarker registry row still **ADMITS** (0 edges for
BlobRef). README calls this an internal unit probe, not the public consumer. The W1 structural fix
is the 4-argument API. Do not call the helper as a consumer.

#### Coverage harness still does not exercise `decode_edge`

71/476/132 is extraction completeness against hand-written maps. `coverage_harness.py` never calls
`decode_edge`. Decoder evidence is the 63 checks, 11 mutants, and the probes above. WIRE_REGISTRY vs
REGISTRY coverage gap from the prior review is unchanged.

#### Stated owed work (not r4 regressions)

Full graph walk, aggregate graph budgets, old-T ABORT/S4.5 exceptions through every embedding,
event/role/outcome joins on generic prior/head/closing edges (prior W-2). Hash-only fields stay
non-edges.

---

# Part 2 — listed envelope index 234 r1

## Confirmed

OWNER.md is the missing 229 D4 producer: listed paths only, manifest slot chooses body kind, UTF-8
path order, unique `(kind, domain, storedSHA)` even for identical copies, no first-wins or signature
combining, recovery authorization must be the exact listed pair, logical path/alias/file-parent
preflight before capture, per-index budgets that may only lower 222 caps.

Independent probes on the unmodified model:

| probe | result |
|---|---|
| A1 identical-copy root envelopes: **constructing** the index | ADMITS (retains both) |
| A2 selecting that root body | `envelope-ambiguous` |
| A3 selecting **unique catalog** in the same package | ADMITS |
| A4 same triple, different envelope/signature bytes | `envelope-ambiguous` (no combining) |
| A5 extra still-routable `root.1` envelope beside unique `root.2` | ADMITS (different key) |
| B1 `select(envelope path)` | `unowned-body-path` |
| R1 authorization bound to another listed pair | `authorization-exact-envelope` |
| F1 `CATALOG.JSON` alias | `member-path-alias`, **zero captures** |
| F2 init captures only listed envelope paths in UTF-8 order | True |
| F4 unlisted `secret.json` | never captured |
| G1 missing listed envelope, no guessed name | `envelope-missing` |
| L1–L6 zero / bool / negative / cap+1 | `budget-profile` |
| L7 `edge_limit=5` / L8 exact 6 | `edge-budget` / ADMITS |
| P1 file-as-parent `roots` / P2 `payload.json` / P3 non-NFC | `member-file-parent` / `reserved-frame-path` / `member-path` |
| O1 reversed envelope array | same body bytes |

A1–A3 are the compatibility point with accepted-root equal-body envelope law: **package ambiguity is
not a root fork**. Duplicate listed subjects refuse *that pairing*. They do not quarantine the
payload, do not pick the first envelope, and do not refuse an unrelated unique subject. 215
accepted-head rules for equal root *bodies* with different envelopes stay outside this producer.

Four cases added after r3 (54 → 58): preflight-before-read, authorization-cannot-use-other-listed-pair,
duplicate-envelope-key, root-body-version-exact-int. Implementation otherwise matches the earlier
file-parent-before-crypto note in README.

Variants: disabling uniqueness admits `duplicate-subject-even-identical-bytes` (exact oracle). Hash
variant reports a secondary tuple `(listed-envelope-rehash, envelope-shape, member-digest)` —
disclosed, not recategorized as a kill of a different reason.

Crypto: selected pairs feed the unchanged 233 verifier under the overlay. Ordinary and recovery
pairs VERIFIED; two-of-three recovery is THRESHOLD-SHORTFALL; tampered catalog signature is RJ-4.
Catalog/list/authorization **bodies are synthetic**. This is carrier composition, not document,
chain, held-authority, current revocation, time, or ceremony admission. Test keys are fixtures.

## Remaining (234)

#### I-1 (stated owner gap, not a silent hole) — capture and budgets

The capture callback is a trusted reference adapter: it must enforce the byte cap before allocation
and apply native no-follow/ancestor custody. Per-index object/edge/byte counters are this producer's
limits, **not** operation-wide shared `Work`. OWNER.md says both. Composing other indexes must not
reset the operation budget; that wiring is not in this module.

#### I-2 (stated) — pairing is not authentication

Returned body/envelope bytes still need the 215/225/226 producers (held authority, root continuity,
current revocations, role, time, ceremony) and the manifest's own TR-BUNDLE authentication. Artifact,
permission, and repair bodies are not this index's signature targets.

No required implementation defect was found inside the stated pairing/preflight/limit surface.

---

## Verdict

- [x] **232 r4 closes W1 at the public consumer.** Whole-row BlobRef/StoreMarker relabel is not
  accepted through `decode_edge(source_type, source_raw, source_pointer, target_raw)`.
- [x] **234 r1 implements the listed-envelope uniqueness/preflight/pairing policy.** Ambiguity is
  package-scoped, not a root-fork diagnosis.
- [ ] **Not approved as a protocol, source, runtime, or implementation.**

No harness failure. Crypto used the recorded one-line path redirect only. No extra design work.
