# Control C9 - apply the minimal OWNER patches against candidate25, and the minimal patches
# against root's latest planning inputs.
#
# Reads Source25 and the planning inputs READ-ONLY. Writes patched copies and unified diffs into
# scratch only. Never modifies Source25, a live repository, product code or a historical document.
#
# usage: python apply-owner-patches.py <source25Root> <runtimeRoot>
import difflib
import hashlib
import json
import os
import sys

SRC, ROOT = sys.argv[1], sys.argv[2]
PATCHED = os.path.join(ROOT, 'scratch', 'patched')
PATCHES = os.path.join(ROOT, 'scratch', 'patches')
PROPOSAL = os.path.join(ROOT, 'scratch', 'proposal')
os.makedirs(PATCHED, exist_ok=True)
os.makedirs(PATCHES, exist_ok=True)

report = {'control': 'c9-apply-owner-patches', 'ownerFiles': [], 'planningFiles': []}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def emit(bucket, rel, before, after_text, srcLabel):
    after = after_text.encode('utf-8')
    out = os.path.join(PATCHED, rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'wb') as fh:
        fh.write(after)
    diff = ''.join(difflib.unified_diff(
        before.decode('utf-8').splitlines(keepends=True),
        after_text.splitlines(keepends=True),
        fromfile='a/' + rel, tofile='b/' + rel, n=3))
    pname = rel.replace('/', '__') + '.patch'
    with open(os.path.join(PATCHES, pname), 'w', encoding='utf-8') as fh:
        fh.write(diff)
    report[bucket].append({
        'path': rel, 'source': srcLabel,
        'beforeSha256': sha(before), 'beforeBytes': len(before),
        'afterSha256': sha(after), 'afterBytes': len(after),
        'patch': 'scratch/patches/' + pname,
        'addedLines': sum(1 for l in diff.splitlines()
                          if l.startswith('+') and not l.startswith('+++')),
        'removedLines': sum(1 for l in diff.splitlines()
                            if l.startswith('-') and not l.startswith('---')),
    })


def anchored(text, edits):
    for anchor, replacement in edits:
        assert text.count(anchor) == 1, 'anchor not unique: ' + anchor[:70]
        text = text.replace(anchor, replacement)
    return text


# =========================================================== owner 1: identity and evidence
IDR = 'docs/v2/contracts/product-v1/identity-and-evidence.md'
before = open(os.path.join(SRC, IDR), 'rb').read()
text = before.decode('utf-8')

E1_A = 'with uniqueness checked in the corresponding operational ledger before use.'
E1_B = E1_A + (
    '\nThat reservation additionally carries a **monotone attempt phase**. `AttemptCustodyV1`\n'
    '(private, ledger-owned) extends the existing reservation row with\n'
    '`{phase: admitted | settled, settledOutcome: null | committed | refused | undetermined,\n'
    'operationRef}`; `admitted → settled` is the only transition, it is never reversed, deleted or\n'
    're-opened, and the settle write is ordered **after** the receipt write. It authorizes nothing:\n'
    'settling records an outcome and never licenses a retry, so a settled ExecutionId stays\n'
    'terminal. `operationRef` here is the durable home of the `executionId ↔ operationRef`\n'
    'correlation for attempts that never commit, which is why no field is added to the closed\n'
    'schema-3 `JournalRecord` to correlate a pending `REV`.')

E2_A = 'mutation. Duplicate retry can share a Run but has a separate attempt receipt.'
E2_B = E2_A + (
    '\n\n**Read-only recovery selectors.** `recover(ExecutionId)` takes the `SHARED-READ` lease and\n'
    'reads **one** consistent committed ledger snapshot carrying the receipt, the private\n'
    'recovery association **and** the `AttemptCustodyV1` phase together. Terminality is decided\n'
    'inside that single snapshot and never from a separately timed liveness probe or an in-memory\n'
    'active set: receipt absent with phase `settled` is the failed answer; phase `admitted` is\n'
    '`unknown-attempt-open`; no attempt row is `unknown-attempt-unobserved`. Carrier observations\n'
    '(journal tail, witness, SC-TRUST floor) are captured with before/after stability brackets and\n'
    'at most one fresh journal retry. It performs no witness INIT/REVERT/ADVANCE, no high-water\n'
    'raise, no store-binding allocation, no new execution grant, no fence acquisition and no wait\n'
    'on a writer. Security §S6 and §S9 own the exact carrier rules; the bounded algorithm is\n'
    '`architecture/commit-recovery-readonly.v2.md`.\n\n'
    '**Narrow assurance limit, stated here because recovery is often read as proof.** Confirming a\n'
    'historical commit from the retained carrier establishes that the sealing record is present\n'
    'with its joined digest, operation reference and Run identity, that the sequence is\n'
    'contiguous, and that no rollback below the last **observed** operation boundary occurred. It\n'
    'does **not** cryptographically authenticate the interior record prefix: the inherited chain\n'
    'value binds only the immediately previous body digest and index, and the witness names the\n'
    'tail body digest, so an interior substitution is not detected by either. The conclusion class\n'
    'is therefore a cryptographic proof of the retained prefix, and an unmet\n'
    'anchor is reported `unknown`, never as invalidation of an earlier committed receipt.')

