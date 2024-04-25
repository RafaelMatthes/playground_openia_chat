from fastapi import APIRouter, Body, HTTPException
from models.chat_image_payload import ChatImagePayload
from openai.types import ImagesResponse

from llm.llm_image_creator import (
    LlmImagesCreator, 
    ImageCreatorNotFoundError, 
    ImageCreatorPolicyError
)

dall_e = APIRouter()


@dall_e.post('/create', status_code=200)
async def chat_whit_history(chat_payload: ChatImagePayload = Body(...)) -> ImagesResponse:
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
