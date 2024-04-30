#Chat server to handle and send messages between clients
#Tyler Judt-Martine, Nazar Potapchuk
#CSC138
#usage: python chatserver.py <svr_port>

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
	client_socket.send(msg.encode())
	
def sendOut(client_socket, data):
	for u in users:
		if users[u] == client_socket:
			empty = "if"
		else:
			cSock = users[u]
			cSock.send(data.encode())

def addUser(client_socket, username):
	if len(users) < 10:
		if registered(client_socket):
			msg = "You have already registered"
			client_socket.send(msg.encode())
		else:
			users[username] = client_socket
			print(username + " has registered")
			msg = username + " has joined!"
			sendOut(client_socket, msg)
	else:
		msg = "Sorry, chatroom is currently full"
		client_socket.send(msg.encode())

def listUsers(client_socket):
	if registered(client_socket):
		listOfUsers = ""
		for u in users:
			listOfUsers = listOfUsers + u + "\n"
		client_socket.send(listOfUsers.encode())
		for u in users:
			if users[u] == client_socket:
				print(u + " has requested list of users")
	else:
		registerMsg(client_socket)

def msgUser(client_socket, userTo, msg):
	if registered(client_socket):
		if userTo in users:
			clientTo_socket = users[userTo]
			for u in users:
				if users[u] == client_socket:
					output = u + ": " + msg
					clientTo_socket.send(output.encode())
					print(u + " sent " + userTo + ": " + msg)
		else:
			result = "No such user [" + userTo + "] exists"
			client_socket.send(result.encode())
	else:
		registerMsg(client_socket)

def msgRoom(client_socket, msg):
	if registered(client_socket):
		output = ""
		for u in users:
			if users[u] == client_socket:
				output = u + ": " +  msg
		for u in users:
			if users[u] != client_socket:
				sock = users[u]
				sock.send(output.encode())
			else:
				print(u + " sent everyone: " + msg)
	else:
		registerMsg(client_socket)

def quit(client_socket):
	for u in users:
		if users[u] == client_socket:
			msg = u + " has left the chatroom"
			sendOut(client_socket, msg)
			print(u + " has left the chatroom")
			users.pop(u)
			client_socket.close()
			break

def unrecognized(client_socket):
	prompt = "Unrecognized message\nPossible commands to send:\n"
	prompt = prompt + "	JOIN <username>			:join chatroom with selected username\n"
	prompt = prompt + "	LIST					:list all current users\n"
	prompt = prompt + "	MESG <username> <msg>	:send private message to selected username\n"
	prompt = prompt + "	BCST <msg>				:send message to all users\n"
	prompt = prompt + "	QUIT					:leave the chatroom\n"
	client_socket.send(prompt.encode())

def send_out(client_socket, client_list, data):
    for client_socket in client_list:
        client_socket.send(data)
    
def client_connect(client_socket, client_list):
	while True:
		data = client_socket.recv(1024)
	    #send_out(client_socket, client_list, data)
		data = data.decode()
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

def Main():
	if(len(sys.argv) != 2):
		print("Usage: python chatserver.py <svr_port>")
		sys.exit(1);

	host = '127.0.0.1'
	port = int(sys.argv[1])

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((host, port))
	server.listen()
	client_list = []

	print('Server is listening on ' + host + '...')

	while True:
        	client_socket, address = server.accept()
        	print(f'Connected to : {str(address)}')
        	#client_list.append(client_socket)
        	thread = threading.Thread(target=client_connect, args=(client_socket, client_list))
        	thread.start()
        	
	server.close()

if __name__ == "__main__":
    Main()


