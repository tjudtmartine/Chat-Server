#Client file to connect to server
#Tyler Judt-Martine, Nazar Potapchuk
#CSC138

import socket
import threading
import sys

def client_in(client):
    while True:
        message = client.recv(1024).decode('ascii')
        print(message)

def client_out(client):
    while True:
        message = input('==> ')
        client.send(message.encode('ascii'))

def Main():
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

if __name__ == '__main__':
    Main()
