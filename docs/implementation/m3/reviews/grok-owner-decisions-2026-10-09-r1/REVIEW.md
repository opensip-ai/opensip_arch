# Owner decisions 2026-10-09 r1

Verdict: ACCEPT.

This accepts the exact archival record of three explicit owner instructions dated 2026-10-09. It is an architecture-only publication record. It is not a new design acceptance, a product acceptance, or a revision of any accepted law, review, schema, historical status snapshot, or design lock.

## Subject

`subject.json` is 2989 bytes, SHA-256 `edcc0a1164768f5c8dfdf73c26150f5178807f8c58c0e73650a7accd0abf7229`. It names four sorted, unique archive members. Each member's bytes and SHA-256 match the staged file, and each file ends with one trailing newline.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `D13-OWNER-DECISION-2026-10-09.json` | 1235 | `92b30760d56005052874d879beffeae0e5d5c8b17a320e0f5f5c956f37ed4edb` |
| `D3-OWNER-DECISION-2026-10-09.json` | 1466 | `723d198bd4ef51c85c07e2f2f84a14642cd2993904706a06b7fe0b6f2c5e966d` |
| `O7-OWNER-DECISION-2026-10-09.json` | 1676 | `625caf46fcbe4a4292d85e42f91f186223a7e68fc3b091ac8d7419b853e9b255` |
| `README.md` | 2406 | `ce01054c4858cf10dfff14afadd1ec9a9b0f7207b95848997915ea4754e5d4fa` |

The nine `authorityPins` are the union of the three records' authority lists, in the subject's order, with no extras and no duplicates. Every pin matches the blob at architecture `5ec79d46c6dd3f69924f086104e4b9c953a90a32`. `docs/implementation/m3/owner-decisions/` is absent at that commit. The architecture worktree's only porcelain entry is the unrelated untracked `docs/implementation/m3/syntax-e/e2s/`, which is outside this record.

Product `bf4be44ffbaf02e8518c276882524831ee8e12c4` is clean and contains no owner-decision path. `design-lock.json` at that commit is 614747 bytes, SHA-256 `9c73578855ed10eb52dcd507a4498761045efa60c7a5899afb1726d35f43973f`. It has 139 inventory successors. The last candidate is `docs/implementation/m2/repository-file-inventory.v179.json`, 649241 bytes, SHA-256 `8363e0d57ef5350d4d50880c63887644c287a059add2e1c5ac3af6f2f92b172a`. Contract successors remain 154. Inventory stays 179. Product code stays unchanged.

`README.md` has three same-directory links, and each target is present. It has no angle-bracket links.

## Owner instructions

The request supplies the owner's words. Each record transcribes one sentence exactly:

- O7: `adopt the existing O7 proposal`
- D3: `yes, i approve the exact reviewed T2 selection`
- D13: `i approve the the exact reviewed Q0 r13 exploratory envelope`

The repeated "the" in the D13 sentence is the owner's spelling, and the staged string keeps it. `ownerAssentInferred` is false. These records quote those instructions. Review acceptance of the underlying proposals is a separate, already closed fact.

## O7, owner choice L-G9

Status is `ADOPTED-EXISTING-PROPOSAL`. `sectionFSelectedAsRecommended` and `ownerDecisionGateLG9Met` are true. The selected bullets follow the existing recommendation, which is still pending in the pinned plan and is the section F placeholder in the pinned supervisor D proposal.

Pinned `M3-PLAN-r10.md` (226011 bytes, `ec8c38f8c6ac8d522989ea6226363817a1b77c5b37560e72e2520088601bb964`) lines 750–757 recommend: analysis never executes repository code by default; providers run under Landlock, seccomp, and no network on Linux and AL2023, and under a macOS Seatbelt profile that denies network access and any write outside the provider's scratch; unavailable confinement is disclosed and the documentation requires containers for untrusted pull requests; repository-code execution requires `RepoExecutionGrantV2` and runs only inside confinement or a container. Lines 791–794 keep repository-code execution out of M3. Line 799 states that nothing is enforced or measured yet.

Pinned `supervisor-d/PROPOSAL-r5.md` (209266 bytes, `224b9228e9d7c0bc11c848c88cd2ed7fa7da8734208c45d70fbb678a97afec6d`) section F, lines 920–926, repeats those four points and is binding only once O7 is decided as recommended. F-0's "As recommended" row makes section F binding, with D1b still to build F-1 through F-5 and D5 still to add F-7. Alternatives A, B, and C are not selected. F-4 says unavailable means disclose and continue, and an available confinement whose apply step fails means refuse the launch (`confinement-refused`). F-6 says no repository code executes at M3, and future repository code stays behind `RepoExecutionGrantV2` and the existing M5-EX conditions. The record's "ordinary analysis fallback" is that disclose-and-continue rule. Its "Providers/tools" wording follows F-4's launch rule for both, using the confinement mechanisms already written there. It adds no profile, carrier, or launch class.

