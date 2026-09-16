"""Proposed final required output operation. Reference only; no host custody."""
import copy

ENVELOPE_MAX_BYTES = 4 * 1024 * 1024
DIAGNOSTIC = b"opensip: OUTPUT.SERIALIZATION_FAILED\n"


class SerializationFailure(Exception):
    """Trusted admission/codec failure already mapped by the host owner."""


class Finalizer:
    def __init__(self, aggregate, output_fault, class_to_exit):
        # These are private admitted owner values in the product, not public
        # caller-controlled dictionaries. Synthetic dictionaries model them here.
        self.aggregate = copy.deepcopy(aggregate)
        self.output_fault = copy.deepcopy(output_fault)
        self.class_to_exit = copy.deepcopy(class_to_exit)
        self.committed = None
        self.commit_count = 0

    def deliver(self, envelope, admit_and_encode, writer, diagnostic_writer):
        if self.committed is not None:
            raise RuntimeError("finalization-already-committed")
        # Owner admission checks the rest of the envelope; this exact join is
        # independently required at the output boundary.
        failed = False
        try:
            if envelope.get("termination") != self.aggregate:
                raise SerializationFailure("aggregate-envelope-mismatch")
            if envelope.get("exitCode") != self.class_to_exit[self.aggregate["class"]]:
                raise SerializationFailure("aggregate-exit-mismatch")
            raw = admit_and_encode(envelope)
            if type(raw) is not bytes or not raw or len(raw) > ENVELOPE_MAX_BYTES:
                raise SerializationFailure("envelope-codec-output")
            self._write_all(writer, raw)
            writer.flush()
        except (SerializationFailure, OSError):
            failed = True
        termination = self.output_fault if failed else self.aggregate
        if failed:
            try:
                self._write_all(diagnostic_writer, DIAGNOSTIC)
                diagnostic_writer.flush()
            except OSError:
                pass
        self.committed = copy.deepcopy(termination)
        self.commit_count += 1
        return {"termination": copy.deepcopy(termination),
                "exitCode": self.class_to_exit[termination["class"]],
                "delivery": "failed" if failed else "complete"}

    @staticmethod
    def _write_all(writer, raw):
        view = memoryview(raw)
        offset = 0
        while offset < len(raw):
            count = writer.write(view[offset:])
            if type(count) is not int or count <= 0 or count > len(raw) - offset:
                raise OSError("invalid-writer-progress")
            offset += count

    def after_commit(self, event):
        if self.committed is None:
            raise RuntimeError("finalization-not-committed")
        if event not in ("user-signal", "transport-close", "optional-delivery-failure"):
            raise ValueError("not-an-after-commit-event")
        return copy.deepcopy(self.committed)
