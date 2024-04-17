from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import StreamingResponse

from llm.azure import Llm_chat
from models.chat_payload import ChatPayload


chat = APIRouter()


@chat.post('/history', status_code=200)
async def chat_whit_history(document_search: ChatPayload = Body(...)):

    async def stream_response():
        async for chunk in Llm_chat().chat_llm_with_history(
            history=document_search.chat_history,
            question=document_search.question
        ):
            yield chunk

    return StreamingResponse(
            content=stream_response(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive"
            }
        )