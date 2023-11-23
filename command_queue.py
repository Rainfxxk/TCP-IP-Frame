from threading import Thread


class CommandQueue:
    commands = []

    def add(self, command):
        self.commands.append(command)

    
    def execute(self):
        while True:
            if len(self.commands):
                command = self.commands.pop()
                
                thread = Thread(target=command.execute())
                thread.start()


    def listen(self):
        thread = Thread(target=self.execute())
        thread.start()