E3_A = ('Read-only `recover(ExecutionId)` inspects the committed\n'
        'receipt after a lost acknowledgement and never repeats effects.')
E3_B = ('Read-only `recover(ExecutionId)` inspects the committed\n'
        'receipt after a lost acknowledgement and never repeats effects. Where **no** receipt is\n'
        'present it reports the §5 selectors rather than inferring absence: only the ledger-owned\n'
        '`settled` phase in that same snapshot establishes that the attempt did not commit, and an\n'
        'attempt still `admitted` stays unknown until an authorized sweep settles it.')

text = anchored(text, [(E1_A, E1_B), (E2_A, E2_B), (E3_A, E3_B)])
emit('ownerFiles', IDR, before, text, 'candidate25')

# =========================================================== owner 2: security and lifecycle
SECR = 'docs/v2/contracts/product-v1/security-and-lifecycle.md'
before = open(os.path.join(SRC, SECR), 'rb').read()
text = before.decode('utf-8')

S1_A = 'Grant tokens and root compatibility schema 2 are a different axis and stay. |'
S1_B = (S1_A + '\n'
        '| `security-schemas.v2/grant-journal.sql` physical carrier | 14 record types including '
        '`TERMINAL`, no `SEAL`, four display-alias platform values | retained as the immutable '
        'historical physical carrier. The **selected product physical carrier** is '
        '`design-corrections/security/grant-journal.carrier.v3.sql` (**carrierFormat 3**) with '
        'dispatch `carrier-dispatch.v3.json` and prose `carrier-format.v3.md`. `carrierFormat` is '
        'a third axis, distinct from `recordSchema` and from the S9 `stateSchema`; no historical '
        'row is rewritten, relabelled or re-admitted as current. |')

S6_A = 'not mint it.'
S6_B = (
    'not mint it.\n\n'
    '**Commit-admission gate (one atomic bit state).** `ADMITTED = 1`, `LATCHED = 2`: `0` is\n'
    'preparing, `1` admitted, `2` latched before admission, `3` admitted then latched. Commit\n'
    'admission is a compare-exchange `0 → 1`; the observer always fetch-ORs `2`, including\n'
    '`1 → 3`, so a post-admission latch cannot be lost. No state resets during the attempt. A\n'
    'successful gate mints one internal single-use permit for the already prepared commit and is\n'
    'not a reusable grant for later effects. A latch winning at state `0` prevents the gate\n'
    'entirely. State `3` does **not** revoke the already admitted attempt or relabel its outcome:\n'
    'it records the latch and forbids further effect admission or retries. The observer bound\n'
    'bounds admitting new effects; it cannot abort an in-flight syscall or rewrite its outcome. A\n'
    'confirmed durable commit stays committed; an uncertain commit or barrier stays\n'
    'durability-undetermined with its ExecutionId and no automatic write retry. The gate orders\n'
    'admission only and is not the durability point.\n\n'
    '**`REV` after `SEAL` is not a refusal.** The linearization law above constrains one\n'
    'direction only: after `REV` no `RA`, intent, commit or `SEAL` is appended. It does not follow\n'
    'that a `REV` appearing later in sequence order refuses an earlier `SEAL`. Durable commitment\n'
    'is established solely by the guarded evidence-ledger receipt and its private association. A\n'
    'reader must not infer refusal from record order, and no member is added to the closed\n'
    'schema-3 `JournalRecord` to carry that correlation: the private association and the\n'
    '`AttemptCustodyV1` `executionId ↔ operationRef` mapping (identity §2) are its lawful home.\n\n'
    '**Required delivery is a separate phase.** On any end path security returns a stopped\n'
    'cleanup-only session. Required rendering and delivery draw no authority from it: they are a\n'
    'read-and-materialise activity in `SHARED-READ` mode (S7), not a brokered effect. The handoff\n'
    'is: cleanup `REV`/`CLN` through a fresh lawful level-3 then level-4 append while the stopped\n'
    'session still holds the operation lease; release the lease; ordinary S7 end handoff; then a\n'
    'new `SHARED-READ` phase over the committed snapshot. A latched attempt (state `2` or `3`)\n'
    'starts no delivery phase and cannot reacquire authority that way; for state `3` the commit\n'
    'stays committed with its RunId observable and the required delivery is reported failed\n'
    'through the existing `DELIVERY.REQUIRED_FAILED` path.')

