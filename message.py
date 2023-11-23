from netconfig import *


class Package():
    def __init__(self,content):
        self.content = content

    def make_header(self):
        length = len(self.content)
        header =  length.to_bytes(12,'little')
        return header
    
    def complete_mes(self):
        mes = self.make_header() + mes.encode(charset)
        return mes
    
    
