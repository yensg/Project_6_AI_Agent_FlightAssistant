# ✈️ Yen's AI Agent Flight Assistant

## Overview

Yen's AI Agent Flight Assistant is a **stateful, tool-augmented AI flight assistant** built with:

* **FastAPI** → backend API layer
* **Chainlit** → interactive chat UI
* **Azure OpenAI** → LLM reasoning
* **Semantic Kernel** → tool execution layer
* **Pydantic** → schema validation

<img src="Assets/Landing Page.png" alt="first_page" width="500"/>
<img src="Assets/Landing Page 2.png" alt="first_page" width="500"/>

This system is **NOT a full agentic loop**, but a:

> **Single-step reasoning system with optional tool execution + persistent context**

---

## System Architecture

```
Chainlit UI
   ↓ (httpx)
FastAPI API
   ↓
Orchestrator
   ↓
AzureOpenAIService (LLM)
   ↓
(Optional) Tool Call
   ↓
FlightSkill (API)
   ↓
Response → UI
```

---

## Core Behavior

### Execution Flow (Current Design)

```
1. User sends message
2. LLM processes message
3. LLM decides:
   → Respond directly
   → OR call a tool
4. If tool is called:
   → Backend executes tool
   → Return result
5. Response sent to UI
```

---

## Key Components

### 1. Orchestrator

Responsible for:

* session management
* conversation lifecycle
* calling LLM
* updating context

```
cleanup → create → process → update
```

---

### 2. Conversation System

#### Message

Stores raw chat messages

#### ConversationContext

Stores structured memory:

* last intent
* entities
* preferences
* inferred defaults

#### Conversation

Container for full session

---

### 3. LLM Layer (AzureOpenAIService)

Handles:

* prompt construction
* structured extraction
* tool-call detection

---

### 4. Tool System

#### Tool Schema (LLM interface)

Defines:

```
name
parameters
description
```

#### Tool Execution

```
result = await search_flights(**args)
```

---

### 5. Context System

#### Structured Context Flow

```
User message
   ↓
LLM extraction
   ↓
ContextUpdate (validated)
   ↓
update_context()
   ↓
ConversationContext updated
```

---

## State Management

### Session Store

```
session_conversations: Dict[conversation_id, (Conversation, last_active)]
```

### TTL (Session Expiry)

```
SESSION_TIMEOUT = 30 minutes
```

Expired sessions are cleaned automatically.

---

## Design Concepts

### 1. LLM vs Tools

| Component | Role      |
| --------- | --------- |
| LLM       | reasoning |
| Tools     | execution |

---

### 2. Schema Separation

| Type             | Purpose           |
| ---------------- | ----------------- |
| Canonical Schema | guide LLM output  |
| Typed Schema     | validate data     |
| Tool Schema      | enable tool calls |

---

### 3. Async Design

* `await` → enables concurrency
* `async with` → resource management
* Use async only when necessary

---

## 🧪 Common Errors

### ChatHistory issue

```
'ChatHistory' has no attribute 'to_string'
```

✅ Remove usage

---

### Deployment error

```
DeploymentNotFound
```

✅ Fix Azure deployment

---

### Tool not found

```
KernelFunctionNotFoundError
```

✅ Ensure plugin registration matches schema

---

### JSON Schema error

```
Missing 'required'
```

✅ Add required fields

---

## 🚧 Limitations (Current Version)

* No multi-step reasoning
* No tool chaining
* No autonomous planning
* Single LLM decision per request

---

## 🚀 Future Improvements

### 1. Agent Loop

```
while True:
    call LLM
    if tool_call:
        run tool
        append result
        continue
    break
```

### 2. Tool chaining

* flight → hotel → itinerary

### 3. Planning layer

* multi-step task decomposition

---

## Summary

This system is:

> ✅ Stateful
> ✅ Tool-augmented
> ✅ Schema-driven
> ❌ Not fully agentic (yet)

---

## Notes

This project demonstrates:

* real-world backend architecture
* LLM + tool integration
* structured context memory
* production-ready patterns

---

## The step by step guide to build this agentic AI Flight Assistant

A stateful flight assistant built with FastAPI, Chainlit, Azure OpenAI, Semantic Kernel, Pydantic, and external flight APIs.

The project demonstrates how to build an agentic AI application that can:

