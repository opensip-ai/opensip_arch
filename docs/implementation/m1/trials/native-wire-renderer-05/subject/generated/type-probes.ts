import type {
  Ts2CancelledV1, Ts2SnapshotEntryV1, Ts2SnapshotFileChunkV1,
  Rust3C2PlanStageV3, Ts2FrameV2, Rust3ProviderFrameV3, Rust3DependencySourceAcceptedV3, Rust3DependencySourceChunkV3,
} from './wire.js';

const cancelled: Ts2CancelledV1 = { executionId: null, analysisOrdinal: null, observedPhase: 'snapshot' };
// @ts-expect-error present null and missing are different
const missing: Ts2CancelledV1 = { executionId: null, observedPhase: 'snapshot' };
// @ts-expect-error integer literal remains bigint
const rounded: Ts2CancelledV1 = { executionId: null, analysisOrdinal: 0, observedPhase: 'snapshot' };
// @ts-expect-error const is not broadened to arbitrary bigint
const nonzero: Ts2CancelledV1 = { executionId: null, analysisOrdinal: 1n, observedPhase: 'snapshot' };
const file: Ts2SnapshotEntryV1 = { kind: 'file', path: 'a', byteLength: 18446744073709551615n, contentSha256: 'a', linkTarget: null };
// @ts-expect-error discriminator must agree with field shape
const wrongKind: Ts2SnapshotEntryV1 = { kind: 'symlink', path: 'a', byteLength: 4n, contentSha256: 'a', linkTarget: null };
const chunk: Ts2SnapshotFileChunkV1 = { snapshotId: 's', path: 'a', chunkIndex: 0n, byteOffset: 0n, bytes: new Uint8Array([255]) };
// @ts-expect-error byte arrays cannot become number arrays
const arrayChunk: Ts2SnapshotFileChunkV1 = { ...chunk, bytes: [255] };
// @ts-expect-error no hex/text representation at the carrier
const textChunk: Ts2SnapshotFileChunkV1 = { ...chunk, bytes: 'ff' };
const stage: Rust3C2PlanStageV3 = { kind: 'fact-derivation', stageId: 's', relations: ['calls'], operator: 'semantic-provider' };
const presentStage: Rust3C2PlanStageV3 = { ...stage, dependsOn: [], providerId: 'rust-semantic' };
// @ts-expect-error optional means absent, not undefined
const undefinedStage: Rust3C2PlanStageV3 = { ...stage, dependsOn: undefined };
// @ts-expect-error optional does not imply nullable
const nullStage: Rust3C2PlanStageV3 = { ...stage, dependsOn: null };
const frame: Ts2FrameV2 = { protocolMajor: 2n, frameType: 'Cancelled', sequence: 4n, payload: cancelled };
// @ts-expect-error actual wire tag determines payload type
const mismatchedFrame: Ts2FrameV2 = { protocolMajor: 2n, frameType: 'SnapshotFileChunk', sequence: 4n, payload: cancelled };
// @ts-expect-error wire major is exact bigint
const wrongMajor: Ts2FrameV2 = { ...frame, protocolMajor: 3n };
declare const accepted: Rust3DependencySourceAcceptedV3;
const validDirection: Rust3ProviderFrameV3 = { protocolMajor: 3n, direction: 'worker-to-host', sequence: 0n, frameType: 'DependencySourceAccepted', payload: accepted };
// @ts-expect-error payload is valid; only the direction is wrong
const wrongDirection: Rust3ProviderFrameV3 = { protocolMajor: 3n, direction: 'host-to-worker', sequence: 0n, frameType: 'DependencySourceAccepted', payload: accepted };
void [cancelled, missing, rounded, nonzero, file, wrongKind, chunk, arrayChunk, textChunk,
  stage, presentStage, undefinedStage, nullStage, frame, mismatchedFrame, wrongMajor, validDirection, wrongDirection];

declare const seal: Rust3DependencySourceChunkV3;
const validHostDirection: Rust3ProviderFrameV3 = { protocolMajor: 3n, direction: 'host-to-worker', sequence: 0n, frameType: 'DependencySourceChunk', payload: seal };
// @ts-expect-error complete valid host payload; only direction is wrong
const wrongHostDirection: Rust3ProviderFrameV3 = { protocolMajor: 3n, direction: 'worker-to-host', sequence: 0n, frameType: 'DependencySourceChunk', payload: seal };
void [validHostDirection, wrongHostDirection];
