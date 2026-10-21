//! RPP limitPolicy, RUST3-SPOOL and D2b LD-3/8: checked response safety
//! bounds. Payload totals exclude the forty-byte transport prefix. A spool
//! entry is constructed from the validated semantic value, never sliced
//! from received bytes or measured by candidate length/allocator capacity.
use super::super::cbor::{self, Value};
use opensip_identity::{JsonValue as J, parse_json};

const HANDSHAKE: &[u8] = include_bytes!("../../../../../schemas/sources/handshake-v1.schema.json");

#[derive(Debug, Clone, Copy)]
struct Limits {
    frame: u64,
    payload_total: u64,
    frames: u64,
    candidates: u64,
    spool: u64,
}
impl Limits {
    fn load() -> Result<Self, String> {
        let doc = parse_json(HANDSHAKE).map_err(|e| format!("handshake: {e}"))?;
        let get = |name: &str| -> Result<u64, String> {
            let mut value = &doc;
            for key in ["$defs", "ProtocolLimitsV3", "properties", name, "const"] {
                let J::Object(fields) = value else {
                    return Err(format!("limit {name}"));
                };
                value = fields.get(key).ok_or_else(|| format!("limit {name}"))?;
            }
            let J::Integer(n) = value else {
                return Err(format!("limit {name}"));
            };
            u64::try_from(n.get()).map_err(|_| format!("limit {name}"))
        };
        Ok(Self {
            frame: get("maxFramePayloadBytes")?,
            payload_total: get("maxResponsePayloadBytesTotal")?,
            frames: get("maxResponseFrames")?,
            candidates: get("maxFactCandidatesTotal")?,
            spool: get("maxCandidateSpoolBytes")?,
        })
    }
}

/// Counts already charged for this Rust3 response stream. The empty spool
/// has zero bytes. None of these counters saturates or wraps.
#[derive(Debug, Default, Clone, Copy, PartialEq, Eq)]
pub struct ResponseTotals {
    pub payload_bytes: u64,
    pub frames: u64,
    pub candidates: u64,
    pub spool_bytes: u64,
}

/// Validated FactBatch candidates and their context. The receive codec must
/// perform its canonical, closed-schema and contextual checks first. This
/// borrowed view grants no independent candidate or frame admission.
#[derive(Debug, Clone, Copy)]
pub struct CandidateBatch<'v> {
    pub analysis_ordinal: u64,
    pub stage_id: &'v str,
    pub candidates: &'v [Value],
}

/// A safety refusal is provider-protocol, never semantic BudgetExhausted.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ResponseBoundsRefusal {
    Frame,
    PayloadTotal,
    Frames,
    Candidates,
    Spool,
    Overflow,
    EncodingLength,
    AfterRefusal,
}

