class IBKRClient:
    def __init__(self):
        self.connected = False

    def connect(self):
        self.connected = False
        return self.connected

    def disconnect(self):
        self.connected = False

    def is_connected(self):
        return self.connected
