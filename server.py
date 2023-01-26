import socket,threading


def accept_conn():
    while 1:
        client,addr=server.accept()
        client.send(bytes("Hello!!, Enter your name and press Enter!","utf8"))
        addresses[client]=addr
        threading.Thread(target=handle_client,args=(client,)).start()


def handle_client(client):
    name=client.recv(BUFFER_SIZE).decode("utf8")
    welcome='Welcome %s! If you ever want to quit,type {quit} to exit.'%name
    client.send(bytes(welcome,"utf8"))
    text="%s has joined the chat"%name
    broadcast(bytes(text,"utf8"))
    clients[client]=name
    while 1:
        msg=client.recv(BUFFER_SIZE)
        if msg!=bytes("{quit}","utf8"):
            broadcast(msg,name+":")
        else:
            client.send(bytes("{quit}","utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat"%name,"utf8"))
            break


def broadcast(text,n=""):
    for sock in clients:
        sock.send(bytes(n,"utf8")+text)



clients={}
addresses={}

HOST=socket.gethostname()
PORT=47177
BUFFER_SIZE=1024
ADDR=(HOST,PORT)

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)
server.listen(3)
accept_thread=threading.Thread(target=accept_conn)
accept_thread.start()
accept_thread.join()
server.close()