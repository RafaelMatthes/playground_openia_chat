import os

from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

from models.chat_history import MessageHistory

load_dotenv()


class Llm_chat():

    def __init__(self) -> None:
        self.llm = AzureChatOpenAI(
            openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            openai_api_version="2023-05-15",
            azure_deployment="gpt-4-32k",
            streaming=True
        )

    def _build_chat_history(self, chat_history: MessageHistory) -> list:
        history = []
        for message in chat_history:

            if message.role == 'system':
                history.append(("system", message.content))
            elif message.role == 'user':
                history.append(("human", message.content))
            elif message.role == 'assistant':
                history.append(("assistant", message.content))

        history.append(("human", "{question}"))
        return history

    def _build_prompt_template(self, question: str, chat_history: MessageHistory) -> list:

        new_chat_history = self._build_chat_history(chat_history)
        new_chat_history.append(("human", question))

        return new_chat_history
    
    def chat_invoke(self, history: list[dict], question: str):
        prompt = self._build_prompt_template(question, history)
        return self.llm.invoke(prompt)

    async def chat_stream(self, history: list[dict], question: str):

        prompt = self._build_prompt_template(question, history)
        for chunk in self.llm.stream(prompt):
            yield chunk.content

