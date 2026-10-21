//! M3-D r5 items 10 and 11 (unit D2b): the provider codecs, one per
//! protocol, selected before spawn. D2b-1 lands the shared wire mechanics:
//! the strict deterministic-CBOR profiles ([`cbor`]), the frame prefix
//! (`uint64` big-endian payload length, then 32 raw SHA-256 bytes of the
//! payload; DLV:1111, RPP:160-170), the length checked against
//! `maxFramePayloadBytes` before any allocation, the per-direction sequences,
//! and the commitment and manifest-digest functions (DLV:1077; RPP:209-219).
//! Nothing here translates a provider frame (item 11): a frame's payload
//! bytes are kept exactly as received, and every commitment is computed from
//! them.
use opensip_identity::{RawSha256, digest_hex, raw_sha256};
use std::io::{self, Read};

pub mod cbor;
pub mod table;
pub mod ts2;

/// `maxFramePayloadBytes` (DLV:658; RPP:97; NE:2962).
pub const MAX_FRAME_PAYLOAD_BYTES: u64 = 67_108_864;
/// The frame prefix: the 8-byte length and the 32-byte digest.
pub const FRAME_PREFIX_BYTES: usize = 40;

/// Why one frame read refused. Every refusal is `PROVIDER.PROTOCOL_VIOLATION`
/// with this detail (RPP:168; DLV:1111).
#[derive(Debug)]
pub enum FrameRefusal {
    /// The stream ended inside a frame's prefix or payload.
    Truncated,
    /// The declared payload length exceeds the bound, refused before any
    /// payload byte is read or allocated.
    Oversize(u64),
    /// The payload's SHA-256 is not the prefix's digest.
    DigestMismatch,
    /// The payload is not one canonical item of the selected profile.
    Cbor(cbor::CborRefusal),
    /// The stream failed.
    Io(io::Error),
    /// A frame was pushed after the accumulator refused: a refusal ends the
    /// stream.
    AfterRefusal,
}

/// One received frame: its exact payload bytes, their decoded value, and
/// each value's received byte range.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ReceivedFrame {
    payload: Vec<u8>,
    value: cbor::Value,
    spans: Vec<cbor::Span>,
}
impl ReceivedFrame {
    pub fn payload(&self) -> &[u8] {
        &self.payload
    }
    pub fn value(&self) -> &cbor::Value {
        &self.value
    }
    /// Node `index`'s received bytes: node 0 is the payload, then each
    /// value in pre-order (map keys are not nodes).
    pub fn node(&self, index: usize) -> Option<ReceivedBytes<'_>> {
        let span = self.spans.get(index)?;
        Some(ReceivedBytes(&self.payload[span.start..span.end]))
    }
    /// The nodes whose container is node `index`, in received order.
    pub fn children(&self, index: usize) -> impl Iterator<Item = usize> + '_ {
        self.spans
            .iter()
            .enumerate()
            .filter(move |(_, span)| span.parent == Some(index))
            .map(|(child, _)| child)
    }
}

/// A received value's exact bytes, borrowed from the frame that carried
/// them. Only [`ReceivedFrame::node`] makes one, so a commitment over
/// received bytes can never be handed a re-encoding (LD-D2B-3 item 5).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ReceivedBytes<'a>(&'a [u8]);
impl<'a> ReceivedBytes<'a> {
    pub fn as_bytes(&self) -> &'a [u8] {
        self.0
    }
}

/// Read exactly `buf.len()` bytes; EOF before any byte is `Ok(false)`, EOF
/// after some is truncation.
fn read_exact_or_eof(reader: &mut impl Read, buf: &mut [u8]) -> Result<bool, FrameRefusal> {
    let mut filled = 0;
    while filled < buf.len() {
        match reader.read(&mut buf[filled..]) {
            Ok(0) if filled == 0 => return Ok(false),
            Ok(0) => return Err(FrameRefusal::Truncated),
            Ok(n) => filled += n,
            Err(error) if error.kind() == io::ErrorKind::Interrupted => {}
            Err(error) => return Err(FrameRefusal::Io(error)),
        }
    }
    Ok(true)
}

