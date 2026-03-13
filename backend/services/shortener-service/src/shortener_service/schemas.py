import uuid
from datetime import datetime

from pydantic import BaseModel, HttpUrl


class URLCreate(BaseModel):
    original_url: HttpUrl
    custom_code: str | None = None


class ShortenRequest(BaseModel):
    original_url: HttpUrl


class ShortenResponse(BaseModel):
    short_code: str
    original_url: str

    model_config = {"from_attributes": True}


class URLResponse(BaseModel):
    id: uuid.UUID
    short_code: str
    original_url: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