/// Response safety accounting using the selected handshake's fixed Rust3
/// limits. It is not a substitute for the receive codec's schema/context
/// admission. After refusal no later frame can be charged.
#[derive(Debug)]
pub struct ResponseAccounting {
    limits: Limits,
    totals: ResponseTotals,
    refused: bool,
}
impl ResponseAccounting {
    pub fn new() -> Result<Self, String> {
        Ok(Self {
            limits: Limits::load()?,
            totals: ResponseTotals::default(),
            refused: false,
        })
    }
    // A fixture state immediately before a published full-limit boundary.
    // This avoids materializing a GiB or a million frames in receiver tests.
    #[cfg(test)]
    pub(super) fn seed_totals_for_test(&mut self, totals: ResponseTotals) {
        assert!(totals.payload_bytes <= self.limits.payload_total);
        assert!(totals.frames <= self.limits.frames);
        assert!(totals.candidates <= self.limits.candidates);
        assert!(totals.spool_bytes <= self.limits.spool);
        self.totals = totals;
    }
    pub fn totals(&self) -> ResponseTotals {
        self.totals
    }
    /// The length prefix must be checked against this allowance before
    /// allocation, in addition to the per-frame limit (D2b-1 accumulator).
    pub fn remaining_payload_bytes(&self) -> u64 {
        self.limits.payload_total - self.totals.payload_bytes
    }
    /// Charge one response envelope's canonical-CBOR payload bytes and,
    /// when it is a FactBatch, construct its spool entries. Every checked
    /// next counter and every entry length is established before allocating
    /// or encoding any entry. A refusal leaves all totals unchanged.
    pub fn charge(
        &mut self,
        payload_bytes: u64,
        batch: Option<CandidateBatch<'_>>,
    ) -> Result<Vec<Vec<u8>>, ResponseBoundsRefusal> {
        if self.refused {
            return Err(ResponseBoundsRefusal::AfterRefusal);
        }
        match self.prepare(payload_bytes, batch) {
            Ok((next, entries)) => {
                self.totals = next;
                Ok(entries)
            }
            Err(error) => {
                self.refused = true;
                Err(error)
            }
        }
    }
    fn prepare(
        &self,
        payload_bytes: u64,
        batch: Option<CandidateBatch<'_>>,
    ) -> Result<(ResponseTotals, Vec<Vec<u8>>), ResponseBoundsRefusal> {
        use ResponseBoundsRefusal as E;
        if payload_bytes > self.limits.frame {
            return Err(E::Frame);
        }
        let mut next = self.totals;
        next.payload_bytes = next
            .payload_bytes
            .checked_add(payload_bytes)
            .ok_or(E::Overflow)?;
        if next.payload_bytes > self.limits.payload_total {
            return Err(E::PayloadTotal);
        }
        next.frames = next.frames.checked_add(1).ok_or(E::Overflow)?;
        if next.frames > self.limits.frames {
            return Err(E::Frames);
        }
        if let Some(batch) = batch {
            for candidate in batch.candidates {
                let size = entry_length(batch.analysis_ordinal, batch.stage_id, candidate)
                    .ok_or(E::Overflow)?;
                next.spool_bytes = next.spool_bytes.checked_add(size).ok_or(E::Overflow)?;
                if next.spool_bytes > self.limits.spool {
                    return Err(E::Spool);
                }
                next.candidates = next.candidates.checked_add(1).ok_or(E::Overflow)?;
                if next.candidates > self.limits.candidates {
                    return Err(E::Candidates);
                }
            }
        }
        // Only after the complete batch fits do any entry allocations occur.
        let mut entries = Vec::new();
        if let Some(batch) = batch {
            for candidate in batch.candidates {
                let entry = Value::Map(vec![
                    (
                        "analysisOrdinal".to_owned(),
                        Value::Unsigned(batch.analysis_ordinal),
                    ),
                    ("stageId".to_owned(), Value::Text(batch.stage_id.to_owned())),
                    ("candidate".to_owned(), candidate.clone()),
                ]);
                let expected = entry_length(batch.analysis_ordinal, batch.stage_id, candidate)
                    .ok_or(E::Overflow)?;
                let bytes = cbor::encode(&entry);
                if bytes.len() as u64 != expected {
                    return Err(E::EncodingLength);
                }
                entries.push(bytes);
            }
        }
        Ok((next, entries))
    }
}

fn head_length(n: u64) -> u64 {
    match n {
        0..=23 => 1,
        24..=255 => 2,
        256..=65535 => 3,
        65536..=4294967295 => 5,
        _ => 9,
    }
}
fn text_length(s: &str) -> Option<u64> {
    head_length(s.len() as u64).checked_add(s.len() as u64)
}
fn entry_length(ordinal: u64, stage: &str, candidate: &Value) -> Option<u64> {
    let mut bytes = head_length(3); // the constructed three-member map
    for key in ["analysisOrdinal", "stageId", "candidate"] {
        bytes = bytes.checked_add(text_length(key)?)?;
    }
    bytes
        .checked_add(head_length(ordinal))?
        .checked_add(text_length(stage)?)?
        .checked_add(cbor::encoded_length(candidate)?)
}