/// Read one frame (LD-D2B-12's order): the length, the bound, the digest,
/// exactly the payload, the digest's check, then the strict decode and the
/// re-encode comparison. `Ok(None)` is EOF at a frame boundary, which only the
/// transition table may accept (RPP:170). `remaining` is the stream's
/// aggregate payload allowance, when its protocol has one (RPP:143-146).
pub fn read_frame(
    reader: &mut impl Read,
    profile: cbor::Profile,
    max_depth: usize,
    remaining: Option<u64>,
) -> Result<Option<ReceivedFrame>, FrameRefusal> {
    let mut length = [0u8; 8];
    if !read_exact_or_eof(reader, &mut length)? {
        return Ok(None);
    }
    let length = u64::from_be_bytes(length);
    if length > MAX_FRAME_PAYLOAD_BYTES || remaining.is_some_and(|r| length > r) {
        return Err(FrameRefusal::Oversize(length));
    }
    let mut digest = [0u8; 32];
    if !read_exact_or_eof(reader, &mut digest)? {
        return Err(FrameRefusal::Truncated);
    }
    let mut payload = vec![0u8; length as usize];
    if !payload.is_empty() && !read_exact_or_eof(reader, &mut payload)? {
        return Err(FrameRefusal::Truncated);
    }
    if raw_sha256(&payload) != digest {
        return Err(FrameRefusal::DigestMismatch);
    }
    let (value, spans) =
        cbor::decode_spanned(&payload, profile, max_depth).map_err(FrameRefusal::Cbor)?;
    Ok(Some(ReceivedFrame {
        payload,
        value,
        spans,
    }))
}

