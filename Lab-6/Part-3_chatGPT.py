import socket
import os

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 8080))
server_socket.listen(1)

while True:
    client_socket, client_address = server_socket.accept()
    request = client_socket.recv(1024).decode("utf-8")
    request_lines = request.split("\r\n")
    file_requested = request_lines[0].split(" ")[1]
    if file_requested == "/":
        file_requested = "/index.html"
    file_path = os.getcwd() + file_requested
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            response = "HTTP/1.1 200 OK\r\n\r\n" + file.read().decode("utf-8")
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
    client_socket.sendall(response.encode("utf-8"))
    client_socket.close()