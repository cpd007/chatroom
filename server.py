import socket
import threading

host = '127.0.0.1'
port = 59000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
aliases = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            alias = aliases[index]
            print(f'Error in handling client {alias}')
            broadcast(f'{alias} has left the chat'.encode('utf-8'))
            clients.remove(client)
            aliases.remove(alias)
            client.close()
            break


def receive():
    while True:
        print('Server is running and listening.....')
        client, address = server.accept()
        print(f'connection established with {str(address)}')
        clients.append(client)
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024).decode('utf-8')
        aliases.append(alias)
        client.send('You are now connected'.encode('utf-8'))
        broadcast(f'{alias} has entered the chat'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=[client])
        thread.start()


receive()
