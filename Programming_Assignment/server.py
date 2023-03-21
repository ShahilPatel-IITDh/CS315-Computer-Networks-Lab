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

    def handle_client(conn, addr):
        """
        Handles a client connection.
        """

        print(f'Connected by {addr}')

        # Receive the client's name
        name = conn.recv(1024).decode()
        activeClients.append((name, conn))

        # Broadcast the list of active clients to all clients
        for client_name, client_conn in activeClients:
            client_conn.sendall(f'{name} has joined. Active clients: {", ".join([n for n, _ in activeClients])}'.encode())

        # Keep receiving messages from the client
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            # Broadcast the message to all clients
            for client_name, client_conn in activeClients:
                if client_conn != conn:
                    client_conn.sendall(f'{name}: {data}'.encode())

        # Remove the client from the list of active clients
        activeClients.remove((name, conn))

        # Broadcast the updated list of active clients to all clients
        for client_name, client_conn in activeClients:
            client_conn.sendall(f'{name} has left. Active clients: {", ".join([n for n, _ in activeClients])}'.encode())

        print(f'Client {name} disconnected.')

    # Accept incoming connections
    while True:
        conn, addr =SS.accept()
        # Start a new thread to handle the client
        threading.Thread(target=handle_client, args=(conn, addr)).start()
