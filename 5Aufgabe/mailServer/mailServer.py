import base64, socket, time

HOST = ("asmtp.htwg-konstanz.de", 25)
NEW_LINE = "\r\n"
USERNAME_64 = str(base64.b64encode(("rnetin").encode('utf-8')))
PASSWORD_64 = str(base64.b64encode(("ntsmobil").encode('utf-8')))


def main():
    print("Username: " + USERNAME_64)
    print("Password: " + PASSWORD_64)


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.settimeout(10000)
    sock.setblocking(True)

    # Initial Connection
    sock.connect(HOST)
    response = sock.recv(1024).decode('utf-8')
    print(response)

    # Start Login
    data = ("AUTH LOGIN" + NEW_LINE)
    print(data)
    sock.send(data.encode('utf-8'))
    response = sock.recv(1024).decode('utf-8')
    print(response)


    # Send Base64 Username for Authentication
    data = (USERNAME_64 + NEW_LINE)
    print(data)
    sock.send(data.encode('utf-8'))

    response = sock.recv(1024).decode('utf-8')
    print(response)


    # sock.send((PASSWORD_64 + NEW_LINE).encode('utf-8'))
    # response = sock.recv(1024).decode('utf-8')
    # print(response)







    sock.close()
    print("Socket closed!")


main()


