import socket
import uuid
import base64
import binascii
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, field_validator

class ApiStatus(BaseModel):
    timestamp: datetime | None = datetime.now()
    method: Literal["GET", "POST", "PUT", "DELETE"]
    hostname: str | None = socket.gethostname()
    base_url: str | None = None
    url_path: str | None = None
    message: str | None = None


class TxtFile(BaseModel):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4)
    name: str
    filename: str | None = None
    comment: str | None = None

    def model_post_init(self, __context):
        if self.filename is None:
            self.filename = self.name

    
class TxtFileWithData(TxtFile):
    data: str | None = None

    @field_validator("data")
    def validate_base64(cls, v: str) -> str:
        try:
            base64.b64decode(v, validate=True)
        except binascii.Error:
            raise ValueError("Value is not valid Base64")
        return v


class TxtFileAppend(BaseModel):
    id: uuid.UUID
    path: str | None = "/"
    @field_validator("path", mode="before")
    def normalize_path(cls, v):
        if v == "": return "/"
        return v


class IsoFile(BaseModel):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4)
    name: str
    comment: str | None = None
    label: str | None = ""
    text_files: list[TxtFileAppend] | None = []


