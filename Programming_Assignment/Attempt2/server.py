# Write a code in python using socket programming such that the code enables client-to-client file transfer application, comprising multiple clients and a server, the server should be always ON which maintains the list of currently active peers across the network at all times. A newly arrived peer connects to the manager. The manager adds this newly arrived peer to its list of active peers and broadcasts the updated list. The manager periodically checks the availability of active peers from its list, updates the same, if some peers leaves the network and broadcast the updated list. The peer informs the manager when it leaves the network, the manager deletes this peer from the list of active peers and broadcasts the updated list. 
# A new peer is expected to know the manager's IP and port. It pings the manager and saves the list of active peers sent by the manager. It also maintains a list of shareable files, Before going offline, a peer informs the manager, To fetching a file from other peer(s), a peer: a) broadcasts its requirement to all peers (from its list of active peers) b)based on received responses, parallely fetches different fragments of the required file from available peers c) if any of transmitting peers go offline, the requesting peer fetches its missing fragments from the remaining available peers (v) On being requested to share a file by another peer, a peer: a)informs the requesting peer of its availabilityb) transmits the requested fragment(s)1 of one of its shareable files 

import socket
import threading

# define the manager IP and port
MANAGER_IP = '127.0.0.1'
MANAGER_PORT = 8000

# define the maximum message length
MAX_MESSAGE_LENGTH = 4096

# define the list of active peers
active_peers = []

# function to send a message to a specific socket
def send_message(socket, message):
    socket.sendall(message.encode())

# function to broadcast a message to all active peers
def broadcast_message(message):
    for peer in active_peers:
        send_message(peer['socket'], message)

# function to handle a new client connection
def handle_client_connection(client_socket, client_address):
    try:
        # receive the client's shared files list
        shared_files_message = client_socket.recv(MAX_MESSAGE_LENGTH).decode()
        shared_files = shared_files_message.split(',')

        # add the client to the list of active peers
        active_peers.append({
            'socket': client_socket,
            'address': client_address,
            'shared_files': shared_files
        })

        # broadcast the updated list of active peers
        broadcast_message(f"Active peers: {[peer['address'] for peer in active_peers]}")

        # continuously receive messages from the client
        while True:
            message = client_socket.recv(MAX_MESSAGE_LENGTH).decode()

            # handle client leaving the network
            if message == "LEAVE":
                active_peers.remove({
                    'socket': client_socket,
                    'address': client_address,
                    'shared_files': shared_files
                })
                # broadcast the updated list of active peers
                broadcast_message(f"Active peers: {[peer['address'] for peer in active_peers]}")
                break

    except ConnectionResetError:
        pass

    finally:
        # handle client leaving the network
        active_peers.remove({
            'socket': client_socket,
            'address': client_address,
            'shared_files': shared_files
        })
        # broadcast the updated list of active peers
        broadcast_message(f"Active peers: {[peer['address'] for peer in active_peers]}")
        client_socket.close()

# function to handle the manager's incoming connections
def handle_manager_connections(manager_socket):
    while True:
        client_socket, client_address = manager_socket.accept()
        client_thread = threading.Thread(target=handle_client_connection, args=(client_socket, client_address))
        client_thread.start()

# function to check the availability of active peers
def check_active_peers():
    while True:
        for peer in active_peers:
            try:
                send_message(peer['socket'], "PING")
                peer['socket'].recv(MAX_MESSAGE_LENGTH)
            except ConnectionResetError:
                active_peers.remove(peer)
        # broadcast
        broadcast_message(f"Active peers: {[peer['address'] for peer in active_peers]}")

if __name__ == '__main__':
    # create a manager socket and bind it to the manager IP and port
    manager_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    manager_socket.bind((MANAGER_IP, MANAGER_PORT))
    manager_socket.listen()

    # create a thread to handle incoming connections from peers
    manager_thread = threading.Thread(target=handle_manager_connections, args=(manager_socket,))
    manager_thread.start()

    # create a thread to check the availability of active peers
    check_thread = threading.Thread(target=check_active_peers)
    check_thread.start()
