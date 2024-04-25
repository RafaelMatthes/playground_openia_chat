from dataclasses import dataclass
from .chat_history import MessageHistory
from typing import List
from .llm_credentials import LlmCredentials


@dataclass
class ChatPayload:
    chat_history: List[MessageHistory]
    question: str
    credentials: LlmCredentials
    stream: bool = True