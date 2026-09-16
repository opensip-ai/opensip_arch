"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const cancel = { executionId: null, analysisOrdinal: null, observedPhase: "snapshot" };
const frame = { protocolMajor: 2n, frameType: "Cancelled", sequence: 0n, payload: cancel };
// @ts-expect-error binary chunks remain byte arrays
const bad = { snapshotId: "s", path: "a", chunkIndex: 0n, byteOffset: 0n, bytes: [1] };
void [frame, bad];
