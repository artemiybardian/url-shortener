from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ClickEvent(_message.Message):
    __slots__ = ("url_id", "short_code", "ip_address", "user_agent", "referrer", "country")
    URL_ID_FIELD_NUMBER: _ClassVar[int]
    SHORT_CODE_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    REFERRER_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    url_id: str
    short_code: str
    ip_address: str
    user_agent: str
    referrer: str
    country: str
    def __init__(self, url_id: _Optional[str] = ..., short_code: _Optional[str] = ..., ip_address: _Optional[str] = ..., user_agent: _Optional[str] = ..., referrer: _Optional[str] = ..., country: _Optional[str] = ...) -> None: ...

class LogResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
