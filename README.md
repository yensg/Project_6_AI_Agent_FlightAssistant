# ✈️ Yen's AI Agent Flight Assistant

## 📌 Overview

Yen's AI Agent Flight Assistant is a **stateful, tool-augmented AI flight assistant** built with:

* **FastAPI** → backend API layer
* **Chainlit** → interactive chat UI
* **Azure OpenAI** → LLM reasoning
* **Semantic Kernel** → tool execution layer
* **Pydantic** → schema validation

<img src="Assets/Landing Page.png" alt="first_page" width="500"/>
<img src="Assets/Landing Page 2.png" alt="first_page" width="500"/>

This system is **NOT a full agentic loop**, but a:

> ✅ **Single-step reasoning system with optional tool execution + persistent context**

---

## 🧠 System Architecture

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

## ⚙️ Core Behavior

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

### ❗ Important

This is **NOT an agentic loop** because:

* No iterative reasoning
* No multi-step planning
* No repeated LLM calls

---

## 🧩 Key Components

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

## 🔄 State Management

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

## ⚠️ Important Design Concepts

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

## 🧭 Summary

This system is:

> ✅ Stateful
> ✅ Tool-augmented
> ✅ Schema-driven
> ❌ Not fully agentic (yet)

---

## 👨‍💻 Notes

This project demonstrates:

* real-world backend architecture
* LLM + tool integration
* structured context memory
* production-ready patterns

---

## 📜 License

MIT