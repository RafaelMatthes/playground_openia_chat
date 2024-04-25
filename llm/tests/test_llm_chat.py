from unittest.mock import patch
from fastapi.testclient import TestClient
from llm.llm_chat import LlmChat
from models.chat_history import MessageHistory
from models.llm_credentials import LlmCredentials
from routes.chat_route import chat
from dataclasses import dataclass


@dataclass
class MockIAMessage:
    content: str


MOCK_CREDENTIALS = LlmCredentials(**{
        "endpoint": "https://teste.openai.azure.com/",
        "api_key": "7afbae282a"
    })


@patch('langchain_openai.AzureChatOpenAI.invoke')
def test_chat_whit_history_stream_off(mock_invoke):
    client = TestClient(chat)

    mock_invoke.return_value = MockIAMessage(content="teste")
    payload = {
        "chat_history": [
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
        "credentials": {
            "endpoint": "https://teste.openai.azure.com/",
            "api_key": "7afbae282a"
        },
        "stream": False
    }
    response = client.post('/history', json=payload)
    assert response.status_code == 200
    assert response.json()


@patch('langchain_openai.AzureChatOpenAI.stream')
def test_chat_whit_history_stream(mock_stream):
    client = TestClient(chat)

    mock_stream.return_value = [
            MockIAMessage(content="t"),
            MockIAMessage(content="e"),
            MockIAMessage(content="s"),
            MockIAMessage(content="t"),
            MockIAMessage(content="e"),
        ]
    payload = {
        "chat_history": [
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
        "credentials": {
            "endpoint": "https://teste.openai.azure.com/",
            "api_key": "7afbae282a"
        },
        "stream": True
    }

    response = client.post('/history', json=payload)
    assert response.status_code == 200


def test_llm_cha_invoke():
    with patch('langchain_openai.AzureChatOpenAI.invoke') as mock_azure_chat:
        mock_azure_chat.return_value = "Mocked response"

        llm_chat = LlmChat(credentials=MOCK_CREDENTIALS)

        history = [
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


def test_LlmChat_stream():
    with patch('langchain_openai.AzureChatOpenAI.stream') as mock_azure_chat:
        mock_azure_chat.return_value = "Mocked response"

        llm_chat = LlmChat(credentials=MOCK_CREDENTIALS)

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
        "credentials": {
            "endpoint": "https://teste.openai.azure.com/",
            "api_key": "7afbae282a"
        },
        "stream": False
    }
    response = client.post('/history', json=payload)
    assert response.status_code == 200
    assert response.json() 
