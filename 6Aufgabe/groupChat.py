import socket
import time
from threading import Thread
import sys

ownIp = '127.0.0.1'
scanMessageTag = "<scan>"
buddyList = []



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
        global buddyList
        while True:
            txt = input("S  -> Scan for others\n"
                        "L  -> List Buddies\n"
                        "C  -> Chat to <BuddyName> <Message>\n"
                        "G  -> send <Message> to every buddy\n")

            inputComponents = txt.split(" ")

            if inputComponents[0].upper() == "S":
                buddyList = scanForOtherClients()
                print("Scanned ports and found " + str(len(buddyList)))

            elif inputComponents[0].upper() == "L":
                for buddy in buddyList:
                    print(buddy)

            elif inputComponents[0].upper() == "C":
                receiverName = inputComponents[1]
                receiverPort = 0

                for buddy in buddyList:
                    if buddy[0] == receiverName:
                        receiverPort = int(buddy[2])

                sendSock = setupSendingSocket()

                sendSock.connect((ownIp, receiverPort))
                msg = ownName + " " + txt
                sendSock.send(msg.encode("utf-8"))
                time.sleep(0.1)
                sendSock.close()

            elif inputComponents[0].upper() == "G":
                receivingPorts = []
                for buddy in buddyList:
                    receivingPorts.append(int(buddy[2]))

                for port in receivingPorts:
                    sendSock = setupSendingSocket()

                    sendSock.connect((ownIp, port))
                    # please dont mind this shitty code
                    msg = ownName + " " + "placeholder" + " " + txt
                    sendSock.send(msg.encode("utf-8"))
                    time.sleep(0.1)
                    sendSock.close()



            print("\n")




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
                        receivedScanMessage = data.split(" ")
                        buddyList.append([receivedScanMessage[1], receivedScanMessage[2], receivedScanMessage[3]])
                        # Print updated buddy List
                        print("Scan Request received and added a new buddy.")

                        conn.send((ownName + " " + str(ownIp) + " " + str(ownPort)).encode("utf-8"))
                    else:
                        splitMessage = data.split(" ")
                        message = ""
                        for i in range(3, len(splitMessage)):
                            message += splitMessage[i] + " "


                        print("┌------", splitMessage[0])
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
            scanMessage = scanMessageTag + " " + ownName + " " + str(ownIp) + " " + str(ownPort)
            scanSock.send(scanMessage.encode("utf-8"))
            msg = scanSock.recv(1024).decode('utf-8')
            lst.append(msg.split(" "))
        except:
            continue
            # print("Connection denied.")

    return lst



receiver = Receiver()
receiver.start()



sender = Sender()
sender.start()







def setupSendingSocket():

    sendSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sendSock.settimeout(5)
    return sendSock
