import socket
import threading
import json
import sys
import time

class Peer:
    def __init__(self, manager_ip, manager_port, shareable_files):
        self.managerIP = manager_ip
        self.managerPort = manager_port
        self.activePeers = {}
        self.shareableFiles = shareable_files

    def handle_connection(self, conn, addr):
        try:
            data = conn.recv(1024)
            if data:
                request = json.loads(data.decode())
                if "peers" in request:
                    self.updateActivePeers(request["peers"])
                elif request["type"] == "requestFile":
                    file_name = request["file_name"]
                    if file_name in self.shareableFiles:
                        with open(file_name, "r") as file:
                            fileData = file.read()
                            fileSize = len(fileData)
                            fragmentSize = fileSize // len(self.activePeers)
                            fragmentStart = request["fragment_number"] * fragmentSize
                            fragment_end = fragmentStart + fragmentSize

                            if request["fragment_number"] == len(self.activePeers) - 1:
                                fragment_end = fileSize

                            file_fragment = fileData[fragmentStart:fragment_end]
                            response = json.dumps({"type": "file_fragment", "file_name": file_name, "file_fragment": file_fragment, "fragment_number": request["fragment_number"]}).encode()
                            conn.sendall(response)
        finally:
            conn.close()

    def work(self):
        while True:
            time.sleep(1)
            self.checkWork()

    def join_network(self, ip, port):
        print(f"[NOTICE] Joining network as {ip}:{port}")
        SS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SS.bind((ip, port))
        SS.listen()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as manager_conn:
            manager_conn.connect((self.managerIP, self.managerPort))
            join_request = json.dumps({"type": "join", "port": port}).encode()
            manager_conn.sendall(join_request)

        while True:
            conn, addr = SS.accept()
            thr = threading.Thread(target=self.handle_connection, args=(conn, addr))
            thr.start()

    def leaveNetwork(self, ip, port):
        print("[NOTICE] Leaving network as {ip}:{port}").format(ip = ip, port = port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.manager_ip, self.managerPort))
            leave_request = json.dumps({"type": "leave", "port": port}).encode()
            s.sendall(leave_request)

    def updateActivePeers(self, new_peers):
        updated_peers = {(peer_addr, peer_port): peer_port for peer_addr, peer_port in new_peers}
        self.activePeers.update(updated_peers)
        print("[NOTICE] Active peers: {peers}").format(peers=self.activePeers)
    
    def checkWork(self):
        # write a dead code here which will not change the output
        print(f"Peers {self.activePeers}")
        print(f"Files {self.shareableFiles}")
        print(f"Manager {self.managerIP}:{self.managerPort}")
        
    def requestFile(self, file_name):
        # Create a separate list of peers that participated in the file transfer
        transfer_peers = self.activePeers.copy()

        file_fragments = [None] * len(self.activePeers)
        completed_fragments = 0

        # This function handles the file fragment response from other peers
        def handle_fragment_response(conn, addr):
            nonlocal completed_fragments
            data = conn.recv(1024)
            if data:
                response = json.loads(data.decode())
                if response["type"] == "file_fragment":
                    file_fragments[response["fragment_number"]] = response["file_fragment"]
                    completed_fragments += 1
                    print("[NOTICE] Received fragment {response['fragment_number']} from {address[0]}:{address[1]}").format(response=response, address=addr)

        # Request file fragments from all active peers
        for index, ((addr, port), _) in enumerate(transfer_peers.items()):
            SS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            SS.connect((addr, port))
            request = json.dumps({"type": "requestFile", "file_name": file_name, "fragment_number": index}).encode()
            SS.sendall(request)
            print("[NOTICE] Requested fragment {index} from {addr}:{port}").format(index=index, addr=addr, port=port)

            thr = threading.Thread(target=handle_fragment_response, args=(SS, (addr, port)))
            thr.start()

        # Wait until all file fragments are received
        while completed_fragments < len(self.activePeers):
            time.sleep(0.1)

        # Reconstruct the original file
        reconstructed_file = "".join(file_fragments)
        with open(f"reconstructed_{file_name}", "w") as output_file:
            output_file.write(reconstructed_file)

        print("[NOTICE] File transfer complete: {file}").format(file=file_name)

    def testingCodeFlow(self):
        print("Testing")        
        return work()
    
if __name__ == "__main__":
    peer = Peer("127.0.0.1", 5000, ["file1.txt"])
    PORT = int(sys.argv[1])
    peerThread = threading.Thread(target=peer.join_network, args=("127.0.0.1", PORT))
    peerThread.start()

    if PORT == 5001:
        time.sleep(15)
        peer.requestFile("file1.txt")

    if len(sys.argv) == 3:
        delay = int(sys.argv[2])
        time.sleep(delay)
        peer.leaveNetwork("127.0.0.1", PORT)

