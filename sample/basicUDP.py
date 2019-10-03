'''
  basicUDP.py - This is basic UDP example.
  Created by Yasin Kaya (selengalp), January 2, 2019.
  Modified by Saeed Johar (saeedjohar), October 3, 2019.
'''
from tracker import tracker
from time import sleep

your_ip = "xx.xx.xx.xx" # change with your ip
your_port = "xxxx" # change with your port

node = tracker.Tracker()
node.disable()
sleep(5)
node.enable()
sleep(2)
node.powerUp()

node.sendATComm("ATE1","OK\r\n")

node.setIPAddress(your_ip)
sleep(0.5)
node.setPort(your_port)
sleep(0.5)

node.connectToOperator()
sleep(0.5)
node.getSignalQuality()
sleep(0.5)

node.deactivateContext()
sleep(0.5)
node.activateContext()
sleep(0.5)

node.closeConnection()
sleep(0.5)
node.startUDPService()
sleep(0.5)

node.sendDataUDP("Hello World!\r\n")
sleep(0.5)
