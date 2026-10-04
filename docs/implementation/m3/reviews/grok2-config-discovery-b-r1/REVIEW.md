# M3-B r1 — REQUIRED-FINDINGS

Subject: `docs/implementation/m3/config-discovery-b/PROPOSAL.md`, 85905 bytes, sha256 `da014f54d1beff4a7187fc716205319ba5facf41a9caddec5c29e0464b618e2f`. Read-only. No cargo and no tests. The cited product files match the pins at `30c5db1` and at `3e64266`. `~/Library/Application Support/OpenSIP` was absent.

## Decisions

**R1.** A recognized native declaration at W is enough intent to admit the repository it names, and D15 does not need a new consent flag. The declaration is a literal relative path in a file W's owner controls (`--workspace-root`, `discovery.workspaceRoots`, `.cargo/config.toml` `[patch]` path-only, or a literal `package.json` `workspaces` entry). Globs, undeclared nested repositories, and "every checkout under W" stay out. Admission grants no execution, write, custody waiver, or second authority root, and B3-b cannot cross SL:163-168 until B-S1 is accepted. The minimal further consent is the one RF-1 states: once a `discovery.workspaceRoots` array is supplied, that array is the membership, and the readers stop adding members.

**R2.** The order amendment is sound, and "nothing to clean up" still holds, apart from the stands-clause in RF-2. `ObservationSession::begin` and `DurableWriteGate::begin` allocate an in-memory ledger and a process flag. The gate then takes a nonblocking lock on the existing `lifecycle.fence` and runs directory barriers. Neither begin writes a registry row, a RESERVED document, a lease, or a journal. Item 10 places pack admission after selection and the carrier reads and before X2's registry capture, registration, lease, and every effect. Selection and the carrier reads are reads. Dropping the session releases the fence. X12:132's residue (no evaluation, no `policyOutcome`, no facts, Coverage, or universe) is unchanged. The control in item 10 matches that order.

**R3.** A downward walk after the fence, on one discovery ledger, is compatible with X2 item 9 and with the no-retry rule. Item 9 binds the admission operation to the session or gate ledger at the owner's caps. X2:280 already gives unit discovery to M3, and item 12 runs it after the handoff (X2:231-248), once, on a ledger that is not recreated after failure (`work_ledger.rs:1-8`). The raised caps are a new constructor; `with_limits` still cannot raise (`work_ledger.rs:203-213`), and the session ledger stays at 65536 / 131072 / 256 MiB. The provisional caps are adequate: the census must show a 2× margin or the caps return to this law, and a member's index and config stay inside X2:272's 4 MiB and 64 KiB ceilings (64 members, about 260 MiB, under 2^30).

**R4.** The empty semantic fold is consistent with AQ:104-110, AQ:155-158, and AQ:330-332. Those sentences say discovery may populate defaults before the resolver runs, and that a field is present only when default, discovery, or an explicit layer selected it. Absent `entryPoints` and `workspaceRoots` keep the meaning "automatic". Writing discovered units or entry points into `discovery.*` would make that false and would bind the same input in `resolvedConfigDigest` and again in `membershipDigest`. An empty fold is a fold of no semantic observations. Membership, recognition, and scope stay on their own records.

**R5.** CI equals not-interactive, decided from terminal state, is a lawful lead decision. AQ:107-108 and HFC:196-197 require that CI not probe the local carrier; they do not define the test. Item 3's test (stdin and stderr both terminals; no environment variable; no `--ci`) meets that requirement and matches CH13:60. A full-pty automation is interactive and does read `local.json`. F11 already records that the contracts leave the test unspecified.

**R6.** The waiver reach is correct. SLM:832-833 refuses `trustProjectOwner` without an explicit `--project`. SLM:669-680 applies the waiver to directories from the explicit root to a unit. SLM:636 applies it to that root's `opensip.json` only in explicit mode. SLM:665 judges marker files with the waiver off. Item 23 applies the directory waiver to member directories, keeps it off marker files and member Git evidence, and does not extend it to `local.json`. `local.json` is a carrier the reference does not have; leaving it unwaved is a narrowing, and W's `opensip.json` stays the waived config file.

