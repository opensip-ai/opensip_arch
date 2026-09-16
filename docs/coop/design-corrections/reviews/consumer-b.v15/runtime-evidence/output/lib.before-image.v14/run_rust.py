"""Complete positive Rust Run exercising the Rust universe/fact/Coverage path.

Exhibited properties (all on THIS exported Run):
  R-RUN-RUST                              Rust universe/fact/Coverage path
  R-RUN-RUST-MIXED-EDITION                a mixed-edition workspace (edition map with >1)
  R-RUN-RUST-TARGET-EDITION               a target-specific edition != its package default
  R-RUN-RUST-BODY-DIALECT                 body-specific dialect selected from the admitted
                                          compiler context and body provenance
  R-RUN-RUST-SAME-FILE-TWO-EDITIONS       one physical path under two distinct explicitly
                                          selected target editions -- two sourceUniverses in
                                          one Run, two body identities over the same bytes
  R-RUN-RUST-HASH-MARKER                  a valid `#` marker directory, inventoried
  R-RUN-RUST-LARGE-EDITION-MAP            a representative large edition map (24 crates)
  R-RUN-RUST-VERSION-COMPONENT            bounded version component derived, not guessed
  R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE  measured pair: body identity stable when only
                                          the ownership SELECTION changes without changing
                                          the effective dialect
  R-RUN-NONCEMPTY-CONTEXT                 nonempty selected native context
  R-NATIVE-PREIMAGE-JOINS                 dependency source set, file manifests and every
                                          member's bytes, unified features, cargo config
                                          projection and the projected config file bytes

Synthetic trusted observations only.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_build as B
import opensip_eval as E
import opensip_compose as CO
import opensip_capmanifest as CM

PROJECT_ID = 'prj1-' + '9e2a7b4c1d5f80369a7c2e4b6d8f0a1c3e5b7d9f2a4c6e8b0d1f3a5c7e9b0d2f'[:64]

# A `#` marker directory: CanonicalPath and LogicalPath admit `#`, which is exactly why a
# compilation-unit identity is H over a published four-field preimage rather than a
# delimiter-joined label.
HASH_DIR = 'crates/app#1'

SHARED_RS = b'pub fn shared() -> u32 { 7 + 1 }\n'
LIB_RS = b'pub mod shared;\npub fn lib_entry() -> u32 { shared::shared() }\n'
BIN_RS = b'fn main() { println!("{}", app1::lib_entry()); }\n'
BODY = b'{ 7 + 1 }'

EDITIONS = {
    'app1': 2021, 'core-lib': 2021, 'edge-svc': 2018, 'legacy-shim': 2015,
    'next-proto': 2024, 'metrics': 2021, 'codec': 2018, 'cli': 2021,
    'store': 2021, 'index': 2021, 'query': 2024, 'planner': 2021,
    'replay': 2018, 'audit': 2021, 'ingest': 2021, 'egress': 2021,
    'schema-gen': 2015, 'macro-util': 2021, 'fuzz-harness': 2024, 'bench-util': 2018,
    'telemetry': 2021, 'tracing-shim': 2018, 'config-loader': 2021, 'testkit': 2024,
}

FILES = {
    'Cargo.lock': b'version = 3\n[[package]]\nname = "app1"\nversion = "0.3.0"\n',
    'Cargo.toml': b'[workspace]\nmembers = ["crates/app#1", "crates/core-lib"]\n',
    HASH_DIR + '/Cargo.toml': b'[package]\nname = "app1"\nedition = "2021"\n'
                              b'[[bin]]\nname = "app1"\npath = "src/main.rs"\n'
                              b'[[test]]\nname = "it"\nedition = "2024"\npath = "src/lib.rs"\n',
    HASH_DIR + '/src/lib.rs': LIB_RS,
    HASH_DIR + '/src/main.rs': BIN_RS,
    HASH_DIR + '/src/shared.rs': SHARED_RS,
    'crates/core-lib/Cargo.toml': b'[package]\nname = "core-lib"\nedition = "2021"\n',
    'crates/core-lib/src/lib.rs': b'pub fn c() -> u32 { 7 + 1 }\n',
    '.cargo/config.toml': b'[build]\nrustflags = ["--cfg", "opensip"]\n',
}

L0_SPEC = (b'opensip level specification\nlevel: L0-verbatim\n'
           b'lexical-boundary: none (tokenisation forbidden)\n'
           b'token-kind-registry: none\ndirective-classification: none\n'
           b'transform-order: []\nreplacement-bytes: none\nlanguages: rust\n')

PROJECTED_CARGO_CONFIG = (b'# opensip projected .cargo/config.toml (CC-5)\n'
                          b'[build]\nrustflags = ["--cfg", "opensip"]\n')


def unit_id(marker_path, target_kind, target_name):
    """H(native.compilation-unit.v1, UnitIdentityV1{schemaVersion:1, markerPath,
    targetKind, targetName}) -- a published four-field preimage, re-derived at admission."""
    rec = {'schemaVersion': 1, 'markerPath': marker_path, 'targetKind': target_kind,
           'targetName': target_name}
    return 'sha256:' + K.H('native.compilation-unit.v1', rec), rec


def build():
    b = B.Builder(PROJECT_ID)
    st = b.st
    for d in (B.IDENTITY_DOC, B.RELATION_DOC, B.NATIVE_DOC, B.POLICY_V2_DOC, B.POLICY_V1_DOC,
              B.ENUM_PLAN_DOC, B.EMIT_PLAN_DOC, B.SUBJ_INV_DOC, B.EXEC_IN_DOC):
        b.retain_schema_doc(d)

    # ---------------------------------------------------------------- closures
    RUSTC, CARGO, PMS, LINKER, AR = (b'\x7fELF-synthetic-rustc-1.84.0',
                                     b'\x7fELF-synthetic-cargo-1.84.0',
                                     b'\x7fELF-synthetic-proc-macro-srv',
                                     b'\x7fELF-synthetic-linker',
                                     b'\x7fELF-synthetic-ar')
    tool_tid, tool_rec, _ = b.closure(
        'toolchain', '1.84.0', 3, 'macos-aarch64',
        [('bin/rustc', RUSTC), ('bin/cargo', CARGO), ('libexec/proc-macro-srv', PMS),
         ('bin/ld', LINKER), ('bin/ar', AR)], 'opensip-rust-toolchain')
    llvm_tid, llvm_rec, _ = b.closure(
        'rust-dev-llvm', '1.84.0', 3, 'macos-aarch64',
        [('lib/librustc_driver.dylib', b'\x7fELF-synthetic-rustc-driver'),
         ('lib/libLLVM.dylib', b'\x7fELF-synthetic-llvm')], 'opensip-rustc-dev-llvm')
    provider_tid, _, _ = b.closure(
        'provider', '2.5.0', 3, 'macos-aarch64',
        [('bin/opensip-rust-provider', b'\x7fELF-synthetic-rust-provider')],
        'opensip-rust-provider')
    evaluator_tid, _, _ = b.closure(
        'evaluator', '3.0.0', 3, 'macos-aarch64',
        [('bin/opensip-evaluator', b'\x7fELF-synthetic-pure-evaluator')],
        'opensip-evaluator')
    detector_tid, _, _ = b.closure(
        'detector', '1.1.0', 3, 'macos-aarch64',
        [('rules/rust-hygiene.json', b'{"detector":"rust-hygiene","rev":2}')],
        'opensip-rust-hygiene-detector')

    # ---------------------------------------------------------------- snapshot
    config = {
        'analysis': {'profileId': 'rust-cargo',
                     'capabilities': sorted(['inventory', 'syntax', 'clones-fact'],
                                            key=lambda s: K.C(s)),
                     'budget': {'unit': 'work-units', 'limit': 40000000}},
        'components': {'request': [{'stableId': '33333333-4444-4555-8666-777777777777',
                                    'version': '1.84.0'}],
                       'allowedScopes': ['project', 'global']},
        'discovery': {'workspaceRoots': ['.']},
        'policy': {'packIds': ['pack.rust-hygiene']},
        'evidence': {},
    }
    scope_desc = {'schemaVersion': 2, 'workspaceRoots': ['.'], 'pathPrefixes': [],
                  'excludedPathPrefixes': ['target']}
    snapshot_id, snapshot, sh = b.snapshot(
        FILES, config, scope_desc, vcs_kind='git',
        commit_id='fedcba98765432100123456789abcdef01234567', dirty=False)
    st.put_blob(L0_SPEC, label='level-spec:L0-verbatim')
    st.put_blob(PROJECTED_CARGO_CONFIG, label='projected-cargo-config')

    # ---------------------------------------------------------------- nested native records
    DEP_FILES = {'src/lib.rs': b'pub fn helper() -> u32 { 1 }\n',
                 'Cargo.toml': b'[package]\nname = "serde-lite"\nversion = "0.9.1"\n'}
    manifest = sorted([{'path': p, 'contentSha256': K.raw_sha256(by), 'byteLength': len(by)}
                       for p, by in DEP_FILES.items()], key=lambda r: r['path'].encode())
    for p, by in DEP_FILES.items():
        st.put_blob(by, label='dependency-source:' + p)
    man_hex = b.native_framed('native.dependency-file-manifest.v1', B.NATIVE_DOC,
                              '#/$defs/DependencyFileManifestV1', manifest,
                              'dependency-file-manifest')
    lockid = {'path': 'Cargo.lock', 'lockfileVersion': 3,
              'contentSha256': K.raw_sha256(FILES['Cargo.lock'])}
    depset = {'schemaVersion': 1, 'language': 'rust', 'lockfileIdentity': lockid,
              'packages': [{'name': 'serde-lite', 'version': '0.9.1',
                            'sourceKind': 'registry',
                            'sourceId': 'registry+https://example.invalid/index',
                            'lockChecksum': K.raw_sha256(b'synthetic-registry-checksum'),
                            'fileManifestSha256': man_hex,
                            'fileCount': len(manifest),
                            'totalBytes': sum(r['byteLength'] for r in manifest),
                            'checksumVerification': 'tarball-matched',
                            'provenanceAssurance': 'registry-authenticated',
                            'acquisition': {'mode': 'in-snapshot-vendored',
                                            'descriptorId': None,
                                            'vendorPath': 'vendor/serde-lite'}}],
              'completeness': {'state': 'complete', 'missing': []}}
    dep_hex = b.native_framed('native.dependency-source-set.v1', B.NATIVE_DOC,
                              '#/$defs/DependencySourceSetV1', depset,
                              'dependency-source-set')
    feats = {'schemaVersion': 1, 'resolverVersion': 2, 'targetTriple': 'aarch64-apple-darwin',
             'activated': [{'packageKey': 'serde-lite 0.9.1', 'features': ['std']}],
             'computedBy': {'producer': 'opensip-cargo-adapter',
                            'producerBuildId': 'synthetic-cargo-adapter-1'}}
    feat_hex = b.native_framed('native.unified-features.rust.v1', B.NATIVE_DOC,
                               '#/$defs/UnifiedFeaturesV1', feats, 'unified-features')
    cargo_proj = {
        'schemaVersion': 2, 'honoredKeys': ['build.rustflags'],
        'strippedKeys': ['build.target-dir'],
        'replacedSnapshotConfigs': ['.cargo/config.toml'],
        'rustflags': {'honored': ['--cfg', 'opensip'], 'stripped': [],
                      'executableSelected': False},
        'ancestorCarrierVerified': True, 'cargoHome': 'private-empty',
        'environmentProjection': 'none', 'claimsCargoSwitch': False,
        'projectionSha256': K.raw_sha256(PROJECTED_CARGO_CONFIG),
    }
    cargo_hex = b.native_framed('native.cargo-config-projection.v2', B.NATIVE_DOC,
                                '#/$defs/CargoConfigProjectionV2', cargo_proj,
                                'cargo-config-projection')

    # ---------------------------------------------------------------- native context
    toolchain = {
        'rustCommitHash': '0123456789abcdef0123456789abcdef01234567',
        'rustcVersion': tool_rec['semanticVersion'], 'cargoVersion': '1.84.0',
        'sysrootDigest': K.raw_sha256(b'synthetic-sysroot-tree-manifest'),
        'rustcDevLlvmDigest': st.suffix(llvm_tid),
        'standardLibraryComponentDigests': [
            {'component': 'libcore', 'sha256': K.raw_sha256(b'synthetic-libcore')},
            {'component': 'libstd', 'sha256': K.raw_sha256(b'synthetic-libstd')}],
        'targetTriple': 'aarch64-apple-darwin',
    }
    st.put_blob(b'synthetic-sysroot-tree-manifest', label='sysroot-tree-manifest')
    ctx = {'schemaVersion': 2, 'targetTriple': 'aarch64-apple-darwin',
           'hostTriple': 'aarch64-apple-darwin', 'toolchain': toolchain,
           'toolClosure': {'closureId': tool_tid, 'rustc': K.raw_sha256(RUSTC),
                           'cargo': K.raw_sha256(CARGO),
                           'procMacroServer': K.raw_sha256(PMS),
                           'linker': K.raw_sha256(LINKER), 'ar': K.raw_sha256(AR)},
           'baseCfg': sorted(['target_arch="aarch64"', 'target_os="macos"']),
           'resolverVersion': 2, 'dependencySourceSetId': 'sha256:' + dep_hex,
           'unifiedFeaturesId': 'sha256:' + feat_hex, 'preparedOutputSetId': None,
           'configProjection': cargo_proj}
    ctx_hex = b.native_framed('native.context.rust.v2', B.NATIVE_DOC,
                              '#/$defs/NativeContextV2', ctx, 'native-context:rust')

    # ---------------------------------------------------------------- ownership + universes
    LIB_UNIT, lib_pre = unit_id(HASH_DIR + '/Cargo.toml', 'lib', 'app1')
    BIN_UNIT, bin_pre = unit_id(HASH_DIR + '/Cargo.toml', 'bin', 'app1')
    TEST_UNIT, test_pre = unit_id(HASH_DIR + '/Cargo.toml', 'test', 'it')
    CORE_UNIT, core_pre = unit_id('crates/core-lib/Cargo.toml', 'lib', 'core-lib')
    for pre in (lib_pre, bin_pre, test_pre, core_pre):
        b.admit(B.NATIVE_DOC, '#/$defs/UnitIdentityV1', pre, 'unit-identity')
    units = sorted([
        # lib target takes the package default (targetEdition null -> edition map 2021)
        {'unitId': LIB_UNIT, 'markerPath': HASH_DIR + '/Cargo.toml', 'crateName': 'app1',
         'targetKind': 'lib', 'targetName': 'app1', 'targetEdition': None},
        # bin target takes the package default too
        {'unitId': BIN_UNIT, 'markerPath': HASH_DIR + '/Cargo.toml', 'crateName': 'app1',
         'targetKind': 'bin', 'targetName': 'app1', 'targetEdition': None},
        # TARGET-SPECIFIC EDITION that differs from its package default (2021 -> 2024)
        {'unitId': TEST_UNIT, 'markerPath': HASH_DIR + '/Cargo.toml', 'crateName': 'app1',
         'targetKind': 'test', 'targetName': 'it', 'targetEdition': 2024},
        {'unitId': CORE_UNIT, 'markerPath': 'crates/core-lib/Cargo.toml',
         'crateName': 'core-lib', 'targetKind': 'lib', 'targetName': 'core-lib',
         'targetEdition': None},
    ], key=lambda u: u['unitId'].encode())
    SHARED = HASH_DIR + '/src/shared.rs'
    LIBP = HASH_DIR + '/src/lib.rs'
    ownership = sorted([
        {'path': SHARED, 'unitId': LIB_UNIT},
        {'path': SHARED, 'unitId': BIN_UNIT},
        {'path': LIBP, 'unitId': LIB_UNIT},
        {'path': LIBP, 'unitId': TEST_UNIT},     # same physical file, test target at 2024
        {'path': HASH_DIR + '/src/main.rs', 'unitId': BIN_UNIT},
        {'path': 'crates/core-lib/src/lib.rs', 'unitId': CORE_UNIT},
    ], key=lambda r: (r['path'].encode(), r['unitId'].encode()))

    def ownership_record(selected):
        rec = {'schemaVersion': 1, 'enumeration': 'complete', 'units': units,
               'selectedUnitIds': sorted(selected, key=lambda s: s.encode()),
               'ownership': ownership}
        hx = b.native_framed('native.source-unit-ownership.v1', B.NATIVE_DOC,
                             '#/$defs/SourceUnitOwnershipV1', rec,
                             'source-unit-ownership:' + ','.join(
                                 s[7:15] for s in sorted(selected)))
        return hx, rec

    own_lib_hex, own_lib = ownership_record([LIB_UNIT, BIN_UNIT, CORE_UNIT])
    own_test_hex, own_test = ownership_record([TEST_UNIT])
    # stable-body pair: adding the BIN target changes the SELECTION but not the effective
    # dialect of crates/app#1/src/shared.rs (both lib and bin take the 2021 package default)
    own_libonly_hex, own_libonly = ownership_record([LIB_UNIT, CORE_UNIT])

    def universe(own_hex, label):
        rec = {'schemaVersion': 2, 'edition': dict(EDITIONS),
               'lockfileIdentity': lockid,
               'dependencySourceSetId': 'sha256:' + dep_hex,
               'unifiedFeaturesId': 'sha256:' + feat_hex,
               'nativeContextId': 'sha256:' + ctx_hex,
               'cfgSets': [{'cfgSetId': 'default',
                            'cfg': sorted(['feature="std"', 'target_os="macos"'])}],
               'rustflags': cargo_proj['rustflags'],
               'crateRootPaths': sorted([LIBP, 'crates/core-lib/src/lib.rs'],
                                        key=lambda s: s.encode()),
               'configProjectionSha256': cargo_hex,
               'executionCapableResolution': False,
               'preparedOutputSetId': None, 'preparedResolution': 'none',
               'sourceUnitOwnershipId': 'sha256:' + own_hex}
        hx = b.native_framed('native.semantic-universe.rust.v2', B.NATIVE_DOC,
                             '#/$defs/RustUniverseV2ResolvedInputs', rec,
                             'native-universe:rust:' + label)
        return hx, rec

    uni_a_hex, uni_a = universe(own_lib_hex, 'selection-lib-bin-core')
    uni_b_hex, uni_b = universe(own_test_hex, 'selection-test-2024')
    uni_c_hex, uni_c = universe(own_libonly_hex, 'selection-lib-core')

    # ---------------------------------------------------------------- capability manifest
    A = CM.CapabilityManifestAdmitter()
    cap = {'schemaVersion': 1, 'profile': 'rust-cargo',
           'providers': [{'providerId': 'opensip.provider.rust', 'language': 'rust',
                          'providerVersionSource': 'closure2.semanticVersion',
                          'toolchainIdentitySource': 'ToolchainIdentityV1',
                          'relations': {'file': 'enumerated',
                                        'package': 'manifest-declared',
                                        'vcs-change': 'vcs-reported',
                                        'declares': 'syntactic', 'literal': 'syntactic',
                                        'control-flow': 'syntactic',
                                        'clones': 'normalized-body-hash',
                                        'imports': 'resolved-target',
                                        'references': 'resolved-binding',
                                        'calls': 'resolved-callee', 'types': 'checked',
                                        'reachability': 'from-resolved-calls',
                                        'unresolved-edge': 'observed'},
                          'platformIds': ['macos-aarch64']}],
           'coverageForAbsent': []}
    capres = A.admit(cap)
    assert capres['admitted']
    st.put_blob(capres['committedBytes'], label='capability-manifest-artifact')

    # ---------------------------------------------------------------- body identities
    def effective_edition(own, path, selected=None):
        """The EFFECTIVE edition of the SELECTED compilation target that owns this path:
        the unit targetEdition when it states one, otherwise the universe edition map entry
        for its crateName. Rows are those whose path EQUALS the anchor path; then restricted
        to selectedUnitIds; selected owners must AGREE."""
        sel = set(selected if selected is not None else own['selectedUnitIds'])
        rows = [r for r in own['ownership'] if r['path'] == path]
        if not rows:
            raise RuntimeError('BODY_LANGUAGE_OWNER_NOT_COMPILED:' + path)
        chosen = [r for r in rows if r['unitId'] in sel]
        if not chosen:
            raise RuntimeError('BODY_LANGUAGE_OWNER_NOT_SELECTED:' + path)
        eds = set()
        for r in chosen:
            u = [x for x in own['units'] if x['unitId'] == r['unitId']][0]
            eds.add(u['targetEdition'] if u['targetEdition'] is not None
                    else EDITIONS[u['crateName']])
        if len(eds) != 1:
            raise RuntimeError('BODY_LANGUAGE_OWNER_AMBIGUOUS:%s %s' % (path, sorted(eds)))
        return eds.pop()

    def body_for(path, span_bytes, own, label):
        ed = effective_edition(own, path)
        blv = {'schemaVersion': 1, 'languageId': 'rust', 'compilerName': 'rustc',
               'compilerVersion': toolchain['rustcVersion'],
               'compilerBuild': toolchain['rustCommitHash'],
               'dialect': {'edition': ed}}
        b.admit(B.IDENTITY_DOC, '#/$defs/body-language-version', blv,
                'body-language-version:rust:%d' % ed)
        st.put_blob(K.C(blv), label='body-language-version:rust:%d' % ed)
        lv = bytes.fromhex(K.rec_digest(blv))
        frame = B.body_identity_frame('L0-verbatim', K.raw_sha256(L0_SPEC), 'rust', lv,
                                      B.l0_payload(span_bytes))
        bid = K.raw_sha256(frame)
        st.put_blob(frame, label='body-identity-frame:%s' % label)
        return ({'bodyIdentity': 'sha256:' + bid, 'normalisationLevel': 'L0-verbatim',
                 'normalisationVersion': K.raw_sha256(L0_SPEC)}, bid, ed, blv)

    lib_body = b'{ shared::shared() }'
    p_shared_a, bid_shared_a, ed_a, blv_a = body_for(SHARED, BODY, own_lib, 'shared-selA')
    p_lib_a, bid_lib_a, _, _ = body_for(LIBP, lib_body, own_lib, 'lib-selA')
    p_lib_b, bid_lib_b, ed_b, blv_b = body_for(LIBP, lib_body, own_test, 'lib-selB')
    p_core, bid_core, _, _ = body_for('crates/core-lib/src/lib.rs', b'{ 7 + 1 }',
                                      own_lib, 'core')
    MAIN_BODY = b'{ println!("{}", app1::lib_entry()); }'
    p_main, bid_main, _, _ = body_for(HASH_DIR + '/src/main.rs', MAIN_BODY, own_lib, 'main')
    # measured stable-body pair: selection changes, effective dialect does not
    p_shared_c, bid_shared_c, ed_c, _ = body_for(SHARED, BODY, own_libonly, 'shared-selC')

    # ---------------------------------------------------------------- facts
    facts, fact_payloads = {}, {}

    def mk_fact(relation, rung, payload, anchors, label, uni, confidence=1000000):
        fid = b.fact(snapshot_id, relation, rung, uni, uni, provider_tid, payload,
                     anchors, confidence, label)
        facts[fid] = st.objects[fid]
        fact_payloads[fid] = payload
        return fid

    def anchor(path, span):
        row = [r for r in sh['inventory'] if r['path'] == path][0]
        return {'path': path, 'blobDigest': row['sha256'],
                'startByte': span[0], 'endByte': span[1]}

    for p in sorted(FILES, key=lambda s: s.encode()):
        row = [r for r in sh['inventory'] if r['path'] == p][0]
        mk_fact('file', 'enumerated',
                {'path': p, 'contentSha256': row['sha256'], 'byteLength': row['bytes']},
                [], 'file:' + p, uni_a_hex)
    mk_fact('package', 'manifest-declared',
            {'packageName': 'app1', 'packageVersion': '0.3.0',
             'manifestPath': HASH_DIR + '/Cargo.toml'}, [], 'package:app1', uni_a_hex)
    mk_fact('package', 'manifest-declared',
            {'packageName': 'core-lib', 'packageVersion': '0.1.0',
             'manifestPath': 'crates/core-lib/Cargo.toml'}, [], 'package:core-lib',
            uni_a_hex)
    shared_span = (SHARED_RS.index(BODY), SHARED_RS.index(BODY) + len(BODY))
    lib_span = (LIB_RS.index(lib_body), LIB_RS.index(lib_body) + len(lib_body))
    core_src = FILES['crates/core-lib/src/lib.rs']
    core_span = (core_src.index(b'{ 7 + 1 }'), core_src.index(b'{ 7 + 1 }') + 9)
    mk_fact('clones', 'normalized-body-hash', p_shared_a, [anchor(SHARED, shared_span)],
            'clones:shared-selA', uni_a_hex)
    mk_fact('clones', 'normalized-body-hash', p_lib_a, [anchor(LIBP, lib_span)],
            'clones:lib-selA', uni_a_hex)
    mk_fact('clones', 'normalized-body-hash', p_core,
            [anchor('crates/core-lib/src/lib.rs', core_span)], 'clones:core', uni_a_hex)
    main_span = (BIN_RS.index(MAIN_BODY), BIN_RS.index(MAIN_BODY) + len(MAIN_BODY))
    mk_fact('clones', 'normalized-body-hash', p_main,
            [anchor(HASH_DIR + '/src/main.rs', main_span)], 'clones:main', uni_a_hex)
    # SAME PHYSICAL FILE under the other explicitly selected target edition (2024)
    mk_fact('clones', 'normalized-body-hash', p_lib_b, [anchor(LIBP, lib_span)],
            'clones:lib-selB', uni_b_hex)
    SYMS = {'rs:app1::shared::shared': (SHARED, 'app1::shared::shared'),
            'rs:app1::lib_entry': (LIBP, 'app1::lib_entry'),
            'rs:core-lib::c': ('crates/core-lib/src/lib.rs', 'core-lib::c')}
    for sid, (path, qn) in sorted(SYMS.items()):
        src = FILES[path]
        mk_fact('declares', 'syntactic',
                {'container': 'rs:' + path, 'declared': sid, 'declarationKind': 'function'},
                [anchor(path, (0, len(src) - 1))], 'declares:' + sid, uni_a_hex)

    # ---------------------------------------------------------------- scopes + coverage
    scopes, coverages, coverage_payloads = {}, {}, {}

    def mk_scope_cov(relation, rung, subjects, label, uni, cov='complete', rc=None,
                     deficiency=None, native_cause=None):
        sid = b.scope(snapshot_id, relation, rung, uni, uni, provider_tid, subjects, label)
        scopes[sid] = st.objects[sid]
        ent = B.entry(cov, B.closed_world_open(['synthetic trusted observation']),
                      deficiency=deficiency, native_cause=native_cause,
                      rc=rc or B.rc_not_applicable())
        cid = b.coverage(sid, ent, label)
        coverages[cid] = st.objects[cid]
        coverage_payloads[cid] = json.loads(
            st.get_blob(st.objects[cid]['payloadDigest']).decode())
        return sid, cid

    RUST_CODE_A = sorted([SHARED, LIBP, HASH_DIR + '/src/main.rs',
                          'crates/core-lib/src/lib.rs'], key=lambda s: s.encode())
    s_file, c_file = mk_scope_cov('file', 'enumerated', sorted(FILES), 'file-enumerated',
                                 uni_a_hex)
    s_pkg, c_pkg = mk_scope_cov('package', 'manifest-declared', ['app1', 'core-lib'],
                                'package-declared', uni_a_hex)
    s_decl, c_decl = mk_scope_cov('declares', 'syntactic', sorted(SYMS),
                                  'declares-syntactic', uni_a_hex)
    s_clone_a, c_clone_a = mk_scope_cov('clones', 'normalized-body-hash', RUST_CODE_A,
                                        'clones-selA', uni_a_hex)
    s_clone_b, c_clone_b = mk_scope_cov('clones', 'normalized-body-hash', [LIBP],
                                        'clones-selB', uni_b_hex)
    return dict(b=b, st=st, snapshot_id=snapshot_id, snapshot=snapshot, sh=sh,
                closures=dict(tool=tool_tid, llvm=llvm_tid, provider=provider_tid,
                              evaluator=evaluator_tid, detector=detector_tid),
                ctx_hex=ctx_hex, uni_hex=uni_a_hex,
                universe_digests=[uni_a_hex, uni_b_hex, uni_c_hex],
                uni_a=uni_a_hex, uni_b=uni_b_hex, uni_c=uni_c_hex,
                cap=cap, capres=capres, config=config, files=FILES,
                facts=facts, fact_payloads=fact_payloads, scopes=scopes,
                coverages=coverages, coverage_payloads=coverage_payloads,
                syms=SYMS, code=RUST_CODE_A, editions=EDITIONS, toolchain=toolchain,
                units=units, ownership=ownership, own_lib=own_lib, own_test=own_test,
                own_libonly=own_libonly,
                own_hex=dict(a=own_lib_hex, b=own_test_hex, c=own_libonly_hex),
                unit_ids=dict(lib=LIB_UNIT, bin=BIN_UNIT, test=TEST_UNIT, core=CORE_UNIT),
                bodies=dict(shared_a=bid_shared_a, shared_c=bid_shared_c,
                            lib_a=bid_lib_a, lib_b=bid_lib_b, core=bid_core,
                            main=bid_main),
                body_editions=dict(a=ed_a, b=ed_b, c=ed_c),
                blv=dict(a=blv_a, b=blv_b), hash_dir=HASH_DIR, shared=SHARED, libp=LIBP,
                dep_hex=dep_hex, feat_hex=feat_hex, cargo_hex=cargo_hex, man_hex=man_hex,
                depset=depset, feats=feats, cargo_proj=cargo_proj, manifest=manifest,
                l0_spec=L0_SPEC, lockid=lockid,
                view_parts=dict(scopes=[s_file, s_pkg, s_decl, s_clone_a, s_clone_b],
                                coverages=[c_file, c_pkg, c_decl, c_clone_a, c_clone_b]))


if __name__ == '__main__':
    g = build()
    print('snapshot', g['snapshot_id'])
    print('context ', g['ctx_hex'])
    print('universes', g['universe_digests'])
    print('body editions', g['body_editions'])
    print('bodies', {k: v[:16] for k, v in g['bodies'].items()})
    print('facts', len(g['facts']), 'scopes', len(g['scopes']))
    print('admissions', len(g['b'].admissions),
          'all admitted', all(a['admitted'] for a in g['b'].admissions))
