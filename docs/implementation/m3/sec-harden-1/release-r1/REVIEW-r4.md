# SEC-HARDEN-1 independent review r4

Reviewer: Codex, R3-FRONTIER, gpt-6-astra/high. Date: 2026-11-01. Scope: REQUEST-r4's narrow application check under LD-Q-256. REVIEW-r3 and earlier verdicts are preserved.

The requested amendments are correctly applied. No blocking application or fit finding remains. ITEM-1 is accepted for PLAN-r3 and the previously reviewed plan/test delta at `ed3c37e05a151bfc71a64fe400aca04db735f88c`, on this branch. The successor r2 is ADOPTABLE; coordinator adoption by receipt remains a separate action.

## Custody and verification

- REQUEST-r4.md: `f6ec38c7aebac6aa9d73c0a688c17ae7c371df41fa7c683945d4920169a278c4`.
- SUMS-r4.txt: `1c8d9397698f993bdc73d8630df5e7b89d0f38714a072274f680baf0d24fc16d`. All eight members match and have no write bits.
- PLAN-r3.md: `4cd27cf301d7096f4ba15f29108bb9d86f9d393d192e55d712358cc1e286046e`.
- SUCCESSOR-SECHARDEN-RELEASE-r2.md: `20d4bbb381edca1d8a6422e9b2d336f1bcf4fd8ebc81734000e88e8c463fd667`.
- Builder: `scripts/build_r3_amendments_v1.py`, `2f43cbd93a9aa4fad0eb66aa8f880d75539e450914c89ab31d861e7d9397ef87`.
- REVIEW-r3.md remains `69a9e4abb7af9ff53639cf268f7283b82504b12b0a42484272cd9d5bdbecfa93`; both locked predecessor documents also match the manifest.

The live control decision remains LD-Q-256, with its successor-receipt gate. I refreshed that decision and the top control checkpoint, preserving the current-state distinction between live decisions/map and historical checkpoints. The own-session preflight against PLAN-r3 returned exit 0, `ROUTE-OK R3-FRONTIER codex gpt-6-astra/high`:

`python3 -I -B /Users/sb/code/opensip-ai/opensip_arch/tools/agent_model_route.py check --provider codex --plan /Users/sb/code/.opensip-implementation-cache/lead-2026-10-25/sec-harden-1/PLAN-r3.md`

Product HEAD remains exactly ed3c37e and its worktree is clean. I performed hash/mode checks, document diffs, source inspection of the builder, and a read-only in-memory reconstruction. I did not run the builder's write path, product tests, or new product code. No product edit, store/key/real-home/held-tree access, or other artifact write occurred. R3's source and author-run test evidence carries forward with its original limitations; this is not fresh test execution.

## 1. Verbatim application and builder correspondence

I independently extracted the quoted amendments from REVIEW-r3 and compared their text with the submitted documents. Removing only Markdown quotation/list wrappers, each occurs exactly once:

| R3 amendment | Applied location in successor r2 |
|---|---|
| A | S2, line 34, immediately after the list-order sentence |
| B, both paragraphs | S3, lines 40-41, replacing the old digest and unconditional confirming-row sentences |
| C | S4, line 46, immediately after the immutable-start-subject sentence |
| D | Entire replacement §3, lines 50-61 |
| E | §6, lines 87-91, under “Amendments to these controls” |

The finding-1 paragraph occurs verbatim at PLAN-r3:66, after the preceding-refusals statement and before the reason for keeping the check before time. This closes the remaining item-1 disclosure requirement.

I parsed the builder as data rather than executing its top-level writes. Its literal amendments match REVIEW-r3. Replaying the seven successor replacements, twelve plan replacements, and §3 slice replacement in memory reproduces both complete frozen output files exactly. Every replacement anchor occurs once in its actual predecessor at the relevant step; the two §3 boundary headings also each occur once. The builder uses exact-once checks for its `apply` replacements (:10-15), heading indices for the section replacement (:66-68), and refuses an existing target before writing it (:120-124). The checked result establishes this one-off transformation of the pinned inputs; no write-path execution is claimed.

