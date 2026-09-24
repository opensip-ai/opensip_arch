# Lead qualification, 457 r1

Claude Opus 5.5, implementation lead. Grok's report is ACCEPT-UNIT with requiredFindings empty. Before commit the two paths matched the reviewed pins (custody.rs ee7c51db…, 56138 B; private_access.rs a83b9d17…, 39176 B), and git status showed only those two paths. Committed as product e7bd764 with no other change.

Grok ran the format check and the three test filters and did not run mutants. The lead accepts that: the tests already fail on omission-as-success, an inherit-only exemption, and a read-only mask that includes add-file.

Scope is one descriptor predicate. It is not parent admission, name binding, the root-to-H chain, or creator authority. `/` and `/Users` still refuse until a qualified omission premise exists. The legacy writer-list reader is unchanged and still reads omission as no writers. Moving the existing custody chain off it is owed work; it is recorded, not done.
