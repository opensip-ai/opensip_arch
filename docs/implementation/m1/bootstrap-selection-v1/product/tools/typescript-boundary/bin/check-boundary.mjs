#!/usr/bin/env node
// CLI entry. It always runs: there is no argv[1] self-detection, so realpath,
// /tmp-aliased and .bin symlink invocations behave identically (review-02 R1).
// Node honours the parent argument of import.meta.resolve(specifier, parent)
// only with --experimental-import-meta-resolve, so the CLI re-executes itself
// with that flag; src/resolve.mjs verifies the flag took effect before use.
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const FLAG = '--experimental-import-meta-resolve';
if (!process.execArgv.includes(FLAG)) {
  const self = fs.realpathSync(fileURLToPath(import.meta.url));
  const child = spawnSync(process.execPath, [FLAG, '--no-warnings', self, ...process.argv.slice(2)], { stdio: 'inherit' });
  process.exit(child.status ?? 3);
}
const { main } = await import('../src/check.mjs');
process.exitCode = await main(process.argv.slice(2));