## 2. Fit with retained text

No further rewrite is required. The retained prose and explicitly labeled amendments read together consistently:

- **S3's opening bullet, successor:39:** the Present/(Clock)/Revoke sequence and event reference remain correct. Lines 40-42 supply the raw-body identity, H/D mismatch disposition, earlier standing precedence, single-Revoke rule, and unchanged pre-Present threshold refusal. The opening bullet does not override those qualifications or cause a second event for another match.
- **S1/S2/S4:** whole-view refusal at admission/use remains compatible with recorded acceptance followed by refused confirmation. List order is expressly preserved, and start subjects must be available independently of P-0 retention. No component-first pass, catalog-only acceptance identity, refreshed start inventory, or retention-only observer path is introduced.
- **§4, successor:65-67:** the rejected alternatives remain rejection of a new release-match refusal at acceptance, leaving the applicable role trusted, and refreshing start subjects. They do not reject the pre-existing below-quorum refusal preserved in S3, or erase Clock and earlier-standing outcomes.
- **§5, successor:71-72:** charged-or-covered work, bounds, controls and size_of sizes remain owed to implementation review. The separate ceiling unit remains separate. There is no allocation exemption or budget-constant change.
- **Kept §6 bullets, successor:78-83:** the subsequent “Amendments to these controls” expressly qualify them. C-SR-2's component:revoked comparator is the ordinary case with preceding checks passing; amended C-SR-2 requires actual earlier core/index outcomes for the crossed cases, including expired/stale variants. C-SR-5's same-version/unrelated negatives apply after successful current-view admission with no other revoking match, as amended, rather than overriding S2. C-SR-6's amended charged-or-covered proof alternative must meet §5's bound/control obligation; it is not a waiver of accounting. C-SR-1's confirming mode is covered through C-SR-2. Retaining the original bullets with these explicit amendments does not reinstate the unconditional readings rejected in r3.

S1 through S4 are therefore adoptable as now composed. The original §3 blanket claim has been replaced, not merely contradicted by an appended note. Existing and newly recognized matches, earlier failures, H/D mismatches, dropped-start components, current-only components, and budget-boundary obligations now retain the r3 dispositions.

## 3. Additional plan edits

The additions accurately convey the r3 findings:

- PLAN-r3:62 names the affected S4 rows. Line 66 distinguishes evidence-floor checks 1/2 from the later held-fence check 3, includes observation/evaluator/publication failures, and qualifies the old write-ahead as required **if any**. Read the short table at :59 with that explicit qualification; it is not a promise of an unconditional old-path write.
- PLAN-r3:91 narrows the matrix fix to the missing diagnostic and existing bounded ChangedDuringRead retry. It does not claim the uncaptured original cause is proven. Lines 118-119 retain supporting observations while expressly declining proof against timing/resource interaction. The two failures remain historical evidence.
- PLAN-r3:120 correctly calls successful stress/isolated counts summary evidence and does not equate a successful run with zero internal settled retries. No new execution result is introduced. Earlier gate identities remain those recorded and distinguished in REVIEW-r3.
- PLAN-r3:73-74 preserves the scoped “none found” conclusion, G15's different conditional-model ordering, and JRW RW-C18's authenticated-store premise. It does not claim exhaustive historical-archive coverage or authorize changing those reference pins.
- The successor pointer, review order and current manifest reference are updated without changing the production-code pin or the implementation funding obligation. The statement that the flake was reported to its owner is author-reported coordination, not a delivery receipt independently established by this review.

There are no new required findings. Item-1 acceptance does not cover integration, the rebase onto SEC-PREDRAW-1, or final-head validation. Successor adoptability does not itself adopt or bind the law, authorize bypassing the coordinator's receipt, approve item-2 code/funding, or establish publisher execution or qualification. Only REVIEW-r4.md is written.

ITEM-1: ACCEPT
SECHARDEN-RELEASE-SUCCESSOR: ADOPTABLE
