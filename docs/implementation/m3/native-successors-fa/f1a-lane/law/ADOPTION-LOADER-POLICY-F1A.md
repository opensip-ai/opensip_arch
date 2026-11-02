# Adoption receipt: the F1-a check-boundary loader policy (POLICY-DELTA-DRAFT r3), 2026-10-31

**Decision LD-COORD-F1A-LOADER (coordinator, session 9ce22ffd, under OD-AUTO-1; custody-verifier tooling; flagged to the owner).**

**Adopted:** the two loader exceptions D-1 and D-2 of `f1/evidence/f1a-boundary/draft/POLICY-DELTA-DRAFT-r3.md`, sha256
`a76b42971ac35422b143bd29994d841a613a18d0a400e36107edfdd242470410` (verified at signing), at product `b3d215c0010082f4d7afce47f86f9cb1b2445a65`, policy `8e660469…`:
- **compiler.ts** `import(location.compilerUrl)`: a runtime load of the closure's pinned TypeScript T.
- **gen-ts-enums.mjs** createRequire: build time only, with the digest checked before the load.
D-3 is informational and NOT adopted (the reviewer did not score it).

**Basis, bound by value:** the R3 different-vendor review (Codex gpt-6-astra/high, codex-f1a-policy-r3 at w36),
`review-r3/REVIEW-r1.md`, sha256 `b7562b842f18d24a4109466a79ca82efbf83bc20cb76bc8cc2688f296201ecfd`:
`LOADER-COMPILER-TS: ACCEPT`, `LOADER-GEN-TS-ENUMS: ACCEPT`, `CONDITION-F1C: ADEQUATE`, with no required findings. The request is `REQUEST-r1.md` (`286c2c04…`), with lock `1a8fb92a…` (757 rows).

**Binding condition: carry CP-F1C-COMPILER-VERIFY, as the reviewer sharpened it in §4. All five parts are required at F1-c review:**
1. Verify the ACTUAL `lib/typescript.js` row of the selected D_T. The row must be PRESENT, because an absent row is refused (verifyToolClosures only iterates the rows it is given). Then import that SAME path.
2. The mismatch control observes ZERO import or module-execution attempts, plus a process fault.
3. A valid-row positive reaches the import.
4. A mutant that moves the import before the verification fails the zero-attempt observation.
5. The residual stays recorded: the re-read after verification is F4's release custody. Atomic verify-and-execute is NOT established.

**Owed at selection (non-blocking corrections from the review):**
- reword the gen-ts-enums reason (`provider-loader-policy.DRAFT.json:493`): the order is digest, then load, then version;
- add the reverse kind-separation test (the product kind on tooling refuses);
- record the REQUEST item 8 test-attribution correction and the narrower custody wording.

**Not adopted here:**
- the contract successor selection;
- the final checker and policy re-pin against the real provider inputs;
- the 74 inventory rows (binding);
- the bound-lane run;
- integration.
