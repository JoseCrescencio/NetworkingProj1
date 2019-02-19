from socket import *
import time

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET,SOCK_DGRAM)
clientSocket.settimeout(1)
maxi = 0.0
mini = 0.0


for i in range(2):
 message = raw_input('Input lowercase sentence:')
 start = time.time()
 clientSocket.sendto(message.encode(),(serverName, serverPort))
 try:
  modifiedMessage, serverAddress = clientSocket.recvfrom(2048) 
  print modifiedMessage.decode()
  end = time.time()
  RTT = end - start
  print "Roundtrip time: ", RTT
  
  if maxi < RTT:
   maxi = RTT
  if mini > RTT:
   mini = RTT

 except timeout:
  print "Request timed out"
  end = 1
clientSocket.close()

print mini
print maxi
