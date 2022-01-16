import os

class Messages:
    def __init__(self) -> None:
        self.messages = []

    def checkMessages(self):
        with open(os.getcwd() + '/messages.txt') as f:
            line = f.readline()
            if line!='':
                self.messages.append(line)
            print("Messages:", self.messages)
        
        # clear file
        open(os.getcwd() + '/messages.txt', 'w').close()