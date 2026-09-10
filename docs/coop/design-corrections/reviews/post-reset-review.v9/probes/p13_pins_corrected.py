"""v9 probe 13 - pin authentication, corrected.

p12's tamper test was INVALID for foundation, security and workflows: those runners require
--report, so they exited 2 on an argparse usage error, not on a pin check. Only native genuinely
reported 'sha256 mismatch'. Reviewer harness error, not a product defect.

Here every runner gets its required arguments, each tamper run is paired with an UNTAMPERED
CONTROL on the same throwaway copy, and the refusal text is inspected for an actual pin fault.
"""
import hashlib, json, shutil, subprocess, tempfile
from pathlib import Path

SUB = Path('/tmp/opensip-design-corrections/candidate-subject.v9')
PY = '/tmp/opensip-architecture-review-env/bin/python'
DCR = 'docs/coop/design-corrections/'
WANTED = ['delivery.v4.json', 'fact-plane.v1.json', 'fact-identity-policy.v2.json', 'resolved-inputs.v2.json']
RUNNERS = {
    'foundation': ('foundation/run-reference-checks.py', ['--report', DCR + 'foundation/validation-report.json']),
    'security': ('security/check-security-lifecycle.v1.py', ['--report', DCR + 'security/security-lifecycle-report.v1.json']),
    'native': ('native/check_native_evidence.v2.py', []),
    'workflows': ('workflows/run-reference-checks.py', ['--report', DCR + 'workflows/workflows-validation-report.json']),
}
out = {'probe': 'p13_pins_corrected',
       'standing': 'independent reviewer probe; design/reference only',
       'harnessCorrection': 'p12 omitted --report for three runners, so its refusals were argparse '
                            'usage errors, not pin faults. Reviewer error, not a product defect.'}


def run(root, suite):
    rel, args = RUNNERS[suite]
    r = subprocess.run([PY, '-I', '-B', str(root / DCR / rel)] + args,
                       cwd=root, capture_output=True, text=True, timeout=300)
    return r.returncode, (r.stdout + r.stderr)


rows = []
for suite in RUNNERS:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / 'copy'
        shutil.copytree(SUB, root)
        code, blob = run(root, suite)
        rows.append({'suite': suite, 'case': 'CONTROL-untampered', 'exitCode': code,
                     'passed': code == 0, 'tail': blob.strip()[-160:]})
    for artifact in WANTED:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / 'copy'
            shutil.copytree(SUB, root)
            t = root / 'docs/coop/artifacts' / artifact
            t.write_bytes(t.read_bytes().replace(b'{', b'{ ', 1))
            code, blob = run(root, suite)
            up = blob.upper()
            rows.append({'suite': suite, 'case': 'TAMPER-' + artifact, 'exitCode': code,
                         'refused': code != 0,
                         'reportsPinFault': ('SHA256 MISMATCH' in up or 'PIN' in up),
                         'tail': blob.strip()[-260:]})
out['rows'] = rows
controls = [r for r in rows if r['case'] == 'CONTROL-untampered']
tampers = [r for r in rows if r['case'].startswith('TAMPER')]
out['summary'] = {
    'allControlsPass': all(r['passed'] for r in controls),
    'allTampersRefuse': all(r['refused'] for r in tampers),
    'allTampersReportAPinFault': all(r['reportsPinFault'] for r in tampers),
    'tamperCount': len(tampers),
    'suitesFailingToAuthenticate': sorted({r['suite'] for r in tampers
                                           if not (r['refused'] and r['reportsPinFault'])}),
}
print(json.dumps(out, indent=1))
