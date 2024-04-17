#Client file to connect to server
#Tyler Judt-Martine,
#CSC138

import socket
import threading

def client_in(client):
    while True:
        message = client.recv(1024).decode('ascii')
        print(message)

def client_out(client):
    while True:
        message = input('==> ')
        client.send(message.encode('ascii'))

def Main():
    host = '127.0.0.1'
    port = 5000

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    
    threadIn = threading.Thread(target=client_in, args = (client,))
    threadOut = threading.Thread(target=client_out, args = (client,))

    threadIn.start()
    threadOut.start()

if __name__ == '__main__':
    Main()
