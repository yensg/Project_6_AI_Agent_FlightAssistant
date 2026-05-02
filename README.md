# ✈️ AI Agent Flight Assistant (RoamMind)

## 📌 Overview

RoamMind is a **stateful, agentic AI flight assistant** built with:

* **FastAPI** → Backend API layer
* **Chainlit** → Interactive chat UI
* **Azure OpenAI** → LLM reasoning
* **Semantic Kernel** → Tool orchestration
* **Pydantic** → Data validation & schema enforcement

The system follows a **full agentic loop**:

1. Understand user intent
2. Extract structured data
3. Update conversation context
4. Decide tool usage
5. Execute tools
6. Generate final response

---

## 🧠 Architecture

```
Chainlit (UI)
   ↓
HTTP (httpx)
   ↓
FastAPI (API Layer)
   ↓
Orchestrator (State + Control Flow)
   ↓
AzureOpenAIService (LLM Reasoning)
   ↓
Tools / Skills (Flight APIs)
   ↓
Response → UI
```

---

## ⚙️ Installation

### 1. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m ensurepip --upgrade
python -m pip install --upgrade pip setuptools wheel
```

### 2. Install Dependencies

```bash
pip install aiohttp openai pydantic semantic-kernel python-dotenv fastapi uvicorn chainlit httpx
pip freeze > requirements.txt
```

### 3. Setup Git

```bash
git init
touch .gitignore
git add .
git commit -m "Initial commit"

git branch -M main
git remote add origin <repo-url>
git push -u origin main
```

---

## 🔐 Environment Variables (.env)

```env
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini

AVIATIONSTACK_ACCESS_KEY=...
```

---

## 🚀 Running the App

### Run both FastAPI + Chainlit

```bash
python src/main.py
```

### Access:

* FastAPI → http://127.0.0.1:8000
* Chainlit UI → http://127.0.0.1:8501

---

## 🧩 Core Components

### 1. Orchestrator

Responsible for:

* Session lifecycle (create → use → update → expire)
* Calling LLM
* Updating context
* Managing conversation history

```python
process_message():
    cleanup()        # expire sessions
    get_or_create()  # create session
    run_agent()      # execute logic
    save_state()     # persist updates
```

---

### 2. Conversation Models

#### Message

Stores raw chat history

```python
content, role, timestamp
```

#### ConversationContext

Stores structured memory

```python
last_intent
last_entities
preferences
memory
```

#### Conversation

Container for session state

---

### 3. LLM Layer (AzureOpenAIService)

Responsibilities:

* Prompt construction
* Structured extraction
* Tool-calling orchestration

Key idea:

```
LLM = THINK
Tools = ACT
```

---

### 4. Tool System

#### Tool Schema (LLM Interface)

```python
{
  "type": "function",
  "function": {
    "name": "search_flights",
    "parameters": {...}
  }
}
```

#### Tool Types (Validation)

```python
class SearchFlightsArgs(BaseModel):
    airport: str
```

#### Tool Execution

```python
result = await search_flights(**validated_args)
```

---

### 5. Agentic Loop

```python
while True:
    response = call_llm(messages)

    if tool_call:
        result = run_tool()
        messages.append(tool_result)
        continue

    return final_answer
```

---

## 🔄 Context System

### Key Layers

| Layer             | Purpose               |
| ----------------- | --------------------- |
| Raw History       | What user said        |
| Structured Memory | What system remembers |
| Execution Context | What tools need       |

---

### Context Update Flow

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

## ⚠️ Important Design Concepts

### 1. TTL (Session Expiry)

```python
SESSION_TIMEOUT = timedelta(minutes=30)
```

Ensures stale sessions are cleaned.

---

### 2. Async Model

* Use `async` only when needed
* `await` enables concurrency
* `async with` manages resources

---

### 3. Error Handling

```python
response.raise_for_status()
```

* Convert HTTP errors → exceptions
* Validate response structure manually

---

### 4. Schema Separation

| Schema Type      | Purpose            |
| ---------------- | ------------------ |
| Canonical Schema | Guide LLM output   |
| Typed Schema     | Validate in Python |
| Tool Schema      | Enable tool calls  |

---

## 🧪 Common Errors & Fixes

### ❌ ChatHistory error

```
'ChatHistory' object has no attribute 'to_string'
```

✅ Fix: Remove `.to_string()`

---

### ❌ Deployment Not Found

```
DeploymentNotFound
```

✅ Fix: Create deployment in Azure Foundry

---

### ❌ Tool not found

```
KernelFunctionNotFoundError
```

✅ Fix:

* Ensure plugin registered
* Ensure function name matches schema

---

### ❌ JSON Schema error

```
Missing 'required'
```

✅ Fix:

* Add `"required": [...]` for all properties

---

## 📈 Future Improvements

* Add Redis for session persistence
* Add streaming responses
* Improve tool ranking logic
* Add multi-domain support (hotel, excursion)
* Introduce caching with TTL

---

## 🧭 Key Takeaways

* **Orchestrator = brain of system**
* **LLM = reasoning engine**
* **Tools = real-world execution**
* **Context = memory**
* **TTL = lifecycle control**

---

## 👨‍💻 Author Notes

This project demonstrates:

* Agentic system design
* Structured LLM workflows
* Clean separation of concerns
* Production-ready backend patterns

---

## 📜 License

MIT License
