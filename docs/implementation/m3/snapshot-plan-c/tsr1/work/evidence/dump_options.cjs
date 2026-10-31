// Interpretation evidence only: dump TypeScript's own compiler option declarations from the pinned package.
const ts = require(process.argv[2]);
const out = [];
for (const o of ts.optionDeclarations) {
  const t = typeof o.type === 'string' ? o.type : 'enum';
  out.push({
    name: o.name, type: t,
    element: o.element ? (typeof o.element.type === 'string' ? o.element.type : 'enum') : undefined,
    isCommandLineOnly: !!o.isCommandLineOnly,
    isFilePath: !!o.isFilePath || !!(o.element && o.element.isFilePath),
    affectsModuleResolution: !!o.affectsModuleResolution,
    affectsProgramStructure: !!o.affectsProgramStructure,
    affectsSemanticDiagnostics: !!o.affectsSemanticDiagnostics,
    affectsEmit: !!o.affectsEmit,
    affectsSourceFile: !!o.affectsSourceFile,
    affectsBindDiagnostics: !!o.affectsBindDiagnostics,
    strictFlag: !!o.strictFlag,
    allowConfigDirTemplateSubstitution: !!o.allowConfigDirTemplateSubstitution,
    enumKeys: (typeof o.type !== 'string') ? [...o.type.keys()] : (o.element && typeof o.element.type !== 'string' ? [...o.element.type.keys()] : undefined),
    deprecatedKeys: o.deprecatedKeys ? [...o.deprecatedKeys] : (o.element && o.element.deprecatedKeys ? [...o.element.deprecatedKeys] : undefined),
    category: o.category ? o.category.message : undefined,
  });
}
console.log(JSON.stringify({version: ts.version, options: out}, null, 1));
