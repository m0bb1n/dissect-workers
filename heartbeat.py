import socket
import threading

class HeartbeatSocket(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listenForClient(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(120)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()
            client.accept
    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    client.send('PONG')
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False


