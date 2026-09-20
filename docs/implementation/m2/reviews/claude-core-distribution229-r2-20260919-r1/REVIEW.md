# Independent scoped review — frozen core-distribution-wip-229-r2 (corrections to my G-1…G-7)

Scope: root's corrections to my 229 r1 findings. **No cumulative approval, no readiness claim, no
approval of my own author drafts.** No repo/product/candidate edit, commit or push; output only here.
227 not re-reviewed.

## Verification and reproduction

- Archive `cb75fac1…e508`, 89160 bytes: pin matched; all 54 `subject.json` members matched (path,
  sha256, bytes) from the tar before extraction; re-verified at the end.
- Beforeimages checked against my own earlier extraction: `distribution_model-before-r1-review.py`
  is byte-equal to the r1 model I reviewed. `trust-owner215-before-embedded-head.md` is a48e122c…,
  i.e. the LIVE 215 working "revision15" I pinned during task 230 — it differs from frozen r14
  (d8165f14…) by a title bump and one added section ("Exact current restriction projection (226
  completion)"). That extra section is NOT part of this review and is not approved by it.
- Fresh output-local copy without `distribution-mutants-r2/` and `distribution-guard-variants-r1.json`
  (both runners refuse to overwrite); reference-201 reached through a symlink to my verified
  extraction; the model hash-asserts `canonical.py` and the kernel. **No script edited.**
- Results: 67 cases → **byte-identical** to `distribution-check-r4.json`; 9 source variants +
  baseline → directory **identical**; 20 guard variants → **byte-identical** json.

## Disposition of my r1 findings

| r1 | r2 state | evidence |
|---|---|---|
| **G-1** index-0 anchor × 215 pre-acceptance authority | **closed as owner law; selector correct in its stated premise** | 229 OWNER "G1 cross-owner authority completion" and the 215 successor copy (5 sentences + closing paragraph) make index 0 the authentication anchor only and the FINAL root of the COMPLETE authenticated embedded chain the pre-acceptance authority and replacement floor; no prefix. My probes of `conditional_embedded_head` / `conditional_recovery_authority` (adv229r2 H0–H11): version gap, wrong `previousRootVersion`, backdated issue, repeated root, policy-invalid middle root, 65 roots, bool version, same-version/different-digest head and negative floor all refuse with the right label; single-root chain yields head == anchor; a schema-1 → schema-2 rotation inside the chain yields a schema-2 head with the `.root.2` domain |
| **G-2** unexercised guards | **closed except three (below)** | default fixture is two platforms / two roots; my all-reasons guard-off survey: 35 of 43 reasons killed, 4 end in an unrelated exception (each has a positive label hit), 4 survive — see R-1 |
| **G-3** symlink targets | **closed** | resolution is relative to the link's parent, through declared links, cycle- and length-bounded (S1, S4–S9); see R-2 for one inconsistency |
| **G-4** `:` | **closed** | only a drive-letter prefix refuses; `data/a:b` and `ab:c` admit (G4a–d) |
| **G-5** TCB positive | **closed in claimed scope** | a non-empty template-conformant profile admits (`nonempty-profile-template-shape-NOT-qualification`); the label itself disclaims qualification |
| **G-6** A.3 by digest | **closed** | restated by delivery route/envelope kind with `storedSha256 == manifestDigest` |
| **G-7** first person | **closed** | both sentences re-attributed; no first-person remains in OWNER.md |

## Remaining findings

### R-1 (low–medium, test adequacy) — the two NEW G-1 chain guards have no owner case

Disabling `embedded-chain-gap` or `embedded-chain-backdated` leaves all 67 cases, the 9 source
variants' baseline and the 20 guard variants green (`guard-survey229r2.json`). README lists
"contiguousversions/nondecreasingissue" among what the new selector checks, and they are the part of
G-1 that makes "in order" mean something; yet the corpus has only prefix, reorder and the two
authority cases. My H1–H3/H5 show the guards work. **Action:** add the three negatives (gap, wrong
`previousRootVersion`, backdated) and put both reasons in the guard-variant list. Also surviving:
`symlink-resolution-bound` (my S7 `a → a/x` reaches it) and `retained-budget` (a 256 MiB limit no
fixture can reach; acceptable to leave, better to parameterise the limit as 227 does).

