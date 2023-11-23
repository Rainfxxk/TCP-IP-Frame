from abc import abstractclassmethod

import netconfig


class Command:
    def __init__(self, command):
        self.command = command

    @abstractclassmethod
    def execute(self):
        pass

# image:000000

class ImageCommand(Command):
    def __init__(self, command):
        super().__init__(command)


    def execute(self):
        print("execute a image command")

# instruction:

class InstructionCommand(Command):
    def __init__(self, command):
        super().__init__(command.decode(netconfig.charset))


    def execute(self):
        print("execute a instruction command: " + self.command)

# 

class DataCommand(Command):
    def __init__(self, command):
        super().__init__(command.decode(netconfig.charset))


    def execute(self):
        print("execute a data command: " + self.command)


class LogCommand(Command):
    def __init__(self, command):
        super().__init__(command.decode(netconfig.charset))


    def execute(self):
        print("execute a log command: " + self.command)


def command_factory(command_type, command):
    if (command_type == "image"):
        command = ImageCommand(command=command)
    elif (command_type == "instruction"):
        command = InstructionCommand(command=command)
    elif (command_type == "data"):
        command = DataCommand(command=command)
    elif (command_type == "log"):
        command = LogCommand(command=command)
    else:
        raise Exception("Receive a unexcepted command")
    
    return command