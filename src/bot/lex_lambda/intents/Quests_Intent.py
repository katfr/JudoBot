import json
import boto3
import logging
from utils import elicit_slot, sendMessage, send2Messages
from bedrock_handler import generate_response

# Configuração do logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def Quests_Intent(event):
    try:
        slots = event.get('sessionState', {}).get('intent', {}).get('slots', {})

        # Etapa 1: Geração da questão e resposta correta
        if not slots.get('Faixa'):
            return elicit_slot(event, 'Faixa', 'Por favor, informe a cor da faixa.')
            
        faixa_cor = slots['Faixa']['value']['interpretedValue']

        # Mapeia a cor da faixa para o arquivo correspondente no S3
        file_mapping = {
            'Cinza': 'faixa_cinza_prova.txt',
            'Azul': 'faixa_azul_prova.txt',
            'Amarela': 'faixa_amarela_prova.txt',
            'Laranja': 'faixa_laranja_prova.txt',
            'Verde': 'faixa_verde_prova.txt',
            'Roxa': 'faixa_roxa_prova.txt',
            'Marrom': 'faixa_marrom_prova.txt',
        }
            
        file_key = file_mapping.get(faixa_cor)
        if not file_key:
            logger.error(f"Não foi possível encontrar uma prova para a cor {faixa_cor}.")
            return sendMessage('Quests_Intent', 'Failed', f"Não foi possível encontrar uma prova para a cor {faixa_cor}.",)
            
        # Carrega o arquivo do S3
        s3 = boto3.client('s3')
        bucket_name = 'leonardoloureiro-myphotos'
        try:
            logger.info(f"Tentando carregar o arquivo {file_key} do bucket {bucket_name}")
            file_obj = s3.get_object(Bucket=bucket_name, Key=file_key)
            file_content = file_obj['Body'].read().decode('utf-8')
            
        except Exception as e:
            logger.error(f"Erro ao carregar arquivo do S3: {e}")
            return sendMessage(
                'Quests_Intent', 
                'Failed', 
                'Erro ao carregar arquivo de prova. Tente novamente mais tarde.'
                )
            
        # Configura o pedido para o Bedrock, incluindo o conteúdo do arquivo como JSON
        prompt_question = (
            f"Crie uma pergunta objetiva em português adequada para a faixa {faixa_cor}, "
            f"baseada no seguinte conteúdo: {file_content}. "
            "A pergunta deve ser clara, direta e refletir um conhecimento apropriado para essa faixa."
        )

        try:
            generated_prova = generate_response(prompt_question)
            
            # Configura o pedido para gerar a resposta correta com base na questão gerada
            prompt_answer = (
                f"Com base na seguinte questão de judô para a faixa {faixa_cor}, forneça a resposta correta:\n\n"
                f"**Questão**: {generated_prova}\n"
                f"**Conteúdo de Referência**:\n{file_content}\n"
            )

            resposta_correta = generate_response(prompt_answer)

            # Retornar a questão gerada para o usuário e a resposta correta logo em seguida
            return send2Messages(
                "Quests_Intent",
                "Fulfilled",
                generated_prova,
                f"Resposta: {resposta_correta}"
            )

        except Exception as e:
            logger.error(f"Erro ao gerar questão ou resposta no Bedrock: {e}")
            return sendMessage(
                "Quests_Intent",
                "Failed",
                "Erro ao gerar a questão ou resposta. Tente novamente mais tarde.",
            )

    except Exception as erro:
        logger.error(f"Erro inesperado: {erro}")
        return sendMessage(
            "Quests_Intent", 
            "Failed", 
            'Erro inesperado. Tente novamente mais tarde.')
