GROK2 review: **CRC-1**, the identity contract successor that carries out item 9 of law M3-C. CODEX2 accepted r6, and then r7, which leaves item 9 unchanged. CRC-1 defines the core detector, provider and adapter closures and the fields each may occupy. This is a **design unit** (a `verify_design` contract successor). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** with `subjectManifestSha256`, or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/grok2-crc-1-r1`.

(Lead note: this request was first written for Codex. GROK2 reviews it, because it was free. Product main is now `cd5958b` (82 contract successors); the unit binds there, 82 → 83, per its `verify_scratch`. Don't run cargo; P0's lanes are using the machine.)


**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation. Run git only read-only.
- **No builds or tests.** Run no cargo, no tests and no crash-matrix binary or checker.
- **Scripts.** If you run anything, use only the evidence scripts below and read-only commands, at `nice -n 19`, with any scratch files under your review directory.
- **`verify_design`.** The lead ran the real `tools/verify_design.py` in the scratch harness (`evidence/verify_scratch.py`). The harness writes nothing; it holds a synthetic review and assent in memory. You may rerun it. Never edit the product or its lock.
- **Never touch the real home.** `~/Library/Application Support/OpenSIP` stays absent; do not read or create it.
- **Never read the private 413 UUID fixture.**
- **Product main is `9c11c53`**, read only: B-S1's binding, with 79 contract successors. The record is built on it.
  - The checkout has since advanced to `cd5958b`, which binds B-S2, B-S9 and I1-P (82 successors) and X4-F1.
  - The README records that CRC-1 also binds there, and that none of those units touches a CRC-1 key.

## Subject

The pins are in `hashes.txt`. Every file is untracked in arch until acceptance.
- **The subject manifest** is `docs/implementation/m3/snapshot-plan-c/crc-1-subject.json`. Its sha256 is `subjectManifestSha256`.
- **Its 7 members** are:
  - `crc-1/successor.json`;
  - `README.md`;
  - `PASSAGES.md`;
  - `evidence/vector.json`;
  - `evidence/build_crc_1.py`, `check_crc_1.py` and `verify_scratch.py`.
- **Not part of the subject:** `crc-1-unit.json`, the lead's DRAFT-PENDING-REVIEW record.

**Law.**
- `snapshot-plan-c/PROPOSAL-r7.md` (`a1ee9386…`) is your r7 acceptance. Its item 9 is r7:414-477, its CRC-1 row r7:1052 and R1 r7:1210.
- `PROPOSAL-r6.md` (`8274bca1…`) is your r6 acceptance, with X-C1. r6 and r7 differ only in row 8 and R1's wording.
- M3-E1 r3 item 14b (`syntax-e/PROPOSAL-r3.md`, `d71031ff…`) is X-C1's source.

## What it does

The README has the full tables. In brief, there are **nine insert-only passage overrides on six accepted parents.** Each line selector is on a Markdown parent and each JSON Pointer on a JSON parent, and none is already bound:
1. **IE:285.** A new paragraph, **Core role closures**:
   - the core detector, provider and adapter closures are EC1's descriptor D with another `kind`;
   - their `manifestDigest` is the TR-CORE-signed inventory body, which also covers EC1's kind-`evaluator` wording at IE:273 and IE:455 for every core role closure;
   - none is a component-manifest closure;
   - **recognition:** a closure is a core role closure of a Plan exactly when its descriptor equals the Plan's core evaluator closure's descriptor except for `kind`;
   - **the admitted fields**, a closed list, so any other field refuses, `cache-key.producerClosure` included:
     - **detector:** bundled-pack emission rows and `finding.ruleClosure`;
     - **adapter:** `import.adapterClosure` of `dependency` and `prepared` imports only, never a `semanticClosures` member;
     - **provider:** exactly two uses. One is `import.producerClosure` of those imports. The other is the producer of syntax-universe work only, in `subject-scope.enumeratorClosure`, `view.producerClosure` and `fact.producerClosure`, `stage-spec.producerClosure`, `enumerator.closureId` and `CandidateProducerResultV1.producerClosure`. It is a `semanticClosures` member exactly when a syntax universe is selected, and never on a TypeScript or Rust record;
   - **the detector join** at Run closure;
   - retention and the identity consequence.
2. **IE:1377.** The `semanticClosures` exception for the core provider and adapter closures.
3. **IDS-L, three JSON Pointer strings.** IDS-L is I1-L's selected copy of the identity schema bundle: `docs/implementation/m3/preview-pack-i1/i1-l/design/foundation/identity-schemas.v3.json`. The three pointers are:
   - `/$defs/closure/properties/manifestDigest/x-opensip-digest/artifact`;
   - `/x-opensip-digest-domains/closureKinds/note`;
   - `/x-opensip-digest-domains/closureMembership/selectionLaw`.

   `byField` and the kind list are unchanged.
4. **COMP:9.** The bundled-pack detector join, beside "A provider or evaluator closure cannot stand in for it."
5. **WS:308, WSE:312 and DMS `/description`.** `closure.manifestDigest` is the core inventory body for a core role closure that carries a detector compatibility listing.

**A vector** on EC1's `baseline-macos` fixture gives all five closures of one core:
- detector `closure2:be7bd6cc…`;
- provider `closure2:df5e7cba…`;
- adapter `closure2:670d260f…`.

The core and evaluator closures equal EC1's vector. All 53 accepted fixture cases give five pairwise-distinct ids.

## Lead decisions for you to rule on

The README records nine, each with the alternatives it rejects:
- **LD-1.** The overrides use JSON Pointers on IDS-L and fresh lines elsewhere. There are no complete copies:
  - the original IDS's two EC1 pointers are bound, and a second override refuses;
  - a new IDS copy would be a sibling of SYN-1F's copy, which is drafted tonight from IDS-L.
- **LD-2.** IE:273, IE:278 and IE:455 are bound by EC1. CRC-1's paragraph extends their kind-`evaluator` wording instead of rewriting it. The verify_scratch probe shows that a second override refuses.
- **LD-3.** One core per Plan: recognition is by the Plan's core evaluator closure descriptor.
- **LD-4.** The admitted fields form a closed list, `cache-key.producerClosure` included.
- **LD-5.** No new refusal code.
- **LD-6.** The consequential passages COMP:9, WS:308, WSE:312 and DMS are included.
- **LD-7.** Product copies keep their bytes, as EC1 decided.
- **LD-8, X-H3** (M3-H r1, `fact-admission-h/PROPOSAL-r1.md` X-H3 and row 685). **CRC-1 does not resolve X-H3.**
  - **Why:** MC r7:443, :464 and :474 forbid the core provider closure on any TypeScript or Rust record, and a successor carries its law. M3-H is not accepted: Grok returned REQUIRED-FINDINGS on r1 and on r2, and r2 repeats X-H3 word for word. X-H3 changes C's Plan shape and controls. It gates only C4a's start (day 16), while CRC-1 gates C2a.
  - **Recommendation:** M3-C r8 once M3-H is accepted, plus a follow-on CRC-2 at fresh selectors (for example the blank line IE:286), before C4a.
  - **Rejected:** enacting it here; folding it into r7; a conditional clause; attributing the records to the language provider; a new kind.
- **LD-9.** Binding-only product commit before C2a.

## Cross-law items, recorded

1. **SYN-1F's IDS copy** (`syntax-e/syn-1f/`, unbound, drafted tonight from IDS-L). Whichever unit binds second takes the other in:
   - SYN-1F's copy carries CRC-1's three strings, or
   - CRC-1's three overrides are re-pointed to SYN-1F's copy. The lead checked that the draft copy leaves all three strings identical.
2. **Core packaging.** The syntax stage output schema must be a core platform tree member (IE:1303-1318).
3. **NIJ-1.** NE's import passages should name the core provider and adapter closures.
4. **X-H3**, as in LD-8.
5. **M5's detector listing receipt.**

## Decide

1. **Exactness.**
   - Is every `before` the exact parent text?
   - Does every `after` only insert?
   - Are the inserted texts true and minimal?
   - Is the IE paragraph exactly MC item 9 with r6's X-C1, and ME item 14b, neither wider nor narrower? Look especially at the admitted-field list, `semanticClosures` membership and the detector join.
2. **Form.**
   - Rule on LD-1 and LD-2: overriding I1-L's copy rather than the original IDS, and extending EC1's bound lines through a later passage.
   - Is the SYN-1F coordination stated correctly?
3. **Recognition and closure.** Rule on LD-3, LD-4 and LD-5. Is "the Plan's core evaluator closure's descriptor with another kind" a sound test at admission and at Run closure?
4. **Consequential passages (LD-6).**
   - Are WS:308, WSE:312, DMS `/description` and COMP:9 needed and right?
   - Does any other accepted passage still say that a closure's `manifestDigest` is always a component manifest body, or confine the core detector, provider or adapter closures differently? Look in IE, IDS-L, COMP, WS, SL, NE and the enumeration and execution-input schemas.
5. **X-H3 (LD-8).** Is leaving X-H3 to M3-C r8 and a CRC-2 right? Is CRC-2's binding path, at fresh selectors, sound?
6. **The vector.** Is it reproducible from the fixture, is it consistent with EC1, and does it fit IDS-L's closed `closure` shape?
7. **Selection.** Is the record well-formed under `verify_design`'s `contract_successor` and `successor_chain` rules? Is anything else wrong?

## Running the evidence (optional)

Use `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, from `docs/implementation/m3/snapshot-plan-c/crc-1/`:
1. `evidence/build_crc_1.py --check` rebuilds every generated file in memory and compares it with the files on disk. It reads the product lock and fixture at `9c11c53` with `git show`.
2. `evidence/check_crc_1.py` runs the independent checks: pins, `before`s, inserts, the IDS-L mask, the paragraph's clauses, the vector, all 53 fixture cases, and the README's passage list. `--rev cd5958b` also passes.
3. `evidence/verify_scratch.py --rev 9c11c53` binds 79 to 80 and runs the second-override probe. With no `--rev`, it uses the checkout (now `cd5958b`, 82 to 83) and also checks generation and admission sources.

The lead ran each twice, with byte-identical generated files.

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `crc-1-subject.json`. The lead's value is `adfa0d97dd525e631c5893bb568b7ba249d36b1cb2d95bb62e0da5ea4bc8d73a`.
- `"successor"`: `{path, bytes, sha256}` of `crc-1/successor.json`. The lead's value is 21459 bytes, `55b43151ec7d634fd42f14cc352658dfa6c848212428536db872403eafcd8477`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change bytes, give the exact replacement text. CR-1 (`codex-cr-1-r1`) is the sibling unit. The two share no parent and can be reviewed in either order. Do not commit.
