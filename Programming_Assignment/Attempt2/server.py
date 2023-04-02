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

	def __init__(self, host, port, timeout=10):
		# Setup socket
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind((host, port))

		self.timeout = timeout
		self.lock = threading.Lock()
		self.activeClients = []

	def removePeer(self, peer):

		# Remove peer from active peers, lock the connection and close it
		self.lock.acquire()
		print(f'[INFO] Peer disconnected: {peer.addr}')
		self.activeClients.remove(peer)
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
			except socket.timeout:
				print(f'[INFO] Pinging {peer.addr}')
				peer.conn.sendall(b'PING')
				data = peer.conn.recv(1024)
				if not data == b'PONG':
					self.removePeer(peer)
					break

	def run(self):
		print('[NOTICE] Manager started!')

		try:
			while True:
				self.socket.listen()
				connection, address = self.socket.accept()
				connection.settimeout(10)
				self.lock.acquire()
				self.activeClients.append(peer)
				print(f'[INFO] New peer connected: {address}')
				self.lock.release()
				self.lock.acquire()
				for peer in self.activeClients:
					l = ';'.join([f"{p.addr[0]},{p.addr[1]}" for p in self.activeClients])
					connection.sendall(l.encode())
				self.lock.release()
				threading.Thread(target=self.handlePeer, args=(self.activeClients[-1],), daemon=True).start()
				
		except KeyboardInterrupt:
			print('[NOTICE] Shutting down...')
			self.socket.close()
			for peer in self.activeClients.copy():
				peer.conn.close()
				self.activeClients.remove(peer)
			exit(0)
		except Exception as e:
			self.socket.close()
			for peer in self.activeClients.copy():
				peer.conn.close()
				self.activeClients.remove(peer)
			print(f'[ERROR] {e}')
			raise

if __name__ == '__main__':
	Manager(HOST, PORT).run()