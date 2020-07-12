import socket
import time
from threading import Thread
import sys

ownIp = '127.0.0.1'
scanMessageTag = "<scan>"


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
            msg = ownName + " " + txt
            sendSock.send(msg.encode("utf-8"))
            time.sleep(0.1)
            sendSock.close()



class Receiver(Thread):

            def __init__(self):
                Thread.__init__(self)

            def run(self):
                # print("Receiver waits for connections.")
                while True:
                    try:
                        # receiveSock = setupReceivingSocket()
                        conn, addr = receiveSock.accept()
                        # print("Connection received.")
                    except socket.timeout:
                        # print("Still waiting for connections.")
                        continue

                    data = conn.recv(1024).decode("utf-8")
                    if not data:
                        print("Connection was closed due to empty message.")
                        conn.close()

                    if data.startswith(scanMessageTag):
                        conn.send((ownName + " " + str(ownIp) + " " + str(ownPort)).encode("utf-8"))
                    else:
                        splitMessage = data.split(" ")
                        message = ""
                        for i in range(2, len(splitMessage)):
                            message += splitMessage[i] + " "


                        print("Message from: ", splitMessage[0])
                        print("|\t", message)
                        print("\n")
                        # print("Connection closed.\n\n")

                    conn.close()


def scanForOtherClients():
    lst = []
    for port in range(50000, 50010):
        scanSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        scanSock.settimeout(0.05)

        try:
            scanSock.connect((ownIp, port))
            scanSock.send(scanMessageTag.encode("utf-8"))
            msg = scanSock.recv(1024).decode('utf-8')
            lst.append(msg)
        except:
            continue
            # print("Connection denied.")

    return lst



receiver = Receiver()
receiver.start()

clientList = scanForOtherClients()
print("Found other clients at:")
for entry in clientList:
    print(entry)
print("\n\n")

sender = Sender()
sender.start()







def setupSendingSocket():

    sendSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sendSock.settimeout(5)
    return sendSock
