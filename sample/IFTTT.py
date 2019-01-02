'''
  IFTTT.py - This is send data to IFTTT via http post method.
  Created by Metin KOC (saucompeng), September 11, 2018.
'''
from gprsiot import gprsiot
import time

event_name = "" # change with your eventName
api_key = ""; # change with api-key

data = "{\"value1\":\"%d\"}"

node = gprsiot.gprsiot()
node.disable()
node.enable()
node.powerUp()

node.sendATComm("ATE1","OK\r\n")

node.getIMEI()
time.sleep(0.5)
node.getFirmwareInfo()
time.sleep(0.5)
node.getHardwareInfo()
time.sleep(0.5)

node.setGSMBand(node.GSM_900)
time.sleep(0.5)
node.setMode(node.GSM_MODE)
time.sleep(0.5)

node.connectToOperator()
time.sleep(0.5)
node.getSignalQuality()
time.sleep(0.5)
node.getQueryNetworkInfo()
time.sleep(0.5)

node.deactivateContext()
time.sleep(0.5)
node.activateContext()
time.sleep(0.5)

node.sendDataIFTTT(event_name, api_key, data % node.readTemp())

