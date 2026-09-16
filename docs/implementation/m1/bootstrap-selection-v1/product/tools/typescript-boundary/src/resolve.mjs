// Resolver adapters. Each graph has one authority and nothing is executed:
//   Node runtime  -> Node 24's own resolvers: createRequire(parent).resolve
//                    (checks existence) and import.meta.resolve(specifier, parent)
//                    followed by an explicit regular-file check, because
//                    import.meta.resolve does not check that its result exists.
//   browser       -> actual esbuild scanner with inert tool-owned module bodies.
// TypeScript build resolution is called directly from check.mjs.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire, isBuiltin } from 'node:module';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { createBrowserResolver } from './browser-scanner.mjs';

export function assertImportMetaResolveParent() {
  const probe = import.meta.resolve('./probe.mjs', 'file:///opensip-boundary-probe/base/');
  if (probe !== 'file:///opensip-boundary-probe/base/probe.mjs') {
    throw new Error('import.meta.resolve ignores its parent argument; run under --experimental-import-meta-resolve (bin/check-boundary.mjs does this)');
  }
}

export function nodeResolve(request, baseFile, mode) {
  if (isBuiltin(request)) return { core: true, resolved: request };
  if (mode === 'require') {
    try {
      const result = createRequire(baseFile).resolve(request);
      if (isBuiltin(result)) return { core: true, resolved: result };
      return { resolved: fs.realpathSync(result) };
    } catch (error) {
      const relative = request.startsWith('./') || request.startsWith('../');
      return { error: error.code ?? 'ERR_RESOLVE', candidate: relative ? path.resolve(path.dirname(baseFile), request) : undefined };
    }
  }
  let url;
  try {
    url = import.meta.resolve(request, pathToFileURL(baseFile).href);
  } catch (error) {
    return { error: error.code ?? 'ERR_RESOLVE' };
  }
  if (url.startsWith('node:')) return { core: true, resolved: url };
  if (!url.startsWith('file:')) return { error: 'ERR_UNSUPPORTED_ESM_URL_SCHEME', url };
  const candidate = fileURLToPath(url);
  const stat = fs.statSync(candidate, { throwIfNoEntry: false });
  if (!stat) return { error: 'ERR_MODULE_NOT_FOUND', candidate };
  if (stat.isDirectory()) return { error: 'ERR_UNSUPPORTED_DIR_IMPORT', candidate };
  if (!stat.isFile()) return { error: 'ERR_MODULE_NOT_FOUND', candidate };
  return { resolved: fs.realpathSync(candidate) };
}

// Node's package scope: nearest package.json, not crossing a node_modules directory.
// (module.findPackageJSON requires an existing module; emitted outputs may not exist.)
export function packageScope(file) {
  for (let dir = path.dirname(file); ; dir = path.dirname(dir)) {
    if (path.basename(dir) === 'node_modules') return { type: undefined };
    const manifest = path.join(dir, 'package.json');
    if (fs.existsSync(manifest)) {
      try {
        const parsed = JSON.parse(fs.readFileSync(manifest, 'utf8'));
        return { manifest, type: parsed.type };
      } catch {
        return { manifest, invalid: true };
      }
    }
    if (path.dirname(dir) === dir) return { type: undefined };
  }
}

export function nodeFormat(location, usages) {
  if (location.endsWith('.mjs')) return 'module';
  if (location.endsWith('.cjs')) return 'commonjs';
  const scope = packageScope(location);
  if (scope.invalid) return 'invalid-package-scope';
  if (scope.type === 'module') return 'module';
  if (scope.type === 'commonjs') return 'commonjs';
  if (/\.jsx?$/.test(location)) {
    // Node 24 detects module syntax in .js files whose scope has no "type" field.
    if (usages.esmSyntax && usages.requireCalls && !usages.declaresRequire) return 'ambiguous';
    if (usages.esmSyntax) return 'module';
  }
  return 'commonjs';
}

// Proposed selected esbuild scanner; package ownership uses the physical path.
// Query/fragment suffixes remain evidence and do not create a package boundary.
export async function createBrowserResolvers(root) {
  return createBrowserResolver(root);
}

export async function browserResolve(resolver, request, baseFile, mode) {
  const result = await resolver.resolve(request, baseFile, mode);
  if (result.kind === 'resolved') return { resolved: result.path, suffix: result.suffix };
  if (result.kind === 'ignored') return { ignored: true };
  if (isBuiltin(request)) return { core: true, resolved: request };
  const relative = request.startsWith('./') || request.startsWith('../');
  return { error: 'ERR_BROWSER_POLICY_UNRESOLVED',
    candidate: relative ? path.resolve(path.dirname(baseFile), request) : undefined,
    message: result.detail };
}
