The review is written. **Verdict: changes-required.** The candidate is close, but it isn't yet good enough to be the single input for the shared Rust/TS generator plus handwritten admission. It has six required findings, and each has a concrete fix that needs no wire change.

**Frozen subject:** 18 files, manifest sha256 `01f4ba5d…0cab`. The complete file set matched the manifest before and after the review. My rerun of `check.py` from a scratch copy gave 133 checks, 0 failed, identical to `check-result.json`, and `selftest.py` again caught all 16 controls. That clean result has two catches (the first two findings).

**Required findings:**
1. **The checker needs files outside the frozen set.** It reads three /tmp author files (the TS and Rust translation `fields.json` and `resolutions.md`). With those paths removed it crashes with `FileNotFoundError`.
2. **Source pins are incomplete.** The pinned model code loads files that aren't pinned: `discovery-defaults.py`, `native-capability-matrix.v2.json`, `identity-schemas.v2.json`, `capability-manifest-domains.v2.json` and `check-fact-plane.py`. When I byte-changed three of them in a copy of the architecture, the checker still passed 133/0. The CVE1 owner `resolved-inputs.v2.json` and the generator `options.json` are also cited but unpinned.
3. **PreparedOutput row bounds (author choice 1): rejected.**
   - The manifest limit is retained at 256 total entries, but the candidate allows up to 2,000,256.
   - It also treats an oversized prepared set as a host bug (`operational-failed`). Such a set can come from a real user repository, so it should be refused before spawn as `request-rejected` / `REQUEST.PRECONDITION_FAILED`.
4. **ProviderFault phase and null rules (part of choice 3): rejected.** The worker can send ProviderFault while a host frame such as SnapshotManifest or Analyze is still in flight. The P3 table admits both of those interleavings as a provider fault, which I confirmed with the native model. The worker can't know the host's phase at receipt, so the rule turns a lawful fault into a protocol violation. Cancelled `observedPhase` is fine.
5. **`Rust3CanonicalPath` doesn't match the rust2 rule it cites.** Because `.` doesn't match newline, it accepts paths like `a\n/../b` and `a\n//b`. The dependency-source path pattern taken from the native-evidence schema has the same hole. No regex dialect is declared, and 13 patterns use lookahead, which the Rust `regex` crate doesn't support.
6. **`packageKey` contradicts the owner schemas.** A key built from the owner field limits can reach 4,610 characters, against a registered maximum of 4,096. `minScalars 5` refuses the valid key `"a 1 "` (empty sourceId). The claimed sort-order equivalence breaks if a name contains a byte ≤0x20, which the schema allows.

**Other author choices:**
- **Accepted:** the `outputSeen` guard on P3-25; the host never sending Cancel before Hello; Cancelled `observedPhase`; the `exec1_` grammar and both 4096 path bounds; and the 100,000-anchor limit.
- **Also confirmed against owners:**
  - the per-key scope2 recipe;
  - the raw TS2 manifest digest;
  - the dependency-source self-reference;
  - the non-empty wire anchor rule versus the zero-length fact2 rule;
  - the fact-ref refusal;
  - the inert-only row kinds;
  - the CBOR profile differences (independent byte probes);
  - field coverage, exactly TS2 200/200 and Rust3 372/372.

**Advisories:** there are 10. The most important: 10 of my 14 mutations to the handwritten rules still passed the checker, because the checks pin literal values rather than rule behaviour. Also, 20 of the 26 pinned architecture files are uncommitted in the working tree.

**Limits:** no generator was run, and the author's CBOR codec is test scaffolding. I accepted the fixture-heavy joins from the author's owner checks plus my reading of the owner code, without re-deriving them. I deliberately didn't read the `author-01` or `root-validation-01` directories, and I deleted my temporary 20 GB architecture copy after recording its result.

Files are in /tmp/opensip-implementation/m1-native-wire-owner-review-01:
- review.json
- review.md
- scratch/
