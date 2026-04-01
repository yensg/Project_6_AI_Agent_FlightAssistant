from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid
from typing import Dict, List, Optional, Any

class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    role: str  # 'user' or 'assistant'
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # def to_dict(self) -> Dict:
    #     return {
    #         "id": self.id,
    #         "content": self.content,
    #         "role": self.role,
    #         "timestamp": self.timestamp.isoformat()
    #     }

class ConversationContext(BaseModel):
    user_id: str
    memory: Dict[str, Any] = {}
    session_id: Optional[str] = None
    preferences: Dict[str, Any] = {}
    last_intent: Optional[str] = None
    last_entities: Dict[str, Any] = {}

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types

    # def to_dict(self) -> Dict:
    #     return {
    #         "user_id": self.user_id,
    #         "memory": self.memory,
    #         "session_id": self.session_id,
    #         "preferences": self.preferences,
    #         "last_intent": self.last_intent,
    #         "last_entities": self.last_entities
    #     }

class Conversation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    context: ConversationContext
    messages: List[Message] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active: bool = True

    def add_message(self, content: str, role: str):
        message = Message(content=content, role=role)
        self.messages.append(message)
        self.updated_at = datetime.now(timezone.utc)

    # def to_dict(self) -> Dict:
    #     return {
    #         "id": self.id,
    #         "user_id": self.user_id,
    #         "context": self.context.to_dict(),
    #         "messages": [m.to_dict() for m in self.messages],
    #         "created_at": self.created_at.isoformat(),
    #         "updated_at": self.updated_at.isoformat(),
    #         "active": self.active
    #     }