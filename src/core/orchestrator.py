from typing import Dict, Optional, Any, List
from datetime import datetime, timezone, timedelta

# from openai import api_key

from ..models.orchestrator import Conversation
import logging
from ..core.config import get_settings

from semantic_kernel.kernel import Kernel
from ..infrastracture.azure_openai import AzureOpenAIService

from ..skills.flight_skill import FlightSkill
from ..schemas.context.typed_schema import ConversationContext
import uuid

session_conversations: Dict[str, tuple[Conversation, datetime]] = {}


SESSION_TIMEOUT = timedelta(minutes=30)

class Orchestrator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        settings = get_settings()

        self.kernel = Kernel(
            endpoint = settings.azure_openai_endpoint,
            api_key = settings.azure_openai_api_key
        )
        self.azure_service = AzureOpenAIService(self.kernel)

        self.flight_skill = FlightSkill()
        self.kernel.add_plugin(self.flight_skill, plugin_name="flight_skill")

    def cleanup_session(self, conversation_id: str) -> None:
        """Clean up session data when conversation ends."""
        if conversation_id in session_conversations:
            del session_conversations[conversation_id]

    # no I/O so no need async
    def load_conversation_history(self, conversation_id:str) -> Optional[tuple[Conversation, datetime]]:
        """Load conversation history from memory."""
        return session_conversations.get(conversation_id)

    def _cleanup_expired_sessions(self) -> None:
        """Remove expired sessions."""
        now = datetime.now(timezone.utc)
        expired_ids = [
            conversation_id
            for conversation_id, (_, last_active) in session_conversations.items()
            if now - last_active > SESSION_TIMEOUT
        ]

        for conversation_id in expired_ids:
            del session_conversations[conversation_id]

    async def save_conversation_state(self, conversation_id: str, message: str, role: str) -> None:
        """Save conversation state in memory with timestamp."""
        try:
            self._cleanup_expired_sessions()

            if conversation_id not in session_conversations:
                conversation = Conversation(
                    id=conversation_id,
                    context=ConversationContext(),
                    messages=[]
                )
                session_conversations[conversation_id] = (conversation, datetime.now(timezone.utc))

            conversation, _ = session_conversations[conversation_id]
            conversation.add_message(content=message, role=role)
            session_conversations[conversation_id] = (conversation, datetime.now(timezone.utc))

        except Exception as e:
            self.logger.error(f"Error saving conversation state: {str(e)}")
            raise

    async def get_or_create_conversation(self, conversation_id: str) -> Conversation:
        """Retrieve a conversation from session storage if not expired. Otherwise, create a new session"""
        self._cleanup_expired_sessions()

        if conversation_id in session_conversations:
            conversation, _ = session_conversations[conversation_id]
            session_conversations[conversation_id] = (
                conversation,
                datetime.now(timezone.utc)
            )
            return conversation

        conversation = Conversation(
            id=conversation_id,
            context=ConversationContext()
        )
        session_conversations[conversation_id] = (
            conversation,
            datetime.now(timezone.utc)
        )
        return conversation

    async def process_user_input(
            self,
            conversation_id: str,
            user_message: str,
    ) -> Dict[str, Any]:
        conversation = await self.get_or_create_conversation(conversation_id)
        # but what if there's no historical session based on that id?

        # save user message first
        conversation.add_message(content=user_message, role="user")

        try:
            result = await self.azure_service.process_message(
                message=user_message,
                context=conversation.context,
            )

            # update context if returned
            if "context_update" in result and result["context_update"] is not None:
                conversation.context = result["context_update"]

            assistant_response = result.get(
                "response",
                "Sorry, I could not process your request."
            )

            conversation.add_message(content=assistant_response, role="assistant")
            await self.save_conversation_state(conversation)

            return {
                "success": result.get("decision_type") != "error",
                "conversation_id": conversation.id,
                "response": assistant_response,
                "decision_type": result.get("decision_type"),
                "context": conversation.context.model_dump(),
                "tool_name": result.get("tool_name"),
                "tool_args": result.get("tool_args"),
                "tool_result": result.get("tool_result"),
                "suggestions": [],
            }

        except Exception as e:
            self.logger.exception("Error processing user input")
            return {
                "success": False,
                "conversation_id": conversation_id,
                "response": f"Error: {str(e)}",
                "decision_type": "error",
                "context": conversation.context.model_dump() if conversation else {},
                "tool_name": None,
                "tool_args": None,
                "tool_result": None,
                "suggestions": [],
            }