from fastapi import APIRouter, Body, HTTPException
from models.chat_image_payload import ChatImagePayload, ChatCreativePayload
from openai.types import ImagesResponse

from llm.llm_image_creator import (
    LlmImagesCreator, 
    LlmCreativeImageCreator,
    ImageCreatorNotFoundError, 
    ImageCreatorPolicyError
)

dall_e = APIRouter()


@dall_e.post('/create', status_code=200)
async def create_images(chat_payload: ChatImagePayload = Body(...)) -> ImagesResponse:
    try:
        return LlmImagesCreator(
                credentials=chat_payload.credentials
            ).create_image( 
                question=chat_payload.question
            )

    except ImageCreatorNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
    except ImageCreatorPolicyError as err:
        raise HTTPException(status_code=400, detail=str(err))


@dall_e.post('/creative_chat', status_code=200)
async def creative_chat(chat_payload: ChatCreativePayload = Body(...)) -> ImagesResponse:
    try:
        return LlmCreativeImageCreator(
                credentials=chat_payload.credentials
            ).creative_chat( 
                chat_history=chat_payload.chat_history,
                question=chat_payload.question
            )

    except ImageCreatorNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
    except ImageCreatorPolicyError as err:
        raise HTTPException(status_code=400, detail=str(err))