S9_A = 'EXCLUSIVE. Both stages keep the metadata profile of S2.'
S9_B = (S9_A + '\n\n'
        '**Physical carrier bridge (carrierFormat).** The project grant-journal carrier has its\n'
        'own format axis, and it is not the state schema. Detection on open is by schema\n'
        'introspection only, because the oldest format carries no version row. Reader staging\n'
        'mirrors the root-reader and state-decoder pattern: a core supporting only carrierFormat\n'
        '{1, 2} refuses a carrierFormat 3 carrier **typed** and keeps its prior generation until it\n'
        'expires; a carrierFormat {1, 2, 3} core reads both, under recordSchema-1 semantics for\n'
        'historical generations and recordSchema-3 for current ones. A historical `platform` value\n'
        'is surfaced as a historical alias and is never presented as an S8 machine id, rewritten,\n'
        'or joined to `RepoExecutionGrantV2.platformId`. Migration 1 or 2 → 3 runs under the fence\n'
        'with `EXCLUSIVE` on the affected namespace, is additive, disables no inherited constraint\n'
        'or trigger, and rewrites no inherited row.\n\n'
        '**Grant-generation closure gains a third cause.** The inherited rule (security v8 §5.4\n'
        'WA-13, retained unchanged as historical text) advances `grantGeneration` only on\n'
        'whole-generation `REV` and on the uint53 rollover. Carrier-format migration is a third\n'
        'cause of generation closure. It reuses the existing typed `TERMINAL` cause\n'
        '`grantGenerationClosure` and changes no schema, enum or wire major. Floors copy forward\n'
        'unchanged and a poisoned floor is not lowered; only S4.5 lowers it.')

S12_A = '| `OBSERVER.FAIL_STOP`, I/O failure | operational-failed / 4 / `HOST.IO_FAILURE` |'
S12_B = (S12_A + '\n'
         '| read-only recovery: requested attempt still `admitted`, or observations temporally '
         'skewed beyond the single permitted retry | operational-failed / 4 / '
         '`LEDGER.BUSY_TIMEOUT` (detail `PROJECT.BUSY`) |\n'
         '| read-only recovery: stably observed carrier quarantine condition '
         '(`uncertainTailLoss`, `witnesslessRestore`, `witnessMalformed`) | operational-failed / '
         '4 / `LEDGER.CORRUPT` |\n'
         '| read-only recovery: requested binding names a foreign carrier or a swapped '
         'store/namespace | request-rejected / 2 / `EXTENSION.ADMISSION_REJECTED` (detail '
         '`RECOVERY.REFUSED`, typed subject) |')

text = anchored(text, [(S1_A, S1_B), (S6_A, S6_B), (S9_A, S9_B), (S12_A, S12_B)])
emit('ownerFiles', SECR, before, text, 'candidate25')

# =========================================================== planning input 1: the plan JSON
PLAN = 'commit-recovery-plan.v1.json'
before = open(os.path.join(ROOT, PLAN), 'rb').read()
plan = json.loads(before.decode('utf-8'))
new = json.load(open(os.path.join(PROPOSAL, 'carrier-fault-cases.v1.json'), encoding='utf-8'))

existing = [c['id'] for c in plan['cases']]
assert len(existing) == new['existingCaseCount'], (len(existing), new['existingCaseCount'])
assert len(new['cases']) == new['addedCaseCount']
for c in new['cases']:
    assert c['id'] not in existing, c['id']
