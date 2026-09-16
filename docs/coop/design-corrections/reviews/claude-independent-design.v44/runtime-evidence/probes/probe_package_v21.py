"""Package v21 evidence probe: complete artifact manifest, formal44 versus files-only source manifests, overlay base-digest
provenance against package15, packages 16..20 preserved as history, the pre-binding manifest retained in the package, measured
export/RunId equality against package20, content agreement of this review's own author-tool runs (verify-package.py and
probe-native-v2.py on this review's verified source44 copy) with the root final44 rebuild verification and probe, and the exact
TypeScript normalization-map negative controls. Reads only; writes only receipts/probes/package-v21.json."""
import hashlib, json, os, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v44')
B = Path('/tmp/opensip-design-corrections')
PKG = B / 'claude-author-package-successor.v21'
P20 = B / 'claude-author-package-successor.v20'
P15 = B / 'claude-author-package-successor.v15'
HISTORY = {'16': 'a88697c1bb82b4f4ad9abf05b22f01f3a0ddfd53fdbfa4b7dd6bfbbdb9ea2f6e', '17': 'f179b7568201c5218e10ad830a81c66cbeddc4aedac9e8fe5f91988b69ca1a4e',
           '18': '10bafe77c0e1e4201243784ed0a4524f3f96c9f6e1a83da93fabcacaef37e139', '19': '346a4d4b298404b9dabd1f9a6206733351723853cd5bd7f23e9896199b641a31',
           '20': '803d1e1692c71dcede01efa0206fec68050c596a9c228b55123435dbdde4920b'}
