import socket
import threading


# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
host = '127.0.0.1'
port = 8081


# Listening to Server and Sending Nickname
def receive(client, client_nick):
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode()
            if message == 'NICK':
                client.send(client_nick.encode())
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occurred!")
            client.close()
            break


# def write():
#     while True:
#         message = f'{nickname}: {input("")}'
#         client.send(message.encode())


def chat_client(clients_number=1):
    for index in range(clients_number):
        client_nick = f'{nickname}_{str(index)}'
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        # Starting Threads For Listening And Writing
        receive_thread = threading.Thread(target=receive, args=[client, client_nick])
        receive_thread.start()

        # write_thread = threading.Thread(target=write)
        # write_thread.start()


chat_client()
