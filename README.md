# Assistente de Chat com FastAPI

Este é um projeto de assistente de chat desenvolvido com FastAPI, utilizando uma integração com serviços da Azure para geração de respostas baseadas em modelos de linguagem.

## Funcionalidades

- **Chat em Tempo Real**: O endpoint `/chain_chat` permite conversas em tempo real com o assistente de chat.
- **Streaming de Respostas**: Suporte para streaming de respostas para manter a conexão aberta durante a conversa.
- **Integração com Azure**: Utilização dos serviços da Azure para geração de respostas utilizando modelos de linguagem.

## Instalação

1. Clone o repositório:

    ```
    git clone https://github.com/seu-usuario/seu-projeto.git
    ```

2. Instale as dependências:

    ```
    cd seu-projeto
    pip install -r requirements.txt
    ```

## Uso

1. Inicie o servidor:

    ```
    uvicorn main:app --reload
    ```

2. Faça uma requisição para o endpoint `/chain_chat` utilizando um cliente HTTP ou uma aplicação cliente.

## Testes

Execute os testes unitários com o seguinte comando:

```
pytest
```

## Swagger

```
/docs
```

## TO-DO:
- Add DockerFile and docker-compose
- Add Vectorial database endpoints (POST/DELETE)
- Add Retrieval Augmented Generation endpoint (RAG)
  

