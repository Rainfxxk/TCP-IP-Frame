from netconfig import *


class Package():
    def __init__(self,content):
        self.content = content

    def generate_header(self):
        length = len(self.content)
        print(length)
        header =  length.to_bytes(12,'little')
        print("data size decode: " + str(int.from_bytes(header, "little")))
        return header
    
    def get_package(self):
        package = self.generate_header() + self.content
        return package
    
    
