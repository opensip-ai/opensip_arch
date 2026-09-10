#!/usr/bin/env python3
"""Deterministic dependency selection reference model; no product/trust claim.

Input admission/current-trust fields are observations from the future security
verifier, not signatures made or verified by this model. The fixture JSON byte
encoding is fixture custody only. Production canonical lock preimages are owned
by opensip-metadata-canonical.1 and must be joined separately.

Requires jsonschema==4.25.1; replay with the documented review virtualenv or an
equivalent pinned environment. Version 3 repairs COMP2-M1 and admits input structure before dereferencing fields.
"""
from __future__ import annotations
import argparse
import copy
from functools import cmp_to_key
import hashlib
import json
from pathlib import Path
from jsonschema import Draft202012Validator
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LOCK_SCHEMA = json.loads((HERE / 'component-lock-schema.completed.v2.json').read_text())
INPUT_VALIDATOR = Draft202012Validator(LOCK_SCHEMA['properties']['resolutionInputs'])
LOCK_VALIDATOR = Draft202012Validator(LOCK_SCHEMA)
SEMVER = re.compile(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-(0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?')
CAPS = ['typescript.calls', 'typescript.imports', 'typescript.reachability', 'typescript.references', 'typescript.types']


def fixture_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def sha(value):
    return hashlib.sha256(value).hexdigest()


def compare_bytes(a, b):
    return (a > b) - (a < b)


def version(value):
    if not isinstance(value, str) or not SEMVER.fullmatch(value):
        raise ValueError('invalid SemVer')
    core, sep, pre = value.split('+', 1)[0].partition('-')
    return tuple((len(p), p) for p in core.split('.')), pre.split('.') if sep else []


def compare_versions(a, b):
    ac, ap = version(a)
    bc, bp = version(b)
    if ac != bc:
        return compare_bytes(ac, bc)
    if not ap or not bp:
        return compare_bytes(not ap, not bp)
    for av, bv in zip(ap, bp):
        if av == bv:
            continue
        if av.isdigit() and bv.isdigit():
            return compare_bytes((len(av), av), (len(bv), bv))
        if av.isdigit() != bv.isdigit():
            return -1 if av.isdigit() else 1
        return compare_bytes(av.encode(), bv.encode())
    return compare_bytes(len(ap), len(bp))


def valid_constraint(c):
    try:
        if isinstance(c, str):
            version(c)
            return True
        if not isinstance(c, dict) or set(c) != {'min', 'max', 'includeMin', 'includeMax'}:
            return False
        if type(c['includeMin']) is not bool or type(c['includeMax']) is not bool:
            return False
        relation = compare_versions(c['min'], c['max'])
        return relation < 0 or relation == 0 and c['includeMin'] and c['includeMax']
    except (ValueError, TypeError):
        return False


def satisfies(v, c):
    if not valid_constraint(c):
        return False
    try:
        core, pre = version(v)
        if isinstance(c, str):
            return v == c
        if pre and not any(version(c[b])[0] == core and version(c[b])[1] for b in ['min', 'max']):
            return False
        lo, hi = compare_versions(v, c['min']), compare_versions(v, c['max'])
        return (lo > 0 or lo == 0 and c['includeMin']) and (hi < 0 or hi == 0 and c['includeMax'])
    except ValueError:
        return False


def provenance_bytes(provenance):
    # Explicit field ordering, not repr(), dictionary insertion order or locale.
    return (provenance['publisher'].encode('utf-8'), provenance['sourceClass'].encode('utf-8'))


def candidate_compare(a, b):
    """Project before global, then highest precedence, then ascending byte ties."""
    for av, bv in [(0 if a['scope'] == 'project' else 1, 0 if b['scope'] == 'project' else 1)]:
        if av != bv:
            return compare_bytes(av, bv)
    sem = compare_versions(a['version'], b['version'])
    if sem:
        return -sem
    for av, bv in [(a['version'].encode(), b['version'].encode()),
                   (provenance_bytes(a['provenance']), provenance_bytes(b['provenance'])),
                   (a['manifestDigest'].encode(), b['manifestDigest'].encode())]:
        if av != bv:
            return compare_bytes(av, bv)
    return 0


def tuple_compare(a, b):
    """Output order differs from preference: UUID, ascending version, scope."""
    if a['stableId'] != b['stableId']:
        return compare_bytes(a['stableId'].encode(), b['stableId'].encode())
    sem = compare_versions(a['version'], b['version'])
    if sem:
        return sem
    for av, bv in [(a['version'].encode(), b['version'].encode()),
                   (0 if a['scope'] == 'global' else 1, 0 if b['scope'] == 'global' else 1),
                   (provenance_bytes(a['provenance']), provenance_bytes(b['provenance'])),
                   (a['manifestDigest'].encode(), b['manifestDigest'].encode())]:
        if av != bv:
            return compare_bytes(av, bv)
    return 0


class Exhausted(Exception):
    pass


def solve(data, model_visit_limit=100000, model_depth_limit=64):
    """Depth-first search over root IDs; every branch recomputes closure constraints.

    Returns no partial lock on any refusal or exhaustion. Model-only test limits
    exercise boundary arithmetic; the architecture's production limits stay
    100000 visits and 64 dependency vertices.
    """
    visits, rejections = 0, set()
    def refuse(reason):
        return {'status': 'REFUSE', 'reason': reason, 'resolved': [], 'visits': visits}
    # Structural admission must precede every resolutionInputs dereference.
    x = data.get('resolutionInputs') if isinstance(data, dict) else None
    if not INPUT_VALIDATOR.is_valid(x):
        return refuse('INPUT-SCHEMA')
    releases = data['index']['releases']
    if not data['index'].get('custodyValid') or sha(fixture_bytes(data['index'])) != x['indexDigest']:
        return refuse('INDEX-CUSTODY')
    if x['requestedProfile'] != 'preview-typescript' or x['requestedCapabilities'] != CAPS:
        return refuse('PROFILE-OR-CAPABILITIES')
    scope = x['scopeContext']
    if scope['allowedScopes'] not in [['global'], ['project', 'global']] or ('project' in scope['allowedScopes'] and not scope['projectKey']):
        return refuse('SCOPE-CONTEXT')
    if x['canonicalProfileId'] != 'opensip-metadata-canonical.1':
        return refuse('CANONICAL-PROFILE')
    if any(not re.fullmatch('[0-9a-f]{64}', x[k]) for k in ['permissionPolicyDigest', 'compatibilityPolicyDigest']):
        return refuse('PUBLIC-POLICY-DIGEST')
    if x['hostCoreStateMajor'] != 1:
        return refuse('HOST-STATE')
    try:
        version(x['hostCoreVersion'])
        for r in releases:
            version(r['version'])
            if set(r['surfaceRanges']) != {'coreState', 'root', 'index', 'manifest', 'lock', 'control', 'typescript', 'componentState'}:
                return refuse('COMPATIBILITY-METADATA')
            if any(not isinstance(pair, list) or len(pair) != 2 or any(type(n) is not int or n < 1 or n > 9007199254740991 for n in pair) or pair[0] > pair[1] for pair in r['surfaceRanges'].values()):
                return refuse('COMPATIBILITY-METADATA')
            if not valid_constraint(r['hostCoreConstraint']) or any(not valid_constraint(dep['versionConstraint']) for dep in r['dependencies']):
                return refuse('CONSTRAINT-GRAMMAR')
    except (ValueError, KeyError):
        return refuse('VERSION-GRAMMAR')
    # These are already-declared, digest-bound resolutionInputs. Reject instead
    # of normalizing them after declaration, which would change input custody.
    request_ids = [item['stableId'] for item in x['request']]
    if len(set(request_ids)) != len(request_ids):
        return refuse('DUPLICATE-REQUEST-ID')
    if request_ids != sorted(request_ids, key=lambda value: value.encode('utf-8')):
        return refuse('NONCANONICAL-REQUEST-ORDER')
    seen_exact = {}
    for item in x['pins'] + x['holds']:
        sid, release_version = item['stableId'], item['version']
        if sid in seen_exact:
            return refuse('DUPLICATE-PIN-HOLD' if seen_exact[sid] == release_version else 'PIN-HOLD-CONFLICT')
        seen_exact[sid] = release_version
    for field in ['pins', 'holds']:
        ids = [item['stableId'] for item in x[field]]
        if ids != sorted(ids, key=lambda value: value.encode('utf-8')):
            return refuse('NONCANONICAL-' + field.upper() + '-ORDER')
    if not INPUT_VALIDATOR.is_valid(x):
        return refuse('INPUT-SCHEMA')
    roots = {}
    for req in x['request']:
        c = req.get('version', req.get('versionConstraint'))
        if not valid_constraint(c):
            return refuse('CONSTRAINT-GRAMMAR')
        roots.setdefault(req['stableId'], []).append(c)
    exacts = {}
    for item in x['pins'] + x['holds']:
        if item['stableId'] not in exacts:
            exacts[item['stableId']] = item['version']
        elif exacts[item['stableId']] != item['version']:
            return refuse('PIN-HOLD-CONFLICT')
        try:
            version(item['version'])
        except ValueError:
            return refuse('VERSION-GRAMMAR')
    # Detect equivocation before any choice. Identical duplicate observations are
    # collapsed; differing bytes under the same full release key are refused.
    unique = {}
    for r in releases:
        key = (r['stableId'], r['version'], r['scope'], r['projectKey'])
        if key in unique and fixture_bytes(unique[key]) != fixture_bytes(r):
            return refuse('CONFLICTING-RELEASE-TUPLE')
        unique[key] = r
    releases = list(unique.values())
    by_id = {}
    for r in releases:
        if r['scope'] not in scope['allowedScopes']:
            continue
        if r['scope'] == 'project' and r['projectKey'] != scope['projectKey']:
            continue
        if not r['admitted'] or not r['currentTrustPermits']:
            continue
        if r['provenance'] != data['index']['currentProvenance'].get(r['stableId']):
            continue
        if x['platform'] not in r['platforms']:
            continue
        if not satisfies(x['hostCoreVersion'], r['hostCoreConstraint']):
            continue
        if any(not lo <= 1 <= hi for lo, hi in r['surfaceRanges'].values()):
            continue
        if r['stableId'] in roots and not set(CAPS) <= set(r['capabilities']):
            continue
        by_id.setdefault(r['stableId'], []).append(r)
    for values in by_id.values():
        values.sort(key=cmp_to_key(candidate_compare))

    def closure(assigned):
        constraints = copy.deepcopy(roots)
        graph = {}
        for sid, release in assigned.items():
            deps = release['dependencies']
            graph[sid] = [d['stableId'] for d in deps]
            for dep in deps:
                constraints.setdefault(dep['stableId'], []).append(dep['versionConstraint'])
        def walk(node, stack):
            if node in stack:
                rejections.add('DEPENDENCY-CYCLE')
                return False
            if len(stack) >= model_depth_limit:
                rejections.add('DEPTH-LIMIT')
                return False
            return all(walk(target, stack + [node]) for target in graph.get(node, []))
        if not all(walk(root, []) for root in sorted(roots)):
            return None
        for sid, chosen in assigned.items():
            cs = constraints.get(sid, []) + ([exacts[sid]] if sid in exacts else [])
            if not all(satisfies(chosen['version'], c) for c in cs):
                return None
        return constraints

    def search(assigned):
        nonlocal visits
        constraints = closure(assigned)
        if constraints is None:
            return None
        unresolved = sorted(set(constraints) - set(assigned))
        if not unresolved:
            # A pin/hold constrains a present identity; it does not itself add a
            # root. Refuse dangling pins/holds rather than silently dropping them.
            if not set(exacts) <= set(assigned):
                rejections.add('DANGLING-PIN-HOLD')
                return None
            for edge in data['observedRequiredEdges']:
                if edge['from'] not in assigned or edge['to'] not in {d['stableId'] for d in assigned[edge['from']]['dependencies']}:
                    rejections.add('UNDECLARED-REQUIRED-EDGE')
                    return None
            return assigned
        sid = unresolved[0]
        cs = constraints[sid] + ([exacts[sid]] if sid in exacts else [])
        for candidate in by_id.get(sid, []):
            visits += 1
            if visits > model_visit_limit:
                raise Exhausted()
            if not all(satisfies(candidate['version'], c) for c in cs):
                continue
            result = search(dict(assigned, **{sid: candidate}))
            if result is not None:
                return result
        return None

    try:
        result = search({})
    except Exhausted:
        return refuse('VISIT-LIMIT')
    if result is None:
        # Stable diagnostic priority. All outcomes use the owning RJ-5 family in
        # product integration; these labels are design diagnostics, not new codes.
        for reason in ['UNDECLARED-REQUIRED-EDGE', 'DANGLING-PIN-HOLD', 'DEPTH-LIMIT', 'DEPENDENCY-CYCLE']:
            if reason in rejections:
                return refuse(reason)
        return refuse('NO-COMPATIBLE-CLOSURE')
    selected = []
    for r in result.values():
        selected.append({k: copy.deepcopy(r[k]) for k in ['stableId', 'provenance', 'version', 'scope', 'manifestDigest', 'platformTreeEntryCount', 'artifactDigests']})
        selected[-1]['artifactDigests'].sort(key=lambda a: (a['artifact'].encode(), a['sha256'].encode()))
        selected[-1]['selectedCompatibility'] = {'S-CORE': {'release': x['hostCoreVersion'], 'coreState': x['hostCoreStateMajor']},
            'S-SCHEMA': {'root': 1, 'index': 1, 'manifest': 1, 'lock': 1}, 'S-CTRL': 1, 'S-TS1': 1, 'S-STATE': 1}
    selected.sort(key=cmp_to_key(tuple_compare))
    lock = {'lockSchemaVersion': 1, 'resolutionInputs': copy.deepcopy(x), 'resolved': selected,
            'exclusionsRecorded': 'NO_SECRETS_NO_TRUST_DECISIONS_NO_AUTHORITY'}
    # A semantic ACCEPT can never emit a structurally invalid applied-schema lock.
    if not LOCK_VALIDATOR.is_valid(lock):
        return refuse('OUTPUT-SCHEMA')
    return {'status': 'ACCEPT', 'resolved': selected, 'referenceLock': lock, 'visits': visits}


def verify_artifact_bytes(tuples, artifact_bytes):
    """Plain digest verification join, not signature/admission verification."""
    wanted = {}
    for entry in tuples:
        for artifact in entry['artifactDigests']:
            key = entry['stableId'] + '/' + artifact['artifact']
            if key in wanted:
                return False
            wanted[key] = artifact['sha256']
    if set(wanted) != set(artifact_bytes):
        return False
    try:
        return all(sha(bytes.fromhex(artifact_bytes[key])) == digest for key, digest in wanted.items())
    except ValueError:
        return False


def summary(result):
    return {'status': result['status'], **({'reason': result['reason']} if result['status'] == 'REFUSE' else {}),
            'resolved': [{k: r[k] for k in ['stableId', 'version', 'scope', 'manifestDigest']} for r in result['resolved']]}


def run(args):
    cases_path = HERE / 'compatibility-selection-cases.v3.json'
    corpus = json.loads(cases_path.read_text())
    results = []
    for pin in corpus['sourcePins']:
        observed = sha((ROOT / pin['path']).read_bytes())
        results.append({'id': 'source/' + pin['path'], 'passed': observed == pin['sha256']})
    for case in corpus['comparisons']:
        observed = (candidate_compare if case['kind'] == 'candidate' else tuple_compare)(case['a'], case['b'])
        results.append({'id': case['id'], 'passed': observed == case['expected'], 'observed': observed, 'expected': case['expected']})
    for case in corpus['artifactCustody']:
        observed = verify_artifact_bytes(case['tuples'], case['artifactBytes'])
        results.append({'id': case['id'], 'passed': observed == case['expected'], 'observed': observed, 'expected': case['expected']})
    accepted_locks = {}
    for case in corpus['selections']:
        result = solve(case['input'], **case.get('modelOnlyLimits', {}))
        observed = summary(result)
        good = observed == case['expected']
        again = solve(copy.deepcopy(case['input']), **case.get('modelOnlyLimits', {}))
        stable = fixture_bytes(result) == fixture_bytes(again)
        results.append({'id': case['id'], 'passed': good and stable, 'expected': case['expected'], 'observed': observed,
                        'repeatBytesIdentical': stable, 'candidateVisits': result['visits']})
        if result['status'] == 'ACCEPT':
            results.append({'id': case['id'] + '/accepted-lock-schema', 'passed': LOCK_VALIDATOR.is_valid(result['referenceLock'])})
            accepted_locks[case['id']] = {'lock': result['referenceLock'], 'fixtureBytesSha256': sha(fixture_bytes(result['referenceLock']))}
            # Reordering index observations changes snapshot bytes, so lock input
            # indexDigest changes. Compare selections only across that mutation.
            shuffled = copy.deepcopy(case['input'])
            shuffled['index']['releases'].reverse()
            shuffled['resolutionInputs']['indexDigest'] = sha(fixture_bytes(shuffled['index']))
            changed = solve(shuffled, **case.get('modelOnlyLimits', {}))
            results.append({'id': case['id'] + '/index-permutation', 'passed': changed['resolved'] == result['resolved']})
    report = {'status': 'DESIGN-MODEL-RESULT-NOT-PRODUCT-QUALIFICATION', 'passed': sum(r['passed'] for r in results), 'total': len(results),
              'sourcePins': [{'path': str(p.relative_to(ROOT)), 'sha256': sha(p.read_bytes())} for p in [Path(__file__), cases_path]],
              'limitations': corpus['limitations'], 'results': results, 'acceptedReferenceLocks': accepted_locks}
    Path(args.report).write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(f"Compatibility selection design: {report['passed']}/{report['total']} passed")
    for item in results:
        if not item['passed']:
            print(json.dumps(item))
    return 0 if report['passed'] == report['total'] else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', default=str(HERE / 'compatibility-selection-report.v3.json'))
    raise SystemExit(run(parser.parse_args()))
