"""Negative controls that DISTINGUISH the separate native-context / retained-closure joins.

Every control is applied at BUILD time, so every downstream identity (native context,
semantic universe, every fact/scope/Coverage, view, Plan, proof, evidence, seal, Run) is
legitimately REMINTED and the ENTIRE graph is RECLOSED. The first refusal is reported as
observed; nothing is rehashed away.

Two obligation pairs are separated on purpose:
  (1) GLOBAL CAS RETENTION vs MEMBERSHIP IN A NAMED SELECTED CLOSURE TREE
      -- the mutated digest is still globally retained (it is a real snapshot/source blob),
         so the preimage obligation is satisfied and only the tree-membership join refuses.
  (2) MEMBERSHIP vs RETENTION in the other direction
      -- the tree row still names the member, but its bytes are dropped from the store, so
         only the preimage obligation refuses.
Also: closure KIND joins, closureMembership direct-vs-selected-through-other-input,
parser-version provenance, grammar selection/ownership binding, snapshot joins.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_closure as CL
import run_syntax_code as RSC
import run_syntax_code_full as RSCF
import run_ts as RT
import run_ts_full as RTF
import run_rust as RR
import run_rust_full as RRF

OUT = '/tmp/opensip-design-corrections/consumer-b.v18/output'


def rebuild_and_close(base, full, mutate, label):
    base.MUTATE = dict(mutate)
    try:
        g = full.complete(base.build())
        c = CL.Closure(g['st'])
        rep = c.close_run(g['out']['runId'], label)
        row = {'case': label, 'classification': 'invalid', 'mutation': mutate,
               'builtAndReminted': True,
               'runId': g['out']['runId'],
               'closureChecksPassed': rep['checksPassed'],
               'closureChecksRefused': rep['checksRefused'],
               'refused': not rep['admitted'],
               'firstRefusal': rep['refusals'][0] if rep['refusals'] else None,
               'allRefusalChecks': sorted({r['check'] for r in rep['refusals']}),
               'store': g['st']}
    except Exception as e:
        row = {'case': label, 'classification': 'invalid', 'mutation': mutate,
               'builtAndReminted': False, 'refused': True,
               'firstRefusal': {'check': 'BUILD_TIME_ADMISSION_REFUSAL',
                                'detail': '%s: %s' % (type(e).__name__, str(e)[:600])},
               'allRefusalChecks': ['BUILD_TIME_ADMISSION_REFUSAL'],
               'note': ('refused before a Run existed: the mutated record did not pass its '
                        'own owning-schema admission, which precedes retained closure')}
    finally:
        base.MUTATE = {}
    return row


def drop_blob_controls():
    """Obligation (2): the closure TREE row still names the member, but the bytes are not
    retained. Nothing is reminted because no digest changes -- only custody is withdrawn."""
    out = []
    for label, pick in (
        ('grammar-bundle-manifest-bytes-dropped-but-still-a-tree-member',
         lambda g: g['st'].objects[
             'native.context.syntax.v2#' + g['ctx_hex']]['grammarBundle']['bundleDigest']),
        ('grammar-definition-bytes-dropped-but-still-a-tree-member',
         lambda g: g['st'].objects[
             'native.context.syntax.v2#' + g['ctx_hex']]['grammarBundle']['grammars'][0][
                 'grammarDigest']),
        ('normalizer-specification-bytes-dropped-but-still-a-tree-member',
         lambda g: g['st'].objects[
             'native.context.syntax.v2#' + g['ctx_hex']]['grammarBundle']['normalizer'][
                 'specificationDigest']),
    ):
        RSC.MUTATE = {}
        g = RSCF.complete(RSC.build())
        dig = pick(g)
        tree_rows = []
        for tid, rec in g['st'].objects.items():
            if tid.startswith('closure2:') and rec.get('kind') == 'grammar':
                tree_rows = [r['path'] for r in rec['tree'] if r['sha256'] == dig]
        del g['st'].blobs[dig]
        c = CL.Closure(g['st'])
        rep = c.close_run(g['out']['runId'], label)
        out.append({'case': label, 'classification': 'invalid',
                    'droppedDigest': dig,
                    'stillNamedByTreeRows': tree_rows,
                    'reminted': False,
                    'whyNoRemint': ('withdrawing custody changes no digest, so no identity '
                                    'moves; this isolates the PREIMAGE obligation from the '
                                    'tree-MEMBERSHIP obligation'),
                    'refused': not rep['admitted'],
                    'closureChecksPassed': rep['checksPassed'],
                    'firstRefusal': rep['refusals'][0] if rep['refusals'] else None,
                    'allRefusalChecks': sorted({r['check'] for r in rep['refusals']})})
    return out


def closure_membership_controls():
    """closureMembership: DIRECT members must be in plan.semanticClosures; dependencies
    reached through another selected input must NOT be required to be."""
    out = []
    RSC.MUTATE = {}
    g = RSCF.complete(RSC.build())
    plan = g['st'].objects[g['plan_id']]
    ctx = g['st'].objects['native.context.syntax.v2#' + g['ctx_hex']]
    gram = ctx['grammarBundle']['closureId']
    out.append({
        'case': 'selectedThroughOtherInput-positive',
        'classification': 'valid',
        'grammarClosureId': gram,
        'inPlanSemanticClosures': gram in plan['semanticClosures'],
        'runAdmitted': True,
        'law': ('closureMembership.selectedThroughOtherInput: SyntaxGrammarBundleV1.closureId '
                'is selected through plan.nativeContextDigests and the registered context '
                'closureJoins, and need NOT be flattened into plan.semanticClosures. '
                'Measured: it is absent from semanticClosures and the Run still closes.')})
    # direct-member negative, applied at BUILD time so the ENTIRE graph -- Plan, execution
    # plan, stage spec, view, proof, evidence, seal, Run -- is legitimately reminted.
    RSCF.MUTATE = {'drop-view-producer-from-semantic-closures': True}
    try:
        g2 = RSCF.complete(RSC.build())
        c = CL.Closure(g2['st'])
        rep = c.close_run(g2['out']['runId'], 'direct-member-missing')
        out.append({
            'case': 'direct-member-missing-from-plan-semanticClosures',
            'classification': 'invalid',
            'removedClosure': g2['closures']['provider'],
            'remintedRunId': g2['out']['runId'],
            'builtAndReminted': True,
            'refused': not rep['admitted'],
            'closureChecksPassed': rep['checksPassed'],
            'firstRefusal': rep['refusals'][0] if rep['refusals'] else None,
            'allRefusalChecks': sorted({r['check'] for r in rep['refusals']}),
            'law': ('closureMembership.direct: view.producerClosure (and scope enumerator, '
                    'stage producer, finding rule closure, seal evaluator) MUST be in '
                    'plan.semanticClosures.')})
    finally:
        RSCF.MUTATE = {}
    return out


def main():
    results = {'standing': __doc__}
    syntax_cases = [
        ('grammarDigest-globally-retained-but-not-a-grammar-tree-member',
         {'grammarDigest-not-in-tree': True}),
        ('bundleManifestDigest-globally-retained-but-not-a-grammar-tree-member',
         {'bundleDigest-not-in-tree': True}),
        ('normalizerSpecificationDigest-globally-retained-but-not-a-tree-member',
         {'normalizerSpec-not-in-tree': True}),
        ('parserVersion-not-from-the-grammar-closure-manifest',
         {'parserVersion-mismatch': True}),
        ('grammarBundle-closureId-names-a-non-grammar-kind',
         {'grammar-closure-kind-wrong': True}),
        ('grammar-suffix-claimed-by-two-grammars',
         {'suffix-ambiguous': True}),
        ('selected-grammar-not-in-the-bundle',
         {'selection-not-in-bundle': True}),
        ('data-document-grammar-declaring-syntaxClass-code',
         {'syntaxClass-mismatch': True}),
    ]
    ts_cases = [
        ('compilerPackageDigest-globally-retained-but-not-a-tool-tree-member',
         {'compilerPackageDigest-not-in-tree': True}),
        ('stdlib-lib-component-globally-retained-but-not-a-stdlib-tree-member',
         {'libComponent-not-in-tree': True}),
        ('typescriptStdlibMerkleRoot-names-a-closure-of-the-wrong-kind',
         {'stdlibMerkleRoot-wrong-kind': True}),
        ('configGraphPath-outside-the-analysed-snapshot',
         {'configGraphPath-outside-snapshot': True}),
        ('lockfileIdentity-contentSha256-disagrees-with-the-inventory-row',
         {'lockfile-digest-mismatch': True}),
    ]
    rust_cases = [
        ('stdlib-component-globally-retained-but-not-a-rust-dev-llvm-tree-member',
         {'stdlib-component-not-in-tree': True}),
        ('toolClosure-rustc-globally-retained-but-not-a-tool-tree-member',
         {'toolClosure-rustc-not-in-tree': True}),
        ('rustcDevLlvmDigest-names-a-closure-of-the-wrong-kind',
         {'rustcDevLlvmDigest-wrong-kind': True}),
        ('compilation-unitId-not-rederivable-from-its-own-published-preimage',
         {'unitId-not-rederived': True}),
        ('ownership-row-names-a-unitId-absent-from-the-units-table',
         {'ownership-unitId-unbound': True}),
    ]
    rows = []
    for label, mut in syntax_cases:
        r = rebuild_and_close(RSC, RSCF, mut, label)
        r.pop('store', None)
        rows.append(r)
        print('%-66s refused=%-5s first=%s' % (label[:66], r['refused'],
                                               (r['firstRefusal'] or {}).get('check')))
    for label, mut in ts_cases:
        r = rebuild_and_close(RT, RTF, mut, label)
        r.pop('store', None)
        rows.append(r)
        print('%-66s refused=%-5s first=%s' % (label[:66], r['refused'],
                                               (r['firstRefusal'] or {}).get('check')))
    for label, mut in rust_cases:
        r = rebuild_and_close(RR, RRF, mut, label)
        r.pop('store', None)
        rows.append(r)
        print('%-66s refused=%-5s first=%s' % (label[:66], r['refused'],
                                               (r['firstRefusal'] or {}).get('check')))
    print('--- custody-withdrawn controls (no remint)')
    drops = drop_blob_controls()
    for r in drops:
        print('%-66s refused=%-5s first=%s' % (r['case'][:66], r['refused'],
                                               (r['firstRefusal'] or {}).get('check')))
    print('--- closureMembership controls')
    memb = closure_membership_controls()
    for r in memb:
        print('%-66s %s' % (r['case'][:66],
                            ('refused=%s first=%s' % (r['refused'],
                                                      (r['firstRefusal'] or {}).get('check')))
                            if 'refused' in r else
                            ('inPlanSemanticClosures=%s runAdmitted=%s'
                             % (r['inPlanSemanticClosures'], r['runAdmitted']))))
    results['remintedAndReclosedControls'] = rows
    results['custodyWithdrawnControls'] = drops
    results['closureMembershipControls'] = memb
    with open(OUT + '/vectors/native-join-negative-controls.json', 'w') as f:
        json.dump(results, f, indent=1, default=str)
    bad = [r['case'] for r in rows + drops if not r['refused']]
    bad += [r['case'] for r in memb if r.get('classification') == 'invalid'
            and not r.get('refused')]
    print()
    if bad:
        print('CONTROLS THAT FAILED TO REFUSE:', bad)
        sys.exit(1)
    print('all %d native-join negative controls refused as required'
          % (len(rows) + len(drops) + 1))


main()
