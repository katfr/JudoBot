import json
import boto3
from utils import sendMessage, send2Messages
from bedrock_handler import generate_response

prompt_question = (
    f'Me conte sobre a filosofia do Judô. Faça uma resposta curta de no maximo 1 linha'
    )

def Philosophy_Intent(event):

    # Configura o pedido para o Bedrock, incluindo o conteúdo do arquivo como JSON
    try:
        respostaGerada = generate_response(prompt_question)

        # Retornar a questão gerada para o usuário e a resposta correta logo em seguida
        return sendMessage(
            "Philosophy_Intent",
            "Fulfilled",
            f"{respostaGerada}",
        )

    except Exception as erro:
        return send2Messages(
            "Philosophy_Intent",
            "Failed",
            "Erro inesperado: ",
            erro
        )
