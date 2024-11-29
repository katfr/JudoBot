import json
import boto3

# Cria um cliente para o serviço 'bedrock-runtime' da AWS
bedrock_client = boto3.client('bedrock-runtime')

def generate_response(prompt):
    native_request = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 1024,
            "temperature": 0.6,
        },
    }

    request = json.dumps(native_request)

    try:
        bedrock_response = bedrock_client.invoke_model(
            modelId="amazon.titan-text-premier-v1:0",  # Verifique se o ID do modelo está correto
            contentType="application/json",
            accept="application/json",
            body=request
        )

        model_response = json.loads(bedrock_response["body"].read().decode('utf-8'))
        return model_response["results"][0]["outputText"]

    except Exception as e:
        raise e