* receive user messages through a chat UI
* route requests through a FastAPI backend
* maintain conversation state
* extract structured context from user messages
* call LLM tools
* execute backend flight search functions
* return final user-friendly responses

---

## 1. Tech Stack

| Layer        | Technology                    | Purpose                                     |
| ------------ | ----------------------------- | ------------------------------------------- |
| UI           | Chainlit                      | Chat interface                              |
| API          | FastAPI                       | Backend HTTP API                            |
| Server       | Uvicorn                       | ASGI server for FastAPI                     |
| HTTP Client  | httpx                         | Chainlit → FastAPI requests                 |
| LLM          | Azure OpenAI                  | Reasoning and tool-calling                  |
| Tool Runtime | Semantic Kernel               | Register and invoke skills/tools            |
| Validation   | Pydantic                      | Validate user input, context, and tool args |
| Config       | python-dotenv / BaseSettings  | Load `.env` variables                       |
| Flight Data  | Aviationstack / external APIs | Flight search data                          |

---

## 2. Project Architecture

```text
Chainlit UI
   ↓
chat_interface.py
   ↓ call_api()
HTTP POST via httpx
   ↓
FastAPI app.py
   ↓ route handler
Orchestrator
   ↓
AzureOpenAIService
   ↓
LLM tool-calling / context extraction
   ↓
Semantic Kernel
   ↓
FlightSkill
   ↓
External Flight API
   ↓
Final response back to Chainlit
```

---

## 3. Recommended Build Sequence

This is the recommended order to create the project from scratch.

### Step 1 — Create project folder and virtual environment

```bash
mkdir Project_6_AI_Agent_FlightAssistant
cd Project_6_AI_Agent_FlightAssistant

python3 -m venv .venv
source .venv/bin/activate
python -m ensurepip --upgrade
python -m pip install --upgrade pip setuptools wheel
```

### Step 2 — Initialize Git

```bash
git init
touch .gitignore
git add .
git commit -m "Initial commit"

git branch -M main
git remote add origin <repo-url>
git push -u origin main
```

### Step 3 — Install dependencies

```bash
pip install aiohttp openai pydantic pydantic-settings semantic-kernel python-dotenv fastapi uvicorn chainlit httpx
pip freeze > requirements.txt
```

### Step 4 — Create base folder structure

```text
src/
├── api/
│   └── app.py
├── agents/
│   └── flight_agent.py
├── core/
│   ├── config.py
│   └── orchestrator.py
├── infrastructure/
│   └── azure_openai.py
├── models/
│   ├── orchestrator.py
│   └── user.py
├── schemas/
│   ├── context/
│   │   ├── canonical_schema.py
│   │   ├── json_schema.py
│   │   ├── typed_schema.py
│   │   └── updater.py
│   └── tools/
│       ├── json_schema.py
│       └── typed_schema.py
├── skills/
│   └── flight_skill.py
├── utils/
│   └── logger.py
├── chat_interface.py
└── main.py
```

### Step 5 — Build utility files first

Create:

```text
src/utils/logger.py
src/core/config.py
```

These are dependencies used by many other files.

### Step 6 — Build data models

Create:

```text
src/models/user.py
src/models/orchestrator.py
```

Recommended order:

1. `Message`
2. `ConversationContext`
3. `Conversation`
4. `UserInput`
5. `UserResponse`

Reason: `Conversation` depends on `Message` and `ConversationContext`.

### Step 7 — Build context schemas

Create:

```text
src/schemas/context/canonical_schema.py
src/schemas/context/typed_schema.py
src/schemas/context/json_schema.py
src/schemas/context/updater.py
```

Purpose:

| File                  | Purpose                                                  |
| --------------------- | -------------------------------------------------------- |
| `canonical_schema.py` | Human-readable schema to guide the LLM                   |
| `typed_schema.py`     | Pydantic models for Python validation                    |
| `json_schema.py`      | Strict JSON schema for structured LLM output             |
| `updater.py`          | Merge extracted context into stored conversation context |

### Step 8 — Build tool schemas and tool argument validation

Create:

```text
src/schemas/tools/json_schema.py
src/schemas/tools/typed_schema.py
```

Purpose:

| File              | Purpose                                |
| ----------------- | -------------------------------------- |
| `json_schema.py`  | Tool definitions sent to Azure OpenAI  |
| `typed_schema.py` | Pydantic validation for tool arguments |

The tool schema is for the LLM.

The typed schema is for your backend.

### Step 9 — Build the skill layer

