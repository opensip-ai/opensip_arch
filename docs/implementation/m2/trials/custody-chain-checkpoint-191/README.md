# Retained directory-chain observations checkpoint191

Unselected private successor to product189. Actual Claude review required; no custody grant, host admission, continuous exclusion or cumulative approval.

Platform RetainedDirectoryPath can now observe every retained descriptor, root first and leaf last, using its existing metadata/ACL observer. It exports no raw descriptor and accepts no observation callback. A failed observation returns no partial vector; Linux ACL observation remains explicitly UnsupportedPlatform. These are sequential samples, not a coherent permission snapshot or filesystem/mount qualification.

Security reuses its existing observation-to-predicate conversion to inspect the whole chain, with complete name rechecks before and after observation. It preserves distinct name-observation, changed-name, descriptor and policy-refusal errors, including the refusing component index. It grants no owner waiver and no sticky-directory exception. Invoking UID/groups, local-filesystem policy, SQLite main/WAL/SHM custody and exclusion through consumption remain host obligations. It does not close124F1/149N4 or prevent ABA or permission changes between/after samples.

Only platform/filesystem/path_binding.rs and security/custody.rs change; all352 source members and37 fixtures remain.43platform and145security tests, strict workspace Clippy r3 pass. Five compiled mutants (skip root, skip ancestors, skip policy, omit precheck, omit postcheck) are killed, with a green baseline. Host120 uses232sources/51archives and passes418workspace tests plus2doctests, metadata/version/help and source unchanged.

The initial author script stopped at a trailing-newline assertion after editing platform; beforeimages and the corrected continuation are preserved. Platform r2 caught a genuine ChangedDuringRead on a shared temporary ancestor modified by parallel tests. Production remains one attempt and returns this error. Test-only helpers retry only ChangedDuringRead, at most256 times with1ms intervals, to obtain a positive stable sample; they do not mask name/policy failures or assert continuous stability. The final r3 receipts use these exact bytes.
