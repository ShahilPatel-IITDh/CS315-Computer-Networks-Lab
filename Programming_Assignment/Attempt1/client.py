import socket
import threading

HOST = '127.0.0.1'  # Localhost IP address
PORT = 65432  # Port number to connect to

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def receive_messages(sock):
    """
    Receives messages from the server and prints them to the console.
    """
    
    while True:
        data = sock.recv(1024).decode()
        if not data:
            break
        print(data)

with clientSocket as CS:
    # Connect to the server
    CS.connect((HOST, PORT))

    # Send the client's name to the server
    name = input('Enter your name: ')
    CS.sendall(name.encode())

    # Start a new thread to receive messages from the server
    threading.Thread(target=receive_messages, args=(CS,)).start()

    # Send messages to the server
    while True:
        message = input()
        CS.sendall(message.encode())
