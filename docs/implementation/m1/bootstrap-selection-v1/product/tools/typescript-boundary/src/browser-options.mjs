// Shared explicit options for the proposed report bundler and its resolver.
// Return fresh mutable arrays because the esbuild API consumes ordinary options.
export function browserOptions() {
 return {bundle:true,platform:'browser',format:'iife',target:['es2022'],
  mainFields:['browser','module','main'],conditions:['module'],
  resolveExtensions:['.js','.mjs','.cjs','.json'],preserveSymlinks:false,
  tsconfigRaw:{compilerOptions:{}},packages:'bundle',splitting:false,
  write:false,logLevel:'silent'};
}
