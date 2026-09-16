"""Package v17 evidence probe: complete artifact manifest, formal versus files-only source manifests, overlay base-digest
provenance against package15, package16 preserved as history, content agreement of this review's own author-tool runs with
the root verification and rebuild, and the exact TypeScript normalization-map negative controls.
Reads only; writes only receipts/probes/package-v17.json."""
import hashlib, json, os, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v40')
B = Path('/tmp/opensip-design-corrections')
PKG = B / 'claude-author-package-successor.v17'
P15 = B / 'claude-author-package-successor.v15'
P16 = B / 'claude-author-package-successor.v16'
LIVE40 = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v40.json')
ROOTVER = B / 'author-package-final40-verification.v1'
REBUILD = B / 'root-author-package-final40-rebuild.v1/rebuild-report.json'
OVERLAY = B / 'claude-author-package-migration.v1/overlay'
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
    row('artifact-manifest-sha-is-the-header-value', am_sha == 'f179b7568201c5218e10ad830a81c66cbeddc4aedac9e8fe5f91988b69ca1a4e', am_sha)
    listed = {f['path']: f for f in AM['files']}
    actual = walk(PKG, skip=('artifact-manifest.json',))
    bad = sorted(p for p, f in listed.items() if p not in actual or sha(actual[p]) != f['sha256'] or os.path.getsize(actual[p]) != f['bytes'])
    row('every-package-file-matches-the-artifact-manifest-and-none-is-unlisted', not bad and set(actual) == set(listed),
        {'listed': len(listed), 'mismatched': bad[:10], 'unlisted': sorted(set(actual) - set(listed))[:10]})
    sm_sha = sha(PKG / 'source-manifest.json')
    formal = json.loads(LIVE40.read_text())
    SM = json.loads((PKG / 'source-manifest.json').read_text())
    row('files-only-source-manifest-sha-is-the-header-value', sm_sha == 'ec4f69fc01cd46385c1d01dd108ccda4076b9e95f9c1b77d153c662be2d9d796', sm_sha)
    row('formal-and-files-only-are-different-objects-with-equal-file-members',
        sha(LIVE40) != sm_sha and triples(SM) == triples(formal) and AM['formalSubjectManifestSha256'] == sha(LIVE40) and AM['sourceManifestSha256'] == sm_sha,
        {'formal': sha(LIVE40), 'filesOnly': sm_sha, 'members': len(triples(formal))})
    row('formal-manifest-copy-in-package-equals-the-live-formal-manifest', sha(PKG / 'formal-source-manifest.v40.json') == sha(LIVE40))
    bind = json.loads((PKG / 'source-binding.v40.json').read_text())
    row('binding-names-rebuild-report-and-counts', bind['rebuildReportSha256'] == sha(REBUILD) and (bind['exportCount'], bind['queryCount'], bind['membershipProbeCount']) == (17, 7, 9)
        and bind['exportsChangedByBinding'] is False and bind['independentGradesGranted'] == 0, bind)
    RB = json.loads(REBUILD.read_text())
    row('rebuild-report-sha-is-the-header-value', sha(REBUILD) == 'd6772c06bcab2f5ab20e1b122370201c7dce206a13096d075ab2e1841c019891', sha(REBUILD))
    inputs = RB['inputs']
    om = json.loads((OVERLAY / 'overlay-manifest.json').read_text())
    row('rebuild-base-is-package15-constructors-plus-migration-overlay-not-package16',
        inputs['packageManifestSha256'] == '6a8d4feca9db7ea48e91debf3a080415f769ac7271b8bf67df145263148b701e' and 'successor.v15' in inputs['package']
        and inputs['overlayManifestSha256'] == sha(OVERLAY / 'overlay-manifest.json') and '6a8d4feca9db7ea48e91debf3a080415f769ac7271b8bf67df145263148b701e' in om['base']
        and inputs['sourceManifestSha256'] == sm_sha, {'package': inputs['package'], 'overlayBase': om['base']})
    if (P15 / 'artifact-manifest.json').exists():
        p15_sha = sha(P15 / 'artifact-manifest.json')
        base_ok = []
        for f in om['files']:
            if f.get('package15Sha256'):
                base_ok.append((f['path'], (P15 / f['path']).exists() and sha(P15 / f['path']) == f['package15Sha256']))
        overlay_ok = [(f['path'], (OVERLAY / f['path']).exists() and sha(OVERLAY / f['path']) == f['sha256']) for f in om['files']]
        row('package15-base-digests-named-by-the-overlay-match-retained-package15', p15_sha == '6a8d4feca9db7ea48e91debf3a080415f769ac7271b8bf67df145263148b701e'
            and all(ok for _, ok in base_ok), {'package15Manifest': p15_sha, 'modifiedBaseFiles': base_ok})
        row('overlay-files-match-their-overlay-manifest', all(ok for _, ok in overlay_ok), overlay_ok)
    else:
        row('package15-base-available', False, 'package15 not readable')
    in_pkg = walk(PKG)
    template_diffs = []
    for f in om['files']:
        rel = f['path']
        if rel in in_pkg and (OVERLAY / rel).exists() and sha(in_pkg[rel]) != sha(OVERLAY / rel):
            template_diffs.append(rel)
    ov_verify = (OVERLAY / 'verify-package.py').read_text().replace('__SOURCE_MANIFEST_SHA256__', sm_sha) == (PKG / 'verify-package.py').read_text()
    ov_readme = (PKG / 'README.md').read_text().endswith((OVERLAY / 'README.md').read_text())
    row('overlay-files-differ-in-package-only-by-placeholder-instantiation-and-binding-header', set(template_diffs) <= {'verify-package.py', 'README.md'} and ov_verify and ov_readme,
        {'differing': template_diffs, 'verifyPlaceholderOnly': ov_verify, 'readmeHeaderOnly': ov_readme})
    if (P16 / 'artifact-manifest.json').exists():
        row('package16-preserved-unchanged-as-history', sha(P16 / 'artifact-manifest.json') == 'a88697c1bb82b4f4ad9abf05b22f01f3a0ddfd53fdbfa4b7dd6bfbbdb9ea2f6e', sha(P16 / 'artifact-manifest.json'))
    row('pre-binding-package-equals-rebuilt-package', AM['predecessorArtifactManifestSha256'] == RB['packageManifestSha256'] == bind['rebuiltPackageBeforeMetadataBindingSha256'],
        RB['packageManifestSha256'])
    ec = RB['exportComparison']
    store_shas = {}
    for r, p in walk(PKG).items():
        if r.endswith('.store.json') and not r.startswith('historical'):
            store_shas.setdefault(sha(p), []).append(r)
    row('seventeen-exports-reconstructed-with-new-run-ids-and-bytes-present-in-package', len(ec) == 17 and all(e['runId'] != e.get('previousRunId') for e in ec)
        and all(e['exportSha256'] in store_shas for e in ec), {'exports': len(ec), 'newFlags': [e.get('new') for e in ec],
                                                              'groups': sorted({e['group'] for e in ec})})
    mine = RT / 'work/package-v17-verify'
    mv, rv = json.loads((mine / 'verification.json').read_text()), json.loads((ROOTVER / 'verification.json').read_text())
    row('this-reviews-verification-is-content-equal-to-the-root-verification', mv == rv and sha(ROOTVER / 'verification.json') == 'fc69c7aea8f96fbb5f145da48a93b5ca71330c5ef0a4ec1d2a82980d2fd2e984',
        {'groups': [(g['group'], g.get('count'), g.get('passed'), g.get('exitCode')) for g in mv['groups']]})
    mf, rf = walk(mine), walk(ROOTVER)
    common = sorted(set(mf) & set(rf))
    differ = [r for r in common if sha(mf[r]) != sha(rf[r])]
    row('every-common-output-file-is-byte-equal-to-the-root-run', not differ and len(common) >= 50, {'compared': len(common), 'differing': differ,
                                                                                                    'onlyMine': sorted(set(mf) - set(rf))[:10], 'onlyRoot': sorted(set(rf) - set(mf))[:10]})
    counts = {g['group']: g.get('count') for g in mv['groups']}
    row('exports-7-groups-sum-to-17-and-query-count-7', sum(v for k, v in counts.items() if k != 'query') == 17 and counts.get('query') == 7, counts)
    nv = json.loads((RT / 'work/probe-native-v2.json').read_text())
    row('nine-membership-probes-content-equal-to-the-root-rebuild-probe', nv == RB['nativeV2Probe'] and len(nv['runs']) == 9 and nv['passed'] is True
        and nv['unitsVsDiscoveryDisagreements'] == [], [r['name'] for r in nv['runs']])
    nm = json.loads((mine / 'normalization-map-controls1/report.json').read_text())
    row('normalization-map-controls1-report', True, nm if len(json.dumps(nm)) < 4000 else {k: nm[k] for k in list(nm)[:12]}, None, 'record')
    claims = json.loads((PKG / 'normalization-map-controls1/claims.json').read_text()) if (PKG / 'normalization-map-controls1/claims.json').exists() else None
    row('normalization-map-controls1-claims', True, claims, None, 'record')


try:
    main()
except Exception:  # noqa: BLE001
    row('probe-crashed', False, traceback.format_exc()[-2500:])
out = RT / 'receipts/probes/package-v17.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({'standing': 'independent reviewer package evidence probe; author tools were run separately on this review copy; not reconstruction or qualification',
                           'rows': ROWS, 'failed': [r for r in ROWS if not r['ok']]}, indent=1, default=str))
print(json.dumps({'total': len(ROWS), 'failed': [(r['case'], r['observed']) for r in ROWS if not r['ok']]}, indent=1, default=str)[:6000])
