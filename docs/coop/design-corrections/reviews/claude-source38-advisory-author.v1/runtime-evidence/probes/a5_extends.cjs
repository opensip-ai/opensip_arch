// A5 focused counterexample probe: effective allowJs/checkJs under `extends`, with the retained official
// TypeScript 5.6.3 compiler bytes from root's A5 directory (read-only). Memory files only; no repository code runs;
// no network. Supporting evidence, not a toolchain pin or product qualification.
const ts = require('/tmp/opensip-design-corrections/root-consumer24-js-options.v1/compiler/lib/typescript.js');
const cases = [
  {id: 'jsconfig-entry-extends-base-allowJs-false', entry: 'jsconfig.json', own: {}, base: {name: 'base.json', options: {allowJs: false}}},
  {id: 'jsconfig-entry-checkJs-extends-base-allowJs-false', entry: 'jsconfig.json', own: {checkJs: true}, base: {name: 'base.json', options: {allowJs: false}}},
  {id: 'jsconfig-entry-extends-base-allowJs-false-checkJs-true', entry: 'jsconfig.json', own: {}, base: {name: 'base.json', options: {allowJs: false, checkJs: true}}},
  {id: 'jsconfig-entry-own-allowJs-false-extends-base-allowJs-true', entry: 'jsconfig.json', own: {allowJs: false}, base: {name: 'base.json', options: {allowJs: true}}},
  {id: 'tsconfig-entry-extends-base-named-jsconfig', entry: 'tsconfig.json', own: {}, base: {name: 'shared/jsconfig.json', options: {}}},
  {id: 'tsconfig-entry-extends-base-named-jsconfig-explicit-false', entry: 'tsconfig.json', own: {}, base: {name: 'shared/jsconfig.json', options: {allowJs: false}}},
  {id: 'tsconfig-entry-extends-base-checkJs-true', entry: 'tsconfig.json', own: {}, base: {name: 'base.json', options: {checkJs: true}}},
  {id: 'tsconfig-entry-checkJs-false-extends-base-checkJs-true', entry: 'tsconfig.json', own: {checkJs: false}, base: {name: 'base.json', options: {checkJs: true}}},
  {id: 'tsconfig-entry-checkJs-true-extends-base-allowJs-false', entry: 'tsconfig.json', own: {checkJs: true}, base: {name: 'base.json', options: {allowJs: false}}},
  {id: 'tsconfig-entry-allowJs-true-extends-base-allowJs-false', entry: 'tsconfig.json', own: {allowJs: true}, base: {name: 'base.json', options: {allowJs: false}}},
];
const rows = [];
for (const c of cases) for (const jsFilePresent of [false, true]) {
  const files = {'/review/main.ts': 'export const x = 1;'};
  if (jsFilePresent) files['/review/helper.js'] = 'export const y = 1;';
  const basePath = '/review/' + c.base.name;
  files[basePath] = JSON.stringify({compilerOptions: c.base.options});
  const config = {extends: './' + c.base.name, compilerOptions: {noLib: true, noEmit: true, ...c.own}, include: ['*.ts', '*.js']};
  const configName = '/review/' + c.entry;
  files[configName] = JSON.stringify(config);
  const readFile = name => files[name];
  const parsed = ts.parseJsonConfigFileContent(config, {
    useCaseSensitiveFileNames: true, readFile, fileExists: name => name in files,
    readDirectory: (_root, extensions) => Object.keys(files).filter(name => !name.endsWith('.json') && extensions.some(ext => name.endsWith(ext))),
  }, '/review', undefined, configName);
  const host = {
    getSourceFile: (name, v) => files[name] === undefined ? undefined : ts.createSourceFile(name, files[name], v, true),
    getDefaultLibFileName: () => '/lib.d.ts', writeFile: () => {}, getCurrentDirectory: () => '/review', getDirectories: () => [],
    fileExists: name => name in files, readFile, getCanonicalFileName: name => name, useCaseSensitiveFileNames: () => true, getNewLine: () => '\n',
  };
  const program = ts.createProgram(parsed.fileNames, parsed.options, host);
  const roots = program.getRootFileNames();
  rows.push({id: c.id, entry: c.entry, own: c.own, base: c.base, jsFilePresent,
    parsedAllowJs: parsed.options.allowJs ?? null, parsedCheckJs: parsed.options.checkJs ?? null,
    effectiveAllowJs: ts.getAllowJSCompilerOption(parsed.options), checkJs: !!parsed.options.checkJs,
    rootFiles: roots, jsRootFiles: roots.filter(n => /\.(?:js|mjs|cjs|jsx)$/.test(n)),
    configDiagnostics: parsed.errors.map(x => x.code), optionDiagnostics: program.getOptionsDiagnostics().map(x => x.code)});
}
process.stdout.write(JSON.stringify({compilerVersion: ts.version, rows}, null, 1) + '\n');