Create:

```text
src/skills/flight_skill.py
```

This layer executes real actions, such as:

* `get_flight_details`
* `search_flights`
* `count_flights`
* `list_flights`

This is where external API calls happen.

### Step 10 — Build Azure OpenAI infrastructure layer

Create:

```text
src/infrastructure/azure_openai.py
```

This layer talks to Azure OpenAI.

Responsibilities:

* create OpenAI client
* build messages
* call LLM
* handle tool calls
* parse structured output
* return final response

### Step 11 — Build the agent loop

Create:

```text
src/agents/flight_agent.py
```

This is where the real classic agent loop should live.

```python
async def run(...):
    messages = [...]

    for step in range(MAX_STEPS):
        response = await call_llm(messages)

        if tool_call:
            tool_result = await handle_tool_call(...)
            messages = tool_result["messages"]
            continue

        return final_answer
```

This separates the agent loop from the lower-level Azure OpenAI adapter.

### Step 12 — Build the orchestrator

Create:

```text
src/core/orchestrator.py
```

The orchestrator should handle only application flow:

1. clean expired sessions
2. get or create conversation
3. add user message
4. call agent / Azure service
5. update context
6. add assistant message
7. save conversation state
8. return response

Recommended flow:

```python
process_message():
    cleanup()                 # expire old sessions
    get_or_create()           # create/load session
    add_user_message()        # mutate conversation
    run_agent_logic()         # LLM/tools
    update_context()          # save structured memory
    add_assistant_message()   # save raw reply
    save_session()            # update last_active
```

### Step 13 — Build FastAPI app

Create:

```text
src/api/app.py
```

FastAPI responsibilities:

* define HTTP routes
* parse request body with Pydantic
* call orchestrator
* return response
* convert unexpected errors into HTTP errors

Example route:

```python
@app.post("/conversations/{conversation_id}/messages")
async def process_message(conversation_id: str, user_input: UserInput):
    response = await orchestrator.process_user_input(
        conversation_id=conversation_id,
        message=user_input.message
    )
    return UserResponse(**response)
```

### Step 14 — Build Chainlit interface

Create:

```text
src/chat_interface.py
```

Chainlit responsibilities:

* create `conversation_id`
* store session state with `cl.user_session`
* receive user messages
* call FastAPI via `httpx`
* render response back to UI
* attach optional buttons or structured data

### Step 15 — Build main runner

Create:

```text
src/main.py
```

This starts both servers:

* FastAPI through Uvicorn
* Chainlit through CLI subprocess

---

## 4. Installation

### Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m ensurepip --upgrade
python -m pip install --upgrade pip setuptools wheel
```

### Install libraries

```bash
pip install aiohttp openai pydantic pydantic-settings semantic-kernel python-dotenv fastapi uvicorn chainlit httpx
pip freeze > requirements.txt
```

---

## 5. Environment Variables

Create a `.env` file in the project root.

```env
AZURE_OPENAI_API_KEY="your_azure_openai_key"
AZURE_OPENAI_ENDPOINT="your_azure_openai_endpoint"
AZURE_OPENAI_API_VERSION="2024-02-15-preview"
AZURE_OPENAI_DEPLOYMENT_NAME="your_deployment_name"

AVIATIONSTACK_ACCESS_KEY="your_aviationstack_key"
```

Do not commit `.env` into GitHub.

Recommended `.gitignore`:

```gitignore
.venv/
__pycache__/
*.pyc
.env
.DS_Store
.chainlit/
```

---

## 6. Running the App

```bash
python src/main.py
```

Expected services:

```text
FastAPI:  http://127.0.0.1:8000
Chainlit: http://127.0.0.1:8501
```

---

## 7. `src/main.py`

### Root directory setup

```python
from pathlib import Path
import sys

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))
```

This allows Python to import modules from the project root.

### Run FastAPI programmatically

```python
from src.api.app import app
import uvicorn

async def run_fastapi():
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()
```

### Run Chainlit through CLI

```python
import subprocess
import asyncio

async def run_chainlit():
    process = subprocess.Popen(
        ["chainlit", "run", str(root_dir / "src" / "chat_interface.py"), "-w", "--port", "8501"],
        cwd=str(root_dir)
    )

    try:
        await asyncio.get_event_loop().run_in_executor(None, process.wait)
    except Exception as e:
        process.kill()
        raise e
