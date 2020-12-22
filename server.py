from socket import *

HOST = ""
PORT = 9000
s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)

s.bind((HOST,PORT))

s.listen(5)

while True:
    c, a = s.accept()
    data = c.recv(1024).decode("utf8")
    print(data)
    c.send(bytes('HTTP/1.1 200 OK\n'.encode()))
    c.send(bytes('Content-Type: text/html\n\n'.encode()))

    file = open("index.html")
    data = file.read()
    c.send(bytes(data.encode()))

    BrowserData = c.recv(1024).decode("utf8")

    # print(BrowserData)
    # path = BrowserData[BrowserData.find("/") + 1 : BrowserData.find("HTTP") - 1]
    # print(path)
    # file = open(path)
    # data = file.read()


    file.close()
    if (c.fileno() == -1):
        break
s.close()



