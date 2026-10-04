# The safe event vocabulary and sink law — contract-successor proposal S-OP-2 r1

**DRAFT r1, not accepted.** This is a contract-successor proposal. The verdict it seeks is ACCEPT-DESIGN-UNIT.

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. It is successor **S-OP-2** of the accepted operability plan. That plan's §9 row reads: "Registry, `SafeField` set, privacy classes, per-sink allowlists, §3.3 bounds and loss marker", owned by the "DR-125 owners: Component architecture + CLI/operability/security" (OPP:408; REG:314). It is written under:
- OPP §3.1–§3.6, §5.3, §6, §7 and §10 (r3, accepted);
- the draft law M3-L, items 12–14, which name what that law needs from S-OP-2 (M3L:345-425);
- the accepted contracts listed under "Joins" (items 18–22).

## Standing

- **What it succeeds.** Accepted text names the host's diagnostic behaviour but does not define it:
  - DR-125's standardized family SF-2: "Bounded structured diagnostics only. No unstructured host logs. Redaction is host-owned." (SDK4:78-82). It carries F02:186 ("diagnostic taxonomy, redaction, bounds, structured logging/audit correlation") and F02:193-195 ("bounded structured diagnostics … must not … write unstructured host logs").
  - DRC §8, the D.SDK selection (APP:620-630): diagnostics "may use the existing bounded stderr channel and carry no protocol meaning" (DRC:574-576), and the SDK "never hide[s] dropped messages" (DRC:578-579).
  - The gates: DR-G20 requires "redaction/bounds/audit correlation … no direct UI/unstructured logs" (QG:408), and DR-G21 requires "bounded redacted diagnostics/audit" (QG:428).

  S-OP-2 gives these phrases their concrete meaning for the host: the event registry, the field kinds, the privacy classes, the sinks, the bounds and loss accounting.
- **What it changes.** No frozen or pinned text is edited, and no accepted sentence is narrowed. Item 24 gives the recording form.
- **What it joins without changing:**
  - DR-114's redaction contract (DC4:1005-1086);
  - the secret-value rule (F03:45-50, F03:56-59, F03:65-67);
  - the no-hidden-environment-input rule (CH13:59-62);
  - the S-OP-4 record join, which M3-L carries (M3L:345-371);
  - OPP §3.1's phase-lawful identities.
- **Its role as a gate:**
  - **Drafted.** This draft existing meets M3-L gate item G7, "S-OP-2 drafted" (M3P:160; M3L:24), on the lead's reading. Acceptance is separate.
  - **Accepted.** Acceptance gates M3-O's O1 part, whose dependency column reads "P0; S-OP-2" (M3P:174), and OPP §8's M3 row (OPP:381).
- **Decisions.** Items marked **(LD)** are lead decisions, dated 2026-10-04. They are made under the owner's standing direction to proceed on the lead's recommendation and to block only where there is none. Each names the alternative it rejects, and the owner may reverse any of them.
- **Numbers.** Every number is **provisional**, to be tuned by OPP §10's overhead and loss measurements, unless it is a cited protocol constant.

## Short names

Line numbers are those of the live files on 2026-10-04. Each was checked against the file; see "Citations checked".
- **OPP** `docs/implementation/m3/operability/PLAN.md` (r3, accepted; the live file carries a two-line acceptance note)
- **M3L** `docs/implementation/m3/provider-protocol-l/PROPOSAL.md` (r1, draft, not accepted)
- **M3P** `docs/implementation/m3/M3-PLAN.md` (r4, accepted)
- **REG** `docs/v2/architecture/08-decision-and-readiness-register.md`
- **APP** `docs/coop/completion/architecture-application.v1.json` (the D-369 application)
- **DRC** `docs/coop/completion/distribution-runtime-completion.v2.md` (sha256 `9ab2874e…`, the pin APP:626 carries)
- **SDK4** `docs/coop/artifacts/component-sdk-contract.v4.json` (sha256 `c53d541f…`). The DR-125 application row inherits it (APP:3860-3865). Its own header says `CANDIDATE-NOT-APPLIED` and `"binds": "NOTHING"` (SDK4:7-10). This proposal cites SF-2 as the text the D-369 application inherits, not as a self-standing grant.
- **DC4** `docs/coop/artifacts/doctor-contract.v4.json` (sha256 `df2e7175…`, pinned by APP:7573-7574)
- **F02 / F03 / CH13** `docs/v2/architecture/{02-distribution-and-components,03-configuration-and-security,13-evidence-workflows-and-product-contracts}.md`
- **CC** `docs/coop/completion/control-completion.contract.v5.md`
- **QG** `docs/coop/design-corrections/qualification-gates.applied.v1.json`
- **OPV10** `docs/coop/artifacts/operability.v10.json` (V1 candidate, historical; it informs and grants nothing)
- **DLV / RPP** `docs/coop/artifacts/{delivery.v2,rust-provider-protocol.v2}.json`
- **NE / WS / IE** `docs/v2/contracts/product-v1/{native-evidence,workflows-and-surfaces,identity-and-evidence}.md`
- **SLJ** `docs/coop/artifacts/sdk-leftover-join.v9.json` (the DR-125 prior measured join, APP:3866-3869)
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

So no implementation constrains this law.

**The threat** is OP-R1-03's. Compiler diagnostics, provider stderr, `fault` detail and I/O error text can carry source lines, identifiers and secrets in formats no pattern can recognise (DC4:1023, DC4:1078). A scrubber at the sink cannot undo bytes already queued, ringed, written or exported. The guarantee must therefore be a property of **how a record is constructed**, as DC4's GUARANTEE tier is a property of "the construction path" (DC4:1017). Scrubbing is only a backstop.

## Decisions

### A. The registry and the record model

**1. One host-owned registry; records exist only as registry events (LD).**
- **Decision.**
  - **One registry.** Every operational record the host writes to any sink is an instance of an event declared in **one registry**, a single declarative source file in the product. The M3-O unit chooses its crate. For each event, the registry declares:
    - its name (item 2);
    - its level, fixed at registration;
    - the identities it requires (item 9);
    - its typed fields, each of one `SafeField` kind (item 5);
    - a static message template;
    - whether it is a candidate for export (item 12).
  - **Record shape.** It follows OPP:161: `{ts, level, event, requestId, [projectId], [planId], [executionId], [runId], [component], [phase], fields, [omitted], [truncated]}`.
    - `ts` is UTC with millisecond precision.
    - `component` is a host-assigned slot: a closed role code plus an ordinal.
    - `phase` is a closed phase code.
    - `omitted` and `truncated` are counts, present only when nonzero (items 12 and 14).
  - **Encodings.** The file and bundle encoding is one JSON object per line, UTF-8. Every C0 and C1 control, DEL, U+2028 and U+2029 is escaped, so one record is always exactly one line. The human stderr encoding is in item 13.
- **Basis:** OPP:161, OPP:168, OPP:369; F02:193-195; SDK4:81.
- **Rejected:**
  - **Records as arbitrary serializable structs** (`derive(Serialize)` events). Any `String` field compiles.
  - **Per-crate registries.** There is no single list to audit or document.

