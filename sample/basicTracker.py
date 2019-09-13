'''
  basicTraker.py - This is basic Tracker example.
  Created by Yasin Kaya (selengalp), January 2, 2019.
'''
from gprsiot import gprsiot
from time import sleep

your_ip = "xx.xx.xx.xx" # change with your ip
your_port = "xxxx" # change with your port

node = gprsiot.GPRSIoT()
node.disable()
sleep(2)

node.enable()
sleep(2)
node.powerUp()

#node.sendATComm("ATE1","OK\r\n")

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
sleep(1)

node.startUDPService()
sleep(0.5)

node.sendDataUDP("Starting sending message!\r\n")
sleep(0.5)

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
  sleep(1)
    
