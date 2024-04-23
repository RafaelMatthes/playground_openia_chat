from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import StreamingResponse

from llm.llm_chat import Llm_chat
# from models.chat_payload import ChatPayload


chat = APIRouter()


from pydantic import BaseModel, Field
from typing import List


class MessageHistory(BaseModel):
    role: str
    content: str


class ChatPayload(BaseModel):
    chat_history: List[MessageHistory]
    question: str = Field(..., description="The question field is required")
    stream: bool = True


@chat.post('/history', status_code=200)
async def chat_whit_history(chat_payload: ChatPayload = Body(...)):

    try:
        if chat_payload.stream:
            async def stream_response(payload):
                async for chunk in Llm_chat().chat_stream(
                    history=payload.chat_history,
                    question=payload.question
                ):
                    yield chunk

            return StreamingResponse(
                    content=stream_response(chat_payload),
                    media_type="text/event-stream",
                    headers={
                        "Cache-Control": "no-cache",
                        "Connection": "keep-alive"
                    }
                )

        return Llm_chat().chat_invoke(
                history=chat_payload.chat_history,
                question=chat_payload.question
            )
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) 
