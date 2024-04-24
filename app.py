from fastapi import FastAPI
from routes.chat_route import chat as chat_with_history
from routes.dalle_route import dall_e as  chat_image_creator

app = FastAPI()
app.include_router(chat_with_history, prefix="/chat", tags=["Chain Chat"])
app.include_router(chat_image_creator, prefix="/image/chat", tags=["Image Creator"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8080)