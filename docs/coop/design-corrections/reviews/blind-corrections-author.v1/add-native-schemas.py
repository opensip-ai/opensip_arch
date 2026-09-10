"""Author edit: add the closed TypeScript native-context descriptor family (blind consumer M-2) and the
subject-scope commitment / coverage-admission records (M-1) to the native schema bundle."""
import json, sys
from collections import OrderedDict
from pathlib import Path

p = Path(sys.argv[1]) / 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'
doc = json.loads(p.read_text(), object_pairs_hook=OrderedDict)
D = doc['$defs']

def obj(required, properties, **extra):
    o = OrderedDict([('type', 'object'), ('additionalProperties', False),
                     ('required', sorted(required)), ('properties', OrderedDict(properties))])
    o.update(extra)
    return o

ref = lambda n: OrderedDict([('$ref', '#/$defs/' + n)])
enum = lambda vals: OrderedDict([('type', 'string'), ('enum', list(vals))])
nullable = lambda s: OrderedDict([('oneOf', [s, OrderedDict([('type', 'null')])])])

new = OrderedDict()

new['TypeScriptModuleResolutionMode'] = OrderedDict([
    ('type', 'string'),
    ('enum', ['node16', 'nodenext', 'bundler', 'node10', 'classic']),
    ('description', 'The effective moduleResolution the admitted compiler applies. It changes which specifiers resolve, so it is a native-context field and a universe key.')])

new['TypeScriptLibComponentV1'] = obj(
    ['component', 'sha256'],
    [('component', OrderedDict([('type', 'string'), ('minLength', 1), ('maxLength', 256),
                                ('description', 'declaration file name inside the admitted stdlib closure tree, e.g. lib.es2022.d.ts')])),
     ('sha256', ref('DigestHex'))])

new['TypeScriptToolchainIdentityV1'] = obj(
    ['compilerName', 'compilerVersion', 'compilerPackageDigest', 'standardLibraryClosureId',
     'typescriptStdlibMerkleRoot', 'standardLibraryComponentDigests', 'libSelection'],
    [('compilerName', OrderedDict([('const', 'typescript')])),
     ('compilerVersion', OrderedDict([('type', 'string'), ('minLength', 1), ('maxLength', 256),
                                      ('description', 'the semanticVersion of the ADMITTED signed compiler closure manifest; never the output of an unverified `tsc --version`')])),
     ('compilerPackageDigest', ref('DigestHex')),
     ('standardLibraryClosureId', ref('ClosureId2')),
     ('typescriptStdlibMerkleRoot', OrderedDict([
         ('type', 'string'), ('pattern', '^[0-9a-f]{64}(?![\\s\\S])'),
         ('description', 'identity-and-evidence section 3: the 64-hex SUFFIX of standardLibraryClosureId (kind=stdlib). A bare DigestHex, not a Sha256Text: the typed prefix belongs to the foundation closure2 identity it was taken from. admit_typescript_native_context refuses a value that is not that suffix.')])),
     ('standardLibraryComponentDigests', OrderedDict([
         ('type', 'array'), ('items', ref('TypeScriptLibComponentV1')),
         ('minItems', 1), ('maxItems', 256), ('uniqueItems', True),
         ('description', 'raw SHA-256 of every declaration file of the admitted stdlib closure tree, which is retained whole; sorted by component UTF-8 bytes')])),
     ('libSelection', OrderedDict([
         ('type', 'array'), ('items', OrderedDict([('type', 'string'), ('minLength', 1), ('maxLength', 256)])),
         ('minItems', 1), ('maxItems', 64), ('uniqueItems', True),
         ('description', 'the effective `lib` names the resolved compilerOptions select (after target defaulting), sorted; each must name a retained component')]))])

new['TypeScriptToolClosureV1'] = obj(
    ['compiler', 'runtime', 'closureId'],
    [('compiler', ref('DigestHex')),
     ('runtime', ref('DigestHex')),
     ('closureId', ref('ClosureId2'))],
    description='Every executable the TypeScript adapter may select: the bundled compiler and the bundled JavaScript runtime that executes it, both members of the signed closure2 named by closureId. No PATH lookup, no system `node`, no NODE_OPTIONS/NODE_PATH/TS_NODE_* from the environment.')

new['TypeScriptStrippedOptionV1'] = obj(
    ['option', 'reason'],
    [('option', OrderedDict([('type', 'string'), ('minLength', 1), ('maxLength', 256)])),
     ('reason', enum(['selects-an-executable', 'emits-output', 'reads-the-environment',
                      'acquires-types-from-the-network', 'not-a-resolution-or-membership-option']))])

