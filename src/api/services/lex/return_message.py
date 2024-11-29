import requests
import os

def send_message_to_telegram(payload):    
    telegram_token = os.environ['TELEGRAM_TOKEN']
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(telegram_token) 

    r = requests.post(url, json=payload)

    if r.status_code != 200:
        raise Exception(f"Erro ao enviar mensagem ao Telegram: {r.text}")