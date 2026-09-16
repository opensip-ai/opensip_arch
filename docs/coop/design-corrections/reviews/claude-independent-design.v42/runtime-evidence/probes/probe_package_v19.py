"""Package v19 evidence probe: complete artifact manifest, formal42 versus files-only source manifests, overlay base-digest
provenance against package15, packages 16/17/18 preserved as history, content agreement of this review's own author-tool runs
with the root final42 verification and rebuild, and the exact TypeScript normalization-map negative controls.
Reads only; writes only receipts/probes/package-v19.json."""
import hashlib, json, os, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v42')
B = Path('/tmp/opensip-design-corrections')
PKG = B / 'claude-author-package-successor.v19'
P15 = B / 'claude-author-package-successor.v15'
HISTORY = {'16': 'a88697c1bb82b4f4ad9abf05b22f01f3a0ddfd53fdbfa4b7dd6bfbbdb9ea2f6e', '17': 'f179b7568201c5218e10ad830a81c66cbeddc4aedac9e8fe5f91988b69ca1a4e',
           '18': '10bafe77c0e1e4201243784ed0a4524f3f96c9f6e1a83da93fabcacaef37e139'}
LIVE42 = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v42.json')
ROOTVER = B / 'author-package-final42-verification.v1'
REBUILD = B / 'root-author-package-final42-rebuild.v1/rebuild-report.json'
OVERLAY = B / 'claude-author-package-migration.v1/overlay'
P15_SHA = '6a8d4feca9db7ea48e91debf3a080415f769ac7271b8bf67df145263148b701e'
ROWS = []


def row(case, ok, observed=None, expected=None, kind=None):
    r = {'case': case, 'ok': bool(ok), 'observed': observed}
    if expected is not None:
        r['expected'] = expected
    if kind:
        r['kind'] = kind
    ROWS.append(r)


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


def walk(root, skip=()):
    out = {}
    for d, _, files in os.walk(root):
        for f in files:
            p = os.path.join(d, f)
            r = os.path.relpath(p, root)
            if r not in skip:
                out[r] = p
    return out


def triples(doc):
    files = doc['files'] if isinstance(doc, dict) else doc
    return sorted((f['path'], f['sha256'], f.get('bytes', f.get('size'))) for f in files)


