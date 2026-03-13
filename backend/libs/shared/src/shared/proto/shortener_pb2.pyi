from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ResolveRequest(_message.Message):
    __slots__ = ("short_code",)
    SHORT_CODE_FIELD_NUMBER: _ClassVar[int]
    short_code: str
    def __init__(self, short_code: _Optional[str] = ...) -> None: ...

class ResolveResponse(_message.Message):
    __slots__ = ("original_url", "url_id", "is_active")
    ORIGINAL_URL_FIELD_NUMBER: _ClassVar[int]
    URL_ID_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    original_url: str
    url_id: str
    is_active: bool
    def __init__(self, original_url: _Optional[str] = ..., url_id: _Optional[str] = ..., is_active: bool = ...) -> None: ...
