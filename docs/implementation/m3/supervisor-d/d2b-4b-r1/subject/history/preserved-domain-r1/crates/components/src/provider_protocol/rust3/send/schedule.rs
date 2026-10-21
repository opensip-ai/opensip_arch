//! Mechanical REQUEST-WIRE-ACCOUNTING and immutable slot recording.
//! Host shape/context construction and independent sender realization remain
//! separate, so arithmetic agreement cannot substitute for either check.
use super::super::super::cbor::{self, Value};
use opensip_identity::raw_sha256;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(super) enum Frame {
    Hello,
    OpenUniverse,
    SnapshotManifest,
    SnapshotFileChunk,
    SnapshotSeal,
    DependencySourceManifest,
    DependencySourceChunk,
    DependencySourceSeal,
    PreparedOutputManifest,
    PreparedOutputChunk,
    PreparedOutputSeal,
    Analyze,
}
impl Frame {
    pub(super) fn name(self) -> &'static str {
        match self {
            Self::Hello => "Hello",
            Self::OpenUniverse => "OpenUniverse",
            Self::SnapshotManifest => "SnapshotManifest",
            Self::SnapshotFileChunk => "SnapshotFileChunk",
            Self::SnapshotSeal => "SnapshotSeal",
            Self::DependencySourceManifest => "DependencySourceManifest",
            Self::DependencySourceChunk => "DependencySourceChunk",
            Self::DependencySourceSeal => "DependencySourceSeal",
            Self::PreparedOutputManifest => "PreparedOutputManifest",
            Self::PreparedOutputChunk => "PreparedOutputChunk",
            Self::PreparedOutputSeal => "PreparedOutputSeal",
            Self::Analyze => "Analyze",
        }
    }
    fn is_chunk(self) -> bool {
        matches!(
            self,
            Self::SnapshotFileChunk | Self::DependencySourceChunk | Self::PreparedOutputChunk
        )
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub(super) enum Entry {
    Snapshot(String),
    Dependency { package_key: String, path: String },
    Prepared(u64),
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub(super) struct Chunk {
    pub entry: Entry,
    pub index: u64,
    pub offset: u64,
    pub length: u64,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub(super) struct Slot {
    pub sequence: u64,
    pub frame: Frame,
    pub chunk: Option<Chunk>,
    pub total_chunk_count: Option<u64>,
    pub payload_bytes: u64,
    pub payload_sha256: [u8; 32],
    pub entry_content_sha256: Option<String>,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(super) struct Bounds {
    pub frame_bytes: u64,
    pub payload_bytes: u64,
    pub frames: u64,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(super) struct Totals {
    pub payload_bytes: u64,
    pub frames: u64,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub(super) enum Refusal {
    Arithmetic,
    FrameLimit { sequence: u64, bytes: u64 },
    PayloadLimit,
    FrameCountLimit,
    Shape(&'static str),
    SlotCount,
}

fn head(n: u64) -> u64 {
    match n {
        0..=23 => 1,
        24..=255 => 2,
        256..=65_535 => 3,
        65_536..=4_294_967_295 => 5,
        _ => 9,
    }
}
pub(super) fn chunk_count(length: u64, maximum: u64) -> Result<u64, Refusal> {
    if maximum == 0 {
        return Err(Refusal::Shape("zero chunk maximum"));
    }
    (length / maximum)
        .checked_add(u64::from(length % maximum != 0))
        .ok_or(Refusal::Arithmetic)
}
pub(super) fn envelope(sequence: u64, name: &str, payload: Value) -> Value {
    Value::Map(vec![
        ("protocolMajor".into(), Value::Unsigned(3)),
        ("direction".into(), Value::Text("host-to-worker".into())),
        ("sequence".into(), Value::Unsigned(sequence)),
        ("frameType".into(), Value::Text(name.into())),
        ("payload".into(), payload),
    ])
}
fn envelope_length_for_payload(sequence: u64, name: &str, length: u64) -> Result<u64, Refusal> {
    // The null probe has the exact envelope overhead. Replacing its one-byte
    // value does not change the envelope map head or any other member.
    cbor::encoded_length(&envelope(sequence, name, Value::Null))
        .and_then(|n| n.checked_sub(1))
        .and_then(|n| n.checked_add(length))
        .ok_or(Refusal::Arithmetic)
}
pub(super) fn envelope_length(sequence: u64, name: &str, payload: &Value) -> Result<u64, Refusal> {
    envelope_length_for_payload(
        sequence,
        name,
        cbor::encoded_length(payload).ok_or(Refusal::Arithmetic)?,
    )
}
pub(super) fn chunk_envelope_length(
    sequence: u64,
    frame: Frame,
    header: &Value,
    length: u64,
) -> Result<u64, Refusal> {
    let Value::Map(fields) = header else {
        return Err(Refusal::Shape("chunk header map"));
    };
    if !frame.is_chunk() || fields.iter().any(|(k, _)| k == "bytes") {
        return Err(Refusal::Shape("chunk header excludes bytes"));
    }
    let count = u64::try_from(fields.len()).map_err(|_| Refusal::Arithmetic)?;
    let payload = cbor::encoded_length(header)
        .and_then(|n| n.checked_sub(head(count)))
        .and_then(|n| count.checked_add(1).and_then(|k| n.checked_add(head(k))))
        // Deterministic CBOR text key "bytes": one-byte head and five bytes.
        .and_then(|n| n.checked_add(6))
        .and_then(|n| n.checked_add(head(length)))
        .and_then(|n| n.checked_add(length))
        .ok_or(Refusal::Arithmetic)?;
    envelope_length_for_payload(sequence, frame.name(), payload)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub(super) struct Schedule {
    pub slots: Vec<Slot>,
    pub cancel_reserve_bytes: u64,
    pub totals: Totals,
}
/// The expected ordinary-slot count is computed from entry lengths before
/// allocation. It also gives the maximal Cancel sequence. The reserve already
/// includes its maximal actual correlation echo, not an invented uint64-MAX
/// sequence or arbitrary longer execution identifier.
pub(super) struct Recorder {
    bounds: Bounds,
    expected: u64,
    schedule: Schedule,
}
impl Recorder {
    pub(super) fn new(
        bounds: Bounds,
        expected: u64,
        cancel_reserve_bytes: u64,
    ) -> Result<Self, Refusal> {
        let frames = expected.checked_add(1).ok_or(Refusal::Arithmetic)?;
        if frames > bounds.frames {
            return Err(Refusal::FrameCountLimit);
        }
        if cancel_reserve_bytes > bounds.frame_bytes {
            return Err(Refusal::FrameLimit {
                sequence: expected,
                bytes: cancel_reserve_bytes,
            });
        }
        if cancel_reserve_bytes > bounds.payload_bytes {
            return Err(Refusal::PayloadLimit);
        }
        Ok(Self {
            bounds,
            expected,
            schedule: Schedule {
                slots: Vec::new(),
                cancel_reserve_bytes,
                totals: Totals {
                    payload_bytes: cancel_reserve_bytes,
                    frames: 1,
                },
            },
        })
    }
    pub(super) fn sequence(&self) -> Result<u64, Refusal> {
        u64::try_from(self.schedule.slots.len()).map_err(|_| Refusal::Arithmetic)
    }
    fn next_totals(&self, length: u64) -> Result<Totals, Refusal> {
        let sequence = self.sequence()?;
        if sequence >= self.expected {
            return Err(Refusal::SlotCount);
        }
        if length > self.bounds.frame_bytes {
            return Err(Refusal::FrameLimit {
                sequence,
                bytes: length,
            });
        }
        let payload_bytes = self
            .schedule
            .totals
            .payload_bytes
            .checked_add(length)
            .ok_or(Refusal::Arithmetic)?;
        let frames = self
            .schedule
            .totals
            .frames
            .checked_add(1)
            .ok_or(Refusal::Arithmetic)?;
        if payload_bytes > self.bounds.payload_bytes {
            return Err(Refusal::PayloadLimit);
        }
        if frames > self.bounds.frames {
            return Err(Refusal::FrameCountLimit);
        }
        Ok(Totals {
            payload_bytes,
            frames,
        })
    }
    pub(super) fn fixed(
        &mut self,
        frame: Frame,
        payload: &Value,
        total_chunk_count: Option<u64>,
    ) -> Result<(), Refusal> {
        if frame.is_chunk() {
            return Err(Refusal::Shape("fixed chunk slot"));
        }
        let sequence = self.sequence()?;
        let length = envelope_length(sequence, frame.name(), payload)?;
        let totals = self.next_totals(length)?;
        // The complete wire payload and slot allocation follow checked
        // frame/request/count charging. Nothing is retained on refusal.
        let hash = raw_sha256(&cbor::encode(payload));
        self.schedule.slots.push(Slot {
            sequence,
            frame,
            chunk: None,
            total_chunk_count,
            payload_bytes: length,
            payload_sha256: hash,
            entry_content_sha256: None,
        });
        self.schedule.totals = totals;
        Ok(())
    }
    pub(super) fn chunk(
        &mut self,
        frame: Frame,
        header: &Value,
        coordinates: &Chunk,
        last_digest: Option<&str>,
    ) -> Result<(), Refusal> {
        if coordinates.length == 0 {
            return Err(Refusal::Shape("zero-length chunk"));
        }
        let class_matches = matches!(
            (frame, &coordinates.entry),
            (Frame::SnapshotFileChunk, Entry::Snapshot(_))
                | (Frame::DependencySourceChunk, Entry::Dependency { .. })
                | (Frame::PreparedOutputChunk, Entry::Prepared(_))
        );
        if !class_matches {
            return Err(Refusal::Shape("chunk entry class"));
        }
        let sequence = self.sequence()?;
        let length = chunk_envelope_length(sequence, frame, header, coordinates.length)?;
        let totals = self.next_totals(length)?;
        let hash = raw_sha256(&cbor::encode(header));
        self.schedule.slots.push(Slot {
            sequence,
            frame,
            chunk: Some(coordinates.clone()),
            total_chunk_count: None,
            payload_bytes: length,
            payload_sha256: hash,
            entry_content_sha256: last_digest.map(str::to_owned),
        });
        self.schedule.totals = totals;
        Ok(())
    }
    pub(super) fn finish(self) -> Result<Schedule, Refusal> {
        if self.sequence()? != self.expected {
            return Err(Refusal::SlotCount);
        }
        Ok(self.schedule)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn header(count: usize) -> Value {
        Value::Map(
            (0..count)
                .map(|n| (format!("key{n:02}"), Value::Unsigned(n as u64)))
                .collect(),
        )
    }
    #[test]
    fn chunk_measurement_matches_real_encoding_at_all_heads_without_a_dummy_buffer() {
        for size in [0, 1, 23, 24, 255, 256, 65_535, 65_536, 1_048_576] {
            for keys in [0, 4, 23, 24] {
                for sequence in [0, 23, 24, 255, 256, u64::MAX] {
                    let h = header(keys);
                    let Value::Map(mut full) = h.clone() else {
                        unreachable!()
                    };
                    full.push(("bytes".into(), Value::Bytes(vec![0x81; size])));
                    let encoded =
                        cbor::encode(&envelope(sequence, "SnapshotFileChunk", Value::Map(full)));
                    assert_eq!(
                        chunk_envelope_length(sequence, Frame::SnapshotFileChunk, &h, size as u64),
                        Ok(encoded.len() as u64)
                    );
                }
            }
        }
        assert_eq!(
            chunk_envelope_length(0, Frame::SnapshotFileChunk, &header(4), u64::MAX),
            Err(Refusal::Arithmetic)
        );
    }
    #[test]
    fn request_totals_include_one_reserved_cancel_and_refuse_before_retaining_a_slot() {
        let payload = Value::Null;
        let n = envelope_length(0, "Hello", &payload).unwrap();
        let bounds = Bounds {
            frame_bytes: n,
            payload_bytes: n + 3,
            frames: 2,
        };
        let mut r = Recorder::new(bounds, 1, 3).unwrap();
        r.fixed(Frame::Hello, &payload, None).unwrap();
        let s = r.finish().unwrap();
        assert_eq!(
            s.totals,
            Totals {
                frames: 2,
                payload_bytes: n + 3
            }
        );
        assert_eq!(s.cancel_reserve_bytes, 3);
        let mut r = Recorder::new(
            Bounds {
                payload_bytes: n + 2,
                ..bounds
            },
            1,
            3,
        )
        .unwrap();
        let before = r.schedule.clone();
        assert_eq!(
            r.fixed(Frame::Hello, &payload, None),
            Err(Refusal::PayloadLimit)
        );
        assert_eq!(r.schedule, before);
        assert!(matches!(
            Recorder::new(
                Bounds {
                    frames: 1,
                    ..bounds
                },
                1,
                3
            ),
            Err(Refusal::FrameCountLimit)
        ));
        assert!(matches!(
            Recorder::new(bounds, u64::MAX, 3),
            Err(Refusal::Arithmetic)
        ));
    }
    #[test]
    fn huge_declared_chunks_overflow_counts_or_refuse_without_materializing_their_bytes() {
        assert_eq!(chunk_count(0, 1_048_576), Ok(0));
        assert_eq!(chunk_count(1_048_576, 1_048_576), Ok(1));
        assert_eq!(chunk_count(1_048_577, 1_048_576), Ok(2));
        assert_eq!(chunk_count(u64::MAX, 1), Ok(u64::MAX));
        assert_eq!(chunk_count(u64::MAX, 2), Ok(1 << 63));
        assert!(chunk_count(1, 0).is_err());
        let mut r = Recorder::new(
            Bounds {
                frame_bytes: 128,
                payload_bytes: 128,
                frames: 2,
            },
            1,
            1,
        )
        .unwrap();
        let before = r.schedule.clone();
        let c = Chunk {
            entry: Entry::Snapshot("src/lib.rs".into()),
            index: 0,
            offset: 0,
            length: u64::MAX,
        };
        assert_eq!(
            r.chunk(Frame::SnapshotFileChunk, &header(4), &c, None),
            Err(Refusal::Arithmetic)
        );
        assert_eq!(r.schedule, before);
    }
}
