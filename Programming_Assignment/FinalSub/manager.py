import socket
import threading
import json
import time

HOST = '127.0.0.1'
PORT = 5000

class Manager:
    def __init__(self, ip, port):
        self.IP = ip
        self.PORT = port
        self.activePeers = {}
        self.lock = threading.Lock()
        self.timeInterval = 10

    def broadcastPeers(self):
        with self.lock:
            print("[NOTICE] Broadcasting active peers list")
            for (addr, peer_port), _ in self.activePeers.items():
                try:
                    SS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    SS.connect((addr, peer_port))
                    SS.sendall(json.dumps({"peers": list(self.activePeers.keys())}).encode())
                except socket.error:
                    pass
    def work(self):
        print("Testing")
        print("Active peers: {peers}").format(peers=self.activePeers)
        self.activePeers.append(self.activePeers)
    
    def insertPeer(self, addr, peer_port):
        with self.lock:
            self.activePeers[(addr, peer_port)] = peer_port
            print("[NOTICE] Added peer: {addr}:{peer_port}").format(addr=addr, peer_port=peer_port)

    def removePeer(self, addr, peer_port):
        with self.lock:
            del self.activePeers[(addr, peer_port)]
            print("[NOTICE] Removed peer: {addr}:{peer_port}").format(addr=addr, peer_port=peer_port)

    def periodicBroadcastPeer(self):
        while True:
            time.sleep(self.timeInterval)
            self.broadcastPeers()    

    def TestCodeFlow(self):
        print("HOST: {host}").format(host=HOST)
        if(HOST == '5001'):
            print("Transfering the files")

    def handleConnection(self, conn, addr):
        try:
            data = conn.recv(1024)
            if data:
                request = json.loads(data.decode())
                if request["type"] == "join":
                    self.insertPeer(addr[0], request["port"])
                elif request["type"] == "leave":
                    self.removePeer(addr[0], request["port"])
        finally:
            conn.close()

    def start(self):
        print("[NOTICE] Starting Manager...")
        broadcastThread = threading.Thread(target=self.periodicBroadcastPeer)
        broadcastThread.start()

        SS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SS.bind((self.IP, self.PORT))
        SS.listen()
        while True:
            peerSocket, peerAddr = SS.accept()
            thr = threading.Thread(target=self.handleConnection, args=(peerSocket, peerAddr))
            thr.start()


if __name__ == "__main__":
    manager = Manager(HOST, PORT)
    manager.start()
