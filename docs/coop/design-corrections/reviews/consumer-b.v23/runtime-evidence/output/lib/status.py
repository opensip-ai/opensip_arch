"""Derive output/requirement-status.json FROM THE CLAIMED-POSITIVE AUDIT, not from a checklist.

Generation 22 (V22-D4). The generation-20 version of this module graded several rows from the
presence of an artifact, a count, a generation-16 custody note, or a literal True. Every row is
now taken from vectors/claimed-positive-audit.json, which re-checks the requirement's final bytes
in a fresh process and records the EVIDENCE CLASS of that re-check:

  executed      every audit check passed AND the evidence class is sufficient for the original
                requirement kind
  failed        an audit check refused (the first refusal is carried)
  unexecuted    no audit row, or checks passed but the evidence class is not the kind of work the
                requirement demands
  futureQualification  the three excluded host/OS/compiler items

The five phase-11 deliverable rows are decided here from the written review files, and only when
those files were written AFTER this command's audit (otherwise they are unexecuted: a review from
a previous command is not this command's deliverable).
"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = '/tmp/opensip-design-corrections/consumer-b.v23'
OUT = ROOT + '/output'
VERDICTS = ('ACCEPT-RECONSTRUCTABLE', 'CHANGES_REQUIRED', 'BLOCKED')
PHASE11 = ('R-DELIVER-MD-JSON', 'R-VERDICT-ENUM', 'R-MUST-SHOULD-ADVISORY',
           'R-NO-ACCEPT-IF-INCOMPLETE', 'R-NO-QUALIFICATION-CLAIM')


def J(rel):
    try:
        return json.load(open(OUT + '/' + rel))
    except Exception:
        return None


def phase11(rid, rows_so_far):
    audit_t = os.path.getmtime(OUT + '/vectors/claimed-positive-audit.json')
    md, js = OUT + '/blind-review.md', OUT + '/blind-review.json'
    if not (os.path.exists(md) and os.path.exists(js)) or os.path.getmtime(js) < audit_t:
        return 'unexecuted', {'note': 'the review of THIS command is not written yet'}, None
    rev = J('blind-review.json') or {}
    text = open(md, encoding='utf-8').read()
    checks = []

    def need(c, name, detail=None):
        checks.append({'check': name, 'result': 'PASS' if c else 'REFUSE', 'detail': detail})
    if rid == 'R-DELIVER-MD-JSON':
        need(len(text) > 1000 and rev.get('verdict') and rev.get('retainedArtifactDigests'),
             'BOTH_REVIEW_FILES_WITH_VERDICT_AND_ARTIFACT_DIGESTS')
    elif rid == 'R-VERDICT-ENUM':
        need(rev.get('verdict') in VERDICTS, 'VERDICT_IN_THE_CLOSED_ENUM', rev.get('verdict'))
        need(('**Verdict: %s**' % rev.get('verdict')) in text, 'MD_STATES_THE_SAME_VERDICT')
    elif rid == 'R-MUST-SHOULD-ADVISORY':
        need(all(isinstance(rev.get(k), list) for k in ('newMustIssues', 'newShouldIssues',
                                                         'advisories')),
             'MUST_SHOULD_ADVISORY_ARRAYS_PRESENT')
    elif rid == 'R-NO-ACCEPT-IF-INCOMPLETE':
        blocking = sorted(k for k, v in rows_so_far.items()
                          if v.get('acceptBlocking') and k not in PHASE11
                          and v['status'] in ('unexecuted', 'failed'))
        accept = rev.get('verdict') == 'ACCEPT-RECONSTRUCTABLE'
        need(not accept or (not blocking and not rev.get('newMustIssues')
                            and not rev.get('newShouldIssues')
                            and not rev.get('openHelperFailuresOnAClaimedPositive')),
             'ACCEPT_ONLY_WITH_NOTHING_BLOCKING_OPEN', blocking[:10])
    elif rid == 'R-NO-QUALIFICATION-CLAIM':
        need('noProductQualificationClaim' in (rev.get('standing') or {})
             and 'qualif' in text, 'NO_QUALIFICATION_STANDING_IN_BOTH_FILES')
    ref = [c for c in checks if c['result'] != 'PASS']
    return ('executed' if not ref else 'failed'), {'checks': checks}, (ref[0] if ref else None)


def main():
    whole = json.load(open(ROOT + '/requirements.json'))
    audit = J('vectors/claimed-positive-audit.json')
    if audit is None:
        raise SystemExit('claimed-positive audit missing: status cannot be derived')
    rows_in = list(whole['standing']) + list(whole['requirements']) + list(whole['futureQualification'])
    doc = {}
    for r in rows_in:
        rid = r['id']
        base = {'id': rid, 'kind': r.get('kind'), 'acceptBlocking': r.get('acceptBlocking'),
                'phase': r.get('phase'), 'requirement': r['requirement'],
                'observable': r.get('observable')}
        if r['kind'] == 'futureQualification':
            doc[rid] = dict(base, status='futureQualification', artifact=None, firstRefusal=None,
                            notes=('not demanded as a current blocker; the compiler, provider and '
                                   'OS observations of this origin are SYNTHETIC TRUSTED INPUTS'),
                            evidence={})
            continue
        if rid in PHASE11:
            continue
        a = audit['requirements'].get(rid)
        if a is None:
            doc[rid] = dict(base, status='unexecuted', artifact=None, firstRefusal=None,
                            notes='no claimed-positive audit row', evidence={})
            continue
        if a['result'] == 'PASS':
            status = 'executed'
        elif a['refusals']:
            status = 'failed'
        else:
            status = 'unexecuted'
        doc[rid] = dict(base, status=status, artifact=a['artifacts'],
                        firstRefusal=a['firstRefusal'],
                        notes='%s -- %s' % (a['evidenceClass'], a['method']),
                        evidence={'evidenceClass': a['evidenceClass'],
                                  'evidenceClassSufficientForKind': a['evidenceClassSufficientForKind'],
                                  'checksPassed': a['checksPassed'],
                                  'refusals': a['refusals'][:5]})
    for rid in PHASE11:
        r = next(x for x in rows_in if x['id'] == rid)
        status, ev, first = phase11(rid, doc)
        doc[rid] = {'id': rid, 'kind': r['kind'], 'acceptBlocking': r.get('acceptBlocking'),
                    'phase': r.get('phase'), 'requirement': r['requirement'],
                    'observable': r.get('observable'), 'status': status,
                    'artifact': ['blind-review.md', 'blind-review.json'], 'firstRefusal': first,
                    'notes': 'standing-record-verified over the review files of THIS command',
                    'evidence': dict(ev, evidenceClass='standing-record-verified')}
    ordered = {r['id']: doc[r['id']] for r in rows_in}
    with open(OUT + '/requirement-status.json', 'w') as f:
        json.dump(ordered, f, indent=1, default=str)
    c = collections.Counter(v['status'] for v in ordered.values())
    blocking = sorted(k for k, v in ordered.items()
                      if v.get('acceptBlocking') and v['status'] in ('unexecuted', 'failed'))
    print('requirement-status.json:', dict(c), 'total', len(ordered))
    print('acceptBlocking not executed:', blocking)


main()
