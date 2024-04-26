from abc import ABC, abstractmethod
from models.chat_history import MessageHistory
from models.llm_credentials import LlmCredentials
from typing import List


class LlmHelper(ABC):

    def __init__(self,  credentials: LlmCredentials) -> None:
        self._credentials = credentials
        self.llm = self._get_llm()

    @abstractmethod
    def _get_llm(self):
        pass

    def _build_chat_history(self, chat_history: List[MessageHistory]) -> list:

        history = []
        for message in chat_history:
            if message.role == 'system':
                history.append(("system", message.content))
            elif message.role == 'human':
                history.append(("human", message.content))
            elif message.role == 'assistant':
                history.append(("assistant", message.content))

        return history

    def _build_prompt_template(self, question: str, chat_history: List[MessageHistory]) -> list:

        new_chat_history = self._build_chat_history(chat_history)
        new_chat_history.append(("human", question))

        return new_chat_history
