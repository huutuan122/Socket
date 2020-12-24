import os
import os.path
import time
from datetime import datetime

def send_files(client_connection):
    filename = 'html/files.html'
    print(filename)
    f = open(filename, 'r', encoding = "utf-8")

    client_connection.sendall(str.encode("HTTP/1.1 200 OK\n", 'iso-8859-1'))
    client_connection.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
    # client_connection.sendall(str.encode('Transfer-Encoding: chunked\n', 'iso-8859-1'))
    
    client_connection.send(str.encode('\r\n'))

    for line in f.readlines(): #Doc tung dong trong files.html 
        client_connection.sendall(str.encode(""+line+"", 'iso-8859-1'))
        if '<tbody>' in line:   # Den <tbody> thi them download_file vao style="width:150px;height:150px;"
            for i in os.scandir("download"): # Vao duong dan
                html = '<tr><td style="text-align: center;"><a href="../download/{}" download>{}\
                        </a></td>\n<td style="text-align: center;">{}</td>\n<td style="text-align: center;">{}\
                        </td></tr>\n'.format(i.name, i.name, datetime.fromtimestamp(os.stat("download/"+i.name).st_mtime)\
                        , size_formatted(os.stat("download/"+i.name).st_size))
                #Tra len server
                client_connection.sendall(str.encode(""+html+"", 'iso-8859-1'))
            line = f.read(1024)



def size_formatted(bytes, units=[' bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']):
    return str(bytes) + units[0] if bytes < 1024 else size_formatted(bytes >> 10, units[1:])
