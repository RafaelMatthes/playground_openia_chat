from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import StreamingResponse

from llm.llm_chat import LlmChat
from models.chat_payload import ChatPayload


chat = APIRouter()


@chat.post('/history', status_code=200)
async def chat_whit_history(chat_payload: ChatPayload = Body(...)):

    try:
        if chat_payload.stream:
            async def stream_response(payload):
                async for chunk in LlmChat(credentials=chat_payload.credentials).chat_stream(
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

        return LlmChat(credentials=chat_payload.credentials).chat_invoke(
                history=chat_payload.chat_history,
                question=chat_payload.question
            )
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) 
