// Review type-level controls for the provider carrier subset.
import type * as P from "../subject/output-b/providers/typescript/src/generated/protocol.js";
import type * as R from "../subject/output-b/apps/report/src/generated/report.js";

// Exact integer carriers: number must not be assignable where bigint literal is declared.
// @ts-expect-error number is not the bigint literal 262144n
export const numberLimit: P.Handshake1TypeScriptProtocolLimitsV1["maxStderrBytes"] = 262144;
export const bigintLimit: P.Handshake1TypeScriptProtocolLimitsV1["maxStderrBytes"] = 262144n;

// Stable table names: entrypoints whose schemas carry a title.
// @ts-expect-error provider entrypoint FactBatch3Root is not exported under its stable table name
export type ProviderFactBatch = P.FactBatch3Root;
// @ts-expect-error report catalogue root FactBatch3Root is not exported under its stable table name
export type ReportFactBatch = R.FactBatch3Root;
export type ReportFactBatchTitleName = R.FactBatchV3NegotiatedFactBatchPayloadWhenCapabilityTokenTargetAttributionV2IsPresent;
// Numeric deduplication suffix is what the provider union actually references.
export type DedupedLimits = P.Handshake1TypeScriptProtocolLimitsV11;
