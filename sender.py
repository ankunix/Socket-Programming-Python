#!/usr/bin/env python
#Import all modules from socket.
from socket import *
#Import all modules from sys.
import sys
#Import router address and port.
from routerInfo import *
#Main function begins here.
def Main():
	#Creating a sender socket object using socket() function.
	senderSocket = socket()
	#Connect sender socket object with the router socket
	senderSocket.connect((HOST,PORT))
	#Set time out for retransmission, as 3 seconds.
	senderSocket.settimeout(3)
	totalPackets=int(sys.argv[1])
	retransmissionCount=0
	#Loop for the count of data packets to be transmitted, totalPackets is a count provided as a command line argument.
	for seq in range(0,totalPackets):
		#Append data packets with sequence number
		outData= "pkt" + str(seq)
		#Infinite Loop for retransmission of unacknowleged data packets
		while True:
			#Print the outgoing data to router
			print "send " + outData
			#Send data to router
			senderSocket.send(outData)
			try:
				#Wait for incoming packet till the timeout occurs
				inData = senderSocket.recv(BUFFER_SIZE)
			except:
				#Retransmission of the unacknowleged packet begins
				retransmissionCount+=1
				print "timeout"
				continue
			#If ACK received for current sequence, send the next pkt, else retransmit.
			if inData==("ACK" + str(seq)):
				break
		#Print the incoming data
		print "rcv " + inData
	#Signal the router to terminate further communications
	senderSocket.send("end")
	#Close Sender Socket
	senderSocket.close()
	print("Total packets transmitted: " + str(totalPackets))
	print("Retransmissions Occured: " + str(retransmissionCount))
if __name__ == '__main__':
	Main()
