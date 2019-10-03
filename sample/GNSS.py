'''
  basicUDP.py - This is basic UDP example.
  Created by Yasin Kaya (selengalp), January 2, 2019.
  Modified by Saeed Johar (saeedjohar), October 3, 2019.
'''
from tracker import tracker
from time import sleep

node = tracker.Tracker()

#node.Sendline()
node.readNMEA()
sleep(2)

while True:
  message = node.readNMEA()
  msg = message.decode(encoding="utf-8", errors='ignore')
  #print(msg)
  msg = ""
  sleep(2)
  