**R7.** X2 r9 is safe on the eight points item 21 argues, and S3–S6 name the frozen texts that otherwise block D15: SL:163-168 and NE U-8 (S3), IE `vcs-observation` (S4), NE:1750 and the `--locked` carrier (S5, NE:1786), and NE:1413-1418 (S6). Item 6b reuses the closed layout (`git_tracking.rs:295-317`, `:429`, `:697-713`, `:807`) and adds no Git object beyond `.git`, `config`, and `index`. F2–F4 correctly leave U-6, config-level `patch`, and cross-member resolution outside this law. S3 is not complete until item 20 states RF-1, because the Config2-join text S3 is supposed to carry still forbids widening a supplied root list.

Citations checked and matched include X2:29, :68, :74, :144-145, :209, :231-248, :250-280; X12:125-132; I1:381-388; `git_tracking.rs:5-6`, `:321-346`, `:429`, `:587`, `:697-713`, `:721`, `:743-776`, `:807`; `project_admission.rs:240-269`, `:303-384`; `project_chain.rs:422-438`; `work_ledger.rs:1-8`, `:12-14`, `:203-213`; AQ:104-110, :112-118, :155-173, :175-181, :330-332; SL:111-112, :127-130, :146-185, :246-262; SLM:632-680, :771-785, :832-833; NE:869-870, :907-921, :1413-1418, :1743-1752, :1786; T2M:7752-7764, :7865, :8952, :9097, :10263; T2R:187-221, :303, :306; T2F:41-62, :112-125; HFC:159-168, :196-197; OPP:365-367; M3P:162, :204; AQP:556. The T2 workspace ids, member counts, and link counts in item 19 match the manifest and README.

## Required findings

### RF-1 — a supplied `workspaceRoots` array must suppress reader membership

Item 20, the sentence "An explicit source suppresses the readers for membership".

That sentence uses "explicit" for the CLI tier only. A `discovery.workspaceRoots` array from the project or local layer therefore still lets `cargo-config-patch@1` and `npm-workspaces-members@1` add members. NE:919-921 restricts discovery, for both Config2 `workspaceRoots` and `--workspace-root`, to exactly those roots and forbids widening them into a scan. SLM:774-785 implements the same precedence as `if` / `elif` / `else`: a config array does not fall through to automatic discovery. AQ:115 selects automatic discovery only when the array is omitted. S3 names the Config2 join as text it will carry (item 25), and items 19, 20, 22, and 24 are the text it carries, so copying item 20 as written would drop the exact-roots rule for the config tier.

**Fix.** State that a present admitted `discovery.workspaceRoots` array, from the config layer or from `--workspace-root`, suppresses reader membership. Readers may still record links whose directories lie inside members that array already admitted. Readers declare members only when the array is absent. Keep "exactly those roots, never widened" in the Config2-join text S3 edits.

### RF-2 — I1:388 freezes the order item 10 amends

Item 10, "Everything else in X12 r3, and in I1's M3 amendments (I1:381-388), stands."

I1:381-388 is the whole amendment block. I1:383-386 changes three row counts. I1:388 then says everything else in X12 r3 stands, including the order: pack admission before any fence (X12:125-130). Item 10 changes that order and, in the same sentence, says I1:381-388 stands. I1-c and S2 would then each be required to preserve the order the other changes.

**Fix.** Say that I1:383-386 stands, and that I1:388's statement that the X12 order stands is withdrawn by S2. Do not cite I1:381-388 as standing in full.

## Non-blocking

**NBO-1.** Item 12's census counts directories and entries outside pruned segments. The 2^30 byte cap is not part of that count. The separate bound in item 19 (64 members, each at most 4 MiB of index and 64 KiB of config) is what puts bytes under the cap. The return-to-law rule covers a census miss. No change is required for acceptance.

**NBO-2.** S3's content cell names a "U-9 note", and no decision states the note. U-9 (NE:879-905) still keys off no explicit roots and no surviving `rust` or `tsjs` unit; a member is not a second fallback site. Either drop the phrase or write that one sentence into item 22.
