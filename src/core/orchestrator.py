from typing import Dict, Optional, Any, List
from datetime import datetime, timezone, timedelta
from ..models.orchestrator import Conversation
import logging
from ..core.config import get_settings

session_conversations: Dict[str, tuple[Conversation, datetime]] = {}

SESSION_TIMEOUT = timedelta(minutes=30)

class Orchestrator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        settings = get_settings()