#!/usr/bin/env python
#Import all modules from socket.
import socket
import sys
#Import router address and port.
from routerInfo import *
#Main function begins here.
def Main():
	#Creating a receiver socket object using socket() function.
	receiverSocket = socket.socket(socket.AF_INET, # Internet
	                     socket.SOCK_DGRAM) # UDP
	receiverSocket.bind((HOST,RECEIVER_PORT))
	receiverSocket.settimeout(5)
	totalPackets=int(sys.argv[1])
	packetTracker=[False]*totalPackets
	#Wait for incoming packet from router
	#Infinite loop for transmission of data packets
	while (not all(packetTracker)):
		try:
			inData, routerAddr = receiverSocket.recvfrom(BUFFER_SIZE)
			#Print the incoming data
			print "rcv " + inData
			#Slice out the sequence number
			if(inData[:3]=="pkt"):
				seq = int(inData[3:])
				packetTracker[seq]=True
		except:
			print "timeout"
			for seq in range(len(packetTracker)):
				if(not packetTracker[seq]):
					outData="NAK"+str(seq)
					print "send " + outData
					receiverSocket.sendto(outData,(HOST,ROUTER_PORT))
	receiverSocket.sendto("END",(HOST,ROUTER_PORT))
	#Close Receiver Socket
	receiverSocket.close()
if __name__ == '__main__':
	Main()
