HSR r2: **ACCEPT**. HSR-RF-01 is closed; there are no required findings.

The reviewed law is docs/implementation/m3/syntax-e/hsr/PROPOSAL.md, 47157 bytes, SHA-256 f56145e21f6e05a3699c636bc0d6bc5bf0733decb7f213601670d70a927334fe. The diff base is PROPOSAL-r1.md, 44788 bytes, SHA-256 19770e3541f71139b2771350399e7967df6da8c6517b747e07d4a435d2d5ae6e. Codex is the single reviewer under the controlling r2 request; Grok is the implementation lead.

**HSR-RF-01 closure.**

Item 13 / LD-H10, line 222, now substitutes Some(H1) only for the 14 producer cases with null payloadSchemaDigest. It preserves every explicit declaration and every expected result and forbids editing the corpus or replacing wrong-schema's explicit digest.

I checked the fixture and test source at pinned product 43ea32a. The fixture has 15 producer cases: 14 null declarations and one explicit digest, wrong-schema's 64 zero digits. That case expects REFUSE, faults: [], and exactly native.coverage-payload-schema-not-registered. Its schema, Coverage and scope result fields remain unchanged. The test source at native_owner_tests.rs:865–869 uses None only for null and preserves explicit declarations.

The revised controls cover both reader states. HSR-T9 (line 256) requires the same wrong-schema refusal while H1 is dormant. HSR-T10 (line 257) and E2s-T3 (line 260) require it after H1 is active and retain the corpus byte checks. The 14 substituted declarations continue to select H1 in either state; the all-zero declaration remains outside the closed reader set. This addresses the original finding and preserves the unknown-digest negative control. It is a law and source assessment; no Rust test was executed.

**Other decisions and prior questions.**

The complete r1-to-r2 diff changes revision/review metadata, records HSR-1's existing acceptance, corrects LD-H10 and strengthens the three related controls. It changes no other substantive decision. Q1, Q2, Q3 and Q5 remain PASS: contract fit, the exact closed historical-reader table and its extension route, current-only minting versus retained checks, and S2/X9 scope are undisturbed. Q4 is now PASS because its sole required finding is closed; the remaining sites, controls and unit order are unchanged.

HSR-NB-01, nonblocking: item 15 at line 236 still labels the prerequisite law as HSR r1. The new introduction and acceptance gate unambiguously require acceptance of the corrected law. In a later record revision, change that label to HSR r2 or the accepted HSR law. This stale label does not alter the gate or revive r1's REQUIRED-FINDINGS verdict.

**HSR-1 and validation.**

HSR-1 was not re-reviewed. Its existing ACCEPT-DESIGN-UNIT review matches the requested 5297-byte pin, fd5906f65fda99ec5ea255812dffeab002de4b15d27bf75aaa9551bdf4771c7f. All six manifest members remain byte-identical to their accepted pins. This was a continuity check, not a second design-unit verdict. R1 binding evidence stands; verify_scratch.py was not rerun. No binding was performed.

All seven supplied r2 pins match, including the fixture and test source at 43ea32a. Product HEAD was verified as 43ea32a6419c961cec1e0ba30d7dd791acbd7f49. Python inspection used /opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B at nice -n 19 with a private 0700 TMPDIR under DARWIN_USER_TEMP_DIR. Temporary directories were removed after use.

Only this review.json and REVIEW.md were written in the requested r2 output directory. The r1 output files and repository contents were left unchanged. No Cargo, build/test lane, crash matrix, lane lock access, delegation, commits or pushes were used. The real OpenSIP home and private 413 UUID fixture were not accessed. HSR-a/E2s code, active-reader Rust controls and construction timings remain later implementation-review gates.
