from time import sleep
from message_queue import MassageQueue
from sender import Sender

if __name__ == "__main__":
    sender = Sender("127.0.0.1", 2004)

    message_queue = MassageQueue(sender=sender)

    message_queue.listen()

    messages = []

    image_file = open("./1.tif", "rb")

    image = image_file.read()

    image = "a" * 100000

    image = image.encode("utf-8")

    messages.append("image:".encode() + image)
    messages.append("instruction:start".encode())
    messages.append("data:123".encode())
    messages.append("log:this is a log".encode())

    for i in range(len(messages)):
        message_queue.add(message=messages[i])