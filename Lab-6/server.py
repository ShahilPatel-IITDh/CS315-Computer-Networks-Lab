import socket
import random

serverName = "Server"

# get local machine name
LocalHostName = socket.gethostname()

# create a socket object
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a public host, and a port
serverSocket.bind((LocalHostName, 12345))

# become a server socket
serverSocket.listen(1)

print(f"Server waiting for incoming connections...")

while True:
    # establish a connection
    clientSocket, SocketAddress = serverSocket.accept()

    print(f"got a connection from {SocketAddress}")

    # receive client data
    clientData = clientSocket.recv(1024).decode('utf-8')

    # extract client name and number
    client_name, client_number = clientData.split()
    client_number = int(client_number)

    # check if the number is in range
    if client_number < 1 or client_number > 100:
        break

    # generate a random number between 1 and 100
    randNum = random.randint(1, 100)

    # send a reply to the client
    reply = f"{serverName} {randNum}"
    clientSocket.sendall(reply.encode('utf-8'))

    # close the client socket
    clientSocket.close()

# close the server socket
serverSocket.close()