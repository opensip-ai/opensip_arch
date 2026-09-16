"""Discriminating negative controls over an EXPORTED positive Run.

Two families, deliberately kept apart:

A. TAMPERED-RESULT controls (composition section 7). Every one PRESERVES valid record
   identities and citation membership and INDEPENDENTLY REMINTS all enclosing identities,
   so the tampered graph is hash-consistent and linkage-valid. Only SEMANTIC REPLAY can
   refuse it. This is exactly why "helper self-consistency (reminted C-byte equality,
   verdict/count equality)" is not admission.

B. IDENTITY/RETENTION controls (identity-and-evidence section 6 reference checks):
   altered frame, missing preimage, wrong preimage, unregistered H domain, a raw payload
   offered where an H identity is required, and a hidden input. These are refused at
   retained-closure admission, BEFORE replay.

Neither family is a claim about future authentication or host qualification.
"""
import base64
import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_store as ST
import opensip_closure as CL
import opensip_replay as R


def load(path):
    return json.load(open(path))


def store_from_doc(doc):
    s = ST.Store()
    for d, b64 in doc['blobs'].items():
        s.blobs[d] = base64.b64decode(b64)
    for tid, row in doc['objectTable'].items():
        s.objects[tid] = row['record']
        s.meta[tid] = {'domain': row['domain'], 'frameDigest': row['frameDigest']}
    s.labels = doc.get('labels', {})
    return s


def write_doc(doc, st, path, claim):
    doc = copy.deepcopy(doc)
    doc['blobs'] = {d: base64.b64encode(b).decode('ascii')
                    for d, b in sorted(st.blobs.items())}
    doc['objectTable'] = {k: {'domain': st.meta[k]['domain'],
                              'frameDigest': st.meta[k]['frameDigest'],
                              'record': v} for k, v in sorted(st.objects.items())}
    doc['claim'] = claim
    doc['blobCount'] = len(st.blobs)
    doc['objectCount'] = len(st.objects)
    doc['totalBlobBytes'] = sum(len(b) for b in st.blobs.values())
    with open(path, 'w') as f:
        json.dump(doc, f)
    return path


def remint(st, proof, evidence, seal, run):
    """Independently remint every enclosing identity so the tampered graph is internally
    hash-consistent: a tamperer CAN do this, and a stale-hash check would not catch it."""
    proof_id = K.ID('proof-bundle', proof)
    evidence = dict(evidence, proofBundleId=proof_id, findingIds=proof['findingIds'])
    ev_id = K.ID('semantic-evidence', evidence)
    seal = dict(seal, proofBundleId=proof_id, evidenceId=ev_id, verdict=proof['verdict'])
    seal_id = K.ID('evaluation-seal', seal)
    run = dict(run, evidenceId=ev_id, evaluationSealId=seal_id)
    run_id = K.ID('run', run)
    for dom, obj in (('proof-bundle', proof), ('semantic-evidence', evidence),
                     ('evaluation-seal', seal), ('run', run)):
        st.put_framed(dom, obj)
    return proof_id, ev_id, seal_id, run_id


