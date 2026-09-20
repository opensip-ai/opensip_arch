# Independent bounded review — primary integration 233 r1 and reference reader 232 r3

ROOT-authored working bytes. **Not cumulative approval, not readiness, no selection.** The 71
coverage fixtures in 232 r3 are MINE; nothing below treats them as independent evidence. 230 C-1 is
being fixed by root separately and is not re-reported. No repo/product/candidate edit, commit or push.

## Verification and reproduction

- 233 r1 `b44374d9…fb5c` (159072 B, 192 members) and 232 r3 `fa47e201…1b1e` (56976 B, 40 members):
  pin and EVERY subject member verified from the tar before extraction; both re-verified at the end.
- 233 beforeimages: `envelope_reference.py`, `signature-envelope.schema.json`,
  `signature-envelope-routes.v1.json` and `identity-schemas.v3.json` under
  `before-format-integration/` are byte-equal to my verified reference-201 copies.
- Overlay: an output-local COPY of my verified 201 `candidate/` with 233's `candidate/` laid over it
  (`claude-out/overlay`). The check script's own source-pin assertion (1296 bindings) passed there,
  so every pinned dependency resolved from 201 + the 19 frozen files; **I needed no live working-203
  file.**
- Envelope check with `--openssl /opt/homebrew/opt/openssl@3/bin/openssl` (OpenSSL 3.6.3), Python 3.12
  reference env: `status pass, 52`. My `report.json` equals the frozen
  `primary203-envelope-check-r2/report.json` in EVERY key (cases, 1296 source bindings, verifier /
  schema / routes / tool hashes), although the test keys are freshly generated.
- Variant runner: it hard-codes live `/tmp/…/m2-transition-carriers-reference-203` paths, so I ran a
  copy with ONE line changed (the `S`/`O` paths → my overlay and a fresh output dir); the 4-line diff
  is `claude-out/io/variants-runner-redirect.diff`. All three variants produce `VERIFIED` and die on
  the owner assertion; `results.json` equals the frozen one.
- 232 r3: 51 checks → **byte-identical** to `reader-check-r4.json`; 9 variants → `reader-mutants-r2/`
  identical; the coverage run equals `coverage-report-root-r1.json` except the reader path. The r3
  reader is byte-equal to the live file I had pinned (6f2a7497…); the fixtures are byte-equal to mine.

---

# Part 1 — primary integration 233 r1

## Confirmed

- **The delta is exactly what is claimed.** Routes: `payload` gains domain `.payload.2`; one new route
  `root-recovery-authorization` / `opensip.metadata.root-recovery.1` / `RECOVERY`. Envelope schema:
  one kind and two domains added to the enums, nothing else. `envelopeSchema 2`, the Ed25519 profile
  and the existing eight routes are untouched. Identity schema: `core` appended to `closure.kind` and
  the `manifestDigest` artifact sentence rewritten to the route/subject rule (my 229 G-6 form);
  nothing else in 197 KB changed.
- **Copied bytes are the reviewed ones:** private trust bundle a3a0b4f4… (231 r2), core inventory
  schema 960ecdfd… (229 r3), payload v2 47bc09e5… (215 r14), input joins d2b05b97… (230 r2), codecs
  772a2975… (227 r9), proof-node joins fd687e4e…, state continuity 780a6dd5… (the 215 embedded-head
  successor), core binding f0860bf6… (229 r3 OWNER). `trust-event-joins` differs from 227 r9 by one
  line — my P-1 fix ("working 222 r7 (latest separately frozen 222 r6)").
- **Dispatch is by BODY version, not by label.** `payloadSchema` must be an exact int in {1,2}, be in
  the reader's declared set, and its derived domain must equal the envelope's; string, bool, 3,
  missing and non-object bodies refuse (K8). The preimage is computed under the body-derived domain,
  so a relabelled domain fails `preimage digest` even with valid signatures.
- **No old-reader promotion.** `reader_payload_schemas` defaults to `(1,)`; empty, 3, bool and
  duplicate values refuse at construction (K2b–e). A legacy-default reader refuses payload2
  ("unsupported for reader") and the ninth kind ("unsupported kind for reader") (K9).