```

Chainlit does not expose an async server API like Uvicorn, so it is started through the CLI.

### Run both servers

```python
async def main():
    try:
        print("Starting RoamMind servers...")
        print("FastAPI will be available at http://127.0.0.1:8000")
        print("Chainlit UI will be available at http://127.0.0.1:8501")

        await asyncio.gather(
            run_fastapi(),
            run_chainlit()
        )
    except KeyboardInterrupt:
        print("\nShutting down servers...")
    except Exception as e:
        print(f"Error: {str(e)}")
        raise e

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServers stopped.")
```

---

## 8. `src/chat_interface.py`

This is the Chainlit server-side UI controller.

It is not a browser frontend file. It runs on the server and controls the chat UI.

### Runtime flow

```text
1. User opens Chainlit UI
2. Chainlit triggers @cl.on_chat_start
3. User sends message
4. Chainlit triggers @cl.on_message
5. on_message calls call_api()
6. httpx sends HTTP request to FastAPI
7. FastAPI calls orchestrator
8. Orchestrator runs agent logic
9. FastAPI returns JSON
10. Chainlit renders response
```

### `call_api()`

```python
import httpx
from typing import Dict, Any
from datetime import datetime

API_BASE_URL = "http://localhost:8000"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

async def call_api(endpoint: str, method: str = "POST", data: Dict[str, Any] | None = None) -> Dict[str, Any]:
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = f"{API_BASE_URL}{endpoint}"
        try:
            if method == "GET":
                response = await client.get(url, headers=HEADERS)
            elif method == "POST":
                payload = {
                    "message": (data or {}).get("message", ""),
                    "type": (data or {}).get("type", "text"),
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
```

### Key point: `httpx` vs `aiohttp`

| Library   | Behavior                                                          |
| --------- | ----------------------------------------------------------------- |
| `aiohttp` | Gives a live response stream; you usually use nested `async with` |
| `httpx`   | Usually buffers the response; `response.json()` is enough         |

The real difference is lifecycle and response handling.

---

## 9. Decorators in Chainlit

Chainlit uses decorators to register lifecycle functions.

```python
@cl.on_chat_start
async def start():
    ...

@cl.on_message
async def main(message: cl.Message):
    ...

@cl.action_callback("flights")
async def handle_flights(action):
    ...
```

A decorator registers the function so Chainlit knows when to execute it.

Example:

```python
def timer_dec(base_fn):
    def enhanced_fn():
        start_time = time.time()
        base_fn()
        end_time = time.time()
        print(f"Task time: {end_time - start_time} seconds")
    return enhanced_fn

@timer_dec
def brew_tea():
    print("Brewing tea...")
```

---

## 10. `src/api/app.py`

FastAPI receives HTTP requests and forwards them to the orchestrator.

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ..core.orchestrator import Orchestrator
from ..models.user import UserInput, UserResponse
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = Orchestrator()

@app.post("/conversations/{conversation_id}/messages")
async def process_message(conversation_id: str, user_input: UserInput):
    try:
        response = await orchestrator.process_user_input(
            conversation_id=conversation_id,
            message=user_input.message
        )
        return UserResponse(
            response=response["response"],
            success=response.get("success", True),
            data=response.get("data"),
            suggestions=response.get("suggestions", [])
        )
    except Exception as e:
        logger.exception(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 11. User Models

```python
from pydantic import BaseModel
from typing import Optional, Dict, List, Any

class UserInput(BaseModel):
    message: str
    type: Optional[str] = "text"

class UserResponse(BaseModel):
    response: str
    success: bool = True
    data: Optional[Dict[str, Any]] = None
    suggestions: Optional[List[str]] = None
```

Important Pydantic rule:

```python
field: Optional[str]
```

means `None` is allowed.

```python
field: Optional[str] = None
```

means the field is not required.

---

## 12. Conversation Models

### Message

```python
class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    role: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
```

### ConversationContext

Stores structured memory.

```python
class ConversationContext(BaseModel):
    active_domain: str = "flight"
    last_intent: Optional[str] = None
    last_entities: Dict[str, Any] = Field(default_factory=dict)
    preferences: Dict[str, Any] = Field(default_factory=dict)
    memory: Dict[str, Any] = Field(default_factory=dict)
    unresolved_slots: List[str] = Field(default_factory=list)
```

### Conversation

Groups raw messages and structured context.

```python
class Conversation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    context: ConversationContext = Field(default_factory=ConversationContext)
    messages: List[Message] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active: bool = True

    def add_message(self, content: str, role: str):
        message = Message(content=content, role=role)
        self.messages.append(message)
        self.updated_at = datetime.now(timezone.utc)
```

Use `Field(default_factory=list)` instead of `messages: List[Message] = []` to avoid shared mutable defaults.

---

## 13. Context Design

A chat agent needs three things:

| Need                        | Model                 |
| --------------------------- | --------------------- |
| Raw history                 | `Message`             |
| Structured memory           | `ConversationContext` |
| Top-level session container | `Conversation`        |

### Context update flow

```text
User message
   ↓
LLM extraction
   ↓
ContextUpdate
   ↓
update_context()
   ↓
ConversationContext
```

### Update strategy

| Field              | Behavior | Reason                          |
| ------------------ | -------- | ------------------------------- |
| `active_domain`    | replace  | only one active domain          |
| `last_intent`      | replace  | latest intent wins              |
| `last_entities`    | update   | partial information accumulates |
| `preferences`      | update   | preferences grow over time      |
| `memory`           | update   | session facts accumulate        |
| `unresolved_slots` | replace  | current missing fields only     |

---

## 14. Azure OpenAI Layer

`src/infrastructure/azure_openai.py` talks to Azure OpenAI.

It belongs in `infrastructure`, not `utils`, because it connects to an external system.

### Main responsibilities

* create Azure OpenAI client
* build system/user messages
* call `chat.completions.create()`
* provide tools through `tools=FLIGHT_TOOLS`
* inspect `assistant_message.tool_calls`
* parse tool arguments
* invoke tools
* call LLM again for final response

### LLM call with tools

```python
response = await self.client.chat.completions.create(
    model=self.deployment_name,
    messages=messages,
    tools=FLIGHT_TOOLS,
    tool_choice="auto",
    temperature=0.2,
    max_tokens=800,
)
```

`tool_choice="auto"` means the model may call a tool, but it is not forced to.

---

## 15. Tool Calling Flow

```text
1. User asks question
2. LLM receives messages + tool schemas
3. LLM returns tool_calls
4. Backend parses tool name and arguments
5. Backend validates arguments with Pydantic
6. Backend invokes function through Semantic Kernel
7. Tool result is appended back to messages
8. LLM produces final answer
```

The LLM does not execute the tool itself. It only returns the intent to call a tool.

---

## 16. Tool Schema vs Tool Type vs Tool Function

| Part          | Purpose                                |
| ------------- | -------------------------------------- |
| Tool schema   | Interface shown to the LLM             |
| Tool type     | Pydantic validation for backend safety |
| Tool function | Actual executable Python logic         |

### Tool schema

```python
SEARCH_FLIGHTS_TOOL = {
    "type": "function",
    "function": {
        "name": "search_flights",
        "description": "Search flights by airport and direction.",
        "parameters": {
            "type": "object",
            "properties": {
                "airport": {"type": "string"},
                "direction": {"type": "string", "enum": ["arrival", "departure"]},
                "max_results": {"type": "integer"}
            },
            "required": []
        }
    }
}
```

### Tool type

```python
class SearchFlightsArgs(BaseModel):
    airport: str | None = None
    direction: Literal["arrival", "departure"] | None = None
    max_results: int | None = 10
```

### Tool function

```python
async def search_flights(self, airport: str | None = None, direction: str | None = None, max_results: int | None = 10):
    ...
```

---

## 17. Semantic Kernel Tool Invocation

```python
tool_result = await self.kernel.invoke(
    plugin_name="flight_skill",
    function_name=tool_name,
    arguments=kernel_args
)
```

Semantic Kernel may wrap the result.

```python
if hasattr(tool_result, "value"):
    serializable_result = tool_result.value
else:
    serializable_result = str(tool_result)
```

Always unwrap and normalize before sending the result back to the LLM.

---

## 18. Flight Skill Layer

`src/skills/flight_skill.py` is the tool/plugin layer.

It handles actual business execution.

Example:

```python
from semantic_kernel.functions import kernel_function
from typing import Dict, Any

class FlightSkill:
    API_FLIGHT_URL = "http://api.aviationstack.com/v1/flights"
    HEADERS = {"Accept": "application/json"}

    @kernel_function(name="search_flights", description="Search flights")
    async def search_flights(
        self,
        airport: str | None = None,
        direction: str | None = None,
        max_results: int | None = 10,
    ) -> Dict[str, Any]:
        ...
```

---

## 19. Error Handling

### HTTP request lifecycle

```python
response = await client.get(...)
response.raise_for_status()
data = response.json()
flights = data.get("data", [])
```

| Step                 | Possible issue       |
| -------------------- | -------------------- |
| `client.get()`       | network error        |
| `raise_for_status()` | HTTP 4xx/5xx         |
| `response.json()`    | invalid JSON         |
| `data.get("data")`   | unexpected structure |

Validating structure is not automatic. You must decide whether to return fallback data or raise an exception.

---

## 20. Session TTL

TTL means Time To Live.

In this project:

```python
SESSION_TIMEOUT = timedelta(minutes=30)
```

This means conversation sessions expire after 30 minutes of inactivity.

Recommended lifecycle:

```text
expire → create → use → update
```

Cleanup first establishes a system invariant: expired sessions should not be used.

---

## 21. Common Errors and Fixes

### Error 1 — `ChatHistory` has no `to_string()`

```text
'ChatHistory' object has no attribute 'to_string'
```

Fix: do not send `chat_history.to_string()` from Chainlit.

The backend orchestrator already stores authoritative conversation history.

### Error 2 — Azure deployment not found

```text
DeploymentNotFound
```

Fix:

* create a deployment in Azure AI Foundry
* ensure `AZURE_OPENAI_DEPLOYMENT_NAME` matches the deployment name exactly

### Error 3 — Semantic Kernel function not found

```text
KernelFunctionNotFoundError: Function 'list_flights' not found in plugin 'flight_skill'
```

Fix:

* ensure function is decorated with `@kernel_function`
* ensure function name matches the tool schema
* ensure the skill is registered as a plugin

### Error 4 — `save_conversation_state()` missing arguments

```text
TypeError: Orchestrator.save_conversation_state() missing 2 required positional arguments
```

Fix:

Use one consistent design.

Recommended:

```python
async def save_conversation_state(self, conversation: Conversation):
    session_conversations[conversation.id] = (conversation, datetime.now(timezone.utc))
```

Save the whole `Conversation` object instead of passing `message` and `role` separately.

### Error 5 — Strict JSON schema missing `required`

```text
Invalid schema for response_format 'context_update'
```

Fix:

When using strict JSON schema, every object with `properties` must also include `required` with all property keys.

---

## 22. Business Logic vs Infrastructure Logic

| Layer                | Example                                                 | Responsibility                          |
| -------------------- | ------------------------------------------------------- | --------------------------------------- |
| Business logic       | `orchestrator.py`, `flight_agent.py`, `flight_skill.py` | Application decisions and tool behavior |
| Infrastructure logic | `azure_openai.py`, external API clients                 | Connecting to outside services          |
| Schema logic         | `schemas/`                                              | Contracts and validation                |
| UI logic             | `chat_interface.py`                                     | User interaction                        |
| API logic            | `app.py`                                                | HTTP routing                            |

Do not put Azure OpenAI code in `utils`, because it is not a generic helper. It is infrastructure.

---

## 23. Async Rules

Use `async` when the function needs to `await` something.

Common examples:

* HTTP calls
* database calls
* LLM calls
* file/network I/O
* external services

Key idea:

```text
async def returns a coroutine
await gets the actual result
```

`async with` manages resource setup and cleanup. It does not itself create concurrency. Concurrency happens when execution reaches `await`.

---

## 24. Future Improvements

* Move session storage from memory to Redis
* Add persistent database storage
* Add streaming responses
* Add better retry handling
* Add structured logging
* Add test suite
* Add multi-domain agents: hotel, excursion, restaurant
* Add caching with TTL
* Add tool result summarization before sending back to LLM

---

## 25. Key Takeaways

* `Chainlit` controls the chat UI.
* `FastAPI` exposes backend routes.
* `httpx` sends HTTP requests from Chainlit to FastAPI.
* `Orchestrator` manages session lifecycle and application flow.
* `AzureOpenAIService` talks to the LLM.
* `FlightSkill` executes real-world actions.
* `Pydantic` validates unsafe input before execution.
* `Semantic Kernel` registers and invokes tools.
* `ConversationContext` stores structured memory.
* `Conversation` groups the full session.
* TTL prevents stale sessions from living forever.

---

## License

MIT
