# Independent review: reference108 — private witness / floor file bytes (storage97 D1) — Claude, r1

Reviewer: Claude (independent; Codex remains implementation owner). Date: 2026-09-18.
Scope, as requested: my storage97 decision **D1 only** — the prospective byte rule for the private witness
and SC-TRUST floor files (strict metadata decode → closed shape → `raw == C(value)`; writer emits exactly
`C(value)`); the pure reference `operational_file_reference.py`, its cases and sweep; the contract S2.1
binding and the floor-schema description; and the legitimacy of the added planning input.

**Not covered and not approved:** storage97 **D2** (generation-mismatched witness / Step 4) and storage99
**D3–D6** (purge disclosure) — all still open; read-only recovery; any witness / floor / journal writer;
file I/O, presence, custody, quarantine; the Rust drafts; Linux, hardware, dependency or current-authority
claims; formal selection. This is a codec verdict and nothing more.

## Bounded verdict

**No blocking finding. D1 is closed exactly as I proposed it (correction C1 in the storage review), and the
rule is pinned: 6 of 8 mutants killed; one survivor is admission-equivalent, one is a small real gap
(N-1).**

| Question | Adjudication |
|---|---|
| Is the rule the right one? | **Yes.** Strict metadata loader, then the complete closed shape, then **exact byte equality with `C(value)`**. Byte equality is what makes the file canonical *and* makes the decoder choice unobservable for every admissible file — the property that removed the need to pick "metadata vs product" in the first place. |
| Does it import S2 by stealth? | **No.** S2.1 says in terms that these are private operational files, "neither signed metadata nor product data"; it borrows the metadata codec as an explicit pinned dependency and registers no domain tag, digest or identity. |
| Negative zero | Refused — `NONCANONICAL_BYTES` (decodes to `0`, re-encodes as `0`, bytes differ). The only spelling on which the two decoders disagreed in my storage probe. |
| Does the reader repair? | **No.** No path returns normalised bytes; `decode` returns the value or raises. |
| Absent / unreadable | Correctly **outside** the codec: only exact `bytes` are accepted; `None` is `BYTES_REQUIRED`, not "absent". The contract forbids synthesising either condition from a decode error. |
| Does a malformed file authorise a diagnosis? | **No**, and S2.1 says so: no quarantine, reconciliation, read-only diagnosis, rewrite or floor mutation follows from the codec; raw bytes are retained for W/H brackets, and decode/re-encode "must never replace byte-stability comparisons". That is the correct seam with my storage Q2 / D2. |
| Existing development files | No grandfathering, rewrite, deletion or reset; unadmitted observations preserved; future migration needs its own disposition. Matches the second half of my D1. |
| Added planning input | **Legitimate and necessary** (details below). |

## Reviewed bytes (independently verified)

| Item | SHA-256 | Result |
|---|---|---|
| `trials/operational-file-reference-checkpoint-108/subject.tar.xz` | `1052e444eeede6d6b14b4ceaad359aa3b83a899e9359e531aa101eae1b91fc56` | = `archive-pin.json` |
| `subject.json` (1,440 members) | `6c143cb2834791d88c1e21df7e9ca2f0a21d93ce738be3a60308bb2cc93ea042` | every member re-hashed from the tar **before** extraction |
| `frozen-candidate.json` (1,280 entries) | in manifest | all hash-match; 0 unlisted files |
| parent | — | `parent-inputs.json` **equals frozen reference107 exactly** (1,277 files) |

0 symlinks / non-regular members / unsafe paths; extraction unchanged after all work. **Change set vs 107:
8 changed, 3 new, 0 removed** — new: `operational_file_reference.py`, `operational-file-cases.v1.json`, and
`docs/v2/architecture/implementation-boundaries-and-build-plan.md`. The floor schema changes only in its
`description` string (the S2.1 binding sentence); no constraint changed.

### The added planning input
`check-integrated-carrier.v1.py` reads that file; without it the check cannot run. I verified:
- the candidate bytes (`8e6e8babd30bc342…`) equal the live architecture file, the live file equals git
  `HEAD`, and **`git show ffb3c0789:<path>` yields the same bytes** — the stated commit exists and the
  provenance is exact;
- it is referenced by `check-carrier-v3.py`, `check-integrated-carrier.v1.py` and `carrier-format.v3.md`,
  i.e. it is a genuine inherited input, not new authority;
- **with** it the integrated carrier check reports **406 passed / 0 failed**; in a scratch copy **without**
  it the same check dies with `FileNotFoundError` on exactly that path.
