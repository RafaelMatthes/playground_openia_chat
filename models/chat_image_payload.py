from dataclasses import dataclass
from .llm_credentials import LlmCredentials


@dataclass
class ChatImagePayload:
    question: str
    credentials: LlmCredentials