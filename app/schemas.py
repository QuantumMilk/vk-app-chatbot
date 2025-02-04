from pydantic import BaseModel
from typing import List, Optional

class Photo(BaseModel):
    id: int
    owner_id: int
    access_key: Optional[str] = None

class Attachment(BaseModel):
    type: str
    photo: Optional[Photo] = None

class Action(BaseModel):
    type: str
    member_id: Optional[int] = None

class Message(BaseModel):
    peer_id: int
    conversation_message_id: int
    text: str = ""
    attachments: Optional[List[Attachment]] = []
    action: Optional[Action] = None

class VKCallbackObject(BaseModel):
    message: Message

class VKCallbackEvent(BaseModel):
    type: str
    object: Optional[VKCallbackObject] = None