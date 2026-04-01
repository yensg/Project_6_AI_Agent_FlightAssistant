from typing import Dict, Optional, Any, List
from datetime import datetime, timezone, timedelta

from openai import api_key

from ..models.orchestrator import Conversation
import logging
from ..core.config import get_settings

from semantic_kernel.kernel import Kernel
from ..infrastracture.azure_openai import AzureOpenAIService

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