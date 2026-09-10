"""CB7-MUST-1: controls. Updates the one control whose refusal boundary legitimately moved, and
adds the discriminating set for the new law."""
import pathlib

W = pathlib.Path('/private/tmp/opensip-design-corrections/v19-native-coauthor.v1/work')
P = W / 'docs/coop/design-corrections/foundation/check-identity.py'
s = P.read_text(encoding='utf-8')

OLD = """rejects_because('injected-false-complete-for-a-markdown-scoped-clone-refuses',
    lambda:inject_syntax_coverage('clones','README.md',
        lambda e:e.update(coverage='complete',deficiency=None,nativeCause=None)),
    'SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE:')
"""
NEW = """# This claim still dies; CB7-MUST-1 moved WHERE. `.md` is in no dialect table, and a `clones` scope
# carries its own paths, so the source-variant law can be applied by the PRODUCER boundary - one
# layer earlier than any Run-closure prerequisite - and is. The refusal names the source variant
# because that is the defect it saw: this universe mints no body for `README.md` in any dialect.
# The syntax universe's own grammar guard is not weakened and still solely owns everything a suffix
# table cannot see: every `symbol` relation (the two labels above), and the SELECTION case where a
# path's suffix IS in the dialect table but no selected grammar row owns it (below).
rejects_because('injected-false-complete-for-a-markdown-scoped-clone-refuses',
    lambda:inject_syntax_coverage('clones','README.md',
        lambda e:e.update(coverage='complete',deficiency=None,nativeCause=None)),
    'native.coverage-source-variant-unsupported-complete:clones@normalized-body-hash:capability-missing')
rejects_because('injected-false-complete-for-a-markdown-scoped-clone-refuses-at-the-producer-boundary',
    lambda:inject_syntax_coverage('clones','README.md',
        lambda e:e.update(coverage='complete',deficiency=None,nativeCause=None)),
    'COVERAGE_PRODUCER_ADMISSION:')
# The grammar guard's OWN case, which the dialect table provably cannot reach: `.tsx` stays in the
# syntax dialect table while its grammar row is dropped from the bundle, so the source-variant law
# says supported and only the selected-grammar law can refuse. Without this the two guards could be
# mistaken for duplicates of one another.
def clone_scope_with_grammar_suffixes(path,dropped=()):
    saved=dict(N.BUNDLED_GRAMMARS)
    try:
        for suffix in dropped:N.BUNDLED_GRAMMARS.pop(suffix,None)
        run,objects,blobs=build(resolved=True,has_match=False,universe_language='syntax',
                                relation='clones',source_path=path,pure_syntax=True)
        entry=C.parse(blobs[next(v['payloadDigest'] for k,(d,v) in objects.items() if d=='coverage')])['entry']
        return entry,M.close_run(run,objects,blobs)
    finally:
        N.BUNDLED_GRAMMARS.clear();N.BUNDLED_GRAMMARS.update(saved)
_SYNTAX_DIALECT=M.DIGESTS['domainSets']['native-semantic-universe'][
    'native.semantic-universe.syntax.v2']['languageVersionBinding']['dialect']
check('a-dropped-grammar-row-is-still-inside-the-syntax-dialect-table',
      '.tsx' in _SYNTAX_DIALECT['table'] and
      N.source_variant_capability_support(_SYNTAX_DIALECT,'clones','normalized-body-hash',
                                          ['a.tsx'],True) is None)
_DROPPED_ENTRY,_DROPPED_RUN=clone_scope_with_grammar_suffixes('a.tsx',dropped=('.tsx',))
check('an-unselected-grammar-row-still-makes-a-clone-scope-unavailable',
      _DROPPED_RUN.startswith('run2:') and _DROPPED_ENTRY['coverage']=='unknown' and
      _DROPPED_ENTRY['deficiency']=='language-tier-unsupported' and
      _DROPPED_ENTRY['nativeCause']=='capability-missing')

# ------------------------------------------------------- CB7-MUST-1: the SOURCE VARIANT scope law.
# A universe whose body axis is a closed suffix table refused an unlisted suffix only while deriving
# a BODY. A scope with no facts derives none, so a `clones` scope over `package.json` under the
# TypeScript universe was classified by nothing at all and closed a Run claiming `complete`: a
# determinate `no clones here` about a file that universe cannot read as any TypeScript dialect.
# Unsupported is now UNKNOWN with the EXISTING published pair - no new deficiency, cause or detail
# code - and a supported code path stays eligible for `complete` with no body, because an absent
# body is a finding and an absent capability is not.
_TS_DIALECT=M.DIGESTS['domainSets']['native-semantic-universe'][
    'native.semantic-universe.typescript.v2']['languageVersionBinding']['dialect']
_RUST_DIALECT=M.DIGESTS['domainSets']['native-semantic-universe'][
    'native.semantic-universe.rust.v2']['languageVersionBinding']['dialect']
check('the-typescript-body-axis-is-a-closed-suffix-table-with-no-ownership-key',
      _TS_DIALECT['form']=='closed-suffix-table' and 'ownership' not in _TS_DIALECT and
      _TS_DIALECT['onUnknown']=='BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN')
check('every-published-universe-now-has-an-owning-scope-law',
      all(('ownership' in d) or d.get('form')=='closed-suffix-table'
          for d in [M.DIGESTS['domainSets']['native-semantic-universe'][u]['languageVersionBinding']['dialect']
                    for u in M.DIGESTS['domainSets']['native-semantic-universe']]))
# The suffix table is READ from the owning registry, so these are not a second copy of it.
check('a-registered-suffix-selects-its-variant-and-longest-match-wins',
      N.source_variant_of_path('a.d.ts',_TS_DIALECT['table'])=='ts-declaration' and
      N.source_variant_of_path('a.ts',_TS_DIALECT['table'])=='ts' and
      N.source_variant_of_path('deep/dir/a.mts',_TS_DIALECT['table'])=='mts' and
      N.source_variant_of_path('package.json',_TS_DIALECT['table']) is None)
check('a-supported-code-scope-is-not-made-unavailable',
      N.source_variant_capability_support(_TS_DIALECT,'clones','normalized-body-hash',
                                          ['src/a.ts','src/b.tsx'],True) is None)
check('an-unregistered-suffix-scope-is-unavailable-with-the-published-pair',
      N.source_variant_capability_support(_TS_DIALECT,'clones','normalized-body-hash',
                                          ['package.json'],True)==N.UNAVAILABLE_CAPABILITY_DISCLOSURE)
check('a-mixed-source-variant-scope-cannot-hide-its-unsupported-part',
      N.source_variant_capability_support(_TS_DIALECT,'clones','normalized-body-hash',
                                          ['src/a.ts','package.json'],True) is not None)
check('an-empty-source-variant-scope-is-not-vacuously-supported',
      N.source_variant_capability_support(_TS_DIALECT,'clones','normalized-body-hash',[],True) is not None)
check('inventory-capability-is-never-source-variant-gated',
      all(N.source_variant_capability_support(_TS_DIALECT,rel,rung,['package.json','vendor/blob.bin'],True) is None
          for rel,rung in [('file','enumerated'),('package','manifest-declared'),('vcs-change','vcs-reported')]))
check('a-universe-with-no-suffix-table-is-not-owned-by-this-law',
      'table' not in _RUST_DIALECT and
      N.source_variant_capability_support(_RUST_DIALECT,'clones','normalized-body-hash',
                                          ['package.json'],True) is None)

# --- FULL RUNS. The blind's exact measurement, and the positives it must not disturb.
def ts_clone_scope(path,universe_language='typescript'):
    run,objects,blobs=build(resolved=True,has_match=False,universe_language=universe_language,
                            relation='clones',source_path=path)
    entry=C.parse(blobs[next(v['payloadDigest'] for k,(d,v) in objects.items() if d=='coverage')])['entry']
    return entry,M.close_run(run,objects,blobs)
_PKG_ENTRY,_PKG_RUN=ts_clone_scope('package.json')
check('a-package-json-scoped-typescript-clone-request-closes-as-disclosed',
      _PKG_RUN.startswith('run2:') and _PKG_ENTRY['coverage']=='unknown' and
      _PKG_ENTRY['deficiency']=='language-tier-unsupported' and
      _PKG_ENTRY['nativeCause']=='capability-missing')
_FOREIGN_ENTRY,_FOREIGN_RUN=ts_clone_scope('a.py')
check('an-unlisted-suffix-scoped-typescript-clone-request-closes-as-disclosed',
      _FOREIGN_RUN.startswith('run2:') and _FOREIGN_ENTRY['coverage']=='unknown' and
      _FOREIGN_ENTRY['nativeCause']=='capability-missing')
# POSITIVE CONTROLS: a supported path with NO clone body is still a complete examination, and the
# longest-suffix rule keeps `.d.ts` supported rather than folding it into `.ts`. If either of these
# went indeterminate the law would be over-refusing, which is the failure mode opposite the finding.
for _label,_path in (('ts','a.ts'),('declaration','a.d.ts'),('tsx','a.tsx')):
    _OK_ENTRY,_OK_RUN=ts_clone_scope(_path)
    check('a-supported-typescript-clone-scope-with-no-body-still-closes-complete.'+_label,
          _OK_RUN.startswith('run2:') and _OK_ENTRY['coverage']=='complete' and
          _OK_ENTRY['deficiency'] is None and _OK_ENTRY['nativeCause'] is None)
check('a-rust-clone-scope-is-unaffected-by-the-source-variant-law',
      ts_clone_scope('src/plain.rs',universe_language='rust')[1].startswith('run2:'))
# The scope is judged on the COMMITTED REQUEST, never on whether facts exist: this view has none.
check('the-disclosed-typescript-clone-scope-really-has-no-facts',
      not [k for k,(d,v) in build(resolved=True,has_match=False,universe_language='typescript',
                                  relation='clones',source_path='package.json')[1].items()
           if d=='fact' and v['relation']=='clones'])

# --- BOTH ADMISSION BOUNDARIES, each exercised on its own.
def ts_clone_injection(path,mutate):
    run,objects,blobs=build(resolved=True,has_match=False,universe_language='typescript',
                            relation='clones',source_path=path)
    key=next(k for k,(d,v) in objects.items() if d=='coverage')
    coverage=copy.deepcopy(objects[key][1]);payload=C.parse(blobs[coverage['payloadDigest']])
    mutate(payload['entry'])
    coverage['payloadDigest']=put_blob(blobs,payload)
    rekey(objects,key,coverage,run);resync_witness(objects,blobs,run)
    return M.close_run(run,objects,blobs)
rejects_because('injected-false-complete-for-a-package-json-clone-scope-refuses',
    lambda:ts_clone_injection('package.json',
        lambda e:e.update(coverage='complete',deficiency=None,nativeCause=None)),
    'native.coverage-source-variant-unsupported-complete:clones@normalized-body-hash:capability-missing')
rejects_because('injected-wrong-cause-for-an-unsupported-source-variant-refuses',
    lambda:ts_clone_injection('package.json',lambda e:e.update(nativeCause='no-program-unit')),
    'native.coverage-cause-not-for-deficiency:language-tier-unsupported:no-program-unit')
# A claim that is internally COHERENT and merely wrong about what this universe can serve reaches
# the derivation itself, which is where the deficiency and the cause are each compared.
rejects_because('injected-wrong-deficiency-for-an-unsupported-source-variant-refuses',
    lambda:ts_clone_injection('package.json',
        lambda e:(e.update(deficiency='budget-exhausted',nativeCause=None),
                  e['resolutionCompleteness'].update(stageTerminal='budget-exhausted'))),
    'native.coverage-source-variant-deficiency-mismatch:clones@normalized-body-hash:expected=language-tier-unsupported')
# The PRODUCER boundary, called directly with only the universe's own dialect spec as context. The
# scope descriptor and the dialect come from the host; nothing is read from the payload, so a
# provider cannot switch its own capability on by asserting a flag.
_PROD_RUN,_PROD_OBJECTS,_PROD_BLOBS=build(resolved=True,has_match=False,universe_language='typescript',
                                          relation='clones',source_path='package.json')
_PROD_COVERAGE=next(v for k,(d,v) in _PROD_OBJECTS.items() if d=='coverage')
_PROD_SCOPE=_PROD_OBJECTS[_PROD_COVERAGE['scopeId']][1]
_PROD_PAYLOAD=C.parse(_PROD_BLOBS[_PROD_COVERAGE['payloadDigest']])
def _producer(entry_update,dialect=_TS_DIALECT):
    payload=copy.deepcopy(_PROD_PAYLOAD);payload['entry'].update(entry_update)
    return N.admit_coverage_result_v3(payload,_PROD_SCOPE,[],
                                      _PROD_COVERAGE['payloadSchemaDigest'],dialect)
check('the-producer-boundary-admits-the-disclosed-unsupported-scope',
      _producer({})['result']=='ADMIT')
check('the-producer-boundary-refuses-a-false-complete-for-an-unsupported-scope',
      any(r.startswith('native.coverage-source-variant-unsupported-complete:')
          for r in _producer({'coverage':'complete','deficiency':None,'nativeCause':None})['refusals']))
check('the-producer-boundary-refuses-an-undisclosed-unsupported-scope',
      any(r.startswith('native.coverage-source-variant-deficiency-mismatch:')
          for r in _producer({'deficiency':None,'nativeCause':None})['refusals']))
check('the-producer-boundary-makes-no-capability-claim-without-the-owning-dialect',
      not any(r.startswith('native.coverage-source-variant-')
              for r in _producer({'coverage':'complete','deficiency':None,'nativeCause':None},
                                 dialect=None)['refusals']))
check('the-producer-boundary-derivation-ignores-a-payload-asserted-variant',
      any(r.startswith('native.coverage-source-variant-unsupported-complete:')
          for r in _producer({'coverage':'complete','deficiency':None,'nativeCause':None,
                              'derivationKinds':['ts']})['refusals']))

# --- OUTPUT PROJECTION. The disclosure is not cosmetic: it is what turns a silent success into a
# reported indeterminate. Before this law the same request projected exit 0 with no typed detail.
_PROJECTED=N.run_termination(N.stage_authority('complete'),[_PKG_ENTRY])
check('an-unsupported-source-variant-scope-projects-an-indeterminate-run',
      _PROJECTED['d9']['class']=='indeterminate' and _PROJECTED['d9']['exitCode']==3 and
      _PROJECTED['typedDetail']['deficiency']=='language-tier-unsupported' and
      _PROJECTED['typedDetail']['nativeCauses']==['capability-missing'])
check('a-supported-source-variant-scope-still-projects-a-successful-run',
      N.run_termination(N.stage_authority('complete'),
                        [ts_clone_scope('a.ts')[0]])['d9']['exitCode']==0)
"""
assert s.count(OLD) == 1
P.write_text(s.replace(OLD, NEW), encoding='utf-8')
print('ok')
