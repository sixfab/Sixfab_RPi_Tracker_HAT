'''
  basicUDP.py - This is basic UDP example.
  Created by Yasin Kaya (selengalp), January 2, 2019.
'''
from gprsiot import gprsiot
import time

node = gprsiot.GPRSIoT()

while True:
  node.readNMEA()
  time.sleep(0.5)
