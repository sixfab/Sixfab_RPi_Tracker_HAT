'''
  basicUDP.py - This is basic UDP example.
  Created by Yasin Kaya (selengalp), January 2, 2019.
'''
from gprsiot import gprsiot
import time

node = gprsiot.GPRSIoT()

#node.Sendline()
node.readNMEA()
time.sleep(2)

while True:
  message = node.readNMEA()
  msg = message.decode(encoding="utf-8", errors='ignore')
  #print(msg)
  msg = ""
  time.sleep(2)
  
