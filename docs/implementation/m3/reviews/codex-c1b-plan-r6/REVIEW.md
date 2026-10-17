# C1B-PLAN-r6 review

**Verdict: ACCEPT.** No required findings or non-blocking observations.

C1BPLAN-R5-RF-1 is resolved. This accepts the revised plan and its design evidence, not C1b-1/C1b-2 implementation, integration, receipt freshness or qualification.

## Subject and verification

Manifest: `docs/implementation/m3/snapshot-plan-c/c1b-plan-r6-subject.json`, 4,746 bytes, SHA-256 `09c05df25923bdcb370e6eb7d38cc71d66d207cbe379bfed68026cd4a5d71d15`.

Independently rehashed all 22 members. Every one of round 5's 15 historical members retains exactly its r5 manifest pin. Live product and architecture heads match the manifest bases: `813d559efccbfc30b81b7530833c8427bb4f7dfd` and `fa875bfd5c2bc1627742c5363ebc2787b7db46ed`. Git confirms both identity and platform are unchanged between caa71e2 and 813d559 and in the scratch dependency worktree relative to 813d559. All 19 discovery cost-closure pins match current product bytes.

Read the r5 review, r5/r6 plan diff, derivation sources/outputs, scratch source/manifests/log, LogicalPath and native directory/file open implementations, Git tracking error/reach owners, r9's row-byte accounting and C1c-0's retention evidence. No evidence script or scratch program was executed. Independent read-only arithmetic reproduces the reach maximum, output-vector changes, doubled totals, cap comparisons and residual margin.

## R5-RF-1 resolution

The script now distinguishes the 4,096-scalar path bound from UTF-8 name bytes. For s separators with at most 256 segments, the names contain at most min(4096−s, 255(s+1)) scalars, each costing at most four UTF-8 bytes. Independent enumeration gives **16,320 bytes**, attained with either 15 or 16 separators. The scratch's 16 segments of 255 four-byte scalars use 15 separators and 4,095 total scalars, validly attaining that maximum. The script's tie selection reports 16 separators; this is the same maximum, not a discrepancy.

The fixed directory-open, device-status and marker-lookup costs remain priced at 256 segments independently of that name-byte maximum. Combining their separate maxima is conservative. The prior review's 256-segment counterexample is covered: its names total 15,364 bytes. No admission limit or path grammar is narrowed.

The archived scratch log agrees with the inspected source and price owner:

- Counterexample: 256 opens cost 52,484 bytes = 256 × 145 + 15,364 name bytes.
- Maximum-name spelling: 16 opens cost 18,640 bytes = 16 × 145 + 16,320 name bytes.
- Both pass LogicalPath; increasing the final maximal segment to 256 scalars refuses.

This scratch checks LogicalPath and the native price function; it performs no directory reach or filesystem admission. C1b-1 still owes its model/native reach controls in its implementation lane. The plan does not turn this design check into product acceptance.

## Unit and ownership audit

The remaining lengths retain their correct units. Fixed ASCII names use byte-equal literal lengths. H is HEAD's byte length and conservatively covers its ref target's directory/leaf name bytes. File read/parse lengths and retained target/commit values are bytes. The record uses canonical escaped payload bytes, including six-byte control escapes and raw UTF-8 otherwise; its maximum remains 1,573,798 bytes. C1c-0's retention already charges 64 × (4 × 4096 + 128) = 1,056,768 bytes. R9's row accounting explicitly uses UTF-8 path bytes, with four bytes per scalar, rather than repeating the reach's former mistake.

The reach's allocation requirements are now explicit: split the borrowed AdmittedBoundaries path, build no MemberPath or segment-vector copies, and retain only the current directory rather than a vector of opened directories. The existing charged opens price their native-name storage and descriptors. This is a coherent implementation requirement; reproducing item 6b's path/device/marker semantics does not require reproducing its owned container representation.

## Updated derivation

Relative to r5, the corrected reach adds **64 × (16320−4096) = 782,336 bytes**. Of the shared derivation definitions, only repository changes; record sizing, reader pricing, total composition and search logic remain intact. Each of the four published term/total vectors differs from r5 by exactly that byte increment, with unchanged object/edge coordinates.

At **D*=226** and **H*=1,048,575**:

- VCS term: **173,770 objects; 2,165,048 edges; 1,645,984,870 bytes**.
- Cumulative total: **950,510; 8,383,512; 4,185,914,024**.
- Doubled total: **1,901,020; 16,767,024; 8,371,828,048**, within 2^21, 2^24 and 2^33.
- Residual cap-minus-total margin: **1,146,642; 8,393,704; 4,404,020,568**.

One directory more gives doubled edges **16,783,794**, exceeding 2^24. One HEAD byte more triggers buffer growth and doubled bytes **8,644,458,198**, exceeding 2^33. The uniform-INDEX_CAP-HEAD output also reproduces and fails the byte 2x inequality. The tighter name bound is 64 bytes below the prior review's conservative 16,384-byte allowance per member, hence term/total figures are **4,096 bytes lower** across 64 members and residual margin is that much higher. No cap or law gate changes.

## Long-component rule and controls

The revised error distinction matches the inspected mechanisms. Directory component validation returns InvalidInput before openat when a name exceeds 1,023 bytes; kernel name-length rejection arrives as ENAMETOOLONG. After the closed ref grammar has excluded other invalid-component spellings, either maps to ref-name, preserving member-vcs-unsupported:ref-name for members. These cases must precede is_link_or_not_directory, which otherwise includes InvalidInput in its broad link/non-directory predicate. No C1b-specific length constant is introduced.

For single Git-file leaf opens, the validated path grammar excludes the invalid-relative-path cases. open_regular's non-regular result is InvalidInput and appropriately maps to head-not-file, loose-ref-not-file or packed-refs-not-file, following X2's existing config/index vocabulary. A kernel-rejected overlong ref leaf remains ref-name. O_NONBLOCK plus the regular-file check supports the planned FIFO-as-HEAD refusal without treating it as an absent/unborn HEAD.

The added implementation controls cover both multibyte reach spellings and model/native charge equality, the 300-byte kernel rejection and 1,100-byte platform rejection, member projection, and FIFO head-not-file. These complement the existing exact-cap, one-over, remaining-budget, custody and mutation controls; they were not run during this review.

## No regression and remaining gates

R5's sound canonical encoding/ownership correction remains unchanged. Proof lending, same-root joining, per-read no-follow custody/evidence recheck, innermost selection, ref grammar, one symbolic level, loose-ref precedence, dirty meaning, schema preservation, typed J2 origins and combined census-batch protocol remain intact.

Q6/Q7's qualifications remain explicit: D*/H* are evidence-envelope coordinates, not runtime thresholds; HEAD has a 4 MiB refusal bound, distinct from guaranteed 2x fit; aggregate non-row work shares r9's conditional margin; exhaustion may precede classification and yields no partial observation or unborn-head substitution. C1b-1 still owns its complete implemented model, regenerated vectors and cap derivation before acceptance. C1b-2 owns exact sealing and charge-site equality. The corrected design evidence does not satisfy those future gates by itself.

Only read-only inspection, hashing, JSON parsing, Git queries and independent arithmetic were performed. No repository, worktree or control file was edited; no Cargo, rustc, build, lane, evidence script, scratch program, network, private fixture, installation, signing key, held tree or T2 store/cache was accessed or run. No other pane or delegation was used. Only REVIEW.md and review.json were written in the requested directory.
