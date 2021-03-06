# Name: UDPPingerClient.py
# Date: February 19, 2019
# Authors: Jose Crescencio, Judith Ramirez
# Description: This program acts like a client and pings the server.
# Average, maximum and minimum RTT are shown, as well as packet loss percentage.  

#imports
from socket import *
import time

#variables
ranOnce = False
mini = 0.0
maxi = 0.0
avgRTT = 0.0
missPercent = 0.0
estimatedRTT = 0.0

#setting server name, port number, socket and timeout of 1 second
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET,SOCK_DGRAM)
clientSocket.settimeout(1)

#loop for 10 packets to be sent 
for i in range(10):
 #setting the message for the packet
 message = raw_input('Input lowercase sentence:')
 
 #starting timer to determine RTT
 start = time.time()
 
 #packet is sent to server
 clientSocket.sendto(message.encode(),(serverName, serverPort))
 
 #try catch to catch a timed out request
 try:
  #receiving message and printing it
  modifiedMessage, serverAddress = clientSocket.recvfrom(2048) 
  print modifiedMessage.decode()
  
  #ending timer, finding RTT and printing the results
  end = time.time()
  RTT = (end - start)* 1000
  print "Roundtrip time: %.4f ms\n" % ( RTT )
  
  #calculating estimate RTT EstimatedRTT = (1- alpha*EstimatedRTT + alpha*SampleRTT
  estimatedRTT = ( 1 - 0.125 ) * estimatedRTT + ( 0.125 * RTT )
  
  #adding packet's RTT to overall sum to divide by n successful packets later
  avgRTT += RTT
  
  #setting min and max RTT to the first value for first packet sent
  if not ranOnce:
   maxi = RTT
   mini = RTT
   ranOnce = True
  
  #determining maximum and minimum RTT 
  if maxi < RTT:
   maxi = RTT
  if mini > RTT:
   mini = RTT
   
  #catch for timeout  
 except timeout:
  print "Request timed out\n"
  missPercent += 1
  
clientSocket.close()

#print statements for the RTT statements
print "\nEstimated RTT: %.4f ms" % (estimatedRTT)
print "\nMinimum RTT: %.4f ms" % ( mini )
print "Maximum RTT: %.4f ms" % ( maxi )
print "Average RTT: %.4f ms" % ( avgRTT / (10 - missPercent) )
print "Packet loss percentage: %d%%\n" % ( (missPercent / 10) * 100 )