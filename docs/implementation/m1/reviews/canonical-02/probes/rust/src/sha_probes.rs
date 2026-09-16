//! Review-02 probes for the software SHA-256 dependency and public hash API.
//! hashlib is the oracle; `sha_differential.py compare` checks these outputs.

use opensip_identity::{
    CanonicalError, DigestError, digest_hex, hash_canonical_value, hash_preimage, parse_json,
    raw_sha256,
};
use std::time::Instant;

fn unhex(text: &str) -> Vec<u8> {
    (0..text.len())
        .step_by(2)
        .map(|index| u8::from_str_radix(&text[index..index + 2], 16).unwrap())
        .collect()
}

fn lines(path: &str) -> Vec<String> {
    let text = std::fs::read_to_string(path).unwrap();
    let mut lines: Vec<String> = text.split('\n').map(String::from).collect();
    assert_eq!(lines.pop().as_deref(), Some(""));
    lines
}

#[test]
fn sha_and_h_differential_outputs() {
    let (Ok(inputs), Ok(out)) = (std::env::var("PROBE_SHA_INPUTS"), std::env::var("PROBE_SHA_OUT"))
    else {
        eprintln!("probe: SHA differential outputs NOT produced");
        return;
    };
    let mut text = String::new();
    for line in lines(&inputs) {
        text.push_str(&digest_hex(&raw_sha256(&unhex(&line))));
        text.push('\n');
    }
    std::fs::write(out, text).unwrap();

    let (Ok(corpus), Ok(h_out)) = (std::env::var("PROBE_CORPUS"), std::env::var("PROBE_H_OUT")) else {
        eprintln!("probe: H differential outputs NOT produced");
        return;
    };
    let mut text = String::new();
    for line in lines(&corpus) {
        match parse_json(&unhex(&line)) {
            Ok(value) => {
                let identity = hash_canonical_value("probe", &value).unwrap();
                let preimage = hash_preimage("probe", &value).unwrap();
                assert_eq!(raw_sha256(&preimage), identity);
                text.push_str(&digest_hex(&identity));
            }
            Err(_) => text.push('-'),
        }
        text.push('\n');
    }
    std::fs::write(h_out, text).unwrap();
}

#[test]
fn digest_error_is_a_core_error_with_source() {
    let error = DigestError::Canonical(CanonicalError::DepthLimit);
    let dynamic: &dyn core::error::Error = &error;
    assert!(dynamic.source().is_some());
    assert_eq!(format!("{error}"), "canonical encoding failed: DepthLimit");
    let domain: &dyn core::error::Error = &DigestError::Domain;
    assert!(domain.source().is_none());
    assert_eq!(format!("{}", DigestError::Domain), "invalid hash domain");
}

#[test]
fn software_sha256_throughput_observation() {
    let data = vec![0x5a_u8; 16 * 1024 * 1024];
    let started = Instant::now();
    let digest = raw_sha256(&data);
    let seconds = started.elapsed().as_secs_f64();
    eprintln!(
        "probe-sha-throughput: bytes={} seconds={seconds:.3} MiBps={:.1} digest={}",
        data.len(),
        16.0 / seconds,
        digest_hex(&digest)
    );
}
