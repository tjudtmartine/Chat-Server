#Client file to connect to server
#Tyler Judt-Martine, Dylan Dumitru, Nazar Potapchuk
#CSC138
# usage: python client.py <hostname> <port>

import socket
import threading
import sys

def client_in(client):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message:
                print(message)
            else:
                print("Error")
                break
        except ConnectionError:
            print("Connection to server lost.")
            break

def Main():
	if (len(sys.argv) != 3):
		print("Usage: python chatclient.py <hostname> <svr_port>")
		sys.exit(1)
	host = sys.argv[1]
	port = int(sys.argv[2])

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((host, port))

	thread = threading.Thread(target=client_in, args=(client,))

	thread.start()

	try:
		print("To join server please enter JOIN <username>")
		while True:
			user_input = input("==>")
			input_split = user_input.split()
			if len(input_split) == 2 and input_split[0].upper() == 'JOIN':
				username = input_split[1]
				print(f"Welcome {username}!")
			if input_split[0].upper() == 'QUIT':
				client.send(input_split[0].upper().encode('ascii'))
				print(f"{username} left the chat!")
				break
			else:
				client.send(user_input.encode())
	finally:
		client.close()
		sys.exit(1)

if __name__ == '__main__':
    Main()

