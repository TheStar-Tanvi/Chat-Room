import socket,tkinter,threading
from tkinter import *
from socket import *
from threading import *
import json
from datetime import datetime
from tkinter import messagebox

date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
session_data = {"date": date, "session":[]}



def receive():
    while 1:
        try:
            message=client.recv(BUFFER_SIZE).decode("utf8")
            msgs_list.insert(END,message)
            session_data["session"].append(message)
        except OSError:
            break

        

def send(*args):
    message=msg.get()
    msg.set("")
    client.send(bytes(message,"utf8"))
    session_data["session"].append(message)
    if message=="{quit}":
        with open("chat_history.json", "w") as file:
            json.dump(session_data, file)
        client.close()
        root.quit()

  

# def on_closing():
#     msg.set("{quit}")
#     send()
def loadChats():
    with open("chat_history.json", "r") as file:
        chat_history = json.load(file)
    for message in chat_history["session"]:
        session_data['session'].append(message)
        msgs_list.insert(END,message)


root=Tk()
root.title('TorcAI CHAT ROOM')

menu=Menu(root)
root.config(menu=menu)


msgframe = Frame(root)
msg=StringVar()
msg.set("")
scroll_bar=Scrollbar(msgframe)
scroll_bar.pack(side=RIGHT,fill=BOTH)




msgs_list=Listbox(root,height=15,width=50,yscrollcommand=scroll_bar.set)



msgs_list.pack(side=LEFT,fill=BOTH)
msgs_list.pack()
msgframe.pack(fill=BOTH)
msgframe.pack()


nameTextArea=Entry(root,textvariable=msg,bg="black",fg="white")
nameTextArea.bind("<Return>",send)
nameTextArea.pack()

join_button=Button(root,text="Send",bg="lightgreen",fg="black",command=send)
join_button.pack()

# root.protocol("WM_DELETE_WINDOW",on_closing)



#sockets
HOST=gethostname()
PORT=47177
BUFFER_SIZE=1024
ADDR=(HOST,PORT)
client=socket(AF_INET,SOCK_STREAM)
client.connect(ADDR)
btn=Button(root,text="Load Chats",command=loadChats)
btn.pack()
result=messagebox.askyesno("Chat Room","Do you want to load previous chats?")
if result:
    loadChats()
recvThread=Thread(target=receive)
recvThread.start()


root.mainloop()