# bv4-corrections-author.v4 — pre-edit assessment

Written **before** any edit. `work/` verified byte-exact against the frozen v14
manifest (`45b1e128ca51d114…`, 6047 files, all hashes match). The concurrent
independent session on immutable v14 has not been accessed.

Inputs read in full: `root-input/root-publication-probe/{report.json,probe.py}`,
the frozen `admission-and-qualification.md` §1.1 (`9b39fef9acc94d74…`), the
selected law in `native-evidence.md` §1.4 and §10, and
`workflows-and-surfaces.md` §8. Grounding probe: `probes/p0_boundary.py`
(reference model only; no host, renderer or Run execution).

---

## 1 · CX-V14-ADMISSION-AVAILABILITY-MIRROR — confirmed, agreed

The frozen §1.1 paragraph ends:

> Independently of either, the absence is delivered publicly as a `DomainDetail`
> carrying the existing `native.capability-unavailable`, through
> `DoctorResult.defects[]` or `StepTermination.domainDetail`.

That is the **checkpoint-1** carrier, superseded twice afterwards. It contradicts
three selected sources that shipped in the same freeze: native §1.4 (per-step
`CapabilityAvailabilityV1` on `CommandEnvelope.availability`, typed ownership
tuple including `workspaceRoot`, and the explicit statement that
`StepTermination.domainDetail` is *singular* and a `doctor` report is a
*different invocation*), workflows §8, and
`common.schema.json#/$defs/CapabilityAvailabilityV1` +
`command-envelope.availability`.

I take root's framing exactly: my prior source assent and the six passing pinned
commands do not make this correct. The v3 pass corrected the *native* and
*workflow* statements of this law and left the *admission* mirror behind — the
same class of defect the pass was fixing, in a file I edited that turn. A
whole-file substring or count check would not have caught it, because the file
also contains correct text; the stale sentence is a **specific superseded
carrier** in one owning paragraph.

The second half of root's item is also real. §1.1 opens with "The authenticated
release declaration registry supplies the `default` profile **and exact
applicable TS/JS/Rust capabilities**", which is the pre-correction reading; four
paragraphs later the same section says "The registry states **availability**,
never scope. The `default` profile … is fixed by the matrix." Two statements of
one law in one section, and the first is the superseded one.

**Correction (no new behaviour).** Rewrite the two affected sentences so §1.1
mirrors the selected law: the registry supplies the `default` *profile* and the
**availability** of capabilities, with request scope fixed by the matrix; and the
absence is delivered on `CommandEnvelope.availability` as the per-step
`CapabilityAvailabilityV1`, typed tuple including `workspaceRoot`, declared
parity field of **every** `requestClass: analysis` command, advisory authority
preserved, with native §1.4/§10 remaining the owning detail. I will add a
**targeted mirror control** that asserts the superseded carrier phrasing is
absent from this owning paragraph *and* that the selected carrier is named —
tied to the paragraph, not a file-wide substring or a count.

## 2 · Default-cardinality boundary — investigated; a real, narrow gap

Reproduced on my copy, and I can answer the three questions root left open.

| | observed |
|---|---|
| `analysis-spec.requestedCapabilities` `maxItems` | **1024** |
| default capabilities per TS unit / Rust unit | **11** / 10 |
| largest TS unit count whose default fits | **93** (1023 requests, ADMIT) |
| 94 TS units | 1034 requests → **generic `ValidationError`, 265 492 scalars, untyped, no subject** |
| `scope-descriptor.workspaceRoots` `maxItems` | **1024** — and `unit_scope_descriptor` **admits** at 94 units |

**Is it default-only?** No. An *explicit* 1025-row `analysis-spec` hits the same
untyped `ValidationError`. This is the analysis-spec boundary in general, not an
artefact of the default helper.

**Does an existing law own it?** No. The published scope-refusal paragraph says
"A **scope array** that exceeds the shared foundation schema bound…" and names
only `workspaceRoots`, `pathPrefixes`, `excludedPathPrefixes`; no §10 row and no
contract sentence mentions `requestedCapabilities` as a refusal condition. So
units **94 … 1024** are a band of ordinary repositories that the scope law admits
and the default analysis cannot express, with no owning public route. That is the
narrow gap, and it is genuinely reachable — 94 TypeScript units is unremarkable.

**Severity, stated plainly.** This is a real correction, not a documentation
nicety: today the only outcome is a generic schema exception. Root is right that
this does *not* prove a real host emits that string, and right that passing it to
the native normalizer (which correctly refuses it as an unregistered key) proves
nothing about the host. A pure helper `ValidationError` is not a public
termination — which is exactly why the condition needs an owning typed refusal
rather than being left to whatever a host does with an exception.

**What I will not do**, per root's constraints: not truncate, not lower the
matrix-fixed default, not shard or raise limits, not auto-execute more steps, and
not classify an ordinary oversized selection as a host bug. The host computed the
default correctly; the *request* cannot be served within a published bound. That
is `request-rejected`, not `host-invariant`.

**Selected correction, and the judgement call in it.** `ScopeRefusal` is already
**field-generic** — `ScopeRefusal('requestedCapabilities', 1034, 1024)` today
yields detail `PROJECT.SCOPE_LIMIT`, subject
`{field, count, limit}`, and `d9_map` → `request-rejected` / exit 2 /
`REQUEST.UNSATISFIABLE`. It is merely never *called* for this field. I intend to
call it, and to widen the published sentence from "a scope array" to name both
bounded selection arrays explicitly.

I flag this as the judgement call root asked me not to fudge. The argument for
reuse: a D9 code is a **remedy class**, and the remedy here is identical to the
existing one — *narrow your selection explicitly; nothing was truncated* — the
subject encoding `field:count>limit` already carries which field overflowed, the
class and code are unambiguously right, and the paragraph already says "the
public code is shared across host/native scope admission". The argument against:
`PROJECT.SCOPE_LIMIT` is named for the project scope descriptor, and
`requestedCapabilities` is an analysis-spec field, so a consumer switching on the
code currently expects one of three scope fields. My position is that reuse is
honest **only if the published meaning is widened in the same edit**, so the code
is not silently stretched; that is what I will do. If Codex prefers a distinct
member instead, that is a one-line registry change and I will say so at the
checkpoint rather than defend reuse for its own sake.

**Scope of the change:** the guard belongs in `default_capability_selection` and
at the analysis-spec admission boundary so the generic `ValidationError` is never
the public path; the owning law goes in native §10 (the D9 row and the scope
paragraph). No Plan and no Run are minted — this refuses pre-Plan. I will show a
fitting positive control (93 units → 1023, ADMIT), the overflow guard with exact
observed field/count/limit, and the **actual public failure envelope** composed
through the existing route, not merely an exception string.

---

## Bounds of this pass

Only these two points. I will not restart closed Bv4 items, will not touch the
live repo, frozen v14, v1–v3, history, pins, generated reports or readiness, and
will keep before-images against frozen v14 for every edit. Any source correction
here needs a **successor freeze and review** — it does not mutate v14, and the
concurrent independent session's subject is unaffected.
