"""Replay every freshly reminted export through the frozen owner named by --source.

Uses the BUNDLED check-export.v4.py transport/driver from the package. Retains the full
per-Run report for each group, and records which registered native schema digest each store
actually carries.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ENV = '/tmp/opensip-architecture-review-env/bin/python'
R = Path('/private/tmp/opensip-design-corrections/claude-author-remint.v1')

GROUPS = [('checkpoint3', 'a-checkpoint3/checkpoint3', False),
          ('normalized-examples6', 'b-normalized/normalized-examples6', False),
          ('rust-selection-examples1', 'c-rust-selection/rust-selection-examples1', False),
          ('semantic-controls1', 'd-controls/semantic-controls1', True)]

OLD_DIGEST = 'd8e9a1fcaa980ef397eb9f3c6b294a546783c4155fd924d0a1290eef1de71728'


def main():
    outroot = Path(sys.argv[1]).resolve()
    source = Path(sys.argv[2]).resolve()
    package = Path(sys.argv[3]).resolve()
    reportdir = Path(sys.argv[4]).resolve()
    reportdir.mkdir(parents=True, exist_ok=True)
    new_digest = hashlib.sha256(
        (source / 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json').read_bytes()).hexdigest()

    summary = {'standing': 'AUTHOR replay of freshly reminted exports through the frozen owner '
                           'named by --source. Not independent reconstruction, not acceptance.',
               'source': str(source), 'registeredNativeSchemaSha256': new_digest, 'groups': []}
    allok = True
    for name, rel, negative in GROUPS:
        d = outroot / rel
        out = reportdir / ('owner-' + name)
        if out.exists():
            shutil.rmtree(out)
        cmd = [ENV, '-I', '-B', str(package / 'check-export.v4.py'),
               '--input', str(d), '--claims', str(d / 'claims.json'),
               '--source', str(source), '--out', str(out)]
        p = subprocess.run(cmd, capture_output=True, text=True)
        rep = json.loads((out / 'report.json').read_text())
        rows = []
        for c in rep['checks']:
            store = json.loads((d / c['path']).read_text())
            txt = json.dumps(store)
            rows.append({'name': c['name'], 'runId': c['claimedRunId'],
                         'ownerAdmission': c['ownerAdmission'],
                         'semanticAdmission': c['semanticAdmission'],
                         'reason': c.get('reason'),
                         'carriesNewSchemaDigest': new_digest in txt,
                         'carriesOldSchemaDigest': OLD_DIGEST in txt})
        if negative:
            ok = (p.returncode == 1 and len(rows) == 3
                  and all(r['ownerAdmission'] == 'ADMIT' and r['semanticAdmission'] == 'REFUSE'
                          for r in rows))
        else:
            ok = (p.returncode == 0 and rep['passed'] is True
                  and all(r['ownerAdmission'] == 'ADMIT' and r['semanticAdmission'] == 'ADMIT'
                          for r in rows))
        allok = allok and ok
        summary['groups'].append({'group': name, 'negativeControls': negative, 'passed': ok,
                                  'count': len(rows), 'reportPath': str(out / 'report.json'),
                                  'reportSha256': hashlib.sha256((out / 'report.json').read_bytes()).hexdigest(),
                                  'runs': rows})
        print('== %-26s passed=%-6s count=%s' % (name, ok, len(rows)))
        for r in rows:
            print('   %-24s owner=%-7s semantic=%-7s newDigest=%-6s oldDigest=%-6s %s'
                  % (r['name'], r['ownerAdmission'], r['semanticAdmission'],
                     r['carriesNewSchemaDigest'], r['carriesOldSchemaDigest'],
                     (r['reason'] or '')[:64]))
    summary['passed'] = allok
    json.dump(summary, open(reportdir / 'replay-summary.json', 'w'), indent=1)
    print()
    print('all groups as intended:', allok)
    return 0 if allok else 1


if __name__ == '__main__':
    raise SystemExit(main())
