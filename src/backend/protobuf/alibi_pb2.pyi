from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class StudentFaceRequest(_message.Message):
    __slots__ = ["accuracy", "detected_name", "image_data_b64"]
    ACCURACY_FIELD_NUMBER: _ClassVar[int]
    DETECTED_NAME_FIELD_NUMBER: _ClassVar[int]
    IMAGE_DATA_B64_FIELD_NUMBER: _ClassVar[int]
    accuracy: float
    detected_name: str
    image_data_b64: str
    def __init__(self, detected_name: _Optional[str] = ..., accuracy: _Optional[float] = ..., image_data_b64: _Optional[str] = ...) -> None: ...

class StudentFaceResponse(_message.Message):
    __slots__ = ["message", "success"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    message: str
    success: bool
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...
