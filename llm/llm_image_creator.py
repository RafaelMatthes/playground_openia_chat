from openai import AzureOpenAI
from openai import NotFoundError, BadRequestError
from openai.types import ImagesResponse

from .llm_helper import LlmHelper


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

    def create_image(self, chat_history: list[dict], question: str) -> ImagesResponse:

        try:
            # llm = self._get_llm()
         
            # return llm.images.generate(
            #     model="Dalle3",
            #     prompt=question,
            #     n=1
            # )

            return self.llm.images.generate(
                model="Dalle3",
                prompt=question,
                size="1024x1024",
                n=1,
                quality="hd",
                style="vivid"
            )

        except NotFoundError as err:
            raise ImageCreatorNotFoundError(str(err))
        except BadRequestError as err:
            raise ImageCreatorPolicyError(err)