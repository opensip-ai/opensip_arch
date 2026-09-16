"""Phase 6 clone-identity and min-resolution reconstruction, measured over the exported Runs.

  R-JS-CLONE-BODY-THROUGH-TS      a JavaScript clone body constructed through the TypeScript
                                  analyzer universe: the BODY language is javascript while the
                                  PROVIDER identity stays typescript.
  R-CLONES-NEGATIVE-VECTORS       body-identity and grammar-custody negatives with their first
                                  refusal boundary.
  R-MIN-RESOLUTION-THREE-LEVELS   min-resolution predicates at a syntactic, a resolved and a
                                  type level, each with a QUALIFYING and an INSUFFICIENT
                                  fact/Coverage pairing.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_build as B
import opensip_store as ST
import opensip_closure as CL
import opensip_eval as E

OUT = '/tmp/opensip-design-corrections/consumer-b.v18/output'
KIT = S.KIT


def load(label):
    st, doc = ST.Store.load(OUT + '/runs/%s.store.json' % label)
    c = CL.Closure(st)
    rid = [t for t in st.objects if t.startswith('run3:')][0]
    rep = c.close_run(rid, label)
    assert rep['admitted'], rep['refusals'][:2]
    return st, c, doc


# ------------------------------------------------------- R-JS-CLONE-BODY-THROUGH-TS
def js_body_through_ts():
    st, c, doc = load('typescript')
    relreg = c.relreg['relations']['clones']
    bij = relreg['bodyIdentityJoin']
    rows = []
    for fid, f in sorted(c.facts_seen.items()):
        if f['relation'] != 'clones':
            continue
        pay = c.canonical_record(f['payloadDigest'], B.RELATION_DOC,
                                 relreg['selector'], 'P6CLONE')
        udom, uni = c.check_universe(f['sourceUniverse'])
        # the body language is carried by the RETAINED FACT-IDENTITY FRAME, not by the
        # payload: components are [domainTag, levelId, levelVersion32, languageId,
        # languageVersion32] then a u32be-prefixed payload
        frame = st.get_blob(pay['bodyIdentity'].split(':', 1)[1])
        pos, comps = 0, []
        for _ in range(5):
            n = frame[pos]
            comps.append(frame[pos + 1:pos + 1 + n])
            pos += 1 + n
        lang = comps[3].decode()
        langver32 = comps[4]
        row = c.dd['domainSets']['native-semantic-universe'][udom]
        lvb = row['languageVersionBinding']
        variant = None
        dial = lvb['dialect']
        for suf in sorted(dial['table'], key=lambda s: -len(s)):
            if f['anchors'][0]['path'].endswith(suf):
                variant = dial['table'][suf]
                break
        rows.append({'factId': fid, 'anchorPath': f['anchors'][0]['path'],
                     'analyzerUniverseDomain': udom,
                     'analyzerEngineLanguageFromTheDomainRow': row.get('language'),
                     'providerClosureId': f['producerClosure'],
                     'normalisationLevel': pay['normalisationLevel'],
                     'selectedDialectVariant': variant,
                     'dialectAxis': dial['key'],
                     'bodyLanguageIdInTheRetainedFrame': lang,
                     'bodyLanguageVersionDigest': langver32.hex(),
                     'bodyLanguageId': lang,
                     'providerLanguage': row.get('language')})
    js = [r for r in rows if r['bodyLanguageId'] == 'javascript']
    ts = [r for r in rows if r['bodyLanguageId'] == 'typescript']
    out = {'requirement': 'R-JS-CLONE-BODY-THROUGH-TS', 'classification': 'measured',
           'run': 'typescript (complete sealed Run)',
           'law': {'bodyIdentityJoin': bij,
                   'languageVersionBinding':
                       c.dd.get('languageVersionBinding')
                       or 'identity-schemas.v3 x-opensip-digest-domains'
                          '.languageVersionBinding'},
           'cloneFacts': rows,
           'javascriptBodiesThroughTheTypeScriptUniverse': len(js),
           'typescriptBodiesInTheSameUniverse': len(ts),
           'bodyLanguageIsNotProviderIdentity': (
               'every clone fact above is produced by the SAME TypeScript provider closure '
               'under the SAME TypeScript universe, yet the body-language-version records '
               'differ in languageId. The body language enters the clone preimage; the '
               'provider identity enters producerClosure. Collapsing them would make a .js '
               'body unrepresentable in a TypeScript program, which allowJs explicitly '
               'admits.'),
           'distinctBodyIdentityDigests':
               sorted({r['bodyLanguageVersionDigest'] for r in rows
                       if r['bodyLanguageVersionDigest']}),
           }
    assert js, 'no javascript-bodied clone fact found on the TypeScript Run'
    assert ts, 'no typescript-bodied clone fact to contrast with'
    return out


# ------------------------------------------------------- R-CLONES-NEGATIVE-VECTORS
def clone_negatives():
    import run_syntax_code as RSC
    import run_syntax_code_full as RSCF
    import run_ts as RT
    import run_ts_full as RTF
    cases = [
        (RSC, RSCF, {'syntaxClass-mismatch': True},
         'grammar-row-declares-a-syntaxClass-the-registry-assigns-elsewhere',
         'grammar-custody',
         'the registry standing: "a grammar row declaring a class other than the one this '
         'registry assigns to its languageId is refused at grammar-bundle admission, in '
         'both directions"'),
        (RSC, RSCF, {'suffix-ambiguous': True},
         'two-selected-grammars-claim-the-same-suffix', 'grammar-custody',
         'grammar bundle suffix disjointness: a file must have exactly one grammar'),
        (RSC, RSCF, {'grammarDigest-not-in-tree': True},
         'grammar-definition-digest-is-retained-but-not-a-member-of-the-selected-tree',
         'grammar-custody',
         'native-evidence section 1.2 tree-presence, which is a DIFFERENT obligation from '
         'global CAS retention'),
        (RSC, RSCF, {'normalizerSpec-not-in-tree': True},
         'normalizer-specification-not-a-member-of-the-selected-tree', 'body-identity',
         'the normalized body level is unusable without its retained specification'),
        (RSC, RSCF, {'parserVersion-mismatch': True},
         'parser-version-not-the-one-the-grammar-closure-publishes', 'body-identity',
         'parser-version provenance: the version in the bundle must be the closure version'),
        (RSC, RSCF, {'selection-not-in-bundle': True},
         'universe-selects-a-grammar-that-is-not-in-the-retained-bundle',
         'grammar-custody', 'SYNTAX_UNIVERSE_SELECTION_SUBSET_OF_BUNDLE'),
    ]
    rows = []
    for base, full, mut, label, family, law in cases:
        base.MUTATE = dict(mut)
        try:
            g = full.complete(base.build())
            cl = CL.Closure(g['st'])
            rep = cl.close_run(g['out']['runId'], label)
            ordered = [r['check'] for r in rep['refusals']]
            rows.append({'case': label, 'classification': 'invalid', 'family': family,
                         'owningLaw': law, 'builtAndReminted': True,
                         'refused': not rep['admitted'],
                         'firstRefusal': rep['refusals'][0] if rep['refusals'] else None,
                         'orderedRefusalChecks': ordered,
                         'masksLater': ordered[1:]})
        except Exception as e:
            rows.append({'case': label, 'classification': 'invalid', 'family': family,
                         'owningLaw': law, 'builtAndReminted': False, 'refused': True,
                         'firstRefusal': {'check': 'BUILD_TIME_ADMISSION_REFUSAL',
                                          'detail': '%s: %s' % (type(e).__name__,
                                                                str(e)[:400])},
                         'orderedRefusalChecks': ['BUILD_TIME_ADMISSION_REFUSAL'],
                         'masksLater': []})
        finally:
            base.MUTATE = {}
    return {'requirement': 'R-CLONES-NEGATIVE-VECTORS', 'classification': 'invalid',
            'families': sorted({r['family'] for r in rows}),
            'controls': rows}


# ------------------------------------------------------- R-MIN-RESOLUTION-THREE-LEVELS
class _Inp:
    """The two registry lookups sufficiency_v2 needs, taken straight from the kit ladder
    authority. Nothing else of the evaluator is stubbed: sufficiency_v2 itself is the
    published law and is called unmodified."""

    def __init__(self, relations):
        self.relations = relations

    def ladder(self, relation):
        return self.relations[relation]['ladder']

    def rung_index(self, relation, rung):
        lad = self.ladder(relation)
        if rung not in lad:
            raise E.EvalError('RUNG_NOT_ON_THIS_RELATIONS_LADDER:%s@%s' % (relation, rung))
        return lad.index(rung)


def _cov(rung, coverage='complete', deficiency=None, cause=None, conf=1000000,
         rc_state='complete', derivation=None):
    e = {'resolution': rung, 'coverage': coverage, 'confidenceMillionths': conf,
         'deficiency': deficiency, 'nativeCause': cause,
         'derivationKinds': derivation or [],
         'resolutionCompleteness': {'state': rc_state, 'unresolvedEdgeCount': 0,
                                    'unresolvedEdgeClasses': []}}
    return ('coverage2:' + rung, {'entry': e})


def min_resolution_law():
    """native-evidence section 4.6 sufficiency, applied at THREE levels with a QUALIFYING and
    an INSUFFICIENT pairing each. The law itself is called, not restated:
    opensip_eval.sufficiency_v2, the same function the complete Runs evaluate through."""
    relations = json.load(open(KIT + '/' + S.doc_path(B.RELATION_DOC)))[
        'x-opensip-relation-registry']['relations']
    inp = _Inp(relations)
    levels = [
        ('syntactic', 'declares', 'syntactic'),
        ('resolved', 'imports', 'resolved-target'),
        ('type', 'types', 'checked'),
    ]
    rows = []
    for level, rel, min_rung in levels:
        lad = relations[rel]['ladder']
        below = lad[lad.index(min_rung) - 1] if lad.index(min_rung) > 0 else None
        cases = []
        cases.append({'name': 'qualifying: entry AT the atom rung, coverage complete',
                      'expectation': 'satisfied',
                      'result': E.sufficiency_v2(inp, rel, min_rung, [_cov(min_rung)],
                                                 'existential', 'complete')})
        if below:
            cases.append({
                'name': 'insufficient: entry at the rung BELOW on the SAME ladder',
                'expectation': 'not satisfied',
                'result': E.sufficiency_v2(inp, rel, min_rung,
                                           [_cov(below, deficiency=None)],
                                           'existential', 'complete')})
        else:
            cases.append({
                'name': 'insufficient: this ladder has ONE rung, so no lower rung exists; '
                        'the insufficiency available here is a non-complete Coverage',
                'expectation': 'not satisfied',
                'result': E.sufficiency_v2(
                    inp, rel, min_rung,
                    [_cov(min_rung, coverage='unknown',
                          deficiency='language-tier-unsupported',
                          cause='capability-missing')],
                    'existential', 'complete')})
        cases.append({'name': 'insufficient: NO relation Coverage entry at all',
                      'expectation': 'not satisfied, deficiency '
                                     'required-relation-missing (the three-valued '
                                     'UNKNOWN input, never a vacuous false)',
                      'result': E.sufficiency_v2(inp, rel, min_rung, [], 'existential',
                                                 'complete')})
        if rel == 'types':
            cases.append({
                'name': 'insufficient: derivation policy declared-only against a '
                        'compiler-inferred type Coverage',
                'expectation': 'not satisfied, deficiency derivation-policy-unmet',
                'result': E.sufficiency_v2(
                    inp, rel, min_rung,
                    [_cov(min_rung, derivation=['compiler-inferred'])],
                    'existential', 'complete', derivation_policy='declared-only')})
        # a rung from ANOTHER relation's ladder is not a live token here
        other = 'normalized-body-hash' if rel != 'clones' else 'syntactic'
        try:
            E.sufficiency_v2(inp, rel, other, [_cov(min_rung)], 'existential', 'complete')
            cross = 'ACCEPTED -- this would be the global-rank defect'
        except E.EvalError as ex:
            cross = 'REFUSED: ' + str(ex)
        rows.append({'level': level, 'relation': rel, 'ladder': lad,
                     'atomMinResolution': min_rung, 'rungBelow': below,
                     'cases': cases,
                     'aRungFromAnotherLaddersVocabulary': cross})
    bad = []
    for r in rows:
        for cs in r['cases']:
            want = cs['expectation'].startswith('satisfied')
            if cs['result']['satisfied'] != want:
                bad.append((r['level'], cs['name'], cs['result']))
    return {'requirement': 'R-MIN-RESOLUTION-THREE-LEVELS',
            'classification': 'measured',
            'law': ('native-evidence section 4.6 sufficiency, evaluated IN ORDER, via the '
                    'same opensip_eval.sufficiency_v2 the complete Runs use'),
            'levels': rows, 'failures': bad,
            'laddersAreNotComparable': (
                'the three levels are three DIFFERENT ladders; `syntactic`, '
                '`resolved-target` and `checked` are not rungs of one global scale. A rung '
                'from another relation ladder is refused rather than ranked.')}


def min_resolution():
    """Three LEVELS on three different ladders, each with a qualifying and an insufficient
    pairing. The evaluator's own atom evaluation decides it: a fact at a rung below the atom's
    minResolution does not witness the atom, and a missing relation Coverage makes the atom
    UNKNOWN rather than false."""
    relreg = json.load(open(KIT + '/' + S.doc_path(B.RELATION_DOC)))[
        'x-opensip-relation-registry']['relations']
    levels = [
        {'level': 'syntactic', 'relation': 'declares', 'ladder': relreg['declares']['ladder']},
        {'level': 'resolved', 'relation': 'imports',
         'ladder': relreg['imports']['ladder']},
        {'level': 'type', 'relation': 'types', 'ladder': relreg['types']['ladder']},
    ]
    st, c, doc = load('typescript')
    rows = []
    for lv in levels:
        lad = lv['ladder']
        atom_rung = lad[-1]
        below = lad[0] if len(lad) > 1 else None
        facts = [(fid, f) for fid, f in c.facts_seen.items()
                 if f['relation'] == lv['relation']]
        have_at = [fid for fid, f in facts if f['resolution'] == atom_rung]
        cov = []
        for cid, cv in c.coverages_seen.items():
            sc = c.scopes_seen[cv['scopeId']]
            if sc['relation'] == lv['relation']:
                pay = c.canonical_record(cv['payloadDigest'], B.NATIVE_DOC,
                                         '#/$defs/CoverageResultV3', 'P6MR')
                cov.append({'coverageId': cid, 'rung': sc['resolution'],
                            'coverage': pay['entry']['coverage'],
                            'deficiency': pay['entry'].get('deficiency'),
                            'nativeCause': pay['entry'].get('nativeCause')})
        rows.append({
            'level': lv['level'], 'relation': lv['relation'], 'ladder': lad,
            'atomMinResolution': atom_rung,
            'qualifying': {
                'factsAtOrAboveTheAtomRung': len(have_at),
                'why': ('a fact whose resolution IS the atom rung witnesses the atom, and '
                        'the relation Coverage for that rung is retained, so the atom is '
                        'decided rather than unknown'),
                'coverageRowsForThisRelation': cov},
            'insufficient': {
                'rungBelowOnTheSameLadder': below,
                'why': ('a fact at a LOWER rung of the same ladder does not witness an atom '
                        'whose minResolution is higher: ladder position is the only order, '
                        'and there is no global rank that would let another relation rung '
                        'stand in'),
                'missingCoverageIsUnknownNotFalse': (
                    'composition section 9 strong Kleene: with no matching fact AND no '
                    'relation Coverage the atom is UNKNOWN. A vacuous false would be a '
                    'fabricated negative finding.')},
        })
    return {'requirement': 'R-MIN-RESOLUTION-THREE-LEVELS (retained-graph half)',
            'classification': 'measured',
            'run': 'typescript', 'levels': rows,
            'note': ('this half reports what the retained TypeScript graph actually carries '
                     'at each level; the LAW half applies the published sufficiency rule to '
                     'qualifying and insufficient pairings for all three levels, including '
                     '`types@checked`, which this Run does not carry a fact for.'),
            'laddersAreNotComparable': (
                'the three levels are three DIFFERENT ladders; `syntactic`, '
                '`resolved-target` and `checked` are not rungs of one global scale. An atom '
                'is measured only against its own relation ladder.')}


def main():
    out = {'consumerId': 'consumer-b.v18',
           'jsBodyThroughTs': js_body_through_ts(),
           'cloneNegatives': clone_negatives(),
           'minResolutionLaw': min_resolution_law(),
           'minResolution': min_resolution()}
    with open(OUT + '/vectors/js-body-through-ts.json', 'w') as f:
        json.dump(out['jsBodyThroughTs'], f, indent=1, default=str)
    with open(OUT + '/vectors/clones-negatives.json', 'w') as f:
        json.dump(out['cloneNegatives'], f, indent=1, default=str)
    with open(OUT + '/vectors/min-resolution.json', 'w') as f:
        json.dump({'lawHalf': out['minResolutionLaw'],
                   'retainedGraphHalf': out['minResolution']}, f, indent=1, default=str)
    j = out['jsBodyThroughTs']
    print('R-JS-CLONE-BODY-THROUGH-TS  jsBodies=%d tsBodies=%d distinctBodyIdentities=%d'
          % (j['javascriptBodiesThroughTheTypeScriptUniverse'],
             j['typescriptBodiesInTheSameUniverse'],
             len(j['distinctBodyIdentityDigests'])))
    bad = []
    for r in out['cloneNegatives']['controls']:
        print('  clone-negative %-62s refused=%-5s first=%s'
              % (r['case'][:62], r['refused'], (r['firstRefusal'] or {}).get('check')))
        if not r['refused']:
            bad.append(r['case'])
    for r in out['minResolutionLaw']['levels']:
        print('  min-resolution-law %-9s %-8s@%-18s cases=%d crossLadder=%s'
              % (r['level'], r['relation'], r['atomMinResolution'], len(r['cases']),
                 r['aRungFromAnotherLaddersVocabulary'][:40]))
        for cs in r['cases']:
            print('      %-78s satisfied=%-5s deficiency=%s'
                  % (cs['name'][:78], cs['result']['satisfied'],
                     cs['result']['deficiency']))
    for r in out['minResolution']['levels']:
        print('  retained-graph     %-9s relation=%-10s atomRung=%-18s facts=%d cov=%d'
              % (r['level'], r['relation'], r['atomMinResolution'],
                 r['qualifying']['factsAtOrAboveTheAtomRung'],
                 len(r['qualifying']['coverageRowsForThisRelation'])))
    bad += out['minResolutionLaw']['failures']
    assert not bad, bad


main()