LIVE44 = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v44.json')
REBUILD_DIR = B / 'root-author-package-final44-rebuild.v1'
REBUILD = REBUILD_DIR / 'rebuild-report.json'
ROOTVER = REBUILD_DIR / 'work/verification'
FORMAL = B / 'root-author-package-formal44-binding.v1/binding.json'
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
    row('artifact-manifest-sha-is-the-header-value', am_sha == 'e5639aa3f16399f180cde9e43f59e64698eaaa851f2a15f51a63dd8d0bf5d245', am_sha)
    listed = {f['path']: f for f in AM['files']}
    actual = walk(PKG, skip=('artifact-manifest.json',))
    bad = sorted(p for p, f in listed.items() if p not in actual or sha(actual[p]) != f['sha256'] or os.path.getsize(actual[p]) != f['bytes'])
    row('every-package-file-matches-the-artifact-manifest-and-none-is-unlisted', not bad and set(actual) == set(listed),
        {'listed': len(listed), 'mismatched': bad[:10], 'unlisted': sorted(set(actual) - set(listed))[:10]})
    sm_sha = sha(PKG / 'source-manifest.json')
    formal = json.loads(LIVE44.read_text())
    SM = json.loads((PKG / 'source-manifest.json').read_text())
    bind = json.loads((PKG / 'source-binding.v44.json').read_text())
    row('live-formal44-manifest-is-the-header-value', sha(LIVE44) == 'e873c8db7b50f8d4bc4c6b1754239fb200b11f4e5d0f23b1ceaa6ea17297a32b', sha(LIVE44))
    row('source-binding-sha-is-the-header-value', sha(PKG / 'source-binding.v44.json') == 'ba2e92467ea18facbb2a50797b8ee5b0eee9286b16727149ee4bc4e19bf5046a',
        sha(PKG / 'source-binding.v44.json'))
    row('formal44-and-files-only-projection-are-different-objects-with-equal-file-members',
        sha(LIVE44) != sm_sha and triples(SM) == triples(formal) and AM['formalSubjectManifestSha256'] == sha(LIVE44) and AM['sourceManifestSha256'] == sm_sha
        and bind['filesOnlySourceProjectionSha256'] == sm_sha and bind['formalSubjectManifestSha256'] == sha(LIVE44) and bind['projectionEqualsFormalFiles'] is True,
        {'formal': sha(LIVE44), 'filesOnly': sm_sha, 'members': len(triples(formal))})
    row('files-only-projection-equals-this-reviews-verified-manifest44-index',
        {p: s for p, s, _ in triples(SM)} == json.loads((RT / 'receipts/manifest44-index.json').read_text()), len(triples(SM)))
    row('formal-manifest-copy-in-package-equals-the-live-formal-manifest', sha(PKG / 'formal-source-manifest.v44.json') == sha(LIVE44))
    RB = json.loads(REBUILD.read_text())
    row('rebuild-report-sha-is-the-header-value', sha(REBUILD) == '332e5d51f7d781b119811f6eabfbc75b9eddc11fef2b139a12075bfdc7c34808', sha(REBUILD))
    row('binding-names-rebuild-report-and-counts', bind['rebuildReportSha256'] == sha(REBUILD) and (bind['exportCount'], bind['queryCount'], bind['membershipProbeCount']) == (17, 7, 9)
        and bind['exportsChangedByBinding'] is False and bind['independentGradesGranted'] == 0, bind)
    FB = json.loads(FORMAL.read_text())
    row('root-formal44-binding-record-embeds-the-package-binding-not-header-bound', FB['binding'] == bind and FB['packageManifestSha256'] == am_sha and FB['packageFiles'] == len(listed),
        {'sha': sha(FORMAL), 'packageFiles': FB.get('packageFiles')}, None, 'record')
    inputs = RB['inputs']
    om = json.loads((OVERLAY / 'overlay-manifest.json').read_text())
    row('rebuild-base-is-package15-constructors-plus-native-v2-migration-overlay-on-frozen-source44',
        inputs['packageManifestSha256'] == P15_SHA and inputs['package'].endswith('successor.v15') and inputs['overlayManifestSha256'] == sha(OVERLAY / 'overlay-manifest.json')
        and P15_SHA in om['base'] and inputs['sourceManifestSha256'] == sm_sha and inputs['sourceFiles'] == 12919 and inputs['source'].endswith('candidate-subject.v44'),
        {'source': inputs['source'], 'package': inputs['package'], 'overlay': inputs['overlay'], 'overlayManifest': inputs['overlayManifestSha256'], 'overlayBase': om['base']})
    reg = {'native': 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'}
    idx = json.loads((RT / 'receipts/manifest44-index.json').read_text())
    row('rebuild-registered-native-schema-is-the-unchanged-source44-bundle', idx.get(reg['native']) == inputs['registeredNativeSchemaSha256'], inputs['registeredNativeSchemaSha256'])
    p15_sha = sha(P15 / 'artifact-manifest.json')
    base_ok = [(f['path'], (P15 / f['path']).exists() and sha(P15 / f['path']) == f['package15Sha256']) for f in om['files'] if f.get('package15Sha256')]
    overlay_ok = [(f['path'], (OVERLAY / f['path']).exists() and sha(OVERLAY / f['path']) == f['sha256']) for f in om['files']]
    row('package15-base-digests-named-by-the-overlay-match-retained-package15', p15_sha == P15_SHA and all(ok for _, ok in base_ok),
        {'package15Manifest': p15_sha, 'modifiedBaseFiles': base_ok})
    row('overlay-files-match-their-overlay-manifest', all(ok for _, ok in overlay_ok), overlay_ok)
    row('rebuild-script-is-the-overlay-rebuild-script', RB['scriptSha256'] == sha(OVERLAY / 'rebuild-author-package.v2.py'), RB['scriptSha256'])
    in_pkg = walk(PKG)
    template_diffs = [f['path'] for f in om['files'] if f['path'] in in_pkg and (OVERLAY / f['path']).exists() and sha(in_pkg[f['path']]) != sha(OVERLAY / f['path'])]
    ov_verify = (OVERLAY / 'verify-package.py').read_text().replace('__SOURCE_MANIFEST_SHA256__', sm_sha) == (PKG / 'verify-package.py').read_text()
    ov_readme = (PKG / 'README.md').read_text().endswith((OVERLAY / 'README.md').read_text())
    row('overlay-files-differ-in-package-only-by-placeholder-instantiation-and-binding-header', set(template_diffs) <= {'verify-package.py', 'README.md'} and ov_verify and ov_readme,
        {'differing': template_diffs, 'verifyPlaceholderOnly': ov_verify, 'readmeHeaderOnly': ov_readme})
    for v, want in HISTORY.items():
        f = B / ('claude-author-package-successor.v%s/artifact-manifest.json' % v)
        row('package%s-preserved-unchanged-as-history' % v, f.exists() and sha(f) == want, sha(f) if f.exists() else None)
    hist = PKG / 'historical-before-formal-binding44/artifact-manifest.json'
    row('pre-binding-package-equals-rebuilt-package-and-is-retained-inside-package21',
        AM['predecessorArtifactManifestSha256'] == RB['packageManifestSha256'] == bind['rebuiltPackageBeforeMetadataBindingSha256'] == sha(hist)
        and sha(REBUILD_DIR / 'package/artifact-manifest.json') == RB['packageManifestSha256'],
        {'rebuilt': RB['packageManifestSha256'], 'retainedHistorical': sha(hist), 'rebuildDirPackage': sha(REBUILD_DIR / 'package/artifact-manifest.json')})
    pre = walk(REBUILD_DIR / 'package', skip=('artifact-manifest.json',))
    only_meta = sorted(r for r in set(pre) | set(actual) if r not in pre or r not in actual or sha(pre[r]) != sha(actual[r]))
    row('metadata-binding-changed-only-metadata-files-every-export-and-replay-helper-byte-preserved',
        not [r for r in only_meta if r.endswith('.store.json') or (r.endswith('.py') and not r.startswith('historical'))] or only_meta == ['verify-package.py'],
        {'differingOrAddedByBinding': only_meta})
    ec = RB['exportComparison']
    store = {r: p for r, p in walk(PKG).items() if r.endswith('.store.json') and not r.startswith('historical')}
    store_shas = {}
    for r, p in store.items():
        store_shas.setdefault(sha(p), []).append(r)
    row('seventeen-exports-present-in-package-by-bytes', len(ec) == 17 and all(e['exportSha256'] in store_shas for e in ec),
        {'exports': len(ec), 'groups': sorted({e['group'] for e in ec})})
    s20 = {r: p for r, p in walk(P20).items() if r.endswith('.store.json') and not r.startswith('historical')}
    same = {r: (r in s20 and sha(store[r]) == sha(s20[r])) for r in sorted(store)}
    row('every-current-export-store-is-byte-equal-to-package20-at-the-same-path-so-byte-derived-RunIds-are-unchanged-not-reminted',
        all(same.values()) and set(store) == set(s20), {'current': len(store), 'package20': len(s20), 'differing': [r for r, v in same.items() if not v],
                                                         'onlyCurrent': sorted(set(store) - set(s20)), 'onlyPackage20': sorted(set(s20) - set(store))})
    rb20 = json.loads((B / 'root-author-package-final43-rebuild.v1/rebuild-report.json').read_text())
    ids20 = sorted(e['runId'] for e in rb20['exportComparison'])
    row('measured-source44-RunIds-equal-the-source43-package20-rebuild-RunIds', sorted(e['runId'] for e in ec) == ids20,
        {'source44': sorted(e['runId'] for e in ec), 'source43': ids20})
    row('formal-binding-source43-comparison-all-17-same-RunId-and-bytes', len(FB['source43Comparison']) == 17 and all(c['sameRunId'] and c['sameExportBytes'] for c in FB['source43Comparison'])
        and sorted(c['source44RunId'] for c in FB['source43Comparison']) == sorted(e['runId'] for e in ec), len(FB['source43Comparison']))
    mine = RT / 'work/package-v21-verify'
    mv, rv = json.loads((mine / 'verification.json').read_text()), json.loads((ROOTVER / 'verification.json').read_text())
    keydiff = sorted(k for k in set(mv) | set(rv) if mv.get(k) != rv.get(k))
    # attempt1 expected only packageManifestSha256 to differ; the root rebuild verified the pre-binding package (c97d6f3b, fewer files)
    # while this review verified metadata-bound package21 (e5639aa3), so the verified package file count legitimately differs too.
    row('this-reviews-verification-of-bound-package21-is-content-equal-to-the-root-pre-binding-verification-except-package-identity-and-file-count',
        set(keydiff) <= {'packageManifestSha256', 'packageFilesVerified'} and mv['groups'] == rv['groups'] and mv['passed'] is True
        and mv['packageManifestSha256'] == am_sha and rv['packageManifestSha256'] == RB['packageManifestSha256']
        and mv['packageFilesVerified'] == len(listed) and rv['packageFilesVerified'] == len(pre) and mv['sourceFilesVerified'] == rv['sourceFilesVerified'] == 12919,
        {'keysDiffering': keydiff, 'mine.packageManifestSha256': mv.get('packageManifestSha256'), 'root.packageManifestSha256': rv.get('packageManifestSha256'),
         'root.packageFilesVerified': rv.get('packageFilesVerified'), 'preBindingPackageFiles': len(pre),
         'groups': [(g['group'], g.get('count'), g.get('passed'), g.get('exitCode')) for g in mv['groups']], 'packageFilesVerified': mv.get('packageFilesVerified'),
         'sourceFilesVerified': mv.get('sourceFilesVerified'), 'rootVerificationSha256': sha(ROOTVER / 'verification.json')})
    mf, rf = walk(mine), walk(ROOTVER)
    common = sorted(set(mf) & set(rf))
    differ = [r for r in common if sha(mf[r]) != sha(rf[r])]
    row('every-common-output-file-is-byte-equal-to-the-root-run-except-verification-json', set(differ) <= {'verification.json'} and len(common) >= 50,
        {'compared': len(common), 'differing': differ, 'onlyMine': sorted(set(mf) - set(rf))[:10], 'onlyRoot': sorted(set(rf) - set(mf))[:10]})
    counts = {g['group']: g.get('count') for g in mv['groups']}
    row('exports-6-groups-sum-to-17-and-query-count-7', sum(v for k, v in counts.items() if k != 'query') == 17 and counts.get('query') == 7, counts)
    nv = json.loads((RT / 'work/probe-native-v2.json').read_text())
    rnv = json.loads((REBUILD_DIR / 'work/probe-native-v2.json').read_text())
    row('nine-membership-probes-content-equal-to-the-root-rebuild-probe', nv == RB['nativeV2Probe'] == rnv and len(nv['runs']) == 9 and nv['passed'] is True
        and nv['unitsVsDiscoveryDisagreements'] == [], [r['name'] if isinstance(r, dict) else r[0] for r in nv['runs']])
    nm = next(g for g in mv['groups'] if g['group'] == 'normalization-map-controls1')
    row('four-typescript-normalization-map-negatives-refuse-at-owner-admission-exactly', [(o['name'], o['ownerAdmission'], o['semanticAdmission'], o['reason']) for o in nm['observed']] == [
        ('ts-map-absent', 'REFUSE', 'NOT-REACHED', 'BODY_NORMALIZATION_MAP_MISSING:opensip-interface/normalization/specification-map.v1.json'),
        ('ts-map-level-unmapped', 'REFUSE', 'NOT-REACHED', 'BODY_NORMALIZATION_LEVEL_UNMAPPED:L0-verbatim'),
        ('ts-map-level-swapped', 'REFUSE', 'NOT-REACHED', 'BODY_NORMALIZATION_LEVEL_VERSION_MISMATCH:L0-verbatim'),
        ('ts-spec-outside-closure', 'REFUSE', 'NOT-REACHED', 'BODY_NORMALIZATION_SPECIFICATION_NOT_IN_CLOSURE:L0-verbatim')], nm['observed'])
    bc = next(g for g in mv['groups'] if g['group'] == 'binding-controls')
    row('binding-controls-record', True, bc['observed'], None, 'record')
    q = next((g for g in mv['groups'] if g['group'] == 'query'), None)
    row('query-group-record', q is not None and q.get('passed') is True, q, None, 'record')


try:
    main()
except Exception:  # noqa: BLE001
    row('probe-crashed', False, traceback.format_exc()[-2500:])
out = RT / 'receipts/probes/package-v21.json'
out.parent.mkdir(parents=True, exist_ok=True)
kept = RT / 'receipts/probes/package-v21.attempt1-row-expectation-too-narrow.json'
if out.exists() and not kept.exists():
    out.rename(kept)  # preserve the failed first attempt verbatim
out.write_text(json.dumps({'standing': 'independent reviewer package evidence probe; author tools were run separately on this review copy; not reconstruction or qualification',
                           'rows': ROWS, 'failed': [r for r in ROWS if not r['ok']]}, indent=1, default=str))
print(json.dumps({'total': len(ROWS), 'failed': [(r['case'], r['observed']) for r in ROWS if not r['ok']]}, indent=1, default=str)[:6000])
