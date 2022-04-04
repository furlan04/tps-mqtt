import paho.mqtt.publish as publish
import struct
from nrf24 import *
import sys
import pigpio

TOPIC = "tps/dati_sensore"
BROKER = sys.argv[1:][0]

ID = "BL"
ADDR = "RAS1"
TYPE = "SL"

PIGPIONAME='localhost'
PIGPIOPORT=8888
READINGPIPE='00001'


pi = pigpio.pi(PIGPIONAME, PIGPIOPORT)
if not pi.connected:
    print("Pigpiod non connesso. Lanciare: SUDO PIGPIOD")
    sys.exit()
 
nrf = NRF24(pi, ce=17, payload_size=32, channel=76, data_rate=RF24_DATA_RATE.RATE_1MBPS, pa_level=RF24_PA.LOW)

nrf.set_address_bytes(5)
nrf.open_reading_pipe(RF24_RX_ADDR.P1, READINGPIPE)


while True:
    if nrf.data_ready():
        (id, mittente, destinatario, type, valore, vuoto)= (struct.unpack("2s 4s 4s 2s 4s 16s", nrf.get_payload()))
        if id.decode() == ID and type.decode() == TYPE and destinatario.decode() == ADDR:
            publish.single(TOPIC, str({"valore-sensore": valore.decode()}), hostname=BROKER)