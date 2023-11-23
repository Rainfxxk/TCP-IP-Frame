import socket
from threading import Thread

from command import command_factory
from command_queue import CommandQueue
import netconfig


class Receiver:
    
    def __init__(self, connect, host, port):
        self.socket = connect
        self.host = host
        self.port = port
        self.socket_file = connect.makefile()
        
        self.command_queue = CommandQueue()


    def parse_message(self, message):
        index = message.find(':'.encode(netconfig.charset))

        # 获取指令的类型及内容
        if index == -1:
            command_type = None
            command = message
        else:
            command_type = message[0:index]
            command_type = command_type.decode(netconfig.charset)
            command = message[(index + 1):]

        return (command_type, command)
    

    def writeline(self, message):
        self.socket_file.write(message + "\n".encode(netconfig.charset))
        self.socket_file.flush()


    def readline(self):
        line = self.socket_file.readline()
        return line[0:-1]
    

    def send(self, message):
        self.socket.send(message)


    def recv(self):
        header = self.socket.recv(netconfig.package_header_size)

        data_size = int.from_bytes(header, "little")
        print(data_size)

        return self.socket.recv(data_size)
        

    def receive(self):

        while True:
            message = self.recv()

            command_type, command = self.parse_message(message)

            if command_type is None:
                continue

            # 依据正确的指令收发顺序进行
            if command_type == 'package num':

                # 1. 接受 `package num` 指令，确认数据包的数量
                package_num = int(command)
                is_successed = True
                message = b''

                print("package num : " + str(package_num))

                package = None
                # 2. 接受数据包并进行拼接
                for i in range(0, package_num):

                    package = self.recv()

                    print(str(i) + "th. package, len: " + str(len(package)))

                    # 如果提前收到finish，说明有包丢失，本次接受不成功
                    if (package == "finish"):
                        is_successed = False

                    message += package

                # 3. 接受 `finish!` 指令结束接收指令
                if is_successed:

                    finish_command = self.recv()
                    finish_command = self.parse_message(finish_command)[1]
                    print(finish_command)                
                    finish_command = finish_command.decode(netconfig.charset)

                    print("finish: " + finish_command)
                    
                    if (finish_command == 'finish!'):
                        print("接收结束")
                    else:
                        print("收到的不是finish!")
                    
                else:
                    continue
                
                # 4. 发送 `finish!!` 指令通知发送端确认接受
                self.send("finish!!\n".encode(netconfig.charset))

                command_type, command = self.parse_message(message)

            print("command_type: " + command_type)
            print(command[:100])

            # 5. 处理数据包信息
            command = command_factory(command_type, command)

            self.command_queue.add(command)
                

    
    def listen(self):
            thread = Thread(target=self.receive)
            thread.start()

            self.command_queue.listen()
