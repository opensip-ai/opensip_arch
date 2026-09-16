#[path = "../generated/wire.rs"]
pub mod wire;
#[cfg(test)]
mod tests;
/// Frame payloads have no generic serde implementation: a stateful decoder
/// must select their alternatives explicitly before constructing a frame.
/// ```compile_fail
/// use opensip_native_wire_carrier_trial::wire::Ts2FrameV2;
/// let _: Ts2FrameV2 = serde_json::from_str("{}").unwrap();
/// ```
/// ```compile_fail
/// use opensip_native_wire_carrier_trial::wire::Rust3ProviderFrameV3;
/// fn generic_serializer<T: serde::Serialize>() {}
/// generic_serializer::<Rust3ProviderFrameV3>();
/// ```
pub struct FrameSelectionRequiresHostState;
