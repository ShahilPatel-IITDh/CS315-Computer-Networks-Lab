from socket import *
import time
from socket import timeout

clientMessage = "This is UDP client"

bytesToSend = str.encode(clientMessage)
serverAddress = ("127.0.0.1", 1200)

# Create a UDP socket at client side
UDPClientSocket = socket(AF_INET, SOCK_DGRAM)
UDPClientSocket.settimeout(1)
 
# Send to server using created UDP socket
for i in range(10):
	messageToSend = f'Ping {i + 1} {time.ctime()}'
	currTime = time.time()
	messageToSend = messageToSend.encode()
	UDPClientSocket.sendto(messageToSend, serverAddress)

	try:
		clientMessage, clientAddress = UDPClientSocket.recvfrom(1024)
	except timeout:
		print(f'# {i + 1} Request Timed Out')
		continue

	endTime = time.time()
	RTT = endTime-currTime
	print(f'# {i +1} RTT: {RTT*1000} milli seconds', end="  ")
	print(clientMessage.decode())