/// Incremental frame acquisition for a non-blocking stream (LD-D2B-12 steps 1
/// to 6, as `read_frame` performs them over a blocking one): bytes are pushed
/// as they arrive, in any split, and the partial prefix and payload are kept
/// across calls. The length is judged against the bound and the remaining
/// aggregate as soon as its 8 bytes are whole, before any digest or payload
/// byte is copied; the payload is allocated only then. A frame completes when
/// its payload is whole, then its digest and strict decode are checked. A
/// refusal ends the stream, after every frame completed before it: the frames
/// and the refusal are `read_frame`'s, in its order, at every split.
#[derive(Debug)]
pub struct FrameAccumulator {
    profile: cbor::Profile,
    max_depth: usize,
    remaining: Option<u64>,
    prefix: [u8; FRAME_PREFIX_BYTES],
    have: usize,
    payload: Option<Vec<u8>>,
    refused: bool,
}
impl FrameAccumulator {
    /// A new stream under `profile`, with `remaining` its aggregate payload
    /// allowance when its protocol has one (RPP:143-146).
    pub fn new(profile: cbor::Profile, max_depth: usize, remaining: Option<u64>) -> Self {
        Self {
            profile,
            max_depth,
            remaining,
            prefix: [0; FRAME_PREFIX_BYTES],
            have: 0,
            payload: None,
            refused: false,
        }
    }
    /// Push the next bytes: every frame they complete, in wire order, then
    /// the refusal that ended the stream, if one did. After a refusal every
    /// push is `AfterRefusal`, with no frame.
    pub fn push(&mut self, mut bytes: &[u8]) -> Pushed {
        let mut pushed = Pushed {
            frames: Vec::new(),
            refusal: None,
        };
        if self.refused {
            pushed.refusal = Some(FrameRefusal::AfterRefusal);
            return pushed;
        }
        while !bytes.is_empty() {
            match self.step(&mut bytes) {
                Ok(Some(frame)) => pushed.frames.push(frame),
                Ok(None) => {}
                Err(refusal) => {
                    self.refused = true;
                    pushed.refusal = Some(refusal);
                    break;
                }
            }
        }
        pushed
    }
    /// Consume what one frame still needs from `bytes`.
    fn step(&mut self, bytes: &mut &[u8]) -> Result<Option<ReceivedFrame>, FrameRefusal> {
        // The length's 8 bytes, and nothing past them, then its bound.
        if self.have < 8 {
            self.take_prefix(bytes, 8);
            if self.have < 8 {
                return Ok(None);
            }
            let length = self.length();
            if length > MAX_FRAME_PAYLOAD_BYTES || self.remaining.is_some_and(|r| length > r) {
                return Err(FrameRefusal::Oversize(length));
            }
        }
        // Only then the digest's 32, and only then the payload's allocation.
        if self.have < FRAME_PREFIX_BYTES {
            self.take_prefix(bytes, FRAME_PREFIX_BYTES);
            if self.have < FRAME_PREFIX_BYTES {
                return Ok(None);
            }
            self.payload = Some(Vec::with_capacity(self.length() as usize));
        }
        let length = self.length() as usize;
        let payload = self
            .payload
            .as_mut()
            .expect("the payload follows the prefix");
        let take = (length - payload.len()).min(bytes.len());
        payload.extend_from_slice(&bytes[..take]);
        *bytes = &bytes[take..];
        if payload.len() < length {
            return Ok(None);
        }
        let payload = self.payload.take().expect("a whole payload");
        let mut digest = [0u8; 32];
        digest.copy_from_slice(&self.prefix[8..]);
        self.have = 0;
        if raw_sha256(&payload) != digest {
            return Err(FrameRefusal::DigestMismatch);
        }
        if let Some(remaining) = &mut self.remaining {
            *remaining -= payload.len() as u64;
        }
        let (value, spans) = cbor::decode_spanned(&payload, self.profile, self.max_depth)
            .map_err(FrameRefusal::Cbor)?;
        Ok(Some(ReceivedFrame {
            payload,
            value,
            spans,
        }))
    }
    /// Copy the prefix's bytes from `bytes` up to offset `to`, no further.
    fn take_prefix(&mut self, bytes: &mut &[u8], to: usize) {
        let take = (to - self.have).min(bytes.len());
        self.prefix[self.have..self.have + take].copy_from_slice(&bytes[..take]);
        self.have += take;
        *bytes = &bytes[take..];
    }
    fn length(&self) -> u64 {
        let mut length = [0u8; 8];
        length.copy_from_slice(&self.prefix[..8]);
        u64::from_be_bytes(length)
    }
    /// Whether the stream stands at a frame boundary: no partial prefix or
    /// payload is held. EOF here is the boundary, which only the transition
    /// table may accept (RPP:170).
    pub fn at_boundary(&self) -> bool {
        self.have == 0
    }
    /// EOF: at a boundary it is no refusal; inside a frame it is truncation.
    pub fn finish(&self) -> Result<(), FrameRefusal> {
        if self.refused {
            Err(FrameRefusal::AfterRefusal)
        } else if self.at_boundary() {
            Ok(())
        } else {
            Err(FrameRefusal::Truncated)
        }
    }
    /// The aggregate payload allowance still remaining, if the protocol has
    /// one.
    pub fn remaining(&self) -> Option<u64> {
        self.remaining
    }
}

/// What one [`FrameAccumulator::push`] yields: the frames it completed, in
/// wire order, then the refusal that ended the stream, if one did. A frame
/// completed before a refusal is never lost (Codex D2B1-R1-RF-1).
#[derive(Debug)]
pub struct Pushed {
    pub frames: Vec<ReceivedFrame>,
    pub refusal: Option<FrameRefusal>,
}

