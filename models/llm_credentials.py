from dataclasses import dataclass


@dataclass
class LlmCredentials:
    api_key: str
    endpoint: str
