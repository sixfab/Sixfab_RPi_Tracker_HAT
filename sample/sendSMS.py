'''
  sendSMS.py - This is basic SMS Service example.
  Created by Yasin Kaya (selengalp), January 2, 2019.
  Modified by Saeed Johar (saeedjohar), October 3, 2019. 
'''
from tracker import tracker
from time import sleep

node = tracker.Tracker()
node.disable()
sleep(0.5)
node.enable()
sleep(0.5)
node.powerUp()

node.sendATComm("ATE1","OK\r\n")

node.sendSMS("+xxxxxxxxxxx","hello world!") #replace +xxxx with phone number and hello world with your text message.
