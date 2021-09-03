import socket
import threading
import random
import string
from random import randint
from time import sleep


class ChatClient:
    def __init__(self, host, port, nickname):
        self.host = host
        self.port = port
        self.nickname = nickname
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run_client(self):
        """Starting client"""
        # Connecting To Server
        self.client.connect((self.host, self.port))
        # Starting Threads For Listening And Writing
        receive_thread = threading.Thread(target=self._receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self._write)
        write_thread.start()

        simulation_thread = threading.Thread(target=self._simulate_chat)
        simulation_thread.start()

    def _receive(self):
        """Listening to Server and Sending Nickname"""
        while True:
            try:
                # Receive Message From Server
                # If 'NICK' Send Nickname
                message = self.client.recv(1024).decode()
                if message == 'NICK':
                    self.client.send(self.nickname.encode())
                else:
                    print(message, end='')

            except:
                # Close Connection When Error
                print("An error occurred!")
                self.client.close()
                break

    def _write(self):
        """Writing messages"""
        while True:
            message = f'{self.nickname}: {input("")}'
            self.client.send(message.encode())

    def _simulate_chat(self):
        """Writing random messages"""
        while True:
            sleep(0.1)
            message = f'{self.nickname}: {self._get_random_string()}'
            self.client.send(message.encode())

    def _get_random_string(self):
        """Generating random string"""
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(randint(1, 20)))
        return str(result_str)


# ChatClient('127.0.0.1', 8081, 'nick').run_client()
def chat_client(clients_number=1):
    for index in range(clients_number):
        ChatClient('127.0.0.1', 8081, f'nick_{str(index)}').run_client()


chat_client(10)
