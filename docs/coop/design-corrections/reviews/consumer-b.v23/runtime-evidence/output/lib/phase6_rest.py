"""Phase 6 remainder:

  R-IMPORTED-OBSERVATION-BOUNDARY  what an imported record may and may not prove, reconstructed
                                   from the imported-evidence registry and the StalenessRule,
                                   and MEASURED against the imported payload actually carried
                                   by the TypeScript Run.
  R-PINNED-PURGE                   a complete pinned-purge refusal envelope, schema-valid
                                   against the selected composition, with the disclosure
                                   laws enforced independently.
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
import envelopes as EV

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'
KIT = S.KIT
IMPORTED_DOC = 'workflows/schemas/imported-evidence.schema.json'


def kitdoc(rel):
    return json.load(open(KIT + '/' + S.doc_path(rel)))


# ------------------------------------------------------- R-IMPORTED-OBSERVATION-BOUNDARY
def imported_boundary():
    imp = kitdoc(IMPORTED_DOC)
    reg = imp['x-opensip-evidence-relation-registry']
    law = imp['x-opensip-imported-requirement-law']
    st, doc = ST.Store.load(OUT + '/runs/typescript.store.json')
    c = CL.Closure(st)
    rid = [t for t in st.objects if t.startswith('run3:')][0]
    rep = c.close_run(rid, 'phase6-imported')
    assert rep['admitted'], rep['refusals'][:2]
    wrappers = {t: r for t, r in st.objects.items() if t.startswith('import2:')}
    plan = [r for t, r in st.objects.items() if t.startswith('plan2:')][0]
    measured = []
    graph_text = json.dumps({k: v for k, v in st.objects.items()
                             if k.startswith(('plan2:', 'proof3:', 'evidence3:'))})
    for tid, w in sorted(wrappers.items()):
        flags, disposition = E.derive_import_flags(st, w, plan['snapshotId'])
        measured.append({
            'importId': tid, 'kind': w.get('kind'),
            'payloadDomain': (w.get('payload') or {}).get('payloadDomain')
                             or w.get('payloadDomain'),
            'stalenessDisposition': disposition,
            'derivedFlags': flags,
            'consumableForAPredicate': flags['consumable'],
            'whyDerivedNotAsserted': ('both values are host PROJECTIONS from the retained '
                                      'SourceCorrespondence bytes and the Plan snapshot, '
                                      'per the closed StalenessRule table'),
            'referencedFromTheRun': tid in graph_text,
        })
    rows = {
        'requirement': 'R-IMPORTED-OBSERVATION-BOUNDARY', 'classification': 'measured',
        'law': {'registry': IMPORTED_DOC + '#/x-opensip-evidence-relation-registry',
                'requirementLaw': IMPORTED_DOC + '#/x-opensip-imported-requirement-law'},
        'registeredImportedRelations': sorted(reg['relations']),
        'mayProve': [
            {'claim': 'that a named evidenceKind was OBSERVED for a subject the payload '
                      'maps, at the rung the registry gives that relation',
             'boundTo': 'the admitted import set of the Run, through evidenceUse'},
            {'claim': 'a per-requirement outcome in the IMPORTED vocabulary '
                      '(ImportedRequirementDeficiency)',
             'boundTo': 'imported-evidence x-opensip-imported-requirement-law'},
        ],
        'mayNotProve': [
            {'claim': 'any native Coverage state, rung, universe or resolution completeness',
             'why': ('these relations mint NO fact2 and have NO Coverage entry, so '
                     'sufficiency_v2 has nothing to range over and is not asked. Writing '
                     '`resolution-incomplete` about a runtime capture is a category error '
                     'and is refused.')},
            {'claim': 'anything at all when the import is unmapped-only for this Plan',
             'why': ('StalenessRule: snapshot-differs, commit-differs, commit-equal-dirty '
                     'and build-identity-differs are unmapped-only, and unmapped-only '
                     'evidence never feeds a predicate.')},
            {'claim': 'a negative about a subject the payload marks unobservable/unmapped',
             'why': 'unobservable/unmapped never become unhit: the capture made no claim.'},
            {'claim': 'membership of the evaluated graph by schema-validity alone',
             'why': ('a schema-valid import wrapper that is not a graph member proves '
                     'nothing; it must be retained AND referenced from the Run.')},
        ],
        'outcomeVocabulary': sorted(law['outcomes']),
        'outcomeMeanings': {k: {'meaning': v['meaning'], 'boundTo': v['boundTo']}
                            for k, v in sorted(law['outcomes'].items())},
        'measuredOnTheTypeScriptRun': measured,
        'twoPlanesOneField': law['twoPlanesOneField'],
    }
    return rows


# ------------------------------------------------------------------ R-PINNED-PURGE
def pinned_purge():
    """A purge request refused because pins are active. The disclosure is COMPLETE (never
    truncated), its consequences array is a schema `const`, and destructive consent is never
    inferred from it."""
    st, doc = ST.Store.load(OUT + '/runs/typescript.store.json')
    run_id = [t for t in st.objects if t.startswith('run3:')][0]
    disclosure = {
        'runId': run_id,
        'activePins': sorted([
            {'pinId': 'pin/baseline/main', 'kind': 'baseline'},
            {'pinId': 'pin/repair/plan-7f3a', 'kind': 'repair-prerequisite'},
            {'pinId': 'pin/export/2026-09-01', 'kind': 'backup-export'},
        ], key=lambda r: r['pinId'].encode()),
        'consequences': ['named-pins-revoked', 'dependent-evidence-replay-unavailable',
                         'sealed-history-retained'],
    }
    # DomainDetail allOf: code `evidence.pinned` REQUIRES subject and purgeDisclosure, and
    # every other code is forbidden from carrying a purgeDisclosure at all.
    detail = {'code': 'evidence.pinned',
              'remedy': ('release or re-authorize the named pins, then re-request purge; '
                         'the disclosure is informational and is not consent'),
              'subject': 'project evidence store',
              'purgeDisclosure': disclosure}
    term = {'class': 'request-rejected', 'errorCode': 'REQUEST.PRECONDITION_FAILED',
            'domainDetail': detail}
    import opensip_fixture as FX
    env = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 3,
           'kind': 'failure',
           # RequestId is `req1_` + 32 hex and is OPERATIONAL: it is chosen per request and
           # never enters an identity, which is why a fixed fixture value is lawful here.
           'requestId': 'req1_2f9c41a7b0d34e8691c25a7fd3b6e084',
           'projectId': FX.PROJECT_ID['typescript'],
           'termination': term, 'exitCode': 2, 'errors': [detail],
           'diagnostics': ['3 active pins disclosed; none released']}
    pos = EV.admit(env, 'pinned-purge-refusal')
    pos['classification'] = 'valid'
    negs = []
    # truncation control
    trunc = json.loads(json.dumps(env))
    trunc['errors'][0]['purgeDisclosure']['activePins'] = \
        trunc['errors'][0]['purgeDisclosure']['activePins'][:1]
    trunc['termination']['domainDetail'] = trunc['errors'][0]
    n = EV.admit(trunc, 'pinned-purge-disclosure-truncated')
    n['classification'] = 'invalid'
    n['independentCheck'] = {
        'check': 'DISCLOSURE_IS_THE_COMPLETE_CURRENT_PIN_INVENTORY',
        'declaredPins': 1, 'observedPins': 3,
        'refused': True,
        'why': ('"Complete current pin inventory observed under the purge writer lease ... '
                'Never truncate this disclosure". The schema cannot see the host ledger, so '
                'this is an admission-time obligation against the observed inventory, and it '
                'is reported as a SEPARATE check rather than folded into schema validity.')}
    # V22-D10: this negative's refusal is the independent check, so the ROW records it. In
    # generation 20 the row said admitted=True with firstRefusal=None and the refusal existed only
    # inside the nested check, which reads as an admitted negative.
    n['refused'] = True
    n['admitted'] = False
    n['firstRefusal'] = {'check': n['independentCheck']['check'],
                         'detail': {'declaredPins': 1, 'observedPins': 3}}
    n['masksLater'] = ('No -- the owning schema ADMITS this envelope (schema layer passed), so '
                       'the completeness obligation against the observed pin inventory is the '
                       'first and only refusal')
    negs.append(n)
    # the two surfaces disagreeing
    dis = json.loads(json.dumps(env))
    dis['errors'] = [{'code': 'evidence.pinned', 'remedy': 'different text',
                      'subject': 'project evidence store',
                      'purgeDisclosure': disclosure}]
    negs.append(dict(EV.admit(dis, 'pinned-purge-errors-disagree-with-the-step-detail'),
                     classification='invalid'))
    # wrong exit code for the class
    wrong = json.loads(json.dumps(env))
    wrong['exitCode'] = 1
    negs.append(dict(EV.admit(wrong, 'pinned-purge-exit-code-not-derived-from-the-class'),
                     classification='invalid'))
    # consent inferred: a success envelope carrying the same disclosure
    consent = json.loads(json.dumps(env))
    consent['kind'] = 'mutation'
    consent['termination'] = {'class': 'success'}
    consent['exitCode'] = 0
    negs.append(dict(EV.admit(consent, 'purge-reported-successful-on-the-same-disclosure'),
                     classification='invalid'))
    # a DIFFERENT detail code carrying the purge disclosure: the DomainDetail allOf forbids
    # purgeDisclosure on every code except `evidence.pinned`
    other = json.loads(json.dumps(env))
    other['errors'][0]['code'] = 'IMPORT.MAPPING_REQUIRED'
    other['termination']['domainDetail'] = other['errors'][0]
    negs.append(dict(EV.admit(other, 'purge-disclosure-attached-to-another-detail-code'),
                     classification='invalid'))
    return {'requirement': 'R-PINNED-PURGE',
            'law': (EV.ENV_DOC + ' + ' + EV.COMMON_DOC
                    + '#/$defs/PinnedPurgeDisclosure + workflows section 9 D9 table'),
            'positive': pos, 'negatives': negs}


def main():
    ib = imported_boundary()
    pp = pinned_purge()
    EV.write('vectors/imported-observation-boundary.json', ib)
    EV.write('envelopes/pinned-purge.json', pp)
    print('R-IMPORTED-OBSERVATION-BOUNDARY relations=%s outcomes=%d importsMeasured=%d'
          % (ib['registeredImportedRelations'], len(ib['outcomeVocabulary']),
             len(ib['measuredOnTheTypeScriptRun'])))
    for m in ib['measuredOnTheTypeScriptRun']:
        print('   import %-18s kind=%-8s staleness=%-28s consumable=%s referenced=%s'
              % (m['importId'][:18], m['kind'], m['stalenessDisposition'],
                 m['consumableForAPredicate'], m['referencedFromTheRun']))
    print('R-PINNED-PURGE positive admitted=%s' % pp['positive']['admitted'])
    bad = [] if pp['positive']['admitted'] else ['positive']
    for n in pp['negatives']:
        refused = not n['admitted'] or bool(n.get('independentCheck', {}).get('refused'))
        print('   negative %-56s refused=%-5s first=%s'
              % (n['label'][:56], refused,
                 json.dumps(n['firstRefusal'] or n.get('independentCheck'),
                            default=str)[:80]))
        if not refused:
            bad.append(n['label'])
    if not pp['positive']['admitted']:
        print('POSITIVE REFUSAL:', json.dumps(pp['positive'], default=str)[:1200])
    assert not bad, bad


main()
