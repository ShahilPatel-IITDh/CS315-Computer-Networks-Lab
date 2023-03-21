import socket
import threading
import hashlib
import os

# Initialize variables
HOST = 'localhost'
PORT = 5000
BUFSIZ = 1024
SHARE_DIR = './shared_files'
clients = {}
shared_files = []

# Define a function to get sha256 hash of a file
def get_file_hash(file_path):
    with open(file_path, 'rb') as f:
        file_contents = f.read()
        return hashlib.sha256(file_contents).hexdigest()

# Define a function to update the list of active clients
def update_clients():
    while True:
        client_list = []
        for client in clients:
            if clients[client]['status']:
                client_list.append(client)
        for client in clients:
            try:
                clients[client]['socket'].send(str(client_list).encode())
            except:
                del clients[client]
                print(f"Connection to {client} lost.")
        time.sleep(5)

# Define a function to handle a new client
def handle_client(conn, addr):
    print(f"New client connected: {addr}")
    clients[addr] = {'socket': conn, 'status': True}

    # Handle client's requests
    while True:
        try:
            data = conn.recv(BUFSIZ).decode()
            if not data:
                raise Exception("Client disconnected.")
            elif data == "list":
                # Send list of shared files
                conn.send(str(shared_files).encode())
            elif data.startswith("download"):
                # Fetch file from available clients
                file_name = data.split(" ")[1]
                file_hash = data.split(" ")[2]
                file_size = int(data.split(" ")[3])
                fragments = []
                for client in clients:
                    if clients[client]['status']:
                        try:
                            clients[client]['socket'].send(f"check {file_hash}".encode())
                            response = clients[client]['socket'].recv(BUFSIZ).decode()
                            if response == "yes":
                                fragments.append(client)
                        except:
                            clients[client]['status'] = False
                            print(f"Connection to {client} lost.")