def tamper_cases(doc, st):
    """Return a list of (name, description, mutate_fn)."""
    cases = []

    def c(name, desc, fn):
        cases.append({'name': name, 'description': desc, 'fn': fn})

    c('verdict-flipped',
      'proof.verdict pass -> fail; every fact, Coverage, witness, finding and citation is '
      'byte-identical and every enclosing identity is reminted.',
      lambda p, w, f: p.__setitem__('verdict', 'fail' if p['verdict'] != 'fail' else 'pass'))

    def flip_predicate(p, w, f):
        for pp in p['predicateProofs']:
            if pp['value'] == 'indeterminate':
                pp['value'] = 'true'
                return
        p['predicateProofs'][0]['value'] = (
            'false' if p['predicateProofs'][0]['value'] == 'true' else 'true')
    c('predicate-value-flipped',
      'one predicateProofs[].value changed (indeterminate -> true) with the SAME witness '
      'digest, the same matching fact and Coverage sets and the same counts.',
      flip_predicate)

    def rule_outcome(p, w, f):
        for rr in p['ruleResults']:
            if rr['outcome'] == 'pass':
                rr['outcome'] = 'fail'
                return
    c('rule-outcome-flipped', 'one ruleResults[].outcome pass -> fail.', rule_outcome)

    def enum_drop(p, w, f):
        for rr in p['ruleResults']:
            if len(rr['enumeration']['selectedSubjectIds']) > 1:
                rr['enumeration']['selectedSubjectIds'] = \
                    rr['enumeration']['selectedSubjectIds'][:-1]
                return
    c('enumeration-subject-dropped',
      'one ruleResults[].enumeration.selectedSubjectIds member removed: the enumeration '
      'claim no longer matches the independently derived census.', enum_drop)

    def waiver_add(p, w, f):
        if p['findingIds']:
            p['waivedFindingIds'] = K.cset_strings(list(p['waivedFindingIds'])
                                                   + [p['findingIds'][0]])
    c('waiver-membership-added',
      'waivedFindingIds gains an existing finding id although the effective WaiverSet '
      'targets nothing: waiver membership is recomputed from the retained waiver bytes.',
      waiver_add)

    def finding_drop(p, w, f):
        if p['findingIds']:
            p['findingIds'] = p['findingIds'][1:]
    c('finding-dropped',
      'one finding id removed from proof.findingIds (and therefore from evidence) while '
      'the finding record itself stays retained.', finding_drop)

    def deficiency_drop(p, w, f):
        for rr in p['ruleResults']:
            if rr['deficiencies']:
                rr['deficiencies'] = rr['deficiencies'][1:]
                return
    c('deficiency-dropped',
      'one recomputed evaluation-deficiency removed from a ruleResult: all deficiencies '
      'remain visible in the reference result, including on a branch whose value does not '
      'determine the root.', deficiency_drop)
    return cases


def run_tamper(export_path, outdir):
    doc = load(export_path)
    base_st = store_from_doc(doc)
    cl0 = CL.Closure(base_st)
    cl0.close_run(doc['claim']['runId'], 'base')
    run0 = cl0.resolved[doc['claim']['runId']]
    seal0 = cl0.resolved[run0['evaluationSealId']]
    ev0 = cl0.resolved[run0['evidenceId']]
    proof0 = cl0.resolved[seal0['proofBundleId']]

    results = []
    for case in tamper_cases(doc, base_st):
        st = store_from_doc(doc)
        p = copy.deepcopy(proof0)
        case['fn'](p, None, None)
        if K.C(p) == K.C(proof0):
            # the mutation has no target in THIS positive (e.g. no ruleResult deficiency to
            # drop). Recorded as not-applicable rather than silently counted as a pass.
            results.append({'case': case['name'], 'description': case['description'],
                            'classification': 'invalid',
                            'applicable': False,
                            'reason': ('this positive Run carries no instance of the field '
                                       'this control mutates, so no tampered variant '
                                       'exists; exercised on the other positives'),
                            'refused': True, 'replayVerdict': 'NOT-APPLICABLE',
                            'closureAdmitted': None})
            continue
        pid, evid, sealid, runid = remint(st, p, copy.deepcopy(ev0), copy.deepcopy(seal0),
                                         copy.deepcopy(run0))
        path = os.path.join(outdir, 'tamper-%s.store.json' % case['name'])
        write_doc(doc, st, path, {**doc['claim'], 'runId': runid, 'sealId': sealid,
                                  'evidenceId': evid, 'proofId': pid,
                                  'verdict': p['verdict']})
        res = R.replay(path, 'tamper:' + case['name'])
        row = {'case': case['name'], 'description': case['description'],
               'classification': 'invalid',
               'identitiesReminted': True,
               'tamperedRunId': runid,
               'originalRunId': doc['claim']['runId'],
               'citationMembershipPreserved': True,
               'closureAdmitted': res['closure']['admitted'],
               'closureChecksPassed': res['closure']['checksPassed'],
               'closureRefusals': res['closure']['refusals'],
               'replayVerdict': res['verdict'],
               'refused': res['verdict'] != 'REPLAY_MATCH',
               'firstRefusal': None, 'masksLater': None,
               'exportPath': path}
        if res.get('replayAttempted'):
            diffs = []
            for cmpd in res['bundleComparisons']:
                if not cmpd['equal']:
                    diffs.append({'object': cmpd['object'],
                                  'fields': [d['field'] for d in
                                             cmpd.get('fieldDifferences', [])]})
            row['semanticReplayDifferences'] = diffs
            row['firstRefusal'] = ('semantic replay comparison of the complete proof bundle: '
                                   + json.dumps(diffs)[:300])
            row['masksLater'] = ('No -- retained-closure admission PASSED on this graph '
                                 '(%d checks) because every identity was reminted and every '
                                 'citation stayed a member; only semantic replay refuses it.'
                                 % res['closure']['checksPassed'])
        else:
            row['firstRefusal'] = 'retained-closure admission'
            row['masksLater'] = ('Yes -- closure refused before replay, so the semantic '
                                 'comparison was not reached for this graph.')
        with open(path.replace('.store.json', '.replay.json'), 'w') as f:
            res.pop('closureFullReport', None)
            json.dump(res, f, indent=1)
        results.append(row)
    return results


