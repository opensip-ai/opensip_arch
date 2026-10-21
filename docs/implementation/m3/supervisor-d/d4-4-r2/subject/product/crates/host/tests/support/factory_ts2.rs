//! Synthetic public A2 field projection, matching D2b's public first-party
//! descriptor fixture literals. Neither signatures nor C4 admission claimed.
use opensip_components::provider_protocol::{cbor::Value, ts2::DescriptorFields};
fn t(s: &str) -> Value {
    Value::Text(s.into())
}
pub fn provider() -> DescriptorFields {
    DescriptorFields::from_iter([
        ("providerBuildId".into(), t("typescript-provider 1.0.0")),
        ("protocolMajor".into(), Value::Unsigned(2)),
        ("typescriptVersion".into(), t("5.9.2")),
        ("typescriptCompilerSha256".into(), t(&"1".repeat(64))),
        ("typescriptStdlibMerkleRoot".into(), t(&"2".repeat(64))),
        (
            "defaultWorkBudgetProfileId".into(),
            t("typescript-provider-default-work-budget-v1"),
        ),
        (
            "defaultWorkBudgetProfileSha256".into(),
            t("bf7305a12d26a1938b615c861f995d66eac494915e6140c4942a2ea6f0846da6"),
        ),
    ])
}
pub fn runtime() -> DescriptorFields {
    DescriptorFields::from_iter([
        ("nodeVersion".into(), t("24.16.0")),
        ("v8Version".into(), t("13.6")),
        ("modulesAbi".into(), t("137")),
        ("platformId".into(), t("darwin-arm64")),
    ])
}
