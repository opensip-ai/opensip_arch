**Verdict on author05: changes-required.** Two small required findings and four advisories remain, but the four review-04 required fixes hold up under my own probes. The write-up is in `m1-native-wire-owner-review-05/review.json` and `review.md`; probes, mutants and outputs are under `scratch/`. This is a resumed review from my review-03/04 context, not a fresh session.

**Custody (before and after):**
- **Subject:** 102/102 files, bytes match, no bytecode in subjects 03, 04 or 05.
- **Inner manifest:** 40 inputs, 4 outputs, 57 evidence files, plus the manifest itself.
- **Pins:** 44/44 match, and the Node pin is unchanged. Against HEAD `c3856824`, 12 pinned files are modified and 18 are untracked.
- **Earlier evidence:** the review-04, root-04 and subject-04 copies under `prior/` are byte-equal to their originals.
- **Method:** nothing was imported from the frozen subject, and every run used my own copy with `-I -B` and a private pycache.

**My reproduction from only the 40 inputs:** check 567/0, identical to the frozen result, and selftest 132/132. For root, I only saw its check result (567/0); there was no root selftest or isolation run, so I don't claim either. The receipt confirms root04 ran checks only.

**What I verified independently:**
- **Prepared limits:** they now apply to every non-rejected owner outcome and count all carried rows. That is justified: the owner's set identity hashes every row, and dropping one row changes it. Defaulted over-limit sets fall back with zero usable rows and keep the stale evidence; explicit stale sets keep the owner's refusal first. The planner refuses manifests with too many entries.
- **ECMA scope:** only the four scoped model instances are affected, and no shared canonical validator is patched. Identity v2/v3, workflows common, c2v3 and rust2 give the same results pinned and scoped through their real consumers.
- **Relation paths:** `x<LF>/../y.rs` is now refused and `a/..<LF>` admitted, across all four payload fields.
- **Cancel position and fields:** a Cancel before Hello is refused, and wrong execution, ordinal or reason are refused.
- **Mutants:** all 12 of mine are caught, including the four that survived review 04.

**Required findings:**
1. **The sender checks the Cancel echo against the plan, not against what was actually sent.** I sent a same-length substitute `executionId` in OpenUniverse. The sender accepted a Cancel echoing the planned value and refused the true echo of what was sent. It also accepted a substituted SnapshotManifest digest of the same length. An `analysisOrdinal` of `False` passes because Python treats `False == 0`; the carrier rejects it. Fix: bind each slot to its planned payload digest, and compare the Cancel by encoded bytes.
2. **Two wording problems.**
   - `contract.md` still says root ran 108 mutants, which contradicts the receipt.
   - The `OWNER-PATTERN-EVALUATION` rule calls an unpromoted, in-memory successor "the selected final owner".

**Advisories:**
- **Fact-plane `_is_path`:** not a live contradiction for fact2. The control-character ban is stricter than fact-plane v1's own `CanonicalPath` text, and fact2 admission (identity-model.v3) never calls `_is_path`. The contract wrongly implies newline paths would be refused at fact2 admission. The real gap is that relation v2 `CanonicalPath` admits `a//b`, `a/` and control characters, pinned and scoped alike; that belongs to the relation-registry unit.
- **Worker read authority:** the manifest carries stale and failed rows with no usable-row marker. The duty should say whether the worker recomputes staleness or the host sends the partition.
- **Carried-row counting is deliberately strict:** 257 rows with one stale row loses all 256 usable rows. Keep the vector that pins this.
- **Pins and trust:** root must keep the 44 exact pinned bytes. Node's system libraries are trusted but unpinned, and the audit only covers file opens and process launches.

**Not done:** no full retained `admit_frame` run, no production sender, admission, generator or platform qualification, and no Rust regex lowering (the crate isn't available offline).
