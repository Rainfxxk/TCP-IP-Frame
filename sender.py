import  socket
from package import *
import netconfig


class Sender():
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect((self.host,self.port))
        self.socket_file = self.socket.makefile("rwb")


    def writeline(self, message):
        self.socket_file.write(message + "\n".encode(netconfig.charset))
        self.socket_file.flush()


    def readline(self):
        line = self.socket_file.readline()
        return line[0:-1]
    

    def send(self, message):
        self.socket.send(message)


    def recv(self):
        return self.socket.recv(netconfig.package_size)

    '''
    836数据内容 12消息头
    '''
    def send_message(self, message):
        total_length = len(message)

        # 定义一个数据包大小为 848 bytes

        if total_length % netconfig.package_data_size:
            package_num = total_length // netconfig.package_data_size + 1
        else:
            package_num = total_length  // netconfig.package_data_size - 1 + 2

        # 如果一个数据包可以直接发送，则不需要切片
        if package_num == 1:
            self.send(Package(message).get_package())
        else:
            # 向接收端发送包的数量
            begin=f'package num:{package_num}'
            self.send(Package(begin.encode(netconfig.charset)).get_package())

            offset = 0
            while offset < total_length:
                chunk = message[offset :offset + (netconfig.package_data_size - 1)]
                self.send(Package(chunk).get_package())
                offset += len(chunk)

            # 向接收端发送结束消息
            end =f'finish!'
            print(end)
            self.send(Package(end.encode(netconfig.charset)).get_package())

            # 核实接收端的确认消息
            confirm_message = self.recv()
            confirm_message = confirm_message.decode(netconfig.charset)
            if confirm_message =='finish!!':
                pass


    def close(self):
        self.socket.close()








