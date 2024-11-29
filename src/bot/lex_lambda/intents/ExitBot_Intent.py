import json
import boto3
import logging
import requests
import random
from utils import send2Messages

# Vetor com as frases
frases_judo = [
    "Nunca te orgulhes de haver vencido a um adversário, ao que venceste hoje poderá derrotar-te amanhã. A única vitória que perdura é a que se conquista sobre a própria ignorância.",
    "Somente se aproxima da perfeição quem a procura com constância, sabedoria e, sobretudo humildade.",
    "Quem teme perder já está vencido.",
    "O judoca não se aperfeiçoa para lutar, luta para se aperfeiçoar.",
    "Conhecer-se é dominar-se, dominar-se é triunfar.",
    "Praticar judô é educar a mente a pensar com velocidade e exatidão, bem como o corpo obedecer com justeza. O corpo é uma arma cuja eficiência depende da precisão com que se usa a inteligência.",
    "Judô não é uma luta é uma arte.",
    "Saber cada dia um pouco mais e usá-lo todos os dias para o bem, esse é o caminho dos verdadeiros judocas.",
    "O judoca é o que possui inteligência para compreender aquilo que lhe ensinam, paciência para ensinar o que aprendeu aos seus semelhantes e fé para acreditar naquilo que não compreende.",
    "Pior do que não ter o que fazer é não fazer nada para ter"
]

def ExitBot_Intent(event):
    session_id = event['sessionId']
    print(f"Session ID: {session_id}")

    if not session_id:
        raise ValueError("O session_id está vazio ou ausente.")
    try:
        # Pegando uma frase aleatória
        frase_aleatoria = random.choice(frases_judo)
        
        # Configurar a carga útil para a função Lambda integrador Polly
        body = {
            'phrase': frase_aleatoria
        }
        
        # inicializa o cliente lambda
        client = boto3.client('lambda')
        
        # Invocar a função Lambda que retorna a resposta da api com URL do audio
        res = client.invoke(
            FunctionName='bot-judo-dev-polly',
            InvocationType='RequestResponse',
            Payload=json.dumps({'body': json.dumps(body)})
        )
        
        api_res = json.loads(res['Payload'].read())
        print(f"API Response: {api_res}")
    
        # Analisar o corpo da resposta e pegar a url do audio no s3
        body_res = json.loads(api_res['body'])
        audio_url = body_res.get("url_to_audio")
        print(f"API Response2: {audio_url}")
        
        
        # Baixar o áudio da URL no S3
        audio_response = requests.get(audio_url)
        print(f"API Responsex: {audio_response}")
        audio_data = audio_response.content
        print(f"API Responsexx: {audio_data}")
        
        # Payload para enviar o áudio
        payload = {
            'chat_id': session_id
        }
        print(f"API Response3: {payload}")
        
        files = {
        'audio': ('Audio Motivacional.mp3', audio_data, 'audio/mpeg')
        }
    

        send_audio_to_telegram(payload, files)
        
    except Exception as erro:
        #logger.error(f"Erro inesperado: {erro}")
        print(f"Erro inesperado: {erro}")
    
    return send2Messages('ExitBot_Intent', 
                        'Fulfilled', 
                        'Obrigado por usar o Judobot! Até a próxima!',
                        f'{frase_aleatoria}' + ' - Jigoro Kano',
                        )

def send_audio_to_telegram(payload,files):
    #telegram_token = os.environ['TELEGRAM_TOKEN']
    
    telegram_token = "7391591189:AAEJrdiVWV63JjCkJzpA38yeP78KlF2N4o0"    # MUDAR AQUI DEPOIS
    url = 'https://api.telegram.org/bot{}/sendAudio'.format(telegram_token) 
    
    r = requests.post(url, data=payload, files=files)
    print(f"API Response4: {url}")
    if r.status_code != 200:
        raise Exception(f"Erro ao enviar áudio ao Telegram: {r.text}")