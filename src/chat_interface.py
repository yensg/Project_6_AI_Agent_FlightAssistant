import httpx
from typing import Dict, Any, Optional
from datetime import datetime
import chainlit as cl
import uuid
from semantic_kernel.contents.chat_history import ChatHistory
import json

API_BASE_URL = "http://localhost:8000"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

async def call_api(endpoint: str, method: str = "POST", data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Make API calls to FastAPI backend."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = f"{API_BASE_URL}{endpoint}"
        # Ensures data is always a dictionary so it can be safely passed to params or json.
        data = data or {}
        try:
            if method == "GET":
                response = await client.get(url, headers=HEADERS)
            elif method == "POST":
                payload = {
                    "message": data.get("message", ""),
                    "type": data.get("type", "text"),
                    "timestamp": datetime.now().isoformat()
                }
                response = await client.post(url, headers=HEADERS, json=payload)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(f"API error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            raise Exception(f"Request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")

@cl.on_chat_start
async def start():
    """Initialize chat session."""
    conversation_id = str(uuid.uuid4())
    cl.user_session.set("conversation_id", conversation_id)

    # Initialize chat history
    chat_history = ChatHistory()
    cl.user_session.set("chat_history", chat_history)

    welcome_message = """👋 Welcome to Yen's Travel Assistant!

I can help you with:
- Flight searches and booking information

How can I assist you today?"""

    await cl.Message(
        content=welcome_message,
        actions=[
            cl.Action(
                name="flights",
                value="Search flights",
                label="✈️ Flights",
                payload={"category": "flights"}
            )
        ]
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """Handle user messages."""
    conversation_id = cl.user_session.get("conversation_id")
    chat_history = cl.user_session.get("chat_history")

    if not conversation_id:
        conversation_id = str(uuid.uuid4())
        cl.user_session.set("conversation_id", conversation_id)

    if not chat_history:
        chat_history = ChatHistory()
        cl.user_session.set("chat_history", chat_history)

    async with cl.Step() as step:
        try:
            # Add user message to history
            chat_history.add_user_message(message.content)

            # Show typing indicator
            await cl.Message(content="").send()

            response = await call_api(
                f"/conversations/{conversation_id}/messages",
                method="POST",
                data={
                    "message": message.content,
                    "chat_history": chat_history.to_string()
                }
            )

            # Add assistant response to history
            response_text = response.get("response", "No response received")
            chat_history.add_assistant_message(response_text)

            # Create response message
            msg = cl.Message(content=response_text)

            # Add structured data if available
            if response.get("data"):
                msg.elements = [
                    cl.Text(
                        content=json.dumps(response["data"], indent=2),
                        language="json",
                        name="Details"
                    )
                ]

            # Add suggestions as actions
            if response.get("suggestions"):
                msg.actions = [
                    cl.Action(
                        name=f"suggestion_{i}",
                        value=suggestion,
                        label=suggestion,
                        payload={"type": "suggestion"}
                    ) for i, suggestion in enumerate(response["suggestions"])
                ]

            await msg.send()

        except Exception as e:
            error_message = f"⚠️ Error: {str(e)}"
            await cl.Message(content=error_message).send()

@cl.action_callback("flights")
async def handle_flights(action):
    """Handle flight search actions."""
    await main(cl.Message(content="Show me available flights"))