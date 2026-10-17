use super::cbor::{CborRefusal, Profile, Value};
use super::*;

/// A reader that serves `bytes` and records how many it served.
struct Counted<'a> {
    bytes: &'a [u8],
    served: usize,
}
impl Read for Counted<'_> {
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
        let n = buf.len().min(self.bytes.len() - self.served).min(3);
        buf[..n].copy_from_slice(&self.bytes[self.served..self.served + n]);
        self.served += n;
        Ok(n)
    }
}
fn counted(bytes: &[u8]) -> Counted<'_> {
    Counted { bytes, served: 0 }
}
fn frame_of(payload: &[u8]) -> Vec<u8> {
    let mut frame = (payload.len() as u64).to_be_bytes().to_vec();
    frame.extend_from_slice(&raw_sha256(payload));
    frame.extend_from_slice(payload);
    frame
}

#[test]
fn a_frame_round_trips_with_its_exact_payload() {
    let value = Value::Map(vec![
        ("sequence".to_owned(), Value::Unsigned(0)),
        ("frameType".to_owned(), Value::Text("Hello".to_owned())),
    ]);
    let frame = write_frame(&value).unwrap();
    assert_eq!(frame.len(), FRAME_PREFIX_BYTES + cbor::encode(&value).len());
    let two = [frame.clone(), frame.clone()].concat();
    let mut reader = counted(&two);
    for _ in 0..2 {
        let received = read_frame(&mut reader, Profile::Rust3, 8, None)
            .unwrap()
            .unwrap();
        assert_eq!(received.payload(), &frame[FRAME_PREFIX_BYTES..]);
        assert_eq!(
            received.value(),
            &cbor::decode(received.payload(), Profile::Rust3, 8).unwrap()
        );
    }
    // EOF at a frame boundary is not a refusal; the table decides it.
    assert!(
        read_frame(&mut reader, Profile::Rust3, 8, None)
            .unwrap()
            .is_none()
    );
}

#[test]
fn the_length_is_bounded_before_anything_else_is_read() {
    for length in [MAX_FRAME_PAYLOAD_BYTES + 1, u64::MAX] {
        let mut bytes = length.to_be_bytes().to_vec();
        bytes.extend_from_slice(&[0; 64]);
        let mut reader = counted(&bytes);
        let refusal = read_frame(&mut reader, Profile::Ts2, 8, None).unwrap_err();
        assert!(matches!(refusal, FrameRefusal::Oversize(n) if n == length));
        // Only the length was read: no digest byte and no payload byte.
        assert_eq!(reader.served, 8);
    }
    // The stream's remaining aggregate bounds the frame the same way.
    let frame = frame_of(b"\x80");
    let mut reader = counted(&frame);
    assert!(matches!(
        read_frame(&mut reader, Profile::Rust3, 8, Some(0)),
        Err(FrameRefusal::Oversize(1))
    ));
    assert_eq!(reader.served, 8);
    let mut reader = counted(&frame);
    assert!(
        read_frame(&mut reader, Profile::Rust3, 8, Some(1))
            .unwrap()
            .is_some()
    );
}

#[test]
fn truncation_digest_and_payload_refuse() {
    let frame = frame_of(b"\x82\x01\x02");
    for cut in 1..frame.len() {
        let mut reader = counted(&frame[..cut]);
        assert!(
            matches!(
                read_frame(&mut reader, Profile::Rust3, 8, None),
                Err(FrameRefusal::Truncated)
            ),
            "cut {cut}"
        );
    }
    let mut wrong = frame.clone();
    wrong[8] ^= 1;
    assert!(matches!(
        read_frame(&mut counted(&wrong), Profile::Rust3, 8, None),
        Err(FrameRefusal::DigestMismatch)
    ));
    let mut wrong = frame.clone();
    *wrong.last_mut().unwrap() ^= 1;
    assert!(matches!(
        read_frame(&mut counted(&wrong), Profile::Rust3, 8, None),
        Err(FrameRefusal::DigestMismatch)
    ));
    // A zero-length payload is a decode refusal (LD-D2B-12).
    assert!(matches!(
        read_frame(&mut counted(&frame_of(b"")), Profile::Ts2, 8, None),
        Err(FrameRefusal::Cbor(CborRefusal::Truncated))
    ));
    // The decode follows the digest: a canonical digest over a
    // non-canonical payload refuses as CBOR.
    assert!(matches!(
        read_frame(&mut counted(&frame_of(b"\x18\x05")), Profile::Ts2, 8, None),
        Err(FrameRefusal::Cbor(CborRefusal::NonShortest))
    ));
    // A read error is the stream's.
    struct Failing;
    impl Read for Failing {
        fn read(&mut self, _: &mut [u8]) -> io::Result<usize> {
            Err(io::Error::other("broken"))
        }
    }
    assert!(matches!(
        read_frame(&mut Failing, Profile::Ts2, 8, None),
        Err(FrameRefusal::Io(_))
    ));
}

