from re import T
import socket
import os
from _thread import *
ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
ThreadCount = 0
userConnectionMapping = {}

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(5)

def multi_threaded_client(connection):
    userId = "User_"+str(ThreadCount)
    connection.send(str.encode('Connected! Your User Id: '+userId+'\n'))
    userConnectionMapping[userId] = connection
    flag = False
    try:
        while True:
            data = connection.recv(2048)
            decodedData = data.decode('utf-8')
            #print(userId, "**"+decodedData+"**")
            if not data:
                break
            splitData = decodedData.split()
            if splitData[0] == "/users":
                users = list(userConnectionMapping.keys())
                usersList = f"server: Below is a list of users:\n \
                    {str(users)}"
                connection.send(str.encode(usersList))
            elif splitData[0] == "/dm":
                if splitData[1] in userConnectionMapping.keys():
                    receiverConnection = userConnectionMapping[splitData[1]]
                    dmMessage = decodedData.split('"')[1]
                    dmMessage = f"{userId}: {dmMessage}"
                    receiverConnection.send(dmMessage.encode('utf-8'))
                else:
                    msg = f"server: User {splitData[1]} is not connected to the server.\n"
                    connection.send(msg.encode('utf-8'))
            elif splitData[0] == "/bc":
                for conn in userConnectionMapping.keys():
                    if conn != userId:
                        dmMessage = decodedData.split('"')[1]
                        dmMessage = f"{userId}: {dmMessage}"
                        userConnectionMapping[conn].send(str.encode(dmMessage))
            elif splitData[0] == "/quit":
                connection.send(str.encode("closed"))
                connection.close()
                userConnectionMapping.pop(userId)
                message = f"{userId} has quit!"
                for conn in userConnectionMapping.keys():
                    userConnectionMapping[conn].send(str.encode(message))
                print(f"Connection with {userId} closed!")
                flag = True
                break
            else:
                connection.send(str.encode("server: Invalid Command!"))
        if not flag:
            connection.close()
            userConnectionMapping.pop(userId)
            message = f"Lost connection with {userId}"
            for conn in userConnectionMapping.keys():
                userConnectionMapping[conn].send(str.encode(message))
    except:
        userConnectionMapping.pop(userId)
        message = f"Server: Lost connection with {userId}"
        for conn in userConnectionMapping.keys():
            userConnectionMapping[conn].send(str.encode(message))

while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSideSocket.close()