So this is closure of a checked input set that was silently incomplete in earlier candidates. Adding an
unchanged, already-accepted architecture file and pinning it is the right repair.

## Owner checks, re-run in the required order (`claude-out/checks/`)

Envelope qualification → pass, receipt written. Integration with that receipt → **423 / 0**. Security
**581 / 581**, **16 / 16** sweeps (new `operational-file-exact-canonical-bytes`: 161 checks), pins valid.
Integrated carrier **406 / 0**. Foundation 231; workflows 1,816; native 477 / 66. All reproduce.

## The codec, read line by line

`decode(kind, raw)`: `kind ∈ {witness, floor}` (exact `str`); `raw` must be exactly `bytes`; strict metadata
loader (4 MiB, depth 64, no BOM, no floats or non-finite, no duplicate keys, i64 integers, valid UTF-8);
then `encode(kind, value)` — which runs the closed shape and then `canonical_bytes` — and finally
`raw != expected → NONCANONICAL_BYTES`. `encode` refuses any value that fails the shape, so a writer cannot
emit an inadmissible file. Every foreign exception is wrapped as an `OperationalFileError`.

The floor shape is: exact member set; `highWaterSchema` a strict integer 1; then the floor is *projected
onto the retained v8 witness shape* (`lastSeq → seq`, `tailSha256 → bodySha256`, state `COMMITTED`) and that
validator is reused. That gives the floor, for free and from one owner, the digest grammar (full-string),
`grantGeneration` in `1..2⁶³−1`, `lastSeq` in `0..2⁵³−1`, non-boolean integers, and — because the v8 rule is
"null only at `COMMITTED 0`" — exactly **`tailSha256` null ⇔ `lastSeq == 0`**. One statement of the rule
instead of two is the right architecture.

## Independent probes (`claude-out/probes/codec.json`)

**Spellings — 27 per file kind, 54 in all: only the two canonical encodings are admitted.** 24 refuse at
`DECODE` (BOM, duplicate key, `1.0`, `1e0`, leading zero, `+1`, trailing NUL, two documents, empty,
invalid UTF-8, nesting 65, over 4 MiB), 18 at `NONCANONICAL_BYTES` (negative zero, trailing newline / space
/ CRLF, leading space, inner whitespace, reordered keys, escaped ASCII in a value, escaped key), 10 at
`SHAPE` (unknown member, `[]`, a string, `null`, upper-case hex).

**Shapes — 36 values, each presented as exact canonical bytes so that only the shape rule decides:** every
outcome as the owners specify. Admitted: genesis; `COMMITTED 1`; `PENDING 1`; `seq = 2⁵³−1`;
`grantGeneration = 2⁶³−1`; floor `0 / null`; floor `1 / hash`; `lastSeq = 2⁵³−1`. Refused: `PENDING 0`;
`COMMITTED 0` with a hash; `COMMITTED 1` with null; **hash member absent** (missing ≠ null); `2⁵³`; boolean
or negative sequence; generation 0 or boolean; schema 2 or boolean; lower-case state; 63-character, integer
or **trailing-LF** digest; floor `0 / hash`; floor `1 / null`; floor with `tailSha256` absent; a floor with
an extra `state`; **a canonical witness presented as a floor, and a canonical floor presented as a
witness**.

**Two statements of the floor shape agree.** 30,000 mutated floor values through (a) the codec's shape and
(b) the JSON schema `carrier-highwater.schema.v1.json` plus the null-iff-zero rule: **30,000 agree, 0
differ**, 0 exceptions.

**Byte fuzz.** 60,000 byte-level mutations of four canonical files: 59,668 refused, 332 admitted, and for
every admitted input **`encode(decode(raw)) == raw`** — 0 violations, 0 untyped exceptions. (The 301
admitted non-seed inputs are simply other valid canonical files — a changed digit or hex character.)

**Type guards.** Unknown / `None` / list kind → `KIND`; `str`, `bytearray`, `memoryview`, `None` →
`BYTES_REQUIRED`.

## Mutation evidence (`mutation.json`; pins valid and 581 cases executed for every mutant)

| Mutant | Result |
|---|---|
| `raw == C(value)` check removed | **killed** |
| closed shape skipped | **killed** |
| floor adapter shape skipped | **killed** |
| floor null-iff-zero weakened | **killed** |
| floor schema constant unchecked | **killed** |
| floor member set not exact | **killed** |
| strict loader replaced by `json.loads` | survives — **admission-equivalent** (N-2) |
| `bytes` type guard removed | survives — **small real gap** (N-1) |

