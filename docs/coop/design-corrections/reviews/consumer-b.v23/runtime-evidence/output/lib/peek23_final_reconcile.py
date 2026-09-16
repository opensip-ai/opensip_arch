"""READ-ONLY post-command reconciliation (generation 23). Run AFTER the from-scratch command
returns. Writes nothing. Checks that:
  - every row of blind-review.json retainedArtifactDigests equals the sha256 of the bytes on disk,
    except artifacts the command legitimately rewrote AFTER the final reconciliation stage read
    them (only verify-all.json and the per-command receipt, which are not in the table);
  - verify-all.json records every declared stage with exit 0, including the final deliver stage;
  - the per-command receipt beside the stage logs equals verify-all.json;
  - the report's run table, requirement status, audit counts and SHOULD list equal their sources;
  - the md and json state the same verdict.
"""
import collections
import hashlib
import json
import os

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def J(rel):
    return json.load(open(os.path.join(OUT, rel)))


def main():
    br, va = J('blind-review.json'), J('verify-all.json')
    bad = []
    for rel, d in br['retainedArtifactDigests'].items():
        p = os.path.join(OUT, rel)
        now = sha(p) if os.path.exists(p) else None
        if now != d:
            bad.append((rel, d, now))
    print('digest rows %d, mismatching %d' % (len(br['retainedArtifactDigests']), len(bad)))
    for b in bad:
        print('  MISMATCH', b)
    print('stages recorded %s / declared %s, failed %s, nonzero %s'
          % (va['stagesRecorded'], va['declaredStageCount'], va['failedStages'],
             [s['script'] for s in va['stages'] if s['exit'] != 0]))
    print('last stage', va['stages'][-1]['script'], va['stages'][-1]['exit'])
    rec = json.load(open(os.path.join(va['stageIoDir'], 'verify-all.receipt.json')))
    print('per-command receipt equals verify-all.json:', rec == va)
    st = J('requirement-status.json')
    counts = dict(collections.Counter(v['status'] for v in st.values()))
    print('status counts', counts, 'report', br['requirementStatus']['counts'],
          'equal', counts == br['requirementStatus']['counts'])
    au = J('vectors/claimed-positive-audit.json')
    print('audit counts', au['counts'], 'report', br['claimedPositiveAudit']['counts'],
          'equal', au['counts'] == br['claimedPositiveAudit']['counts'])
    gaps = J('vectors/phase10-design-gaps.json')
    print('SHOULD ids equal phase 10:', [s['id'] for s in br['newShouldIssues']]
          == [s['id'] for s in gaps['newShouldIssues']])
    for r in br['claimedCompletePositives']:
        s = J(r['exportFile'])
        ok = (s['claim']['runId'] == r['claimedRunId'] and sha(os.path.join(OUT, r['exportFile']))
              == r['exportFileSha256'] and J('runs/%s.replay.json' % r['label'])['runId'] == r['claimedRunId'])
        print('  run %-13s %s joins export+replay: %s' % (r['label'], r['claimedRunId'][:20], ok))
    md = open(os.path.join(OUT, 'blind-review.md'), encoding='utf-8').read()
    print('verdict json %s, md states it: %s' % (br['verdict'], ('**Verdict: %s**' % br['verdict']) in md))
    rg = J('notes/v23-read-graph.json')
    print('read graph', rg['result'], 'dir is this command:', rg['commandStageIoDir'] == va['stageIoDir'],
          'stages logged', rg['stagesLogged'])
    outcomes = {}
    for f in sorted(os.listdir(va['stageIoDir'])):
        if f[:3].isdigit():
            o = json.load(open(os.path.join(va['stageIoDir'], f))).get('outcome') or {}
            outcomes.setdefault(o.get('kind'), []).append(f)
    print('stage outcomes', {k: len(v) for k, v in outcomes.items()},
          {k: v for k, v in outcomes.items() if k != 'returned'})


main()