#[test]
fn sequences_step_by_exactly_one_from_zero() {
    let mut sequence = Sequence::default();
    assert!(!sequence.accept(1));
    assert!(sequence.accept(0));
    assert!(!sequence.accept(0));
    assert!(sequence.accept(1));
    assert!(!sequence.accept(3));
    assert_eq!(sequence.next(), 2);
    // The counter never reaches 2^64 - 1.
    let mut last = Sequence { next: u64::MAX };
    assert!(!last.accept(u64::MAX));
}

/// Trial 07's `commit-empty-stream` known answer, and the empty manifest
/// digest `hex(SHA-256(0x80))` (DEPSRC-CUSTODY).
#[test]
fn commitments_and_manifest_digests_have_their_known_answers() {
    let empty = Value::Array(Vec::new());
    let stage_facts = "opensip.rust-provider.stage-facts.v2";
    let known = "sha256:c2949d3ae8fe48685ed7e7ac3460facae8c4c9e5594f16a451aed5ac3c158d5d";
    assert_eq!(received_commitment(stage_facts, &[]), known);
    assert_eq!(built_commitment(stage_facts, &empty), known);
    assert_eq!(
        manifest_digest(&empty),
        "76be8b528d0075f7aae98d6fa57a6d3c83ae480a8469e668d7b0af968995ac71"
    );
    // The domain separator is one zero byte after the domain's UTF-8.
    assert_ne!(
        built_commitment(stage_facts, &empty),
        built_commitment("opensip.rust-provider.stage-facts.v", &empty)
    );
}

fn received(value: &Value) -> ReceivedFrame {
    let frame = write_frame(value).unwrap();
    read_frame(&mut counted(&frame), Profile::Ts2, 8, None)
        .unwrap()
        .unwrap()
}

#[test]
fn every_value_has_its_received_byte_range_in_pre_order() {
    let value = Value::Map(vec![
        (
            "facts".to_owned(),
            Value::Array(vec![
                Value::Unsigned(1),
                Value::Array(vec![Value::Unsigned(2), Value::Text("x".to_owned())]),
                Value::Negative(-1),
            ]),
        ),
        ("batchIndex".to_owned(), Value::Unsigned(0)),
    ]);
    let frame = received(&value);
    // Node 0 is the payload; its members follow in received order, which
    // is encoded-key order: "facts" (5 bytes) before "batchIndex".
    assert_eq!(frame.node(0).unwrap().as_bytes(), frame.payload());
    let members: Vec<usize> = frame.children(0).collect();
    assert_eq!(members.len(), 2);
    assert_eq!(
        frame.node(members[1]).unwrap().as_bytes(),
        cbor::encode(&Value::Unsigned(0))
    );
    let Value::Map(fields) = frame.value() else {
        panic!("a map")
    };
    assert_eq!(fields[0].0, "facts");
    let Value::Array(items) = &fields[0].1 else {
        panic!("facts")
    };
    let elements: Vec<usize> = frame.children(members[0]).collect();
    assert_eq!(elements.len(), items.len());
    for (node, item) in elements.iter().zip(items) {
        assert_eq!(frame.node(*node).unwrap().as_bytes(), cbor::encode(item));
    }
    assert_eq!(frame.children(elements[1]).count(), 2);
    assert!(frame.node(100).is_none());
}

