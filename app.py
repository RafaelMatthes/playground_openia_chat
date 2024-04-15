import os
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI

load_dotenv()


# async def teste(message):

#     model = AzureChatOpenAI(
#         openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#         azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
#         openai_api_version="2023-05-15",
#         azure_deployment="gpt-4-32k",
#         streaming=True,
#     )

#     for chunk in model([message]):
#         yield chunk


async def chamada_teste():

    message = HumanMessage(
            content="crie um texto de 100 caracteres sobre a importância da programação na vida das pessoas."
        )

    model = AzureChatOpenAI(
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        openai_api_version="2023-05-15",
        azure_deployment="gpt-4-32k",
        streaming=True
    )

    for chunk in model([message]).__dict__['content']:
        yield chunk
        await asyncio.sleep(.05)

# print(response.__dict__['content'])


# model = AzureChatOpenAI(
#     openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#     azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
#     openai_api_version="2023-05-15",
#     azure_deployment="gpt-4-32k"
# )

# message = HumanMessage(
#     content="Translate this sentence from English to PT-BR. I love programming."
# )

# print(model([message]))

app = FastAPI()


@app.post('/teste', status_code=200)
async def retrieval():

    async def stream_response():
        async for chunk in chamada_teste():
            yield chunk

    return StreamingResponse(
            content=stream_response(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive"
            }
        )


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI app using Uvicorn
    uvicorn.run(app, port=8080)