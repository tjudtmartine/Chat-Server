#Chat server to handle and send messages between clients
#Tyler Judt-Martine, Nazar Potapchuk
#CSC138
#usage: python chatserver.py <svr_port>

import socket
import threading
import sys

users = {}
for i in range(1, 11):
	users[i] = None

def amountOfUsers() :
	count = 0
	for u in range(1, 11):
		if user[u] != None:
			count++
	return count

def send_out(client_socket, client_list, data):
    for client_socket in client_list:
        client_socket.send(data)
    
def client_connect(client_socket, client_list):
    while True:
        data = client_socket.recv(1024)
        send_out(client_socket, client_list, data)


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

	while True:
        	print('Server is listening on ' + host + '...')
        	client_socket, address = server.accept()
        	print(f'Connected to : {str(address)}')
        	client_list.append(client_socket)
        	thread = threading.Thread(target=client_connect, args=(client_socket, client_list))
        	thread.start()
	server.close()

if __name__ == "__main__":
    Main()


