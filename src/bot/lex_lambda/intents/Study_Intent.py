import json
import boto3
from utils import elicit_slot, sendMessage, send2Messages
from bedrock_handler import generate_response


def Study_Intent(event):
    try:
        slots = event.get("sessionState", {}).get("intent", {}).get("slots", {})
        # Etapa 1: Geração da questão e resposta correta
        if slots.get("Faixa") == None:
            return elicit_slot(
                event, "Faixa", "Por favor, informe a cor da faixa."
            )

        Faixa = slots["Faixa"]["value"]["interpretedValue"]
        prompt_question = f"Me conte sobre quais conteúdos devem ser aprendidos para o exame de faixa do judô para a cor de faixa {Faixa}.. Gere essa resposta em forma de lista separada por área de conhecimento, Faça uma resposta curta de no maximo 2 linhas"

        try:
            respostaGerada = generate_response(prompt_question)
            
            # Retornar a questão gerada para o usuário e a resposta correta logo em seguida
            return sendMessage(
                "Study_Intent", "Fulfilled", respostaGerada
            )

        except Exception as erro:
            return sendMessage(
                "Study_Intent",
                "Failed",
                erro
            )

    except Exception as erro:
        return sendMessage(
            "Study_Intent",
            "Failed",
            erro
        )