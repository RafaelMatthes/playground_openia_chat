from dataclasses import dataclass


@dataclass
class MessageHistory:
    """"
        chat_history [
            {"role": "system", "content": "Você é uma ferramenta de IA interessada em ajudar."},
            {"role": "user", "content": "olá, meu nome é fernando, use ele para se referir a mim."}
        ]
    """
    role: str
    content: str