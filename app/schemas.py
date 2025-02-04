from pydantic import BaseModel
from typing import List, Optional

class Photo(BaseModel):
    id: int
    owner_id: int
    access_key: Optional[str] = None

class Attachment(BaseModel):
    type: str
    photo: Optional[Photo] = None

class Message(BaseModel):
    peer_id: int
    conversation_message_id: int
    attachments: Optional[List[Attachment]] = []

class VKCallbackObject(BaseModel):
    message: Message

class VKCallbackEvent(BaseModel):
    type: str
    object: Optional[VKCallbackObject] = None