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
            if not message:
                print("Connection terminated.")
                break
            else:
                print(message)
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
		print("To register on server please enter JOIN <username>.")
		while True:
			user_input = input('')
			input_split = user_input.split()
			if len(input_split) == 0:
				print("Please enter a command.")
			elif input_split[0].upper() == 'LIST':
				client.send(input_split[0].upper().encode())
			elif input_split[0].upper() == 'JOIN':
				username = input_split[1]
				msg = input_split[0].upper() + ' ' + username
				client.send(msg.encode())
				print(f"Welcome {username}!")
			elif input_split[0].upper() == 'BCST':
				double_split = user_input.split(maxsplit=1)
				msg = double_split[0].upper() + ' ' + double_split[1]
				client.send(msg.encode())
			elif input_split[0].upper() == 'MESG':
				triple_split = user_input.split(maxsplit=2)
				msg = triple_split[0].upper() + ' ' + triple_split[1] + ' ' + triple_split[2]
				client.send(msg.encode())
			elif input_split[0].upper() == 'QUIT':
				client.send(input_split[0].upper().encode('ascii'))
				print(f"{username} left the chat!")
				break
			
	finally:
		client.close()
		sys.exit(1)

if __name__ == '__main__':
    Main()

