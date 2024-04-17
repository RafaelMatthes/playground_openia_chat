import os
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI

from routes.chat_route import chat as chat_with_history

# from fastapi.responses import StreamingResponse
# from langchain_core.messages import HumanMessage, AIMessage
# from langchain_openai import AzureChatOpenAI

# load_dotenv()

# from langchain.prompts import (
#         ChatPromptTemplate,
#         MessagesPlaceholder,
#         SystemMessagePromptTemplate,
#         HumanMessagePromptTemplate,
#     )
# from langchain.chains import LLMChain
# from langchain.memory import ConversationBufferMemory


# async def chamada_teste2():

#     llm = AzureChatOpenAI(
#         openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#         azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
#         openai_api_version="2023-05-15",
#         azure_deployment="gpt-4-32k",
#         streaming=True
#     )
#     prompt = ChatPromptTemplate(
#         messages=[
#             SystemMessagePromptTemplate.from_template(
#                 "You are a nice chatbot having a conversation with a human."
#             ),
#             HumanMessage(content='hi! My Name is Rafael', additional_kwargs={}),
#             AIMessage(content='whats up human?', additional_kwargs={}),
#             MessagesPlaceholder(variable_name="chat_history"),
#             HumanMessagePromptTemplate.from_template("{question}"),
#         ]
#     )
#     # Notice that we `return_messages=True` to fit into the MessagesPlaceholder
#     # Notice that `"chat_history"` aligns with the MessagesPlaceholder name.
#     memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
#     conversation_chain = LLMChain(
#         llm=llm,
#         prompt=prompt,
#         verbose=True,
#         memory=memory
#     )

#     print(conversation_chain({"question": "What is my name"}))

#     for chunk in conversation_chain({"question": "What is my name"})['text']:
#         yield chunk

app = FastAPI()

app.include_router(chat_with_history, prefix="/chat", tags=["chat_with_history"])


# @app.post('/teste', status_code=200)
# async def retrieval():

#     async def stream_response():
#         async for chunk in chamada_teste2():
#             yield chunk

#     return StreamingResponse(
#             content=stream_response(),
#             media_type="text/event-stream",
#             headers={
#                 "Cache-Control": "no-cache",
#                 "Connection": "keep-alive"
#             }
#         )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8080)