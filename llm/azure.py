import os

from langchain_core.messages import HumanMessage, AIMessage
from langchain.memory import ChatMessageHistory
from langchain_openai import AzureChatOpenAI
from langchain.prompts import (
        ChatPromptTemplate,
        MessagesPlaceholder,
        SystemMessagePromptTemplate,
        HumanMessagePromptTemplate,
    )
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
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

    def _build_prompt_template(self, chat_history=MessageHistory) -> ChatPromptTemplate:

        chat_old_messages = self._build_chat_history(chat_history)

        prompt = ChatPromptTemplate.from_messages(
            messages=chat_old_messages
        )

        return prompt

    async def chat_llm_with_history(self, history: list[dict], question: str):

        prompt = self._build_prompt_template(history)
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        conversation_chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
            verbose=True,
            memory=memory
        )

        for chunk in conversation_chain({"question": question})['text']:
            yield chunk