#[cfg(test)]
mod tests {
    use super::*;
    fn small() -> ResponseAccounting {
        ResponseAccounting {
            limits: Limits {
                frame: 100,
                payload_total: 200,
                frames: 2,
                candidates: 2,
                spool: 10000,
            },
            totals: ResponseTotals::default(),
            refused: false,
        }
    }
    fn candidate() -> Value {
        Value::Map(vec![
            ("candidateOrdinal".to_owned(), Value::Unsigned(0)),
            (
                "canonicalRelationPayload".to_owned(),
                Value::Bytes(vec![0xa0]),
            ),
        ])
    }
    #[test]
    fn selected_limits_and_each_response_boundary_are_exact() {
        let real = ResponseAccounting::new().unwrap();
        assert_eq!(
            (
                real.limits.frame,
                real.limits.payload_total,
                real.limits.frames,
                real.limits.candidates,
                real.limits.spool
            ),
            (67108864, 1073741824, 1000000, 1000000, 1073741824)
        );
        let mut a = small();
        a.limits.frames = 3; // isolate the payload-total guard from frame count
        assert!(a.charge(100, None).unwrap().is_empty());
        assert!(a.charge(100, None).is_ok());
        assert_eq!(a.remaining_payload_bytes(), 0);
        let before = a.totals();
        assert_eq!(a.charge(1, None), Err(ResponseBoundsRefusal::PayloadTotal));
        assert_eq!(a.totals(), before);
        assert_eq!(a.charge(0, None), Err(ResponseBoundsRefusal::AfterRefusal));
        let mut a = small();
        assert_eq!(a.charge(101, None), Err(ResponseBoundsRefusal::Frame));
        assert_eq!(a.totals(), ResponseTotals::default());
        let mut a = small();
        assert!(a.charge(1, None).is_ok());
        assert!(a.charge(1, None).is_ok());
        let before = a.totals();
        assert_eq!(a.charge(1, None), Err(ResponseBoundsRefusal::Frames));
        assert_eq!(a.totals(), before);
    }
    #[test]
    fn full_entry_bytes_and_candidate_count_are_charged_before_any_partial_batch() {
        let candidates = [candidate(), candidate()];
        let batch = CandidateBatch {
            analysis_ordinal: 24,
            stage_id: "stage-😀",
            candidates: &candidates,
        };
        let mut a = small();
        let entries = a.charge(1, Some(batch)).unwrap();
        assert_eq!(a.totals().candidates, 2);
        assert_eq!(
            a.totals().spool_bytes,
            entries.iter().map(|e| e.len() as u64).sum::<u64>(),
            "charge the full constructed entries, including every key and context field"
        );
        for bytes in &entries {
            let entry = cbor::decode(bytes, cbor::Profile::Rust3, 16).unwrap();
            let Value::Map(fields) = entry else {
                panic!("entry");
            };
            assert_eq!(fields.len(), 3);
            assert!(fields.contains(&("analysisOrdinal".to_owned(), Value::Unsigned(24))));
            assert!(fields.contains(&("stageId".to_owned(), Value::Text("stage-😀".to_owned()))));
            assert!(fields.contains(&("candidate".to_owned(), candidate())));
        }
        let full = entry_length(24, "stage-😀", &candidates[0]).unwrap();
        assert!(full > cbor::encode(&candidates[0]).len() as u64);
        let mut a = small();
        a.limits.spool = full * 2;
        assert!(a.charge(1, Some(batch)).is_ok());
        let mut a = small();
        a.limits.spool = full * 2 - 1;
        assert_eq!(a.charge(1, Some(batch)), Err(ResponseBoundsRefusal::Spool));
        assert_eq!(a.totals(), ResponseTotals::default());
        let mut a = small();
        a.limits.candidates = 1;
        assert_eq!(
            a.charge(1, Some(batch)),
            Err(ResponseBoundsRefusal::Candidates)
        );
        assert_eq!(a.totals(), ResponseTotals::default());
    }
    #[test]
    fn response_arithmetic_refuses_overflow_without_saturation_or_partial_counts() {
        for counter in 0..4 {
            let mut a = small();
            a.limits = Limits {
                frame: u64::MAX,
                payload_total: u64::MAX,
                frames: u64::MAX,
                candidates: u64::MAX,
                spool: u64::MAX,
            };
            match counter {
                0 => a.totals.payload_bytes = u64::MAX,
                1 => a.totals.frames = u64::MAX,
                2 => a.totals.candidates = u64::MAX,
                _ => a.totals.spool_bytes = u64::MAX,
            }
            let before = a.totals();
            let candidates = [candidate()];
            let batch = CandidateBatch {
                analysis_ordinal: u64::MAX,
                stage_id: "stage",
                candidates: &candidates,
            };
            assert_eq!(
                a.charge(1, Some(batch)),
                Err(ResponseBoundsRefusal::Overflow)
            );
            assert_eq!(a.totals(), before);
            assert_eq!(a.charge(1, None), Err(ResponseBoundsRefusal::AfterRefusal));
        }
    }

