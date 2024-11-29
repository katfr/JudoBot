import json
from services.image.image_handler import return_image_description
from services.lex.lex_call import process_user_message, send_message_to_telegram
from services.telegram.save_image import save_image_s3

def integration_telegram(event, context):    
    try:
        # Pegando o corpo da requisição(body)        
        body = json.loads(event['body'])
        # print("body do telegram", body)        
        
        # Verifica se a mensagem contém uma imagem (photo)
        if 'message' in body and 'photo' in body['message']:
            chat_id = body['message']['chat']['id']
            file_id = body['message']['photo'][-1]['file_id']  # Pega a imagem de maior resolução

            # Salva a imagem em um bucket no s3 com um nome criado a partir do seu id
            file_name = save_image_s3(file_id)

            # Retorna informações sobre a imagem
            response = return_image_description(file_name)

            # Responder o usuário 
            payload = {
                'chat_id': chat_id,
                'text': response
            }            
            send_message_to_telegram(payload)

            # Envia mensagem para o lex indicando encerramento da intent 
            message_part = "CHAMAR ENCERRAMENTO"
            process_user_message(message_part, chat_id)

            # Retornar resposta de sucesso
            return {'statusCode': 200, 'body': json.dumps({'status': 'received'})}        

        # Verifica se a mensagem contém um callback_query
        if 'callback_query' in body:
            callback_query = body['callback_query']
            callback_data = callback_query['data']
            chat_id = callback_query['message']['chat']['id']

            # Enviar o valor do callback_data como uma mensagem no chat
            payload = {
                'chat_id': chat_id,
                'text': callback_data  # Enviar o valor do callback_data como mensagem
            }
            send_message_to_telegram(payload)
            
            # Reprocessar a mensagem simulada como se fosse uma nova mensagem de texto
            process_user_message(callback_data, chat_id)

            # Retornar resposta de sucesso
            return {'statusCode': 200, 'body': json.dumps({'status': 'received'})}   

        # Verifica se a mensagem contém texto
        if 'message' in body and 'text' in body['message']:
            chat_id = body['message']['chat']['id']

            # Envia a mensagem para o lex, processa a resposta dada pelo lex (texto ou card) e retorna a resposta ao telegram
            process_user_message(body['message']['text'], chat_id)
            
            # Retornar resposta de sucesso
            return {'statusCode': 200, 'body': json.dumps({'status': 'received'})}   

        else:            
            chat_id = body['message']['chat']['id']

            # Responder o usuário que o formato da mensagem não é válido
            payload = {
                'chat_id': chat_id,
                'text': "Formato de mensagem inválido"
            }            
            send_message_to_telegram(payload)

            # Retornar resposta de sucesso
            return {'statusCode': 200, 'body': json.dumps({'status': 'received'})}              

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }