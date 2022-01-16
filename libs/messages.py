class Messages:
    def __init__(self) -> None:
        self.messages = []

    def checkMessages(self):
        with open('messages.txt') as f:
            line = f.readline()
            self.messages.append(line)