import boto3, os
from contextlib import closing

def tts_polly(text_blocks, polly, phrase_hash):
        for textBlock in text_blocks:
            response = polly.synthesize_speech(
                OutputFormat='mp3',
                Text=textBlock,
                VoiceId='Camila',
                LanguageCode='pt-BR'
            )
            if "AudioStream" in response:
                with closing(response["AudioStream"]) as stream:
                    output = os.path.join("/tmp/", phrase_hash)
                    with open(output, "ab") as file:
                        file.write(stream.read())   
        
        s3 = boto3.client('s3')

        # Faz o uploado do audio gerado no s3
        s3.upload_file('/tmp/' + phrase_hash, os.environ['S3_BUCKET_NAME_AUDIO'], phrase_hash + ".mp3")
        # Define o inicio da url com base no nome do bucket
        url_begining = "https://" + str(os.environ['S3_BUCKET_NAME_AUDIO']) + ".s3.us-east-1.amazonaws.com/" \

        url = url_begining \
            + str(phrase_hash) \
            + ".mp3"
        
        return url