KEYS = ['id', 'checkpoint', 'possibleStoredState', 'initialConclusion',
        'expectedBehavior', 'verificationOwner', 'executionStanding']
assert list(plan['cases'][0].keys()) == KEYS

# root's F32 fix must survive untouched
f32 = [c for c in plan['cases'] if c['id'] == 'F32'][0]
assert 'CarrierCapacityExhausted' in f32['expectedBehavior']
assert f32['verificationOwner'] == 'crates/host/tests/retention_tests.rs'
report['rootF32FixPreserved'] = True

for c in new['cases']:
    plan['cases'].append({k: c[k] for k in KEYS})
plan['standing'] = (plan['standing'].rstrip('.') +
                    '. Extended by the carrierFormat 3 correction with cases F38-F49; every '
                    'added case is not-executed.')
after_plan = json.dumps(plan, indent=2, ensure_ascii=False) + '\n'
emit('planningFiles', PLAN, before, after_plan, 'root latest planning input')

# =========================================================== planning input 2: the build plan
MD = 'implementation-boundaries-and-build-plan.md'
before = open(os.path.join(ROOT, MD), 'rb').read()
text = before.decode('utf-8')

A1 = 'Do not disable SQL checks or relabel old rows as current.'
A1N = A1 + (
    '\n**COV-03 resolved (proposed, not accepted):** the versioned carrier is\n'
    '`docs/coop/design-corrections/security/carrier-format.v3.md` with DDL\n'
    '`grant-journal.carrier.v3.sql` and dispatch `carrier-dispatch.v3.json`, selected by security\n'
    '§S1 and bridged by §S9. It adds `carrierFormat` as an axis distinct from `recordSchema` and\n'
    '`stateSchema`, carries TERMINAL as the frozen recordSchema-1 body so schema 3 is not widened,\n'
    'uses the four S8 machine ids, and migrates additively. The inherited carrier is incompatible\n'
    'in exactly two ways, both measured: the `SEAL` record type, and the three alias-only machine\n'
    'platform ids on a GRANT. Eight of the nine schema-3 operational record types insert cleanly.')

A2 = 'then a new read-only recovery can retry.'
A2N = A2 + (
    ' The exact bounded algorithm is\n'
    '`docs/v2/architecture/commit-recovery-readonly.v2.md`. Carrier observations are captured with\n'
    'before/after stability brackets and at most one fresh journal retry; an owner quarantine\n'
    'condition is reportable only from stable brackets plus two agreeing tail observations, so a\n'
    'temporally skewed observation is attributed to busy rather than corruption. Terminality of an\n'
    'attempt comes from the ledger-owned `AttemptCustodyV1` phase read in the same snapshot as the\n'
    'receipt, never from an in-memory active set. A confirming result is\n'
    '`confirmed-under-retained-custody`, never a cryptographic proof of the interior prefix.')

END = '<!-- END GENERATED COMMIT RECOVERY -->'
rows = ''.join('| %s — %s | %s | %s: %s |\n' % (
    c['id'], c['checkpoint'], c['possibleStoredState'], c['initialConclusion'],
    c['expectedBehavior']) for c in new['cases'])
marker = '\n\n' + END

text = anchored(text, [(A1, A1N), (A2, A2N), (marker, '\n' + rows + '\n' + END)])
emit('planningFiles', MD, before, text, 'root latest planning input')

report['note'] = (
    'Only two candidate25 owner files are patched, and neither is historical: '
    'security-completion.v1.md, security-completion.v8.md, grant-journal.sql, the '
    'journal-record schemas and security-lifecycle.schemas.v1.json are all untouched. The '
    'failure-matrix rows sit inside the generated block and were regenerated in the same row '
    'format the existing rows use; the project generator must be re-run at integration.')
out = os.path.join(ROOT, 'scratch', 'out', 'c9-patches.json')
with open(out, 'w', encoding='utf-8') as fh:
    fh.write(json.dumps(report, indent=1) + '\n')
print('WROTE', out)
for bucket in ('ownerFiles', 'planningFiles'):
    print('--', bucket)
    for f in report[bucket]:
        print('  ', f['path'], '+%d/-%d' % (f['addedLines'], f['removedLines']))
        print('      before', f['beforeSha256'], f['beforeBytes'])
        print('      after ', f['afterSha256'], f['afterBytes'])
print('root F32 fix preserved:', report.get('rootF32FixPreserved'))
