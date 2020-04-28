
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
  