/// LD-D2B-3 item 5 (Codex D2BPLAN-R1-NBO-3): a received commitment's
/// preimage elements are slices of the received payload itself. A
/// re-encoding would give the same digest, so the control observes
/// provenance directly: every element lies inside the payload allocation.
#[test]
fn received_commitments_hash_slices_of_the_received_payload() {
    let facts = Value::Array(vec![
        Value::Text("one".to_owned()),
        Value::Map(vec![("k".to_owned(), Value::Bytes(vec![7; 30]))]),
    ]);
    let frame = received(&Value::Map(vec![("facts".to_owned(), facts.clone())]));
    let array = frame.children(0).next().unwrap();
    let elements: Vec<ReceivedBytes<'_>> = frame
        .children(array)
        .map(|n| frame.node(n).unwrap())
        .collect();
    let payload = frame.payload().as_ptr_range();
    for element in &elements {
        let range = element.as_bytes().as_ptr_range();
        assert!(payload.start <= range.start && range.end <= payload.end);
    }
    let domain = "opensip.ts-provider.fact-batch.v1";
    assert_eq!(
        received_commitment(domain, &elements),
        built_commitment(domain, &facts)
    );
    // Order and domain matter.
    let swapped = [elements[1], elements[0]];
    assert_ne!(
        received_commitment(domain, &swapped),
        received_commitment(domain, &elements)
    );
    assert_ne!(
        received_commitment("opensip.ts-provider.stage-facts.v1", &elements),
        received_commitment(domain, &elements)
    );
}

fn two_frames() -> (Vec<u8>, Vec<Value>) {
    let values = vec![
        Value::Map(vec![("a".to_owned(), Value::Bytes(vec![9; 70]))]),
        Value::Array(vec![Value::Unsigned(1), Value::Text("t".to_owned())]),
    ];
    let stream = values
        .iter()
        .flat_map(|v| write_frame(v).unwrap())
        .collect();
    (stream, values)
}

/// D3a's participant reads a non-blocking stream: the accumulator yields the
/// same frames as `read_frame` however the bytes are split, including one
/// byte at a time, and the boundary is known exactly.
#[test]
fn the_accumulator_yields_the_same_frames_at_every_split() {
    let (stream, values) = two_frames();
    for split in 0..=stream.len() {
        let mut acc = FrameAccumulator::new(Profile::Rust3, 8, None);
        let mut frames = acc.push(&stream[..split]).unwrap();
        frames.extend(acc.push(&stream[split..]).unwrap());
        let got: Vec<&Value> = frames.iter().map(|f| f.value()).collect();
        assert_eq!(got, values.iter().collect::<Vec<_>>(), "split {split}");
        assert!(acc.at_boundary());
        assert!(acc.finish().is_ok());
    }
    let mut acc = FrameAccumulator::new(Profile::Rust3, 8, None);
    let mut count = 0;
    for (at, byte) in stream.iter().enumerate() {
        count += acc.push(std::slice::from_ref(byte)).unwrap().len();
        // Inside a frame EOF is truncation; between frames it is the boundary.
        let boundary = acc.at_boundary();
        assert_eq!(acc.finish().is_ok(), boundary, "byte {at}");
    }
    assert_eq!(count, 2);
}

/// The length is judged when its eighth byte arrives, before any digest or
/// payload byte is kept, against the bound and the remaining aggregate; the
/// aggregate falls by each frame's payload; a refusal ends the stream.
#[test]
fn the_accumulator_bounds_the_length_from_its_eight_bytes() {
    let over = (MAX_FRAME_PAYLOAD_BYTES + 1).to_be_bytes();
    let mut acc = FrameAccumulator::new(Profile::Ts2, 8, None);
    assert!(acc.push(&over[..7]).unwrap().is_empty());
    assert!(matches!(
        acc.push(&over[7..]),
        Err(FrameRefusal::Oversize(n)) if n == MAX_FRAME_PAYLOAD_BYTES + 1
    ));
    assert!(matches!(acc.push(b"x"), Err(FrameRefusal::AfterRefusal)));
    let (stream, _) = two_frames();
    let first = FRAME_PREFIX_BYTES + cbor::encode(&two_frames().1[0]).len();
    let mut acc = FrameAccumulator::new(Profile::Rust3, 8, Some(first as u64 - 40 + 3));
    let frames = acc.push(&stream[..first]).unwrap();
    assert_eq!(frames.len(), 1);
    assert_eq!(acc.remaining(), Some(3));
    // The second frame's payload is longer than the 3 bytes left.
    assert!(matches!(
        acc.push(&stream[first..first + 8]),
        Err(FrameRefusal::Oversize(_))
    ));
    // A digest or decode failure refuses too.
    let mut bad = stream.clone();
    bad[8] ^= 1;
    let mut acc = FrameAccumulator::new(Profile::Rust3, 8, None);
    assert!(matches!(acc.push(&bad), Err(FrameRefusal::DigestMismatch)));
    let mut acc = FrameAccumulator::new(Profile::Rust3, 8, None);
    assert!(matches!(
        acc.push(&frame_of(b"\x18\x05")),
        Err(FrameRefusal::Cbor(CborRefusal::NonShortest))
    ));
}
