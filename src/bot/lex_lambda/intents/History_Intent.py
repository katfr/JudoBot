import json
import boto3
from utils import sendMessage, detectar_celebridade
from bedrock_handler import generate_response

def History_Intent(event):
    
    # Extraindo o dicionário de slots
    slots = event.get('sessionState', {}).get('intent', {}).get('slots', {})
    user_input = event.get('inputTranscript', '').lower()
        
    # Extraindo o slot específico
    marco_historico = slots.get('MarcoHistorico', {})
        
    # Verificando se o slot 'MarcoHistorico' existe e se 'value' está presente
    if marco_historico is not None and isinstance(marco_historico, dict):
        interpreted_value = marco_historico.get('value', {}).get('interpretedValue', None)
    else:
            interpreted_value = None
        
    try:
        if interpreted_value == None:
            return sendMessage(
                'History_Intent',
                'InProgress',
                'placeholder', 
                type='Delegate')
        
        else:
            prompt_historia = (
                f"Me conte sobre {user_input}, em português do brasil.Faça uma resposta curta de no máximo 1 linha. Se esse assunto não tiver relação com o judô, retorne apenas 'Esse assunto não tem relação com a história do Judô, tente outro.'. Nunca retorne os erros ao gerar o prompt"
            )
            respostaGerada = generate_response(prompt_historia)
            return sendMessage(
                "Philosophy_Intent",
                "Fulfilled",
                f"{respostaGerada}"
            )

    except Exception as erro:
        # Certifique-se de converter o erro para string antes de retorná-lo
        return sendMessage(
            "Philosophy_Intent",
            "Failed",
            str(erro)
        )

