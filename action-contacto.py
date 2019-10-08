#!/usr/bin/env python3
from hermes_python.hermes import Hermes
import hermes_python 
from urls_ayto import urls_dict
import json

cache_file = "cache.json"   # sets the name of the cache file

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883 
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT)) 


# open the cache file and read the json
with open (cache_file, "r") as read_file:
    cache = json.load(read_file)

print(">>>", cache)
print("telefono: ", cache["telephone"])

def intent_received(hermes, intentMessage):

    snips_account = cache["snips-console"]
    if intentMessage.intent.intent_name == (snips_account + ':contacto'):
        if intentMessage.slots.fax:
            payload = cache["fax"]
            sentence = 'El número de faxs es el ' + payload
        elif intentMessage.slots.telefono:
            payload = cache["telephone"]
            sentence = 'El número de teléfono del ayuntamiento es el ' + payload
        elif intentMessage.slots.email:
            payload = cache["email"]
            sentence = 'El correo electrónico del ayuntamiento es el ' + payload
        elif intentMessage.slots.movil:
            payload = cache["telephone"]
            sentence = 'El ayuntamiento no tiene número móvil de momento, pero su teléfono fijo es el ' + payload
        else:
            sentence = "Vaya, de momento no tengo esa información."
    # nlu cannot recognise the code of below
    else:
        sentence = "Lo siento, no te he entendido."
    
    hermes.publish_end_session(intentMessage.session_id, sentence)
    
    
with Hermes(MQTT_ADDR) as h:
    h.subscribe_intents(intent_received).start()