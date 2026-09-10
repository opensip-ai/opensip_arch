// DRAFT reference design types. Not product code or a shipped SDK.
declare const hostWriteBrand: unique symbol;
declare const projectReadBrand: unique symbol;
export interface HostStateWriteHandle { readonly [hostWriteBrand]: never; }
export interface ProjectReadHandle { readonly [projectReadBrand]: never; }
export type DecisionClass = 'PR-1' | 'PR-2' | 'PR-3' | 'PR-4' | 'PR-5' | 'PR-6' | 'PR-7' | 'PR-8' | 'PR-9';
export type CommitClass = 'REVERSIBLE' | 'IRREVERSIBLE';
export interface EffectRefusal { readonly kind: 'REFUSED'; readonly decisionClass: DecisionClass; }
export interface EffectFailure { readonly kind: 'FAILED' | 'INDETERMINATE'; readonly commitClass: CommitClass; }
export interface WriteCompleted { readonly kind: 'COMPLETED'; readonly commitClass: CommitClass; }
export interface ReadCompleted { readonly kind: 'COMPLETED'; readonly bytes: Uint8Array; }
export interface BrokerEffects {
  readonly hostStateWriteHandles: readonly HostStateWriteHandle[];
  readonly projectReadHandles: readonly ProjectReadHandle[];
  writeHostState(handle: HostStateWriteHandle, bytes: Uint8Array): Promise<WriteCompleted | EffectFailure | EffectRefusal>;
  readProject(handle: ProjectReadHandle): Promise<ReadCompleted | EffectFailure | EffectRefusal>;
}
// Startup/local object misuse and protocol/courier faults reject the Promise
// through the existing SDK/provider-operability failure path. They are not RF
// messages, host outcomes, or permission denials invented by the SDK.
