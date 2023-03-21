import socket
import threading
import hashlib
import os

HOST = '127.0.0.1'
PORT = 65432

serverAddress = (HOST, PORT)

# Dictionary to store active clients
activeClients = {}

# Dictionary to store available files of clients
clientFiles = {}

# Dictionary to store requested files and their fragments
requestedFiles = {}

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# List of shareable files
shareableFile = ['file1.txt', 'file2.txt', 'file3.txt']

def send_file(clientSocket, filePath):
    # Function to send a file to a client
    with open(filePath, 'rb') as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            clientSocket.sendall(data)


def handleClient(clientSocket, clientAddress):
    # Function to handle a client connection
    print(f'New client connected: {clientAddress}')
    
    # Send server IP address and port number to client
    clientSocket.sendall(str(serverAddress).encode())
    
    # Receive client's shareable files
    clientFiles = []

    while True:
        file_name = clientSocket.recv(1024).decode()
        if not file_name:
            break
        clientFiles.append(file_name)
    
    # Add client to active clients list and store its shareable files
    activeClients[clientAddress] = clientSocket
    clientFiles[clientAddress] = clientFiles
    
    # Send active client list to all clients
    for addr, sock in activeClients.items():
        if addr != clientAddress:
            sock.sendall(str(list(activeClients.keys())).encode())
    
    # Receive file request from client
    while True:
        request = clientSocket.recv(1024).decode()
        if not request:
            break
        
        # Parse file request
        file_name, start, end = request.split(':')
        start = int(start)
        end = int(end)
        
        # Check if file is already being requested
        if file_name in requestedFiles:
            requestedFiles[file_name]['fragments'].append((start, end))
        else:
            # Store requested file and its fragments
            requestedFiles[file_name] = {
                'fragments': [(start, end)],
                'peers': []
            }
            # Broadcast file request to all clients
            for addr, sock in activeClients.items():
                if addr != clientAddress:
                    sock.sendall(request.encode())
    
    # Remove client from active clients list and remove its shareable files
    activeClients.pop(clientAddress)
    clientFiles.pop(clientAddress)
    
    # Close client socket
    clientSocket.close()
    print(f'Client disconnected: {clientAddress}')

def handleRequest(clientSocket, clientAddress, request):
    # Function to handle a file request from a client
    # Parse file request
    file_name, start, end = request.split(':')
    start = int(start)
    end = int(end)
    
    # Check if file is available in client's shareable files
    if file_name in shareableFile:
        filePath = os.path.join(os.getcwd(), file_name)
        file_size = os.path.getsize(filePath)
        
        # Check if requested file fragment is within file size
        if start >= 0 and end < file_size:
            # Send file fragment to requesting client
            clientSocket.sendall(f'{file_name}:{start}:{end}:'.encode())
            send_file(clientSocket, filePath)
    
    # Close client socket
    clientSocket.close()


def receive_messages(sock):

    while True:
        data = sock.recv(1024).decode()
        if not data:
            break
        print (data)


clientSocket.connect((HOST, PORT))
name = input('Enter client name: ')
clientSocket.sendall(name.encode())
threading.Thread(target=receive_messages, args=(clientSocket,)).start()

while True:
    message = input()
    clientSocket.sendall(message.encode())
                