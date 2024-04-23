from unittest.mock import patch
from fastapi.testclient import TestClient
from llm.llm_chat import Llm_chat
from models.chat_history import MessageHistory
from routes.chat_route import chat


def test_chat_whit_history():
    client = TestClient(chat)

    payload = {
        "chat_history": [
            {
                "role": "system",
                "content": "You are an AI assistant that helps people find information and answer formatted in markdown."
            },
            {
                "role": "user",
                "content": "Olá meu nome é rafael"
            },
            {
                "role": "assistant",
                "content": "Olá Rafael, como posso te ajudar hoje?"
            }
        ],
        "question": "What's the question?",
        "stream": False
    }
    response = client.post('/history', json=payload)
    assert response.status_code == 200
    assert response.json()

    payload["stream"] = True
    response = client.post('/history', json=payload)
    assert response.status_code == 200


def test_llm_cha_invoke():
    with patch('langchain_openai.AzureChatOpenAI.invoke') as mock_azure_chat:
        mock_azure_chat.return_value = "Mocked response"

        llm_chat = Llm_chat()

        history = [
            MessageHistory(**{
                "role": "system",
                "content": "You are an AI assistant that helps people find information and answer formatted in markdown."
            }),
            MessageHistory(**{
                "role": "user",
                "content": "Olá meu nome é Rafael"
            }),
            MessageHistory(**{
                "role": "assistant",
                "content": "Olá Rafael, como posso te ajudar hoje?"
            })
        ]
        question = "What's the question?"
        response = llm_chat.chat_invoke(history, question)
        assert response == "Mocked response"


def test_llm_chat_stream():
    with patch('langchain_openai.AzureChatOpenAI.stream') as mock_azure_chat:
        mock_azure_chat.return_value = "Mocked response"

        llm_chat = Llm_chat()

        history = [
            MessageHistory(**{
                "role": "system",
                "content": "You are an AI assistant that helps people find information and answer formatted in markdown."
            }),
            MessageHistory(**{
                "role": "user",
                "content": "Olá meu nome é Rafael"
            }),
            MessageHistory(**{
                "role": "assistant",
                "content": "Olá Rafael, como posso te ajudar hoje?"
            })
        ]
        question = "What's the question?"
        stream_response = llm_chat.chat_stream(history, question)
        assert stream_response is not None 


@patch('langchain_openai.AzureChatOpenAI.invoke')
def test_chat_whit_history_200(mock_invoke):
    mock_invoke.return_value = "teste"
    client = TestClient(chat)
    payload = {
        "chat_history": [{"role": "system", "content": "System message"}],
        "question": "What's the question?",
        "stream": False
    }
    response = client.post('/history', json=payload)
    assert response.status_code == 200
    assert response.json() 
