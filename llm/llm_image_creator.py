import json
from openai import AzureOpenAI
from openai import NotFoundError, BadRequestError
from openai.types import ImagesResponse
from typing import List

from models.chat_history import MessageHistory
from models.llm_credentials import LlmCredentials

from .llm_helper import LlmHelper
from .llm_chat import LlmChat

from dotenv import load_dotenv
import os

load_dotenv()


class ImageCreatorNotFoundError(Exception):
    pass


class ImageCreatorPolicyError(Exception):
    pass


class ImageDescriptionError(Exception):
    pass


class LlmImagesCreator(LlmHelper):

    def _get_llm(self):
        return AzureOpenAI(
                api_version="2024-02-01",
                azure_endpoint=self._credentials.endpoint,
                api_key=self._credentials.api_key,
            )

    def create_image(self, question: str) -> ImagesResponse:

        print(question)

        try:
            return self.llm.images.generate(
                model="Dalle3",
                prompt=question,
                size="1024x1024",
                n=1,
                quality="standard",
                style="vivid"
            )

        except NotFoundError as err:
            raise ImageCreatorNotFoundError(str(err))
        
        except BadRequestError as err:
            raise ImageCreatorPolicyError(err)


class LlmCreativeImageCreator(LlmImagesCreator):

    TEMPLATE = """Você é uma IA que ajuda pessoas criando imagens, quando o humano lhe fizer uma pergunta, 
    vc deve descrever em detalhes uma imagem que irá responder a pergunta, dê preferência a descrição de 
    imagens anteriores caso exista, desde que seja totalmente descrita novamente. A sua resposta deverá 
    ser estruturada somente em um dicionário {"img": " ", "mensagem": " "}, onde o campo "img" é utilizado 
    para a descrição da imagem e "mensagem" para qualquer mensagem que não faça parte da descrição de imagem. 
    Não utilize aspas no seu texto."""

    def _create_creative_prompt(self, chat_history: List[MessageHistory], question: str) -> str:
        try:
            template_msg = MessageHistory(**{"role": "system", "content": self.TEMPLATE})
            chat_history.insert(0, template_msg)

            # FIXME: deverá ser fornecido via endpoint, porém no momento
            # existem 2 serviços ativos, cada um deles faz apenas uma tarefa
            # ideial seria ter 1 serviço com as duas funcionalidades ativadas.
            # fix_me_credendtials = LlmCredentials(**{
            #         "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT", ""),
            #         "api_key": os.getenv("AZURE_OPENAI_API_KEY", "")
            #     })

            # chain_chat = LlmChat(
            #     fix_me_credendtials
            chain_chat = LlmChat(
                self._credentials
            ).chat_invoke(
                chat_history=chat_history,
                question=question
            )
            
            try:
                chain_response = json.loads(chain_chat.content.replace("'", "\""))
                return chain_response['img']
            except ValueError:
                return chain_chat.content
            
        except NotFoundError as err:
            raise ImageCreatorNotFoundError(str(err))

        except BadRequestError as err:
            raise ImageCreatorPolicyError(err)
        
        except Exception as err:
            raise ImageDescriptionError(f"erro ao converter resposta em dict: {err}")

    def creative_chat(self, chat_history: List[MessageHistory], question: str) -> ImagesResponse:

        return self.create_image(
            question=self._create_creative_prompt(chat_history, question)
        )
