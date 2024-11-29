import requests
import boto3
import os

from .telegram_files import get_telegram_file_info

s3_client = boto3.client('s3')

def save_image_s3(file_id):
        # Obter a URL do arquivo a partir do file_id
        file_info = get_telegram_file_info(file_id)
        file_url = "https://api.telegram.org/file/bot{}/{}".format(os.environ['TELEGRAM_TOKEN'], file_info['file_path'])

        # Fazer download da imagem
        file_content = requests.get(file_url).content

        # Definir o nome do arquivo e o bucket S3
        file_name = f"telegram_images/{file_id}.jpg"
        bucket_name = os.environ['S3_BUCKET_NAME']

        # Fazer o upload da imagem para o S3
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)

        return file_name