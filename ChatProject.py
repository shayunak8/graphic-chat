import tkinter as tk
from DesignCode import *
import socket
from threading import Thread
import pickle
from datetime import datetime


def UserNameButtonPressed(name):  # כאשר מכניסים את השם מתחילה ההתחברות לסרבר
    if designObj.userNameEntry.get() == "Username entry" or designObj.userNameEntry.get() == "":
        designObj.popupMsg("you have to enter an user name!!!")
    else:
        clientSocket.connect(('127.0.0.1', 2344))
        clientSocket.send(designObj.userNameEntry.get().encode())
        data = clientSocket.recv(1024)
        userNames = pickle.loads(data)
        GetMsgProcess = Thread(target=GetMsg, args=(userNames,))
        GetMsgProcess.start()
        PrintUserNamesConncted(userNames)
        designObj.popupMsg("submitted, you are connected!!!")
        designObj.userNameEntry.config(state="disabled")
        designObj.userNameButton.config(state="disabled")
        designObj.textEntry.config(state="normal")
        designObj.sendButton.config(state="normal")


def SendButtonPressed(message):  # שולח את ההודעה
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    if designObj.textEntry.get() == "add your text here" or designObj.textEntry.get() == "":
        designObj.popupMsg("you have to enter something!!!")
    else:
        designObj.chatListBox.insert(tk.END, (
                current_time + "ME: " + designObj.textEntry.get()))
        clientSocket.send((designObj.userNameEntry.get() + ": " + designObj.textEntry.get()).encode())


def DisconnectButtonPressed(self):  # מנתנק מהסרבר
    clientSocket.send(('DISCONNECT' + designObj.userNameEntry.get()).encode())
    designObj.popupMsg("you are disconnected")
    connected = False
    clientSocket.close()
    designObj.root.destroy()


def GetMsg(userNames):  # מקבל הודעות
    while connected:
        try:
            msg = clientSocket.recv(1024)
            if msg[:3] == '$@#':  # $@# סימן שמשתמש חדש נכנס
                designObj.connectedUsersListBox.insert(tk.END, msg[3:])  # מדפיס את השם
                userNames.append(msg[3:])
            elif msg[:10] == "DISCONNECT":
                designObj.chatListBox.insert(tk.END, (msg[10:] + " diconnected".decode()))
                designObj.connectedUsersListBox.delete(
                    userNames.index(msg[10:]))
            elif msg == "StopThisThread":
                clientSocket.close()
                break
            else:
                masg = msg.decode() + '\n'
                designObj.chatListBox.insert(tk.END, masg.encode())
        except:
            break


def PrintUserNamesConncted(userNames):  # מדפיס בצד את כל השמות של כל האנשים המחוברים
    for userName in userNames:
        if userName != designObj.userNameEntry.get():
            designObj.connectedUsersListBox.insert(tk.END, userName)


def Main():
    global connected
    connected = True
    global clientSocket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    global designObj
    designObj = Design()
    designObj.userNameButton.bind("<Button-1>", UserNameButtonPressed)
    designObj.sendButton.bind("<Button-1>", SendButtonPressed)
    designObj.disconnectButton.bind("<Button-1>", DisconnectButtonPressed)
    designObj.root.mainloop()


if __name__ == "__main__":
    Main()
