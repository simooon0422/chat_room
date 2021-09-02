import socket
import threading
from time import sleep

# Connection Data
host = '127.0.0.1'
port = 8081

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients, Their Nicknames And Their Messages
clients = []
nicknames = []
messages = []


# Sending Messages To All Connected Clients
def broadcast():
    while True:
        # while messages:
        #     message = messages.pop(0)
        #     for client in clients:
        #         client.send(message)
        # sleep(0.1)

        # count = len(messages)
        # for client in clients:
        #     for i in range(count):
        #         client.send(messages[i])
        # for i in range(count):
        #     messages.pop(0)
        # if count == 0:
        #    sleep(0.1)

        if messages:
            print(f'List: {messages}')
            message = messages.pop(0)
            print(f'Message: {message}')
            for client in clients:
                client.send(message)
            # sleep(0.01)
        else:
            sleep(0.1)


# Handling Messages From Clients
def handle(client):
    # Request And Store Nickname
    client.send('NICK'.encode())
    nickname = client.recv(1024).decode()
    nicknames.append(nickname)
    clients.append(client)

    # Print And Broadcast Nickname
    print(f'Nickname is {nickname}')
    messages.append(f'{nickname} joined the chat!\n'.encode())

    client.send('Connected to server!'.encode())

    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            messages.append(message+'\n')
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            messages.append(f'{nickname} left the chat!'.encode())
            nicknames.remove(nickname)
            break


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(f'Connected with {(str(address))}')

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


broadcast_thread = threading.Thread(target=broadcast)
broadcast_thread.start()

print('Server is listening ...')
receive()