I resolved the two survivors by running the original and the doubly-mutated codec over my spelling corpus
(`survivor-equivalence.json`).

### N-1 (low) — without the type guard a `bytearray` is admitted
`bytearray(canonical) == canonical` is `True` in Python, so with the guard removed a mutable buffer is
admitted; no fixture presents one. The shipped guard is correct and the contract's requirement that raw
bytes be *retained* for byte-stability comparison is a reason to insist on an immutable value. One
`bytearray` negative pins it.

### N-2 (low) — the strict loader is admission-equivalent to a lenient one; only the refusal class differs
With `json.loads` in place of the strict loader, **no spelling changes admission**: BOM and duplicate keys
move from `DECODE` to `NONCANONICAL_BYTES`; floats, exponents, `NaN`, `Infinity` and deep nesting move from
`DECODE` to `SHAPE`. That is a consequence of the design, and a good one — exact-byte equality subsumes the
lexical rules. It does mean the contract's stated *order* ("first applies the strict metadata loader") is not
pinned, because the fixtures do not assert the refusal class. If the class is meant to be observable (for
the "bounded reason" S2.1 allows in diagnostic records), assert it in a handful of cases; if not, say the
class is advisory. Either is fine; today it is unstated.

### N-3 (observation) — the module imports the whole security model to reach the metadata codec
`operational_file_reference.py` loads `security_lifecycle_model_v1.py` to obtain `_RV8`. That buys the UCD-15
load guard and a single pinned path to v8, at the cost of importing ~3,400 lines to use two functions. It is
declared ("explicit pinned dependency") and harmless in a reference; a Rust implementation should depend on
the metadata codec directly.

## Seams with the open decisions (so nothing is inferred)
- **D2** is untouched. S2.1 ends "generation selection and stable read-only diagnosis remain separate from
  this byte rule", and a present-but-unadmitted witness is only "the existing `witnessMalformed`
  observation" — whether and when that may be *reported* is still my storage Q2 / D2.
- The rule is **prospective**: "No current product writer has been shipped or admitted by this
  implementation sequence". I did not look for development witness files and none is claimed.
- S2.1's diagnostic hash rule — an exact raw SHA-256, "never a normalized-byte hash pretending to bind the
  original file" — is the right statement and is consistent with the editorial correction I proposed for
  Step 4.

## Commands and outcomes (all under `claude-out/`)

| Command | Outcome |
|---|---|
| `verify_extract.py` (before extraction; after all work) | 1,440 / 1,440 verified from tar; 0 unsafe; unchanged |
| planning-input provenance (`git show ffb3c0789:…`, `git diff HEAD`) | bytes identical at the stated commit, at `HEAD`, and in the candidate |
| owner checkers, required order | envelope pass + receipt; integration 423 / 0; security 581 / 16; foundation 231; workflows 1,816; native 477 / 66 |
| integrated carrier check **r1** | **Invalid — reviewer omitted the required `--source` argument** (argparse exit 2). Preserved with a note. |
| integrated carrier check r2 | 406 / 0 with the planning file; `FileNotFoundError` without it (scratch copy) |
| `probes/codec.py` | 54 spellings, 36 shapes, 7 type guards, 30,000-value schema differential, 60,000-input byte fuzz |
| `probes/mutation.py` **r1** | **Failed — reviewer script-generation bug** (newline escapes lost through a nested heredoc → `SyntaxError`); no mutant ran. Preserved. |
| `probes/mutation.py` r2 | 8 mutants, all valid: 6 killed, 2 survive |
| survivor equivalence **r1** | **Failed — reviewer path bug**; no comparison ran. Preserved as a note. |
| survivor equivalence r2 | lenient loader: 0 admission differences; type guard: `bytearray` admitted |

Toolchain: Python 3.12.13 / UCD 15, OpenSSL 3.6.3; aarch64 macOS.

## Limits
1. Pure reference only. No file was read or written by the codec or by me; presence, custody and stability
   are other owners.
2. The codec inherits the retained v8 witness validator and metadata codec; I exercised them through this
   module and did not re-review them here.
3. Mutation covers the codec's eight decision points, not the rest of the tree.
4. I re-ran but did not review the foundation / workflows / native checkers, and verified the pin
   inventories (29 + 9 + 9 changes) through the checkers and my harness rather than re-deriving each round.
5. D2, D3–D6, the Rust drafts and everything else in the storage / journal groups remain open.
