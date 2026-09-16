//! Required process-output delivery, coordinated by the host.
//!
//! This initial owner covers metadata output only. Atomic artifact publication,
//! committed Run associations and browser launch are separate later operations.
use crate::RenderedResponse;
use std::io::{self, Write};

/// Consume one complete rendered response and deliver all bytes, then flush.
/// Return its settled exit code only after both operations succeed.
///
/// Failure may leave a prefix or even all normal bytes visible. The caller must
/// report the required-output failure through its terminal error path and must
/// not append a replacement envelope or retry this response. This function
/// claims no atomic stdout publication, durability, or rollback of prior work.
/// The output handle is explicitly supplied by ingress; no global stdout,
/// project configuration, store, provider, asset or network is discovered here.
pub fn deliver_required(response: RenderedResponse, mut output: impl Write) -> io::Result<u8> {
    output.write_all(&response.bytes)?;
    output.flush()?;
    Ok(response.exit_code)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[derive(Default)]
    struct Sink {
        bytes: Vec<u8>,
        writes: usize,
        flushes: usize,
        interrupt_first: bool,
        max_chunk: Option<usize>,
        fail_after: Option<usize>,
        fail_flush: bool,
        write_zero: bool,
    }
    impl Write for Sink {
        fn write(&mut self, bytes: &[u8]) -> io::Result<usize> {
            self.writes += 1;
            if self.interrupt_first && self.writes == 1 {
                return Err(io::ErrorKind::Interrupted.into());
            }
            if self.write_zero {
                return Ok(0);
            }
            let remaining = match self.fail_after {
                Some(n) if self.bytes.len() >= n => return Err(io::ErrorKind::BrokenPipe.into()),
                Some(n) => n - self.bytes.len(),
                None => usize::MAX,
            };
            let n = bytes
                .len()
                .min(self.max_chunk.unwrap_or(usize::MAX))
                .min(remaining);
            self.bytes.extend_from_slice(&bytes[..n]);
            Ok(n)
        }
        fn flush(&mut self) -> io::Result<()> {
            self.flushes += 1;
            if self.fail_flush {
                Err(io::ErrorKind::Other.into())
            } else {
                Ok(())
            }
        }
    }
    fn response(exit_code: u8) -> RenderedResponse {
        RenderedResponse {
            bytes: b"complete output\n".to_vec(),
            exit_code,
        }
    }
    #[test]
    fn short_writes_and_interruption_preserve_complete_bytes_and_settled_exit() {
        for exit_code in [0, 2, 4] {
            let mut sink = Sink {
                max_chunk: Some(2),
                interrupt_first: true,
                ..Sink::default()
            };
            assert_eq!(
                deliver_required(response(exit_code), &mut sink).unwrap(),
                exit_code
            );
            assert_eq!(sink.bytes, b"complete output\n");
            assert_eq!(sink.flushes, 1);
            assert!(sink.writes > 2);
        }
    }
    #[test]
    fn every_partial_failure_preserves_only_observed_prefix_without_retry_or_flush() {
        for n in 0..b"complete output\n".len() {
            let mut sink = Sink {
                fail_after: Some(n),
                ..Sink::default()
            };
            let error = deliver_required(response(0), &mut sink).unwrap_err();
            assert_eq!(error.kind(), io::ErrorKind::BrokenPipe);
            assert_eq!(sink.bytes, &b"complete output\n"[..n]);
            assert_eq!(sink.flushes, 0);
            assert_eq!(sink.writes, if n == 0 { 1 } else { 2 });
        }
    }
    #[test]
    fn zero_write_and_flush_failure_never_return_success_exit() {
        let mut sink = Sink {
            write_zero: true,
            ..Sink::default()
        };
        assert_eq!(
            deliver_required(response(0), &mut sink).unwrap_err().kind(),
            io::ErrorKind::WriteZero
        );
        assert!(sink.bytes.is_empty());
        assert_eq!(sink.flushes, 0);
        let mut sink = Sink {
            fail_flush: true,
            ..Sink::default()
        };
        assert!(deliver_required(response(0), &mut sink).is_err());
        assert_eq!(sink.bytes, b"complete output\n");
        assert_eq!(sink.writes, 1);
        assert_eq!(sink.flushes, 1);
    }
    #[test]
    fn even_empty_required_output_must_flush_successfully() {
        let mut sink = Sink {
            fail_flush: true,
            ..Sink::default()
        };
        assert!(
            deliver_required(
                RenderedResponse {
                    bytes: Vec::new(),
                    exit_code: 0
                },
                &mut sink
            )
            .is_err()
        );
        assert_eq!(sink.writes, 0);
        assert_eq!(sink.flushes, 1);
    }
}