**2. The naming rule: `domain.component.action` (LD).**
- **Decision.**
  - **Grammar.** A name is exactly three dot-separated segments. Each segment matches `[a-z][a-z0-9]*(_[a-z0-9]+)*` and is at most 32 bytes; the whole name is at most 96 bytes.
    - The **domain** comes from a closed list in the registry: `host`, `config`, `discovery`, `snapshot`, `plan`, `supervision`, `provider`, `evaluation`, `storage`, `delivery`, `doctor` and `log`. `crash`, `bundle` and `export` are reserved for S-OP-7, S-OP-9 and S-OP-10.
    - The **component** is the noun the event is about (`process`, `stage`, `stderr`, `queue`).
    - The **action** is a past-tense verb or an observed state (`spawned`, `reaped`, `missed`, `absent`, `reduced`, `counted`).
  - **Names are constants.** A name is never built at run time.
  - **Names are never reused.** Fields may be **added** to a registered event, but never removed or retyped. Any other change registers a new name and retires the old one. Retired names stay reserved, so a reader of old files is never misled.
  - **OPP's working names.** OPP uses three two-segment working names. They are registered as:

    | OPP working name | Registered name |
    |---|---|
    | `log.record_refused` (OPP:191) | the loss reason `refused`, a counter in `log.loss.counted` |
    | `log.loss` (OPP:202) | `log.loss.counted` |
    | `supervision.no_progress` (OPP:238; M3L:417) | `supervision.progress.absent` |

- **Rejected:**
  - **Free-form dotted names of any depth.** A third segment makes the component explicit, and it lets the generated documentation group events by component.
  - **Keeping OPP's two-segment names beside the three-segment ones.** That would leave two grammars.

**3. Registration, change control and generated documentation (LD).**
- **Ordinary registration.** A code unit may add an event or a field without a new successor if all of these hold:
  - it uses only existing kinds (item 5) and existing domains;
  - it obeys the naming rule;
  - it passes the static bounds (item 14);
  - it is reviewed in that code unit.

  Adding a domain, or a member to a `RegisteredCode` table (item 5, K3), is ordinary too, within K3's constraints.
- **Changes that need an S-OP-2 successor:**
  - a new `SafeField` kind;
  - a change of any kind's class;
  - a new privacy class;
  - a new sink, or a change to a sink's ceiling;
  - a change to item 12's projection rule;
  - export eligibility beyond item 12's candidates, which also needs S-OP-10.
- **Generated documentation.** The registry renders two artifacts, both committed in the product and drift-checked by a test that fails on any difference:
  - an event reference in Markdown: per domain, each event's name, level, required identities, fields with kinds and classes, sink projection, export candidacy and message template;
  - the same content as JSON, for S-OP-9's bundle builder and the S-OP-11 harness.

  The runbook (OPP:359) consumes them. This answers the predecessor's drift lesson F1 (OPP:129).
- **Rejected:**
  - **A JSON or TOML registry with a code generator.** It adds a generation source, and with it the product's generator-closure and inventory pins, for a Rust-only consumer. Providers never emit registry events (item 22).
  - **Attribute macros scattered across crates.** There is no single list.

### B. Privacy classes and the closed `SafeField` set

**4. Privacy classes P0–P3.** These definitions refine OPP:169. Each says what may determine the bits of a value.

| Class | Definition | Examples |
|---|---|---|
| **P0** release and measurement | Every bit is fixed by an OpenSIP release constant, a closed enumeration, an admitted signed or release catalog, or a count, size or duration the host measured. Nothing comes from project content, the user's account or provider free text. | D9 and DomainDetail codes, reason enums, counts, byte sizes, durations, versions, platform, admitted component or pack ids, the length of a reduced text |
| **P1** correlation | Opaque identifiers the host minted from a CSPRNG (RequestId, ExecutionId, ProjectId; WS:78-82; IE:42-43, IE:61-63), content-addressed identities over sealed structures (PlanId, SnapshotId, committed RunId, universe keys, closure ids), the process id, and the keyed ephemeral path tag (item 6). They reveal no name or content, but they link records. That linking is why export excludes them by default (OPP:180). | `req1_…`, `exec1_…`, `plan2` text, the universe-key suffix |
| **P2** project structure | Names and positions chosen by the project or an operator: project-relative paths, file and directory names, line and column, rule ids, and declared names (environment-variable names, future secret-handle names). Never content, but possibly sensitive in itself (DC4:1079). | `src/a/b.ts`, line 41, a rule id, `GITHUB_TOKEN` (the name, never the value) |
| **P3** content and free text | Source bytes; provider stderr; control `fault` and `refusal` detail; error and panic message text; caller free text; configuration string values of no P0–P2 kind; secret values; environment values; any digest or fingerprint of these (OPP:168; OP-R2-NB-01). | everything else |

**P3 has no `SafeField` kind, so nothing of P3 can be put in a record of any class.** That is the structural claim. The type system enforces it (item 8). The scrubber does not (item 11).

**5. The closed `SafeField` kinds.** This is the whole set. Each kind is sealed: only the vocabulary module defines kinds. Its lawful constructors are listed, and no kind has a constructor from `&str`, `String`, `[u8]`, `Path`, `OsStr`, `fmt::Arguments`, an error object or a deserializer.

| # | Kind | Class | Lawful constructors | Encoded bound | Why it cannot carry source or secrets |
|---|---|---|---|---|---|
| K1 | `Code<E>` | P0 | Any `E: CodeEnum`. The trait's text table is an **associated `const`**, and the only run-time part is an index into it. | longest table entry; ≤ 64 B, checked statically | Text comes only from compile-time constants in the binary, and an associated `const` cannot hold run-time data. Covers D9 codes, DomainDetail codes, I/O error kinds, phases, roles, signals, outcomes, reason enums (DLV:857; NE:2025), configuration keys and enum values from the closed PCS schema, and sink and loss-reason names. |
| K2 | `Count`, `Bytes`, `Elapsed`, `Flag`, `Errno` | P0 | Integers and booleans. `Elapsed` comes from the monotonic clock. `Errno` comes only from `raw_os_error()`. | fixed | A number. **Forbidden:** a number computed from a secret value. Secret types expose no length (item 20). |
| K3 | `RegisteredCode<T>` | P0 | Exact byte-match of external text against a host-owned **const** table `T`. On a match it encodes the table's own entry. Otherwise it yields `{unrecognized: Reduced}`. Members are ASCII `[a-z0-9-]`, at most 64 B each, and a table holds at most 256 entries. | ≤ 64 B | It never re-emits the input bytes. A non-member is reduced to its length. |
| K4 | `Version` | P0 | Release constants, or the version fields of admitted signed manifests | ≤ 64 B | Fixed by a release or a signed catalog. |
| K5 | `AdmittedId` | P0 | An entry of an admitted signed or release catalog: a component stable id, capability id, bundled pack id `name:version`, or platform id. Built from the catalog entry type, never from text. | ≤ 128 B | The value is a catalog member the host already verified. |
| K6 | `CodeLocation` | P0 | `&'static core::panic::Location` only. The file is emitted only if it is workspace-relative (`apps/`, `crates/`, `providers/`). Otherwise the field is `external` plus the line. | ≤ 160 B | It names OpenSIP's own code. Dependency paths under the build machine's home (absolute; product has no path remapping) are never emitted (C-9). |
| K7 | `Reduced` | P0 | `Reduced::of(text, captured_truncated)` **consumes** any bytes and keeps only `{bytes, truncated}`. `bytes` is the total observed, saturating. `truncated` is set when the capture hit its bound. | fixed | The text is dropped in the constructor. **No digest is kept** (OPP:171; OP-R2-NB-01). |
| K8 | `Counts<E>` | P0 | One `u64` per variant of a closed `CodeEnum`. Reserved for the loss marker. | 24 B × variants, checked statically | Counts indexed by compile-time names. Depth 2. |
| K9 | `IdentityDigest<K>` | P1 | Only from the typed identity value of kind `K`: SnapshotId, universe key (the 64-hex suffix, NE:3160-3164), closure id, or the manifest digest of a signed artifact. **Never from bytes, a hasher or text.** | ≤ 80 B | A content-addressed identity over a sealed structure, not a file-content digest. A raw SHA-256 of a source file is not constructible, because it is an oracle for guessed content (OP-R2-NB-01). |
| K10 | `PathRef` | P1 | `{anchor: Code<PathAnchor>, tag}` (item 6). Built from a path held as a typed handle. | 32 B | It contains no path bytes and no unkeyed digest. |
| K11 | `ProcessId` | P1 | The host's own pid, or the pid of a process the host spawned | fixed | A number. |
| K12 | `ProjectPath` | P2 | Only from the host's admitted project-relative path types: discovery and snapshot entries, and admitted fact anchors. Never from a string, even a well-formed one. | ≤ 256 B, tail-preserving elision + `truncated` | It is a name that exists in the project tree, so it may be sensitive (DC4:1079). That is why it is P2. It carries no file content. |
| K13 | `Position` | P2 | Line and optional column from admitted spans | fixed | Numbers. P2 because, joined to a path, they locate content (OPP:169). |
| K14 | `RuleId` | P2 | Entries of the admitted policy catalog | ≤ 128 B | A catalog name. P2 follows OPP:169, because policy may be project-authored (open question R5). |
| K15 | `DeclaredName` | P2 | Names validated against a declaration: environment-variable names a manifest declares (DC4:1035), and secret-handle names once DR-108 lands (item 20) | ≤ 128 B | A name only, never a value. P2 because an operator chose it (DC4:1079). |

