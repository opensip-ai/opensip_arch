'use strict';
// Adapter around the byte-identical copy of the unreviewed compiler-API
// reference. The reference itself is not modified.
const fs = require('node:fs');
const path = require('node:path');
const { check } = require('../../reference-copy/check-typescript-edges.cjs');

const REFERENCE_TYPESCRIPT = '/tmp/opensip-implementation/m1-control-generation-candidate-02/tools/contracts/node_modules/typescript';
const INVENTORY = '/Users/sb/code/opensip-ai/opensip_arch/docs/v2/architecture/repository-file-inventory.v1.json';

const [root, laneId, lanesFile] = process.argv.slice(2);
const lanes = JSON.parse(fs.readFileSync(lanesFile, 'utf8'));
const lane = lanes.lanes[laneId];
const inventory = { packages: JSON.parse(fs.readFileSync(INVENTORY, 'utf8')).packages };
const started = process.hrtime.bigint();
let output;
try {
  const result = check({ root, inventory, lane: lane.referenceInventoryId, config: lane.tsconfig, files: lane.inputs, compiler: path.resolve(REFERENCE_TYPESCRIPT) });
  output = { passed: true, result };
} catch (error) {
  output = { passed: false, message: error.message };
}
output.milliseconds = Number(process.hrtime.bigint() - started) / 1e6;
process.stdout.write(JSON.stringify(output) + '\n');
