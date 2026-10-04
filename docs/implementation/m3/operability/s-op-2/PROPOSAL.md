# The safe event vocabulary and sink law — contract-successor proposal S-OP-2 r2

**DRAFT r2, not accepted.** This is a contract-successor proposal. The verdict it seeks is ACCEPT-DESIGN-UNIT.

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run.

**Review history.** r1 (`PROPOSAL-r1.md`, sha256 `e3b117f0…`, 60,424 bytes) was reviewed by Codex (`/tmp/opensip-implementation/reviews/codex-s-op-2-r1/`): REQUIRED-FINDINGS, with seven required findings (SOP2-R1-01 to -07) and six non-blocking (SOP2-R1-NB-01 to -06). r2 answers all thirteen. Where Codex offered a choice, r2 takes the lead's stated preference. The "r2 changes" table maps each finding to its change.

**What it is.** S-OP-2 is the successor that the accepted operability plan names. Its §9 row reads "Registry, `SafeField` set, privacy classes, per-sink allowlists, §3.3 bounds and loss marker", owned by the "DR-125 owners: Component architecture + CLI/operability/security" (OPP:408; REG:314). It is written under:
- OPP §3.1–§3.6, §5.3, §6, §7 and §10 (r3, accepted);
- the draft law M3-L, items 12–14, which name what it needs from S-OP-2 (M3L:345-425);
- the accepted contracts listed under "Joins" (items 18–22).

## r2 changes and review responses

