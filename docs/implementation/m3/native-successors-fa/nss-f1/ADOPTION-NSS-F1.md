# Adoption receipt: NSS-F1, the TS2 native-context inputs successor (token `native-context-inputs-v1`), 2026-10-30

**Decision LD-COORD-NSSF1 (coordinator, session 9ce22ffd): ADOPTED, owner-delegated under OD-AUTO-1, as a law-class
NE successor and handshake token, after R3 review. It follows LD-Q-37.**

## What it does
- **The token:** a new optional, non-identity `typescript-semantic` capability token, `native-context-inputs-v1`, adds
  `nativeContextInputs` to `OpenUniverse`.
- **The payload:** the exact retained `C` bytes of the Plan-bound context, the configuration graph and (when non-null)
  the layout, plus the unit root.
- **What the worker does:** it checks each preimage against the ids it holds, takes only the selection, and
  re-derives everything else.
- **The outcomes:** a context mismatch is `PreAnalyzeUnavailableV1`, as before. A graph-only disagreement or a
  closed-key refusal is the new token-gated `TypeScriptPreAnalyzeInputMismatchV1`.
- **Without the token:** every frame, payload, vector, identity and PlanId is byte-identical.
- **Program roots** stay Plan authority (LD-N7, disclosed).

## What was reviewed
| Artifact | sha256 |
|---|---|
| **`NSS-F1-r2.md`** (the successor) | `9e4a5839fe69f36408553b5f2aee6b21161a66651bc82223cb23e9d6bfa6503a` |
| **`section-9-5a.md`** (the NE §9.5a prose) | `9a021ab79d636a61664ffd65dc7a531bb118d0d6a4c2032e5152a06dec81945f` |
| **`design/native/native-context-inputs.schemas.v1.json`** | `c6bb1eeac84ea57332be5765d74516e3e5562a4d902d9575daffcef10bf6e730` |
| **`provider-handshake.schemas.v1.json`**, and its identical `handshake-v1.schema.json` | `260fb53558de21301bdb1cb66617a7a19711918160e1d8d48ba8acd2df554a0a` |
| **`overrides.json`** (18 insert-only passage overrides) | `723ff2ef53fa6af3b49526770d56885cd62cdaf44e429119dfdfd565ee4cc832` |
| Evidence: `build_overrides.py`, `build_nss_f1.py`, `vectors.json` | as listed in `HANDOFF-ADOPTION.md` |
| **R3 review r2 (`NSS-F1: ACCEPT`, no findings; both scripts re-run, MATCHES; 30 refusal-pairing checks):** `REVIEW-r2.md` | `671171f8bee2b9efb412f1c5cfa7fc550fdc30410bd5cf23ecd9e119626c9596` |
| R3 review r1 (REQUIRED-FINDINGS: RF-1 and RF-2, text corrections) | `b05449608ac68d069b84c1a4e6ab39cd1e9c1264e216f65451d30dd13874e065` |
| The author's handoff | `75fcb3046eedee38c08044b3549334374242014a13c90204f5cf328330341c58` |

- **The reviewer:** opensip-nss-f1-review, Codex gpt-6-astra/high, R3-FRONTIER (w1R:p2). It is a different vendor
  from the Claude author (opensip-nss-f1, Opus 5.5 high).

## The assignments (NSS-F1 §9; LD-Q-51)
- **X-NSS-B (the binding):** F1's first host sub-unit. It re-runs `build_overrides.py` against the then-current lock
  first.
- **X-NSS-D (the host codec):** F1.
- **X-NSS-C4:** C4a-TS. It sends the token's four values from the retained records.
- **X-NSS-C2B:** C2b-1b, through an additive accessor change reviewed by its R2 reviewer. It exposes the retained
  context bytes, graph, layout bytes and unit root, with no new derivation. C2b-1a's accepted plan is not reopened.
- **X-NSS-F1 (the worker):** F1 at R2. NC-1 to NC-17 and M-1 to M-12, with positives on production frames.
- **X-NSS-F4:** F4. The signed TS rows carry the token, and the closures support the worker's own recomputation.
- **X-NSS-PRICE (ruling):**
  - LD-N10's enumerated **host** operations are performed **once, at C4a-TS's metered admission**, and charged inline
    there under M1a C1 (OD-PROC-1 §3.3(a)). Any bound used must be lawful under BOUND-1.
  - That admission passes a **typed prior-admission result** to F1's host codec, which consumes it without
    re-charging or re-deriving. That follows the "admit once, at the owning boundary" pattern of LD-C2A-1.
  - Worker code stays outside §3.3(a) (LD-Q-38).

## Flags carried
- **CP-RUST-CTX-1:** Rust's `NativeContextV2` recomputation (NE §2.3, §9.5) may have the same input gap. It is routed
  to the first Rust worker unit that plans recomputation (RS1).
- **Every TypeScript worker now needs the token** (LD-N2). No signed TS release exists yet. F4 carries this.

## Binding
X-NSS-B, as above. These files and this receipt are copied unchanged.

## Owner notification
It is flagged to the owner as an owner-delegated, law-class adoption.
