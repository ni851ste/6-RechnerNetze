import socket
from threading import Thread

# Server_IP = '127.0.0.1'
Server_IP = '141.37.168.26'

openPorts = []

class TcpPortScanner(Thread):

    def __init__(self, port):
        Thread.__init__(self)
        self.port = port

    def run(self):


        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            print("Connecting to " + str(self.port))

            sock.connect((Server_IP, self.port))
            print("TCP: Connecting worked on port " + str(self.port))
            sock.send("MESSAGE".encode('utf-8'))

        except socket.timeout:
            print("Failed to connect to " + str(self.port))


class UdpPortScanner(Thread):

    def __init__(self, port):
        Thread.__init__(self)
        self.port = port

    def run(self):


        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)
            print("Connecting to " + str(self.port))

            sock.sendto("MESSAGE".encode('utf-8'), (Server_IP, self.port))
            data, addr = sock.recvfrom(1024)
            print('UDP Port ' + str(self.port) +': received message: ' + data.decode('utf-8') + ' from ', addr)

        except socket.timeout:
            print("No answer recieved " + str(self.port))



def startPortScanner(maxCount):
    openThreads = []

    for currentPort in range(1, maxCount + 1):
        openThreads.append(TcpPortScanner(currentPort))

    for thread in openThreads:
        thread.start()


    for thread in openThreads:
        thread.join()

    print("TCP Threads have joined")

    openThreads = []

    for currentPort in range(1, maxCount + 1):
        openThreads.append(UdpPortScanner(currentPort))

    for thread in openThreads:
        thread.start()

    for thread in openThreads:
        thread.join()

    print("UDP Threads have joined")








startPortScanner(50)
