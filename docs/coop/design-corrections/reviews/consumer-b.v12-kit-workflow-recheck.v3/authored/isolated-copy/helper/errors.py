"""Typed refusal codes for independent reconstruction. Not product D9 codes unless mapped later."""


class AdmissionError(Exception):
    def __init__(self, code: str, message: str, *, path: str = "", extra=None):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
        self.path = path
        self.extra = extra or {}

    def as_dict(self):
        d = {"code": self.code, "message": self.message, "path": self.path}
        if self.extra:
            d["extra"] = self.extra
        return d
