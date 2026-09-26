//! Generated exact private trust schema. Structural evidence only.
// SHA256 359345411d91585f76bbbad276b6bc2d774ba3e167aeb0bb2b70bfabb44d902f
use super::*;
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(in super::super) enum Definition {
    AbortTerminationAnnotationEventV1,
    AcceptedHeads,
    AcceptedMetadataHead,
    AcceptedRootHead,
    AcceptedStanding,
    Anchor,
    ArtifactCaptureObservationV1,
    BatchTerminationEventV1,
    BeginBatchV1,
    BlobRef,
    CapsuleAfterProjection,
    CapsuleImageV1,
    ClockInputV1,
    ClockPhase,
    ClockWriteEventV1,
    ClosureId,
    Consent,
    ContinuityEventV1,
    CoreAnchorNodeV1,
    CoreInventoryV2,
    CoreLogicalPath,
    CorePlatformV2,
    CoreProfileBindingV2,
    CreationEventV1,
    CreationInputV1,
    CreationStoreBindingV1,
    D9,
    DocRef,
    Effects,
    EmbeddedBootstrapV1,
    EnforcementV1,
    EventRef,
    ExecutionId,
    ExpiryStates,
    FileRef,
    Hex64,
    I64NonNegative,
    I64Positive,
    InstallationMutationReplayScopeV1,
    InstallationTransitionIntentV1,
    InvocationBinding,
    JournalRecord,
    JournalRecordV2,
    JournalState,
    LiveBatch,
    LogicalPath,
    MetadataAdmissionNodeV1,
    NamespaceList,
    NativeBefore,
    NodeRef,
    NullableD9,
    NullableString,
    NullableTimestamp,
    OperationInputV1,
    OriginalContextV1,
    P1Projection,
    PayloadEvidenceV1,
    PayloadMetadataClosureV1,
    PendingRecoveryChallenge,
    PlatformId,
    PrivateCeremonyTerminationEventV1,
    ProjectId,
    ProvenImageV1,
    PrunedTreeRowV2,
    PublicationDescriptorV1,
    PublicationEventV1,
    PublicationRef,
    RecoveryAction,
    RepairMaterialAbsence,
    RepairPlanId,
    RequestId,
    RestoreDeclarationInputV1,
    RestoreEventV1,
    RestoreProofV1,
    RestrictionEvidenceV1,
    RestrictionObservationInputV1,
    RetainedClockRecord,
    RetainedMemberV1,
    RevocationHistoryNodeV1,
    RevocationSubjectKindV1,
    RevocationSubjectV1,
    RoleChangeV1,
    RoleEventV1,
    RoleRecordV1,
    RoleToken,
    RootAdmissionNodeV1,
    RootBinding,
    RootRole,
    S45ChallengeInputV1,
    S45EpochInputV1,
    S4EvaluationInput,
    S4EvaluationInputV1,
    S4EvaluationInputV2,
    SignedMemberPath,
    SignedTimeSourceV1,
    SixRoleRecords,
    SnapshotId,
    SourceFence,
    StagedPayload,
    StandingResetEventV1,
    StateSchema,
    StateToken,
    StepId,
    StoreBinding,
    StoreId,
    StoreMarkerV1,
    StringList,
    TargetAbsenceInputV1,
    TcbProfileTemplateV1,
    TimeEvidenceV1,
    TimeInputV1,
    Timestamp,
    TransitionIntentInputV1,
    TransitionOperation,
    TransitionRefusal,
    TransitionSlotObservationV1,
    TreeCommitment,
    TreeEntry,
    TrustAdmissionInputV1,
    TrustCapsuleV1,
    TrustCommandOutcomeV1,
    TrustEventV1,
    TrustFloors,
    TrustMutationReceiptV1,
    V14Event,
    V14Refusal,
    WalkRecord,
    CoreInventoryV3,
    CorePlatformV3,
}
impl Definition {
    #[cfg(test)]
    pub(super) fn named(s: &str) -> Option<Self> {
        match s {
            "AbortTerminationAnnotationEventV1" => Some(Self::AbortTerminationAnnotationEventV1),
            "AcceptedHeads" => Some(Self::AcceptedHeads),
            "AcceptedMetadataHead" => Some(Self::AcceptedMetadataHead),
            "AcceptedRootHead" => Some(Self::AcceptedRootHead),
            "AcceptedStanding" => Some(Self::AcceptedStanding),
            "Anchor" => Some(Self::Anchor),
            "ArtifactCaptureObservationV1" => Some(Self::ArtifactCaptureObservationV1),
            "BatchTerminationEventV1" => Some(Self::BatchTerminationEventV1),
            "BeginBatchV1" => Some(Self::BeginBatchV1),
            "BlobRef" => Some(Self::BlobRef),
            "CapsuleAfterProjection" => Some(Self::CapsuleAfterProjection),
            "CapsuleImageV1" => Some(Self::CapsuleImageV1),
            "ClockInputV1" => Some(Self::ClockInputV1),
            "ClockPhase" => Some(Self::ClockPhase),
            "ClockWriteEventV1" => Some(Self::ClockWriteEventV1),
            "ClosureId" => Some(Self::ClosureId),
            "Consent" => Some(Self::Consent),
            "ContinuityEventV1" => Some(Self::ContinuityEventV1),
            "CoreAnchorNodeV1" => Some(Self::CoreAnchorNodeV1),
            "CoreInventoryV2" => Some(Self::CoreInventoryV2),
            "CoreLogicalPath" => Some(Self::CoreLogicalPath),
            "CorePlatformV2" => Some(Self::CorePlatformV2),
            "CoreProfileBindingV2" => Some(Self::CoreProfileBindingV2),
            "CreationEventV1" => Some(Self::CreationEventV1),
            "CreationInputV1" => Some(Self::CreationInputV1),
            "CreationStoreBindingV1" => Some(Self::CreationStoreBindingV1),
            "D9" => Some(Self::D9),
            "DocRef" => Some(Self::DocRef),
            "Effects" => Some(Self::Effects),
            "EmbeddedBootstrapV1" => Some(Self::EmbeddedBootstrapV1),
            "EnforcementV1" => Some(Self::EnforcementV1),
            "EventRef" => Some(Self::EventRef),
            "ExecutionId" => Some(Self::ExecutionId),
            "ExpiryStates" => Some(Self::ExpiryStates),
            "FileRef" => Some(Self::FileRef),
            "Hex64" => Some(Self::Hex64),
            "I64NonNegative" => Some(Self::I64NonNegative),
            "I64Positive" => Some(Self::I64Positive),
            "InstallationMutationReplayScopeV1" => Some(Self::InstallationMutationReplayScopeV1),
            "InstallationTransitionIntentV1" => Some(Self::InstallationTransitionIntentV1),
            "InvocationBinding" => Some(Self::InvocationBinding),
            "JournalRecord" => Some(Self::JournalRecord),
            "JournalRecordV2" => Some(Self::JournalRecordV2),
            "JournalState" => Some(Self::JournalState),
            "LiveBatch" => Some(Self::LiveBatch),
            "LogicalPath" => Some(Self::LogicalPath),
            "MetadataAdmissionNodeV1" => Some(Self::MetadataAdmissionNodeV1),
            "NamespaceList" => Some(Self::NamespaceList),
            "NativeBefore" => Some(Self::NativeBefore),
            "NodeRef" => Some(Self::NodeRef),
            "NullableD9" => Some(Self::NullableD9),
            "NullableString" => Some(Self::NullableString),
            "NullableTimestamp" => Some(Self::NullableTimestamp),
            "OperationInputV1" => Some(Self::OperationInputV1),
            "OriginalContextV1" => Some(Self::OriginalContextV1),
            "P1Projection" => Some(Self::P1Projection),
            "PayloadEvidenceV1" => Some(Self::PayloadEvidenceV1),
            "PayloadMetadataClosureV1" => Some(Self::PayloadMetadataClosureV1),
            "PendingRecoveryChallenge" => Some(Self::PendingRecoveryChallenge),
            "PlatformId" => Some(Self::PlatformId),
            "PrivateCeremonyTerminationEventV1" => Some(Self::PrivateCeremonyTerminationEventV1),
            "ProjectId" => Some(Self::ProjectId),
            "ProvenImageV1" => Some(Self::ProvenImageV1),
            "PrunedTreeRowV2" => Some(Self::PrunedTreeRowV2),
            "PublicationDescriptorV1" => Some(Self::PublicationDescriptorV1),
            "PublicationEventV1" => Some(Self::PublicationEventV1),
            "PublicationRef" => Some(Self::PublicationRef),
            "RecoveryAction" => Some(Self::RecoveryAction),
            "RepairMaterialAbsence" => Some(Self::RepairMaterialAbsence),
            "RepairPlanId" => Some(Self::RepairPlanId),
            "RequestId" => Some(Self::RequestId),
            "RestoreDeclarationInputV1" => Some(Self::RestoreDeclarationInputV1),
            "RestoreEventV1" => Some(Self::RestoreEventV1),
            "RestoreProofV1" => Some(Self::RestoreProofV1),
            "RestrictionEvidenceV1" => Some(Self::RestrictionEvidenceV1),
            "RestrictionObservationInputV1" => Some(Self::RestrictionObservationInputV1),
            "RetainedClockRecord" => Some(Self::RetainedClockRecord),
            "RetainedMemberV1" => Some(Self::RetainedMemberV1),
            "RevocationHistoryNodeV1" => Some(Self::RevocationHistoryNodeV1),
            "RevocationSubjectKindV1" => Some(Self::RevocationSubjectKindV1),
            "RevocationSubjectV1" => Some(Self::RevocationSubjectV1),
            "RoleChangeV1" => Some(Self::RoleChangeV1),
            "RoleEventV1" => Some(Self::RoleEventV1),
            "RoleRecordV1" => Some(Self::RoleRecordV1),
            "RoleToken" => Some(Self::RoleToken),
            "RootAdmissionNodeV1" => Some(Self::RootAdmissionNodeV1),
            "RootBinding" => Some(Self::RootBinding),
            "RootRole" => Some(Self::RootRole),
            "S45ChallengeInputV1" => Some(Self::S45ChallengeInputV1),
            "S45EpochInputV1" => Some(Self::S45EpochInputV1),
            "S4EvaluationInput" => Some(Self::S4EvaluationInput),
            "S4EvaluationInputV1" => Some(Self::S4EvaluationInputV1),
            "S4EvaluationInputV2" => Some(Self::S4EvaluationInputV2),
            "SignedMemberPath" => Some(Self::SignedMemberPath),
            "SignedTimeSourceV1" => Some(Self::SignedTimeSourceV1),
            "SixRoleRecords" => Some(Self::SixRoleRecords),
            "SnapshotId" => Some(Self::SnapshotId),
            "SourceFence" => Some(Self::SourceFence),
            "StagedPayload" => Some(Self::StagedPayload),
            "StandingResetEventV1" => Some(Self::StandingResetEventV1),
            "StateSchema" => Some(Self::StateSchema),
            "StateToken" => Some(Self::StateToken),
            "StepId" => Some(Self::StepId),
            "StoreBinding" => Some(Self::StoreBinding),
            "StoreId" => Some(Self::StoreId),
            "StoreMarkerV1" => Some(Self::StoreMarkerV1),
            "StringList" => Some(Self::StringList),
            "TargetAbsenceInputV1" => Some(Self::TargetAbsenceInputV1),
            "TcbProfileTemplateV1" => Some(Self::TcbProfileTemplateV1),
            "TimeEvidenceV1" => Some(Self::TimeEvidenceV1),
            "TimeInputV1" => Some(Self::TimeInputV1),
            "Timestamp" => Some(Self::Timestamp),
            "TransitionIntentInputV1" => Some(Self::TransitionIntentInputV1),
            "TransitionOperation" => Some(Self::TransitionOperation),
            "TransitionRefusal" => Some(Self::TransitionRefusal),
            "TransitionSlotObservationV1" => Some(Self::TransitionSlotObservationV1),
            "TreeCommitment" => Some(Self::TreeCommitment),
            "TreeEntry" => Some(Self::TreeEntry),
            "TrustAdmissionInputV1" => Some(Self::TrustAdmissionInputV1),
            "TrustCapsuleV1" => Some(Self::TrustCapsuleV1),
            "TrustCommandOutcomeV1" => Some(Self::TrustCommandOutcomeV1),
            "TrustEventV1" => Some(Self::TrustEventV1),
            "TrustFloors" => Some(Self::TrustFloors),
            "TrustMutationReceiptV1" => Some(Self::TrustMutationReceiptV1),
            "V14Event" => Some(Self::V14Event),
            "V14Refusal" => Some(Self::V14Refusal),
            "WalkRecord" => Some(Self::WalkRecord),
            "CoreInventoryV3" => Some(Self::CoreInventoryV3),
            "CorePlatformV3" => Some(Self::CorePlatformV3),
            _ => None,
        }
    }
}
pub(super) fn shape(definition: Definition, v: &V) -> bool {
    match definition {
        Definition::AbortTerminationAnnotationEventV1 => node_1(v),
        Definition::AcceptedHeads => node_15(v),
        Definition::AcceptedMetadataHead => node_18(v),
        Definition::AcceptedRootHead => node_20(v),
        Definition::AcceptedStanding => node_22(v),
        Definition::Anchor => node_26(v),
        Definition::ArtifactCaptureObservationV1 => node_30(v),
        Definition::BatchTerminationEventV1 => node_33(v),
        Definition::BeginBatchV1 => node_37(v),
        Definition::BlobRef => node_42(v),
        Definition::CapsuleAfterProjection => node_45(v),
        Definition::CapsuleImageV1 => node_58(v),
        Definition::ClockInputV1 => node_59(v),
        Definition::ClockPhase => node_67(v),
        Definition::ClockWriteEventV1 => node_76(v),
        Definition::ClosureId => node_114(v),
        Definition::Consent => node_115(v),
        Definition::ContinuityEventV1 => node_118(v),
        Definition::CoreAnchorNodeV1 => node_128(v),
        Definition::CoreInventoryV2 => node_132(v),
        Definition::CoreLogicalPath => node_143(v),
        Definition::CorePlatformV2 => node_145(v),
        Definition::CoreProfileBindingV2 => node_154(v),
        Definition::CreationEventV1 => node_156(v),
        Definition::CreationInputV1 => node_158(v),
        Definition::CreationStoreBindingV1 => node_163(v),
        Definition::D9 => node_166(v),
        Definition::DocRef => node_170(v),
        Definition::Effects => node_172(v),
        Definition::EmbeddedBootstrapV1 => node_174(v),
        Definition::EnforcementV1 => node_176(v),
        Definition::EventRef => node_177(v),
        Definition::ExecutionId => node_179(v),
        Definition::ExpiryStates => node_180(v),
        Definition::FileRef => node_181(v),
        Definition::Hex64 => node_182(v),
        Definition::I64NonNegative => node_183(v),
        Definition::I64Positive => node_178(v),
        Definition::InstallationMutationReplayScopeV1 => node_184(v),
        Definition::InstallationTransitionIntentV1 => node_189(v),
        Definition::InvocationBinding => node_192(v),
        Definition::JournalRecord => node_193(v),
        Definition::JournalRecordV2 => node_202(v),
        Definition::JournalState => node_204(v),
        Definition::LiveBatch => node_205(v),
        Definition::LogicalPath => node_209(v),
        Definition::MetadataAdmissionNodeV1 => node_210(v),
        Definition::NamespaceList => node_213(v),
        Definition::NativeBefore => node_215(v),
        Definition::NodeRef => node_42(v),
        Definition::NullableD9 => node_216(v),
        Definition::NullableString => node_218(v),
        Definition::NullableTimestamp => node_219(v),
        Definition::OperationInputV1 => node_220(v),
        Definition::OriginalContextV1 => node_268(v),
        Definition::P1Projection => node_269(v),
        Definition::PayloadEvidenceV1 => node_271(v),
        Definition::PayloadMetadataClosureV1 => node_274(v),
        Definition::PendingRecoveryChallenge => node_287(v),
        Definition::PlatformId => node_288(v),
        Definition::PrivateCeremonyTerminationEventV1 => node_289(v),
        Definition::ProjectId => node_294(v),
        Definition::ProvenImageV1 => node_295(v),
        Definition::PrunedTreeRowV2 => node_296(v),
        Definition::PublicationDescriptorV1 => node_305(v),
        Definition::PublicationEventV1 => node_311(v),
        Definition::PublicationRef => node_314(v),
        Definition::RecoveryAction => node_315(v),
        Definition::RepairMaterialAbsence => node_316(v),
        Definition::RepairPlanId => node_319(v),
        Definition::RequestId => node_320(v),
        Definition::RestoreDeclarationInputV1 => node_321(v),
        Definition::RestoreEventV1 => node_326(v),
        Definition::RestoreProofV1 => node_332(v),
        Definition::RestrictionEvidenceV1 => node_336(v),
        Definition::RestrictionObservationInputV1 => node_344(v),
        Definition::RetainedClockRecord => node_347(v),
        Definition::RetainedMemberV1 => node_350(v),
        Definition::RevocationHistoryNodeV1 => node_352(v),
        Definition::RevocationSubjectKindV1 => node_358(v),
        Definition::RevocationSubjectV1 => node_27(v),
        Definition::RoleChangeV1 => node_359(v),
        Definition::RoleEventV1 => node_360(v),
        Definition::RoleRecordV1 => node_384(v),
        Definition::RoleToken => node_392(v),
        Definition::RootAdmissionNodeV1 => node_393(v),
        Definition::RootBinding => node_399(v),
        Definition::RootRole => node_402(v),
        Definition::S45ChallengeInputV1 => node_407(v),
        Definition::S45EpochInputV1 => node_408(v),
        Definition::S4EvaluationInput => node_410(v),
        Definition::S4EvaluationInputV1 => node_413(v),
        Definition::S4EvaluationInputV2 => node_416(v),
        Definition::SignedMemberPath => node_417(v),
        Definition::SignedTimeSourceV1 => node_418(v),
        Definition::SixRoleRecords => node_423(v),
        Definition::SnapshotId => node_424(v),
        Definition::SourceFence => node_425(v),
        Definition::StagedPayload => node_426(v),
        Definition::StandingResetEventV1 => node_427(v),
        Definition::StateSchema => node_429(v),
        Definition::StateToken => node_430(v),
        Definition::StepId => node_431(v),
        Definition::StoreBinding => node_432(v),
        Definition::StoreId => node_161(v),
        Definition::StoreMarkerV1 => node_433(v),
        Definition::StringList => node_434(v),
        Definition::TargetAbsenceInputV1 => node_435(v),
        Definition::TcbProfileTemplateV1 => node_437(v),
        Definition::TimeEvidenceV1 => node_496(v),
        Definition::TimeInputV1 => node_499(v),
        Definition::Timestamp => node_502(v),
        Definition::TransitionIntentInputV1 => node_503(v),
        Definition::TransitionOperation => node_504(v),
        Definition::TransitionRefusal => node_505(v),
        Definition::TransitionSlotObservationV1 => node_506(v),
        Definition::TreeCommitment => node_507(v),
        Definition::TreeEntry => node_510(v),
        Definition::TrustAdmissionInputV1 => node_518(v),
        Definition::TrustCapsuleV1 => node_526(v),
        Definition::TrustCommandOutcomeV1 => node_527(v),
        Definition::TrustEventV1 => node_531(v),
        Definition::TrustFloors => node_541(v),
        Definition::TrustMutationReceiptV1 => node_543(v),
        Definition::V14Event => node_549(v),
        Definition::V14Refusal => node_550(v),
        Definition::WalkRecord => node_551(v),
        Definition::CoreInventoryV3 => node_555(v),
        Definition::CorePlatformV3 => node_559(v),
    }
}
fn node_0(_v: &V) -> bool {
    true
}
fn node_1(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("abort").is_some_and(node_3)
                    && o.get("batch").is_some_and(node_4)
                    && o.get("eventSchema").is_some_and(node_5)
                    && o.get("from").is_some_and(node_6)
                    && o.get("kind").is_some_and(node_7)
                    && o.get("operation").is_some_and(node_4)
                    && o.get("previous").is_some_and(node_8)
                    && o.get("reason").is_some_and(node_10)
                    && o.get("role").is_some_and(node_11)
                    && o.get("sequence").is_some_and(node_12)
                    && o.get("store").is_some_and(node_13)
                    && o.get("to").is_some_and(node_14)
                    && o.keys().all(|k| {
                        [
                            "abort",
                            "batch",
                            "eventSchema",
                            "from",
                            "kind",
                            "operation",
                            "previous",
                            "reason",
                            "role",
                            "sequence",
                            "store",
                            "to",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_2(_v: &V) -> bool {
    false
}
fn node_3(v: &V) -> bool {
    node_177(v)
}
fn node_4(v: &V) -> bool {
    node_42(v)
}
fn node_5(v: &V) -> bool {
    matches!(v, V::Integer(n) if n.get() == 1_i128)
}
fn node_6(v: &V) -> bool {
    matches!(v, V::String(s) if s == "ST-RECOVERY")
}
fn node_7(v: &V) -> bool {
    matches!(v, V::String(s) if s == "abort-termination-annotation")
}
fn node_8(v: &V) -> bool {
    (usize::from(node_3(v)) + usize::from(node_9(v))) == 1
}
fn node_9(v: &V) -> bool {
    matches!(v, V::Null)
}
fn node_10(v: &V) -> bool {
    matches!(v, V::String(s) if s == "RECOVERY-ABORTED")
}
fn node_11(v: &V) -> bool {
    node_392(v)
}
fn node_12(v: &V) -> bool {
    node_178(v)
}
fn node_13(v: &V) -> bool {
    node_161(v)
}
fn node_14(v: &V) -> bool {
    matches!(v, V::String(s) if s == "ST-REVOKED")
        || matches!(v, V::String(s) if s == "ST-QUORUM-LOST")
        || matches!(v, V::String(s) if s == "ST-EXPIRED")
        || matches!(v, V::String(s) if s == "ST-STALE-REVOCATION")
        || matches!(v, V::String(s) if s == "ST-UNBOOTSTRAPPED")
}
fn node_15(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("catalog").is_some_and(node_16)
                    && o.get("revocation").is_some_and(node_16)
                    && o.get("root").is_some_and(node_17)
                    && o.keys()
                        .all(|k| ["catalog", "revocation", "root"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_16(v: &V) -> bool {
    node_18(v)
}
fn node_17(v: &V) -> bool {
    node_20(v)
}
fn node_18(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("admission").is_some_and(node_4)
                    && o.get("document").is_some_and(node_19)
                    && o.get("version").is_some_and(node_12)
                    && o.keys()
                        .all(|k| ["admission", "document", "version"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_19(v: &V) -> bool {
    node_170(v)
}
fn node_20(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("admission").is_some_and(node_4)
                    && o.get("binding").is_some_and(node_21)
                    && o.get("document").is_some_and(node_19)
                    && o.keys()
                        .all(|k| ["admission", "binding", "document"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_21(v: &V) -> bool {
    node_399(v)
}
fn node_22(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("by").is_some_and(node_3)
                    && o.get("catalog").is_some_and(node_23)
                    && o.get("namespaces").is_some_and(node_24)
                    && o.get("root").is_some_and(node_21)
                    && o.get("rootAdmission").is_some_and(node_4)
                    && o.keys().all(|k| {
                        ["by", "catalog", "namespaces", "root", "rootAdmission"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_23(v: &V) -> bool {
    (usize::from(node_19(v)) + usize::from(node_9(v))) == 1
}
fn node_24(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => a.len() <= 16 && unique(a) && a.iter().all(node_25) && ordered(a, &[]),
            _ => true,
        })
}
fn node_25(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => s.chars().count() >= 1 && s.chars().count() <= 4194304 && token(s),
            _ => true,
        })
}
fn node_26(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("bootId").is_some_and(node_27)
                    && o.get("mono").is_some_and(node_28)
                    && o.get("wall").is_some_and(node_29)
                    && o.keys()
                        .all(|k| ["bootId", "mono", "wall"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_27(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => s.chars().count() >= 1 && s.chars().count() <= 256,
            _ => true,
        })
}
fn node_28(v: &V) -> bool {
    node_183(v)
}
fn node_29(v: &V) -> bool {
    node_502(v)
}
fn node_30(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("observedBytes").is_some_and(node_28)
                    && o.get("path").is_some_and(node_31)
                    && o.get("sha256").is_some_and(node_32)
                    && o.keys()
                        .all(|k| ["observedBytes", "path", "sha256"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_31(v: &V) -> bool {
    node_417(v)
}
fn node_32(v: &V) -> bool {
    node_182(v)
}
fn node_33(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("batch").is_some_and(node_4)
                    && o.get("cause").is_some_and(node_34)
                    && o.get("closing").is_some_and(node_35)
                    && o.get("eventSchema").is_some_and(node_5)
                    && o.get("kind").is_some_and(node_36)
                    && o.get("operation").is_some_and(node_4)
                    && o.get("previous").is_some_and(node_8)
                    && o.get("sequence").is_some_and(node_12)
                    && o.get("store").is_some_and(node_13)
                    && o.keys().all(|k| {
                        [
                            "batch",
                            "cause",
                            "closing",
                            "eventSchema",
                            "kind",
                            "operation",
                            "previous",
                            "sequence",
                            "store",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_34(v: &V) -> bool {
    matches!(v, V::String(s) if s == "INTERRUPTED")
        || matches!(v, V::String(s) if s == "ABORTED")
        || matches!(v, V::String(s) if s == "COMMITTED")
        || matches!(v, V::String(s) if s == "ROOT_CHANGED")
        || matches!(v, V::String(s) if s == "MIGRATED")
        || matches!(v, V::String(s) if s == "RESTORED")
}
fn node_35(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => !a.is_empty() && a.len() <= 6 && a.iter().all(node_3),
            _ => true,
        })
}
fn node_36(v: &V) -> bool {
    matches!(v, V::String(s) if s == "batch-termination")
}
fn node_37(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("authority").is_some_and(node_21)
                    && o.get("authorization").is_some_and(node_19)
                    && o.get("batchSchema").is_some_and(node_38)
                    && o.get("beforeRoles").is_some_and(node_39)
                    && o.get("beginEvents").is_some_and(node_40)
                    && o.get("closure").is_some_and(node_4)
                    && o.get("payload").is_some_and(node_19)
                    && o.get("replacement").is_some_and(node_21)
                    && o.get("selected").is_some_and(node_41)
                    && o.keys().all(|k| {
                        [
                            "authority",
                            "authorization",
                            "batchSchema",
                            "beforeRoles",
                            "beginEvents",
                            "closure",
                            "payload",
                            "replacement",
                            "selected",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_38(v: &V) -> bool {
    (matches!(v, V::Integer(_))) && (matches!(v, V::Integer(n) if n.get() == 1_i128))
}
fn node_39(v: &V) -> bool {
    node_423(v)
}
fn node_40(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("TR-BUNDLE").is_none_or(node_3)
                    && o.get("TR-COMPONENT").is_none_or(node_3)
                    && o.get("TR-CORE").is_none_or(node_3)
                    && o.get("TR-INDEX").is_none_or(node_3)
                    && o.get("TR-PROFILE").is_none_or(node_3)
                    && o.get("TR-REPAIR").is_none_or(node_3)
                    && o.keys().all(|k| {
                        [
                            "TR-BUNDLE",
                            "TR-COMPONENT",
                            "TR-CORE",
                            "TR-INDEX",
                            "TR-PROFILE",
                            "TR-REPAIR",
                        ]
                        .contains(&k.as_str())
                    })
                    && !o.is_empty()
            }
            _ => true,
        })
}
fn node_41(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => {
                !a.is_empty()
                    && a.len() <= 6
                    && unique(a)
                    && a.iter().all(node_11)
                    && ordered(a, &[])
            }
            _ => true,
        })
}
fn node_42(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("bytes").is_some_and(node_43)
                    && o.get("sha256").is_some_and(node_44)
                    && o.keys().all(|k| ["bytes", "sha256"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_43(v: &V) -> bool {
    (matches!(v, V::Integer(_)))
        && (match v {
            V::Integer(n) => n.get() >= 1_i128 && n.get() <= 4194304_i128,
            _ => true,
        })
}
fn node_44(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => hex(s, 64),
            _ => true,
        })
}
fn node_45(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("batch").is_some_and(node_46)
                    && o.get("capsuleSchema").is_some_and(node_38)
                    && o.get("clock").is_some_and(node_48)
                    && o.get("eventHead").is_some_and(node_8)
                    && o.get("heads").is_some_and(node_49)
                    && o.get("history").is_some_and(node_51)
                    && o.get("previous").is_some_and(node_52)
                    && o.get("revision").is_some_and(node_12)
                    && o.get("roles").is_some_and(node_39)
                    && o.get("sourceFence").is_some_and(node_53)
                    && o.get("staged").is_some_and(node_55)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        [
                            "batch",
                            "capsuleSchema",
                            "clock",
                            "eventHead",
                            "heads",
                            "history",
                            "previous",
                            "revision",
                            "roles",
                            "sourceFence",
                            "staged",
                            "store",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_46(v: &V) -> bool {
    (usize::from(node_47(v)) + usize::from(node_9(v))) == 1
}
fn node_47(v: &V) -> bool {
    node_205(v)
}
fn node_48(v: &V) -> bool {
    node_67(v)
}
fn node_49(v: &V) -> bool {
    (usize::from(node_50(v)) + usize::from(node_9(v))) == 1
}
fn node_50(v: &V) -> bool {
    node_15(v)
}
fn node_51(v: &V) -> bool {
    (usize::from(node_4(v)) + usize::from(node_9(v))) == 1
}
fn node_52(v: &V) -> bool {
    (usize::from(node_32(v)) + usize::from(node_9(v))) == 1
}
fn node_53(v: &V) -> bool {
    (usize::from(node_54(v)) + usize::from(node_9(v))) == 1
}
fn node_54(v: &V) -> bool {
    node_425(v)
}
fn node_55(v: &V) -> bool {
    (usize::from(node_56(v)) + usize::from(node_9(v))) == 1
}
fn node_56(v: &V) -> bool {
    node_426(v)
}
fn node_57(v: &V) -> bool {
    node_432(v)
}
fn node_58(v: &V) -> bool {
    node_526(v)
}
fn node_59(v: &V) -> bool {
    (usize::from(node_60(v)) + usize::from(node_62(v)) + usize::from(node_65(v))) == 1
}
fn node_60(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("by").is_some_and(node_3)
                    && o.get("kind").is_some_and(node_61)
                    && o.keys().all(|k| ["by", "kind"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_61(v: &V) -> bool {
    matches!(v, V::String(s) if s == "clock-write")
}
fn node_62(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("kind").is_some_and(node_63)
                    && o.get("reason").is_some_and(node_64)
                    && o.keys().all(|k| ["kind", "reason"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_63(v: &V) -> bool {
    matches!(v, V::String(s) if s == "not-required")
}
fn node_64(v: &V) -> bool {
    matches!(v, V::String(s) if s == "pregenesis-abort-no-time-cause")
}
fn node_65(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("input").is_some_and(node_4)
                    && o.get("kind").is_some_and(node_66)
                    && o.keys().all(|k| ["input", "kind"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_66(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "observed-context"))
}
fn node_67(v: &V) -> bool {
    (usize::from(node_68(v)) + usize::from(node_70(v)) + usize::from(node_73(v))) == 1
}
fn node_68(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("phase").is_some_and(node_69)
                    && o.keys().all(|k| ["phase"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_69(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "unevaluated"))
}
fn node_70(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("phase").is_some_and(node_71)
                    && o.get("projection").is_some_and(node_72)
                    && o.get("timeEvidence").is_some_and(node_4)
                    && o.keys()
                        .all(|k| ["phase", "projection", "timeEvidence"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_71(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "evaluated"))
}
fn node_72(v: &V) -> bool {
    node_269(v)
}
fn node_73(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("phase").is_some_and(node_74)
                    && o.get("record").is_some_and(node_75)
                    && o.get("timeEvidence").is_some_and(node_4)
                    && o.keys()
                        .all(|k| ["phase", "record", "timeEvidence"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_74(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "retained"))
}
fn node_75(v: &V) -> bool {
    node_347(v)
}
fn node_76(v: &V) -> bool {
    (usize::from(node_77(v)) + usize::from(node_108(v)) + usize::from(node_111(v))) == 1
}
fn node_77(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (node_78(v) && node_84(v) && node_94(v))
        && (match v {
            V::Object(o) => {
                o.get("evaluation").is_some_and(node_4)
                    && o.get("eventSchema").is_some_and(node_5)
                    && o.get("kind").is_some_and(node_61)
                    && o.get("operation").is_some_and(node_4)
                    && o.get("phaseAfter").is_some_and(node_97)
                    && o.get("phaseBefore").is_some_and(node_98)
                    && o.get("previous").is_some_and(node_8)
                    && o.get("sequence").is_some_and(node_12)
                    && o.get("source").is_some_and(node_99)
                    && o.get("store").is_some_and(node_13)
                    && o.get("timeEvidence").is_some_and(node_100)
                    && o.get("writes").is_some_and(node_105)
                    && o.keys().all(|k| {
                        [
                            "evaluation",
                            "eventSchema",
                            "kind",
                            "operation",
                            "phaseAfter",
                            "phaseBefore",
                            "previous",
                            "sequence",
                            "source",
                            "store",
                            "timeEvidence",
                            "writes",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_78(v: &V) -> bool {
    if node_81(v) { node_83(v) } else { node_79(v) }
}
fn node_79(v: &V) -> bool {
    match v {
        V::Object(o) => o.get("phaseAfter").is_none_or(node_80),
        _ => true,
    }
}
fn node_80(v: &V) -> bool {
    matches!(v, V::String(s) if s == "evaluated")
}
fn node_81(v: &V) -> bool {
    match v {
        V::Object(o) => o.get("phaseBefore").is_none_or(node_82),
        _ => true,
    }
}
fn node_82(v: &V) -> bool {
    matches!(v, V::String(s) if s == "retained")
}
fn node_83(v: &V) -> bool {
    match v {
        V::Object(o) => o.get("phaseAfter").is_none_or(node_82),
        _ => true,
    }
}
fn node_84(v: &V) -> bool {
    if node_88(v) { node_91(v) } else { node_85(v) }
}
fn node_85(v: &V) -> bool {
    match v {
        V::Object(o) => o.get("timeEvidence").is_none_or(node_86),
        _ => true,
    }
}
fn node_86(v: &V) -> bool {
    match v {
        V::Object(o) => o.get("kind").is_none_or(node_87),
        _ => true,
    }
}
fn node_87(v: &V) -> bool {
    matches!(v, V::String(s) if s == "kept")
}
fn node_88(v: &V) -> bool {
    match v {
        V::Object(o) => o.get("writes").is_none_or(node_89),
        _ => true,
    }
}
fn node_89(v: &V) -> bool {
    match v {
        V::Array(a) => a.iter().any(node_90),
        _ => true,
    }
}
fn node_90(v: &V) -> bool {
    matches!(v, V::String(s) if s == "lastAccepted")
}
fn node_91(v: &V) -> bool {
    match v {
        V::Object(o) => o.get("timeEvidence").is_none_or(node_92),
        _ => true,
    }
}
fn node_92(v: &V) -> bool {
    match v {
        V::Object(o) => o.get("kind").is_none_or(node_93),
        _ => true,
    }
}
fn node_93(v: &V) -> bool {
    matches!(v, V::String(s) if s == "new")
}
fn node_94(v: &V) -> bool {
    if node_95(v) { node_88(v) } else { true }
}
fn node_95(v: &V) -> bool {
    match v {
        V::Object(o) => o.get("phaseBefore").is_none_or(node_96),
        _ => true,
    }
}
fn node_96(v: &V) -> bool {
    matches!(v, V::String(s) if s == "unevaluated")
}
fn node_97(v: &V) -> bool {
    matches!(v, V::String(s) if s == "evaluated") || matches!(v, V::String(s) if s == "retained")
}
fn node_98(v: &V) -> bool {
    matches!(v, V::String(s) if s == "unevaluated")
        || matches!(v, V::String(s) if s == "evaluated")
        || matches!(v, V::String(s) if s == "retained")
}
fn node_99(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "s4"))
}
fn node_100(v: &V) -> bool {
    (usize::from(node_101(v)) + usize::from(node_103(v))) == 1
}
fn node_101(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("kind").is_some_and(node_102)
                    && o.keys().all(|k| ["kind"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_102(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "kept"))
}
fn node_103(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("kind").is_some_and(node_104)
                    && o.get("proof").is_some_and(node_4)
                    && o.keys().all(|k| ["kind", "proof"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_104(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "new"))
}
fn node_105(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => {
                !a.is_empty()
                    && a.len() <= 3
                    && unique(a)
                    && a.iter().all(node_107)
                    && a.iter().any(node_106)
                    && ordered(a, &[])
            }
            _ => true,
        })
}
fn node_106(v: &V) -> bool {
    matches!(v, V::String(s) if s == "evalHighWater")
}
fn node_107(v: &V) -> bool {
    matches!(v, V::String(s) if s == "anchor")
        || matches!(v, V::String(s) if s == "evalHighWater")
        || matches!(v, V::String(s) if s == "lastAccepted")
}
fn node_108(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("evaluation").is_some_and(node_4)
                    && o.get("eventSchema").is_some_and(node_5)
                    && o.get("kind").is_some_and(node_61)
                    && o.get("operation").is_some_and(node_4)
                    && o.get("phaseAfter").is_some_and(node_74)
                    && o.get("phaseBefore").is_some_and(node_74)
                    && o.get("previous").is_some_and(node_8)
                    && o.get("sequence").is_some_and(node_12)
                    && o.get("source").is_some_and(node_109)
                    && o.get("store").is_some_and(node_13)
                    && o.get("timeEvidence").is_some_and(node_103)
                    && o.get("writes").is_some_and(node_110)
                    && o.keys().all(|k| {
                        [
                            "evaluation",
                            "eventSchema",
                            "kind",
                            "operation",
                            "phaseAfter",
                            "phaseBefore",
                            "previous",
                            "sequence",
                            "source",
                            "store",
                            "timeEvidence",
                            "writes",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_109(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "s4.5-apply"))
}
fn node_110(v: &V) -> bool {
    matches!(v, V::Array(a) if a.len() == 5 && matches!(&a[0], V::String(s) if s == "anchor") && matches!(&a[1], V::String(s) if s == "evalHighWater") && matches!(&a[2], V::String(s) if s == "lastAccepted") && matches!(&a[3], V::String(s) if s == "pendingRecoveryChallenge") && matches!(&a[4], V::String(s) if s == "recoveryEpochSerial"))
}
fn node_111(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("evaluation").is_some_and(node_4)
                    && o.get("eventSchema").is_some_and(node_5)
                    && o.get("kind").is_some_and(node_61)
                    && o.get("operation").is_some_and(node_4)
                    && o.get("phaseAfter").is_some_and(node_74)
                    && o.get("phaseBefore").is_some_and(node_74)
                    && o.get("previous").is_some_and(node_8)
                    && o.get("sequence").is_some_and(node_12)
                    && o.get("source").is_some_and(node_112)
                    && o.get("store").is_some_and(node_13)
                    && o.get("timeEvidence").is_some_and(node_101)
                    && o.get("writes").is_some_and(node_113)
                    && o.keys().all(|k| {
                        [
                            "evaluation",
                            "eventSchema",
                            "kind",
                            "operation",
                            "phaseAfter",
                            "phaseBefore",
                            "previous",
                            "sequence",
                            "source",
                            "store",
                            "timeEvidence",
                            "writes",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_112(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "s4.5-challenge"))
}
fn node_113(v: &V) -> bool {
    matches!(v, V::Array(a) if a.len() == 1 && matches!(&a[0], V::String(s) if s == "pendingRecoveryChallenge"))
}
fn node_114(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => tag_hex(s, "closure2:", 64),
            _ => true,
        })
}
fn node_115(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("ci").is_some_and(node_116)
                    && o.get("mode").is_some_and(node_117)
                    && o.get("policyRecordId").is_some_and(node_52)
                    && o.keys()
                        .all(|k| ["ci", "mode", "policyRecordId"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_116(v: &V) -> bool {
    matches!(v, V::Bool(_))
}
fn node_117(v: &V) -> bool {
    matches!(v, V::String(s) if s == "interactive-explicit")
        || matches!(v, V::String(s) if s == "policy-record")
}
fn node_118(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("case").is_some_and(node_119)
                    && o.get("eventSchema").is_some_and(node_5)
                    && o.get("executionId").is_some_and(node_120)
                    && o.get("intentDigest").is_some_and(node_32)
                    && o.get("kind").is_some_and(node_121)
                    && o.get("operation").is_some_and(node_4)
                    && o.get("previous").is_some_and(node_8)
                    && o.get("sequence").is_some_and(node_12)
                    && o.get("side").is_some_and(node_122)
                    && o.get("sourceBeforeImage").is_some_and(node_4)
                    && o.get("sourceEventHead").is_some_and(node_8)
                    && o.get("store").is_some_and(node_13)
                    && o.get("targetBefore").is_some_and(node_123)
                    && o.keys().all(|k| {
                        [
                            "case",
                            "eventSchema",
                            "executionId",
                            "intentDigest",
                            "kind",
                            "operation",
                            "previous",
                            "sequence",
                            "side",
                            "sourceBeforeImage",
                            "sourceEventHead",
                            "store",
                            "targetBefore",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_119(v: &V) -> bool {
    matches!(v, V::String(s) if s == "forward") || matches!(v, V::String(s) if s == "ancestor")
}
fn node_120(v: &V) -> bool {
    node_179(v)
}
fn node_121(v: &V) -> bool {
    matches!(v, V::String(s) if s == "continuity")
}
fn node_122(v: &V) -> bool {
    matches!(v, V::String(s) if s == "source") || matches!(v, V::String(s) if s == "target")
}
fn node_123(v: &V) -> bool {
    (usize::from(node_124(v)) + usize::from(node_126(v))) == 1
}
fn node_124(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("absenceProof").is_some_and(node_4)
                    && o.get("kind").is_some_and(node_125)
                    && o.keys()
                        .all(|k| ["absenceProof", "kind"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_125(v: &V) -> bool {
    matches!(v, V::String(s) if s == "absent")
}
fn node_126(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("image").is_some_and(node_4)
                    && o.get("kind").is_some_and(node_127)
                    && o.keys().all(|k| ["image", "kind"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_127(v: &V) -> bool {
    matches!(v, V::String(s) if s == "capsule")
}
fn node_128(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("admissionSchema").is_some_and(node_38)
                    && o.get("binding").is_some_and(node_21)
                    && o.get("bootstrapManifest").is_some_and(node_19)
                    && o.get("coreClosure").is_some_and(node_129)
                    && o.get("coreInventory").is_some_and(node_19)
                    && o.get("kind").is_some_and(node_130)
                    && o.get("platform").is_some_and(node_131)
                    && o.get("root").is_some_and(node_19)
                    && o.keys().all(|k| {
                        [
                            "admissionSchema",
                            "binding",
                            "bootstrapManifest",
                            "coreClosure",
                            "coreInventory",
                            "kind",
                            "platform",
                            "root",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_129(v: &V) -> bool {
    node_114(v)
}
fn node_130(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "anchor"))
}
fn node_131(v: &V) -> bool {
    node_288(v)
}
fn node_132(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("embeddedBootstrap").is_some_and(node_133)
                    && o.get("inventorySchema").is_some_and(node_134)
                    && o.get("platformProfileBinding").is_some_and(node_135)
                    && o.get("platforms").is_some_and(node_136)
                    && o.get("protocolMajor").is_some_and(node_28)
                    && o.get("semanticVersion").is_some_and(node_138)
                    && o.get("servedProtocolMajors").is_some_and(node_139)
                    && o.get("tcbProfiles").is_some_and(node_140)
                    && o.get("verifiedInstallRoot").is_some_and(node_142)
                    && o.keys().all(|k| {
                        [
                            "embeddedBootstrap",
                            "inventorySchema",
                            "platformProfileBinding",
                            "platforms",
                            "protocolMajor",
                            "semanticVersion",
                            "servedProtocolMajors",
                            "tcbProfiles",
                            "verifiedInstallRoot",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_133(v: &V) -> bool {
    node_174(v)
}
fn node_134(v: &V) -> bool {
    (matches!(v, V::Integer(_))) && (matches!(v, V::Integer(n) if n.get() == 2_i128))
}
fn node_135(v: &V) -> bool {
    node_154(v)
}
fn node_136(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => !a.is_empty() && a.len() <= 4 && a.iter().all(node_137),
            _ => true,
        })
}
fn node_137(v: &V) -> bool {
    node_145(v)
}
fn node_138(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => s.chars().count() <= 256 && loose_version(s),
            _ => true,
        })
}
fn node_139(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => !a.is_empty() && a.len() <= 16 && a.iter().all(node_28),
            _ => true,
        })
}
fn node_140(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => a.len() <= 64 && a.iter().all(node_141),
            _ => true,
        })
}
fn node_141(v: &V) -> bool {
    node_437(v)
}
fn node_142(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "/"))
}
fn node_143(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (!node_144(v))
        && (match v {
            V::String(s) => {
                s.chars().count() >= 1 && s.chars().count() <= 4096 && core_path_shape(s)
            }
            _ => true,
        })
}
fn node_144(v: &V) -> bool {
    match v {
        V::String(s) => dot_segment(s),
        _ => true,
    }
}
fn node_145(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("entrypoint").is_some_and(node_146)
                    && o.get("layers").is_some_and(node_147)
                    && o.get("platform").is_some_and(node_131)
                    && o.get("requires").is_some_and(node_151)
                    && o.get("tree").is_some_and(node_153)
                    && o.keys().all(|k| {
                        ["entrypoint", "layers", "platform", "requires", "tree"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_146(v: &V) -> bool {
    node_143(v)
}
fn node_147(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => a.len() <= 100000 && a.iter().all(node_148),
            _ => true,
        })
}
fn node_148(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("layers").is_some_and(node_149)
                    && o.get("path").is_some_and(node_146)
                    && o.keys().all(|k| ["layers", "path"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_149(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => !a.is_empty() && a.len() <= 2 && a.iter().all(node_150),
            _ => true,
        })
}
fn node_150(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (matches!(v, V::String(s) if s == "L-DIST")
            || matches!(v, V::String(s) if s == "L-HOST")
            || matches!(v, V::String(s) if s == "L-EVAL")
            || matches!(v, V::String(s) if s == "L-COMP")
            || matches!(v, V::String(s) if s == "L-TCB"))
}
fn node_151(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => a.len() <= 100000 && a.iter().all(node_152),
            _ => true,
        })
}
fn node_152(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("from").is_some_and(node_146)
                    && o.get("to").is_some_and(node_146)
                    && o.keys().all(|k| ["from", "to"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_153(v: &V) -> bool {
    node_507(v)
}
fn node_154(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("platformProfileSetBodyDigest").is_some_and(node_32)
                    && o.get("schemaVersion").is_some_and(node_155)
                    && o.keys().all(|k| {
                        ["platformProfileSetBodyDigest", "schemaVersion"].contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_155(v: &V) -> bool {
    matches!(v, V::Integer(n) if n.get() == 2_i128)
}
fn node_156(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("creationInput").is_some_and(node_4)
                    && o.get("eventSchema").is_some_and(node_5)
                    && o.get("kind").is_some_and(node_157)
                    && o.get("operation").is_some_and(node_4)
                    && o.get("previous").is_some_and(node_8)
                    && o.get("sequence").is_some_and(node_12)
                    && o.get("store").is_some_and(node_13)
                    && o.keys().all(|k| {
                        [
                            "creationInput",
                            "eventSchema",
                            "kind",
                            "operation",
                            "previous",
                            "sequence",
                            "store",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_157(v: &V) -> bool {
    matches!(v, V::String(s) if s == "creation")
}
fn node_158(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("deliveringCore").is_some_and(node_129)
                    && o.get("inputSchema").is_some_and(node_38)
                    && o.get("kind").is_some_and(node_159)
                    && o.get("observation").is_some_and(node_160)
                    && o.get("platform").is_some_and(node_131)
                    && o.get("stagingName").is_some_and(node_161)
                    && o.get("store").is_some_and(node_162)
                    && o.get("storeMarker").is_some_and(node_4)
                    && o.keys().all(|k| {
                        [
                            "deliveringCore",
                            "inputSchema",
                            "kind",
                            "observation",
                            "platform",
                            "stagingName",
                            "store",
                            "storeMarker",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_159(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "creation-input"))
}
fn node_160(v: &V) -> bool {
    node_26(v)
}
fn node_161(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => hex(s, 32),
            _ => true,
        })
}
fn node_162(v: &V) -> bool {
    node_163(v)
}
fn node_163(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("stateSchema").is_some_and(node_164)
                    && o.get("storeGeneration").is_some_and(node_165)
                    && o.get("storeInstanceId").is_some_and(node_13)
                    && o.keys().all(|k| {
                        ["stateSchema", "storeGeneration", "storeInstanceId"].contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_164(v: &V) -> bool {
    node_429(v)
}
fn node_165(v: &V) -> bool {
    (matches!(v, V::Integer(_))) && (matches!(v, V::Integer(n) if n.get() == 0_i128))
}
fn node_166(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("class").is_some_and(node_167)
                    && o.get("code").is_some_and(node_168)
                    && o.get("exit").is_some_and(node_169)
                    && o.keys()
                        .all(|k| ["class", "code", "exit"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_167(v: &V) -> bool {
    matches!(v, V::String(s) if s == "request-rejected")
        || matches!(v, V::String(s) if s == "operational-failed")
}
fn node_168(v: &V) -> bool {
    matches!(v, V::String(s) if s == "CONFIG.INVALID")
        || matches!(v, V::String(s) if s == "REQUEST.PRECONDITION_FAILED")
        || matches!(v, V::String(s) if s == "EXTENSION.ADMISSION_REJECTED")
        || matches!(v, V::String(s) if s == "LEDGER.BUSY_TIMEOUT")
        || matches!(v, V::String(s) if s == "REQUEST.SCHEMA_MAJOR_UNSUPPORTED")
        || matches!(v, V::String(s) if s == "LEDGER.CORRUPT")
        || matches!(v, V::String(s) if s == "HOST.IO_FAILURE")
}
fn node_169(v: &V) -> bool {
    matches!(v, V::Integer(n) if n.get() == 2_i128)
        || matches!(v, V::Integer(n) if n.get() == 4_i128)
}
fn node_170(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("body").is_some_and(node_171)
                    && o.get("envelope").is_some_and(node_171)
                    && o.keys().all(|k| ["body", "envelope"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_171(v: &V) -> bool {
    node_42(v)
}
fn node_172(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("environment").is_some_and(node_173)
                    && o.get("filesystemWrite").is_some_and(node_173)
                    && o.get("network").is_some_and(node_173)
                    && o.get("subprocess").is_some_and(node_173)
                    && o.keys().all(|k| {
                        ["environment", "filesystemWrite", "network", "subprocess"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_173(v: &V) -> bool {
    node_176(v)
}
fn node_174(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("directory").is_some_and(node_146)
                    && o.get("envelope").is_some_and(node_175)
                    && o.get("manifest").is_some_and(node_175)
                    && o.keys()
                        .all(|k| ["directory", "envelope", "manifest"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_175(v: &V) -> bool {
    node_181(v)
}
fn node_176(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => s.chars().count() <= 128 && enforcement(s),
            _ => true,
        })
}
fn node_177(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("bytes").is_some_and(node_43)
                    && o.get("sequence").is_some_and(node_178)
                    && o.get("sha256").is_some_and(node_44)
                    && o.get("storeInstanceId").is_some_and(node_161)
                    && o.keys().all(|k| {
                        ["bytes", "sequence", "sha256", "storeInstanceId"].contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_178(v: &V) -> bool {
    (matches!(v, V::Integer(_)))
        && (match v {
            V::Integer(n) => n.get() >= 1_i128 && n.get() <= 9223372036854775807_i128,
            _ => true,
        })
}
fn node_179(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => tag_hex(s, "exec1_", 32),
            _ => true,
        })
}
fn node_180(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("catalogExpired").is_some_and(node_116)
                    && o.get("revocationStale").is_some_and(node_116)
                    && o.get("rootExpired").is_some_and(node_116)
                    && o.keys().all(|k| {
                        ["catalogExpired", "revocationStale", "rootExpired"].contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_181(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("bytes").is_some_and(node_28)
                    && o.get("path").is_some_and(node_146)
                    && o.get("sha256").is_some_and(node_32)
                    && o.keys()
                        .all(|k| ["bytes", "path", "sha256"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_182(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => s.chars().count() >= 64 && s.chars().count() <= 64 && hex(s, 64),
            _ => true,
        })
}
fn node_183(v: &V) -> bool {
    (matches!(v, V::Integer(_)))
        && (match v {
            V::Integer(n) => n.get() >= 0_i128 && n.get() <= 9223372036854775807_i128,
            _ => true,
        })
}
fn node_184(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("kind").is_some_and(node_185)
                    && o.get("operation").is_some_and(node_186)
                    && o.get("requestId").is_some_and(node_187)
                    && o.get("schemaVersion").is_some_and(node_5)
                    && o.get("stepId").is_some_and(node_188)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        [
                            "kind",
                            "operation",
                            "requestId",
                            "schemaVersion",
                            "stepId",
                            "store",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_185(v: &V) -> bool {
    matches!(v, V::String(s) if s == "installation")
}
fn node_186(v: &V) -> bool {
    matches!(v, V::String(s) if s == "trust-acknowledge-restore")
        || matches!(v, V::String(s) if s == "trust-ceremony-abort")
        || matches!(v, V::String(s) if s == "trust-ceremony-begin")
        || matches!(v, V::String(s) if s == "trust-ceremony-commit")
        || matches!(v, V::String(s) if s == "trust-import")
        || matches!(v, V::String(s) if s == "trust-recovery-challenge")
        || matches!(v, V::String(s) if s == "trust-recovery-import")
        || matches!(v, V::String(s) if s == "trust-refresh")
}
fn node_187(v: &V) -> bool {
    node_320(v)
}
fn node_188(v: &V) -> bool {
    node_431(v)
}
fn node_189(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("fromCoreClosure").is_some_and(node_129)
                    && o.get("fromStateSchema").is_some_and(node_164)
                    && o.get("fromStoreGeneration").is_some_and(node_28)
                    && o.get("operation").is_some_and(node_190)
                    && o.get("platformProfileSetBodyDigest").is_some_and(node_32)
                    && o.get("preconditionGeneration").is_some_and(node_28)
                    && o.get("rollbackDeadline").is_some_and(node_191)
                    && o.get("schemaVersion").is_some_and(node_5)
                    && o.get("toCoreClosure").is_some_and(node_129)
                    && o.get("toStateSchema").is_some_and(node_164)
                    && o.get("toStoreGeneration").is_some_and(node_28)
                    && o.keys().all(|k| {
                        [
                            "fromCoreClosure",
                            "fromStateSchema",
                            "fromStoreGeneration",
                            "operation",
                            "platformProfileSetBodyDigest",
                            "preconditionGeneration",
                            "rollbackDeadline",
                            "schemaVersion",
                            "toCoreClosure",
                            "toStateSchema",
                            "toStoreGeneration",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_190(v: &V) -> bool {
    node_504(v)
}
fn node_191(v: &V) -> bool {
    node_219(v)
}
fn node_192(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("executionId").is_some_and(node_120)
                    && o.get("requestId").is_some_and(node_187)
                    && o.get("stepId").is_some_and(node_188)
                    && o.keys()
                        .all(|k| ["executionId", "requestId", "stepId"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_193(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("grant").is_none_or(node_194)
                    && o.get("grantGeneration").is_some_and(node_12)
                    && o.get("operationRef").is_some_and(node_195)
                    && o.get("outcome").is_none_or(node_196)
                    && o.get("postimageSha256").is_none_or(node_32)
                    && o.get("reason").is_none_or(node_194)
                    && o.get("recordSchema").is_some_and(node_197)
                    && o.get("recordType").is_some_and(node_198)
                    && o.get("requestRef").is_none_or(node_194)
                    && o.get("residuals").is_none_or(node_199)
                    && o.get("runId").is_none_or(node_200)
                    && o.get("seq").is_some_and(node_12)
                    && o.get("trustEpochObserved").is_none_or(node_201)
                    && o.keys().all(|k| {
                        [
                            "grant",
                            "grantGeneration",
                            "operationRef",
                            "outcome",
                            "postimageSha256",
                            "reason",
                            "recordSchema",
                            "recordType",
                            "requestRef",
                            "residuals",
                            "runId",
                            "seq",
                            "trustEpochObserved",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_194(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => s.chars().count() <= 256,
            _ => true,
        })
}
fn node_195(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => s.chars().count() >= 1 && s.chars().count() <= 128,
            _ => true,
        })
}
fn node_196(v: &V) -> bool {
    matches!(v, V::String(s) if s == "COMPLETED")
}
fn node_197(v: &V) -> bool {
    matches!(v, V::Integer(n) if n.get() == 3_i128)
}
fn node_198(v: &V) -> bool {
    matches!(v, V::String(s) if s == "GRANT")
        || matches!(v, V::String(s) if s == "RA")
        || matches!(v, V::String(s) if s == "ICI")
        || matches!(v, V::String(s) if s == "RCI")
        || matches!(v, V::String(s) if s == "ICO")
        || matches!(v, V::String(s) if s == "RCO")
        || matches!(v, V::String(s) if s == "REV")
        || matches!(v, V::String(s) if s == "CLN")
        || matches!(v, V::String(s) if s == "SEAL")
}
fn node_199(v: &V) -> bool {
    node_434(v)
}
fn node_200(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => tag_hex(s, "run3:", 64),
            _ => true,
        })
}
fn node_201(v: &V) -> bool {
    matches!(v, V::Object(_))
}
fn node_202(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("grant").is_none_or(node_194)
                    && o.get("grantGeneration").is_some_and(node_12)
                    && o.get("operationRef").is_some_and(node_195)
                    && o.get("outcome").is_none_or(node_196)
                    && o.get("postimageSha256").is_none_or(node_32)
                    && o.get("reason").is_none_or(node_194)
                    && o.get("recordSchema").is_some_and(node_155)
                    && o.get("recordType").is_some_and(node_198)
                    && o.get("requestRef").is_none_or(node_194)
                    && o.get("residuals").is_none_or(node_199)
                    && o.get("runId").is_none_or(node_203)
                    && o.get("seq").is_some_and(node_12)
                    && o.get("trustEpochObserved").is_none_or(node_201)
                    && o.keys().all(|k| {
                        [
                            "grant",
                            "grantGeneration",
                            "operationRef",
                            "outcome",
                            "postimageSha256",
                            "reason",
                            "recordSchema",
                            "recordType",
                            "requestRef",
                            "residuals",
                            "runId",
                            "seq",
                            "trustEpochObserved",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_203(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => tag_hex(s, "run2:", 64),
            _ => true,
        })
}
fn node_204(v: &V) -> bool {
    matches!(v, V::String(s) if s == "PREPARING")
        || matches!(v, V::String(s) if s == "STAGED")
        || matches!(v, V::String(s) if s == "APPLYING")
        || matches!(v, V::String(s) if s == "APPLIED")
        || matches!(v, V::String(s) if s == "COMMITTED")
        || matches!(v, V::String(s) if s == "FAILED_CLEAN")
        || matches!(v, V::String(s) if s == "FAILED_ROLLED_BACK")
        || matches!(v, V::String(s) if s == "RECOVERY_BLOCKED")
        || matches!(v, V::String(s) if s == "INDETERMINATE")
}
fn node_205(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("descriptor").is_some_and(node_4)
                    && o.get("members").is_some_and(node_206)
                    && o.keys()
                        .all(|k| ["descriptor", "members"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_206(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("TR-BUNDLE").is_none_or(node_207)
                    && o.get("TR-COMPONENT").is_none_or(node_207)
                    && o.get("TR-CORE").is_none_or(node_207)
                    && o.get("TR-INDEX").is_none_or(node_207)
                    && o.get("TR-PROFILE").is_none_or(node_207)
                    && o.get("TR-REPAIR").is_none_or(node_207)
                    && o.keys().all(|k| {
                        [
                            "TR-BUNDLE",
                            "TR-COMPONENT",
                            "TR-CORE",
                            "TR-INDEX",
                            "TR-PROFILE",
                            "TR-REPAIR",
                        ]
                        .contains(&k.as_str())
                    })
                    && !o.is_empty()
            }
            _ => true,
        })
}
fn node_207(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("by").is_some_and(node_3)
                    && o.get("status").is_some_and(node_208)
                    && o.keys().all(|k| ["by", "status"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_208(v: &V) -> bool {
    matches!(v, V::String(s) if s == "recovering")
        || matches!(v, V::String(s) if s == "interrupted")
}
fn node_209(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => {
                s.chars().count() >= 1 && s.chars().count() <= 1024 && logical_path_shape(s)
            }
            _ => true,
        })
}
fn node_210(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("admissionSchema").is_some_and(node_38)
                    && o.get("admittingRoot").is_some_and(node_4)
                    && o.get("closure").is_some_and(node_4)
                    && o.get("context").is_some_and(node_211)
                    && o.get("document").is_some_and(node_19)
                    && o.get("kind").is_some_and(node_212)
                    && o.keys().all(|k| {
                        [
                            "admissionSchema",
                            "admittingRoot",
                            "closure",
                            "context",
                            "document",
                            "kind",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_211(v: &V) -> bool {
    node_268(v)
}
fn node_212(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (matches!(v, V::String(s) if s == "catalog")
            || matches!(v, V::String(s) if s == "revocation"))
}
fn node_213(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => {
                a.len() <= 65536 && unique(a) && a.iter().all(node_214) && ordered(a, &[])
            }
            _ => true,
        })
}
fn node_214(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => s.chars().count() >= 1 && s.chars().count() <= 4096,
            _ => true,
        })
}
fn node_215(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("revision").is_some_and(node_12)
                    && o.get("sha256").is_some_and(node_32)
                    && o.keys()
                        .all(|k| ["revision", "sha256"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_216(v: &V) -> bool {
    (usize::from(node_217(v)) + usize::from(node_9(v))) == 1
}
fn node_217(v: &V) -> bool {
    node_166(v)
}
fn node_218(v: &V) -> bool {
    (matches!(v, V::String(_) | V::Null))
        && (match v {
            V::String(s) => s.chars().count() <= 4096,
            _ => true,
        })
}
fn node_219(v: &V) -> bool {
    (usize::from(node_29(v)) + usize::from(node_9(v))) == 1
}
fn node_220(v: &V) -> bool {
    (usize::from(node_221(v))
        + usize::from(node_226(v))
        + usize::from(node_228(v))
        + usize::from(node_230(v))
        + usize::from(node_232(v))
        + usize::from(node_236(v))
        + usize::from(node_240(v))
        + usize::from(node_242(v))
        + usize::from(node_246(v))
        + usize::from(node_249(v))
        + usize::from(node_252(v))
        + usize::from(node_256(v))
        + usize::from(node_260(v))
        + usize::from(node_264(v)))
        == 1
}
fn node_221(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("action").is_some_and(node_222)
                    && o.get("input").is_some_and(node_223)
                    && o.get("invocation").is_some_and(node_225)
                    && o.get("operationSchema").is_some_and(node_5)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        ["action", "input", "invocation", "operationSchema", "store"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_222(v: &V) -> bool {
    matches!(v, V::String(s) if s == "ordinary-import")
}
fn node_223(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("kind").is_some_and(node_224)
                    && o.get("ref").is_some_and(node_4)
                    && o.keys().all(|k| ["kind", "ref"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_224(v: &V) -> bool {
    matches!(v, V::String(s) if s == "payload-metadata-closure")
}
fn node_225(v: &V) -> bool {
    node_192(v)
}
fn node_226(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("action").is_some_and(node_227)
                    && o.get("input").is_some_and(node_223)
                    && o.get("invocation").is_some_and(node_225)
                    && o.get("operationSchema").is_some_and(node_5)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        ["action", "input", "invocation", "operationSchema", "store"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_227(v: &V) -> bool {
    matches!(v, V::String(s) if s == "refresh")
}
fn node_228(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("action").is_some_and(node_229)
                    && o.get("input").is_some_and(node_223)
                    && o.get("invocation").is_some_and(node_225)
                    && o.get("operationSchema").is_some_and(node_5)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        ["action", "input", "invocation", "operationSchema", "store"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_229(v: &V) -> bool {
    matches!(v, V::String(s) if s == "bootstrap")
}
fn node_230(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("action").is_some_and(node_231)
                    && o.get("input").is_some_and(node_223)
                    && o.get("invocation").is_some_and(node_225)
                    && o.get("operationSchema").is_some_and(node_5)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        ["action", "input", "invocation", "operationSchema", "store"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_231(v: &V) -> bool {
    matches!(v, V::String(s) if s == "recovery-stage")
}
fn node_232(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("action").is_some_and(node_233)
                    && o.get("input").is_some_and(node_234)
                    && o.get("invocation").is_some_and(node_225)
                    && o.get("operationSchema").is_some_and(node_5)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        ["action", "input", "invocation", "operationSchema", "store"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_233(v: &V) -> bool {
    matches!(v, V::String(s) if s == "ceremony-begin")
}
fn node_234(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("kind").is_some_and(node_235)
                    && o.get("ref").is_some_and(node_4)
                    && o.keys().all(|k| ["kind", "ref"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_235(v: &V) -> bool {
    matches!(v, V::String(s) if s == "staged-closure")
}
fn node_236(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("action").is_some_and(node_237)
                    && o.get("input").is_some_and(node_238)
                    && o.get("invocation").is_some_and(node_225)
                    && o.get("operationSchema").is_some_and(node_5)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        ["action", "input", "invocation", "operationSchema", "store"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_237(v: &V) -> bool {
    matches!(v, V::String(s) if s == "ceremony-commit")
}
fn node_238(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("kind").is_some_and(node_239)
                    && o.get("ref").is_some_and(node_4)
                    && o.keys().all(|k| ["kind", "ref"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_239(v: &V) -> bool {
    matches!(v, V::String(s) if s == "begin-batch")
}
fn node_240(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("action").is_some_and(node_241)
                    && o.get("input").is_some_and(node_238)
                    && o.get("invocation").is_some_and(node_225)
                    && o.get("operationSchema").is_some_and(node_5)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        ["action", "input", "invocation", "operationSchema", "store"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_241(v: &V) -> bool {
    matches!(v, V::String(s) if s == "ceremony-abort")
}
fn node_242(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("action").is_some_and(node_243)
                    && o.get("input").is_some_and(node_244)
                    && o.get("invocation").is_some_and(node_225)
                    && o.get("operationSchema").is_some_and(node_5)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        ["action", "input", "invocation", "operationSchema", "store"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_243(v: &V) -> bool {
    matches!(v, V::String(s) if s == "clock-recovery-import")
}
fn node_244(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("kind").is_some_and(node_245)
                    && o.get("ref").is_some_and(node_4)
                    && o.keys().all(|k| ["kind", "ref"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_245(v: &V) -> bool {
    matches!(v, V::String(s) if s == "recovery-epoch-proof")
}
fn node_246(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("action").is_some_and(node_157)
                    && o.get("input").is_some_and(node_247)
                    && o.get("invocation").is_some_and(node_225)
                    && o.get("operationSchema").is_some_and(node_5)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        ["action", "input", "invocation", "operationSchema", "store"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_247(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("kind").is_some_and(node_248)
                    && o.get("ref").is_some_and(node_4)
                    && o.keys().all(|k| ["kind", "ref"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_248(v: &V) -> bool {
    matches!(v, V::String(s) if s == "creation-input")
}
fn node_249(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("action").is_some_and(node_121)
                    && o.get("input").is_some_and(node_250)
                    && o.get("invocation").is_some_and(node_225)
                    && o.get("operationSchema").is_some_and(node_5)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        ["action", "input", "invocation", "operationSchema", "store"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_250(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("kind").is_some_and(node_251)
                    && o.get("ref").is_some_and(node_4)
                    && o.keys().all(|k| ["kind", "ref"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_251(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "transition-intent-input"))
}
fn node_252(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("action").is_some_and(node_253)
                    && o.get("input").is_some_and(node_254)
                    && o.get("invocation").is_some_and(node_225)
                    && o.get("operationSchema").is_some_and(node_5)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        ["action", "input", "invocation", "operationSchema", "store"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_253(v: &V) -> bool {
    matches!(v, V::String(s) if s == "acknowledge-restore")
}
fn node_254(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("kind").is_some_and(node_255)
                    && o.get("ref").is_some_and(node_4)
                    && o.keys().all(|k| ["kind", "ref"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_255(v: &V) -> bool {
    matches!(v, V::String(s) if s == "restore-declaration-input")
}
fn node_256(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("action").is_some_and(node_257)
                    && o.get("input").is_some_and(node_258)
                    && o.get("invocation").is_some_and(node_225)
                    && o.get("operationSchema").is_some_and(node_5)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        ["action", "input", "invocation", "operationSchema", "store"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_257(v: &V) -> bool {
    matches!(v, V::String(s) if s == "restore-recovery")
}
fn node_258(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("kind").is_some_and(node_259)
                    && o.get("ref").is_some_and(node_4)
                    && o.keys().all(|k| ["kind", "ref"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_259(v: &V) -> bool {
    matches!(v, V::String(s) if s == "restore-proof")
}
fn node_260(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("action").is_some_and(node_261)
                    && o.get("input").is_some_and(node_262)
                    && o.get("invocation").is_some_and(node_225)
                    && o.get("operationSchema").is_some_and(node_5)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        ["action", "input", "invocation", "operationSchema", "store"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_261(v: &V) -> bool {
    matches!(v, V::String(s) if s == "clock-recovery-challenge")
}
fn node_262(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("kind").is_some_and(node_263)
                    && o.keys().all(|k| ["kind"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_263(v: &V) -> bool {
    matches!(v, V::String(s) if s == "none")
}
fn node_264(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("action").is_some_and(node_265)
                    && o.get("input").is_some_and(node_266)
                    && o.get("invocation").is_some_and(node_225)
                    && o.get("operationSchema").is_some_and(node_5)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        ["action", "input", "invocation", "operationSchema", "store"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_265(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "host-trust-admission"))
}
fn node_266(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("kind").is_some_and(node_267)
                    && o.get("ref").is_some_and(node_4)
                    && o.keys().all(|k| ["kind", "ref"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_267(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "trust-admission-input"))
}
fn node_268(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("incomingRevocation").is_some_and(node_23)
                    && o.get("priorRevocationHistory").is_some_and(node_51)
                    && o.get("time").is_some_and(node_4)
                    && o.keys().all(|k| {
                        ["incomingRevocation", "priorRevocationHistory", "time"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_269(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("anchor").is_some_and(node_270)
                    && o.get("catalogExpiresAt").is_some_and(node_9)
                    && o.get("evalHighWater").is_some_and(node_29)
                    && o.get("lastAccepted").is_some_and(node_29)
                    && o.get("revocationIssuedAt").is_some_and(node_9)
                    && o.get("rootExpiresAt").is_some_and(node_9)
                    && o.keys().all(|k| {
                        [
                            "anchor",
                            "catalogExpiresAt",
                            "evalHighWater",
                            "lastAccepted",
                            "revocationIssuedAt",
                            "rootExpiresAt",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_270(v: &V) -> bool {
    (usize::from(node_160(v)) + usize::from(node_9(v))) == 1
}
fn node_271(v: &V) -> bool {
    (usize::from(node_272(v)) + usize::from(node_262(v))) == 1
}
fn node_272(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("kind").is_some_and(node_273)
                    && o.get("ref").is_some_and(node_4)
                    && o.keys().all(|k| ["kind", "ref"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_273(v: &V) -> bool {
    matches!(v, V::String(s) if s == "closure")
}
fn node_274(v: &V) -> bool {
    (usize::from(node_275(v)) + usize::from(node_285(v))) == 1
}
fn node_275(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("artifactObservations").is_some_and(node_276)
                    && o.get("catalog").is_some_and(node_19)
                    && o.get("closureSchema").is_some_and(node_38)
                    && o.get("manifest").is_some_and(node_19)
                    && o.get("members").is_some_and(node_278)
                    && o.get("repairMaterial").is_some_and(node_280)
                    && o.get("revocation").is_some_and(node_19)
                    && o.get("rootChain").is_some_and(node_283)
                    && o.get("scope").is_some_and(node_284)
                    && o.keys().all(|k| {
                        [
                            "artifactObservations",
                            "catalog",
                            "closureSchema",
                            "manifest",
                            "members",
                            "repairMaterial",
                            "revocation",
                            "rootChain",
                            "scope",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_276(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => a.len() <= 65536 && a.iter().all(node_277) && ordered(a, &["path"]),
            _ => true,
        })
}
fn node_277(v: &V) -> bool {
    node_30(v)
}
fn node_278(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => {
                a.len() <= 65536 && a.iter().all(node_279) && ordered(a, &["slot", "path"])
            }
            _ => true,
        })
}
fn node_279(v: &V) -> bool {
    node_350(v)
}
fn node_280(v: &V) -> bool {
    (usize::from(node_281(v)) + usize::from(node_282(v))) == 1
}
fn node_281(v: &V) -> bool {
    node_316(v)
}
fn node_282(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("blob").is_some_and(node_171)
                    && o.get("path").is_some_and(node_31)
                    && o.keys().all(|k| ["blob", "path"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_283(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => !a.is_empty() && a.len() <= 64 && a.iter().all(node_19),
            _ => true,
        })
}
fn node_284(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "ordinary-inert"))
}
fn node_285(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("artifactObservations").is_some_and(node_276)
                    && o.get("authorization").is_some_and(node_19)
                    && o.get("catalog").is_some_and(node_19)
                    && o.get("closureSchema").is_some_and(node_38)
                    && o.get("manifest").is_some_and(node_19)
                    && o.get("members").is_some_and(node_278)
                    && o.get("repairMaterial").is_some_and(node_280)
                    && o.get("revocation").is_some_and(node_19)
                    && o.get("rootChain").is_some_and(node_283)
                    && o.get("scope").is_some_and(node_286)
                    && o.keys().all(|k| {
                        [
                            "artifactObservations",
                            "authorization",
                            "catalog",
                            "closureSchema",
                            "manifest",
                            "members",
                            "repairMaterial",
                            "revocation",
                            "rootChain",
                            "scope",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_286(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "recovery-full-signed-scope"))
}
fn node_287(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("bootId").is_some_and(node_27)
                    && o.get("createdMono").is_some_and(node_28)
                    && o.get("createdWall").is_some_and(node_29)
                    && o.get("expiresMono").is_some_and(node_28)
                    && o.get("nonce").is_some_and(node_32)
                    && o.get("recordDigest").is_some_and(node_32)
                    && o.keys().all(|k| {
                        [
                            "bootId",
                            "createdMono",
                            "createdWall",
                            "expiresMono",
                            "nonce",
                            "recordDigest",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_288(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (matches!(v, V::String(s) if s == "linux-aarch64-gnu")
            || matches!(v, V::String(s) if s == "linux-x86_64-gnu")
            || matches!(v, V::String(s) if s == "macos-aarch64")
            || matches!(v, V::String(s) if s == "macos-x86_64"))
}
fn node_289(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("batch").is_some_and(node_4)
                    && o.get("before").is_some_and(node_290)
                    && o.get("begin").is_some_and(node_3)
                    && o.get("cause").is_some_and(node_291)
                    && o.get("eventSchema").is_some_and(node_5)
                    && o.get("from").is_some_and(node_6)
                    && o.get("kind").is_some_and(node_292)
                    && o.get("operation").is_some_and(node_4)
                    && o.get("previous").is_some_and(node_8)
                    && o.get("role").is_some_and(node_11)
                    && o.get("sequence").is_some_and(node_12)
                    && o.get("store").is_some_and(node_13)
                    && o.get("to").is_some_and(node_293)
                    && o.keys().all(|k| {
                        [
                            "batch",
                            "before",
                            "begin",
                            "cause",
                            "eventSchema",
                            "from",
                            "kind",
                            "operation",
                            "previous",
                            "role",
                            "sequence",
                            "store",
                            "to",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_290(v: &V) -> bool {
    node_384(v)
}
fn node_291(v: &V) -> bool {
    matches!(v, V::String(s) if s == "ROOT_CHANGED")
        || matches!(v, V::String(s) if s == "MIGRATED")
        || matches!(v, V::String(s) if s == "RESTORED")
}
fn node_292(v: &V) -> bool {
    matches!(v, V::String(s) if s == "private-ceremony-termination")
}
fn node_293(v: &V) -> bool {
    matches!(v, V::String(s) if s == "ST-REVOKED")
        || matches!(v, V::String(s) if s == "ST-UNBOOTSTRAPPED")
}
fn node_294(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => tag_hex(s, "prj1-", 64),
            _ => true,
        })
}
fn node_295(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("image").is_some_and(node_4)
                    && o.get("revision").is_some_and(node_12)
                    && o.keys()
                        .all(|k| ["image", "revision"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_296(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && ((usize::from(node_297(v)) + usize::from(node_299(v))) == 1)
        && (match v {
            V::Object(o) => {
                o.get("markerCount").is_some_and(node_301)
                    && o.get("markerCountBasis").is_some_and(node_302)
                    && o.get("path").is_some_and(node_303)
                    && o.get("reason").is_some_and(node_304)
                    && o.keys().all(|k| {
                        ["markerCount", "markerCountBasis", "path", "reason"].contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_297(v: &V) -> bool {
    match v {
        V::Object(o) => {
            o.get("markerCount").is_none_or(node_9)
                && o.get("markerCountBasis").is_none_or(node_298)
        }
        _ => true,
    }
}
fn node_298(v: &V) -> bool {
    matches!(v, V::String(s) if s == "not-enumerated")
}
fn node_299(v: &V) -> bool {
    match v {
        V::Object(o) => {
            o.get("markerCount").is_none_or(node_28)
                && o.get("markerCountBasis").is_none_or(node_300)
        }
        _ => true,
    }
}
fn node_300(v: &V) -> bool {
    matches!(v, V::String(s) if s == "observed-inventory")
}
fn node_301(v: &V) -> bool {
    (usize::from(node_9(v)) + usize::from(node_28(v))) == 1
}
fn node_302(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (matches!(v, V::String(s) if s == "not-enumerated")
            || matches!(v, V::String(s) if s == "observed-inventory"))
}
fn node_303(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => s.chars().count() <= 4096,
            _ => true,
        })
}
fn node_304(v: &V) -> bool {
    matches!(v, V::String(s) if s == "dependency-tree")
        || matches!(v, V::String(s) if s == "vcs-tree")
        || matches!(v, V::String(s) if s == "cargo-build-output")
}
fn node_305(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("afterProjection").is_some_and(node_306)
                    && o.get("commandOutcome").is_none_or(node_4)
                    && o.get("events").is_some_and(node_307)
                    && o.get("nativeBefore").is_some_and(node_309)
                    && o.get("operation").is_some_and(node_4)
                    && o.get("previousCapsule").is_some_and(node_52)
                    && o.get("publicationSchema").is_some_and(node_38)
                    && o.get("revision").is_some_and(node_12)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        [
                            "afterProjection",
                            "commandOutcome",
                            "events",
                            "nativeBefore",
                            "operation",
                            "previousCapsule",
                            "publicationSchema",
                            "revision",
                            "store",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_306(v: &V) -> bool {
    node_45(v)
}
fn node_307(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => a.len() <= 65536 && a.iter().all(node_308),
            _ => true,
        })
}
fn node_308(v: &V) -> bool {
    node_311(v)
}
fn node_309(v: &V) -> bool {
    (usize::from(node_310(v)) + usize::from(node_9(v))) == 1
}
fn node_310(v: &V) -> bool {
    node_215(v)
}
fn node_311(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("event").is_some_and(node_3)
                    && o.get("roleChange").is_some_and(node_312)
                    && o.keys()
                        .all(|k| ["event", "roleChange"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_312(v: &V) -> bool {
    (usize::from(node_313(v)) + usize::from(node_9(v))) == 1
}
fn node_313(v: &V) -> bool {
    node_359(v)
}
fn node_314(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("bytes").is_some_and(node_43)
                    && o.get("previousCapsule").is_some_and(node_52)
                    && o.get("sha256").is_some_and(node_32)
                    && o.keys()
                        .all(|k| ["bytes", "previousCapsule", "sha256"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_315(v: &V) -> bool {
    matches!(v, V::String(s) if s == "discard-temps")
        || matches!(v, V::String(s) if s == "roll-back-renamed")
        || matches!(v, V::String(s) if s == "verify-postimages-and-commit")
}
fn node_316(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("ridesOn").is_some_and(node_317)
                    && o.get("standing").is_some_and(node_318)
                    && o.keys()
                        .all(|k| ["ridesOn", "standing"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_317(v: &V) -> bool {
    matches!(v, V::String(s) if s == "DR-110")
}
fn node_318(v: &V) -> bool {
    matches!(v, V::String(s) if s == "absent-by-typed-absence")
}
fn node_319(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => tag_hex(s, "repairplan2:", 64),
            _ => true,
        })
}
fn node_320(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => tag_hex(s, "req1_", 32),
            _ => true,
        })
}
fn node_321(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("beforeImage").is_some_and(node_4)
                    && o.get("examinedOrphans").is_some_and(node_322)
                    && o.get("inputSchema").is_some_and(node_38)
                    && o.get("kind").is_some_and(node_324)
                    && o.get("observation").is_some_and(node_160)
                    && o.get("transitionSlot").is_some_and(node_325)
                    && o.keys().all(|k| {
                        [
                            "beforeImage",
                            "examinedOrphans",
                            "inputSchema",
                            "kind",
                            "observation",
                            "transitionSlot",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_322(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => a.len() <= 64 && a.iter().all(node_323),
            _ => true,
        })
}
fn node_323(v: &V) -> bool {
    node_314(v)
}
fn node_324(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "restore-declaration-input"))
}
fn node_325(v: &V) -> bool {
    node_506(v)
}
fn node_326(v: &V) -> bool {
    (usize::from(node_327(v)) + usize::from(node_330(v))) == 1
}
fn node_327(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("eventSchema").is_some_and(node_5)
                    && o.get("kind").is_some_and(node_328)
                    && o.get("nativeBefore").is_some_and(node_310)
                    && o.get("operation").is_some_and(node_4)
                    && o.get("previous").is_some_and(node_8)
                    && o.get("sequence").is_some_and(node_12)
                    && o.get("store").is_some_and(node_13)
                    && o.get("variant").is_some_and(node_329)
                    && o.keys().all(|k| {
                        [
                            "eventSchema",
                            "kind",
                            "nativeBefore",
                            "operation",
                            "previous",
                            "sequence",
                            "store",
                            "variant",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_328(v: &V) -> bool {
    matches!(v, V::String(s) if s == "restore")
}
fn node_329(v: &V) -> bool {
    matches!(v, V::String(s) if s == "declared")
}
fn node_330(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("eventSchema").is_some_and(node_5)
                    && o.get("kind").is_some_and(node_328)
                    && o.get("logicalBefore").is_some_and(node_310)
                    && o.get("nativeBefore").is_some_and(node_310)
                    && o.get("operation").is_some_and(node_4)
                    && o.get("previous").is_some_and(node_8)
                    && o.get("proof").is_some_and(node_4)
                    && o.get("sequence").is_some_and(node_12)
                    && o.get("store").is_some_and(node_13)
                    && o.get("variant").is_some_and(node_331)
                    && o.keys().all(|k| {
                        [
                            "eventSchema",
                            "kind",
                            "logicalBefore",
                            "nativeBefore",
                            "operation",
                            "previous",
                            "proof",
                            "sequence",
                            "store",
                            "variant",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_331(v: &V) -> bool {
    matches!(v, V::String(s) if s == "recovery")
}
fn node_332(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("chain").is_some_and(node_333)
                    && o.get("kind").is_some_and(node_334)
                    && o.get("observation").is_some_and(node_160)
                    && o.get("observed").is_some_and(node_335)
                    && o.get("proofSchema").is_some_and(node_38)
                    && o.get("proven").is_some_and(node_335)
                    && o.get("store").is_some_and(node_57)
                    && o.get("terminalWitness").is_some_and(node_323)
                    && o.get("transitionSlot").is_some_and(node_325)
                    && o.keys().all(|k| {
                        [
                            "chain",
                            "kind",
                            "observation",
                            "observed",
                            "proofSchema",
                            "proven",
                            "store",
                            "terminalWitness",
                            "transitionSlot",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_333(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => !a.is_empty() && a.len() <= 65536 && a.iter().all(node_323),
            _ => true,
        })
}
fn node_334(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "restore-proof"))
}
fn node_335(v: &V) -> bool {
    node_295(v)
}
fn node_336(v: &V) -> bool {
    (usize::from(node_337(v)) + usize::from(node_341(v))) == 1
}
fn node_337(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("acceptedUnder").is_some_and(node_4)
                    && o.get("begin").is_some_and(node_51)
                    && o.get("evidenceSchema").is_some_and(node_38)
                    && o.get("history").is_some_and(node_4)
                    && o.get("kind").is_some_and(node_338)
                    && o.get("listNode").is_some_and(node_4)
                    && o.get("role").is_some_and(node_11)
                    && o.get("subject").is_some_and(node_339)
                    && o.get("subjectKind").is_some_and(node_340)
                    && o.keys().all(|k| {
                        [
                            "acceptedUnder",
                            "begin",
                            "evidenceSchema",
                            "history",
                            "kind",
                            "listNode",
                            "role",
                            "subject",
                            "subjectKind",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_338(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "revocation"))
}
fn node_339(v: &V) -> bool {
    node_27(v)
}
fn node_340(v: &V) -> bool {
    node_358(v)
}
fn node_341(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("begin").is_some_and(node_51)
                    && o.get("context").is_some_and(node_342)
                    && o.get("contextRoot").is_some_and(node_4)
                    && o.get("evidenceSchema").is_some_and(node_38)
                    && o.get("history").is_some_and(node_51)
                    && o.get("kind").is_some_and(node_343)
                    && o.get("role").is_some_and(node_11)
                    && o.keys().all(|k| {
                        [
                            "begin",
                            "context",
                            "contextRoot",
                            "evidenceSchema",
                            "history",
                            "kind",
                            "role",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_342(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (matches!(v, V::String(s) if s == "current-accepted-root")
            || matches!(v, V::String(s) if s == "begin-bound-prospective-root"))
}
fn node_343(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "quorum"))
}
fn node_344(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("beforeClock").is_some_and(node_48)
                    && o.get("beforeImage").is_some_and(node_4)
                    && o.get("inputSchema").is_some_and(node_38)
                    && o.get("invocation").is_some_and(node_225)
                    && o.get("kind").is_some_and(node_345)
                    && o.get("observation").is_some_and(node_160)
                    && o.get("purpose").is_some_and(node_346)
                    && o.get("restrictionEvidence").is_some_and(node_4)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        [
                            "beforeClock",
                            "beforeImage",
                            "inputSchema",
                            "invocation",
                            "kind",
                            "observation",
                            "purpose",
                            "restrictionEvidence",
                            "store",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_345(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "restriction-observation"))
}
fn node_346(v: &V) -> bool {
    matches!(v, V::String(s) if s == "revocation") || matches!(v, V::String(s) if s == "quorum")
}
fn node_347(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("anchor").is_some_and(node_270)
                    && o.get("catalogExpiresAt").is_some_and(node_191)
                    && o.get("evalHighWater").is_some_and(node_29)
                    && o.get("indexSnapshotVersion").is_some_and(node_12)
                    && o.get("lastAccepted").is_some_and(node_29)
                    && o.get("pendingRecoveryChallenge").is_some_and(node_348)
                    && o.get("recoveryEpochSerial").is_some_and(node_28)
                    && o.get("revocationIssuedAt").is_some_and(node_191)
                    && o.get("revocationVersion").is_some_and(node_12)
                    && o.get("rootExpiresAt").is_some_and(node_191)
                    && o.get("rootVersion").is_some_and(node_12)
                    && o.keys().all(|k| {
                        [
                            "anchor",
                            "catalogExpiresAt",
                            "evalHighWater",
                            "indexSnapshotVersion",
                            "lastAccepted",
                            "pendingRecoveryChallenge",
                            "recoveryEpochSerial",
                            "revocationIssuedAt",
                            "revocationVersion",
                            "rootExpiresAt",
                            "rootVersion",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_348(v: &V) -> bool {
    (usize::from(node_9(v)) + usize::from(node_349(v))) == 1
}
fn node_349(v: &V) -> bool {
    node_287(v)
}
fn node_350(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("blob").is_some_and(node_171)
                    && o.get("path").is_some_and(node_31)
                    && o.get("slot").is_some_and(node_351)
                    && o.keys()
                        .all(|k| ["blob", "path", "slot"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_351(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (matches!(v, V::String(s) if s == "envelopes")
            || matches!(v, V::String(s) if s == "manifests")
            || matches!(v, V::String(s) if s == "permissionPolicies"))
}
fn node_352(v: &V) -> bool {
    (usize::from(node_353(v)) + usize::from(node_355(v))) == 1
}
fn node_353(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("admittingRoot").is_some_and(node_4)
                    && o.get("historySchema").is_some_and(node_38)
                    && o.get("kind").is_some_and(node_354)
                    && o.get("list").is_some_and(node_19)
                    && o.get("prior").is_some_and(node_51)
                    && o.keys().all(|k| {
                        ["admittingRoot", "historySchema", "kind", "list", "prior"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_354(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "list"))
}
fn node_355(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("historySchema").is_some_and(node_38)
                    && o.get("kind").is_some_and(node_356)
                    && o.get("parents").is_some_and(node_357)
                    && o.keys()
                        .all(|k| ["historySchema", "kind", "parents"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_356(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "merge"))
}
fn node_357(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => a.len() >= 2 && a.len() <= 2 && unique(a) && a.iter().all(node_4),
            _ => true,
        })
}
fn node_358(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (matches!(v, V::String(s) if s == "namespace")
            || matches!(v, V::String(s) if s == "catalogSnapshot"))
}
fn node_359(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("after").is_some_and(node_290)
                    && o.get("before").is_some_and(node_290)
                    && o.get("role").is_some_and(node_11)
                    && o.keys()
                        .all(|k| ["after", "before", "role"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_360(v: &V) -> bool {
    (usize::from(node_361(v)) + usize::from(node_381(v))) == 1
}
fn node_361(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (node_362(v) && node_368(v))
        && (match v {
            V::Object(o) => {
                o.get("before").is_some_and(node_290)
                    && o.get("clock").is_some_and(node_376)
                    && o.get("event").is_some_and(node_377)
                    && o.get("eventSchema").is_some_and(node_5)
                    && o.get("from").is_some_and(node_378)
                    && o.get("kind").is_some_and(node_379)
                    && o.get("operation").is_some_and(node_4)
                    && o.get("outcome").is_some_and(node_374)
                    && o.get("payloadEvidence").is_some_and(node_380)
                    && o.get("previous").is_some_and(node_8)
                    && o.get("role").is_some_and(node_11)
                    && o.get("sequence").is_some_and(node_12)
                    && o.get("store").is_some_and(node_13)
                    && o.get("to").is_some_and(node_378)
                    && o.keys().all(|k| {
                        [
                            "before",
                            "clock",
                            "event",
                            "eventSchema",
                            "from",
                            "kind",
                            "operation",
                            "outcome",
                            "payloadEvidence",
                            "previous",
                            "role",
                            "sequence",
                            "store",
                            "to",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_362(v: &V) -> bool {
    if node_363(v) { node_366(v) } else { true }
}
fn node_363(v: &V) -> bool {
    match v {
        V::Object(o) => o.get("clock").is_none_or(node_364),
        _ => true,
    }
}
fn node_364(v: &V) -> bool {
    match v {
        V::Object(o) => o.get("kind").is_none_or(node_365),
        _ => true,
    }
}
fn node_365(v: &V) -> bool {
    matches!(v, V::String(s) if s == "observed-context")
}
fn node_366(v: &V) -> bool {
    match v {
        V::Object(o) => o.get("event").is_none_or(node_367),
        _ => true,
    }
}
fn node_367(v: &V) -> bool {
    matches!(v, V::String(s) if s == "EV-REVOKE")
        || matches!(v, V::String(s) if s == "EV-QUORUM-OBSERVE")
}
fn node_368(v: &V) -> bool {
    if node_369(v) { node_371(v) } else { true }
}
fn node_369(v: &V) -> bool {
    match v {
        V::Object(o) => o.get("clock").is_none_or(node_370),
        _ => true,
    }
}
fn node_370(v: &V) -> bool {
    match v {
        V::Object(o) => o.get("kind").is_none_or(node_63),
        _ => true,
    }
}
fn node_371(v: &V) -> bool {
    match v {
        V::Object(o) => {
            o.get("before").is_none_or(node_372)
                && o.get("event").is_none_or(node_373)
                && o.get("from").is_none_or(node_6)
                && o.get("outcome").is_none_or(node_374)
                && o.get("to").is_none_or(node_375)
        }
        _ => true,
    }
}
fn node_372(v: &V) -> bool {
    match v {
        V::Object(o) => o.get("accepted").is_none_or(node_9),
        _ => true,
    }
}
fn node_373(v: &V) -> bool {
    matches!(v, V::String(s) if s == "EV-RECOVER-ABORT")
}
fn node_374(v: &V) -> bool {
    matches!(v, V::String(s) if s == "accepted")
}
fn node_375(v: &V) -> bool {
    matches!(v, V::String(s) if s == "ST-UNBOOTSTRAPPED")
}
fn node_376(v: &V) -> bool {
    node_59(v)
}
fn node_377(v: &V) -> bool {
    node_549(v)
}
fn node_378(v: &V) -> bool {
    node_430(v)
}
fn node_379(v: &V) -> bool {
    matches!(v, V::String(s) if s == "role-event")
}
fn node_380(v: &V) -> bool {
    node_271(v)
}
fn node_381(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (node_362(v) && node_368(v))
        && (match v {
            V::Object(o) => {
                o.get("before").is_some_and(node_290)
                    && o.get("clock").is_some_and(node_376)
                    && o.get("event").is_some_and(node_377)
                    && o.get("eventSchema").is_some_and(node_5)
                    && o.get("from").is_some_and(node_378)
                    && o.get("kind").is_some_and(node_379)
                    && o.get("operation").is_some_and(node_4)
                    && o.get("outcome").is_some_and(node_382)
                    && o.get("payloadEvidence").is_some_and(node_380)
                    && o.get("previous").is_some_and(node_8)
                    && o.get("refusalReason").is_some_and(node_383)
                    && o.get("role").is_some_and(node_11)
                    && o.get("sequence").is_some_and(node_12)
                    && o.get("store").is_some_and(node_13)
                    && o.get("to").is_some_and(node_378)
                    && o.keys().all(|k| {
                        [
                            "before",
                            "clock",
                            "event",
                            "eventSchema",
                            "from",
                            "kind",
                            "operation",
                            "outcome",
                            "payloadEvidence",
                            "previous",
                            "refusalReason",
                            "role",
                            "sequence",
                            "store",
                            "to",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_382(v: &V) -> bool {
    matches!(v, V::String(s) if s == "refused")
}
fn node_383(v: &V) -> bool {
    node_550(v)
}
fn node_384(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("accepted").is_some_and(node_385)
                    && o.get("ceremony").is_some_and(node_387)
                    && o.get("conditionEvidence").is_some_and(node_389)
                    && o.get("reset").is_some_and(node_390)
                    && o.get("state").is_some_and(node_378)
                    && o.keys().all(|k| {
                        [
                            "accepted",
                            "ceremony",
                            "conditionEvidence",
                            "reset",
                            "state",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_385(v: &V) -> bool {
    (usize::from(node_386(v)) + usize::from(node_9(v))) == 1
}
fn node_386(v: &V) -> bool {
    node_22(v)
}
fn node_387(v: &V) -> bool {
    (usize::from(node_388(v)) + usize::from(node_9(v))) == 1
}
fn node_388(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("batch").is_some_and(node_4)
                    && o.get("begin").is_some_and(node_3)
                    && o.keys().all(|k| ["batch", "begin"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_389(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("quorumLostBy").is_some_and(node_8)
                    && o.get("revokedBy").is_some_and(node_8)
                    && o.keys()
                        .all(|k| ["quorumLostBy", "revokedBy"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_390(v: &V) -> bool {
    (usize::from(node_391(v)) + usize::from(node_9(v))) == 1
}
fn node_391(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("by").is_some_and(node_3)
                    && o.get("cause").is_some_and(node_291)
                    && o.keys().all(|k| ["by", "cause"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_392(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (matches!(v, V::String(s) if s == "TR-BUNDLE")
            || matches!(v, V::String(s) if s == "TR-COMPONENT")
            || matches!(v, V::String(s) if s == "TR-CORE")
            || matches!(v, V::String(s) if s == "TR-INDEX")
            || matches!(v, V::String(s) if s == "TR-PROFILE")
            || matches!(v, V::String(s) if s == "TR-REPAIR"))
}
fn node_393(v: &V) -> bool {
    (usize::from(node_394(v)) + usize::from(node_395(v)) + usize::from(node_397(v))) == 1
}
fn node_394(v: &V) -> bool {
    node_128(v)
}
fn node_395(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("admissionSchema").is_some_and(node_38)
                    && o.get("binding").is_some_and(node_21)
                    && o.get("context").is_some_and(node_211)
                    && o.get("kind").is_some_and(node_396)
                    && o.get("parent").is_some_and(node_4)
                    && o.get("root").is_some_and(node_19)
                    && o.keys().all(|k| {
                        [
                            "admissionSchema",
                            "binding",
                            "context",
                            "kind",
                            "parent",
                            "root",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_396(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "ordinary"))
}
fn node_397(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("admissionSchema").is_some_and(node_38)
                    && o.get("authorization").is_some_and(node_19)
                    && o.get("binding").is_some_and(node_21)
                    && o.get("closure").is_some_and(node_4)
                    && o.get("context").is_some_and(node_211)
                    && o.get("kind").is_some_and(node_398)
                    && o.get("parent").is_some_and(node_4)
                    && o.get("root").is_some_and(node_19)
                    && o.keys().all(|k| {
                        [
                            "admissionSchema",
                            "authorization",
                            "binding",
                            "closure",
                            "context",
                            "kind",
                            "parent",
                            "root",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_398(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "recovery"))
}
fn node_399(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("rootDigest").is_some_and(node_400)
                    && o.get("rootSchema").is_some_and(node_401)
                    && o.get("rootVersion").is_some_and(node_178)
                    && o.keys()
                        .all(|k| ["rootDigest", "rootSchema", "rootVersion"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_400(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => {
                s.chars().count() >= 64 && s.chars().count() <= 64 && hex(dollar(s), 64)
            }
            _ => true,
        })
}
fn node_401(v: &V) -> bool {
    (matches!(v, V::Integer(_)))
        && (matches!(v, V::Integer(n) if n.get() == 1_i128)
            || matches!(v, V::Integer(n) if n.get() == 2_i128))
}
fn node_402(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("keys").is_some_and(node_403)
                    && o.get("namespaces").is_some_and(node_404)
                    && o.get("standing").is_none_or(node_405)
                    && o.get("threshold").is_some_and(node_406)
                    && o.keys().all(|k| {
                        ["keys", "namespaces", "standing", "threshold"].contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_403(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => a.len() <= 8 && unique(a) && a.iter().all(node_32),
            _ => true,
        })
}
fn node_404(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => a.len() <= 16 && unique(a) && a.iter().all(node_25),
            _ => true,
        })
}
fn node_405(v: &V) -> bool {
    matches!(v, V::String(s) if s == "active")
        || matches!(v, V::String(s) if s == "typed-absence-DR-110")
}
fn node_406(v: &V) -> bool {
    (matches!(v, V::Integer(_)))
        && (match v {
            V::Integer(n) => n.get() >= 0_i128 && n.get() <= 8_i128,
            _ => true,
        })
}
fn node_407(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("beforeImage").is_some_and(node_4)
                    && o.get("beforeRecord").is_some_and(node_75)
                    && o.get("inputSchema").is_some_and(node_38)
                    && o.get("invocation").is_some_and(node_225)
                    && o.get("kind").is_some_and(node_112)
                    && o.get("nonce").is_some_and(node_32)
                    && o.get("observation").is_some_and(node_160)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        [
                            "beforeImage",
                            "beforeRecord",
                            "inputSchema",
                            "invocation",
                            "kind",
                            "nonce",
                            "observation",
                            "store",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_408(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("acceptedAuthority").is_some_and(node_4)
                    && o.get("beforeImage").is_some_and(node_4)
                    && o.get("beforeRecord").is_some_and(node_75)
                    && o.get("epoch").is_some_and(node_19)
                    && o.get("inputSchema").is_some_and(node_38)
                    && o.get("invocation").is_some_and(node_225)
                    && o.get("kind").is_some_and(node_409)
                    && o.get("observation").is_some_and(node_160)
                    && o.get("revocationHistory").is_some_and(node_4)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        [
                            "acceptedAuthority",
                            "beforeImage",
                            "beforeRecord",
                            "epoch",
                            "inputSchema",
                            "invocation",
                            "kind",
                            "observation",
                            "revocationHistory",
                            "store",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_409(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "s4.5-epoch"))
}
fn node_410(v: &V) -> bool {
    (usize::from(node_411(v)) + usize::from(node_412(v))) == 1
}
fn node_411(v: &V) -> bool {
    node_413(v)
}
fn node_412(v: &V) -> bool {
    node_416(v)
}
fn node_413(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("beforeClock").is_some_and(node_48)
                    && o.get("beforeImage").is_some_and(node_4)
                    && o.get("inputSchema").is_some_and(node_38)
                    && o.get("invocation").is_some_and(node_225)
                    && o.get("kind").is_some_and(node_414)
                    && o.get("observation").is_some_and(node_160)
                    && o.get("source").is_some_and(node_415)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        [
                            "beforeClock",
                            "beforeImage",
                            "inputSchema",
                            "invocation",
                            "kind",
                            "observation",
                            "source",
                            "store",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_414(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "s4-evaluation"))
}
fn node_415(v: &V) -> bool {
    node_418(v)
}
fn node_416(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("authority").is_some_and(node_4)
                    && o.get("beforeClock").is_some_and(node_48)
                    && o.get("beforeImage").is_some_and(node_4)
                    && o.get("inputSchema").is_some_and(node_134)
                    && o.get("invocation").is_some_and(node_225)
                    && o.get("kind").is_some_and(node_414)
                    && o.get("observation").is_some_and(node_160)
                    && o.get("source").is_some_and(node_415)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        [
                            "authority",
                            "beforeClock",
                            "beforeImage",
                            "inputSchema",
                            "invocation",
                            "kind",
                            "observation",
                            "source",
                            "store",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_417(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => {
                s.chars().count() >= 1 && s.chars().count() <= 1024 && signed_path_shape(s)
            }
            _ => true,
        })
}
fn node_418(v: &V) -> bool {
    (usize::from(node_419(v)) + usize::from(node_421(v)) + usize::from(node_422(v))) == 1
}
fn node_419(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("kind").is_some_and(node_420)
                    && o.keys().all(|k| ["kind"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_420(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "none"))
}
fn node_421(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("closure").is_some_and(node_4)
                    && o.get("kind").is_some_and(node_396)
                    && o.keys().all(|k| ["closure", "kind"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_422(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("closure").is_some_and(node_4)
                    && o.get("kind").is_some_and(node_398)
                    && o.keys().all(|k| ["closure", "kind"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_423(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("TR-BUNDLE").is_some_and(node_290)
                    && o.get("TR-COMPONENT").is_some_and(node_290)
                    && o.get("TR-CORE").is_some_and(node_290)
                    && o.get("TR-INDEX").is_some_and(node_290)
                    && o.get("TR-PROFILE").is_some_and(node_290)
                    && o.get("TR-REPAIR").is_some_and(node_290)
                    && o.keys().all(|k| {
                        [
                            "TR-BUNDLE",
                            "TR-COMPONENT",
                            "TR-CORE",
                            "TR-INDEX",
                            "TR-PROFILE",
                            "TR-REPAIR",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_424(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => tag_hex(s, "snapshot2:", 64),
            _ => true,
        })
}
fn node_425(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("by").is_some_and(node_3)
                    && o.get("executionId").is_some_and(node_120)
                    && o.get("intentDigest").is_some_and(node_32)
                    && o.get("sourceBefore").is_some_and(node_32)
                    && o.keys().all(|k| {
                        ["by", "executionId", "intentDigest", "sourceBefore"].contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_426(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("authorization").is_some_and(node_19)
                    && o.get("by").is_some_and(node_3)
                    && o.get("closure").is_some_and(node_4)
                    && o.get("payload").is_some_and(node_19)
                    && o.keys().all(|k| {
                        ["authorization", "by", "closure", "payload"].contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_427(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("before").is_some_and(node_290)
                    && o.get("cause").is_some_and(node_291)
                    && o.get("eventSchema").is_some_and(node_5)
                    && o.get("from").is_some_and(node_378)
                    && o.get("kind").is_some_and(node_428)
                    && o.get("operation").is_some_and(node_4)
                    && o.get("previous").is_some_and(node_8)
                    && o.get("role").is_some_and(node_11)
                    && o.get("sequence").is_some_and(node_12)
                    && o.get("store").is_some_and(node_13)
                    && o.get("to").is_some_and(node_375)
                    && o.keys().all(|k| {
                        [
                            "before",
                            "cause",
                            "eventSchema",
                            "from",
                            "kind",
                            "operation",
                            "previous",
                            "role",
                            "sequence",
                            "store",
                            "to",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_428(v: &V) -> bool {
    matches!(v, V::String(s) if s == "standing-reset")
}
fn node_429(v: &V) -> bool {
    matches!(v, V::Integer(n) if n.get() == 1_i128)
        || matches!(v, V::Integer(n) if n.get() == 2_i128)
}
fn node_430(v: &V) -> bool {
    matches!(v, V::String(s) if s == "ST-UNBOOTSTRAPPED")
        || matches!(v, V::String(s) if s == "ST-TRUSTED")
        || matches!(v, V::String(s) if s == "ST-EXPIRED")
        || matches!(v, V::String(s) if s == "ST-STALE-REVOCATION")
        || matches!(v, V::String(s) if s == "ST-QUORUM-LOST")
        || matches!(v, V::String(s) if s == "ST-REVOKED")
        || matches!(v, V::String(s) if s == "ST-RECOVERY")
}
fn node_431(v: &V) -> bool {
    (matches!(v, V::Integer(_)))
        && (match v {
            V::Integer(n) => n.get() >= 0_i128 && n.get() <= 63_i128,
            _ => true,
        })
}
fn node_432(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("stateSchema").is_some_and(node_164)
                    && o.get("storeGeneration").is_some_and(node_28)
                    && o.get("storeInstanceId").is_some_and(node_13)
                    && o.keys().all(|k| {
                        ["stateSchema", "storeGeneration", "storeInstanceId"].contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_433(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("schemaVersion").is_some_and(node_38)
                    && o.get("storeInstanceId").is_some_and(node_13)
                    && o.keys()
                        .all(|k| ["schemaVersion", "storeInstanceId"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_434(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => a.len() <= 4096 && a.iter().all(node_303),
            _ => true,
        })
}
fn node_435(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("initialBucketForeignNames").is_some_and(node_28)
                    && o.get("inputSchema").is_some_and(node_38)
                    && o.get("intent").is_some_and(node_4)
                    && o.get("invocation").is_some_and(node_225)
                    && o.get("kind").is_some_and(node_436)
                    && o.get("observation").is_some_and(node_160)
                    && o.get("source").is_some_and(node_57)
                    && o.get("target").is_some_and(node_57)
                    && o.keys().all(|k| {
                        [
                            "initialBucketForeignNames",
                            "inputSchema",
                            "intent",
                            "invocation",
                            "kind",
                            "observation",
                            "source",
                            "target",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_436(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "target-absence-input"))
}
fn node_437(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("architecture").is_some_and(node_438)
                    && o.get("filesystemWhereItAffectsResolution")
                        .is_some_and(node_439)
                    && o.get("inapplicabilityProofs").is_some_and(node_440)
                    && o.get("osFamily").is_some_and(node_444)
                    && o.get("platformProfileKey").is_some_and(node_445)
                    && o.get("runnerRequirements").is_some_and(node_446)
                    && o.get("signedEntries").is_some_and(node_448)
                    && o.get("supportedVersionOrBuildSelector")
                        .is_some_and(node_493)
                    && o.get("templateSchema").is_some_and(node_5)
                    && o.keys().all(|k| {
                        [
                            "architecture",
                            "filesystemWhereItAffectsResolution",
                            "inapplicabilityProofs",
                            "osFamily",
                            "platformProfileKey",
                            "runnerRequirements",
                            "signedEntries",
                            "supportedVersionOrBuildSelector",
                            "templateSchema",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_438(v: &V) -> bool {
    matches!(v, V::String(s) if s == "arm64") || matches!(v, V::String(s) if s == "x86_64")
}
fn node_439(v: &V) -> bool {
    matches!(v, V::String(s) if s == "apfs")
        || matches!(v, V::String(s) if s == "hfs-plus")
        || matches!(v, V::String(s) if s == "ext4")
        || matches!(v, V::String(s) if s == "xfs")
        || matches!(v, V::String(s) if s == "btrfs")
        || matches!(v, V::String(s) if s == "tmpfs")
}
fn node_440(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => a.len() <= 16 && a.iter().all(node_441),
            _ => true,
        })
}
fn node_441(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("class").is_some_and(node_442)
                    && o.get("probe").is_some_and(node_443)
                    && o.get("reason").is_some_and(node_443)
                    && o.keys()
                        .all(|k| ["class", "probe", "reason"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_442(v: &V) -> bool {
    matches!(v, V::String(s) if s == "loader")
        || matches!(v, V::String(s) if s == "libc")
        || matches!(v, V::String(s) if s == "framework")
        || matches!(v, V::String(s) if s == "certificate store")
        || matches!(v, V::String(s) if s == "font")
        || matches!(v, V::String(s) if s == "ICU")
        || matches!(v, V::String(s) if s == "comparable system-class dependency")
}
fn node_443(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => s.chars().count() >= 1 && s.chars().count() <= 1024,
            _ => true,
        })
}
fn node_444(v: &V) -> bool {
    matches!(v, V::String(s) if s == "macos") || matches!(v, V::String(s) if s == "linux")
}
fn node_445(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => s.chars().count() >= 1 && s.chars().count() <= 128 && platform(s),
            _ => true,
        })
}
fn node_446(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => a.len() <= 16 && a.iter().all(node_447),
            _ => true,
        })
}
fn node_447(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => s.chars().count() >= 1 && s.chars().count() <= 512,
            _ => true,
        })
}
fn node_448(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => !a.is_empty() && a.len() <= 64 && a.iter().all(node_449),
            _ => true,
        })
}
fn node_449(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("class").is_some_and(node_450)
                    && o.get("identityEvidence").is_some_and(node_451)
                    && o.get("originSearchPolicy").is_some_and(node_466)
                    && o.get("platformProfileKey").is_some_and(node_195)
                    && o.get("schemeStanding").is_none_or(node_491)
                    && o.get("valueSource").is_some_and(node_492)
                    && o.keys().all(|k| {
                        [
                            "class",
                            "identityEvidence",
                            "originSearchPolicy",
                            "platformProfileKey",
                            "schemeStanding",
                            "valueSource",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_450(v: &V) -> bool {
    matches!(v, V::String(s) if s == "OS ABI")
        || matches!(v, V::String(s) if s == "loader")
        || matches!(v, V::String(s) if s == "libc")
        || matches!(v, V::String(s) if s == "framework")
        || matches!(v, V::String(s) if s == "certificate store")
        || matches!(v, V::String(s) if s == "font")
        || matches!(v, V::String(s) if s == "ICU")
        || matches!(v, V::String(s) if s == "comparable system-class dependency")
}
fn node_451(v: &V) -> bool {
    (usize::from(node_452(v)) + usize::from(node_458(v))) == 1
}
fn node_452(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("tag").is_some_and(node_453)
                    && o.get("value").is_some_and(node_454)
                    && o.keys().all(|k| ["tag", "value"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_453(v: &V) -> bool {
    matches!(v, V::String(s) if s == "PLATFORM-ATTESTED")
}
fn node_454(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("authenticityCore").is_some_and(node_455)
                    && o.get("sonameAbi").is_none_or(node_457)
                    && o.keys()
                        .all(|k| ["authenticityCore", "sonameAbi"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_455(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("payload").is_some_and(node_201)
                    && o.get("scheme").is_some_and(node_456)
                    && o.keys()
                        .all(|k| ["payload", "scheme"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_456(v: &V) -> bool {
    matches!(v, V::String(s) if s == "codesign")
        || matches!(v, V::String(s) if s == "package-db")
        || matches!(v, V::String(s) if s == "macos-sealed-boot")
}
fn node_457(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("abiSelector").is_some_and(node_195)
                    && o.get("soname").is_some_and(node_195)
                    && o.keys()
                        .all(|k| ["abiSelector", "soname"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_458(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("tag").is_some_and(node_459)
                    && o.get("value").is_some_and(node_460)
                    && o.keys().all(|k| ["tag", "value"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_459(v: &V) -> bool {
    matches!(v, V::String(s) if s == "DIGEST-BOUND")
}
fn node_460(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("algorithmId").is_some_and(node_461)
                    && o.get("digest").is_some_and(node_462)
                    && o.get("sonameAbi").is_none_or(node_457)
                    && o.keys()
                        .all(|k| ["algorithmId", "digest", "sonameAbi"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_461(v: &V) -> bool {
    matches!(v, V::String(s) if s == "sha-256")
}
fn node_462(v: &V) -> bool {
    (usize::from(node_400(v)) + usize::from(node_463(v))) == 1
}
fn node_463(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("$releaseMeasured").is_some_and(node_464)
                    && o.keys().all(|k| ["$releaseMeasured"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_464(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("field").is_some_and(node_465)
                    && o.get("form").is_some_and(node_195)
                    && o.get("source").is_some_and(node_447)
                    && o.keys()
                        .all(|k| ["field", "form", "source"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_465(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => s.chars().count() >= 1 && s.chars().count() <= 64,
            _ => true,
        })
}
fn node_466(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("allowedLoaderOrSearchOrder").is_some_and(node_467)
                    && o.get("classAppropriateLookup").is_some_and(node_468)
                    && o.get("environmentInfluence").is_some_and(node_469)
                    && o.get("volumeConstraint").is_some_and(node_475)
                    && o.keys().all(|k| {
                        [
                            "allowedLoaderOrSearchOrder",
                            "classAppropriateLookup",
                            "environmentInfluence",
                            "volumeConstraint",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_467(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => a.len() <= 16 && a.iter().all(node_443),
            _ => true,
        })
}
fn node_468(v: &V) -> bool {
    (matches!(v, V::String(_) | V::Null))
        && (match v {
            V::String(s) => s.chars().count() <= 512,
            _ => true,
        })
}
fn node_469(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => o
                .iter()
                .all(|(k, v)| [].contains(&k.as_str()) || node_470(v)),
            _ => true,
        })
}
fn node_470(v: &V) -> bool {
    (usize::from(node_471(v)) + usize::from(node_473(v))) == 1
}
fn node_471(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("standing").is_some_and(node_472)
                    && o.keys().all(|k| ["standing"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_472(v: &V) -> bool {
    matches!(v, V::String(s) if s == "FORBIDDEN")
}
fn node_473(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("expectedValue").is_some_and(node_443)
                    && o.get("standing").is_some_and(node_474)
                    && o.keys()
                        .all(|k| ["expectedValue", "standing"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_474(v: &V) -> bool {
    matches!(v, V::String(s) if s == "FIXED")
}
fn node_475(v: &V) -> bool {
    (usize::from(node_476(v))
        + usize::from(node_479(v))
        + usize::from(node_481(v))
        + usize::from(node_485(v)))
        == 1
}
fn node_476(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("canonicalOrigin").is_some_and(node_477)
                    && o.get("tag").is_some_and(node_478)
                    && o.keys()
                        .all(|k| ["canonicalOrigin", "tag"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_477(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => {
                s.chars().count() >= 1 && s.chars().count() <= 1024 && s.starts_with('/')
            }
            _ => true,
        })
}
fn node_478(v: &V) -> bool {
    matches!(v, V::String(s) if s == "EXTERNAL-ORIGIN")
}
fn node_479(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("tag").is_some_and(node_480)
                    && o.keys().all(|k| ["tag"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_480(v: &V) -> bool {
    matches!(v, V::String(s) if s == "INSTALL-ROOT-VOLUME")
}
fn node_481(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("pathlessObservation").is_some_and(node_482)
                    && o.get("tag").is_some_and(node_484)
                    && o.keys()
                        .all(|k| ["pathlessObservation", "tag"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_482(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("scheme").is_some_and(node_483)
                    && o.get("subject").is_some_and(node_201)
                    && o.keys()
                        .all(|k| ["scheme", "subject"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_483(v: &V) -> bool {
    matches!(v, V::String(s) if s == "codesign")
        || matches!(v, V::String(s) if s == "macos-sealed-boot")
}
fn node_484(v: &V) -> bool {
    matches!(v, V::String(s) if s == "PATHLESS-PLATFORM-ATTESTED")
}
fn node_485(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("builderPublicKey").is_some_and(node_462)
                    && o.get("builderRoot").is_some_and(node_201)
                    && o.get("builderRootDigest").is_some_and(node_462)
                    && o.get("builderSignature").is_some_and(node_486)
                    && o.get("ikconfigDigest").is_none_or(node_462)
                    && o.get("kexecCapability").is_some_and(node_488)
                    && o.get("measuredBootTranscriptDigest").is_some_and(node_462)
                    && o.get("pathlessObservation").is_some_and(node_489)
                    && o.get("tag").is_some_and(node_484)
                    && o.keys().all(|k| {
                        [
                            "builderPublicKey",
                            "builderRoot",
                            "builderRootDigest",
                            "builderSignature",
                            "ikconfigDigest",
                            "kexecCapability",
                            "measuredBootTranscriptDigest",
                            "pathlessObservation",
                            "tag",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_486(v: &V) -> bool {
    (usize::from(node_487(v)) + usize::from(node_463(v))) == 1
}
fn node_487(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => {
                s.chars().count() >= 128 && s.chars().count() <= 128 && hex(dollar(s), 128)
            }
            _ => true,
        })
}
fn node_488(v: &V) -> bool {
    matches!(v, V::String(s) if s == "kexec-absent")
}
fn node_489(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("scheme").is_some_and(node_490)
                    && o.get("subject").is_some_and(node_201)
                    && o.keys()
                        .all(|k| ["scheme", "subject"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_490(v: &V) -> bool {
    matches!(v, V::String(s) if s == "package-db")
}
fn node_491(v: &V) -> bool {
    matches!(v, V::String(s) if s == "v48")
        || matches!(v, V::String(s) if s == "v49-successor-required")
}
fn node_492(v: &V) -> bool {
    matches!(v, V::String(s) if s == "MEASURED-2026-09-04")
        || matches!(v, V::String(s) if s == "PUBLISHED-FACT")
        || matches!(v, V::String(s) if s == "RELEASE-MEASURED")
        || matches!(v, V::String(s) if s == "DECIDED")
}
fn node_493(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("canonicalIdentifier").is_some_and(node_195)
                    && o.get("identifierScheme").is_some_and(node_494)
                    && o.get("tag").is_some_and(node_495)
                    && o.get("valueSource").is_some_and(node_492)
                    && o.keys().all(|k| {
                        [
                            "canonicalIdentifier",
                            "identifierScheme",
                            "tag",
                            "valueSource",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_494(v: &V) -> bool {
    matches!(v, V::String(s) if s == "macos-product-build")
        || matches!(v, V::String(s) if s == "linux-distro-userspace")
}
fn node_495(v: &V) -> bool {
    matches!(v, V::String(s) if s == "EXACT-BUILD")
}
fn node_496(v: &V) -> bool {
    (usize::from(node_497(v)) + usize::from(node_498(v))) == 1
}
fn node_497(v: &V) -> bool {
    node_410(v)
}
fn node_498(v: &V) -> bool {
    node_408(v)
}
fn node_499(v: &V) -> bool {
    (usize::from(node_497(v))
        + usize::from(node_500(v))
        + usize::from(node_498(v))
        + usize::from(node_501(v)))
        == 1
}
fn node_500(v: &V) -> bool {
    node_344(v)
}
fn node_501(v: &V) -> bool {
    node_407(v)
}
fn node_502(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => s.chars().count() >= 20 && s.chars().count() <= 20 && timestamp(s),
            _ => true,
        })
}
fn node_503(v: &V) -> bool {
    node_189(v)
}
fn node_504(v: &V) -> bool {
    matches!(v, V::String(s) if s == "core-update")
        || matches!(v, V::String(s) if s == "core-repair")
        || matches!(v, V::String(s) if s == "core-rollback")
        || matches!(v, V::String(s) if s == "store-migrate")
        || matches!(v, V::String(s) if s == "store-rollback")
}
fn node_505(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => s.chars().count() <= 256 && transition(s),
            _ => true,
        })
}
fn node_506(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (matches!(v, V::String(s) if s == "absent")
            || matches!(v, V::String(s) if s == "coherent-terminal"))
}
fn node_507(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("entries").is_some_and(node_508)
                    && o.keys().all(|k| ["entries"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_508(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => !a.is_empty() && a.len() <= 100000 && a.iter().all(node_509),
            _ => true,
        })
}
fn node_509(v: &V) -> bool {
    node_510(v)
}
fn node_510(v: &V) -> bool {
    (usize::from(node_511(v)) + usize::from(node_514(v)) + usize::from(node_516(v))) == 1
}
fn node_511(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("length").is_some_and(node_28)
                    && o.get("mode").is_some_and(node_512)
                    && o.get("path").is_some_and(node_146)
                    && o.get("sha256").is_some_and(node_32)
                    && o.get("type").is_some_and(node_513)
                    && o.keys()
                        .all(|k| ["length", "mode", "path", "sha256", "type"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_512(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => mode(s),
            _ => true,
        })
}
fn node_513(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "file"))
}
fn node_514(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("mode").is_some_and(node_512)
                    && o.get("path").is_some_and(node_146)
                    && o.get("type").is_some_and(node_515)
                    && o.keys()
                        .all(|k| ["mode", "path", "type"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_515(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "dir"))
}
fn node_516(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("mode").is_some_and(node_512)
                    && o.get("path").is_some_and(node_146)
                    && o.get("target").is_some_and(node_146)
                    && o.get("type").is_some_and(node_517)
                    && o.keys()
                        .all(|k| ["mode", "path", "target", "type"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_517(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "symlink"))
}
fn node_518(v: &V) -> bool {
    (usize::from(node_519(v)) + usize::from(node_522(v)) + usize::from(node_524(v))) == 1
}
fn node_519(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("closure").is_some_and(node_129)
                    && o.get("inputSchema").is_some_and(node_38)
                    && o.get("kind").is_some_and(node_267)
                    && o.get("purpose").is_some_and(node_520)
                    && o.get("surface").is_some_and(node_521)
                    && o.keys().all(|k| {
                        ["closure", "inputSchema", "kind", "purpose", "surface"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_520(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "install"))
}
fn node_521(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "installed-component"))
}
fn node_522(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("closure").is_some_and(node_129)
                    && o.get("inputSchema").is_some_and(node_38)
                    && o.get("kind").is_some_and(node_267)
                    && o.get("purpose").is_some_and(node_523)
                    && o.get("surface").is_some_and(node_521)
                    && o.keys().all(|k| {
                        ["closure", "inputSchema", "kind", "purpose", "surface"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_523(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "continue"))
}
fn node_524(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("inputSchema").is_some_and(node_38)
                    && o.get("kind").is_some_and(node_267)
                    && o.get("purpose").is_some_and(node_525)
                    && o.keys()
                        .all(|k| ["inputSchema", "kind", "purpose"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_525(v: &V) -> bool {
    (matches!(v, V::String(_))) && (matches!(v, V::String(s) if s == "restrictive-observation"))
}
fn node_526(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("batch").is_some_and(node_46)
                    && o.get("capsuleSchema").is_some_and(node_38)
                    && o.get("clock").is_some_and(node_48)
                    && o.get("eventHead").is_some_and(node_8)
                    && o.get("heads").is_some_and(node_49)
                    && o.get("history").is_some_and(node_51)
                    && o.get("previous").is_some_and(node_52)
                    && o.get("publication").is_some_and(node_323)
                    && o.get("revision").is_some_and(node_12)
                    && o.get("roles").is_some_and(node_39)
                    && o.get("sourceFence").is_some_and(node_53)
                    && o.get("staged").is_some_and(node_55)
                    && o.get("store").is_some_and(node_57)
                    && o.keys().all(|k| {
                        [
                            "batch",
                            "capsuleSchema",
                            "clock",
                            "eventHead",
                            "heads",
                            "history",
                            "previous",
                            "publication",
                            "revision",
                            "roles",
                            "sourceFence",
                            "staged",
                            "store",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_527(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("kind").is_some_and(node_528)
                    && o.get("operation").is_some_and(node_4)
                    && o.get("outcomeSchema").is_some_and(node_5)
                    && o.get("receipt").is_some_and(node_529)
                    && o.get("scope").is_some_and(node_530)
                    && o.keys().all(|k| {
                        ["kind", "operation", "outcomeSchema", "receipt", "scope"]
                            .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_528(v: &V) -> bool {
    matches!(v, V::String(s) if s == "trust-command-outcome")
}
fn node_529(v: &V) -> bool {
    node_543(v)
}
fn node_530(v: &V) -> bool {
    node_184(v)
}
fn node_531(v: &V) -> bool {
    (usize::from(node_532(v))
        + usize::from(node_533(v))
        + usize::from(node_534(v))
        + usize::from(node_535(v))
        + usize::from(node_536(v))
        + usize::from(node_537(v))
        + usize::from(node_538(v))
        + usize::from(node_539(v))
        + usize::from(node_540(v)))
        == 1
}
fn node_532(v: &V) -> bool {
    node_360(v)
}
fn node_533(v: &V) -> bool {
    node_427(v)
}
fn node_534(v: &V) -> bool {
    node_289(v)
}
fn node_535(v: &V) -> bool {
    node_1(v)
}
fn node_536(v: &V) -> bool {
    node_33(v)
}
fn node_537(v: &V) -> bool {
    node_76(v)
}
fn node_538(v: &V) -> bool {
    node_156(v)
}
fn node_539(v: &V) -> bool {
    node_118(v)
}
fn node_540(v: &V) -> bool {
    node_326(v)
}
fn node_541(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("evalHighWater").is_some_and(node_191)
                    && o.get("indexSnapshotVersion").is_some_and(node_12)
                    && o.get("lastAccepted").is_some_and(node_191)
                    && o.get("recoveryEpochSerial").is_some_and(node_542)
                    && o.get("revocationVersion").is_some_and(node_12)
                    && o.get("rootVersion").is_some_and(node_12)
                    && o.keys().all(|k| {
                        [
                            "evalHighWater",
                            "indexSnapshotVersion",
                            "lastAccepted",
                            "recoveryEpochSerial",
                            "revocationVersion",
                            "rootVersion",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_542(v: &V) -> bool {
    (usize::from(node_28(v)) + usize::from(node_9(v))) == 1
}
fn node_543(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("commitClass").is_some_and(node_544)
                    && o.get("effectOutcome").is_some_and(node_545)
                    && o.get("executionId").is_some_and(node_120)
                    && o.get("idempotencyKey").is_some_and(node_44)
                    && o.get("operation").is_some_and(node_186)
                    && o.get("receiptId").is_some_and(node_546)
                    && o.get("replayed").is_some_and(node_547)
                    && o.get("requestId").is_some_and(node_187)
                    && o.get("schemaFamily").is_some_and(node_548)
                    && o.get("schemaMajor").is_some_and(node_5)
                    && o.get("stepId").is_some_and(node_188)
                    && o.keys().all(|k| {
                        [
                            "commitClass",
                            "effectOutcome",
                            "executionId",
                            "idempotencyKey",
                            "operation",
                            "receiptId",
                            "replayed",
                            "requestId",
                            "schemaFamily",
                            "schemaMajor",
                            "stepId",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_544(v: &V) -> bool {
    matches!(v, V::String(s) if s == "IRREVERSIBLE")
}
fn node_545(v: &V) -> bool {
    matches!(v, V::String(s) if s == "COMPLETED") || matches!(v, V::String(s) if s == "FAILED")
}
fn node_546(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (match v {
            V::String(s) => tag_hex(s, "receipt2:", 64),
            _ => true,
        })
}
fn node_547(v: &V) -> bool {
    matches!(v, V::Bool(false))
}
fn node_548(v: &V) -> bool {
    matches!(v, V::String(s) if s == "opensip.product.mutation-receipt")
}
fn node_549(v: &V) -> bool {
    matches!(v, V::String(s) if s == "EV-PRESENT-PAYLOAD")
        || matches!(v, V::String(s) if s == "EV-CLOCK")
        || matches!(v, V::String(s) if s == "EV-REVOKE")
        || matches!(v, V::String(s) if s == "EV-QUORUM-OBSERVE")
        || matches!(v, V::String(s) if s == "EV-RECOVER-BEGIN")
        || matches!(v, V::String(s) if s == "EV-RECOVER-COMMIT")
        || matches!(v, V::String(s) if s == "EV-INSTALL")
        || matches!(v, V::String(s) if s == "EV-CONTINUE")
        || matches!(v, V::String(s) if s == "EV-RECOVER-ABORT")
}
fn node_550(v: &V) -> bool {
    matches!(v, V::String(s) if s == "NO-MATCHING-GUARD")
        || matches!(v, V::String(s) if s == "REVOKE-NOT-NEWER-OR-INVALID")
        || matches!(v, V::String(s) if s == "PAYLOAD-NOT-ADMISSIBLE")
        || matches!(v, V::String(s) if s == "INSTALL-NOT-TRUSTED")
        || matches!(v, V::String(s) if s == "RECOVERY-BEGIN-REFUSED")
        || matches!(v, V::String(s) if s == "RECOVERY-COMMIT-REFUSED")
        || matches!(v, V::String(s) if s == "RECOVERY-ABORT-NOT-IN-CEREMONY")
        || matches!(v, V::String(s) if s == "ENVELOPE-INACTIVE")
        || matches!(v, V::String(s) if s == "CONTINUE-CORE-NOT-TRUSTED")
        || matches!(v, V::String(s) if s == "CONTINUE-INDEX-NOT-TRUSTED")
        || matches!(v, V::String(s) if s == "CONTINUE-COMPONENT-NOT-TRUSTED")
        || matches!(v, V::String(s) if s == "CONTINUE-UNMATCHED-COMBINATION")
        || matches!(v, V::String(s) if s == "CONTINUE-REPLAY-NOT-DESIGNED")
}
fn node_551(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("boundary").is_some_and(node_552)
                    && o.get("candidate").is_some_and(node_553)
                    && o.get("custody").is_some_and(node_554)
                    && o.get("path").is_some_and(node_214)
                    && o.keys()
                        .all(|k| ["boundary", "candidate", "custody", "path"].contains(&k.as_str()))
            }
            _ => true,
        })
}
fn node_552(v: &V) -> bool {
    matches!(v, V::Null)
        || matches!(v, V::String(s) if s == "EXPLICIT")
        || matches!(v, V::String(s) if s == "VCS")
        || matches!(v, V::String(s) if s == "HOME")
        || matches!(v, V::String(s) if s == "FS_ROOT")
        || matches!(v, V::String(s) if s == "MOUNT")
        || matches!(v, V::String(s) if s == "FOREIGN_OWNER")
        || matches!(v, V::String(s) if s == "WRITABLE_BY_OTHERS")
        || matches!(v, V::String(s) if s == "WRITABLE_BY_GROUP")
        || matches!(v, V::String(s) if s == "WRITABLE_BY_ACL")
        || matches!(v, V::String(s) if s == "ACL_UNREADABLE")
        || matches!(v, V::String(s) if s == "SYMLINK")
        || matches!(v, V::String(s) if s == "NOT_A_DIRECTORY")
        || matches!(v, V::String(s) if s == "ABSENT")
}
fn node_553(v: &V) -> bool {
    matches!(v, V::String(s) if s == "ABSENT")
        || matches!(v, V::String(s) if s == "PRESENT")
        || matches!(v, V::String(s) if s == "REFUSED")
        || matches!(v, V::String(s) if s == "NOT_EXAMINED")
}
fn node_554(v: &V) -> bool {
    matches!(v, V::String(s) if s == "PASS")
        || matches!(v, V::String(s) if s == "FOREIGN_OWNER")
        || matches!(v, V::String(s) if s == "WRITABLE_BY_OTHERS")
        || matches!(v, V::String(s) if s == "WRITABLE_BY_GROUP")
        || matches!(v, V::String(s) if s == "WRITABLE_BY_ACL")
        || matches!(v, V::String(s) if s == "ACL_UNREADABLE")
        || matches!(v, V::String(s) if s == "SYMLINK")
        || matches!(v, V::String(s) if s == "NOT_A_DIRECTORY")
        || matches!(v, V::String(s) if s == "ABSENT")
}
fn node_555(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("embeddedBootstrap").is_some_and(node_133)
                    && o.get("inventorySchema").is_some_and(node_556)
                    && o.get("platformProfileBinding").is_some_and(node_135)
                    && o.get("platforms").is_some_and(node_557)
                    && o.get("protocolMajor").is_some_and(node_28)
                    && o.get("semanticVersion").is_some_and(node_138)
                    && o.get("servedProtocolMajors").is_some_and(node_139)
                    && o.get("tcbProfiles").is_some_and(node_140)
                    && o.get("verifiedInstallRoot").is_some_and(node_142)
                    && o.keys().all(|k| {
                        [
                            "embeddedBootstrap",
                            "inventorySchema",
                            "platformProfileBinding",
                            "platforms",
                            "protocolMajor",
                            "semanticVersion",
                            "servedProtocolMajors",
                            "tcbProfiles",
                            "verifiedInstallRoot",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_556(v: &V) -> bool {
    (matches!(v, V::Integer(_))) && (matches!(v, V::Integer(n) if n.get() == 3_i128))
}
fn node_557(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => !a.is_empty() && a.len() <= 4 && a.iter().all(node_558),
            _ => true,
        })
}
fn node_558(v: &V) -> bool {
    node_559(v)
}
fn node_559(v: &V) -> bool {
    (matches!(v, V::Object(_)))
        && (match v {
            V::Object(o) => {
                o.get("entrypoint").is_some_and(node_146)
                    && o.get("layers").is_some_and(node_147)
                    && o.get("platform").is_some_and(node_131)
                    && o.get("requiredCodeSigningFlags").is_some_and(node_560)
                    && o.get("requires").is_some_and(node_151)
                    && o.get("stateWriter").is_some_and(node_401)
                    && o.get("tree").is_some_and(node_153)
                    && o.keys().all(|k| {
                        [
                            "entrypoint",
                            "layers",
                            "platform",
                            "requiredCodeSigningFlags",
                            "requires",
                            "stateWriter",
                            "tree",
                        ]
                        .contains(&k.as_str())
                    })
            }
            _ => true,
        })
}
fn node_560(v: &V) -> bool {
    (matches!(v, V::Array(_)))
        && (match v {
            V::Array(a) => {
                !a.is_empty()
                    && a.len() <= 16
                    && unique(a)
                    && a.iter().all(node_562)
                    && a.iter().any(node_561)
                    && ordered(a, &[])
            }
            _ => true,
        })
}
fn node_561(v: &V) -> bool {
    matches!(v, V::String(s) if s == "CS_VALID")
}
fn node_562(v: &V) -> bool {
    (matches!(v, V::String(_)))
        && (matches!(v, V::String(s) if s == "CS_VALID")
            || matches!(v, V::String(s) if s == "CS_HARD")
            || matches!(v, V::String(s) if s == "CS_KILL")
            || matches!(v, V::String(s) if s == "CS_RESTRICT")
            || matches!(v, V::String(s) if s == "CS_ENFORCEMENT")
            || matches!(v, V::String(s) if s == "CS_REQUIRE_LV")
            || matches!(v, V::String(s) if s == "CS_RUNTIME"))
}
pub(super) fn fragment(i: usize, v: &V) -> bool {
    match i {
        0 => node_0(v),
        1 => node_1(v),
        2 => node_2(v),
        3 => node_3(v),
        4 => node_4(v),
        5 => node_5(v),
        6 => node_6(v),
        7 => node_7(v),
        8 => node_8(v),
        9 => node_9(v),
        10 => node_10(v),
        11 => node_11(v),
        12 => node_12(v),
        13 => node_13(v),
        14 => node_14(v),
        15 => node_15(v),
        16 => node_16(v),
        17 => node_17(v),
        18 => node_18(v),
        19 => node_19(v),
        20 => node_20(v),
        21 => node_21(v),
        22 => node_22(v),
        23 => node_23(v),
        24 => node_24(v),
        25 => node_25(v),
        26 => node_26(v),
        27 => node_27(v),
        28 => node_28(v),
        29 => node_29(v),
        30 => node_30(v),
        31 => node_31(v),
        32 => node_32(v),
        33 => node_33(v),
        34 => node_34(v),
        35 => node_35(v),
        36 => node_36(v),
        37 => node_37(v),
        38 => node_38(v),
        39 => node_39(v),
        40 => node_40(v),
        41 => node_41(v),
        42 => node_42(v),
        43 => node_43(v),
        44 => node_44(v),
        45 => node_45(v),
        46 => node_46(v),
        47 => node_47(v),
        48 => node_48(v),
        49 => node_49(v),
        50 => node_50(v),
        51 => node_51(v),
        52 => node_52(v),
        53 => node_53(v),
        54 => node_54(v),
        55 => node_55(v),
        56 => node_56(v),
        57 => node_57(v),
        58 => node_58(v),
        59 => node_59(v),
        60 => node_60(v),
        61 => node_61(v),
        62 => node_62(v),
        63 => node_63(v),
        64 => node_64(v),
        65 => node_65(v),
        66 => node_66(v),
        67 => node_67(v),
        68 => node_68(v),
        69 => node_69(v),
        70 => node_70(v),
        71 => node_71(v),
        72 => node_72(v),
        73 => node_73(v),
        74 => node_74(v),
        75 => node_75(v),
        76 => node_76(v),
        77 => node_77(v),
        78 => node_78(v),
        79 => node_79(v),
        80 => node_80(v),
        81 => node_81(v),
        82 => node_82(v),
        83 => node_83(v),
        84 => node_84(v),
        85 => node_85(v),
        86 => node_86(v),
        87 => node_87(v),
        88 => node_88(v),
        89 => node_89(v),
        90 => node_90(v),
        91 => node_91(v),
        92 => node_92(v),
        93 => node_93(v),
        94 => node_94(v),
        95 => node_95(v),
        96 => node_96(v),
        97 => node_97(v),
        98 => node_98(v),
        99 => node_99(v),
        100 => node_100(v),
        101 => node_101(v),
        102 => node_102(v),
        103 => node_103(v),
        104 => node_104(v),
        105 => node_105(v),
        106 => node_106(v),
        107 => node_107(v),
        108 => node_108(v),
        109 => node_109(v),
        110 => node_110(v),
        111 => node_111(v),
        112 => node_112(v),
        113 => node_113(v),
        114 => node_114(v),
        115 => node_115(v),
        116 => node_116(v),
        117 => node_117(v),
        118 => node_118(v),
        119 => node_119(v),
        120 => node_120(v),
        121 => node_121(v),
        122 => node_122(v),
        123 => node_123(v),
        124 => node_124(v),
        125 => node_125(v),
        126 => node_126(v),
        127 => node_127(v),
        128 => node_128(v),
        129 => node_129(v),
        130 => node_130(v),
        131 => node_131(v),
        132 => node_132(v),
        133 => node_133(v),
        134 => node_134(v),
        135 => node_135(v),
        136 => node_136(v),
        137 => node_137(v),
        138 => node_138(v),
        139 => node_139(v),
        140 => node_140(v),
        141 => node_141(v),
        142 => node_142(v),
        143 => node_143(v),
        144 => node_144(v),
        145 => node_145(v),
        146 => node_146(v),
        147 => node_147(v),
        148 => node_148(v),
        149 => node_149(v),
        150 => node_150(v),
        151 => node_151(v),
        152 => node_152(v),
        153 => node_153(v),
        154 => node_154(v),
        155 => node_155(v),
        156 => node_156(v),
        157 => node_157(v),
        158 => node_158(v),
        159 => node_159(v),
        160 => node_160(v),
        161 => node_161(v),
        162 => node_162(v),
        163 => node_163(v),
        164 => node_164(v),
        165 => node_165(v),
        166 => node_166(v),
        167 => node_167(v),
        168 => node_168(v),
        169 => node_169(v),
        170 => node_170(v),
        171 => node_171(v),
        172 => node_172(v),
        173 => node_173(v),
        174 => node_174(v),
        175 => node_175(v),
        176 => node_176(v),
        177 => node_177(v),
        178 => node_178(v),
        179 => node_179(v),
        180 => node_180(v),
        181 => node_181(v),
        182 => node_182(v),
        183 => node_183(v),
        184 => node_184(v),
        185 => node_185(v),
        186 => node_186(v),
        187 => node_187(v),
        188 => node_188(v),
        189 => node_189(v),
        190 => node_190(v),
        191 => node_191(v),
        192 => node_192(v),
        193 => node_193(v),
        194 => node_194(v),
        195 => node_195(v),
        196 => node_196(v),
        197 => node_197(v),
        198 => node_198(v),
        199 => node_199(v),
        200 => node_200(v),
        201 => node_201(v),
        202 => node_202(v),
        203 => node_203(v),
        204 => node_204(v),
        205 => node_205(v),
        206 => node_206(v),
        207 => node_207(v),
        208 => node_208(v),
        209 => node_209(v),
        210 => node_210(v),
        211 => node_211(v),
        212 => node_212(v),
        213 => node_213(v),
        214 => node_214(v),
        215 => node_215(v),
        216 => node_216(v),
        217 => node_217(v),
        218 => node_218(v),
        219 => node_219(v),
        220 => node_220(v),
        221 => node_221(v),
        222 => node_222(v),
        223 => node_223(v),
        224 => node_224(v),
        225 => node_225(v),
        226 => node_226(v),
        227 => node_227(v),
        228 => node_228(v),
        229 => node_229(v),
        230 => node_230(v),
        231 => node_231(v),
        232 => node_232(v),
        233 => node_233(v),
        234 => node_234(v),
        235 => node_235(v),
        236 => node_236(v),
        237 => node_237(v),
        238 => node_238(v),
        239 => node_239(v),
        240 => node_240(v),
        241 => node_241(v),
        242 => node_242(v),
        243 => node_243(v),
        244 => node_244(v),
        245 => node_245(v),
        246 => node_246(v),
        247 => node_247(v),
        248 => node_248(v),
        249 => node_249(v),
        250 => node_250(v),
        251 => node_251(v),
        252 => node_252(v),
        253 => node_253(v),
        254 => node_254(v),
        255 => node_255(v),
        256 => node_256(v),
        257 => node_257(v),
        258 => node_258(v),
        259 => node_259(v),
        260 => node_260(v),
        261 => node_261(v),
        262 => node_262(v),
        263 => node_263(v),
        264 => node_264(v),
        265 => node_265(v),
        266 => node_266(v),
        267 => node_267(v),
        268 => node_268(v),
        269 => node_269(v),
        270 => node_270(v),
        271 => node_271(v),
        272 => node_272(v),
        273 => node_273(v),
        274 => node_274(v),
        275 => node_275(v),
        276 => node_276(v),
        277 => node_277(v),
        278 => node_278(v),
        279 => node_279(v),
        280 => node_280(v),
        281 => node_281(v),
        282 => node_282(v),
        283 => node_283(v),
        284 => node_284(v),
        285 => node_285(v),
        286 => node_286(v),
        287 => node_287(v),
        288 => node_288(v),
        289 => node_289(v),
        290 => node_290(v),
        291 => node_291(v),
        292 => node_292(v),
        293 => node_293(v),
        294 => node_294(v),
        295 => node_295(v),
        296 => node_296(v),
        297 => node_297(v),
        298 => node_298(v),
        299 => node_299(v),
        300 => node_300(v),
        301 => node_301(v),
        302 => node_302(v),
        303 => node_303(v),
        304 => node_304(v),
        305 => node_305(v),
        306 => node_306(v),
        307 => node_307(v),
        308 => node_308(v),
        309 => node_309(v),
        310 => node_310(v),
        311 => node_311(v),
        312 => node_312(v),
        313 => node_313(v),
        314 => node_314(v),
        315 => node_315(v),
        316 => node_316(v),
        317 => node_317(v),
        318 => node_318(v),
        319 => node_319(v),
        320 => node_320(v),
        321 => node_321(v),
        322 => node_322(v),
        323 => node_323(v),
        324 => node_324(v),
        325 => node_325(v),
        326 => node_326(v),
        327 => node_327(v),
        328 => node_328(v),
        329 => node_329(v),
        330 => node_330(v),
        331 => node_331(v),
        332 => node_332(v),
        333 => node_333(v),
        334 => node_334(v),
        335 => node_335(v),
        336 => node_336(v),
        337 => node_337(v),
        338 => node_338(v),
        339 => node_339(v),
        340 => node_340(v),
        341 => node_341(v),
        342 => node_342(v),
        343 => node_343(v),
        344 => node_344(v),
        345 => node_345(v),
        346 => node_346(v),
        347 => node_347(v),
        348 => node_348(v),
        349 => node_349(v),
        350 => node_350(v),
        351 => node_351(v),
        352 => node_352(v),
        353 => node_353(v),
        354 => node_354(v),
        355 => node_355(v),
        356 => node_356(v),
        357 => node_357(v),
        358 => node_358(v),
        359 => node_359(v),
        360 => node_360(v),
        361 => node_361(v),
        362 => node_362(v),
        363 => node_363(v),
        364 => node_364(v),
        365 => node_365(v),
        366 => node_366(v),
        367 => node_367(v),
        368 => node_368(v),
        369 => node_369(v),
        370 => node_370(v),
        371 => node_371(v),
        372 => node_372(v),
        373 => node_373(v),
        374 => node_374(v),
        375 => node_375(v),
        376 => node_376(v),
        377 => node_377(v),
        378 => node_378(v),
        379 => node_379(v),
        380 => node_380(v),
        381 => node_381(v),
        382 => node_382(v),
        383 => node_383(v),
        384 => node_384(v),
        385 => node_385(v),
        386 => node_386(v),
        387 => node_387(v),
        388 => node_388(v),
        389 => node_389(v),
        390 => node_390(v),
        391 => node_391(v),
        392 => node_392(v),
        393 => node_393(v),
        394 => node_394(v),
        395 => node_395(v),
        396 => node_396(v),
        397 => node_397(v),
        398 => node_398(v),
        399 => node_399(v),
        400 => node_400(v),
        401 => node_401(v),
        402 => node_402(v),
        403 => node_403(v),
        404 => node_404(v),
        405 => node_405(v),
        406 => node_406(v),
        407 => node_407(v),
        408 => node_408(v),
        409 => node_409(v),
        410 => node_410(v),
        411 => node_411(v),
        412 => node_412(v),
        413 => node_413(v),
        414 => node_414(v),
        415 => node_415(v),
        416 => node_416(v),
        417 => node_417(v),
        418 => node_418(v),
        419 => node_419(v),
        420 => node_420(v),
        421 => node_421(v),
        422 => node_422(v),
        423 => node_423(v),
        424 => node_424(v),
        425 => node_425(v),
        426 => node_426(v),
        427 => node_427(v),
        428 => node_428(v),
        429 => node_429(v),
        430 => node_430(v),
        431 => node_431(v),
        432 => node_432(v),
        433 => node_433(v),
        434 => node_434(v),
        435 => node_435(v),
        436 => node_436(v),
        437 => node_437(v),
        438 => node_438(v),
        439 => node_439(v),
        440 => node_440(v),
        441 => node_441(v),
        442 => node_442(v),
        443 => node_443(v),
        444 => node_444(v),
        445 => node_445(v),
        446 => node_446(v),
        447 => node_447(v),
        448 => node_448(v),
        449 => node_449(v),
        450 => node_450(v),
        451 => node_451(v),
        452 => node_452(v),
        453 => node_453(v),
        454 => node_454(v),
        455 => node_455(v),
        456 => node_456(v),
        457 => node_457(v),
        458 => node_458(v),
        459 => node_459(v),
        460 => node_460(v),
        461 => node_461(v),
        462 => node_462(v),
        463 => node_463(v),
        464 => node_464(v),
        465 => node_465(v),
        466 => node_466(v),
        467 => node_467(v),
        468 => node_468(v),
        469 => node_469(v),
        470 => node_470(v),
        471 => node_471(v),
        472 => node_472(v),
        473 => node_473(v),
        474 => node_474(v),
        475 => node_475(v),
        476 => node_476(v),
        477 => node_477(v),
        478 => node_478(v),
        479 => node_479(v),
        480 => node_480(v),
        481 => node_481(v),
        482 => node_482(v),
        483 => node_483(v),
        484 => node_484(v),
        485 => node_485(v),
        486 => node_486(v),
        487 => node_487(v),
        488 => node_488(v),
        489 => node_489(v),
        490 => node_490(v),
        491 => node_491(v),
        492 => node_492(v),
        493 => node_493(v),
        494 => node_494(v),
        495 => node_495(v),
        496 => node_496(v),
        497 => node_497(v),
        498 => node_498(v),
        499 => node_499(v),
        500 => node_500(v),
        501 => node_501(v),
        502 => node_502(v),
        503 => node_503(v),
        504 => node_504(v),
        505 => node_505(v),
        506 => node_506(v),
        507 => node_507(v),
        508 => node_508(v),
        509 => node_509(v),
        510 => node_510(v),
        511 => node_511(v),
        512 => node_512(v),
        513 => node_513(v),
        514 => node_514(v),
        515 => node_515(v),
        516 => node_516(v),
        517 => node_517(v),
        518 => node_518(v),
        519 => node_519(v),
        520 => node_520(v),
        521 => node_521(v),
        522 => node_522(v),
        523 => node_523(v),
        524 => node_524(v),
        525 => node_525(v),
        526 => node_526(v),
        527 => node_527(v),
        528 => node_528(v),
        529 => node_529(v),
        530 => node_530(v),
        531 => node_531(v),
        532 => node_532(v),
        533 => node_533(v),
        534 => node_534(v),
        535 => node_535(v),
        536 => node_536(v),
        537 => node_537(v),
        538 => node_538(v),
        539 => node_539(v),
        540 => node_540(v),
        541 => node_541(v),
        542 => node_542(v),
        543 => node_543(v),
        544 => node_544(v),
        545 => node_545(v),
        546 => node_546(v),
        547 => node_547(v),
        548 => node_548(v),
        549 => node_549(v),
        550 => node_550(v),
        551 => node_551(v),
        552 => node_552(v),
        553 => node_553(v),
        554 => node_554(v),
        555 => node_555(v),
        556 => node_556(v),
        557 => node_557(v),
        558 => node_558(v),
        559 => node_559(v),
        560 => node_560(v),
        561 => node_561(v),
        562 => node_562(v),
        _ => false,
    }
}
#[cfg(test)]
pub(super) fn pattern(i: usize, s: &str) -> bool {
    match i {
        0 => dot_segment(s),
        1 => loose_version(s),
        2 => logical_path_shape(s),
        3 => enforcement(s),
        4 => s.starts_with('/'),
        5 => platform(s),
        6 => transition(s),
        7 => mode(s),
        8 => timestamp(s),
        9 => core_path_shape(s),
        10 => signed_path_shape(s),
        11 => token(s),
        12 => hex(s, 32),
        13 => hex(s, 64),
        14 => hex(dollar(s), 64),
        15 => hex(dollar(s), 128),
        16 => tag_hex(s, "closure2:", 64),
        17 => tag_hex(s, "exec1_", 32),
        18 => tag_hex(s, "prj1-", 64),
        19 => tag_hex(s, "receipt2:", 64),
        20 => tag_hex(s, "repairplan2:", 64),
        21 => tag_hex(s, "req1_", 32),
        22 => tag_hex(s, "run2:", 64),
        23 => tag_hex(s, "run3:", 64),
        24 => tag_hex(s, "snapshot2:", 64),
        _ => false,
    }
}
