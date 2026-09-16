// TypeScript lane boundary checker. Resolver authorities:
//   build/declaration graph -> TypeScript 6.0.3 program, lane tsconfig and
//                              program.getModeForUsageLocation per usage;
//   Node runtime graph      -> Node 24 non-executing resolvers over TypeScript-
//                              emitted JavaScript (type-only imports erased by the
//                              emitter) and materialized JavaScript;
//   browser runtime graph   -> actual esbuild scanner with inert module bodies.
// Nothing is executed. Static literal requests only: unsupported forms are
// refused unless an exact trusted-usage record matches.
import fs from 'node:fs';
import { bindToolPolicy } from './tool-policy.mjs';
import path from 'node:path';
import crypto from 'node:crypto';
import { isBuiltin } from 'node:module';
import ts from 'typescript';
import { LaneError, validateLaneRecord, bindInventory, resolveLane, localPackageNames, strictJson } from './lane.mjs';
import { parse, runtimeUsages, buildUsages } from './usages.mjs';
import { assertImportMetaResolveParent, nodeResolve, nodeFormat, createBrowserResolvers, browserResolve } from './resolve.mjs';

const TOOL_VERSION = '0.10.0-root-candidate';
const TS_SOURCE = /\.(?:tsx|[cm]?ts)$/;
const DECLARATION = /\.d\.[cm]?ts$/;
const JS_FILE = /\.[cm]?jsx?$/;
const SCANNABLE = /\.(?:[cm]?[jt]sx?)$/;
const EXTERNAL = /(?:^|\/)node_modules\//;
const DEPENDENCY_CLASSES = ['dependencies', 'optionalDependencies', 'peerDependencies', 'devDependencies'];

const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const isBare = request => !request.startsWith('.') && !request.startsWith('/') && !request.startsWith('#') && !/^[a-zA-Z][a-zA-Z0-9+.-]*:/.test(request);
const packageName = request => request.startsWith('@') ? request.split('/').slice(0, 2).join('/') : request.split('/')[0];
const within = (rel, dir) => rel === dir || rel.startsWith(dir + '/');

