//! D2b's selected release constants, borrowed by D4's independent output
//! check. These are not caller input or values copied out of a built Hello.
//! Owning controls pin the complete constant sets to the selected sources.
pub(crate) const TS2: [(&str, u64); 10] = [
    ("maxAnalyzeStages", 1024),
    ("maxCoverageEntriesPerFrame", 4096),
    ("maxFactBatchFacts", 4096),
    ("maxFactCandidatePayloadBytes", 1048576),
    ("maxFramePayloadBytes", 67108864),
    ("maxRelationsPerStage", 64),
    ("maxRequestedCoverageKeysPerStage", 128),
    ("maxSnapshotChunkBytes", 1048576),
    ("maxSnapshotEntries", 200000),
    ("maxStderrBytes", 262144),
];
/// Independent selected handshake authority for TS2 Hello and HelloAck.
/// This is protocol policy, never copied from either assembled codec output.
pub(crate) const TS2_IDENTITY_VERSIONS: [(&str, u64); 4] =
    [("coverage", 3), ("fact", 99), ("plan", 2), ("snapshot", 2)];
pub(crate) const RUST3: [(&str, u64); 32] = [
    ("cancellationGraceMilliseconds", 5000),
    ("maxAnalyzeStages", 256),
    ("maxCandidateSpoolBytes", 1073741824),
    ("maxCanonicalRelationPayloadBytes", 1048576),
    ("maxCfgSets", 4),
    ("maxCoverageEntriesPerFrame", 4096),
    ("maxDependencySourceChunkBytes", 1048576),
    ("maxDependencySourceEntries", 1000000),
    ("maxDependencySourcePackages", 4096),
    ("maxDependencySourceTotalBytes", 8589934592),
    ("maxExpansionRows", 1000000),
    ("maxFactBatchCandidates", 4096),
    ("maxFactCandidatesTotal", 1000000),
    ("maxFramePayloadBytes", 67108864),
    ("maxGeneratedFileRows", 1000000),
    ("maxPreparedOutputChunkBytes", 1048576),
    ("maxPreparedOutputEntries", 256),
    ("maxPreparedOutputTotalBlobBytes", 1073741824),
    ("maxRelationsPerStage", 64),
    ("maxRequestFrames", 1000000),
    ("maxRequestPayloadBytesTotal", 9663676416),
    ("maxRequestedCoverageKeysPerStage", 256),
    ("maxResponseFrames", 1000000),
    ("maxResponsePayloadBytesTotal", 1073741824),
    ("maxScratchBytes", 2147483648),
    ("maxSnapshotChunkBytes", 1048576),
    ("maxSnapshotEntries", 200000),
    ("maxSnapshotTotalFileBytes", 8589934592),
    ("maxStderrBytes", 262144),
    ("maxSubjectsPerStage", 256),
    ("maxUnresolvedEdgesPerStage", 1000000),
    ("normalExitGraceMilliseconds", 5000),
];

#[cfg(test)]
mod tests {
    use super::*;
    use opensip_identity::{JsonValue as J, parse_json};
    use std::collections::BTreeMap;

    #[test]
    fn release_limits_equal_all_and_only_selected_constant_schema_members() {
        let J::Object(root) = parse_json(include_bytes!(
            "../../../../schemas/sources/handshake-v1.schema.json"
        ))
        .unwrap() else {
            panic!()
        };
        let J::Object(defs) = &root["$defs"] else {
            panic!()
        };
        for name in ["TypeScriptHelloV2", "TypeScriptHelloAckV2"] {
            let J::Object(definition) = &defs[name] else {
                panic!()
            };
            let J::Object(properties) = &definition["properties"] else {
                panic!()
            };
            let J::Object(identity) = &properties["identityVersions"] else {
                panic!()
            };
            assert_eq!(
                identity["$ref"],
                J::String("#/$defs/IdentityVersionsV1".to_owned())
            );
            let J::Array(required) = &definition["required"] else {
                panic!()
            };
            assert!(required.contains(&J::String("identityVersions".to_owned())));
        }
        for (name, constants) in [
            ("TypeScriptProtocolLimitsV1", TS2.as_slice()),
            ("ProtocolLimitsV3", RUST3.as_slice()),
            ("IdentityVersionsV1", TS2_IDENTITY_VERSIONS.as_slice()),
        ] {
            let J::Object(definition) = &defs[name] else {
                panic!()
            };
            assert_eq!(definition["additionalProperties"], J::Bool(false));
            let J::Array(required) = &definition["required"] else {
                panic!()
            };
            let J::Object(properties) = &definition["properties"] else {
                panic!()
            };
            assert_eq!(required.len(), constants.len());
            assert_eq!(properties.len(), constants.len());
            let expected: BTreeMap<_, _> = constants.iter().copied().collect();
            assert_eq!(expected.len(), constants.len());
            for key in required {
                let J::String(key) = key else { panic!() };
                let J::Object(property) = &properties[key] else {
                    panic!()
                };
                let J::Integer(n) = &property["const"] else {
                    panic!()
                };
                assert_eq!(
                    Some(&u64::try_from(n.get()).unwrap()),
                    expected.get(key.as_str())
                );
            }
        }
    }
}
