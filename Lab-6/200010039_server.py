import socket
import random

serverName = "Server"

# get local machine name
LocalHostName = socket.gethostname()

# create a socket object
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a public host, and a port
# Arguments: (hostname <socket.gethostname>, port)
# bind accept only one argument as a tuple
serverSocket.bind((LocalHostName, 3600))

# become a server socket, maximum 1 connection
serverSocket.listen(1)

print(f"Server waiting for incoming connections...")

while True:
    # establish a connection, return a new socket object representing the connection, and the address of the client
    clientSocket, SocketAddress = serverSocket.accept()

    print(f"got a connection from {SocketAddress}")

    # receive client data, maximum 1024 bytes, decode to utf-8, and send a reply
    clientData = clientSocket.recv(1024).decode('utf-8')

    # extract client name and number, and convert number to integer
    client_name, client_number = clientData.split()
    client_number = int(client_number)

    # check if the number is in range, if not, break the loop
    if client_number < 1 or client_number > 100:
        break

    # generate a random number between 1 and 100
    randNum = random.randint(1, 100)

    # send a reply to the client, encode to utf-8
    reply = f"{serverName} {randNum}"
    clientSocket.sendall(reply.encode('utf-8'))

    print(f"Client name: {client_name}")
    print(f"Client number: {client_number}")
    print(f"Sum: {client_number + randNum}")

    # close the client socket
    clientSocket.close()

# close the server socket
serverSocket.close()