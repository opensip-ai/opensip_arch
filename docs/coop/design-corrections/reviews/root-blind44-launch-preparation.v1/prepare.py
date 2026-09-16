"""Prepare current normative-only continuation after completed predecessor custody.

Never launches, repairs exports, changes consumer helpers, or grants acceptance.
"""
from pathlib import Path
import ast
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--source-sha256',required=True);parser.add_argument('--kit-sha256',required=True);args=parser.parse_args()
import hashlib
import json
import shutil
import subprocess

B = Path('/tmp/opensip-design-corrections')
L = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
A = B / 'consumer-b.v24-source43.v1'
N = B / 'consumer-b.v24-source44.v1'
SID = '9d3dfb70-b2d3-498c-a3c1-f8de9e488514'
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
J = lambda p: json.loads(p.read_bytes())

assert J(A / 'process-completion.json')['exitCode'] == 0
assert J(A / 'result.json').get('is_error') is not True
assert (A / 'output/blind-review.json').is_file()
retained = L / A.name / 'final-public-artifact-manifest.json'
custody = J(retained)
assert custody['actualSessionId'] == SID
assert custody['subjectManifestSha256'] == H(L / 'candidate-subject.v43.json')
for row in custody['files']:
    p = A / row['runtimePath']
    assert H(p) == row['sha256'] and p.stat().st_size == row['bytes']
    q = L / A.name / row['retainedPath'] if 'retainedPath' in row else B / 'candidate-subject.v43' / row['sameAsSubjectPath']
    assert H(q) == row['sha256'] and q.stat().st_size == row['bytes']
ps = subprocess.run(['ps', '-axo', 'comm=,args='], capture_output=True, text=True, check=True).stdout
assert not any(r.strip().split()[0].endswith('/claude') and '--resume ' + SID in r for r in ps.splitlines() if r.strip())
source_hash = H(L / 'candidate-subject.v44.json')
assert source_hash == args.source_sha256
kit = N / 'subject/consumer-input-manifest.json'
k = J(kit)
assert k['parentSubjectSha256'] == source_hash
assert len(k['files']) == 105
for row in k['files']:
    p = N / 'subject' / row['path']
    assert H(p) == row['sha256'] and p.stat().st_size == row['bytes']
assert H(kit) == args.kit_sha256
assert not any((N / p).exists() for p in ['output', 'charter.md', 'requirements.json', 'prompt.md', 'launch.py'])

# Exact own-work transfer only. The independent consumer adapts its own paths/helpers.
shutil.copytree(A / 'output', N / 'output')
rows = []
for p in sorted((A / 'output').rglob('*')):
    if p.is_file():
        q = N / p.relative_to(A)
        assert H(p) == H(q)
        rows.append({'path': str(p.relative_to(A)), 'sha256': H(p), 'bytes': p.stat().st_size})
(N / 'copied-own-work.json').write_text(json.dumps({'source': str(A), 'standing': 'Exact completed own-work copy; no helper/export/result modification or fresh execution.', 'files': rows}, indent=2) + '\n')
old_prep = J(A / 'preparation.json')
def rewrite(text):
    for before, after in [(A.name, N.name), ('source43 reconstruction', 'source44 reconstruction'), (old_prep['sourceManifestSha256'], source_hash), (old_prep['kitManifestSha256'], H(kit))]:
        text = text.replace(before, after)
    return text
(N / 'charter.md').write_text(rewrite((A / 'charter.md').read_text()))
prior = J(A / 'requirements.json')
req = json.loads(rewrite((A / 'requirements.json').read_text()))
for group, count in [('requirements', 123), ('standing', 8), ('futureQualification', 3)]:
    assert len(req[group]) == count
    assert [r['id'] for r in req[group]] == [r['id'] for r in prior[group]]
(N / 'requirements.json').write_text(json.dumps(req, indent=2) + '\n')
prompt = f"""Continue ONLY your SAME originally fresh independent blind origin {SID} in NEW runtime {N}, on current source44 normative kit. Preserve every earlier runtime and historical result. Your own completed source43.v1 output has been copied exactly to output/; adapt its old absolute paths yourself before execution. This is your own work, not author assistance. Parent frozen subject SHA {source_hash}, subject/consumer-input-manifest.json SHA {H(kit)}; verify all105 members.

Read charter.md and requirements.json fully and inspect current normative owners, comparing with your OWN prior normative kit. Independently identify which original constructions and claims the new normative bytes affect, apply those owners and execute the affected requirements. Retain and assess the source43.v1 negotiated payload/exact-byte/request-batch work within the unchanged original scope. Keep all123 requirements,8 standing rules,3 future qualification items. No new complete Runs or product implementation is demanded. Unaffected exact prior measurements may be reused with precise source/helper/input custody and explicit reuse standing; do not relabel old executions as fresh. Every current claimed complete positive still needs exact exports, owning schema/registry/closure admission and independent complete proof replay.

No root outcomes, expected results, semantic diagnoses, author helpers, or other reviews supplied. Read ONLY this normative subject, this charter/requirements and your own current/prior work plus installed Python/jsonschema. Never read LIVE, other runtimes, author reference models/fixtures/reports, root results or private/session logs. Derive every expectation yourself from current normative owners. If a precise law is missing or contradictory, report its selectors; if your helper is wrong under a published law, correct only from the kit and preserve old failures. No subagents, commits/push, product, activation or acceptance claims about root work.

Write only this runtime output/. Use /tmp/opensip-architecture-review-env/bin/python -I -B. Record exact changed and reused artifacts and observations, full original-ID checkpoints, from-scratch replay command and final blind-review.md/json. Finish all children before final substantive report. ACCEPT-RECONSTRUCTABLE only when original charter conditions actually hold; otherwise precise CHANGES_REQUIRED or actual blocker. No arbitrary100turn limit or waiting/status-only completion. Root will separately assess exact current exports without repairing them; that result is unavailable to this blind review.
"""
(N / 'prompt.md').write_text(prompt)
launch = (A / 'launch.py').read_text()
node = next(n for n in ast.parse(launch).body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'cmd' for t in n.targets))
cmd = ast.literal_eval(node.value) + ['--add-dir', str(A)]
lines = launch.splitlines(True)
lines[node.lineno - 1:node.end_lineno] = ['cmd=' + repr(cmd) + '\n']
(N / 'launch.py').write_text(''.join(lines))
prep = {'standing': 'PREPARED UNLAUNCHED; original independent origin, current normative-only kit, exact own-work copy, no root oracle or acceptance.', 'sourceManifestSha256': source_hash, 'kitManifestSha256': H(kit), 'actualSessionId': SID, 'priorPublicManifestSha256': H(retained), 'copiedFiles': len(rows)}
for file in ['prompt.md', 'launch.py', 'charter.md', 'requirements.json', 'copied-own-work.json']:
    prep[file + 'Sha256'] = H(N / file)
(N / 'preparation.json').write_text(json.dumps(prep, indent=2) + '\n')
D = L / (N.name + '-dispatch')
D.mkdir()
for file in ['prompt.md', 'launch.py', 'charter.md', 'requirements.json', 'copied-own-work.json', 'preparation.json']:
    shutil.copyfile(N / file, D / file)
print(json.dumps(prep))
