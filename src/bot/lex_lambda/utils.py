from datetime import datetime
import boto3

def datetime_converter(o):
    if isinstance(o, datetime):
        return o.isoformat()

def elicit_slot(event, slot_to_elicit, message, session_attributes=None):
    intent_name = event['sessionState']['intent']['name']
    slots = event.get('sessionState', {}).get('intent', {}).get('slots', {})
    
    return {
        'sessionState': {
            'dialogAction': {
                'type': 'ElicitSlot',
                'slotToElicit': slot_to_elicit,
            },
            'intent': {
                'name': intent_name,
                'slots': slots
            },
            'sessionAttributes': session_attributes or {}
        },
        'messages': [
            {
                'contentType': 'PlainText',
                'content': message
            }
        ]
    }

def sendMessage(intent_name, fulfillment_state, message, session_attributes=None, type='Close'):
    return {
        'sessionState': {
            'dialogAction': {
                'type': type,
                'fulfillmentState': fulfillment_state,
            },
            'intent': {
                'name': intent_name,
                'state': fulfillment_state
            },
            'sessionAttributes': session_attributes or {}
        },
        'messages': [
            {
                'contentType': 'PlainText',
                'content': message
            }
        ]
    }
    
def send2Messages(intent_name, fulfillment_state, message1, message2, session_attributes=None, type='Close'):
    return {
        'sessionState': {
            'dialogAction': {
                'type': type,
                'fulfillmentState': fulfillment_state,
            },
            'intent': {
                'name': intent_name,
                'state': fulfillment_state
            },
            'sessionAttributes': session_attributes or {}
        },
        'messages': [
            {
                'contentType': 'PlainText',
                'content': message1
            },
            {
                'contentType': 'PlainText',
                'content': message2
            }
        ]
    }
    
def send3Messages(intent_name, fulfillment_state, message1, message2, message3, session_attributes=None, type='Close'):
    return {
        'sessionState': {
            'dialogAction': {
                'type': type,
                'fulfillmentState': fulfillment_state,
            },
            'intent': {
                'name': intent_name,
                'state': fulfillment_state
            },
            'sessionAttributes': session_attributes or {}
        },
        'messages': [
            {
                'contentType': 'PlainText',
                'content': message1
            },
            {
                'contentType': 'PlainText',
                'content': message2
            },
            {
                'contentType': 'PlainText',
                'content': message3
            }
        ]
    }

def responseCard(intent_name, fulfillment_state, mensagem_inicial, title, subtitle, session_attributes=None, type='Close'):
    return {
        'sessionState': {
            'dialogAction': {
                'type': type,
                'fulfillmentState': fulfillment_state,
            },
            'intent': {
                'name': intent_name,
                'state': fulfillment_state
            },
            'sessionAttributes': session_attributes or {}
        },
        'messages': [
            {
                'contentType': 'PlainText',
                'content': mensagem_inicial
            },
            {
                "contentType": "ImageResponseCard",
                "imageResponseCard": {
                    "title": title,
                    "subtitle": subtitle,
                    "buttons": [
                        {
                            "text": "Desenvolver vocabulário",
                            "value": "Quero melhorar meu vocabulário"
                        },
                        {
                            "text": "Exercícios linguísticos",
                            "value": "Quero praticar com exercícios linguísticos"
                        },
                        {
                            "text": "Recomendações de materiais",
                            "value": "Busco por recomendações de materiais"
                        },
                        {
                            "text": "Aprendizado de culturas",
                            "value": "Desejo aprender mais sobre outras culturas!"
                        },
                    ]
                }
            }
        ]
    }
    
    import boto3

def detectar_celebridade(s3_bucket, s3_key):
    # Cria um cliente do Rekognition
    rekognition = boto3.client('rekognition')

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