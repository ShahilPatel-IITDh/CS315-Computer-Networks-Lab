import socket
import threading

# define the manager IP and port
MANAGER_IP = '127.0.0.1'
MANAGER_PORT = 8000

# define the list of active peers
active_peers = []

# define the maximum message length
MAX_MESSAGE_LENGTH = 4096

# define the shared files list for the peer
shared_files = ['file1.txt', 'file2.pdf', 'file3.png']

# function to send a message to the manager
def send_message(socket, message):
    socket.sendall(message.encode())

# function to receive a message from the manager
def receive_message(socket):
    return socket.recv(MAX_MESSAGE_LENGTH).decode()

# function to fetch a file fragment from a peer
def fetch_file_fragment(fragment_index, peer_socket, file_name):
    # send the request to the peer
    send_message(peer_socket, f"FETCH,{file_name},{fragment_index}")
    # receive the fragment from the peer
    fragment = receive_message(peer_socket)
    return fragment

# function to handle the peer's incoming connections
def handle_peer_connections(peer_socket):
    while True:
        message = peer_socket.recv(MAX_MESSAGE_LENGTH).decode()
        if message == "PING":
            send_message(peer_socket, "PONG")
        elif message.startswith("FETCH"):
            parts = message.split(',')
            file_name = parts[1]
            fragment_index = int(parts[2])
            with open(file_name, 'rb') as f:
                f.seek(fragment_index * MAX_MESSAGE_LENGTH)
                fragment = f.read(MAX_MESSAGE_LENGTH)
            send_message(peer_socket, fragment.decode())

# function to broadcast a file request to all active peers
def broadcast_file_request(file_name):
    responses = []
    for peer in active_peers:
        try:
            # send the request to the peer
            send_message(peer['socket'], f"REQUEST,{file_name}")
            # receive the response from the peer
            response = receive_message(peer['socket'])
            responses.append((peer, response))
        except ConnectionResetError:
            active_peers.remove(peer)

    # select a peer to download each fragment from
    fragments = []
    for i in range(len(responses)):
        peer, response = responses[i]
        if response == "AVAILABLE":
            fragment = fetch_file_fragment(i, peer['socket'], file_name)
            fragments.append(fragment)
        else:
            print(f"{peer['address']} does not have the requested file fragment")

    # reconstruct the file from the fragments
    if len(fragments) == len(responses):
        with open(file_name, 'wb') as f:
            for fragment in fragments:
                f.write(fragment.encode())

# function to handle user input
def handle_user_input():
    while True:
        command = input("Enter command (REQUEST <file name>, SHARE <file name>, or EXIT): ")
        parts = command.split()
        if len(parts) == 2 and parts[0] == "REQUEST":
            file_name = parts[1]
            broadcast_file_request(file_name)
        elif len(parts) == 2 and parts[0] == "SHARE":
            file_name = parts[1]
            shared_files.append(file_name)
            print(f"{file_name} added to shared files list")
        elif command == "EXIT":
            send_message(manager_socket, "LEAVE")
            break
        else:
            print("Invalid command")

if __name__ == '__main__':
    # create a socket and connect to the manager
    manager_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    manager_socket.connect((MANAGER_IP, MANAGER_PORT))

    # send the shared files list to the manager
    shared_files_message = ','.join(shared_files)
    send_message(manager_socket, shared_files_message)

   
