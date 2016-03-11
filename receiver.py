#!/usr/bin/env python
#Import all modules from socket.
from socket import *
#Import router address and port.
from routerInfo import *
#Main function begins here.
def Main():
	#Creating a receiver socket object using socket() function.
	receiverSocket = socket()
	#Connect receiver socket object with the router socket
	receiverSocket.connect((HOST,PORT))
	#Wait for incoming packet from router
	inData = receiverSocket.recv(BUFFER_SIZE)
	#Infinite loop for transmission of data packets
	while True:
		#Print the incoming data
		print "rcv " + inData
		#Slice out the sequence number
		seq = int(inData[3:])
		#Create acknowledgement data packet with sequence number appended
		outData = "ACK" + str(seq)
		#Print the acknowledgement data packet
		print "send " + outData
		#Send the acknowledgement data packet to router
		receiverSocket.send(outData)
		#Wait for incoming packet from router
		inData = receiverSocket.recv(BUFFER_SIZE)
		#Check whether sender has decided to terminate the communications, using a special data value containing "end".
		if inData=="end": break
	#Close Receiver Socket
	receiverSocket.close()
if __name__ == '__main__':
	Main()
