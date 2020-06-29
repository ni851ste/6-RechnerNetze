import base64, socket, time, datetime


HOST = ("asmtp.htwg-konstanz.de", 25)
NEW_LINE = "\r\n"
USERNAME_64 = "cm5ldGlu"
PASSWORD_64 = "bnRzbW9iaWw="


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

    data = (PASSWORD_64 + NEW_LINE)
    print(data)
    sock.send(data.encode('utf-8'))

    response = sock.recv(1024).decode('utf-8')
    print(response)


    # send actual mail
    # start with FROM
    data = ("MAIL FROM: <ro851rud@htwg-konstanz.de>" + NEW_LINE)
    print(data)
    sock.send(data.encode('utf-8'))

    response = sock.recv(1024).decode('utf-8')
    print(response)

    # configure RCPT
    data = ("RCPT TO: <ni851ste@htwg-konstanz.de>" + NEW_LINE)
    print(data)
    sock.send(data.encode('utf-8'))

    response = sock.recv(1024).decode('utf-8')
    print(response)

    # start to write DATA
    data = ("DATA" + NEW_LINE)
    print(data)
    sock.send(data.encode('utf-8'))

    response = sock.recv(1024).decode('utf-8')
    print(response)

    # Email Body
    data = ("Subject: TestMail\n" +
            "Dies is eine Testmail vom " + str(datetime.datetime.now()) +
            "\n." + NEW_LINE)
    print(data)
    sock.send(data.encode('utf-8'))

    response = sock.recv(1024).decode('utf-8')
    print(response)






    sock.close()
    print("Socket closed!")


main()


