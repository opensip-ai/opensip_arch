//! Generated from exact completed manifest schema; not semantic admission.
// SHA256 80254f9e1fd9a3014f5bba73715f1c882d0d511293cc154cc2b59cfbf9d37353
use super::*;
pub(super) fn shape(v: &V) -> bool { node_0(v) }
fn node_0(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    ((usize::from(node_32(v)) + usize::from(node_35(v))) == 1) &&
    (matches!(v, V::Object(o) if o.get("manifestSchemaVersion").is_some_and(node_1) && o.get("kind").is_some_and(node_2) && o.get("stableId").is_some_and(node_3) && o.get("name").is_some_and(node_4) && o.get("displayName").is_none_or(node_5) && o.get("aliases").is_none_or(node_6) && o.get("version").is_some_and(node_7) && o.get("role").is_some_and(node_8) && o.get("commands").is_none_or(node_9) && o.get("capabilities").is_some_and(node_11) && o.get("platforms").is_some_and(node_13) && o.get("dependencies").is_some_and(node_15) && o.get("prerequisites").is_none_or(node_17) && o.get("declarations").is_some_and(node_19) && o.get("permissions").is_some_and(node_21) && o.get("configuration").is_none_or(node_25) && o.get("provenance").is_some_and(node_26) && o.get("stateMigration").is_some_and(node_28) && o.get("updateData").is_some_and(node_29) && o.get("compatibility").is_some_and(node_30) && o.get("closureProtocolMajor").is_none_or(node_1) && o.keys().all(|k| ["manifestSchemaVersion", "kind", "stableId", "name", "displayName", "aliases", "version", "role", "commands", "capabilities", "platforms", "dependencies", "prerequisites", "declarations", "permissions", "configuration", "provenance", "stateMigration", "updateData", "compatibility", "closureProtocolMajor"].contains(&k.as_str()))))
}
fn node_1(v: &V) -> bool {
    (matches!(v, V::Integer(_))) &&
    (matches!(v, V::Integer(n) if n.get() >= 1_i128 && n.get() <= 9223372036854775807_i128))
}
fn node_2(v: &V) -> bool {
    matches!(v, V::String(s) if s == "component")
}
fn node_3(v: &V) -> bool {
    (matches!(v, V::String(_))) &&
    (matches!(v, V::String(s) if uuid(s)))
}
fn node_4(v: &V) -> bool {
    (matches!(v, V::String(_))) &&
    (matches!(v, V::String(s) if token(s)))
}
fn node_5(v: &V) -> bool {
    matches!(v, V::String(_))
}
fn node_6(v: &V) -> bool {
    (matches!(v, V::Array(_))) &&
    (matches!(v, V::Array(a) if a.len() <= 64 && unique(a) && a.iter().all(node_4)))
}
fn node_7(v: &V) -> bool {
    (matches!(v, V::String(_))) &&
    (matches!(v, V::String(s) if version(s)))
}
fn node_8(v: &V) -> bool {
    matches!(v, V::String(s) if s == "analyzer") || matches!(v, V::String(s) if s == "toolchain") || matches!(v, V::String(s) if s == "stdlib") || matches!(v, V::String(s) if s == "rust-dev-llvm") || matches!(v, V::String(s) if s == "grammar")
}
fn node_9(v: &V) -> bool {
    (matches!(v, V::Array(_))) &&
    (matches!(v, V::Array(a) if !a.is_empty() && a.len() <= 4096 && a.iter().all(node_10)))
}
fn node_10(v: &V) -> bool {
    node_69(v)
}
fn node_11(v: &V) -> bool {
    (matches!(v, V::Array(_))) &&
    (matches!(v, V::Array(a) if a.iter().all(node_12)))
}
fn node_12(v: &V) -> bool {
    node_78(v)
}
fn node_13(v: &V) -> bool {
    (matches!(v, V::Array(_))) &&
    (matches!(v, V::Array(a) if !a.is_empty() && a.iter().all(node_14)))
}
fn node_14(v: &V) -> bool {
    node_60(v)
}
fn node_15(v: &V) -> bool {
    (matches!(v, V::Array(_))) &&
    (matches!(v, V::Array(a) if a.iter().all(node_16)))
}
fn node_16(v: &V) -> bool {
    node_106(v)
}
fn node_17(v: &V) -> bool {
    (matches!(v, V::Array(_))) &&
    (matches!(v, V::Array(a) if a.iter().all(node_18)))
}
fn node_18(v: &V) -> bool {
    node_107(v)
}
fn node_19(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("licenses").is_some_and(node_20) && o.get("sbom").is_some_and(node_20) && o.get("attestation").is_some_and(node_20) && o.get("platformQualification").is_some_and(node_20) && o.get("capabilityParityEvidence").is_some_and(node_20) && o.get("performanceBaseline").is_some_and(node_20) && o.keys().all(|k| ["licenses", "sbom", "attestation", "platformQualification", "capabilityParityEvidence", "performanceBaseline"].contains(&k.as_str()))))
}
fn node_20(v: &V) -> bool {
    node_48(v)
}
fn node_21(v: &V) -> bool {
    (matches!(v, V::Array(_))) &&
    (matches!(v, V::Array(a) if a.iter().all(node_22)))
}
fn node_22(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("permission").is_some_and(node_23) && o.get("reason").is_some_and(node_24) && o.keys().all(|k| ["permission", "reason"].contains(&k.as_str()))))
}
fn node_23(v: &V) -> bool {
    matches!(v, V::String(s) if s == "PT-FS-READ-PROJECT") || matches!(v, V::String(s) if s == "PT-FS-READ-COMPONENT") || matches!(v, V::String(s) if s == "PT-FS-WRITE-HOST-STATE") || matches!(v, V::String(s) if s == "PT-PROC-EXEC-DECLARED") || matches!(v, V::String(s) if s == "PT-NET-EGRESS") || matches!(v, V::String(s) if s == "PT-ENV-READ") || matches!(v, V::String(s) if s == "PT-HOST-EFFECT-BROKERED")
}
fn node_24(v: &V) -> bool {
    (matches!(v, V::String(_))) &&
    (matches!(v, V::String(s) if s.chars().count() >= 1))
}
fn node_25(v: &V) -> bool {
    node_126(v)
}
fn node_26(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("publisher").is_some_and(node_24) && o.get("sourceClass").is_some_and(node_27) && o.keys().all(|k| ["publisher", "sourceClass"].contains(&k.as_str()))))
}
fn node_27(v: &V) -> bool {
    matches!(v, V::String(s) if s == "first-party") || matches!(v, V::String(s) if s == "explicitly-trusted")
}
fn node_28(v: &V) -> bool {
    matches!(v, V::Object(o) if o.len() == 2 && o.get("reserved").is_some_and(|v| matches!(v, V::Bool(true))) && o.get("ridesOn").is_some_and(|v| matches!(v, V::Array(a) if a.len() == 4 && matches!(&a[0], V::String(s) if s == "DR-124") && matches!(&a[1], V::String(s) if s == "DR-106") && matches!(&a[2], V::String(s) if s == "DR-109") && matches!(&a[3], V::String(s) if s == "DR-113"))))
}
fn node_29(v: &V) -> bool {
    matches!(v, V::Object(o) if o.len() == 2 && o.get("reserved").is_some_and(|v| matches!(v, V::Bool(true))) && o.get("ridesOn").is_some_and(|v| matches!(v, V::Array(a) if a.len() == 2 && matches!(&a[0], V::String(s) if s == "DR-110") && matches!(&a[1], V::String(s) if s == "DR-112"))))
}
fn node_30(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("manifest").is_some_and(node_1) && o.get("hostCore").is_some_and(node_31) && o.get("control").is_some_and(node_1) && o.get("providerProtocol").is_some_and(node_1) && o.get("componentState").is_some_and(node_1) && o.keys().all(|k| ["manifest", "hostCore", "control", "providerProtocol", "componentState"].contains(&k.as_str()))))
}
fn node_31(v: &V) -> bool {
    node_38(v)
}
fn node_32(v: &V) -> bool {
    matches!(v, V::Object(o) if o.get("role").is_some_and(node_33) && o.get("commands").is_some_and(node_34))
}
fn node_33(v: &V) -> bool {
    matches!(v, V::String(s) if s == "analyzer")
}
fn node_34(v: &V) -> bool {
    (matches!(v, V::Array(_))) &&
    (matches!(v, V::Array(a) if !a.is_empty()))
}
fn node_35(v: &V) -> bool {
    matches!(v, V::Object(o) if o.get("role").is_some_and(node_36) && o.get("commands").is_none_or(node_37))
}
fn node_36(v: &V) -> bool {
    matches!(v, V::String(s) if s == "toolchain") || matches!(v, V::String(s) if s == "stdlib") || matches!(v, V::String(s) if s == "rust-dev-llvm") || matches!(v, V::String(s) if s == "grammar")
}
fn node_37(v: &V) -> bool {
    matches!(v, V::Null)
}
fn node_38(v: &V) -> bool {
    (usize::from(node_7(v)) + usize::from(node_39(v))) == 1
}
fn node_39(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("min").is_some_and(node_7) && o.get("max").is_some_and(node_7) && o.get("includeMin").is_some_and(node_40) && o.get("includeMax").is_some_and(node_40) && o.keys().all(|k| ["min", "max", "includeMin", "includeMax"].contains(&k.as_str()))))
}
fn node_40(v: &V) -> bool {
    matches!(v, V::Bool(_))
}
fn node_41(v: &V) -> bool {
    (matches!(v, V::String(_))) &&
    (matches!(v, V::String(s) if s.chars().count() >= 1))
}
fn node_42(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("path").is_some_and(node_43) && o.get("sha256").is_some_and(node_44) && o.keys().all(|k| ["path", "sha256"].contains(&k.as_str()))))
}
fn node_43(v: &V) -> bool {
    node_41(v)
}
fn node_44(v: &V) -> bool {
    (matches!(v, V::String(_))) &&
    (matches!(v, V::String(s) if hex(s)))
}
fn node_45(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("absent").is_some_and(node_46) && o.get("exceptionApprovalRef").is_some_and(node_24) && o.get("typedAbsenceBehavior").is_some_and(node_47) && o.keys().all(|k| ["absent", "exceptionApprovalRef", "typedAbsenceBehavior"].contains(&k.as_str()))))
}
fn node_46(v: &V) -> bool {
    matches!(v, V::Bool(true))
}
fn node_47(v: &V) -> bool {
    matches!(v, V::String(s) if s == "RJ-1") || matches!(v, V::String(s) if s == "RJ-2") || matches!(v, V::String(s) if s == "RJ-3") || matches!(v, V::String(s) if s == "RJ-4") || matches!(v, V::String(s) if s == "RJ-5") || matches!(v, V::String(s) if s == "RJ-6")
}
fn node_48(v: &V) -> bool {
    (usize::from(node_49(v)) + usize::from(node_50(v))) == 1
}
fn node_49(v: &V) -> bool {
    node_42(v)
}
fn node_50(v: &V) -> bool {
    node_45(v)
}
fn node_51(v: &V) -> bool {
    (usize::from(node_52(v)) + usize::from(node_56(v)) + usize::from(node_58(v))) == 1
}
fn node_52(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("path").is_some_and(node_43) && o.get("type").is_some_and(node_53) && o.get("mode").is_some_and(node_54) && o.get("length").is_some_and(node_55) && o.get("sha256").is_some_and(node_44) && o.keys().all(|k| ["path", "type", "mode", "length", "sha256"].contains(&k.as_str()))))
}
fn node_53(v: &V) -> bool {
    matches!(v, V::String(s) if s == "file")
}
fn node_54(v: &V) -> bool {
    (matches!(v, V::String(_))) &&
    (matches!(v, V::String(s) if mode(s)))
}
fn node_55(v: &V) -> bool {
    (matches!(v, V::Integer(_))) &&
    (matches!(v, V::Integer(n) if n.get() >= 0_i128 && n.get() <= 9223372036854775807_i128))
}
fn node_56(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("path").is_some_and(node_43) && o.get("type").is_some_and(node_57) && o.get("mode").is_some_and(node_54) && o.keys().all(|k| ["path", "type", "mode"].contains(&k.as_str()))))
}
fn node_57(v: &V) -> bool {
    matches!(v, V::String(s) if s == "dir")
}
fn node_58(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("path").is_some_and(node_43) && o.get("type").is_some_and(node_59) && o.get("mode").is_some_and(node_54) && o.get("target").is_some_and(node_43) && o.keys().all(|k| ["path", "type", "mode", "target"].contains(&k.as_str()))))
}
fn node_59(v: &V) -> bool {
    matches!(v, V::String(s) if s == "symlink")
}
fn node_60(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("os").is_some_and(node_24) && o.get("arch").is_some_and(node_24) && o.get("tree").is_some_and(node_61) && o.get("entrypoint").is_some_and(node_43) && o.keys().all(|k| ["os", "arch", "tree", "entrypoint"].contains(&k.as_str()))))
}
fn node_61(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("entries").is_some_and(node_62) && o.keys().all(|k| ["entries"].contains(&k.as_str()))))
}
fn node_62(v: &V) -> bool {
    (matches!(v, V::Array(_))) &&
    (matches!(v, V::Array(a) if !a.is_empty() && a.len() <= 100000 && a.iter().all(node_63)))
}
fn node_63(v: &V) -> bool {
    node_51(v)
}
fn node_64(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("flag").is_some_and(node_65) && o.get("description").is_some_and(node_5) && o.get("valueKind").is_some_and(node_66) && o.get("repeatable").is_some_and(node_40) && o.get("default").is_none_or(node_67) && o.keys().all(|k| ["flag", "description", "valueKind", "repeatable", "default"].contains(&k.as_str()))))
}
fn node_65(v: &V) -> bool {
    (matches!(v, V::String(_))) &&
    (matches!(v, V::String(s) if flag(s)))
}
fn node_66(v: &V) -> bool {
    matches!(v, V::String(s) if s == "string") || matches!(v, V::String(s) if s == "integer") || matches!(v, V::String(s) if s == "boolean") || matches!(v, V::String(s) if s == "path")
}
fn node_67(v: &V) -> bool {
    matches!(v, V::String(_) | V::Integer(_) | V::Bool(_) | V::Array(_))
}
fn node_68(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("name").is_some_and(node_4) && o.get("description").is_some_and(node_5) && o.get("required").is_some_and(node_40) && o.get("variadic").is_some_and(node_40) && o.keys().all(|k| ["name", "description", "required", "variadic"].contains(&k.as_str()))))
}
fn node_69(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("name").is_some_and(node_4) && o.get("description").is_some_and(node_5) && o.get("aliases").is_none_or(node_6) && o.get("parent").is_none_or(node_4) && o.get("visibility").is_none_or(node_70) && o.get("options").is_none_or(node_71) && o.get("args").is_none_or(node_73) && o.get("scope").is_none_or(node_75) && o.get("outputModes").is_none_or(node_76) && o.keys().all(|k| ["name", "description", "aliases", "parent", "visibility", "options", "args", "scope", "outputModes"].contains(&k.as_str()))))
}
fn node_70(v: &V) -> bool {
    matches!(v, V::String(s) if s == "public") || matches!(v, V::String(s) if s == "internal")
}
fn node_71(v: &V) -> bool {
    (matches!(v, V::Array(_))) &&
    (matches!(v, V::Array(a) if a.iter().all(node_72)))
}
fn node_72(v: &V) -> bool {
    node_64(v)
}
fn node_73(v: &V) -> bool {
    (matches!(v, V::Array(_))) &&
    (matches!(v, V::Array(a) if a.iter().all(node_74)))
}
fn node_74(v: &V) -> bool {
    node_68(v)
}
fn node_75(v: &V) -> bool {
    matches!(v, V::String(s) if s == "project") || matches!(v, V::String(s) if s == "none")
}
fn node_76(v: &V) -> bool {
    (matches!(v, V::Array(_))) &&
    (matches!(v, V::Array(a) if !a.is_empty() && unique(a) && a.iter().all(node_77)))
}
fn node_77(v: &V) -> bool {
    matches!(v, V::String(s) if s == "human") || matches!(v, V::String(s) if s == "json") || matches!(v, V::String(s) if s == "sarif")
}
fn node_78(v: &V) -> bool {
    (usize::from(node_79(v)) + usize::from(node_86(v)) + usize::from(node_91(v)) + usize::from(node_96(v)) + usize::from(node_101(v))) == 1
}
fn node_79(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("capabilityId").is_some_and(node_80) && o.get("roleSubprotocol").is_some_and(node_81) && o.get("subprotocolVersion").is_some_and(node_82) && o.get("declarationData").is_some_and(node_83) && o.keys().all(|k| ["capabilityId", "roleSubprotocol", "subprotocolVersion", "declarationData"].contains(&k.as_str()))))
}
fn node_80(v: &V) -> bool {
    matches!(v, V::String(s) if s == "typescript.imports")
}
fn node_81(v: &V) -> bool {
    matches!(v, V::String(s) if s == "typescript")
}
fn node_82(v: &V) -> bool {
    matches!(v, V::Integer(n) if n.get() == 1)
}
fn node_83(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("relation").is_some_and(node_84) && o.get("rung").is_some_and(node_85) && o.keys().all(|k| ["relation", "rung"].contains(&k.as_str()))))
}
fn node_84(v: &V) -> bool {
    matches!(v, V::String(s) if s == "imports")
}
fn node_85(v: &V) -> bool {
    matches!(v, V::String(s) if s == "resolved-target")
}
fn node_86(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("capabilityId").is_some_and(node_87) && o.get("roleSubprotocol").is_some_and(node_81) && o.get("subprotocolVersion").is_some_and(node_82) && o.get("declarationData").is_some_and(node_88) && o.keys().all(|k| ["capabilityId", "roleSubprotocol", "subprotocolVersion", "declarationData"].contains(&k.as_str()))))
}
fn node_87(v: &V) -> bool {
    matches!(v, V::String(s) if s == "typescript.references")
}
fn node_88(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("relation").is_some_and(node_89) && o.get("rung").is_some_and(node_90) && o.keys().all(|k| ["relation", "rung"].contains(&k.as_str()))))
}
fn node_89(v: &V) -> bool {
    matches!(v, V::String(s) if s == "references")
}
fn node_90(v: &V) -> bool {
    matches!(v, V::String(s) if s == "resolved-binding")
}
fn node_91(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("capabilityId").is_some_and(node_92) && o.get("roleSubprotocol").is_some_and(node_81) && o.get("subprotocolVersion").is_some_and(node_82) && o.get("declarationData").is_some_and(node_93) && o.keys().all(|k| ["capabilityId", "roleSubprotocol", "subprotocolVersion", "declarationData"].contains(&k.as_str()))))
}
fn node_92(v: &V) -> bool {
    matches!(v, V::String(s) if s == "typescript.calls")
}
fn node_93(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("relation").is_some_and(node_94) && o.get("rung").is_some_and(node_95) && o.keys().all(|k| ["relation", "rung"].contains(&k.as_str()))))
}
fn node_94(v: &V) -> bool {
    matches!(v, V::String(s) if s == "calls")
}
fn node_95(v: &V) -> bool {
    matches!(v, V::String(s) if s == "resolved-callee")
}
fn node_96(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("capabilityId").is_some_and(node_97) && o.get("roleSubprotocol").is_some_and(node_81) && o.get("subprotocolVersion").is_some_and(node_82) && o.get("declarationData").is_some_and(node_98) && o.keys().all(|k| ["capabilityId", "roleSubprotocol", "subprotocolVersion", "declarationData"].contains(&k.as_str()))))
}
fn node_97(v: &V) -> bool {
    matches!(v, V::String(s) if s == "typescript.types")
}
fn node_98(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("relation").is_some_and(node_99) && o.get("rung").is_some_and(node_100) && o.keys().all(|k| ["relation", "rung"].contains(&k.as_str()))))
}
fn node_99(v: &V) -> bool {
    matches!(v, V::String(s) if s == "types")
}
fn node_100(v: &V) -> bool {
    matches!(v, V::String(s) if s == "checked")
}
fn node_101(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("capabilityId").is_some_and(node_102) && o.get("roleSubprotocol").is_some_and(node_81) && o.get("subprotocolVersion").is_some_and(node_82) && o.get("declarationData").is_some_and(node_103) && o.keys().all(|k| ["capabilityId", "roleSubprotocol", "subprotocolVersion", "declarationData"].contains(&k.as_str()))))
}
fn node_102(v: &V) -> bool {
    matches!(v, V::String(s) if s == "typescript.reachability")
}
fn node_103(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("relation").is_some_and(node_104) && o.get("rung").is_some_and(node_105) && o.keys().all(|k| ["relation", "rung"].contains(&k.as_str()))))
}
fn node_104(v: &V) -> bool {
    matches!(v, V::String(s) if s == "reachability")
}
fn node_105(v: &V) -> bool {
    matches!(v, V::String(s) if s == "from-resolved-calls")
}
fn node_106(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("stableId").is_some_and(node_3) && o.get("versionConstraint").is_some_and(node_31) && o.get("reason").is_some_and(node_24) && o.keys().all(|k| ["stableId", "versionConstraint", "reason"].contains(&k.as_str()))))
}
fn node_107(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("exceptionApprovalRef").is_some_and(node_24) && o.get("ownership").is_some_and(node_24) && o.get("trust").is_some_and(node_24) && o.get("network").is_some_and(node_24) && o.get("prerequisiteExpectations").is_some_and(node_24) && o.get("doctorContract").is_some_and(node_43) && o.get("typedAbsenceBehavior").is_some_and(node_47) && o.get("typedFailureBehavior").is_some_and(node_47) && o.keys().all(|k| ["exceptionApprovalRef", "ownership", "trust", "network", "prerequisiteExpectations", "doctorContract", "typedAbsenceBehavior", "typedFailureBehavior"].contains(&k.as_str()))))
}
fn node_108(v: &V) -> bool {
    (usize::from(node_109(v)) + usize::from(node_116(v)) + usize::from(node_118(v)) + usize::from(node_121(v)) + usize::from(node_124(v))) == 1
}
fn node_109(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("type").is_some_and(node_110) && o.get("properties").is_some_and(node_111) && o.get("required").is_some_and(node_114) && o.get("additionalProperties").is_some_and(node_115) && o.keys().all(|k| ["type", "properties", "required", "additionalProperties"].contains(&k.as_str()))))
}
fn node_110(v: &V) -> bool {
    matches!(v, V::String(s) if s == "object")
}
fn node_111(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.values().all(node_113) && o.keys().all(|k| node_112(&V::String(k.clone())))))
}
fn node_112(v: &V) -> bool {
    (matches!(v, V::String(_))) &&
    (matches!(v, V::String(s) if config_key(s)))
}
fn node_113(v: &V) -> bool {
    node_108(v)
}
fn node_114(v: &V) -> bool {
    (matches!(v, V::Array(_))) &&
    (matches!(v, V::Array(a) if unique(a) && a.iter().all(node_112)))
}
fn node_115(v: &V) -> bool {
    matches!(v, V::Bool(false))
}
fn node_116(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("type").is_some_and(node_117) && o.get("items").is_some_and(node_113) && o.get("minItems").is_none_or(node_55) && o.get("maxItems").is_none_or(node_55) && o.keys().all(|k| ["type", "items", "minItems", "maxItems"].contains(&k.as_str()))))
}
fn node_117(v: &V) -> bool {
    matches!(v, V::String(s) if s == "array")
}
fn node_118(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("type").is_some_and(node_119) && o.get("minLength").is_none_or(node_55) && o.get("maxLength").is_none_or(node_55) && o.get("enum").is_none_or(node_120) && o.keys().all(|k| ["type", "minLength", "maxLength", "enum"].contains(&k.as_str()))))
}
fn node_119(v: &V) -> bool {
    matches!(v, V::String(s) if s == "string")
}
fn node_120(v: &V) -> bool {
    (matches!(v, V::Array(_))) &&
    (matches!(v, V::Array(a) if !a.is_empty() && unique(a) && a.iter().all(node_5)))
}
fn node_121(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("type").is_some_and(node_122) && o.get("minimum").is_none_or(node_123) && o.get("maximum").is_none_or(node_123) && o.keys().all(|k| ["type", "minimum", "maximum"].contains(&k.as_str()))))
}
fn node_122(v: &V) -> bool {
    matches!(v, V::String(s) if s == "integer")
}
fn node_123(v: &V) -> bool {
    (matches!(v, V::Integer(_))) &&
    (matches!(v, V::Integer(n) if n.get() >= -9223372036854775808_i128 && n.get() <= 9223372036854775807_i128))
}
fn node_124(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("type").is_some_and(node_125) && o.keys().all(|k| ["type"].contains(&k.as_str()))))
}
fn node_125(v: &V) -> bool {
    matches!(v, V::String(s) if s == "boolean") || matches!(v, V::String(s) if s == "null")
}
fn node_126(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.get("namespace").is_some_and(node_4) && o.get("schema").is_some_and(node_113) && o.get("classifications").is_some_and(node_127) && o.keys().all(|k| ["namespace", "schema", "classifications"].contains(&k.as_str()))))
}
fn node_127(v: &V) -> bool {
    (matches!(v, V::Object(_))) &&
    (matches!(v, V::Object(o) if o.values().all(node_128) && o.keys().all(|k| node_112(&V::String(k.clone())))))
}
fn node_128(v: &V) -> bool {
    matches!(v, V::String(s) if s == "host.analysis.semantic") || matches!(v, V::String(s) if s == "host.operability.nonsemantic")
}
