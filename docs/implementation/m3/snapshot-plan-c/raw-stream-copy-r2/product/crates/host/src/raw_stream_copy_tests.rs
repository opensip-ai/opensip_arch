use super::*;
use opensip_identity::raw_sha256;

#[derive(Default)]
struct Check {
    calls: usize,
    stop: Option<usize>,
}
impl CopyCheckpoint for Check {
    type Error = u64;
    fn checkpoint(&mut self) -> Result<(), Self::Error> {
        self.calls += 1;
        if self.stop == Some(self.calls) {
            Err(917)
        } else {
            Ok(())
        }
    }
}
struct Source<'a> {
    bytes: &'a [u8],
    width: usize,
    largest: usize,
    calls: usize,
    interrupted: bool,
}
impl Read for Source<'_> {
    fn read(&mut self, out: &mut [u8]) -> io::Result<usize> {
        self.calls += 1;
        self.largest = self.largest.max(out.len());
        if self.interrupted {
            self.interrupted = false;
            return Err(io::Error::new(io::ErrorKind::Interrupted, "interrupt"));
        }
        let n = out.len().min(self.width).min(self.bytes.len());
        out[..n].copy_from_slice(&self.bytes[..n]);
        self.bytes = &self.bytes[n..];
        Ok(n)
    }
}
#[derive(Default)]
struct Sink {
    data: Vec<u8>,
    width: usize,
    largest: usize,
    flushes: usize,
    interrupt_write: bool,
    interrupt_flush: bool,
}
impl Write for Sink {
    fn write(&mut self, bytes: &[u8]) -> io::Result<usize> {
        self.largest = self.largest.max(bytes.len());
        if self.interrupt_write {
            self.interrupt_write = false;
            return Err(io::Error::new(io::ErrorKind::Interrupted, "interrupt"));
        }
        let n = bytes.len().min(self.width);
        self.data.extend_from_slice(&bytes[..n]);
        Ok(n)
    }
    fn flush(&mut self) -> io::Result<()> {
        self.flushes += 1;
        if self.interrupt_flush {
            self.interrupt_flush = false;
            return Err(io::Error::new(io::ErrorKind::Interrupted, "interrupt"));
        }
        Ok(())
    }
}
#[test]
fn actual_partial_reads_writes_keep_raw_preimage_order_and_fixed_buffers() {
    for len in [0, 1, 3, 4095, 4096, 4097, 65536] {
        let bytes: Vec<u8> = (0..len).map(|i| ((31 * i + 7) % 256) as u8).collect();
        for rwidth in [1, 7, 4096] {
            for wwidth in [1, 13, 4096] {
                let mut source = Source {
                    bytes: &bytes,
                    width: rwidth,
                    largest: 0,
                    calls: 0,
                    interrupted: false,
                };
                let mut sink = Sink {
                    width: wwidth,
                    ..Sink::default()
                };
                let mut check = Check::default();
                let value = copy_raw(&mut source, &mut sink, &mut check).unwrap();
                assert_eq!(value.byte_length, len as u64);
                assert_eq!(value.sha256, raw_sha256(&bytes));
                assert_eq!(sink.data, bytes);
                assert_eq!(sink.flushes, 1);
                assert!(source.largest <= 4096);
                assert!(sink.largest <= 4096);
                assert!(check.calls >= 2);
            }
        }
    }
}
#[test]
fn known_empty_and_abc_vectors() {
    for (bytes, expected) in [
        (
            b"".as_slice(),
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        ),
        (
            b"abc".as_slice(),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
        ),
    ] {
        let mut sink = Sink {
            width: 1,
            ..Sink::default()
        };
        let value = copy_raw(bytes, &mut sink, &mut Check::default()).unwrap();
        let actual: String = value.sha256.iter().map(|b| format!("{b:02x}")).collect();
        assert_eq!(actual, expected);
        assert_eq!(sink.data, bytes);
    }
}
#[test]
fn interrupted_read_write_and_flush_each_retry_through_checkpoint() {
    let mut source = Source {
        bytes: b"abcdef",
        width: 4096,
        largest: 0,
        calls: 0,
        interrupted: true,
    };
    let mut sink = Sink {
        width: 2,
        interrupt_write: true,
        interrupt_flush: true,
        ..Sink::default()
    };
    let mut check = Check::default();
    let value = copy_raw(&mut source, &mut sink, &mut check).unwrap();
    assert_eq!(sink.data, b"abcdef");
    assert_eq!(value.byte_length, 6);
    assert_eq!(source.calls, 3);
    assert_eq!(sink.flushes, 2);
    assert_eq!(check.calls, 9);
}
#[test]
fn owning_stop_before_any_read_yields_no_output() {
    let mut source = Source {
        bytes: b"abc",
        width: 1,
        largest: 0,
        calls: 0,
        interrupted: false,
    };
    let mut sink = Sink {
        width: 1,
        ..Sink::default()
    };
    assert!(matches!(
        copy_raw(
            &mut source,
            &mut sink,
            &mut Check {
                calls: 0,
                stop: Some(1)
            }
        ),
        Err(CopyError::Owner(917))
    ));
    assert_eq!(source.calls, 0);
    assert!(sink.data.is_empty());
    assert_eq!(sink.flushes, 0);
}
#[test]
fn owning_stop_before_write_yields_no_successful_prefix_summary() {
    let mut sink = Sink {
        width: 1,
        ..Sink::default()
    };
    assert!(matches!(
        copy_raw(
            b"abc".as_slice(),
            &mut sink,
            &mut Check {
                calls: 0,
                stop: Some(2)
            }
        ),
        Err(CopyError::Owner(917))
    ));
    assert!(sink.data.is_empty());
    assert_eq!(sink.flushes, 0);
}
#[test]
fn owning_stop_before_flush_refuses_even_when_all_bytes_were_written() {
    let mut sink = Sink {
        width: 4096,
        ..Sink::default()
    };
    assert!(matches!(
        copy_raw(
            b"abc".as_slice(),
            &mut sink,
            &mut Check {
                calls: 0,
                stop: Some(4)
            }
        ),
        Err(CopyError::Owner(917))
    ));
    assert_eq!(sink.data, b"abc");
    assert_eq!(sink.flushes, 0);
}
struct FailedRead;
impl Read for FailedRead {
    fn read(&mut self, _: &mut [u8]) -> io::Result<usize> {
        Err(io::Error::other("exact-read-origin"))
    }
}
#[test]
fn read_error_is_preserved_without_summary_or_flush() {
    let mut sink = Sink {
        width: 1,
        ..Sink::default()
    };
    match copy_raw(FailedRead, &mut sink, &mut Check::default()).unwrap_err() {
        CopyError::Read(e) => assert_eq!(e.to_string(), "exact-read-origin"),
        other => panic!("wrong origin{other:?}"),
    };
    assert!(sink.data.is_empty());
    assert_eq!(sink.flushes, 0);
}
struct FailedWrite {
    flush: bool,
}
impl Write for FailedWrite {
    fn write(&mut self, b: &[u8]) -> io::Result<usize> {
        if self.flush {
            Ok(b.len())
        } else {
            Err(io::Error::other("exact-write-origin"))
        }
    }
    fn flush(&mut self) -> io::Result<()> {
        Err(io::Error::other("exact-flush-origin"))
    }
}
#[test]
fn write_and_flush_errors_preserve_distinct_underlying_values() {
    for (flush, expected) in [(false, "exact-write-origin"), (true, "exact-flush-origin")] {
        match copy_raw(
            b"abc".as_slice(),
            &mut FailedWrite { flush },
            &mut Check::default(),
        )
        .unwrap_err()
        {
            CopyError::Write(e) => assert_eq!(e.to_string(), expected),
            other => panic!("wrong origin{other:?}"),
        };
    }
}
#[test]
fn zero_progress_refuses_without_looping() {
    let mut sink = Sink::default();
    assert!(matches!(
        copy_raw(b"abc".as_slice(), &mut sink, &mut Check::default()),
        Err(CopyError::NoWriteProgress)
    ));
    assert_eq!(sink.flushes, 0);
}
struct BadRead;
impl Read for BadRead {
    fn read(&mut self, b: &mut [u8]) -> io::Result<usize> {
        Ok(b.len() + 1)
    }
}
#[test]
fn invalid_read_contract_does_not_slice_or_write_unobserved_bytes() {
    let mut sink = Sink {
        width: 1,
        ..Sink::default()
    };
    assert!(matches!(
        copy_raw(BadRead, &mut sink, &mut Check::default()),
        Err(CopyError::InvalidReadCount)
    ));
    assert!(sink.data.is_empty());
}
struct BadWrite;
impl Write for BadWrite {
    fn write(&mut self, b: &[u8]) -> io::Result<usize> {
        Ok(b.len() + 1)
    }
    fn flush(&mut self) -> io::Result<()> {
        panic!("no flush after invalid write")
    }
}
#[test]
fn invalid_write_contract_does_not_report_completion() {
    assert!(matches!(
        copy_raw(b"abc".as_slice(), &mut BadWrite, &mut Check::default()),
        Err(CopyError::InvalidWriteCount)
    ));
}
#[test]
fn partial_written_prefix_is_data_only_after_later_stop() {
    let mut sink = Sink {
        width: 1,
        ..Sink::default()
    };
    assert!(matches!(
        copy_raw(
            b"abc".as_slice(),
            &mut sink,
            &mut Check {
                calls: 0,
                stop: Some(3)
            }
        ),
        Err(CopyError::Owner(917))
    ));
    assert_eq!(sink.data, b"a");
    assert_eq!(sink.flushes, 0);
}
