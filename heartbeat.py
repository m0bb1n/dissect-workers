import socket
import threading
import requests
class HeartbeatSocket(object):
    app_host='localhost'
    app_port='9998'
    def __init__(self, host, port):

        self.manager_host = host
        self.manager_port = port
        self.app_sock = self.manager_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.manager_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.manager_sock.bind((self.manager_host, self.manager_port))

        self.app_sock.setsocketopt(socket.SOL_SOCKETm socket,SO_REUSEADDR,1)
        self.app_sock.bind((self.app_host, self.app_port))

    def listenForManager(self):
        self.manager_sock.listen(5)
        while True:
            manager_client, address = self.manager_sock.accept()
            manager_client.settimeout(200)
            threading.Thread(target = self.listenToManager,args = (manager_client,address)).start()
            #self.listenToManager(manager_client,address)

            client.accept

    def listenForApp(self):
        self.app_sock.listen(5)
        while True:
            app_client, address = self.app_sock.accept()
            app_client.settimeout(100)
            threading.Thread(target = self.listenToApp, args=(app_client,address)).start()

    def listenToApp(self):
        size=1024
        while True:
            try:
                data = client.recv(size)
                if data is not None:
                    self.respondToApp("SDSDA")

    def respondToApp(self, request):
        if request == 'Success':
            pass
            #message to m
    def listenToManager(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data is not None:
                    client.send('PONG')
                else:

                    raise error('Client disconnected')
            except:
                client.close()
                return False


