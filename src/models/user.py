from pydantic import BaseModel, Dict, List, Any
from typing import Optional

class UserInput(BaseModel):
    message: str
    type: Optional[str] = "text"

class UserResponse(BaseModel):
    response: str
    success: bool = True
    date: Optional[Dict[str, Any]] = None
    suggestions: Optional[List[str]] = None