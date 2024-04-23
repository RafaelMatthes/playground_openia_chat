from fastapi import FastAPI
from routes.chat_route import chat as chat_with_history

app = FastAPI()
app.include_router(chat_with_history, prefix="/chat", tags=["chat_with_history"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8080)