export async function checkBoundary({ root, record, designLock, architecture, unboundKind, toolPolicyPath }) {
  const started = process.hrtime.bigint();
  assertImportMetaResolveParent();
  validateLaneRecord(record);
  if (typeof root !== 'string' || !fs.statSync(root, { throwIfNoEntry: false })?.isDirectory()) throw new LaneError('root must be an existing directory');
  root = fs.realpathSync(root);
  const binding = bindInventory({ architecture, designLock });
  const lane = resolveLane({ record, binding, unboundKind });
  const toolPolicy = bindToolPolicy({ architecture, designLock, policyPath: toolPolicyPath, root, record, lane });
  const trustedUsages = toolPolicy?.trustedUsages ?? record.trustedUsages;
  const rel = abs => path.relative(root, abs).split(path.sep).join('/');
  const abs = relPath => path.join(root, relPath);
  const own = record.packageRoot;
  const refusals = [];
  const refuse = (category, detail) => refusals.push({ category, ...detail });
  const inputs = new Set(record.inputs);
  let inventoryRowsPresent = [];
  let unboundInputs = [];
  let topology;
  // finish() may run before analysis (early refusal): everything it reads is bound here.
  const edges = [];
  const trustedApplied = new Set();
  const reachedLocal = new Set();
  const verifiedOutputs = new Map();

  // ---- declared inputs, manifest, package-source census ----
  for (const file of [...record.inputs, record.manifest, ...(record.tsconfig ? [record.tsconfig] : [])]) {
    if (!within(file, own) || EXTERNAL.test(file)) refuse('input-path', { file, message: 'declared file outside lane package or under node_modules' });
    let current = root;
    for (const part of file.split('/')) {
      current = path.join(current, part);
      const stat = fs.lstatSync(current, { throwIfNoEntry: false });
      if (!stat) { refuse('unresolved', { file, message: 'declared file missing' }); break; }
      if (stat.isSymbolicLink()) { refuse('input-path', { file, message: 'symlink in declared file path' }); break; }
    }
  }
  if (record.inputs.length !== inputs.size) refuse('input-path', { message: 'duplicate declared input' });
  if (refusals.length) return finish();
  if (lane.standing === 'bound' && record.trustedUsages.length) refuse('lane-record-invalid', { message: 'caller records cannot authorize loader exceptions for bound product packages; an independently selected tool policy is required' });
  const manifest = strictJson(fs.readFileSync(abs(record.manifest)), record.manifest);
  const localNames = localPackageNames(root, binding, manifest);
  const walkSources = dir => fs.readdirSync(abs(dir), { withFileTypes: true }).flatMap(entry => {
    const child = `${dir}/${entry.name}`;
    if (entry.isDirectory()) return entry.name === 'node_modules' ? [] : walkSources(child);
    return SCANNABLE.test(entry.name) ? [child] : [];
  });
  const localSources = walkSources(own);
  inventoryRowsPresent = lane.inventoryRows.filter(row => SCANNABLE.test(row) && fs.existsSync(abs(row)));
  unboundInputs = [...new Set([...record.inputs, record.manifest, ...(record.tsconfig ? [record.tsconfig] : [])])].filter(file => !lane.inventoryRows.includes(file));
  if (lane.standing === 'bound') for (const file of unboundInputs) refuse('inventory-ownership', { file, message: 'bound package input has no selected inventory row for this package' });

  // ---- package manager topology ----
  topology = { kind: record.packageManager.kind, lockfile: record.packageManager.lockfile };
  if (record.packageManager.lockfile) {
    const lockPath = abs(record.packageManager.lockfile);
    if (!fs.existsSync(lockPath)) refuse('topology', { message: 'declared lockfile missing ' + record.packageManager.lockfile });
    else topology.lockfileSha256 = sha256(fs.readFileSync(lockPath));
    if (record.packageManager.kind === 'pnpm') {
      const modulesYaml = path.join(path.dirname(lockPath), 'node_modules', '.modules.yaml');
      const text = fs.existsSync(modulesYaml) ? fs.readFileSync(modulesYaml, 'utf8') : '';
      topology.pnpm = { packageManager: /"packageManager": "([^"]+)"/.exec(text)?.[1], nodeLinker: /"nodeLinker": "([^"]+)"/.exec(text)?.[1] };
      if (!topology.pnpm.packageManager?.startsWith('pnpm@')) refuse('topology', { message: 'pnpm lane without a pnpm-materialized node_modules/.modules.yaml' });
      if (manifest.packageManager && manifest.packageManager !== topology.pnpm.packageManager) refuse('topology', { message: `manifest packageManager ${manifest.packageManager} differs from materialization ${topology.pnpm.packageManager}` });
    }
  }

  // ---- TypeScript configuration and program ----
  let parsed;
  let program;
  let options;
  const plannedOutputs = new Map();
  const emitted = new Map();
  const tsInputs = record.inputs.filter(file => TS_SOURCE.test(file) && !DECLARATION.test(file));
  if (record.tsconfig) {
    const reads = new Set();
    const host = {
      ...ts.sys,
      readFile(file) { const raw = ts.sys.readFile(file); if (raw !== undefined) reads.add(path.resolve(file)); return raw; },
      onUnRecoverableConfigFileDiagnostic(d) { refuse('config-invalid', { message: ts.flattenDiagnosticMessageText(d.messageText, '\n') }); },
    };
    parsed = ts.getParsedCommandLineOfConfigFile(abs(record.tsconfig), {}, host);
    if (parsed) {
      for (const d of parsed.errors) refuse('config-invalid', { message: ts.flattenDiagnosticMessageText(d.messageText, '\n') });
      if (parsed.projectReferences?.length) refuse('config-invalid', { message: 'project references are not selected' });
      if (parsed.options.plugins?.length) refuse('config-invalid', { message: 'compiler plugins are not selected' });
      if (parsed.options.outFile) refuse('config-invalid', { message: 'outFile concatenation is not selected' });
      if (parsed.options.typeRoots !== undefined) refuse('ambient-types', { message: 'typeRoots is not selected' });
      if (!Array.isArray(parsed.options.types)) refuse('ambient-types', { message: 'compilerOptions.types must be explicit' });
      for (const read of reads) {
        const physical = rel(fs.realpathSync(read));
        if (!within(physical, own) && !physical.startsWith('node_modules/')) refuse('config-owner', { file: physical, message: 'configuration read outside the lane package' });
      }
      for (const file of parsed.fileNames) if (!inputs.has(rel(path.resolve(file)))) refuse('config-include', { file: rel(file), message: 'tsconfig selects an undeclared input' });
      for (const name of parsed.options.types ?? []) {
        const typesPackage = name.startsWith('@types/') ? name : '@types/' + name.replace(/^@/, '').replace('/', '__');
        if (!DEPENDENCY_CLASSES.some(key => manifest[key]?.[typesPackage] !== undefined || manifest[key]?.[name] !== undefined)) refuse('ambient-types', { request: name, message: 'ambient type package not declared by the lane manifest' });
        if (lane.groups.some(g => g.platform === 'browser') && (name === 'node' || name === '@types/node')) refuse('browser-node', { request: name, message: 'browser lane selects Node ambient types' });
      }
      for (const option of ['outDir', 'declarationDir', 'tsBuildInfoFile']) {
        const output = parsed.options[option];
        if (typeof output !== 'string') continue;
        let existing = path.resolve(output);
        const missing = [];
        while (!fs.existsSync(existing) && path.dirname(existing) !== existing) {
          missing.unshift(path.basename(existing)); existing = path.dirname(existing);
        }
        const physical = rel(path.join(fs.realpathSync(existing), ...missing));
        if (!within(physical, own) || EXTERNAL.test(physical)) refuse('config-owner', { file: physical, message: `${option} would write outside owned package outputs` });
      }
      options = { ...parsed.options, allowJs: true, checkJs: false, noEmit: false, emitDeclarationOnly: false, declaration: false, declarationMap: false,
        sourceMap: false, inlineSourceMap: false, composite: false, incremental: false, noEmitOnError: false };
      const compilerHost = ts.createCompilerHost(options, true);
      program = ts.createProgram({ rootNames: record.inputs.filter(f => SCANNABLE.test(f)).map(abs), options, host: compilerHost });
      for (const file of record.inputs.filter(f => SCANNABLE.test(f))) {
        const sf = program.getSourceFile(abs(file));
        const diagnostics = sf ? program.getSyntacticDiagnostics(sf) : [];
        if (!sf) refuse('parse-failure', { file, message: 'compiler did not load declared input' });
        else if (diagnostics.length) refuse('parse-failure', { file, message: ts.flattenDiagnosticMessageText(diagnostics[0].messageText, '\n') });
      }
      for (const file of tsInputs) {
        const sf = program.getSourceFile(abs(file));
        if (!sf) continue;
        for (const output of ts.getOutputFileNames({ ...parsed, options }, abs(file), !ts.sys.useCaseSensitiveFileNames)) {
          if (JS_FILE.test(output)) plannedOutputs.set(path.resolve(output), abs(file));
        }
        program.emit(sf, (fileName, text, bom) => { if (JS_FILE.test(fileName)) emitted.set(abs(file), { location: path.resolve(fileName), text, bom }); }, undefined, false);
      }
    }
  } else if (tsInputs.length) {
    refuse('config-invalid', { message: 'TypeScript inputs require a lane tsconfig' });
  }

  // A completed build may leave JavaScript next to the authored source tree.
  // Admit only exact regular-file outputs freshly derived from declared inputs;
  // directory names such as dist are never a blanket source-census exemption.
  for (const file of localSources) {
    if (inputs.has(file)) continue;
    const physical = abs(file);
    const source = plannedOutputs.get(physical);
    const output = source && emitted.get(source);
    if (output && output.location === physical && fs.lstatSync(physical).isFile() &&
        fs.readFileSync(physical).equals(Buffer.from((output.bom ? '\uFEFF' : '') + output.text, 'utf8'))) {
      verifiedOutputs.set(physical, source);
    } else {
      refuse('undeclared-local', { file, message: 'package source is neither declared nor an exact compiler output' });
    }
  }

  const groupOf = file => lane.groups.find(g => g.match(file.slice(own.length + 1)));

  // ---- edge policy (shared by all graphs) ----
  function evaluate(edge, group) {
    edges.push(edge);
    const fromExternal = EXTERNAL.test(edge.from);
    if (isBare(edge.request) && (edge.request.includes('\\') || edge.request.split('/').some(part => part === '' || part === '.' || part === '..'))) { refuse('external-by-path', edgeDetail(edge, 'bare dependency request contains path traversal or ambiguous separators')); return false; }
    if (edge.core) {
      if (group?.platform === 'browser' && (edge.graph === 'runtime' || !fromExternal)) refuse('browser-node', edgeDetail(edge, 'Node built-in reached from browser code'));
      return false;
    }
    if (edge.ignored) return false;
    if (!edge.resolved) {
      const candidate = edge.candidate;
      if (!fromExternal && candidate && !EXTERNAL.test(candidate) && !candidate.startsWith('../') && !within(candidate, own)) refuse('lane-escape', edgeDetail(edge, 'unresolved request points into another package'));
      if (edge.graph === 'runtime' && matchTrusted('optional-unresolved', edge)) return false;
      refuse('unresolved', edgeDetail(edge, edge.error ?? 'unresolved request'));
      return false;
    }
    const target = edge.resolved;
    if (target.startsWith('../')) { refuse('outside-root', edgeDetail(edge, 'target outside the checked root')); return false; }
    const targetExternal = EXTERNAL.test(target);
    const requestName = isBare(edge.request) ? packageName(edge.request) : undefined;
    let traverse = true;
    if (!fromExternal) {
      if (targetExternal) {
        const ownMaterialization = target.startsWith('node_modules/') || within(target, own);
        if (!ownMaterialization) { refuse('lane-escape', edgeDetail(edge, 'own source reaches another package installation')); traverse = false; }
        if (!requestName) refuse('external-by-path', edgeDetail(edge, 'own source reaches materialized dependency files by path'));
        else declared(edge, group, requestName);
      } else if (!within(target, own)) {
        refuse('lane-escape', edgeDetail(edge, 'own source reaches another package'));
        traverse = false;
      }
      if (requestName && localNames.has(requestName) && requestName !== manifest.name && targetExternal) refuse('local-name-shadow', edgeDetail(edge, 'local package name realized from materialized dependencies'));
    } else {
      const materialized = target.startsWith('node_modules/') || (within(target, own) && EXTERNAL.test(target.slice(own.length + 1)));
      if (!targetExternal || !materialized) { refuse('reentry', edgeDetail(edge, 'materialized dependency reaches repository sources or another package installation')); traverse = false; }
      if (requestName && localNames.has(requestName)) refuse('local-name-shadow', edgeDetail(edge, 'dependency requests a local package name'));
    }
    if (targetExternal) {
      const segments = target.split('/');
      const index = segments.lastIndexOf('node_modules');
      const dirName = segments[index + 1]?.startsWith('@') ? segments.slice(index + 1, index + 3).join('/') : segments[index + 1];
      if (localNames.has(dirName)) refuse('local-name-shadow', edgeDetail(edge, 'materialized package directory uses a local package name'));
      const packageRoot = segments.slice(0, index + (segments[index + 1]?.startsWith('@') ? 3 : 2)).join('/');
      const packageManifest = abs(packageRoot + '/package.json');
      if (fs.existsSync(packageManifest)) {
        const realized = strictJson(fs.readFileSync(packageManifest), packageRoot + '/package.json');
        if (localNames.has(realized.name)) refuse('local-name-shadow', edgeDetail(edge, 'materialized package manifest claims a local package name'));
      }

    } else {
      reachedLocal.add(target);
    }
    return traverse;
  }

  function declared(edge, group, name) {
    const spec = DEPENDENCY_CLASSES.map(key => [key, manifest[key]?.[name]]).find(([, value]) => value !== undefined);
    const typesName = '@types/' + name.replace(/^@/, '').replace('/', '__');
    const typesSpec = edge.graph === 'build' ? DEPENDENCY_CLASSES.map(key => manifest[key]?.[typesName]).find(v => v !== undefined) : undefined;
    if (!spec && !typesSpec) { refuse('undeclared-external', edgeDetail(edge, `package ${name} is not declared by ${record.manifest}`)); return; }
    if (spec && typeof spec[1] === 'string' && spec[1].startsWith('npm:')) {
      const alias = /^(@[^/@]+\/[^/@]+|[^/@]+)(?:@.+)?$/.exec(spec[1].slice(4));
      if (!alias) { refuse('lane-record-invalid', edgeDetail(edge, 'malformed npm alias')); return; }
      const aliased = alias[1];
      if (localNames.has(name) || localNames.has(aliased)) refuse('local-name-shadow', edgeDetail(edge, `npm alias ${name} -> ${spec[1]} involves a local package name`));
    }
    if (edge.graph === 'runtime' && spec && group && !group.runtimeClasses.includes(spec[0])) refuse('runtime-dev-dependency', edgeDetail(edge, `${name} is only a ${spec[0]} entry but is reached by ${group.name}`));
  }

  const edgeDetail = (edge, message) => ({ graph: edge.graph, group: edge.group, from: edge.from, line: edge.line, column: edge.column, request: edge.request, mode: edge.mode, resolved: edge.resolved, message });

  function matchTrusted(kind, usage) {
    if (lane.standing === 'bound' && !toolPolicy) return undefined;
    for (const [index, trusted] of trustedUsages.entries()) {
      if (trusted.kind !== kind || trusted.file !== usage.from || trusted.line !== usage.line || trusted.column !== usage.column || trusted.text !== usage.text) continue;
      if (trusted.sha256 !== sha256(fs.readFileSync(abs(usage.from)))) continue;
      if (kind === 'optional-unresolved' && (trusted.request !== usage.request || trusted.mode !== usage.mode || !usage.guarded)) continue;
      trustedApplied.add(index);
      return trusted;
    }
    return undefined;
  }

  // ---- build/declaration graph (TypeScript resolver) ----
  if (program) {
    const host = ts.createCompilerHost(options, true);
    const cache = ts.createModuleResolutionCache(root, name => ts.sys.useCaseSensitiveFileNames ? name : name.toLowerCase(), options);
    const explained = new Set(record.inputs.map(abs));
    for (const sf of program.getSourceFiles()) {
      if (program.isSourceFileDefaultLibrary(sf)) continue;
      const from = rel(sf.fileName);
      const group = EXTERNAL.test(from) ? undefined : groupOf(from);
      // TypeScript checks TS sources and declarations (and JS only with checkJs); for
      // unchecked JS the build edge is recorded but resolvability belongs to the runtime graph.
      const typeChecked = !JS_FILE.test(sf.fileName) || options.checkJs === true || parsed.options.checkJs === true;
      for (const usage of buildUsages(sf)) {
        const edge = { graph: 'build', group: group?.name, from, kind: usage.kind, request: usage.request, line: usage.line, column: usage.column, typeOnly: usage.typeOnly, typeChecked };
        if (isBuiltin(usage.request)) { evaluate({ ...edge, core: true, coreModule: usage.request }, group); continue; }
        const mode = program.getModeForUsageLocation(sf, usage.node);
        edge.mode = mode === ts.ModuleKind.ESNext ? 'import' : mode === ts.ModuleKind.CommonJS ? 'require' : 'unspecified';
        const result = ts.resolveModuleName(usage.request, sf.fileName, options, host, cache, undefined, mode).resolvedModule;
        if (result) {
          const physical = fs.realpathSync(result.resolvedFileName);
          explained.add(physical);
          edge.resolved = rel(physical);
          // A tsconfig mapping cannot make a private external package path an
          // exported dependency interface. Preserve the real compiler edge,
          // and separately check the same package request without path aliases.
          if (!EXTERNAL.test(from) && EXTERNAL.test(edge.resolved) && isBare(usage.request)) {
            const publicOptions = { ...options, paths: undefined, baseUrl: undefined };
            const publicResult = ts.resolveModuleName(usage.request, sf.fileName, publicOptions, host, undefined, undefined, mode).resolvedModule;
            if (!publicResult || fs.realpathSync(publicResult.resolvedFileName) !== physical) refuse('external-by-path', edgeDetail(edge, 'tsconfig path mapping bypasses the external package export interface'));
          }

        } else if (usage.kind === 'augmentation') {
          continue; // an augmentation of an ambient module name is not a file request
        } else if (!typeChecked) {
          edges.push({ ...edge, error: 'TypeScript could not resolve the request (unchecked JavaScript; runtime graph decides)' });
          continue;
        } else {
          edge.error = 'TypeScript could not resolve the request';
        }
        evaluate(edge, group);
      }
      for (const reference of sf.referencedFiles) {
        const target = path.resolve(path.dirname(sf.fileName), reference.fileName);
        const exists = fs.existsSync(target);
        if (exists) explained.add(fs.realpathSync(target));
        evaluate({ graph: 'build', group: group?.name, from, kind: 'triple-slash-path', request: reference.fileName, resolved: exists ? rel(fs.realpathSync(target)) : undefined, error: exists ? undefined : 'referenced file missing' }, group);
      }
      for (const reference of sf.typeReferenceDirectives) {
        const result = ts.resolveTypeReferenceDirective(reference.fileName, sf.fileName, options, host, undefined, undefined, reference.resolutionMode).resolvedTypeReferenceDirective;
        if (result?.resolvedFileName) explained.add(fs.realpathSync(result.resolvedFileName));
        const edge = { graph: 'build', group: group?.name, from, kind: 'types-reference', request: reference.fileName, resolved: result?.resolvedFileName ? rel(fs.realpathSync(result.resolvedFileName)) : undefined, error: result ? undefined : 'unresolved type reference' };
        if (group?.platform === 'browser' && /^(?:@types\/)?node$/.test(reference.fileName)) refuse('browser-node', edgeDetail(edge, 'browser source requests Node ambient types'));
        if (evaluate(edge, group) && edge.resolved && !EXTERNAL.test(from) && EXTERNAL.test(edge.resolved)) declared(edge, group, reference.fileName);
      }
    }
    for (const name of parsed.options.types ?? []) {
      const result = ts.resolveTypeReferenceDirective(name, abs(record.tsconfig), options, host).resolvedTypeReferenceDirective;
      if (result?.resolvedFileName) explained.add(fs.realpathSync(result.resolvedFileName));
      else refuse('unresolved', { graph: 'build', from: record.tsconfig, request: name, message: 'types entry does not resolve' });
    }
    for (const sf of program.getSourceFiles()) {
      if (program.isSourceFileDefaultLibrary(sf)) continue;
      if (!explained.has(fs.realpathSync(sf.fileName))) refuse('compiler-unexplained-input', { file: rel(sf.fileName), message: 'TypeScript loaded a file no declared input or recorded edge explains' });
    }
  }

  // ---- runtime graphs (Node resolver / declared browser bundler policy) ----
  const browserResolvers = await createBrowserResolvers(root);
  const runtimeFiles = new Map();
  for (const group of lane.groups) {
    const entries = record.inputs.filter(file => SCANNABLE.test(file) && !DECLARATION.test(file) && groupOf(file) === group);
    const queue = entries.map(file => ({ file, viaOutput: true }));
    const seen = new Set();
    while (queue.length) {
      const { file, viaOutput } = queue.shift();
      const unitKey = file + (viaOutput ? '' : '#in-place');
      if (seen.has(unitKey)) continue;
      seen.add(unitKey);
      const unit = runtimeUnit(file, viaOutput);
      if (!unit) continue;
      const sf = parse(unit.location, unit.text, ts.ScriptKind.JS);
      runtimeFiles.set(unit.location, { file, text: unit.text, own: !EXTERNAL.test(file) });
      const usages = runtimeUsages(sf);
      const format = group.platform === 'node' ? nodeFormat(unit.location, usages) : 'bundled';
      if (format === 'invalid-package-scope' || format === 'ambiguous') refuse('unsupported-module-format', { graph: 'runtime', group: group.name, from: file, message: format === 'ambiguous' ? 'untyped .js mixes module syntax with require' : 'nearest package.json is invalid' });
      if (format === 'commonjs' && usages.esmSyntax) refuse('unsupported-module-format', { graph: 'runtime', group: group.name, from: file, message: 'module syntax in a CommonJS-format file' });
      if (format === 'module' && usages.requireCalls && !usages.declaresRequire) refuse('unsupported-module-format', { graph: 'runtime', group: group.name, from: file, message: 'require in an ES module without a local require binding' });
      for (const item of usages.unsupported) {
        if (EXTERNAL.test(file) && group.platform === 'node') continue; // inert without an AMD loader; disclosed limit
        if (item.localExportsOnly) continue; // exports/module pseudo-dependencies create no external module edge
        refuse('unsupported-module-format', { graph: 'runtime', group: group.name, from: file, line: item.line, column: item.column, message: `AMD request (${item.kind}) is not selected` });
      }
      for (const loader of usages.loaders) {
        if (loader.declaredInputsOnly && EXTERNAL.test(file)) continue;
        const trusted = unit.raw ? matchTrusted('dynamic-loader', { from: file, line: loader.line, column: loader.column, text: loader.text }) : undefined;
        if (!trusted) { refuse('unsupported-loader', { graph: 'runtime', group: group.name, from: file, line: loader.line, column: loader.column, message: `${loader.kind}: ${loader.text}` }); continue; }
        for (const target of trusted.targets) {
          if (!inputs.has(target)) { refuse('lane-record-invalid', { from: file, message: `trusted dynamic loader target ${target} is not a declared input` }); continue; }
          evaluate({ graph: 'runtime', group: group.name, from: file, kind: 'trusted-dynamic-loader', request: target, line: loader.line, column: loader.column, resolved: target }, group);
          queue.push({ file: target, viaOutput: true });
        }
      }
      for (const request of usages.requests) {
        const edge = { graph: 'runtime', group: group.name, from: file, kind: request.kind, request: request.request, mode: request.mode, line: request.line, column: request.column, text: request.text, guarded: request.guarded };
        let result = group.platform === 'node' ? nodeResolve(request.request, unit.location, request.mode) : await browserResolve(browserResolvers, request.request, unit.location, request.mode);
        if (request.builtinOnly && !result.core) result = { error: 'ERR_UNKNOWN_BUILTIN_MODULE' };
        let viaTarget = false;
        if (result.resolved && verifiedOutputs.has(path.resolve(result.resolved))) {
          const outputPath = path.resolve(result.resolved);
          result = { ...result, resolved: verifiedOutputs.get(outputPath), emittedOutput: rel(outputPath) };
          viaTarget = true;
        }
        if (!result.resolved && !result.core && !result.ignored && !EXTERNAL.test(file) && result.candidate && plannedOutputs.has(result.candidate)) {
          result = { resolved: plannedOutputs.get(result.candidate), emittedOutput: rel(result.candidate) };
          viaTarget = true;
        }
        Object.assign(edge, { suffix: result.suffix, core: result.core, ignored: result.ignored, error: result.error, emittedOutput: result.emittedOutput, candidate: result.candidate ? rel(result.candidate) : undefined, resolved: result.resolved && !result.core ? rel(result.resolved) : result.core ? result.resolved : undefined });
        if (edge.core) edge.resolved = undefined, edge.coreModule = result.resolved;
        if (evaluate(edge, group) && edge.resolved && !edge.core) queue.push({ file: edge.resolved, viaOutput: viaTarget });
      }
      for (const asset of usages.assets) {
        const target = path.resolve(path.dirname(unit.location), asset.request);
        const exists = fs.statSync(target, { throwIfNoEntry: false })?.isFile();
        const emittedSource = verifiedOutputs.get(target) ?? (!exists && !EXTERNAL.test(file) ? plannedOutputs.get(target) : undefined);
        const resolvedAsset = emittedSource ? rel(emittedSource) : exists ? rel(fs.realpathSync(target)) : undefined;
        const edge = { graph: 'runtime', group: group.name, from: file, kind: asset.kind, request: asset.request, line: asset.line, column: asset.column, resolved: resolvedAsset, emittedOutput: emittedSource ? rel(target) : undefined, candidate: resolvedAsset ? undefined : rel(target), error: resolvedAsset ? undefined : 'asset target missing' };
        if (evaluate(edge, group) && edge.resolved && SCANNABLE.test(edge.resolved)) queue.push({ file: edge.resolved, viaOutput: !!emittedSource });
      }
    }
  }

  await browserResolvers.dispose();

  function runtimeUnit(file, viaOutput) {
    const physical = abs(file);
    if (DECLARATION.test(file)) { refuse('unsupported-runtime-target', { graph: 'runtime', from: file, message: 'declaration file reached at runtime' }); return undefined; }
    if (TS_SOURCE.test(file) && !EXTERNAL.test(file)) {
      const output = emitted.get(physical);
      if (!output) { refuse('config-invalid', { graph: 'runtime', from: file, message: 'TypeScript runtime source has no emitted JavaScript (not part of the lane program)' }); return undefined; }
      return { location: viaOutput ? output.location : physical, text: output.text, raw: false };
    }
    if (JS_FILE.test(file)) {
      // Verified outputs have already mapped to their declared TypeScript input.
      // Never scan an undeclared local resolver hit on a failing census path.
      if (!EXTERNAL.test(file) && !inputs.has(file)) {
        refuse('unsupported-runtime-target', { graph: 'runtime', from: file, message: 'local JavaScript runtime target is not a declared input or verified compiler output' });
        return undefined;
      }
      return { location: physical, text: fs.readFileSync(physical, 'utf8'), raw: true };
    }
    if (TS_SOURCE.test(file)) { refuse('unresolved', { graph: 'runtime', from: file, message: 'TypeScript file under node_modules is not runnable (ERR_UNSUPPORTED_NODE_MODULES_TYPE_STRIPPING)' }); return undefined; }
    return undefined; // JSON, .node and other non-module assets are leaves
  }

  // ---- reached externals and syntax ----
  const externalUnits = [...runtimeFiles.entries()].filter(([, v]) => !v.own);
  if (externalUnits.length) {
    const texts = new Map(externalUnits.map(([location, v]) => [location, v.text]));
    const parseOptions = { allowJs: true, noResolve: true, noLib: true, types: [], noEmit: true };
    const host = ts.createCompilerHost(parseOptions, true);
    host.readFile = file => texts.get(path.resolve(file)) ?? ts.sys.readFile(file);
    const syntaxProgram = ts.createProgram({ rootNames: [...texts.keys()], options: parseOptions, host });
    for (const [location, v] of externalUnits) {
      const sf = syntaxProgram.getSourceFile(location);
      const diagnostics = sf ? syntaxProgram.getSyntacticDiagnostics(sf) : [];
      if (!sf || diagnostics.length) refuse('parse-failure', { graph: 'runtime', from: v.file, message: sf ? ts.flattenDiagnosticMessageText(diagnostics[0].messageText, '\n') : 'not parsed' });
    }
  }

  // ---- census of reached lane files and trusted-usage staleness ----
  for (const file of reachedLocal) if (within(file, own) && !inputs.has(file)) refuse('undeclared-local', { file, message: 'graph reaches an undeclared lane file' });
  trustedUsages.forEach((trusted, index) => {
    if (!trustedApplied.has(index)) refuse('lane-record-invalid', { file: trusted.file, line: trusted.line, column: trusted.column, message: `stale or mismatched ${trusted.kind} record` });
  });

  return finish();

  function finish() {
    const seen = new Set();
    const unique = refusals.filter(r => { const key = JSON.stringify(r); if (seen.has(key)) return false; seen.add(key); return true; });
    return {
      schemaVersion: 1,
      tool: { name: 'check-boundary', version: TOOL_VERSION, typescript: ts.version, node: process.version },
      lane: { package: record.package, packageRoot: record.packageRoot, standing: lane.standing, policy: lane.policyId, groups: lane.groups.map(g => ({ name: g.name, platform: g.platform, runtimeClasses: g.runtimeClasses })) },
      inventoryBinding: { designLockSha256: binding.designLockSha256, selectedInventory: binding.selectedInventory, inventoryStanding: binding.inventoryStanding, pinsVerified: binding.pinsVerified, inventorySuccessorsVerified: binding.inventorySuccessorsVerified, acceptanceChain: binding.acceptanceChain,
        inventoryRowsPresentUndeclared: inventoryRowsPresent.filter(row => !inputs.has(row)), inputsWithoutInventoryRow: unboundInputs },
      topology,
      passed: unique.length === 0,
      refusals: unique,
      selectedToolPolicy: toolPolicy ? { pin: toolPolicy.pin, acceptanceChain: toolPolicy.acceptanceChain, unfollowedDynamicLoaders: toolPolicy.unfollowedDynamicLoaders } : null,
      trustedUsagesApplied: trustedUsages.filter((_, index) => trustedApplied.has(index)),
      edges,
      stats: { verifiedGeneratedFiles: verifiedOutputs.size, edges: edges.length, milliseconds: Math.round(Number(process.hrtime.bigint() - started) / 1e6), maxRssBytes: process.resourceUsage().maxRSS * 1024 },
      sourcePurityQualified: false,
      dependencyClosureQualified: false,
      limits: [
        'Static literal module requests only; no module is executed. Computed loaders are refused unless an exact trusted-usage record matches; eval/Function are refused in lane sources only.',
        'Existing generated JavaScript is recognized only when regular-file bytes equal the selected compiler emission from declared inputs. Changed, linked and unexpected outputs remain undeclared; no output-directory exemption.',
        'Build graph: TypeScript 6.0.3 resolution with the lane tsconfig (allowJs forced on, emit forced for analysis). It does not prove runtime resolvability.',
        'Node runtime graph: Node 24 non-executing resolution of TypeScript-emitted or materialized JavaScript. Load-time failures other than missing files, directory imports and node_modules type stripping are not modelled.',
        'Browser runtime graph: proposed esbuild0.28.2 explicit browser recipe; tool-owned inert bodies prevent dependency execution. Physical ownership and query/fragment suffix are separate. External plugin/config execution is not selected. Tool/bootstrap/source selection remains pending.',
        'AMD calls inside materialized dependencies of Node groups are treated as inert (no AMD loader) and are not followed.',
        'Inventory binding verifies design-lock pins only; the acceptance chain is owned by tools/verify_design.py.',
      ],
    };
  }
}

