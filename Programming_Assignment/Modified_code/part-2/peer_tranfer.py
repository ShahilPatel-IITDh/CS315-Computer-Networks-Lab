import os
import socket
import threading

HOST = '127.0.1.1'
PORT = 8000

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.file_list = ["file1.txt", "file2.txt", "file3.txt"] # list of shareable files

    def handle_manager(self):
        name = input('Enter peer name: ')
        while True:
            data = self.socket.recv(1024)
            if not data:
                raise Exception('Manager disconnected!')
            
            if data == b'PING':
                print('Pong!')
                self.socket.sendall(b'PONG')
                continue
            
            print('Received peer update!')
            self.peers = [(p.split(",")[0], p.split(",")[1]) for p in data.decode().split(';')]
            print('Active peers:')
            for peer in self.peers:
                print(peer)
            # handle file requests from peers
            file_request = input('Enter file name to download or type "quit" to exit: ')
            if file_request == "quit":
                self.socket.sendall(b'CLOSE')
                self.socket.close()
                print('Shutting down...')
                exit(0)
            elif file_request in self.file_list:
                print(f'Sending {file_request} to peer...')
                # get the file path and size
                file_path = os.path.join(os.getcwd(), file_request)
                file_size = os.path.getsize(file_path)
                # send the file size to the peer
                self.socket.sendall(str(file_size).encode())
                # send the file to the peer in chunks
                with open(file_path, 'rb') as f:
                    while True:
                        data = f.read(1024)
                        if not data:
                            break
                        self.socket.sendall(data)
                print(f'{file_request} sent successfully!')
            else:
                print(f'{file_request} not found in shareable files list!')

    def run(self):
        try:
            self.socket.connect((self.host, self.port))
            self.handle_manager()

        except KeyboardInterrupt:
            self.socket.sendall(b'CLOSE')
            self.socket.close()
            print('Shutting down...')
            exit(0)

        except Exception as exp:
            self.socket.sendall(b'CLOSE')
            self.socket.close()
            print(f'[ERROR] {exp}')
            raise

if __name__ == '__main__':
    Peer(HOST, PORT).run()
