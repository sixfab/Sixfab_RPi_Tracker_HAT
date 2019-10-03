 '''
  ThingSpeak.py - This is send data to ThingSpeak via http post method.
  Created by Metin KOC (saucompeng), September 11, 2018.
  Modified by Saeed Johar (saeedjohar), October 3, 2019
'''
from gprsiot import gprsiot
import time

api_key = "XXXXXXXXXXXXX"; # change with api-key

data = "field1=%d"

node = gprsiot.GPRSIoT()
node.disable()
node.enable()
node.powerUp()

node.sendATComm("ATE1","OK\r\n")


node.getSignalQuality()
time.sleep(0.5)

node.deactivateContext()
time.sleep(0.5)
node.activateContext()
time.sleep(0.5)

node.sendDataThingspeak(api_key, data % node.readTemp())


