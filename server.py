
import socket
from threading import Thread

from receiver import Receiver


class Server:
    
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(5)


    def listen(self):
        while True:
            connection, address = self.socket.accept()
            print("accept a connect( ip: "+ str(address[0]) + " port: " + str(address[1]) + ")")
            receiver = Receiver(connection, address[0], address[1])
            receiver.listen()