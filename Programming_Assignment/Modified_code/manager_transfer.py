import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 65345

class Manager:
	class Peer:
		def __init__(self, conn, addr):
			self.conn = conn
			self.addr = addr
			self.files = []

	def __init__(self, host, port, timeout=10):
		# Setup socket
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind((host, port))

		self.timeout = timeout
		self.lock = threading.Lock()
		self.active_peers = []

	def broadcastActivePeers(self):
		self.lock.acquire()
		for peer in self.active_peers:
			l = ';'.join([f"{p.addr[0]},{p.addr[1]}" for p in self.active_peers])
			peer.conn.sendall(l.encode())
		self.lock.release()

	def registerPeer(self, peer):
		peer.conn.settimeout(10)
		self.lock.acquire()
		self.active_peers.append(peer)
		print(f'[INFO] New peer connected: {peer.addr}')
		self.lock.release()

		self.broadcastActivePeers()

	def removePeer(self, peer):

		# Remove peer from active peers, lock the connection and close it
		self.lock.acquire()
		print(f'[INFO] Peer disconnected: {peer.addr}')
		self.active_peers.remove(peer)
		self.lock.release()
		peer.conn.close()

		self.broadcastActivePeers()

	def handlePeer(self, peer):
		while True:
			try:
				data = peer.conn.recv(1024)

				if not data or data == b'CLOSE':
					self.removePeer(peer)
					break
				elif data.startswith(b'LIST_FILES'):
					files = ';'.join(peer.files)
					peer.conn.sendall(files.encode())
				elif data.startswith(b'SEND_FILE'):
					file_name = data[10:].decode()
					if file_name in peer.files:
						peer.conn.sendall(b'START_TRANSFER')
						with open(file_name, 'rb') as f:
							data = f.read(1024)
							while data:
								peer.conn.sendall(data)
								data = f.read(1024)
					else:
						peer.conn.sendall(b'FILE_NOT_FOUND')
				elif data.startswith(b'ADD_FILE'):
					file_name = data[9:].decode()
					if file_name not in peer.files:
						peer.files.append(file_name)
						peer.conn.sendall(b'FILE_ADDED')
					else:
						peer.conn.sendall(b'FILE_ALREADY_ADDED')
				elif data.startswith(b'REMOVE_FILE'):
					file_name = data[12:].decode()
					if file_name in peer.files:
						peer.files.remove(file_name)
						peer.conn.sendall(b'FILE_REMOVED')
					else:
						peer.conn.sendall(b'FILE_NOT_FOUND')
			except socket.timeout:
				print(f'[INFO] Pinging {peer.addr}')
				peer.conn.sendall(b'PING')
				data = peer.conn.recv(1024)
				if not data == b'PONG':
					self.removePeer(peer)
					break

	def handleConnections(self):
			while True:
				self.socket.listen()
				conn, addr = self.socket.accept()

				self.registerPeer(self.Peer(conn, addr))

				threading.Thread(target=self.handlePeer, args=(self.active_peers[-1],), daemon=True).start()

	def run(self):
		print('[NOTICE] Manager started!')
		try:
			self.handleConnections()
		except KeyboardInterrupt:
			print('[NOTICE] Shutting down...')
			self.socket.close()
			for peer in self.active_peers.copy():
				peer.conn.close()
				self.active_peers.remove(peer)
			exit(0)
		except Exception as e:
			self.socket.close()
			for peer in self.active_peers.copy():
				peer.conn.close()
				self.active_peers.remove(peer)
			print(f'[ERROR] {e}')
			raise

if __name__ == '__main__':
	Manager(HOST, PORT).run()