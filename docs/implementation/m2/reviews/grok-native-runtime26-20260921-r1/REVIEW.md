# Native runtime selection26 — design-unit review

**Verdict: `NEEDS-CHANGES`**

Bounded **development source integration** of frozen374 onto selected inventory56, runtime25, and registry-owner-selection-v1. Not release, not M2 completion, not current authority, not writers, not five-member binding, not S9.3, not native registry/root/marker admission, not directory-birth375, not product installation. Root assent is **not** manufactured. Live product was **not** written (`HEAD` `c57b816`; identity `lib.rs` still 1739 B `f08e459f…`; codec files absent).

**subjectManifestSha256** `05a44e60ca90e04752dd5e6237b230720ec3ff253ec77bccd39e99b6ce39bec7`  
`docs/implementation/m2/native-runtime-selection-v26-subject.json` **7794** B, **36** members, unique paths, **0** pin mismatches. `passageOverrides`: [].

The composition (map, archive, stage helper, 373-r1 invalidation, independent-vs-author checks) independently restages. Activation still fails `contract_successor` because three formal pin lists are not lexicographically sorted.

---

## requiredFindings

1. `verify_design.py` `pin_rows` (`tools/verify_design.py` 146–152), used by `contract_successor` on the subject `files`, successor `candidates`, and successor `parents`, requires `paths == sorted(set(paths))`. All three lists are unique and **unsorted**. Runtime25’s subject/candidates/parents were sorted. Binding this unit will raise `contract subject paths must be sorted and unique` (then the same for candidates and parents).
   - Subject/candidates inversion: `…/project-registry-codec-checkpoint-373/subject.tar.xz` is listed before `…/project-registry-codec-checkpoint-373-r2/README.md`. Lexicographic order puts `checkpoint-373-r2` first (`-` < `/`).
   - Parents inversion: `repository-file-inventory.v56.json` is listed before `project-registry-owner-selection-v1/successor.json`. Lexicographic order is owner-selection, then inventory.v56, with runtime25 successor already first.
   - Fix is sort-only on those three JSON arrays. Member bytes/pins otherwise stay. The subject SHA will change. Do not treat this as a codec, map, or staging defect.

---

## What independently checked out (not acceptance)

Three **selected** parents: runtime25 successor `1d51c00c…deab` / 8692 B; inventory56 `8935bf9d…786c` / 277494 B; registry-owner-selection-v1 successor `0909f44a…828f4` / 11178 B. Live lock: **32** inventory successors / **46** contract successors. `stage.py` **5719 B** `3a71d80a…b1c4` is byte-identical to selected25.

Map schemaVersion **2**: **3** mapped writes (`lib.rs` replacement + two identity additions) + **581** unchanged non-lock. Archive `product/design-lock.json` is **excluded** from both lists so live selected inventory56 lock is preserved. Source archive **615** members / 6909112 B `46aeaeb6…bcbe`. `baseProductHead` `c57b816`.

Independent restage to `grok-out/staged-product`: verified **615** members **before** creating output; mapped 3; unchanged non-lock 581; non-lock source 584; staged lock byte-equal live; live product unchanged; `runtimeAcceptance: false`. Staged identity files match frozen373/374 (`lib.rs` `0158775c…`, codec `f3bb0fb6…`, tests `68df88f6…`). `verify_design.py` on the staged tree against the **current** selected lock: **passed** (32 inventory / 46 contract / generation 40 / admission 48). That is **not** this unit’s bind.

README correctly separates author 52 identity + workspace-build from independent identity 52; inspects provider 28/19 without claiming a rerun; refuses a 764 native aggregate. Frozen 373 r1 nine-kill is explicitly invalid FileNotFound (`ROOT-CORRECTION.md` / `author-fault-correction.md` `c06e8af0…`, 373 ADDENDUM `68286ecf…`, root-assessment). Independent 374 REVIEW `4b679fc3…` / findings `d95f77f4…` are in this subject.

Directory-birth375, S9.3, full binding, and native registry admission remain **out of scope**. Persisted `deviceId` across reboot/remount is **not** this unit and is left for the next task.

---

## Scope / limits

No commits, push, live edits, or native suites. A sort-only successor of the three pin lists is required before `ACCEPT-DESIGN-UNIT` can be considered. This record does not install source.
