import requests
import os

def get_telegram_file_info(file_id):
    telegram_token = os.environ['TELEGRAM_TOKEN']
    url = f'https://api.telegram.org/bot{telegram_token}/getFile?file_id={file_id}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()['result']
    else:
        raise Exception(f"Erro ao obter informações do arquivo: {response.text}")