def main():
    am_sha = sha(PKG / 'artifact-manifest.json')
    AM = json.loads((PKG / 'artifact-manifest.json').read_text())
    row('artifact-manifest-sha-is-the-header-value', am_sha == '346a4d4b298404b9dabd1f9a6206733351723853cd5bd7f23e9896199b641a31', am_sha)
    listed = {f['path']: f for f in AM['files']}
    actual = walk(PKG, skip=('artifact-manifest.json',))
    bad = sorted(p for p, f in listed.items() if p not in actual or sha(actual[p]) != f['sha256'] or os.path.getsize(actual[p]) != f['bytes'])
    row('every-package-file-matches-the-artifact-manifest-and-none-is-unlisted', not bad and set(actual) == set(listed),
        {'listed': len(listed), 'mismatched': bad[:10], 'unlisted': sorted(set(actual) - set(listed))[:10]})
    sm_sha = sha(PKG / 'source-manifest.json')
    formal = json.loads(LIVE42.read_text())
    SM = json.loads((PKG / 'source-manifest.json').read_text())
    bind = json.loads((PKG / 'source-binding.v42.json').read_text())
    row('source-binding-sha-is-the-header-value', sha(PKG / 'source-binding.v42.json') == '0c50efc7742a38ba7a62b78e0f10c9762632b0cb753e962c2aff7003993e91bc',
        sha(PKG / 'source-binding.v42.json'))
    row('formal42-and-files-only-projection-are-different-objects-with-equal-file-members',
        sha(LIVE42) != sm_sha and triples(SM) == triples(formal) and AM['formalSubjectManifestSha256'] == sha(LIVE42) and AM['sourceManifestSha256'] == sm_sha
        and bind['filesOnlySourceProjectionSha256'] == sm_sha and bind['formalSubjectManifestSha256'] == sha(LIVE42) and bind['projectionEqualsFormalFiles'] is True,
        {'formal': sha(LIVE42), 'filesOnly': sm_sha, 'members': len(triples(formal))})
    row('formal-manifest-copy-in-package-equals-the-live-formal-manifest', sha(PKG / 'formal-source-manifest.v42.json') == sha(LIVE42))
    row('binding-names-rebuild-report-and-counts', bind['rebuildReportSha256'] == sha(REBUILD) and (bind['exportCount'], bind['queryCount'], bind['membershipProbeCount']) == (17, 7, 9)
        and bind['exportsChangedByBinding'] is False and bind['independentGradesGranted'] == 0, bind)
    RB = json.loads(REBUILD.read_text())
    row('rebuild-report-sha-is-the-header-value', sha(REBUILD) == '73f1f73861eb570167bc4b416f68c3527e2d010ba305b8c643810c47a7e3d5e4', sha(REBUILD))
    inputs = RB['inputs']
    om = json.loads((OVERLAY / 'overlay-manifest.json').read_text())
    row('rebuild-base-is-package15-constructors-plus-native-v2-migration-overlay-not-a-later-package',
        inputs['packageManifestSha256'] == P15_SHA and inputs['package'].endswith('successor.v15') and inputs['overlayManifestSha256'] == sha(OVERLAY / 'overlay-manifest.json')
        and P15_SHA in om['base'] and inputs['sourceManifestSha256'] == sm_sha and inputs['sourceFiles'] == 12913,
        {'package': inputs['package'], 'overlay': inputs['overlay'], 'overlayManifest': inputs['overlayManifestSha256'], 'overlayBase': om['base']})
    p15_sha = sha(P15 / 'artifact-manifest.json')
    base_ok = [(f['path'], (P15 / f['path']).exists() and sha(P15 / f['path']) == f['package15Sha256']) for f in om['files'] if f.get('package15Sha256')]
    overlay_ok = [(f['path'], (OVERLAY / f['path']).exists() and sha(OVERLAY / f['path']) == f['sha256']) for f in om['files']]
    row('package15-base-digests-named-by-the-overlay-match-retained-package15', p15_sha == P15_SHA and all(ok for _, ok in base_ok),
        {'package15Manifest': p15_sha, 'modifiedBaseFiles': base_ok})
    row('overlay-files-match-their-overlay-manifest', all(ok for _, ok in overlay_ok), overlay_ok)
    in_pkg = walk(PKG)
    template_diffs = [f['path'] for f in om['files'] if f['path'] in in_pkg and (OVERLAY / f['path']).exists() and sha(in_pkg[f['path']]) != sha(OVERLAY / f['path'])]
    ov_verify = (OVERLAY / 'verify-package.py').read_text().replace('__SOURCE_MANIFEST_SHA256__', sm_sha) == (PKG / 'verify-package.py').read_text()
    ov_readme = (PKG / 'README.md').read_text().endswith((OVERLAY / 'README.md').read_text())
    row('overlay-files-differ-in-package-only-by-placeholder-instantiation-and-binding-header', set(template_diffs) <= {'verify-package.py', 'README.md'} and ov_verify and ov_readme,
        {'differing': template_diffs, 'verifyPlaceholderOnly': ov_verify, 'readmeHeaderOnly': ov_readme})
    for v, want in HISTORY.items():
        f = B / ('claude-author-package-successor.v%s/artifact-manifest.json' % v)
        row('package%s-preserved-unchanged-as-history' % v, f.exists() and sha(f) == want, sha(f) if f.exists() else None)
    row('pre-binding-package-equals-rebuilt-package', AM['predecessorArtifactManifestSha256'] == RB['packageManifestSha256'] == bind['rebuiltPackageBeforeMetadataBindingSha256'],
        RB['packageManifestSha256'])
    ec = RB['exportComparison']
    store_shas = {}
    for r, p in walk(PKG).items():
        if r.endswith('.store.json') and not r.startswith('historical'):
            store_shas.setdefault(sha(p), []).append(r)
    row('seventeen-exports-reconstructed-with-new-run-ids-and-bytes-present-in-package', len(ec) == 17 and all(e['runId'] != e.get('previousRunId') for e in ec)
        and all(e['exportSha256'] in store_shas for e in ec), {'exports': len(ec), 'newFlags': [e.get('new') for e in ec], 'groups': sorted({e['group'] for e in ec})})
    mine = RT / 'work/package-v19-verify'
    mv, rv = json.loads((mine / 'verification.json').read_text()), json.loads((ROOTVER / 'verification.json').read_text())
    row('this-reviews-verification-is-content-equal-to-the-root-verification', mv == rv and sha(ROOTVER / 'verification.json') == 'eeca54cdef3ab86ac09ae9ced23cbd847bc1a25f8936a0ded8aad1f3d825dee1',
        {'groups': [(g['group'], g.get('count'), g.get('passed'), g.get('exitCode')) for g in mv['groups']]})
    mf, rf = walk(mine), walk(ROOTVER)
    common = sorted(set(mf) & set(rf))
    differ = [r for r in common if sha(mf[r]) != sha(rf[r])]
    row('every-common-output-file-is-byte-equal-to-the-root-run', not differ and len(common) >= 50,
        {'compared': len(common), 'differing': differ, 'onlyMine': sorted(set(mf) - set(rf))[:10], 'onlyRoot': sorted(set(rf) - set(mf))[:10]})
    counts = {g['group']: g.get('count') for g in mv['groups']}
    row('exports-6-groups-sum-to-17-and-query-count-7', sum(v for k, v in counts.items() if k != 'query') == 17 and counts.get('query') == 7, counts)
    nv = json.loads((RT / 'work/probe-native-v2.json').read_text())
    row('nine-membership-probes-content-equal-to-the-root-rebuild-probe', nv == RB['nativeV2Probe'] and len(nv['runs']) == 9 and nv['passed'] is True
        and nv['unitsVsDiscoveryDisagreements'] == [], [r['name'] for r in nv['runs']])
    nm = next(g for g in mv['groups'] if g['group'] == 'normalization-map-controls1')
    row('four-typescript-normalization-map-negatives-refuse-at-owner-admission-exactly', [(o['name'], o['ownerAdmission'], o['semanticAdmission'], o['reason']) for o in nm['observed']] == [
        ('ts-map-absent', 'REFUSE', 'NOT-REACHED', 'BODY_NORMALIZATION_MAP_MISSING:opensip-interface/normalization/specification-map.v1.json'),
        ('ts-map-level-unmapped', 'REFUSE', 'NOT-REACHED', 'BODY_NORMALIZATION_LEVEL_UNMAPPED:L0-verbatim'),
        ('ts-map-level-swapped', 'REFUSE', 'NOT-REACHED', 'BODY_NORMALIZATION_LEVEL_VERSION_MISMATCH:L0-verbatim'),
        ('ts-spec-outside-closure', 'REFUSE', 'NOT-REACHED', 'BODY_NORMALIZATION_SPECIFICATION_NOT_IN_CLOSURE:L0-verbatim')], nm['observed'])
    bc = next(g for g in mv['groups'] if g['group'] == 'binding-controls')
    row('binding-controls-record', True, bc['observed'], None, 'record')


try:
    main()
except Exception:  # noqa: BLE001
    row('probe-crashed', False, traceback.format_exc()[-2500:])
out = RT / 'receipts/probes/package-v19.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({'standing': 'independent reviewer package evidence probe; author tools were run separately on this review copy; not reconstruction or qualification',
                           'rows': ROWS, 'failed': [r for r in ROWS if not r['ok']]}, indent=1, default=str))
print(json.dumps({'total': len(ROWS), 'failed': [(r['case'], r['observed']) for r in ROWS if not r['ok']]}, indent=1, default=str)[:6000])
