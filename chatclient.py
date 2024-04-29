#Client file to connect to server
<<<<<<< HEAD
#Tyler Judt-Martine, Nazar Potapchuk
=======
#Tyler Judt-Martine, Dylan Dumitru, Nazar Potapchuk
>>>>>>> Dylan
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

def client_out(client):
    while True:
        message = input('==> ')
        client.send(message.encode('ascii'))

def join_server(client, username):
    join_message = f"JOIN {username}"
    client.send(join_message.encode('ascii'))
    print(f"{username} joined!")

def list_users(client):
    list_message = "LIST"
    client.send(list_message.encode('ascii'))

def send_message(client, recipient, message):
    mesg_message = f"MESG {recipient} {message}"
    client.send(mesg_message.encode('ascii'))

def broadcast_message(client, message):
    bcst_message = f"BCST {message}"
    client.send(bcst_message.encode('ascii'))

def quit_server(client):
    quit_message = "QUIT"
    client.send(quit_message.encode('ascii'))

def Main():
<<<<<<< HEAD
	if (len(sys.argv) != 3):
		print("Usage: python chatclient.py <hostname> <svr_port>")
		sys.exit(1)
	host = '127.0.0.1'
	port = 8000

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((host, port))

	threadIn = threading.Thread(target=client_in, args = (client,))
	threadOut = threading.Thread(target=client_out, args = (client,))

	threadIn.start()
	threadOut.start()
=======
    if (len(sys.argv) != 3):
        print("Usage: python chatclient.py <hostname> <svr_port>")
        sys.exit(1)
    host = '127.0.0.1'
    port = 5000

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    # Prompt user to enter their username
    while True:
        username_input = input("Enter JOIN followed by your username (e.g., JOIN Mike): ").split()
        if len(username_input) == 2 and username_input[0].upper() == 'JOIN':
            username = username_input[1]
            break
        else:
            print("Invalid format. Please enter in the format: JOIN <username>")

    join_server(client, username)
    
    threadIn = threading.Thread(target=client_in, args=(client,))
    threadOut = threading.Thread(target=client_out, args=(client,))

    threadIn.start()
    threadOut.start()
    
    while True:
        #command = input("Enter command (LIST, MESG, BCST, QUIT): \n").split()
		i = input("").split()
		command = i.split()
        '''if command[0] == 'LIST':
            list_users(client)
        elif command[0] == 'MESG':
            if len(command) >= 3:
                recipient = command[1]
                message = ' '.join(command[2:])
                send_message(client, recipient, message)
            else:
                print("Invalid MESG command format. Use: MESG <recipient> <message>")
        elif command[0] == 'BCST':
            if len(command) >= 2:
                message = ' '.join(command[1:])
                broadcast_message(client, message)
            else:
                print("Invalid BCST command format. Use: BCST <message>")
		elif command == 'QUIT':
			quit_server(client)'''	
        if command[0] == 'QUIT':
            quit_server(client)
            break
        else:
        	client.send(i.encode(ascii)

    client.close()
>>>>>>> Dylan

if __name__ == '__main__':
    Main()