| Finding | Items | Change |
|---|---|---|
| SOP2-R1-01 code-table provenance | 3, 5 (K1, K3), 8; C-1, C-2 | **Code tables are admitted only through a sealed host registration.** `CodeEnum` is sealed. Its only implementations are emitted by `code_tables!` inside the registry module, which alone can mint the `TableRegistration<E>` token each implementation must carry. Every table is listed in the registry with its provenance, a release constant of one of three classes: registry literal, generated contract enum, or closed protocol enum. Members are taken only as `literal` tokens and checked against a grammar. `include_str!`, `include_bytes!`, `env!`, `option_env!`, `concat!`, build-script output and generic implementations are refused. Message templates follow the same rule. C-1 and C-2 add the `include_str!` table, a generic adapter and an unregistered implementation. |
| SOP2-R1-02 bundle re-admission | 2, 13a (new); C-4, C-12 | **Closed re-admission of persisted records** before any re-emission (the bundle, and later the doctor query):<br>- a bounded line read;<br>- a validated header;<br>- the event's descriptor looked up;<br>- each field re-admitted by its kind's read-back predicate and re-encoded from the admitted value;<br>- unknown fields and invalid values dropped;<br>- a record without a valid header or a descriptor dropped;<br>- a bounded P0 count disclosure.<br>Retired events keep their **complete descriptors**, or their records are dropped. Code-table members are never removed, only retired. Raw serialized values and class claims are never trusted. |
| SOP2-R1-03 gate linearization | 17; C-7 | **The atomic load is the admission point.** Every syscall needs its own load: first writes, short-write continuations and the marker. Nothing is admitted after a load sees `closed`. A write unit admitted before closure may be issued or complete after it. That residual is stated (at most one unit of ≤ 64 KiB per sink writer) and referred to S-OP-7, with the X3D owner's assent. C-7 adds a pause hook between the gate load and the syscall. |
| SOP2-R1-04 drain independent of I/O | 16, 17; C-7 | **The deadline is on the termination path's timed wait for optional logging**, independent of any sink syscall:<br>- producer admission is cut off first;<br>- on expiry the gates close and the final snapshot is taken;<br>- a blocked writer is abandoned to process exit, and the command completes.<br>The in-flight I/O limitation is stated. The marker is best-effort, with four observable outcomes (`written`, `failed`, `suppressed`, `skipped`). No logging sink holds a lock the termination path takes. C-7's "exactly one marker" is replaced. |
| SOP2-R1-05 full-encoding proof | 5, 8, 14; C-7 | **The static bound covers the whole line in both forms:**<br>- field keys are at most 32 B by grammar;<br>- the header reserve is 768 B, proved: maximal JSON header 678 B, maximal human header with message 756 B;<br>- per-field overhead is at most 36 B;<br>- each kind's encoded value bound includes quotes, wrappers, escaping and numeric widths.<br>K3 is corrected to 66 B, K10 to 64 B, and K8 uses a compact fixed-index array (≤ 24 B per variant). `registry!` asserts 768 + Σ(36 + V) ≤ 4,096. C-7 adds long-key, maximal-escape, saturated-counter and full-header cases. |
| SOP2-R1-06 one escaping rule | 1, 13, 13b (new); C-5 | **One rule E for both encodings and every string value:** `"`, `\`, C0, DEL, C1, U+2028, U+2029, and the complete Unicode `Bidi_Control` set (U+061C, U+200E, U+200F, U+202A–U+202E, U+2066–U+2069), each as `\uXXXX`, at most 6 B per escaped code point. Elision works on encoded bytes, so the bounds include the expansion. C-5 lists every case. |
| SOP2-R1-07 native RSS | 23; C-12 | **`max_rss_native`** is a K2 Count with a closed `rss_unit` code (`kib` on Linux, `bytes` on macOS; Q0:889). It is M3-L's `hostReapedMaxRss`: "`wait4` `ru_maxrss` in the platform's native unit, labelled" (M3L:405). An optional `max_rss_bytes` sits beside it, a checked conversion that is absent on overflow. Every duration and resource field's interpretation is stated (item 23). M3L:286's SM-10 unit is noted for M3-L's next revision. |
| SOP2-R1-NB-01 | 4; C-12 | P0 names provider-asserted closed numeric members explicitly. They are labelled `asserted`, and they are never progress and never admitted fact. |
| SOP2-R1-NB-02 | 11; C-4, C-6 | The guard reports a credential-shape match wholly inside a P2 span as `p2-name-match`, an expected disclosure, not a defect. Escaping under rule E is not a guard action. |
| SOP2-R1-NB-03 | 9, 23; C-1, C-8 | The commit event is split by receipt: `storage.commit.published`, from `PublishedCommit` and through a Run-bearing scope, and `storage.commit.not_published`, from `CommitUndetermined`/`Refused`. Both are owner-token constructed. Scope and identity-marker traits are sealed. |
| SOP2-R1-NB-04 | 12, 13a; "Not decided" | OPP:356's per-member P2 consent is carried to S-OP-9. Approval for one P2 member or class never authorizes another. |
| SOP2-R1-NB-05 | 24 | The DRC insertion keeps "meaning." intact and only inserts a sentence. The SDK4 sentence is scoped to operational records, and the doctor report keeps DR-114's tiers. |
| SOP2-R1-NB-06 | 5 (K7), 12, 17, 22 | Counter ownership is defined: producer-side counters are invocation-global, sink-side counters are per sink, and there is one disposition per missed sink projection. The final snapshot is taken after the cutoff. `Reduced::from_capture` takes the capture owner's summary. `diagnostics` receives only the loss summary. |
| Codex's per-kind and per-control notes | 5 (K6, K9, K13), 9; C-3, C-6, C-8 to C-12 | Adopted:<br>- K6 rejects dot segments and non-workspace origins;<br>- K9 is never built from a parsed value;<br>- K13 never comes from a worker echo;<br>- provider events require ProjectId (M3L:378);<br>- C-3 instruments visitors;<br>- C-7 covers EACCES, ENOSPC, EIO and short writes;<br>- C-8 covers stored-read and ephemeral cases;<br>- C-10 compares effective settings;<br>- C-11 covers sink failure and initialization failure. |

Nothing else of substance changed from r1.

## Standing

- **What it succeeds.** Accepted text names the host's diagnostic behaviour but does not define it:
  - DR-125's standardized family SF-2: "Bounded structured diagnostics only. No unstructured host logs. Redaction is host-owned." (SDK4:78-82). It carries F02:186 ("diagnostic taxonomy, redaction, bounds, structured logging/audit correlation") and F02:193-195 ("bounded structured diagnostics … must not … write unstructured host logs").
  - DRC §8, the D.SDK selection (APP:620-630): diagnostics "may use the existing bounded stderr channel and carry no protocol meaning" (DRC:574-576), and the SDK "never hide[s] dropped messages" (DRC:578-579).
  - The gates: DR-G20 requires "redaction/bounds/audit correlation … no direct UI/unstructured logs" (QG:408), and DR-G21 requires "bounded redacted diagnostics/audit" (QG:428).

  S-OP-2 gives these phrases their concrete meaning for the host's **operational records**: the event registry, the field kinds, the privacy classes, the sinks, the bounds and loss accounting.
- **What it changes.** No frozen or pinned text is edited, and no accepted sentence is narrowed. Item 24 gives the recording form.
- **What it joins without changing:**
  - DR-114's redaction contract (DC4:1005-1086); the doctor report keeps its tiers;
  - the secret-value rule (F03:45-50, F03:56-59, F03:65-67);
  - the no-hidden-environment-input rule (CH13:59-62);
  - the S-OP-4 record join, which M3-L carries (M3L:345-371);
  - OPP §3.1's phase-lawful identities.
- **Its role as a gate:**
  - **Drafted.** The draft existing meets M3-L gate item G7, "S-OP-2 drafted" (M3P:160; M3L:24), on the lead's reading.
  - **Accepted.** Acceptance gates M3-O's O1 part (M3P:174, "P0; S-OP-2") and OPP §8's M3 row (OPP:381).
- **Decisions.** Items marked **(LD)** are lead decisions, dated 2026-10-04. They are made under the owner's standing direction to proceed on the lead's recommendation. Each names the alternative it rejects, and the owner may reverse any of them.
- **Numbers.** Every number is **provisional** unless it is a cited protocol constant, a schema pattern length or a computed encoding bound.

## Short names

Line numbers are those of the live files on 2026-10-04. Each was checked; see "Citations checked".
- **OPP** `docs/implementation/m3/operability/PLAN.md` (r3, accepted; the live file carries a two-line acceptance note)
- **M3L** `docs/implementation/m3/provider-protocol-l/PROPOSAL.md` (r1, draft, not accepted)
- **M3P** `docs/implementation/m3/M3-PLAN.md` (r4, accepted)
- **Q0** `docs/implementation/m3/harness/DESIGN.md` (r13, accepted)
- **REG** `docs/v2/architecture/08-decision-and-readiness-register.md`
- **APP** `docs/coop/completion/architecture-application.v1.json` (the D-369 application)
- **DRC** `docs/coop/completion/distribution-runtime-completion.v2.md` (sha256 `9ab2874e…`, the pin APP:626 carries)
- **SDK4** `docs/coop/artifacts/component-sdk-contract.v4.json` (sha256 `c53d541f…`). The DR-125 application row inherits it (APP:3860-3865). Its own header says `CANDIDATE-NOT-APPLIED` and `"binds": "NOTHING"` (SDK4:7-10). SF-2 is cited as the text the D-369 application inherits.
- **DC4** `docs/coop/artifacts/doctor-contract.v4.json` (sha256 `df2e7175…`, pinned by APP:7573-7574)
- **F02 / F03 / CH13** `docs/v2/architecture/{02-distribution-and-components,03-configuration-and-security,13-evidence-workflows-and-product-contracts}.md`
- **CC** `docs/coop/completion/control-completion.contract.v5.md`
- **QG** `docs/coop/design-corrections/qualification-gates.applied.v1.json`
- **OPV10** `docs/coop/artifacts/operability.v10.json` (V1 candidate, historical; it informs and grants nothing)
- **DLV / RPP** `docs/coop/artifacts/{delivery.v2,rust-provider-protocol.v2}.json`
- **NE / WS / IE** `docs/v2/contracts/product-v1/{native-evidence,workflows-and-surfaces,identity-and-evidence}.md`
- **SLJ** `docs/coop/artifacts/sdk-leftover-join.v9.json` (the DR-125 prior measured join, APP:3866-3869)
- **X3D** `docs/implementation/m2/commit-session-x3d/PROPOSAL.md`
- **UCD** Unicode 17.0.0 `PropList.txt`, property `Bidi_Control`
- Product paths are under `opensip/`, at main `3d2d5b5` (X9-6 integrated).

## Problem

**Accepted law asks for structured, bounded, redacted and correlated host diagnostics, but defines none of the pieces:**
- the event set;
- the field types;
- privacy classes, outside doctor's report;
- the sink rules;
- the record and queue bounds.

OPP fixed the shape (§3.2–§3.3) and left the contract to this successor (OPP:408).

**The product today** (`3d2d5b5`):
- three fixed coded stderr lines (`apps/cli/src/bootstrap.rs:18`, `:43`, `:64`);
- no logging dependency (`Cargo.lock` has neither `tracing` nor `log`);
- no panic hook and no event type.

**The threat** is OP-R1-03's. Compiler diagnostics, provider stderr, `fault` detail and I/O error text can carry source lines, identifiers and secrets in formats no pattern recognises (DC4:1023, DC4:1078). A sink scrubber cannot undo bytes already queued, ringed, written or exported. The guarantee must therefore be a property of **how a record is constructed and admitted**, as DC4's GUARANTEE tier is a property of "the construction path" (DC4:1017). Scrubbing is only a backstop.

## Decisions

### A. The registry and the record model

**1. One host-owned registry; records exist only as registry events (LD).**
- **Decision.**
  - **One registry.** Every operational record the host writes to any sink is an instance of an event declared in **one registry**, a single declarative source module in the product. M3-O chooses its crate. For each event, the registry declares:
    - its name (item 2);
    - its level, fixed at registration;
    - the identities it requires (item 9);
    - its typed fields, each of one `SafeField` kind (item 5);
    - a static message template (item 3);
    - whether it is a candidate for export (item 12);
    - whether it is owner-constructed (item 9).
  - **Record shape.** It follows OPP:161: `{ts, level, event, requestId, [projectId], [planId], [executionId], [runId], [component], [phase], fields, [omitted], [truncated]}`.
    - `ts` is UTC with millisecond precision.
    - `component` is a host-assigned slot: a K1 role plus a `u16` ordinal.
    - `phase` is a K1 phase code.
    - `omitted` and `truncated` are counts, present only when nonzero.
  - **Encodings.** Two forms, both bounded by item 14 and both escaped by rule E (item 13b):
    - **JSON line**, for the file and the bundle: one object per line, UTF-8;
    - **human line**, for stderr (item 13).
- **Basis:** OPP:161, OPP:168, OPP:369; F02:193-195; SDK4:81.
- **Rejected:**
  - **Records as arbitrary serializable structs.** Any `String` field compiles.
  - **Per-crate registries.** There is no single list to audit.

**2. The naming rule: `domain.component.action`, and retirement (LD).**
- **Grammar.** A name is exactly three dot-separated segments. Each segment matches `[a-z][a-z0-9]*(_[a-z0-9]+)*` and is at most 32 bytes; the whole name is at most 96 bytes.
  - The **domain** comes from a closed list in the registry: `host`, `config`, `discovery`, `snapshot`, `plan`, `supervision`, `provider`, `evaluation`, `storage`, `delivery`, `doctor` and `log`. `crash`, `bundle` and `export` are reserved for S-OP-7, S-OP-9 and S-OP-10.
  - The **component** is the noun the event is about.
  - The **action** is a past-tense verb or an observed state.
- **Names are constants.** A name is never built at run time.
- **Change and retirement.**
  - **Additions.** A field may be added to a registered event, but never removed or retyped. Any other change registers a new name and retires the old one.
  - **Descriptors (r2).** A retired event keeps its **complete descriptor** in the registry's `retired` section: its name, fields, kinds, code tables and static bound. Readers re-admit its records by that descriptor (item 13a).
  - **Pruning.** A descriptor may be pruned only by an ordinary registration that leaves the name reserved. Records of a name with no descriptor are then dropped on read.
  - **Code-table members** are never removed, only marked retired, so persisted values keep their meaning.
- **OPP's working names**, registered:

  | OPP working name | Registered name |
  |---|---|
  | `log.record_refused` (OPP:191) | the loss reason `refused`, counted in `log.loss.counted` |
  | `log.loss` (OPP:202) | `log.loss.counted` |
  | `supervision.no_progress` (OPP:238; M3L:417) | `supervision.progress.absent` |

- **Rejected:**
  - **Free-form names of any depth.**
  - **Two grammars side by side.**
  - **Name-only retirement.** It cannot classify old fields (SOP2-R1-02).

**3. Registration, code-table admission, templates and generated documentation (LD).**
- **Code tables (r2, SOP2-R1-01).** A code table is the text table behind a K1 or K3 field. It is admissible only through `code_tables!`, invoked inside the registry module. The macro is not exported.
  - **The token.** For each table the macro emits the `CodeEnum` implementation and a `TableRegistration<E>` token. The token's constructor is private to the registry module, and `CodeEnum` requires it.
  - **Sealing.** `CodeEnum` is also sealed, so no other crate can implement it at all.
  - **What gets listed.** Each table is listed with its **provenance**, which must be one of three release-constant classes:

    | Provenance class | What the table is | How it is checked |
    |---|---|---|
    | `registry-literal` | members written as string literals in the registry source | — |
    | `generated-contract` | the literal table of an enum in a pinned generated contract module (D9 codes, DomainDetail codes, PCS configuration keys and enum values) | the module is named with its generation pin; C-2 checks the table is literal |
    | `protocol-enum` | members written as literals in the registry, citing a closed enum of a pinned protocol schema (for example DLV:857 `UnavailableV1.reason`, RPP:445 `faultKind`, CC:34 health status) | C-2 checks the members equal the schema's enum |

  - **Member rules.** Members are accepted only as `literal` macro tokens. So `include_str!`, `include_bytes!`, `env!`, `option_env!`, `concat!` and any other macro call or build-script (`OUT_DIR`) output fail to match the macro, a compile error. Each member is checked by a `const` assertion:
    - K1: `[A-Za-z0-9][A-Za-z0-9_.:-]{0,63}`, so D9 codes such as `HOST.IO_FAILURE` fit;
    - K3: `[a-z0-9][a-z0-9-]{0,63}`.
  - **No generic tables.** Implementations are emitted only for concrete, non-generic types. A generic adapter (`impl<T> CodeEnum for W<T>`) can be written neither outside the module, because the trait is sealed, nor by the macro.
  - **What is not claimed.** Provenance means reviewed OpenSIP release source or a pinned schema. S-OP-2 does not protect against someone committing a secret into OpenSIP's own source or schemas.
- **Templates.** A message template is a `literal` token in its registry entry: printable ASCII (0x20–0x7E), at most 160 bytes, checked by a `const` assertion. It has no placeholders: the human form appends `key=value` pairs (item 13). Field keys are identifiers matching `[a-z][a-z0-9_]{0,31}`.
- **Ordinary registration.** A code unit may add any of these without a new successor, provided it uses existing kinds, obeys items 2 and 14, and is reviewed in that unit:
  - an event or a field;
  - a domain;
  - a code table or member of one of the three provenance classes;
  - a retirement that keeps its descriptor.
- **Changes that need an S-OP-2 successor:**
  - a new `SafeField` kind;
  - a kind's class;
  - a new privacy class;
  - a new provenance class;
  - a new sink, or a sink ceiling;
  - item 12's projection rule;
  - rule E's escape set;
  - export eligibility beyond item 12's candidates, which also needs S-OP-10.
- **Generated documentation.** The registry renders two artifacts, both committed in the product and checked by a drift test:
  - an event reference in Markdown, giving per event its name, level, required identities, fields with kinds, classes and encoded bounds, sink projection, export candidacy and template, plus every code table with its provenance and every retired descriptor;
  - the same content as JSON. It is the descriptor source for item 13a's readers and for the S-OP-11 harness.

  The runbook (OPP:359) consumes them (lesson F1, OPP:129).
- **Rejected:**
  - **An open `CodeEnum` whose only guard is constness.** A `const` can hold `include_str!` contents, so it bounds run-time substitution but proves nothing about provenance (SOP2-R1-01).
  - **A JSON or TOML registry with a code generator.** It adds a generation source for a Rust-only consumer.
  - **Attribute macros spread across crates.**

### B. Privacy classes and the closed `SafeField` set

**4. Privacy classes P0–P3.** These refine OPP:169. Each class is defined by what may determine a value's bits.

| Class | Definition | Examples |
|---|---|---|
| **P0** release, measurement and closed assertion | Every bit is fixed by one of: an OpenSIP release constant; a registered code table (item 3); an admitted signed or release catalog; a count, size or duration the host measured; or **a closed numeric member a provider asserted through an admitted protocol message**. Asserted values are labelled `asserted` in the registry and are never progress or admitted fact (r2, SOP2-R1-NB-01). Nothing comes from project content, the user's account or provider free text. | D9 and DomainDetail codes, reason enums, counts, sizes, durations, versions, platform, admitted ids, the length of a reduced text, `resourceReport` values (asserted) |
| **P1** correlation | Opaque identifiers the host minted from a CSPRNG (RequestId, ExecutionId, ProjectId; WS:78-82; IE:42-43, IE:61-63), content-addressed identities over sealed structures (PlanId, SnapshotId, committed RunId, universe keys, closure ids), the process id, and the keyed ephemeral path tag (item 6). They reveal no name or content, but they link records, so export excludes them by default (OPP:180). | `req1_…`, `exec1_…`, `plan2:…`, the universe-key suffix |
| **P2** project structure | Names and positions chosen by the project or an operator: project-relative paths, file and directory names, line and column, rule ids, and declared names. Never content, but possibly sensitive in itself (DC4:1079). | `src/a/b.ts`, line 41, a rule id, `GITHUB_TOKEN` (the name only) |
| **P3** content and free text | Source bytes; provider stderr; `fault` and `refusal` detail; error and panic message text; caller free text; configuration string values of no P0–P2 kind; secret values; environment values; any digest or fingerprint of these (OPP:168; OP-R2-NB-01). | everything else |

**P3 has no `SafeField` kind, so nothing of P3 can be put in a record of any class.** The type system enforces this (item 8), and item 13a enforces it again at read-back. The scrubber does not (item 11).

**5. The closed `SafeField` kinds.** This is the whole set. Each kind is sealed: only the vocabulary module defines kinds. Each lists its lawful constructors. No kind has a constructor from `&str`, `String`, `[u8]`, `Path`, `OsStr`, `fmt::Arguments`, an error object or a deserializer.

The **V** column is the maximum encoded value in either form, including quotes, wrapper syntax, rule E escaping and maximum numeric width (item 14).

| # | Kind | Class | Lawful constructors | V | Why it cannot carry source or secrets |
|---|---|---|---|---|---|
| K1 | `Code<E>` | P0 | `E` is a **registered** table (item 3). The run-time part is only an index. | 66 | Member text is a registered literal or a pinned-schema member, matching `[A-Za-z0-9_.:-]` and at most 64 bytes. An unregistered or generic table does not compile. |
| K2 | `Count`, `Bytes`, `Elapsed`, `Flag`, `Errno` | P0 | Integers and booleans:<br>- `Elapsed` is monotonic nanoseconds;<br>- `Errno` comes only from `raw_os_error()`;<br>- asserted values only from an admitted protocol member, labelled. | 20 | A number of at most 20 digits (`Errno` at most 11). **Forbidden:** a number computed from a secret value. Secret types expose no length (item 20). |
| K3 | `RegisteredCode<T>` | P0 | Exact byte-match of external text against a registered table `T` with `[a-z0-9-]` members of at most 64 B, at most 256 entries. On a match it encodes the table's own member. Otherwise it encodes `{"unrecognized":{"bytes":N,"truncated":B}}` (65 B maximum). | 66 | It never re-emits the input bytes; a non-member is reduced to its length. |
| K4 | `Version` | P0 | Release constants, or the version fields of admitted signed manifests, matching `[0-9A-Za-z.+-]{1,64}` | 66 | Fixed by a release or a signed catalog. |
| K5 | `AdmittedId` | P0 | An entry of an admitted signed or release catalog (component, capability, bundled pack `name:version`, platform), built from the catalog entry type and matching `[A-Za-z0-9_.:@/+-]{1,128}` | 130 | A catalog member the host verified. |
| K6 | `CodeLocation` | P0 | `&'static core::panic::Location` only. The file is emitted only if all of these hold:<br>- it is relative;<br>- every component is a normal component matching `[A-Za-z0-9._-]+` (no empty, `.` or `..`);<br>- the first component is `apps`, `crates` or `providers`;<br>- the file is at most 128 B.<br>Otherwise it is emitted as `external` plus the line. | 160 | It names only OpenSIP's own workspace code. Dependency and absolute paths, and apparent prefixes with traversal, never appear (C-9). |
| K7 | `Reduced` | P0 | Exactly two constructors:<br>- `Reduced::of(text)`, for text held whole, such as `fault` or `refusal` detail of at most 1,024 B;<br>- `Reduced::from_capture(&CaptureSummary)`, where the capture owner supplies the total bytes observed (saturating) and whether the bound was hit.<br>Neither keeps any byte of text. | 48 | Only `{bytes, truncated}` remains; **no digest** (OPP:171; OP-R2-NB-01). |
| K8 | `Counts<E>` | P0 | One `u64` per variant of a registered table, encoded as a **fixed-index JSON array** in table order: at most 21·n + 1 B for n variants, within 24 B per variant. The descriptor maps index to member. Reserved for the loss marker. | 21·n+1 | Counts indexed by registered names. Depth 2. |
| K9 | `IdentityDigest<K>` | P1 | Only from the owning typed identity value of kind `K`: SnapshotId (`snapshot2:`+64 hex), universe key (64-hex suffix, NE:3160-3164), closure id (`closure2:`+64 hex), or the manifest digest of a signed artifact. **Never from bytes, a hasher, text, or a value parsed from a record.** | 80 | A content-addressed identity over a sealed structure, never a file-content digest (OP-R2-NB-01). |
| K10 | `PathRef` | P1 | `{"anchor": K1 PathAnchor, "tag": 16 lowercase hex}` (item 6), built from a path the host holds as a typed handle | 64 | No path bytes and no unkeyed digest. |
| K11 | `ProcessId` | P1 | The host's own pid, or the pid of a process the host spawned | 10 | A number. |
| K12 | `ProjectPath` | P2 | Only from the host's admitted project-relative path types: discovery and snapshot entries, and admitted fact anchors. Must be valid UTF-8; otherwise the caller uses `PathRef`. | 256 | A name that exists in the project tree. It may be sensitive (DC4:1079), hence P2. It carries no content. |
| K13 | `Position` | P2 | Line and optional column from **admitted** spans, never a worker echo | 40 | Numbers. P2 because, joined to a path, they locate content (OPP:169). |
| K14 | `RuleId` | P2 | Entries of the admitted policy catalog | 130 | A catalog name. P2 follows OPP:169; Codex confirmed keeping it P2 in its r1 review. |
| K15 | `DeclaredName` | P2 | Names validated against a declaration: environment-variable names a manifest declares (DC4:1035), and secret-handle names once DR-108 lands (item 20) | 130 | A name, never a value. P2 because an operator chose it (DC4:1079). |

