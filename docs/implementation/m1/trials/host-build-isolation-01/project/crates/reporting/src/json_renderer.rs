use opensip_contracts::generated::output::Envelope7Root;
use std::io::{self, Write};

const ENVELOPE_BYTES: usize = 4 * 1024 * 1024;

/// An owned, bounded staging buffer. Nothing is exposed until the complete
/// encoding, including its line delimiter, fits. This is not semantic admission.
struct BoundedOutput {
    bytes: Vec<u8>,
}
impl Write for BoundedOutput {
    fn write(&mut self, input: &[u8]) -> io::Result<usize> {
        let needed = self
            .bytes
            .len()
            .checked_add(input.len())
            .ok_or_else(|| io::Error::other("required JSON output capacity exceeded"))?;
        if needed > ENVELOPE_BYTES {
            return Err(io::Error::other("required JSON output capacity exceeded"));
        }
        if needed > self.bytes.capacity() {
            let capacity = self
                .bytes
                .capacity()
                .max(4096)
                .saturating_mul(2)
                .max(needed)
                .min(ENVELOPE_BYTES);
            self.bytes
                .try_reserve_exact(capacity - self.bytes.len())
                .map_err(|_| io::Error::other("required JSON output allocation failed"))?;
        }
        self.bytes.extend_from_slice(input);
        Ok(input.len())
    }
    fn flush(&mut self) -> io::Result<()> {
        Ok(())
    }
}

/// Serialize a host-selected projection with bounded staging. Schema and private
/// request/source joins remain the caller's admission responsibility.
pub fn render_json(value: &Envelope7Root) -> Result<Vec<u8>, serde_json::Error> {
    encode_json(value)
}

/// Shared encoding primitive; tests use scalar stress values, not admitted envelopes.
pub(crate) fn encode_json<T: serde::Serialize>(value: &T) -> Result<Vec<u8>, serde_json::Error> {
    let mut output = BoundedOutput { bytes: Vec::new() };
    serde_json::to_writer(&mut output, value)?;
    output.write_all(b"\n").map_err(serde_json::Error::io)?;
    Ok(output.bytes)
}

#[cfg(test)]
mod tests {
    use opensip_contracts::generated::output::Envelope7Root;

    // These values test representation/encoding only, not host admission or Run custody.
    fn failure(diagnostic: String) -> Envelope7Root {
        serde_json::from_value(serde_json::json!({
            "schemaFamily":"opensip.product.envelope", "schemaMajor":7,
            "kind":"failure", "requestId":"req1_00000000000000000000000000000000",
            "termination":{"class":"request-rejected","errorCode":"REQUEST.UNKNOWN_OPTION"},
            "exitCode":2, "errors":[], "diagnostics":[diagnostic]
        }))
        .unwrap()
    }

    #[test]
    fn bounded_encoding_counts_escaped_bytes_and_preserves_complete_small_output() {
        let value = serde_json::json!({"value":"\0".repeat(100_000)});
        let encoded = crate::json_renderer::encode_json(&value).unwrap();
        assert!(encoded.len() > 600_000);
        assert!(encoded.ends_with(b"\n"));
        let decoded: serde_json::Value = serde_json::from_slice(&encoded).unwrap();
        assert_eq!(decoded["value"], "\0".repeat(100_000));
        let normal = crate::render_json(&failure("safe diagnostic".to_owned())).unwrap();
        let decoded: serde_json::Value = serde_json::from_slice(&normal).unwrap();
        assert_eq!(decoded["errors"], serde_json::json!([]));
        assert_eq!(decoded["schemaMajor"], 7);
        // Raw input is well below4MiB but JSON escaping exceeds it. No partial
        // projection may be returned from the renderer.
        assert!(
            crate::json_renderer::encode_json(&serde_json::json!("\0".repeat(700_000))).is_err()
        );
    }

    #[test]
    fn bounded_encoding_counts_utf8_bytes_instead_of_characters() {
        assert!(
            crate::json_renderer::encode_json(&serde_json::json!("界".repeat(100_000))).is_ok()
        );
        assert!(
            crate::json_renderer::encode_json(&serde_json::json!("界".repeat(1_400_000))).is_err()
        );
    }

    #[test]
    fn bounded_encoding_has_an_inclusive_complete_emission_limit() {
        let overhead = crate::json_renderer::encode_json(&serde_json::json!(String::new()))
            .unwrap()
            .len();
        let limit = 4 * 1024 * 1024;
        let exactly =
            crate::json_renderer::encode_json(&serde_json::json!("x".repeat(limit - overhead)))
                .unwrap();
        assert_eq!(exactly.len(), limit);
        assert!(exactly.ends_with(b"\n"));
        assert!(
            crate::json_renderer::encode_json(&serde_json::json!("x".repeat(limit - overhead + 1)))
                .is_err()
        );
    }
}