function parseArguments(argv) {
  const usage = 'usage: check-boundary --root DIR --lane-record FILE --design-lock FILE --architecture DIR [--unbound-lane tooling] [--tool-policy ARCHITECTURE_RELATIVE_PATH]';
  const keys = ['--root', '--lane-record', '--design-lock', '--architecture', '--unbound-lane', '--tool-policy'];
  const values = {};
  for (let i = 0; i < argv.length; i += 2) {
    const [key, value] = [argv[i], argv[i + 1]];
    if (!keys.includes(key) || Object.hasOwn(values, key) || typeof value !== 'string' || !value || value.startsWith('--')) throw new LaneError(usage);
    values[key] = value;
  }
  for (const key of keys.slice(0, 4)) if (!values[key]) throw new LaneError(usage);
  return values;
}

export async function main(argv) {
  try {
    const args = parseArguments(argv);
    let record;
    try { record = strictJson(fs.readFileSync(args['--lane-record']), 'lane record'); } catch (error) {
      throw error instanceof LaneError ? error : new LaneError('cannot read lane record: ' + error.message);
    }
    if (!fs.existsSync(args['--design-lock']) || !fs.statSync(args['--architecture'], { throwIfNoEntry: false })?.isDirectory()) throw new LaneError('design lock file and architecture directory must exist');
    const report = await checkBoundary({ root: args['--root'], record, designLock: args['--design-lock'], architecture: args['--architecture'], unboundKind: args['--unbound-lane'], toolPolicyPath: args['--tool-policy'] });
    process.stdout.write(JSON.stringify(report, null, 2) + '\n');
    return report.passed ? 0 : 1;
  } catch (error) {
    process.stderr.write('boundary check refused: ' + error.message + '\n');
    return error instanceof LaneError ? 2 : 3;
  }
}
