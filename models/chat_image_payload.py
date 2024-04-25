from dataclasses import dataclass
from .llm_credentials import LlmCredentials
from .chat_history import MessageHistory
from typing import List


@dataclass
class ChatImagePayload:
    question: str
    credentials: LlmCredentials


@dataclass
class ChatCreativePayload:
    question: str
    credentials: LlmCredentials
    chat_history: List[MessageHistory]
    question: str