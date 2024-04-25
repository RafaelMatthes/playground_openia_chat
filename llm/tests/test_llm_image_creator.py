import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from dataclasses import dataclass

@pytest.fixture
def mock_env_variables():
    with patch.dict(os.environ, {"AZURE_OPENAI_API_KEY": "test_api_key", "AZURE_OPENAI_AD_TOKEN": "test_ad_token"}):
        yield

@pytest.fixture
def client():
    from app import app
    return TestClient(app)


@dataclass
class MockIAMessage:
    content: str


@dataclass
class MockImagesResponse:
    created: int
    data: list
    content: str


@patch('llm.llm_image_creator.LlmImagesCreator.create_image')
def test_create_images_endpoint(mock_dall_e, client, mock_env_variables):

    mock_dall_e.return_value = MockImagesResponse(created=123, data=[], content="{'img': '123'}")

    response = client.post('image/chat/create', json={"question": "Test question", "credentials": {"endpoint": "test_endpoint", "api_key": "test_api_key"}})
    assert response.status_code == 200


@patch('llm.llm_image_creator.LlmImagesCreator.create_image')
@patch('langchain_openai.AzureChatOpenAI.invoke')
def test_creative_chat_endpoint(mock_dall_e, mock_invoke, client, mock_env_variables):

    mock_dall_e.return_value = MockImagesResponse(created=123, data=[], content="{'img': '123'}")
    mock_invoke.return_value = MockImagesResponse(created=123, data=[], content="{'img': '123'}")

    response = client.post(
        'image/chat/creative_chat',
        json={
            "question": "Test question",
            "credentials": {
                "endpoint": "test_endpoint",
                "api_key": "test_api_key"
            },
            "chat_history": [
                {"role": "user", "content": "Test message"}
            ]
        }
    )
    assert response.status_code == 200
