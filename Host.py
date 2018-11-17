class Host:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = []
        self.port.append(port)

    def add_port(self, port):
        self.ports.append(port)

    def remove_port(self, port):
        self.ports.remove(port)
