'''
  basicUDP.py - This is basic UDP example.
  Created by Yasin Kaya (selengalp), January 2, 2019.
'''
from gprsiot import gprsiot
import time

your_ip = "78.183.237.146" # change with your ip
your_port = "4000" # change with your port

node = gprsiot.GPRSIoT()
node.disable()
time.sleep(2)

node.enable()
time.sleep(2)
node.powerUp()

node.sendATComm("ATE1","OK\r\n")

node.setIPAddress(your_ip)
time.sleep(0.5)
node.setPort(your_port)
time.sleep(0.5)

node.connectToOperator()
time.sleep(0.5)
node.getSignalQuality()
time.sleep(0.5)

node.deactivateContext()
time.sleep(0.5)
node.activateContext()
time.sleep(0.5)

node.closeConnection()
time.sleep(0.5)
time.sleep(0.5)
node.startUDPService()
time.sleep(0.5)

node.sendDataUDP("Hello World!\r\n")
time.sleep(0.5)

counter = 0

# send GPS message to server 
while(True):
  gps_message = node.readNMEA()
  msg = gps_message.decode(encoding="utf-8", errors='ignore')
  print("Recieved Message: " + str(msg))
  
  if(len(msg) > 200):
    msg = "long message"
  node.sendDataUDP(msg)
  msg = ""
  time.sleep(1)
    