def run_identity_controls(export_path, outdir):
    doc = load(export_path)
    claim = doc['claim']
    out = []

    def attempt(name, desc, mutate, masks=None):
        """mutate(st) returns either a description string, or (description, newRunId) when
        the control re-keys and reminints, so the closure walks the mutated Run."""
        st = store_from_doc(doc)
        target = mutate(st)
        run_id = claim['runId']
        if isinstance(target, tuple):
            target, run_id = target
        cl = CL.Closure(st)
        rep = cl.close_run(run_id, name)
        row = {'case': name, 'description': desc, 'classification': 'invalid',
               'target': target, 'runIdClosed': run_id,
               'closureAdmitted': rep['admitted'],
               'refused': not rep['admitted'],
               'checksPassed': rep['checksPassed'],
               'firstRefusal': (rep['refusals'][0] if rep['refusals'] else None),
               'allRefusals': rep['refusals'][:6],
               'masksLater': masks or ('Yes -- this retained-closure refusal precedes '
                                       'semantic proof replay entirely; the replay '
                                       'comparison is never reached.')}
        out.append(row)
        return row

    # 1. altered frame: flip one byte inside a retained H preimage frame
    def alter_frame(st):
        run_hex = claim['runId'].split(':', 1)[1]
        fr = bytearray(st.blobs[run_hex])
        fr[-2] ^= 0x01
        st.blobs[run_hex] = bytes(fr)
        return 'run3 frame byte flipped, key unchanged'
    attempt('altered-frame',
            'One byte inside the retained run3 H preimage frame is flipped while the CAS '
            'key is left alone: the stored bytes no longer re-hash to the key.', alter_frame)

    # 2. missing preimage
    def drop_preimage(st):
        pol = None
        for tid, rec in st.objects.items():
            if tid.startswith('plan2:'):
                pol = rec['policyDigest']
        del st.blobs[pol]
        return 'plan.policyDigest preimage removed (declaration kept)'
    attempt('missing-preimage',
            'The Plan still DECLARES policyDigest but the PolicyDocumentV2 preimage bytes '
            'are not retained. A digest declaration alone never retains its bytes.',
            drop_preimage)

    # 3. wrong preimage: different bytes stored under an existing digest
    def wrong_preimage(st):
        pol = None
        for tid, rec in st.objects.items():
            if tid.startswith('plan2:'):
                pol = rec['policyDigest']
        st.blobs[pol] = b'{"schemaFamily":"opensip.product.policy"}'
        return 'policy preimage replaced with other bytes under the same key'
    attempt('wrong-preimage',
            'Different bytes are stored under the policy digest, so the fetched preimage '
            'does not re-hash to the digest that named it.', wrong_preimage)

    # 4. unregistered H domain -- RE-KEYED so the rehash check passes and the
    #    frame-domain check is the FIRST refusal rather than being masked by it
    def unregistered_domain(st):
        cl = CL.Closure(store_from_doc(doc))
        cl.close_run(claim['runId'], 'x')
        run = copy.deepcopy(cl.resolved[claim['runId']])
        plan = cl.resolved[run['planId']]
        frame = K.h_frame('plan.v3-unregistered', plan)
        nhex = K.raw_sha256(frame)
        st.blobs[nhex] = frame
        st.objects['plan2:' + nhex] = plan
        st.meta['plan2:' + nhex] = {'domain': 'plan', 'frameDigest': nhex}
        run['planId'] = 'plan2:' + nhex
        st.put_framed('run', run)
        return ('plan preimage re-framed under domain "plan.v3-unregistered", stored under '
                'its OWN digest, and run.planId repointed with run3 reminted',
                K.ID('run', run))
    attempt('unregistered-h-domain',
            'The Plan preimage is re-framed under a domain that no domain set registers, '
            'and is stored under its own correct digest so the rehash check passes. Frame '
            'admission requires the domain to be a member of the annotation\'s named set.',
            unregistered_domain,
            masks=('No -- the frame is stored under its own correct digest, so the '
                   'PREIMAGE_REHASH_MISMATCH check passes and the frame-domain check is '
                   'the first refusal. Compare the same-key variant below, where the '
                   'rehash check fires first and masks this one.'))

    def unregistered_domain_same_key(st):
        for tid, rec in list(st.objects.items()):
            if tid.startswith('plan2:'):
                hx = tid.split(':', 1)[1]
                st.blobs[hx] = K.h_frame('plan.v3-unregistered', rec)
                return 'plan frame re-framed in place, CAS key left unchanged'
    attempt('unregistered-h-domain-same-key-masked',
            'Same fault written in place under the original key. Recorded to show the '
            'MASKING explicitly: the CAS rehash check refuses first and the frame-domain '
            'check is never reached.', unregistered_domain_same_key,
            masks=('Yes -- PREIMAGE_REHASH_MISMATCH fires first and masks the '
                   'FRAME_DOMAIN_UNREGISTERED check this case was written to exercise.'))

    # 5. raw canonical payload offered where an H identity frame is required -- RE-KEYED
    def raw_payload_as_h(st):
        cl = CL.Closure(store_from_doc(doc))
        cl.close_run(claim['runId'], 'x')
        run = copy.deepcopy(cl.resolved[claim['runId']])
        snap = cl.resolved[run['snapshotId']]
        payload = K.C(snap)
        nhex = K.raw_sha256(payload)
        st.blobs[nhex] = payload
        run['snapshotId'] = 'snapshot2:' + nhex
        st.put_framed('run', run)
        return ('C(snapshot) stored under SHA256(C(snapshot)) and run.snapshotId repointed '
                'at it, with run3 reminted', K.ID('run', run))
    attempt('raw-payload-offered-as-h-identity',
            'C(X) is offered where the annotation says h-identity, under its own correct '
            'raw digest. C(X) does not begin with the framing prefix and SHA256(C(X)) is '
            'not H(D,X), so it fails the prefix.', raw_payload_as_h,
            masks=('No -- the payload is stored under its own correct digest, so the rehash '
                   'check passes and the FRAME_PREFIX check is the first refusal.'))

    # 6. hidden input: a well-formed, hash-valid fact outside the evaluated closure,
    #    cited as finding evidence
    def hidden_input(st):
        src = None
        for tid, rec in st.objects.items():
            if tid.startswith('fact2:'):
                src = (tid, rec)
                break
        hidden = dict(src[1], confidenceMillionths=999999)
        hframe = K.h_frame('fact', hidden)
        hhex = K.raw_sha256(hframe)
        st.blobs[hhex] = hframe
        st.objects['fact2:' + hhex] = hidden
        st.meta['fact2:' + hhex] = {'domain': 'fact', 'frameDigest': hhex}
        # cite it from a finding and remint the finding + enclosing identities
        cl = CL.Closure(store_from_doc(doc))
        cl.close_run(claim['runId'], 'hidden-base')
        run = cl.resolved[claim['runId']]
        seal = cl.resolved[run['evaluationSealId']]
        ev = cl.resolved[run['evidenceId']]
        proof = copy.deepcopy(cl.resolved[seal['proofBundleId']])
        fid = proof['findingIds'][0]
        f = copy.deepcopy(cl.resolved[fid])
        f['evidenceRefs'] = K.cset(list(f['evidenceRefs'])
                                   + [{'domain': 'fact', 'digest': hhex}])
        new_fid = K.ID('finding', f)
        st.put_framed('finding', f)
        proof['findingIds'] = K.cset_strings(
            [x for x in proof['findingIds'] if x != fid] + [new_fid])
        _, _, _, new_run = remint(st, proof, copy.deepcopy(ev), copy.deepcopy(seal),
                                  copy.deepcopy(run))
        return ('a hash-valid fact2 outside every evaluated view cited from a finding, with '
                'the finding and every enclosing identity reminted', new_run)
    attempt('hidden-input-cited-as-finding-evidence',
            'A well-formed, hash-valid fact2 that belongs to no evaluated view is cited '
            'from a finding. identity section 3: "A well-formed, hash-valid object outside '
            'this closure is refused, rather than admitted as hidden finding evidence."',
            hidden_input,
            masks=('No -- the graph is fully reminted and internally hash-consistent, so '
                   'every digest and frame check passes; the citation-closure join is the '
                   'first refusal.'))
    return out
