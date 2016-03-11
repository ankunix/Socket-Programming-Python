#!/usr/bin/env python
#Import all modules from socket.
from socket import *
#Import all modules from sys.
import sys
#Imprt all modules from random.
from random import *
#Import OptionParser modules from optparse.
from optparse import OptionParser
parser = OptionParser()
#Add a command line option for demonstrating lossless scenario
parser.add_option("-l", "--lossless", action="store_true", dest="scenario")
#Add a command line option for demonstrating lossy(packet drop) scenario
parser.add_option("-d","--drops",  action="store_false", dest="scenario")
#Parse the command line options
(options, args) = parser.parse_args()
#Import router address and port.
from routerInfo import *
#Main function begins here.
def Main():
	#This boolean value helps to decide which scenario of the algorithm to be run based on the command line options
	isLossy = not(bool(options.scenario))
	#Ankush Chauhan's Panther ID.
	PANTHER_ID1=int("002238254")
	#Fayaz Shaik's Panther ID.
	PANTHER_ID2=int("002241063")
	#Sum of last digits of both the Panther IDs.
	X=(PANTHER_ID1 % 10) + (PANTHER_ID2 % 10)
	#Creating a router socket object using socket() function.
	routerSocket = socket()
	#Bind the socket object to the router address and port, providing these values as a tuple to the bind() function.
	routerSocket.bind((HOST,PORT))
	#Listening for incoming connections.
	routerSocket.listen(0)
	print("Router Online!, waiting for receiver to connect...")
	#Router Socket blocked, until receiver connects.
	#New socket object for receiver created, and address stored.
	receiver, receiverAddr= routerSocket.accept()
	print("Receiver Connected @ " + str(receiverAddr))
	print("Waiting for sender to connect...")
	#Router Socket blocked, until sender connects, and address stored.
	#New socket object for sender created.
	sender, senderAddr= routerSocket.accept()
	print("Sender Connected @ " + str(senderAddr))
	#Infinite loop to proceed with the store-and-forward algorithm for the router.
	while True:
		#Receive data from Sender Socket
		inSender=sender.recv(BUFFER_SIZE)
		#Store the sender data and forward it to receiver.
		outReceiver=inSender
		#Check whether sender has decided to terminate the communications, using a special data value containing "end".
		if (inSender=="end"):
			#Signal the receiver to terminate further communications
			receiver.send(outReceiver)
			break
		#Print the incoming data from Sender Socket
		print(str(senderAddr) + " ==> " + inSender)
		#Randomly generate a number between [0-99] inclusive, and if that value is less than or equal to probability X, then packet is dropped and returns to begining of the loop.
		if ((isLossy) and (randint(0,99)<=10+X)):
			print "Packet Dropped!"
			continue
		#Print the outgoing data to Receiver Socket.
		print(str(receiverAddr) + " <== " + outReceiver)
		#Send data to Receiver Socket.
		receiver.send(outReceiver)
		#Receive data from Receiver Socket.
		inReceiver=receiver.recv(BUFFER_SIZE)
		#Print the incoming data from Receiver Socket.
		print(str(receiverAddr) + " ==> " + inReceiver)
		#Store the receiver data and forward it to sender.
		outSender=inReceiver
		#Print the outgoing data to Sender Socket.
		print(str(senderAddr) + " <== " + outSender)
		#Send data to Sender Socket.
		sender.send(outSender)
	#Close sender socket.
	sender.close()
	#Close receiver socket.
	receiver.close()
	#Close router socket.
	routerSocket.close()
	print "Hosts Disconnected, quiting now!"
if __name__ == '__main__':
	Main()
