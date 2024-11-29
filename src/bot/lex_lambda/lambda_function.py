import json
from intents.ExitBot_Intent import ExitBot_Intent
from intents.FallbackIntent import FallbackIntent
from intents.History_Intent import History_Intent
from intents.Philosophy_Intent import Philosophy_Intent
from intents.Quests_Intent import Quests_Intent
from intents.Study_Intent import Study_Intent


def lambda_handler(event, context):
    
    # Identificar a intent em progresso
    intent_name = event.get('sessionState', {}).get('intent', {}).get('name')
    last_intent = 'Menu_Intent'
    
    print('event:', event)
    # Processar a intent conforme o nome
    print('Intent atual é:', intent_name)
    print('Last Intent:', last_intent)
    
    
    if intent_name == 'History_Intent':
        last_intent = 'History_Intent'
        return History_Intent(event)
        
    elif intent_name == 'Philosophy_Intent':
        last_intent = 'Philosophy_Intent'
        return Philosophy_Intent(event)
        
    elif intent_name == 'Quests_Intent':
        last_intent = 'Quests_Intent'
        return Quests_Intent(event)
            
    elif intent_name == 'Study_Intent':
        last_intent = 'Study_Intent'
        return Study_Intent(event)
        
    elif intent_name == 'ExitBot_Intent':
        return ExitBot_Intent(event)
        
    else:
        return FallbackIntent(event, last_intent)
