#!/usr/bin/env python
import time
#Import all modules from socket.
import socket
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
#This boolean value helps to decide which scenario of the algorithm to be run based on the command line options
isLossy = not(bool(options.scenario))
#Ankush Chauhan's Panther ID.
PANTHER_ID1=int("002238254")
#Fayaz Shaik's Panther ID.
PANTHER_ID2=int("002241063")
#Sum of last digits of both the Panther IDs.
X=(PANTHER_ID1 % 10) + (PANTHER_ID2 % 10)
#Creating a router socket object using socket() function.
routerSocket = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) #Internet,UDP
#Bind the socket object to the router address and port, providing these values as a tuple to the bind() function.
routerSocket.bind((HOST,ROUTER_PORT))
#Statistics
netDrop=0
netDelay=0
print("Router Online!")
def senderToReceiver(inSender):
	#Store the sender data and forward it to receiver.
	outReceiver=inSender
	#Randomly generate a number between [0-99] inclusive, and if that value is less than or equal to probability X, then packet is dropped and returns to begining of the loop.
	if ((isLossy) and (randint(0,99)<=10+X)):
		global netDrop
		netDrop+=1
		print "Packet Dropped!"
	else:
        #Calculate Delay
		delay=randint(1,10)
		print "Delaying transmission by "+str(delay)+"ms"
		time.sleep(delay/100)
		global netDelay
		netDelay+=delay
		#Print the outgoing data to Receiver Socket.
		print(str(HOST) + ", " + str(RECEIVER_PORT) + " <== " + outReceiver)
		#Send data to Receiver Socket.
		routerSocket.sendto(outReceiver,(HOST,RECEIVER_PORT))

def reciverToSender(inReceiver):
	outSender=inReceiver
	print(str(HOST) + ", " + str(SENDER_PORT) + " <== " + outSender)
	routerSocket.sendto(outSender,(HOST,SENDER_PORT))


def Main():
	#Infinite loop to proceed with the store-and-forward algorithm for the router.
	while True:
		inPacket, fromAddr = routerSocket.recvfrom(BUFFER_SIZE)
		#Check whether receiver has decided to terminate the communications, using a special data value containing "end".
		if (inPacket=="END"):
			reciverToSender(inPacket)
			routerSocket.close()
			print "Transmisson Complete, quiting now!"
			print "Total Packets dropped:" + str(netDrop)
			print "Total delay:" + str(netDelay) + "ms"

			exit(0)
		print(str(fromAddr) + " ==> " + inPacket)
		if(fromAddr[1]==SENDER_PORT):
			#Receive data from SENDER_PORT
			senderToReceiver(inPacket)
		elif(fromAddr[1]==RECEIVER_PORT):
			reciverToSender(inPacket)
if __name__ == '__main__':
	Main()
