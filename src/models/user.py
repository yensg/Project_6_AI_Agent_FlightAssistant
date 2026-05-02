from pydantic import BaseModel
from typing import Optional, Dict, List, Any

class UserInput(BaseModel):
    message: str
    type: Optional[str] = "text"

class UserResponse(BaseModel):
    response: str
    success: bool = True
    date: Optional[Dict[str, Any]] = None
    suggestions: Optional[List[str]] = None