The same record keeps CF-1, CF-2, D1b, platform enforcement, and provider launch false, and it keeps D3 and D13 sign-off, effective L, qualification, plan completion, and push false. The pinned plan still says O7 is pending and that no provider launches until O7 is decided and D1b's primitive exists. This file records the owner choice. It leaves that plan text in place.

## D3, sign-off L-G4

Status is `SIGNED-OFF`. `ownerDecisionGateLG4Met` is true. The instruction approves the exact reviewed T2 selection. The recorded counts are 49 repositories, 5 multi-repository workspaces, 33 independence families, and 10 held-out families.

Those counts are the pinned T2b manifest, `t2-corpus-manifest.draft.json` (322483 bytes, `c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578`). It has 49 repository entries, 5 workspace entries, and 33 families. Ten families have `heldOut` true, the held-out set has 10 entries, and 10 repositories are held out. Every repository is in exactly one family. No held-out family contains a dev repository, and no dev family contains a held-out repository. All five workspaces are dev. The pinned corpus `README.md` (26701 bytes, `3d355e72466e228f2021c0b6386b2d04576f44cf11637e9880edfa859ae5b2ac`) states the same 49, 5, 33, and 10 figures. Plan row B3 says to approve T2a and T2b as reviewed at 49 repositories and 33 families, and plan row B2 records the 10 held-out families.

`grok2-corpus-t2b-r1/review.json` (1904 bytes, `7ac14f110bcd58f448624abe978584f45027ae4078ae9a073bf5e7c835e7f048`) is ACCEPT with an empty required-finding list, and its manifest and README subjects are these pins. `grok2-corpus-t2a-r1/review.json` (1545 bytes, `4fe93f4408ef353921f363fdf67485d0ae2a66d30256a998df754420392ad666`) is the earlier ACCEPT. Its subject hashes differ from these pins. It stays an authority for that earlier acceptance. The selection object is the T2b bytes.

The manifest still says the T2 selection is proposed and not signed off. This record is the later sign-off and does not edit that sentence. Python entries stay pinned and not analyzed. npm and Python workspace rendering stay with the discovery successor named in the corpus README. Held-out source opening, a precision-threshold change, a ground-truth freeze, Python analysis support, measurement, the D13 sign-off, effective L, qualification, plan completion, and push stay false on this record.

## D13, sign-off L-G5

Status is `SIGNED-OFF`. `ownerDecisionGateLG5Met` is true. The selected envelope is the Q0 r13 exploratory envelope. Standing is `exploratory-never-promoted`. `qualificationEvidence` is false.

Pinned `DESIGN-r13.md` (151216 bytes, `37438317e7233bbb8bdc64dc9c8fe838f590c7e06fba3e54a0966002c1436be4`) line 1148 requires `standing` const `exploratory-never-promoted` and `qualificationEvidence` const `false`. The pinned schema (60241 bytes, `71f682d125c956eaec7a0f015fc8a0203f78b15f4538935f7beab45a398a2eb6`) has those two consts. `codex2-harness-q0-r13/review.json` (4947 bytes, `7fd3f094e6522789daea3c5931a144d5ad08e69a31ff3bb47674497aa4e9e8ec`) is ACCEPT with an empty required-finding list. Its design subject hash and schema hash are these two pins. Its scope text limits that acceptance to the exact r13 design subjects and excludes implementation and qualification evidence.

At the same architecture commit, live `harness/DESIGN.md` is 151414 bytes, SHA-256 `1f1083993dce42b5fbc620c0b0e9a2ee13c0be6690dd23a668b041146125ac47`. The sign-off pins the reviewed r13 snapshot, not that later file. Live `exploratory-quality-envelope.schema.v1.json` is byte-identical to the pinned r13 schema.

The design keeps Q6 qualification on the Linux D12 runner, leaves macOS rows incomplete until a whole-tree settlement source and a group-peak source exist, and keeps root-reaped elapsed informational. D12 runner selection is a separate owner item. Whether cgroup `memory.peak` satisfies the charged-memory / peak-RSS qualification question is also left open. This record keeps macOS settlement, D12 selection, charged-memory/RSS equivalence, measurement, effective L, qualification, plan completion, and push false. Plan row L-G5 still says the Q0 r13 mechanisms were accepted and the owner sign-off was open. This file is that sign-off.

## Boundaries that remain

The three records together close only the owner-choice portion of L-G9 and the sign-off portions of L-G4 and L-G5. The pinned plan, lines 467–472 and 711–716, still defines day 0 as M3-L in effect only when every gate item is met and every delta round is accepted. L-G1, S-M, remains open, and its report still waits on the D13 mechanisms being carried into measurement. Recording these sentences leaves CF-1, CF-2, D1b, platform enforcement, provider launch, held-out opening, measurement, the D12 runner, charged-memory/RSS equivalence, macOS settlement, effective L, product qualification, and plan completion false. Historical status-board r26 stays closed at its 2026-10-08 cut-off. Nothing is pushed.

`verify_design.py` was not run. The lead integrates this architecture record only after this exact ACCEPT, substantive assent, and the current `verify_design`.
