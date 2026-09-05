# CI carrier independent review v1

**NO-OBJECTION-WITHIN-CARRIER-SCOPE — 0 MUST, 0 SHOULD.** Reviewer authored none of the five parent-authored subjects.

Freeze SHA-256: `2f5b798abb59a9388bac75c2b792069fb6a0f23bec56a5c130f362ec48014405`. All five subject hashes match before and after review; exact custody is retained in the companion JSON.

Fresh external replay passes **24/24**, byte-identical to the frozen report. **17 independent probes pass**, covering observed versus forged conflicts, refusal-before-conflict for missing/empty/unknown maps or mismatched digest, untouched owner forgery, deleted paths, source-record-change expansion, trailing-newline digest/tree rejection and the legal roleless sentinel. Inputs remain unchanged.

The admission precondition is independently acquired trusted observations: complete Git unit/component sets and changes, exact source-record ownership/digests, verified manifest dependencies and consumer/role/platform maps. Every caller ownership map is compared with those observations before conflict handling. A caller-invented conflict cannot obtain SELECT-ALL. The exact `.opensip-ci-ownership.json` source blob supplies the record digest; the compiled carrier is not recursively hashed as its own source record.

The model explicitly injects observations. Actual Git acquisition, strict raw JSON parsing, signature verification and CI execution are separate obligations. The full selector’s 26 scenarios, fixed-point selection and six lane result slots remain a separate reviewed unit. No qualification, subject change, register mutation or acceptance/SATISFIED state is implied.
