import socket
import random

# Create a string containing the server name
server_name = "Server"

# Start a TCP socket to accept connections from clients
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 12345))
server_socket.listen(1)

while True:
    # Accept a connection from a client
    conn, addr = server_socket.accept()


    # Receive the client message
    client_message = conn.recv(1024).decode()
    client_name, client_num = client_message.split()

    # Generate a random number between 1 and 100 and use it as server number
    server_num = random.randint(1, 100)

    # Display the client name, server name, client number, server number, and their sum
    print("Client Name:", client_name)
    print("Server Name:", server_name)
    print("Client Number:", client_num)
    print("Server Number:", server_num)
    print("Sum:", int(client_num) + server_num)

    # Send the server name and server number back to the client
    conn.sendall((server_name + " " + str(server_num)).encode())

    # Close the connection
    conn.close()