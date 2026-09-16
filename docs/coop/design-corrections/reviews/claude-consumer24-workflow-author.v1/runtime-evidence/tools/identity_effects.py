"""Pair before-edit and after-edit probe receipts (same owner fixtures, same inputs) into an explicit identity/behaviour account.

usage: python -I -B identity_effects.py
Inputs: receipts/probes/probe-items.before-edits.json (A11 section failed; its retry is probe-items.before-edits-retry.json)
and receipts/probes/probe-items.after-edits.json. Output: receipts/identity-effects.json.
"""
import json
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v1')
before = json.loads((RT / 'receipts/probes/probe-items.before-edits-retry.json').read_text())['sections']
after = json.loads((RT / 'receipts/probes/probe-items.after-edits.json').read_text())['sections']


def outcome(x):
    if not isinstance(x, dict):
        return x
    if x.get('result') in ('ADMIT', 'REFUSE'):
        return x['result'] + ('' if x['result'] == 'ADMIT' else ': ' + x.get('message', ''))
    if x.get('result') == 'RAISED':
        return 'RAISED %s / %s' % (x.get('errorCode'), x.get('detail'))
    if x.get('result') == 'OK':
        return 'OK'
    return x


m4 = {}
for key in ('original', 'remintedRename', 'staleHashRename', 'remintedEntryDetectorOutsideClosure', 'remintedConflictingContributionRow'):
    b, a = before['M4'][key], after['M4'][key]
    m4[key] = {'before': {k: outcome(v) for k, v in b.items() if k in ('verify', 'schema', 'e0JoinAgainstOriginal', 'baselineId')},
               'after': {k: outcome(v) for k, v in a.items() if k in ('verify', 'schema', 'e0JoinAgainstOriginal', 'baselineId')}}
s7 = {}
for gate in ('gate-true', 'gate-false'):
    s7[gate] = {'baselineId': {'before': before['S7'][gate]['baselineId'], 'after': after['S7'][gate]['baselineId']}}
    for case in ('complete-x1-removed', 'partial-inventory-x1-missing', 'budget-exhausted-both-rows', 'complete-unchanged'):
        bc, ac = before['S7'][gate][case]['comparison']['value'], after['S7'][gate][case]['comparison']['value']
        s7[gate][case] = {
            'currentFacts': after['S7'][gate][case]['current'],
            'before': {'comparisonResultId': bc['comparisonResultId'], 'verdict': bc['verdict'], 'entries': [(e['classification'], e['indeterminateReason'], e['presence']['E4']) for e in bc['entries']], 'schema': outcome(bc['schema'])},
            'after': {'comparisonResultId': ac['comparisonResultId'], 'verdict': ac['verdict'], 'entries': [(e['classification'], e['indeterminateReason'], e['presence']['E4']) for e in ac['entries']], 'schema': outcome(ac['schema'])},
            'comparisonIdChanged': bc['comparisonResultId'] != ac['comparisonResultId'],
        }
env = {k: {'before': outcome(before['M5-S6-A13-envelopes'][k]) if isinstance(before['M5-S6-A13-envelopes'][k], dict) and 'result' in before['M5-S6-A13-envelopes'][k] else before['M5-S6-A13-envelopes'][k],
           'after': outcome(after['M5-S6-A13-envelopes'][k]) if isinstance(after['M5-S6-A13-envelopes'][k], dict) and 'result' in after['M5-S6-A13-envelopes'][k] else after['M5-S6-A13-envelopes'][k]}
       for k in before['M5-S6-A13-envelopes']}
a6 = {k: {'before': before['A6'][k]['value'], 'after': after['A6'][k]['value']} for k in before['A6']}
a9 = {k: {'before': before['A9'][k]['value'], 'after': after['A9'][k]['value']} for k in before['A9']}
report = {'standing': 'same owner fixtures and inputs before and after the correction; synthetic retained graphs, not qualification',
          'M4': m4, 'S7': s7, 'M5-S6-A13': env, 'A6-unchanged-reference-behaviour': a6, 'A9-unchanged-reference-behaviour': a9,
          'A6A9Identical': all(v['before'] == v['after'] for v in a6.values()) and all(v['before'] == v['after'] for v in a9.values()),
          'A11A12': {'before': before['A11-A12'], 'after': after['A11-A12']}}
(RT / 'receipts/identity-effects.json').write_text(json.dumps(report, indent=1, default=str) + '\n')
print(json.dumps({'M4': m4, 'S7-summary': {g: {c: {'before': v['before']['entries'], 'after': v['after']['entries'], 'idChanged': v['comparisonIdChanged']} for c, v in s7[g].items() if c != 'baselineId'} for g in s7},
                  'baselineIds': {g: s7[g]['baselineId'] for g in s7}, 'A6A9Identical': report['A6A9Identical']}, indent=1, default=str)[:9000])
