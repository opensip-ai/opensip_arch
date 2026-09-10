"""CB7-ADV-4: controls for the published transition table."""
import pathlib

W = pathlib.Path('/private/tmp/opensip-design-corrections/v19-native-coauthor.v1/work')
P = W / 'docs/coop/design-corrections/foundation/check-identity.py'
s = P.read_text(encoding='utf-8')

ANCHOR = """# ------------------------------------------------- CB7-SHOULD-2: the PLAN's own bounded selections.
"""
NEW = '''# ------------------------------------------- CB7-ADV-4: the PUBLISHED protocol-3 transition table.
# The 34 rows, their order, their guards and their terminal semantics were author-code-only, so a
# review kit that excludes author code could not reconstruct the host state machine that section 9.2
# names. They now live in one artifact the model CONSUMES. These controls live here rather than in
# the native case list because the discriminating ones need to drive the interpreter with a permuted
# table, which the native case DSL's JSON argument form cannot express.
_P3=json.loads((H.parent/'native/protocol3-transitions.v1.json').read_text())
check('the-published-protocol-table-is-the-table-the-reference-runs',
      N.PROTOCOL3_RULES==_P3['rules'] and len(N.PROTOCOL3_RULES)==_P3['ruleCount']==34 and
      N.PROTOCOL3_PHASES==_P3['phases'])
check('the-published-pre-complete-wildcard-agrees-with-its-published-derivation',
      N.PROTOCOL3_PHASES[1:17]==_P3['wildcards']['*PRE_COMPLETE']['phases']==N._PRE_COMPLETE)
check('the-published-out-of-band-and-source-frame-sets-are-the-ones-applied',
      set(_P3['wildcards']['*PROCESS_FAULT']['frames'])==N._PROCESS_FAULTS and
      {f for u in _P3['stateUpdates'] for f in u.get('onFrames',())}==N._SOURCE_FRAMES)
# The published vocabulary is CLOSED: every row's phase, next and terminal are drawn from the phase
# list, the published wildcards or the one published stage-dependent token. An unresolvable `next`
# would leave a conforming host with no defined successor.
_P3_TOKENS=set(_P3['phases'])|set(_P3['stageDependentTransitions'])
check('every-published-transition-names-a-published-successor',
      all(r['next'] in _P3_TOKENS for r in _P3['rules']))
check('every-published-row-names-a-published-phase-or-wildcard',
      all(r['phase'] in set(_P3['phases'])|set(_P3['wildcards']) for r in _P3['rules']))
check('the-published-table-states-what-remains-prose-owned',
      len(_P3['ownedByProse'])>=4 and _P3['consumedBy'].endswith('protocol3_run)'))
# ORDER IS LOAD-BEARING, demonstrated rather than asserted: P3-08..P3-10 differ ONLY by guard, so a
# table sorted by id descending sends the same dependency-mode exchange somewhere else.
_P3_EVENTS=[{'frame':'Hello'},{'frame':'HelloAck','capabilities':list(N.IDENTITY_TOKENS)},
            {'frame':'OpenUniverse','dependencyMode':True},{'frame':'UniverseAccepted'},
            {'frame':'SnapshotManifest'},{'frame':'SnapshotSeal'},{'frame':'SnapshotAccepted'}]
_P3_ORDERED=N.protocol3_run(_P3_EVENTS)
_P3_REVERSED=N.protocol3_run(_P3_EVENTS,rules=list(reversed(N.PROTOCOL3_RULES)))
check('the-published-order-selects-the-dependency-mode-transition',
      _P3_ORDERED['trace'][-1]=='P3-08' and _P3_ORDERED['finalPhase']=='READY_DEPENDENCY_MANIFEST')
check('a-reordered-published-table-does-not-reproduce-the-same-transition',
      _P3_REVERSED['trace']!=_P3_ORDERED['trace'])
# GUARDS decide between the three same-phase same-frame rows; without dependency or prepared mode the
# exchange skips both custody phases.
check('the-published-guards-select-the-plain-snapshot-transition',
      N.protocol3_run([{'frame':'Hello'},{'frame':'HelloAck','capabilities':list(N.IDENTITY_TOKENS)},
                       {'frame':'OpenUniverse'},{'frame':'UniverseAccepted'},
                       {'frame':'SnapshotManifest'},{'frame':'SnapshotSeal'},
                       {'frame':'SnapshotAccepted'}])['trace'][-1]=='P3-10')
# THE FALLBACK AND OUT-OF-BAND ROWS, which the matching loop never reaches and the published law
# assigns to the two named code paths.
check('an-unknown-frame-takes-the-published-fallback-row',
      N.protocol3_run([{'frame':'Hello'},{'frame':'not-a-frame'}])['trace']==['P3-01','P3-34'] )
check('an-out-of-band-process-fault-takes-the-published-any-phase-row',
      N.protocol3_run([{'frame':'Hello'},{'frame':'signal-death'}])['trace']==['P3-01','P3-33'])
check('a-post-terminal-frame-is-refused-by-the-published-pre-match-law',
      N.protocol3_run([{'frame':'Hello'},{'frame':'HelloAck','capabilities':list(N.IDENTITY_TOKENS)},
                       {'frame':'OpenUniverse'},{'frame':'UniverseAccepted'},
                       {'frame':'SnapshotManifest'},{'frame':'SnapshotSeal'},
                       {'frame':'SnapshotAccepted'},{'frame':'NativeContextVerified'},
                       {'frame':'Analyze'},{'frame':'BudgetExhausted'},
                       {'frame':'FactBatch'}])['trace'][-1]=='post-terminal-frame')
# THE STAGE-DEPENDENT TRANSITION, which cannot be read off the rows at all: one CoverageV3 per stage,
# and only the last may be followed by Complete.
def _p3_stages(coverage_count,stage_count):
    return N.protocol3_run([{'frame':'Hello'},{'frame':'HelloAck','capabilities':list(N.IDENTITY_TOKENS)},
                            {'frame':'OpenUniverse'},{'frame':'UniverseAccepted'},
                            {'frame':'SnapshotManifest'},{'frame':'SnapshotSeal'},
                            {'frame':'SnapshotAccepted'},{'frame':'NativeContextVerified'},
                            {'frame':'Analyze'}]+
                           [{'frame':'CoverageV3'}]*coverage_count+
                           [{'frame':'Complete'},{'frame':'zero-exit'},{'frame':'eof'}],
                           stage_count=stage_count)
check('the-published-stage-dependent-transition-completes-a-two-stage-run',
      _p3_stages(2,2)['finalPhase']=='DONE' and _p3_stages(2,2)['terminalKind']=='complete' and
      _p3_stages(2,2)['stagesCompleted']==2)
check('a-two-stage-run-cannot-complete-after-one-coverage',
      _p3_stages(1,2)['finalPhase']=='FAULT' and _p3_stages(1,2)['terminalKind'] is None)

# ------------------------------------------------- CB7-SHOULD-2: the PLAN's own bounded selections.
'''
assert s.count(ANCHOR) == 1
P.write_text(s.replace(ANCHOR, NEW), encoding='utf-8')
print('ok')
