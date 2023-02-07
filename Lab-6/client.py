import socket
import random

clientName = "Client"

# generate a random number between 1 and 100
randomNumber = random.randint(1, 100)

# create a socket object
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
LocalHostName = socket.gethostname()

# server port
port = 12345

# connection to hostname on the port.
clientSocket.connect((LocalHostName, port))

# send a thank you message to the client.
clientSocket.sendall(f"{clientName} {randomNumber}".encode('utf-8'))

# receive data from the server
receivedData = clientSocket.recv(1024).decode('utf-8')

print(f"Received from server: {receivedData}")

# close the client socket
clientSocket.close()