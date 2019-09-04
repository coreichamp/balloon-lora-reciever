from network import LoRa
import socket
import time
from network import WLAN
# from mqtt import MQTTClient
import machine
import pycom

pycom.heartbeat(False)

lora = LoRa(mode=LoRa.LORA, frequency=863000000, bandwidth=LoRa.BW_125KHZ, tx_power=14, sf=12)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

wifiSSID = "Ake's iPhone"
wifiPassword = "qwertyuiopqq"

def settimeout(duration): 
    pass
print("*** Wifi Connecting to {} ***".format(wifiSSID))
wlan = WLAN(mode=WLAN.STA)
wlan.connect(wifiSSID, auth=(WLAN.WPA2, wifiPassword), timeout=10000)
time.sleep(5)

while not wlan.isconnected():
    print("*** Wifi Not Connected, wait 3 sec for reconnect. ***")
    time.sleep(3)
    wlan.connect(wifiSSID, auth=(WLAN.WPA2, wifiPassword), timeout=10000)
    time.sleep(5)

print("*** Wifi Connected to {} ***".format(wifiSSID))

print("*** MQTT Connecting ***")
client = MQTTClient("lora_balloon321654", "161.246.38.104", port=1883)
client.settimeout = settimeout
client.connect()
# try:
#     client.connect()
# except :    
#     print("error: {}".format(e))


print("*** MQTT Connected ***")
client.publish("lora_balloon", "Hello")

while True:
    data = s.recv(240)
    # print(data)
    if len(data) > 0:
        print("LoraRecieve: {}".format(data))
        client.publish("lora_balloon", data)
        pycom.rgbled(0xA0A0A0)
        time.sleep(0.1)
        pycom.rgbled(0x000000)
    
    time.sleep(1)
