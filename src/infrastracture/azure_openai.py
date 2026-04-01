from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class AzureOpenAIService:
    def __init__(self, kernel):
        self.kernel = kernel