import socket
import mimetypes
import time
import manageFile

class Server:
    def __init__(self, SERVER_HOST = '127.0.0.1', SERVER_PORT = 8888):
        self.SERVER_HOST = SERVER_HOST
        self.SERVER_PORT = SERVER_PORT
        self.login = False

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server.bind((self.SERVER_HOST, self.SERVER_PORT))
        server.listen(5)

        print("Listening at (%s, %s)" % (self.SERVER_HOST, self.SERVER_PORT))

        while True:
            client_connection, client_addr = server.accept()
            print("Connected by", client_addr)

            request = client_connection.recv(1024).decode()
            if request == "":
                continue
                
            self.handle_request(request, client_connection)

            client_connection.close()

        server.close()
    
    def handle_request(self, request, client_connection):
        
        headers = request.split('\n')
        # headers['Cache-Control'] = 'no-cache'
        filename = headers[0].split()[1]
        print('Filename: ', filename)
        method = headers[0].split()[0]
        print('Method: ', method)
        print('\n')

        if method == 'POST':
            if headers[-1] == 'username=1&password=1':
                filename = '/info.html'
                self.login = True

            else:
                filename = '/404.html'
                self.login = True

        # if method == 'GET':
        #     if filename[6::] != 'html':


        if self.login == False and filename != '/':
                filename = '/index.html'

        if filename == '/logout' or filename == '/back':
                self.login = False
                filename = '/index.html'
            
        if filename == '/':
                filename = '/home.html'

        # doc cac file tru files.html
        if filename[-4::] == 'html' and filename[1:-5]!='files':
            try:
                fin = open('html' + filename)

                content = fin.read()
                fin.close()

                content_type = 'text/html'
                header = 'Content-Type: ' + content_type + '\n'

                response = 'HTTP/1.1 200 OK\n' + header + content

            except FileNotFoundError:
                response = 'HTTP/1.1 404 NOT FOUND\n\nFile Not Found'
            client_connection.send(response.encode())

        elif filename[1:-5] == 'files':
                manageFile.send_files(client_connection)

        else:
            fin = open(filename[1::], 'rb')
            content = fin.read(1024)
            response_body = b''
            header = 'Transfer-Encoding: chunked\r\n'
            response = 'HTTP/1.1 200 OK\r\n' + header + 'Content-Type: text/plain'
            response_body += response.encode() + b'\r\n'
            
            while content:  # Doc lien tuc
                content_len = len(content)
                content_len_hex = hex(content_len)[2:content_len].encode()
                response_body += content_len_hex + b'\r\n' + content + b'\r\n'
                content = fin.read(1024)
            response_body += b'0\r\n\r\n'
            client_connection.sendall(response_body)
            

if __name__ == '__main__':
    server = Server()
    server.start()
