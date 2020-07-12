import socket
import time
from threading import Thread
import sys

ownIp = '127.0.0.1'


txt = input("Please specify <Name> and <Port> of your chat client!\n")
args = txt.split(" ")

if len(args) != 2:
    sys.stderr.write("Wrong number of arguments!")
    exit(-1)


ownName = args[0]
ownPort = int(args[1])

receiveSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiveSock.bind((ownIp, ownPort))
receiveSock.listen(3)
receiveSock.settimeout(20)


def setupSendingSocket():

    sendSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sendSock.settimeout(5)
    return sendSock



class Sender(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            txt = input("Type message you want to send!\n"
                        "<Port> <Message>\n")
            targetPort = int(txt.split(" ")[0])

            sendSock = setupSendingSocket()

            sendSock.connect((ownIp, targetPort))
            sendSock.send(txt.encode("utf-8"))
            time.sleep(0.1)
            sendSock.close()



class Receiver(Thread):

            def __init__(self):
                Thread.__init__(self)

            def run(self):
                print("Receiver waits for connections.")
                while True:
                    try:
                        # receiveSock = setupReceivingSocket()
                        conn, addr = receiveSock.accept()
                        print("Connection received.")
                    except socket.timeout:
                        print("Still waiting for connections.")
                        continue

                    data = conn.recv(1024)
                    if not data:
                        print("Connection was closed due to empty message.")
                        conn.close()

                    print("Received message: ", data.decode("utf-8"))
                    print("Connection closed.\n\n")
                    conn.close()




receiver = Receiver()
receiver.start()

sender = Sender()
sender.start()

# for i in args:
#     print(i)
