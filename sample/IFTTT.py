''' 
  IFTTT.py - This is send data to IFTTT via http post method.
  Created by Metin KOC (saucompeng), September 11, 2018.
  Modified by Saeed Johar (saeedjohar), October 3, 2019.
'''
from tracker import tracker
import time

event_name = "" # change with your eventName
api_key = "" # change with api-key

data = "{\"value1\":\"%d\"}"

node = tracker.Tracker()
node.disable()
node.enable()
node.powerUp()
sleep(1)

node.getSignalQuality()
time.sleep(0.5)

node.deactivateContext()
time.sleep(0.5)
node.activateContext()
time.sleep(0.5)

mydata = 50 # arbitrary value, could be replaced with any sensor data
node.sendDataIFTTT(event_name, api_key, data % mydata )

