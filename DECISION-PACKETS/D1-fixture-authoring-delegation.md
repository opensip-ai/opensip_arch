# Packet D1 — Fixture-authoring delegation (DECISIONS-NEEDED item D1)

Prepared 2026-08-27 by the Claude orchestrator for the human owner. HEAD `4abb961aad98525ca8b992a24609a6286964a451` (D-292; `git rev-parse HEAD`). This packet decides nothing. Every number below was measured from bytes at that HEAD, with two provenance exceptions: `STATUS.2026-08-26.md` is quoted from its HEAD blob (the working-tree copy is modified and still changing; every passage quoted below was checked to be present identically in both) and `DECISIONS-NEEDED.md` is untracked (`git status`: `??`); both are pinned by sha256 in the table below. Every quotation is verbatim. Where the record has no value the packet says "not in the record".

Sources of truth and digests used:

| Source | sha256 |
|---|---|
| `docs/v2/architecture/08-decision-and-readiness-register.md` (file 08) | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| `docs/coop/COORDINATOR-DECISIONS.md` (COORD; 277 lines match `^## D-`) | (tracked at HEAD; not a frozen artifact) |
| `docs/coop/artifacts/coordinator-decisions.D-056.turn2.draft.md` (the D-056 subject) | `dfb0c2af39ff31df9bf3609c131f03ee2d87a585dcd684abd633d47ffb11ed82` |
| `HANDOFF.D-000-orchestrator-live.txt` (Grok's handoff; tracked at HEAD, repo root) | `b926489df28b183eccf4447e7f0b4c7f9bb56ef1c1f19747ae2f01b147804c3d` |
| `STATUS.2026-08-26.md` (HEAD blob; the working-tree copy is modified and still changing) | `49fd34e10173a4b02f1231215d97252973438186030fc484189364a9f52bd798` |
| `DECISIONS-NEEDED.md` (untracked, repo root) | `efe87b114cdcb679f4540149a7bf4775228baf3f131d01975079c971afebea9e` |
| 37 current leftover-join files | listed with sha256 in section 2 |

---

## 0. The question as put (DECISIONS-NEEDED.md, heading `## D. Delegation scope for fixture authoring (39 obligations)`, item `D1.`)

> May I choose fixture shapes / byte-sets / envelope formats on your behalf under D-000 adversarial review where the register does not determine them (accepting CONTESTED risk), or do you want to specify them? If delegated, name any classes you want to reserve for yourself (e.g. security-sensitive: G08 trust recovery, G09 permissions).

STATUS.2026-08-26.md section `### B. Leftover-design an AI cycle could author *if the bytes were uniquely determined by closed types* — 39 obligations`:

> Fixture authoring for ~20 gates (G07, G08, G09 ×14 FX classes, G12 ×12 FC, G14, G15/AT ×8, G16, G18, G19, G20, G21, G22, G24–G30, DR-114 JOIN ×13, DR-122 SARIF, DR-127 hostile goldens, DR-105 R-6/R-10) plus two schema successors (DR-103 unicode-norm, OD-2 fold).
> Grok's standing judgment (handoff): "uniquely determined leftover-design of fixture bytes from closed types is exhausted — do not invent." I.e. **what is left requires choices** (envelope shapes, byte-sets, corpus contents) that the register does not determine. Closing these means either (a) you decide the shapes/inputs, or (b) you explicitly authorize the orchestrator to choose on your behalf under D-000 adversarial review, accepting the CONTESTED risk.

---

## 1. Standing rules that bound any answer (verbatim)

**D-000 (COORD heading `## D-000 — Delegation protocol adopted`, Decision clauses 1–3, 5):**

> 1. Any decision that would have needed the user is put to an ADVERSARIAL subagent review (prompted to refute, not confirm), iterating to consensus.
> 2. **Termination clause: 3 turns each side.** If no consensus after three exchanges per party, the decision is recorded `CONTESTED` with both positions, parked, and batched to the user; work proceeds on other surfaces. A forced consensus is never recorded as consensus.
> 3. Every such decision is documented in this register — decision, alternatives, rationale, reviewer verdict with digest, reversibility class, overturn procedure.
> 5. Decisions that turn on the user's preferences rather than on judgment are additionally marked `PREFERENCE-LADEN`, and their overturn procedure is written to cost less than the decision did.

**D-056 (subject `coordinator-decisions.D-056.turn2.draft.md`, Decision clause 5, lines 186–190; clause 2, lines 110–114):**

> 5. **Authoring fixtures and harness *specifications* remains lawful design work now.** Execution remains qualification. DR-103's own schema already places fixture generation under DR-120 / DR-G15. That authoring must exist and be independently reviewed before DR-103 can become eligible.

> 2. Every remaining acceptance-evidence member is **only** harness *execution*, fixture *execution*, or qualification *measurement*. Authoring of fixtures, schemas, successors, actor-joins, missing design, or still-UNDECIDED numbers is **not** a remainder this amendment may split.

Consequence stated by D-056 itself: a row whose fixtures are unauthored is not eligible for SATISFIED; authoring them is design work that D-056 calls lawful now, but nothing in D-056 or file 08 says *who* chooses the bytes. File 08 contains no occurrence of the token `leftoverDesign` (grep at HEAD: zero hits); the leftover-design partition lives only in the leftover-join artifacts and COORD.

**Grok's standing judgement (HANDOFF.D-000-orchestrator-live.txt, heading `## Do not invent / do not SATISFY`, line 81, verbatim):**

> Uniquely determined leftover-design of fixture bytes from closed types is exhausted. Do not invent remaining G21 CC-5 injections, reserved lists, UNDECIDED numbers, finding schemas, D9, section 7.1 recipes, pack IR, selectors, observation bytes, a D-002 platform list, SARIF goldens, sealed-Run fixtures, HostTermination, adapter implementations, reserved CI encodings, a journal, reserved SDK APIs, or Rosetta. Do not authorize implementation. Do not occupy CGHS promised paths except frozen occupancies.

Same file, line 5 (preamble under the file title at line 1, `# D-000 orchestrator live handoff — paste this entire file as the first user message after reboot.`; it precedes the first `##` heading, `## How to start after reboot`, which is at line 7), verbatim excerpt:

> Do not invent leftover-design, a Codex/Claude verdict, fixture bytes, headings without dual ACCEPT, or `docs/v2/implementation/`.

Same file, line 83 (same heading `## Do not invent / do not SATISFY`), verbatim:

> Do not SATISFY DR-117 / DR-131 / DR-133 (Class A unopened). Do not SATISFY remaining rows while leftover-design (FX-AUTHORING / reserved / adapter / SDK-API-RESERVED) remains. Do not steal OBL-THRESHOLDS / OBL-MATRIX-CORPUS / OBL-G13-RESERVED / OBL-RESERVED-NUMBERS / OBL-ADAPTER-IMPL / OBL-CI-ENCODING-RESERVED / OBL-ENCODING-RESERVED / OBL-SDK-API-RESERVED / OBL-RESERVED-TABLES / OBL-WINDOWS-PATH / OBL-ENVELOPE-MISMATCH / OBL-UNICODE-NORM / OBL-OD-1 / OBL-OD-2. Do not reopen leftover-design of EE-3a. Do not reopen DR-119 SATISFIED.

Four of this packet's 39 measurements are named in line 83's do-not-steal list: `OBL-WINDOWS-PATH`, `OBL-ENVELOPE-MISMATCH` (section 3.3), `OBL-UNICODE-NORM`, `OBL-OD-2` (section 3.4). Lifting line 81 alone would leave those four bound by line 83.

Same file, line 136 (heading `## Completion bar`), verbatim:

> Architecture is not complete. Condition 2 is 5 of 32. SATISFIED of remaining rows is blocked while leftover-design remains and Gate 1 Class A is unopened. Keep leftover-remeasuring uniquely determined occupancy-stale leftover-joins, then leftover-design that can close without inventing reserved lists/UNDECIDED numbers. Dual 0/0 always. Condition 5 last.

Note on wording: STATUS section 3B renders the judgement as `"uniquely determined leftover-design of fixture bytes from closed types is exhausted — do not invent."`; the handoff's own bytes are the first sentence of line 81 followed by the itemised "Do not invent …" list quoted above. The two are consistent; the handoff is the source.

**What Grok's line means operationally for this packet:** the handoff is a standing instruction to the orchestrator, not a user decision. It says the *self-evident* fixture work is done; it does not say fixture authoring is forbidden as such. Lifting or narrowing it is the owner's call, which is exactly item D1.

---

## 2. Inventory method and the 37 current leftover-joins

**Method.** COORD headings of the form `## D-NNN — Record <lineage> leftover-join.vN …` were enumerated (grep at HEAD). For each lineage the highest recorded version whose heading is not marked `(CONTESTED)` was taken as current. The only CONTESTED leftover-join heading is `## D-272 — Record language-quality leftover-join.v5 as DR-118 leftover remasurement (CONTESTED)`; `## D-273 — Record language-quality leftover-join.v5 as DR-118 leftover remasurement` records the same subject, so `language-quality-leftover-join.v5` is current. Every obligation object with `"leftoverDesign": true` in each file's `obligations` array was extracted.

**Result: 37 lineages, 71 obligations with `leftoverDesign: true`** (two joins carry an empty set: `g23-leftover-join.v8` `summary.leftoverDesign []` and `identity-namespace-leftover-join.v6` `summary.leftoverDesign []`). This packet covers the 39 fixture-class obligations (section 3); the other 32 are reserved numbers / lists / owners / routes and belong to DECISIONS-NEEDED section C (listed for completeness in section 5).

Discrepancy to note: STATUS section 2 says "71 obligations measured across the 38 current leftover-joins"; the heading enumeration at HEAD yields 37 lineages. The 71 matches. The 38 is not reproducible from headings at HEAD (open question 1).

| # | Current join file (`docs/coop/artifacts/`) | Recorded at | registerRow | sha256 |
|---|---|---|---|---|
| 1 | `anti-lockstep-leftover-join.v3.json` | D-186 | DR-127 | `820d724a10a1e11a2188a323a3425cd13f4c483892bb487fb93f6542103c85e1` |
| 2 | `compatibility-leftover-join.v2.json` | D-177 | DR-111 | `33e4299d7f65bf37c2f5d54193e004c69d542d3f5da99417e1360efc2f8b7259` |
| 3 | `component-manifest-leftover-join.v9.json` | D-282 | DR-103 | `e71dca64c78a8feea9e72df5ae846eb2843be50fb10d01d54d5b65714ed1d2c4` |
| 4 | `distribution-core-leftover-join.v9.json` | D-287 | DR-101 | `e6b235d3330a03e62acede6770919a413791c958a3e791eca5f677e822100bc7` |
| 5 | `doctor-actor-leftover-join.v12.json` | D-285 | DR-114 | `0c0b894ffb5f80981282455a99153975e3fac30ade076d2596efb2b4fcf1a9e9` |
| 6 | `exact-bytes-leftover-join.v7.json` | D-286 | DR-G07 | `2f73148e1fe6e1b0a734ba92978e876bb0594f5770f5ac23d1ab1fe3dd1d0df7` |
| 7 | `g08-leftover-join.v5.json` | D-281 | DR-G08 | `ba1c19d7f5e6ec4b67fc5b7589e0b5ef3c946d186166660ccdf63ea916d9a60f` |
| 8 | `g09-leftover-join.v12.json` | D-288 | DR-G09 | `fc96ba91080ccef81259c6eb5ac004303a2b919e922d4bb54a448e26d149727c` |
| 9 | `g12-leftover-join.v5.json` | D-289 | DR-G12 | `5770cc9cb993ba5ac467df4648820167addff7b5f7a10d4442fa7e57913779d4` |
| 10 | `g15-leftover-join.v6.json` | D-290 | DR-G15 | `4b2ac34c6f8c16422c1afa3f7c45ca92864953cae94c8154e508cdcfd0c8b2d2` |
| 11 | `g16-leftover-join.v5.json` | D-278 | DR-G16 | `7ce75ea514322a6e17546ec8e9b91c4fb2f66128271d6c6d757e3f627e05ab78` |
| 12 | `g18-leftover-join.v6.json` | D-276 | DR-G18 | `f531ba6a952c8c55733454c19e46ac388f0eec4d31f3b5d29bfe04fbdeaac66e` |
| 13 | `g19-leftover-join.v5.json` | D-291 | DR-G19 | `d7bce01edb64e25ac70df8feb9119e2e87aadd40c6259ffd50d797e9bfb6d126` |
| 14 | `g20-leftover-join.v6.json` | D-269 | DR-G20 | `d666a4492ef3c598b53606fff453cb14a968822b9c29b25b0b535ebde01b2d97` |
| 15 | `g21-leftover-join.v13.json` | D-292 | DR-G21 | `058717f51ee62e85fa3094e9a65c207fb78a7f706e57a35a854f1a9a55ecc66e` |
| 16 | `g22-leftover-join.v5.json` | D-271 | DR-G22 | `70e0efd68e9003d7828c93e2d7d26dad81664adebfcb1c8d38b006c80e620d3f` |
| 17 | `g23-leftover-join.v8.json` | D-240 | DR-G23 | `498324e5e456562317c7681b44cdac9138ca1e947aa363dad5a331caa3eef812` |
| 18 | `g24-leftover-join.v4.json` | D-250 | DR-G24 | `c451f7ce20e93442172322ff2fd29a029a9a0ca209538ece7c590d32c72e43d7` |
| 19 | `g25-leftover-join.v5.json` | D-249 | DR-G25 | `9f2b137fe0b01830b4113ef26c8283214a75982f588f164391d61c5510f67aa3` |
| 20 | `g26-leftover-join.v4.json` | D-251 | DR-G26 | `aba91c5a43f77ccb9244977c746ca8238b54a4e3af5f431b37b74ce6e5e68591` |
| 21 | `g27-leftover-join.v4.json` | D-252 | DR-G27 | `630b226a852e2d6479513559cb0773fad67f80271d4814e726fc69c3aa943a5f` |
| 22 | `g28-leftover-join.v4.json` | D-253 | DR-G28 | `604dc98dfc4fd6ec2df1c22f2169b5ec921f2f43ab43ef7e0c98b48750dee085` |
| 23 | `g29-leftover-join.v4.json` | D-254 | DR-G29 | `9e1af4ba3b21e483154825fa2c6d275f7ee805d1fb455f01c9d35e48411c3f64` |
| 24 | `g30-leftover-join.v4.json` | D-255 | DR-G30 | `3f3d84e0e24a2aea0ba95c282f809c8343d1827d0577ca8396d4560c5e012c75` |
| 25 | `identity-namespace-leftover-join.v6.json` | D-175 | DR-104 | `ab31c6075723d34503958a838ad1a3c4da37b3644390b6df8117ae34758099cc` |
| 26 | `language-quality-leftover-join.v5.json` | D-273 | DR-118 | `e12101736f9a320a06a3311f405981801fad73c42ba9b7537f506e6c4859bd53` |
| 27 | `language-runtime-leftover-join.v7.json` | D-274 | DR-G14 | `90e29696f0b3ed2b23c3a5f1d7c089d54aef6887e6f3a8d9d9dfe988282fb4e3` |
| 28 | `lifecycle-leftover-join.v4.json` | D-275 | DR-107 | `bcc76ee3d99c88c258496dcc5591682d4ad655e06049b802a383ba03d3f1ddfb` |
| 29 | `monorepo-leftover-join.v4.json` | D-277 | DR-121 | `03d4478c3ce6ea843f8a4ee3ea1dcc6d8c06bd661f71970fe836ce107b611481` |
| 30 | `packaging-leftover-join.v4.json` | D-266 | DR-120 | `03251cc80cc774c12335ad038eedbb38ce73431623306f11fa1e75e40db61d07` |
| 31 | `permission-leftover-join.v12.json` | D-283 | DR-105 | `496b75c60c6540c3272c2c57d86c43ca71a77a1ed2eceaa6e3a1c49251374fb3` |
| 32 | `platform-tcb-leftover-join.v9.json` | D-268 | DR-126 | `1774427e9500940d24f75fbaee622142a8be72547d68a026e18d6e957369e26a` |
| 33 | `provider-leftover-join.v4.json` | D-279 | DR-G10 | `0e31f5b558e77b55a5aa42b711e5f5927062f67ed9f150d78c875326b79f16d4` |
| 34 | `sarif-leftover-join.v4.json` | D-182 | DR-122 | `a2ab59d79051337906ae610b4c34f8203dcac0d9038f2826b32f68630bd07640` |
| 35 | `sdk-leftover-join.v6.json` | D-267 | DR-125 | `e91d6e926830833d563bb89f3693d65328173af6f0d42275ad5339ef73880341` |
| 36 | `signed-index-leftover-join.v4.json` | D-280 | DR-112 | `ae5176e2a420be75b8aade77e7f265bc411968a75a35647ae01bfc708835a174` |
| 37 | `state-class-leftover-join.v4.json` | D-284 | DR-124 | `16b00ce69fea9e5fe83f44892ffee0a69f5b41a4ad18a6aca1ce7e77e830c902` |

---

## 3. The 39 fixture-class obligations, grouped by gate

**Partition rule used (mine, stated so it can be checked):** an obligation is "fixture-class" when its `reason` text says the undetermined thing is fixture bytes / goldens / a byte-set / a fixture envelope, or (two cases) a schema successor that STATUS 3B names alongside them. Counting every such `leftoverDesign: true` measurement, *including the same obligation id measured on both a GATE join and a ROW join*, gives **39**, which matches STATUS 3B's figure. STATUS does not state its counting convention, so the match is a reconstruction, not a confirmation (open question 2). Excluding the ROW-side duplicates, there are **30 distinct obligation ids**.

**Class legend** (what kind of choice the register does not determine):
- **envelope shape** — the format/schema of a fixture record itself is unspecified
- **byte-set** — the exact bytes (inputs, digests, goldens, report bytes) of named cases are unauthored
- **corpus content** — the harness cell names a corpus class/matrix; which concrete cases populate it is unauthored
- **list or number** — a reserved list/number/table must be set before the fixture can be authored (these are Packet C items; shown here only where the fixture reason text itself names them)
- **other** — schema successor

Owner cells are quoted verbatim from file 08's gate table (`| Gate ID | Claim | Platform matrix / harness | Required retained evidence | Owner | Assurance stage now | Threshold / waiver | Status |`, line 335) and register table (line 280). The "adjacent clause" column quotes, verbatim, the `does not …` clause from the same reason text that names a neighbouring reserved item; it is quoted because it tells you which Packet C decision sits next to the fixture, not because the bytes state a hard dependency (they do so only where the class column says "axis reserved").

### 3.1 GATE-side obligations (20 gates, 20 measurements)

| Gate (file 08 line; owner cell verbatim) | Join / id | `namedCorpusNotAuthored` (verbatim) | Reason excerpt (verbatim) | Class | Adjacent clause (verbatim) | ROW twin |
|---|---|---|---|---|---|---|
| **DR-G07 EXACT-BYTES** (l.343; `Security + platform`) | `exact-bytes-leftover-join.v7` / `OBL-G07-FX-AUTHORING` | `["hostile archive","hostile path","hostile loader","TOCTOU"]` | "Fixtures are unauthored." | corpus content / byte-set | none in this reason; same join carries `OBL-FILESYSTEM-COVERAGE` ("The set remains unpopulated.") and file 08 l.343 harness cell reads "hostile archive/path/loader/TOCTOU corpus on supported filesystems" | none (no ROW twin) |
| **DR-G08 TRUST-RECOVERY** (l.344; `Security + release`) | `g08-leftover-join.v5` / `OBL-G08-FX-AUTHORING` | `["online","offline","air-gap","removable-media"]` | "Fixtures are unauthored." | corpus content / byte-set | "does not invent a recovery ceremony implementation" | `signed-index-leftover-join.v4` (DR-112) |
| **DR-G09 PERMISSIONS** (l.345; `Security`) | `g09-leftover-join.v12` / `OBL-FX-AUTHORING` | `["FX-1","FX-2A","FX-2B","FX-3","FX-4","FX-5","FX-6","FX-7","FX-8","FX-9","FX-10","FX-11","FX-12","FX-13"]` (14) | "Fixtures are unauthored." | envelope shape + byte-set (see ROW twin: "The admitted/refused decision-record envelope named in permission-truth-tables.v9 remains unspecified.") | "does not invent a decision-record envelope" | `permission-leftover-join.v12` (DR-105) |
| **DR-G10 PROVIDER-CONFORMANCE** (l.346; `Protocol + semantic owners`; status `HARD-BLOCKED pending selector refresh`) | `provider-leftover-join.v4` / `OBL-G10-FX-AUTHORING` | `["exact V1 goldens","D9/fault joins","no-reuse/process cleanup"]` | "Fixtures are unauthored." | corpus content / byte-set (goldens) | "does not invent a D9 code"; same join carries `OBL-SELECTOR-REFRESH` ("does not invent a V2 selector") | none ("There is no separate GATE leftover-join family for G10.") |
| **DR-G12 DOCTOR-PURGE** (l.348; `Operability + security`) | `g12-leftover-join.v5` / `OBL-DOCTOR-FX-AUTHORING` | `["FC-RO","FC-NC","FC-NN","FC-SCHEMA","FC-D9","FC-REDACT","FC-MODE","FC-CONSENT","FC-POSTREPORT","FC-DEGRADED","FC-HOSTILE","FC-REMEDIATION"]` (12) | "Fixtures are unauthored." (ROW twin: "Those corpora do not pin pre-image digest sets, post-image digest sets, or report bytes.") | byte-set | "does not invent a D9 code" | `doctor-actor-leftover-join.v12` (DR-114) |
| **DR-G14 LANGUAGE-RUNTIME-UX** (l.350; `Product + language + release + security`) | `language-runtime-leftover-join.v7` / `OBL-G14-FX-AUTHORING` | `["language-role × clean supported-platform matrix","offline signed closure","hostile PATH/loader/system-tool substitutions"]` | "Fixtures are unauthored." | corpus content | "does not invent a numeric threshold" | none |
| **DR-G15 PACKAGING-ADAPTER-CONFORMANCE** (l.351; `Component architecture + language publisher + release/DevEx`) | `g15-leftover-join.v6` / `OBL-AT-FX-AUTHORING` | `["AT-1 clean install","AT-2 no ambient dependencies","AT-3 hostile paths","AT-4 health/subprotocol negotiation","AT-5 offline/air-gap use","AT-6 update/rollback","AT-7 size/quality/performance gates","AT-8 archive profile byte identity and negatives"]` (8) | "Occupancy v9 authorityClaim recites fixture bytes for AT-ARCHIVE-* remain NOT-AUTHORED." | byte-set | "does not invent a numeric threshold, and does not invent an adapter implementation" | `packaging-leftover-join.v4` (DR-120) |
| **DR-G16 CI-ISOLATION-INTEGRATION** (l.352; `Release engineering + component/core/protocol/integration owners (owner cell made concrete 2026-08-13, C4)`) | `g16-leftover-join.v5` / `OBL-G16-FX-AUTHORING` | `["change-impact corpus × component/language/platform matrix","forced dependency/ownership mutations","aggregate release selection"]` | "Fixtures are unauthored." | corpus content | "does not apply v16, and does not invent reserved CI encodings" | `monorepo-leftover-join.v4` (DR-121) |
| **DR-G18 LIFECYCLE-GENERATION-RECOVERY** (l.354; `Lifecycle + storage + versioning`) | `g18-leftover-join.v6` / `OBL-G18-FX-AUTHORING` | `["crash at every journal write/fsync/rename/pointer and migration prepare/commit/abort/no-return transition","conflicting project locks","process death"]` | "Fixtures are unauthored." | corpus content | "does not invent a journal" | `lifecycle-leftover-join.v4` (DR-107) |
| **DR-G19 STATE-CLASS-AUTHORITY** (l.355; `Semantic + evidence + storage`) | `g19-leftover-join.v5` / `OBL-G19-FX-AUTHORING` | `["state-class × migration/backup/purge/recovery matrix","cross-class mutations"]` | "G19 occupancy v2 liveHarnessCellVerbatim names unauthored fixture cells of the state-class × migration/backup/purge/recovery matrix and cross-class mutations." | corpus content | "does not invent a grant-journal, and does not invent a sealed-Run class" | `state-class-leftover-join.v4` (DR-124) |
| **DR-G20 COMPONENT-OPERABILITY** (l.356; `Component architecture + CLI/operability`) | `g20-leftover-join.v6` / `OBL-G20-FX-AUTHORING` | `["component-role × human/JSON/SARIF/doctor/fault/config/progress/log corpus"]` | "Fixtures are unauthored." | corpus content | "does not invent reserved SDK APIs" | `sdk-leftover-join.v6` (DR-125) |
| **DR-G21 COMPONENT-FAILURE-CONTAINMENT** (l.357; `Supervisor + protocol + operability`) | `g21-leftover-join.v13` / `OBL-G21-FX-AUTHORING` | field is `remainingNotAuthored`: `liveCell` `["crash","panic","timeout","resource","malformed","truncated","duplicate","EOF","process-tree","recovery"]`; `dr102` `["CC-1","CC-2","CC-3","CC-4","remaining CC-5 injections","CC-6","CC-7","CC-8","CC-9","CC-10","CC-11"]`; `remainingCc5Injections` `["CC-5 prefix exactly at the operative bound","CC-5 prefix far over the operative bound","CC-5 truncated bodies","CC-5 invalid UTF-8","CC-5 duplicate members","CC-5 unknown members","CC-5 floats","CC-5 negative integers","CC-5 over-uint53 integers","CC-5 prefix one over the postHandshake bound"]`; `dr133` `["NT-6"]`; `doctor` `["FC-NC-CA1-PROCESS-TREE"]` | "Remaining namedCorpusWhenFixturesExist classes are unauthored: live-cell crash/panic/timeout/resource/malformed/truncated/duplicate/EOF/process-tree/recovery, CC-1 through CC-4, remaining CC-5 injections, CC-6 through CC-11, DR-133 NT-6, and FC-NC-CA1-PROCESS-TREE." | byte-set | "does not invent a D-002 platform list, does not invent a CC/NT/FC identifier, does not author NT-6" | none |
| **DR-G22 PLATFORM-ABI-LOADER** (l.358; `Security + release + platform`) | `g22-leftover-join.v5` / `OBL-G22-FX-AUTHORING` | `["supported OS/filesystem/architecture × hostile loader/system library/tool environment"]` | "Fixtures are unauthored." (ROW twin states: "The filesystem token of that class is the TCB filesystem selector; that axis is RESERVED and is OBL-RESERVED-TABLES, not a populated fixture set.") | corpus content (**axis reserved** — list/table decision precedes it) | "does not populate reserved TCB tables" | `platform-tcb-leftover-join.v9` (DR-126) |
| **DR-G24 PREVIEW-ANALYZE-WELL-FORMED-ADMISSION** (l.360; `Product + CLI / output`) | `g24-leftover-join.v4` / `OBL-G24-FX-AUTHORING` | `["hostile-but-well-formed admission corpus (DR-131 NT-1, NT-2)"]` | "Fixtures are unauthored." | corpus content | "does not invent NT-3 through NT-8 as G24 classes" | none |
| **DR-G25 PREVIEW-ANALYZE-MISSING-RUNG** (l.361; `Product + CLI / output + semantic owners`) | `g25-leftover-join.v5` / `OBL-G25-FX-AUTHORING` | `["missing-required-rung corpus (DR-131 NT-3)"]`; `namedNt3Readings` `["NT-3.missing-required-rung","NT-3.universe-unconstructible"]` | "G25 v2 names two unauthored fixture cells of one NT-3 class." | corpus content | "does not collapse the two readings" | none |
| **DR-G26 PREVIEW-ANALYZE-SARIF-NOT-ADVERTISED** (l.362; `Output/operability + CLI/product owners`) | `g26-leftover-join.v4` / `OBL-G26-FX-AUTHORING` | `["refuse-or-not-offer corpus (DR-131 NT-5)"]` | "G26 v1 retained evidence EV-1 and EV-2 are unauthored fixture cells of the refuse-or-not-offer corpus." | corpus content | "does not invent a SARIF advertisement, and does not restore G17" | none |
| **DR-G27 PREVIEW-ANALYZE-NOT-SEALED-RUN** (l.363; `Product + CLI / output`) | `g27-leftover-join.v4` / `OBL-G27-FX-AUTHORING` | `["no-silent-promotion corpus (DR-131 NT-6)"]` | "G27 v1 names unauthored fixture cells of the no-silent-promotion corpus." | corpus content | "does not invent a sealed-Run class, and does not take over G19" | none |
| **DR-G28 PREVIEW-ANALYZE-HOST-MUST-NOT-MINT** (l.364; `Product + CLI / output`) | `g28-leftover-join.v4` / `OBL-G28-FX-AUTHORING` | `["host-must-not-mint corpus (DR-131 NT-7, NT-8)"]` | "G28 v3 names unauthored fixture cells of the host-must-not-mint corpus." | corpus content | "does not invent a D9 code, exit, or HostTermination" | none |
| **DR-G29 PREVIEW-BOUNDARY-EXCLUDED-FORM-ADMISSION** (l.365; `Product owner`) | `g29-leftover-join.v4` / `OBL-G29-FX-AUTHORING` | `["hostile-but-well-formed excluded-form admission corpus and post-admission/pre-stage substitution-mutation corpus (DR-117 EE-1, EE-2, EE-3b, EE-4, EE-5a, EE-5b, EE-6a)"]` | "G29 v2 names unauthored fixture cells of the excluded-form admission and substitution-mutation corpus." | corpus content | "does not invent a D9 code or a section 7.1 recipe" | none |
| **DR-G30 PREVIEW-BOUNDARY-INSTALL-SHAPE** (l.366; `Product owner`) | `g30-leftover-join.v4` / `OBL-G30-FX-AUTHORING` | `["useful-install advertisement, role-list, and product-statement corpus (DR-117 EE-7a, EE-7b, EE-7d)"]` | "G30 occupancy v2 names unauthored fixture cells of the useful-install advertisement, role-list, and product-statement corpus." | corpus content | "does not invent the DR-131 pack, and does not mint Rust-as-core" | none |

Every GATE row above carries `"rideStanding": "not-capable-of-riding as execution-only remainder"` and `"executionObligationOwnerToday": "none"` (G21: `"existingGate": "none as authored implementations of remaining classes"`).

### 3.2 ROW-side obligations that are the same id as a GATE row above (9 measurements — the duplicates)

| ROW join / id | Row owner (file 08 register table, verbatim) | Reason excerpt (verbatim) | Cross-custody sentence (verbatim) |
|---|---|---|---|
| `signed-index-leftover-join.v4` / `OBL-G08-FX-AUTHORING` | DR-112 `Security + operations` | "Fixtures are unauthored." | "g08 leftover-join.v4 (D-259) remains the current G08 GATE leftover-join and also measures OBL-G08-FX-AUTHORING leftoverDesign true. This DR-112 leftover-join does not steal that leftover as a closure and does not close it." |
| `permission-leftover-join.v12` / `OBL-FX-AUTHORING` | DR-105 `Security + platform owners` | "The admitted/refused decision-record envelope named in permission-truth-tables.v9 remains unspecified." | "No path or digest of an FX decision-record is pinned." |
| `doctor-actor-leftover-join.v12` / `OBL-DOCTOR-FX-AUTHORING` | DR-114 `Operability + security` | "Those corpora do not pin pre-image digest sets, post-image digest sets, or report bytes." | "does not mint a D9 code" |
| `packaging-leftover-join.v4` / `OBL-AT-FX-AUTHORING` (`acceptanceTestClasses` `["AT-1",…,"AT-8"]`) | DR-120 `Component architecture + release/developer-experience + language owners` | "This join does not invent those AT fixture bytes." | "The 51 D-106 fixtures are FG-3 hand-authored DR-103 admission-class evidence, not adapter-run AT fixtures." |
| `monorepo-leftover-join.v4` / `OBL-G16-FX-AUTHORING` | DR-121 `Release engineering + component owners + core/protocol/integration owners` | "Fixtures are unauthored." | "g16 leftover-join.v4 (D-262) remains the current G16 GATE leftover-join and also measures OBL-G16-FX-AUTHORING leftoverDesign true. This DR-121 leftover-join does not steal that leftover as a closure and does not close it." |
| `lifecycle-leftover-join.v4` / `OBL-G18-FX-AUTHORING` | DR-107 `Lifecycle + versioning` | "Fixtures are unauthored." | "g18 leftover-join.v5 (D-263) remains the current G18 GATE leftover-join and also measures OBL-G18-FX-AUTHORING leftoverDesign true. This DR-107 leftover-join does not steal that leftover as a closure and does not close it." |
| `state-class-leftover-join.v4` / `OBL-G19-FX-AUTHORING` | DR-124 `Semantic/evidence/storage/lifecycle owners` | "Fixtures are unauthored." | "g19 leftover-join.v4 (D-256) remains the current G19 GATE leftover-join and also measures OBL-G19-FX-AUTHORING leftoverDesign true. This DR-124 leftover-join does not steal that leftover as a closure and does not close it." |
| `sdk-leftover-join.v6` / `OBL-G20-FX-AUTHORING` | DR-125 `Component architecture + CLI/operability/security owners` | "Fixtures are unauthored." | "does not invent reserved SDK APIs" |
| `platform-tcb-leftover-join.v9` / `OBL-G22-FX-AUTHORING` | DR-126 `Security + release + platform owners` | "The filesystem token of that class is the TCB filesystem selector; that axis is RESERVED and is OBL-RESERVED-TABLES, not a populated fixture set." | "does not populate reserved TCB tables" |

Note: the ROW twins cite the GATE join version current at *their* recording (e.g. "g08 leftover-join.v4 (D-259)") while the GATE lineage has since moved (g08 is at v5, D-281); COORD precedent D-276/D-278/D-281 keeps such ROW joins current (STATUS 3A, item "Not candidates"; DECISIONS-NEEDED A4). Closing a fixture obligation would require a successor on *both* the GATE join and its ROW twin, since the same id is measured true on both.

### 3.3 ROW-only fixture obligations (8 measurements, 8 distinct ids)

| Join / id | Row owner (file 08 register table, verbatim) | Named classes (verbatim) | Reason excerpt (verbatim) | Class | Adjacent clause (verbatim) |
|---|---|---|---|---|---|
| `anti-lockstep-leftover-join.v3` / `OBL-HOSTILE-GOLDENS` | DR-127 `Protocol + versioning + release owners` | `namedNotAuthored`: "hostile dual-channel race/fault/EOF/duplicate/teardown goldens with byte-opaque provider frames" | "D-111 records hostile dual-channel goldens remain named, not authored here." | byte-set (goldens) | "v7 raceCatalogByReference consumes J-1..J-5 and CC-1..CC-11 of control-protocol-contract.v2 and does not copy them." |
| `component-manifest-leftover-join.v9` / `OBL-WINDOWS-PATH` | DR-103 `Delivery + security` | "reserved device names, trailing dot, trailing space" (named by `component-manifest-windows-path-input-corpus.v1`) | "Fixture bytes remain unauthored and unscored." | byte-set + list | "does not invent a reserved-device-name list" |
| `component-manifest-leftover-join.v9` / `OBL-ENVELOPE-MISMATCH` | DR-103 `Delivery + security` | "TC-SIG conditional ENVELOPE_MISMATCH" | "corpus v6 notAuthored TC-SIG conditional ENVELOPE_MISMATCH. Not authored. Not scored." | byte-set (envelope-dependent) | none (reason is three sentences; quoted in full) |
| `doctor-actor-leftover-join.v12` / `OBL-JOIN-FX-AUTHORING` | DR-114 `Operability + security` | `namedClassesNotAuthored` (13): `["FC-JOIN-HOST-OUTSIDE-DR105","FC-JOIN-HOST-DEFAULT-AND-OPMETA","FC-JOIN-DOCTOR-CONSENT-NOT-GRANT","FC-JOIN-COMPONENT-TAIL","FC-JOIN-CA2-TAIL","FC-JOIN-FAIL-CLOSED-UNRECORDED","FC-JOIN-PERMISSIONREF-RESERVED","FC-JOIN-CA2-UNEXERCISABLE","FC-JOIN-CA2-D000-GATE","FC-JOIN-CA1-INPROCESS-UNEXERCISABLE","FC-JOIN-CA3-KEYCHAIN-UNEXERCISABLE","FC-JOIN-INHERITED-PERM-RECITAL","FC-JOIN-BLK-STILL-ROUTED"]` | "doctor-actor-join-integration-contract.v8: thirteen join fixture classes are NAMED-NOT-AUTHORED." | byte-set | "Naming is not authoring. bytes remain NOT-AUTHORED." (executing gate: file 08 l.368 DR-G32 ACTOR-JOIN-FIXTURE-EXECUTION, owner `Operability + security`) |
| `permission-leftover-join.v12` / `OBL-R10-AUTHORING` | DR-105 `Security + platform owners` | R-10 initial state named by `permission-r6-r10-input-corpus.v2` | "Authoring of the R-10 expiry-materialization byte-set remains leftover-design (D-056 Decision clause 5)." | byte-set | "'OBL-FX-AUTHORING remains the D-163 fourteen. This occupancy does not widen it. R-10 and R-6 authoring is leftover on DR-105 beyond that fourteen.'" |
| `permission-leftover-join.v12` / `OBL-R6-AUTHORING` | DR-105 `Security + platform owners` | R-6 initial state named by `permission-r6-r10-input-corpus.v2` | "Authoring of the R-6 process-death byte-set remains leftover-design (D-056 Decision clause 5)." | byte-set | same as above |
| `sarif-leftover-join.v4` / `OBL-FC-NONAUTH-TERM-FX` | DR-122 `Output/operability owner + CLI/product owner` | `sarif-fc-nonauth-term-bind.v1 namedCases` | "sarif-fc-nonauth-term-bind.v1 namedCases carry fixtureBytes NOT-AUTHORED." | byte-set (goldens) | "does not mint a D9 code" |
| `sarif-leftover-join.v4` / `OBL-FC-OUTFAIL-FX` | DR-122 `Output/operability owner + CLI/product owner` | `sarif-fc-outfail-golden-bind.v1 namedCases` | "sarif-fc-outfail-golden-bind.v1 namedCases carry fixtureBytes NOT-AUTHORED." | byte-set (goldens) | "does not mint a D9 code" |

### 3.4 The two schema successors (2 measurements, 2 distinct ids)

| Join / id | Row owner | Reason excerpt (verbatim) | Class |
|---|---|---|---|
| `component-manifest-leftover-join.v9` / `OBL-UNICODE-NORM` | DR-103 `Delivery + security` | "corpus v6: TC-PATH unicode-norm-duplicate is BLOCKED on schemas.v11 pathRule / RJ-3. A later schema successor is required before this member can be scored." | other: schema successor (a fixture member is blocked on it) |
| `component-manifest-leftover-join.v9` / `OBL-OD-2` | DR-103 `Delivery + security` | "whether to normalize TC-ACCEPT/TC-SIG/TC-BYTE-EXACT lock deferral onto a single conditionalRequires array-of-{member,gate} shape" … "Candidate owner is this schema surface (DR-103). Activation is a later successor of that artifact." | envelope shape (schema shape). DECISIONS-NEEDED C7 already says of OD-2: "may be delegated to me". |

### 3.5 Totals

| Measure | Count |
|---|---|
| Fixture-class `leftoverDesign: true` measurements (this packet) | **39** = 20 GATE + 9 ROW-twin + 8 ROW-only + 2 schema |
| Distinct obligation ids among them | **30** = 20 GATE ids + 8 ROW-only + 2 schema (the 9 ROW-twins repeat GATE ids) |
| Gates with a fixture obligation | **20**: G07, G08, G09, G10, G12, G14, G15, G16, G18, G19, G20, G21, G22, G24, G25, G26, G27, G28, G29, G30 (STATUS 3B says "~20 gates" and lists 19; it omits G10) |
| By class (distinct ids): envelope shape | 2 (`OBL-FX-AUTHORING` G09/DR-105 envelope + bytes; `OBL-OD-2`) |
| By class (distinct ids): byte-set | 12 (`OBL-DOCTOR-FX-AUTHORING`, `OBL-AT-FX-AUTHORING`, `OBL-G21-FX-AUTHORING`, `OBL-HOSTILE-GOLDENS`, `OBL-WINDOWS-PATH`, `OBL-ENVELOPE-MISMATCH`, `OBL-JOIN-FX-AUTHORING`, `OBL-R10-AUTHORING`, `OBL-R6-AUTHORING`, `OBL-FC-NONAUTH-TERM-FX`, `OBL-FC-OUTFAIL-FX`, plus `OBL-G10-FX-AUTHORING` counted here for its "exact V1 goldens") |
| By class (distinct ids): corpus content | 15 (`OBL-G07-`, `G08-`, `G14-`, `G16-`, `G18-`, `G19-`, `G20-`, `G22-`, `G24-`, `G25-`, `G26-`, `G27-`, `G28-`, `G29-`, `G30-FX-AUTHORING`) |
| By class (distinct ids): other (schema successor) | 1 (`OBL-UNICODE-NORM`) |
| Fixture obligations whose reason text itself states a reserved axis must be set first | 1 (`OBL-G22-FX-AUTHORING`: "that axis is RESERVED and is OBL-RESERVED-TABLES") |
| Remaining `leftoverDesign: true` measurements outside this packet | 32 (section 5) |

Sanity: 39 + 32 = 71 = the count STATUS section 2 reports.

---

## 4. Precedent already in the record: fixture bytes have been chosen by the orchestrator under D-000 review

The record contains six ADOPTED recordings of fixture-corpus artifacts authored by the orchestrator and accepted at dual review, none CONTESTED (COORD headings, verbatim). A seventh heading matches `^## D-.*fixture-corpus` — `## D-106 — Record component-manifest-fixture-corpus.v6 as DR-103's accepted fixture-corpus candidate` (COORD line 4169; Status "**ADOPTED 2026-08-15.** Turn 3 of 3") — but it is not listed as a precedent of the same kind: packaging v4 (section 3.2) describes those fixtures as "FG-3 hand-authored DR-103 admission-class evidence", so this packet does not treat D-106 as an orchestrator-under-D-000 precedent of the same kind.

- `## D-237 — Record g23-fixture-corpus.v3 as G23 leftover-design fixture implementations` — Status "**ADOPTED 2026-08-23.** Turn 1 of 3"; Decision: "Frozen v1 and v2 remain historical REJECT. Do not record v1 or v2 as current."
- `## D-239 — Record g23-fixture-corpus.v4 as G23 leftover-design per-D-002-platform copies`
- `## D-241 — Record g21-fixture-corpus.v1 as G21 leftover-design NT-1/NT-2 fixture implementations` — Status "**ADOPTED 2026-08-23.** Turn 2 of 3"
- `## D-243 — Record g21-fixture-corpus.v2 as G21 leftover-design per-D-002-platform copies`
- `## D-245 — Record g21-fixture-corpus.v7 as G21 leftover-design CC-5 prefix injections` — Status "**ADOPTED 2026-08-23.** Turn 2 of 3"; Decision: "Lands G21FXV3-M1, G21FXV4-M1, G21FXV5-S1, G21FXV6-S1, D245-M1, and CODEX-D245-SF1." (finding identifiers carrying corpus version tokens v3 through v6 were landed before v7 was the recorded version)
- `## D-247 — Record g21-fixture-corpus.v8 as G21 leftover-design per-D-002-platform copies of two CC-5 payloads` — Status "**ADOPTED 2026-08-23.** Turn 2 of 3"

Effect on the partition: G23's `summary.leftoverDesign` is now `[]` (g23-leftover-join.v8) and G21's reason text (g21-leftover-join.v13, `OBL-G21-FX-AUTHORING`) records, for NT-1/NT-2, "leftover-design of those two implementations is therefore stale as an authoring claim" and, for the two CC-5 injections, "leftover-design of those two injections is therefore stale as an authoring claim". These are the cases the handoff treats as "uniquely determined … from closed types"; the handoff's line 81 then says that class "is exhausted" and names, among the do-not-invent items, "remaining G21 CC-5 injections", "SARIF goldens", "sealed-Run fixtures", "HostTermination", "section 7.1 recipes", "pack IR", "a journal", "reserved SDK APIs", "reserved CI encodings", "adapter implementations". Four of those tokens appear verbatim in the "adjacent clause" column of section 3 (G18 "journal", G20 "SDK APIs", G16 "CI encodings", G28 "HostTermination"); two match modulo number (G15 "adapter implementation" for the handoff's "adapter implementations", G29 "section 7.1 recipe" for "section 7.1 recipes"). Three more are related but not verbatim matches: the handoff's "sealed-Run fixtures" against G27's "sealed-Run class" (shared token `sealed-Run`), the handoff's "pack IR" against G30's "does not invent the DR-131 pack", and the handoff's "SARIF goldens" against DR-122's two sarif ids, whose adjacent clause is "does not mint a D9 code" and whose reason text contains no `SARIF goldens` token (the goldens are named by the reason's "fixtureBytes NOT-AUTHORED").

What the precedent shows about cost: D-237 recorded v3 after v1 and v2 were "historical REJECT"; D-245 recorded v7 after landing findings named against v3, v4, v5 and v6; D-241, D-245 and D-247 each reached CONSENT at "Turn 2 of 3". What it does not show: any of those acts reaching D-000 clause 2's `CONTESTED` terminus. The record contains no CONTESTED entry for a fixture-corpus subject.

---

## 5. The 32 `leftoverDesign: true` measurements not in this packet (Packet C territory; listed so the boundary is checkable)

`OBL-AL1-AL2-AL5`, `OBL-AL3-CORE-ROLLBACK` (anti-lockstep v3); `OBL-LOCK-JOIN`, `OBL-NUMERIC-WINDOWS` (compatibility v2); `OBL-OD-1` (component-manifest v9); `OBL-2`, `OBL-D1`, `OBL-D2` (distribution-core v9); `OBL-BLK-1`, `OBL-BLK-2`, `OBL-BLK-3`, `OBL-BLK-4`, `OBL-FC-C1` (doctor-actor v12); `OBL-FILESYSTEM-COVERAGE` (exact-bytes v7); `OBL-G13-RESERVED`, `OBL-MATRIX-CORPUS`, `OBL-THRESHOLDS` (language-quality v5); `OBL-ENCODING-RESERVED` (lifecycle v4); `OBL-CI-ENCODING-RESERVED` (monorepo v4); `OBL-ADAPTER-IMPL` (packaging v4); `OBL-BLK-1`, `OBL-BLK-2`, `OBL-BLK-3`, `OBL-BLK-4`, `OBL-FC-C1` (permission v12); `OBL-RESERVED-TABLES` (platform-tcb v9); `OBL-SELECTOR-REFRESH` (provider v4); `OBL-SDK-API-RESERVED` (sdk v6); `OBL-RESERVED-NUMBERS` (signed-index v4); `OBL-GRANT-JOURNAL`, `OBL-INHERIT-BLOCKED`, `OBL-MONOTONIC` (state-class v4).

Borderline: `OBL-MATRIX-CORPUS` (DR-118) reads "Authoring remains design work (D-056 Decision 5). This join does not author that corpus. Matrix authoring waits on DR-125 closure or disposition (OBL-DR125-ACTIVATION)." It is corpus authoring, but DECISIONS-NEEDED C2 (line 43) names "matrix corpus acceptance" (the obligation id itself is not listed there; the mapping is this packet's inference) and it waits on DR-125; it is left in Packet C. If you want it treated as fixture authoring under this packet, say so (open question 3).

---

## 6. The decision

### Option (a) — you specify shapes / inputs per gate

You state, per gate or per class, the envelope shape, the byte-set membership, and/or the corpus contents; the orchestrator then authors the artifact, runs Stage A dual ACCEPT and Stage B dual CONSENT, and records. Consequences:
- 30 distinct obligation ids (20 gate ids across 20 gates, 8 ROW-only, 2 schema) need your input; several (G09 envelope, G12 digest sets/report bytes, DR-114 13 join classes, G21 10 remaining CC-5 injections plus 10 live-cell classes plus CC-1..4, CC-6..11, NT-6, FC-NC-CA1-PROCESS-TREE) are enumerated case lists rather than single choices.
- No CONTESTED risk on the choice itself (a user-made decision is recorded "verbatim rather than made on their behalf", as D-000's own Status line puts it); reviewers still adversarially check byte-faithfulness.
- Grok's handoff line stands unchanged.
- Nothing moves until you write the inputs; the register is "decision-bound, not effort-bound" (STATUS section 4).

### Option (b) — you authorise the orchestrator to choose, under D-000 dual adversarial review, with a stated default policy

You lift or scope Grok's "do not invent" instruction for the fixture class; each choice becomes a D-000 clause-1 decision (adversarial dual review, 3-turn terminus, `CONTESTED` batched to you if no consensus), recorded per clause 3, marked `PREFERENCE-LADEN` per clause 5 where it turns on preference. Consequences:
- CONTESTED risk is real per clause 2; the fixture-corpus precedents in section 4 show iteration cost (multiple REJECT versions, second Stage B turns) but no CONTESTED terminus so far.
- Each authored fixture obligation needs a successor on the GATE join and, where a ROW twin exists (9 ids), on the ROW join too; each such successor is itself a dual-review act (STATUS 3A: "~30–45 min per act when reviews pass first time" for remasurement acts; fixture-corpus acts cost more, see section 4).
- Authoring does not SATISFY any row: D-056's five gates still apply, Class A for DR-117/131/133 stays unopened (Packet B), and G24–G30 fixtures serve DR-131/DR-117 whose SATISFIED is separately withheld (handoff: "Do not SATISFY DR-117 / DR-131 / DR-133 (Class A unopened)").
- Where the reason text names a reserved axis (G22: "that axis is RESERVED and is OBL-RESERVED-TABLES"), the fixture cannot be completed before the Packet C decision; the orchestrator would have to stop at the reserved axis or you would have to decide C4 first.
- Fixture bytes chosen by the orchestrator are still subject to the handoff's other prohibitions unless you lift them (no D9 code, no D-002 platform list, no HostTermination, no section 7.1 recipe, no pack IR, no journal, no SDK APIs, no CI encodings, no adapter implementation, no selector, no reserved numbers/lists). Every "adjacent clause" in section 3 is one of these.

**Orchestrator recommendation (candidate default policy per class, for you to accept, edit, or reject; no specific fixture bytes are proposed here):**
- *corpus content* (15 ids): delegate. Default policy: populate each named corpus class with the minimum case set that exercises every member the harness cell names verbatim, one case per named member, no member the cell does not name; per-D-002-platform copies follow the D-239/D-243/D-247 pattern; the corpus artifact recites the cell verbatim as its naming parent.
- *byte-set* (12 ids): delegate, except the security-owned ones below. Default policy: bytes are derived only from already-accepted artifacts (INPUT corpora, occupancies, contracts) cited by path + sha256; any value not derivable from an accepted artifact is recorded as a named open decision in the artifact rather than chosen.
- *envelope shape* (2 ids: G09/DR-105 decision-record envelope; DR-103 OD-2 fold): reserve to you, or delegate with the policy "shape must be a projection of an already-accepted schema; no new top-level members". OD-2 is already flagged in C7 as delegable.
- *other — schema successor* (`OBL-UNICODE-NORM`): delegate; it is a DR-103 schema surface change (`schemas.v11 pathRule / RJ-3`) and D-056 clause 5 already says DR-103 authoring "must exist and be independently reviewed".
- *Candidate reserve set* (criterion: the file 08 owner cell of the gate, or of a ROW row that measures the same id, contains `security`): DR-G07 `Security + platform`, DR-G08 `Security + release`, DR-G09 `Security`, DR-G14 `Product + language + release + security`, DR-G22 `Security + release + platform`, DR-105 `Security + platform owners`, DR-112 `Security + operations`, DR-114/DR-G12 `Operability + security`, DR-125 `Component architecture + CLI/operability/security owners` (file 08 l.307; ROW twin of G20, whose own gate cell `Component architecture + CLI/operability` does not contain `security`), DR-126 `Security + release + platform owners`, DR-103 `Delivery + security`. Applied uniformly that is 7 of the 20 gates (G07, G08, G09, G12, G14, G20 [via its ROW twin DR-125; closing `OBL-G20-FX-AUTHORING` needs a successor on both joins, section 3.2 note], G22) — 8 if you also hold G10 for its `HARD-BLOCKED pending selector refresh` status — and 5 of the 8 ROW-only ids (DR-103 ×2 `OBL-WINDOWS-PATH` / `OBL-ENVELOPE-MISMATCH`, DR-105 ×2, DR-114 `OBL-JOIN-FX-AUTHORING`). The two DR-103 schema items of section 3.4 (`OBL-UNICODE-NORM`, `OBL-OD-2`) are not in this reserve set: the class-level lines above propose delegating them, and that class rule is intended to take precedence over DR-103's owner cell for those two ids (if you want owner-cell precedence instead, they join the reserve set and the ROW-side count becomes 7). DECISIONS-NEEDED D1 itself names "G08 trust recovery, G09 permissions" as the example reserve.

### Option (c) — mixed

You delegate by class and/or by gate and reserve the rest. The natural split the bytes suggest: delegate the 7 DR-131/DR-117 preview gates (G24–G30, owners `Product owner` / `Product + CLI / output` / `Product + CLI / output + semantic owners` [G25] / `Output/operability + CLI/product owners`) and the operability/architecture gates (G14–G21 except where security-owned: G14 by its own owner cell, G20 via its ROW twin DR-125), reserve the security-owned set above, and hold G22 until C4 and G10 until its selector refresh. Consequences: fastest path to shrinking the partition where CONTESTED risk is lowest; the reserved set waits on your inputs as in (a); the split must be written into the COORD act that records the delegation so reviewers can hold the orchestrator to it.

### What any answer must contain to be actionable
1. Which of (a)/(b)/(c).
2. If (b) or (c): the list of gate IDs / obligation ids reserved to you (or "none").
3. If (b) or (c): whether the default policies above are accepted as written, edited, or replaced.
4. Whether the handoff's line-81 instruction is lifted for the delegated set only, or rewritten; and, separately, whether line 83's do-not-steal list is lifted for the four packet ids it names (`OBL-WINDOWS-PATH`, `OBL-ENVELOPE-MISMATCH`, `OBL-UNICODE-NORM`, `OBL-OD-2`) — lifting line 81 alone leaves those four bound.
5. Whether the delegation itself is to be recorded as a COORD D-000 entry "made directly by the user in conversation" (the D-000 pattern) — the orchestrator's recommendation is yes, so that reviewers can cite it.

---

## 7. Open questions not resolvable from bytes

1. STATUS section 2 counts "38 current leftover-joins"; heading enumeration at HEAD yields 37 lineages. The 38th is not in the record as a `## D-NNN — Record <lineage> leftover-join.vN` heading. One on-disk candidate: `docs/coop/artifacts/doctor-leftover-join.v1.json` exists with no Record heading (zero `^## D-.*doctor-leftover-join` headings; COORD line 6924 reads "`doctor-leftover-join.v1.json` is not this subject."); whether STATUS counted it is not in the record. (The 71-obligation count matches either way.)
2. STATUS 3B's "39" and 3C's "25" do not partition 71 (39 + 25 = 64); the byte-derived partition here is 39 + 32. STATUS does not state its convention; the 39 here is a reconstruction that happens to match.
3. Whether `OBL-MATRIX-CORPUS` (DR-118) is to be treated as fixture authoring under this packet or as Packet C2; DECISIONS-NEEDED C2 (line 43) names "matrix corpus acceptance" (the obligation id itself is not listed there).
4. Whether G15/AT fixtures can be authored at all before an adapter exists: packaging v4 reason says "The 51 D-106 fixtures are FG-3 hand-authored DR-103 admission-class evidence, not adapter-run AT fixtures." and `OBL-ADAPTER-IMPL` is "owner after condition 5". The bytes do not state whether AT fixture *bytes* depend on the adapter or only AT *execution* does.
5. Whether G07 fixtures depend on `OBL-FILESYSTEM-COVERAGE`: file 08 l.343 harness cell says "on supported filesystems" and `filesystems.standing` is UNPOPULATED, but the G07 FX reason text does not state a dependency.
6. The handoff is Grok's instruction to its successor orchestrator; the record does not say whether you had endorsed line 81 as your own policy or whether it was Grok's reading of the "do not invent" discipline. If the latter, option (b) is a first authorisation, not a reversal.