/// The process events the supervisor feeds a participant (LD-D2B-6; M3-D
/// r5 item 13, :470): exactly the protocols' own, `zero-exit`, `eof` and
/// the four `*PROCESS_FAULT` members (P3T:75-85; T2O:61-68; RPP:652). Unit
/// D3a-1 lands it here with LD-D2B-6's shape (D3a plan r4, LD-D3A-3, Q2);
/// D2b-3 and D2b-4 consume it unchanged.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ProcessEvent {
    ZeroExit,
    Eof,
    Fault(ProcessFault),
}
/// A `*PROCESS_FAULT` member. `Deadline` is delivered only when a host
/// deadline expires while the participant waits on the child (item 13;
/// RPP:601); a death the host caused for any other cause is `SignalDeath`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ProcessFault {
    Deadline,
    NonzeroExit,
    SignalDeath,
    StdoutByte,
}
impl ProcessEvent {
    /// The event's frame in both tables (P3T:75-85; T2O:61-68).
    pub fn frame(self) -> &'static str {
        match self {
            Self::ZeroExit => "zero-exit",
            Self::Eof => "eof",
            Self::Fault(ProcessFault::Deadline) => "deadline",
            Self::Fault(ProcessFault::NonzeroExit) => "nonzero-exit",
            Self::Fault(ProcessFault::SignalDeath) => "signal-death",
            Self::Fault(ProcessFault::StdoutByte) => "stdout-byte",
        }
    }
    /// The table engine's event for it (D2b-2's `table::Event`).
    pub fn table_event(self) -> table::Event {
        table::Event::frame(self.frame())
    }
}

/// One frame's bytes for `value`: the prefix, then its deterministic
/// encoding. A payload over the bound is not written.
pub fn write_frame(value: &cbor::Value) -> Option<Vec<u8>> {
    let payload = cbor::encode(value);
    if payload.len() as u64 > MAX_FRAME_PAYLOAD_BYTES {
        return None;
    }
    let mut frame = (payload.len() as u64).to_be_bytes().to_vec();
    frame.extend_from_slice(&raw_sha256(&payload));
    frame.extend_from_slice(&payload);
    Some(frame)
}

/// A direction's sequence (DLV:1123; RPP:674-679): from 0, stepping by
/// exactly 1; a duplicate, skip, decrease or overflow is a protocol fault.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct Sequence {
    next: u64,
}
impl Sequence {
    /// Accept `seq` if it is the next one.
    pub fn accept(&mut self, seq: u64) -> bool {
        if seq != self.next || seq == u64::MAX {
            return false;
        }
        self.next += 1;
        true
    }
    pub fn next(&self) -> u64 {
        self.next
    }
}

/// `C(d, v) = "sha256:" + lowerhex(SHA-256(UTF8(d) || 0x00 || dCBOR(v)))`
/// (DLV:1077) over the preimage's parts, in order.
fn commitment_over<'p>(domain: &str, parts: impl IntoIterator<Item = &'p [u8]>) -> String {
    let mut digest = RawSha256::new()
        .update(domain.as_bytes())
        .and_then(|h| h.update(&[0]))
        .expect("a domain is within the digest's domain");
    for part in parts {
        digest = digest
            .update(part)
            .expect("a commitment is within the digest's domain");
    }
    format!("sha256:{}", digest_hex(&RawSha256::finish(digest)))
}

/// `C(d, v)` for `v` an array of received values (every `commitmentMap`
/// value class a worker's frames carry: stage entries, candidates, batch
/// facts), over their received bytes in order (LD-D2B-3). The array head
/// is computed from the count, which canonicality makes the reference's.
pub fn received_commitment(domain: &str, elements: &[ReceivedBytes<'_>]) -> String {
    let mut head = Vec::with_capacity(9);
    cbor::head(&mut head, 4, elements.len() as u64);
    commitment_over(
        domain,
        std::iter::once(head.as_slice()).chain(elements.iter().map(|e| e.as_bytes())),
    )
}

/// `C(d, v)` for a value the host builds (a request domain, a subject
/// scope), over its deterministic encoding.
pub fn built_commitment(domain: &str, value: &cbor::Value) -> String {
    commitment_over(domain, [cbor::encode(value).as_slice()])
}

/// A manifest digest: `hex(SHA-256(dCBOR(entries)))`, with no domain and no
/// prefix (TS2-MANIFEST-DIGEST, RAW-MANIFEST-DIGEST), over the host's
/// entries.
pub fn manifest_digest(entries: &cbor::Value) -> String {
    digest_hex(&raw_sha256(&cbor::encode(entries)))
}

#[cfg(test)]
#[path = "provider_protocol_tests.rs"]
mod tests;
