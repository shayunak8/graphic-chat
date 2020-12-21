import tkinter as tk


class Design(object):

    def __init__(self):
        self.root = tk.Tk()
        self.connectedUsersFrame = self.CreateFrame(self.root, 650, 225, '#7fb3e8', tk.LEFT)
        self.textFrame = self.CreateFrame(self.root, 100, 400, 'white', tk.BOTTOM)
        self.userNameFrame = self.CreateFrame(self.root, 50, 400, 'white', tk.TOP)
        self.chatFrame = self.CreateFrame(self.root, 500, 400, '#7fb3e8', tk.TOP)
        self.CreateLabel(self.root, 235, 10, "enter your Username: ", 10, )
        self.CreateLabel(self.root, 30, 10, "connected users:", 10)
        self.userNameEntry = self.CreateEntry(self.root, "Username entry", 410, 10, 10)
        self.userNameEntry.bind("<Button-1>", lambda event: self.userNameEntry.delete(0, tk.END))
        self.textEntry = self.CreateEntry(self.root, "add your text here", 235, 580, 15)
        self.textEntry.config(state="disabled")
        self.textEntry.bind("<Button-1>", lambda event: self.textEntry.delete(0, tk.END))
        self.connectedUsersListBox = self.CreateListBox(self.root, 12, 50, 20, 30, 9)
        self.chatListBox = self.CreateListBox(self.root, 260, 80, 30, 23, 12)
        self.sendButton = self.CreateButton(self.root, 480, 579, 15, "Send", 2, 15)
        self.sendButton.config(state="disabled")
        self.userNameButton = self.CreateButton(self.root, 551, 9, 15, "Submit", 1, 8)
        self.disconnectButton = self.CreateButton(self.root, 80, 579, 9, 'disconnect', 1, 10)

    def CreateFrame(self, root, FrameHeight, frameWidth, frameColor, frameSide):
        frame = tk.Frame(root, height=FrameHeight, width=frameWidth, background=frameColor, borderwidth=4,
                         relief='ridge')
        frame.pack(side=frameSide)
        return frame

    def CreateLabel(self, root, labelX, labelY, labelText, labelSize):
        label = tk.Label(root, text=labelText)
        label.pack()
        label.config(font=("Courier", labelSize))
        label.place(x=labelX, y=labelY)
        return label

    def CreateEntry(self, root, entryText, entryX, entryY, fontSize):
        text = tk.StringVar()
        entry = tk.Entry(root, textvariable=text)
        entry.pack()
        text.set(entryText)
        entry.config(font=("Courier", fontSize))
        entry.place(x=entryX, y=entryY)
        return entry

    def CreateListBox(self, root, frame, listboxHeight, listboxWidth, fontSize):
        listbox = tk.Listbox(frame, width=listboxWidth, height=listboxHeight, font=("Courier", fontSize))
        listbox.pack(side="left", fill="y")
        return listbox

    def CreateButton(self, root, X, Y, FontSize, ButtonText, Height, Width):
        btn1 = tk.Button(root, text=ButtonText, command=None, height=Height, width=Width)
        btn1.pack()
        btn1.place(x=X, y=Y)
        return btn1

    def CreateListBox(self, root, placeX, placeY, lbWidth, lbHeight, fontSize):
        listboxFrame = tk.Frame(root)
        listboxFrame.place(x=placeX, y=placeY)
        lb = tk.Listbox(listboxFrame, width=lbWidth, height=lbHeight, font=("Courier", fontSize))
        lb.pack(side="right", fill="y")
        lbScrollbar = tk.Scrollbar(listboxFrame, orient="vertical", command=lb.yview)
        lbScrollbar.pack(side="right", fill="y")
        lb.config(yscrollcommand=lbScrollbar.set)
        return lb

    def CreateScrollInFrame(self):
        scrollbar = tk.Scrollbar(self.root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=self.chatFrame)

    def popupMsg(self, msg):
        popup = tk.Toplevel()
        popup.title("pay attention!!!")
        label = tk.Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        btn = tk.Button(popup, text="Okay", command=popup.destroy)
        btn.pack()