new['TypeScriptHonoredOptionsV1'] = obj(
    ['allowJs', 'checkJs', 'module', 'moduleResolution', 'target', 'strict', 'skipLibCheck',
     'noEmit', 'types', 'lib', 'baseUrl', 'paths', 'rootDirs', 'resolveJsonModule',
     'allowSyntheticDefaultImports', 'esModuleInterop', 'customConditions', 'jsx'],
    [('allowJs', OrderedDict([('type', 'boolean')])),
     ('checkJs', OrderedDict([('type', 'boolean')])),
     ('module', OrderedDict([('type', 'string'), ('minLength', 1), ('maxLength', 64)])),
     ('moduleResolution', ref('TypeScriptModuleResolutionMode')),
     ('target', OrderedDict([('type', 'string'), ('minLength', 1), ('maxLength', 64)])),
     ('strict', OrderedDict([('type', 'boolean')])),
     ('skipLibCheck', OrderedDict([('type', 'boolean')])),
     ('noEmit', OrderedDict([('const', True)])),
     ('types', nullable(OrderedDict([('type', 'array'), ('items', ref('Text')), ('maxItems', 1024), ('uniqueItems', True)]))),
     ('lib', OrderedDict([('type', 'array'), ('items', ref('Text')), ('minItems', 1), ('maxItems', 64), ('uniqueItems', True)])),
     ('baseUrl', nullable(ref('CanonicalPath'))),
     ('paths', OrderedDict([('type', 'array'), ('items', obj(['pattern', 'substitutions'], [
         ('pattern', OrderedDict([('type', 'string'), ('minLength', 1), ('maxLength', 1024)])),
         ('substitutions', OrderedDict([('type', 'array'), ('items', ref('CanonicalPath')), ('minItems', 1), ('maxItems', 64)]))])),
         ('maxItems', 4096), ('uniqueItems', True)])),
     ('rootDirs', OrderedDict([('type', 'array'), ('items', ref('CanonicalPath')), ('maxItems', 1024), ('uniqueItems', True)])),
     ('resolveJsonModule', OrderedDict([('type', 'boolean')])),
     ('allowSyntheticDefaultImports', OrderedDict([('type', 'boolean')])),
     ('esModuleInterop', OrderedDict([('type', 'boolean')])),
     ('customConditions', OrderedDict([('type', 'array'), ('items', ref('Text')), ('maxItems', 64), ('uniqueItems', True)])),
     ('jsx', nullable(OrderedDict([('type', 'string'), ('minLength', 1), ('maxLength', 64)])))],
    description='The closed subset of the resolved compilerOptions that changes program membership, module resolution or checking. Every value is the EFFECTIVE post-resolution value of the admitted tsconfig graph (or of SynthesizedCompilerOptionsV1 under js-synthesized), never a raw file field.')

new['TypeScriptConfigProjectionV2'] = obj(
    ['schemaVersion', 'ancestorCarrierVerified', 'environmentSanitized', 'typeAcquisitionEnabled',
     'executableSelected', 'honoredOptions', 'strippedOptions', 'configGraphPaths'],
    [('schemaVersion', OrderedDict([('const', 2)])),
     ('ancestorCarrierVerified', OrderedDict([('const', True)])),
     ('environmentSanitized', OrderedDict([('const', True)])),
     ('typeAcquisitionEnabled', OrderedDict([('const', False)])),
     ('executableSelected', OrderedDict([('const', False)])),
     ('honoredOptions', ref('TypeScriptHonoredOptionsV1')),
     ('strippedOptions', OrderedDict([('type', 'array'), ('items', ref('TypeScriptStrippedOptionV1')),
                                      ('maxItems', 256), ('uniqueItems', True)])),
     ('configGraphPaths', OrderedDict([('type', 'array'), ('items', ref('CanonicalPath')), ('minItems', 0),
                                       ('maxItems', 1024), ('uniqueItems', True),
                                       ('description', 'every tsconfig/jsconfig file in the resolved extends graph, in the snapshot, sorted by logical path; empty under configOrigin=synthesized')]))],
    description='The TypeScript counterpart of CargoConfigProjectionV2. Stripping an option is disclosed here; it is never a reason to read the option from anywhere else.')

new['TypeScriptLockfileIdentityV1'] = obj(
    ['kind', 'path', 'contentSha256'],
    [('kind', enum(['package-lock', 'pnpm-lock', 'yarn-lock', 'bun-lock'])),
     ('path', ref('CanonicalPath')),
     ('contentSha256', ref('DigestHex'))])