`Correlation<K>` (RequestId, ProjectId, PlanId, ExecutionId, RunId) is **header-only** and P1. Records get it only from the emitting scope (item 9), never as a field the caller supplies.

**6. Paths: project-relative, or an anchored placeholder with a keyed ephemeral tag (LD).**
- **Decision.** A path appears in a record in exactly one of two forms:
  - **`ProjectPath`** (P2), when the host holds it as an admitted project-relative path.
  - **`PathRef`** (P1) otherwise:
    - **The anchor** is a closed code: `installation`, `store`, `log-root`, `scratch`, `project` (when the path is not admitted), `system-temp` or `external`.
    - **The tag** is the first 64 bits of HMAC-SHA-256(*k*, the path's native bytes). *k* is a 256-bit key drawn from the platform CSPRNG when logging starts. It is held in memory, never written, never derived from an identity, and different in every process.

  So two records of one process can be seen to name the same path, but a reader without *k* can test no guess. The same path gets different tags in different processes.
- **Never present:** absolute paths, home directories, user or host names (DC4:1038-1043).
- **Basis:** DC4:1039 ("a non-identifying marker otherwise"); DC4:1043; DC4:1071 ("not a truncated hash presented as an identity"); OPP:168.
- **Rejected:**
  - **An unkeyed hash of the absolute path** (the "placeholder plus hash" read literally). A home directory and username are low-entropy, so the hash is an oracle for them.
  - **A persistent per-installation key.** Cross-process correlation would need the key's custody beside the logs (S-OP-1), and then the key and the logs leak together.
  - **Anchor plus a relative path under OpenSIP-owned roots.** Store object paths are content digests, and some are digests of source blobs.

**7. What is never a field.** These have no kind, so no record can carry them:
- free text of any origin: provider stderr; `fault` detail (CC:36); `refusal` detail (CC:32); the health or ping nonce (CC:33, CC:53); I/O and library error messages; panic payloads; `Debug` or `Display` output;
- caller text: `clientCorrelationId` (`command-envelope-v7.schema.json:38-42`; OPV10:191 "untrusted display/audit metadata"). Its presence may be a K2 `Flag`;
- configuration string values that are not of a P0–P2 kind;
- secret values and environment-variable values;
- backtraces;
- digests of P3 data;
- DomainDetail `remedy` and `subject` strings (`common-v4.schema.json:641-686`). The detail **code** is K1, and the remedy text is derivable from it.

### C. Enforcement at construction

**8. Type-level closure (LD).** A free-text value must not compile into an event of any class. The reference design follows; its names are illustrative and M3-O chooses the final ones.

```rust
mod sealed { pub trait Sealed {} }
#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum PrivacyClass { P0, P1, P2 }                  // no P3 variant exists

pub trait SafeField: sealed::Sealed {                 // implemented only for K1..K15
    const CLASS: PrivacyClass;
    const MAX_ENCODED: usize;                         // static per-kind bound
    fn encode(&self, form: SinkForm, out: &mut FieldOut<'_>);
}
pub trait CodeEnum: Copy {                            // open: any crate may define codes
    const TEXT: &'static [&'static str];              // compile-time table only
    fn index(self) -> usize;                          // the only run-time part
}
pub trait Event: sealed::Sealed {                     // implemented only by registry!{}
    const NAME: &'static str;
    const LEVEL: Level;
    type Requires: IdentitySet;                       // item 9
    const FIELD_CLASSES: &'static [PrivacyClass];
    const MAX_ENCODED: usize;                         // header reserve + Σ field bounds
}

registry! {
    provider.process.spawned: info, requires(Plan, Execution), export(no),
        "provider process started" {
        role: Code<ProviderRole>, universe: IdentityDigest<Universe>, pid: ProcessId,
    }
}
// Per entry the macro emits a struct with exactly these typed fields, its Event impl, and
// const _: () = assert!(Self::MAX_ENCODED <= RECORD_BOUND && Self::FIELDS <= 32);
```

What this gives:
- **`SafeField` is sealed and has no impl for any text, byte, path, error or formatting type.** `ProviderProcessSpawned { role: "…".to_string(), … }` is a type error (E0308/E0277). Sealing stops another crate adding an impl.
- **`Code<E>` takes any `CodeEnum`, but the text is an associated `const`.** Constants are evaluated at compile time, so an implementor cannot return run-time text. Even `Box::leak` of a run-time `String` cannot occupy a `const`.
- **Constructor provenance** decides what the P1 and P2 kinds can hold. Each such kind is built only in one of two ways:
  - (a) a `From` impl from the owning typed value (an admitted path, a typed identity);
  - (b) a mint capability that the vocabulary issues once at initialization to the owning module. The `RequestId` mint goes to `RequestAuthority` (`crates/host/src/request.rs:15-55`).

  Neither takes text or bytes. The constructor list belongs to OPP §7's audited exception list, and a structural check refuses any new constructor (C-2).
- **Static class and bounds.** Each event's field classes and maximum encoded size are compile-time constants, so the record bound (item 14) is a compile error, not a run-time refusal.
- **No debug-build escape hatch.** Development and harness builds, including their stderr sink before S-OP-6 (OPP:228), use the same vocabulary. `cfg(debug_assertions)` free-text logging is forbidden.
- **Secret stand-in.** Until DR-108, a test-only `SecretValue` type stands in for any future secret type. C-1 shows it cannot be a field (item 20).
- **Basis:** OPP:168 ("A non-safe value fails to compile"); OPP:170; OPP:369; DC4:1017.
- **Rejected:**
  - **Run-time privacy tags on string values.** The class would be a caller's assertion: free text tagged P0 would pass.
  - **A validated "safe string"** (for example `[A-Za-z0-9_./-]{0,256}`). It is a shape check, not provenance. Identifiers, tokens and many secrets match it.
  - **A `#[allow]`-style `unsafe_text()` escape.**

**9. Phase-lawful identities, enforced by scope types (OPP §3.1).**
- **Decision.**
  - **Emission needs a scope.** Records are emitted only through a scope value. Each scope type implements one marker trait per identity it lawfully holds: `HasProject`, `HasPlan`, `HasExecution` and `HasRun`. Every scope holds a RequestId.
  - **Who creates scopes.** Only the transition that mints the identity creates the scope:
    - project admission;
    - Plan sealing;
    - attempt admission (IE:61-63);
    - a `Committed` publish, or a stored-Run read.
  - **Requirements are checked at compile time.** `emit::<E>` is bounded by `E::Requires`. An event that needs `HasExecution` therefore cannot compile at a scope from before admission.
  - **Headers.** Header identities are filled from the scope, never from fields.
  - **What the rules give:**
    - **The ExecutionId outlives an undetermined commit.** It stays available for CommitUndetermined, because the attempt scope outlives the commit outcome (X3D:130-132 via OPP:156).
    - **No candidate RunId.** No RunId constructor takes a candidate, so a candidate RunId is never stringified (OPP:157-159).
  - **The emergency case.** If `RequestAuthority::begin` fails there is no scope, so no record can be built. The fixed line `HOST.IO_FAILURE: request identity allocation failed.` stays the only output (`bootstrap.rs:15-23`; OPP:160).
- **Not decided here.** A process-level scope for a host that serves several requests is M5's (AQP INC-6). M3 processes serve one request.
- **Rejected:** a run-time check of phase against the header. It catches the error only on the paths tests execute.

**10. Foreign events and the framework (LD).**
- **Decision.** S-OP-2 does not require `tracing`. OPP:147 leaves the framework "unchosen by law". Whatever transport M3-O picks must keep four rules:
  - **(a)** every record is built from a registry event;
  - **(b)** a callsite not in the registry, including any dependency's `tracing` or `log` event, never reaches a sink and never has its fields visited or formatted. With `tracing`, its subscriber returns `Interest::never()` for every callsite outside the registry's set.
  - **(c)** no `log` logger is installed;
  - **(d)** spans are registry entries too, named by the closed phase code.
- **Rejected:** a deny-list layer over free-form `tracing` fields. It formats `?`/`%` values before deciding.

**11. The final guard at every sink.**
- **Decision.** One scrubber runs at every sink, as OPP:182 requires:
  - ANSI first, then C0 controls (DC4:1062-1063);
  - a length bound with a marker (DC4:1066-1067);
  - known credential shapes.

  It is DISCLOSURE-tier (DC4:1020-1025). Because no record contains free text, **the guard is a tripwire**:
  - every firing increments a counter;
  - the M3 privacy corpus requires zero firings (C-6);
  - a firing in qualification is a vocabulary defect, never an accepted redaction.
- **Basis:** OPP:182; DC4:1012-1028.

### D. Sinks

**12. Per-sink allowlists, enforced by static projection (LD).**

| Sink | Owner of the sink itself | Classes it may carry | Notes |
|---|---|---|---|
| stderr, human | S-OP-6 (switches); this law (content) | P0, P1, P2 | Off unless asked (OPP:162, OPP:228). Rendering in item 13. |
| file | S-OP-1 | P0, P1, P2 | No file before S-OP-1 (OPP:211). |
| pre-scope buffer | this law | P0, P1, P2 | Memory only. Flushed only into the file sink (item 16). |
| crash ring | S-OP-7 (read path, crash file) | P0, P1 | Plus the event name and phase (OPP:178). |
| support bundle | S-OP-9 | P0, P1 by default; P2 only with that bundle's explicit consent | Re-projected by the registry (item 13). |
| OTLP export | S-OP-10, owner decision O4 | P0 only, plus an export-local trace id | Only events marked export-candidate, and only once S-OP-10 admits them (OPP:180, OPP:256). |
| envelope `diagnostics` | S-OP-6 | P0 only, the loss summary | An existing carrier (`command-envelope-v7.schema.json:143-150`). Not a log sink. |
| P3 | — | **no sink** | No kind exists. |

- **Projection.** Every event may reach every sink except OTLP; OTLP is opt-in per event (item 23). Each sink has a constant class ceiling. Its encoder writes a field only if that field's **static** class is at or below the ceiling. It counts the fields it left out in the record's `omitted` header. The decision reads compile-time data only, never the value.
- **Rejected:**
  - **Refusing at compile time to route any event with a P2 field to the ring or the bundle.** Ring records would then lose whole events where losing one field would do.
  - **Projection by inspecting values.** That is content classification, the DISCLOSURE tier.

**13. Sink-specific rules.**
- **stderr, human.** One line per record: `<level> <event>: <message> key=value…`.
  - The message is the registry's static template.
  - Values use each kind's human form.
  - `ProjectPath` escapes C0, DEL, C1 and bidirectional controls (U+202A–U+202E, U+2066–U+2069) as `\u{…}`. A hostile file name cannot inject terminal sequences or reorder text, and it stays visible rather than being silently stripped.

  Which identities to print, colour and verbosity are S-OP-6's. The three fixed bootstrap lines stay outside the vocabulary, as output of the termination owner on OPP §7's audited exception list.
- **File.** JSON Lines (item 1). The first record of each stream is `log.stream.opened`. S-OP-1 owns layout, custody, rotation, retention and the stop rule (OPP:204-206).
- **Crash ring.** Every emitted record at or above the ring's level is also projected to P0–P1 and copied into the preallocated ring (item 16). The ring's provisional level is `info`, the same as the file default. S-OP-7 owns the hook, the crash file and suppression after a latched or uncertain operation (OPP:302-313). The hook never reads a panic payload (OPP:183, OPP:307).
- **Support bundle.** S-OP-9 re-projects each record **using the registry of the running build, never the record's own claims**:
  - fields are classed by event name;
  - records whose name is neither registered nor retired are dropped;
  - P2 fields are included only with that bundle's consent.

  The bundle lists member classes before writing (OPP:356). The parser that reads records back for this is not a `SafeField` type.
- **OTLP.** The event name, P0 fields, and a trace id drawn at random for each export session. No RequestId, path or rule id unless S-OP-10 admits one (OPP:180, OPP:256).
- **Envelope `diagnostics`.** It carries only the loss summary of item 17, as P0 counts. S-OP-6 owns its wording and placement in the existing `BoundedText` carrier (≤ 1,024 characters, ≤ 256 entries; `common-v4.schema.json:132-135`).

### E. Bounds (OPP §3.3)

**14. Record, field and depth limits are static (LD).**

| Bound | Provisional value | Where it is enforced |
|---|---|---|
| field, string-bearing kinds (K5, K6, K12, K14, K15) | ≤ 256 B encoded (OPP:191). K12 elides from the front, keeps the tail, and sets `truncated`. | each kind's encoder; the constant `MAX_ENCODED` |
| fields per record | ≤ 32 (OPP:191) | `registry!` static assertion |
| depth | ≤ 2 (OPP:191). Every kind is flat except `Reduced`, `PathRef` and `Counts`, each of depth 2 | the closed kind set |
| encoded record | ≤ 4 KiB (OPP:191), of which 768 B is reserved for the header | `registry!` static assertion on `Σ MAX_ENCODED` |
| message template | ≤ 160 B ASCII | `registry!` static assertion |
| event name | ≤ 96 B | the naming rule |

An event that could exceed a bound does not compile. The run-time `refused` count (OPP:191's `log.record_refused`) therefore survives only as a defensive check in the encoder. C-7 requires it to stay zero.

**15. Admission, the queue and the drop policy.**
- **Order.** Level filter, then the per-name budget, then queue reservation, then encoding.
  - The level filter runs before the event is constructed. A filtered record is not loss.
  - The producer reserves `E::MAX_ENCODED` bytes and one slot with atomic operations **before** encoding, then releases the unused part (admission before allocation; OPP:192).
- **Bounds:**
  - **Queue:** 2 MiB and 4,096 records, whichever comes first (OPP:192).
  - **Headroom for `warn` and `error` (LD):** the last 256 KiB and 512 records are admitted only for those levels, so a `debug` flood cannot crowd out the records support needs. Rejected: evicting lower-level records already queued, which needs a scan under a lock.
  - **Per-name budget (LD):** at most 1,024 records of any one event name per RequestId. A storm of one event cannot starve the others. OPV10's `event-count-budget` (OPV10:170-171) is the precedent.
- **Drop.**
  - When a bound is hit, the **new** record is dropped and counted by reason and level (OPP:192).
  - **Producers never wait.** No producer takes a lock that is held across I/O, and none waits for space. Control-plane, supervision and cancellation paths enqueue without blocking (OPP:201).
- **Memory.** About 2.2 MiB per host process (queue, ring and pre-scope buffer), counted in the host's RSS budget (OPP:207).

**16. The pre-scope buffer, the crash ring and the drain deadlines.**
- **Pre-scope buffer.** It holds records from before the invocation's sink is known: 64 KiB and 256 records, drop-newest, counted `prescope-full` (OPP:193). "Pre-scope" is OPP's term for the time before the sink scope is known. It is unrelated to item 9's identity scopes: every pre-scope record already has a RequestId.
  - If the same invocation later holds S-OP-1's write capability, the records are flushed into the file in their original order and with their original `ts` (OPP:220).
  - Otherwise they are discarded at exit and counted `unpersisted`.
- **Crash ring.** 64 KiB preallocated, at most 256 records, overwriting the oldest (OPP:194).
  - Overwrites are reported in the crash record's header (S-OP-7), not as loss.
  - The ring holds P0–P1 projections only.
- **Drain.** The writer drains the queue until the deadline less a 20 ms marker reserve, then writes the marker (item 17). The deadlines are:
  - **normal exit:** 200 ms;
  - **cancellation:** 100 ms, inside OPP §5.5's goal;
  - **export shutdown at M5:** 1 s (OPP:197-199).

  At the deadline the writer abandons the rest, counts it `drain-abandoned`, and leaves the exit unchanged.

**17. Loss accounting, the non-recursive marker and the sink gate.**
- **Loss reasons.** A closed enum of eight:

  | Reason | Category | Meaning |
  |---|---|---|
  | `refused` | loss | defensive encoder refusal; expected zero |
  | `budget` | loss | per-name budget exceeded |
  | `queue-full` | loss | queue bound hit |
  | `prescope-full` | loss | pre-scope bound hit |
  | `sink-failed` | loss | an I/O error on the sink; that record and every later one for the sink |
  | `sink-stopped` | loss | the sink's gate closed |
  | `drain-abandoned` | loss | not written by the drain deadline |
  | `unpersisted` | policy | pre-scope records discarded because no persistent sink was admitted |

  S-OP-6 may word the categories differently.
- **Counters.** One atomic counter per (reason, level): 40 counters, plus the first I/O error kind and errno per sink.
- **The marker** is `log.loss.counted`: one record per persistent sink, written once at drain.
  - It is **encoded into a slot preallocated at logging start, bypasses the queue, and is written by the writer directly.** It cannot be dropped, cannot spend a budget, and cannot fail to encode, because its size is static.
  - If its write fails, nothing more happens: no counter, no retry, no further record and no panic. A cap hit never emits through the saturated path (OPP:202).
- **Visibility.** If any loss counter is nonzero and the command produces an envelope, the P0 loss summary goes to `diagnostics` through S-OP-6 (OPP:203). Loss never changes Coverage, termination, exit or a committed Run (OPP:203; OPP §5.2).
- **The sink gate (the mechanism behind OP-R3-NB-02).** Each persistent sink has an atomic admission gate.
  - **When it is read.** The writer reads it **immediately before issuing each write syscall**, and that read is the linearization point.
  - **A write already issued may complete after the gate closes.** No retroactive suppression is claimed.
  - **After closure,** records queued for that sink are counted `sink-stopped`, and no marker is written to it.
  - **Who closes the gate is not decided here.** S-OP-1's stop rule closes it (OPP:205), and so may S-OP-7's suppression after an uncertain or latched outcome (OPP:312). This law fixes only the mechanism and the accounting.
- **Basis:** DRC:578-579 ("never hide dropped messages"); OPP:201-203; OPV10:101-102.

### F. Joins

**18. With DR-114 (DC4 redaction).**
- **Decision.** S-OP-2 applies DC4's two-tier structure to every operational sink, without changing DC4.
  - **The GUARANTEE tier is the vocabulary.** DC4's guarantee covers "members that doctor CONSTRUCTS from sources whose classification the host already knows" (DC4:1016-1017). S-OP-2 makes **every** record field such a member: no record field exists outside the closed kinds.
  - **The DISCLOSURE tier is only item 11's tripwire guard.**
- **Mapping of DC4's default-redacted classes** (DC4:1028-1068):

  | DC4 class | S-OP-2 treatment |
  |---|---|
  | secret values (DC4:1030-1031) | no kind; a handle name and presence flag only, after DR-108 |
  | environment values (DC4:1034-1035) | no kind; names only as `DeclaredName`, for declared variables |
  | absolute paths (DC4:1038-1039) | `ProjectPath` or `PathRef` |
  | host and account identifiers (DC4:1042-1043) | no kind |
  | raw error objects (DC4:1058-1059) | a closed error-kind `Code` plus `Errno`, and **no message at all**. DC4's "name plus scrubbed message" is stricter here. |
  | ANSI and C0 (DC4:1062-1063) | escaped at encoding; the guard backs it |
  | unbounded strings (DC4:1066-1067) | static bounds |
  | secret previews (DC4:1070-1072) | none, and no digest of a secret |

  DC4's honest exclusions carry over (DC4:1076-1083). Names the operator chose are reported as names (P2). The fact that a thing exists is disclosed. Bytes outside OpenSIP's sinks, such as CI logs, scrollback and hand-made copies, are outside this law.
- **Projections.** DC4's rule that "every projection consumes the already-redacted report" (DC4:1086) becomes: every sink encoder consumes an already-typed record and never sees an unsafe value.
- **Doctor.** Doctor's **report** stays DC4's, and S-OP-2 changes no doctor schema. Doctor's operational **records** follow S-OP-2 and go only to nonpersistent sinks (OPP:216). Open question R2 asks the DR-114 owners to confirm this split.

**19. With DR-125 (the SDK's "bounded structured diagnostics").**
- **The reading.** For the host, "structured host logs" means registry records only, and "unstructured host logs" means any byte a log sink receives that a registry encoder did not produce. That is forbidden (SDK4:81, SDK4:103; F02:194-195). "Redaction is host-owned" (SDK4:81) is items 8–11.
- **Component diagnostics under O1(a)** (M3L:326-343). Components emit no structured diagnostic frame. Their "bounded structured diagnostics" reach operational records only as host-constructed events:
  - their closed protocol responses become `Code` values (P0);
  - their non-authoritative stderr channel (DRC:574-576; DLV:1133) is reduced to `Reduced` by the host.

  Components never write a log, receive a log path or emit a registry event (OPP:222; M3L:389).
- **What S-OP-2 does not add:**
  - no SDK operation. DRC §8's operation set (DRC:521-533) is unchanged.
  - no wire member.
  - no change to "never hide dropped messages" (DRC:578-579). Item 17 realises it for host records.
- **The gates.** DR-G20's surface set includes `log` (SLJ:481). DR-G20's "redaction/bounds/audit correlation" (QG:408) and DR-G21's "bounded redacted diagnostics/audit" (QG:428) are exercised by this law's controls, which S-OP-11 authors (OPP:418).
- **Open question R1** asks the DR-125 owners to confirm this reading.

**20. With the secret-handle rule (F03:45-50; DR-108).**
- **Decision.**
  - **Values.** A resolved configuration secret value is "excluded from … diagnostics, and support bundles" (F03:49-50). It has no `SafeField` kind, and sealing makes that permanent.
  - **Any future secret-bearing type** (the DR-108 successor; REG:297) must also have:
    - no `Display` or `Serialize`;
    - no `Debug` that shows the value;
    - no `AsRef<[u8]>` or `Deref` to text;
    - no exposed length.
  - **Handles.** When DR-108 lands, a handle's **name** is `DeclaredName` (P2), and its presence is a `Flag` (P0), as in DC4's "handle plus presence" (DC4:1017).
  - **Brokers.** A broker resolving a handle logs no value (F03:65-67).
- **Source is not covered by the secret rule.** The secret rule "does not classify arbitrary analyzed source text as a configuration secret" (F03:56-59). S-OP-2 therefore does **not** rely on secret classification for source. Source is P3 because no kind accepts its bytes, which is stronger.
- **What is not claimed.** S-OP-2 does not claim that code which reads source cannot see secrets in it (F03:57-59). It governs only what the host writes to its sinks.

**21. With the no-hidden-environment-input rule (CH13:59-62).**
- **Decision.** The level filters, sink selection, export settings and every bound come only from:
  - release constants;
  - S-OP-5's configuration section;
  - S-OP-6's flags.

  Nothing is read from the environment: no `RUST_LOG`, `RUST_BACKTRACE`, `RUST_LIB_BACKTRACE` or `OTEL_*` (OPP:139, F11; OPP:226). No subscriber or filter constructor that reads the environment is used.
- **Environment variables in records.** They appear only as declared names, never values (OPP:170).
- **Basis:** CH13:59-61 ("no seventh configuration layer, provider-private override, or hidden environment input"); OPP:367.

**22. With S-OP-4: the provider records (M3L items 12–14).**
- **Decision.** S-OP-2 registers the needs in M3L:410-419 (item 23) and fixes how each provider-originated value is disposed of. **Nothing crosses the wire because of S-OP-2.** Neither TS2 nor Rust3 gains a frame or member (M3L:98-117).
- **The host is the only author.** It writes every provider-attributed record from host-held values, never worker echoes (M3L:382). RequestId never reaches a child (M3L:376).

| Provider-originated value | Source | Disposition | Class |
|---|---|---|---|
| stderr bytes | DRC:574-576; DLV:1133; bound 262,144 (NE:2967; RPP:117; `handshake-v1.schema.json:281-283`) | `Reduced`: total bytes observed, and whether the capture hit its bound | P0 |
| control `fault.detail` | CC:36, ≤ 1,024 B (CC:56-58) | `Reduced` | P0 |
| control `refusal.detail` | CC:32 | `Reduced`, plus the refusal family as `Code` (RF1–RF8) | P0 |
| health and ping nonce | CC:33, CC:50-54 | never recorded | — |
| `healthReport` status | CC:34 | `Code` (ready, busy, stopping) | P0 |
| `resourceReport` | CC:35 | `Bytes`, `Elapsed`, `Count`, described in the registry as provider-asserted (not progress, M3L:339) | P0 |
| Rust `ProviderFaultV2.faultKind` | RPP:445 | `Code` (compiler-crash, internal-invariant, input-rejected) | P0 |
| Rust `ProviderFaultV2.detailCode` | RPP:445, "diagnostic only, never D9 authority" | `RegisteredCode<RustDetailCode>` with an **empty table at r1**, so every value is `{unrecognized: Reduced}`. This equals M3L:351. The Rust provider unit (G) may add members as an ordinary registration within K3's limits. | P0 |
| closed terminal responses | for example `UnavailableV1.reason` (DLV:857) and their NE §9 successors | `Code` | P0 |
| stage terminal | NE:2025 | `Code` | P0 |
| progress | host-counted admitted transitions (M3L:352-356) | `Count` per stage and universe | P0 |
| universe | NE:3160-3164 | `IdentityDigest<Universe>`, the 64-hex suffix | P1 |

- **Lead decisions.** Two rows go beyond M3L:345-371:
  - **refusal detail** is reduced, because CC:32 carries "optional opaque detail";
  - **nonces** are never recorded.

  Both apply that law's logic to members it did not list.
- **Rejected:** registering a closed `detailCode` set now. It would bind the G unit's design and give an open protocol member a meaning, which M3L item 1 forbids this law to change.

### G. The initial registry

**23. The initial events (r1).** These are names and fields for review. The levels are provisional. Every event carries the header of item 1. "Requires" lists identities beyond the RequestId. "Export" marks candidates that S-OP-10 may admit; nothing is exported before it.

| Event | Level | Requires | Fields (kind; class) | Export |
|---|---|---|---|---|
| `log.stream.opened` | info | — | version (K4; P0), platform (K1; P0), build (K1; P0), sink (K1; P0), pid (K11; P1) | no |
| `log.loss.counted` | warn | — | sink (K1), counts (K8 over loss reason × level), sink_error (K1, opt), errno (K2, opt); all P0. The reserved marker of item 17. | no |
| `host.request.parsed` | info | — | command (K1), format (K1), steps (K2); P0 | candidate |
| `host.settings.resolved` | info | — | concurrency, cpus (K2), memory (K2 `Bytes`), source (K1); P0 (OPP:249, OPP:277) | candidate |
| `host.phase.completed` | info | — | phase (K1), wall, cpu (K2 `Elapsed`), outcome (K1); P0 (OPP:248) | candidate |
| `host.signal.received` | warn | — | signal (K1), ordinal (K2), arrival_phase (K1, OPP §5.5's A–E); P0 | candidate |
| `host.termination.decided` | info | — | class, exit, reason (D9, opt), detail (DomainDetail code, opt), all K1; P0 | candidate |
| `host.reuse.disclosed` | info | Plan | stage (K1), universe (K9; P1), state (K1, `recomputed`), cause (K1, `no-reuse-path`) (M3L:307-322) | no |
| `config.value.resolved` | debug | — | key (K1), layer (K1); then one of flag/count/choice (K2/K1; P0), path (K12; P2), or present (K2; P0) for string and secret-classified values | no |
| `discovery.path.skipped` | debug | Project | path (K12; P2), reason (K1; P0) | no |
| `snapshot.seal.completed` | info | Project | snapshot (K9; P1), files (K2), bytes (K2), wall (K2) | no |
| `provider.process.spawned` | info | Plan, Execution | role (K1), protocol (K1), universe (K9; P1), pid (K11; P1) | no |
| `provider.process.ready` | info | Plan, Execution | role, universe, start (K2), transfer (K2) (M3L:400) | no |
| `provider.stage.changed` | debug | Plan, Execution | role, universe, stage (K1), state (K1) | no |
| `provider.stage.terminal` | info | Plan, Execution | role, universe, stage, terminal (K1, NE:2025), reason (K1, opt), fact_frames, coverage_frames (K2), analysis (K2) | candidate (P0 fields only) |
| `provider.process.reaped` | info | Plan, Execution | role, universe, pid, exit_class (K1), signal (K1, opt), max_rss (K2 `Bytes`), rss_unit (K1), cpu, teardown (K2) (M3L:402-406) | no |
| `provider.stderr.reduced` | info | Plan, Execution | role, universe, stderr (K7) | no |
| `provider.fault.reduced` | warn | Plan, Execution | role, universe, source (K1: control-fault, control-refusal, rust-provider-fault), fault_kind (K1, opt), refusal_family (K1, opt), detail (K7), detail_code (K3, opt) | candidate (P0 fields only) |
| `provider.resources.reported` | debug | Plan, Execution | role, universe, resident (K2 `Bytes`), cpu (K2), handles (K2), all provider-asserted | no |
| `supervision.liveness.missed` | warn | Plan, Execution | role, universe, window (K2) | candidate |
| `supervision.progress.absent` | info | Plan, Execution | role, universe, stage (K1), since (K2) (OPP:238) | no |
| `supervision.limit.breached` | warn | Plan, Execution | role, universe, limit (K1), observed (K2), unit (K1) | candidate |
| `supervision.cancel.sent` | info | Plan, Execution | role, universe, inband (K2 `Flag`), control_reason (K1, CC:37) (M3L:444-448) | no |
| `supervision.cancel.forced` | warn | Plan, Execution | role, universe, trigger (K1: second-signal, grace-expired), grace (K2) (M3L:458) | no |
| `supervision.wait.expired` | warn | Plan, Execution | role, universe, wait (K1), limit (K2) (M3L:457) | no |
| `storage.commit.classified` | info | Plan, Execution (+ Run only if `Committed`) | outcome (K1), latched (K2 `Flag`) | candidate |

- **Covered.** This covers every row of M3L:412-419 and the operational record's fields at the provider boundary (M3L:396-409). The operational record (OPP:249) is composed of these events, and its harness projection is Q0's.
- **Rejected:** an r1 registry that names only the provider events. The loss marker, phase spans and termination record are needed at M3 too (M3P:92-93).

### H. Recording

**24. Recording on acceptance (LD).**
- **Decision.** The accepted PROPOSAL is the successor text. When M3-O's first code unit lands, the lead records a verify_design successor (`successor.json` plus a subject manifest, the EC1 form). It makes two insert-only passage overrides, so the product's design lock sees the join:
  - **SDK4** `/standardizedFamilies/1/rule`. Append: " Host operational records are only events of the S-OP-2 registry, whose fields are only S-OP-2 SafeField kinds; free text reaches no sink (contract successor S-OP-2)."
  - **DRC line 576.** Before: "meaning. The SDK owns framing,". After: "meaning; the host reduces that channel to its byte count and truncation flag before any sink (contract successor S-OP-2). The SDK owns framing,".

  F02:193-197 is not overridden. DRC §8 is already its preview successor (OPP:82), and F02 is D-372-pinned.
- **Review.** That recording unit gets its own review (`ACCEPT-DESIGN-UNIT` with a single-string `subjectManifestSha256`). It changes no meaning beyond this text.
- **Rejected:** recording now. The product design lock changes only with a product unit, and no product unit is due before M3-O.

## Controls

The controls are authored at M3 under S-OP-11 and qualified at M6 (OPP:424). They refine OPP:428-437, and each names the item it proves.

| # | Control | Proves |
|---|---|---|
| C-1 | **Compile-fail suite.** Rustdoc `compile_fail` tests with error codes, or a UI-test harness, if M3-O admits one. Each of these must fail to compile:<br>- a field of type `String`, `&str`, `Cow<str>`, `PathBuf`, `OsString`, `Vec<u8>`, `io::Error`, `&dyn Error`, `fmt::Arguments` or `serde_json::Value`;<br>- `Correlation` built from text;<br>- `IdentityDigest` built from bytes or a hasher;<br>- `ProjectPath` built from `&str`;<br>- the `SecretValue` stand-in used as a field;<br>- an `Execution`-requiring event at a scope from before admission;<br>- a RunId from a candidate;<br>- an event over 4 KiB, over 32 fields, or at depth 3;<br>- an `Event` impl outside `registry!`;<br>- a `CodeEnum` whose table is not `const`. | 5, 8, 9, 14, 20 |
| C-2 | **Registry integrity.**<br>- Names match the grammar and are unique.<br>- Domains are in the list, and retired names are not reused.<br>- Every field is a K1–K15 kind.<br>- The Markdown and JSON renderings equal the committed files.<br>- The constructor list equals the audited exception list. | 2, 3, 8 |
| C-3 | **Foreign events.** A dependency emits `tracing` and `log` events carrying canaries: no sink receives a byte of them, and no logger is installed. | 10 |
| C-4 | **Canary privacy** (OPP:428).<br>- **Canaries:** random high-entropy, low-entropy passphrase, unknown formats, Unicode and bidi, ANSI and C0, and 10× over each bound, plus source snippets.<br>- **Injected into:** TS and Rust provider stderr, `fault` detail, `refusal` detail, `detailCode`, nonce, `clientCorrelationId`, configuration strings, declared and undeclared environment values, file and directory names, absolute paths outside the project (including a home directory with a canary username), I/O error text, panic payloads and nested configuration.<br>- **Sinks checked:** file, stderr at every level, crash ring and crash file, bundle with and without P2 consent, a captured OTLP stream, envelope `diagnostics`, and the pre-scope flush.<br>- **Pass rule:** canary bytes appear only as P2 names in P2-permitted sinks. The SHA-256 (hex and base64) and 12-hex prefix of each canary appear nowhere. | 4–7, 12, 13 |
| C-5 | **Path rendering.**<br>- ESC, C0, DEL, C1, bidi controls and newline in file names are escaped in both encodings; every record is one line.<br>- A `PathRef` tag differs across processes for the same path, and never equals the path's SHA-256. | 6, 13 |
| C-6 | **Guard tripwire.**<br>- Zero guard firings over the whole C-4 corpus.<br>- Unit tests of the guard on synthetic bytes check the ANSI-then-C0 order, the length marker and the credential shapes. | 11 |
| C-7 | **Bounds** (OPP:431).<br>- **Floods:** stderr at 10× its bound; a single-name storm (the budget); queue saturation with the writer blocked on a FIFO. Producers never wait, and the counts are right by reason and level.<br>- **Headroom:** `error` records are admitted after `debug` fills the queue.<br>- **Pre-scope:** overflow is counted.<br>- **Drain:** the deadline holds with a stalled sink.<br>- **Marker:** written exactly once per sink and never enqueued. A failed marker write leaves no further output and no panic.<br>- **`refused`:** stays zero.<br>- **Sink gate:** closed with a populated queue and a write in flight (OP-R3-NB-02): the in-flight write completes, queued records count `sink-stopped`, and no new write is issued. | 14–17 |
| C-8 | **Phase-lawful identity at run time** (OPP:429). Records in each phase carry exactly the lawful header identities, and allocation failure emits only the fixed line. | 9 |
| C-9 | **Code locations.** A release build emits no absolute path or `.cargo` path in any `CodeLocation`. Dependency locations encode as `external`. | 5 (K6) |
| C-10 | **Environment.** Setting `RUST_LOG`, `RUST_BACKTRACE`, `RUST_LIB_BACKTRACE` and `OTEL_*` changes no sink's content, level or set. | 21 |
| C-11 | **Invariance** (OPP:437). Results are identical with logging off and on, at every level. | all |
| C-12 | **Provider dispositions.** Fake TS2 and Rust3 providers exercise every row of item 22's table, including an unregistered `detailCode`. | 22 |

## Rejected alternatives

The rejected alternatives are recorded with the items that reject them. The principal ones:
- **Sink-side redaction as the guarantee**, by pattern or entropy scrubbing (DC4:1023-1025; OP-R1-03; item 11).
- **Run-time privacy tags or validated safe strings** (item 8).
- **Free-form `tracing` fields behind a deny-list** (item 10).
- **Serializable arbitrary event structs, or per-crate registries** (item 1).
- **A JSON registry with code generation** (item 3).
- **Unkeyed path hashes, or a persistent per-installation path key** (item 6).
- **Value-inspecting projection, or whole-event refusal per sink** (item 12).
- **Evicting queued lower-level records** (item 15).
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
- Any digest or fingerprint of P3 data. An unkeyed hash of a path. A source-file content digest.
- A P3 class, a "restricted" class, or any escape that admits free text into a record. O9's consented capture is not this law's.
- A `SafeField` impl or kind constructor outside the vocabulary module, or a P1/P2 constructor that takes text or bytes.
- A run-time event name, an event outside the registry, a second registry, or a reused retired name.
- Sink projection by value inspection, or a sink receiving a record before projection.
- A producer that blocks on the queue or on writer I/O; a loss marker that is enqueued, retried, or itself counted; a cap hit emitted through the saturated path.
- Level, sink or export settings read from the environment.
- RequestId, a path or a rule id exported before S-OP-10 admits it; any export before O4.
- A provider that writes logs, receives a log path or emits registry events; host-side parsing of stderr.
- A record field entering any identity, digest, Plan, Coverage, verdict or exit (OPV10:79; OPP:203).
- `cfg(debug_assertions)` free-text logging.

## What this does not decide

- **S-OP-1, log storage and custody:**
  - which capability creates, opens, rotates and prunes files;
  - the layout (OPP:221);
  - the 512 MiB best-effort retention target, the 14-day age and the 768 MiB stop rule (OPP:204-206);
  - the log-directory lock;
  - doctor's read rules.

  S-OP-2 supplies only the `sink-stopped` gate and its accounting (item 17).
- **S-OP-5, configuration.** The `operability` section, its fields and their provenance (OPP:226).
- **S-OP-6, output carriers:**
  - the `-v`, `-vv`, `--log-level` and `--timings` grammar;
  - the human `request` line;
  - the wording and placement of the loss summary in `diagnostics`;
  - which header identities human stderr prints.
- **S-OP-7, crash records:**
  - the panic hook;
  - descriptor admission;
  - the crash file;
  - the nonblocking stderr path;
  - suppression after a latched or uncertain operation, including when the item 17 gate closes;
  - the ring's read path.
- **Also not decided:**
  - S-OP-3, because O1(a) adds no frame;
  - S-OP-9's bundle consent flow and member limits;
  - S-OP-10's export admission and owner decision O4;
  - S-OP-12;
  - O7 (confinement);
  - O9 (restricted stderr capture);
  - the choice of `tracing`;
  - the vocabulary's crate placement;
  - a process-level scope for a multi-request host (M5).

## Open questions

- **R1. DR-125 owners.** Is item 19's reading right? Under O1(a), "bounded structured diagnostics" from components reach records only as host-constructed codes and reductions, and "unstructured host logs" means any sink byte that a registry encoder did not produce.
- **R2. DR-114 owners.** Confirm item 18's split. Doctor's report keeps DC4's "name plus scrubbed message", while operational records carry only error kinds and errno.
- **R3. S-OP-9 and O5.** Is P2 consent per bundle sufficient, or per member class?
- **R4. S-OP-10 and O4.** Are the export candidates of item 23 right?
- **R5. The reviewer.** Should `RuleId` be P0 while only bundled packs exist (X12)? r1 keeps OPP's P2, so that the class does not depend on pack policy.
- **R6. S-OP-7.** Is the ring's `info` level right? A crash record would then omit `debug` context.
- **R7. The lead.** Item 24's recording timing.

## Citations checked

Every citation above was opened and read on 2026-10-04. Points a reader may trip on:
- **The secret-value rule** is at F03:45-50: the heading is at 45 and the rule at 47-50; line 44 is blank. Its source-text limit is at F03:56-59.
- **The D.SDK selector** is APP:620-630. It pins DRC (`9ab2874e…`) at "## 8. SDK contract (DR-125)", DRC:513. §8 runs to DRC:601, and §8.1 starts at DRC:603.
- **The DR-125 application row** starts at APP:3860, and its inherited SDK4 pin matches the file's sha256.
- **"Bounded structured diagnostics"** is F02:193-194 and SDK4:81. DRC §8 does not use the phrase. It says "Non-authoritative diagnostics may use the existing bounded stderr channel" (DRC:574-576).
- **Product facts are re-read at `3d2d5b5`:**
  - the bootstrap lines (18, 43, 64);
  - `request.rs:15-55`;
  - `command-envelope-v7.schema.json:12, 35-42, 143-150`;
  - `common-v4.schema.json:7-10, 132-135, 641-686`;
  - `handshake-v1.schema.json:281-283`;
  - no `tracing` or `log` in `Cargo.lock`.

## Not claimed

- **Measurements.** No number is measured. All bounds and budgets are provisional, and the only constants are cited protocol bounds.
- **Edits.** No contract, schema, gate, threshold, register row or pinned file is changed, and item 24's overrides are proposals.
- **A complete confinement claim.** The vocabulary prevents free text and fingerprints from reaching OpenSIP's sinks. It does not prevent deliberate covert signalling by code that already reads source: a first-party provider could choose among codes, counts or timings. G21 "does not claim security confinement" (QG:429), and confinement is O7.
- **Bytes outside OpenSIP's sinks** (DC4:1081).
- **Implementation.** No product code, cargo command or test was run for this revision. M3-L is cited as a draft; if its accepted text changes items 12–14, item 22's table and item 23's provider rows follow by ordinary registration, unless a kind or class must change.
