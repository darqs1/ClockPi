import os

class Messages:
    def __init__(self) -> None:
        self.messages = []

    def checkMessages(self):
        with open(os.getcwd() + '/messages.txt') as f:
            lines = f.readlines()
            for line in lines:
                if (line!='') and (line!='\\n'):
                    self.messages.append(line)
            print("Messages:", self.messages)
        
        # clear file
        open(os.getcwd() + '/messages.txt', 'w').close()