# In-progress TypeScript configuration graph representation

Codex coauthor inspection, not independent acceptance. The new TypeScriptConfigGraphV1/node `extendsResolved` is a single nullable path and `typescript_config_origin` classifies jsconfig only when EVERY graph node is named jsconfig.json. These are additional representational concerns within blind G5/G10.

TypeScript supports an ordered array of base configurations in `extends`; later entries override earlier conflicting fields. A single resolved edge cannot preserve that input. [Official TypeScript 5.0 release notes](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-0.html#supporting-multiple-configuration-files-in-extends).

JavaScript projects use jsconfig.json as the project configuration, with JavaScript-related defaults; a project can be selected through an explicit configuration path. [Official project configuration documentation](https://www.typescriptlang.org/docs/handbook/tsconfig-json.html).

Inference for OpenSIP: retain the selected entry configuration explicitly, derive its origin from that entry, and retain ordered resolved extends edges per node. A JavaScript project's inheritance of a shared config with another filename should not change the selected entry's origin. Include positive mixed-name jsconfig inheritance and ordered multi-base inheritance; validate membership, source bytes, reachability and cycles under the declared read-graph law. This is a proposed contract correction for the coauthor to assess, not a claim that a real compiler was executed. Exact current files remain in-progress and no snapshot acceptance is asserted by this note.

## Codex final integration delta after retained Claude v3 handoff

The released native prose still described the earlier configOrigin/single-edge record; aligned it with the actual entryConfigPath/nodes/kind/ordered-edges schema. Removed uniqueItems from the extends sequence so repeated bases are represented without normalization. Explicitly selected custom config names now derive tsconfig instead of raising CONFIG_GRAPH_ENTRY_KIND. TypeScript documents --project accepting a path to a valid configuration JSON file: https://www.typescriptlang.org/docs/handbook/tsconfig-json.html. Three reference checks distinguish repeated entries, precedence and custom entry names. This is a Codex correction after the retained Claude source images, pending fresh actual independent review; the handoff is preserved unchanged.
