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
                print("Connection closed by server.")
                break
            print(message)
        except ConnectionError:
            print("Connection to server lost.")
            break

def quit_server(client):
    quit_message = "QUIT"
    client.send(quit_message.encode('ascii'))


def client_out(client):
	while True:
		message = input('==> ')
		command = message.split()
		if command[0] == 'QUIT':
			quit_server(client)
			#client.close()
			break
		else:
			client.send(message.encode('ascii'))

def Main():
	if (len(sys.argv) != 3):
		print("Usage: python chatclient.py <hostname> <svr_port>")
		sys.exit(1)
	host = sys.argv[1]
	port = int(sys.argv[2])

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((host, port))

    # Prompt user to enter their username
	while True:
		username_input = input("Enter JOIN followed by your username (e.g., JOIN Mike): ")
		inputSplit = username_input.split()
		if len(inputSplit) == 2 and inputSplit[0].upper() == 'JOIN':
			client.send(username_input.encode())
			break
		else:
			print("Invalid format. Please enter in the format: JOIN <username>")

	threadIn = threading.Thread(target=client_in, args=(client,))
	threadOut = threading.Thread(target=client_out, args=(client,))

	threadIn.start()
	threadOut.start()

	threadIn.join()
	threadOut.join()

	client.close()
	sys.exit(1)

if __name__ == '__main__':
    Main()

