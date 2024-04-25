from langchain_openai import AzureChatOpenAI
from .llm_helper import LlmHelper



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

    async def chat_stream(self, history: list[dict], question: str) -> str:

        prompt = self._build_prompt_template(question, history)
        for chunk in self.llm.stream(prompt):
            yield chunk.content