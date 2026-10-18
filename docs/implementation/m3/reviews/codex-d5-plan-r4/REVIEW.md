# D5 plan r4 review

**Verdict: REQUIRED-FINDINGS.** The Boolean path treatment is materially corrected, but the disabled-build-target case still lacks a closed classification and matching control.

## Subject and provenance

Verified the 933-byte subject manifest at SHA-256 `6a57ec202520eadb301eeba104e312b06a3b245469867e5c615a0fb004542048` and independently rehashed all four members. PLAN-r4 is 61,774 bytes at SHA-256 `866647e2ab1733ef2dcfe687fe511a27db80f3021052393297d5da97a3340f1d`; r1 through r3 match both their manifest pins and the unchanged historical copies in the architecture checkout. Product main remains `4e475c753002d21ed99e0d53e64218e55af0cb1f`, architecture remains `e9474b1fe502c82a477ddafe15cf16ad0a92766a`, and all eleven opening authority hash prefixes match the referenced live files.

The r3-to-r4 diff is confined to the stated status/disposition text, LD-D5-6, the corresponding D5-0 controls and Q10. The r3 portions previously accepted by the review, including Q9's D1b ownership, remain unchanged.

## D5PLAN-R4-RF-1 (P2): Close the zero-root case for `build = false`

Location: `d5/PLAN-r4.md:184-193,345` (LD-D5-6 roots/classification and D5-0 build-root controls).

The enabled cases are corrected: implicit and custom build scripts are production roots, ordinary helpers inherit their reachability, exact environment reads remain site-level baseline entries, and both owner tools receive matching spawn/environment controls.

The disabled case is not closed. `build = false` removes the implicit `build.rs` production root. The test-gate rule then says a region may be test code when no production-root path is satisfiable with `test = false`. With zero production-root paths, that statement is vacuously true unless the plan explicitly requires a nonempty gated path. The fallback for unknown or unresolved analysis does not cover a successfully resolved source file that simply has no effective target. The only disabled-target control says that a file also reached by another production path stays production; it does not exercise the dormant `build.rs` or its helper with no alternative production edge.

Required change: state that a source region in scan scope with no root path is non-exempt (or makes the structural check fail), and that a gate-based test exemption requires at least one resolved path whose combined condition proves `test`. Add a `build = false` temporary package whose otherwise-unreachable `build.rs` and helper contain a planted forbidden spawn and environment read, with no alternative production edge; require both owner tools to refuse them. Keep the existing mixed-path control separately.

## Boolean reachability and Q10

The remaining Boolean correction is sound at plan level. Conditions from targets, enclosing items and inline modules, declarations and ancestor edges are conjoined per path and alternative paths are disjoined. `not(test)`, `any(test, not(feature = "crash-matrix"))`, mixed production/test paths, alternative ungated feature paths and unsupported conditional syntax cannot establish an exemption. Unknown atoms are considered over both truth values, and uncertainty fails closed. The positive and negative controls cover both owner tools and keep the relevant census/baseline data synchronized.

**Q10: REQUIRED-FINDINGS.** RF-2's Boolean-condition defect is resolved, and RF-1 is resolved for enabled implicit/custom build roots and their helpers. Q10 cannot be accepted until the zero-root `build = false` case is expressly non-exempt and controlled as described above.

This is a plan ruling only. No implementation, runtime behavior or qualification is accepted. No build, Cargo, rustc, lane, network operation or test was run. Only `REVIEW.md` and `review.json` were written in the request directory.
