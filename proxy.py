#CS 4390 HW4 Project
#Proxy server

from socket import *
import os
import re

#Initialize golbal buffer size
bufferSize = 10000
def proxy():

    #Initialize the port NO and the request
    request = ""
    port = 12345

    ##Server creating listening socket
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('',port))
    serverSocket.listen(1)
    print("Listening . . . ")

    #recieve the request from the browser
    while True:
        connectionSocket, addr = serverSocket.accept()
        print("Connection at " + str(addr))
        request = connectionSocket.recv(bufferSize).decode()
        break;
    
    #split the request into words and find the filename and print it
    words = request.split(" ")
    fileName = words[1]
    print("Filename: " + fileName)

    #seperate the file from the whole URL
    result = re.sub(r"^\/(\w+\.)+\w+:\d{0,5}"," ",fileName)
    print("Result: " + result)


    condition = False
    while not condition:
        fileCondition = False
        
        #Try to find the file locally before finding it on the web server
        for root, dirs, files in os.walk("C:"):
            for file in files:
                if file == os.path.basename(result):
                    fileCondition = True
        
        #If file is found locally, display it in the browser
        if fileCondition:
            result = os.path.basename(result)
            with open(result, "rb") as f:
                while True:
                    bytes_read = f.read(bufferSize)
                    if not bytes_read:
                        break;
                    connectionSocket.sendall(bytes_read)
            connectionSocket.close()
            condition = True
        #If file isnt found locally, find it on the webserver
        else:
            s = socket(AF_INET, SOCK_STREAM)
            s.connect(('csvm07.cs.bgsu.edu', 80))
            s.send(("GET http:/" + fileName + " HTTP/1.0\r\n\r\n").encode())
            with open(os.path.basename(result), "wb") as g:
                while True:
                    bytes_read = s.recv(1024)
                    if not bytes_read:
                        break
                    g.write(bytes_read)
            s.close()
    serverSocket.close()

proxy()

