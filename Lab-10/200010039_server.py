from socket import *
import random

localIP = "127.0.0.1"
localPort = 1200

messageFromServer = "This is UDP client"

bytesToSend = str.encode(messageFromServer) 

# Create a datagram socket
UDPServerSocket = socket(AF_INET, SOCK_DGRAM)
UDPServerSocket.bind(('', localPort))

print("UDP server up and listening")

while(True):
	rand = random.randint(0, 10)
	message, address = UDPServerSocket.recvfrom(1024)
	client_message = message.upper()
	
	if rand < 4:
		continue

	UDPServerSocket.sendto(client_message, address)