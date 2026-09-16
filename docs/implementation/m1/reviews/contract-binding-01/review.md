# Review: design-lock v3 contract successor binding

**Verdict: ACCEPT-UNIT**. There are no required findings.

- Subject manifest: `/tmp/opensip-implementation/m1-contract-binding-subject-01.json`
- subjectManifestSha256: `37e1112f314f1ab8affcc2c53749ec20d150e8d5760806cee24cf3ffe821cfe3`
- Baseline: `m1-successor-subject-02` (accepted binding2)

This review covers only the code binding. It does not establish full M1 completion, product qualification, runtime authorization or cryptographic reviewer identity. The checked-in lock is the trust anchor.

## Assessment

| Area | Result |
|---|---|
| Closed lock/version/pin shapes | v1, v2 and v3 field sets are exact. A bool or float version refuses, and so do v4, v2 with a contract successor, v1 with an inventory successor, and v3 missing either successor. The four contract pins are closed, and every byte-reading pin must have an int byte count. |
| Immutable joins | Review must be ACCEPT-DESIGN-UNIT with `[]` findings and must name the manifest sha. Root assent must be ACCEPTED-DESIGN-UNIT with `rootSubstantiveAssent is True` and `[]` findings. The subject, review and successor joins include path, sha and bytes. Isolated probes with rebinding reach each named diagnostic. |
| Candidate completeness | Record pin must equal its subject member row. Candidates must be exactly the other members, with identical pins, sorted and unique. All bytes are verified, and no candidate script is executed. |
| Accepted-parent membership | Each parent must be in the source/application overlay or be the selected inventory v3, with equal sha and bytes, and its bytes are verified. The real record uses 2 parents accepted only through the overlay, which the spec permits. |
| Parent preservation | A parent path that is also a subject member refuses. Output reports pins and overrides, and nothing is rewritten. |
| Before-text and selectors | Line selection needs an int ≥1 within the document. JSON Pointer handling follows RFC 6901: escapes are validated, array indexes must be ASCII digits without leading zeros, and the pointer must resolve. The before-text must match exactly, and after must be a nonempty string that differs from it. |
| Duplicate/stale/malformed | Duplicate (parent, selector) pairs refuse, as do stale before-text, unknown override fields, override parents outside the record, and a missing or non-list `passageOverrides`. |
| previousCandidate | Checked as a closed pin with verified bytes. It is not treated as an approval. |

## Advisories (non-blocking)

- **CB-A01**: Candidates are checked against declared parents only. A reviewed candidate could reuse the path of an accepted overlay file that is neither a lock input nor a parent, with different bytes (probe passed). The real record has no such collision.
- **CB-A02**: `str.splitlines()` also splits on `\x0b \x0c \x1c-\x1e \x85 U+2028 U+2029`, so line numbers can differ from a `\n`-only consumer. The real parents contain none of these characters, and each before-text occurs exactly once. Consider specifying `\n`-only splitting.
- **CB-A03**: A line selector and a pointer can address the same JSON passage with conflicting afters. The duplicate check compares selector spelling only.
- **CB-A04**: The record's top-level fields and schemaVersion are not closed. Unknown semantic fields are silently ignored.
- **CB-A05**: `==` accepts float byte counts such as `1521.0` in assent join pins and override parent pins. Pins that read bytes still require an int.
- **CB-A06**: A pointer on a non-JSON parent, or non-UTF-8 bytes under a line selector, raise ValueError subclasses rather than DesignError. The tool still fails closed. RecursionError on deeply nested JSON predates this change.
- **CB-A07**: Mutation testing killed every join, decision, membership, overwrite, duplicate, before-text and version guard. Some guards would fail open without any test failing: pointer-does-not-resolve (`/files/7/description/x`), line ≥1 (0 selects the last line), unknown override fields, previousCandidate bytes, leading-zero index (the fixture array has length 1), empty after, unsupported selector and slash-prefix. Probes confirm the shipped verifier refuses all of these. Adding isolated tests is recommended.

## Executed checks

- Manifest and all 13 files: sha256 and byte lengths verified before and after. No extra files or bytecode in the frozen root.
- `diff -rq` against binding2: only the three stated files differ.
- Read the v3 proposal, the full verifier, the full tests, the lock and the bound arch artifacts. The failed test source differs only by the stated deepcopy fixes.
- 29 unit tests OK in a byte-identical copy.
- Real verification (absolute arch path) before and after probes: passed, 46 inputs, inventory v3 (+4 files), 9 candidates, 4 overrides, productQualification false. `--architecture .` fails closed.
- Mutation testing of the new code: 40 mutants (`mutate.py`).
- 80 adversarial probes on a mirror of all pinned arch files with downstream rebinding (`probe.py`, `probe-results.json`). All 74 refusal/pass expectations were met, and 6 advisory behaviors were confirmed. My first probe run had an aliasing bug in its own harness; it was fixed before results were counted.

## Limitations

- The substance of metadata-v2 and the semantic correctness of the passage overrides were not reviewed. They rely on the existing Claude design-unit acceptance and root assent.
- Rust was not rebuilt (bytes unchanged).
- The arch working tree has unrelated uncommitted changes. Verification relies on pins.
- The mirror and mutation work trees were deleted after the runs. The scripts and results are kept in this directory.
