from ..utils.logger import setup_logger
from fastapi import FastAPI, Request, HTTPException
from chainlit.server import app as chainlit_app
from fastapi.middleware.cors import CORSMiddleware
from ..core.orchestrator import Orchestrator
from ..models.user import UserInput, UserResponse

logger = setup_logger(__name__)

app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.mount("/", chainlit_app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = Orchestrator()

@app.post("/conversations/{conversation_id}/messages")
async def process_message( conversation_id: str, request: Request, user_input: UserInput):
    try:
        response = await orchestrator(
            conversation_id = conversation_id,
            message = user_input.message
        )
        return UserResponse(
            response = response["response"],
            success = True,
            date = response.get("date"),
            suggestions = response.get("suggestions",[])
        )
    except Exception as e:
        logger.exception(f"Error processing message: {str(e)}")
        raise HTTPException(
            status_code = 500,
            detail = str(e)
        )