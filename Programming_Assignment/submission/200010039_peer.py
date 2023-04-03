import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 65345

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.files = ['file1.txt', 'file2.txt', 'file3.txt']

    def handleManager(self):
        name = input('Enter peer name: ')
        while True:
            data = self.socket.recv(1024)
            if not data:
                raise Exception('Manager disconnected!')
            
            if data == b'PING':
                print('Pong!')
                self.socket.sendall(b'PONG')
                
                cmd = input('Enter a command (list, send, download, share, quit): ')
                # list the names of available files
                if cmd == 'list':
                    print('Shared files:')
                    for file in self.files:
                        print(f"- {file}")

                elif cmd == 'send':
                    filename = input('Enter filename to send: ')
                    self.sendFile(filename)

                elif cmd == 'download':
                    filename = input('Enter filename to download: ')
                    self.requestFile(filename)

                elif cmd == 'share':
                    filename = input('Enter filename to share: ')
                    self.shareFile(filename)

                elif cmd == 'quit':
                    self.socket.sendall(b'CLOSE')
                    self.socket.close()
                    print('Shutting down...')
                    exit(0)
                    
                else:
                    print('Invalid command')
                    continue
            
            print('Received peer update!')
            self.peers = [(p.split(",")[0], p.split(",")[1]) for p in data.decode().split(';')]
            # print the active peers list here
            print(self.peers)

    def sendFile(self, filename):
        if filename not in self.files:
            print(f"{filename} not shared!")
            return
        # if file present then send the file to the requesting peer
        with open(filename, 'rb') as f:
            data = f.read()
        self.socket.sendall(f"SHARE {filename},{len(data)}".encode())
        ack = self.socket.recv(1024)
        if ack == b'OK':
            self.socket.sendall(data)
            print(f"{filename} shared successfully!")
        else:
            print(f"Error sharing {filename}: {ack.decode()}")

    def requestFile(self, filename):
        threads = []
        # Request file from each peer in parallel
        for peer in self.peers:
            t = threading.Thread(target=self.fetchFile, args=(peer, filename), daemon=True)
            threads.append(t)
            t.start()
        
        # Wait for all threads to finish
        for t in threads:
            t.join()

        # Combine the file fragments and save the complete file
        with open(filename, 'wb') as f:
            for i in range(len(threads)):
                filepath = f"{filename}.part{i}"
                with open(filepath, 'rb') as part:
                    f.write(part.read())
                os.remove(filepath)
        print(f"{filename} downloaded successfully!")

    def fetchFile(self, peer, filename):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((self.host, 0))
            sock.listen()
            sock.settimeout(10)
            sock.sendall(f"GET {filename}".encode())
            data = sock.recv(1024)
            filesize = int(data.decode().split(",")[1])
            print(f"Fetching {filename} from {peer}")
            recv_bytes = 0
            with open(f"{filename}.part{peer[1]}", 'wb') as f:
                while recv_bytes < filesize:
                    data = sock.recv(1024)
                    f.write(data)
                    recv_bytes += len(data)
            sock.sendall(f"DISCONNECT {peer[1]}".encode())
            sock.close()
        except:
            print(f"Could not fetch {filename} from {peer}")
    def shareFile(self, filename):
        if filename not in self.files:
            print(f"{filename} not shared!")
            return
        
        # if file present then send the file to the requesting peer
        with open(filename, 'rb') as f:
            data = f.read()
        self.socket.sendall(f"SHARE {filename},{len(data)}".encode())
        self.socket.recv(1024)
        self.socket.sendall(data)
        print(f"{filename} shared successfully!")

    def run(self):
        try:
            self.socket.connect((self.host, self.port))
            self.handleManager()

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