"""Launch a FRESH independent final application review. Not executed by this preparation.

Vendor CLI and public stdout name come from the bound receipt / launch block.
Coauthor sessions must not be resumed. Write only the application-review output dir.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import coverage_contract as C

p = argparse.ArgumentParser()
p.add_argument('--root', type=Path, required=True)
p.add_argument('--stage', type=Path, required=True)
p.add_argument('--version', required=True)
p.add_argument('--bound-receipt', type=Path, required=True)
a = p.parse_args()
root = a.root.resolve()
stage = a.stage.resolve()
bound = json.loads(a.bound_receipt.read_text())
assert bound.get('readyForAssembly') is True
assert bound['applicationVersion'] == a.version
vendor = bound['vendor']
reviewer_label = bound['reviewerPublicLabel']
launch = bound.get('launch') or {}
manifest = stage / ('application-subject.' + a.version + '.json')
digest = hashlib.sha256(manifest.read_bytes()).hexdigest()
out = stage.parent / ('application-review.' + a.version)
out.mkdir(exist_ok=False)
app = json.loads((stage / 'files/docs/coop/design-corrections/application.v1.json').read_text())
design_snapshot = app['designSnapshotRoot']
design_ref = app['independentDesignReview']
blind_ref = app['freshBlindConsumerReview']
if vendor == 'grok':
    cli = launch.get('cli', '/Users/sb/.grok/bin/grok')
    stdout_name = launch.get('stdoutName', 'response.raw.json')
    permission = launch.get('permissionMode', 'dontAsk')
    max_turns = str(launch.get('maxTurns', 60))
    args = [
        cli,
        '--cwd',
        str(stage),
        '--permission-mode',
        permission,
        '--no-subagents',
        '--disable-web-search',
        '--max-turns',
        max_turns,
        '--output-format',
        'json',
        '--prompt-file',
        str(out / 'prompt.txt'),
    ]
elif vendor == 'claude':
    cli = launch.get('cli', '/Users/sb/.local/bin/claude')
    stdout_name = launch.get('stdoutName', 'response.json')
    args = [
        cli,
        '-p',
        '--model',
        'opus',
        '--effort',
        'high',
        '--permission-mode',
        'dontAsk',
        '--tools',
        'Read,Grep,Glob,Write,Bash',
        '--allowedTools',
        'Read',
        'Grep',
        'Glob',
        'Bash',
        'Write',
        '--strict-mcp-config',
        '--output-format',
        'json',
    ]
else:
    raise SystemExit('unknown vendor')
prompt = f'''You are {reviewer_label} in a FRESH INDEPENDENT FINAL APPLICATION REVIEW session. You authored NONE of these bytes and did not conduct the design or blind reviews. Coauthor sessions are not this review and must not be resumed. User requires actual independent {vendor} and Codex alignment. No product implementation, fixes, commit, push or agents. Read autonomously, write ONLY {out}, including disposable probes. Never change frozen package, repository, or evidence.

Review the COMPLETE proposed application package {stage}. Manifest {manifest}, SHA256 {digest}. Verify manifest and EVERY files, beforeImages and support entry by its path convention; reverify at finish. Files/ contains prospective exact current documentation and applied design/readiness records; before/ preserves working-tree before-images; support/ contains assembly scripts and executed validation/provenance evidence. Read manifest's path definitions. Repository {root} supplies retained dependencies; the accepted design snapshot is {design_snapshot}. Check exact hashes and evidence, not asserted labels. Python /tmp/opensip-architecture-review-env/bin/python -I -B is available. No inherited acceptance is automatically extended. Historical Claude source21 ACCEPT does not accept a changed successor.

Prerequisites MUST be substantive actual review evidence: accepted independent design review {design_ref}, Codex coauthor assent with correct limitation, fresh blind consumer B {blind_ref} from separate actual session with independently authored canonical/descriptor/Run vectors and read custody. Review these exact retained inputs, including substantive findings and limitations. Normative product contract/schema/model bytes must match the actual accepted design subject and blind parent. Any semantic change needs new design and blind review, not application-only assent.

The earlier incomplete application was rejected in docs/coop/design-corrections/reviews/application-review.v1/application-review.md/json. Independently verify ALL M1..M7, S1..S6, and BOTH A1/A2 are individually accounted, with exact selectors and explicit findings. The old stage.v2 is historical/rejected. This is a new full package after real design+blind review. Review all28 condition2 rows and mappings, six inherited source accounts, all30 evaluation subresiduals, DR001..011/DR011-R01..16, all AR01..16/FW01..15, five NEW scoped DR201..205 dispositions, and32 implementation/release gates. Each grade must be justified by its actual contract and review, not merely a count or broad link. IMPORTANT: the historical v12 design reviewer explicitly records all27 inherited rows and all30 evaluation subresiduals as CARRIED-UNCHANGED and says it did NOT grade, close or discharge them; DR201..205 acceptance covers routing only. Inspect the actual accepted successor review independently for its exact scope and authority too. Historical v13/v21 owner rows may be ROUTING-ASSESSED-ONLY-NOT-APPLIED or ROUTED-ONLY with both authority flags false. These are literal limitations to preserve, not new grades. Your final application review must substantively grade every proposed AR/FW outcome as well as all inherited, per-row and owner outcomes against the actual normative sources and applicable prior review basis. Applied wrappers preserve those literal dispositions and bind proposed grades to YOUR new final application review and eventual activation. Substantively assess each proposed grade using exact normative contracts and applicable prior review basis; never turn CARRIED-UNCHANGED or routing-only acceptance into a grade by inference. Assess the v12-A1 count-account requirement against the actual accepted successor measurement and application referenceEvidenceSummary (passing calls, distinct IDs and duplicate extra instances), plus v12-A2 relative-source reproduction commands with exact source pins. Historical767/757/10 belongs to v12 only; use the actual selected subject counts and preserve original evidence. Validate both recorded exact relative sources and normalized historical absolute-source forms. Specifically DR106 admission2/3/securityS9.1/G06/G11; G11on109/113/124; DR117 admission5 seven boundary obligations; DR130 securityS16/file05 exact preservation5/distinctions5/prohibitions6; DR122 actual D372 SARIF/G17 scope re-entry. G06/G11/G10/G17 current obligations must reconcile historical register/table language. Mandatory future qualification is not claimed complete. Condition5 remains NOT MET and no implementation is authorized.

Explicitly assess D9-APP-1 against the bounded historical actual-Claude D9 assessment and Codex's qualified assessment retained in support/d9-obligation-evidence. Do not relabel that historical Claude D9 bundle as a Grok session. The broad claim that no application record carries the obligation was incorrect: CB-ADV-4 in the accepted advisory account is dynamically copied by the assembler. The added row-specific carriedCrossUnitObligation on exactly DR-007 and DR-011-R08 must preserve the mandatory live D9 successor-artifact obligation, its owner, exact host-invariant to SYSTEM.OUTCOME.ILLEGAL_STATE mapping and inherited artifact hash. Determine whether the selected current composition is complete from actual normative selectors; distinguish that from the undisclosed completion of future owning-unit artifact integration or qualification. Condition 1 MET, ACCEPT-DESIGN, activation and your application review must not discharge that obligation. The phase label is a planning classification, not a verbatim normative phase requirement or a new restriction on the user's architecture authorization. Assess the actual generated records, not only static strings in the builder. Do not infer a prospective grade from a historical HARD-BLOCKED table. The bounded assessor did not execute integration checks or conduct final application review. D9 is a carried implementation-unit obligation, not a design-level blocker.

Review every staged current Markdown edit and applying D372 body. One complete intended product design implemented in stages; historical preview grades remain bounded, chronology clearly historical. START-HERE topic walkthrough, dated snapshot forward pointer, current root README, central register, source map, generated catalog and inventories must agree. Check local links/anchors including the explicit external activation target created LAST by the reviewed finalizer. It does not exist before application and must not be represented as already existing evidence. It is a reviewed deterministic output.

Hash-cycle mechanism: application.v1 and coordinator body are frozen prospective bytes. They name an EXTERNAL application-activation.v1.json. Finalizer requires your ACTUAL ACCEPT bound to this manifest and exact review hash, verifies all staged hashes and unchanged live before-images (or exact after-images for interrupted copy resume), then applies only reviewed documentation and creates activation LAST. Only that verified activation makes grades/act effective. Assess the exact finalizer code/procedure; do not demand the not-yet-produced review hash be embedded in its own subject. Conversely reject false accepted claims without a coherent actual post-review binding. Final JSON MUST expose top-level verdict and subjectManifestSha256 for this procedure. Reviewed manifest/source archive/review will be retained before activation. No user permission needed beyond existing architecture authorization. The earlier application A2 explicitly notes untracked link targets. This is an authorized working-tree delivery only: commit, push and publication are excluded. Account that limitation explicitly; do not claim the committed tree alone contains the delivered design or silently close A2 by committing. The old A1 anchor defect must retain its actual inherited or corrected disposition.

Inspect inventory/classification/generator correctness and scoped exclusions without claiming exhaustive historic inbound counts. Exact before-images must preserve preexisting working-tree changes. Inspect prospective native source-pin delta (only two documentation provenance hashes unless the freeze evidence shows a reviewed different set), actual source-pinned native report rerun and other current checks. Accepted original manifest/report preserved; no silent historical repin. Integration checker pinned by whole accepted subject and exact application reference. Account any NEW nonblocking advisories from the accepted fresh blind result as well as independent design advisories; earlier accounts do not silently cover later findings. Preserve historical original bypass evidence and separately retained final-source rechecks. Application semantic sources must come from the frozen accepted snapshot, and multiple native contexts per language must not be misrepresented as a scalar. 32 product gates remain unperformed and are separate from design acceptance.

Deliver {out}/review.md AND review.json with substantive ACCEPT / CHANGES_REQUIRED / BLOCKED, top-level subjectManifestSha256='{digest}', all previous finding dispositions, per-row/gate/scoped review assessments, any MUST/SHOULD/advisories with exact selectors, independent probes/checks, counts and limitations. ACCEPT requires no unresolved MUST/SHOULD application/design issue. Include top-level newMustIssues and newShouldIssues arrays, both empty for ACCEPT; an absent or malformed account is not application authority. Reverify subject bytes. Work thoroughly and conclude with actual verdict. This is a final application review, not a new author pass or blind consumer substitute.'''
(out / 'prompt.txt').write_text(prompt)
stdout_path = out / stdout_name
proc = subprocess.Popen(
    args,
    stdin=subprocess.PIPE if vendor == 'claude' else None,
    stdout=stdout_path.open('wb'),
    stderr=(out / 'stderr.log').open('wb'),
    cwd=stage,
    start_new_session=True,
)
if vendor == 'claude':
    proc.stdin.write(prompt.encode())
    proc.stdin.close()
(out / 'process.json').write_text(
    json.dumps(
        {
            'pid': proc.pid,
            'manifestSha256': digest,
            'startedAt': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'command': args,
            'vendor': vendor,
            'stdoutName': stdout_name,
            'knownCoauthorSessionsExcluded': list(C.KNOWN_GROK_COAUTHOR_SESSIONS),
            'standing': 'Independent application review launch metadata; not a verdict.',
        },
        indent=2,
    )
    + '\n'
)
print(proc.pid, digest, vendor, stdout_name)
