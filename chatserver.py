#Chat server to handle and send messages between clients
#Tyler Judt-Martine,
#CSC138

import socket
import threading
import sys

users = {}

def registered(client_socket):
    result = False
    for u in users:
        if users[u] == client_socket:
            result = True
            break
    return result

def registerMsg(client_socket):
    msg = "You must first register via \"JOIN <username>\" in order to use the chatroom and its functions"
    client_socket.send(msg.encode('ascii'))

def addUser(client_socket, username):
    if len(users) < 10:
        if registered(client_socket):
            msg = "You have already registered"
            client_socket.send(msg.encode('ascii'))
        else:
            users[username] = client_socket
            print(username + " has registered")
    else:
        msg = "Sorry, chatroom is currently full"
        client_socket.send(msg.encode('ascii'))

def listUsers(client_socket):
    if registered(client_socket):
        listOfUsers = ""
        for u in users:
            listOfUsers = listOfUsers + u + "\n"
        client_socket.send(listOfUsers.encode('ascii'))
    else:
        registerMsg(client_socket)

def msgUser(client_socket, userTo, msg):
    if registered(client_socket):
        if userTo in users:
            clientTo_socket = users[userTo]
            clientTo_socket.send(msg.encode('ascii'))
        else:
            result = "No such user [" + useranme + "] exists"
            client_socket.send(result.encode('ascii'))
    else:
        registerMsg(client_socket)

def msgRoom(client_socket, msg):
    if registered(client_socket):
        for u in users:
            if users[u] != client_socket:
                sock = users[u]
                sock.send(msg.encode('ascii'))
    else:
        registerMsg(client_socket)

def quit(client_socket):
    for u in users:
        if users[u] == client_socket:
            users.pop(u)
            client_socket.close()
            break

def unrecognized(client_socket):
    prompt = "Unrecognized message\nPossible commands to send:\n"
    prompt = prompt + "    JOIN <username>            :join chatroom with selected username\n"
    prompt = prompt + "    LIST                    :list all current users\n"
    prompt = prompt + "    MESG <username> <msg>    :send private message to selected username\n"
    prompt = prompt + "    BCST <msg>                :send message to all users\n"
    prompt = prompt + "    QUIT                    :leave the chatroom\n"
    client_socket.send(prompt.encode('ascii'))

def send_out(client_socket, client_list, data):
    for client_socket in client_list:
        client_socket.send(data)

def client_connect(client_socket, client_list):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            data = data.decode('ascii')
            action = data[0:4]
            dataSplit = data.split(" ")
            if action == "JOIN" and len(dataSplit) == 2:
                addUser(client_socket, dataSplit[1])
            elif action == "LIST" and len(dataSplit) == 1:
                listUsers(client_socket)
            elif action == "MESG":
                msg = data[4 + len(dataSplit[1]) + 2:]
                msgUser(client_socket, dataSplit[1], msg)
            elif action == "BCST":
                msg = data[5:]
                msgRoom(client_socket, msg)
            elif action == "QUIT" and len(dataSplit) == 1:
                quit(client_socket)
            else:
                unrecognized(client_socket)
        except Exception as e:
            print("Error:", e)
            break

def Main():
    if(len(sys.argv) != 2):
        print("Usage: python chatserver.py <svr_port>")
        sys.exit(1)

    host = '127.0.0.1'
    port = int(sys.argv[1])

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    client_list = []

    while True:
        print('Server is listening on ' + host + '...')
        client_socket, address = server.accept()
        print(f'Connected to : {str(address)}')
        thread = threading.Thread(target=client_connect, args=(client_socket, client_list))
        thread.start()
        client_list.append(client_socket)

    server.close()

if __name__ == "__main__":
    Main()