- **Route confusion refuses with real signatures:** an authorization carrier claiming role ROOT (K3),
  carrying the recovery-EPOCH domain (K4), a genuine RECOVERY-signed epoch carrier presented as an
  authorization (K5), and the same epoch signatures relabelled to the authorization kind/domain
  (K6, `preimage digest`). RECOVERY signatures do not transfer between the two RECOVERY kinds.
- **ROOT keys cannot count toward RECOVERY — and not only in the verifier.** `selection` is
  `root['recoveryAuthority']` alone, and the pinned root policy refuses a root document that lists a
  key in both sets (`ROOT.KEY_REUSE:rootKeys:recoveryAuthority`, K1a), so the overlap cannot be
  manufactured through the root either.
- The carrier boundary is stated and real: a body that is NOT a `RootRecoveryAuthorizationV1`
  verifies (K10), and `payloadSchema 2` with `payloadKind ordinary` verifies (K7). Both are the
  documented "authenticates bytes, does not admit the body" boundary, not findings.

## Findings

### I-1 (medium, integration) — changing the shared identity schema breaks four other lanes' pins, and the new schema's own provenance pins the OLD hash

`identity-schemas.v3.json` moves a76c9e2f… → febc37bd…. In the overlaid reference the OLD hash is
still asserted by `native/source-pins.v2.json`, `workflows/source-pins.v1.json`,
`foundation/source-pins.v1.json` and `foundation/evaluator3-source-pins.v1.json`; only
`security/source-pins.v1.json` carries the new one. Every check in those four lanes that binds its
pins will now stop. README says the "full frozen-candidate/source manifest" is stale, which covers
this in general, but it does not say that a FOUNDATION schema every lane pins was edited — that is
the part a reader would not guess, and it determines the order of the remaining work (re-pin and
re-run foundation/native/workflows, with an explicit expected delta, before any freeze). Related:
the copied `core-distribution.schema.v2.json` carries `x-source-pins` naming identity a76c9e2f… —
correct as the patch BASE, but inside the primary tree it now reads as a pin of a file that no longer
has that hash. State which it is.

### I-2 (low) — a reader can declare payload2 without the ninth kind

`Verifier(reader_payload_schemas=(1,2), supported_kinds=<eight>)` constructs (K2). Payload2 exists
only for the root ceremony and always carries a `rootRecoveryAuthorization` member, so such a reader
authenticates a payload whose mandatory authorization it must refuse. Harmless (the ceremony cannot
complete), but the two capabilities are one feature; refuse the combination at construction, or state
that capability coherence is the 215 producer's job.

### I-3 (low, evidence) — the 66 historical recorded payloads

README discloses that schema-less synthetic payloads in `signature-envelope-recorded66` now refuse and
that the legacy lane / differential must be reconciled "with explicit expected delta". I did not run
that lane (it is declared owed) and found no list of WHICH recorded cases change. Until that list
exists, "intentionally refuse" is a statement of intent, not an audited delta.

---

# Part 2 — reference reader 232 r3 (code changes only)

## Confirmed

- **V-2 fixed where an owner fixes the variant.** `event_target` maps `clock.by` → ClockWrite,
  `reset.by` → StandingReset, `sourceFence.by` → Continuity, and the known role edges → RoleEvent;
  decoding `clock.by` against a CREATION event now refuses `record-shape` (r2 admitted it), while the
  generic `previous` still decodes it (V2a/b). Prior/head/closing/live-batch edges stay generic by
  stated design.
- **V-3 fixed for inconsistent rows.** `decode_edge` looks the row up by `schemaPointer` and requires
  `referenceType`, `collection` and `expectedDefinition` to equal it, then validates `ref` under the
  terminal's own definition: my r2 forgery (`expectedDefinition: None`), a wrong collection, a
  missing pointer and a ref with an extra member all refuse (V3a, b, e, f).
- The six formerly pending targets are concrete; the schema pin is a3a0b4f4…; README states the
  hash-only, per-record and old-T boundaries.

## Findings

### W-1 (medium-low) — row re-derivation does not bind the edge to a SOURCE record

`schemaPointer` is itself a field of the caller-supplied edge. A whole-row relabel — take any other
registry row that is internally consistent and attach it to the ref — passes `edge-registry-binding`:

| probe | result |
|---|---|
| V3c a NodeRef field (`/operation`) presented with a consistent **BlobRef** row | **ADMITS**, 0 edges: no shape check at all, the private record is treated as opaque signed metadata |
| V3d the same field presented with the `StoreMarkerV1` row, target bytes a marker | **ADMITS** |

So the forgery space shrank from "anything" to "any of the 132 rows", but the property README
states ("refuses forged row collection/type/target") holds only for rows that disagree with
THEMSELVES. `decode_edge` never sees the record the edge came from, so it cannot know which field it
is decoding. The README's internal-producer contract still covers this; the fix that makes it
structural is small: `decode_edge(source_type, source_raw, source_pointer, target_raw)` re-extracts
the source and takes the edge from its own result (or edges become opaque objects only `extract` can
mint). The `forged-target` mutant covers the inconsistent-row case only.

### W-2 (low, stated boundary) — a fixed variant is not the event's meaning

`ceremony.begin` and `revokedBy` decode successfully against an EV-INSTALL role event (V2c/d): the
variant is RoleEvent, the token/role/outcome are not checked. Correct for a structural reader and
consistent with the README; recorded so "field-specific" is not read as "event-specific".

## Does the coverage harness give false confidence? — yes, in four specific ways

1. **It never calls `decode_edge`.** Both corrections reviewed here (V-2's effect on decoding, V-3)
   live there. 132/132 says nothing about them; they rest on root's 12 `decode_edge` call sites in
   `check_reader.py` and the 9 variants.
2. **It counts `REGISTRY` lookups, not `WIRE_REGISTRY`**, the table `decode_edge` actually uses. The
   two are built from the same rows today; a future divergence would be invisible to the harness.
3. **Coverage is per (owner, schema path), not per embedding or per root type**, as I noted when
   authoring it.
4. **The expected maps are not blind.** I wrote them by hand from owner prose, but after dumping the
   registry to see which rows needed covering. Agreement on 476 assertions shows the reader matches my
   reading; a shared misreading passes. The one property the harness does establish independently of
   my reading is completeness: no registered field is unreachable by the runtime walk, and a new
   registry row without a fixture fails the run.

Treat the harness as a regression net for extraction, not as evidence for decoding or for the
correctness of the target mapping itself.

---

## Limitations

233: I reviewed the carrier/dispatch code, the three schema/route deltas and the provenance of copied
bytes; the copied prose was compared by hash to versions I reviewed earlier, not re-read. I did not
run the foundation/native/workflows lanes (I-1 is a static pin observation) nor the legacy recorded-66
lane. Probe K8a/K8c outcomes read "malformed envelope" because the owner's helper derives the envelope
domain from the bad body; the refusal is real, the label is a probe artefact. 232: probes use
synthetic shape-valid values. No harness failure occurred; the one runner redirect is recorded.

## Pins

233: `envelope_reference.py` ea06a7856a8e5304c021c7f477c505c8eaf8e17ed6487de4ecd468dbb55f69d1 ·
`check-trust-envelope-successor.v1.py` c354b900e7b250c96171010b5dc10b8ff05f97ae3ea2c10bb9cd66e7189dce10 ·
`signature-envelope.schema.json` 3657ef6938da23fbc0b693cbed76861dafb9fe5f3d102740b6e53fa6c5faa045 ·
`signature-envelope-routes.v1.json` 674c1bf52836903ddff351bab88d230ef02d1be416d35bb7720a1e1aeff44057 ·
`identity-schemas.v3.json` febc37bd37504e8f048d9b1ede042dd3f810a7513e73f7936d8b60cbad727b2d (was a76c9e2f…) ·
`security/source-pins.v1.json` 9eb47e2405863a78266e9bb1b1d798da6ab70e978a04756b259e442da72c025a
232 r3: `reference_reader.py` 6f2a7497029e4a942209f38e513cb0bbea5acdcfb6e451e4c305ca9c9894cfea ·
`check_reader.py` 03bf6f05d97c6639023e2ea06d0f75a20ecebebac9b64c25c82d02b0426c4458 · schema a3a0b4f4…
Reference: `canonical.py` d47f25db… · kernel df45c9c5… · OpenSSL 3.6.3