new['TypeScriptNativeContextV2'] = obj(
    ['schemaVersion', 'languageMode', 'toolchain', 'toolClosure', 'configProjection',
     'moduleResolutionMode', 'packageModuleType', 'nodeModulesLayoutDigest', 'lockfileIdentity'],
    [('schemaVersion', OrderedDict([('const', 2)])),
     ('languageMode', enum(['ts-tsconfig', 'js-allowjs', 'js-synthesized'])),
     ('toolchain', ref('TypeScriptToolchainIdentityV1')),
     ('toolClosure', ref('TypeScriptToolClosureV1')),
     ('configProjection', ref('TypeScriptConfigProjectionV2')),
     ('moduleResolutionMode', ref('TypeScriptModuleResolutionMode')),
     ('packageModuleType', enum(['module', 'commonjs', 'absent'])),
     ('nodeModulesLayoutDigest', nullable(ref('DigestHex'))),
     ('lockfileIdentity', nullable(ref('TypeScriptLockfileIdentityV1')))],
    description='Closed native context for the typescript-v2 universe; H domain `native.context.typescript.v2`. It carries no platform family: TypeScript resolution is platform-invariant by design (section 1.1), so the same source must not mint two nativeContextIds on two platform families. It is NOT NativeContextV2, which is the Rust context (targetTriple/hostTriple/cargo resolver); a typescript-v2 universe whose nativeContextId was minted from a Rust descriptor is refused.')

new['NativeContextLanguageV1'] = OrderedDict([
    ('type', 'string'), ('enum', ['rust', 'typescript']),
    ('description', 'which closed native-context record and H domain a universe binds')])

new['NativeContextAdmissionV1'] = obj(
    ['language', 'domain', 'nativeContextId', 'planNativeContextDigest', 'refusals'],
    [('language', ref('NativeContextLanguageV1')),
     ('domain', enum(['native.context.rust.v2', 'native.context.typescript.v2'])),
     ('nativeContextId', ref('Sha256Text')),
     ('planNativeContextDigest', ref('DigestHex')),
     ('refusals', OrderedDict([('type', 'array'), ('items', ref('Text')), ('maxItems', 64)]))],
    description='Host result of admitting one native context. nativeContextId is the Sha256Text the universe carries; planNativeContextDigest is the same 64 hex without the prefix, the spelling foundation plan.nativeContextDigests requires.')

new['SubjectScopeCommitmentV1'] = obj(
    ['scopeId', 'subjectScopeCommitment', 'subjectCount'],
    [('scopeId', OrderedDict([('type', 'string'), ('pattern', '^scope2:[0-9a-f]{64}(?![\\s\\S])')])),
     ('subjectScopeCommitment', ref('Sha256Text')),
     ('subjectCount', ref('Uint64'))],
    description='The producing result for the retained c2-plan-stage-schema.v4 coverage key field. subjectScopeCommitment is the SAME 64 hex as the foundation subject-scope identity scopeId, re-spelled in the native Sha256Text text form; it introduces no second preimage and no native H domain.')

new['CoverageAdmissionV1'] = obj(
    ['result', 'scopeId', 'coverageId', 'subjectScopeCommitment', 'subjectCount', 'refusals', 'faults'],
    [('result', enum(['ADMIT', 'REFUSE'])),
     ('scopeId', nullable(OrderedDict([('type', 'string'), ('pattern', '^scope2:[0-9a-f]{64}(?![\\s\\S])')]))),
     ('coverageId', nullable(OrderedDict([('type', 'string'), ('pattern', '^coverage2:[0-9a-f]{64}(?![\\s\\S])')]))),
     ('subjectScopeCommitment', nullable(ref('Sha256Text'))),
     ('subjectCount', nullable(ref('Uint64'))),
     ('refusals', OrderedDict([('type', 'array'), ('items', ref('Text')), ('maxItems', 64), ('uniqueItems', True)])),
     ('faults', OrderedDict([('type', 'array'), ('items', OrderedDict([('type', 'object')])), ('maxItems', 1024)]))],
    description='Result of the admitted native producer boundary for one CoverageResultV3 payload: the host mints scope2 from its own subject enumeration and refuses a payload whose committed key disagrees. A provider-supplied commitment is never authority.')

for k, v in new.items():
    if k in D:
        raise SystemExit('def already present: ' + k)
    D[k] = v

doc['description'] = doc['description'] + ' Blind-consumer corrections: the closed TypeScript native context (TypeScriptNativeContextV2 and family, domain native.context.typescript.v2, carrying typescriptStdlibMerkleRoot) and the subject-scope commitment / coverage-admission records.'
p.write_text(json.dumps(doc, indent=2) + '\n')
print('added', len(new), 'defs; total', len(D))
