#Client file to connect to server
#Tyler Judt-Martine, Dylan Dumitru, Nazar Potapchuk
#CSC138 Chat Group Project - 04/30/2024
# usage: python client.py <hostname> <port>

import socket
import threading
import sys


#client_in function handles incoming messages from the server and prints connection error messages.
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
    client.close()

#Main function connects chat to the server.
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

	#Loop exists when user chooses to quit the chat server. Contains all need functionality for interacting with other users via the server. 
	try:
		print("To register on server please enter JOIN <username>.")
		while True:
			user_input = input('')
			input_split = user_input.split()
			if len(input_split) == 0:
				print("Please enter a command.")
				#client.send(msg.encode())
			elif input_split[0].upper() == 'LIST':
				client.send(input_split[0].upper().encode())
			elif input_split[0].upper() == 'JOIN':
				username = input_split[1]
				msg = input_split[0].upper() + ' ' + username
				client.send(msg.encode())
			elif input_split[0].upper() == 'BCST':
				print(f"{username} is sending a broadcast")
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
			else: 
				client.send(input_split[0].upper().encode('ascii'))
			
	finally:
		thread.join()
		client.close()
		sys.exit(1)

if __name__ == '__main__':
    Main()


