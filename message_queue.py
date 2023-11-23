from collections import deque
from threading import Thread
import time
from multiprocessing import Process


class MassageQueue():

    def __init__(self,message=None,sender=None):
        self.message_queue=deque()
        self.sender = sender
    
    
    def add(self,message):
        self.message_queue.append(message)
    
    def send(self):
        while True:
            if len(self.message_queue) != 0:
                print("len:" + str(len(self.message_queue)))

                message = self.message_queue.popleft()

                self.sender.send_message(message)


    def listen(self):
        print("------------------listen---------------------")
        thread = Thread(target=self.send)
        thread.start()
        print("------------------listen start--------------------")