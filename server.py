import socket
import os.path
import time
import sys
import urllib.parse

class Request:
    def __init__(self,querySting):
        self.queryString=queryString
        self.data={}
        splits=queryString.split("&")
        for  x in splits:
            y=x.split("=")
            self.data[y[0]]=urllib.parse.unquote_plus(y[1])

    def get(self,name):
        if name in self.data==False:return" "
        return self.data[name]

class Response:
    def __init__(self,clientSocket):
        self.contentType="text/html"
        self.clientSocket=clientSocket
        self.closed=False
        self.headerSent=False

    def write(self,data):
        if self.closed==True: return
        if self.headerSent==False:
            header = "HTTP/1.1 200 OK\n"
            header += f"Content-Type: {self.contentType}\n"
            header += "\n"
            cc.sendall(bytes(header, encoding="utf-8"))
            self.headerSent=True
        self.clientSocket.sendall(bytes(data,encoding="utf-8"))

    def close(self):
        if self.closed==False:
            self.clientSocket.close()
            self.closed=True


def getMIMEType(file):
    return "text/html"

sys.path.append("private")
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("localhost", 5050))
serverSocket.listen()
while True:
    print("HTTP Server is ready to accept requests on port 5050...")

    cc, ss = serverSocket.accept()
    a = cc.recv(5000)
    b = a.decode(encoding="utf-8")
    print("*" * 50)
    print(b)
    print("*" * 50)

    lines = b.split("\n")
    firstline = lines[0]
    words = firstline.split(" ")

    if len(words) < 2:
        continue

    requestURL = words[1]
    print(f"Request URL is {requestURL}")

    if requestURL=="/close":
        header="HTTP/1.1 404 Not Found\n\n"
        cc.sendall(bytes(header,encoding="utf-8"))
        cc.close()
        break
        
    file=""   
    queryString=""
    requestMethodType=words[0]
    isPYResourse=False
    if requestURL == "/":
        if os.path.exists("index.html"):
            file = "index.html"
        elif os.path.exists("index.htm"):
            file = "index.htm"
    else:
        file=requestURL[1:] 
        if file.startswith("private/"):
            header="HTTP/1.1 404 Not Found\n\n"
            cc.sendall(bytes(header,encoding="utf-8"))
            cc.close()
            continue 

        if requestMethodType=='GET':
            questionMarkIndex=file.find("?")
            if questionMarkIndex!=-1:
                queryString=file[questionMarkIndex+1:]
                print(queryString)
                file=file[0:questionMarkIndex]
        if requestMethodType=='POST':
            queryString=lines[len(lines)-1]

        if file.find(".")==-1:
            isPYResourse=True
        if isPYResourse==False and(not os.path.exists(file)):
            file = ""

    if isPYResourse==False and file=="":
        header="HTTP/1.1 404 Not Found\n\n"
        cc.sendall(bytes(header,encoding="utf-8"))
        cc.close()
        continue
    if isPYResourse==True:
        if not os.path.exists("private/"+file+".py"):
             header="HTTP/1.1 404 Not Found\n\n"
             cc.sendall(bytes(header,encoding="utf-8"))
             cc.close()
             continue 
        request=Request(queryString)
        response=Response(cc)
        pyResourse=__import__(file)
        pyResourse.processRequest(request,response)
        response.close()
        continue
    f=open(file,"rb")
    data=f.read()
    responseLength=len(data)
    f.close()

    header = "HTTP/1.1 200 OK\n"
    header += f"Content-Type: {getMIMEType(file)}\n"
    header += f"Content-Length: {responseLength}\n"
    header += "\n"
     
    cc.sendall(bytes(header, encoding="utf-8"))
    cc.sendall(data)
    cc.close()
serverSocket.close()
time.sleep(3)
print("Server is down")
    
