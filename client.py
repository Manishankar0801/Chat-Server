from concurrent.futures import thread
import socket
from _thread import *
import threading
from matplotlib import use

ClientMultiSocket = socket.socket()
# host = '127.0.0.1'
# port = 2004
host = input("Please enter the server's IP address: ")
port = int(input("Please enter the port: "))

print('Waiting for connection response')

try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))
res = ClientMultiSocket.recv(1024)
userId = res.decode('utf-8').split()[-1]
print("server :", res.decode('utf-8'))
def listenToServer():
    while True:
        res = ClientMultiSocket.recv(1024)
        msg = res.decode('utf-8')
        if len(msg) > 0:
            if msg == "closed":
                quit()
            print(msg)


def getUserInput():
    while True:
        userInput = input()
        splitData = userInput.split()
        if splitData[0] == "/dm" or splitData[0] == "/bc":
            msg = userInput.split('"')[1]
            print(f"{userId}: {msg}")
        if userInput == "/help":
            print(f"Commands: \n\
            Direct Message:/dm <to_user_id> \"<message_to_be_sent>\"\n \
            Broadcast Message: /bc \"<message_to_be_broadcasted>\"\n \
            Quit: /quit\n")
        else:
            ClientMultiSocket.send(str.encode(userInput))

# start_new_thread(listenToServer, (ClientMultiSocket, ))
thread1 = threading.Thread(target=listenToServer)
thread1.start()

thread2 = threading.Thread(target=getUserInput)
thread2.start()
# ClientMultiSocket.close()