import os
from botocore.exceptions import ClientError

from .bedrock_call import generate_response
from .rekognition_call import recognize_celebrity

s3_bucket = os.environ['S3_BUCKET_NAME']

def return_image_description(file_name):
    try:
        s3_key = file_name

        nome_celebridade = recognize_celebrity(s3_bucket, s3_key)

        if nome_celebridade is None:
            respostaGerada = "Não foi possivel reconhecer esta pessoa, ela não tem relações históricas com o Judô, ou é uma celebridade ainda muito recente"
            return respostaGerada
        else:
            prompt_foto = (
                f"Me conte brevemente sobre a trajetória e carreira no Judô de {nome_celebridade}, "
                f"Faça uma resposta curta, em português do brasil, de no máximo 1 linha. Se essa pessoa não tiver relação com o esporte do Judô, "
                f"me retorne apenas: 'Esta pessoa não tem relações históricas com o Judô, ou é uma celebridade ainda muito recente, "
                f"tente outro.'"
            )
            respostaGerada = generate_response(prompt_foto)
            return respostaGerada

    except Exception as erro:
        raise erro