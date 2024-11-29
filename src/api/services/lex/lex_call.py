import json
import boto3
import os
from .return_message import send_message_to_telegram

# Configurar o cliente do Amazon Lex V2
lex_client = boto3.client('lexv2-runtime', region_name="us-east-1")

def process_user_message(message_part, chat_id):
    # Configurar os parâmetros da solicitação ao Lex V2
    params = {
        'botId': os.environ['LEX_BOT_ID'],          # ID do seu bot no Lex V2     
        'botAliasId': os.environ['LEX_BOT_ALIAS_ID'],   # ID do alias no Lex V2      
        'localeId': 'pt_BR',            # Substitua pelo locale apropriado, como 'pt_BR'
        'sessionId': str(chat_id),      # ID da sessão, geralmente usando o chat_id do Telegram
        'text': message_part,           # Texto da mensagem recebida
    }

    # Enviar a mensagem ao Amazon Lex V2 e obter a resposta
    response = lex_client.recognize_text(**params)
    # print(response)
    
    # Verificar se a chave 'messages' está presente na resposta
    if 'messages' in response:
        # Processar todas as mensagens retornadas pelo Lex
        for message in response['messages']:
            if message['contentType'] == 'PlainText':
                lex_response_message = message['content']

                # Prepara o payload com o texto
                payload = {
                    'chat_id': chat_id,
                    'text': lex_response_message                    
                }
                
                # Enviar a mensagem de volta ao Telegram
                send_message_to_telegram(payload)
            elif message['contentType'] == 'ImageResponseCard':
                card = message['imageResponseCard']
                title = card.get('title', '')
                buttons = card.get('buttons', [])

                # Criar os botões do Telegram
                keyboard = {
                    'inline_keyboard': [[{'text': button['text'], 'callback_data': button['value']}] for button in buttons]
                }

                # Prepara o payload com o card
                payload = {
                    'chat_id': chat_id,
                    'text': title,
                    'reply_markup': json.dumps(keyboard)
                }
                # Enviar a mensagem de volta ao Telegram
                send_message_to_telegram(payload)            
    else:
        print("Nenhuma mensagem retornada pelo Lex")