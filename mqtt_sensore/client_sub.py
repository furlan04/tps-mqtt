import paho.mqtt.client as client
import json
import sys

TOPIC = "tps/dati_sensore"

BROKER = sys.argv[1:][0]

def on_connect(subscriber, userdata, flags, rc):
    print(f"Connesso con return code {str(rc)}")
    subscriber.subscribe(TOPIC)

def on_message(subscriber, userdata, msg):
    dato = msg.payload.decode()
    val = json.load(dato)["valore-sensore"]
    print(f"{msg.topic}: {val}")

subscriber = client.Client()
subscriber.on_connect = on_connect
subscriber.on_message = on_message

subscriber.connect(BROKER, 1883)

subscriber.loop_forever()