    #[test]
    fn published_bounds_accept_the_last_unit_and_refuse_the_next_without_giant_fixtures() {
        // Seed accounting immediately before each actual published boundary.
        // This tests release-limit arithmetic, not a materialized GiB stream.
        let mut a = ResponseAccounting::new().unwrap();
        assert!(a.charge(a.limits.frame, None).is_ok());
        let mut a = ResponseAccounting::new().unwrap();
        assert_eq!(
            a.charge(a.limits.frame + 1, None),
            Err(ResponseBoundsRefusal::Frame)
        );
        let mut a = ResponseAccounting::new().unwrap();
        a.totals.payload_bytes = a.limits.payload_total - 1;
        assert!(a.charge(1, None).is_ok());
        assert_eq!(a.remaining_payload_bytes(), 0);
        assert_eq!(a.charge(1, None), Err(ResponseBoundsRefusal::PayloadTotal));
        let mut a = ResponseAccounting::new().unwrap();
        a.totals.frames = a.limits.frames - 1;
        assert!(a.charge(1, None).is_ok());
        assert_eq!(a.charge(1, None), Err(ResponseBoundsRefusal::Frames));
        let candidates = [candidate()];
        let batch = CandidateBatch {
            analysis_ordinal: 24,
            stage_id: "stage-😀",
            candidates: &candidates,
        };
        let mut a = ResponseAccounting::new().unwrap();
        a.totals.candidates = a.limits.candidates - 1;
        assert_eq!(a.charge(1, Some(batch)).unwrap().len(), 1);
        assert_eq!(
            a.charge(1, Some(batch)),
            Err(ResponseBoundsRefusal::Candidates)
        );
        let mut a = ResponseAccounting::new().unwrap();
        a.totals.spool_bytes =
            a.limits.spool - entry_length(24, "stage-😀", &candidates[0]).unwrap();
        assert_eq!(a.charge(1, Some(batch)).unwrap().len(), 1);
        assert_eq!(a.totals().spool_bytes, a.limits.spool);
        assert_eq!(a.charge(1, Some(batch)), Err(ResponseBoundsRefusal::Spool));
    }
    #[test]
    fn semantic_length_preflight_matches_the_encoder_at_every_header_width() {
        for n in [
            0,
            23,
            24,
            255,
            256,
            65535,
            65536,
            u32::MAX as u64,
            u32::MAX as u64 + 1,
            u64::MAX,
        ] {
            let candidate = Value::Map(vec![
                ("n".to_owned(), Value::Unsigned(n)),
                ("utf8".to_owned(), Value::Text("😀".repeat(24))),
                (
                    "nested".to_owned(),
                    Value::Array(vec![
                        Value::Null,
                        Value::Bool(true),
                        Value::Bytes(vec![0; 256]),
                    ]),
                ),
            ]);
            assert_eq!(
                cbor::encoded_length(&candidate),
                Some(cbor::encode(&candidate).len() as u64)
            );
            let entry = Value::Map(vec![
                ("candidate".to_owned(), candidate.clone()),
                ("stageId".to_owned(), Value::Text("s".repeat(24))),
                ("analysisOrdinal".to_owned(), Value::Unsigned(n)),
            ]);
            assert_eq!(
                entry_length(n, &"s".repeat(24), &candidate),
                Some(cbor::encode(&entry).len() as u64)
            );
        }
    }
}
