"""PROBE J — cross-unit surface applicability, measured against the command inventory
rather than taken from three prose restatements.

Claims: HTML is advertised by exactly {default, analyze, fit, audit, candidates, inspect,
review-brief, repair-preview}; SARIF by exactly {default, analyze, audit, repair-verify};
every advertised SARIF command declares the six common parity fields; `capability-availability`
is a declared parity field of EVERY requestClass=analysis command; `query` advertises only
human/JSON/agent."""
import json, os, re, collections

ROOT = '/tmp/opensip-design-corrections/candidate-subject.v26'
DC = os.path.join(ROOT, 'docs/coop/design-corrections')
inv = json.load(open(os.path.join(DC, 'workflows/command-inventory.v3.json'), encoding='utf-8'))
R = {}
cmds = inv['commands']
R['command_count'] = len(cmds)
R['command_row_keys'] = sorted(cmds[0].keys())


def fmts(c):
    return set(c.get('formats') or c.get('renderers') or c.get('applicableFormats') or [])


allf = sorted({f for c in cmds for f in fmts(c)})
R['formats_seen'] = allf
html = sorted(c['name'] for c in cmds if 'html' in fmts(c))
sarif = sorted(c['name'] for c in cmds if 'sarif' in fmts(c))
R['html_commands'] = html
R['sarif_commands'] = sarif
R['html_matches_declared_eight'] = set(html) == {
    'default', 'analyze', 'fit', 'audit', 'candidates', 'inspect', 'review-brief', 'repair-preview'}
R['sarif_matches_declared_four'] = set(sarif) == {'default', 'analyze', 'audit', 'repair-verify'}
q = [c for c in cmds if c['name'] == 'query']
R['query_formats'] = sorted(fmts(q[0])) if q else None

SARIF_COMMON = {'run-id', 'verdict', 'required-coverage', 'deficiency', 'findings',
                'termination-class', 'retention-disclosure'}
R['sarif_commands_missing_common_parity'] = {
    c['name']: sorted(SARIF_COMMON - set(c.get('parityFields') or []))
    for c in cmds if 'sarif' in fmts(c) and SARIF_COMMON - set(c.get('parityFields') or [])}

analysis = [c for c in cmds if c.get('requestClass') == 'analysis']
R['analysis_commands'] = sorted(c['name'] for c in analysis)
R['analysis_commands_missing_capability_availability'] = sorted(
    c['name'] for c in analysis if 'capability-availability' not in (c.get('parityFields') or []))
R['non_analysis_commands_declaring_capability_availability'] = sorted(
    c['name'] for c in cmds if c.get('requestClass') != 'analysis'
    and 'capability-availability' in (c.get('parityFields') or []))

R['renderers'] = [{'format': r.get('format'), 'version': r.get('version')} for r in inv['renderers']]
ops = None
for k in ('queryOperations', 'operations'):
    if k in inv:
        ops = inv[k]
R['query_operation_count'] = len(ops) if ops else None

# prototype report rows
proto = open(os.path.join(ROOT, 'docs/v2/architecture/prototype-report-inventory.md'), encoding='utf-8').read()
rows = re.findall(r'^### (R\d\d) — (.*)$', proto, re.M)
disp = re.findall(r'\*\*Proposed disposition: (Preserve|Change)\.\*\*', proto)
R['report_feature_rows'] = len(rows)
R['report_feature_ids_contiguous'] = [r[0] for r in rows] == ['R%02d' % i for i in range(1, 25)]
R['report_dispositions'] = dict(collections.Counter(disp))
R['report_dispositions_total'] = len(disp)

# coverage reportFeatures must agree
cov = json.load(open(os.path.join(ROOT, 'docs/v2/architecture/implementation-coverage.v1.json'), encoding='utf-8'))
rf = cov['groups']['reportFeatures']
ids = [x.get('id') for x in (rf if isinstance(rf, list) else rf.values())]
R['coverage_reportFeature_ids_match'] = sorted(ids) == sorted(r[0] for r in rows)

print(json.dumps(R, indent=1)[:5200])
json.dump(R, open('/tmp/opensip-design-corrections/claude-independent-design.v26/receipts/probeJ.json', 'w'), indent=1)
