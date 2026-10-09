'use strict';
const ts = require(process.argv[2]);
if (ts.version !== '6.0.3' || typeof ts.createProgram !== 'function') throw new Error('compiler-pin-api-mismatch');
process.stdout.write(JSON.stringify({event:'ready',version:ts.version})+'\n');
process.stdin.once('data', () => process.exit(0));
