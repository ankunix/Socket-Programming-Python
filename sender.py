#!/usr/bin/env python
#Import all modules from socket.
import socket
#Import all modules from sys.
import sys
import time
#Import router address and port.
from routerInfo import *
#Main function begins here.
def Main():
	startTime=time.time() #Statistics
	#Creating a sender socket object using socket() function.
	senderSocket = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) #Internet,UDP
	senderSocket.bind((HOST, SENDER_PORT))
	totalPackets=int(sys.argv[1])
	retransmissionCount=0 #Statistics
	#Loop for the count of data packets to be transmitted, totalPackets is a count provided as a command line argument.
	for seq in range(0,totalPackets):
		#Append data packets with sequence number
		outData= "pkt" + str(seq)
		#Print the outgoing data to router
		print "send " + outData
		#Send data to router
		senderSocket.sendto(outData,(HOST,ROUTER_PORT))

	while True:
		inData, addr = senderSocket.recvfrom(BUFFER_SIZE)
		print inData
		if (inData[:3]=="NAK"):
			seq=inData[3:]
			#Append data packets with sequence number
			outData= "pkt" + str(seq)
			retransmissionCount+=1
			#Print the outgoing data to router
			print "send " + outData
			senderSocket.sendto(outData,(HOST,ROUTER_PORT))
		elif (inData=="END"):
			break
	#Close Sender Socket
	senderSocket.close()
	endTime=time.time()
	#Statistics
	print("Total packets transmitted: " + str(totalPackets))
	print("Retransmissions Occured: " + str(retransmissionCount))
	print("Transmisson Time: %s seconds" % (endTime - startTime))
	totalPackets=int(sys.argv[1])
if __name__ == '__main__':
	Main()
