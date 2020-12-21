import socket
from threading import Thread
import pickle
from datetime import datetime


def WaitForNewUser():
    while 1:
        clientSocket, addr = serverSocket.accept()
        userName = clientSocket.recv(1024)
        userNames.append(userName)
        userName = userName.decode()
        AddUser(clientSocket)
        SendTOAll(clientSocket, '$@#' + userName)  # $@# סימן התחברות
        data = pickle.dumps(userNames)
        clientSocket.send(data)  # כל השמות המחוברים לצאט עכשיו
        for x in oldmsg:  # שולח הודעות ישנות
            clientSocket.send(x.encode())
        print('{} connected to server!'.format(addr))


def AddUser(user):  # מפעיל ט'ריד של קבלת ושליחת הודעות
    usersSockets.append(user)
    Thread(target=GetMessage, args=(user,)).start()


def GetMessage(userSocket):  # מקבל הודעות
    connected = True
    while connected:
        try:
            msg = userSocket.recv(1024).decode()
            if 'DISCONNECT' in msg:  # אם לוחצים התנתנקות מתבצעת פעולת התנתקות בלי להקריס את הסרבר
                connected = False
                userSocket.send("StopThisThread".encode())
                DisconnectUser(userSocket)
                userNames.remove(msg.replace('DISCONNECT', ''))
                SendTOAll(userSocket, msg)
                return 3
            SendTOAll(userSocket, msg)
        except:
            pass


def SendTOAll(userThatSentMsg, msg):  # שולח את ההודעה
    with open("alltext.txt", "a") as f:
        f.write(current_time + ' ' + msg + "\r\n")
    for user in usersSockets:
        if user is not userThatSentMsg:
            user.send((current_time + ' ' + msg).encode())


def DisconnectUser(user):  # מוציא את השם מרשימת המחוברים
    usersSockets.remove(user)


def main():
    global oldmsg
    oldmsg = []
    with open("alltext.txt", "r") as f:
        oldmsg = f.readlines()
    global serverSocket
    serverSocket = socket.socket()
    serverSocket.bind(('127.0.0.1', 2344))
    serverSocket.listen(5)
    print('the server listen to port 2344')
    global now
    global current_time
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    global usersSockets
    usersSockets = []
    global userNames
    userNames = []
    Thread(target=WaitForNewUser, args=()).start()


if __name__ == '__main__':
    main()
