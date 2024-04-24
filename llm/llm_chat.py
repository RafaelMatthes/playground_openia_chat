from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI
from openai import NotFoundError, BadRequestError
from openai.types import ImagesResponse

from models.chat_history import MessageHistory
from models.llm_credentials import LlmCredentials


class LlmHelper:

    def __init__(self,  credentials: LlmCredentials) -> None:
        self._credentials = credentials

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


class LlmChat(LlmHelper):

    def _get_llm(self):
        return AzureChatOpenAI(
            openai_api_key=self._credentials.api_key,
            azure_endpoint=self._credentials.endpoint,
            openai_api_version="2023-05-15",
            azure_deployment="gpt-4-32k",
            streaming=True
        )

    def chat_invoke(self, history: list[dict], question: str):
        prompt = self._build_prompt_template(question, history)
        return self.llm.invoke(prompt)

    async def chat_stream(self, history: list[dict], question: str):

        prompt = self._build_prompt_template(question, history)
        for chunk in self.llm.stream(prompt):
            yield chunk.content


class ImageCreatorNotFoundError(Exception):
    pass


class ImageCreatorPolicyError(Exception):
    pass


class LlmImagesCreator(LlmHelper):

    def _get_llm(self):
        return AzureOpenAI(
                api_version="2024-02-01",
                azure_endpoint=self._credentials.endpoint,
                api_key=self._credentials.api_key,
            )

    def create_image(self, history: list[dict], question: str) -> ImagesResponse:

        try:
            llm = self._get_llm()
            return llm.images.generate(
                model="Dalle3",
                prompt=question,
                n=1
            )

        except NotFoundError as err:
            raise ImageCreatorNotFoundError(str(err))
        except BadRequestError as err:
            raise ImageCreatorPolicyError(err)