`Correlation<K>` (RequestId, ProjectId, PlanId, ExecutionId, RunId) is **header-only** and P1. Records get it only from the emitting scope (item 9).

**6. Paths: project-relative, or an anchored placeholder with a keyed ephemeral tag (LD).**
- **Decision.** A path appears in a record in exactly one of two forms:
  - **`ProjectPath`** (P2), when the host holds it as an admitted project-relative UTF-8 path.
  - **`PathRef`** (P1) otherwise:
    - **The anchor** is a K1 code from a registered table: `installation`, `store`, `log-root`, `scratch`, `project`, `system-temp` or `external`.
    - **The tag** is the first 64 bits of HMAC-SHA-256(*k*, the path's native bytes), written as 16 lowercase hex digits. *k* is a 256-bit key drawn from the platform CSPRNG when logging starts. It is held in memory only, never written, never derived from an identity, and different in every process.

  The tag correlates records within one process. It is not an identity and not collision-free.
- **Never present:** absolute paths, home directories, user or host names (DC4:1038-1043).
- **Basis:** DC4:1039, DC4:1043, DC4:1071; OPP:168.
- **Rejected:**
  - **An unkeyed hash.** It is an oracle for low-entropy home directories and usernames.
  - **A persistent per-installation key.** Its custody would sit beside the logs.
  - **A relative path under OpenSIP-owned roots.** Store object paths are content digests.

**7. What is never a field.** These have no kind, so no record can carry them:
- free text of any origin: provider stderr; `fault` detail (CC:36); `refusal` detail (CC:32); the health or ping nonce (CC:33, CC:53); I/O and library error messages; panic payloads; `Debug` or `Display` output;
- caller text: `clientCorrelationId` (`command-envelope-v7.schema.json:38-42`; OPV10:191). Its presence may be a `Flag`;
- configuration string values of no P0–P2 kind;
- secret values and environment-variable values;
- backtraces;
- digests of P3 data;
- DomainDetail `remedy` and `subject` strings (`common-v4.schema.json:641-686`). The detail code is K1.

### C. Enforcement at construction

**8. Type-level closure (LD).** The reference design follows. Its names are illustrative; M3-O chooses the final ones.

```rust
mod sealed { pub trait Sealed {} }
#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum PrivacyClass { P0, P1, P2 }                  // no P3 variant exists

pub trait SafeField: sealed::Sealed {                 // implemented only for K1..K15
    const CLASS: PrivacyClass;
    const MAX_VALUE: usize;                           // V of item 5, whole encoded value
    fn encode(&self, form: Form, out: &mut FieldOut<'_>);  // never exceeds MAX_VALUE
}
pub struct TableRegistration<E>(PhantomData<E>);     // constructor private to registry
pub trait CodeEnum: Copy + sealed::Sealed {           // sealed: impls only via code_tables!
    const REGISTRATION: TableRegistration<Self>;      // only code_tables! can mint it
    const TEXT: &'static [&'static str];              // literal members, grammar-checked
    fn index(self) -> usize;
}
pub trait Event: sealed::Sealed {                     // implemented only by registry!{}
    const NAME: &'static str;
    const LEVEL: Level;
    type Requires: IdentitySet;                       // item 9
    const FIELD_CLASSES: &'static [PrivacyClass];
    const MAX_LINE: usize;                            // item 14: 768 + Σ(36 + V)
}

code_tables! {
    ProviderRole: registry_literal { "typescript-semantic", "rust-semantic" };
    // A D9 code table names its pinned generated contract module (provenance class
    // generated-contract); a protocol enum lists literals and cites its schema.
}
registry! {
    provider.process.spawned: info, requires(Project, Plan, Execution), export(no),
        "provider process started" {
        role: Code<ProviderRole>, universe: IdentityDigest<Universe>, pid: ProcessId,
    }
}
// Per entry: a struct with exactly these typed fields, its Event impl, and
// const _: () = assert!(Self::MAX_LINE <= 4096 && Self::FIELDS <= 32 && keys_ok && template_ok);
```

What this gives:
- **No text in a field.** `SafeField` is sealed and has no implementation for any text, byte, path, error or formatting type.
- **K1 and K3 text is provenance-checked.** It comes only from registered tables, whose members are grammar-checked `literal` tokens, or a pinned literal table. `include_str!`, environment macros, build output, unregistered tables and generic adapters do not compile (C-1, C-2).
- **Constructor provenance** decides what the P1 and P2 kinds can hold. Each is built only in one of two ways:
  - (a) a `From` impl from the owning typed value;
  - (b) a mint capability the vocabulary issues once at initialization to the owning module. The `RequestId` mint goes to `RequestAuthority` (`crates/host/src/request.rs:15-55`).

  There is no blanket text or byte adapter and no deserializer constructor. The constructor and mint list is OPP §7's audited exception list, and C-2 refuses additions.
- **Static bounds.** Field classes and the whole-line maximum are compile-time constants, so item 14's bound is a compile error.
- **No debug-build escape** and no `unsafe_text()` hatch. A test-only `SecretValue` stand-in proves that secrets are not fields (item 20).
- **Basis:** OPP:168, OPP:170, OPP:369; DC4:1017.
- **Rejected:**
  - **Run-time privacy tags.**
  - **A validated "safe string".** It is a shape check, not provenance.
  - **An escape hatch.**

**9. Phase-lawful identities, enforced by sealed scope types (OPP §3.1).**
- **Emission needs a scope.** Records are emitted only through a scope value. Each scope type implements one **sealed** marker trait per identity it holds: `HasProject`, `HasPlan`, `HasExecution` and `HasRun`. Every scope holds a RequestId.
- **Who creates scopes.** Only the transition that mints the identity creates the scope:
  - project admission;
  - Plan sealing;
  - attempt admission (IE:61-63);
  - a `Committed` publish (`CommitOutcome::Committed(PublishedCommit)`, `crates/storage/src/commit.rs:66-75`), or a stored-Run read.
- **Requirements are checked at compile time.** `emit::<E>` is bounded by `E::Requires`.
- **What the rules give:**
  - **No forged scopes.** No scope or marker can be built or implemented outside its owning transition.
  - **The ExecutionId survives.** It stays available for CommitUndetermined, because the attempt scope outlives the outcome (X3D:130-132 via OPP:156).
  - **No candidate RunId.** No RunId constructor takes a candidate (OPP:157-159).
  - **The emergency case.** If `RequestAuthority::begin` fails there is no scope and no record. The fixed line stays the only output (`bootstrap.rs:15-23`; OPP:160).
- **Owner-constructed events (r2, SOP2-R1-NB-03).** An event the registry marks `owned(Owner)` has private fields, and it can be built only with an owner token minted once to that owner. Two commit events, split by receipt, carry this mark:
  - `storage.commit.published` is built only from `PublishedCommit` and emitted through the Run-bearing scope that the same receipt yields;
  - `storage.commit.not_published` is built only from `CommitUndetermined` or `Refused`, through the attempt scope.

  No free struct or outcome pairing exists, so CommitUndetermined cannot reach a Run-bearing scope, and Committed cannot be recorded without its Run.
- **Not decided here.** A process-level scope for a multi-request host is M5's.
- **Rejected:**
  - **A run-time phase check.** It catches errors only on the paths tests reach.
  - **One commit event with a run-time outcome code.**

**10. Foreign events and the framework (LD).**
- **Decision.** S-OP-2 does not require `tracing` (OPP:147). Whatever transport M3-O picks must keep four rules:
  - **(a)** every record is built from a registry event;
  - **(b)** a callsite outside the registry, including any dependency's `tracing` or `log` event, never reaches a sink and never has its fields visited or formatted. With `tracing`, the subscriber returns `Interest::never()` for every callsite outside the registry;
  - **(c)** no `log` logger is installed;
  - **(d)** spans are registry entries too.
- **Rejected:** a deny-list layer over free-form `tracing` fields.

**11. The final guard at every sink.**
- **Decision.** One scrubber runs at every sink, as OPP:182 requires:
  - ANSI first, then C0 (DC4:1062-1063);
  - a length bound with a marker (DC4:1066-1067);
  - known credential shapes.

  It is DISCLOSURE-tier (DC4:1020-1025).
- **How firings are classified (r2, SOP2-R1-NB-02).** The encoder passes the guard the byte spans of each P2 field. A firing is one of three things:
  - **any ANSI or C0 strip, length cut, or credential-shape match outside a P2 span** is a **defect**, because rule E makes such bytes impossible in a lawful line;
  - **a credential-shape match wholly inside a P2 span** is counted `p2-name-match`. It is an expected disclosure of an operator-chosen name (DC4:1079), not a defect;
  - **rule E escaping** is the encoder's work, never a guard action.

  The M3 corpus requires zero defects (C-6).
- **Basis:** OPP:182; DC4:1012-1028.

### D. Sinks

**12. Per-sink allowlists, enforced by static projection (LD).**

| Sink | Owner of the sink | Classes | Notes |
|---|---|---|---|
| stderr, human | S-OP-6 (switches); this law (content) | P0, P1, P2 | Off unless asked (OPP:162, OPP:228). |
| file | S-OP-1 | P0, P1, P2 | No file before S-OP-1 (OPP:211). |
| pre-scope buffer | this law | P0, P1, P2 | Memory only. Flushed only into the file sink. |
| crash ring | S-OP-7 | P0, P1 | Plus the event name and phase (OPP:178). |
| support bundle | S-OP-9 | P0, P1 by default; P2 only with **per-member consent** (OPP:356) | Records are re-admitted first (item 13a). |
| OTLP export | S-OP-10, O4 | P0 only, plus an export-local trace id | Only export-candidate events, once S-OP-10 admits them (OPP:180, OPP:256). |
| envelope `diagnostics` | S-OP-6 | P0, **the loss summary only** | No ordinary event reaches it (SOP2-R1-NB-06). |
| P3 | — | **no sink** | No kind exists. |

- **Projection.** Every event may reach the stderr, file, pre-scope, ring and bundle sinks. OTLP is opt-in per event, and `diagnostics` carries only the loss summary. Each sink has a constant class ceiling. Its encoder writes a field only if that field's **static** class is at or below the ceiling, and counts the fields it left out in `omitted`. Projection reads compile-time data only, never the value.
- **Rejected:**
  - **Whole-event refusal per sink.**
  - **Projection by inspecting values.**

**13. Sink-specific rules.**
- **stderr, human.** One line per record: `<level> <event>: <template> key=value…`.
  - String values are double-quoted and escaped by rule E (item 13b).
  - Numbers are bare.
  - Composite kinds (K3's unrecognized form, K6, K7, K8, K10, K13) use their JSON text.
  - Which identities to print, colour and verbosity are S-OP-6's; the bound covers printing all of them (item 14).
  - **The stderr sink never holds a lock the command's output or termination path takes.** In particular it does not hold std's `Stderr` lock across a write, so a blocked log write cannot block the termination path's coded line. That line keeps its ordinary blocking behaviour (OPP:308).

  The three fixed bootstrap lines stay outside the vocabulary, on OPP §7's audited exception list.
- **File.** JSON lines. Each stream's first record is `log.stream.opened`. S-OP-1 owns layout, custody, rotation, retention and the stop rule (OPP:204-206).
- **Crash ring.** Every emitted record at or above `info` (provisional) is also projected to P0–P1 and copied into the preallocated ring (item 16). S-OP-7 owns the hook and the crash file (OPP:302-313). The hook never reads a panic payload (OPP:183, OPP:307).
- **Support bundle.** It contains only records re-admitted by item 13a and projected by the descriptor's classes. P2 members are included only with their own consent: approval for one P2 member or class never authorizes another (OPP:356). The consent flow is S-OP-9's.
- **OTLP.** The event name, P0 fields, and a random per-session trace id. No RequestId, path or rule id unless S-OP-10 admits one (OPP:180, OPP:256).
- **Envelope `diagnostics`.** It receives only item 17's loss summary, in the existing `BoundedText` carrier (≤ 1,024 characters, ≤ 256 entries; `common-v4.schema.json:132-135`), worded by S-OP-6.

**13a. Closed re-admission of persisted records (r2, SOP2-R1-02).**
- **Who it binds.** Every reader that takes persisted operational records and emits them to another sink or output: S-OP-9's bundle and its later doctor log query, and any harness projection. Such a reader **never passes through raw serialized values and never trusts a record's own class claims**.
- **The steps, for each line:**
  1. **Bounded read.** A line longer than 4,096 bytes plus its newline is dropped (`oversize`).
  2. **Parse.** The line must be one JSON object with no duplicate keys and only header members. Otherwise it is dropped (`malformed`).
  3. **Header.** Every header value must satisfy its grammar. Otherwise the record is dropped (`header-invalid`). The grammars:
     - identities by the `common-v4.schema.json` patterns (RequestId `req1_`+32 hex, ProjectId `prj1-`+64 hex, PlanId `plan2:`+64 hex, ExecutionId `exec1_`+32 hex, RunId `run3:`+64 hex);
     - `level` from its table;
     - `event` by item 2's grammar;
     - `ts` by its fixed format;
     - `component` and `phase` as members of their registered tables;
     - `omitted` and `truncated` as integers of at most 32.
  4. **Descriptor.** The event name must have a descriptor, active or retired, in the running registry. Otherwise the record is dropped (`unknown-event`).
  5. **Fields.** Each key in `fields` is checked against the descriptor. An unknown key is dropped (`unknown-field`). A value failing its kind's read-back predicate is dropped (`invalid-value`). Fields absent from an older record are simply absent.
  6. **Re-encode.** The reader re-encodes from the admitted typed values only, by item 5's encoders and rule E, so the output's bounds are item 14's.
  7. **Project.** The reader projects by the descriptor's static classes, then by its own ceiling (the bundle: P0–P1, P2 with consent).
  8. **Disclose.** One P0 manifest member counts records dropped by reason (`oversize`, `malformed`, `header-invalid`, `unknown-event`) and fields dropped by reason (`unknown-field`, `invalid-value`). Rejected bytes are never echoed.
- **Read-back predicates, by kind:**

  | Kinds | Predicate |
  |---|---|
  | K1, K3 | exact member, active or retired, of the descriptor's registered table, re-encoded from the table's own constant. K3's unrecognized form must be its exact two-integer shape. |
  | K2, K7, K8, K11, K13 | integers within the kind's width, in the exact shape. K8's array length equals the table size. |
  | K4 | the version grammar |
  | K5 | membership in an admitted catalog the running build holds; otherwise dropped |
  | K6 | item 5's workspace-path predicate, or `external` |
  | K9 | the exact identity grammar of the descriptor's identity kind |
  | K10 | a registered anchor plus 16 lowercase hex |
  | K12, K14, K15 | a valid JSON string whose decoded value is UTF-8 and within the kind's limits; re-escaped by rule E; P2 only |

- **Residual, stated.** Re-admission proves that every re-emitted value is a valid encoding of its registered kind, and for K1, K3 and K5 a member of its table or catalog. It does not prove the host wrote the value. A party able to write the log directory can place values that pass the grammar. Log custody is S-OP-1's, and tamper evidence is not claimed.
- **Rejected:** class projection of parsed records by event name alone. A known name can carry text in a P0 field (SOP2-R1-02).

**13b. Escaping rule E (r2, SOP2-R1-06).**
- **Scope.** One rule for both encodings and for every string value of every kind. Today K12, K14 and K15 need it. K1, K3, K4, K5 and K6 have grammars that already exclude the escaped set, and rule E still applies to them.
- **The escaped set:**

  | Code points | What they are |
  |---|---|
  | U+0022, U+005C | `"` and `\` |
  | U+0000–U+001F | C0 |
  | U+007F | DEL |
  | U+0080–U+009F | C1 |
  | U+2028, U+2029 | line and paragraph separators |
  | U+061C, U+200E, U+200F, U+202A–U+202E, U+2066–U+2069 | the complete Unicode `Bidi_Control` property (UCD), 12 code points |

- **Form.** `\"` and `\\` for the first two. Every other escaped code point is `\u` plus 4 lowercase hex digits (for example `\u001b`, `‮`); no short forms are used.
  - The output is valid JSON, and the same bytes appear in the human form, where strings are double-quoted.
  - An ESC is always escaped, so an ANSI sequence is inert.
- **Expansion.** At most 6 bytes per escaped code point:
  - a 1-byte C0 becomes 6 bytes;
  - a 2-byte U+061C or C1 becomes 6 bytes;
  - a 3-byte U+202E becomes 6 bytes.

  Encoders elide on **encoded** bytes, from the front, at a code-point boundary and never inside an escape. The elided value starts with the fixed ASCII prefix `...`, and the record's `truncated` count rises. Every V in item 5 therefore includes the expansion.
- **The set is closed.** A future Unicode version that adds `Bidi_Control` members needs an S-OP-2 successor.
- **Non-UTF-8** names are not constructible as string kinds; the caller uses `PathRef`.
- **Rejected:**
  - **Stripping.** It hides what a name really is; escaping is lossless.
  - **JSON-standard escaping only.** It leaves bidi controls and U+2028/U+2029 raw in files that are later printed.

### E. Bounds (OPP §3.3)

**14. The full-encoding proof (LD; r2, SOP2-R1-05).**
- **What is bounded.** The whole output line, newline included, in both forms (item 1).
- **Header reserve: 768 bytes.** Computed with every lawful header member at its maximum:
  - **JSON header: 678 B.** `{`, `ts` 24, `level` 5, `event` 96, `requestId` 37, `projectId` 69, `planId` 70, `executionId` 38, `runId` 69, `component` 70, `phase` 32, each with its quotes, key, colon and comma; `"fields":{}`; `omitted` and `truncated` at 2 digits; `}` and the newline.
  - **Human header: 756 B.** Level, event, `": "`, the 160-byte template, and every identity, `component`, `phase`, `omitted` and `truncated` as ` key=value`, plus the newline.
- **Per-field overhead: at most 36 B** in JSON (`"key":` and `,`, with a key of at most 32 B), and 34 B in human form (` key=`).
- **Per-kind value bound V:** item 5's column. It includes quotes, wrapper objects or arrays, rule E escaping, elision and maximum numeric widths.
- **The assertion.** `registry!` asserts, for every event:
  - 768 + Σ (36 + V) ≤ 4,096 bytes;
  - at most 32 fields;
  - keys of at most 32 B by grammar;
  - a template of at most 160 B of printable ASCII.

  Since 36 > 34 and both headers are within 768, one assertion covers both forms.
- **Other bounds.**
  - **Depth** is at most 2: every kind is flat except K3's unrecognized form, K6, K7, K8, K10 and K13, each of depth 2.
  - **String fields** are at most 256 encoded bytes (OPP:191).
  - **Example.** The largest initial event is `log.loss.counted`, at most 1,905 B, because K8 over 40 entries is 841 B. The widest is `provider.process.reaped`: 10 fields, at most 1,562 B.
- **What does not compile.** An event that could exceed a bound. The run-time `refused` count remains only as a defensive encoder check, and C-7 requires it to stay zero.

**15. Admission, the queue and the drop policy.**
- **Order.** Level filter, then the per-name budget, then queue reservation, then encoding.
  - The level filter runs before the event is constructed. A filtered record is not loss.
  - The producer reserves `E::MAX_LINE` bytes and one slot with atomic operations **before** encoding, then releases the unused part (admission before allocation; OPP:192).
- **Bounds.**
  - **Queue:** 2 MiB and 4,096 records, whichever comes first (OPP:192).
  - **Headroom for `warn` and `error` (LD):** the last 256 KiB and 512 records are admitted only for those levels.
  - **Per-name budget (LD):** at most 1,024 records of one event name per RequestId (OPV10:170-171 precedent).
- **Drop.**
  - At a bound, the **new** record is dropped and counted (OPP:192).
  - **Producers never wait.** No producer takes a lock that is held across I/O, and none waits for space (OPP:201).
- **Memory.** About 2.2 MiB per host process (OPP:207). It is a total across however many writer threads M3-O uses.

**16. The pre-scope buffer, the crash ring and the bounded termination wait (LD; r2, SOP2-R1-04).**
- **Pre-scope buffer.** 64 KiB and 256 records, drop-newest, counted `prescope-full` (OPP:193). "Pre-scope" means before the sink is known; it is unrelated to item 9's scopes.
  - If the invocation later holds S-OP-1's write capability, the records are flushed into the file in order (OPP:220).
  - Otherwise they are discarded at exit and counted `unpersisted`.
- **Crash ring.** 64 KiB preallocated, at most 256 records, overwriting the oldest, holding P0–P1 projections (OPP:194). Overwrites go in the crash record's header (S-OP-7), not into loss.
- **The termination wait.** The deadline belongs to the **command's termination path**, not to any sink syscall.
  1. **Cutoff.** Once the command's result is decided and its required output is done, or on the cancellation termination path, the termination path closes producer admission with one atomic store. A record emitted afterwards, for example by a reaper thread, is dropped and counted `drain-abandoned`.
  2. **Timed wait.** The termination path signals the writer or writers to drain, then waits on a timed primitive (a condition variable, or a park with timeout) for their "drained" notification. The budget is 200 ms on normal exit and 100 ms on cancellation (OPP:197-198). A writer blocked in `write(2)` cannot lengthen this wait.
  3. **On notification or expiry:**
     - every persistent sink gate is closed, so nothing more is admitted (item 17);
     - the **final counter snapshot** is taken;
     - every record still queued, or in an admitted unit whose completion was not confirmed, is added as `drain-abandoned` for its sink;
     - the loss summary goes to S-OP-6's carrier;
     - the command proceeds to exit, with its exit code unchanged.
  4. **Abandonment.** A writer still blocked is not joined and not signalled. Process exit ends it. The command's output and exit code are complete within the budget.
- **In-flight I/O limitation, stated.** A thread blocked in a kernel write to a stalled regular file or network filesystem can delay the operating system's teardown of the process until the kernel returns. That is the same residual OPP:310 states for the crash path. S-OP-2 bounds the command's wait, not the kernel's. An abandoned unit that was already admitted may still complete afterwards, and the summary will have counted it as abandoned, so the summary may overcount loss.
- **Export shutdown.** 1 s at M5 (OPP:199), under the same rule, which is S-OP-10's.

**17. Loss accounting, the best-effort marker and the sink gate (r2, SOP2-R1-03, -04, NB-06).**
- **Loss reasons.** A closed enum of eight:

  | Reason | Category | Owner | Meaning |
  |---|---|---|---|
  | `refused` | loss | producer, global | defensive encoder refusal; expected zero |
  | `budget` | loss | producer, global | per-name budget exceeded |
  | `queue-full` | loss | producer, global | queue bound hit |
  | `prescope-full` | loss | producer, global | pre-scope bound hit |
  | `unpersisted` | policy | producer, global | pre-scope records discarded because no persistent sink was admitted |
  | `sink-failed` | loss | per sink | I/O error; that record and every later one for the sink |
  | `sink-stopped` | loss | per sink | the gate was closed at admission, including a short-write remainder |
  | `drain-abandoned` | loss | global after the cutoff; per sink for queued or unconfirmed records | not written within the termination wait |

- **Counters.** A global matrix and one matrix per sink, each over (reason, level). Each lost record has **one disposition per sink projection it missed**: a record dropped before the queue counts once in the global matrix, and a queued record that missed sink S counts once in S's matrix. Each sink also keeps its first I/O error kind and errno.
- **The final snapshot** is the one item 16 takes, after the cutoff. It is the only source of the loss summary.
- **The marker, `log.loss.counted`, is best-effort.**
  - **When it is attempted.** Only when all three hold:
    - the writer has drained sink S's queue;
    - S's gate is open;
    - the termination wait has not expired.

    The writer then encodes, into a slot preallocated at logging start, the global matrix plus S's matrix as of that moment, and admits the marker as an ordinary write unit through the gate.
  - **Outcomes.** A closed set, observable by tests and by the termination path:
    - `written`;
    - `failed`, with its errno;
    - `suppressed`, when the gate was closed;
    - `skipped`, when the wait had expired or the writer was blocked and never reached it.
  - **On failure.** No retry, no counter, no further record and no panic. A cap hit never emits through the saturated path (OPP:202).
  - **Its counts are as of its admission.** They may undercount later abandonment. The final snapshot is authoritative.
- **Visibility.** If any loss counter is nonzero and the command produces an envelope, the P0 summary goes to `diagnostics` through S-OP-6 (OPP:203). Loss never changes Coverage, termination, exit or a committed Run (OPP:203; OPP §5.2).
- **The sink gate. The atomic load is the admission point.**
  - **Closing.** Each persistent sink has an atomic gate. Closing it is one atomic store with release ordering, and it never waits.
  - **Admission.** The writer's acquire load of `open`, made immediately before a syscall, is that syscall's admission. **Every syscall needs its own successful load**: a write unit's first write, every short-write continuation, and the marker.
  - **After a load sees `closed`,** nothing more is admitted to that sink. A unit's unwritten remainder is abandoned and counted `sink-stopped`. Readers drop the torn last line (item 13a).
  - **Write units** are at most 64 KiB (provisional).
  - **Residual, stated.** A unit admitted before closure may be **issued and completed after** it, because the writer can be descheduled between its load and its syscall. The bound is at most one admitted unit per sink writer, at most 64 KiB. S-OP-2 claims no retroactive suppression and no syscall-issuance ordering. Whether this residual is acceptable after an uncertain or latched commit outcome is **S-OP-7's decision with the X3D owner's assent** (OPP:312; OP-R3-NB-02). If it is not, S-OP-7 must specify a coordinated issuance mechanism.
  - **Who closes the gate:** S-OP-1's stop rule (OPP:205), S-OP-7's suppression, and item 16's wait expiry. This law fixes only the mechanism and the accounting.
- **Basis:** DRC:578-579; OPP:201-203; OPV10:101-102.

### F. Joins

**18. With DR-114 (DC4 redaction).**
- **Decision.** S-OP-2 applies DC4's two-tier structure to every operational sink, without changing DC4.
  - **The GUARANTEE tier is the vocabulary plus re-admission.** Every record field is a member constructed from classified sources (DC4:1016-1017), and no field exists outside the closed kinds.
  - **The DISCLOSURE tier is only item 11's guard.**
- **Mapping of DC4's classes** (DC4:1028-1068):

  | DC4 class | S-OP-2 treatment |
  |---|---|
  | secret values | no kind; a handle name and presence only, after DR-108 |
  | environment values | no kind; declared names only, as K15 |
  | absolute paths | K12 or K10 |
  | host and account identifiers | no kind |
  | raw error objects | an error-kind code plus `Errno`, and no message (stricter than DC4's "name plus scrubbed message") |
  | ANSI and C0 | rule E |
  | unbounded strings | item 14 |
  | secret previews | none |

  DC4's honest exclusions carry over (DC4:1076-1083).
- **Projections.** "Every projection consumes the already-redacted report" (DC4:1086) becomes: every encoder consumes an already-typed record, and every reader re-admits before re-encoding (item 13a).
- **Doctor.** Doctor's **report** stays DC4's, with no schema change. Doctor's operational **records** follow S-OP-2 and go to nonpersistent sinks (OPP:216). Codex accepted this split in its r1 review (R2).

**19. With DR-125 (the SDK's "bounded structured diagnostics").**
- **The reading.** For the host's operational records, "structured host logs" means registry records only, and "unstructured host logs" means any byte that a log sink receives and a registry encoder did not produce. That is forbidden (SDK4:81, SDK4:103; F02:194-195). "Redaction is host-owned" (SDK4:81) is items 8–13b.
- **Component diagnostics under O1(a)** (M3L:326-343) reach records only as host-constructed codes and reductions:
  - closed protocol responses become K1;
  - stderr becomes K7 (DRC:574-576; DLV:1133).

  Components never write a log, receive a log path or emit a registry event (OPP:222; M3L:389).
- **What S-OP-2 does not add:** no SDK operation (DRC:521-533 is unchanged) and no wire member. "Never hide dropped messages" (DRC:578-579) is realised for host records by item 17.
- **The gates.** DR-G20's `log` surface (SLJ:481) and its "redaction/bounds/audit correlation" (QG:408), and DR-G21's "bounded redacted diagnostics/audit" (QG:428), are exercised by the controls S-OP-11 authors (OPP:418).
- **Review.** Codex accepted this reading within O1(a) in its r1 review (R1).

**20. With the secret-handle rule (F03:45-50; DR-108).**
- **Values.** A resolved configuration secret value is "excluded from … diagnostics, and support bundles" (F03:49-50). It has no `SafeField` kind, and sealing keeps it that way.
- **Any future secret-bearing type** (the DR-108 successor; REG:297) also has:
  - no `Display` or `Serialize`;
  - no `Debug` that shows the value;
  - no `AsRef<[u8]>` or text `Deref`;
  - no exposed length.
- **Handles.** A handle's name is K15 (P2), and its presence is a `Flag` (P0) (DC4:1017).
- **Brokers.** A broker logs no value (F03:65-67).
- **Source.** Source is not a configuration secret (F03:56-59). It is P3 because no kind accepts its bytes. S-OP-2 does not claim that code which reads source cannot see secrets in it.

**21. With the no-hidden-environment-input rule (CH13:59-62).**
- **Decision.** Level filters, sink selection, export settings and every bound come only from:
  - release constants;
  - S-OP-5's configuration section;
  - S-OP-6's flags.

  Nothing is read from `RUST_LOG`, `RUST_BACKTRACE`, `RUST_LIB_BACKTRACE` or `OTEL_*` (OPP:139, OPP:226). No filter constructor that reads the environment is used.
- **Environment variables in records** appear only as declared names, never values (OPP:170).
- **Platform access.** Legitimate platform and resolver environment access stays on OPP:367's owner list.

**22. With S-OP-4: the provider records (M3L items 12–14).**
- **Nothing crosses the wire because of S-OP-2.** Neither TS2 nor Rust3 gains a frame or member (M3L:98-117).
- **The host is the only author.** It writes every provider-attributed record from host-held values (M3L:382). RequestId never reaches a child (M3L:376).

| Provider-originated value | Source | Disposition | Class |
|---|---|---|---|
| stderr bytes | DRC:574-576; DLV:1133; bound 262,144 (NE:2967; RPP:117; `handshake-v1.schema.json:281-283`) | `Reduced::from_capture`: total bytes observed, and whether the capture hit its bound | P0 |
| control `fault.detail` | CC:36, ≤ 1,024 B (CC:56-58) | `Reduced::of` | P0 |
| control `refusal.detail` | CC:32 | `Reduced::of`, plus the refusal family as K1 (`protocol-enum`, RF1–RF8) | P0 |
| health and ping nonce | CC:33, CC:50-54 | never recorded | — |
| `healthReport` status | CC:34 | K1 (`protocol-enum`: ready, busy, stopping) | P0 |
| `resourceReport` | CC:35 | K2 `Bytes`, `Elapsed` and `Count`, labelled `asserted`. Never progress (M3L:339). | P0 |
| Rust `ProviderFaultV2.faultKind` | RPP:445 | K1 (`protocol-enum`) | P0 |
| Rust `ProviderFaultV2.detailCode` | RPP:445 | K3 `RustDetailCode`, with an **empty table at r2**, so every value is `{unrecognized}` (= M3L:351). The G unit may add members as an ordinary registration. | P0 |
| closed terminal responses | for example DLV:857 `UnavailableV1.reason`, and their NE §9 successors | K1 (`protocol-enum`) | P0 |
| stage terminal | NE:2025 | K1 (`protocol-enum`) | P0 |
| progress | host-counted admitted transitions (M3L:352-356) | K2 `Count` per stage and universe | P0 |
| universe | NE:3160-3164 | K9 `Universe`, the 64-hex suffix | P1 |

- **Lead decisions.** Two rows go beyond M3L:345-371: `refusal` detail is reduced, and nonces are never recorded. Codex accepted both in its r1 review.
- **Rejected:** a closed `detailCode` set now. It would give an open protocol member a meaning, which M3L item 1 forbids.

### G. The initial registry

**23. The initial events (r2).** These are names and fields for review; the levels are provisional.
- **Header and requirements.** Every event carries item 1's header. "Requires" lists identities beyond the RequestId.
- **Common fields.** In every `provider.*` and `supervision.*` row:
  - `role` is K1 `ProviderRole`;
  - `universe` is K9 `Universe`;
  - the requirement is **Project, Plan, Execution** (M3L:378).
- **Export.** "Cand." marks a candidate for S-OP-10 (P0 fields only, after projection). Nothing is exported before S-OP-10.
- **Owner-constructed events.** The two `storage.commit.*` events are `owned(storage)` (item 9).

| Event | Level | Requires | Fields: name kind (table); class P0 unless marked | Export |
|---|---|---|---|---|
| `log.stream.opened` | info | — | `version` K4; `platform` K1 (Platform); `build` K1 (BuildProfile); `sink` K1 (Sink); `pid` K11 (P1) | no |
| `log.loss.counted` | warn | — | `sink` K1 (Sink); `counts` K8 (LossReason × Level, 40 entries); `sink_error` K1 (IoErrorKind), optional; `errno` K2 `Errno`, optional | no |
| `host.request.parsed` | info | — | `command` K1 (Command); `format` K1 (OutputFormat); `steps` K2 `Count` | cand. |
| `host.settings.resolved` | info | — | `concurrency` K2 `Count`; `cpus` K2 `Count`; `memory` K2 `Bytes`; `source` K1 (SettingSource) (OPP:249, OPP:277) | cand. |
| `host.phase.completed` | info | — | `phase` K1 (Phase); `wall` K2 `Elapsed`; `cpu` K2 `Elapsed`; `outcome` K1 (PhaseOutcome) (OPP:248) | cand. |
| `host.signal.received` | warn | — | `signal` K1 (Signal); `ordinal` K2 `Count`; `arrival_phase` K1 (CancelPhase: A–E, OPP §5.5) | cand. |
| `host.termination.decided` | info | — | `class` K1 (TerminationClass); `exit` K1 (ExitCode); `reason` K1 (D9Code), optional; `detail` K1 (DomainDetailCode), optional | cand. |
| `host.reuse.disclosed` | info | Plan | `stage` K1 (StageKind); `universe` K9 (P1); `state` K1 (ReuseState: `recomputed`); `cause` K1 (ReuseCause: `no-reuse-path`) (M3L:307-322) | no |
| `config.value.resolved` | debug | — | `key` K1 (ConfigKey); `layer` K1 (ConfigLayer); then exactly one of: `flag` K2 `Flag`, `number` K2 `Count`, `choice` K1 (ConfigEnumValue), `path` K12 (P2), or `present` K2 `Flag` for string and secret-classified values | no |
| `discovery.path.skipped` | debug | Project | `path` K12 (P2); `reason` K1 (SkipReason) | no |
| `snapshot.seal.completed` | info | Project | `snapshot` K9 (P1); `files` K2 `Count`; `bytes` K2 `Bytes`; `wall` K2 `Elapsed` | no |
| `provider.process.spawned` | info | P, P, E | `protocol` K1 (ProtocolMajor); `pid` K11 (P1) | no |
| `provider.process.ready` | info | P, P, E | `start` K2 `Elapsed`; `transfer` K2 `Elapsed` (M3L:400) | no |
| `provider.stage.changed` | debug | P, P, E | `stage` K1 (StageKind); `state` K1 (ProviderState) | no |
| `provider.stage.terminal` | info | P, P, E | `stage` K1 (StageKind); `terminal` K1 (StageTerminal, NE:2025); `reason` K1 (ProviderReason), optional; `fact_frames` K2 `Count`; `coverage_frames` K2 `Count`; `analysis` K2 `Elapsed` | cand. |
| `provider.process.reaped` | info | P, P, E | `pid` K11 (P1); `exit_class` K1 (ExitClass); `signal` K1 (Signal), optional; **`max_rss_native` K2 `Count`; `rss_unit` K1 (RssUnit: `kib`, `bytes`); `max_rss_bytes` K2 `Bytes`, optional**; `cpu` K2 `Elapsed`; `teardown` K2 `Elapsed` (M3L:402-406) | no |
| `provider.stderr.reduced` | info | P, P, E | `stderr` K7 | no |
| `provider.fault.reduced` | warn | P, P, E | `source` K1 (FaultSource: `control-fault`, `control-refusal`, `rust-provider-fault`); `fault_kind` K1 (RustFaultKind), optional; `refusal_family` K1 (RefusalFamily), optional; `detail` K7; `detail_code` K3 (RustDetailCode), optional | cand. |
| `provider.resources.reported` | debug | P, P, E | `resident` K2 `Bytes`, asserted; `cpu` K2 `Elapsed`, asserted; `handles` K2 `Count`, asserted | no |
| `supervision.liveness.missed` | warn | P, P, E | `window` K2 `Elapsed` | cand. |
| `supervision.progress.absent` | info | P, P, E | `stage` K1 (StageKind); `since` K2 `Elapsed` (OPP:238) | no |
| `supervision.limit.breached` | warn | P, P, E | `limit` K1 (LimitKind); `observed` K2 `Count`; `unit` K1 (LimitUnit) | cand. |
| `supervision.cancel.sent` | info | P, P, E | `inband` K2 `Flag`; `control_reason` K1 (ControlCancelReason, CC:37) (M3L:444-448) | no |
| `supervision.cancel.forced` | warn | P, P, E | `trigger` K1 (ForceTrigger: `second-signal`, `grace-expired`); `grace` K2 `Elapsed` (M3L:458) | no |
| `supervision.wait.expired` | warn | P, P, E | `wait` K1 (BoundedWait); `limit` K2 `Elapsed` (M3L:457) | no |
| `storage.commit.published` | info | Project, Plan, Execution, **Run** | `latched` K2 `Flag`. Owner-built from `PublishedCommit`. | cand. |
| `storage.commit.not_published` | info | Project, Plan, Execution | `outcome` K1 (CommitNotPublished: `undetermined`, `refused`); `termination` K1 (TerminationCode), optional. Owner-built from `CommitUndetermined` or `Refused` (`commit.rs:66-75`). | cand. |

"P, P, E" is Project, Plan, Execution. There are 27 events. The largest bound is `log.loss.counted`'s 1,905 B; every event is within 4,096 B (item 14).

**What each measured field means (r2, SOP2-R1-07).**
- **Elapsed fields.** All are monotonic nanoseconds:
  - `wall`: from the span's start event to its end event;
  - `start`, `transfer`, `analysis` and `teardown`: M3L:400-402's boundaries;
  - `window`, `since`, `grace` and `limit`: the configured window or the elapsed time since the last admitted transition.
- **CPU.** `cpu` in `host.phase.completed` is this process's user plus system CPU delta over the phase (`getrusage(RUSAGE_SELF)`). In `provider.process.reaped` it is the reaped child's user plus system CPU from `wait4`.
- **RSS.** `max_rss_native` is the raw `wait4` `ru_maxrss`, in the platform's native unit, which `rss_unit` labels: `kib` on Linux, `bytes` on macOS (Q0:889). It covers the child and the descendants it reaped. It is M3-L's `hostReapedMaxRss` (M3L:405) and is information only (AQP:343). `max_rss_bytes` is its checked conversion to bytes, absent on overflow. It is never a relabelling of the raw value. A new platform adds an `rss_unit` member.
- **`provider.resources.reported`.** Its values are `resourceReport`'s provider-asserted `residentBytes` (bytes), `cpuNanoseconds` (ns) and `openHandles` (count) (CC:35).
- **Other sizes.** `memory` in `host.settings.resolved` is the host's observed physical memory in bytes. `bytes` in `snapshot.seal.completed` is the total of the sealed files.

- **Covered.** Every row of M3L:412-419 and the provider-boundary record (M3L:396-409). The operational record (OPP:249) is composed of these events; its harness projection is Q0's.
- **Cross-law note.** M3L:286 gives S-M figure SM-10 ("Per-process `ru_maxrss`") the unit "bytes". M3-L's next revision should say either "native unit, labelled" or "converted to bytes", to match M3L:405 and Q0:889.

### H. Recording

**24. Recording on acceptance (LD; r2, SOP2-R1-NB-05).**
- **Decision.** The accepted PROPOSAL is the successor text. When M3-O's first code unit lands, the lead records a verify_design successor (`successor.json` plus a subject manifest that pins this accepted PROPOSAL's bytes, the EC1 form). It makes two **insertion-only** passage overrides:
  - **SDK4 `/standardizedFamilies/1/rule`.** Append: " For host operational records, the only records are events of the S-OP-2 registry whose fields are S-OP-2 SafeField kinds, and free text reaches no operational sink; the doctor report keeps its DR-114 redaction tiers (contract successor S-OP-2)."
  - **DRC line 576.**
    - Before: "meaning. The SDK owns framing,".
    - After: "meaning. The host reduces that channel to its byte count and truncation flag before any operational sink (contract successor S-OP-2). The SDK owns framing,".

    The original punctuation is preserved.

  F02:193-197 is not overridden. DRC §8 is already its preview successor (OPP:82), and F02 is D-372-pinned.
- **Review.** That recording unit gets its own review: `ACCEPT-DESIGN-UNIT` with a single-string `subjectManifestSha256`. The review checks the selectors, the parents and the DR-114 report split.
- **Rejected:** recording now, because no product unit is due before M3-O.

## Controls

The controls are authored at M3 under S-OP-11 and qualified at M6 (OPP:424). They refine OPP:428-437. Each must fail for its intended reason, not because of an unrelated compile error.

| # | Control | Proves |
|---|---|---|
| C-1 | **Compile-fail suite.** Rustdoc `compile_fail` tests with the expected error codes, or a UI harness if M3-O admits one. Each must fail to compile:<br>- a field typed `String`, `&str`, `Cow<str>`, `PathBuf`, `OsString`, `Vec<u8>`, `io::Error`, `&dyn Error`, `fmt::Arguments` or `serde_json::Value`;<br>- **a code table member written `include_str!(…)`, `env!(…)` or `concat!(…)`;**<br>- **a `CodeEnum` impl outside the registry module (unregistered);**<br>- **a generic `impl<T> CodeEnum for W<T>` adapter;**<br>- a `TableRegistration` built outside the module;<br>- `Correlation` from text;<br>- `IdentityDigest` from bytes or a parsed value;<br>- `ProjectPath` from `&str`;<br>- `SecretValue` as a field;<br>- an `Execution`-requiring event at a scope from before admission;<br>- a RunId from a candidate;<br>- a scope or marker impl outside its owner;<br>- **`storage.commit.published` without `PublishedCommit`, or `not_published` through a Run-bearing scope;**<br>- **a 33-character field key;**<br>- a template over 160 B or with a non-ASCII byte;<br>- an event whose 768 + Σ(36 + V) exceeds 4,096;<br>- 33 fields;<br>- depth 3;<br>- an `Event` impl outside `registry!`. | 3, 5, 8, 9, 14, 20 |
| C-2 | **Registry integrity.**<br>- Names follow the grammar and are unique; domains are listed; retired names are not reused, and **every retired name has a complete descriptor or is marked pruned**.<br>- Every field is K1–K15.<br>- **Every code table has a listed provenance. `registry-literal` members are literal tokens. `generated-contract` tables come from pinned generation outputs. `protocol-enum` members equal their schema's enum. A source scan finds no `include_str!`, `include_bytes!`, `env!`, `option_env!` or `OUT_DIR` in the registry or the registered generated modules.**<br>- Code members are never removed.<br>- **The documented per-event maximum equals the computed 768 + Σ(36 + V).**<br>- The renderings equal the committed files.<br>- The constructor and mint list equals the audited exception list. | 2, 3, 8, 14 |
| C-3 | **Foreign events.** A dependency emits `tracing` and `log` events carrying canaries, with **field visitors and formatters instrumented**. No visitor or formatter runs, no sink receives a byte, and no logger is installed. | 10 |
| C-4 | **Canary privacy** (OPP:428).<br>- **Canaries:** random high-entropy, low-entropy passphrase, unknown formats, Unicode, bidi and ANSI/C0, and 10× each bound, plus source snippets.<br>- **Injected into:** TS and Rust stderr, `fault` detail, `refusal` detail, `detailCode`, nonces, `clientCorrelationId`, configuration strings, declared and undeclared environment values, file and directory names (**including `password=CANARY`**), absolute paths with a canary username, I/O error text, panic payloads and nested configuration.<br>- **Sinks checked:** file, stderr at every level, ring and crash file, bundle with and without P2 consent, captured OTLP, `diagnostics`, and the pre-scope flush.<br>- **Poisoned persisted files fed to the bundle reader:** a known event with text in a P0 code field, extra fields, malformed values, an oversize line, a torn last line, a retired name with and without a descriptor, an older schema missing newer fields, and a header with a non-identity `requestId`.<br>- **Pass rule:** canary bytes appear only as P2 names in P2-permitted sinks. Poisoned values are dropped and counted, never re-emitted. Each canary's SHA-256 (hex and base64) and 12-hex prefix appear nowhere. | 4–7, 12, 13, 13a |
| C-5 | **Rule E.** In both encodings and in every string-bearing kind (K12, K14, K15, plus a K5/K6 attempt), each of these is escaped exactly as rule E says:<br>- U+0000–U+001F, ESC sequences, U+007F, U+0080–U+009F;<br>- **U+061C, U+200E, U+200F**, U+202A–U+202E, U+2066–U+2069;<br>- **U+2028, U+2029**;<br>- `"` and `\`.<br>Every record is exactly one line. A value made entirely of escaped code points elides on encoded bytes within V, at a code-point boundary. Non-UTF-8 names are refused as K12. `PathRef` tags differ across processes for one path and never equal its SHA-256. | 6, 13, 13b |
| C-6 | **Guard.**<br>- Zero defects over the C-4 corpus.<br>- **`password=CANARY` file names are reported as `p2-name-match`, never as defects.**<br>- Escaping is never counted as a firing.<br>- Unit tests run the guard on synthetic bytes, separately from the construction checks. | 11 |
| C-7 | **Bounds, gate and termination wait** (OPP:431).<br>- **Floods:** stderr at 10× its bound; a single-name storm; saturation with the writer blocked on a FIFO. Producers never wait, and counts are right by reason, level and owner.<br>- **Headroom:** `error` is admitted after `debug` fills the queue.<br>- **Pre-scope:** overflow is counted.<br>- **Sink failures:** EACCES, ENOSPC, EIO and **short writes**.<br>- **Gate pause:** a test hook pauses the writer **between a successful gate load and its syscall**. The gate closes during the pause. The admitted unit completes; its continuation, the next unit and the marker are not admitted; the remainder counts `sink-stopped`; the reader drops the torn line.<br>- **Termination wait:** with a **permanently blocked write**, the command completes, and its exit code and output are produced within 200 ms (normal) or 100 ms (cancellation). The writer is not joined, and the summary counts `drain-abandoned`.<br>- **Marker:** its outcome is observed as `written`, `failed`, `suppressed` (gate closed) or `skipped` (expired or blocked), never assumed.<br>- **`refused`** stays zero.<br>- **Boundaries:** a 32-byte key, a maximally escaped K12, every counter at `u64::MAX` in K8, and a full header with every identity, the longest component, phase and event. Each line is at most its computed bound and at most 4,096 B. | 14–17 |
| C-8 | **Run-time identities** (OPP:429). Each phase carries exactly its lawful headers, including:<br>- `storage.commit.published` with the Run and `not_published` without it;<br>- a stored-Run read carrying the Run;<br>- an ephemeral analysis carrying no Run;<br>- allocation failure emitting only the fixed line. | 9 |
| C-9 | **Code locations.** A release build emits no absolute path, `.cargo` path, `crates/../…`, `crates/./…` or other non-workspace origin. Dependency locations encode as `external`. | 5 (K6) |
| C-10 | **Environment.** With the declared resolver input held fixed, setting `RUST_LOG`, `RUST_BACKTRACE`, `RUST_LIB_BACKTRACE` and `OTEL_*` changes no sink's content, **and no effective filter, sink set or bound**. | 21 |
| C-11 | **Invariance** (OPP:437). Deterministic results (not counters or timestamps) are identical:<br>- with logging off and on, at every level;<br>- under sink failure, logging-initialization failure and saturation;<br>- at concurrency 1 and automatic. | all |
| C-12 | **Provider dispositions.** Fake TS2 and Rust3 providers exercise every item 22 row:<br>- registered and unregistered `detailCode`;<br>- health, nonces and refusals;<br>- asserted resources, which never become progress;<br>- **`max_rss_native` with `rss_unit` `kib` (Linux) and `bytes` (macOS)**, and the `max_rss_bytes` conversion, including overflow.<br>It also feeds poisoned persisted provider records to the bundle reader. | 13a, 22, 23 |

## Rejected alternatives

The rejected alternatives are recorded with the items that reject them. The principal ones:
- **Sink-side redaction as the guarantee** (DC4:1023-1025; OP-R1-03; item 11).
- **An open, const-only `CodeEnum`** (item 3).
- **Run-time privacy tags, or validated safe strings** (item 8).
- **Free-form `tracing` fields behind a deny-list** (item 10).
- **Serializable arbitrary event structs, or per-crate registries** (item 1).
- **A JSON registry with code generation** (item 3).
- **Unkeyed path hashes, or a persistent path key** (item 6).
- **Value-inspecting projection, or whole-event refusal per sink** (item 12).
- **Name-only re-admission, and name-only retirement** (items 2, 13a).
- **Stripping, or JSON-standard escaping only** (item 13b).
- **A writer-side drain deadline** (item 16).
- **A run-time commit-outcome pairing** (item 9).
- **Evicting queued records** (item 15).
- **A closed `detailCode` set now** (item 22).
- **Recording overrides before M3-O** (item 24).

## Forbidden substitutes

- Any field, header or message containing:
  - text produced by `Debug`, `Display`, `format!` or `to_string`;
  - an error object or its message;
  - a panic payload or a backtrace;
  - provider stderr, `fault` or `refusal` detail, or a nonce;
  - `clientCorrelationId`;
  - a configuration string value of no kind;
  - an environment value;
  - a secret value or its length.
- Any digest or fingerprint of P3 data; an unkeyed hash of a path; a source-file content digest.
- An unregistered code table. A table member from `include_str!`, `include_bytes!`, `env!`, `option_env!`, `concat!` or build output. A generic `CodeEnum` adapter. A `CodeEnum` or `TableRegistration` outside the registry module.
- A P3 class, a "restricted" class, or any escape that admits free text into a record.
- A `SafeField` impl or kind constructor outside the vocabulary module. A P1 or P2 constructor that takes text, bytes or a parsed value. A forgeable scope or marker.
- A run-time event name, an event outside the registry, a second registry, a reused retired name, or a retired name kept without its descriptor.
- A reader that re-emits a persisted record without item 13a's re-admission, passes raw serialized values through, or trusts a record's class claims.
- Sink projection by value inspection.
- Escaping that differs between the two encodings, or that omits any rule E code point.
- A producer that blocks on the queue or on writer I/O.
- A syscall admitted after a load observed `closed`. A short-write retry or a marker without its own gate load.
- A termination path that waits on a sink syscall, joins a blocked writer, or exceeds its wait budget for optional logging. A logging sink holding a lock that the output or termination path takes.
- A loss marker that is enqueued, retried, assumed written, or counted itself. A cap hit emitted through the saturated path.
- Native `ru_maxrss` labelled as bytes on a platform whose native unit is not bytes.
- Level, sink or export settings read from the environment.
- RequestId, a path or a rule id exported before S-OP-10 admits it. Any export before O4.
- A provider that writes logs, receives a log path or emits registry events. Host-side parsing of stderr.
- A record field entering any identity, digest, Plan, Coverage, verdict or exit (OPV10:79; OPP:203).
- `cfg(debug_assertions)` free-text logging.

## What this does not decide

- **S-OP-1, log storage and custody:**
  - which capability creates, opens, rotates and prunes files;
  - the layout (OPP:221);
  - retention and the stop rule (OPP:204-206);
  - the log-directory lock;
  - doctor's read rules;
  - tamper evidence for log files.

  S-OP-2 supplies only the gate and its accounting.
- **S-OP-5:** the `operability` configuration section (OPP:226).
- **S-OP-6:** the switch grammar, the human `request` line, the wording of the loss summary, and which identities human stderr prints.
- **S-OP-7:**
  - the panic hook, descriptor admission and the crash file;
  - the nonblocking stderr path;
  - suppression after a latched or uncertain operation, **including whether the one-unit residual of item 17 is acceptable**, with the X3D owner;
  - the ring's read path.
- **S-OP-9:** bundle custody, the **per-member P2 consent** flow (OPP:356) and member limits. Item 13a binds its reader.
- **Also not decided:** S-OP-3; S-OP-10 and O4; S-OP-12; O7; O9; the choice of `tracing`; crate placement; a multi-request host scope (M5).

## Open questions

- **R3. S-OP-9 and O5.** The P2 consent granularity. r2 keeps OPP:356's per-member rule; the UI is S-OP-9's.
- **R4. S-OP-10 and O4.** Are item 23's export candidates the right ones?
- **R6. S-OP-7.** Is the ring's `info` level right?
- **R7. The lead.** Item 24's recording timing.
- **R8. S-OP-7 and the X3D owner.** Is item 17's residual acceptable after an uncertain or latched outcome: at most one admitted unit of ≤ 64 KiB per sink writer, issued after closure? Or is a coordinated issuance mechanism required?
- **R9. The lead (M3-L).** The SM-10 unit label at M3L:286 (item 23's cross-law note).

Codex settled R1, R2 and R5 in its r1 review: the DR-125 reading stands, the DC4 split stands, and `RuleId` stays P2.

## Citations checked

Every citation was opened and read on 2026-10-04. New or changed in r2:
- **Q0:889.** `wait4` `ru_maxrss` "KiB on Linux, bytes on macOS", labelled `hostReapedMaxRss`. M3L:405 has the same label, and M3L:286 is the SM-10 row.
- **`common-v4.schema.json`.** The identity patterns behind item 14's header lengths: RequestId 37, ProjectId 69, ExecutionId 38, PlanId 70, RunId 69, SnapshotId 74 and ClosureId 73 characters.
- **`crates/storage/src/commit.rs:66-75`.** `CommitOutcome { Committed(PublishedCommit), CommitUndetermined { execution_id }, Refused(T) }`.
- **UCD `PropList.txt` `Bidi_Control`.** 061C, 200E..200F, 202A..202E and 2066..2069.
- **r1 citations still hold.** The secret rule is F03:45-50, not 44-50. APP:620-630 is the D.SDK selector of DRC §8 (DRC:513-601). APP:3860-3865 is the DR-125 row and its SDK4 pin.
- **Product facts** were read at `3d2d5b5`.

## Not claimed

- **Measurements.** Nothing is measured. All bounds, budgets and deadlines are provisional, except the cited constants and the computed encoding bounds.
- **Edits.** No contract, schema, gate, threshold, register row or pinned file is changed, and item 24's overrides are proposals.
- **Confinement.** Not claimed. The vocabulary prevents free text and fingerprints from reaching OpenSIP's sinks. It does not prevent a first-party provider from deliberately signalling through its choice of codes, counts or timings. G21 "does not claim security confinement" (QG:429); confinement is O7.
- **Provenance of read-back values.** A party that can write the log directory can place valid encodings (item 13a).
- **No retroactive suppression.** A unit admitted before a gate closes may be issued and complete after it (item 17).
- **The kernel's wait.** The bound is on the command's wait (item 16), not on the kernel. A stalled kernel write can delay process teardown.
- **Bytes outside OpenSIP's sinks** (DC4:1081).
- **Implementation.** No product code, cargo command or test was run for this revision. M3-L is cited as a draft. If its accepted text changes items 12–14, item 22's table and item 23's provider rows follow by ordinary registration, unless a kind or class must change.
