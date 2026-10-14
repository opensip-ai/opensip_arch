# Codex review: S-M-DESK-U4A-r1

**Verdict: ACCEPT.** No required findings or nonblocking observations. The six SM-8 desk rows apply D-6, and the twelve snapshot2-equivalent population records apply D-9. This accepts U-4a's derivation, not the assembled S-M report or any gate closure.

## Subject and boundaries

Stage: `/tmp/opensip-implementation/s-m-desk-u4a-r1-stage`.

`subject.json`: 1100 bytes, SHA-256 `30c07eac6c6836ba7974b6bc41e7a698b34b2372fcf18f924ea7aa0951ec3299`. Independently rehashed all four members; every size and digest matches:

| Member under docs/implementation/m3/spikes/s-m-desk-u4a-2026-10-13 | Bytes | SHA-256 |
|---|---:|---|
| REPORT.md | 4194 | db658a66c0cb49ef4187e1f8265f2294e6028be799c57a2ce2152c433b2ca8e4 |
| derive_u4a.py | 5949 | ea3cf8c0c30ae80d54187d16e3473f1a2b5adb3525252080b9498b29dd697efa |
| runners/freeze_s_m_desk_u4a_r1.py | 5561 | d387acff9c6e624c41bbd46cba8cc8de0868130fbd5cf9a1ea0a77bd5f1d8f76 |
| u4a-desk-records.json | 29345 | b1586053c18a36312189d5660c4a8485a56168e578e343c3532649bb40914f99 |

Live product HEAD is `95279fa8ae086f98bd221cd827f6c0efc156c0c5`, clean; architecture HEAD is `fe77f91641c34f3b0c2997e34f53726b99d09149`. Its pre-existing untracked held E2s directory was not read or changed. The committed accepted PLAN-r2 and review retain their previously reviewed hashes `b4f7c332…` and `6f30038c…`.

## Derivation reproduction

Before execution, checked that the external derive_u4a.py and u4a-desk-records.json equal their staged copies. Inspected the derivation: it reads the specified accepted evidence and writes only its adjacent output JSON.

Ran exactly the permitted command:

`nice -n 10 python3 -I -B /tmp/opensip-implementation/s-m-desk-u4a-2026-10-13/derive_u4a.py`

It exited zero and reproduced the output **byte for byte**: 29345 bytes, SHA-256 `b1586053c18a36312189d5660c4a8485a56168e578e343c3532649bb40914f99`. No compiler or experimental driver ran.

## SM-8 checks

Independently checked all six rows against results.json and all 42 selected stdout files. Selection is exactly non-warmup ordinals 3 through 9, each with exitCode zero. Evidence basenames match the selected workload and ordinal, hashes match the derived provenance, and every input equals its committed Git blob. Express uses the synthesized-program series, not the cohort's initialization-only entry.

The independent calculation flattened every configuration's retained calls, including incomplete configurations, before taking the per-run maximum. Across the six rows this covers 2464 configuration observations, including 189 incomplete observations, and 383054 retained public-call observations. Every recorded maxPublicCompilerCall agrees with its configuration's retained maximum; configurations lacking that field are incomplete. Per-run winning call names/durations and all six medians/maxima agree with the submission.

Hand spot-checks, using the fourth sorted value as the seven-sample median:

- **Napi:** ordinal3..9 maxima in ns are 105719167, 114748583, 105551625, 105684042, 106265292, 107590334, 105060958. Sorted median is **105719167**, maximum **114748583**, both createProgram. In ordinal3, cli/tsconfig.json supplies the winner; the two incomplete configurations' maxima, 283916 and 118250, are included and smaller.
- **Express:** maxima are 109893958, 106777125, 106561208, 105831250, 105494833, 106490417, 107415500 ns. Sorted median is **106561208**, maximum **109893958**, both createProgram in the synthesized configuration.
- **Vite:** the independent sorted median is **198878333** ns and maximum **206101000** ns, both getSemanticDiagnostics, matching the displayed 198.878/206.101 ms.

All report values round correctly to three decimal places. The public-API granularity label is adequate under D-6: createProgram per configuration and getSemanticDiagnostics per file, with the program-wide blocking caveat retained for the D-law liveness-floor use. These records do not measure the entire uninterrupted event-loop stretch or replace the accepted definition with a different timing boundary.

## S_eff first-term checks

Independently compared every selected row with the accepted sealing checks.json input. The eight medium rows and four large rows copy regularRows, bytes, snapshotDescriptorBytes and all three bound flags exactly. Source checks hashes match, and both files equal their committed blobs. In total, 46 distinct evidence/result/check files were compared with Git bytes.

Recomputed each bound separately: rows ≤100000, descriptor bytes ≤4194304 and total bytes ≤8589934592. All twelve selected populations are within every bound. Rspack's 4085164-byte descriptor leaves exactly 109140 bytes below the descriptor bound; that is measured headroom, not an extrapolated row ceiling.

No ceiling is derived from average bytes per row. The records remain measured repository-only snapshot2-equivalent populations, not native admission. Every Rust row marks the D-2 dependency-source part owed and separate from snapshot2's rows. The final S_eff minimum and its later-owned terms are not filled.

## Split and standing

The report explicitly splits U-4a's SM-8/first-term desk derivations from U-4b's per-component SM-10 and coverage-labelled SM-4/SM-10 work. U-4b follows U-1 because its analysis coverage can change. This is a sound partition of the accepted plan's owed desk work; it does not claim full U-4 completion or skip U-1, U-2, other measurements or report assembly.

No placeholder, S_eff, F, T or outcome is recorded. SMComplete, LG1Met, effectiveL and productQualification remain false. O7, D3 and D13 remain closed; only L-G1 remains open among L's gates. Lead-host figures remain preliminary, not D12 or qualification evidence.

Only read-only inspection, hashing, JSON parsing, Git queries and the expressly permitted derivation were used. Its sole authorized working-output rewrite was byte-identical. No compiler, Cargo, Node, tests, other driver, lane, network, other pane or delegation. No private 413 fixture, installation directory, signing keys or held-tree content was read. Neither repository, stage nor control files were edited. Only REVIEW.md and review.json were otherwise written. Exact lead assent and fresh design verification before architecture publication remain separate lead work; nothing was pushed.
