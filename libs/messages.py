import os

class Messages:
    def __init__(self) -> None:
        self.messages = []

    def checkMessages(self):
        with open(os.getcwd() + '/messages.txt') as f:
            line = f.readline()
            self.messages.append(line)
        
        # clear file
        open(os.getcwd() + '/messages.txt', 'w').close()