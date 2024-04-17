from dataclasses import dataclass
from .chat_history import MessageHistory


@dataclass
class ChatPayload:
    chat_history: list[MessageHistory]
    question: str