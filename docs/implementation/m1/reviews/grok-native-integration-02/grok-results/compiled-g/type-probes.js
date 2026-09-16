"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const cancelled = { executionId: null, analysisOrdinal: null, observedPhase: 'snapshot' };
// @ts-expect-error present null and missing are different
const missing = { executionId: null, observedPhase: 'snapshot' };
// @ts-expect-error integer literal remains bigint
const rounded = { executionId: null, analysisOrdinal: 0, observedPhase: 'snapshot' };
// @ts-expect-error const is not broadened to arbitrary bigint
const nonzero = { executionId: null, analysisOrdinal: 1n, observedPhase: 'snapshot' };
const file = { kind: 'file', path: 'a', byteLength: 18446744073709551615n, contentSha256: 'a', linkTarget: null };
// @ts-expect-error discriminator must agree with field shape
const wrongKind = { kind: 'symlink', path: 'a', byteLength: 4n, contentSha256: 'a', linkTarget: null };
const chunk = { snapshotId: 's', path: 'a', chunkIndex: 0n, byteOffset: 0n, bytes: new Uint8Array([255]) };
// @ts-expect-error byte arrays cannot become number arrays
const arrayChunk = { ...chunk, bytes: [255] };
// @ts-expect-error no hex/text representation at the carrier
const textChunk = { ...chunk, bytes: 'ff' };
const stage = { kind: 'fact-derivation', stageId: 's', relations: ['calls'], operator: 'semantic-provider' };
const presentStage = { ...stage, dependsOn: [], providerId: 'rust-semantic' };
// @ts-expect-error optional means absent, not undefined
const undefinedStage = { ...stage, dependsOn: undefined };
// @ts-expect-error optional does not imply nullable
const nullStage = { ...stage, dependsOn: null };
const frame = { protocolMajor: 2n, frameType: 'Cancelled', sequence: 4n, payload: cancelled };
// @ts-expect-error actual wire tag determines payload type
const mismatchedFrame = { protocolMajor: 2n, frameType: 'SnapshotFileChunk', sequence: 4n, payload: cancelled };
// @ts-expect-error wire major is exact bigint
const wrongMajor = { ...frame, protocolMajor: 3n };
const validDirection = { protocolMajor: 3n, direction: 'worker-to-host', sequence: 0n, frameType: 'DependencySourceAccepted', payload: accepted };
// @ts-expect-error payload is valid; only the direction is wrong
const wrongDirection = { protocolMajor: 3n, direction: 'host-to-worker', sequence: 0n, frameType: 'DependencySourceAccepted', payload: accepted };
void [cancelled, missing, rounded, nonzero, file, wrongKind, chunk, arrayChunk, textChunk,
    stage, presentStage, undefinedStage, nullStage, frame, mismatchedFrame, wrongMajor, validDirection, wrongDirection];
const validHostDirection = { protocolMajor: 3n, direction: 'host-to-worker', sequence: 0n, frameType: 'DependencySourceChunk', payload: seal };
// @ts-expect-error complete valid host payload; only direction is wrong
const wrongHostDirection = { protocolMajor: 3n, direction: 'worker-to-host', sequence: 0n, frameType: 'DependencySourceChunk', payload: seal };
void [validHostDirection, wrongHostDirection];
