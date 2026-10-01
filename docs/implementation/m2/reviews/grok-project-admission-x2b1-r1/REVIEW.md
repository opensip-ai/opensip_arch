# X2b-1 project admission r1

REQUIRED-FINDINGS. Inventory v88 is REQUIRED-FINDINGS.

Worktree `/Users/sb/code/opensip-ai/opensip-x2b` at `8bfc78a741158e961f727dd44f481549ec09225d`. `product.diff` is 68149 bytes, sha256 `ca85302fdad7134bf1105a6db2c88b463b03077a28e7ecae448f18a6a350fac0`, seven files. Pins match hashes.txt. Real `~/Library/Application Support/OpenSIP` is absent. Law X2 r5 is the accepted text; the live `PROPOSAL.md` is that text plus the acceptance sentence (35822 bytes, sha256 `1ff89472a0ec8b878a0a7878e4941f5f2dbbfd650a07e4a57e680b6dc3e3ddbf`). The operative items are unchanged.

Replay: Rust 1.95.0, `cargo test --locked --offline -p opensip-security --lib -- project_admission`, 15 passed, 635 filtered out. The cargo target was deleted. The workspace suite, clippy, fmt, check_package_edges, and verify_scratch were not replayed.

## Findings

RF-1. `sample_incarnation` debits `VOLUME` (objects 0, edges 3, bytes 2560) and then calls `RetainedDirectory::observe_volume`. That sampler takes a metadata sample, `observe_filesystem`, the volume-UUID attribute, `observe_filesystem` again, and a closing metadata sample. Each filesystem observation has a published cost, `descriptor_filesystem_observation_cost`: objects 1, edges 2, and bytes covering `struct statfs` (2168 on this host) plus the status buffer and the filesystem value. Two of those statfs buffers are 4336 bytes before the outer status reads. Item 9 charges the sample before it runs. Required: debit both filesystem observations at that published cost, plus the two outer status reads and the attribute buffer, before `observe_volume` runs.

RF-2. An ACL-capture `Io` error on `opensip.json` becomes `CONFIG.CUSTODY_REFUSED` subject `custody`. `ProjectAdmissionRefusal::row` maps a `ConfigRefusal::Custody` inner whose chain row is host I/O onto that subject. The same `Io` error on `project-id.v1` becomes `PROJECT.ROOT_CUSTODY_REFUSED` subject `marker-custody`, because `observe_marker` maps every capture `Operation` to `MarkerCustody`. Item 8 assigns I/O to the host I/O row. `ProjectChainRefusal` already maps `DescriptorAclCaptureError::Io` to that row, and a failed open of either name already uses it. Required: keep a private-predicate failure on `marker-custody` and a config custody failure on `CONFIG.CUSTODY_REFUSED`, and map capture `Io` to the host I/O row.

## Inventory

v88 is 325071 bytes, sha256 `658a4dfdb17af2971e27f18a4b510fd2f9f5f9f84e12df3a816749b9d8edbe4a`. Parent v84 is 322464 bytes, sha256 `99b80dc4eb4790b380223c7eb575f9259f6fac69e0f33922ea7df1ab45653c2b`. Successor `docs/implementation/m2/project-admission-inventory-v88/successor.json` is 20169 bytes, sha256 `8e528243ea34975dcace10ae4c949d4ae170f2e413b2c80bf20d438190f0ed7c`. Against v84 the row diff is two added files (`project_admission.rs`, `project_admission_tests.rs`) and no removed or changed rows. v85, v86, and v87 are siblings. Provisional parent v84 is right.

`project_chain.rs`'s description still describes the chain walk. Selection, the registry, and `ProjectRootAdmission` are this unit's and live in `project_admission.rs`. The new configuration-file arm of `judge_project_object` is unstated, and no sentence of that description is false.

`installation_read.rs` still ends with "Nothing walks from the root again." `ReadSession::admit_project_root` opens the launch or the explicit path, and the selected root, from `/` through retained no-follow handles. That sentence is false. Required: the row says this entry walks from the filesystem root.

## Judgment calls

1. The split holds. The admission carries its classification and has no namespace, registration, or tracking effect. Item 6a's untracked observation remains required before either grant. The write path stays with X2c and X2d.

2. H is `Chain::home_spelling`, copied during the session's step 0 walk and charged before the copy. Admission reads that spelling. It does not read the account record again.

3. There is no write-gate entry. `installation_admission.rs` only retains the walked spelling of H.

4. The marker file is judged with `judge_capture` (`assess_private_descendant_capture` for a regular file: invoking uid, mode 0600, one link, zero-rights owner allow). The omission premise is not applied. `.opensip` is judged with `judge_project_object` as a directory, so the premise applies, matching item 1. A custody failure is `PROJECT.ROOT_CUSTODY_REFUSED` with `marker-directory-custody` or `marker-custody`. A symlink, a non-regular object, a short or over-long body, or a bad frame is `MarkerObservation::Malformed`, and `classify` returns `Contradiction`. Those subjects are subject data on the existing root-custody code. Capture `Io` is RF-2.

5. Registry missing, oversized, malformed, and `project-registry.v1` present are `Incomplete`. A metadata mismatch with the session's judgment is `RequiredFilesChanged`. An open or bounded-read error is host I/O. The capture returns no document in those cases. v1 absence is a positive no-follow observation and is repeated on recheck.

6. `ProjectRegistryDocument::decode` runs inside one `work.run` over the captured bytes. The document keeps those exact bytes. Classification runs only after that decode returns.

7. The walk examines the home directory, including `opensip.json` and the VCS markers, and then stops. A selected root that is H, an ancestor of H, or inside `H/Library/Application Support/OpenSIP` fails `placement` before the registry capture. The home index matches the retained component index (`Path` components include the root; the retained index counts children below `/`).

8. `check` is called with owner waiver off. The diff adds no `--trust-project-owner`. An explicit path is opened with `open_project_root` and is not normalized; a symlink, a missing path, or a non-directory is the explicit-path row from `open_refusal`.

9. A device change stops on the parent volume before that directory is custody-checked or examined, and the selected root is the launch. The mount root shares `st_dev` with the launch, so it is examined first. That is S3's mount boundary inclusive of the mount root (`cwd-default`, stop mount; a config on the parent volume stays unexamined). The missing scratch mount is consistent with that code.

10. Ruled with the inventory section above.

## What matches

S3 order on one passing directory is config, then any of `.git`, `.hg`, `.svn`, `.jj`, then home, then the filesystem root. A config custody failure refuses and is not skipped. Launch custody refuses. Ancestor custody selects the launch and does not examine above that ancestor. A VCS marker selects its own directory. An explicit path is examined once and stays the root. The walk allows 256 levels and refuses the 257th. `ProjectRootAdmission` is not `Clone`. Its recheck covers the chain (names, custody, volume, birth), the volume UUID against the stored incarnation, the marker, the registry metadata, and v1 absence. Birth is the X2a sample; the volume UUID is `observe_volume` on that same descriptor, and a zero UUID is refused by the sampler. Eligible, FirstUseCandidate, RecoveryNeeded, OneSided, and Contradiction follow the registry owner's table, including a retired row with the same incarnation as first use. The read session runs this on its ledger, rechecks, and latches a refusal.