### R-2 (low) — directory rows are optional for parents but mandatory for symlink targets

`tree_check` treats an undeclared parent as an implied directory (`kinds.get(parent, 'dir')`), and
the owner fixture declares NO `dir` rows at all. But a symlink to such an implied directory refuses
`symlink-target-missing` (S2), and admits once the row is declared (S3). DR-103 calls TreeCommitment
a "full-tree path/type/mode … commitment", which argues for REQUIRING dir rows everywhere; the
current mix means the same tree is lawful or not depending on whether something links to a
directory. **Action:** pick one rule — require every parent directory to be a declared `dir` row
(and add them to the fixture), or let resolution end at an implied directory. I would choose the
former: modes of directories are part of what install verifies.

### R-3 (low, prose/scope) — what "complete" can and cannot mean in the selector

`conditional_embedded_head` takes the chain from `manifest.members.rootChain`; "no prefix fallback"
therefore means "the caller may not pass fewer roots than the manifest lists", and the case is named
accordingly. It cannot detect a manifest that itself lists a shorter chain than the vendor intended
— correctly so, since the signed/tree-bound manifest DEFINES the embedded chain. One sentence in
OWNER G1 would prevent a reader from taking "complete" as a stronger property. Likewise the
selector does not join later roots' envelopes or subjects (the index-0 anchor check does for root 0);
the docstring and README say upstream authentication is assumed, so this is a stated boundary, noted
only so the eventual chain authenticator is not assumed to exist.

### R-4 (note) — the 215 copy carries an unreviewed delta

As above: the 215 before/successor pair is based on working revision15, not frozen r14. My review
covers the five changed sentences and the closing paragraph only. When 215 is next frozen, the
"restriction projection (226 completion)" section needs its own review.

## Boundaries not treated as findings

Synthetic signatures; no old/new quorum, revocation or time evaluation of the chain; no native
path/custody/alias admission; no install/launch/first-channel evidence; envelope subject index and
ambiguity policy; payload2 / nine-kind envelope integration; primary schema/reference/runtime
selection. All stated in README/OWNER.

## Limitations

Probes call the owner's unmodified functions with its fixture builder; verdicts are the toy
model's. The guard survey disables a reason LABEL, so conditions sharing one label
(`logical-path`, `embedded-replacement-floor`, `protocol-membership-order`) are disabled together and
a kill there does not show every sub-condition is tested. I read the OWNER and 215 diffs and the new
model/test code in full, the unchanged r1 text was not re-read. No harness failure occurred;
ERROR-not-a-kill rows are preserved in the survey output.

## Pins

`distribution_model.py` d15bb9e413fd6f0def799ccf39a9e5aa4f837bebefb956191b7283a36d8c0e8e ·
`check_distribution.py` 184b815360fd1d84d0364a9e1660f2f39834c1226ac42ac447386a7a3413c340 ·
`core-distribution.v1.json` 960ecdfd14495e57297432644d47b53376a2223c053b7e5485e505b63db1f91f ·
`OWNER.md` 76bab0acd0a3b57b16e28fe3052c06f02f41bbb01709bca7c7d80bc9224d9384 ·
`ROOT-DISPOSITION.md` 349f86bd3c0e0ea1321a6f3dc9b1de7985a1d0149851111858651431b7d6945a (unchanged from r1) ·
215 before a48e122cc60337a9290a3d3210c9a9d8eb64a31194334d56abc3b141cd072ae9 · 215 successor
780a6dd5e3d3c43c14d325504085bde99c4254d87fba3ac7872150da701a0d60 · `canonical.py` d47f25db… ·
kernel df45c9c5…
