import os, json, hashlib, time, boto3
from datetime import datetime  
from services.audio.text_to_block import text_to_block
from services.audio.tts_polly import tts_polly

dynamodb = boto3.resource('dynamodb')

def polly_tts(event, context):
    body = json.loads(event['body'])
    phrase = body['phrase']    

    # Gera o hash único para a frase recebida
    phrase_hash = hashlib.md5(phrase.encode()).hexdigest()
    phrase_hash 

    # Logica para verificar se a frase já existe no dynamodb
    table_name = os.environ['DYNAMODB_TABLE_NAME']
    table = dynamodb.Table(table_name)
    dynamo_res = table.get_item(Key={'unique_id': phrase_hash})

    if 'Item' not in dynamo_res:
        # implementar POLLY aqui
        polly = boto3.client('polly')
        
        rest = phrase
        text_blocks = text_to_block(rest)
        url = tts_polly(text_blocks, polly, phrase_hash)

        # Gera timestamp para o audio 
        timestamp = float(str(time.time()))
        formatted_timestamp = str(datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y %H:%M:%S"))

        item = {
            'received_phrase': phrase,
            'url_to_audio': url,
            'created_audio': formatted_timestamp,
            'unique_id': phrase_hash,
        }

        # Coloca o item no dynamob db
        table.put_item(Item=item)
        # Resgata os dados no novo item que foi colocado no dynamodb         
        dynamo_res = table.get_item(Key={'unique_id': phrase_hash})

    # Resposta da requisição, retorna dados armazenados no dynamodb
    response_body = {
        "received_phrase": dynamo_res['Item']['received_phrase'],
        "url_to_audio": dynamo_res['Item']['url_to_audio'],
        "created_audio": dynamo_res['Item']['created_audio'],
        "unique_id": dynamo_res['Item']['unique_id'] 
    }

    response = {"statusCode": 200, "body": json.dumps(response_body)}
    return response