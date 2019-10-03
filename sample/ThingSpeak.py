 '''
  ThingSpeak.py - This is send data to ThingSpeak via http post method.
  Created by Metin KOC (saucompeng), September 11, 2018.
  Modified by Saeed Johar (saeedjohar), October 3, 2019.
'''
from tracker import tracker
from time import sleep

api_key = "XXXXXXXXXXXXX"; # change with api-key

data = "field1=%d"

node = gprsiot.GPRSIoT()
node.disable()
node.enable()
node.powerUp()

node.sendATComm("ATE1","OK\r\n")


node.getSignalQuality()
sleep(0.5)

node.deactivateContext()
sleep(0.5)
node.activateContext()
sleep(0.5)

mydata = 50 # arbitrary value, could be replaced with any sensor data
node.sendDataThingspeak(api_key, data % mydata)


