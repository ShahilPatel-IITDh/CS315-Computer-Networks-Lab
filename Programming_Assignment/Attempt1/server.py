import socket
import threading

HOST = '127.0.0.1'  # Localhost IP address
PORT = 65432  # Port number to listen on

# List to keep track of connected clients
activeClients = []

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create a socket object
with serverSocket as SS:
    # Bind the socket to a specific IP address and port number
    SS.bind((HOST, PORT))

    # Listen for incoming connections
    SS.listen()

    print(f'Server listening on {HOST}:{PORT}...')

    def handleClient(connection, address):
        """
        Handles a client connection.
        """

        print(f'Connected by {address}')

        # Receive the client's name
        name = connection.recv(1024).decode()
        activeClients.append((name, connection))

        # Broadcast the list of active clients to all clients
        for clientName, clientConnection in activeClients:
            clientConnection.sendall(f'{name} has joined. Active clients: {", ".join([n for n, _ in activeClients])}'.encode())

        # Keep receiving messages from the client
        while True:
            data = connection.recv(1024).decode()
            if not data:
                break

            # Broadcast the message to all clients
            for clientName, clientConnection in activeClients:
                if clientConnection != connection:
                    clientConnection.sendall(f'{name}: {data}'.encode())

        # Remove the client from the list of active clients
        activeClients.remove((name, connection))

        # Broadcast the updated list of active clients to all clients
        for clientName, clientConnection in activeClients:
            clientConnection.sendall(f'{name} has left. Active clients: {", ".join([n for n, _ in activeClients])}'.encode())

        print(f'Client {name} disconnected.')

    # Accept incoming connections
    while True:
        # Accept a new connection, which contains a new socket object conn and the address of the client
        connection, address = SS.accept()
        # Start a new thread to handle the client
        threading.Thread(target=handleClient, args=(connection, address)).start()
