import boto3
from botocore.exceptions import ClientError

# Cria um cliente do Rekognition
rekognition = boto3.client('rekognition', region_name='us-east-1')

def recognize_celebrity(s3_bucket, s3_key):
    try:
        # Chama o Rekognition para detectar celebridades
        response = rekognition.recognize_celebrities(
            Image={
                'S3Object': {
                    'Bucket': s3_bucket,
                    'Name': s3_key
                }
            }
        )

        # Verifica se alguma celebridade foi detectada
        if 'CelebrityFaces' in response and response['CelebrityFaces']:
            # Encontra a celebridade com a maior confiança
            top_celebrity = max(response['CelebrityFaces'], key=lambda x: x['MatchConfidence'])

            return top_celebrity['Name']
        else:
            return None
    except ClientError as e:
            print(f"Ocorreu um erro: {e}")
            return "Formato de imagem inválido. Por favor, envie uma imagem em um formato suportado (JPEG, PNG, etc.)."