import json
from utils import sendMessage

def FallbackIntent(event, last_intent):

    return sendMessage(
        last_intent,
        'Fulfilled', 
        'Parece que não entendi o que você disse. Pode repetir?', 
        type= "Delegate")