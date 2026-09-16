"""Phase 4 -- state-dependent count/class/attempt rules, the code-vs-data capability matrix,
the enumerated-vs-resolved standing rule, and the advertised-mode path table.

Everything here is MEASURED over the five already-admitted exported Runs plus the kit
registries. Nothing is asserted from a count of passing helper lines.
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

OUT = '/tmp/opensip-design-corrections/consumer-b.v17/output'
KIT = S.KIT
RUNS = ['syntax-code', 'typescript', 'rust', 'rust-partial', 'syntax-data']
CONSUMER = 'consumer-b.v17'


def kit(doc):
    return json.load(open(KIT + '/' + S.doc_path(doc)))


_CACHE = {}


def load(label):
    """Fresh-process-equivalent: the store is rebuilt FROM THE EXPORTED BYTES ONLY and the
    whole closure is re-executed; every blob key is re-hashed by Store.load itself."""
    if label in _CACHE:
        return _CACHE[label]
    st, doc = ST.Store.load(OUT + '/runs/%s.store.json' % label)
    c = CL.Closure(st)
    rep = c.close_run(run_id_of(st), label)
    assert rep['admitted'], (label, rep['refusals'][:2])
    _CACHE[label] = (st, c, rep)
    return _CACHE[label]


def run_id_of(st):
    for tid in st.objects:
        if tid.startswith('run3:'):
            return tid
    raise KeyError('no run3 in store')


# --------------------------------------------------------------- R-COUNT-CLASS-ATTEMPT
def count_class_attempt():
    """Three DIFFERENT state-dependent rule families, applied to retained scopes/Coverage:

      CLASS   relation-payload-schemas x-opensip-relation-registry `anchorLaw.class`:
              a closed cardinality class per relation (source-text >=1, body-identity ==1,
              inventory ==0). The class is a property of the RELATION, not of the fact.
      COUNT   `coverageTotalityLaw`: for the one relation@rung it names, a `complete`
              Coverage owes exactly one fact per subject THAT IS IN THE SNAPSHOT INVENTORY.
              A subject outside the inventory is owed nothing, and an `unknown` Coverage
              owes nothing at all -- the two fact-ABSENT cases that are legitimate.
      ATTEMPT `resolutionCompleteness` / exhaustiveness may be claimed only where resolution
              was ATTEMPTED. Where no resolution is attempted, zero unresolved-edge facts is
              NOT evidence that there are no unresolved edges.
    """
    relreg = kit(B.RELATION_DOC)['x-opensip-relation-registry']
    mat = kit('docs/coop/design-corrections/native/native-capability-matrix.v2.json')
    rows, attempt_rows, absent_rows = [], [], []
    classes = {}
    for rel, row in sorted(relreg['relations'].items()):
        classes[rel] = {'class': row['anchorLaw']['class'],
                        'cardinality': row['anchorLaw'].get('cardinality'),
                        'ladder': row['ladder']}
    for label in RUNS:
        st, c, rep = load(label)
        inv = c.inv
        for fid, f in sorted(c.facts_seen.items()):
            rel = f['relation']
            cls = classes[rel]
            n = len(f['anchors'])
            ok = ({'inventory': n == 0,
                   'body-identity': n == 1,
                   'source-text': n >= 1}[cls['class']])
            rows.append({'run': label, 'relation': rel, 'resolution': f['resolution'],
                         'anchorClass': cls['class'],
                         'declaredCardinality': cls['cardinality'],
                         'measuredAnchorCount': n, 'satisfiesClass': ok})
        # COUNT: the totality relation@rung, with both fact-absent exemptions measured
        for sid, sc in sorted(c.scopes_seen.items()):
            row = relreg['relations'].get(sc['relation'], {})
            tot = row.get('coverageTotality')
            cov = [cv for cv in c.coverages_seen.values() if cv['scopeId'] == sid]
            if not cov:
                continue
            pay = c.canonical_record(cov[0]['payloadDigest'], B.NATIVE_DOC,
                                     '#/$defs/CoverageResultV3', 'PHASE4')
            state = pay['entry']['coverage']
            in_inv = [s for s in sc['subjects'] if s in c.inv]
            out_inv = [s for s in sc['subjects'] if s not in c.inv]
            facts = 0
            if tot and tot['rung'] == sc['resolution']:
                for fid, f in c.facts_seen.items():
                    if f['relation'] == sc['relation'] and f['resolution'] == sc['resolution']:
                        facts += 1
            absent_rows.append({
                'run': label, 'relation': sc['relation'], 'resolution': sc['resolution'],
                'coverageState': state,
                'totalityLawApplies': bool(tot and tot['rung'] == sc['resolution']),
                'subjectsInInventory': len(in_inv), 'subjectsOutsideInventory': out_inv,
                'factsAtThisPair': facts,
                'obligation': (
                    'one fact per inventoried subject' if tot and tot['rung'] == sc['resolution']
                    and state == 'complete' else
                    'none: unknown Coverage owes no fact' if state != 'complete' else
                    'none: no coverageTotalityLaw row for this relation@rung'),
                'factAbsentIsLegitimateHere': (
                    state != 'complete' or not tot or tot['rung'] != sc['resolution']
                    or not in_inv),
            })
        # ATTEMPT: the universes, their resolution posture and what that licenses
        for tid in sorted(st.objects):
            if not tid.startswith('native.semantic-universe.'):
                continue
            dom, hx = tid.split('#')
            uni = st.objects[tid]
            attempted = (dom == 'native.semantic-universe.typescript.v2'
                         or dom == 'native.semantic-universe.rust.v2')
            unresolved_facts = [f for f in c.facts_seen.values()
                                if f['relation'] == 'unresolved-edge'
                                and f['sourceUniverse'].endswith(hx)]
            attempt_rows.append({
                'run': label, 'universeDomain': dom,
                'resolutionAttempted': attempted,
                'resolutionCompletenessImplied': uni.get('resolutionCompletenessImplied'),
                'unresolvedEdgeFactsRetained': len(unresolved_facts),
                'licensedClaim': (
                    'CoverageV3.resolutionCompleteness may be claimed only after resolution '
                    'was attempted over an exhaustive examined partition with a complete '
                    'stage' if attempted else
                    'no resolution is attempted, so no unresolved edges are OBSERVED; zero '
                    'retained unresolved-edge facts is NOT a claim that none exist'),
            })
    bad_class = [r for r in rows if not r['satisfiesClass']]
    bad_absent = [r for r in absent_rows
                  if r['obligation'].startswith('one fact') and r['factsAtThisPair'] == 0
                  and r['subjectsInInventory']]
    # no syntax-only universe may imply resolution completeness
    bad_attempt = [r for r in attempt_rows
                   if not r['resolutionAttempted'] and r['resolutionCompletenessImplied']]
    doc = {'classification': 'explanatory+measured', 'consumerId': CONSUMER,
           'law': {'class': (B.RELATION_DOC
                             + '#/x-opensip-relation-registry/relations/*/anchorLaw'),
                   'count': (B.RELATION_DOC
                             + '#/x-opensip-relation-registry/coverageTotalityLaw'),
                   'attempt': ('docs/coop/design-corrections/native/'
                               'native-capability-matrix.v2.json#/'
                               + 'resolutionCompleteness')},
           'attemptLawText': mat.get('resolutionCompleteness'),
           'anchorClassesByRelation': classes,
           'measuredAnchorClassRows': rows,
           'measuredTotalityAndFactAbsentRows': absent_rows,
           'measuredAttemptRows': attempt_rows,
           'failures': {'anchorClass': bad_class, 'totalityCount': bad_absent,
                        'attempt': bad_attempt}}
    w('vectors/count-class-attempt.json', doc)
    assert not bad_class and not bad_absent and not bad_attempt, doc['failures']
    print('R-COUNT-CLASS-ATTEMPT  anchorClassRows=%d totality/absentRows=%d attemptRows=%d'
          % (len(rows), len(absent_rows), len(attempt_rows)))
    print('   fact-absent cases measured: %d outside-inventory, %d unknown-coverage'
          % (sum(1 for r in absent_rows if r['subjectsOutsideInventory']),
             sum(1 for r in absent_rows if r['coverageState'] != 'complete')))
    return doc


# --------------------------------------------------------------- R-CODE-VS-DATA-MATRIX
def code_vs_data():
    """The grammar-capability registry splits bundled grammars by `syntaxClass`:
    `code` vs `data-document`. The split is not cosmetic -- it decides which relation@rung
    pairs a selected grammar may serve at enforcement boundary (2)/(3), and it decides which
    BODY/NORMALIZER law is available: a normalized clone body identity needs a normalizer
    specification that declares the level for that syntaxClass.
    """
    nat = kit(B.NATIVE_DOC)
    greg = nat['x-opensip-grammar-capability-registry']
    grams = greg['languages']          # keyed by languageId
    by_class = {}
    for gid, g in sorted(grams.items()):
        by_class.setdefault(g['syntaxClass'], []).append(
            {'languageId': gid, 'suffixes': g.get('suffixes'),
             'capabilities': sorted(g.get('capabilities') or [])})
    # measured: which capabilities each syntax Run actually served, per syntaxClass
    measured = []
    for label in ('syntax-code', 'syntax-data'):
        st, c, rep = load(label)
        served, unavailable = set(), []
        for fid, f in c.facts_seen.items():
            served.add('%s@%s' % (f['relation'], f['resolution']))
        for cid, cv in c.coverages_seen.items():
            pay = c.canonical_record(cv['payloadDigest'], B.NATIVE_DOC,
                                     '#/$defs/CoverageResultV3', 'PHASE4CD')
            e = pay['entry']
            if e['coverage'] != 'complete':
                sc = c.scopes_seen[cv['scopeId']]
                unavailable.append({'pair': '%s@%s' % (sc['relation'], sc['resolution']),
                                    'coverage': e['coverage'],
                                    'deficiency': e.get('deficiency'),
                                    'nativeCause': e.get('nativeCause')})
        sel, sel_langs = [], []
        for tid in st.objects:
            if tid.startswith('native.context.syntax.v2#'):
                for g in st.objects[tid]['grammarBundle']['grammars']:
                    sel.append(g['grammarId'])
                    sel_langs.append(g.get('languageId') or g['grammarId'])
        classes = sorted({grams[l]['syntaxClass'] for l in sel_langs if l in grams})
        measured.append({'run': label, 'selectedGrammarIds': sorted(sel),
                         'selectedLanguageIds': sorted(set(sel_langs)),
                         'selectedSyntaxClasses': classes,
                         'servedPairs': sorted(served),
                         'nonCompleteCoverage': sorted(unavailable,
                                                       key=lambda r: r['pair']),
                         'inventoryPairsAreNeverGrammarGated':
                             sorted(p for p in served
                                    if p in ('file@enumerated', 'package@manifest-declared',
                                             'vcs-change@vcs-reported'))})
    # the matrix distinction as a table: which pairs are code-only
    code_caps = set()
    data_caps = set()
    for gid, g in grams.items():
        (code_caps if g['syntaxClass'] == 'code' else data_caps).update(
            g.get('capabilities') or [])
    doc = {'classification': 'explanatory+measured', 'consumerId': CONSUMER,
           'law': {'registry': B.NATIVE_DOC + '#/x-opensip-grammar-capability-registry',
                   'syntaxClassKey': 'languages[*].syntaxClass',
                   'classLaw': greg['classLaw'],
                   'boundaries': greg.get('enforcementBoundaries'),
                   'inventoryIsNotGrammarGated': greg.get('inventoryIsNotGrammarGated'),
                   'unavailableRequestDisclosure':
                       greg.get('unavailableRequestDisclosure'),
                   'selectionMatters': greg.get('selectionMatters')},
           'syntaxClassIsNotCallerSelected': greg['standing'],
           'grammarsBySyntaxClass': by_class,
           'capabilityUnionByClass': {'code': sorted(code_caps),
                                      'data-document': sorted(data_caps)},
           'capabilitiesOnlyAvailableToCode': sorted(code_caps - data_caps),
           'capabilitiesSharedByBothClasses': sorted(code_caps & data_caps),
           'measuredOnSyntaxRuns': measured,
           'bodyAndNormalizerLaw': (
               'A normalized clone body identity is admissible only where the SELECTED '
               'grammar bundle retains a normalizer specification whose level applies to '
               'that grammar; the L0 level is byte-span only and needs no normalizer. The '
               'data-document class in this kit carries no clones capability, so a '
               'normalized body level is not merely unused there -- it is unavailable, and '
               'the honest record is the published unavailability pairing, never a '
               'complete-empty clones result.')}
    w('vectors/code-vs-data-matrix.json', doc)
    # the distinguishing measurement: data-document must NOT serve a code-only capability
    bad = []
    for m in measured:
        if m['selectedSyntaxClasses'] == ['data-document']:
            for p in m['servedPairs']:
                capid = p.split('@')[0]
                if capid in (code_caps - data_caps):
                    bad.append((m['run'], p))
    assert not bad, bad
    print('R-CODE-VS-DATA-MATRIX  classes=%s code-only caps=%s'
          % (sorted(by_class), sorted(code_caps - data_caps)))
    return doc


# --------------------------------------------------------------- R-ENUM-VS-RESOLUTION
def enum_vs_resolution():
    """Standing rule: do not invent a resolved rung for file facts. Measured over EVERY
    claimed graph: the `file` ladder is exactly the enumerated rung, every retained file
    fact sits on it, and no file fact carries a rung borrowed from another relation's
    ladder."""
    relreg = kit(B.RELATION_DOC)['x-opensip-relation-registry']
    file_ladder = relreg['relations']['file']['ladder']
    all_rungs = sorted({r for row in relreg['relations'].values() for r in row['ladder']})
    rows, bad = [], []
    for label in RUNS:
        st, c, rep = load(label)
        for fid, f in sorted(c.facts_seen.items()):
            if f['relation'] != 'file':
                continue
            rows.append({'run': label, 'factId': fid[:24], 'resolution': f['resolution'],
                         'onFileLadder': f['resolution'] in file_ladder})
            if f['resolution'] not in file_ladder:
                bad.append((label, fid, f['resolution']))
        for sid, sc in sorted(c.scopes_seen.items()):
            if sc['relation'] == 'file' and sc['resolution'] not in file_ladder:
                bad.append((label, 'scope:' + sid, sc['resolution']))
    doc = {'classification': 'measured', 'consumerId': CONSUMER,
           'law': B.RELATION_DOC + '#/x-opensip-relation-registry/relations/file/ladder',
           'fileLadder': file_ladder,
           'flatRungVocabulary': all_rungs,
           'rungsThatExistButAreNotAdmissibleForFile':
               [r for r in all_rungs if r not in file_ladder],
           'measuredFileFactRows': rows,
           'violations': bad,
           'standing': ('The flat rung vocabulary is necessary but never sufficient: a rung '
                        'that is a member of another relation ladder is refused for `file`, '
                        'not accepted. Inventory evidence stays enumerated; nothing in the '
                        'retained graph upgrades it to a resolved claim.')}
    w('vectors/enum-vs-resolution.json', doc)
    assert not bad, bad
    print('R-ENUM-VS-RESOLUTION  fileFacts=%d all on %s; inadmissible rungs for file=%d'
          % (len(rows), file_ladder, len(doc['rungsThatExistButAreNotAdmissibleForFile'])))
    return doc


def w(rel, obj):
    p = OUT + '/' + rel
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w') as f:
        json.dump(obj, f, indent=1, default=str)


def main():
    count_class_attempt()
    code_vs_data()
    enum_vs_resolution()


main()
